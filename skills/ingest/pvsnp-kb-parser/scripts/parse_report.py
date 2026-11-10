# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT

"""Parse a LaTeX-style deep research report into KB statements.

The parser targets theorem-like environments such as:
- definition
- theorem
- lemma
- proposition
- corollary
- remark

It can optionally write directly into a KB markdown file by invoking
skills/ingest/latex-kb-ingest/scripts/kb_writeback.py.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any

_COMMON_DIR = Path(__file__).resolve().parents[3] / "common"
if str(_COMMON_DIR) not in sys.path:
    sys.path.insert(0, str(_COMMON_DIR))

from reasoning_log import ReasoningLogger

ENV_PATTERN = re.compile(
    r"\\begin\{(definition|theorem|lemma|proposition|corollary|remark)\}"
    r"(?:\[([^\]]+)\])?\s*(.*?)\\end\{\1\}",
    re.DOTALL,
)
SECTION_PATTERN = re.compile(r"\\section\*?\{([^}]*)\}")
PARAGRAPH_PATTERN = re.compile(r"\\paragraph\{([^}]*)\}")
SOURCE_COMMENT_PATTERN = re.compile(r"(?m)^%\s*sources:\s*(.+)$")

KIND_MAP = {
    "definition": "definition",
    "theorem": "theorem",
    "lemma": "lemma",
    "proposition": "theorem",
    "corollary": "corollary",
    "remark": "observation",
}

CONFIDENCE_MAP = {
    "definition": 0.95,
    "theorem": 0.86,
    "lemma": 0.84,
    "proposition": 0.83,
    "corollary": 0.82,
    "remark": 0.72,
}

KIND_SHORT = {
    "definition": "def",
    "theorem": "thm",
    "lemma": "lem",
    "corollary": "cor",
    "observation": "obs",
}


def _slugify(text: str) -> str:
    """
    Relevance: Operates within the P vs NP KB parsing layer.
    Concept: Stable naming and path-derivation helper for artifact routing.
    Contribution: Contributes a deterministic transformation that supports end-to-end reasoning reproducibility.
    """

    slug = text.lower()
    slug = re.sub(r"\\[a-zA-Z]+", " ", slug)
    slug = re.sub(r"\$+", "", slug)
    slug = re.sub(r"[^a-z0-9]+", "-", slug)
    slug = re.sub(r"-{2,}", "-", slug).strip("-")
    if not slug:
        slug = "item"
    return slug[:48]


def _compact(text: str) -> str:
    """
    Relevance: Operates within the P vs NP KB parsing layer.
    Concept: Internal helper implementing one deterministic step of this stage.
    Contribution: Contributes a deterministic transformation that supports end-to-end reasoning reproducibility.
    """

    return re.sub(r"\s+", " ", text).strip()


def _to_informal(latex_text: str, max_chars: int) -> str:
    """
    Relevance: Operates within the P vs NP KB parsing layer.
    Concept: Internal helper implementing one deterministic step of this stage.
    Contribution: Contributes a deterministic transformation that supports end-to-end reasoning reproducibility.
    """

    cleaned = re.sub(r"\\begin\{[^}]+\}|\\end\{[^}]+\}", " ", latex_text)
    # Preserve command names (e.g., \Pclass -> Pclass) for readability.
    cleaned = cleaned.replace("\\", "")
    cleaned = cleaned.replace("{", " ").replace("}", " ")
    cleaned = cleaned.replace("$", " ")
    cleaned = _compact(cleaned)
    if len(cleaned) > max_chars:
        return cleaned[: max_chars - 3].rstrip() + "..."
    return cleaned


def _collect_sections(text: str) -> list[tuple[int, str]]:
    """
    Relevance: Operates within the P vs NP KB parsing layer.
    Concept: Internal helper implementing one deterministic step of this stage.
    Contribution: Contributes a deterministic transformation that supports end-to-end reasoning reproducibility.
    """

    sections: list[tuple[int, str]] = []
    for match in SECTION_PATTERN.finditer(text):
        sections.append((match.start(), _compact(match.group(1))))
    for match in PARAGRAPH_PATTERN.finditer(text):
        sections.append((match.start(), f"Paragraph: {_compact(match.group(1))}"))
    sections.sort(key=lambda item: item[0])
    return sections


def _section_at(position: int, sections: list[tuple[int, str]]) -> str:
    """
    Relevance: Operates within the P vs NP KB parsing layer.
    Concept: Internal helper implementing one deterministic step of this stage.
    Contribution: Contributes a deterministic transformation that supports end-to-end reasoning reproducibility.
    """

    current = "Unspecified"
    for start, title in sections:
        if start > position:
            break
        current = title
    return current


def _next_source_marker(text: str, start: int, window: int = 600) -> str:
    """
    Relevance: Operates within the P vs NP KB parsing layer.
    Concept: Internal helper implementing one deterministic step of this stage.
    Contribution: Contributes a deterministic transformation that supports end-to-end reasoning reproducibility.
    """

    snippet = text[start : start + window]
    match = SOURCE_COMMENT_PATTERN.search(snippet)
    if not match:
        return ""
    return _compact(match.group(1))


def _next_statement_id(kind: str, anchor: str, taken: set[str]) -> str:
    """
    Relevance: Operates within the P vs NP KB parsing layer.
    Concept: Internal helper implementing one deterministic step of this stage.
    Contribution: Contributes a deterministic transformation that supports end-to-end reasoning reproducibility.
    """

    short = KIND_SHORT.get(kind, "stmt")
    base = _slugify(anchor)
    candidate = f"st.{short}.{base}"
    if candidate not in taken:
        taken.add(candidate)
        return candidate

    suffix = 2
    while f"{candidate}-{suffix}" in taken:
        suffix += 1
    unique = f"{candidate}-{suffix}"
    taken.add(unique)
    return unique


def parse_report_to_statements(
    text: str,
    source_id: str,
    citation: str,
    max_informal_chars: int,
) -> dict[str, Any]:
    """
    Relevance: Operates within the P vs NP KB parsing layer.
    Concept: Primary callable implementing a stage-level behavior.
    Contribution: Contributes a deterministic transformation that supports end-to-end reasoning reproducibility.
    """

    sections = _collect_sections(text)
    taken_ids: set[str] = set()

    statements: list[dict[str, Any]] = []
    env_counts: dict[str, int] = {key: 0 for key in KIND_MAP}

    for index, match in enumerate(ENV_PATTERN.finditer(text), start=1):
        env_name = match.group(1)
        label = _compact(match.group(2) or "")
        body = (match.group(3) or "").strip()

        mapped_kind = KIND_MAP[env_name]
        confidence = CONFIDENCE_MAP.get(env_name, 0.75)
        section = _section_at(match.start(), sections)
        source_marker = _next_source_marker(text, match.end())

        anchor = label or _to_informal(body, 80) or f"item-{index}"
        statement_id = _next_statement_id(mapped_kind, anchor, taken_ids)

        notes_parts = [
            f"parsed_env: {env_name}",
            f"section: {section}",
            f"source_citation: {citation}",
        ]
        if label:
            notes_parts.append(f"label: {label}")
        if source_marker:
            notes_parts.append(f"source_marker: {source_marker}")
        if env_name == "proposition":
            notes_parts.append("normalization: proposition mapped to theorem")
        if env_name == "remark":
            notes_parts.append("normalization: remark mapped to observation")

        statement = {
            "id": statement_id,
            "kind": mapped_kind,
            "status": "accepted",
            "latex": body,
            "informal": _to_informal(body, max_informal_chars),
            "source_ids": [source_id],
            "used_symbols": [],
            "depends_on": [],
            "confidence": confidence,
            "proof_sketch": "",
            "notes": "\n".join(notes_parts),
        }
        statements.append(statement)
        env_counts[env_name] += 1

    return {
        "source": {
            "source_id": source_id,
            "type": "file",
            "citation": citation,
            "locator": "full document",
            "reliability": "high",
            "notes": "Parsed via pvsnp-kb-parser",
        },
        "stats": {
            "total_statements": len(statements),
            "environment_counts": env_counts,
        },
        "statements": statements,
    }


def _ensure_source_index_row(kb_path: Path, source: dict[str, Any]) -> None:
    """
    Relevance: Operates within the P vs NP KB parsing layer.
    Concept: Internal helper implementing one deterministic step of this stage.
    Contribution: Contributes a deterministic transformation that supports end-to-end reasoning reproducibility.
    """

    content = kb_path.read_text(encoding="utf-8")
    lines = content.splitlines()

    section_idx = None
    for i, line in enumerate(lines):
        if line.strip() == "# Source Index":
            section_idx = i
            break

    if section_idx is None:
        return

    next_heading = len(lines)
    for i in range(section_idx + 1, len(lines)):
        if lines[i].startswith("# "):
            next_heading = i
            break

    source_id = str(source.get("source_id", "")).strip()
    if not source_id:
        return

    id_pattern = re.compile(rf"\|\s*{re.escape(source_id)}\s*\|")

    row = (
        f"| {source_id} | {source.get('type', 'file')} | {source.get('citation', '')} | "
        f"{source.get('locator', 'full document')} | {source.get('reliability', 'high')} | "
        f"{source.get('notes', '')} |"
    )

    # Upsert behavior: replace matching source row if present, otherwise insert.
    for i in range(section_idx + 1, next_heading):
        if id_pattern.search(lines[i]):
            lines[i] = row
            kb_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
            return

    insert_at = None
    for i in range(section_idx + 1, next_heading):
        if lines[i].startswith("|---"):
            insert_at = i + 1
            break

    if insert_at is None:
        return

    lines.insert(insert_at, row)
    kb_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def _default_writeback_path() -> Path:
    # .../skills/ingest/pvsnp-kb-parser/scripts/parse_report.py -> .../skills
    """
    Relevance: Operates within the P vs NP KB parsing layer.
    Concept: Internal helper implementing one deterministic step of this stage.
    Contribution: Contributes a deterministic transformation that supports end-to-end reasoning reproducibility.
    """

    skills_dir = Path(__file__).resolve().parents[3]
    return skills_dir / "ingest" / "latex-kb-ingest" / "scripts" / "kb_writeback.py"


def _default_kb_template_path() -> Path:
    # .../skills/ingest/pvsnp-kb-parser/scripts/parse_report.py -> repository root
    """
    Relevance: Operates within the P vs NP KB parsing layer.
    Concept: Internal helper implementing one deterministic step of this stage.
    Contribution: Contributes a deterministic transformation that supports end-to-end reasoning reproducibility.
    """

    repo_root = Path(__file__).resolve().parents[4]
    return repo_root / "KB" / "problem-template.kb.md"


def _writeback_to_kb(args: argparse.Namespace, statements_path: Path) -> int:
    """
    Relevance: Operates within the P vs NP KB parsing layer.
    Concept: Internal helper implementing one deterministic step of this stage.
    Contribution: Contributes a deterministic transformation that supports end-to-end reasoning reproducibility.
    """

    writeback_script = (
        Path(args.writeback_script)
        if args.writeback_script
        else _default_writeback_path()
    )
    if not writeback_script.exists():
        print(
            f"[ERROR] Writeback script not found: {writeback_script}", file=sys.stderr
        )
        return 1

    command = [
        sys.executable,
        str(writeback_script),
        "--kb",
        args.kb,
        "--statements",
        str(statements_path),
        "--section-policy",
        args.section_policy,
        "--change-note",
        args.change_note,
    ]
    if args.dry_run:
        command.append("--dry-run")

    result = subprocess.run(command, check=False)
    return result.returncode


def main() -> int:
    """
    Relevance: Operates within the P vs NP KB parsing layer.
    Concept: CLI entrypoint orchestration for this script.
    Contribution: Binds parsing, computation, and artifact emission into a reproducible script execution.
    """

    logger = ReasoningLogger("pvsnp-kb-parser")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, help="Path to report file to parse.")
    parser.add_argument(
        "--output-statements", required=True, help="Path to output statements JSON."
    )
    parser.add_argument(
        "--source-id", default="src.001", help="Source ID to attach to statements."
    )
    parser.add_argument(
        "--citation",
        help="Citation label/path for the source index row (default: input path).",
    )
    parser.add_argument(
        "--max-informal-chars",
        type=int,
        default=280,
        help="Max informal summary length per statement.",
    )
    parser.add_argument("--kb", help="Optional KB file path for direct writeback.")
    parser.add_argument(
        "--init-kb-from-template",
        default=str(_default_kb_template_path()),
        help="Template used to create --kb if missing (set empty string to disable).",
    )
    parser.add_argument(
        "--section-policy",
        choices=["status", "canonical", "derived"],
        default="status",
        help="Placement policy passed to kb_writeback.py when --kb is set.",
    )
    parser.add_argument(
        "--change-note",
        default="Parsed report into PvsNP KB using pvsnp-kb-parser.",
        help="Change-log note used during KB writeback.",
    )
    parser.add_argument(
        "--writeback-script",
        help="Override path to kb_writeback.py.",
    )
    parser.add_argument(
        "--dry-run", action="store_true", help="Dry-run writeback if --kb is set."
    )
    args = parser.parse_args()
    logger.step(
        "Parsed parser arguments",
        "\n".join(
            [
                f"input={args.input}",
                f"output_statements={args.output_statements}",
                f"kb={args.kb or ''}",
                f"source_id={args.source_id}",
                f"section_policy={args.section_policy}",
                f"dry_run={args.dry_run}",
            ]
        ),
    )

    input_path = Path(args.input)
    if not input_path.exists():
        log_path = logger.finalize(
            "error", summary=f"Input report not found: {input_path}"
        )
        print(f"[LOG] {log_path}", file=sys.stderr)
        print(f"[ERROR] Input report not found: {input_path}", file=sys.stderr)
        return 1

    citation = args.citation or str(input_path)
    text = input_path.read_text(encoding="utf-8", errors="replace")

    parsed = parse_report_to_statements(
        text=text,
        source_id=args.source_id,
        citation=citation,
        max_informal_chars=args.max_informal_chars,
    )

    output_path = Path(args.output_statements)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(parsed, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )

    print(f"[OK] Parsed statements: {parsed['stats']['total_statements']}")
    print(f"[OK] Wrote JSON: {output_path}")
    logger.add_output("parsed_statements_json", output_path)
    logger.step(
        "Parsed theorem environments",
        f"statement_count={parsed['stats']['total_statements']}\nenvironment_counts={parsed['stats']['environment_counts']}",
    )

    if args.kb:
        kb_path = Path(args.kb)
        if not kb_path.exists():
            template_arg = (args.init_kb_from_template or "").strip()
            if not template_arg:
                log_path = logger.finalize(
                    "error", summary=f"KB file not found: {kb_path}"
                )
                print(f"[LOG] {log_path}", file=sys.stderr)
                print(f"[ERROR] KB file not found: {kb_path}", file=sys.stderr)
                return 1
            template_path = Path(template_arg)
            if not template_path.exists():
                log_path = logger.finalize(
                    "error",
                    summary=f"KB template not found for initialization: {template_path}",
                )
                print(f"[LOG] {log_path}", file=sys.stderr)
                print(
                    f"[ERROR] KB template not found for initialization: {template_path}",
                    file=sys.stderr,
                )
                return 1
            kb_path.parent.mkdir(parents=True, exist_ok=True)
            kb_path.write_text(
                template_path.read_text(encoding="utf-8"), encoding="utf-8"
            )
            print(f"[OK] Initialized KB from template: {kb_path}")
            logger.step(
                "Initialized missing KB from template",
                f"kb={kb_path}\ntemplate={template_path}",
            )

        if not args.dry_run:
            _ensure_source_index_row(kb_path, parsed["source"])
        rc = _writeback_to_kb(args, output_path)
        if rc != 0:
            log_path = logger.finalize(
                "error", summary=f"KB writeback failed with rc={rc}"
            )
            print(f"[LOG] {log_path}", file=sys.stderr)
            return rc
        logger.add_output("updated_kb", kb_path)

    log_path = logger.finalize(
        "success",
        summary=f"Parsed {parsed['stats']['total_statements']} statements from report.",
    )
    print(f"[LOG] {log_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
