#!/usr/bin/env python3
"""Bounded, schema-backed discovery document validator and deterministic index builder."""
from __future__ import annotations
import argparse
import json
import re
import sys
from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse

from jsonschema import Draft202012Validator, FormatChecker

KINDS = {"agent", "tool", "service", "repository", "dataset", "schema"}
ID_RE = re.compile(r"^[a-z0-9][a-z0-9._:-]{2,127}$")
MAX_DOCUMENT_BYTES = 1_048_576
MAX_JSON_DEPTH = 32
SCHEMA_PATH = Path(__file__).resolve().parents[1] / "schemas" / "discovery-document.schema.json"


def _pairs_no_duplicates(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON object key: {key}")
        result[key] = value
    return result


def _reject_constant(value):
    raise ValueError(f"non-standard JSON numeric constant: {value}")


def _check_raw_depth(raw):
    depth = 0
    in_string = False
    escaped = False
    for char in raw:
        if in_string:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                in_string = False
        elif char == '"':
            in_string = True
        elif char in "[{":
            depth += 1
            if depth > MAX_JSON_DEPTH:
                raise ValueError(f"JSON nesting exceeds {MAX_JSON_DEPTH}")
        elif char in "]}":
            depth -= 1
            if depth < 0:
                raise ValueError("invalid JSON structure")


def load_document(path):
    raw_bytes = Path(path).read_bytes()
    if len(raw_bytes) > MAX_DOCUMENT_BYTES:
        raise ValueError(f"document exceeds {MAX_DOCUMENT_BYTES} bytes")
    try:
        raw = raw_bytes.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError("discovery document must be valid UTF-8") from exc
    _check_raw_depth(raw)
    try:
        document = json.loads(raw, object_pairs_hook=_pairs_no_duplicates, parse_constant=_reject_constant)
    except (json.JSONDecodeError, RecursionError) as exc:
        raise ValueError("invalid or excessively nested JSON document") from exc
    validate(document)
    return document


def _validate_uri(value, label):
    if not isinstance(value, str):
        raise ValueError(f"{label} must be an HTTPS URI")
    try:
        parsed = urlparse(value)
        port = parsed.port
    except ValueError as exc:
        raise ValueError(f"{label} contains malformed URI authority or port") from exc
    if (parsed.scheme != "https" or not parsed.hostname or parsed.username is not None
            or parsed.password is not None or parsed.fragment):
        raise ValueError(f"{label} must be HTTPS without credentials or fragments")
    if port is not None and not 1 <= port <= 65535:
        raise ValueError(f"{label} port is outside permitted range")


def _validate_timestamp(value, label):
    if not isinstance(value, str):
        raise ValueError(f"{label} must be a timezone-aware date-time")
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise ValueError(f"{label} must be a valid date-time") from exc
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        raise ValueError(f"{label} must include a timezone offset")


def validate(doc):
    if not isinstance(doc, dict):
        raise ValueError("document must be an object")
    try:
        schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
        Draft202012Validator.check_schema(schema)
        errors = sorted(
            Draft202012Validator(schema, format_checker=FormatChecker()).iter_errors(doc),
            key=lambda error: (tuple(str(part) for part in error.absolute_path), error.message),
        )
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        raise ValueError(f"normative discovery schema unavailable or invalid: {type(exc).__name__}") from exc
    if errors:
        error = errors[0]
        location = ".".join(str(part) for part in error.absolute_path) or "<root>"
        raise ValueError(f"schema violation at {location}: {error.message}")

    publisher = doc["publisher"]
    _validate_uri(publisher["manifest_uri"], "publisher.manifest_uri")
    _validate_timestamp(doc["generated_at"], "generated_at")
    seen = set()
    for i, resource in enumerate(doc["resources"]):
        label = f"resources[{i}]"
        if not ID_RE.fullmatch(resource["id"]):
            raise ValueError(f"{label}.id invalid")
        if resource["id"] in seen:
            raise ValueError(f"{label}.id duplicate: {resource['id']}")
        seen.add(resource["id"])
        _validate_uri(resource["manifest_uri"], f"{label}.manifest_uri")
        if "updated_at" in resource:
            _validate_timestamp(resource["updated_at"], f"{label}.updated_at")
    return doc


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("documents", nargs="+", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    try:
        rows = []
        for path in args.documents:
            document = load_document(path)
            rows.extend({"publisher_id": document["publisher"]["id"], **resource}
                        for resource in document["resources"])
        rows.sort(key=lambda row: (row["kind"], row["id"]))
        ids = [row["id"] for row in rows]
        if len(ids) != len(set(ids)):
            raise ValueError("duplicate resource ID across documents")
        output = json.dumps(
            {"index_version": "1.0.0", "resource_count": len(rows), "resources": rows},
            indent=2, sort_keys=True,
        ) + "\n"
        if args.output:
            args.output.write_text(output, encoding="utf-8")
        else:
            sys.stdout.write(output)
        return 0
    except (OSError, ValueError, RecursionError) as exc:
        print(f"discovery-index: error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
