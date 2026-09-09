import unittest
from pathlib import Path
from pnp_architecture.history_sufficiency_v1 import experiment
class HistoryTests(unittest.TestCase):
 def setUp(self):self.r=experiment(Path('/Users/leoguinan/pnp-session-review'))['representations']
 def test_current_state_is_indistinguishable(self):
  x=self.r['current_only'];self.assertTrue(x['indistinguishable']);self.assertEqual([r['oracle_outcome'] for r in x['rows']],[False,True])
 def test_retained_contract_state_distinguishes(self):
  for name in ('event_log','transition_record','digest_summary','minimal_state'):
   self.assertFalse(self.r[name]['indistinguishable'],name)
   self.assertTrue(self.r[name]['exact_for_pair'],name)
 def test_minimal_state_is_smaller_than_event_log(self):
  self.assertLess(self.r['minimal_state']['rows'][0]['representation_bytes'],self.r['event_log']['rows'][0]['representation_bytes'])
if __name__=='__main__':unittest.main()
