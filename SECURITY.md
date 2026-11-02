# Security Policy

## Scope
This is a public repository. Treat issues, pull requests, manifests, schemas, code, dependencies, generated artifacts, and external references as untrusted until validated.

## Reporting
Do not publish exploitable vulnerabilities, credentials, personal data, or sensitive operational details in public issues. Use GitHub's private vulnerability reporting for this repository if enabled. If unavailable, contact the repository owner through a verified private channel; do not include secrets in the report.

## Baseline requirements
- No secrets or credentials in source control, examples, logs, or test fixtures.
- Validate and constrain untrusted input.
- Apply least privilege and default-deny to protected actions.
- Fail closed when required authentication, authorization, integrity, or revocation checks cannot complete.
- Pin and review dependencies and CI actions; use short-lived credentials where supported.
- Record security-relevant events while minimizing sensitive payloads.
- Distinguish authentication from authorization and descriptive metadata from proof of trust.

## Disclosure
Please allow time for triage and remediation before public disclosure. Coordinate a disclosure timeline with the maintainer.

## Current status
This policy is an initial baseline, not a completed threat model or independent security audit.
