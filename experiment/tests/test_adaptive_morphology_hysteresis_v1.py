import unittest
from pnp_architecture.adaptive_morphology_hysteresis_v1 import experiment
class HysteresisTests(unittest.TestCase):
 def setUp(self):self.rows=experiment()['rows']
 def row(self,d,s):return next(x for x in self.rows if x['d']==d and x['start']==s)
 def test_enter_exit_differ(self):self.assertEqual(self.row(4,'remote')['policy'][0],'local');self.assertEqual(self.row(.1,'local')['policy'][0],'remote')
 def test_band_retains_morphology(self):self.assertEqual(self.row(1,'remote')['policy'][0],'remote');self.assertEqual(self.row(1,'local')['policy'][0],'local')
 def test_boundaries(self):self.assertEqual(self.row(2.25,'remote')['cost'],27);self.assertEqual(self.row(3,'remote')['policy'][0],'local');self.assertEqual(self.row(.25,'local')['cost'],9);self.assertEqual(self.row(.1,'local')['policy'][0],'remote')
if __name__=='__main__':unittest.main()
