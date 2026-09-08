# Stored dialogue

Context summaries are in records.jsonl, not repeated here. Inactive historical rows and replayed text are retained; ordering is database ID order, not deduplicated chronology.

## Record 685486 — user

Stored active=1; compacted=0.

Read-only adversarial review of <HOME>/pnp-network-architecture/src/pnp_architecture/history.py, scripts/run_history.py, tests/test_history.py and docs/protocol-history-v1.md. Do not edit or run external calls. Check hidden observation leaks, counter accounting consistency (declared proxy not real time), correctness oracle, misleading consequence eligibility, omissions that materially affect claims. Return only concrete bugs or limits, with file/function reference. Parent already ran 38 tests. This is a finite dynamic polynomial computation with result-cache policies, not P/NP, no universal theorem. Keep scope tight.

## Record 685496 — assistant

Stored active=1; compacted=0.

- **Counter granularity is inconsistent for total updates.** `history.py:Engine.update` (106–111) performs two mutations of `self.result['total']` (`-= old`, then `+= new`) but charges one `total_read` and one `total_write`. This could intentionally represent a fused read/compute/write operation, but neither code nor protocol declares that convention. Under the stated reads/writes accounting, these are undercounted; the ambiguity also affects counter reweighting and break-even prices. This is a proxy-definition issue, not a runtime claim.

- **The hidden-observation regression does not exercise the dangerous repair path.** `tests/test_history.py:test_hidden_mutation_not_leaked` supplies an empty feed, so `Engine.update` never evaluates a dirty output. It would still pass if dirty-output repair were changed to read omniscient `state`. Add a case with a delivered mutation and an omitted mutation sharing a subproblem. The current implementation correctly uses `self.cached`; the limit is that the advertised regression does not protect that behavior.

- **Receipt source hashes need not describe the executed implementation.** `scripts/run_history.py` imports `experiment` through normal package resolution (7), but `main` hashes the repository-local `history.py` (66). An installed or differently resolved `pnp_architecture` can therefore execute while the receipt identifies this checkout’s source. `test_cli_replay_readback_and_overwrite` forces the correct `PYTHONPATH`, so it cannot detect this mismatch. Resolve and verify the imported module path before recording provenance.

- **The printed consequence summary omits strict-correctness winners.** `history.py:surface` retains `strict_correctness_winners` in JSON, but `scripts/run_history.py:summary` (42–53) aggregates only unrestricted priced winners. Its caveats are accurate, yet a reader of the Markdown alone cannot see the corresponding eligible winners required by `docs/protocol-history-v1.md:30`. The earlier cold-versus-snapshot comparison is not a substitute: it excludes other retrospectively exact policies.
