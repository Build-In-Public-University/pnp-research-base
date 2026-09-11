"""Tests for the independently specified v3 workload family."""

import unittest

from pnp_architecture.queue_migration_v3_bursty import SEEDS, audit, run


class QueueMigrationV3Tests(unittest.TestCase):
    def test_deterministic(self):
        self.assertEqual(run(), run())

    def test_two_workloads_and_independent_audit(self):
        receipt = run()
        self.assertEqual(receipt["independent_audit"], "passed")
        self.assertEqual(len(receipt["records"]), 2 * 8 * len(SEEDS))
        for row in receipt["records"]:
            audit(row)

    def test_burst_release_ladder_localizes_stage(self):
        receipt = run()
        for workload in ("burst_train", "jittered"):
            for stage in ("evaluation", "integration", "maintenance", "retirement"):
                rows = [
                    row for row in receipt["records"]
                    if row["workload_family"] == workload
                    and row["condition"] == f"capacity_ladder_{stage}"
                ]
                self.assertTrue(rows)
                self.assertTrue(all(row["bottleneck"] == stage for row in rows))

    def test_high_rate_exposes_evaluation(self):
        receipt = run()
        for workload in ("burst_train", "jittered"):
            rows = [
                row for row in receipt["records"]
                if row["workload_family"] == workload
                and row["condition"] == "generation_sweep_r8"
            ]
            self.assertTrue(all(row["bottleneck"] == "evaluation" for row in rows))


if __name__ == "__main__":
    unittest.main()
