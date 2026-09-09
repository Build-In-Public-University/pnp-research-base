# Recursive history sufficiency v1: results

This experiment promotes the release contract to a finite observed transition system with states:

- `clean`;
- `migration_missing`;
- `migration_satisfied`.

Events are `inspect`, `approve`, `joint_release`, `joint_release_with_migration`, and `reset`.

## Three sufficiency tests

Decision sufficiency:

\[
G(h)=v(R(h)).
\]

Update sufficiency:

\[
R(ho)=U(R(h),o).
\]

Continuation sufficiency:

\[
R(h_1)=R(h_2)\Rightarrow\forall u,\;G(h_1u)=G(h_2u).
\]

The implementation factors both observation and update through the three-state semantic representation. Because both functions depend only on the retained state and next event, continuation sufficiency follows by induction over every finite continuation. Exhaustive enumeration through length 6 provides a bounded regression receipt: 19,531 sequences.

## Representation comparison

| Representation | Serialized bytes | Distinct values |
|---|---:|---|
| Current-state-only | 18 | no: same-current-files |
| Semantic state strings | 19 | clean, migration_missing, migration_satisfied |
| Serialized state strings | 19 | clean, migration_missing, migration_satisfied |
| Trusted state code | 1 | 00, 01, 02 |
| Semantic state code | 1 | 0, 1, 2 |

The one-byte code is a semantic compression result, not an authenticity result. It requires a trusted update mechanism and integrity protection if used operationally.

The finite machine has three future-distinguishable states, so an ideal fixed-length encoding requires at least:

\[
\lceil\log_2 3\rceil=2\text{ bits}.
\]

The one-byte executable code is a convenient byte-aligned encoding, not the information-theoretic minimum.

The result is contract-specific and does not establish a universal minimal automaton for release systems or any P/NP claim.
