"""Tests for the queue-migration synthetic instrument."""

import json
import tempfile
import unittest
from pathlib import Path

from pnp_architecture.queue_migration_v1 import STAGES, run


class QueueMigrationV1Tests(unittest.TestCase):
    def test_receipt_is_deterministic(self):
        self.assertEqual(run(20), run(20))

    def test_all_conditions_drain(self):
        receipt = run(20)
        self.assertTrue(all(row["drained"] for row in receipt["conditions"]))
        self.assertTrue(all(row["generated"] == row["completed"] for row in receipt["conditions"]))

    def test_capacity_release_ladder_localizes_each_bottleneck(self):
        receipt = run(20)
        ladder = {
            row["condition"]: row["bottleneck_by_max_queue"]
            for row in receipt["conditions"]
            if row["family"] == "capacity_release_ladder"
        }
        for stage in ("evaluation", "integration", "maintenance", "retirement"):
            self.assertEqual(ladder[f"capacity_ladder_{stage}"], stage)

    def test_generation_sweep_exposes_downstream_pressure(self):
        receipt = run(20)
        sweep = {
            row["condition"]: row
            for row in receipt["conditions"]
            if row["family"] == "generation_sweep_fixed_downstream"
        }
        self.assertEqual(sweep["generation_sweep_r1"]["bottleneck_by_max_queue"], "generation")
        self.assertEqual(sweep["generation_sweep_r8"]["bottleneck_by_max_queue"], "evaluation")
        self.assertGreater(
            next(x["max_queue"] for x in sweep["generation_sweep_r8"]["stages"] if x["stage"] == "evaluation"),
            0,
        )

    def test_stage_schema_is_explicit(self):
        receipt = run(5)
        self.assertEqual(receipt["stages"], list(STAGES))
        for row in receipt["conditions"]:
            self.assertEqual([x["stage"] for x in row["stages"]], list(STAGES))
            self.assertEqual(set(row["capacities"]), set(STAGES))


if __name__ == "__main__":
    unittest.main()
