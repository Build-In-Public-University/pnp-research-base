# Fixed-contract representation architecture calibration v1

Hold the n-bit unresolved-obligation contract fixed and compare representations only: raw mask, mask plus unresolved-count index, sparse unresolved set, and append-only event log with replay.

For each n in 1..8, run a deterministic workload that invalidates and satisfies each obligation, and compare every architecture's decision with the direct mask oracle after every event. Report retained semantic/index bytes, update work, global decision work, observation work, and evidence work.

The mask+counter architecture retains redundant derived state. The sparse set preserves the same semantic mask in a different representation. The event log retains observations but reconstructs the current mask at query time. Costs are explicit modeled units, not wall-clock benchmarks.
