# Adaptive observation-policy calibration v1: results

Four synthetic hidden states must be identified exactly. The channels expose different partitions:

- `local_parity`, cost 1;
- `local_group`, cost 3;
- `privileged_exact`, cost 6.

Passive observation returns `nominal` for every state and provides no identifying information.

The bounded finite search found:

| Policy | Cost | Exact identification |
|---|---:|---|
| Passive | 0 | no |
| `local_group` then `local_parity` | 4 | yes |
| `privileged_exact` | 6 | yes |

Either coarse channel alone is insufficient. Their complementary partitions jointly identify all four states. The two-channel route therefore beats privileged exact observation under the declared modeled costs.

The route is a valid adaptive policy; it happens not to branch after the first observation in this fixture. The search enumerates finite channel sequences up to length three, so it is not a general optimal-policy solver for arbitrary observation trees.

The result supports:

\[
\boxed{
\pi_G^*=\arg\min_\pi C_O(\pi)\quad\text{subject to contract-relative identifiability}
}
\]

for this finite fixture and channel set. It also illustrates that observation value is contract-relative: a channel can add distinctions without being necessary for the declared decision, while two individually insufficient channels can be jointly sufficient.

All energy/state labels and costs are synthetic modeled values. This is not hardware telemetry and does not establish actual energy savings.
