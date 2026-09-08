# Gate pilot v1: executed readout

Source proposal: pnp 3.md, staged validation gates. Corrected definitions and wider research integration: docs/pnp3-integration.md. Claims: claims/pnp3.md.

| Workload (100 candidates each) | Cheap-first | Composition-first | Full checks | Accepted by each |
|---|---:|---:|---:|---:|
| Local-failure-heavy | 380 | 710 | 730 | 10 |
| Composition-failure-heavy | 680 | 590 | 730 | 10 |
| All valid | 800 | 800 | 800 | 100 |
| Correlated failures | 380 | 590 | 730 | 10 |

All cost columns are DECLARED SYNTHETIC GATE-INVOCATION POINTS (syntax 1, local 2, composition 5), not timings, physical energy, or operation counts for predicate internals. Gates execute actual type, nonnegativity and sum predicates. Syntax is a prerequisite for both later checks. Full-check baseline evaluates both remaining checks after syntax passes; it does not run undefined predicates on malformed inputs. The correlated fixture's two non-syntax failure types overlap explicitly.

Every per-candidate acceptance vector matched an independent imperative oracle, not just aggregate counts. Accepting requires all gates, never a cheap-filter shortcut. There were 400 unique candidate positions across four constructed workloads and three policy evaluations per position, not 1,200 independent data points. Repetitions use a small set of deterministic templates; this is a counterexample/control, not an empirical population estimate.

Cheap-first wins local-heavy, loses composition-heavy. Selection on local-heavy yields cheap-first; transferred unchanged to composition-heavy it spends 680 versus the retrospective best 590. The retrospective best uses full outcomes and is not a free learned optimizer; policy-selection overhead is excluded and no online speedup claimed. All-valid ties at 800: filters only save downstream checking when they reject.

## Verification receipts

- Protocol was written and SHA-256 frozen before implementation/run; runner checks it.
- Initial test execution failed with ModuleNotFoundError for the not-yet-created gates module. This establishes missing implementation, not behavioral red coverage for all tests.
- Full final suite: 29 tests, OK (1.868 seconds on this execution).
- Retained runs: artifacts/gates_v1.json and artifacts/gates_v1-repeat.json; cmp returned exit 0.
- Tests exercise real predicates, prerequisites, accepted candidates passing all gates, cost-counter identity, matched acceptance, counterexample/control, deterministic CLI execution and refusal to overwrite.
- No providers, installs, network requests, permission changes, real deployments or publication.

Reproduce to a fresh path from repository root:

```sh
PYTHONPATH=src python3 scripts/run_gates.py --output artifacts/gates_v1-local.json
PYTHONPATH=src python3 -m unittest discover -s tests -v
```

## What remains open

The fixture tests ordering with perfect deterministic checks, not imperfect evidence/AI confidence. It does not establish search-validation divergence, prove value of retained history under drift, model real CI pipelines, or price irreversible consequences. Those remain separately specified research tasks, not inferred results.
