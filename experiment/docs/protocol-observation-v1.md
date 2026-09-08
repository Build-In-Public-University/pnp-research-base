# Observation-system experiment v1 — prospective local protocol

Frozen before implementation and results; SHA-256 companion verified by runner. This is a local procedural freeze, not externally timestamped preregistration. No network, installs, commits, or production deployment.

## Matched worlds and contracts

Use Python stdlib Random(seed), n in {16,64}, seeds {1,7,19}, changes per tick {0,1,n//4,n}. Initialize each coordinate uniformly from integers [-4,4]. Tick 0 is initial observation; ticks 1..15 choose k distinct indices using sample(range(n),k), sorted for publication; independently choose -1/+1 per index, reflecting inward at domain boundaries -8/+8. Every selected coordinate really changes by exactly one. Preserve all states and update lists. Policies know only n, domain [-8,8], maximum per-coordinate movement 1/tick, clock tick, threshold T=16*n, and their observations; NOT seed, realized change count, random generator, future states or hidden current state. All combinations use the same trajectory across policies, transports and contracts.

Contracts: exact vector, and Boolean sum(x_i^2) >= T. Every tick requests an immediate answer. Unavailable is safe non-emission but NOT service fulfillment. Record emitted, unavailable, wrong emitted, guaranteed emitted and correct-but-not-guaranteed separately. No penalty converts an unsafe answer into authorized correctness.

## Four policies, two transport conditions

1. event_log: all source writes atomically advance sequence and append [seq,index,value]. Every tick publishes authentic fresh [tick,last_seq] after all events, including zero-change ticks. Consumer checks each event sequence against next expected, plus checkpoint tick/sequence, and detects interior/trailing omissions. Any gap causes an authoritative same-tick recovery snapshot [tick,last_seq,vector...]. Partial event repairs before recovery remain charged. Initial snapshot tick 0. Incrementally maintain sum of squares for threshold contract; exact contract carries vector without computing unused squares.
2. full_snapshot: acquire full fresh snapshot each tick, inspect/compare each coordinate and update changed cached entries; same incremental sum maintenance for threshold.
3. poll_unchecked: snapshots at ticks 0,4,8,12; otherwise return cached answer with no freshness proof. Fresh outputs guaranteed, reused outputs explicitly not guaranteed, even when retrospectively correct. Do not let oracle agreement authorize reuse.
4. poll_guarded: same poll schedule. At stale ticks derive each interval [max(-8,cached_i-age), min(8,cached_i+age)]. Exact answer only if every interval singleton. Threshold answer only if sum of coordinate minimum squares >= T or sum of maximum squares < T; otherwise unavailable. Bounds use only cached observed values plus age, never hidden state or realized sparsity. This product domain deliberately does not exploit a promise of k changes because no such promise is supplied to any consumer.

Cross complete event delivery and dropped transport (drop events with sequence divisible by 5; checkpoints and recovery snapshots reliable). Snapshot policies unchanged across transport labels (paired duplicates, not independent evidence). Producer pays logging and sending even dropped events. Fresh checkpoint assumes authenticated, current, atomic source publication and that EVERY write participates. No unlogged bypass-write control, adversarial checkpoint forging, asynchronous races or checkpoint loss in v1. Authentication is an assumed capability, NOT a implemented cryptographic proof; crypto cost excluded. Checkpoints cannot certify bypass writes.

## Executed unit counters and payloads

Each listed action is incremented where executed. Sum counters with weight 1; NOT wall-clock time, CPU instructions, energy, byte cost or optimal implementation. Composite arithmetic operations below are declared logical units. Separate payload counts are integer fields, NOT bytes and NOT added again to operation sum.

- source_write: each actual coordinate assignment (common environment update applied separately per policy); world RNG/generation excluded.
- source_sequence: each increment of logged source sequence.
- source_log_field: each of three fields retained in an event record.
- source_checkpoint_field: each of two fields constructing fresh checkpoint.
- source_snapshot_field: each of tick, sequence and coordinate fields acquired into a snapshot.
- producer_publish_field: each field copied into outgoing wire record (also for dropped events).
- delivery_field: each wire field processed by transport; dropped fields are charged here too.
- receive_field: each delivered field ingested into an incoming record.
- snapshot_compare: each coordinate compared with cache (including initial missing entries).
- cache_write: each initialized/changed cached coordinate, including event repair before snapshot recovery.
- calculation_square: each evaluated square; initial/new and old squares distinct.
- calculation_total_write: initial sum accumulator initialization and each fused assignment total = total - old_square + new_square (one mutation), or initial addition total += square (one mutation). This is explicitly a fused arithmetic abstraction, not two separately executed total mutations.
- sequence_check: each event sequence comparison, plus checkpoint sequence and tick comparisons; snapshot freshness tick check too.
- schedule_check: each periodic poll scheduling decision (including initial tick).
- interval_coordinate: each coordinate interval construction/singleton check, without early exit for exact contract; threshold also calculates minimum/maximum squares (two calculation_square) and accumulates two sums (two calculation_total_write plus their two initializations).
- contract_check: each scalar threshold comparison actually performed; fresh exact has no arithmetic predicate.
- output_field: each emitted vector element or Boolean copied into response; unavailable has zero output fields.

Track sent/delivered/dropped fields and message counts separately; checkpoint/snapshot/event incoming records, recovered flag, cache after processing, age and derived intervals/bounds, decisions, guarantee flags and per-tick counters. Track retained log peak fields and cached vector entries; audit receipts retained by evaluator are excluded memory, not consumer memory. Log holds current-tick records until checkpoint/recovery completes, then drains; reliable synchronous snapshot recovery makes this sufficient.

## Oracle, artifacts, tests and interpretation

Independent evaluator computes truth directly from immutable world state, outside policy objects; policies only receive transport-returned data. Preserve full trajectories, source updates, observed inputs and per-tick decisions/counters. Hash canonical world inputs, frozen protocol, implementation, runner, tests. Before running verify imported observation module resolves to this checkout's exact file. Exclusive-create outputs; refuse overwrite. Run twice to distinct observation_v1 artifact paths and require byte-identical JSON. No timestamps/output paths in deterministic receipt.

Tests first: API failure recorded honestly, then behavioral RED via minimal stubs; test bounds against exhaustive small domains, cold threshold accumulation, delivered-plus-dropped updates and trailing omission recovery, sender/drop/checkpoint charges, zero-change freshness, no hidden-state leakage, unchecked lucky correctness versus sufficient evidence, fail-closed unavailability, deterministic matched suite, provenance rejection and no-overwrite runner. Test only tests/test_observation.py; parent runs broader suite. Preserve genuine regressions for discovered bugs before fixes. Report errors, coverage, guaranteed coverage and full-service strict cost comparisons, including losses. A cheap abstaining policy cannot win a full-service comparison. No universal optimum, real distributed latency, AI learning claim, P/NP consequence or independent population inference follows.
