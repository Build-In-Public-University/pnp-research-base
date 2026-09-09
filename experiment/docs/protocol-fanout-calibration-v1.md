# Fan-out calibration v1 protocol

Calibrate archive-manifest dependency geometry using 12 copied base files, fan-outs `1,2,4,8,11`, depths `1,2,4`, and assurance scopes `full,affected`. Mutate only base file `f0.txt` in a temporary copy. Derived graph nodes are recomputed through the declared transitive fan-out branch.

Primary outputs are total derived nodes, affected nodes, affected fraction rho, repair-node counts, assurance-node counts, transport bytes, wall-clock repair/assurance timings, and mechanical exactness against an independent full oracle. Compare full recomputation against indexed incremental repair. The archive checkout is read-only for the run.

The falsifiers are: incremental repair is not exact, declared affected counts do not match the graph closure, or its repair reduction disappears at low affected fraction. Full assurance is intentionally retained as a separate scope; affected-only assurance is not equivalent to global assurance.

This is a measured local temporary-file calibration, not distributed, runtime-general, energy, security, or P/NP evidence.
