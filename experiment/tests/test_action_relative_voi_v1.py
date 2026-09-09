import unittest
from pnp_architecture.action_relative_voi_v1 import experiment
class VOITests(unittest.TestCase):
 def setUp(self):self.r=experiment()['beliefs']
 def test_entropy_symmetry(self):self.assertAlmostEqual(self.r['p_0.1']['entropy_bits'],self.r['p_0.9']['entropy_bits']);self.assertAlmostEqual(self.r['p_0.1']['entropy_bits'],0.4689955935892812)
 def test_policy_asymmetry(self):self.assertEqual(self.r['p_0.1']['best_policy'],'touch');self.assertEqual(self.r['p_0.9']['best_policy'],'inspect')
 def test_voi_and_cost_differ(self):self.assertAlmostEqual(self.r['p_0.1']['voi_perfect_information'],10);self.assertAlmostEqual(self.r['p_0.9']['voi_perfect_information'],10);self.assertNotEqual(self.r['p_0.1']['costs']['touch'],self.r['p_0.9']['costs']['touch'])
if __name__=='__main__':unittest.main()
