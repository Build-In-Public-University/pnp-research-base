import json
import unittest

from pnp_architecture.model import Architecture, ProblemInstance, fixture, receipt, run_case


class ModelTests(unittest.TestCase):
    def test_local_relation_is_fixed_across_architectures(self):
        p = ProblemInstance("x", 10, 5, 2)
        rows = [run_case(p, a) for a in fixture()[1]]
        self.assertEqual({r["local_verify_ops"] for r in rows}, {15})
        self.assertTrue(all(r["formal_relation_held_fixed"] for r in rows))

    def test_network_cost_varies_and_centralized_is_minimum_fixture(self):
        data = receipt()
        means = data["summary"]
        self.assertGreater(means["dense"]["mean_network_ops"], means["centralized"]["mean_network_ops"])
        self.assertLess(means["centralized"]["mean_total_lifecycle_ops"], means["chain"]["mean_total_lifecycle_ops"])

    def test_rows_have_separate_cost_components(self):
        data = receipt()
        self.assertEqual(len(data["rows"]), 12)
        for row in data["rows"]:
            components = ["transport_ops", "coordination_ops", "reproduction_ops", "revalidation_ops", "review_ops"]
            self.assertEqual(row["network_ops"], sum(row[k] for k in components))
            self.assertEqual(row["total_lifecycle_ops"], row["local_verify_ops"] + row["network_ops"])

    def test_invalid_problem_rejected(self):
        with self.assertRaises(ValueError):
            run_case(ProblemInstance("bad", 0, 1, 1), fixture()[1][0])

    def test_receipt_is_json_serializable(self):
        json.dumps(receipt())


if __name__ == "__main__":
    unittest.main()
