import unittest
from pnp_architecture.branching_adaptive_observation_policy_v1 import experiment
class BranchingTests(unittest.TestCase):
 def setUp(self):self.p=experiment()['policy']
 def test_exact_transcripts(self):self.assertTrue(self.p['identifiable']);self.assertEqual(len(set(self.p['transcripts'].values())),5)
 def test_branches(self):
  self.assertEqual(len(self.p['transcripts']['A']),1);self.assertEqual(len(self.p['transcripts']['C']),2);self.assertEqual(len(self.p['transcripts']['E']),3)
 def test_expected_and_worst_cost(self):self.assertEqual(self.p['cost_by_state'],{'A':1,'B':1,'C':3,'D':3,'E':9});self.assertEqual(self.p['worst_cost'],9);self.assertAlmostEqual(self.p['expected_cost'],3.4);self.assertLess(self.p['expected_cost'],self.p['always_privileged_cost'])
if __name__=='__main__':unittest.main()
