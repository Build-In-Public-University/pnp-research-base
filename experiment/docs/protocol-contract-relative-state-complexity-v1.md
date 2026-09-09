# Contract-relative state complexity calibration v1

For a contract `G`, define history equivalence by future behavior:

`h1 ~G h2` iff every permissible continuation has the same contract observations from both histories.

Define `K_G` as the number of reachable equivalence classes and `I_G = ceil(log2 K_G)` as the ideal fixed-length semantic state bits. This protocol uses the recursive release machine from `recursive_history_v1.py`, whose states and event alphabet are frozen there.

Enumerate histories through length 6, assign each history its reachable semantic state, and verify that histories with the same state have identical bounded continuation signatures. Find shortest event sequences distinguishing every pair of states. Report lifecycle counters per event for full-log, semantic-state, and trusted-code representations: observation, update, decision, evidence, and retained-state bytes.

The receipt estimates the finite contract's state complexity and modeled lifecycle work. It is not a universal complexity measure, an information lower bound beyond the finite machine, or a P/NP claim.
