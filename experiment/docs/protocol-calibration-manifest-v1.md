# Concrete calibration v1: archive manifest integrity

## Application

The application is integrity validation for this repository archive: a manifest names files, byte counts, and SHA-256 digests. A validator must detect changed files and repair the affected manifest records. The workload is copied into a temporary directory; the public checkout is never modified.

## Arms

- `full_recompute`: parse the manifest and hash every selected file on each update.
- `indexed_incremental`: build a reverse index from file path to manifest record, detect changed paths, invalidate only affected records, and hash only those files.

Both arms validate the resulting selected records against an independently constructed expected digest map. Certificate production hashes the canonical selected-record payload; certificate validation recomputes that digest. Serialized certificate bytes are transport bytes.

## Measured phases

each update reports wall-clock nanoseconds for dependency discovery, graph/index construction, update detection, certificate production, certificate validation, transport serialization, invalidation, repair, and full verification. Counts and bytes are reported beside time; no phase is inferred from a composite score.

## Workload

The runner selects up to 24 existing repository files with manifest records and creates four copied updates. Each update mutates one copied file by appending a marker byte. The changed paths are known only to the update generator; policies discover them through file metadata. The input manifest is unchanged.

## Falsifiers and boundaries

The incremental arm fails this calibration if it does not hash fewer files than full recomputation for one-file updates, or if its repaired records differ from the independent expected map. The result is not evidence about distributed systems, network latency, security guarantees, P/NP, or a universal incremental-validation advantage. Timing is machine-local and should be treated as diagnostic.
