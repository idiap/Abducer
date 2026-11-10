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

"""Render the current surfaced reasoning state as a terminal dashboard."""

from __future__ import annotations

import argparse
import json
import re
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Any

from rich.console import Console
from rich.console import Group
from rich.layout import Layout
from rich.live import Live
from rich.panel import Panel
from rich.table import Table
from rich.text import Text


def _clean_text(value: Any) -> str:
    return " ".join(str(value or "").strip().split())


def _first_nonempty(*values: Any) -> str:
    for value in values:
        text = _clean_text(value)
        if text:
            return text
    return ""


def _truncate(text: Any, limit: int = 120) -> str:
    cleaned = _clean_text(text)
    if len(cleaned) <= limit:
        return cleaned
    return cleaned[: max(0, limit - 3)].rstrip() + "..."


def _ensure_dict(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def _ensure_list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def _load_json(path: Path) -> dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}
    return payload if isinstance(payload, dict) else {}


def _parse_timestamp(value: Any) -> datetime:
    text = str(value or "").strip()
    if not text:
        return datetime.min
    try:
        return datetime.fromisoformat(text.replace("Z", "+00:00"))
    except ValueError:
        return datetime.min


def _latex_to_terminal(text: str) -> str:
    """Convert the small LaTeX fragment set used by PDL into terminal-friendly Unicode."""

    rendered = str(text or "")
    replacements = {
        r"\Rightarrow": "⇒",
        r"\rightarrow": "→",
        r"\twoheadrightarrow": "↠",
        r"\leadsto": "⇝",
        r"\vdash": "⊢",
        r"\parallel": "∥",
        r"\circ": "∘",
        r"\sim": "∼",
        r"\approx": "≈",
        r"\neq": "≠",
        r"\in": "∈",
        r"\notin": "∉",
        r"\subseteq": "⊆",
        r"\supseteq": "⊇",
        r"\cap": "∩",
        r"\cup": "∪",
        r"\{": "{",
        r"\}": "}",
        r"\_": "_",
        r"\textbackslash{}": "\\",
    }
    for src, dst in replacements.items():
        rendered = rendered.replace(src, dst)
    rendered = re.sub(r"\\mathsf\{([^}]*)\}", r"\1", rendered)
    rendered = re.sub(r"\\text\{([^}]*)\}", r"\1", rendered)
    rendered = re.sub(r"\\mathrm\{([^}]*)\}", r"\1", rendered)
    rendered = re.sub(r"\\mathbb\{([^}]*)\}", r"\1", rendered)
    rendered = re.sub(r"\\mathcal\{([^}]*)\}", r"\1", rendered)
    rendered = rendered.replace("$", "")
    rendered = re.sub(r"\s+", " ", rendered).strip()
    return rendered


def _discover_kb_ref(record: dict[str, Any]) -> str:
    context = _ensure_dict(record.get("context"))
    kb_ref = _clean_text(context.get("kb_ref"))
    if kb_ref:
        return kb_ref
    for row in _ensure_list(record.get("outputs")):
        if not isinstance(row, dict):
            continue
        path_text = _clean_text(row.get("path"))
        match = re.search(r"artifacts[/\\]([^/\\]+)[/\\]", path_text)
        if match:
            return _clean_text(match.group(1))
    return ""


def _detail_rows(moment: dict[str, Any]) -> list[str]:
    return [_clean_text(row) for row in _ensure_list(moment.get("details")) if _clean_text(row)]


def _detail_pairs(moment: dict[str, Any]) -> list[tuple[str, str]]:
    pairs: list[tuple[str, str]] = []
    for row in _detail_rows(moment):
        if "=" not in row:
            continue
        key, value = row.split("=", 1)
        key_norm = _clean_text(key).lower().replace(" ", "_")
        if re.fullmatch(r"[a-z0-9_.-]+", key_norm):
            pairs.append((key_norm, _clean_text(value)))
    return pairs


