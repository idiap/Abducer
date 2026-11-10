#!/usr/bin/env python3
# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT

"""Validate structured Looper TODO cards."""

from __future__ import annotations

from pathlib import Path
import json

from agentic_common import ROOT, clean_text, fail, load_json_array, load_json_object, rel


SCHEMA = ROOT / "agentic" / "todos" / "todo_schema.yaml"
TODOS = ROOT / "agentic" / "todos"
LIST_FIELDS = {
    "use_skills",
    "required_artifact",
    "acceptance_criteria",
    "blocked_by",
    "evidence",
    "failure_modes",
    "dependencies",
    "required_artifacts",
    "validation",
    "validation_commands",
}


def strip_yaml_value(raw: str) -> str:
    value = raw.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {'"', "'"}:
        return value[1:-1]
    return value


def fallback_load_todo_yaml(path: Path) -> list:
    """Parse the repo's TODO-card YAML subset when PyYAML is unavailable."""
    lines = path.read_text(encoding="utf-8").splitlines()
    created_at = ""
    implementation_status = ""
    for raw in lines:
        if raw.startswith("created_at:"):
            created_at = strip_yaml_value(raw.split(":", 1)[1])
        if raw.startswith("  status:") and not implementation_status:
            implementation_status = strip_yaml_value(raw.split(":", 1)[1])
    try:
        start = next(index for index, line in enumerate(lines) if line.strip() == "todos:")
    except StopIteration:
        fail(f"{rel(path)} is not JSON-compatible YAML and has no fallback-parsable todos section")
    rows: list[dict] = []
    current: dict | None = None
    index = start + 1
    while index < len(lines):
        line = lines[index]
        stripped = line.strip()
        if not stripped:
            index += 1
            continue
        if line.startswith("  - id:"):
            if current is not None:
                rows.append(current)
            current = {}
            first = line[4:]
            if ":" in first:
                key, value = first.split(":", 1)
                current[key.strip()] = strip_yaml_value(value)
            index += 1
            continue
        if current is None or not line.startswith("    "):
            index += 1
            continue
        field_text = line[4:]
        if ":" not in field_text:
            index += 1
            continue
        key, value = field_text.split(":", 1)
        key = key.strip()
        value = value.strip()
        if value == ">":
            collected: list[str] = []
            index += 1
            while index < len(lines) and (lines[index].startswith("      ") or not lines[index].strip()):
                collected.append(lines[index].strip())
                index += 1
            current[key] = clean_text(" ".join(collected))
            continue
        if key in LIST_FIELDS and not value:
            items: list[str] = []
            index += 1
            while index < len(lines):
                item_line = lines[index]
                item_stripped = item_line.strip()
                if not item_stripped:
                    index += 1
                    continue
                if item_line.startswith("      - "):
                    items.append(strip_yaml_value(item_line[8:]))
                    index += 1
                    continue
                if item_line.startswith("        ") and items:
                    items[-1] = clean_text(f"{items[-1]} {item_stripped}")
                    index += 1
                    continue
                break
            current[key] = items
            continue
        if key in LIST_FIELDS and value == "[]":
            current[key] = []
        elif key in LIST_FIELDS and value.startswith("[") and value.endswith("]"):
            try:
                current[key] = json.loads(value.replace("'", '"'))
            except json.JSONDecodeError:
                current[key] = [strip_yaml_value(item) for item in value.strip("[]").split(",") if clean_text(item)]
        else:
            current[key] = strip_yaml_value(value)
        index += 1
    if current is not None:
        rows.append(current)
    if not rows:
        fail(f"{rel(path)} fallback parser found no TODO rows")
    default_status = "resolved" if implementation_status in {"completed", "implemented"} else "open"
    for row in rows:
        if "skill" in row and "use_skills" not in row:
            row["use_skills"] = [row["skill"]]
        if "proposed_skill" in row and "use_skills" not in row:
            row["use_skills"] = [row["proposed_skill"]]
        if "required_artifacts" in row and "required_artifact" not in row:
            row["required_artifact"] = row["required_artifacts"]
        if "dependencies" in row and "blocked_by" not in row:
            row["blocked_by"] = row["dependencies"]
        if "promotion_criterion" in row and "acceptance_criteria" not in row:
            criteria = [row["promotion_criterion"]]
            if isinstance(row.get("validation"), list):
                criteria.extend(row["validation"])
            row["acceptance_criteria"] = criteria
        if "demotion_criterion" in row and "failure_modes" not in row:
            row["failure_modes"] = [row["demotion_criterion"]]
        row.setdefault("type", "workflow_todo")
        row.setdefault("phase", clean_text(row.get("module")) or "paper-result-elaboration")
        row.setdefault("owner", "skills/results_ellaboration")
        row.setdefault("risk_class", "domain_specific_todo")
        row.setdefault("intent", clean_text(row.get("why_needed")) or clean_text(row.get("result_artifact")) or clean_text(row.get("title")))
        row.setdefault("required_artifact", [clean_text(row.get("result_artifact"))] if clean_text(row.get("result_artifact")) else [])
        row.setdefault("blocked_by", [])
        row.setdefault("evidence", [clean_text(row.get("result_artifact"))] if clean_text(row.get("result_artifact")) else [])
        if isinstance(row.get("priority"), str) and row["priority"].isdigit():
            row["priority"] = int(row["priority"])
        if isinstance(row.get("priority"), int):
            row["priority"] = "critical" if row["priority"] >= 90 else "high" if row["priority"] >= 70 else "medium"
        row.setdefault("review_date", created_at)
        row.setdefault("status", default_status)
    return rows


