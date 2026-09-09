# Dynamic dependencies and selective repair v1

## Question

When cached outputs depend on a changing dependency graph, does selective repair reduce modeled work without accepting stale outputs, and when does full reset become safer or cheaper?

## Frozen comparison

Each world contains base values and derived outputs. A derived output is the sum of the base values named by its dependency tuple. Each step supplies an actual graph and state to an independent oracle. Policies receive a visible graph/version; the certificate policy additionally receives a declared graph digest that represents a validation channel. Hidden drift changes the actual graph while leaving the visible graph/version unchanged.

Policies:

- `cold_recompute`: recompute every output at every step.
- `selective_repair`: compare visible state/graph with retained state and recompute outputs affected by visible changes.
- `full_reset`: rebuild every cached output whenever visible state or graph changes.
- `certificate_repair`: validate the cached graph certificate; on any digest mismatch, identify and repair only affected outputs using the received actual graph.
- `unchecked_cache`: reuse retained outputs without invalidation; unsafe control.

The certificate channel is a modeled input contract, not cryptographic proof of semantic truth. Its digest computation cost is charged separately from output repair. The actual graph remains available to the certificate validator as the declared validation input; ordinary selective repair is deliberately not allowed to inspect hidden graph changes.

## Frozen counters

Counters are listed logical operations, not runtime, energy, money, or hardware measurements:

- `dependency_discovery`: inspect visible/validated dependency metadata;
- `graph_construction`: construct or copy graph state;
- `index_maintenance`: update reverse dependency index;
- `state_read`, `state_compare`, `state_write`;
- `certificate_validation`: compare the retained certificate with the supplied digest;
- `output_validation`: compare/recompute affected output values;
- `output_read`, `output_write`, `add`;
- `cache_lookup`, `stale_acceptance`.

World generation, oracle execution, receipt serialization, and the cost of producing the validation channel are excluded. Costs are reported by category and as a declared unit-weight sum. No policy is required to win.

## Falsifiers and controls

1. Selective repair does not beat cold recomputation under low churn after discovery/index costs are included.
2. Full reset is cheaper than selective repair under high churn.
3. A visible-compatibility control with hidden graph drift is incorrectly accepted by ordinary selective repair.
4. Certificate repair fails to detect that hidden drift or does not restore oracle equality.
5. A zero-drift replay changes because the random generator consumed extra draws.
6. Repeated runs are not byte-identical.

The experiment must retain both favorable and unfavorable cells. Cell counts sharing a generated trajectory are paired observations, not independent samples. Results remain bounded to this synthetic dependency system.
