MEGHANANDGRACE-SQA2026-AUBURN
Software Quality Assurance semester project - contributors: Meghan Murphy & Grace Robinson

Included collaborators are Effat Farhana (Course instructor) and Jahidul Arafat (Course Teaching Assistant)

Project Overview
This project processes regulatory text from 21 CFR 117.130 and transforms it into structured, testable artifacts. The system parses the CFR markdown file into atomic requirements, structures relationships between them, and generates validation-ready test cases.

The goal of this project is to demonstrate how regulatory requirements can be converted into machine-readable formats and verified using automated scripts and CI pipelines.

Objectives
Extract atomic requirements from CFR regulatory text
Structure relationships between requirements
Generate test cases based on selected requirements

Verify that all requirements are correctly structured with no duplicate or missing IDs
Validate that every selected requirement has full test case coverage
Integrate forensic audit logging to track pipeline events
Automate the full V&V pipeline using GitHub Actions CI

Project Structure
MEGHANANDGRACE-SQA2026-AUBURN/
├── .github/
│   └── workflows/
│       └── ci.yml                        ← GitHub Actions CI pipeline
├── Input CFR File/
│   └── 21_CFR_117.130.md                 ← Source CFR regulation in Markdown
├── scripts/
│   ├── generate_requirements.py          ← Parses MD into requirements.json
│   ├── generate_expected_structure.py    ← Builds expected_structure.json
│   ├── generate_test_cases.py            ← Generates test_cases.json
│   ├── verify.py                         ← Verifies requirements structure
│   ├── validate.py                       ← Validates test case coverage
│   └── forensick.py                      ← Forensic audit logging module
├── output/
│   ├── requirements.json                 ← 26 parsed atomic requirements
│   ├── expected_structure.json           ← 10 selected rules mapped to parents
│   ├── test_cases.json                   ← 10 generated test cases
│   └── forensick_log.json                ← Audit event log with timestamps
└── README.md


Meghan's portion:
I contributed to this project via Tasks 1was responsible for Tasks 0 (Create Project Repo) and 2 - 1 (Extract and Structure Requirements & ) and contributed to Task 2 (Generate Test Cases).

Parsed the CFR 117.130 markdown file to generate requirements.json
Developed and used generate_requirements.py to extract atomic requirements
Structured requirement relationships in expected_requirements.json
Ensured correct mapping between parent and child requirements
Assisted in generating test cases from selected requirements
Helped ensure test cases aligned with requirement intent and structure
Contributed to test case structure and validation
Reviewed generated test cases to ensure alignment with requirement intent

Grace's portion:
I was responsible for Tasks 2 (Generate Test Cases), 3 (Verification and Validation),
4 (Forensick Integration), and setting up the GitHub Actions CI pipeline.

Fixed a duplicate ID bug in the CFR markdown where section (b) had two sub-sections
both using letters A, B, C — renamed the second sub-section to D, E, F so all
requirement IDs are unique
Wrote generate_expected_structure.py to map 10 selected atomic rules to their
parent requirements and produce expected_structure.json
Wrote generate_test_cases.py to automatically produce one test case per selected
requirement including description, input data, expected output, steps, and notes
Wrote verify.py to check requirements for duplicate IDs, missing fields, and
invalid parent references
Wrote validate.py to check test cases for coverage, completeness, and correct
requirement references
Built forensick.py, a shared forensic audit logging module that tracks five event
types (MISSING_REQUIREMENT, DUPLICATE_ID, REQUIREMENT_SKIPPED, CI_BUILD,
SCHEMA_VALIDATION_FAILURE) and writes them to a timestamped JSON log
Set up the GitHub Actions CI workflow (ci.yml) to run all pipeline steps
automatically on every push to main


How to Reproduce This Project
Requirements

Python 3.8 or higher
Git

Clone the Repository
bashgit clone https://github.com/mnm0076/MEGHANANDGRACE-SQA2026-AUBURN
cd MEGHANANDGRACE-SQA2026-AUBURN
Run the Pipeline
bashpython3 scripts/generate_requirements.py \
  -i "Input CFR File/21_CFR_117.130.md" \
  -o "output/requirements.json" \
  -c "21 CFR 117.130"

python3 scripts/generate_expected_structure.py \
  -i "output/requirements.json" \
  -o "output/expected_structure.json" \
  -s REQ-117.130-001A REQ-117.130-001B REQ-117.130-001C \
     REQ-117.130-002A REQ-117.130-002B REQ-117.130-002C \
     REQ-117.130-003A REQ-117.130-003A1 \
     REQ-117.130-003B REQ-117.130-003B1

python3 scripts/generate_test_cases.py \
  -r "output/requirements.json" \
  -s "output/expected_structure.json" \
  -o "output/test_cases.json"

python3 scripts/verify.py \
  -r "output/requirements.json" \
  -s "output/expected_structure.json"

python3 scripts/validate.py \
  -t "output/test_cases.json" \
  -s "output/expected_structure.json"