def load_todo_rows(path: Path) -> list:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
        if isinstance(payload, list):
            return payload
        fail(f"{rel(path)} must be a TODO array or an object with a todos array")
    except json.JSONDecodeError:
        try:
            import yaml
        except Exception as exc:
            return fallback_load_todo_yaml(path)
        try:
            payload = yaml.safe_load(path.read_text(encoding="utf-8"))
        except Exception:
            # Several historical decks intentionally use the repository's
            # Markdown-friendly TODO-card subset (for example unquoted
            # backtick list items).  Validation must not change merely because
            # PyYAML happens to be installed in the locked environment.
            return fallback_load_todo_yaml(path)
        if isinstance(payload, list):
            return payload
        if isinstance(payload, dict) and isinstance(payload.get("todos"), list):
            review_date = clean_text(
                payload.get("implementation_status", {}).get("completed_at")
                if isinstance(payload.get("implementation_status"), dict)
                else ""
            ) or clean_text(payload.get("created_at"))
            rows = payload["todos"]
            status = clean_text(
                payload.get("implementation_status", {}).get("status")
                if isinstance(payload.get("implementation_status"), dict)
                else ""
            )
            if review_date:
                for row in rows:
                    if isinstance(row, dict):
                        row.setdefault("review_date", review_date)
            for row in rows:
                if not isinstance(row, dict):
                    continue
                if "skill" in row and "use_skills" not in row:
                    row["use_skills"] = [row["skill"]]
                if "proposed_skill" in row and "use_skills" not in row:
                    row["use_skills"] = [row["proposed_skill"]]
                if "required_artifacts" in row and "required_artifact" not in row:
                    row["required_artifact"] = row["required_artifacts"]
                if "dependencies" in row and "blocked_by" not in row:
                    row["blocked_by"] = row["dependencies"]
                if "promotion_criterion" in row and "acceptance_criteria" not in row:
                    criteria = [row["promotion_criterion"]]
                    if isinstance(row.get("validation"), list):
                        criteria.extend(row["validation"])
                    row["acceptance_criteria"] = criteria
                if "demotion_criterion" in row and "failure_modes" not in row:
                    row["failure_modes"] = [row["demotion_criterion"]]
                row.setdefault("type", "workflow_todo")
                row.setdefault("phase", clean_text(row.get("module")) or "paper-result-elaboration")
                row.setdefault("owner", "skills/results_ellaboration")
                row.setdefault("risk_class", clean_text(payload.get("schema")) or "domain_specific_todo")
                row.setdefault("intent", clean_text(row.get("why_needed")) or clean_text(row.get("result_artifact")) or clean_text(row.get("title")))
                row.setdefault("required_artifact", [clean_text(row.get("result_artifact"))] if clean_text(row.get("result_artifact")) else [])
                row.setdefault("blocked_by", [])
                if "source_artifacts" in payload and isinstance(payload.get("source_artifacts"), dict):
                    row.setdefault("evidence", [clean_text(item) for item in payload["source_artifacts"].values() if clean_text(item)])
                else:
                    row.setdefault("evidence", [clean_text(payload.get("source_paper"))] if clean_text(payload.get("source_paper")) else [])
                if isinstance(row.get("priority"), int):
                    row["priority"] = "critical" if row["priority"] >= 90 else "high" if row["priority"] >= 70 else "medium"
                row.setdefault("status", "resolved" if status == "completed" else "open")
            return rows
        fail(f"{rel(path)} must be a TODO array or an object with a todos array")


def validate_todo_file(path: Path, schema: dict) -> int:
    rows = load_todo_rows(path)
    seen: set[str] = set()
    for row in rows:
        if not isinstance(row, dict):
            fail(f"{rel(path)} TODO entries must be objects")
        for field in schema["required_fields"]:
            if field not in row:
                fail(f"{rel(path)} {row.get('id')} missing {field}")
        todo_id = clean_text(row.get("id"))
        if not todo_id or todo_id in seen:
            fail(f"{rel(path)} missing or duplicate id: {todo_id}")
        seen.add(todo_id)
        if row["type"] not in schema["allowed_type"]:
            fail(f"{rel(path)} {todo_id} invalid type: {row['type']}")
        if row["status"] not in schema["allowed_status"]:
            fail(f"{rel(path)} {todo_id} invalid status: {row['status']}")
        if row["priority"] not in schema["allowed_priority"]:
            fail(f"{rel(path)} {todo_id} invalid priority: {row['priority']}")
        for list_field in ["use_skills", "required_artifact", "acceptance_criteria", "blocked_by", "evidence", "failure_modes"]:
            if not isinstance(row[list_field], list):
                fail(f"{rel(path)} {todo_id} {list_field} must be a list")
        if todo_id.startswith(("DWF-", "YM21-")):
            commands = row.get("validation_commands")
            if not isinstance(commands, list) or not commands or not all(
                isinstance(command, str) and clean_text(command) for command in commands
            ):
                fail(f"{rel(path)} {todo_id} requires executable validation_commands")
        if row["status"] == "resolved" and not row["evidence"]:
            fail(f"{rel(path)} {todo_id} resolved without evidence")
    unknown_blockers = sorted({blocker for row in rows for blocker in row["blocked_by"] if blocker not in seen})
    if unknown_blockers:
        fail(f"{rel(path)} unknown blockers: {', '.join(unknown_blockers)}")
    return len(rows)


def main() -> int:
    schema = load_json_object(SCHEMA)
    paths = sorted(TODOS.glob("*_todos.yaml"))
    if not paths:
        fail("no TODO files found")
    total = 0
    for path in paths:
        total += validate_todo_file(path, schema)
    print(f"validated {total} TODO cards across {len(paths)} TODO files")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
