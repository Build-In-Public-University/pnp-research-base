import json,unittest
from pathlib import Path
from pnp_architecture.archive_release_contract_v1 import experiment
class ReleaseContractTests(unittest.TestCase):
 def test_real_manifest_is_validated(self):
  r=experiment(Path('/Users/leoguinan/pnp-session-review'))
  self.assertTrue(all(c['current_state_valid'] for c in r['cases']))
 def test_transition_requirement_is_not_final_state_only(self):
  r=experiment(Path('/Users/leoguinan/pnp-session-review'));by={c['case']:c for c in r['cases']}
  self.assertTrue(by['both_without_migration']['state_only_accepts'])
  self.assertFalse(by['both_without_migration']['oracle_transition_valid'])
  self.assertTrue(by['both_with_migration']['oracle_transition_valid'])
if __name__=='__main__':unittest.main()
