import importlib
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


class ExperimentTests(unittest.TestCase):
    def setUp(self):
        name = 'pnp_architecture.experiments_v2'
        self.assertIsNotNone(importlib.util.find_spec(name), 'v2 executable instrument missing')
        self.m = importlib.import_module(name)

    def test_explicit_edges(self):
        expected = {
            'chain': [(0, 1), (1, 2), (2, 3)],
            'star': [(0, 1), (0, 2), (0, 3)],
            'balanced_tree': [(0, 1), (0, 2), (1, 3)],
            'complete': [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)],
            'disconnected': [(0, 1), (2, 3)],
        }
        for kind, edges in expected.items():
            self.assertEqual(self.m.edges(self.m.graph(kind, 4)), edges)
            self.assertEqual(self.m.graph(kind, 1), ((),))

    def test_graph_sizes_and_symmetry(self):
        for kind in self.m.CONFIG['topologies']:
            for n in self.m.CONFIG['network_sizes']:
                g = self.m.graph(kind, n)
                self.assertEqual(len(g), n)
                for u, neighbors in enumerate(g):
                    self.assertEqual(tuple(sorted(set(neighbors))), neighbors)
                    self.assertNotIn(u, neighbors)
                    for v in neighbors:
                        self.assertIn(u, g[v])

    def test_flood_counter_rounds_and_exactness(self):
        r = self.m.propagate(self.m.graph('chain', 4), '00000000')
        self.assertEqual((r['sends'], r['payload_bit_hops'], r['rounds'], r['delivery_rounds']), (6, 48, 4, 3))
        self.assertEqual(r['reached'], [0, 1, 2, 3])
        self.assertTrue(r['all_reached_exact'])
        r = self.m.propagate(self.m.graph('complete', 4), '0' * 16)
        self.assertEqual((r['sends'], r['rounds'], r['delivery_rounds']), (12, 2, 1))
        self.assertEqual(r['payload_bit_hops'], 192)

    def test_singleton_and_disconnected(self):
        for kind in self.m.CONFIG['topologies']:
            r = self.m.propagate(self.m.graph(kind, 1), '0')
            self.assertEqual((r['sends'], r['rounds']), (0, 0))
            self.assertTrue(r['all_reached_exact'])
        g = self.m.graph('disconnected', 8)
        r = self.m.propagate(g, '01')
        self.assertEqual(r['reached'], [0, 1, 2, 3])
        self.assertEqual(r['reached'], self.m.reachability_oracle(g))
        self.assertFalse(r['all_reached_exact'])
        self.assertEqual(r['sends'], 6)

    def test_bfs_setup_tree_and_reuse(self):
        g = self.m.graph('complete', 4)
        tree, parent, inspections = self.m.bfs_tree(g)
        self.assertEqual(tree, ((1, 2, 3), (), (), ()))
        self.assertEqual(parent, [None, 0, 0, 0])
        self.assertEqual(inspections, 12)
        r = self.m.propagate(tree, '0000')
        self.assertEqual((r['sends'], r['rounds']), (3, 1))
        r = self.m.reuse_propagation(g, '0000', 4)
        self.assertEqual(r['bfs_setup_inspections'], 12)
        self.assertEqual(r['flood']['sends'], 48)
        self.assertEqual(r['routed']['sends'], 12)
        self.assertEqual(r['routed']['payload_bit_hops'], 48)
        self.assertTrue(r['routed']['all_reached_exact'])

    def test_containing_witness_conflict_not_unsat(self):
        g = self.m.graph('chain', 4)
        r = self.m.containing(g, [0, 0, 0, 1])
        self.assertTrue(r['local_only']['all_local_valid'])
        self.assertFalse(r['local_only']['naive_global_prediction_correct'])
        self.assertEqual(r['centralized']['status'], 'reject_witness')
        self.assertTrue(r['centralized']['agrees_with_oracle'])
        self.assertEqual(r['centralized']['sends'], 6)
        self.assertEqual(r['centralized']['rounds'], 3)
        self.assertEqual(r['centralized']['equality_comparisons'], 3)
        self.assertFalse(r['oracle_global_valid'])
        self.assertEqual(r['problem_status'], 'SAT')
        self.assertEqual(self.m.containing(g, [0]*4)['centralized']['status'], 'accept_witness')
        self.assertEqual(self.m.containing(g, [0, 0, 0, 2])['centralized']['status'], 'reject_witness')

    def test_incomplete_collection_never_accepts(self):
        g = self.m.graph('disconnected', 4)
        for bits in [[0]*4, [0, 0, 0, 1]]:
            r = self.m.containing(g, bits)
            self.assertEqual(r['centralized']['status'], 'unavailable')
            self.assertEqual(r['centralized']['received'], 2)
            self.assertEqual(r['centralized']['local_inspections'], 2)
            self.assertIsNone(r['centralized']['agrees_with_oracle'])
        r = self.m.containing(self.m.graph('disconnected', 1), [1])
        self.assertTrue(r['oracle_global_valid'])
        self.assertEqual(r['centralized']['status'], 'accept_witness')

    def test_cnf_verifier_real_literals(self):
        f = [(1, -2, 3), (-1, 2, 3)]
        self.assertEqual(self.m.verify_cnf(f, 0), (True, 3))
        self.assertEqual(self.m.verify_cnf(f, 1), (False, 4))
        self.assertFalse(self.m.cnf_oracle(f, 1))
        for a in range(16):
            self.assertFalse(self.m.verify_cnf(self.m.unsat_core(), a)[0])
        self.assertEqual(len(set(self.m.unsat_core())), 8)
        self.assertEqual(self.m.verify_cnf([], 0), (True, 0))

    def test_truth_table_and_seed_identity(self):
        f = [(1, 2, 3)]
        r = self.m.exhaustive(f, 4)
        self.assertEqual(r['truth_table'], '0111111101111111')
        self.assertEqual(r['literal_inspections'], sum(r['candidate_work']))
        self.assertTrue(r['oracle_agreement'])
        self.assertEqual(self.m.random_cnf(6, 42), self.m.random_cnf(6, 42))
        self.assertNotEqual(self.m.random_cnf(6, 42), self.m.random_cnf(6, 43))
        self.assertEqual(len(self.m.random_cnf(6, 42)), 24)
        for clause in self.m.random_cnf(6, 42):
            self.assertEqual(len({abs(x) for x in clause}), 3)
            self.assertTrue(all(1 <= abs(x) <= 6 for x in clause))

    def test_scheduler_charges_entire_winning_batch(self):
        f = [(1, 2, 3)]
        serial = self.m.schedule(f, 4, 1)
        batched = self.m.schedule(f, 4, 4)
        self.assertEqual((serial['candidates'], serial['total_work'], serial['idealized_makespan']), (2, 4, 4))
        self.assertEqual((batched['candidates'], batched['total_work'], batched['idealized_makespan']), (4, 7, 3))
        self.assertEqual(batched['witness'], 1)
        self.assertTrue(batched['witness_verified'])
        self.assertEqual(batched['verification_inspections'], 1)
        r = self.m.schedule(self.m.unsat_core(), 4, 4)
        self.assertEqual(r['status'], 'UNSAT')
        self.assertEqual(r['candidates'], 16)
        self.assertEqual(r['batches'], 4)
        self.assertIsNone(r['witness'])
        full = self.m.exhaustive(self.m.unsat_core(), 4)
        self.assertEqual(r['total_work'], full['literal_inspections'])

    def test_all_grid_counter_accounting(self):
        for kind in self.m.CONFIG['topologies']:
            for n in self.m.CONFIG['network_sizes']:
                g = self.m.graph(kind, n)
                reached = self.m.reachability_oracle(g)
                tree, _, setup = self.m.bfs_tree(g)
                expected_sends = sum(len(g[u]) for u in reached)
                self.assertEqual(setup, expected_sends)
                for payload_length in self.m.CONFIG['payload_bits']:
                    flood = self.m.propagate(g, '0' * payload_length)
                    routed = self.m.propagate(tree, '0' * payload_length)
                    self.assertEqual(flood['sends'], expected_sends)
                    self.assertEqual(flood['payload_bit_hops'], expected_sends * payload_length)
                    self.assertEqual(routed['sends'], len(reached) - 1)
                    self.assertEqual(routed['payload_bit_hops'], (len(reached) - 1) * payload_length)
                    self.assertEqual(flood['reached'], reached)
                    self.assertEqual(routed['reached'], reached)
                    self.assertEqual(routed['all_reached_exact'], len(reached) == n)

    def test_frozen_protocol_drift_refused(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / 'docs').mkdir()
            (root / 'docs/protocol-v2.md').write_text('changed')
            (root / 'docs/protocol-v2.sha256').write_text('not-the-hash')
            with self.assertRaisesRegex(ValueError, 'frozen protocol hash mismatch'):
                self.m.run_suite(root)

    def test_bad_parameters(self):
        for kind, n in [('bad', 4), ('chain', 0)]:
            with self.assertRaises(ValueError):
                self.m.graph(kind, n)
        with self.assertRaises(ValueError):
            self.m.schedule([], 4, 0)
        with self.assertRaises(ValueError):
            self.m.containing(self.m.graph('chain', 2), [0])


