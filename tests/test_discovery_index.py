import json
import tempfile
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker
from tools.discovery_index import load_document, validate

ROOT = Path(__file__).resolve().parents[1]
BASE = {
    "discovery_version": "1.0.0",
    "publisher": {"id": "PCakes303", "name": "MrCakes931", "manifest_uri": "https://example.org/manifest.json"},
    "generated_at": "2026-11-01T00:00:00Z",
    "resources": [{"id": "agent.one", "kind": "agent", "name": "One", "manifest_uri": "https://example.org/one.json", "manifest_version": "1.0.0"}],
}
SCHEMA = json.loads((ROOT / "schemas" / "discovery-document.schema.json").read_text(encoding="utf-8"))
Draft202012Validator.check_schema(SCHEMA)
SCHEMA_VALIDATOR = Draft202012Validator(SCHEMA, format_checker=FormatChecker())


class DiscoveryTests(unittest.TestCase):
    def assert_rejected(self, doc):
        with self.assertRaises(ValueError):
            validate(doc)
        self.assertTrue(list(SCHEMA_VALIDATOR.iter_errors(doc)))

    def test_valid_and_schema_agreement(self):
        self.assertEqual(validate(BASE)["resources"][0]["id"], "agent.one")
        self.assertEqual(list(SCHEMA_VALIDATOR.iter_errors(BASE)), [])

    def test_duplicate_resource_id(self):
        with self.assertRaisesRegex(ValueError, "duplicate"):
            validate({**BASE, "resources": BASE["resources"] * 2})

    def test_http_and_relative_uris_rejected(self):
        for uri in ("http://example.org/manifest.json", "/manifest.json"):
            doc = json.loads(json.dumps(BASE))
            doc["resources"][0]["manifest_uri"] = uri
            self.assert_rejected(doc)

    def test_credentials_fragments_and_bad_ports_rejected(self):
        for uri in ("https://user:pass@example.org/manifest.json", "https://example.org/manifest.json#frag", "https://example.org:99999/x"):
            doc = json.loads(json.dumps(BASE))
            doc["resources"][0]["manifest_uri"] = uri
            with self.assertRaises(ValueError):
                validate(doc)

    def test_publisher_types_and_bounds(self):
        for publisher in (
            {**BASE["publisher"], "id": 7},
            {**BASE["publisher"], "name": 7},
            {**BASE["publisher"], "id": "x" * 129},
            {**BASE["publisher"], "name": "n" * 161},
        ):
            self.assert_rejected({**BASE, "publisher": publisher})

    def test_timezone_naive_timestamp_rejected(self):
        self.assert_rejected({**BASE, "generated_at": "2026-11-01T00:00:00"})

    def test_unknown_nested_properties_rejected(self):
        doc = json.loads(json.dumps(BASE))
        doc["publisher"]["extra"] = True
        self.assert_rejected(doc)
        doc = json.loads(json.dumps(BASE))
        doc["resources"][0]["extra"] = True
        self.assert_rejected(doc)

    def test_resource_collection_and_string_bounds(self):
        self.assert_rejected({**BASE, "resources": BASE["resources"] * 513})
        doc = json.loads(json.dumps(BASE))
        doc["resources"][0]["capabilities"] = ["cap"] * 129
        self.assert_rejected(doc)
        doc = json.loads(json.dumps(BASE))
        doc["resources"][0]["tags"] = ["t" * 129]
        self.assert_rejected(doc)

    def test_duplicate_capability_and_tag_values_rejected(self):
        doc = json.loads(json.dumps(BASE))
        doc["resources"][0]["capabilities"] = ["x", "x"]
        self.assert_rejected(doc)
        doc = json.loads(json.dumps(BASE))
        doc["resources"][0]["tags"] = ["x", "x"]
        self.assert_rejected(doc)

    def test_duplicate_json_keys_and_nonstandard_numbers_rejected(self):
        for raw in (
            '{"discovery_version":"1.0.0","discovery_version":"1.0.0"}',
            '{"discovery_version":"1.0.0","publisher":{},"generated_at":"2026-11-01T00:00:00Z","resources":[{"x":NaN}]}',
        ):
            with tempfile.TemporaryDirectory() as tmp:
                path = Path(tmp) / "document.json"
                path.write_text(raw, encoding="utf-8")
                with self.assertRaises(ValueError):
                    load_document(path)

    def test_byte_and_depth_limits(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "document.json"
            path.write_bytes(b" " * (1_048_577))
            with self.assertRaisesRegex(ValueError, "exceeds"):
                load_document(path)
            raw = '{"nested":' + ("[" * 33) + "0" + ("]" * 33) + "}"
            path.write_text(raw, encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "nesting"):
                load_document(path)


if __name__ == "__main__":
    unittest.main()
