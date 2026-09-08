# Observation systems v1 — parent-verified results

## Outcome and scope

24 configured trajectories, 96 matched contract/transport cells, four policies, 16 ticks: **6,144 policy-tick decisions**. Exact-vector and threshold (`sum(x_i^2) >= 16*n`) contracts share the same worlds. Domain [-8,8], per-coordinate movement at most one per tick. Consumers do not know seed, realized update count, future state or current unobserved state.

The event-log and full-snapshot policies emit correct, certified answers at every tick under the frozen source/transport assumptions. Guarded polling emits no wrong answer but frequently cannot fulfill the immediate-answer contract. Unchecked polling produces wrong answers; some unverified correct answers are actually information-sufficient, others merely correct on the realized world. These categories are separate.

The delegated observation worker timed out after creating source, tests and two receipts, before writing this report. The parent recovered by reading those artifacts, independently auditing every observation counter and received-state reconstruction, running the entire repository suite, and executing a third byte-identical observation run. This is verified artifact recovery, not treating worker timeout as success.

## Source-side cost is no longer omitted

Actual source writes, log sequence advances, three-field event construction, fresh two-field checkpoints, snapshot field acquisition, publication/transport/receive loops, comparison, cache updates, contract calculations and outputs are charged at their declared logical unit weights. Payload field counts are separate, not added twice. These are not the units or workloads of history v1.1, so do not interpret cross-suite numbers as a speedup.

Representative n=64, seed=7, exact-vector contract, 16 ticks (including initialization):

| Changes/tick | Transport | Log + checkpoint + recovery | Full snapshot | Log recoveries |
|---:|---|---:|---:|---:|
| 0 | complete | 1,577 | 6,352 | 0 |
| 1 | complete | 1,817 | 6,382 | 0 |
| 1 | drop every fifth event | 2,792 | 6,382 | 3 |
| 16 | complete | 5,417 | 6,832 | 0 |
| 16 | drop every fifth event | 10,160 | 6,832 | 15 |
| 64 | complete | 16,937 | 8,272 | 0 |
| 64 | drop every fifth event | 21,104 | 8,272 | 15 |

Every log/snapshot entry above supplies 16 correct certified outputs. Sparse event observation retains an advantage even after its production is charged. Dense logging loses; repeated gap recovery can reverse a complete-transport win. Neither retaining history nor logging every change is universally cheapest.

Full-service certified winners across 48 cells per contract: event log 30, full snapshot 18, for both exact and threshold. Transport-labeled snapshot/poll results are duplicate controls, not independent population samples. Cell counts reflect the predeclared grid, not deployment success probabilities.

## Contract-relative coverage

Aggregated over both transport labels, per policy and contract (768 requests each):

| Contract | Policy | Emitted | Certified emitted | Wrong emitted | Unavailable |
|---|---|---:|---:|---:|---:|
| exact | event log | 768 | 768 | 0 | 0 |
| exact | full snapshot | 768 | 768 | 0 | 0 |
| exact | guarded polling | 192 | 192 | 0 | 576 |
| exact | unchecked polling | 768 | 192 | 432 | 0 |
| threshold | event log | 768 | 768 | 0 | 0 |
| threshold | full snapshot | 768 | 768 | 0 | 0 |
| threshold | guarded polling | 334 | 334 | 0 | 434 |
| threshold | unchecked polling | 768 | 192 | 40 | 0 |

Guarded polling can certify 142 additional threshold answers between snapshots without learning the exact vector. It still does not fulfill the full-service contract. Interval construction and endpoint-square evaluation are charged; guaranteed partial coverage is not automatically a cheaper full solver.

Unchecked threshold polling has 394 correct outputs on insufficient evidence, and 142 correct outputs with sufficient evidence that this policy never checked/certified. It would be wrong to describe all uncertified outputs as lucky guesses. A genuine pre-result regression caught this reporting distinction; retained RED log: `artifacts/observation_v1-sufficiency-regression-red.txt`.

In the stable n=64 seed=7 exact control, guarded and unchecked polling both cost 2,420 logical units. Guarded interval work replaces the output-copy work it avoids. The unchecked policy happens to be correct but cannot establish stability from its stale snapshot. Equal cost does not imply equivalent service or guarantees.

## Trust, exclusions and limits

All source writes participate in atomic source logging. Checkpoints and recovery snapshots are fresh, authentic, synchronous and reliably delivered by assumption. Events alone may be dropped. Sequence gaps catch interior and trailing omissions, with paid authoritative snapshot recovery. This does not solve bypass writes, forged/stale checkpoints, asynchronous races, checkpoint/snapshot loss, cryptographic authentication or adversarial source completeness. Authentication/key management costs are excluded, not secretly charged as one comparison.

Fixture RNG/initial source construction, instrumentation, audit copying, receipt serialization, Python allocation and real network/OS/energy costs are excluded. The declared fused `total = total - old_square + new_square` is one accumulator mutation; squares are separately counted. Unlike history v1's corrected defect, there are not two separately executed accumulator mutations priced as one. Every listed observation counter was independently reconstructed by the parent audit.

No world-distribution optimum, AI learning result, hardware benchmark, complexity-class change or external-action permission follows.

## Verification and reproduction

- Parent repository run: **76 tests passed**, retained in `artifacts/situated_v1-full-tests.txt`.
- `tests/test_situated_receipt_audit.py` imports no experiment modules: reconstructs consumer cache from received events/snapshots, all declared observation counters, actual truth and compatible-world sufficiency, policy aggregates, source hashes and replay pairs.
- Original/repeat/parent JSON all byte-identical; SHA-256 `f0897e62eb45249a7decc8b4a20300e06a4547f360e310074b6d8c30c097a82a`.
- Original: `artifacts/observation_v1.json`; repeat: `artifacts/observation_v1-repeat.json`; parent: `artifacts/observation_v1-parent.json`.
- Source, protocol, freeze file, runner and test hashes embedded; imported module checked against this checkout. Existing outputs refused.

```sh
PYTHONPATH=src python3 scripts/run_observation.py --output artifacts/observation_v1-local.json
PYTHONPATH=src python3 -m unittest discover -s tests -v
```

Use a fresh output path. Earlier history/gate/graph receipts are preserved unchanged.
