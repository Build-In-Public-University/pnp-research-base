"""Post-run audit outside the frozen trajectory generator; no changed primary inputs."""
import random
import unittest
from pnp_architecture.history import Engine, oracle


class HistoryPropertyTests(unittest.TestCase):
    def test_arbitrary_replacements_full_observation(self):
        rng = random.Random(2026)
        state = [rng.randrange(4) for _ in range(16)]
        snapshot = Engine('incremental_snapshot', state)
        feed = Engine('incremental_feed', state)
        for _ in range(200):
            indices = rng.sample(range(16), rng.randrange(17))
            for j in indices:
                state[j] = rng.randrange(4)
            events = [(j, state[j]) for j in indices]
            snapshot.update(state, events)
            feed.update(state, events)
            self.assertEqual(snapshot.result, oracle(state))
            self.assertEqual(feed.result, oracle(state))

    def test_partial_feed_computes_only_observed_cache(self):
        rng = random.Random(2027)
        state = [rng.randrange(4) for _ in range(16)]
        expected_cached = list(state)
        policy = Engine('incremental_feed', state)
        for _ in range(200):
            events = []
            for j in rng.sample(range(16), rng.randrange(17)):
                state[j] = rng.randrange(4)
                if rng.randrange(2):
                    events.append((j, state[j]))
                    expected_cached[j] = state[j]
            policy.update(state, events)
            self.assertEqual(policy.result, oracle(expected_cached))


if __name__ == '__main__':
    unittest.main()
