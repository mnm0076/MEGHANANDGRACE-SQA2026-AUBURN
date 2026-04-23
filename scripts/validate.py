"""
validate.py  (Task 3 – Validation)
Validates test_cases.json against expected_structure.json.

Checks:
  • All required fields are present in every test case
  • No duplicate test-case IDs
  • Every requirement in expected_structure has at least one test case
  • No test case references an unknown requirement

Usage:
    python scripts/validate.py \
        -t "output/test_cases.json" \
        -s "output/expected_structure.json"

Exit code 0 = PASS, 1 = FAIL.
"""

import json
import sys
import argparse
import os

sys.path.insert(0, os.path.dirname(__file__))
from forensick import log_event, print_summary

REQUIRED_TC_FIELDS = [
    "test_case_id",
    "requirement_id",
    "description",
    "input_data",
    "expected_output",
]
OPTIONAL_TC_FIELDS = ["steps", "notes"]

# ---------- Arguments ----------
parser = argparse.ArgumentParser(description="Validate test_cases.json")
parser.add_argument("--testcases", "-t", required=True, help="test_cases.json")
parser.add_argument("--structure", "-s", required=True, help="expected_structure.json")
args = parser.parse_args()

# ---------- Load ----------
with open(args.testcases) as f:
    test_cases = json.load(f)

with open(args.structure) as f:
    structure = json.load(f)

# Build expected requirement IDs from structure
expected_ids = set()
for parent, children in structure.items():
    for child in children:
        expected_ids.add(f"{parent}{child}")

errors   = []
warnings = []

covered_req_ids = set()
seen_tc_ids     = set()

# ── Check each test case ──────────────────────────────────────────────────────
for tc in test_cases:
    tc_id = tc.get("test_case_id", "UNKNOWN")

    # Check 1: Duplicate test-case IDs
    if tc_id in seen_tc_ids:
        msg = f"Duplicate test-case ID: {tc_id}"
        errors.append(msg)
        log_event("DUPLICATE_ID", msg)                   # forensick event 2
    seen_tc_ids.add(tc_id)

    # Check 2: Required fields present and non-empty
    for field in REQUIRED_TC_FIELDS:
        if not tc.get(field):
            msg = f"Missing/empty field '{field}' in test case {tc_id}"
            errors.append(msg)
            log_event("SCHEMA_VALIDATION_FAILURE", msg)  # forensick event 5

    # Check 3: requirement_id references a known requirement
    req_id = tc.get("requirement_id", "")
    if req_id:
        covered_req_ids.add(req_id)
        if req_id not in expected_ids:
            msg = f"Test case {tc_id} references unknown requirement: {req_id}"
            errors.append(msg)
            log_event("MISSING_REQUIREMENT", msg)        # forensick event 1

    # Check 4: Optional fields warning (informational only)
    missing_optional = [f for f in OPTIONAL_TC_FIELDS if not tc.get(f)]
    if missing_optional:
        warnings.append(
            f"Test case {tc_id} is missing optional field(s): {missing_optional}"
        )

# ── Check 5: Coverage – every expected ID has at least one test case ──────────
uncovered = expected_ids - covered_req_ids
for uid in sorted(uncovered):
    msg = f"Requirement not covered by any test case: {uid}"
    errors.append(msg)
    log_event("REQUIREMENT_SKIPPED", msg)                # forensick event 3

# ---------- Result ----------
print_summary()

if warnings:
    print("WARNINGS:")
    for w in warnings:
        print(f"  ⚠  {w}")

if errors:
    print("VALIDATION FAILED:")
    for e in errors:
        print(f"  ✗ {e}")
    log_event("CI_BUILD", f"FAILED – {len(errors)} validation error(s)")    # forensick event 4
    sys.exit(1)
else:
    print(f"VALIDATION PASSED: {len(test_cases)} test case(s) valid ✓")
    log_event("CI_BUILD", "PASSED – Validation successful")                 # forensick event 4
    sys.exit(0)