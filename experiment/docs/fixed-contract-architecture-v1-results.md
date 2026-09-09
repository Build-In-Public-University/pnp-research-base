# Fixed-contract architecture calibration v1: results

The contract is held fixed: an n-bit unresolved-obligation mask, with one event changing one obligation and `inspect` accepting exactly when no obligation remains.

## Architecture result

| Architecture | Retained state | Single update | Global decision | Evidence |
|---|---|---:|---:|---:|
| Raw mask | n bits | 1 modeled unit | n-bit scan | 0 modeled units |
| Mask + count | n + ceil(log2(n+1)) bits | 1 | 1 | 1 |
| Sparse unresolved set | fixed-width set estimate | 1 | 1 | 1 |
| Event log | event history | append 1 | replay history | 2 |

All architectures were exact against the direct mask oracle over the deterministic workload for n=1 through 8:

```text
invalidate all obligations
satisfy all obligations in reverse order
inspect
```

The mask-plus-counter architecture adds redundant retained state but changes the global decision from a scan to a constant-time count check. It does not replace the mask: two masks with equal unresolved counts can react differently to a future `satisfy_i` event.

The sparse set preserves the semantic mask while changing its physical representation. Its memory estimate depends on the number and encoding of unresolved identifiers; the receipt uses a worst-case fixed-width index estimate.

The event log retains observations rather than a current semantic summary. It has simple append updates but pays replay cost at decision time.

## Interpretation

For the same exact contract and semantic state complexity:

\[
\boxed{
\text{representation architecture changes lifecycle costs without changing }G
}
\]

The comparison is a resource vector, not a single ranking. Deliberate redundancy can reduce query cost while increasing retained state and evidence maintenance. Compression can reduce state size while increasing reconstruction cost. These are modeled unit costs, not wall-clock timings, and no architecture is universally Pareto-optimal without workload weights.

The experiment does not claim that the counter is sufficient for recursive state by itself. The mask remains necessary for obligation-specific future events; the counter is a materialized view for the current global query.

No P/NP conclusion follows.
