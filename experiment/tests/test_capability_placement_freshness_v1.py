import unittest
from pnp_architecture.capability_placement_freshness_v1 import best,totals,experiment
class FreshnessTests(unittest.TestCase):
 def test_demand_favors_local(self):self.assertEqual(best(12,0),'local');self.assertEqual(best(12,.2),'remote')
 def test_change_rate_erodes_locality(self):self.assertLess(totals(12,0)['local'],totals(12,0)['remote']);self.assertGreater(totals(12,.4)['local'],totals(12,.4)['remote'])
 def test_low_demand(self):self.assertEqual(best(1,0),'fresh');self.assertEqual(best(2,0),'remote')
 def test_surface_size(self):self.assertEqual(len(experiment()['rows']),60)
if __name__=='__main__':unittest.main()
