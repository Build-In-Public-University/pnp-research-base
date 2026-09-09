# History sufficiency theorem and calibration v1

For contract `G`, let `R(h)` be a retained representation of history `h`. If there exist histories `h1,h2` such that `R(h1)=R(h2)` but `G(h1) != G(h2)`, then no checker `v(R(h))` can be exact for both histories: identical input requires identical output.

The experiment constructs two release histories with identical current manifest and compatibility bytes. One has a valid migration receipt bound to the previous manifest; the other does not. The transition contract accepts only the witnessed history.

Compare current-state-only, complete event log, explicit transition record, trusted digest summary, and minimal contract state. Report representation bytes, maintenance bytes, query bytes, equality across the witness pair, and exactness. Current-state-only is the coarsening expected to fail. Digest and minimal-state representations are trusted retained-state controls, not self-authenticating proofs.

This is a finite logical witness for the declared contract, plus local representation-cost measurements. It is not a claim that one representation is universally minimal or that any P/NP boundary follows.
