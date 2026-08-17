#!/usr/bin/env python3
"""
Vocabulary HTML Builder v0.2

Build a self-contained HTML vocabulary artifact from Vocabulary Markdown Format v0.1.

This builder delegates all Markdown parsing and validation to vocab_validator.py v0.6+.

Usage:
    python vocab_build.py [options] vocabulary.md

Exit codes:
    0 = build succeeded
    1 = validation/build failure
    2 = usage/read error
"""

from __future__ import annotations

import argparse
import html
import json
import shutil
import sys
from datetime import datetime
from pathlib import Path

import vocab_validator as vocab_validate

BUILDER_NAME = "Vocabulary HTML Builder"
BUILDER_VERSION = "0.2.0"
HTML_FORMAT_VERSION = "0.1"

SECTION_DIR = {
    "atom": "atoms",
    "enumerator": "enumerators",
    "composite": "composites",
    "resource": "resources",
    "affordance": "affordances",
}

SECTION_TITLE = {
    "atom": "Atoms",
    "enumerator": "Enumerators",
    "composite": "Composites",
    "resource": "Resources",
    "affordance": "Affordances",
}

SECTION_INTRO = {
    "atom": "Atoms are stable leaf terms.",
    "enumerator": "Enumerators define named sets of controlled values.",
    "composite": "Composites assemble atoms and/or other composites for a particular context.",
    "resource": "Resources are leaf terms; API relationships are defined later in the API Story.",
    "affordance": "Affordances are leaf terms naming domain behaviors; inputs and returns are defined later in the API Story.",
}

CSS = """
body{font:16px/1.55 system-ui,sans-serif;max-width:920px;margin:auto;padding:32px 24px;color:#222}
nav{margin-bottom:24px}nav a{margin-right:12px}a{color:#065fd4}
table{width:100%;border-collapse:collapse;margin:16px 0}
th,td{padding:9px;border-bottom:1px solid #ccc;text-align:left;vertical-align:top}
.meta,.subtle{color:#666}.card{background:#f6f6f6;padding:14px 18px;border-radius:7px}
.backlinks{margin-top:32px;padding-top:14px;border-top:1px solid #ccc}
input{width:100%;padding:11px;font:inherit}.result{padding:10px 0;border-bottom:1px solid #ddd}
code{font-family:monospace}footer{margin-top:42px;color:#666;font-size:.9rem}
"""

SEARCH_JS = r"""
(function(){
  const q=document.getElementById('q'),r=document.getElementById('results');
  if(!q)return;
  const esc=s=>s.replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  q.addEventListener('input',()=>{
    const x=q.value.trim().toLowerCase();
    if(!x){r.innerHTML='';return;}
    const hits=VOCAB_INDEX.filter(t=>(t.name+' '+t.kind+' '+t.definition).toLowerCase().includes(x)).slice(0,50);
    r.innerHTML=hits.length
      ? hits.map(t=>`<div class="result"><a href="${t.path}"><code>${esc(t.name)}</code></a> <span class="subtle">${esc(t.kind)}</span><br>${esc(t.definition)}</div>`).join('')
      : '<p class="subtle">No matching terms.</p>';
  });
})();
"""


def page(title, body, rel=".", kind=None, search=False, artifact_version=""):
    nav = (
        f'<nav>'
        f'<a href="{rel}/index.html">Vocabulary</a>'
        f'<a href="{rel}/atoms/index.html">Atoms</a>'
        f'<a href="{rel}/enumerators/index.html">Enumerators</a>'
        f'<a href="{rel}/composites/index.html">Composites</a>'
        f'<a href="{rel}/resources/index.html">Resources</a>'
        f'<a href="{rel}/affordances/index.html">Affordances</a>'
        f'</nav>'
    )

    kindline = f'<p class="meta">Kind: {html.escape(kind.title())}</p>' if kind else ""
    searchbox = (
        '<h2>Search</h2>'
        '<label for="q" class="subtle">Search terms, kinds, and definitions</label>'
        '<input id="q" type="search" placeholder="Search vocabulary…">'
        '<div id="results" aria-live="polite"></div>'
        if search else ""
    )
    scripts = (
        '<script src="assets/search-index.js"></script>'
        '<script src="assets/search.js"></script>'
        if search else ""
    )

    return (
        '<!doctype html><html lang="en"><head>'
        '<meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width,initial-scale=1">'
        f'<title>{html.escape(title)}</title>'
        f'<link rel="stylesheet" href="{rel}/assets/styles.css">'
        '</head><body>'
        f'{nav}<h1>{html.escape(title)}</h1>{kindline}{searchbox}{body}'
        f'<footer>Vocabulary artifact version {html.escape(artifact_version or "")}.</footer>'
        f'{scripts}</body></html>'
    )


