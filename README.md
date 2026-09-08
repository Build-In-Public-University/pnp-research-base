# From forced-fluid claims to situated computation

LOCAL REVIEW DRAFT — NOT APPROVED FOR PUBLICATION.

This repository packages a research conversation, its available source documents, and a runnable snapshot of the experiments for independent analysis. It is not a proof of a Millennium Prize result, a certification of the papers, or a production trust-system benchmark.

The research progressed from forced-fluid paper reviews and comparison with an earlier blog post to P/NP distinctions, architecture-relative costs, incremental computation, observation sufficiency, and shared validation. The proposed correlated-error/containment experiment was **not implemented** before this archive request.

## Read in this order

1. `conversation/dialogue.md` — human-facing parent conversation; summaries labeled separately.
2. `conversation/records.jsonl` — parent user/assistant/tool records, including compacted/inactive rows.
3. `conversation/subagents/` — separately labeled child-session records.
4. `sources/` — supplied papers, notes, reports, historical web extractions, and source inventory.
5. `experiment/docs/situated-v1-results.md` — latest completed experiment synthesis.
6. `experiment/docs/history-v1.1-results.md` — corrected history accounting; v1 is superseded.
7. `ARCHIVE-BOUNDARY.md`, `manifest.json`, and `verification/` — scope, redaction, provenance and verification.

## Reproduce the completed experiment tests

```sh
cd experiment
PYTHONPATH=src python3 -m unittest discover -s tests -v
```

Use the original experiment README for runners. Choose fresh output paths. Some historical receipts contain normalized local path metadata; source and exported hashes are recorded separately. Do not interpret sanitized receipt bytes as unchanged originals.

## Independent analysis questions

- Which claims are supported by executed predicates, and which remain assigned arithmetic or speculation?
- Are observation, maintenance, evidence production, communication and recovery charged fairly?
- Where do corrected counters reverse conclusions?
- Are retrospective correctness, guaranteed correctness and service coverage kept separate?
- Does a trusted attestation establish truth, or only transfer reliance on a particular validator?
- Does any proposed loss model actually penalize correlated failure, rather than only marginal expected errors?
- Which statements about the fluid papers require independent formal verification?

Conversation records are evidence of what was said, not proof that each statement was true. Tool records may contain failed calls, stale claims, truncated output and duplicated context. Preserve those limitations during analysis.

## Publication

No remote is configured or pushed. Third-party PDFs, quoted web text, personal source notes, and the redacted conversation still require publication review. No blanket license is granted over third-party material. See `RIGHTS.md`.

This export is a frozen cutoff at the user's archive request, not a promise to contain future messages about making this archive.