class CliTests(unittest.TestCase):
    def test_v2_runner_determinism_and_no_overwrite(self):
        root = Path(__file__).resolve().parents[1]
        runner = root / 'scripts/run_experiments_v2.py'
        self.assertTrue(runner.is_file(), 'v2 runner missing')
        with tempfile.TemporaryDirectory() as directory:
            command = [sys.executable, str(runner)]
            outputs = []
            for index in range(2):
                out = Path(directory) / f'run{index}.json'
                summary = Path(directory) / f'run{index}.md'
                p = subprocess.run(command + ['--output', str(out), '--summary', str(summary)], capture_output=True, text=True)
                self.assertEqual(p.returncode, 0, p.stderr)
                outputs.append((out.read_bytes(), summary.read_bytes()))
            self.assertEqual(outputs[0], outputs[1])
            data = json.loads(outputs[0][0])
            self.assertEqual(len(data['propagation']), 120)
            self.assertEqual(len(data['containing_constraint']), 60)
            self.assertEqual(len(data['cnf']), 30)
            self.assertEqual(len(data['graphs']), 30)
            self.assertIn('src/pnp_architecture/experiments_v2.py', data['source_sha256'])
            self.assertIn('No real parallel hardware', outputs[0][1].decode())
            p = subprocess.run(command + ['--output', str(out), '--summary', str(summary)], capture_output=True, text=True)
            self.assertNotEqual(p.returncode, 0)
            self.assertEqual(out.read_bytes(), outputs[1][0])

    def test_legacy_module_cli_executes(self):
        with tempfile.TemporaryDirectory() as directory:
            out = Path(directory) / 'legacy.json'
            p = subprocess.run([sys.executable, '-m', 'pnp_architecture.cli', '--output', str(out)], capture_output=True, text=True)
            self.assertEqual(p.returncode, 0, p.stderr)
            self.assertTrue(out.is_file(), 'module CLI failed to execute main')
            self.assertEqual(len(json.loads(out.read_text())['rows']), 12)


if __name__ == '__main__':
    unittest.main()