def build_backlinks(model):
    backlinks = {}

    for term in model["terms"]:
        if term["kind"] != "composite":
            continue

        for entry in term["composition"]:
            backlinks.setdefault(entry["term"], []).append(term["name"])

    for key in backlinks:
        backlinks[key] = sorted(set(backlinks[key]))

    return backlinks


def render_term_page(term, model_by_name, backlinks, artifact_version):
    body = f"<p>{html.escape(term['definition'])}</p>"

    if term["kind"] == "enumerator":
        body += "<h2>Values</h2><table><tr><th>Value</th><th>Definition</th></tr>"
        for entry in term["values"]:
            body += (
                f"<tr><td><code>{html.escape(entry['value'])}</code></td>"
                f"<td>{html.escape(entry['definition'])}</td></tr>"
            )
        body += (
            "</table>"
            "<p class='subtle'>Values belong to this enumerator and do not have independent vocabulary pages.</p>"
        )

    elif term["kind"] == "composite":
        body += "<h2>Composition</h2><table><tr><th>Term</th><th>Requirement</th></tr>"

        for entry in term["composition"]:
            member = entry["term"]
            requirement = entry["requirement"]
            target = model_by_name[member]
            target_folder = SECTION_DIR[target["kind"]]
            href = f"../{target_folder}/{member}.html"

            body += (
                f'<tr><td><a href="{html.escape(href)}"><code>{html.escape(member)}</code></a></td>'
                f'<td>{html.escape(requirement)}</td></tr>'
            )

        body += "</table>"
        body += (
            f"<p><strong>Additional terms:</strong> "
            f"{html.escape(term['fields'].get('Additional', ''))}</p>"
        )
        body += (
            "<p class='subtle'>Requirements describe semantic membership relationships, "
            "not representation structure.</p>"
        )

    if term["externals"]:
        body += "<h2>External references</h2><ul>"

        for ext in term["externals"]:
            source = html.escape(ext.get("Source", "External"))
            uri = html.escape(ext.get("URI", ""))

            body += f'<li>{source}: <a href="{uri}">{uri}</a></li>'

        body += (
            "</ul>"
            "<p class='subtle'>External references supplement the complete local definition.</p>"
        )

    if backlinks.get(term["name"]):
        body += "<section class='backlinks'><h2>Used by</h2><ul>"

        for parent in backlinks[term["name"]]:
            body += (
                f'<li><a href="../composites/{html.escape(parent)}.html">'
                f'<code>{html.escape(parent)}</code></a> '
                f'<span class="subtle">Composite</span></li>'
            )

        body += "</ul></section>"

    return page(
        term["name"],
        body,
        rel="..",
        kind=term["kind"],
        artifact_version=artifact_version,
    )


