# History sufficiency theorem and calibration v1: results

The experiment constructs two release histories with identical current manifest and compatibility digests:

- `missing`: both inputs changed, no migration evidence;
- `satisfied`: both inputs changed, migration evidence bound to the previous manifest.

The contract outcomes are different: reject versus accept.

## Theorem

Let `R(h)` be a retained representation of history `h`. If there exist histories `h1,h2` such that:

\[
R(h_1)=R(h_2)
\quad\text{and}\quad
G(h_1)\ne G(h_2),
\]

then no checker of the form `v(R(h))` can be exact for both histories. It receives identical inputs and must produce identical outputs.

The `current_only` representation is the witness. It is identical for the two histories at 162 bytes, while the oracle outcomes are `False, True`. This establishes final-state insufficiency for the declared release contract. No additional computation over that representation can recover the missing distinction.

## Retained representations

| Representation | Same for witness pair | Distinguishes outcomes | Missing bytes | Satisfied bytes |
|---|---|---|---:|---:|
| current only | yes | no | 162 | 162 |
| complete event log | no | yes | 186 | 185 |
| explicit transition record | no | yes | 194 | 255 |
| trusted digest summary | no | yes | 64 | 64 |
| minimal contract state | no | yes | 17 | 19 |

The digest summary and minimal-state rows are trusted retained-state controls. Their compactness does not make them self-authenticating; production use would need integrity protection and a defined update/validation process.

The minimal state is a contract-specific state machine value: `migration_missing` or `migration_satisfied`. It is small because this contract only distinguishes those two obligations. A different contract may require a larger retained state.

## Interpretation

The result changes the design question from “should the system retain history?” to:

\[
H_G^* = \arg\min_H C_{\mathrm{maintain}}(H)
\quad\text{s.t.}\quad
(S_t,H)\text{ is sufficient for }G.
\]

For this contract, current files alone are insufficient; a small contract-specific historical summary is sufficient in the fixture. The experiment measures representation bytes and logical exactness, not a universal minimum, information-theoretic lower bound, or production storage cost.

This theorem is conditional on the declared contract. It is not a P/NP result.

## Reproduction

```sh
PYTHONPATH=src python3 -m unittest tests.test_history_sufficiency_v1 -q
PYTHONPATH=src python3 scripts/run_history_sufficiency_v1.py \
  --output artifacts/history_sufficiency_v1_local.json \
  --summary artifacts/history_sufficiency_v1_local.md
```
