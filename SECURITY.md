# Security Policy

## Scope
This public repository contains a discovery-document schema and local index-builder scaffold. Discovery metadata is untrusted input and never grants trust, authorization, or permission to execute a resource.

## Reporting

Do not publish exploitable vulnerability details, credentials, personal data, or sensitive operational information in public issues. Use GitHub private vulnerability reporting or a private security advisory only if enabled for this repository. No dedicated private reporting address is published here; if GitHub private reporting is unavailable, the owner must configure an approved private reporting channel before production use.

## Baseline requirements
- Treat all publisher metadata, resource entries, URIs, and capability claims as untrusted.
- Validate structure and freshness; authenticate publishers and authorize actions independently.
- Do not infer identity or permission from HTTPS, repository membership, or discovery presence.
- Bound document size, resource count, string lengths and parser depth in consumers before production use.
- Do not execute resources merely because they appear in an index.
