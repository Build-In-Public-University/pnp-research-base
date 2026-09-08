"""Owned observation experiment tests; run only this file during parallel work."""
import hashlib
import importlib.util
import itertools
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from collections import Counter

from pnp_architecture import observation as obs

ROOT = Path(__file__).resolve().parents[1]


class ObservationTests(unittest.TestCase):
    def test_interval_decision_nontrivial_safe_false(self):
        output, guaranteed, proof = obs.bound_decision([0, 1], 1, 'threshold', 8, Counter())
        self.assertEqual((output, guaranteed), (False, True))
        self.assertEqual(proof['sum_square_bounds'], [0, 5])

    def test_interval_exact_abstains_on_stale_zero_world(self):
        output, guaranteed, _ = obs.bound_decision([0, 0], 1, 'exact', 8, Counter())
        self.assertIsNone(output)
        self.assertFalse(guaranteed)

    def test_interval_sound_exhaustive_small_vectors(self):
        for cache in itertools.product((-8, -2, -1, 0, 1, 2, 8), repeat=2):
            for age in (0, 1, 2):
                for threshold in (0, 2, 8, 20):
                    out, guaranteed, _ = obs.bound_decision(cache, age, 'threshold', threshold, Counter())
                    worlds = itertools.product(*(range(max(-8, v-age), min(8, v+age)+1) for v in cache))
                    possible = {sum(v*v for v in w) >= threshold for w in worlds}
                    self.assertEqual(guaranteed, len(possible) == 1)
                    if guaranteed:
                        self.assertEqual(possible, {out})
                    else:
                        self.assertIsNone(out)

    def test_cold_threshold_and_fused_update_accounting(self):
        world = {'states': [[2, -3], [3, -3]], 'updates': [[], [[0, 3]]]}
        result = obs.run_policy(world, 'full_snapshot', 'threshold', 'complete', threshold=17)
        self.assertEqual([t['output'] for t in result['ticks']], [False, True])
        a, b = [t['counters'] for t in result['ticks']]
        self.assertEqual(a['calculation_square'], 2)
        self.assertEqual(a['calculation_total_write'], 3)
        self.assertEqual(b['calculation_square'], 2)
        self.assertEqual(b['calculation_total_write'], 1)
        self.assertEqual(b['snapshot_compare'], 2)

    def test_delivered_plus_dropped_mutations_recover_same_tick(self):
        # Fifth mutation dropped, first four delivered; trailing gap must not be missed.
        world = {'states': [[0]*5, [1]*5], 'updates': [[], [[i, 1] for i in range(5)]]}
        r = obs.run_policy(world, 'event_log', 'threshold', 'dropped', threshold=5)
        tick = r['ticks'][1]
        self.assertTrue(tick['recovered'])
        self.assertTrue(tick['output'])
        self.assertEqual(tick['cache'], [1]*5)
        self.assertEqual(len(tick['observed']['events']), 4)
        self.assertEqual(tick['observed']['checkpoint'], [1, 5])
        self.assertEqual(tick['counters']['source_log_field'], 15)
        self.assertEqual(tick['counters']['source_sequence'], 5)
        self.assertEqual(tick['counters']['cache_write'], 5)
        self.assertEqual(tick['counters']['calculation_total_write'], 5)
        self.assertEqual(tick['counters']['producer_publish_field'], 24)
        self.assertEqual(tick['counters']['delivery_field'], 24)
        self.assertEqual(tick['counters']['receive_field'], 21)
        self.assertEqual(tick['payload']['dropped_fields'], 3)
        self.assertEqual(tick['payload']['sent_fields'], 24)
        self.assertEqual(tick['counters']['source_snapshot_field'], 7)

    def test_interior_gap_recovery(self):
        world = {'states': [[0]*6, [1]*6], 'updates': [[], [[i, 1] for i in range(6)]]}
        t = obs.run_policy(world, 'event_log', 'exact', 'dropped')['ticks'][1]
        self.assertTrue(t['recovered'])
        self.assertEqual(t['output'], [1]*6)

    def test_zero_change_checkpoint_is_paid_and_fresh(self):
        w = {'states': [[2], [2]], 'updates': [[], []]}
        t = obs.run_policy(w, 'event_log', 'exact', 'complete')['ticks'][1]
        self.assertEqual(t['observed']['checkpoint'], [1, 0])
        self.assertTrue(t['guaranteed'])
        self.assertEqual(t['counters']['source_checkpoint_field'], 2)
        self.assertEqual(t['counters']['producer_publish_field'], 2)
        self.assertEqual(t['counters']['sequence_check'], 2)
        self.assertEqual(t['counters']['source_snapshot_field'], 0)

    def test_no_hidden_state_access_unchecked_lucky_vs_wrong(self):
        stable = {'states': [[0], [0]], 'updates': [[], []]}
        changed = {'states': [[0], [1]], 'updates': [[], [[0, 1]]]}
        a = obs.run_policy(stable, 'poll_unchecked', 'exact', 'complete')['ticks'][1]
        b = obs.run_policy(changed, 'poll_unchecked', 'exact', 'complete')['ticks'][1]
        for key in ('output', 'observed', 'guaranteed', 'cache', 'proof'):
            self.assertEqual(a[key], b[key])
        self.assertFalse(a['guaranteed'])
        self.assertFalse(a['wrong'])
        self.assertTrue(b['wrong'])
        for w in (stable, changed):
            t = obs.run_policy(w, 'poll_guarded', 'exact', 'complete')['ticks'][1]
            self.assertIsNone(t['output'])
            self.assertFalse(t['wrong'])

    def test_uncertified_but_sufficient_is_not_a_lucky_guess(self):
        w = {'states': [[0], [1]], 'updates': [[], [[0, 1]]]}
        t = obs.run_policy(w, 'poll_unchecked', 'threshold', 'complete', threshold=4)['ticks'][1]
        self.assertFalse(t['guaranteed'])  # unchecked policy did not certify reuse
        self.assertTrue(t.get('evidence_sufficient', False))
        self.assertFalse(t['wrong'])
        exact = obs.run_policy(w, 'poll_unchecked', 'exact', 'complete')['ticks'][1]
        self.assertFalse(exact['evidence_sufficient'])

    def test_source_bound_and_world_determinism(self):
        a = obs.make_world(16, 16, 7)
        self.assertEqual(a, obs.make_world(16, 16, 7))
        self.assertEqual(len(a['states']), 16)
        for previous, state in zip(a['states'], a['states'][1:]):
            self.assertEqual(sum(x != y for x, y in zip(previous, state)), 16)
            self.assertTrue(all(-8 <= v <= 8 for v in state))
            self.assertTrue(all(abs(x-y) <= 1 for x,y in zip(previous,state)))

    def test_full_suite_shape_safe_policies_and_determinism(self):
        a = obs.experiment()
        self.assertEqual(a, obs.experiment())
        self.assertEqual(len(a['worlds']), 24)
        self.assertEqual(len(a['cells']), 96)
        for cell in a['cells']:
            for name, policy in cell['policies'].items():
                self.assertEqual(len(policy['ticks']), 16)
                self.assertEqual(policy['operations'], sum(policy['counters'].values()))
                self.assertEqual(policy['emitted']+policy['unavailable'], 16)
                if name != 'poll_unchecked':
                    self.assertEqual(policy['wrong_emitted'], 0)
                    self.assertEqual(policy['emitted'], policy['guaranteed_emitted'])
                if name in ('event_log', 'full_snapshot'):
                    self.assertEqual(policy['emitted'], 16)

    def test_actual_shadow_import_rejected_before_results(self):
        with tempfile.TemporaryDirectory() as temp:
            package = Path(temp)/'pnp_architecture'
            package.mkdir()
            (package/'__init__.py').write_text('')
            (package/'observation.py').write_text('# foreign checkout\n')
            output = Path(temp)/'receipt.json'
            result = subprocess.run([sys.executable, str(ROOT/'scripts/run_observation.py'),
                                     '--output', str(output)], capture_output=True, text=True,
                                    env={**os.environ, 'PYTHONPATH': temp, 'PYTHONDONTWRITEBYTECODE': '1'})
            self.assertNotEqual(result.returncode, 0)
            self.assertIn('does not match this checkout', result.stderr)
            self.assertFalse(output.exists())

    def test_runner_provenance_and_no_overwrite(self):
        spec = importlib.util.spec_from_file_location('observation_runner', ROOT/'scripts/run_observation.py')
        runner = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(runner)
        self.assertEqual(runner.verify_sources()['src/pnp_architecture/observation.py'], hashlib.sha256((ROOT/'src/pnp_architecture/observation.py').read_bytes()).hexdigest())
        with self.assertRaisesRegex(ValueError, 'checkout'):
            runner.verify_sources(module_path=ROOT/'wrong.py')
        with tempfile.TemporaryDirectory() as temp:
            out = Path(temp)/'receipt.json'
            runner.write_exclusive(out, {'ok': True})
            self.assertEqual(json.loads(out.read_text()), {'ok': True})
            with self.assertRaises(FileExistsError):
                runner.write_exclusive(out, {'ok': False})
            self.assertEqual(json.loads(out.read_text()), {'ok': True})


if __name__ == '__main__':
    unittest.main()
