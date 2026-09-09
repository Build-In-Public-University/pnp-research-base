import unittest

from pnp_architecture.dynamic import (
    POLICIES,
    DynamicEngine,
    make_trajectory,
    oracle,
    run_cell,
)


class DynamicDependencyTests(unittest.TestCase):
    def test_engine_starts_exact(self):
        first = make_trajectory(8, 1, 7)[0]
        for policy in POLICIES:
            engine = DynamicEngine(policy, first)
            self.assertEqual(engine.result, oracle(first["state"], first["actual_dependencies"]))

    def test_selective_repair_recomputes_only_affected_outputs(self):
        world = make_trajectory(8, 1, 7)
        engine = DynamicEngine("selective_repair", world[0])
        counters = engine.update(world[1])
        self.assertGreater(counters["output_validation"], 0)
        self.assertLess(counters["output_validation"], len(world[0]["actual_dependencies"]))
        self.assertEqual(engine.result, oracle(world[1]["state"], world[1]["actual_dependencies"]))

    def test_full_reset_recomputes_every_output_after_change(self):
        world = make_trajectory(8, 1, 7)
        engine = DynamicEngine("full_reset", world[0])
        counters = engine.update(world[1])
        self.assertEqual(counters["output_validation"], 8)
        self.assertEqual(engine.result, oracle(world[1]["state"], world[1]["actual_dependencies"]))

    def test_hidden_graph_drift_is_stale_for_ordinary_repair(self):
        world = make_trajectory(8, 0, 7, hidden_drift=True)
        engine = DynamicEngine("selective_repair", world[0])
        engine.update(world[1])
        self.assertNotEqual(engine.result, oracle(world[1]["state"], world[1]["actual_dependencies"]))
        self.assertGreater(engine.stale_acceptances, 0)

    def test_certificate_repair_catches_hidden_graph_drift(self):
        world = make_trajectory(8, 0, 7, hidden_drift=True)
        engine = DynamicEngine("certificate_repair", world[0])
        counters = engine.update(world[1])
        self.assertGreater(counters["certificate_validation"], 0)
        self.assertEqual(engine.stale_acceptances, 0)
        self.assertEqual(engine.result, oracle(world[1]["state"], world[1]["actual_dependencies"]))

    def test_unchecked_control_can_accept_stale_output(self):
        world = make_trajectory(8, 0, 7, hidden_drift=True)
        engine = DynamicEngine("unchecked_cache", world[0])
        engine.update(world[1])
        self.assertNotEqual(engine.result, oracle(world[1]["state"], world[1]["actual_dependencies"]))
        self.assertGreater(engine.stale_acceptances, 0)

    def test_zero_drift_is_seed_stable(self):
        self.assertEqual(make_trajectory(8, 1, 19), make_trajectory(8, 1, 19))
        self.assertEqual(make_trajectory(8, 1, 19), make_trajectory(8, 1, 19, hidden_drift=False))

    def test_run_cell_reports_all_policies_and_correctness(self):
        receipt = run_cell(8, 1, 7, hidden_drift=True)
        self.assertEqual(set(receipt["policies"]), set(POLICIES))
        self.assertEqual(receipt["policies"]["cold_recompute"]["wrong_outputs"], 0)
        self.assertEqual(receipt["policies"]["certificate_repair"]["wrong_outputs"], 0)
        self.assertGreater(receipt["policies"]["selective_repair"]["wrong_outputs"], 0)


if __name__ == "__main__":
    unittest.main()
