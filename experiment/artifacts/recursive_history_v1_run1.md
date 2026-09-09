# Recursive history sufficiency calibration v1

| Representation | Bytes | Distinct semantic values |
|---|---:|---|
| current_only | 18 | ['same-current-files', 'same-current-files', 'same-current-files'] |
| semantic | 19 | ['clean', 'migration_missing', 'migration_satisfied'] |
| serialized | 19 | ['clean', 'migration_missing', 'migration_satisfied'] |
| trusted_code | 1 | ['00', '01', '02'] |
| state_bits | 1 | [0, 1, 2] |

States: clean, migration_missing, migration_satisfied. Events: inspect, approve, joint_release, joint_release_with_migration, reset. Exhaustive sequences through length 6: 19531.

Decision and update factorization passed; continuation sufficiency is established for this finite machine by induction from those two factorizations.
