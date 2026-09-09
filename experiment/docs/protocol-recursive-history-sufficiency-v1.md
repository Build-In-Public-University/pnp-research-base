# Recursive history sufficiency calibration v1

Model the release contract as a finite observed transition system. Semantic retained state is one of `clean`, `migration_missing`, or `migration_satisfied`. Observations are `inspect`, `approve`, `joint_release`, `joint_release_with_migration`, and `reset`.

The decision function accepts every state except `migration_missing`. `approve` updates missing to satisfied; joint release events update the state according to whether migration evidence is present; reset returns to clean. Compare current-state-only, serialized semantic state, and a trusted one-byte state code.

Test decision sufficiency, update sufficiency, and continuation sufficiency. Enumerate every event sequence through length 6 and independently verify the factorization identity for the finite transition/output system. The all-length continuation claim follows by induction because both output and update depend only on the retained state and next observation.

The state code is trusted and not self-authenticating. This protocol measures semantic state size separately from serialized and maintenance representations. It is a contract-specific finite witness, not a universal minimal-automaton result for release systems.
