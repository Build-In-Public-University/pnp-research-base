import unittest
from pnp_architecture.physical_architecture_benchmark_v1 import benchmark
class PhysicalBenchmarkTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.r=benchmark((8,32),(1,10),seed=7)
 def test_matrix_and_exactness(self):self.assertEqual(len(self.r['rows']),16);self.assertTrue(all(x['exact'] for x in self.r['rows']))
 def test_profiles_are_measured(self):
  self.assertTrue(all(x['wall_ns_median']>0 and x['cpu_ns_median']>0 and x['repetitions']==3 for x in self.r['rows']))
 def test_counter_query_not_scan_in_logical_bytes(self):
  for n in (8,32):
   raw=next(x for x in self.r['rows'] if x['n']==n and x['architecture']=='raw_mask' and x['query_update_ratio']==10)
   cnt=next(x for x in self.r['rows'] if x['n']==n and x['architecture']=='mask_counter' and x['query_update_ratio']==10)
   self.assertLess(cnt['logical_read_bytes'],raw['logical_read_bytes'])
if __name__=='__main__':unittest.main()
