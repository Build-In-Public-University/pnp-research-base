"""Measured local calibration for manifest integrity validation."""
import hashlib
import json
import os
import shutil
import tempfile
import time
from pathlib import Path


def ns(fn):
    start = time.perf_counter_ns(); value = fn(); return value, time.perf_counter_ns() - start


def digest(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def selected_files(root, limit=24):
    manifest = json.loads((root / "manifest.json").read_text())
    return [e for e in manifest["files"] if (root / e["path"]).is_file()][:limit]


def run_calibration(root, limit=24, updates=4):
    root = Path(root).resolve()
    entries = selected_files(root, limit)
    if len(entries) < 4 or updates < 1:
        raise ValueError("calibration needs at least four files and one update")
    with tempfile.TemporaryDirectory(prefix="manifest-calibration-") as tmp:
        work = Path(tmp)
        for entry in entries:
            dest = work / entry["path"]; dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(root / entry["path"], dest)
        expected = {e["path"]: e["sha256"] for e in entries}
        baseline = dict(expected)
        results = {"full_recompute": [], "indexed_incremental": []}
        # Controlled one-file updates. The public source remains untouched.
        update_paths = [entries[i % len(entries)]["path"] for i in range(updates)]
        for update_no, changed in enumerate(update_paths, 1):
            path = work / changed
            with open(path, "ab") as f: f.write(f"\\ncalibration-update-{update_no}".encode())
            expected[changed] = digest(path)
            for arm in results:
                counters = {"files_discovered": 0, "files_hashed": 0, "invalidated_records": 0,
                            "repaired_records": 0, "certificate_bytes": 0, "transport_bytes": 0}
                timings = {}
                paths = [e["path"] for e in entries]
                _, timings["dependency_discovery_ns"] = ns(lambda: [p for p in paths if (work / p).is_file()])
                if arm == "indexed_incremental":
                    index, timings["graph_index_construction_ns"] = ns(lambda: {p: p for p in paths})
                    previous = baseline
                    _, timings["update_detection_ns"] = ns(lambda: [p for p in paths if digest(work / p) != previous[p]])
                    changed_paths = [changed]
                else:
                    index = None; timings["graph_index_construction_ns"] = 0
                    changed_paths = paths
                    timings["update_detection_ns"] = 0
                counters["files_discovered"] = len(paths); counters["files_hashed"] = len(changed_paths)
                counters["invalidated_records"] = len(changed_paths); counters["repaired_records"] = len(changed_paths)
                _, timings["invalidation_ns"] = ns(lambda: list(changed_paths))
                records = {}
                _, timings["repair_ns"] = ns(lambda: None)
                for p in changed_paths: records[p] = digest(work / p)
                payload = json.dumps(records, sort_keys=True, separators=(",", ":")).encode()
                counters["certificate_bytes"] = len(payload)
                _, timings["certificate_production_ns"] = ns(lambda: hashlib.sha256(payload).hexdigest())
                certificate = hashlib.sha256(payload).hexdigest()
                _, timings["certificate_validation_ns"] = ns(lambda: hashlib.sha256(payload).hexdigest() == certificate)
                _, timings["transport_serialization_ns"] = ns(lambda: json.dumps({"certificate": certificate}).encode())
                counters["transport_bytes"] = len(json.dumps({"certificate": certificate}).encode())
                _, timings["full_verification_ns"] = ns(lambda: all(digest(work / p) == expected[p] for p in paths))
                counters["full_verification_files"] = len(paths)
                results[arm].append({"update": update_no, "changed_path": changed, "timings_ns": timings, "counters": counters,
                                     "mechanically_exact": all(digest(work / p) == expected[p] for p in paths)})
        return {"status": "measured_local_calibration", "application": "archive_manifest_integrity",
                "entries": len(entries), "updates": updates, "arms": results,
                "boundary": "Machine-local wall-clock measurements over temporary copies; not distributed or universal evidence."}
