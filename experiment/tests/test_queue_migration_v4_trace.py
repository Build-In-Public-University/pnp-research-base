"""Tests for the trace-derived queue-migration calibration."""

import unittest
from pathlib import Path

from pnp_architecture.queue_migration_v4_trace import TRACE_SHA256, audit, load_trace, run


TRACE = Path(__file__).parents[2] / "conversation" / "records.jsonl"


class QueueMigrationV4Tests(unittest.TestCase):
    def test_manifest_anchored_trace_hash_and_metadata_only_load(self):
        trace = load_trace(TRACE)
        self.assertEqual(trace["source_sha256"], TRACE_SHA256)
        self.assertEqual(trace["record_count"], 1190)
        self.assertEqual(trace["arrival_total"], 1190)
        self.assertEqual(trace["role_counts"]["user"], 51)
        self.assertNotIn("content", trace)

    def test_trace_replay_is_deterministic_and_audited(self):
        first = run(TRACE)
        second = run(TRACE)
        self.assertEqual(first, second)
        self.assertEqual(len(first["conditions"]), 8)
        for row in first["conditions"]:
            audit(row)

    def test_generation_capacity_sweep_and_release_ladder(self):
        receipt = run(TRACE)
        for cap in (1, 2, 4):
            row = next(x for x in receipt["conditions"] if x["condition"] == f"generation_sweep_cap{cap}")
            self.assertEqual(row["bottleneck"], "generation")
        high = next(x for x in receipt["conditions"] if x["condition"] == "generation_sweep_cap8")
        self.assertEqual(high["bottleneck"], "evaluation")
        for stage in ("evaluation", "integration", "maintenance", "retirement"):
            row = next(x for x in receipt["conditions"] if x["condition"] == f"capacity_ladder_{stage}")
            self.assertEqual(row["bottleneck"], stage)


if __name__ == "__main__":
    unittest.main()