def _detail_lookup(moment: dict[str, Any], *keys: str) -> str:
    wanted = {_clean_text(key).lower().replace(" ", "_") for key in keys if _clean_text(key)}
    for key, value in _detail_pairs(moment):
        if key in wanted and value:
            return value
    return ""


def _format_metric_value(value: Any) -> str:
    if isinstance(value, float):
        return f"{value:.3f}".rstrip("0").rstrip(".")
    return _clean_text(value)


def _metric_summary(moment: dict[str, Any], *, limit: int = 4) -> str:
    metrics = _ensure_dict(moment.get("metrics"))
    if not metrics:
        return ""
    parts: list[str] = []
    for key, value in metrics.items():
        value_text = _format_metric_value(value)
        if value_text:
            parts.append(f"{key}={value_text}")
        if len(parts) >= limit:
            break
    return ", ".join(parts)


def _first_anchor(program: dict[str, Any], *tokens: str) -> dict[str, Any]:
    anchors = [row for row in _ensure_list(program.get("anchors")) if isinstance(row, dict)]
    tokens_norm = [_clean_text(token).lower() for token in tokens if _clean_text(token)]
    for row in anchors:
        haystack = " ".join(
            [
                _clean_text(row.get("anchor_id")).lower(),
                _clean_text(row.get("anchor_type")).lower(),
                _clean_text(row.get("label")).lower(),
            ]
        )
        if any(token in haystack for token in tokens_norm):
            return row
    return anchors[0] if anchors else {}


def _pdl_semantic_context(pdl: dict[str, Any]) -> dict[str, str]:
    program = _ensure_dict(pdl.get("program"))
    metadata = _ensure_dict(program.get("metadata"))
    target = _ensure_dict(program.get("target"))
    bridge = _ensure_dict(program.get("bridge_object"))
    positive_route = _ensure_dict(program.get("positive_route"))
    conceptual_nexus = _ensure_dict(program.get("conceptual_nexus"))
    source_anchor = _first_anchor(program, "source")
    target_anchor = _first_anchor(program, "target")
    proof_debt = [_clean_text(row) for row in _ensure_list(program.get("proof_debt")) if _clean_text(row)]
    tensions = [_clean_text(row) for row in _ensure_list(program.get("tensions")) if _clean_text(row)]
    return {
        "program_title": _first_nonempty(metadata.get("title")),
        "program_id": _first_nonempty(metadata.get("program_id")),
        "program_kind": _first_nonempty(metadata.get("kind")),
        "program_stage": _first_nonempty(metadata.get("stage")),
        "target_label": _first_nonempty(target.get("label"), target.get("target_id")),
        "target_statement": _first_nonempty(target.get("statement")),
        "bridge_label": _first_nonempty(bridge.get("label")),
        "bridge_kind": _first_nonempty(bridge.get("kind")),
        "bridge_invariant": _first_nonempty(bridge.get("invariant")),
        "route_lemma": _first_nonempty(positive_route.get("route_lemma")),
        "nexus_summary": _first_nonempty(conceptual_nexus.get("summary")),
        "proof_debt": proof_debt[0] if proof_debt else "",
        "tension": tensions[0] if tensions else "",
        "source_excerpt": _first_nonempty(source_anchor.get("content"), source_anchor.get("label")),
        "target_excerpt": _first_nonempty(target_anchor.get("content"), target_anchor.get("label")),
    }


def _semantic_topic(moment: dict[str, Any]) -> str:
    pdl = _ensure_dict(moment.get("pdl"))
    semantic = _pdl_semantic_context(pdl)
    return _first_nonempty(
        semantic.get("program_title"),
        semantic.get("target_label"),
        semantic.get("bridge_label"),
        _detail_lookup(moment, "headline", "detail", "summary"),
        moment.get("focus"),
        moment.get("title"),
    )


