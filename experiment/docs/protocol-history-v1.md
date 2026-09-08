# History applicability experiment v1 — prospective protocol

## Question and boundary

Does retained intermediate state change future work, and when does applicability checking/repair outweigh recomputation? This is a bounded executed dynamic computation, NOT SAT discovery, AI training, real CI, physical energy, a universal caching theorem or a P/NP result. Result caches and learned policies are different forms of history; this experiment tests the former. The earlier gate transfer experiment addresses a fixed policy's workload sensitivity, not online learning.

No policy is required to win. Preserve unfavorable outcomes. 'Maintenance has nonzero cost' is not universal: immutable results, external guarantees and already-performed checking can remove a per-use charge. This protocol deliberately charges explicit inspection of mutable data.

## Instances and global output contract

For n=16,64, form n shared subproblems. Subproblem i uses variables (i+j) mod n for j=0..3 and returns y_i = sum x_j^2 over those dependencies. Global total z=sum_i y_i; decision accept iff z <= 4*n. Return vector y, z and decision. Fresh correctness means all three equal independently computed current-state oracle. A cached total can agree accidentally even when y differs; record vector errors too. All initial variables zero. This is a straightforward polynomial computation with overlapping dependencies. A specialized symbolic simplification is possible; no algorithmic optimality claim is made.

Each trajectory has the cold initialization and 32 updates. At each step increment k distinct seeded-sampled inputs modulo 4, k in {0,1,n//4,n}. Seeds 1,7,19; n/changes/seed grid yields 24 underlying trajectories. Compare full event feed versus omitted feed (only even-index changed variables reported): 48 cells. Generate identical underlying states across feed conditions, no additional RNG draws. World generation, truth-oracle work and receipt serialization excluded and labeled.

## Policies

- cold: recompute all subproblem values and total directly from current full state each step. No persistent application cache.
- incremental_snapshot: charge initial reverse-dependency index and state snapshot; on every update read and compare EVERY input, update cached values, traverse reverse dependencies and deduplicate affected subproblems; recompute only dirty outputs, update total by subtract-old/add-new, check acceptance. Full observation is an explicit capability, charged by per-input reads/comparisons.
- unchecked: initialize once, then return cached result with one cache lookup each step; never detect updates. This is an unsafe experimental control, not deployable approval.
- incremental_feed: use identical index/repair mechanism but detect changes only through delivered id/value events. Repair uses its OWN cached values, NEVER omniscient current input. Complete feed should match oracle. Omitted feed can silently retain stale inputs; this isolates applicability of a metadata-based policy. It must not claim complete validation when feed is incomplete. Feed production costs are excluded; feed reads are charged.

All cold setup, snapshot writes, index entries and first solve are charged. Repair counts cached accesses, dirty dependency visits, set insert attempts, arithmetic and writes. Return cached objects without copying; output publication/serialization excluded for ALL policies. Declare counters explicitly; compare a summed unit-cost RAM-like operation proxy, not equal calibrated physical costs. Retain counter vector for reweighting. Oracle compares outputs only AFTER a policy returns and cannot influence policy state.

## Outcomes and consequence surface

For every step retain inputs, feed, returned y/z/decision, counters, independently computed oracle and flags: wrong output, false acceptance, false rejection. Count semantic stale outputs, not merely differing version numbers. Record modeled retained state slots separately from operation counts; no byte-memory claim.

Primary comparison: cold versus incremental_snapshot at equal exact correctness. Secondary: incremental_feed under complete versus omitted observations. Unchecked and omitted-feed cost rankings are NEVER accuracy-equivalent speedups.

For penalty lambda in {0,10,100,1000,10000}, compute whole-trajectory J=charged proxy operations + lambda * wrong-output-count (including initial setup). Unit weights and penalties are SYNTHETIC consequences, not dollars, measured risk or permission to violate correctness. Each wrong output receives deterministic penalty; no invented failure probability. Report all ties and both per-cell winners and strict-correctness-eligible winners. Record exact pairwise break-even lambda between each erroneous policy and the cheaper exact policy if positive; ties/errors zero handled explicitly. False-acceptance counts retained separately from this wrong-output pricing rule.

## Before-run expectations and falsifiers

Incremental_snapshot may win sparse changes but lose dense churn because it pays detection/index/repair overhead; unchecked may win unpriced work while wrong; snapshot should eliminate omitted-feed staleness. No-change costs can favor unchecked and feed reuse. If these do not happen, report results without tuning fixtures. Complete-feed errors or snapshot errors invalidate efficiency claims. Do not characterize drift rates as empirical probabilities or universal bounds.

Tests: direct algebra against independent oracle, shared reverse dependencies, sparse and dense updates, unchanged state, hidden mutation regression (missing feed must not leak current state), vector mismatch despite equal aggregate, initialization charged, counter identities, complete feed matches snapshot, penalty accounting, deterministic runs, fresh-output runner and overwrite refusal. Freeze this file hash before implementation/runs. Keep previous experiment receipts untouched. Source and input hashes in new receipts; two retained byte-identical runs and independent readback.
