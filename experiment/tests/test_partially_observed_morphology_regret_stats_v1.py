import unittest
from pnp_architecture.partially_observed_morphology_regret_stats_v1 import experiment
class StatsTests(unittest.TestCase):
 def test_sample_and_telescoping(self):
  r=experiment();self.assertEqual(r['seeds'],100);self.assertEqual(r['telescoping_failures'],0);self.assertGreater(r['aggregate_policy_share'],0);self.assertGreater(r['aggregate_uncertainty_share'],0)
if __name__=='__main__':unittest.main()
