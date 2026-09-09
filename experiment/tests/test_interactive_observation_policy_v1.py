import unittest
from pnp_architecture.interactive_observation_policy_v1 import experiment
class ObserverTests(unittest.TestCase):
 def setUp(self):self.r=experiment()['policies']
 def test_passive_not_identifiable(self):self.assertFalse(self.r['passive']['identifiable'])
 def test_privileged_and_calibration_identifiable(self):self.assertTrue(self.r['privileged']['identifiable']);self.assertTrue(self.r['calibration']['identifiable'])
 def test_costs_and_perturbation(self):self.assertLess(self.r['passive']['observation_cost'],self.r['privileged']['observation_cost']);self.assertTrue(self.r['calibration']['measurement_perturbation'])
 def test_passive_transcripts_equal(self):self.assertEqual(self.r['passive']['transcripts']['low_power'],self.r['passive']['transcripts']['high_power'])
if __name__=='__main__':unittest.main()
