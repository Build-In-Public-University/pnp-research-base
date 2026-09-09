import hashlib,json,tempfile,unittest
from pathlib import Path
from pnp_architecture.interaction_v1 import run_cell
class InteractionTests(unittest.TestCase):
 def fixture(self):
  t=tempfile.TemporaryDirectory();r=Path(t.name);fs=[]
  for i in range(12):
   p=r/f'f{i}.txt';p.write_text(str(i));fs.append({'path':p.name,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
  (r/'manifest.json').write_text(json.dumps({'files':fs}));return t,r
 def test_controls_and_joint_cone(self):
  t,r=self.fixture();a=run_cell(r,'adjacent',4);b=run_cell(r,'joint',4);t.cleanup()
  self.assertEqual(a['interaction_nodes'],0);self.assertEqual(b['interaction_nodes'],1)
  self.assertTrue(b['arms']['interaction_aware_repair']['mechanically_exact'])
  self.assertFalse(b['arms']['union_repair']['mechanically_exact'])
 def test_disjoint_has_no_joint_interaction(self):
  t,r=self.fixture();x=run_cell(r,'disjoint',2);t.cleanup()
  self.assertEqual(x['interaction_nodes'],0);self.assertTrue(x['arms']['union_repair']['mechanically_exact'])
if __name__=='__main__':unittest.main()
