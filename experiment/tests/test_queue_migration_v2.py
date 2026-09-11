"""Tests for queue-migration v2."""

import unittest

from pnp_architecture.queue_migration_v2 import SEEDS, STAGES, audit_record, run


class QueueMigrationV2Tests(unittest.TestCase):
    def test_seeded_run_is_deterministic(self):
        self.assertEqual(run(), run())

    def test_independent_audit_passes_every_record(self):
        receipt = run()
        self.assertEqual(receipt["independent_audit"]["status"], "passed")
        self.assertEqual(len(receipt["conditions"]), 8 * len(SEEDS))
        for record in receipt["conditions"]:
            audit_record(record)

    def test_release_ladder_localizes_each_stage_for_all_seeds(self):
        receipt = run()
        for stage in ("evaluation", "integration", "maintenance", "retirement"):
            rows = [
                row for row in receipt["conditions"]
                if row["condition"] == f"capacity_ladder_{stage}"
            ]
            self.assertEqual(len(rows), len(SEEDS))
            self.assertTrue(all(row["bottleneck_by_max_queue"] == stage for row in rows))

    def test_generation_sweep_exposes_evaluation_at_high_rate(self):
        receipt = run()
        rows = [
            row for row in receipt["conditions"]
            if row["condition"] == "generation_sweep_r8"
        ]
        self.assertTrue(all(row["bottleneck_by_max_queue"] == "evaluation" for row in rows))
        self.assertTrue(all(row["arrival_stationarity_diagnostic"] for row in rows))

    def test_stage_schema_and_finite_metrics(self):
        receipt = run(horizon=20)
        for record in receipt["conditions"]:
            self.assertEqual([row["stage"] for row in record["stages"]], list(STAGES))
            for row in record["stages"]:
                self.assertGreaterEqual(row["mean_wait_ticks"], 0.0)
                self.assertGreaterEqual(row["average_queue"], 0.0)
                self.assertGreaterEqual(row["throughput_per_tick"], 0.0)


if __name__ == "__main__":
    unittest.main()
