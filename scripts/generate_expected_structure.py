"""
generate_expected_structure.py
Builds expected_structure.json from requirements.json.
Maps each parent requirement ID → list of child suffixes for selected rules.

Usage:
    python scripts/generate_expected_structure.py \
        -i "output/requirements.json" \
        -o "output/expected_structure.json" \
        -s REQ-117.130-001A REQ-117.130-001B REQ-117.130-001C \
           REQ-117.130-002A REQ-117.130-002B REQ-117.130-002C \
           REQ-117.130-003A REQ-117.130-003A1 \
           REQ-117.130-003B REQ-117.130-003B1
"""

import json
import argparse
import os

parser = argparse.ArgumentParser(description="Generate expected_structure.json")
parser.add_argument("--input",    "-i", required=True,  help="requirements.json")
parser.add_argument("--output",   "-o", required=True,  help="expected_structure.json")
parser.add_argument("--selected", "-s", nargs="+",      help="Space-separated list of selected requirement IDs")
args = parser.parse_args()

with open(args.input) as f:
    requirements = json.load(f)

if args.selected:
    selected_set = set(args.selected)
    requirements = [r for r in requirements if r["requirement_id"] in selected_set]
    found = {r["requirement_id"] for r in requirements}
    missing = selected_set - found
    for m in sorted(missing):
        print(f"WARNING: Selected ID not found in requirements – {m}")

structure = {}

for req in requirements:
    parent = req["parent"]
    req_id = req["requirement_id"]

    suffix = req_id[len(parent):]

    if parent not in structure:
        structure[parent] = []
    if suffix not in structure[parent]:
        structure[parent].append(suffix)

def sort_key(s):
    import re
    m = re.match(r"([A-Z]+)(\d*)", s)
    letter = m.group(1) if m else s
    num    = int(m.group(2)) if m and m.group(2) else 0
    return (letter, num)

for parent in structure:
    structure[parent] = sorted(structure[parent], key=sort_key)

os.makedirs(os.path.dirname(args.output), exist_ok=True)

with open(args.output, "w") as f:
    json.dump(structure, f, indent=2)

print(f"Saved expected structure → {args.output}")
print(json.dumps(structure, indent=2))