def _moment_primary_detail(moment: dict[str, Any]) -> str:
    preferred = _first_nonempty(
        _detail_lookup(moment, "headline"),
        _detail_lookup(moment, "detail"),
        _detail_lookup(moment, "summary"),
        _detail_lookup(moment, "reason"),
    )
    if preferred:
        return preferred
    semantic = _pdl_semantic_context(_ensure_dict(moment.get("pdl")))
    semantic_detail = _first_nonempty(
        semantic.get("nexus_summary"),
        semantic.get("tension"),
        semantic.get("proof_debt"),
    )
    if semantic_detail:
        return semantic_detail
    ignored = {
        "path",
        "status",
        "phase",
        "cycle_count",
        "max_cycles",
        "next_phase",
        "next_phase_before_dispatch",
        "stop_status",
        "stop_reason",
        "high_reward_signal_id",
        "plausibility_score",
        "plausible_solution_detected",
        "kb_ref",
        "artifacts_dir",
    }
    for key, value in _detail_pairs(moment):
        if key not in ignored and value:
            return f"{key}={value}"
    for row in _detail_rows(moment):
        if not row.startswith("path="):
            return row
    return _metric_summary(moment)


def _moment_summary(moment: dict[str, Any]) -> str:
    topic = _truncate(_semantic_topic(moment), 110)
    detail = _truncate(_moment_primary_detail(moment), 140)
    if detail and detail != topic:
        return f"{topic} | {detail}" if topic else detail
    return topic


def _format_epistemic_state(state: dict[str, Any], *, limit: int = 5) -> str:
    parts: list[str] = []
    for key, value in state.items():
        value_text = _format_metric_value(value)
        if value_text:
            parts.append(f"{key}={value_text}")
        if len(parts) >= limit:
            break
    return ", ".join(parts)


def _control_object_labels(rows: list[Any]) -> str:
    labels: list[str] = []
    for row in rows:
        if isinstance(row, dict):
            label = _clean_text(row.get("title")) or _clean_text(row.get("id"))
        else:
            label = _clean_text(row)
        if label:
            labels.append(label)
    return ", ".join(labels)


def load_surface_records(surfaces_root: Path) -> list[dict[str, Any]]:
    """Load all surfaced reasoning JSON files under the reasoning-surfaces root."""

    rows: list[dict[str, Any]] = []
    if not surfaces_root.exists():
        return rows
    for path in surfaces_root.glob("*/*.json"):
        payload = _load_json(path)
        if not payload:
            continue
        payload["_path"] = str(path)
        payload["_agent"] = _clean_text(payload.get("agent")) or path.parent.name
        payload["_kb_ref"] = _discover_kb_ref(payload)
        rows.append(payload)
    rows.sort(key=lambda row: _parse_timestamp(row.get("started_utc")), reverse=True)
    return rows


def filter_surface_records(
    records: list[dict[str, Any]],
    *,
    kb_ref: str = "",
    run_id: str = "",
    agent: str = "",
) -> list[dict[str, Any]]:
    """Filter surfaced reasoning records by problem, run id, and agent."""

    kb_ref_norm = _clean_text(kb_ref)
    run_id_norm = _clean_text(run_id)
    agent_norm = _clean_text(agent)
    filtered: list[dict[str, Any]] = []
    for row in records:
        if kb_ref_norm and _clean_text(row.get("_kb_ref")) != kb_ref_norm:
            continue
        if run_id_norm and _clean_text(row.get("run_id")) != run_id_norm:
            continue
        if agent_norm and _clean_text(row.get("_agent")) != agent_norm:
            continue
        filtered.append(row)
    return filtered


def _latest_moment(record: dict[str, Any]) -> dict[str, Any]:
    moments = [row for row in _ensure_list(record.get("moments")) if isinstance(row, dict)]
    moments.sort(key=lambda row: _parse_timestamp(row.get("timestamp")), reverse=True)
    return moments[0] if moments else {}


