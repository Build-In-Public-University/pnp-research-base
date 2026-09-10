import unittest
from pnp_architecture.persistent_capability_reuse_v1 import experiment,best,totals
class ReuseTests(unittest.TestCase):
 def test_low_demand(self):self.assertEqual(best(1),'fresh');self.assertEqual(best(2),'persistent_remote')
 def test_crossover(self):self.assertEqual(best(3),'persistent_remote');self.assertEqual(best(4),'local_replica');self.assertEqual(best(12),'local_replica')
 def test_amortization(self):
  r=experiment()['rows'];self.assertEqual(r[0]['averages']['persistent_remote'],11);self.assertEqual(r[-1]['averages']['local_replica'],2.25)
if __name__=='__main__':unittest.main()
