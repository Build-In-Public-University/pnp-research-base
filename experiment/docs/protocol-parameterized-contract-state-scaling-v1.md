# Parameterized contract-state scaling v1

For each n, the contract state is an n-bit unresolved-obligation mask. All 2^n masks are reachable from the clean state through `invalidate_i` events. `satisfy_i` clears bit i; `invalidate_i` sets bit i; `inspect` accepts iff the mask is zero.

The intended family has `K_G(n)=2^n` future-distinguishable states and ideal semantic memory `I_G(n)=n` bits. For each n in 1..8, enumerate every state, verify reachability, search shortest distinguishing continuations, and measure modeled update/decision/evidence work. Update touches one bit; decision scans n bits; evidence records n-bit state.

All costs are explicit unit models, not wall-clock claims. The family isolates state-information scaling from transition/update and decision costs; it does not encode a hard update problem or imply a P/NP result.
