import unittest
from pnp_architecture.dual_control_policy_phase_diagram_v1 import experiment,best
class PhaseTests(unittest.TestCase):
 def test_policy_regions(self):
  self.assertEqual(best(.001),'immediate');self.assertEqual(best(.1),'touch');self.assertEqual(best(.5),'inspect');self.assertEqual(best(.99),'immediate')
 def test_threshold_checks(self):
  r=experiment()['checks'];self.assertEqual(r[.01]['best'],'immediate');self.assertEqual(r[.012]['best'],'touch');self.assertEqual(r[.399]['best'],'touch');self.assertEqual(r[.401]['best'],'inspect');self.assertEqual(r[.949]['best'],'inspect');self.assertEqual(r[.951]['best'],'immediate')
 def test_intervals_cover_grid(self):self.assertEqual([(x[0],x[1],x[2]) for x in experiment()['intervals']], [('immediate',0.0,0.011),('touch',0.012,0.399),('inspect',0.4,0.95),('immediate',0.951,1.0)])
if __name__=='__main__':unittest.main()
