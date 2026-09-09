import hashlib,json,tempfile,unittest
from pathlib import Path
from pnp_architecture.dense_coupling_v1 import run_join_cell
class DenseJoinTests(unittest.TestCase):
 def test_exactness_and_join_identity(self):
  with tempfile.TemporaryDirectory() as t:
   r=Path(t); fs=[]
   for i in range(12):
    p=r/f'f{i}.txt';p.write_text('file-'+str(i));fs.append({'path':p.name,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
   (r/'manifest.json').write_text(json.dumps({'files':fs}))
   x=run_join_cell(r,fanout=4,join_width=4,assurance='full')
  self.assertTrue(x['arms']['indexed_incremental']['mechanically_exact'])
  self.assertEqual(x['index_edges'],x['derived_nodes']*4)
  self.assertEqual(x['arms']['indexed_incremental']['edge_checks'],x['affected_nodes']*4)
  self.assertEqual(x['arms']['indexed_incremental']['repair_nodes'],4)
 def test_assurance_scope_is_explicit(self):
  with tempfile.TemporaryDirectory() as t:
   r=Path(t); fs=[]
   for i in range(12):
    p=r/f'f{i}.txt';p.write_text(str(i));fs.append({'path':p.name,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
   (r/'manifest.json').write_text(json.dumps({'files':fs}))
   x=run_join_cell(r,2,2,'affected')
  self.assertEqual(x['arms']['indexed_incremental']['assurance_nodes'],2)
  self.assertTrue(x['arms']['indexed_incremental']['mechanically_exact'])
if __name__=='__main__': unittest.main()
