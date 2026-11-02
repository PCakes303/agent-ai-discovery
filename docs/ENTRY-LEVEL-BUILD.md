# Entry-level build

Requires Python 3.10+; the starter build uses only the Python standard library.

```bash
python tools/starter_build.py
python tools/discovery_index.py examples/discovery.json --output /tmp/discovery-index.json
python -m unittest discover -s tests -v
```

The starter build validates the sample discovery document. The second command produces a deterministic JSON index from one or more discovery documents.

**Next tiers**
- Developer: add a resource, validate its manifest reference, and test duplicate IDs and malformed records.
- Production: add signed publisher metadata, freshness controls, registry federation, provenance checks, and abuse-resistant crawling limits.
