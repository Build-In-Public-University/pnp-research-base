import unittest
from pnp_architecture.gates import run_pipeline, experiment, COSTS


class GateTests(unittest.TestCase):
    def test_real_predicates(self):
        self.assertTrue(run_pipeline({'payload': [1, 2], 'target': 3})['accepted'])
        for record in [{'payload': 'bad', 'target': 3},
                       {'payload': [True], 'target': 1},
                       {'payload': [-1, 2], 'target': 1},
                       {'payload': [1, 2], 'target': 4}]:
            self.assertFalse(run_pipeline(record)['accepted'])

    def test_prerequisites(self):
        with self.assertRaises(ValueError):
            run_pipeline({}, ('local', 'syntax', 'composition'))
        with self.assertRaises(ValueError):
            run_pipeline({}, ('syntax', 'local'))
        r = run_pipeline({'payload': 'bad', 'target': 3}, full=True)
        self.assertEqual(r['calls'], ['syntax'])

    def test_acceptance_requires_all(self):
        r = run_pipeline({'payload': [1, 2], 'target': 3})
        self.assertEqual(set(r['calls']), set(COSTS))

    def test_same_acceptance_and_cost_identity(self):
        for w in experiment()['workloads']:
            for policy in w['policies']:
                self.assertEqual([r['accepted'] for r in policy['rows']], w['oracle'])
                self.assertEqual(policy['modeled_cost'], sum(COSTS[g]*n for g,n in policy['reached'].items()))
                self.assertEqual(policy['modeled_cost'], sum(r['modeled_cost'] for r in policy['rows']))

    def test_counterexample_and_control(self):
        by = {w['name']: w for w in experiment()['workloads']}
        self.assertLess(by['local_heavy']['policies'][0]['modeled_cost'], by['local_heavy']['policies'][1]['modeled_cost'])
        self.assertGreater(by['composition_heavy']['policies'][0]['modeled_cost'], by['composition_heavy']['policies'][1]['modeled_cost'])
        self.assertEqual(by['all_valid']['policies'][0]['modeled_cost'], by['all_valid']['policies'][1]['modeled_cost'])

    def test_determinism(self):
        self.assertEqual(experiment(), experiment())

    def test_cli_fresh_and_no_overwrite(self):
        import os
        from pathlib import Path
        import subprocess
        import sys
        import tempfile
        root = Path(__file__).resolve().parents[1]
        env = dict(os.environ, PYTHONPATH=str(root / 'src'))
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / 'one.json'
            q = Path(tmp) / 'two.json'
            def run(out):
                return subprocess.run([sys.executable, str(root / 'scripts/run_gates.py'),
                                       '--output', str(out)], env=env, capture_output=True)
            self.assertEqual(run(p).returncode, 0)
            self.assertEqual(run(q).returncode, 0)
            before = p.read_bytes()
            self.assertEqual(before, q.read_bytes())
            self.assertNotEqual(run(p).returncode, 0)
            self.assertEqual(p.read_bytes(), before)


if __name__ == '__main__':
    unittest.main()
