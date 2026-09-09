import tempfile
import unittest
from pathlib import Path

from pnp_architecture.calibration_v1 import run_calibration


class CalibrationTests(unittest.TestCase):
    def test_measured_replay_is_exact_and_incremental_hashes_less(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "manifest.json").write_text('{"files": []}')
            # Use a real temporary fixture with valid manifest records.
            files = []
            import hashlib
            for name in ("a.txt", "b.txt", "c.txt", "d.txt"):
                p = root / name; p.write_text(name * 3)
                files.append({"path": name, "bytes": p.stat().st_size, "sha256": hashlib.sha256(p.read_bytes()).hexdigest()})
            (root / "manifest.json").write_text(__import__("json").dumps({"files": files}))
            receipt = run_calibration(root, limit=4, updates=2)
        self.assertEqual(receipt["status"], "measured_local_calibration")
        self.assertEqual(len(receipt["arms"]["full_recompute"]), 2)
        self.assertTrue(all(r["mechanically_exact"] for arm in receipt["arms"].values() for r in arm))
        self.assertTrue(all(r["counters"]["files_hashed"] == 1 for r in receipt["arms"]["indexed_incremental"]))
        self.assertTrue(all(r["counters"]["files_hashed"] == 4 for r in receipt["arms"]["full_recompute"]))
        self.assertTrue(all(r["counters"]["certificate_bytes"] > 0 for r in receipt["arms"]["indexed_incremental"]))


if __name__ == "__main__":
    unittest.main()
