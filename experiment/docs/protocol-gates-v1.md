# Gate pilot v1: frozen before execution

Boundary: deterministic synthetic candidates, real Python predicates, DECLARED gate cost units (not measured runtime or energy). No AI providers, external actions, confidence scores or new P/NP claims.

Candidate has payload and target. Syntax gate requires payload list of exact ints and exact int target (bool excluded). Local gate requires all payload entries nonnegative. Composition gate requires sum(payload)==target. Acceptance requires all three. Syntax must precede other gates; local and composition reorderable. Costs: syntax=1, local=2, composition=5. Fixed costs deliberately ignore data-dependent check duration. Keep gate calls and modeled cost separate.

Four fixture candidate templates: valid [1,2], target 3; syntax-invalid 'bad', target 3; local-invalid [-1,2], target 1; composition-invalid [1,2], target 4. A both-invalid [-1,2], target 4 supports a correlated fixture.

Workloads, deterministic repetition counts in template order:
- local_heavy: valid 10, syntax 10, local 70, composition 10.
- composition_heavy: valid 10, syntax 10, local 10, composition 70.
- all_valid: valid 100.
- correlated: valid 10, syntax 10, local 10, composition 10, both 60.

Compare legal orders syntax/local/composition and syntax/composition/local. Also full-check control: syntax first; evaluate both remaining gates if syntax passes, regardless of first failure. Do not evaluate undefined predicates after syntax failure. Compare all acceptance vectors to independent oracle. Neither observed rejection rate nor model cost can replace mandatory checks.

Charge c_i on each actual gate invocation. Retain per-candidate gate sequence, rejection/acceptance and costs. Expected cost is computed independently from reached counts: sum c_i * reached_i / candidate_count. Enumerate both legal orders, record all ties, label best as retrospective oracle for these candidate sets. Transfer the best local_heavy order unchanged to composition_heavy; no training or router benefit claimed. No adaptive policy or price fitting.

Predictions before run: cheap-first wins local_heavy, loses composition_heavy; all_valid ties; full-check control preserves acceptance but spends unnecessary checks on some rejected candidates. Correlated failures do not permit independence assumptions. Failure to match oracle invalidates efficiency interpretation.

Tests: mandatory syntax ordering, malformed candidate safety, real predicate checks, same acceptances, cheap-first counterexample, never skipping a necessary check for acceptance, deterministic output and cost identity. Source/config/protocol hashes and explicit input records in receipt. Runner refuses overwrite; repeat to fresh paths and compare bytes. Preserve older v2 receipts unchanged.
