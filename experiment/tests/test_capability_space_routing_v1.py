import unittest
from pnp_architecture.capability_space_routing_v1 import experiment
class CapabilityTests(unittest.TestCase):
 def setUp(self):self.r=experiment()
 def test_route(self):self.assertEqual(self.r['best_path'],('discover','move','connect','transfer','compose'));self.assertEqual(self.r['best_cost'],11)
 def test_capability_state(self):self.assertFalse(self.r['discovery_changes_capabilities']);self.assertTrue(self.r['transfer_changes_capabilities']);self.assertTrue(self.r['capability_acquisition']);self.assertEqual(self.r['final_state'][1],frozenset({'parity','group'}))
 def test_composite_goal(self):self.assertEqual(self.r['goal'],['group','parity'])
if __name__=='__main__':unittest.main()
