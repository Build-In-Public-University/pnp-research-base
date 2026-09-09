import unittest
from pnp_architecture.fixed_contract_architecture_v1 import experiment
class ArchitectureTests(unittest.TestCase):
 def setUp(self):self.r=experiment(range(1,9))
 def test_all_architectures_exact(self):self.assertTrue(all(x['exact'] for x in self.r['rows']))
 def test_counter_constant_decision(self):self.assertTrue(all(x['decision_work']==1 for x in self.r['rows'] if x['architecture']=='mask_counter'))
 def test_raw_decision_linear(self):self.assertEqual([x['decision_work'] for x in self.r['rows'] if x['architecture']=='raw_mask'],list(range(1,9)))
 def test_event_log_replay_grows(self):self.assertGreater(self.r['rows'][-1]['decision_work'],self.r['rows'][0]['decision_work'])
if __name__=='__main__':unittest.main()
