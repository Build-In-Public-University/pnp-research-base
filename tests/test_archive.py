import sys
from pathlib import Path
import unittest
sys.path.insert(0, str(Path(__file__).resolve().parents[1]/'scripts'))
from archive_tools import sanitize

class Sanitation(unittest.TestCase):
    def test_vendor_secret(self):
        value='sk-'+'A'*30
        self.assertNotIn(value,sanitize(value))
    def test_bearer(self):
        self.assertNotIn('opaqueCredentialValue',sanitize('Authorization: Bearer '+'opaqueCredentialValue'))
    def test_assignment(self):
        self.assertNotIn('someOpaqueSecretValue',sanitize('API_'+'KEY='+chr(34)+'someOpaqueSecretValue'+chr(34)))
    def test_paths(self):
        self.assertEqual(sanitize('/Users/alice/project'), '<HOME>/project')
    def test_math(self):
        self.assertEqual(sanitize('512 -> 8; E[L] = N*p*l'), '512 -> 8; E[L] = N*p*l')
    def test_idempotence(self):
        x='sk-'+'B'*30
        self.assertEqual(sanitize(sanitize(x)),sanitize(x))

if __name__=='__main__': unittest.main()
