#!/usr/bin/env python3
"""
Regression runner for Vocabulary Markdown Validator fixtures.

Usage:
    python run_tests.py /path/to/vocab_validate.py
"""

from __future__ import annotations
import json
import re
import subprocess
import sys
from pathlib import Path

SUMMARY_RE = {
    "pass": re.compile(r"^PASS:\s+(\d+)\s*$", re.MULTILINE),
    "warn": re.compile(r"^WARN:\s+(\d+)\s*$", re.MULTILINE),
    "error": re.compile(r"^ERROR:\s+(\d+)\s*$", re.MULTILINE),
}

def extract_counts(output: str):
    result = {}
    for key, pattern in SUMMARY_RE.items():
        m = pattern.search(output)
        result[key] = int(m.group(1)) if m else None
    return result

def main():
    if len(sys.argv) != 2:
        print("Usage: python run_tests.py /path/to/vocab_validate.py", file=sys.stderr)
        return 2

    validator = Path(sys.argv[1]).resolve()
    if not validator.exists():
        print(f"Validator not found: {validator}", file=sys.stderr)
        return 2

    root = Path(__file__).resolve().parent
    cases = json.loads((root / "cases.json").read_text(encoding="utf-8"))

    total = 0
    failed = 0

    for filename, expected in cases.items():
        total += 1
        fixture = root / "fixtures" / filename

        proc = subprocess.run(
            [sys.executable, str(validator), str(fixture)],
            capture_output=True,
            text=True,
        )
        output = (proc.stdout or "") + (proc.stderr or "")
        counts = extract_counts(output)

        problems = []

        if proc.returncode != expected["exit"]:
            problems.append(
                f"exit expected {expected['exit']} got {proc.returncode}"
            )

        for key in ("pass", "warn", "error"):
            if expected.get(key) is not None and counts.get(key) != expected[key]:
                problems.append(
                    f"{key} expected {expected[key]} got {counts.get(key)}"
                )

        # Generic sanity checks where exact counts are intentionally not frozen.
        if filename.startswith("valid-") and counts["error"] not in (0,):
            problems.append(f"expected zero errors, got {counts['error']}")
        if filename.startswith("warn-") and counts["error"] not in (0,):
            problems.append(f"warning fixture should have zero errors, got {counts['error']}")
        if filename.startswith("error-") and (counts["error"] is None or counts["error"] < 1):
            problems.append("error fixture did not report an error")

        if problems:
            failed += 1
            print(f"FAIL {filename}")
            for p in problems:
                print(f"  - {p}")
            print("  --- validator output ---")
            for line in output.rstrip().splitlines():
                print(f"  {line}")
        else:
            print(
                f"PASS {filename} "
                f"(exit={proc.returncode}, "
                f"pass={counts['pass']}, warn={counts['warn']}, error={counts['error']})"
            )

    print()
    print(f"Tests: {total}")
    print(f"Passed: {total - failed}")
    print(f"Failed: {failed}")

    return 0 if failed == 0 else 1

if __name__ == "__main__":
    raise SystemExit(main())
