"""
generate_test_cases.py
Produces one test case per selected atomic requirement.

Usage:
    python scripts/generate_test_cases.py \
        -r "output/requirements.json" \
        -s "output/expected_structure.json" \
        -o "output/test_cases.json"
"""

import json
import argparse
import os

parser = argparse.ArgumentParser(description="Generate test_cases.json")
parser.add_argument("--requirements", "-r", required=True, help="requirements.json")
parser.add_argument("--structure",    "-s", required=True, help="expected_structure.json")
parser.add_argument("--output",       "-o", required=True, help="test_cases.json")
args = parser.parse_args()

with open(args.requirements) as f:
    requirements = json.load(f)

with open(args.structure) as f:
    structure = json.load(f)

selected_ids = set()
for parent, children in structure.items():
    for child in children:
        selected_ids.add(f"{parent}{child}")

req_map = {r["requirement_id"]: r for r in requirements}

for sid in sorted(selected_ids):
    if sid not in req_map:
        print(f"WARNING: {sid} is in expected_structure but not found in requirements.json")

test_cases = []

for i, rid in enumerate(sorted(selected_ids), start=1):
    if rid not in req_map:
        continue

    req    = req_map[rid]
    tc_id  = f"TC-{i:03d}"

    test_cases.append({
        "test_case_id":    tc_id,
        "requirement_id":  rid,
        "description":     (
            f"Verify that the food safety plan satisfies: "
            f"{req['description'].lstrip('- ')}"
        ),
        "input_data":      (
            f"A written food safety plan referencing {req['source']} "
            f"under parent {req['parent']}"
        ),
        "expected_output": (
            f"Requirement {rid} is present, documented in writing, "
            f"and correctly addressed per {req['source']}"
        ),
        "steps": [
            f"1. Open the food safety plan document.",
            f"2. Locate the section addressing: {req['description'].lstrip('- ')}",
            f"3. Confirm the section exists and is written (not verbal-only).",
            f"4. Verify the content satisfies {req['source']} – {rid}.",
            f"5. Check that the parent requirement ({req['parent']}) is also addressed."
        ],
        "notes": (
            f"Source regulation: {req['source']}. "
            f"Parent requirement: {req['parent']}. "
            f"This is an atomic rule – test it independently."
        )
    })

os.makedirs(os.path.dirname(args.output), exist_ok=True)

with open(args.output, "w") as f:
    json.dump(test_cases, f, indent=2)

print(f"Saved {len(test_cases)} test cases → {args.output}")