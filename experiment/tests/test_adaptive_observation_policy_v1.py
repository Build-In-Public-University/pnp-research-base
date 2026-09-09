import unittest
from pnp_architecture.adaptive_observation_policy_v1 import experiment,identifiable
class AdaptiveTests(unittest.TestCase):
 def setUp(self):self.r=experiment()
 def test_passive_and_single_channels(self):
  self.assertFalse(self.r['passive_identifiable']);self.assertFalse(identifiable(('local_parity',)));self.assertFalse(identifiable(('local_group',)))
 def test_best_policy(self):
  b=self.r['best_policy'];self.assertEqual(b['cost'],4);self.assertTrue(b['identifiable']);self.assertEqual(set(b['actions']),{'local_parity','local_group'})
 def test_privileged_exact(self):self.assertTrue(identifiable(('privileged_exact',)))
if __name__=='__main__':unittest.main()
