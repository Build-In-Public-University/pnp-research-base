import unittest
from pnp_architecture.stochastic_morphology_switching_v1 import experiment
class StochasticTests(unittest.TestCase):
 def setUp(self):self.r=experiment()['agents']
 def test_adaptive_reduces_switching(self):self.assertLessEqual(self.r['adaptive']['switches'],self.r['symmetric']['switches']);self.assertLess(self.r['adaptive']['switches'],self.r['stateless']['switches'])
 def test_receipt_metrics(self):
  for x in self.r.values():self.assertEqual(sum(x['occupancy'].values()),500);self.assertGreaterEqual(x['cost'],0)
 def test_determinism(self):self.assertEqual(experiment(),experiment())
if __name__=='__main__':unittest.main()
