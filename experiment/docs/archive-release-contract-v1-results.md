# Archive release-contract calibration v1: results

This calibration uses the actual repository `manifest.json` and validates its file entries against the current checkout, including presence, byte counts, and SHA-256 digests. It adds a versioned compatibility declaration and a release contract requiring migration evidence when the manifest and compatibility declaration change together.

## Executed cases

| Case | Current-state valid | State-only accepts | Transition oracle |
|---|---|---|---|
| manifest only | yes | yes | yes |
| compatibility only | yes | yes | yes |
| both without migration | yes | yes | no |
| both with migration | yes | yes | yes |

The `both_without_migration` case is the decisive boundary. Its current files are structurally valid and pass the state-only checker, but the independent transition oracle rejects the release because both inputs changed in one release without `migration-approval` evidence.

The transition-aware case supplies a receipt binding:

- the changed-file set;
- the previous manifest digest;
- the current release transition.

This demonstrates the distinction between a valid final state and a valid path to that state. The compatibility declaration and migration requirement are newly declared research-repo protocol contracts; they are not pre-existing production policy. The manifest validation, file inventory, byte counts, and digests use actual repository artifacts.

Formally, the fixture has two histories that can share current-state validity while differing in contract outcome:

\[
S'(\tau_1)=S'(\tau_2)
\quad\text{but}\quad
G(\tau_1)\ne G(\tau_2).
\]

No checker restricted to the current files can distinguish those paths. The required input is the retained transition fact: which contract-relevant inputs changed together, and from which previous release state.

## Reproduction

```sh
PYTHONPATH=src python3 -m unittest tests.test_archive_release_contract_v1 -q
PYTHONPATH=src python3 scripts/run_archive_release_contract_v1.py \
  --output artifacts/archive_release_contract_v1_local.json \
  --summary artifacts/archive_release_contract_v1_local.md
```

No external release or deployment was performed.
