import hashlib,json,tempfile,unittest
from pathlib import Path
from pnp_architecture.overlap_v1 import run_cell
class OverlapTests(unittest.TestCase):
 def fixture(self):
  t=tempfile.TemporaryDirectory();r=Path(t.name);fs=[]
  for i in range(12):
   p=r/f'f{i}.txt';p.write_text(str(i));fs.append({'path':p.name,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
  (r/'manifest.json').write_text(json.dumps({'files':fs}));return t,r
 def test_union_is_smaller_for_adjacent_updates(self):
  t,r=self.fixture();x=run_cell(r,'adjacent',4);t.cleanup()
  self.assertGreater(x['overlap_savings'],0);self.assertTrue(x['arms']['indexed_incremental']['mechanically_exact'])
  self.assertEqual(x['union_affected_nodes'],x['arms']['indexed_incremental']['repair_nodes'])
 def test_disjoint_has_no_overlap(self):
  t,r=self.fixture();x=run_cell(r,'disjoint',1);t.cleanup()
  self.assertEqual(x['overlap_savings'],0);self.assertTrue(x['arms']['indexed_incremental']['mechanically_exact'])
if __name__=='__main__':unittest.main()
