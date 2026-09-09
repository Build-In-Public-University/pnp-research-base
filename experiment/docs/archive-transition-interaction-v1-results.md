# Archive/release transition interaction calibration v1: results

This is the first application-specific calibration of the synthetic interaction question. The fixture uses the repository archive manifest plus a compatibility declaration as release inputs. Four derived artifacts are modeled:

- `manifest-check`, dependent on the current manifest;
- `compatibility-check`, dependent on the current compatibility declaration;
- `provenance`, a final-state constraint dependent on both current inputs;
- `migration-approval`, a transition constraint activated only when both inputs change in the same release.

## Results

| Release change | Singleton-only | State-complete | Transition-aware | Oracle additions |
|---|---|---|---|---|
| manifest only | exact | exact | exact | manifest-check, provenance |
| compatibility only | exact | exact | exact | compatibility-check, provenance |
| both together | not exact | not exact | exact | migration-approval |

The singleton-only policy represents the union of outputs observed during isolated changes. The state-complete policy adds the correctly indexed final-state factor `provenance`. Neither policy repairs `migration-approval` during the simultaneous release because that artifact is not a function of final state alone in this fixture.

The independent oracle receives previous bytes, current bytes, and the complete change set. When both files change, it activates the explicit transition rule:

\[
(S_{t-1},\Delta S_t,S_t)\rightarrow\text{migration-approval}.
\]

Only the transition-aware policy is exact in that case.

## Interpretation

This separates two explanations for a missed consequence:

1. **Missing state dependency knowledge:** `provenance` would be missed by an incomplete singleton index but is recovered by a complete final-state factor graph.
2. **Transition-relative semantics:** `migration-approval` appears only for the combined release event and requires the previous state plus the change set.

The result supports the second distinction for this explicit archive/release contract. It does not prove that arbitrary semantic systems require hypergraphs, nor does it establish a P/NP result. The transition rule is application-specific and deliberately visible in the protocol.

## Reproduction

```sh
PYTHONPATH=src python3 -m unittest tests.test_archive_transition_v1 -q
PYTHONPATH=src python3 scripts/run_archive_transition_v1.py \
  --output artifacts/archive_transition_v1_local.json \
  --summary artifacts/archive_transition_v1_local.md
```
