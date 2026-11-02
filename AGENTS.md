# Repository working agreement

This file applies to human contributors and AI coding agents.

## Required behavior
- Read this repository's README, manifest, roadmap, security policy, and the master ecosystem registry before making architectural changes.
- Treat the master registry as authoritative for repository identity, dependencies, visibility, and ecosystem-wide maturity.
- Keep this repository authoritative for its own implementation; do not duplicate another repository's source of truth.
- Use existing standards and protocols by composition. Propose a new format only with a documented gap analysis and an Architecture Decision Record (ADR).
- Never commit credentials, tokens, private keys, personal secrets, or restricted operational data.
- Validate all untrusted input; default-deny protected operations; fail closed when required security checks are unavailable.
- Do not infer trust or permission from discovery, manifest contents, network location, or authentication alone.
- Do not expose private model reasoning or hidden chain-of-thought.
- Distinguish proposed, implemented, tested, and released behavior. Never claim a feature works without evidence.

## Change process
1. Identify affected requirement IDs and dependent repositories.
2. Update specifications and examples before or alongside implementation.
3. Add positive, negative, boundary, and failure-mode tests.
4. Update CHANGELOG.md and ROADMAP.md when behavior or milestones change.
5. Record breaking/security-sensitive decisions as ADRs.
6. Report test commands and actual results; disclose untested paths and limitations.
