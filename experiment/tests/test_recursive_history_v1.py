import unittest
from pnp_architecture.recursive_history_v1 import experiment,STATES,EVENTS,run,observe,update
class RecursiveTests(unittest.TestCase):
 def setUp(self):self.r=experiment(6)
 def test_factorization(self):self.assertEqual(self.r['factorization'],{'decision':True,'update':True,'continuation_bounded':True})
 def test_all_three_states_remain_distinguishable(self):self.assertTrue(self.r['distinct_state_signatures'])
 def test_one_byte_semantic_code(self):self.assertEqual(self.r['representations']['state_bits']['bytes'],1)
 def test_bounded_continuations(self):self.assertEqual(self.r['bounded_sequences'],19531)
 def test_transition_examples(self):self.assertEqual(update('migration_missing','approve'),'migration_satisfied');self.assertFalse(observe('migration_missing','inspect'));self.assertTrue(observe('migration_satisfied','inspect'))
if __name__=='__main__':unittest.main()
