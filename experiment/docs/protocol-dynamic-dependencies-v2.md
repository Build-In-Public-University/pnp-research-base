# Dynamic dependency repair v2: delayed validation and consequences

This extension keeps dynamic dependency v1 unchanged and adds a consequence layer.

## Question

When a dependency certificate is partial or delayed, when does validation become worth its modeled cost once stale reuse can cause downstream repair?

## Policies

- `selective_repair`: repairs from the visible dependency view only.
- `certificate_repair`: validates the actual dependency digest on every update.
- `delayed_certificate`: validates only at the declared certificate interval and uses visible selective repair between certificates.
- `unchecked_cache`: reuses without invalidation as an unsafe control.

A stale output is not automatically a failure. For each unsafe reuse, the frozen fixture applies a deterministic stale-failure rule based on seed, time, and output index. A stale failure then incurs a declared downstream-repair penalty. This is a synthetic consequence model, not an incident probability or application loss estimate.

## Sweep and accounting

The runner varies state churn, graph churn, hidden drift, certificate interval, stale-failure probability, and downstream penalty. Validation cost, repair work, stale failures, and downstream consequence cost are reported separately. The break-even surface is `certificate_total - selective_total < 0` under the same cell and penalty.

The falsifiers are: validation never becomes preferable under any disclosed penalty; delayed validation cannot reduce unsafe reuse relative to selective repair; or the result disappears when the same workload is replayed with independent seeds. A zero-drift/no-hidden-change control must show validation as a pure modeled cost.

All results remain bounded to the synthetic dependency system. No P/NP, deployment, runtime, energy, or causal application claim follows.