def _all_moments(records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for record in records:
        for moment in _ensure_list(record.get("moments")):
            if not isinstance(moment, dict):
                continue
            rows.append(
                {
                    **moment,
                    "_agent": _clean_text(record.get("_agent")),
                    "_run_id": _clean_text(record.get("run_id")),
                    "_kb_ref": _clean_text(record.get("_kb_ref")),
                }
            )
    rows.sort(key=lambda row: _parse_timestamp(row.get("timestamp")), reverse=True)
    return rows


def _recent_moments(records: list[dict[str, Any]], limit: int) -> list[dict[str, Any]]:
    rows = _all_moments(records)
    return rows[: max(1, limit)]


def _select_focus_moment(rows: list[dict[str, Any]]) -> dict[str, Any]:
    """Prefer the latest substantive moment over terminal bookkeeping moments."""

    if not rows:
        return {}
    for row in rows:
        kind = _clean_text(row.get("kind"))
        if _ensure_dict(row.get("pdl")):
            return row
        if kind not in {"run_result", "artifact_emitted"}:
            return row
    return rows[0]


def _select_timeline_moments(rows: list[dict[str, Any]], limit: int) -> list[dict[str, Any]]:
    """Prefer substantive reasoning moments in the timeline before bookkeeping moments."""

    if not rows:
        return []
    preferred = [
        row
        for row in rows
        if _clean_text(row.get("kind")) not in {"run_result", "artifact_emitted"}
    ]
    if len(preferred) >= limit:
        return preferred[:limit]
    combined = preferred + [row for row in rows if row not in preferred]
    return combined[:limit]


def _operation_display_text(operation: dict[str, Any]) -> str:
    latex_form = _clean_text(operation.get("latex_form"))
    form = _clean_text(operation.get("form")) or _clean_text(operation.get("id"))
    preferred = _latex_to_terminal(latex_form or form)
    title = _clean_text(operation.get("title"))
    detail = _clean_text(operation.get("detail")) or _clean_text(operation.get("effect"))
    parts = [preferred]
    if title:
        parts.append(title)
    if detail:
        parts.append(detail)
    return " | ".join(parts)


def _judgment_display_text(judgment: dict[str, Any]) -> str:
    form = _latex_to_terminal(_clean_text(judgment.get("latex_form")) or _clean_text(judgment.get("form")))
    meaning = _clean_text(judgment.get("meaning"))
    detail = _clean_text(judgment.get("detail"))
    parts = [form]
    if meaning:
        parts.append(meaning)
    if detail:
        parts.append(detail)
    return " | ".join(parts)


def build_snapshot(records: list[dict[str, Any]], *, max_moments: int) -> dict[str, Any]:
    """Build the current reasoning snapshot used by the terminal dashboard."""

    all_moments = _all_moments(records)
    recent = _select_timeline_moments(all_moments, max(1, max_moments))
    latest_record = records[0] if records else {}
    latest_moment = _select_focus_moment(all_moments)
    latest_run_id = _clean_text(latest_record.get("run_id"))
    run_ids = sorted(
        {
            _clean_text(row.get("run_id"))
            for row in records
            if _clean_text(row.get("run_id"))
        }
    )
    latest_pdl = _ensure_dict(latest_moment.get("pdl"))
    latest_semantic = _pdl_semantic_context(latest_pdl)
    agent_rows = []
    for record in sorted(records, key=lambda row: _parse_timestamp(_latest_moment(row).get("timestamp")), reverse=True):
        moment = _latest_moment(record)
        agent_rows.append(
            {
                "agent": _clean_text(record.get("_agent")),
                "status": _clean_text(record.get("status")) or "running",
                "focus": _clean_text(moment.get("focus")) or _clean_text(moment.get("title")),
                "summary": _moment_summary(moment),
                "stage": _clean_text(moment.get("stage")),
                "timestamp": _clean_text(moment.get("timestamp")),
            }
        )
    return {
        "record_count": len(records),
        "agent_count": len({ _clean_text(row.get("_agent")) for row in records if _clean_text(row.get("_agent")) }),
        "kb_ref": _clean_text(latest_record.get("_kb_ref")),
        "run_id": latest_run_id if len(run_ids) <= 1 else f"mixed/{len(run_ids)}",
        "latest_record": latest_record,
        "latest_moment": latest_moment,
        "latest_pdl": latest_pdl,
        "latest_topic": _semantic_topic(latest_moment),
        "latest_semantic": latest_semantic,
        "agent_rows": agent_rows,
        "recent_moments": recent,
    }


def _render_header(snapshot: dict[str, Any]) -> Panel:
    lines = [
        f"KB: {snapshot.get('kb_ref') or 'all'}",
        f"Run ID: {snapshot.get('run_id') or 'mixed/latest'}",
        f"Agents: {snapshot.get('agent_count', 0)}",
        f"Surface records: {snapshot.get('record_count', 0)}",
    ]
    topic = _truncate(snapshot.get("latest_topic"), 120)
    if topic:
        lines.append(f"Topic: {topic}")
    return Panel("\n".join(lines), title="Show Reasoning", border_style="cyan")


def _render_agents(snapshot: dict[str, Any]) -> Panel:
    table = Table(expand=True)
    table.add_column("Agent", style="bold")
    table.add_column("Status")
    table.add_column("Stage")
    table.add_column("Content", overflow="fold")
    table.add_column("Updated")
    for row in snapshot.get("agent_rows", [])[:10]:
        table.add_row(
            row["agent"],
            row["status"],
            row["stage"],
            row["summary"] or row["focus"],
            row["timestamp"],
        )
    if table.row_count == 0:
        table.add_row("-", "-", "-", "No surfaced reasoning records found.", "-")
    return Panel(table, title="Agents", border_style="blue")


def _render_timeline(snapshot: dict[str, Any]) -> Panel:
    lines: list[Any] = []
    for row in snapshot.get("recent_moments", []):
        prefix = Text(f"{row.get('_agent', '')} ", style="bold cyan")
        body = Text(f"{row.get('kind', '')}: {row.get('title', '')}", style="white")
        focus = _clean_text(row.get("focus"))
        if focus:
            body.append(f" | {focus}", style="magenta")
        summary = _moment_summary(row)
        entry: list[Any] = [prefix + body]
        if summary and summary not in {_clean_text(row.get("title")), focus}:
            entry.append(Text(f"  {summary}", style="white"))
        lines.append(Group(*entry))
    if not lines:
        lines = [Text("No surfaced reasoning moments found.")]
    return Panel(Group(*lines), title="Recent Moments", border_style="green")


def _render_current_reasoning(snapshot: dict[str, Any]) -> Panel:
    moment = _ensure_dict(snapshot.get("latest_moment"))
    if not moment:
        return Panel("No current reasoning moment is available.", title="Current Reasoning", border_style="yellow")
    semantic = _ensure_dict(snapshot.get("latest_semantic"))
    detail = _moment_primary_detail(moment)
    parts: list[Any] = [
        Text(moment.get("title", ""), style="bold"),
    ]
    topic = _truncate(_semantic_topic(moment), 120)
    if topic and topic != _clean_text(moment.get("title")):
        parts.append(Text(f"Topic: {topic}", style="bold yellow"))
    if _clean_text(moment.get("focus")):
        parts.append(Text(f"Focus: {moment.get('focus')}", style="magenta"))
    if detail:
        parts.append(Text(f"Current detail: {_truncate(detail, 180)}", style="cyan"))
    if _clean_text(semantic.get("target_label")):
        parts.append(Text(f"Target: {_truncate(semantic.get('target_label'), 130)}", style="white"))
    elif _clean_text(semantic.get("target_statement")):
        parts.append(Text(f"Target: {_truncate(semantic.get('target_statement'), 130)}", style="white"))
    if _clean_text(semantic.get("bridge_label")):
        bridge_line = f"Bridge object: {_truncate(semantic.get('bridge_label'), 100)}"
        if _clean_text(semantic.get("bridge_invariant")):
            bridge_line += f" | invariant: {_truncate(semantic.get('bridge_invariant'), 70)}"
        parts.append(Text(bridge_line, style="green"))
    if _clean_text(semantic.get("tension")):
        parts.append(Text(f"Open tension: {_truncate(semantic.get('tension'), 150)}", style="yellow"))
    elif _clean_text(semantic.get("proof_debt")):
        parts.append(Text(f"Proof debt: {_truncate(semantic.get('proof_debt'), 150)}", style="yellow"))
    if _clean_text(semantic.get("source_excerpt")):
        parts.append(Text(f"From: {_truncate(semantic.get('source_excerpt'), 150)}", style="white"))
    if _clean_text(semantic.get("target_excerpt")):
        parts.append(Text(f"To: {_truncate(semantic.get('target_excerpt'), 150)}", style="white"))
    if _clean_text(moment.get("significance")):
        parts.append(Text(f"Why it matters: {moment.get('significance')}", style="white"))
    notes: list[Text] = []
    for row in _detail_rows(moment):
        if row == detail or row == f"detail={detail}" or row == f"headline={detail}" or row == f"summary={detail}":
            continue
        if row.startswith("path="):
            continue
        notes.append(Text(f"- {_truncate(row, 140)}"))
    if notes:
        parts.append(Text("Notes:", style="bold"))
        parts.extend(notes[:6])
    return Panel(Group(*parts), title="Current Reasoning", border_style="yellow")


def _render_pdl(snapshot: dict[str, Any]) -> Panel:
    pdl = _ensure_dict(snapshot.get("latest_pdl"))
    if not pdl:
        return Panel("No PDL/material-inference payload was surfaced for the latest moment.", title="PDL / Material Inference", border_style="magenta")
    rows: list[Any] = []
    program = _ensure_dict(pdl.get("program"))
    metadata = _ensure_dict(program.get("metadata"))
    target = _ensure_dict(program.get("target"))
    semantic = _pdl_semantic_context(pdl)
    if metadata or target:
        rows.append(Text(f"Program: {metadata.get('program_id', '')} [{metadata.get('kind', '')} | {metadata.get('stage', '')}]", style="bold"))
        if _clean_text(semantic.get("program_title")):
            rows.append(Text(f"Title: {_truncate(semantic.get('program_title'), 120)}", style="white"))
        if _clean_text(semantic.get("target_label")):
            rows.append(Text(f"Target: {_truncate(semantic.get('target_label'), 120)}", style="white"))
        elif _clean_text(target.get("statement")):
            rows.append(Text(f"Target: {_truncate(target.get('statement'), 150)}", style="white"))
        if _clean_text(semantic.get("bridge_label")):
            bridge_line = f"Bridge: {_truncate(semantic.get('bridge_label'), 100)}"
            if _clean_text(semantic.get("bridge_kind")):
                bridge_line += f" | {_truncate(semantic.get('bridge_kind'), 80)}"
            rows.append(Text(bridge_line, style="cyan"))
        if _clean_text(semantic.get("bridge_invariant")):
            rows.append(Text(f"Invariant: {_truncate(semantic.get('bridge_invariant'), 120)}", style="cyan"))
        if _clean_text(semantic.get("route_lemma")):
            rows.append(Text(f"Route lemma: {_truncate(semantic.get('route_lemma'), 120)}", style="yellow"))
        if _clean_text(semantic.get("tension")):
            rows.append(Text(f"Tension: {_truncate(semantic.get('tension'), 140)}", style="yellow"))
        if _clean_text(semantic.get("nexus_summary")):
            rows.append(Text(f"Nexus: {_truncate(semantic.get('nexus_summary'), 150)}", style="magenta"))
        if _clean_text(semantic.get("source_excerpt")):
            rows.append(Text(f"From: {_truncate(semantic.get('source_excerpt'), 140)}", style="white"))
        if _clean_text(semantic.get("target_excerpt")):
            rows.append(Text(f"To: {_truncate(semantic.get('target_excerpt'), 140)}", style="white"))
    state_summary = _format_epistemic_state(_ensure_dict(pdl.get("epistemic_state")))
    if state_summary:
        rows.append(Text(f"State: {state_summary}", style="magenta"))
    operations = [row for row in _ensure_list(pdl.get("operations")) if isinstance(row, dict)]
    if operations:
        rows.append(Text("Material inferences:", style="bold cyan"))
        for row in operations[:8]:
            display = _operation_display_text(row)
            rows.append(Text(f"• {display}", style="cyan"))
    judgments = [row for row in _ensure_list(pdl.get("judgments")) if isinstance(row, dict)]
    if judgments:
        rows.append(Text("Judgments:", style="bold green"))
        for row in judgments[:6]:
            rows.append(Text(f"• {_judgment_display_text(row)}", style="green"))
    controls = [row for row in _ensure_list(pdl.get("control_objects")) if isinstance(row, dict)]
    label = _control_object_labels(controls)
    if label:
        rows.append(Text(f"Control objects: {label}", style="magenta"))
    program_controls = _control_object_labels(_ensure_list(program.get("control_objects")))
    if program_controls and program_controls != label:
        rows.append(Text(f"Program controls: {program_controls}", style="magenta"))
    if not rows:
        rows = [Text("PDL payload is present but empty.")]
    return Panel(Group(*rows), title="PDL / Material Inference", border_style="magenta")


def render_dashboard(snapshot: dict[str, Any]) -> Layout:
    """Render the live dashboard layout for one reasoning snapshot."""

    layout = Layout()
    layout.split_column(
        Layout(name="header", size=7),
        Layout(name="body"),
    )
    layout["header"].update(_render_header(snapshot))
    layout["body"].split_row(
        Layout(name="left"),
        Layout(name="right"),
    )
    layout["left"].split_column(
        Layout(name="agents"),
        Layout(name="timeline"),
    )
    layout["right"].split_column(
        Layout(name="current"),
        Layout(name="pdl"),
    )
    layout["left"]["agents"].update(_render_agents(snapshot))
    layout["left"]["timeline"].update(_render_timeline(snapshot))
    layout["right"]["current"].update(_render_current_reasoning(snapshot))
    layout["right"]["pdl"].update(_render_pdl(snapshot))
    return layout


def _resolve_repo_root() -> Path:
    return Path(__file__).resolve().parents[4]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--kb-ref", default="", help="Optional KB reference filter.")
    parser.add_argument("--run-id", default="", help="Optional run-id filter.")
    parser.add_argument("--agent", default="", help="Optional agent-name filter.")
    parser.add_argument("--max-moments", type=int, default=18, help="Maximum number of recent moments to display.")
    parser.add_argument("--refresh", type=float, default=1.0, help="Refresh interval in seconds for watch mode.")
    parser.add_argument("--watch", action="store_true", help="Continuously refresh the dashboard.")
    parser.add_argument("--surfaces-root", default="", help="Optional artifacts/reasoning-surfaces root.")
    args = parser.parse_args()

    repo_root = _resolve_repo_root()
    surfaces_root = Path(args.surfaces_root) if args.surfaces_root else (repo_root / "artifacts" / "reasoning-surfaces")
    if not surfaces_root.is_absolute():
        surfaces_root = (repo_root / surfaces_root).resolve()

    console = Console()

    def _build_layout() -> Layout:
        records = load_surface_records(surfaces_root)
        filtered = filter_surface_records(
            records,
            kb_ref=args.kb_ref,
            run_id=args.run_id,
            agent=args.agent,
        )
        snapshot = build_snapshot(filtered, max_moments=max(1, args.max_moments))
        return render_dashboard(snapshot)

    if not args.watch:
        console.print(_build_layout())
        return 0

    with Live(_build_layout(), console=console, refresh_per_second=max(1, int(1 / max(args.refresh, 0.2))), screen=True) as live:
        while True:
            live.update(_build_layout())
            time.sleep(max(args.refresh, 0.2))


if __name__ == "__main__":
    raise SystemExit(main())
