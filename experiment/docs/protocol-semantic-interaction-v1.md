# Semantic interaction calibration v1

Use 12 copied archive-manifest files and 12 derived records with contiguous join widths 1, 2, and 4. Compare ordinary dependency union repair against an interaction-aware oracle after four explicit cases: disjoint updates, adjacent updates, a joint two-input update, and a clustered update.

The `joint` and `cluster` cases activate one additional derived record through an explicit pairwise constraint when inputs 0 and 1 change together. Report ordinary union size, joint affected size, interaction-cone size, repair edge checks, assurance scope, and exactness. The union-only path is deliberately allowed to fail when the joint constraint is active.

This is a synthetic semantic-interaction fixture calibrated over temporary copies of a concrete archive shape. The interaction rule is explicit, not inferred from natural-language semantics. It is not evidence about P/NP or universal runtime.
