"""
verify.py  (Task 3 – Verification)
Checks that requirements.json is structurally correct and
matches the expected_structure.json.

Usage:
    python scripts/verify.py \
        -r "output/requirements.json" \
        -s "output/expected_structure.json"

Exit code 0 = PASS, 1 = FAIL.
"""

import json
import re
import sys
import argparse
import os

sys.path.insert(0, os.path.dirname(__file__))
from forensick import log_event, print_summary

REQUIRED_FIELDS = ["requirement_id", "description", "source", "parent"]

parser = argparse.ArgumentParser(description="Verify requirements.json")
parser.add_argument("--requirements", "-r", required=True, help="requirements.json")
parser.add_argument("--structure",    "-s", required=True, help="expected_structure.json")
args = parser.parse_args()

with open(args.requirements) as f:
    requirements = json.load(f)

with open(args.structure) as f:
    structure = json.load(f)

errors = []

seen = {}
for req in requirements:
    rid = req.get("requirement_id", "")
    if rid in seen:
        msg = f"Duplicate requirement ID: {rid}"
        errors.append(msg)
        log_event("DUPLICATE_ID", msg)          # forensick event 2
    seen[rid] = True

for req in requirements:
    for field in REQUIRED_FIELDS:
        if not req.get(field):
            msg = f"Missing/empty field '{field}' in {req.get('requirement_id', 'UNKNOWN')}"
            errors.append(msg)
            log_event("SCHEMA_VALIDATION_FAILURE", msg)  # forensick event 5

req_ids = {r["requirement_id"] for r in requirements}
for parent, children in structure.items():
    for child in children:
        expected_id = f"{parent}{child}"
        if expected_id not in req_ids:
            msg = f"Requirement expected by structure but missing: {expected_id}"
            errors.append(msg)
            log_event("MISSING_REQUIREMENT", msg)        # forensick event 1

req_root_pattern = re.compile(r"^REQ-[\d.]+-\d+$")
for req in requirements:
    parent = req.get("parent", "")
    if parent and parent not in req_ids and not req_root_pattern.match(parent):
        msg = f"Invalid parent '{parent}' for requirement {req['requirement_id']}"
        errors.append(msg)
        log_event("SCHEMA_VALIDATION_FAILURE", msg)     # forensick event 5

print_summary()

if errors:
    print("VERIFICATION FAILED:")
    for e in errors:
        print(f"  ✗ {e}")
    log_event("CI_BUILD", f"FAILED – {len(errors)} verification error(s)")  # forensick event 4
    sys.exit(1)
else:
    print("VERIFICATION PASSED: All checks passed ✓")
    log_event("CI_BUILD", "PASSED – Verification successful")               # forensick event 4
    sys.exit(0)