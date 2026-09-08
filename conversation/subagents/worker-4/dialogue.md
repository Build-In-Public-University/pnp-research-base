# Stored dialogue

Context summaries are in records.jsonl, not repeated here. Inactive historical rows and replayed text are retained; ordering is database ID order, not deduplicated chronology.

## Record 685134 — user

Stored active=1; compacted=0.

Implement and execute bounded experiment suite in <HOME>/pnp-network-architecture. Local only no external calls/publication. Inspect files first. Preserve old model/receipts. New module experiments_v2.py plus unittest tests and runner. Freeze docs/protocol-v2.md BEFORE runs. Three experiments: (1) explicit undirected chain/star/balanced tree/complete/disconnected graphs at N=1,2,4,8,16,32; payload bit lengths 8,16,32,64. Execute deterministic synchronous flooding with first-arrival forwarding, record real loop counters sends/payload-bit-hops, rounds, reached, all-reached exactness. Compare BFS spanning-tree routed propagation with flood; charge BFS setup inspections separately, repeated reuse counts 1,4,16. No imaginary timing or energy. (2) containing-constraint: each of N nodes local certificate is a bit satisfying local predicate bit in {0,1}; global requirement all bits equal. consistent zeros and single-one conflicts. Local-only vs centralized collection via routing tree; disconnected must mark unavailable not accept. Distinguish rejecting inconsistent submitted witnesses from UNSAT. Independently oracle-check global outcomes. (3) actual small 3-CNF enumeration n=4,6,8,10,12 with deterministic seeded random formulas and explicit UNSAT core (all eight signed triples on vars 0,1,2); use same formula and assignment order. Enumerate full search to get exact truth table, count literal inspections. Simulate batched first-success enumeration p=1,n,2**n; charge all work in winning batch; report idealized makespan=sum max candidate work per batch, processors, total work, verification of returned witness. State no real parallel hardware used; input size includes clauses; don't infer SAT lower bounds from brute force. Tests first including graph edge sets, reachability, counter accounting, inconsistency detection, actual CNF verifier and scheduler. Run full unittest with PYTHONPATH=src; add deterministic JSON receipt with embedded config/input identities source sha256 and outputs, summary markdown from real results. No dependency installs needed. Run twice compare results. Return paths, exact command/results, limitations. Do not commit; parent reviews. Keep scope practical and bounded. Also fix module cli __main__ guard if absent and README runnable PYTHONPATH commands. Mark prior first_attack explicitly arithmetic-only not executed verifier. No universal or PNP separation claims.

## Record 685217 — assistant

Stored active=1; compacted=0.

Implemented and executed locally in `<HOME>/pnp-network-architecture`. **No commits, installs, external calls, or publication.**

### Verified results
- **22 unittest tests passed** (`Ran 22 tests in 1.825s`, `OK`).
- Two retained runs produced **byte-identical JSON receipts and summaries**.
- Coverage: **30 graphs, 120 propagation cells, 60 containing witnesses, 30 CNF formulas, 90 schedules, 32,736 exhaustive assignment outcomes**.
- All nine embedded source hashes matched on readback.
- Historical `model.py` and `artifacts/first_attack.json` unchanged; `git diff --check` passed.

### Findings
- N=32 complete graph: **992 flood sends versus 31 routed sends**, with **992 BFS setup inspections** reported separately.
- All connected spanning-tree routes tied at 31 sends; topology still changed rounds.
- Local-only conjunction made **25 false global predictions**.
- Centralized outcomes: **30 accepts, 20 witness rejections, 10 unavailable**, zero available-oracle disagreements.
- CNF: **10 SAT, 20 UNSAT** cases. All 10 SAT cases consumed more search work with the full processor budget than serial first-success search.

### Files
Created:
- `src/pnp_architecture/experiments_v2.py`
- `tests/test_experiments_v2.py`
- `scripts/run_experiments_v2.py`
- `docs/protocol-v2.md` and `.sha256` — frozen before runs
- `artifacts/experiments_v2.json`
- `artifacts/experiments_v2-repeat.json`
- Corresponding `*-summary.md` files
- `artifacts/experiments_v2-verification.md` — commands, execution record, hashes, limitations

Modified `README.md` with runnable commands and explicit arithmetic-only characterization of the legacy fixture; fixed `cli.py`’s missing `__main__` guard.

### Exact execution
```bash
PYTHONPATH=src python3 -m unittest discover -s tests -v
PYTHONPATH=src python3 scripts/run_experiments_v2.py --output artifacts/experiments_v2.json --summary artifacts/experiments_v2-summary.md
PYTHONPATH=src python3 scripts/run_experiments_v2.py --output artifacts/experiments_v2-repeat.json --summary artifacts/experiments_v2-repeat-summary.md
cmp artifacts/experiments_v2.json artifacts/experiments_v2-repeat.json
cmp artifacts/experiments_v2-summary.md artifacts/experiments_v2-repeat-summary.md
```
All final commands exited 0. Receipt SHA-256:
`54d36defc25fe3d5218575459530709be5001d6fb34e84f215098ffd2d0ea505`

**Limitations:** finite synthetic algorithms; serially simulated parallel scheduling, no measured hardware time/energy; setup and communication exclusions explicit; rejected witnesses are not UNSAT; no SAT lower-bound or P/NP separation claims. Review caught and regression-fixed centralized inspection accounting before retained runs. Parent’s concurrent ledger/formal-boundary files were left untouched.
