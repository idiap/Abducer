#!/usr/bin/env python3
# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT

"""Build a dynamic typed graph of reasoning-process evolution from reasoning logs."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import shlex
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

_COMMON_DIR = Path(__file__).resolve().parents[3] / "common"
if str(_COMMON_DIR) not in sys.path:
    sys.path.insert(0, str(_COMMON_DIR))

from kb_context import kb_ref_from_artifacts_dir
from kb_context import kb_ref_from_kb_filename
from kb_context import normalize_kb_ref
from reasoning_log import ReasoningLogger


HEADER_AGENT_RE = re.compile(r"^# Reasoning Log:\s*(.+?)\s*$", re.MULTILINE)
FIELD_RE = {
    "started_utc": re.compile(r"^- Started \(UTC\):\s*(.+?)\s*$", re.MULTILINE),
    "run_id": re.compile(r"^- Run ID:\s*(.+?)\s*$", re.MULTILINE),
    "status": re.compile(r"^- Status:\s*(.+?)\s*$", re.MULTILINE),
    "ended_utc": re.compile(r"^- Ended \(UTC\):\s*(.+?)\s*$", re.MULTILINE),
    "summary": re.compile(r"^- Summary:\s*(.+?)\s*$", re.MULTILINE),
}
STEP_HEADER_RE = re.compile(r"^## Step @\s*(.+?)\s*$")
INLINE_OUTPUT_RE = re.compile(r"^Output:\s*(.+?)\s*->\s*(.+?)\s*$")
DECLARED_OUTPUT_RE = re.compile(r"^-\s*(.+?)\s*:\s*(.+?)\s*$")
# Skills are organized both directly below ``skills/`` and below thematic
# folders such as ``skills/orchestration/``.  Capture the actual skill folder
# in either layout so the legacy process graph retains its agent edges after
# the thematic-folder migration.
SKILL_SCRIPT_RE = re.compile(r"/skills/(?:[^/\s]+/)?([^/\s]+)/scripts/([A-Za-z0-9._-]+\.py)")
RUN_STAGE_RE = re.compile(r"^Running stage:\s*(.+?)\s*$")
DONE_STAGE_RE = re.compile(r"^Completed stage:\s*(.+?)\s*$")


@dataclass(frozen=True)
class ParsedStep:
    timestamp: str
    title: str
    details: tuple[str, ...]
    outputs: tuple[tuple[str, str], ...]


@dataclass(frozen=True)
class ParsedLog:
    agent: str
    log_path: Path
    started_utc: str
    run_id: str
    status: str
    ended_utc: str
    summary: str
    kv: dict[str, str]
    steps: tuple[ParsedStep, ...]
    declared_outputs: tuple[tuple[str, str], ...]
    commands: tuple[str, ...]

    @property
    def run_key(self) -> str:
        """
        Relevance: Operates within the orchestration and observability layer.
        Concept: Primary callable implementing a stage-level behavior.
        Contribution: Contributes a deterministic transformation that supports end-to-end reasoning reproducibility.
        """

        if self.run_id:
            return self.run_id
        return f"log:{self.log_path.stem}"


def _to_iso_or_empty(text: str) -> str:
    """
    Relevance: Operates within the orchestration and observability layer.
    Concept: Internal helper implementing one deterministic step of this stage.
    Contribution: Contributes a deterministic transformation that supports end-to-end reasoning reproducibility.
    """

    value = (text or "").strip()
    if not value:
        return ""
    try:
        parsed = dt.datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return ""
    return parsed.isoformat()


def _safe_time_key(value: str) -> str:
    """
    Relevance: Operates within the orchestration and observability layer.
    Concept: Defensive conversion/parsing to keep scoring and reporting robust.
    Contribution: Reduces runtime ambiguity and prevents malformed artifacts from destabilizing the workflow.
    """

    if not value:
        return "9999-12-31T23:59:59+00:00"
    return value


def _sanitize_id(raw: str) -> str:
    """
    Relevance: Operates within the orchestration and observability layer.
    Concept: Internal helper implementing one deterministic step of this stage.
    Contribution: Contributes a deterministic transformation that supports end-to-end reasoning reproducibility.
    """

    clean = re.sub(r"[^A-Za-z0-9._:-]+", "-", raw.strip())
    return clean.strip("-") or "unknown"


def _resolve_candidate_path(raw: str, repo_root: Path) -> Path:
    """
    Relevance: Operates within the orchestration and observability layer.
    Concept: Internal helper implementing one deterministic step of this stage.
    Contribution: Contributes a deterministic transformation that supports end-to-end reasoning reproducibility.
    """

    p = Path(raw.strip())
    if not p.is_absolute():
        p = repo_root / p
    return p.resolve()


def _is_under(path: Path, root: Path) -> bool:
    """
    Relevance: Operates within the orchestration and observability layer.
    Concept: Internal helper implementing one deterministic step of this stage.
    Contribution: Contributes a deterministic transformation that supports end-to-end reasoning reproducibility.
    """

    try:
        path.resolve().relative_to(root.resolve())
        return True
    except ValueError:
        return False


def _parse_log(path: Path) -> ParsedLog:
    """
    Relevance: Operates within the orchestration and observability layer.
    Concept: Internal helper implementing one deterministic step of this stage.
    Contribution: Contributes a deterministic transformation that supports end-to-end reasoning reproducibility.
    """

    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()

    agent_match = HEADER_AGENT_RE.search(text)
    agent = agent_match.group(1).strip() if agent_match else path.parent.name

    fields: dict[str, str] = {}
    for key, pattern in FIELD_RE.items():
        m = pattern.search(text)
        fields[key] = m.group(1).strip() if m else ""

    steps: list[ParsedStep] = []
    commands: list[str] = []
    declared_outputs: list[tuple[str, str]] = []
    kv: dict[str, str] = {}

    i = 0
    while i < len(lines):
        line = lines[i]
        m_step = STEP_HEADER_RE.match(line)
        if m_step:
            step_ts = _to_iso_or_empty(m_step.group(1).strip()) or m_step.group(1).strip()
            i += 1
            title = ""
            details: list[str] = []
            outputs: list[tuple[str, str]] = []
            while i < len(lines) and not lines[i].startswith("## "):
                item = lines[i].strip()
                if item.startswith("- "):
                    payload = item[2:].strip()
                    if not title:
                        title = payload
                    else:
                        details.append(payload)
                        m_out = INLINE_OUTPUT_RE.match(payload)
                        if m_out:
                            outputs.append((m_out.group(1).strip(), m_out.group(2).strip()))
                        if "=" in payload:
                            key, value = payload.split("=", 1)
                            key_s = key.strip()
                            if key_s:
                                kv[key_s] = value.strip()
                        if payload.startswith("command="):
                            commands.append(payload.split("=", 1)[1].strip())
                i += 1
            steps.append(
                ParsedStep(
                    timestamp=step_ts,
                    title=title or "(untitled-step)",
                    details=tuple(details),
                    outputs=tuple(outputs),
                )
            )
            continue

        if line.strip() == "## Declared Outputs":
            i += 1
            while i < len(lines) and not lines[i].startswith("## "):
                row = lines[i].strip()
                m_decl = DECLARED_OUTPUT_RE.match(row)
                if m_decl:
                    label = m_decl.group(1).strip()
                    value = m_decl.group(2).strip()
                    declared_outputs.append((label, value))
                i += 1
            continue

        i += 1

    return ParsedLog(
        agent=agent,
        log_path=path.resolve(),
        started_utc=_to_iso_or_empty(fields.get("started_utc", "")),
        run_id=fields.get("run_id", "").strip() or path.stem,
        status=fields.get("status", "").strip().lower(),
        ended_utc=_to_iso_or_empty(fields.get("ended_utc", "")),
        summary=fields.get("summary", "").strip(),
        kv=kv,
        steps=tuple(steps),
        declared_outputs=tuple(declared_outputs),
        commands=tuple(commands),
    )


def _infer_agent_from_command(command: str) -> str:
    """
    Relevance: Operates within the orchestration and observability layer.
    Concept: Internal helper implementing one deterministic step of this stage.
    Contribution: Contributes a deterministic transformation that supports end-to-end reasoning reproducibility.
    """

    m = SKILL_SCRIPT_RE.search(command)
    if not m:
        return ""
    skill_dir = m.group(1).strip()
    script_name = m.group(2).strip()
    if skill_dir == "kb-orchestrator":
        if script_name == "export_phyp_docs.py":
            return "phyp-doc-exporter"
        if script_name == "generate_interpretation_reports.py":
            return "kb-interpretation-reporter"
        if script_name == "generate_reasoning_log_index.py":
            return "kb-log-indexer"
        if script_name == "generate_process_graph.py":
            return "kb-process-graph-visualizer"
        if script_name == "generate_reasoning_dynamics.py":
            return "kb-reasoning-dynamics"
        return "kb-orchestrator"
    return skill_dir


def _iter_command_paths(command: str, repo_root: Path) -> list[Path]:
    """
    Relevance: Operates within the orchestration and observability layer.
    Concept: Internal helper implementing one deterministic step of this stage.
    Contribution: Contributes a deterministic transformation that supports end-to-end reasoning reproducibility.
    """

    paths: list[Path] = []
    try:
        tokens = shlex.split(command)
    except ValueError:
        tokens = command.split()
    for token in tokens:
        t = token.strip()
        if not t:
            continue
        if "/" not in t and "\\" not in t and not t.startswith("artifacts"):
            continue
        try:
            p = _resolve_candidate_path(t, repo_root)
        except Exception:
            continue
        paths.append(p)
    return paths


def _matches_filters(
    log: ParsedLog,
    repo_root: Path,
    artifacts_dir: Path,
    kb_filter: str,
    kb_ref_filter: str,
    run_id_filter: str,
    include_agents: set[str],
    exclude_agents: set[str],
) -> bool:
    """
    Relevance: Operates within the orchestration and observability layer.
    Concept: Internal helper implementing one deterministic step of this stage.
    Contribution: Contributes a deterministic transformation that supports end-to-end reasoning reproducibility.
    """

    if run_id_filter and log.run_id != run_id_filter:
        return False

    if exclude_agents and log.agent in exclude_agents:
        return False

    if include_agents and log.agent not in include_agents:
        return False

    if kb_filter:
        kb_value = log.kv.get("kb", "").strip()
        if kb_value != kb_filter:
            kb_abs = _resolve_candidate_path(kb_value, repo_root) if kb_value else None
            kb_abs_filter = _resolve_candidate_path(kb_filter, repo_root)
            if not kb_abs or kb_abs != kb_abs_filter:
                return False
    if kb_ref_filter:
        log_kb_ref = normalize_kb_ref(log.kv.get("kb_ref", "").strip())
        if not log_kb_ref:
            kb_value = log.kv.get("kb", "").strip()
            if kb_value:
                log_kb_ref = kb_ref_from_kb_filename(Path(kb_value))
        if log_kb_ref and log_kb_ref != kb_ref_filter:
            return False

    artifacts_match = False
    artifacts_kv = log.kv.get("artifacts_dir", "").strip()
    if artifacts_kv:
        try:
            artifacts_match = _resolve_candidate_path(artifacts_kv, repo_root) == artifacts_dir.resolve()
        except Exception:
            artifacts_match = False

    if not artifacts_match:
        for _, out in list(log.declared_outputs) + [o for s in log.steps for o in s.outputs]:
            try:
                if _is_under(_resolve_candidate_path(out, repo_root), artifacts_dir):
                    artifacts_match = True
                    break
            except Exception:
                continue

    if not artifacts_match:
        for command in log.commands:
            for candidate in _iter_command_paths(command, repo_root):
                if _is_under(candidate, artifacts_dir):
                    artifacts_match = True
                    break
            if artifacts_match:
                break

    return artifacts_match


def _load_logs(
    log_root: Path,
    repo_root: Path,
    artifacts_dir: Path,
    kb_filter: str = "",
    kb_ref_filter: str = "",
    run_id_filter: str = "",
    include_agents: set[str] | None = None,
    exclude_agents: set[str] | None = None,
    exclude_log_paths: set[str] | None = None,
) -> list[ParsedLog]:
    """
    Relevance: Operates within the orchestration and observability layer.
    Concept: Loading and structuring external artifacts for deterministic processing.
    Contribution: Provides clean, typed inputs so downstream reasoning steps remain auditable.
    """

    out: list[ParsedLog] = []
    if not log_root.exists():
        return out
    included = include_agents or set()
    excluded_agents = exclude_agents or set()
    excluded = {str(Path(p).resolve()) for p in (exclude_log_paths or set())}
    for path in sorted(log_root.glob("*/*.md")):
        if not path.is_file():
            continue
        if str(path.resolve()) in excluded:
            continue
        try:
            parsed = _parse_log(path)
        except Exception:
            continue
        if _matches_filters(
            parsed,
            repo_root=repo_root,
            artifacts_dir=artifacts_dir,
            kb_filter=kb_filter,
            kb_ref_filter=kb_ref_filter,
            run_id_filter=run_id_filter,
            include_agents=included,
            exclude_agents=excluded_agents,
        ):
            out.append(parsed)
    out.sort(key=lambda x: (_safe_time_key(x.started_utc), str(x.log_path)))
    return out


def _is_end_to_end_orchestrator_log(log: ParsedLog) -> bool:
    """
    Relevance: Operates within the orchestration and observability layer.
    Concept: Internal helper implementing one deterministic step of this stage.
    Contribution: Contributes a deterministic transformation that supports end-to-end reasoning reproducibility.
    """

    if log.agent != "kb-orchestrator":
        return False
    if (log.status or "").strip().lower() != "success":
        return False
    intent = str(log.kv.get("intent", "")).strip().lower()
    if intent in {"pipeline", "abductive-loop"}:
        return True
    summary = (log.summary or "").strip().lower()
    return "intent `pipeline` completed." in summary or "intent `abductive-loop` completed." in summary


def _default_run_id_for_process_view(logs: list[ParsedLog]) -> tuple[str, str]:
    """
    Relevance: Operates within the orchestration and observability layer.
    Concept: Selection/retrieval of the most relevant candidates for reasoning.
    Contribution: Provides clean, typed inputs so downstream reasoning steps remain auditable.
    """

    run_groups: dict[str, list[ParsedLog]] = {}
    for log in logs:
        run_id = (log.run_id or "").strip()
        if not run_id:
            continue
        run_groups.setdefault(run_id, []).append(log)
    if not run_groups:
        return "", "no-run-id"

    def run_time_key(items: list[ParsedLog]) -> str:
        """
        Relevance: Local helper for choosing the default process-visualization run.
        Concept: Temporal ordering of candidate runs using their last observed event time.
        Contribution: Makes default run selection deterministic, which prevents mixed-run timelines in process evolution views.
        """
        # Use last known event timestamp for a run; ISO strings preserve order.
        return max((_safe_time_key(x.ended_utc or x.started_utc) for x in items), default=_safe_time_key(""))

    orchestrator_run_ids = [
        run_id for run_id, run_logs in run_groups.items() if any(item.agent == "kb-orchestrator" for item in run_logs)
    ]
    if orchestrator_run_ids:
        e2e_run_ids = [
            run_id
            for run_id in orchestrator_run_ids
            if any(_is_end_to_end_orchestrator_log(item) for item in run_groups[run_id])
        ]
        if e2e_run_ids:
            selected = max(e2e_run_ids, key=lambda rid: run_time_key(run_groups[rid]))
            return selected, "latest-end-to-end"
        selected = max(orchestrator_run_ids, key=lambda rid: run_time_key(run_groups[rid]))
        return selected, "latest-orchestrator-run"

    selected = max(run_groups.keys(), key=lambda rid: run_time_key(run_groups[rid]))
    return selected, "latest-run"


def _make_node(node_id: str, label: str, node_type: str, meta: dict[str, Any] | None = None) -> dict[str, Any]:
    """
    Relevance: Operates within the orchestration and observability layer.
    Concept: Internal helper implementing one deterministic step of this stage.
    Contribution: Contributes a deterministic transformation that supports end-to-end reasoning reproducibility.
    """

    return {
        "id": node_id,
        "label": label,
        "node_type": node_type,
        "meta": meta or {},
    }


def _make_edge(
    edge_id: str,
    source: str,
    target: str,
    edge_type: str,
    label: str,
    meta: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """
    Relevance: Operates within the orchestration and observability layer.
    Concept: Internal helper implementing one deterministic step of this stage.
    Contribution: Contributes a deterministic transformation that supports end-to-end reasoning reproducibility.
    """

    return {
        "id": edge_id,
        "source": source,
        "target": target,
        "edge_type": edge_type,
        "label": label,
        "meta": meta or {},
    }


def _edge_id(source: str, target: str, edge_type: str, label: str = "") -> str:
    """
    Relevance: Operates within the orchestration and observability layer.
    Concept: Internal helper implementing one deterministic step of this stage.
    Contribution: Contributes a deterministic transformation that supports end-to-end reasoning reproducibility.
    """

    core = f"{source}|{target}|{edge_type}|{label}".strip()
    return _sanitize_id(core)


def _stage_from_title(title: str) -> tuple[str, str]:
    """
    Relevance: Operates within the orchestration and observability layer.
    Concept: Internal helper implementing one deterministic step of this stage.
    Contribution: Contributes a deterministic transformation that supports end-to-end reasoning reproducibility.
    """

    m_start = RUN_STAGE_RE.match(title)
    if m_start:
        return ("stage_started", m_start.group(1).strip())
    m_done = DONE_STAGE_RE.match(title)
    if m_done:
        return ("stage_completed", m_done.group(1).strip())
    return ("step", "")


def _build_graph(logs: list[ParsedLog], repo_root: Path) -> dict[str, Any]:
    """
    Relevance: Operates within the orchestration and observability layer.
    Concept: Construction of derived graph/model structures used by later stages.
    Contribution: Creates the structural substrate that enables cross-stage scoring and interpretation.
    """

    nodes: dict[str, dict[str, Any]] = {}
    edges: dict[str, dict[str, Any]] = {}
    states: list[dict[str, Any]] = []
    run_last_step: dict[str, str] = {}

    def ensure_node(node_id: str, label: str, node_type: str, meta: dict[str, Any] | None = None) -> tuple[dict[str, Any], bool]:
        """
        Relevance: Operates within the orchestration and observability layer.
        Concept: Primary callable implementing a stage-level behavior.
        Contribution: Contributes a deterministic transformation that supports end-to-end reasoning reproducibility.
        """

        if node_id in nodes:
            if meta:
                nodes[node_id]["meta"].update(meta)
            return nodes[node_id], False
        node = _make_node(node_id, label, node_type, meta)
        nodes[node_id] = node
        return node, True

    def ensure_edge(
        source: str,
        target: str,
        edge_type: str,
        label: str = "",
        meta: dict[str, Any] | None = None,
    ) -> tuple[dict[str, Any], bool]:
        """
        Relevance: Operates within the orchestration and observability layer.
        Concept: Primary callable implementing a stage-level behavior.
        Contribution: Contributes a deterministic transformation that supports end-to-end reasoning reproducibility.
        """

        eid = _edge_id(source, target, edge_type, label)
        if eid in edges:
            if meta:
                edges[eid]["meta"].update(meta)
            return edges[eid], False
        edge = _make_edge(eid, source, target, edge_type, label, meta)
        edges[eid] = edge
        return edge, True

    def add_state(
        timestamp: str,
        run_key: str,
        event_type: str,
        description: str,
        added_nodes: list[dict[str, Any]],
        added_edges: list[dict[str, Any]],
    ) -> None:
        """
        Relevance: Operates within the orchestration and observability layer.
        Concept: Primary callable implementing a stage-level behavior.
        Contribution: Contributes a deterministic transformation that supports end-to-end reasoning reproducibility.
        """

        states.append(
            {
                "index": len(states),
                "timestamp": timestamp,
                "run_key": run_key,
                "event_type": event_type,
                "description": description,
                "added_node_ids": [n["id"] for n in added_nodes],
                "added_edge_ids": [e["id"] for e in added_edges],
                "node_ids": sorted(nodes.keys()),
                "edge_ids": sorted(edges.keys()),
            }
        )

    for log in logs:
        run_key = _sanitize_id(log.run_key)
        run_node_id = f"run:{run_key}"
        agent_node_id = f"agent:{_sanitize_id(log.agent)}"

        added_nodes: list[dict[str, Any]] = []
        added_edges: list[dict[str, Any]] = []

        n_run, add_run = ensure_node(
            run_node_id,
            label=log.run_key,
            node_type="run",
            meta={
                "run_id": log.run_id,
                "status": log.status or "unknown",
                "started_utc": log.started_utc,
                "ended_utc": log.ended_utc,
                "summary": log.summary,
            },
        )
        if add_run:
            added_nodes.append(n_run)

        n_agent, add_agent = ensure_node(agent_node_id, label=log.agent, node_type="agent")
        if add_agent:
            added_nodes.append(n_agent)

        e_exec, add_exec = ensure_edge(
            run_node_id,
            agent_node_id,
            edge_type="executed_by",
            label=log.agent,
            meta={"log_path": str(log.log_path)},
        )
        if add_exec:
            added_edges.append(e_exec)

        add_state(
            timestamp=log.started_utc,
            run_key=log.run_key,
            event_type="log_started",
            description=f"{log.agent} started log {log.log_path.name}",
            added_nodes=added_nodes,
            added_edges=added_edges,
        )

        active_stage_by_name: dict[str, str] = {}
        for idx, step in enumerate(log.steps, start=1):
            step_node_id = f"step:{run_key}:{idx}"
            added_nodes = []
            added_edges = []
            n_step, add_step = ensure_node(
                step_node_id,
                label=step.title,
                node_type="step",
                meta={"timestamp": step.timestamp, "index": idx, "agent": log.agent},
            )
            if add_step:
                added_nodes.append(n_step)

            e_has_step, add_has_step = ensure_edge(
                run_node_id,
                step_node_id,
                edge_type="has_step",
                label=f"step-{idx}",
            )
            if add_has_step:
                added_edges.append(e_has_step)

            prev = run_last_step.get(run_key)
            if prev and prev != step_node_id:
                e_seq, add_seq = ensure_edge(prev, step_node_id, edge_type="precedes_step")
                if add_seq:
                    added_edges.append(e_seq)
            run_last_step[run_key] = step_node_id

            stage_event_type, stage_name = _stage_from_title(step.title)
            current_stage_id = ""
            if stage_name:
                current_stage_id = f"stage:{run_key}:{_sanitize_id(stage_name)}"
                n_stage, add_stage = ensure_node(
                    current_stage_id,
                    label=stage_name,
                    node_type="stage",
                    meta={"run_key": log.run_key},
                )
                if add_stage:
                    added_nodes.append(n_stage)
                e_stage, add_stage_edge = ensure_edge(
                    step_node_id,
                    current_stage_id,
                    edge_type=stage_event_type,
                    label=stage_name,
                )
                if add_stage_edge:
                    added_edges.append(e_stage)
                active_stage_by_name[stage_name] = current_stage_id

                if stage_event_type == "stage_started":
                    for item in step.details:
                        if item.startswith("command="):
                            command = item.split("=", 1)[1].strip()
                            child_agent = _infer_agent_from_command(command)
                            if child_agent:
                                child_node_id = f"agent:{_sanitize_id(child_agent)}"
                                n_child, add_child = ensure_node(child_node_id, child_agent, "agent")
                                if add_child:
                                    added_nodes.append(n_child)
                                e_invoke, add_invoke = ensure_edge(
                                    current_stage_id,
                                    child_node_id,
                                    edge_type="invokes_agent",
                                    label=child_agent,
                                    meta={"command": command},
                                )
                                if add_invoke:
                                    added_edges.append(e_invoke)

            output_source = step_node_id
            if stage_name and stage_name in active_stage_by_name:
                output_source = active_stage_by_name[stage_name]

            for label, out_path in step.outputs:
                out_abs = _resolve_candidate_path(out_path, repo_root)
                artifact_id = f"artifact:{_sanitize_id(str(out_abs))}"
                n_art, add_art = ensure_node(
                    artifact_id,
                    label=out_abs.name,
                    node_type="artifact",
                    meta={"path": str(out_abs)},
                )
                if add_art:
                    added_nodes.append(n_art)
                edge_type = "emits_output"
                if "reasoning_log" in label or "/artifacts/reasoning-logs/" in str(out_abs):
                    edge_type = "emits_reasoning_log"
                e_out, add_out = ensure_edge(
                    output_source,
                    artifact_id,
                    edge_type=edge_type,
                    label=label,
                    meta={"path": str(out_abs)},
                )
                if add_out:
                    added_edges.append(e_out)
                if edge_type == "emits_reasoning_log":
                    log_agent = out_abs.parent.name
                    if log_agent:
                        log_agent_id = f"agent:{_sanitize_id(log_agent)}"
                        n_log_agent, add_log_agent = ensure_node(log_agent_id, log_agent, "agent")
                        if add_log_agent:
                            added_nodes.append(n_log_agent)
                        e_log_of, add_log_of = ensure_edge(
                            artifact_id,
                            log_agent_id,
                            edge_type="log_of_agent",
                            label=log_agent,
                        )
                        if add_log_of:
                            added_edges.append(e_log_of)
                        # Prefer child-agent inference from emitted reasoning-log path.
                        # This is more robust than command-path regex matching.
                        if output_source.startswith("stage:"):
                            e_invoke_log, add_invoke_log = ensure_edge(
                                output_source,
                                log_agent_id,
                                edge_type="invokes_agent",
                                label=log_agent,
                                meta={"inferred_from": "reasoning_log_path", "path": str(out_abs)},
                            )
                            if add_invoke_log:
                                added_edges.append(e_invoke_log)

            add_state(
                timestamp=step.timestamp or log.started_utc,
                run_key=log.run_key,
                event_type=stage_event_type if stage_name else "step",
                description=step.title,
                added_nodes=added_nodes,
                added_edges=added_edges,
            )

        for label, out_path in log.declared_outputs:
            added_nodes = []
            added_edges = []
            out_abs = _resolve_candidate_path(out_path, repo_root)
            artifact_id = f"artifact:{_sanitize_id(str(out_abs))}"
            n_art, add_art = ensure_node(
                artifact_id,
                label=out_abs.name,
                node_type="artifact",
                meta={"path": str(out_abs)},
            )
            if add_art:
                added_nodes.append(n_art)
            e_decl, add_decl = ensure_edge(
                run_node_id,
                artifact_id,
                edge_type="declares_output",
                label=label,
            )
            if add_decl:
                added_edges.append(e_decl)
            add_state(
                timestamp=log.ended_utc or log.started_utc,
                run_key=log.run_key,
                event_type="declared_output",
                description=f"Declared output: {label}",
                added_nodes=added_nodes,
                added_edges=added_edges,
            )

    states.sort(key=lambda x: (_safe_time_key(x.get("timestamp", "")), x.get("index", 0)))
    for idx, st in enumerate(states):
        st["index"] = idx

    edge_type_counts: dict[str, int] = {}
    for edge in edges.values():
        et = str(edge.get("edge_type", "unknown"))
        edge_type_counts[et] = edge_type_counts.get(et, 0) + 1

    return {
        "nodes": sorted(nodes.values(), key=lambda x: x["id"]),
        "edges": sorted(edges.values(), key=lambda x: x["id"]),
        "states": states,
        "edge_type_counts": edge_type_counts,
    }


def _render_html(report: dict[str, Any]) -> str:
    """
    Relevance: Operates within the orchestration and observability layer.
    Concept: Rendering internal outputs into human-readable artifacts.
    Contribution: Improves interpretability by exposing machine results in analyst-friendly form.
    """

    payload = json.dumps(report, ensure_ascii=False)
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Reasoning Process Graph</title>
  <style>
    :root {{
      --bg: #f4f7fb;
      --panel: #ffffff;
      --text: #102132;
      --muted: #5d7387;
      --line: #d7e1ea;
      --run: #264653;
      --agent: #e76f51;
      --stage: #2a9d8f;
      --step: #577590;
      --artifact: #457b9d;
    }}
    body {{
      margin: 0;
      font-family: "IBM Plex Sans", "Segoe UI", sans-serif;
      background: radial-gradient(circle at 12% 16%, #e8f0fa 0%, #f4f7fb 42%, #edf3f9 100%);
      color: var(--text);
    }}
    .wrap {{
      max-width: 1440px;
      margin: 0 auto;
      padding: 18px;
      display: grid;
      grid-template-columns: 1fr 360px;
      gap: 16px;
    }}
    .panel {{
      background: var(--panel);
      border: 1px solid var(--line);
      border-radius: 12px;
      box-shadow: 0 10px 24px rgba(16, 33, 50, 0.08);
      overflow: hidden;
    }}
    .toolbar {{
      padding: 12px 14px;
      border-bottom: 1px solid var(--line);
      display: flex;
      flex-wrap: wrap;
      gap: 10px;
      align-items: center;
    }}
    .toolbar button {{
      border: 1px solid #c6d2df;
      background: #fff;
      color: #12253a;
      border-radius: 8px;
      padding: 7px 10px;
      cursor: pointer;
    }}
    .toolbar button:hover {{ background: #f3f7fc; }}
    .toolbar input[type="range"] {{ width: 320px; }}
    .meta {{
      margin-left: auto;
      color: var(--muted);
      font-size: 12px;
    }}
    canvas {{ display: block; width: 100%; height: 820px; background: linear-gradient(180deg, #fbfdff 0%, #f7fbff 100%); }}
    .side {{
      padding: 14px;
      font-size: 13px;
      line-height: 1.35;
    }}
    .side h3 {{
      margin: 0 0 10px;
      font-size: 14px;
      letter-spacing: 0.02em;
      text-transform: uppercase;
      color: #35506a;
    }}
    .kv {{ margin: 6px 0; }}
    .kv span {{ color: var(--muted); display: inline-block; min-width: 96px; }}
    .legend-item {{
      display: flex; align-items: center; gap: 8px; margin: 6px 0;
    }}
    .chip {{
      width: 12px; height: 12px; border-radius: 3px; display: inline-block;
    }}
    .edge-legend {{
      max-height: 300px;
      overflow: auto;
      border: 1px solid var(--line);
      border-radius: 8px;
      padding: 8px;
      background: #fbfdff;
    }}
    .note {{
      color: var(--muted);
      font-size: 12px;
      margin-top: 10px;
    }}
  </style>
</head>
<body>
  <div class="wrap">
    <div class="panel">
      <div class="toolbar">
        <button id="prevBtn">Prev</button>
        <button id="playBtn">Play</button>
        <button id="nextBtn">Next</button>
        <label>State <input id="stateRange" type="range" min="0" max="0" value="0"/></label>
        <label><input id="edgeLabels" type="checkbox" checked /> Edge labels</label>
        <div class="meta" id="metaText"></div>
      </div>
      <canvas id="graphCanvas" width="1100" height="820"></canvas>
    </div>
    <div class="panel side">
      <h3>Current State</h3>
      <div class="kv"><span>Index</span><strong id="stateIndex">0</strong></div>
      <div class="kv"><span>Timestamp</span><strong id="stateTs">-</strong></div>
      <div class="kv"><span>Run</span><strong id="stateRun">-</strong></div>
      <div class="kv"><span>Event</span><strong id="stateType">-</strong></div>
      <div class="kv"><span>Description</span><strong id="stateDesc">-</strong></div>
      <div class="kv"><span>Nodes</span><strong id="stateNodes">0</strong></div>
      <div class="kv"><span>Edges</span><strong id="stateEdges">0</strong></div>
      <h3 style="margin-top:16px;">Node Types</h3>
      <div class="legend-item"><span class="chip" style="background:var(--run)"></span>run</div>
      <div class="legend-item"><span class="chip" style="background:var(--agent)"></span>agent</div>
      <div class="legend-item"><span class="chip" style="background:var(--stage)"></span>stage</div>
      <div class="legend-item"><span class="chip" style="background:var(--step)"></span>step</div>
      <div class="legend-item"><span class="chip" style="background:var(--artifact)"></span>artifact</div>
      <h3 style="margin-top:16px;">Typed Edges</h3>
      <div class="edge-legend" id="edgeLegend"></div>
      <div class="note">The slider replays cumulative intermediary states of the reasoning process.</div>
    </div>
  </div>
  <script>
    const DATA = {payload};
    const TYPE_COLOR = {{
      run: "#264653",
      agent: "#e76f51",
      stage: "#2a9d8f",
      step: "#577590",
      artifact: "#457b9d",
      unknown: "#7f8fa1"
    }};
    const EDGE_COLOR = {{
      executed_by: "#203040",
      has_step: "#4d6f8f",
      precedes_step: "#8da0b3",
      stage_started: "#1b9e77",
      stage_completed: "#66a61e",
      step: "#5b7ea0",
      invokes_agent: "#d95f02",
      emits_output: "#1f78b4",
      emits_reasoning_log: "#6a4c93",
      log_of_agent: "#b15928",
      declares_output: "#0b7285"
    }};
    const NODE_MAP = new Map(DATA.final_graph.nodes.map(n => [n.id, n]));
    const EDGE_MAP = new Map(DATA.final_graph.edges.map(e => [e.id, e]));

    const canvas = document.getElementById("graphCanvas");
    const ctx = canvas.getContext("2d");
    const stateRange = document.getElementById("stateRange");
    const playBtn = document.getElementById("playBtn");
    const prevBtn = document.getElementById("prevBtn");
    const nextBtn = document.getElementById("nextBtn");
    const edgeLabels = document.getElementById("edgeLabels");
    const stateIndexEl = document.getElementById("stateIndex");
    const stateTsEl = document.getElementById("stateTs");
    const stateRunEl = document.getElementById("stateRun");
    const stateTypeEl = document.getElementById("stateType");
    const stateDescEl = document.getElementById("stateDesc");
    const stateNodesEl = document.getElementById("stateNodes");
    const stateEdgesEl = document.getElementById("stateEdges");
    const metaText = document.getElementById("metaText");
    const edgeLegend = document.getElementById("edgeLegend");

    const states = DATA.states || [];
    stateRange.max = Math.max(0, states.length - 1);
    stateRange.value = String(Math.max(0, states.length - 1));

    const edgeTypes = Object.entries(DATA.edge_type_counts || {{}}).sort((a, b) => b[1] - a[1]);
    edgeLegend.innerHTML = edgeTypes.map(([k, v]) =>
      `<div class="legend-item"><span class="chip" style="background:${{EDGE_COLOR[k] || '#94a3b8'}}"></span>${{k}} (${{v}})</div>`
    ).join("") || "<div class='note'>No edge types found.</div>";

    function buildLayout() {{
      const nodes = DATA.final_graph.nodes || [];
      const buckets = {{ run: [], stage: [], step: [], agent: [], artifact: [], unknown: [] }};
      for (const n of nodes) {{
        const t = n.node_type || "unknown";
        (buckets[t] || buckets.unknown).push(n);
      }}
      const xByType = {{ run: 120, stage: 340, step: 560, agent: 780, artifact: 1000, unknown: 920 }};
      const pos = new Map();
      for (const [t, arr] of Object.entries(buckets)) {{
        const count = Math.max(1, arr.length);
        const spacing = (canvas.height - 80) / count;
        arr.sort((a, b) => a.label.localeCompare(b.label));
        arr.forEach((n, idx) => {{
          const y = 40 + spacing * (idx + 0.5);
          pos.set(n.id, {{ x: xByType[t] || xByType.unknown, y }});
        }});
      }}
      return pos;
    }}

    const LAYOUT = buildLayout();

    function draw(stateIndex) {{
      const s = states[stateIndex];
      if (!s) return;
      const nodeIds = new Set(s.node_ids || []);
      const edgeIds = new Set(s.edge_ids || []);
      ctx.clearRect(0, 0, canvas.width, canvas.height);

      for (const eid of edgeIds) {{
        const e = EDGE_MAP.get(eid);
        if (!e) continue;
        if (!nodeIds.has(e.source) || !nodeIds.has(e.target)) continue;
        const a = LAYOUT.get(e.source);
        const b = LAYOUT.get(e.target);
        if (!a || !b) continue;
        const color = EDGE_COLOR[e.edge_type] || "#9aa7b4";
        ctx.strokeStyle = color;
        ctx.lineWidth = 1.4;
        ctx.beginPath();
        ctx.moveTo(a.x, a.y);
        ctx.lineTo(b.x, b.y);
        ctx.stroke();
        const ang = Math.atan2(b.y - a.y, b.x - a.x);
        const arrow = 7;
        ctx.beginPath();
        ctx.moveTo(b.x, b.y);
        ctx.lineTo(b.x - arrow * Math.cos(ang - 0.32), b.y - arrow * Math.sin(ang - 0.32));
        ctx.lineTo(b.x - arrow * Math.cos(ang + 0.32), b.y - arrow * Math.sin(ang + 0.32));
        ctx.closePath();
        ctx.fillStyle = color;
        ctx.fill();
        if (edgeLabels.checked) {{
          const mx = (a.x + b.x) / 2;
          const my = (a.y + b.y) / 2;
          ctx.fillStyle = "#3c4f63";
          ctx.font = "11px IBM Plex Sans, Segoe UI, sans-serif";
          const txt = e.edge_type;
          ctx.fillText(txt, mx + 4, my - 3);
        }}
      }}

      for (const nid of nodeIds) {{
        const n = NODE_MAP.get(nid);
        if (!n) continue;
        const p = LAYOUT.get(nid);
        if (!p) continue;
        const color = TYPE_COLOR[n.node_type] || TYPE_COLOR.unknown;
        ctx.fillStyle = color;
        ctx.beginPath();
        ctx.arc(p.x, p.y, 8, 0, Math.PI * 2);
        ctx.fill();
        ctx.fillStyle = "#102132";
        ctx.font = "11px IBM Plex Sans, Segoe UI, sans-serif";
        ctx.fillText(n.label || nid, p.x + 11, p.y + 4);
      }}

      stateIndexEl.textContent = String(s.index);
      stateTsEl.textContent = s.timestamp || "-";
      stateRunEl.textContent = s.run_key || "-";
      stateTypeEl.textContent = s.event_type || "-";
      stateDescEl.textContent = s.description || "-";
      stateNodesEl.textContent = String((s.node_ids || []).length);
      stateEdgesEl.textContent = String((s.edge_ids || []).length);
      metaText.textContent = `States: ${{states.length}} | Nodes: ${{DATA.final_graph.nodes.length}} | Edges: ${{DATA.final_graph.edges.length}}`;
    }}

    let timer = null;
    function stop() {{
      if (timer) clearInterval(timer);
      timer = null;
      playBtn.textContent = "Play";
    }}
    function play() {{
      if (timer) {{
        stop();
        return;
      }}
      playBtn.textContent = "Pause";
      timer = setInterval(() => {{
        const next = Math.min(states.length - 1, Number(stateRange.value) + 1);
        stateRange.value = String(next);
        draw(next);
        if (next >= states.length - 1) stop();
      }}, 600);
    }}

    stateRange.addEventListener("input", () => draw(Number(stateRange.value)));
    edgeLabels.addEventListener("change", () => draw(Number(stateRange.value)));
    prevBtn.addEventListener("click", () => {{
      const v = Math.max(0, Number(stateRange.value) - 1);
      stateRange.value = String(v);
      draw(v);
    }});
    nextBtn.addEventListener("click", () => {{
      const v = Math.min(states.length - 1, Number(stateRange.value) + 1);
      stateRange.value = String(v);
      draw(v);
    }});
    playBtn.addEventListener("click", play);

    draw(Number(stateRange.value));
  </script>
</body>
</html>
"""


