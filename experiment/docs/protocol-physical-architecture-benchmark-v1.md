# Physical fixed-contract architecture benchmark v1

Hold the n-obligation contract and event semantics fixed while measuring four representations on the local machine: raw mask, mask plus count, sparse unresolved set, and append-only event log with replay.

Frozen workload sizes are n in {128, 512, 2048, 8192}; query/update ratios are {0.1, 1, 10, 100}; event streams are deterministic. Each case runs three timing repetitions. Record wall time, process CPU time, tracemalloc peak allocation, logical bytes read/written, and oracle exactness.

Logical byte counters are instrumentation, not hardware cache or DRAM traffic. tracemalloc is an allocation proxy, not total process memory. Energy and package power are intentionally not reported because no reliable portable counter is assumed on this host. Results are local calibration only.
