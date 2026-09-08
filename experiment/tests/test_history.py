import unittest
from pnp_architecture.history import Engine, oracle, run_cell, surface, trajectory


class HistoryTests(unittest.TestCase):
    def test_shared_and_initial_cost(self):
        e = Engine('incremental_snapshot', [0]*16)
        self.assertEqual(e.result, oracle([0]*16))
        self.assertEqual(len(e.reverse[0]), 4)
        self.assertGreater(e.initial_counters['index_write'], 0)
        self.assertGreater(sum(e.initial_counters.values()), 0)

    def test_sparse_and_dense(self):
        for k in [0, 1, 4, 16]:
            r = run_cell(16, k, 1, 'complete')
            for p in ['cold', 'incremental_snapshot', 'incremental_feed']:
                self.assertEqual(r['policies'][p]['wrong_outputs'], 0)
            for p in r['policies'].values():
                self.assertEqual(p['operations'], sum(p['counters'].values()))
                self.assertEqual(p['operations'], sum(sum(s['counters'].values()) for s in p['steps']))

    def test_hidden_mutation_not_leaked(self):
        hidden = [0]*16
        hidden[1] = 3
        snapshot = Engine('incremental_snapshot', [0]*16)
        feed = Engine('incremental_feed', [0]*16)
        unchecked = Engine('unchecked', [0]*16)
        snapshot.update(hidden, [])
        feed.update(hidden, [])
        unchecked.update(hidden, [])
        self.assertEqual(snapshot.result, oracle(hidden))
        self.assertNotEqual(feed.result, oracle(hidden))
        self.assertEqual(feed.result, unchecked.result)

    def test_equal_total_does_not_mean_equal_vector(self):
        a, b = [0]*16, [0]*16
        a[0] = 1
        b[8] = 1
        self.assertEqual(oracle(a)['total'], oracle(b)['total'])
        self.assertNotEqual(oracle(a)['values'], oracle(b)['values'])

    def test_penalties_and_eligibility(self):
        p = {'exact': {'operations': 100, 'wrong_outputs': 0},
             'unsafe': {'operations': 10, 'wrong_outputs': 2}}
        s = surface(p)
        self.assertEqual(s['rows'][0]['winners'], ['unsafe'])
        self.assertEqual(s['strict_correctness_winners'], ['exact'])
        self.assertEqual(s['break_even_penalties']['unsafe'], {'numerator': 45, 'denominator': 1})

    def test_exact_counters_and_deduplication(self):
        cold = Engine('cold', [0]*16)
        self.assertEqual(sum(cold.initial_counters.values()), 19*16+1)
        incremental = Engine('incremental_snapshot', [0]*16)
        c = incremental.update([1]*16, [(i,1) for i in range(16)])
        self.assertEqual(c['dirty_mark'], 4*16)
        self.assertEqual(c['output_write'], 16)
        c = incremental.update([1]*16, [])
        self.assertEqual(c.get('output_write', 0), 0)
        self.assertEqual(c['compare'], 16)

    def test_feed_pairing(self):
        a = run_cell(16, 4, 7, 'complete')
        b = run_cell(16, 4, 7, 'omitted')
        self.assertEqual(a['world_sha256'], b['world_sha256'])
        for name in ['cold', 'incremental_snapshot', 'unchecked']:
            self.assertEqual(a['policies'][name], b['policies'][name])
        self.assertGreater(b['policies']['incremental_feed']['wrong_outputs'], 0)

    def test_cli_replay_readback_and_overwrite(self):
        import importlib.util
        import json
        import os
        from pathlib import Path
        import subprocess
        import sys
        import tempfile
        root = Path(__file__).resolve().parents[1]
        script = root/'scripts/run_history.py'
        spec = importlib.util.spec_from_file_location('history_runner', script)
        assert spec is not None and spec.loader is not None
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        env = dict(os.environ, PYTHONPATH=str(root/'src'))
        with tempfile.TemporaryDirectory() as tmp:
            outputs = []
            for suffix in ['a','b']:
                p, s = Path(tmp)/(suffix+'.json'), Path(tmp)/(suffix+'.md')
                command = [sys.executable, str(script), '--output', str(p), '--summary', str(s)]
                result = subprocess.run(command, env=env, capture_output=True)
                self.assertEqual(result.returncode, 0, result.stderr.decode())
                self.assertEqual(module.summary(json.loads(p.read_text())), s.read_text())
                self.assertIn('Strict observed-correctness winners', s.read_text())
                outputs.append(p.read_bytes())
            self.assertEqual(*outputs)
            self.assertNotEqual(subprocess.run(command, env=env, capture_output=True).returncode, 0)
            self.assertEqual(p.read_bytes(), outputs[-1])

    def test_review_total_update_reads_writes(self):
        engine = Engine('incremental_snapshot', [0]*16)
        state = [0]*16
        state[0] = 1
        c = engine.update(state, [(0,1)])
        self.assertEqual(c['total_read'], 2*c['output_write'])
        self.assertEqual(c['total_write'], 2*c['output_write'])

    def test_delivered_and_hidden_change_share_dirty_output(self):
        engine = Engine('incremental_feed', [0]*16)
        world = [0]*16
        world[0], world[1] = 1, 3
        observed = [0]*16
        observed[0] = 1
        c = engine.update(world, [(0,1)])
        self.assertGreater(c['output_write'], 0)
        self.assertEqual(engine.result, oracle(observed))
        self.assertNotEqual(engine.result['values'][0], oracle(world)['values'][0])

    def test_wrong_import_rejected_before_execution(self):
        import os
        from pathlib import Path
        import subprocess
        import sys
        import tempfile
        root = Path(__file__).resolve().parents[1]
        with tempfile.TemporaryDirectory() as tmp:
            folder = Path(tmp)
            package = folder/'pnp_architecture'
            package.mkdir()
            (package/'__init__.py').write_text('')
            (package/'history.py').write_text("def experiment():\n    raise RuntimeError('UNEXPECTED execution')\n")
            output = folder/'out.json'
            result = subprocess.run([sys.executable, str(root/'scripts/run_history.py'),
                                     '--output', str(output), '--summary', str(folder/'out.md')],
                                    env=dict(os.environ, PYTHONPATH=str(folder)), capture_output=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn('Imported history module does not match', result.stderr.decode())
            self.assertFalse(output.exists())

    def test_replay(self):
        self.assertEqual(trajectory(16, 4, 7), trajectory(16, 4, 7))
        self.assertEqual(run_cell(16, 1, 7, 'omitted'), run_cell(16, 1, 7, 'omitted'))


if __name__ == '__main__':
    unittest.main()
