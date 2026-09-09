import unittest

from pnp_architecture.dynamic_v2 import (
    CONSEQUENCE_PENALTIES,
    consequence_surface,
    run_consequence_cell,
)


class DynamicConsequenceTests(unittest.TestCase):
    def test_certificate_is_exact_under_hidden_drift(self):
        receipt = run_consequence_cell(8, 1, 7, cert_interval=1, hidden_drift=True)
        result = receipt["policies"]["certificate_repair"]
        self.assertEqual(result["wrong_outputs"], 0)
        self.assertEqual(result["unsafe_reuse"], 0)

    def test_delayed_certificate_has_partial_availability(self):
        receipt = run_consequence_cell(8, 1, 7, cert_interval=3, hidden_drift=True)
        result = receipt["policies"]["delayed_certificate"]
        self.assertGreater(result["certificate_unavailable"], 0)
        self.assertGreater(result["unsafe_reuse"], 0)
        self.assertLess(result["unsafe_reuse"], receipt["policies"]["unchecked_cache"]["unsafe_reuse"])

    def test_consequence_cost_is_penalty_times_failures(self):
        receipt = run_consequence_cell(8, 1, 7, cert_interval=3, hidden_drift=True, stale_failure_rate=1, downstream_penalty=37)
        result = receipt["policies"]["delayed_certificate"]
        self.assertEqual(result["consequence_cost"], result["stale_failures"] * 37)
        self.assertGreater(result["stale_failures"], 0)

    def test_surface_reports_zero_penalty_and_high_penalty(self):
        receipt = run_consequence_cell(8, 1, 7, cert_interval=3, hidden_drift=True, stale_failure_rate=1, downstream_penalty=100)
        surface = consequence_surface(receipt, CONSEQUENCE_PENALTIES)
        self.assertEqual(surface["penalties"], list(CONSEQUENCE_PENALTIES))
        self.assertIn("certificate_repair", surface["rows"][0]["totals"])
        self.assertIn("winners", surface["rows"][-1])

    def test_zero_drift_validation_is_pure_cost(self):
        receipt = run_consequence_cell(8, 1, 7, cert_interval=1, hidden_drift=False)
        cert = receipt["policies"]["certificate_repair"]
        selective = receipt["policies"]["selective_repair"]
        self.assertEqual(cert["unsafe_reuse"], 0)
        self.assertGreater(cert["operations"], selective["operations"])


if __name__ == "__main__":
    unittest.main()
