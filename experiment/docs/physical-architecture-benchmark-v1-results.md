# Physical fixed-contract architecture benchmark v1: results

This is a local-machine calibration of the same n-obligation contract under four representations. It is not an energy measurement, a cache/DRAM measurement, or a hardware-independent complexity theorem.

## Protocol

Sizes: n = 128, 512, 2048, 8192.
Query/update ratios: r = 0.1, 1, 10, 100.
Each cell: deterministic update stream, three timing repetitions, identical oracle and workload per architecture.

Recorded fields:

- median wall-clock nanoseconds;
- median process CPU nanoseconds;
- median tracemalloc peak allocation;
- instrumented logical read/write bytes;
- oracle exactness.

## Observed local boundary

At n=8192 and r=100:

| Architecture | Median wall time |
|---|---:|
| Raw mask | 30.0 ms |
| Mask + counter | 14.8 ms |
| Sparse set | 14.3 ms |
| Event log | 661.7 ms |

At n=128 and r=0.1:

| Architecture | Median wall time |
|---|---:|
| Raw mask | 9.9 µs |
| Mask + counter | 14.3 µs |
| Sparse set | 4.9 µs |
| Event log | 6.5 µs |

The counter is therefore not universally faster. Its extra maintenance and Python-level bookkeeping lose in some small, update-light cells; its constant-time query profile becomes valuable in larger query-heavy cells. The sparse representation wins several cells in this fixture because the workload leaves only a limited set of active obligations and Python set operations are efficient.

The event log confirms the temporal trade: append is simple, but replay cost grows with history and query frequency. At n=8192, r=100, it is more than an order of magnitude slower than the indexed representations in this implementation.

All 64 architecture/cell combinations were oracle-exact. Logical I/O counters are instrumentation: raw-mask reads model packed-mask scan bytes, indexed queries read one counter unit, sparse queries read one set-emptiness unit, and event-log queries charge replayed event records. `tracemalloc` is an allocation proxy, not total resident memory. No package-power or energy counter was used.

## Interpretation

The result supports a bounded claim:

\[
\boxed{
\text{For a fixed exact contract, physical representation and workload jointly determine measured lifecycle cost.}
}
\]

It does not establish a universal winner, a universal crossover, or a P/NP result. The next calibration boundary would be repeated runs across machines and a real energy/thermal counter, if available.
