import unittest
from pnp_architecture.loss_aware_observation_v1 import experiment
class LossAwareTests(unittest.TestCase):
 def setUp(self):self.r=experiment()['scenarios']
 def test_common_escalates(self):x=self.r['common_high_loss'];self.assertEqual(x['residual_choice'],'observe_privileged');self.assertEqual(x['residual_stop_risk'],10);self.assertAlmostEqual(x['policy_expected_cost'],4.6)
 def test_rare_stops(self):x=self.r['rare_low_loss'];self.assertEqual(x['residual_choice'],'stop_safe');self.assertAlmostEqual(x['residual_stop_risk'],2);self.assertAlmostEqual(x['policy_expected_cost'],1.06)
 def test_uncertainty_remains(self):self.assertFalse(self.r['rare_low_loss']['exact_identification'])
if __name__=='__main__':unittest.main()
