# Archive and publication boundary

Status: LOCAL REVIEW DRAFT. No remote or publication approval.

## What this is

An export of the available user, assistant and tool records in one research session, including inactive and compacted historical rows, plus its eight directly linked child sessions. Parent cutoff: record 686233, the request to make this archive. Subsequent archive-building exchanges are deliberately outside that frozen cutoff.

The database retains original historical rows alongside compacted/replayed rows. The export does not silently deduplicate these: IDs, timestamps and active/compacted flags remain available. Five context-summary records remain in JSONL but are omitted from the readable dialogue to reduce repetition. `active` is storage state at export time, not a measure of evidentiary validity.

This is NOT a byte-exact unredacted transcript. Redactions replace recognized secrets, partially masked credential fragments, home paths, and IPv4 addresses. The matching rules are heuristic and may also remove benign lookalikes. The original session database is untouched and is not copied into this repository.

## Deliberate exclusions

- System/developer prompts, hidden reasoning and private reasoning metadata.
- Operational skill-result bodies, which can contain unrelated private-project examples. Invocations remain in tool-call records. Skills are workflow context, not research source papers.
- Global configuration, credentials, the session database, unrelated sessions and private infrastructure files.
- Full source-repository Git history: this archive contains a sanitized working-tree snapshot at the recorded commit, not all previous versions.
- Unavailable bytes behind already truncated tool results. A retained compaction summary is not a replacement for a missing original.

The main four PDFs, their extracted text, three user-supplied P/NP notes, generated analysis reports, historical blog/Clay extraction results, review outputs and the completed experiment snapshot are included. `sources/read-inventory.json` records direct read-file calls detectable in stored tool arguments; it is not exhaustive of embedded Python reads, shell reads, browser interactions or references mentioned in prose. Old session excerpts returned by session_search may remain as quoted tool evidence; they are not complete exports of those other sessions.

## Source fidelity

`manifest.json` records source and exported hashes separately for copied files. `transformed: true` means exported bytes differ. Historical receipt hashes inside the experiment describe the original artifacts and are intentionally not rewritten to pretend redaction never happened. Use the outer manifest for exported-byte integrity.

The copied source documents are current on-disk versions. Their presence does not establish that every byte was identical when first read. Historical tool results provide an additional, sometimes truncated, observation. Web files preserve the historical extraction outputs; they are not full site crawls or fresh downloads.

PDF binaries are copied unchanged and are NOT covered by text-only credential scrubbing. Available extracted text is scanned separately. PDF metadata, annotations, embedded files and third-party author contacts need human review before publication.

## Before any push

1. Review the redacted conversation for incidental personal/third-party/private information that pattern scanners cannot classify.
2. Confirm permission or an appropriate redistribution basis for every third-party PDF, quoted page and source note; otherwise replace the relevant copy with a citation and mark the omission.
3. Inspect the complete Git tracked tree and rerun manifest/tests/scanning.
4. Choose and explicitly approve the repository owner, name and visibility.
5. Only then create/push a remote and independently verify the delivered commit.

A scanner pass is not public-release approval. A local commit is not publication. Claims about mathematical validity require independent adjudication; passing the experiment suite tests the bounded implemented models only.