def main() -> int:
    """
    Relevance: Operates within the orchestration and observability layer.
    Concept: CLI entrypoint orchestration for this script.
    Contribution: Binds parsing, computation, and artifact emission into a reproducible script execution.
    """

    logger = ReasoningLogger("kb-process-graph-visualizer")
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--artifacts-dir", required=True, help="Target artifacts directory for the process.")
    ap.add_argument("--reasoning-log-root", default="artifacts/reasoning-logs")
    ap.add_argument("--kb", default="", help="Optional KB path filter.")
    ap.add_argument("--kb-ref", default="", help="Optional KB reference filter. Defaults to artifacts directory name.")
    ap.add_argument("--run-id", default="", help="Optional run ID filter.")
    ap.add_argument("--include-agent", action="append", default=[])
    ap.add_argument("--exclude-agent", action="append", default=["kb-process-graph-visualizer"])
    ap.add_argument("--exclude-log-path", action="append", default=[])
    ap.add_argument("--output-json", default="")
    ap.add_argument("--output-evolution-json", default="")
    ap.add_argument("--output-html", default="")
    ap.add_argument("--states-dir", default="")
    args = ap.parse_args()

    repo_root = Path(__file__).resolve().parents[4]
    artifacts_dir = _resolve_candidate_path(args.artifacts_dir, repo_root)
    log_root = _resolve_candidate_path(args.reasoning_log_root, repo_root)
    include_agents = {a.strip() for a in args.include_agent if a.strip()}
    exclude_agents = {a.strip() for a in args.exclude_agent if a.strip()}
    kb_ref_filter = normalize_kb_ref(args.kb_ref.strip()) or kb_ref_from_artifacts_dir(artifacts_dir)

    output_json = Path(args.output_json) if args.output_json else artifacts_dir / "process-graph.json"
    output_evolution_json = (
        Path(args.output_evolution_json)
        if args.output_evolution_json
        else artifacts_dir / "process-graph-evolution.json"
    )
    output_html = Path(args.output_html) if args.output_html else artifacts_dir / "process-graph.html"
    states_dir = Path(args.states_dir) if args.states_dir else artifacts_dir / "process-graph-states"

    logger.step(
        "Parsed process-graph arguments",
        "\n".join(
            [
                f"artifacts_dir={artifacts_dir}",
                f"reasoning_log_root={log_root}",
                f"kb={args.kb}",
                f"kb_ref={kb_ref_filter}",
                f"run_id={args.run_id}",
                f"include_agents={sorted(include_agents)}",
                f"exclude_agents={sorted(exclude_agents)}",
                f"exclude_log_paths={args.exclude_log_path}",
                f"output_json={output_json}",
                f"output_evolution_json={output_evolution_json}",
                f"output_html={output_html}",
                f"states_dir={states_dir}",
            ]
        ),
    )

    if not artifacts_dir.exists():
        log_path = logger.finalize("error", summary=f"Artifacts directory not found: {artifacts_dir}")
        print(f"[LOG] {log_path}", file=sys.stderr)
        raise SystemExit(f"[ERROR] Artifacts directory not found: {artifacts_dir}")

    excluded_paths = {str(logger.log_path.resolve())}
    excluded_paths.update(str(_resolve_candidate_path(p, repo_root)) for p in args.exclude_log_path)
    requested_run_id = args.run_id.strip()
    logs = _load_logs(
        log_root=log_root,
        repo_root=repo_root,
        artifacts_dir=artifacts_dir,
        kb_filter=args.kb.strip(),
        kb_ref_filter=kb_ref_filter,
        run_id_filter=requested_run_id,
        include_agents=include_agents,
        exclude_agents=exclude_agents,
        exclude_log_paths=excluded_paths,
    )
    selected_run_id = requested_run_id
    selection_mode = "explicit-run-id" if requested_run_id else "all-matching"
    if not requested_run_id and logs:
        selected_run_id, selection_mode = _default_run_id_for_process_view(logs)
        if selected_run_id:
            logs = [x for x in logs if x.run_id == selected_run_id]
    logger.step(
        "Selected run scope",
        "\n".join(
            [
                f"selection_mode={selection_mode}",
                f"selected_run_id={selected_run_id or '(none)'}",
                f"log_count_after_selection={len(logs)}",
            ]
        ),
    )
    logger.step("Loaded matching reasoning logs", f"log_count={len(logs)}")
    if not logs:
        log_path = logger.finalize("error", summary="No matching logs found for process-graph generation.")
        print(f"[LOG] {log_path}", file=sys.stderr)
        raise SystemExit("[ERROR] No matching logs found.")

    graph = _build_graph(logs, repo_root=repo_root)
    nodes = graph["nodes"]
    edges = graph["edges"]
    states = graph["states"]
    logger.step(
        "Built typed process graph",
        "\n".join(
            [
                f"nodes={len(nodes)}",
                f"edges={len(edges)}",
                f"states={len(states)}",
                f"edge_types={graph['edge_type_counts']}",
            ]
        ),
    )

    metadata = {
        "generated_utc": dt.datetime.now(dt.UTC).isoformat(),
        "artifacts_dir": str(artifacts_dir),
        "reasoning_log_root": str(log_root),
        "kb_filter": args.kb.strip(),
        "kb_ref_filter": kb_ref_filter,
        "run_id_filter": selected_run_id,
        "run_selection_mode": selection_mode,
        "include_agents": sorted(include_agents),
        "exclude_agents": sorted(exclude_agents),
        "log_count": len(logs),
        "logs": [str(l.log_path) for l in logs],
    }

    final_graph_report = {
        "metadata": metadata,
        "edge_type_counts": graph["edge_type_counts"],
        "nodes": nodes,
        "edges": edges,
    }
    evolution_report = {
        "metadata": metadata,
        "edge_type_counts": graph["edge_type_counts"],
        "states": states,
        "final_graph": {"nodes": nodes, "edges": edges},
    }

    output_json.parent.mkdir(parents=True, exist_ok=True)
    output_evolution_json.parent.mkdir(parents=True, exist_ok=True)
    output_html.parent.mkdir(parents=True, exist_ok=True)
    states_dir.mkdir(parents=True, exist_ok=True)
    for stale in states_dir.glob("state-*.json"):
        try:
            stale.unlink()
        except OSError:
            continue

    output_json.write_text(json.dumps(final_graph_report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    output_evolution_json.write_text(
        json.dumps(evolution_report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    output_html.write_text(_render_html(evolution_report), encoding="utf-8")

    node_map = {n["id"]: n for n in nodes}
    edge_map = {e["id"]: e for e in edges}
    for st in states:
        idx = int(st.get("index", 0))
        state_path = states_dir / f"state-{idx:04d}.json"
        state_payload = {
            "metadata": {
                "index": idx,
                "timestamp": st.get("timestamp", ""),
                "run_key": st.get("run_key", ""),
                "event_type": st.get("event_type", ""),
                "description": st.get("description", ""),
            },
            "delta": {
                "added_nodes": [node_map[nid] for nid in st.get("added_node_ids", []) if nid in node_map],
                "added_edges": [edge_map[eid] for eid in st.get("added_edge_ids", []) if eid in edge_map],
            },
            "graph": {
                "nodes": [node_map[nid] for nid in st.get("node_ids", []) if nid in node_map],
                "edges": [edge_map[eid] for eid in st.get("edge_ids", []) if eid in edge_map],
            },
        }
        state_path.write_text(json.dumps(state_payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    print(f"[OK] Wrote process graph JSON: {output_json}")
    print(f"[OK] Wrote process evolution JSON: {output_evolution_json}")
    print(f"[OK] Wrote process graph HTML: {output_html}")
    print(f"[OK] Wrote intermediary states: {states_dir} ({len(states)} files)")

    logger.add_output("process_graph_json", output_json)
    logger.add_output("process_graph_evolution_json", output_evolution_json)
    logger.add_output("process_graph_html", output_html)
    logger.add_output("process_graph_states_dir", states_dir)
    log_path = logger.finalize(
        "success",
        summary=f"Generated typed process graph with {len(nodes)} nodes, {len(edges)} edges, {len(states)} states.",
    )
    print(f"[LOG] {log_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
