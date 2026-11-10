#!/usr/bin/env python3
"""Lint a modular LaTeX manuscript for unresolved structural defects."""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path


CITE_RE = re.compile(r"\\cite[a-zA-Z*]*\s*(?:\[[^\]]*\]\s*)*\{([^}]*)\}")
LABEL_RE = re.compile(r"\\label\{([^}]+)\}")
REF_RE = re.compile(r"\\(?:ref|eqref|autoref|cref|Cref)\{([^}]+)\}")
BIB_RE = re.compile(r"@\w+\s*\{\s*([^,\s]+)\s*,", re.MULTILINE)
ERROR_PATTERNS = {
    "todo_marker": re.compile(r"\b(?:TODO|TBD|FIXME)\b"),
    "template_token": re.compile(r"@@[A-Z0-9_]+@@"),
    "placeholder_citation": re.compile(r"\\cite[a-zA-Z*]*\s*\{\s*(?:\?|PLACEHOLDER)[^}]*\}"),
}
NARRATIVE_PATTERNS = {
    "stage_language": re.compile(r"\bStage\s+\d+\b", re.IGNORECASE),
    "workflow_language": re.compile(
        r"\b(?:next target|previous gap|previous version|current pipeline|"
        r"strongest paper-level object|implement(?:ed)? todo)\b",
        re.IGNORECASE,
    ),
    "revision_language": re.compile(
        r"\b(?:in this revision|we improve upon our previous|remaining todo)\b",
        re.IGNORECASE,
    ),
}


def _line(path: Path, text: str, offset: int) -> str:
    return f"{path.as_posix()}:{text.count(chr(10), 0, offset) + 1}"


def inspect_project(main: Path) -> dict[str, object]:
    main = main.resolve()
    root = main.parent
    if not main.is_file():
        raise FileNotFoundError(f"main LaTeX file not found: {main}")

    tex_files = sorted(
        path for path in root.rglob("*.tex") if "build" not in path.parts
    )
    bib_files = sorted(path for path in root.rglob("*.bib") if "build" not in path.parts)
    errors: list[dict[str, str]] = []
    warnings: list[dict[str, str]] = []
    labels: list[str] = []
    refs: list[str] = []
    cites: list[str] = []

    for path in tex_files:
        text = path.read_text(encoding="utf-8")
        rel = path.relative_to(root)
        labels.extend(LABEL_RE.findall(text))
        refs.extend(REF_RE.findall(text))
        for group in CITE_RE.findall(text):
            cites.extend(key.strip() for key in group.split(",") if key.strip())
        for name, pattern in ERROR_PATTERNS.items():
            for match in pattern.finditer(text):
                errors.append({"kind": name, "location": _line(rel, text, match.start())})
        for name, pattern in NARRATIVE_PATTERNS.items():
            for match in pattern.finditer(text):
                warnings.append(
                    {"kind": name, "location": _line(rel, text, match.start())}
                )

    counts = Counter(labels)
    for label, count in sorted(counts.items()):
        if count > 1:
            errors.append({"kind": "duplicate_label", "location": label})

    label_set = set(labels)
    for ref in sorted(set(refs) - label_set):
        errors.append({"kind": "missing_label", "location": ref})

    bib_keys: set[str] = set()
    for path in bib_files:
        bib_keys.update(BIB_RE.findall(path.read_text(encoding="utf-8")))
    for key in sorted(set(cites) - bib_keys):
        errors.append({"kind": "missing_bib_key", "location": key})

    return {
        "main": str(main),
        "tex_files": [str(path.relative_to(root)) for path in tex_files],
        "bib_files": [str(path.relative_to(root)) for path in bib_files],
        "labels": len(labels),
        "references": len(refs),
        "citations": len(cites),
        "errors": errors,
        "warnings": warnings,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("main_tex", type=Path)
    parser.add_argument("--json", type=Path, help="write the complete report")
    parser.add_argument(
        "--strict-narrative",
        action="store_true",
        help="treat workflow-language warnings as errors",
    )
    args = parser.parse_args()

    try:
        report = inspect_project(args.main_tex)
    except (OSError, UnicodeError) as exc:
        print(f"manuscript lint failed: {exc}", file=sys.stderr)
        return 2

    if args.json:
        args.json.parent.mkdir(parents=True, exist_ok=True)
        args.json.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")

    print(json.dumps(report, indent=2))
    has_errors = bool(report["errors"])
    has_strict_warnings = args.strict_narrative and bool(report["warnings"])
    return 1 if has_errors or has_strict_warnings else 0


if __name__ == "__main__":
    raise SystemExit(main())
