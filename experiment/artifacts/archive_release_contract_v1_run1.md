# Archive release-contract calibration v1

| Case | Current-state valid | State-only accepts | Transition oracle |
|---|---|---|---|
| manifest_only | True | True | True |
| compat_only | True | True | True |
| both_without_migration | True | True | False |
| both_with_migration | True | True | True |

Manifest validation used the actual repository checkout; compatibility and migration rules are declared protocol contracts.
