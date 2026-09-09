import unittest
from pnp_architecture.contract_complexity_v1 import experiment
class ComplexityTests(unittest.TestCase):
 def setUp(self):self.r=experiment(6)
 def test_three_reachable_classes(self):self.assertEqual(self.r['K_G'],3);self.assertEqual(self.r['I_G_bits'],2);self.assertTrue(all(v>0 for v in self.r['reachable_classes'].values()))
 def test_partition_factorization(self):self.assertTrue(self.r['same_state_bounded_factorization'])
 def test_pairwise_distinguishers(self):self.assertTrue(all(v is not None and len(v)<=1 for v in self.r['shortest_distinguishers'].values()))
 def test_cost_dimensions_present(self):
  for c in self.r['costs'].values():self.assertEqual(set(c),{'retained_state_bytes','observation_cost_per_event','update_cost_per_event','decision_cost_per_query','evidence_cost_per_update'})
if __name__=='__main__':unittest.main()
