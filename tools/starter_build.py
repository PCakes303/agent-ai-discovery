#!/usr/bin/env python3
"""Run the entry-level discovery document build."""
import json
from pathlib import Path
from tools.discovery_index import validate
root=Path(__file__).resolve().parents[1]
sample=json.loads((root/"examples/discovery.json").read_text(encoding="utf-8"))
doc=validate(sample)
print(json.dumps({"build_tier":"starter","project":"agent-ai-discovery","resources":len(doc["resources"]),"result":"passed"},indent=2))
