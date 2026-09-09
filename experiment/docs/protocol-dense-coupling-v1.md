# Dense-coupling calibration v1

Use the archive manifest's first 12 files as base inputs. Build 12 derived records with declared join width `j` and fan-out `f`: the first `f` derived records depend on changed base `f0.txt`; every record has exactly `j` parent inputs. Compare full recomputation with indexed incremental repair after mutating only `f0.txt` in a temporary copy.

Report dependency discovery, reverse-index maintenance, edge checks, join-resolution checks, invalidation fan-out, repair nodes, assurance nodes, transport bytes, and mechanical exactness separately. The accounting identities are `index_edges = derived_nodes × join_width`, `affected_nodes = fanout`, and `affected_edge_checks = affected_nodes × join_width`.

Sweep fan-out `1,2,4,8,11`, join width `1,2,4`, and assurance scopes `full,affected`. The independent full oracle validates incremental results. Full assurance remains distinct from affected-only assurance.

Falsifiers: incremental repair is not exact; graph counters violate the declared identities; or low-affected-fraction repair loses its count reduction once join/index costs are charged. This is local calibration evidence, not distributed timing, universal complexity, security, or P/NP evidence.
