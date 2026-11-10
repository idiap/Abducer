#!/usr/bin/env python3
# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT

"""Import a curated complexity-theory KB package into the P vs NP KB.

The package is expected to contain `kb.jsonl` and `relations.csv`, as produced
by the curated complexity_theory_kb export. This script keeps the import
idempotent: statement IDs and relation IDs are stable, existing rows are not
duplicated, and a machine-readable import summary is written for validation.
"""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import json
import re
import shutil
import tempfile
import zipfile
from collections import Counter
from pathlib import Path
from typing import Any


FORMAL_ENTRY_TYPES = {"Definition", "Theorem", "Lemma", "Corollary", "Core result"}

KIND_MAP = {
    "Definition": "definition",
    "Theorem": "theorem",
    "Lemma": "lemma",
    "Corollary": "corollary",
    "Core result": "theorem",
    "Concept": "observation",
    "Claim": "observation",
}

KIND_SHORT = {
    "definition": "def",
    "theorem": "thm",
    "lemma": "lem",
    "corollary": "cor",
    "observation": "obs",
}

CONFIDENCE_MAP = {
    "Definition": 0.95,
    "Theorem": 0.86,
    "Lemma": 0.84,
    "Corollary": 0.82,
    "Core result": 0.86,
    "Concept": 0.78,
    "Claim": 0.72,
}

SOURCE_ROWS = {
    "kozen2006": {
        "source_id": "src.complexity.kozen2006",
        "type": "package",
        "citation": "complexity_theory_kb.zip",
        "locator": "kb.jsonl source_id=kozen2006",
        "reliability": "high",
        "notes": "Curated complexity-theory KB package; imported with entry-level provenance.",
    },
    "np_ch2": {
        "source_id": "src.complexity.np-ch2",
        "type": "package",
        "citation": "complexity_theory_kb.zip",
        "locator": "kb.jsonl source_id=np_ch2",
        "reliability": "high",
        "notes": "Curated NP chapter extraction in complexity-theory KB package; imported with entry-level provenance.",
    },
}


def _slugify(text: str) -> str:
    slug = text.lower()
    slug = re.sub(r"[^a-z0-9]+", "-", slug)
    return re.sub(r"-{2,}", "-", slug).strip("-") or "item"


def _statement_id(entry: dict[str, Any]) -> str:
    kind = KIND_MAP.get(entry.get("entry_type", ""), "observation")
    short = KIND_SHORT[kind]
    return f"st.{short}.complexity.{_slugify(str(entry['entry_id']))}"


def _relation_id(index: int) -> str:
    return f"rel.complexity.{index:03d}"


def _source_id(package_source_id: str) -> str:
    if package_source_id not in SOURCE_ROWS:
        return f"src.complexity.{_slugify(package_source_id)}"
    return SOURCE_ROWS[package_source_id]["source_id"]


def _compact(text: str) -> str:
    return re.sub(r"\s+", " ", text or "").strip()


def _informal(entry: dict[str, Any]) -> str:
    name = _compact(str(entry.get("name", "")))
    statement = _compact(str(entry.get("statement", "")))
    significance = _compact(str(entry.get("significance", "")))
    if name and statement:
        base = f"{name}: {statement}"
    else:
        base = statement or name
    if significance:
        return f"{base} Significance: {significance}"
    return base


def _block_scalar(key: str, value: str) -> list[str]:
    if not value:
        return [f"{key}: ''"]
    lines = [f"{key}: |-"]
    for line in str(value).splitlines() or [""]:
        lines.append(f"  {line.rstrip()}")
    return lines


def _list_scalar(key: str, values: list[str]) -> list[str]:
    if not values:
        return [f"{key}: []"]
    lines = [f"{key}:"]
    lines.extend(f"- {value}" for value in values)
    return lines


