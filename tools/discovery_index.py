#!/usr/bin/env python3
"""Validate discovery documents and build a deterministic index (stdlib only)."""
from __future__ import annotations
import argparse, json, re, sys
from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse

KINDS = {"agent", "tool", "service", "repository", "dataset", "schema"}
ID_RE = re.compile(r"^[a-z0-9][a-z0-9._:-]*$")

def validate(doc):
    if not isinstance(doc, dict): raise ValueError("document must be an object")
    if set(doc) - {"discovery_version","publisher","generated_at","resources"}: raise ValueError("unknown top-level fields")
    if doc.get("discovery_version") != "1.0.0": raise ValueError("unsupported discovery_version")
    pub = doc.get("publisher")
    if not isinstance(pub, dict) or not all(pub.get(k) for k in ("id","name","manifest_uri")): raise ValueError("publisher requires id, name, manifest_uri")
    def uri(value, label):
        p = urlparse(value) if isinstance(value,str) else None
        if not p or p.scheme not in {"http","https"} or not p.netloc: raise ValueError(f"{label} must be an absolute HTTP(S) URI")
    def timestamp(value, label):
        try: datetime.fromisoformat(value.replace("Z","+00:00"))
        except (ValueError, AttributeError): raise ValueError(f"{label} must be ISO-8601")
    uri(pub["manifest_uri"],"publisher.manifest_uri")
    timestamp(doc.get("generated_at"),"generated_at")
    resources=doc.get("resources")
    if not isinstance(resources,list): raise ValueError("resources must be an array")
    seen=set()
    for i,r in enumerate(resources):
        label=f"resources[{i}]"
        if not isinstance(r,dict): raise ValueError(f"{label} must be an object")
        required=("id","kind","name","manifest_uri","manifest_version")
        if not all(r.get(k) for k in required): raise ValueError(f"{label} missing required fields")
        if not ID_RE.fullmatch(r["id"]): raise ValueError(f"{label}.id invalid")
        if r["id"] in seen: raise ValueError(f"{label}.id duplicate: {r['id']}")
        seen.add(r["id"])
        if r["kind"] not in KINDS: raise ValueError(f"{label}.kind unsupported")
        uri(r["manifest_uri"],f"{label}.manifest_uri")
        if "updated_at" in r: timestamp(r["updated_at"],f"{label}.updated_at")
        for key in ("capabilities","tags"):
            if key in r and (not isinstance(r[key],list) or not all(isinstance(x,str) for x in r[key])): raise ValueError(f"{label}.{key} must be a string array")
    return doc

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument("documents",nargs="+",type=Path)
    ap.add_argument("--output",type=Path)
    args=ap.parse_args()
    try:
        rows=[]
        for path in args.documents:
            d=validate(json.loads(path.read_text(encoding="utf-8")))
            rows.extend({"publisher_id":d["publisher"]["id"],**r} for r in d["resources"])
        rows.sort(key=lambda r:(r["kind"],r["id"]))
        ids=[r["id"] for r in rows]
        if len(ids)!=len(set(ids)): raise ValueError("duplicate resource ID across documents")
        output=json.dumps({"index_version":"1.0.0","resource_count":len(rows),"resources":rows},indent=2,sort_keys=True)+"\n"
        if args.output: args.output.write_text(output,encoding="utf-8")
        else: sys.stdout.write(output)
        return 0
    except (OSError,json.JSONDecodeError,ValueError) as exc:
        print(f"discovery-index: error: {exc}",file=sys.stderr); return 2

if __name__=="__main__": raise SystemExit(main())
