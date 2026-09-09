# Overlapping updates calibration v1

Use 12 copied archive-manifest files and 12 derived records. Each derived record joins `j` contiguous base inputs (`j=1,2,4`). Mutate one of four predeclared update sets: `single=(0)`, `disjoint=(0,6)`, `adjacent=(0,1)`, and `cluster=(0,1,2,3)`, in a temporary copy.

For each changed base, derive its reverse-index affected set. Compare the sum of isolated affected-set sizes with the size of their union. Full recomputation repairs all derived records; indexed repair repairs the union. Report index edges, changed inputs, isolated sum, union size, overlap savings, edge checks, assurance scope, and mechanical exactness against an independent oracle.

Falsifiers: incremental results are not exact; union accounting disagrees with independently reconstructed affected sets; or overlap savings are reported when the dependency sets do not overlap. Full assurance remains distinct from affected-only assurance. Timing is local diagnostic data only; this is not a universal runtime or P/NP claim.