def _yaml_block(statement: dict[str, Any]) -> str:
    lines: list[str] = [
        "```yaml",
        f"id: {statement['id']}",
        f"kind: {statement['kind']}",
        f"status: {statement['status']}",
        *_block_scalar("latex", statement["latex"]),
        *_block_scalar("informal", statement["informal"]),
        *_list_scalar("source_ids", statement["source_ids"]),
        "used_symbols: []",
        "depends_on: []",
        f"confidence: {statement['confidence']:.2f}",
        "proof_sketch: ''",
        *_block_scalar("notes", statement["notes"]),
        "```",
    ]
    return "\n".join(lines)


def _notes(entry: dict[str, Any], package_zip: Path) -> str:
    tags = entry.get("tags") or []
    if not isinstance(tags, list):
        tags = [str(tags)]
    parts = [
        "imported_from: complexity_theory_kb.zip",
        f"source_archive: {package_zip}",
        f"package_entry_id: {entry.get('entry_id', '')}",
        f"package_source_id: {entry.get('source_id', '')}",
        f"module_id: {entry.get('module_id', '')}",
        f"entry_type: {entry.get('entry_type', '')}",
        f"label: {entry.get('label', '')}",
        f"name: {entry.get('name', '')}",
        f"pdf_page: {entry.get('pdf_page', '')}",
        f"printed_page: {entry.get('printed_page', '')}",
        f"importance: {entry.get('importance', '')}",
        f"tags: {', '.join(str(tag) for tag in tags)}",
        f"extraction_scope: {entry.get('extraction_scope', '')}",
        f"review_status: {entry.get('review_status', '')}",
    ]
    significance = _compact(str(entry.get("significance", "")))
    if significance:
        parts.append(f"significance: {significance}")
    if entry.get("entry_type") == "Core result":
        parts.append("normalization: Core result imported as theorem-level canonical statement.")
    elif entry.get("entry_type") in {"Concept", "Claim"}:
        parts.append(f"normalization: {entry.get('entry_type')} imported as derived observation.")
    return "\n".join(parts)


def _statement(entry: dict[str, Any], package_zip: Path) -> dict[str, Any]:
    entry_type = str(entry.get("entry_type", "Concept"))
    return {
        "id": _statement_id(entry),
        "kind": KIND_MAP.get(entry_type, "observation"),
        "status": "accepted" if entry.get("review_status") == "curated" else "tentative",
        "latex": str(entry.get("statement", "")).strip(),
        "informal": _informal(entry),
        "source_ids": [_source_id(str(entry.get("source_id", "")))],
        "confidence": CONFIDENCE_MAP.get(entry_type, 0.70),
        "notes": _notes(entry, package_zip),
    }


def _read_package(package_zip: Path) -> tuple[list[dict[str, Any]], list[dict[str, str]], dict[str, str]]:
    with tempfile.TemporaryDirectory(prefix="complexity-kb-import-") as tmp:
        tmp_path = Path(tmp)
        with zipfile.ZipFile(package_zip) as archive:
            archive.extractall(tmp_path)
        candidates = list(tmp_path.rglob("kb.jsonl"))
        if not candidates:
            raise FileNotFoundError("kb.jsonl not found in package")
        package_dir = candidates[0].parent
        entries = [json.loads(line) for line in (package_dir / "kb.jsonl").read_text().splitlines() if line.strip()]
        with (package_dir / "relations.csv").open(newline="") as handle:
            relations = list(csv.DictReader(handle))
        validation_text = (package_dir / "VALIDATION.txt").read_text() if (package_dir / "VALIDATION.txt").exists() else ""
        readme_text = (package_dir / "README.md").read_text() if (package_dir / "README.md").exists() else ""
        return entries, relations, {"validation": validation_text, "readme": readme_text}


def _copy_package_files(package_zip: Path, artifact_dir: Path) -> None:
    artifact_dir.mkdir(parents=True, exist_ok=True)
    shutil.copy2(package_zip, artifact_dir / package_zip.name)
    with zipfile.ZipFile(package_zip) as archive:
        archive.extractall(artifact_dir / "extracted")


