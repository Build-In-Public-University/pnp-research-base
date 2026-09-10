import unittest
from pnp_architecture.morphology_transition_cost_phase_sweep_v1 import experiment
class PhaseSweepTests(unittest.TestCase):
 def setUp(self):self.r=experiment();self.rows={(x['S_RL'],x['S_LR']):x for x in self.r['rows']}
 def test_grid(self):self.assertEqual(len(self.r['rows']),25)
 def test_zero_cost_tracks_crossover(self):x=self.rows[(0,0)];self.assertGreater(x['switches'],self.rows[(20,20)]['switches']);self.assertLess(x['lock_in_rate'],self.rows[(20,20)]['lock_in_rate'])
 def test_cost_decomposition(self):
  for x in self.r['rows']:self.assertAlmostEqual(x['total_cost'],x['operating_cost']+x['transition_cost'])
 def test_oracle_separates_rational_and_maladaptive_persistence(self):
  self.assertGreater(self.rows[(20,20)]['optimal_lock_in_rate'],0);self.assertLess(self.rows[(20,20)]['regret_vs_optimal'],20);self.assertGreater(self.rows[(10,10)]['regret_vs_optimal'],200)
 def test_determinism(self):self.assertEqual(experiment(),experiment())
if __name__=='__main__':unittest.main()
