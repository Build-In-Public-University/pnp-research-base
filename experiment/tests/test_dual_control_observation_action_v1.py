import unittest
from pnp_architecture.dual_control_observation_action_v1 import experiment
class DualControlTests(unittest.TestCase):
 def setUp(self):self.s=experiment()['scenarios']
 def test_rare_prefers_probe(self):x=self.s['rare_fragile'];self.assertEqual(x['best_policy'],'gentle_touch_then_act');self.assertEqual(x['values']['gentle_touch_then_act'],3);self.assertEqual(x['values']['inspect_then_act'],6)
 def test_common_prefers_non_destructive_inspection(self):x=self.s['common_fragile'];self.assertEqual(x['best_policy'],'inspect_then_act');self.assertEqual(x['values']['gentle_touch_then_act'],7)
 def test_probe_is_epistemic_and_intervening(self):x=self.s['rare_fragile'];self.assertTrue(x['touch_observes']);self.assertTrue(x['touch_changes_state'])
if __name__=='__main__':unittest.main()
