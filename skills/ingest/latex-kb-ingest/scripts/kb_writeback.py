#!/usr/bin/env python3
# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
# 
# SPDX-License-Identifier: MIT

"""Append normalized statement records into a KB markdown file.

Input statement JSON formats:
- list of statement objects
- object with key "statements" containing a list
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import sys
from pathlib import Path
from typing import Any

import yaml

_COMMON_DIR = Path(__file__).resolve().parents[3] / "common"
if str(_COMMON_DIR) not in sys.path:
    sys.path.insert(0, str(_COMMON_DIR))

from reasoning_log import ReasoningLogger

_KIND_SHORT = {
    "definition": "def",
    "axiom": "ax",
    "theorem": "thm",
    "lemma": "lem",
    "corollary": "cor",
    "conjecture": "conj",
    "observation": "obs",
}

_ALLOWED_KINDS = set(_KIND_SHORT)
_ALLOWED_STATUS = {"accepted", "tentative", "rejected"}

_ORDERED_KEYS = [
    "id",
    "kind",
    "status",
    "latex",
    "informal",
    "source_ids",
    "used_symbols",
    "depends_on",
    "confidence",
    "proof_sketch",
    "notes",
]


def _slugify(text: str) -> str:
    """
    Relevance: Operates within the ingestion and KB writeback layer.
    Concept: Stable naming and path-derivation helper for artifact routing.
    Contribution: Contributes a deterministic transformation that supports end-to-end reasoning reproducibility.
    """

    slug = text.lower()
    slug = re.sub(r"\$+", "", slug)
    slug = re.sub(r"[^a-z0-9]+", "-", slug)
    slug = re.sub(r"-{2,}", "-", slug).strip("-")
    return slug[:40] if slug else "item"


def _parse_existing_ids(kb_content: str) -> set[str]:
    """
    Relevance: Operates within the ingestion and KB writeback layer.
    Concept: Internal helper implementing one deterministic step of this stage.
    Contribution: Contributes a deterministic transformation that supports end-to-end reasoning reproducibility.
    """

    return set(re.findall(r"(?m)^id:\s*([A-Za-z0-9._-]+)\s*$", kb_content))


def _ensure_list_of_str(value: Any) -> list[str]:
    """
    Relevance: Operates within the ingestion and KB writeback layer.
    Concept: Internal helper implementing one deterministic step of this stage.
    Contribution: Contributes a deterministic transformation that supports end-to-end reasoning reproducibility.
    """

    if value is None:
        return []
    if isinstance(value, list):
        return [str(item) for item in value if str(item).strip()]
    return [str(value)]


def _clamp_confidence(value: Any) -> float:
    """
    Relevance: Operates within the ingestion and KB writeback layer.
    Concept: Internal helper implementing one deterministic step of this stage.
    Contribution: Contributes a deterministic transformation that supports end-to-end reasoning reproducibility.
    """

    try:
        confidence = float(value)
    except (TypeError, ValueError):
        confidence = 0.5
    return max(0.0, min(1.0, confidence))


def _next_unique_id(base_id: str, taken: set[str]) -> str:
    """
    Relevance: Operates within the ingestion and KB writeback layer.
    Concept: Internal helper implementing one deterministic step of this stage.
    Contribution: Contributes a deterministic transformation that supports end-to-end reasoning reproducibility.
    """

    if base_id not in taken:
        taken.add(base_id)
        return base_id
    suffix = 2
    while f"{base_id}-{suffix}" in taken:
        suffix += 1
    candidate = f"{base_id}-{suffix}"
    taken.add(candidate)
    return candidate


def _generate_id(statement: dict[str, Any], taken: set[str]) -> str:
    """
    Relevance: Operates within the ingestion and KB writeback layer.
    Concept: Internal helper implementing one deterministic step of this stage.
    Contribution: Contributes a deterministic transformation that supports end-to-end reasoning reproducibility.
    """

    kind = str(statement.get("kind", "observation")).strip().lower()
    short = _KIND_SHORT.get(kind, "stmt")
    anchor_text = str(statement.get("informal") or statement.get("latex") or "item")
    base = _slugify(anchor_text)
    return _next_unique_id(f"st.{short}.{base}", taken)


def _normalize_statement(raw: dict[str, Any], taken_ids: set[str]) -> dict[str, Any]:
    """
    Relevance: Operates within the ingestion and KB writeback layer.
    Concept: Normalization of input structures into stable internal forms.
    Contribution: Reduces runtime ambiguity and prevents malformed artifacts from destabilizing the workflow.
    """

    statement: dict[str, Any] = {}

    kind = str(raw.get("kind", "observation")).strip().lower()
    if kind not in _ALLOWED_KINDS:
        kind = "observation"

    status = str(raw.get("status", "tentative")).strip().lower()
    if status not in _ALLOWED_STATUS:
        status = "tentative"

    statement_id = str(raw.get("id", "")).strip()
    if statement_id:
        statement_id = _next_unique_id(statement_id, taken_ids)
    else:
        statement_id = _generate_id({"kind": kind, **raw}, taken_ids)

    statement["id"] = statement_id
    statement["kind"] = kind
    statement["status"] = status
    statement["latex"] = str(raw.get("latex", "")).strip()
    statement["informal"] = str(raw.get("informal", "")).strip()
    statement["source_ids"] = _ensure_list_of_str(raw.get("source_ids"))
    statement["used_symbols"] = _ensure_list_of_str(raw.get("used_symbols"))
    statement["depends_on"] = _ensure_list_of_str(raw.get("depends_on"))
    statement["confidence"] = _clamp_confidence(raw.get("confidence", 0.5))
    statement["proof_sketch"] = str(raw.get("proof_sketch", "")).rstrip()
    statement["notes"] = str(raw.get("notes", "")).rstrip()

    return statement


def _statement_to_yaml_block(statement: dict[str, Any]) -> str:
    """
    Relevance: Operates within the ingestion and KB writeback layer.
    Concept: Internal helper implementing one deterministic step of this stage.
    Contribution: Contributes a deterministic transformation that supports end-to-end reasoning reproducibility.
    """

    ordered = {key: statement.get(key, "") for key in _ORDERED_KEYS}
    yaml_text = yaml.safe_dump(
        ordered,
        sort_keys=False,
        default_flow_style=False,
        allow_unicode=False,
        width=1000,
    ).strip()
    return f"```yaml\n{yaml_text}\n```"


def _ensure_section(content: str, heading: str) -> str:
    """
    Relevance: Operates within the ingestion and KB writeback layer.
    Concept: Internal helper implementing one deterministic step of this stage.
    Contribution: Contributes a deterministic transformation that supports end-to-end reasoning reproducibility.
    """

    marker = f"# {heading}\n"
    if marker in content:
        return content
    if not content.endswith("\n"):
        content += "\n"
    return content + f"\n# {heading}\n\n"


def _append_blocks_to_section(content: str, heading: str, blocks: list[str]) -> str:
    """
    Relevance: Operates within the ingestion and KB writeback layer.
    Concept: Internal helper implementing one deterministic step of this stage.
    Contribution: Contributes a deterministic transformation that supports end-to-end reasoning reproducibility.
    """

    if not blocks:
        return content

    marker = f"# {heading}\n"
    start = content.find(marker)
    if start < 0:
        raise ValueError(f"Section not found: {heading}")

    section_start = start + len(marker)
    next_heading = content.find("\n# ", section_start)
    if next_heading < 0:
        next_heading = len(content)

    section_body = content[section_start:next_heading].rstrip()
    block_text = "\n\n".join(blocks)

    if section_body:
        new_body = section_body + "\n\n" + block_text + "\n"
    else:
        new_body = "\n" + block_text + "\n"

    return content[:section_start] + new_body + content[next_heading:]


def _append_changelog(content: str, message: str) -> str:
    """
    Relevance: Operates within the ingestion and KB writeback layer.
    Concept: Internal helper implementing one deterministic step of this stage.
    Contribution: Contributes a deterministic transformation that supports end-to-end reasoning reproducibility.
    """

    heading = "Change Log"
    content = _ensure_section(content, heading)

    marker = f"# {heading}\n"
    start = content.find(marker)
    section_start = start + len(marker)
    next_heading = content.find("\n# ", section_start)
    if next_heading < 0:
        next_heading = len(content)

    today = dt.datetime.now(dt.UTC).strftime("%Y-%m-%d")
    entry = f"- {today}: {message}"
    section_body = content[section_start:next_heading].rstrip()

    if section_body:
        section_body = section_body + "\n" + entry + "\n"
    else:
        section_body = "\n" + entry + "\n"

    return content[:section_start] + section_body + content[next_heading:]


def _load_statement_payload(path: Path) -> list[dict[str, Any]]:
    """
    Relevance: Operates within the ingestion and KB writeback layer.
    Concept: Loading and structuring external artifacts for deterministic processing.
    Contribution: Provides clean, typed inputs so downstream reasoning steps remain auditable.
    """

    payload = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(payload, list):
        raw_statements = payload
    elif isinstance(payload, dict) and isinstance(payload.get("statements"), list):
        raw_statements = payload["statements"]
    else:
        raise ValueError("Statement JSON must be a list or an object containing a 'statements' list.")

    statements: list[dict[str, Any]] = []
    for item in raw_statements:
        if isinstance(item, dict):
            statements.append(item)
    return statements


def main() -> int:
    """
    Relevance: Operates within the ingestion and KB writeback layer.
    Concept: CLI entrypoint orchestration for this script.
    Contribution: Binds parsing, computation, and artifact emission into a reproducible script execution.
    """

    logger = ReasoningLogger("latex-kb-ingest")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--kb", required=True, help="Path to KB markdown file.")
    parser.add_argument("--statements", required=True, help="Path to extracted statements JSON file.")
    parser.add_argument(
        "--section-policy",
        choices=["status", "canonical", "derived"],
        default="status",
        help="Placement policy for new statements (default: status).",
    )
    parser.add_argument(
        "--change-note",
        default="Applied automated KB writeback from extracted statements.",
        help="Change Log note to append.",
    )
    parser.add_argument("--dry-run", action="store_true", help="Validate and summarize without writing KB.")
    args = parser.parse_args()
    logger.step(
        "Parsed writeback arguments",
        "\n".join(
            [
                f"kb={args.kb}",
                f"statements={args.statements}",
                f"section_policy={args.section_policy}",
                f"dry_run={args.dry_run}",
            ]
        ),
    )

    kb_path = Path(args.kb)
    statements_path = Path(args.statements)

    if not kb_path.exists():
        log_path = logger.finalize("error", summary=f"KB file not found: {kb_path}")
        print(f"[LOG] {log_path}", file=sys.stderr)
        print(f"[ERROR] KB file not found: {kb_path}", file=sys.stderr)
        return 1
    if not statements_path.exists():
        log_path = logger.finalize("error", summary=f"Statements file not found: {statements_path}")
        print(f"[LOG] {log_path}", file=sys.stderr)
        print(f"[ERROR] Statements file not found: {statements_path}", file=sys.stderr)
        return 1

    try:
        raw_statements = _load_statement_payload(statements_path)
    except Exception as exc:
        log_path = logger.finalize("error", summary=f"Failed to load statements: {exc}")
        print(f"[LOG] {log_path}", file=sys.stderr)
        print(f"[ERROR] Failed to load statements: {exc}", file=sys.stderr)
        return 1
    logger.step("Loaded statement payload", f"raw_statement_count={len(raw_statements)}")

    kb_content = kb_path.read_text(encoding="utf-8")
    kb_content = _ensure_section(kb_content, "Canonical Statements")
    kb_content = _ensure_section(kb_content, "Derived Statements")

    taken_ids = _parse_existing_ids(kb_content)
    normalized = [_normalize_statement(item, taken_ids) for item in raw_statements]

    canonical_blocks: list[str] = []
    derived_blocks: list[str] = []
    for statement in normalized:
        block = _statement_to_yaml_block(statement)

        if args.section_policy == "canonical":
            canonical_blocks.append(block)
        elif args.section_policy == "derived":
            derived_blocks.append(block)
        else:
            if statement["status"] == "accepted":
                canonical_blocks.append(block)
            else:
                derived_blocks.append(block)

    if args.dry_run:
        print(f"[DRY-RUN] Canonical additions: {len(canonical_blocks)}")
        print(f"[DRY-RUN] Derived additions: {len(derived_blocks)}")
        print(f"[DRY-RUN] KB target: {kb_path}")
        logger.add_output("kb_target", kb_path)
        log_path = logger.finalize(
            "success",
            summary=f"Dry run with {len(canonical_blocks)} canonical and {len(derived_blocks)} derived additions.",
        )
        print(f"[LOG] {log_path}")
        return 0

    kb_content = _append_blocks_to_section(kb_content, "Canonical Statements", canonical_blocks)
    kb_content = _append_blocks_to_section(kb_content, "Derived Statements", derived_blocks)
    kb_content = _append_changelog(
        kb_content,
        f"{args.change_note} Added {len(canonical_blocks)} canonical and {len(derived_blocks)} derived statements.",
    )

    kb_path.write_text(kb_content, encoding="utf-8")
    logger.add_output("updated_kb", kb_path)

    print(f"[OK] Updated KB: {kb_path}")
    print(f"[OK] Canonical additions: {len(canonical_blocks)}")
    print(f"[OK] Derived additions: {len(derived_blocks)}")
    log_path = logger.finalize(
        "success",
        summary=f"Applied {len(canonical_blocks)} canonical and {len(derived_blocks)} derived additions.",
    )
    print(f"[LOG] {log_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
