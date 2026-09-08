# History v1.1 review amendment — before corrected runs

Keep docs/protocol-history-v1.md frozen and all v1 artifacts unchanged. This amendment supersedes only the following implementation/accounting/provenance items. Same inputs, policies, observation conditions, penalties and acceptance contract; no retuning.

1. Each dirty output executes two stored-total mutations: subtract old and add new. Charge TWO total reads and TWO total writes, not one of each. Arithmetic counts unchanged. Expected increase: two proxy operations per repaired output. This corrects an undercount; do not describe old prices as current.
2. Runner checks the resolved imported history module path equals this checkout's src/pnp_architecture/history.py before execution or receipt emission. Fail closed on mismatched package resolution. Hash module provenance plus both protocols and tests.
3. Add deterministic regression with delivered and omitted changes sharing a dirty subproblem, so repairing from omniscient world state would fail. Existing post-run randomized partial-feed audit is additional coverage, not a replacement for the targeted regression.
4. Print strict observed-correctness winners separately from unrestricted priced winners. Eligibility remains retrospective for each trajectory, not a guarantee.

Freeze amendment SHA-256 before corrected run. New output names history_v1_1*. Compare corrected decision vectors to original v1 and assert identical inputs/world hashes. For every policy step require corrected operations = old operations + 2*old_total_write_counter. Preserve v1 findings as historical, update active readout to corrected counts. Retain two identical corrected runs. No external calls or publication.
