# Lessons from “pnp p2” Feedback

Source: `<HOME>/Downloads/pnp p2 .md`

## What the feedback gets right

### 1. Separate local certificate verification from network certificate lifecycle

The first receipt held local verification at 168 while architecture-conditioned lifecycle cost varied. The useful decomposition is:

`C_lifecycle = C_discovery + C_verify + C_coordinate + C_reproduce + C_revalidate`

For the current fixture, the narrower decomposition is:

`C_total = C_local_verify + C_network_lifecycle`

The network term should mean the cost of making a local result usable as shared state: transport, coordination, reproduction, revalidation, dependency repair, and review.

Do not call this “local truth versus network truth.” The instrument does not establish a different truth value. It establishes different costs and obligations around accepting and maintaining a certificate.

### 2. Scale two variables independently

One size gives constants. The next experiment needs at least:

- `n`: input/problem size;
- `N`: network or architecture size.

Measure `C(A, n, N)` over a grid rather than reporting only four architectures at one fixture size. This allows us to distinguish:

- costs growing with the problem;
- costs growing with the network;
- interaction costs between problem and network;
- topology effects at fixed N;
- replication and validation effects.

The initial grid can use small deterministic values such as `n ∈ {8, 16, 32, 64}` and `N ∈ {1, 2, 4, 8, 16}`. The exact values are a protocol choice, not evidence by themselves.

### 3. Test separability rather than assume it

The feedback proposes that discovery, verification, and coordination may move independently. That is a good hypothesis, not a result.

The benchmark should vary them through matched interventions:

- hold certificate and verifier fixed while changing topology;
- hold topology fixed while changing certificate size;
- hold topology and certificate fixed while changing revalidation rounds;
- introduce dependency changes and measure repair separately.

The desired output is a component-wise surface, not one composite score.

### 4. Architecture-relative classes are possible but dangerous

A provisional class could be written as:

`P_A = { L : C_A(L,n) is polynomial in n }`

But this is meaningful only after specifying:

- the architecture family A;
- permitted hardware growth;
- total work versus latency;
- communication model;
- memory model;
- certificate and validation protocol;
- whether A is fixed, uniform, or nonuniform;
- how A is described and generated;
- the simulation relation to a standard model.

Otherwise one can manufacture a class by assigning a favorable cost function or giving the architecture an uncharged oracle.

## What the feedback overclaims

### Star versus dense cannot yet identify graph connectivity

The feedback observes network costs of 576 and 584 and infers that connectivity is not the primary variable. That inference is premature.

The current instrument does not represent the actual edge set of each architecture. The `dependency_edges` field is a property of the problem instance and is held at the same value across architectures. The dense architecture differs through manually assigned `communication_hops` and `review_units`, not through a mechanically traversed dense graph.

Therefore the 8-operation gap says only:

> Under the current cost function, the named star and dense parameter bundles differ by 8 mean operations.

It does not say that physical/logical edge count is unimportant.

Required repair: represent each architecture as an explicit graph and derive edge checks, fan-out, fan-in, depth, and propagation from that graph. Then compare star and dense at equal N, equal problem, equal certificate, and equal validation policy.

### “Three times” is descriptive, not asymptotic

The first result has a roughly 3.48× dense/centralized network-cost ratio. That is a finite-fixture ratio. It is not evidence for an asymptotic separation or a new complexity class.

### The current experiment does not yet show global consistency

It measures declared coordination and revalidation counters. It does not yet implement conflicting certificates, inconsistent replicas, hidden dependencies, or a global acceptance predicate. “Global consistency” must become an explicit state transition with failure cases.

## Revised research claim

The most defensible current claim is:

> For a fixed certificate relation and declared lifecycle protocol, local verification work and network lifecycle work are separable accounting components. The latter may vary with architecture even when the former is unchanged.

A stronger prospective claim is:

> Under a fixed, explicit architecture and resource model, the same locally verifiable relation can have different asymptotic lifecycle costs as a function of problem size and network size.

This remains compatible with standard P/NP. It becomes a new complexity-theoretic result only if the architecture model, uniformity, resource accounting, and simulation relationship are formalized.

## Next experiment specification

### Phase A: scaling without topology ambiguity

Sweep `n` and `N` for centralized, chain, and star architectures using explicit generated graphs. Keep dense out until its edge set is implemented rather than named.

For every cell record:

- local verification operations;
- candidate/discovery work;
- graph edge checks;
- propagation depth/iterations;
- communication operations;
- independent reproduction operations;
- revalidation operations;
- review/coordination operations;
- total lifecycle operations;
- correctness and exactness state.

### Phase B: topology controls

At fixed `N`, compare:

- chain: depth N, low fan-out;
- star: depth 2, high fan-out;
- balanced tree: intermediate depth/fan-out;
- dense: explicit high edge count;
- disconnected control: no cross-node dependencies.

Test whether edge count, diameter, maximum degree, graph depth, or dependency cut size best predicts the measured network term.

### Phase C: containing-problem attack

Introduce a global constraint that depends on multiple local certificates. Compare:

- independent local validation;
- centralized global validation;
- distributed consistency checking;
- an intentionally conflicting-certificate case.

This is the first place where “the containing problem dictates whether subproblem solutions are acceptable” becomes an executable mechanism rather than a metaphor.

## Falsifiers added by the feedback

1. After explicit graph construction, topology metrics explain no additional variance beyond node count and replication.
2. Scaling in N vanishes when coordination and communication are charged honestly.
3. Discovery, verification, and coordination cannot be independently manipulated or observed.
4. A proposed `P_A` distinction disappears under a polynomial simulation with the same resource accounting.
5. Global consistency costs are always reducible to independent local verification with no additional state or communication.

## Bottom line

The feedback improves the research program by moving it from a single architecture comparison toward a two-dimensional scaling experiment and a component-wise lifecycle model.

Its most important warning is implicit: do not infer graph laws from a fixture that has not actually encoded the graph. The machine is willing to flatter us. The receipt is not.
