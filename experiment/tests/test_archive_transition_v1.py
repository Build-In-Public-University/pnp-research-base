import json,unittest
from pathlib import Path
from pnp_architecture.archive_transition_v1 import run_case
class TransitionTests(unittest.TestCase):
 def test_isolated_changes_need_only_state_dependencies(self):
  for case in ('manifest_only','compat_only'):
   x=run_case(Path('/Users/leoguinan/pnp-session-review'),case)
   self.assertTrue(x['arms']['singleton_only']['mechanically_exact'])
   self.assertTrue(x['arms']['state_complete']['mechanically_exact'])
 def test_simultaneous_change_requires_transition_semantics(self):
  x=run_case(Path('/Users/leoguinan/pnp-session-review'),'both')
  self.assertFalse(x['arms']['singleton_only']['mechanically_exact'])
  self.assertFalse(x['arms']['state_complete']['mechanically_exact'])
  self.assertTrue(x['arms']['transition_aware']['mechanically_exact'])
  self.assertIn('migration-approval',x['oracle_artifacts'])
if __name__=='__main__':unittest.main()
