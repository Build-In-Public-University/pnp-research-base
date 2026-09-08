# Protocol v0.1

Status: prospective; synthetic fixture.

## Estimand

Primary estimand: architecture delta in total lifecycle operations for the same certificate-bearing problem instance, controlling for local verification operations.

`total_lifecycle_ops = local_verify_ops + transport_ops + coordination_ops + reproduction_ops + revalidation_ops + review_ops`

Secondary estimand: whether `network_ops = total_lifecycle_ops - local_verify_ops` varies by architecture and graph topology.

## Fixed elements

- same abstract certificate relation;
- same certificate length;
- same problem size;
- same graph node set and dependency edges per topology;
- deterministic execution;
- no provider, model, or human data.

## Varied elements

- architecture topology: centralized, chain, star, dense;
- replication factor;
- validation rounds;
- communication latency units;
- review burden units.

## Controls

- centralized architecture with one verifier;
- same instance evaluated under every architecture;
- graph work reported separately from local checking;
- no composite score used for the primary interpretation.

## Falsifiers

1. Network operations do not vary across architectures.
2. The variation disappears after controlling for local verification work.
3. A trivial centralized baseline dominates every architecture at equal correctness.
4. Network operations are not independently defined and are only renamed runtime.
5. The instrument cannot distinguish a chain from a star or dense graph.

## Evidence boundary

Passing tests prove the instrument's bookkeeping. Passing synthetic runs do not establish a property of real research networks, human teams, or complexity classes.
