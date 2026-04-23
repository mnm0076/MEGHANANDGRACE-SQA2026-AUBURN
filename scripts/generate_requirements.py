"""
generate_requirements.py
Parses a CFR Markdown file into a structured requirements.json.

Usage:
    python scripts/generate_requirements.py \
        -i "Input CFR File/21_CFR_117.130.md" \
        -o "output/requirements.json" \
        -c "21 CFR 117.130"
"""

import json
import re
import argparse

parser = argparse.ArgumentParser(description="Generate requirement JSON from CFR Markdown")
parser.add_argument("--input",  "-i", required=True, help="Input Markdown file (.md)")
parser.add_argument("--output", "-o", required=True, help="Output JSON file")
parser.add_argument("--cfr",    "-c", required=True, help="CFR section label (e.g., 21 CFR 117.130)")
args = parser.parse_args()

INPUT_MD    = args.input
OUTPUT_JSON = args.output
CFR_SECTION = args.cfr

with open(INPUT_MD, "r") as f:
    lines = [line.strip() for line in f if line.strip()]

requirements = []
seen_ids     = set()
current_req  = None

for line in lines:

    req_match = re.search(r"→\s*(REQ-[\d.]+-\d+)\s*$", line)
    if req_match:
        current_req = req_match.group(1)
        continue

    clean = re.sub(r"^[\*\-]\s*", "", line)
    atomic_match = re.match(r"^(.+?)\s*→\s*([A-Z]\d*)\s*$", clean)

    if atomic_match and current_req:
        description    = atomic_match.group(1).strip()
        suffix         = atomic_match.group(2)          # e.g. "A", "B10", "A1"
        requirement_id = f"{current_req}{suffix}"

        if requirement_id in seen_ids:
            print(f"WARNING: Duplicate ID skipped – {requirement_id}")
            continue
        seen_ids.add(requirement_id)

        if len(suffix) == 1:
            parent = current_req
        else:
            parent = f"{current_req}{suffix[0]}"

        requirements.append({
            "requirement_id": requirement_id,
            "description":    description,
            "source":         CFR_SECTION,
            "parent":         parent
        })

import os
os.makedirs(os.path.dirname(OUTPUT_JSON), exist_ok=True)

with open(OUTPUT_JSON, "w") as f:
    json.dump(requirements, f, indent=2)

print(f"Saved {len(requirements)} requirements → {OUTPUT_JSON}")