def _parse_existing_statement_ids(content: str) -> set[str]:
    return set(re.findall(r"(?m)^id:\s*([A-Za-z0-9._-]+)\s*$", content))


def _parse_existing_relation_ids(content: str) -> set[str]:
    return set(re.findall(r"\|\s*(rel\.complexity\.[0-9]{3})\s*\|", content))


def _escape_table_cell(text: str) -> str:
    return _compact(text).replace("|", "\\|")


def _source_table_row(row: dict[str, str]) -> str:
    return (
        f"| {row['source_id']} | {row['type']} | {_escape_table_cell(row['citation'])} | "
        f"{_escape_table_cell(row['locator'])} | {row['reliability']} | {_escape_table_cell(row['notes'])} |"
    )


def _ensure_source_rows(content: str) -> tuple[str, int]:
    insert_rows = []
    for source_row in SOURCE_ROWS.values():
        if f"| {source_row['source_id']} |" not in content:
            insert_rows.append(_source_table_row(source_row))
    if not insert_rows:
        return content, 0
    marker = "\n# Symbol Glossary"
    if marker not in content:
        raise ValueError("Could not find Symbol Glossary section after Source Index")
    # Keep the Markdown source table contiguous. Existing KBs often have one
    # blank line before the next section; insert new rows before that blank.
    split_marker = "\n\n# Symbol Glossary"
    if split_marker in content:
        return content.replace(split_marker, "\n" + "\n".join(insert_rows) + split_marker, 1), len(insert_rows)
    return content.replace(marker, "\n" + "\n".join(insert_rows) + marker, 1), len(insert_rows)


def _append_blocks_to_section(content: str, heading: str, blocks: list[str]) -> str:
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
    body = content[section_start:next_heading].rstrip()
    addition = "\n\n".join(blocks)
    if body:
        new_body = body + "\n\n" + addition + "\n"
    else:
        new_body = "\n" + addition + "\n"
    return content[:section_start] + new_body + content[next_heading:]


def _ensure_relations_section(content: str) -> str:
    if "# Imported Relations\n" in content:
        return content
    marker = "\n# Open Gaps"
    section = (
        "\n# Imported Relations\n\n"
        "| relation_id | subject_statement_id | predicate | object_statement_id | package_subject_id | package_object_id | note |\n"
        "|---|---|---|---|---|---|---|\n"
    )
    if marker in content:
        return content.replace(marker, section + marker, 1)
    return content.rstrip() + section + "\n"


def _append_relations(
    content: str,
    relations: list[dict[str, str]],
    entry_to_statement: dict[str, str],
) -> tuple[str, int]:
    content = _ensure_relations_section(content)
    existing = _parse_existing_relation_ids(content)
    rows: list[str] = []
    for index, relation in enumerate(relations, start=1):
        rel_id = _relation_id(index)
        if rel_id in existing:
            continue
        rows.append(
            "| {rel_id} | {subject} | {predicate} | {object} | {package_subject} | {package_object} | {note} |".format(
                rel_id=rel_id,
                subject=entry_to_statement.get(relation["subject_id"], ""),
                predicate=_escape_table_cell(relation["predicate"]),
                object=entry_to_statement.get(relation["object_id"], ""),
                package_subject=_escape_table_cell(relation["subject_id"]),
                package_object=_escape_table_cell(relation["object_id"]),
                note=_escape_table_cell(relation.get("note", "")),
            )
        )
    if not rows:
        return content, 0
    marker = "# Imported Relations\n"
    start = content.find(marker)
    if start < 0:
        raise ValueError("Imported Relations section missing after creation")
    section_start = start + len(marker)
    next_heading = content.find("\n# ", section_start)
    if next_heading < 0:
        next_heading = len(content)
    section = content[section_start:next_heading].rstrip()
    new_section = section + "\n" + "\n".join(rows) + "\n"
    return content[:section_start] + new_section + content[next_heading:], len(rows)


