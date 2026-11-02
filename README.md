# Agent AI Discovery

**Repository:** [PCakes303/agent-ai-discovery](https://github.com/PCakes303/agent-ai-discovery)  
**Ecosystem:** [MrCakes931 Agent Intelligence Ecosystem](https://github.com/PCakes303/agent-intelligence-ecosystem)  
**Repository ID:** `discovery` · **Maturity:** scaffolding · **Visibility:** public

## Purpose

Publish machine-readable ecosystem entrypoints and discovery metadata so people and agents can find repositories, resources, interfaces, and declared capabilities.

## Scope

- Discovery documents and metadata endpoints
- Capability index publication and versioning
- Opt-in discovery integration guidance
- Links to authoritative resource manifests

## Explicit boundaries

This repository does not own:

- Authentication or authorization decisions
- Credential issuance or trust establishment
- Runtime agent execution
- Copying authoritative schemas or manifests into a competing registry

## Dependencies

- `master`
- `resource-manifest`
- `schema-registry`
- `identity-trust`

See the [canonical dependency graph](https://github.com/PCakes303/agent-intelligence-ecosystem/blob/main/registry/dependencies.json). Declared dependencies are contract relationships; they do not mean those components are already implemented or tested together.

## Initial deliverables

1. A versioned discovery document format
2. A generated index sourced from authoritative manifests
3. Validation for stale, malformed, or duplicate entries
4. A documented opt-in discovery endpoint profile

## First implementation milestone

Define a discovery document schema that references resource-manifest and schema-registry versions; add valid/invalid fixtures and a deterministic index generator.

## Security and trust

Discovery results are untrusted hints. Consumers MUST resolve authoritative manifests, authenticate publishers where required, and independently authorize operations.

Read [SECURITY.md](SECURITY.md) before contributing. Never commit secrets. Validate untrusted data and fail closed for security-sensitive decisions.

## Status

This repository currently contains its initial documentation and metadata scaffold. Domain implementation, interoperability, and conformance are **not yet verified**. The master registry is authoritative for ecosystem-wide status.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) and [AGENTS.md](AGENTS.md). Changes should include tests or validation evidence appropriate to the affected contract.
