#!/usr/bin/env python3
# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT

"""Problem-scoped InformalMathLib storage for informal proof cycles."""

from __future__ import annotations

import datetime as dt
import json
import re
from pathlib import Path
from typing import Any

from kb_context import normalize_kb_ref


MATHLIB_VERSION = 1


def _utc_now() -> str:
    return dt.datetime.now(dt.UTC).isoformat()


def _slugify(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", str(text or "").strip().lower()).strip("-")


def mathlib_root(repo_root: Path, kb_ref: str) -> Path:
    return (repo_root / "InformalMathLib" / normalize_kb_ref(kb_ref)).resolve()


def mathlib_paths(repo_root: Path, kb_ref: str) -> tuple[Path, Path]:
    root = mathlib_root(repo_root, kb_ref)
    return root / "index.json", root / "catalog.md"


def default_mathlib(*, kb_ref: str) -> dict[str, Any]:
    now = _utc_now()
    return {
        "metadata": {
            "kb_ref": normalize_kb_ref(kb_ref),
            "mathlib_version": MATHLIB_VERSION,
            "generated_utc": now,
            "updated_utc": now,
            "positive_result_count": 0,
            "negative_result_count": 0,
            "external_reference_count": 0,
            "attempt_count": 0,
        },
        "results": [],
    }


def load_mathlib_index(path: Path, *, kb_ref: str) -> dict[str, Any]:
    if not path.exists():
        return default_mathlib(kb_ref=kb_ref)
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return default_mathlib(kb_ref=kb_ref)
    if not isinstance(payload, dict):
        return default_mathlib(kb_ref=kb_ref)
    payload.setdefault("metadata", {})
    payload.setdefault("results", [])
    if not isinstance(payload["metadata"], dict):
        payload["metadata"] = {}
    if not isinstance(payload["results"], list):
        payload["results"] = []
    payload["metadata"]["kb_ref"] = normalize_kb_ref(payload["metadata"].get("kb_ref") or kb_ref)
    payload["metadata"]["mathlib_version"] = MATHLIB_VERSION
    return payload


def _refresh_mathlib_metadata(index: dict[str, Any]) -> None:
    metadata = index.setdefault("metadata", {})
    results = [row for row in index.get("results", []) if isinstance(row, dict)]
    metadata["mathlib_version"] = MATHLIB_VERSION
    metadata["updated_utc"] = _utc_now()
    metadata["positive_result_count"] = sum(
        1 for row in results if str(row.get("outcome", "")).strip().lower() == "proved"
    )
    metadata["negative_result_count"] = sum(
        1
        for row in results
        if str(row.get("outcome", "")).strip().lower() in {"disproved", "prior_art_found", "blocked"}
    )
    metadata["external_reference_count"] = sum(
        1
        for row in results
        if str(row.get("entry_kind", "")).strip().lower() == "external-reference"
        or str(row.get("outcome", "")).strip().lower() == "external_reference"
    )
    metadata["attempt_count"] = len(results)


def save_mathlib_index(index: dict[str, Any], *, json_path: Path, md_path: Path) -> None:
    _refresh_mathlib_metadata(index)
    json_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.write_text(json.dumps(index, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    md_path.write_text(render_mathlib_catalog(index), encoding="utf-8")


def append_mathlib_result(index: dict[str, Any], result: dict[str, Any]) -> None:
    results = [row for row in index.get("results", []) if isinstance(row, dict)]
    existing_idx = next(
        (
            idx
            for idx, row in enumerate(results)
            if str(row.get("result_id", "")).strip() == str(result.get("result_id", "")).strip()
        ),
        -1,
    )
    materialized = dict(result)
    materialized["updated_utc"] = _utc_now()
    if existing_idx >= 0:
        results[existing_idx] = materialized
    else:
        results.append(materialized)
    results.sort(key=lambda row: (str(row.get("updated_utc", "")), str(row.get("result_id", ""))), reverse=True)
    index["results"] = results
    _refresh_mathlib_metadata(index)


def write_mathlib_entry_file(
    repo_root: Path,
    *,
    kb_ref: str,
    result: dict[str, Any],
    proof_markdown: str,
) -> Path:
    root = mathlib_root(repo_root, kb_ref)
    outcome = str(result.get("outcome", "")).strip().lower()
    entry_kind = str(result.get("entry_kind", "")).strip().lower()
    if entry_kind == "external-reference" or outcome == "external_reference":
        bucket = "external-references"
    elif outcome == "proved":
        bucket = "positive-results"
    else:
        bucket = "negative-results"
    title_slug = _slugify(str(result.get("title", result.get("result_id", "result"))))[:80] or "result"
    path = root / bucket / f"{str(result.get('result_id', '')).strip() or title_slug}-{title_slug}.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    body = [
        f"# {result.get('title', result.get('result_id', 'Result'))}",
        "",
        f"- Result ID: {result.get('result_id', '')}",
        f"- Outcome: {result.get('outcome', '')}",
        f"- KB ref: {normalize_kb_ref(kb_ref)}",
        f"- Queue ID: {result.get('queue_id', '')}",
        f"- Attempt ID: {result.get('attempt_id', '')}",
        f"- Bridge ID: {result.get('bridge_id', '')}",
        f"- Source statement: {result.get('source_statement_id', '')}",
        f"- Target statement: {result.get('target_statement_id', '')}",
        f"- Web search used: {bool(result.get('web_search_used', False))}",
        f"- Entry kind: {result.get('entry_kind', 'result')}",
        "",
        "## Statement",
        "",
        str(result.get("statement", "")).strip(),
        "",
        "## Summary",
        "",
        str(result.get("summary", "")).strip(),
        "",
    ]
    produced_paper_tex = str(result.get("produced_paper_tex", "")).strip()
    produced_paper_pdf = str(result.get("produced_paper_pdf", "")).strip()
    if produced_paper_tex or produced_paper_pdf:
        body.extend(
            [
                "## Produced Paper",
                "",
                f"- TeX: {produced_paper_tex}",
                f"- PDF: {produced_paper_pdf}",
                "",
            ]
        )
    if entry_kind == "external-reference" or outcome == "external_reference":
        body.extend(
            [
                "## External Reference Metadata",
                "",
                f"- Reference type: {result.get('reference_type', '')}",
                f"- Source name: {result.get('source_name', '')}",
                f"- Source URL: {result.get('source_url', '')}",
                f"- Search query: {result.get('search_query', '')}",
                f"- Used for: {result.get('used_for', '')}",
                "",
                "## Imported Reference Notes",
                "",
                str(proof_markdown or "").rstrip(),
                "",
            ]
        )
    else:
        body.extend(
            [
                "## Informal Proof Or Disproof",
                "",
                str(proof_markdown or "").rstrip(),
                "",
            ]
        )
    path.write_text("\n".join(body).rstrip() + "\n", encoding="utf-8")
    return path


def write_mathlib_result_file(
    repo_root: Path,
    *,
    kb_ref: str,
    result: dict[str, Any],
    proof_markdown: str,
) -> Path:
    return write_mathlib_entry_file(
        repo_root,
        kb_ref=kb_ref,
        result=result,
        proof_markdown=proof_markdown,
    )


def render_mathlib_catalog(index: dict[str, Any]) -> str:
    metadata = index.get("metadata", {}) if isinstance(index.get("metadata"), dict) else {}
    results = [row for row in index.get("results", []) if isinstance(row, dict)]
    lines = [
        "# InformalMathLib Catalog",
        "",
        f"- KB ref: {metadata.get('kb_ref', '')}",
        f"- Updated (UTC): {metadata.get('updated_utc', '')}",
        f"- Positive results: {metadata.get('positive_result_count', 0)}",
        f"- Negative or blocking results: {metadata.get('negative_result_count', 0)}",
        f"- External references: {metadata.get('external_reference_count', 0)}",
        f"- Recorded attempts: {metadata.get('attempt_count', 0)}",
        "",
        "| Result ID | Kind | Outcome | Title | Bridge | Target | File |",
        "|---|---|---|---|---|---|---|",
    ]
    for row in results:
        lines.append(
            "| "
            f"{row.get('result_id', '')} | {row.get('entry_kind', 'result')} | {row.get('outcome', '')} | {row.get('title', '')} | "
            f"{row.get('bridge_id', '')} | {row.get('target_statement_id', '')} | {row.get('artifact_path', '')} |"
        )
    if not results:
        lines.append("| - | - | - | - | - | - | - |")
    lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def search_mathlib(index: dict[str, Any], query_terms: list[str], *, limit: int = 5) -> list[dict[str, Any]]:
    normalized_terms = [_slugify(term) for term in query_terms if _slugify(term)]
    if not normalized_terms:
        return []
    scored: list[tuple[float, dict[str, Any]]] = []
    for row in index.get("results", []) if isinstance(index.get("results"), list) else []:
        if not isinstance(row, dict):
            continue
        haystack = " ".join(
            [
                str(row.get("title", "")),
                str(row.get("statement", "")),
                str(row.get("summary", "")),
                str(row.get("reference_type", "")),
                str(row.get("source_name", "")),
                str(row.get("used_for", "")),
                " ".join(str(tag) for tag in row.get("tags", []) if str(tag).strip())
                if isinstance(row.get("tags"), list)
                else "",
            ]
        ).lower()
        score = sum(1.0 for term in normalized_terms if term and term.replace("-", " ") in haystack)
        if score <= 0.0:
            continue
        scored.append((score, row))
    scored.sort(key=lambda item: (item[0], str(item[1].get("updated_utc", ""))), reverse=True)
    return [row for _, row in scored[: max(1, limit)]]
