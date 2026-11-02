# Discovery contract 1.0.0

## Purpose and security boundary

A discovery document advertises candidate resources and points to their authoritative manifests. It is an index, not an identity provider, authorization service, execution environment, or trust anchor.

Consumers MUST validate documents, resolve authoritative manifests, authenticate publishers where required, independently authorize each action, and apply freshness limits. Discovery results are untrusted hints.

## Versioning

Removing a required field, changing field meaning, or weakening a security guarantee is breaking and requires a major version. Additive optional fields are minor; editorial corrections are patch.

## Identifiers and freshness

Resource IDs are stable lowercase identifiers within the ecosystem namespace. An ID is not authenticated identity unless bound to an authenticated publisher and trust policy. Timestamps are informational; consumers define maximum staleness windows. Stale metadata never grants continued access.

## Privacy

Publish only intentionally public metadata. Do not include secrets, personal data, private endpoints, internal hostnames, credentials, restricted operational details, or hidden model reasoning.

## Validation limitation

The Python reference validator enforces the fields used by the index builder but is not a complete JSON Schema 2020-12 implementation. The JSON Schema is the formal document contract.