def _append_changelog(content: str, message: str) -> str:
    marker = "# Change Log\n"
    if marker not in content:
        content = content.rstrip() + "\n\n# Change Log\n"
    line = f"- {dt.date.today().isoformat()}: {message}"
    if line in content:
        return content
    start = content.find(marker) + len(marker)
    return content[:start] + "\n" + line + content[start:]


def _validate(content: str, expected_ids: set[str]) -> dict[str, Any]:
    ids = re.findall(r"(?m)^id:\s*([A-Za-z0-9._-]+)\s*$", content)
    counts = Counter(ids)
    duplicates = sorted(item for item, count in counts.items() if count > 1)
    missing = sorted(expected_ids - set(ids))
    return {
        "total_statement_ids_in_kb": len(ids),
        "duplicate_statement_ids": duplicates,
        "missing_imported_statement_ids": missing,
        "valid": not duplicates and not missing,
    }


def import_package(package_zip: Path, kb_path: Path, artifact_dir: Path, dry_run: bool = False) -> dict[str, Any]:
    entries, relations, package_meta = _read_package(package_zip)
    entry_to_statement = {str(entry["entry_id"]): _statement_id(entry) for entry in entries}

    content = kb_path.read_text()
    existing_ids = _parse_existing_statement_ids(content)
    content, source_rows_added = _ensure_source_rows(content)

    canonical_blocks: list[str] = []
    derived_blocks: list[str] = []
    imported_ids: set[str] = set()
    skipped_existing = 0

    for entry in entries:
        statement = _statement(entry, package_zip)
        imported_ids.add(statement["id"])
        if statement["id"] in existing_ids:
            skipped_existing += 1
            continue
        block = _yaml_block(statement)
        if entry.get("entry_type") in FORMAL_ENTRY_TYPES:
            canonical_blocks.append(block)
        else:
            derived_blocks.append(block)

    content = _append_blocks_to_section(content, "Canonical Statements", canonical_blocks)
    content = _append_blocks_to_section(content, "Derived Statements", derived_blocks)
    content, relation_rows_added = _append_relations(content, relations, entry_to_statement)
    content = _append_changelog(
        content,
        "Imported complexity_theory_kb.zip into P vs NP KB "
        f"({len(canonical_blocks)} canonical, {len(derived_blocks)} derived, "
        f"{relation_rows_added} relations added; {skipped_existing} statements already present).",
    )

    validation = _validate(content, imported_ids)
    if not validation["valid"]:
        raise ValueError(f"Import validation failed: {validation}")

    summary = {
        "package_zip": str(package_zip),
        "kb_path": str(kb_path),
        "artifact_dir": str(artifact_dir),
        "entries_total": len(entries),
        "relations_total": len(relations),
        "entry_type_counts": dict(Counter(str(entry.get("entry_type", "")) for entry in entries)),
        "package_source_counts": dict(Counter(str(entry.get("source_id", "")) for entry in entries)),
        "source_rows_added": source_rows_added,
        "canonical_added": len(canonical_blocks),
        "derived_added": len(derived_blocks),
        "relations_added": relation_rows_added,
        "skipped_existing_statements": skipped_existing,
        "package_validation_excerpt": package_meta["validation"].strip().splitlines()[:10],
        "validation": validation,
    }

    if not dry_run:
        artifact_dir.mkdir(parents=True, exist_ok=True)
        _copy_package_files(package_zip, artifact_dir)
        kb_path.write_text(content)
        (artifact_dir / "import_summary.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n")
    return summary


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--package-zip", required=True, type=Path)
    parser.add_argument("--kb", default=Path("KB/p-vs-np.kb.md"), type=Path)
    parser.add_argument(
        "--artifact-dir",
        default=Path("artifacts/p-vs-np/complexity-theory-kb"),
        type=Path,
    )
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    summary = import_package(
        package_zip=args.package_zip.resolve(),
        kb_path=args.kb,
        artifact_dir=args.artifact_dir,
        dry_run=args.dry_run,
    )
    print(json.dumps(summary, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
