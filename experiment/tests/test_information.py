import unittest
from itertools import product
from pnp_architecture.information import response_map, enumerate_oracle, experiment

class InformationTests(unittest.TestCase):
    def test_hidden_distinction(self):
        self.assertIsNone(response_map([0,0], [1,2], 7))
        self.assertEqual(response_map([0,1], [1,2], 7), {0:0,1:1})

    def test_pairwise_intersection_is_insufficient(self):
        allowed=[3,6,5]
        self.assertTrue(all(a&b for a,b in zip(allowed,allowed[1:]+allowed[:1])))
        self.assertIsNone(response_map([0,0,0], allowed, 7))

    def test_deferral_requires_contract_and_permission(self):
        self.assertEqual(response_map([0,0], [5,6], 7), {0:2})
        self.assertIsNone(response_map([0,0], [5,6], 3))
        self.assertIsNone(response_map([0,0], [1,2], 7))

    def test_exact_vs_threshold(self):
        self.assertIsNone(response_map([0,0], [1,2], 7))
        self.assertEqual(response_map([0,0], [2,2], 7), {0:1})
        self.assertIsNone(response_map([0,0,0], [2,2,1], 7))

    def test_oracle_and_sweep(self):
        self.assertTrue(enumerate_oracle([0,1], [1,2], 7))
        self.assertFalse(enumerate_oracle([0,0], [1,2], 7))
        result=experiment()
        self.assertEqual(result['binary']['cases'], len(list(product((0,1),repeat=4)))**2)
        self.assertEqual(result['relational']['cases'], 8*8**3*8)
        self.assertEqual(result['binary']['disagreements'], 0)
        self.assertEqual(result['relational']['disagreements'], 0)

    def test_invalid_input(self):
        for obs,allowed,feasible in [([],[],7),([0],[8],7),([2],[1],7),([0],[1],8),([0,0],[1],7)]:
            with self.assertRaises(ValueError): response_map(obs,allowed,feasible)

    def test_cli_provenance_replay_and_no_overwrite(self):
        import os,sys,json,subprocess,tempfile
        from pathlib import Path
        root=Path(__file__).resolve().parents[1]
        with tempfile.TemporaryDirectory() as tmp:
            contents=[]
            cmd=[]
            env=dict(os.environ,PYTHONPATH=str(root/'src'))
            for i in range(2):
                p=Path(tmp)/f'{i}.json'; s=p.with_suffix('.md')
                cmd=[sys.executable,str(root/'scripts/run_information.py'),'--output',str(p),'--summary',str(s)]
                run=subprocess.run(cmd,env=env,capture_output=True)
                self.assertEqual(run.returncode,0,run.stderr.decode())
                contents.append(p.read_bytes())
                self.assertEqual(json.loads(p.read_text())['relational']['disagreements'],0)
            self.assertEqual(*contents)
            self.assertNotEqual(subprocess.run(cmd,env=env,capture_output=True).returncode,0)