def build_artifact(model, output_dir, run_timestamp, verbose=False):
    if output_dir.exists():
        shutil.rmtree(output_dir)

    for directory in [
        "atoms",
        "enumerators",
        "composites",
        "resources",
        "affordances",
        "assets",
    ]:
        (output_dir / directory).mkdir(parents=True, exist_ok=True)

    (output_dir / "assets" / "styles.css").write_text(CSS, encoding="utf-8")
    (output_dir / "assets" / "search.js").write_text(SEARCH_JS, encoding="utf-8")

    backlinks = build_backlinks(model)
    model_by_name = {term["name"]: term for term in model["terms"]}

    search_index = []
    generated_pages = []

    for term in model["terms"]:
        folder = SECTION_DIR[term["kind"]]
        filename = f"{term['name']}.html"
        path = output_dir / folder / filename

        path.write_text(
            render_term_page(
                term,
                model_by_name,
                backlinks,
                model["version"] or "",
            ),
            encoding="utf-8",
        )

        generated_pages.append(str(path))

        search_index.append(
            {
                "name": term["name"],
                "kind": term["kind"],
                "definition": term["definition"],
                "path": f"{folder}/{filename}",
            }
        )

    (output_dir / "assets" / "search-index.js").write_text(
        "window.VOCAB_INDEX=" + json.dumps(search_index, ensure_ascii=False) + ";",
        encoding="utf-8",
    )

    for kind, folder in SECTION_DIR.items():
        terms = [term for term in model["terms"] if term["kind"] == kind]

        listing = "<ul>" + "".join(
            (
                f'<li><a href="{html.escape(term["name"])}.html">'
                f'<code>{html.escape(term["name"])}</code></a> — '
                f'{html.escape(term["definition"])}</li>'
            )
            for term in terms
        ) + "</ul>"

        path = output_dir / folder / "index.html"
        path.write_text(
            page(
                SECTION_TITLE[kind],
                f"<p>{SECTION_INTRO[kind]}</p>{listing}",
                rel="..",
                artifact_version=model["version"] or "",
            ),
            encoding="utf-8",
        )
        generated_pages.append(str(path))

    metadata = (
        '<div class="card"><table>'
        f'<tr><th>Domain</th><td>{html.escape(model["title"] or "")}</td></tr>'
        f'<tr><th>Version</th><td>{html.escape(model["version"] or "")}</td></tr>'
        f'<tr><th>Status</th><td>{html.escape(model["status"] or "")}</td></tr>'
        f'<tr><th>Generated</th><td><time datetime="{html.escape(run_timestamp)}">'
        f'{html.escape(run_timestamp)}</time></td></tr>'
        '</table></div>'
    )

    home = (
        f"<p>{html.escape(model['description'])}</p>"
        "<h2>Browse by kind</h2><ul>"
        + "".join(
            f'<li><a href="{folder}/index.html">{SECTION_TITLE[kind]}</a></li>'
            for kind, folder in SECTION_DIR.items()
        )
        + "</ul>"
        "<p>Every vocabulary term has a complete local HTML page. "
        "External references supplement local definitions.</p>"
        "<h2>Artifact metadata</h2>"
        + metadata
    )

    home_path = output_dir / "index.html"
    home_path.write_text(
        page(
            model["title"] or "Vocabulary",
            home,
            rel=".",
            search=True,
            artifact_version=model["version"] or "",
        ),
        encoding="utf-8",
    )
    generated_pages.append(str(home_path))

    return {
        "termCount": len(model["terms"]),
        "pageCount": len(generated_pages),
        "backlinkTargets": len(backlinks),
        "pages": generated_pages if verbose else [],
    }


