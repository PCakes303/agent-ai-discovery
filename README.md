# Agent AI Discovery

**Ecosystem:** [MrCakes931 Agent Intelligence Ecosystem](https://github.com/PCakes303/agent-intelligence-ecosystem)  
**Repository ID:** `discovery` · **Maturity:** scaffolding with experimental local validator · **Visibility:** public

## Mission

Publish machine-readable discovery documents and deterministic indexes so humans and agents can locate ecosystem resources, understand their declared interfaces, and follow links to authoritative manifests.

## Architecture and trust model

Discovery is a metadata distribution layer—not an identity provider, policy engine, registry of record, or runtime.

1. A publisher publishes a discovery document.
2. A consumer validates its structure and freshness.
3. The consumer resolves the resource's authoritative manifest.
4. Publisher identity is authenticated using a separately configured trust mechanism when required.
5. The consumer independently authorizes the requested operation.

**Discovery never grants trust or permission.** Resource metadata is untrusted input, even when retrieved over HTTPS.

## Repository contents

| Path | Purpose |
|---|---|
| `schemas/discovery-document.schema.json` | Formal JSON Schema 2020-12 contract |
| `examples/discovery.json` | Small valid discovery document |
| `docs/DISCOVERY-CONTRACT.md` | Semantics, trust boundary, versioning, freshness, privacy |
| `tools/discovery_index.py` | Standard-library validator and deterministic index builder |
| `tests/test_discovery_index.py` | Positive and negative unit tests |
| `manifest.json` | Ecosystem repository manifest |
| `capabilities.json` | Capability declarations and maturity status |
| `compatibility.json` | Declared dependencies and test status |

## Quick start

Requires Python 3.10 or later.

```bash
python -m unittest discover -s tests -v
python tools/discovery_index.py examples/discovery.json
python tools/discovery_index.py examples/discovery.json --output build/discovery-index.json
```

The validator checks the subset required by the index builder. It is not a complete JSON Schema 2020-12 validator; use a standards-compliant validator for full schema conformance.

## Document contract

Every document declares:
- contract version;
- publisher identity and publisher-manifest reference;
- generation timestamp;
- resource entries with stable ID, kind, name, authoritative manifest URI, and manifest version;
- optional capabilities, tags, summary, and update timestamp.

See the [schema](schemas/discovery-document.schema.json) and [example](examples/discovery.json).

## Dependencies

- `master` — canonical ecosystem metadata
- `resource-manifest` — authoritative resource descriptions
- `schema-registry` — schema publication and compatibility conventions
- `identity-trust` — publisher/workload identity profiles

These are declared contract dependencies, not verified runtime integrations. See the [dependency graph](https://github.com/PCakes303/agent-intelligence-ecosystem/blob/main/registry/dependencies.json).

## Security and privacy

- Never publish credentials, private endpoints, internal hostnames, personal data, or restricted operational details.
- Validate all discovery input and apply local freshness policies.
- Do not use discovery presence, HTTPS, manifest claims, or repository membership as authorization.
- Do not execute resources merely because they appear in an index.
- Follow [SECURITY.md](SECURITY.md).

## Maturity and roadmap

The repository is still **scaffolding**. A first local validator and unit-test suite have been added, and its starter CI and regression tests pass. External publisher authentication, full JSON Schema 2020-12 conformance, and consumer interoperability remain unimplemented. See [ROADMAP.md](ROADMAP.md).

## Contributing

Read [AGENTS.md](AGENTS.md) and [CONTRIBUTING.md](CONTRIBUTING.md). Changes to the discovery contract require versioning, compatibility analysis, fixtures, and security review.

## Entry-level build

Start with the runnable starter build:

    python tools/starter_build.py
    python tools/discovery_index.py examples/discovery.json --output /tmp/discovery-index.json
    python -m unittest discover -s tests -v

See [Entry-level build guide](docs/ENTRY-LEVEL-BUILD.md) for Starter → Developer → Production progression.
