# P/NP research: representations, evidence, and public contribution

This repository is an open exploration of the P versus NP problem and of the representations we use to study it.

The mission is not to announce a solution. It is to make the problem more inspectable: to examine how different representations—formal, computational, informational, observational, historical, and organizational—make different features of the problem visible, measurable, or easy to miss.

A representation is not the thing itself. It is an instrument. Each instrument gives access to some questions while imposing boundaries on others. Comparing representations can therefore teach us not only about a proposed mechanism, but about the structure of the problem and the limits of the instrument doing the observing.

## What this repository is for

This is a public workspace for:

- preserving the conversation and source artifacts that motivated the exploration;
- implementing small, bounded, inspectable computational models;
- testing invariants, counterexamples, failure modes, and accounting assumptions;
- comparing what different representations reveal, suppress, or confuse;
- inviting public critique, replication, alternative encodings, and new experiments;
- keeping claims proportional to the evidence available.

Contributions are welcome when they make the problem clearer. Useful contributions may be a counterexample, a sharper definition, an alternative representation, a reproduced receipt, a failed approach, a correction, a new test, or a better explanation of what an artifact does not establish.

## Evidence boundary

The repository separates four things that are easy to collapse:

1. **Prose and questions** — hypotheses, interpretations, and research directions.
2. **Executable mechanisms** — code and tests that establish behavior for bounded models.
3. **Synthetic experiments** — deterministic fixtures that compare declared conditions under explicit assumptions.
4. **Mathematical results** — claims requiring independent proof or adjudication beyond this repository's finite runs.

Passing tests demonstrates software behavior. A finite experiment does not establish a universal theorem, a complexity-class separation, or a solution to P/NP. Architecture-relative cost observations are kept separate from standard asymptotic complexity claims.

## Repository contents

- `conversation/` — the archived parent conversation and available child-session records.
- `sources/` — source documents, historical web extractions, reviews, and provenance inventory.
- `experiment/` — executable bounded models, protocols, tests, and receipts.
- `scripts/` — tooling used to assemble, normalize, and verify the archive.
- `verification/` — sanitizer, experiment, integrity, and publication receipts.
- `manifest.json` — the machine-readable archive inventory and file hashes.
- `ARCHIVE-BOUNDARY.md` — inclusion, exclusion, and provenance limits.
- `RIGHTS.md` — attribution and source-release notes.

## Current status

- Public repository: `Build-In-Public-University/pnp-research-base`.
- The archive contains 1,190 parent-session records and the available linked child sessions.
- The bounded experiment snapshot currently passes 76 tests.
- The archive sanitizer suite currently passes 6 tests.
- The local and public manifests are hash-verified.
- The included experiments are bounded and synthetic unless an artifact explicitly says otherwise.
- No claim here should be read as a claimed solution to P/NP.

## How to contribute

Start with the evidence boundary. State:

- which representation you are using;
- what question it makes visible;
- what it leaves out;
- what would falsify the interpretation;
- whether the result is a definition, implementation check, synthetic experiment, or mathematical argument.

Prefer small, reproducible changes. Include tests or a machine-readable receipt where appropriate. Preserve failed results and unresolved cases; they are part of the map. Do not replace an earlier receipt silently—add a correction or a new version and explain the difference.

## Reproduce the current checks

From the repository root:

```bash
python3 -m unittest discover -s tests -q
```

For the experiment snapshot:

```bash
cd experiment
PYTHONPATH=src python3 -m unittest discover -s tests -q
```

These commands verify the bounded implementation. They do not validate the research thesis by themselves.