def build_parser():
    parser = argparse.ArgumentParser(
        prog="vocab_build.py",
        description="Build Vocabulary HTML Artifact Format v0.1 from Vocabulary Markdown.",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"{BUILDER_NAME} {BUILDER_VERSION}",
    )
    parser.add_argument(
        "-q",
        "--quiet",
        action="store_true",
        help="Suppress normal output.",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Show generated page details.",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        dest="json_output",
        help="Emit the build result as JSON.",
    )
    parser.add_argument(
        "-o",
        "--output",
        default="vocab-html",
        help="Output directory.",
    )
    parser.add_argument(
        "--no-validate",
        action="store_true",
        help="Skip source validation. Use only for development/debugging.",
    )
    parser.add_argument(
        "source",
        nargs="?",
        help="Path to the vocabulary Markdown file.",
    )
    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()

    if not args.source:
        parser.print_usage(sys.stderr)
        return 2

    source_path = Path(args.source)
    output_dir = Path(args.output)
    run_timestamp = datetime.now().astimezone().isoformat(timespec="seconds")

    try:
        text = source_path.read_text(encoding="utf-8")
    except Exception as exc:
        if args.json_output:
            print(
                json.dumps(
                    {
                        "builder": BUILDER_NAME,
                        "version": BUILDER_VERSION,
                        "htmlFormatVersion": HTML_FORMAT_VERSION,
                        "run": run_timestamp,
                        "source": source_path.name,
                        "built": False,
                        "reason": "read_error",
                        "message": str(exc),
                    },
                    indent=2,
                )
            )
        elif not args.quiet:
            print(f"ERROR unable to read {source_path}: {exc}", file=sys.stderr)

        return 2

    validation_findings = []
    validation_summary = None

    if not args.no_validate:
        validation_findings = vocab_validate.validate(text)
        validation_summary = vocab_validate.validation_summary(validation_findings)

        if not validation_summary["valid"]:
            if args.json_output:
                print(
                    json.dumps(
                        {
                            "builder": BUILDER_NAME,
                            "version": BUILDER_VERSION,
                            "htmlFormatVersion": HTML_FORMAT_VERSION,
                            "run": run_timestamp,
                            "source": source_path.name,
                            "built": False,
                            "reason": "validation_failed",
                            "validation": {
                                "pass": validation_summary["pass"],
                                "warn": validation_summary["warn"],
                                "error": validation_summary["error"],
                            },
                            "findings": [
                                f.to_dict()
                                for f in validation_findings
                                if args.verbose or f.level != "PASS"
                            ],
                        },
                        indent=2,
                    )
                )
            elif not args.quiet:
                print(BUILDER_NAME)
                print(f"Version: {BUILDER_VERSION}")
                print(f"Validator: {vocab_validate.VALIDATOR_VERSION}")
                print(f"Run: {run_timestamp}")
                print(f"Source: {source_path.name}")
                print()
                print("Validation failed. HTML artifact was not generated.")
                print()

                for finding in validation_findings:
                    if args.verbose or finding.level != "PASS":
                        print(finding)

            return 1

    model = vocab_validate.build_model(text)

    try:
        build_info = build_artifact(
            model,
            output_dir,
            run_timestamp,
            verbose=args.verbose,
        )
    except Exception as exc:
        if args.json_output:
            print(
                json.dumps(
                    {
                        "builder": BUILDER_NAME,
                        "version": BUILDER_VERSION,
                        "htmlFormatVersion": HTML_FORMAT_VERSION,
                        "run": run_timestamp,
                        "source": source_path.name,
                        "built": False,
                        "reason": "build_error",
                        "message": str(exc),
                    },
                    indent=2,
                )
            )
        elif not args.quiet:
            print(f"ERROR build failed: {exc}", file=sys.stderr)

        return 1

    result = {
        "builder": BUILDER_NAME,
        "version": BUILDER_VERSION,
        "htmlFormatVersion": HTML_FORMAT_VERSION,
        "validatorVersion": vocab_validate.VALIDATOR_VERSION,
        "run": run_timestamp,
        "source": source_path.name,
        "built": True,
        "validated": not args.no_validate,
        "output": str(output_dir),
        "termCount": build_info["termCount"],
        "pageCount": build_info["pageCount"],
        "backlinkTargets": build_info["backlinkTargets"],
    }

    if validation_summary is not None:
        result["validation"] = {
            "pass": validation_summary["pass"],
            "warn": validation_summary["warn"],
            "error": validation_summary["error"],
        }

    if args.verbose:
        result["pages"] = build_info["pages"]

    if args.json_output:
        print(json.dumps(result, indent=2))

    elif not args.quiet:
        print(BUILDER_NAME)
        print(f"Version: {BUILDER_VERSION}")
        print(f"Validator: {vocab_validate.VALIDATOR_VERSION}")
        print(f"HTML Format: {HTML_FORMAT_VERSION}")
        print(f"Run: {run_timestamp}")
        print(f"Source: {source_path.name}")
        print(f"Output: {output_dir}")
        print()

        if args.no_validate:
            print("WARN Validation skipped via --no-validate.")
        elif validation_summary is not None:
            print(
                f"Validation: PASS={validation_summary['pass']} "
                f"WARN={validation_summary['warn']} "
                f"ERROR={validation_summary['error']}"
            )

        print(f"Terms: {build_info['termCount']}")
        print(f"Pages: {build_info['pageCount']}")
        print(f"Backlink targets: {build_info['backlinkTargets']}")

        if args.verbose and build_info["pages"]:
            print()
            print("Generated pages:")
            for generated in build_info["pages"]:
                print(f"  {generated}")

        print()
        print("BUILD SUCCESS")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
