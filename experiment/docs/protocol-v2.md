# Frozen bounded experiment protocol v2

Status: frozen before implementation experiments and result generation. The runner
requires the SHA-256 recorded in `protocol-v2.sha256`; it fails on protocol drift.
No external calls, publication, real parallel hardware, timing, or energy measurements.
The v0.1 model and `artifacts/first_attack.json` remain historical arithmetic-only
fixtures: they did not execute a certificate verifier or a graph traversal.

## 1. Explicit propagation

Nodes are integers 0..N-1, root 0. N = 1,2,4,8,16,32. Undirected simple
edge sets: chain (i-1,i); root-centered star (0,i); balanced binary tree
((i-1)//2,i); complete all i<j; disconnected two chain components split at
N//2 (N=1 is a singleton and connected). Sorted adjacency and iteration order.
Payload lengths 8,16,32,64; identical zero bit strings delivered without corruption.

Synchronous first-arrival flooding: root starts informed; each newly informed node
sends once to ALL neighbors, including its sender; duplicates do not forward again.
All messages in a round are sent before arrival processing. Counters increment in
actual send loops. `rounds` counts nonempty transmission rounds until quiescence
(including final redundant traffic); `delivery_rounds` is last first-arrival round.
Reached nodes and exact per-node payload equality are recorded; all-reached exactness
requires every node. Independent component closure checks reachability.

BFS from root builds a directed spanning tree in sorted order; charge one setup
adjacency inspection per visited neighbor entry (not wall time or network traffic).
Routed propagation traverses only parent-to-child arcs with the same synchronous
engine. For each reuse count 1,4,16 execute that many propagations, sum measured
sends, payload-bit-hops, and rounds; BFS setup is once, reported separately.
Do not add unlike units or count centralized BFS as a free distributed protocol.
Graph generation, memory, headers, contention, queueing, failures and acknowledgments
are outside these counters. Graph edge lists are embedded as input identities.

## 2. Containing constraint

Use every graph/N above. Local predicate: each submitted bit belongs to {0,1}.
Global predicate: every submitted bit valid AND all bits equal. Inputs: all zeros
and zeros with node N-1 set to one. N=1 single-one is consistent, not a conflict.
Local-only checks every bit but makes no justified global decision; its conjunction
is recorded as a naive global prediction for comparison, explicitly not a proof.

Central collector uses root's BFS routing tree. Each reachable node's bit is sent
individually one parent hop per synchronous round until root receives it; no
aggregation. Record hop sends, one-bit payload-bit-hops (node-ID headers excluded),
collection rounds, number received, BFS setup inspections, local inspections and
root equality comparisons. Complete collections compare every non-root bit to root.
Incomplete collections return `unavailable`, even if root's component looks consistent;
no accept/reject is asserted for the whole witness. Independent oracle uses all input
bits, not the routing output, to evaluate the actual global predicate. Report naive
prediction correctness and centralized agreement where available.
Rejecting an inconsistent submitted witness is NOT UNSAT: both all-zero and all-one
assignments satisfy this containing problem for every N in this grid.

## 3. Actual 3-CNF and bounded parallel simulation

Variables n=4,6,8,10,12; three replicates r=0,1,2. Seed = 20260908 + 100*n + r.
Python stdlib Random(seed): generate 4*n clauses, each with three distinct variables
from sample(range(n),3), each sign chosen by randrange(2) (1 means positive).
Represent literals as signed 1-based integers, clause order and literal order fixed.
For each seeded formula also append an explicit UNSAT core: all eight signed triples
on variables 0,1,2 in itertools.product((False,True), repeat=3) order.
Full clauses, seed, literal count, and a declared fixed-width encoding size
(n and m plus signed literal slots, excluding object overhead) are recorded.

Assignment IDs run 0..2**n-1; variable i is bit i (least-significant first).
Verifier short-circuits at first true literal within a clause and first false clause;
count every inspected literal. Enumerate ALL assignments to record exact truth table
and per-assignment inspection counts. Independently check with non-short-circuit
clause sums; oracle work is excluded from measured search work, explicitly.

Then re-execute first-success enumeration in contiguous batches with p=1,n,2**n.
All candidates in the winning batch finish and are charged; pick the smallest
satisfying assignment ID. Report processor budget, candidates, batches, total literal
inspections, and idealized makespan = sum of maximum candidate inspections in each
executed batch. Returned witness is separately verified and verification inspections
reported (not silently included in search). Exhaustion without a witness is UNSAT
for this concrete finite formula and is checked against the exhaustive oracle.
No real parallel hardware used. Formula distribution/replication, scheduling,
assignment generation, communication, idle processors and verification of UNSAT
proofs are excluded from the makespan. Input size includes clauses, not just n.
No SAT lower bound or P/NP separation can be inferred from brute-force enumeration.

## Artifacts and checks

Tests are written before implementation: edge sets, reachability, send/bit-hop and
round counters, reuse accounting, consistency/unavailability, verifier and batch
scheduler (including work for later candidates in a winning batch). Run full unittest
with PYTHONPATH=src. Runner writes deterministic JSON and a summary derived solely
from its outputs. Embed complete config/inputs, canonical JSON input hashes, protocol
hash, and SHA-256 of module, runner, tests, old model/receipt and CLI. No timestamps
or host-specific paths in deterministic data. Run twice to separate output paths and
compare bytes; retain both receipts and summaries. Old receipts must not be overwritten.
All conclusions are finite synthetic algorithm observations; negative/null results
are valid. In particular a tree route can erase flood send differences while retaining
depth differences, and large processor budgets can increase total work.
