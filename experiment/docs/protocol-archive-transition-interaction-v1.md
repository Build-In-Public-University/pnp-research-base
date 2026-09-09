# Archive/release transition interaction calibration v1

Use a temporary release fixture with `manifest.json` and `compatibility.json` as inputs. Derived artifacts are `manifest-check`, `compatibility-check`, `provenance`, and `migration-approval`.

`provenance` is a final-state constraint depending on both input files and therefore belongs to a complete state factor graph. `migration-approval` is a transition constraint: it activates only when both inputs change in the same release and depends on the previous state plus the change set.

Compare three repair policies after isolated manifest, isolated compatibility, and simultaneous changes: `singleton_only` (union of isolated affected outputs), `state_complete` (declared final-state dependencies), and `transition_aware` (state dependencies plus the joint transition rule). Validate every policy against an independent oracle that receives previous bytes, current bytes, and the complete change set.

The falsifier is important: if singleton-only repair misses only `provenance`, the issue is incomplete state indexing; if state-complete repair still misses `migration-approval` while transition-aware repair is exact, the residual is genuinely transition-relative in this fixture. This is application-specific calibration, not a P/NP result or a claim about all release systems.
