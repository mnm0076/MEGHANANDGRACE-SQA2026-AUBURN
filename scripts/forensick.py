"""
forensick.py
Forensic audit logging for the CFR V&V pipeline.

Five tracked event types:
  1. MISSING_REQUIREMENT       – expected requirement ID not found
  2. DUPLICATE_ID              – duplicate requirement or test-case ID detected
  3. REQUIREMENT_SKIPPED       – requirement has no test case coverage
  4. CI_BUILD                  – CI pipeline pass / fail status
  5. SCHEMA_VALIDATION_FAILURE – required field absent or empty
"""

import json
import os
from datetime import datetime, timezone

LOG_FILE = "output/forensick_log.json"

EVENT_TYPES = {
    "MISSING_REQUIREMENT",
    "DUPLICATE_ID",
    "REQUIREMENT_SKIPPED",
    "CI_BUILD",
    "SCHEMA_VALIDATION_FAILURE",
}


def log_event(event_type: str, message: str) -> None:
    """Append a forensic event to the JSON log file."""

    if event_type not in EVENT_TYPES:
        print(f"[FORENSICK] WARNING: unknown event type '{event_type}' – logging anyway")

    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)

    # Load existing log (start fresh if missing or corrupt)
    log = []
    if os.path.exists(LOG_FILE):
        try:
            with open(LOG_FILE) as f:
                log = json.load(f)
        except (json.JSONDecodeError, OSError):
            log = []

    entry = {
        "timestamp":  datetime.now(timezone.utc).isoformat(),
        "event_type": event_type,
        "message":    message,
    }
    log.append(entry)

    with open(LOG_FILE, "w") as f:
        json.dump(log, f, indent=2)

    print(f"[FORENSICK] {event_type}: {message}")


def print_summary() -> None:
    """Print a summary of all logged events."""
    if not os.path.exists(LOG_FILE):
        print("[FORENSICK] No log file found.")
        return

    with open(LOG_FILE) as f:
        log = json.load(f)

    counts = {}
    for entry in log:
        et = entry.get("event_type", "UNKNOWN")
        counts[et] = counts.get(et, 0) + 1

    print("\n=== FORENSICK LOG SUMMARY ===")
    for et, count in sorted(counts.items()):
        print(f"  {et}: {count} event(s)")
    print(f"  TOTAL: {len(log)} event(s)")
    print(f"  Log file: {LOG_FILE}\n")