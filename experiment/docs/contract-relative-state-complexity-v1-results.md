# Contract-relative state complexity v1: results

For the recursive release contract, future-equivalence classes are represented by the reachable states:

\[
Q=\{\texttt{clean},\texttt{migration\_missing},\texttt{migration\_satisfied}\}.
\]

All three are reachable. Each pair has a shortest distinguishing continuation of length at most one event. Histories mapped to the same state have identical bounded future signatures through length 6, across 19,531 event sequences.

Therefore, for this finite contract:

\[
K_G=3
\]

and the ideal fixed-length semantic state requirement is:

\[
I_G=\lceil\log_2 3\rceil=2\text{ bits}.
\]

## Modeled lifecycle comparison

| Architecture | Retained bytes | Observation/event | Update/event | Decision/query | Evidence/update |
|---|---:|---:|---:|---:|---:|
| current state only | 18 | 1 | 1 | 1 | 0 |
| event log | 186 | 1 | 1 | 1 | 2 |
| semantic state | 19 | 1 | 1 | 1 | 1 |
| trusted state code | 1 | 1 | 1 | 1 | 1 |

The lifecycle numbers are modeled unit counters, not wall-clock timings. They expose the dimensions that a real implementation would need to measure: observation, state update, contract decision, and evidence maintenance.

The one-byte code is a byte-aligned encoding of three semantic states. It is not the information-theoretic minimum and is not self-authenticating. A two-bit packed representation is the ideal fixed-length bound for this finite state set.

The central quantity is contract-relative:

\[
K_G=|H/\!\sim_G|.
\]

It is not a property of “history” in isolation. Changing the contract changes the equivalence relation and may change the required retained state.

This is a finite-state result for the declared release contract. It is not a universal complexity measure and does not imply a P/NP result.
