# Formal boundary and correction to the initial result

## Correction

The initial first_attack.json is preserved as arithmetic bookkeeping, not evidence from an executed certificate checker or network. Its local_verify_ops was input_length + certificate_length. Its topology labels were hand-selected parameter bundles, and validation, replication, and review changed together. Therefore its variation was built into the formula. Calling this a partial empirical hit for the thesis was too strong. Neither a graph effect nor a verifier invariant was discovered by that run.

A prior module smoke invocation also lacked a __main__ call; successful exit alone did not prove that invocation generated its output. Fresh-output verification is required.

## What the next tests can establish

Explicit finite graphs and exact boolean certificates let us compare implemented protocols at matched correctness. Such experiments can expose resource accounting errors and protocol tradeoffs. They do not establish unknown asymptotic lower bounds. Input bit length, vertex count, edge count, number of candidate assignments, memory, and network rounds must not collapse into one unweighted 'energy' score.

The same network can run a wasteful algorithm or an efficient algorithm. A slow run under architecture A does not prove a language is outside an architecture-relative polynomial class. Membership quantifies over eligible algorithms; nonmembership requires a lower bound for all such algorithms, not an exponential example. Architecture families must be uniform or explicitly account for advice, construction, memory, and processor count.

Polynomial growth measured on a finite grid is not a proof. For an explicit protocol, loop analysis may supply a bound; it is still a protocol bound, not a problem lower bound. Brute-force SAT enumeration has exponential candidate space, but that cannot establish that every SAT algorithm needs exponential work.

## The containing problem distinction

If each local clause has some satisfying assignment, the conjunction need not have a common satisfying assignment. This is a quantifier distinction:

for every clause, there exists a local assignment

is different from:

there exists one assignment satisfying every clause.

A consistency check of supplied assignments is not the search for some globally consistent assignment. Rejecting inconsistent local witnesses does not prove the global formula unsatisfiable. Keeping these separate is essential to the proposed research direction.

Likewise, an isolated verifier may lack enough messages to decide global acceptance; this is unavailable information, not an exponentially hard local calculation. A disconnected protocol must abstain rather than silently count partial reachability as success.

## Predicted outcomes, before the new receipt

- Flooding versus a compiled spanning tree can exchange setup work, repeated send work, and depth; they may tie on trees.
- More edges can reduce round depth while increasing redundant traffic for a particular flooding protocol.
- Disconnected graphs cannot distribute a certificate to unreachable nodes under an edge-only protocol.
- Local validity can coexist with globally conflicting submitted certificates.
- Parallel enumeration can reduce idealized latency without eliminating enumeration work; early stopping may make greater parallelism waste work in the winning batch.

These are baseline sanity predictions, not novel claims. A failed prediction should trigger an instrument or model audit before theoretical interpretation. Physical energy, actual distributed hardware speedups, dynamic drift, and novel complexity-class separations remain untested.
