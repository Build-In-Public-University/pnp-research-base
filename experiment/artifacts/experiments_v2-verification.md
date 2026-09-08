# v2 execution verification

Local-only run; no dependencies installed, external calls, publication, or commits.

## Protocol freeze

`docs/protocol-v2.md` was written and its digest recorded **before** algorithm
implementation/result runs. Frozen SHA-256:

`6976a672e64d772b1e11330d4645f5fa613f0ec3d1e07e38a246a654d8aca987`

The runner checks the hash before execution. A unit test verifies drift refusal.
This is a local procedural freeze, not a timestamped external preregistration.

## Tests-first record

- Initial tests were written before the v2 module: 17 tests ran, 12 assertion
  failures (11 asserted the missing v2 module; one proved the legacy module CLI
  did not execute `main`), 5 existing tests passed. The module-existence failures
  prove missing API, **not** individual algorithm-behavior RED coverage.
- With the module implemented and runner test added: 20 tests ran, only the
  missing runner and legacy CLI execution tests failed.
- After CLI/runner implementation: 20 tests passed.
- Review added a regression for centralized inspections on disconnected graphs:
  expected 2 received-bit inspections, observed 4 (FAIL). Corrected the collector
  to inspect only collected values rather than reuse local-only validity results.
- Added full grid accounting and protocol drift checks. Final command:

```bash
PYTHONPATH=src python3 -m unittest discover -s tests -v
```

Actual final output: `Ran 22 tests in 1.825s`, `OK`, exit 0. This includes the two
`test_quantifier_boundary.py` tests added concurrently by the parent task; this
implementation did not modify that file.

## Two retained executions

From the repository root:

```bash
PYTHONPATH=src python3 scripts/run_experiments_v2.py --output artifacts/experiments_v2.json --summary artifacts/experiments_v2-summary.md
PYTHONPATH=src python3 scripts/run_experiments_v2.py --output artifacts/experiments_v2-repeat.json --summary artifacts/experiments_v2-repeat-summary.md
cmp artifacts/experiments_v2.json artifacts/experiments_v2-repeat.json
cmp artifacts/experiments_v2-summary.md artifacts/experiments_v2-repeat-summary.md
```

Both runner commands returned `executed_synthetic_algorithms`, 30 graphs,
120 propagation cells, 60 containing witnesses and 30 CNF formulas. Both `cmp`
commands returned exit 0 (identical bytes). Both receipts have SHA-256:

`54d36defc25fe3d5218575459530709be5001d6fb34e84f215098ffd2d0ea505`

Each receipt is 1,040,398 bytes and contains 90 scheduling results and 32,736
full-truth-table assignment outcomes. A separate readback recomputed all nine
embedded source SHA-256 values and confirmed all matched the on-disk inputs.

`git diff --check` passed. `git diff --exit-code -- src/pnp_architecture/model.py
artifacts/first_attack.json` returned 0: historical model and receipt unchanged.
Runner overwrite refusal is tested; choose fresh output paths for another run.

## Findings and limits

See `experiments_v2-summary.md` for generated result tables. At N=32, complete
flood sends were 992 versus 31 tree-route sends; all connected tree routes tied
at 31 sends while their rounds differed. BFS setup remained separately charged.
Local-only conjunction made 25 false global predictions; centralized outcomes
were 30 accepts, 20 witness rejections, 10 unavailable, zero available-oracle
mismatches. These containing problems are all SAT, irrespective of bad witnesses.
CNF cases comprised 10 SAT and 20 UNSAT formulas. All 10 SAT formulas used more
search work with the full processor budget than with serial first-success search.

No real parallel hardware was used. Scheduling makespan is idealized, not time.
Graph memory/generation, headers, contention, formula distribution, assignment
construction and orchestration are excluded. Oracle work and returned-witness
verification are not hidden inside search counts. Input size includes clauses.
No brute-force observation establishes a SAT lower bound or P/NP separation.
