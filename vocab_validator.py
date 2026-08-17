#!/usr/bin/env python3
"""
Vocabulary Markdown Validator v0.6

Authoritative parser and validator for Vocabulary Markdown Format v0.1.

This module is both:
1. a command-line validator, and
2. a reusable parser/validation library for tools such as vocab_build.py.

Reusable API:
    parse_document(text) -> ParsedDocument
    build_model(text) -> dict
    validate(text) -> list[Finding]
    validate_model(model) -> list[Finding]

CLI:
    python vocab_validate.py [options] vocabulary.md
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

VALIDATOR_NAME = "Vocabulary Markdown Validator"
VALIDATOR_VERSION = "0.6.0"
FORMAT_VERSION = "0.1"

VALID_KINDS = {"atom", "enumerator", "composite", "resource", "affordance"}
SECTION_TO_KIND = {
    "Atoms": "atom",
    "Enumerators": "enumerator",
    "Composites": "composite",
    "Resources": "resource",
    "Affordances": "affordance",
}
VALID_REQUIREMENTS = {"MUST", "SHOULD", "MAY"}

H1_RE = re.compile(r"^#\s+(.+?)\s*$")
H2_RE = re.compile(r"^##\s+(.+?)\s*$")
H3_RE = re.compile(r"^###\s+(.+?)\s*$")
FIELD_RE = re.compile(r"^([A-Za-z][A-Za-z0-9 _-]*):\s*(.*?)\s*$")
BULLET_PAIR_RE = re.compile(r"^\*\s+(.+?)\s*:\s*(.+?)\s*$")


@dataclass
class Finding:
    level: str
    message: str
    line: int | None = None

    def __str__(self) -> str:
        loc = f"line {self.line}: " if self.line else ""
        return f"{self.level} {loc}{self.message}"

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class ParsedDocument:
    lines: list[str]
    title: str | None
    h1_count: int
    version: str | None
    status: str | None
    description: str
    sections: dict[str, int]
    terms: list[dict[str, Any]]
    parse_findings: list[Finding]


def valid_uri(value: str) -> bool:
    try:
        parsed = urlparse(value.strip())
        return bool(parsed.scheme and parsed.netloc)
    except Exception:
        return False


def _extract_local_definition(lines: list[str], start: int, end: int) -> str:
    """
    Extract the local prose definition for a term.

    start/end are zero-based slice boundaries for the term body.
    Structured blocks stop definition capture.
    """
    blocked = {"External:", "Values:", "Composition:"}
    parts: list[str] = []
    started = False

    for i in range(start, end):
        s = lines[i].strip()

        if not s:
            if started:
                break
            continue

        if s.startswith("Kind:"):
            continue

        if s in blocked or s.startswith("Additional:") or s.startswith("* ") or s.startswith("#"):
            if started:
                break
            continue

        started = True
        parts.append(s)

    return " ".join(parts).strip()


def _extract_document_description(lines: list[str]) -> str:
    parts: list[str] = []
    seen_h1 = False

    for raw in lines:
        s = raw.strip()

        if s.startswith("# "):
            seen_h1 = True
            continue

        if not seen_h1:
            continue

        if s.startswith("## "):
            break

        if not s or s.startswith("Version:") or s.startswith("Status:"):
            continue

        parts.append(s)

    return " ".join(parts).strip()


def parse_document(text: str) -> ParsedDocument:
    """
    Parse Vocabulary Markdown Format v0.1 source.

    This function performs syntax extraction only. It does not decide whether
    the parsed model is valid. Any malformed structured-entry findings discovered
    during parsing are returned in parse_findings.
    """
    lines = text.splitlines()
    findings: list[Finding] = []

    title = None
    version = None
    status = None
    sections: dict[str, int] = {}
    terms: list[dict[str, Any]] = []

    current_section = None
    current_term = None
    h1_count = 0

    for idx, raw in enumerate(lines, start=1):
        line = raw.rstrip()

        m = H1_RE.match(line)
        if m:
            h1_count += 1
            if title is None:
                title = m.group(1).strip()
            continue

        m = H2_RE.match(line)
        if m:
            current_section = m.group(1).strip()
            sections.setdefault(current_section, idx)
            current_term = None
            continue

        m = H3_RE.match(line)
        if m:
            name = m.group(1).strip()
            current_term = {
                "name": name,
                "line": idx,
                "section": current_section,
                "kind": None,
                "fields": {},
                "composition": [],
                "values": [],
                "externals": [],
                "start": idx - 1,
                "end": len(lines),
            }
            if terms:
                terms[-1]["end"] = idx - 1
            terms.append(current_term)
            continue

        m = FIELD_RE.match(line)
        if m:
            key = m.group(1).strip()
            value = m.group(2).strip()

            if current_term is None:
                if key == "Version":
                    version = value
                elif key == "Status":
                    status = value
            else:
                current_term["fields"][key] = value
                if key == "Kind":
                    current_term["kind"] = value
            continue

    for term in terms:
        start = term["start"] + 1
        end = term["end"]
        mode = None
        current_external = None

        for lineno in range(start + 1, end + 1):
            s = lines[lineno - 1].strip()

            if not s:
                continue

            if s == "Values:":
                mode = "values"
                continue

            if s == "Composition:":
                mode = "composition"
                continue

            if s == "External:":
                mode = "external"
                current_external = {}
                term["externals"].append(current_external)
                continue

            if s.startswith("Additional:"):
                mode = None
                continue

            if mode in {"values", "composition"} and s.startswith("* "):
                m = BULLET_PAIR_RE.match(s)
                if not m:
                    findings.append(Finding("ERROR", f"Malformed {mode} entry.", lineno))
                    continue

                left = m.group(1).strip()
                right = m.group(2).strip()

                if mode == "values":
                    term["values"].append((left, right, lineno))
                else:
                    term["composition"].append((left, right, lineno))
                continue

            if mode == "external":
                m = re.match(r"^\*\s+Source:\s*(.+?)\s*$", s)
                if m:
                    current_external = {"Source": m.group(1).strip()}
                    term["externals"][-1] = current_external
                    continue

                m = re.match(r"^URI:\s*(.+?)\s*$", s.lstrip())
                if m and current_external is not None:
                    current_external["URI"] = m.group(1).strip()
                    continue

        term["definition"] = _extract_local_definition(lines, start, end)
        term["has_definition"] = bool(term["definition"])

    return ParsedDocument(
        lines=lines,
        title=title,
        h1_count=h1_count,
        version=version,
        status=status,
        description=_extract_document_description(lines),
        sections=sections,
        terms=terms,
        parse_findings=findings,
    )


def build_model(text: str) -> dict[str, Any]:
    """
    Return the stable parsed vocabulary model intended for downstream tools.

    This does not imply validity. Call validate(text) before relying on the model.
    """
    parsed = parse_document(text)

    return {
        "formatVersion": FORMAT_VERSION,
        "title": parsed.title,
        "version": parsed.version,
        "status": parsed.status,
        "description": parsed.description,
        "sections": dict(parsed.sections),
        "terms": [
            {
                "name": t["name"],
                "kind": t["kind"],
                "section": t["section"],
                "definition": t["definition"],
                "fields": dict(t["fields"]),
                "values": [
                    {"value": value, "definition": definition, "line": line}
                    for value, definition, line in t["values"]
                ],
                "composition": [
                    {"term": member, "requirement": requirement, "line": line}
                    for member, requirement, line in t["composition"]
                ],
                "externals": [dict(ext) for ext in t["externals"]],
                "line": t["line"],
            }
            for t in parsed.terms
        ],
    }


def validate_model(model: dict[str, Any], parsed: ParsedDocument | None = None) -> list[Finding]:
    """
    Validate a parsed vocabulary model.

    parsed may be supplied to preserve precise line/section checks derived from
    the original Markdown. Downstream tools normally call validate(text), which
    supplies both automatically.
    """
    findings: list[Finding] = []

    if parsed is None:
        # Reconstruct only what is safely available from the model.
        # Full Markdown structural validation should use validate(text).
        findings.append(
            Finding(
                "WARN",
                "validate_model() called without ParsedDocument; Markdown structural checks are limited.",
            )
        )

    def check(condition, pass_message, fail_message, line=None, warning=False):
        if condition:
            findings.append(Finding("PASS", pass_message, line))
            return True

        findings.append(
            Finding("WARN" if warning else "ERROR", fail_message, line)
        )
        return False

    title = model.get("title")
    version = model.get("version")
    status = model.get("status")
    sections = model.get("sections", {})
    terms = model.get("terms", [])

    if parsed is not None:
        check(
            parsed.h1_count == 1,
            "Document contains exactly one H1 title.",
            f"Document must contain exactly one H1 title; found {parsed.h1_count}.",
        )

    check(bool(title), "Vocabulary title is present.", "Vocabulary title is missing.")
    check(bool(version), "Version is present.", "Version is required.")
    check(bool(status), "Status is present.", "Status is recommended.", warning=True)

    for section in SECTION_TO_KIND:
        check(
            section in sections,
            f'Required section "{section}" is present.',
            f"Missing required section: {section}.",
        )

    if parsed is not None:
        seen_sections: set[str] = set()
        for idx, line in enumerate(parsed.lines, start=1):
            m = H2_RE.match(line)
            if not m:
                continue

            name = m.group(1).strip()

            if name in seen_sections:
                findings.append(Finding("ERROR", f"Duplicate section: {name}.", idx))
            else:
                findings.append(Finding("PASS", f'Section "{name}" is unique.', idx))
                seen_sections.add(name)

    seen_terms: dict[str, dict[str, Any]] = {}

    for term in terms:
        name = term.get("name")
        line = term.get("line")

        if name in seen_terms:
            findings.append(Finding("ERROR", f'Duplicate vocabulary term "{name}".', line))
        else:
            findings.append(Finding("PASS", f'Term "{name}" is unique.', line))
            seen_terms[name] = term

    for term in terms:
        name = term.get("name")
        section = term.get("section")
        kind = term.get("kind")
        line = term.get("line")
        fields = term.get("fields", {})
        values = term.get("values", [])
        composition = term.get("composition", [])

        check(
            section in SECTION_TO_KIND,
            f'Term "{name}" is under a recognized vocabulary section.',
            f'Term "{name}" is not under a recognized vocabulary section.',
            line,
        )

        if not check(
            bool(kind),
            f'Term "{name}" has a Kind.',
            f'Term "{name}" is missing Kind.',
            line,
        ):
            continue

        kind_is_valid = check(
            kind in VALID_KINDS,
            f'Term "{name}" has valid Kind "{kind}".',
            f'Term "{name}" has invalid Kind "{kind}".',
            line,
        )

        if kind_is_valid and section in SECTION_TO_KIND:
            check(
                SECTION_TO_KIND[section] == kind,
                f'Term "{name}" Kind matches section "{section}".',
                f'Term "{name}" Kind "{kind}" does not match section "{section}".',
                line,
            )

        check(
            bool(term.get("definition")),
            f'Term "{name}" has a local definition.',
            f'Term "{name}" is missing a local definition.',
            line,
        )

        has_values = bool(values)
        has_comp = bool(composition)
        has_additional = "Additional" in fields

        if parsed is not None:
            source_term = next((t for t in parsed.terms if t["name"] == name and t["line"] == line), None)
            if source_term:
                has_values = has_values or any(
                    parsed.lines[i].strip() == "Values:"
                    for i in range(source_term["start"], source_term["end"])
                )
                has_comp = has_comp or any(
                    parsed.lines[i].strip() == "Composition:"
                    for i in range(source_term["start"], source_term["end"])
                )

        if kind == "atom":
            check(
                not has_values,
                f'Atom "{name}" has no Values block.',
                f'Atom "{name}" must not contain Values.',
                line,
            )
            check(
                not has_comp,
                f'Atom "{name}" has no Composition block.',
                f'Atom "{name}" must not contain Composition.',
                line,
            )
            check(
                not has_additional,
                f'Atom "{name}" has no Additional field.',
                f'Atom "{name}" must not contain Additional.',
                line,
            )

        elif kind == "enumerator":
            check(
                bool(values),
                f'Enumerator "{name}" contains values.',
                f'Enumerator "{name}" must contain at least one value.',
                line,
            )
            check(
                not has_comp,
                f'Enumerator "{name}" has no Composition block.',
                f'Enumerator "{name}" must not contain Composition.',
                line,
            )
            check(
                not has_additional,
                f'Enumerator "{name}" has no Additional field.',
                f'Enumerator "{name}" must not contain Additional.',
                line,
            )

            seen_values: set[str] = set()
            for entry in values:
                value = entry.get("value")
                definition = entry.get("definition")
                value_line = entry.get("line")

                if value in seen_values:
                    findings.append(
                        Finding(
                            "ERROR",
                            f'Duplicate value "{value}" in enumerator "{name}".',
                            value_line,
                        )
                    )
                else:
                    findings.append(
                        Finding(
                            "PASS",
                            f'Value "{value}" is unique within enumerator "{name}".',
                            value_line,
                        )
                    )
                    seen_values.add(value)

                check(
                    bool(definition),
                    f'Value "{value}" in enumerator "{name}" has a definition.',
                    f'Value "{value}" in enumerator "{name}" is missing a definition.',
                    value_line,
                )

        elif kind == "composite":
            check(
                bool(composition),
                f'Composite "{name}" contains composition members.',
                f'Composite "{name}" must contain at least one composition member.',
                line,
            )

            additional_present = check(
                has_additional,
                f'Composite "{name}" declares Additional.',
                f'Composite "{name}" must declare Additional.',
                line,
            )

            if additional_present:
                check(
                    fields.get("Additional") in VALID_REQUIREMENTS,
                    f'Composite "{name}" has valid Additional value "{fields.get("Additional")}".',
                    f'Composite "{name}" has invalid Additional value "{fields.get("Additional")}".',
                    line,
                )

            seen_members: set[str] = set()

            for entry in composition:
                member = entry.get("term")
                requirement = entry.get("requirement")
                member_line = entry.get("line")

                check(
                    requirement in VALID_REQUIREMENTS,
                    f'Composite "{name}" member "{member}" has valid requirement "{requirement}".',
                    f'Composite "{name}" member "{member}" has invalid requirement "{requirement}".',
                    member_line,
                )

                if member in seen_members:
                    findings.append(
                        Finding(
                            "ERROR",
                            f'Duplicate member "{member}" in composite "{name}".',
                            member_line,
                        )
                    )
                else:
                    findings.append(
                        Finding(
                            "PASS",
                            f'Composite "{name}" member "{member}" is unique.',
                            member_line,
                        )
                    )
                    seen_members.add(member)

        elif kind in {"resource", "affordance"}:
            label = kind.title()

            check(
                not has_values,
                f'{label} "{name}" has no Values block.',
                f'{label} "{name}" must not contain Values.',
                line,
            )
            check(
                not has_comp,
                f'{label} "{name}" has no Composition block.',
                f'{label} "{name}" must not contain Composition.',
                line,
            )
            check(
                not has_additional,
                f'{label} "{name}" has no Additional field.',
                f'{label} "{name}" must not contain Additional.',
                line,
            )

            forbidden = {"Inputs", "Input", "Returns", "Actions", "Resource"}

            for key in fields:
                if key in forbidden:
                    findings.append(
                        Finding(
                            "ERROR",
                            f'{label} "{name}" must not specify {key}; this belongs in the API Story.',
                            line,
                        )
                    )
                else:
                    findings.append(
                        Finding(
                            "PASS",
                            f'{label} "{name}" field "{key}" is allowed.',
                            line,
                        )
                    )

        for ext in term.get("externals", []):
            check(
                bool(ext.get("Source")),
                f'Term "{name}" external reference has Source.',
                f'Term "{name}" has an external reference without Source.',
                line,
            )

            uri_ok = check(
                bool(ext.get("URI")),
                f'Term "{name}" external reference has URI.',
                f'Term "{name}" has an external reference without URI.',
                line,
            )

            if uri_ok:
                check(
                    valid_uri(ext["URI"]),
                    f'Term "{name}" external URI is valid.',
                    f'Term "{name}" has invalid external URI "{ext["URI"]}".',
                    line,
                )

    term_by_name = {term.get("name"): term for term in terms}

    for term in terms:
        if term.get("kind") != "composite":
            continue

        name = term.get("name")

        for entry in term.get("composition", []):
            member = entry.get("term")
            line = entry.get("line")
            target = term_by_name.get(member)

            target_exists = check(
                target is not None,
                f'Composite "{name}" member "{member}" resolves to a defined term.',
                f'Composite "{name}" references undefined term "{member}".',
                line,
            )

            if not target_exists:
                continue

            check(
                target.get("kind") in {"atom", "composite"},
                f'Composite "{name}" member "{member}" has allowed kind "{target.get("kind")}".',
                f'Composite "{name}" member "{member}" must be an atom or composite, not {target.get("kind")}.',
                line,
            )

    return findings


def validate(text: str) -> list[Finding]:
    """
    Parse and fully validate Vocabulary Markdown source.
    """
    parsed = parse_document(text)
    model = build_model(text)

    findings = list(parsed.parse_findings)
    findings.extend(validate_model(model, parsed))
    return findings


def validation_summary(findings: list[Finding]) -> dict[str, Any]:
    passes = [f for f in findings if f.level == "PASS"]
    warnings = [f for f in findings if f.level == "WARN"]
    errors = [f for f in findings if f.level == "ERROR"]

    return {
        "valid": not errors,
        "pass": len(passes),
        "warn": len(warnings),
        "error": len(errors),
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="vocab_validate.py",
        description="Validate Vocabulary Markdown Format v0.1 documents.",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"{VALIDATOR_NAME} {VALIDATOR_VERSION}",
    )
    parser.add_argument(
        "-q",
        "--quiet",
        action="store_true",
        help="Suppress normal output; use exit code only.",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Show all validation findings, including PASS results.",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        dest="json_output",
        help="Emit the validation result as JSON.",
    )
    parser.add_argument(
        "source",
        nargs="?",
        help="Path to the vocabulary Markdown file.",
    )
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    if not args.source:
        parser.print_usage(sys.stderr)
        return 2

    path = Path(args.source)
    run_timestamp = datetime.now().astimezone().isoformat(timespec="seconds")

    try:
        text = path.read_text(encoding="utf-8")
    except Exception as exc:
        finding = Finding("ERROR", f"Unable to read source: {exc}")

        if args.json_output:
            payload = {
                "validator": VALIDATOR_NAME,
                "version": VALIDATOR_VERSION,
                "formatVersion": FORMAT_VERSION,
                "run": run_timestamp,
                "source": path.name,
                "valid": False,
                "summary": {"pass": 0, "warn": 0, "error": 1},
                "findings": [finding.to_dict()],
            }
            print(json.dumps(payload, indent=2))
        elif not args.quiet:
            print(finding, file=sys.stderr)

        return 2

    findings = validate(text)
    summary = validation_summary(findings)

    # JSON takes precedence over quiet.
    if args.json_output:
        json_findings = (
            findings
            if args.verbose
            else [f for f in findings if f.level != "PASS"]
        )

        payload = {
            "validator": VALIDATOR_NAME,
            "version": VALIDATOR_VERSION,
            "formatVersion": FORMAT_VERSION,
            "run": run_timestamp,
            "source": path.name,
            "valid": summary["valid"],
            "summary": {
                "pass": summary["pass"],
                "warn": summary["warn"],
                "error": summary["error"],
            },
            "findings": [f.to_dict() for f in json_findings],
        }
        print(json.dumps(payload, indent=2))

    elif not args.quiet:
        print(VALIDATOR_NAME)
        print(f"Version: {VALIDATOR_VERSION}")
        print(f"Format: {FORMAT_VERSION}")
        print(f"Run: {run_timestamp}")
        print(f"Source: {path.name}")
        print()
        print("----------------------------------------")
        print()

        visible = (
            findings
            if args.verbose
            else [f for f in findings if f.level != "PASS"]
        )

        for finding in visible:
            print(finding)

        if visible:
            print()

        print(f"PASS: {summary['pass']}")
        print(f"WARN: {summary['warn']}")
        print(f"ERROR: {summary['error']}")
        print()
        print("VALID" if summary["valid"] else "INVALID")

    return 0 if summary["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
