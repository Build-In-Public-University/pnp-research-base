import unittest
from pnp_architecture.partially_observed_morphology_regret_v1 import run
class PartialTests(unittest.TestCase):
 def setUp(self):self.r=run()
 def test_telescoping(self):self.assertAlmostEqual(self.r['cost_heuristic']-self.r['cost_clairvoyant'],self.r['policy_regret']+self.r['uncertainty_regret'])
 def test_nonzero_information_gap(self):self.assertGreater(self.r['policy_regret'],0);self.assertGreater(self.r['uncertainty_regret'],0)
 def test_trace(self):self.assertEqual(len(self.r['trace']),12);self.assertEqual(len(self.r['demand_path']),12)
 def test_determinism(self):self.assertEqual(run(),run())
if __name__=='__main__':unittest.main()
