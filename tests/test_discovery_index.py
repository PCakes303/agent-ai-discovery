import unittest
from tools.discovery_index import validate
BASE={"discovery_version":"1.0.0","publisher":{"id":"PCakes303","name":"MrCakes931","manifest_uri":"https://example.org/manifest.json"},"generated_at":"2026-11-01T00:00:00Z","resources":[{"id":"agent.one","kind":"agent","name":"One","manifest_uri":"https://example.org/one.json","manifest_version":"1.0.0"}]}
class DiscoveryTests(unittest.TestCase):
 def test_valid(self): self.assertEqual(validate(BASE)["resources"][0]["id"],"agent.one")
 def test_duplicate_id(self):
  d={**BASE,"resources":BASE["resources"]*2}
  with self.assertRaisesRegex(ValueError,"duplicate"): validate(d)
 def test_relative_uri(self):
  d={**BASE,"resources":[{**BASE["resources"][0],"manifest_uri":"/manifest.json"}]}
  with self.assertRaisesRegex(ValueError,"absolute"): validate(d)
 def test_bad_kind(self):
  d={**BASE,"resources":[{**BASE["resources"][0],"kind":"mystery"}]}
  with self.assertRaisesRegex(ValueError,"unsupported"): validate(d)
 def test_unknown_field(self):
  with self.assertRaisesRegex(ValueError,"unknown"): validate({**BASE,"unexpected":True})
if __name__=="__main__": unittest.main()
