import unittest
from pnp_architecture.parameterized_state_scaling_v1 import experiment,analyze,shortest
class ScalingTests(unittest.TestCase):
 def setUp(self):self.r=experiment(range(1,9))
 def test_exponential_state_count_and_linear_bits(self):
  for x in self.r['rows']:self.assertEqual(x['K_G'],2**x['n']);self.assertEqual(x['I_G_bits'],x['n']);self.assertEqual(x['reachable_states'],x['K_G'])
 def test_all_pairs_distinguishable(self):self.assertTrue(all(x['all_pairwise_distinguishable'] for x in self.r['rows']))
 def test_update_and_decision_scaling(self):
  self.assertTrue(all(x['update_work_per_event']==1 for x in self.r['rows']));self.assertEqual([x['decision_work_per_query'] for x in self.r['rows']],list(range(1,9)))
 def test_depth_formula_is_bounded(self):self.assertEqual(shortest(3,1,3),2);self.assertEqual(shortest(0,7,3),1)
if __name__=='__main__':unittest.main()
