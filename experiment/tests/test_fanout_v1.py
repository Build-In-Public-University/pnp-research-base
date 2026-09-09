import json, tempfile, hashlib, unittest
from pathlib import Path
from pnp_architecture.fanout_v1 import build_graph, run_geometry

class FanoutTests(unittest.TestCase):
    def test_graph_has_declared_fanout_and_depth(self):
        self.assertEqual(len(build_graph(12, 4, 3),), 3)
        self.assertEqual(sum(1 for x in build_graph(12, 4, 1)[0] if x[0] == 0), 4)

    def test_incremental_is_exact_and_affected_set_scales(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp); files=[]
            for i in range(12):
                p=root/f'f{i}.txt'; p.write_text(f'file-{i}')
                files.append({'path':p.name,'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
            (root/'manifest.json').write_text(json.dumps({'files':files}))
            low=run_geometry(root,1,2); high=run_geometry(root,11,2)
        for r in (low,high): self.assertTrue(all(x['mechanically_exact'] for x in r['arms'].values()))
        self.assertLess(low['affected_fraction'], high['affected_fraction'])
        self.assertEqual(low['arms']['indexed_incremental']['repair_nodes'],2)
        self.assertEqual(high['arms']['indexed_incremental']['repair_nodes'],22)

if __name__=='__main__': unittest.main()
