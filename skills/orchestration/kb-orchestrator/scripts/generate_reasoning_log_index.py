#!/usr/bin/env python3
# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
# 
# SPDX-License-Identifier: MIT

"""Aggregate reasoning logs into a human-readable run index."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import sys
from pathlib import Path
from typing import Any

_COMMON_DIR = Path(__file__).resolve().parents[3] / "common"
if str(_COMMON_DIR) not in sys.path:
    sys.path.insert(0, str(_COMMON_DIR))

from kb_context import kb_ref_from_artifacts_dir
from kb_context import kb_ref_from_kb_filename
from kb_context import normalize_kb_ref
from reasoning_log import ReasoningLogger


HEADER_RE = re.compile(r"^# Reasoning Log:\s*(.+?)\s*$", re.MULTILINE)
FIELD_RE = {
    "started_utc": re.compile(r"^- Started \(UTC\):\s*(.+?)\s*$", re.MULTILINE),
    "run_id": re.compile(r"^- Run ID:\s*(.+?)\s*$", re.MULTILINE),
    "status": re.compile(r"^- Status:\s*(.+?)\s*$", re.MULTILINE),
    "ended_utc": re.compile(r"^- Ended \(UTC\):\s*(.+?)\s*$", re.MULTILINE),
    "duration_s": re.compile(r"^- Duration \(s\):\s*(.+?)\s*$", re.MULTILINE),
    "summary": re.compile(r"^- Summary:\s*(.+?)\s*$", re.MULTILINE),
}
STEP_RE = re.compile(r"^## Step @", re.MULTILINE)
RUN_STAGE_RE = re.compile(r"^- Running stage:\s*(.+?)\s*$")
DONE_STAGE_RE = re.compile(r"^- Completed stage:\s*(.+?)\s*$")


def _safe_float(value: Any, default: float = 0.0) -> float:
    """
    Relevance: Operates within the orchestration and observability layer.
    Concept: Defensive conversion/parsing to keep scoring and reporting robust.
    Contribution: Reduces runtime ambiguity and prevents malformed artifacts from destabilizing the workflow.
    """

    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def _extract_outputs(text: str) -> list[dict[str, str]]:
    """
    Relevance: Operates within the orchestration and observability layer.
    Concept: Extraction of structured signals from raw text or artifact payloads.
    Contribution: Provides clean, typed inputs so downstream reasoning steps remain auditable.
    """

    outputs: list[dict[str, str]] = []
    in_outputs = False
    for raw_line in text.splitlines():
        line = raw_line.rstrip("\n")
        if line.strip() == "## Declared Outputs":
            in_outputs = True
            continue
        if in_outputs and line.startswith("## "):
            break
        if not in_outputs:
            continue
        stripped = line.strip()
        if not stripped.startswith("- "):
            continue
        payload = stripped[2:]
        if ":" not in payload:
            continue
        label, path = payload.split(":", 1)
        label_s = label.strip()
        path_s = path.strip()
        if not label_s or not path_s:
            continue
        outputs.append({"label": label_s, "path": path_s})
    return outputs


def _extract_step_titles(text: str, limit: int = 8) -> list[str]:
    """
    Relevance: Operates within the orchestration and observability layer.
    Concept: Extraction of structured signals from raw text or artifact payloads.
    Contribution: Provides clean, typed inputs so downstream reasoning steps remain auditable.
    """

    titles: list[str] = []
    lines = text.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        if not line.startswith("## Step @"):
            i += 1
            continue
        j = i + 1
        while j < len(lines):
            candidate = lines[j].strip()
            if not candidate:
                j += 1
                continue
            if candidate.startswith("## "):
                break
            if candidate.startswith("- "):
                title = candidate[2:].strip()
                if title:
                    titles.append(title)
                break
            j += 1
        i = j + 1
        if len(titles) >= limit:
            break
    return titles


def _extract_kv_pairs(text: str) -> dict[str, str]:
    """
    Relevance: Operates within the orchestration and observability layer.
    Concept: Extraction of structured signals from raw text or artifact payloads.
    Contribution: Captures stage context fields (`kb`, `kb_ref`, `artifacts_dir`) for run isolation.
    """

    out: dict[str, str] = {}
    for raw in text.splitlines():
        line = raw.strip()
        if not line.startswith("- ") or "=" not in line:
            continue
        payload = line[2:].strip()
        key, value = payload.split("=", 1)
        key_s = key.strip()
        if not key_s:
            continue
        out[key_s] = value.strip()
    return out


def _normalize_stage_id(stage_name: str) -> str:
    """
    Relevance: Operates within the orchestration and observability layer.
    Concept: Typed classification used to guide scoring and prioritization.
    Contribution: Contributes a deterministic transformation that supports end-to-end reasoning reproducibility.
    """

    return re.sub(r"[^A-Za-z0-9._:-]+", "-", stage_name.strip()).strip("-")


def _extract_stage_counts(text: str) -> dict[str, dict[str, int]]:
    """
    Relevance: Operates within the orchestration and observability layer.
    Concept: Extraction of structured signals from raw text or artifact payloads.
    Contribution: Provides stage-level observability rather than agent-only coverage.
    """

    started: dict[str, int] = {}
    completed: dict[str, int] = {}
    for raw in text.splitlines():
        line = raw.strip()
        m_start = RUN_STAGE_RE.match(line)
        if m_start:
            stage = _normalize_stage_id(m_start.group(1))
            if stage:
                started[stage] = started.get(stage, 0) + 1
            continue
        m_done = DONE_STAGE_RE.match(line)
        if m_done:
            stage = _normalize_stage_id(m_done.group(1))
            if stage:
                completed[stage] = completed.get(stage, 0) + 1
    return {"started": started, "completed": completed}


def _parse_log(path: Path) -> dict[str, Any]:
    """
    Relevance: Operates within the orchestration and observability layer.
    Concept: Internal helper implementing one deterministic step of this stage.
    Contribution: Contributes a deterministic transformation that supports end-to-end reasoning reproducibility.
    """

    text = path.read_text(encoding="utf-8")

    header_match = HEADER_RE.search(text)
    agent = header_match.group(1).strip() if header_match else path.parent.name

    payload: dict[str, Any] = {
        "agent": agent,
        "log_path": str(path),
        "step_count": len(STEP_RE.findall(text)),
        "step_titles": _extract_step_titles(text),
        "outputs": _extract_outputs(text),
        "stage_counts": _extract_stage_counts(text),
        "kv": _extract_kv_pairs(text),
    }

    for key, pattern in FIELD_RE.items():
        match = pattern.search(text)
        if match:
            payload[key] = match.group(1).strip()

    payload["duration_s"] = _safe_float(payload.get("duration_s", 0.0), 0.0)
    payload.setdefault("status", "unknown")
    payload.setdefault("summary", "")
    payload.setdefault("run_id", "")
    payload.setdefault("started_utc", "")
    payload.setdefault("ended_utc", "")
    return payload


def _resolve_candidate_path(raw: str, repo_root: Path) -> Path:
    """
    Relevance: Operates within the orchestration and observability layer.
    Concept: Internal helper implementing one deterministic step of this stage.
    Contribution: Normalizes relative/absolute paths so artifact scoping checks are deterministic.
    """

    p = Path(raw.strip())
    if not p.is_absolute():
        p = repo_root / p
    return p.resolve()


def _is_under(path: Path, root: Path) -> bool:
    """
    Relevance: Operates within the orchestration and observability layer.
    Concept: Internal helper implementing one deterministic step of this stage.
    Contribution: Provides containment checks for per-KB artifact isolation.
    """

    try:
        path.resolve().relative_to(root.resolve())
        return True
    except ValueError:
        return False


def _matches_filters(
    item: dict[str, Any],
    repo_root: Path,
    artifacts_dir: Path,
    kb_filter: str,
    kb_ref_filter: str,
    run_id: str,
) -> bool:
    """
    Relevance: Operates within the orchestration and observability layer.
    Concept: Internal helper implementing one deterministic step of this stage.
    Contribution: Enforces one-KB-at-a-time log indexing across multi-KB repositories.
    """

    item_run_id = str(item.get("run_id", "")).strip()
    if run_id and item_run_id != run_id:
        return False

    kv = item.get("kv", {}) if isinstance(item.get("kv"), dict) else {}
    if kb_filter:
        kb_value = str(kv.get("kb", "")).strip()
        if kb_value:
            if kb_value != kb_filter:
                kb_abs = _resolve_candidate_path(kb_value, repo_root)
                kb_abs_filter = _resolve_candidate_path(kb_filter, repo_root)
                if kb_abs != kb_abs_filter:
                    return False

    if kb_ref_filter:
        log_kb_ref = normalize_kb_ref(str(kv.get("kb_ref", "")).strip())
        if not log_kb_ref:
            kb_value = str(kv.get("kb", "")).strip()
            if kb_value:
                log_kb_ref = kb_ref_from_kb_filename(Path(kb_value))
        if log_kb_ref and log_kb_ref != kb_ref_filter:
            return False

    artifacts_kv = str(kv.get("artifacts_dir", "")).strip()
    if artifacts_kv:
        try:
            if _resolve_candidate_path(artifacts_kv, repo_root) == artifacts_dir.resolve():
                return True
        except Exception:
            pass

    outputs = item.get("outputs", []) if isinstance(item.get("outputs"), list) else []
    for out in outputs:
        if not isinstance(out, dict):
            continue
        path_raw = str(out.get("path", "")).strip()
        if not path_raw:
            continue
        try:
            if _is_under(_resolve_candidate_path(path_raw, repo_root), artifacts_dir):
                return True
        except Exception:
            continue

    # If run-id is explicitly scoped, keep logs even when outputs land outside artifacts_dir
    # (e.g., phyp-doc-exporter writes into `phyp/`).
    if run_id:
        return True

    # Keep entries if no explicit artifacts evidence is present but KB/run filters passed.
    return not bool(artifacts_kv or outputs)


def _load_logs(
    log_root: Path,
    repo_root: Path,
    artifacts_dir: Path,
    kb_filter: str = "",
    kb_ref_filter: str = "",
    run_id: str | None = None,
    exclude_log_paths: set[str] | None = None,
) -> list[dict[str, Any]]:
    """
    Relevance: Operates within the orchestration and observability layer.
    Concept: Loading and structuring external artifacts for deterministic processing.
    Contribution: Provides clean, typed inputs so downstream reasoning steps remain auditable.
    """

    logs: list[dict[str, Any]] = []
    if not log_root.exists():
        return logs

    exclude = {str(Path(p).resolve()) for p in (exclude_log_paths or set())}
    for path in sorted(log_root.glob("*/*.md")):
        if not path.is_file():
            continue
        if str(path.resolve()) in exclude:
            continue
        try:
            item = _parse_log(path)
        except Exception:
            continue
        if not _matches_filters(
            item=item,
            repo_root=repo_root,
            artifacts_dir=artifacts_dir,
            kb_filter=kb_filter,
            kb_ref_filter=kb_ref_filter,
            run_id=run_id or "",
        ):
            continue
        logs.append(item)

    logs.sort(key=lambda x: str(x.get("started_utc", "")))
    return logs


def _summarize(
    logs: list[dict[str, Any]],
    expected_agents: list[str],
    expected_stages: list[str] | None = None,
) -> dict[str, Any]:
    """
    Relevance: Operates within the orchestration and observability layer.
    Concept: Internal helper implementing one deterministic step of this stage.
    Contribution: Contributes a deterministic transformation that supports end-to-end reasoning reproducibility.
    """

    by_status: dict[str, int] = {}
    agent_counts: dict[str, int] = {}
    for item in logs:
        status = str(item.get("status", "unknown")).strip().lower() or "unknown"
        by_status[status] = by_status.get(status, 0) + 1
        agent = str(item.get("agent", "unknown")).strip() or "unknown"
        agent_counts[agent] = agent_counts.get(agent, 0) + 1

    observed_agents = sorted(agent_counts.keys())
    expected_set = sorted({a.strip() for a in expected_agents if a.strip()})
    missing_expected = [a for a in expected_set if a not in observed_agents]

    stage_matrix: dict[str, dict[str, Any]] = {}
    per_agent_stage_matrix: dict[str, dict[str, dict[str, int]]] = {}
    for item in logs:
        agent = str(item.get("agent", "unknown")).strip() or "unknown"
        stage_counts = item.get("stage_counts", {}) if isinstance(item.get("stage_counts"), dict) else {}
        starts = stage_counts.get("started", {}) if isinstance(stage_counts.get("started"), dict) else {}
        completes = stage_counts.get("completed", {}) if isinstance(stage_counts.get("completed"), dict) else {}
        for stage_id in sorted(set(starts.keys()) | set(completes.keys())):
            started_count = int(starts.get(stage_id, 0) or 0)
            completed_count = int(completes.get(stage_id, 0) or 0)
            row = stage_matrix.setdefault(
                stage_id,
                {
                    "stage_id": stage_id,
                    "started": 0,
                    "completed": 0,
                    "agents": set(),
                },
            )
            row["started"] += started_count
            row["completed"] += completed_count
            row["agents"].add(agent)
            agent_row = per_agent_stage_matrix.setdefault(agent, {}).setdefault(stage_id, {"started": 0, "completed": 0})
            agent_row["started"] += started_count
            agent_row["completed"] += completed_count

    expected_stage_ids = sorted(
        {_normalize_stage_id(s) for s in (expected_stages or []) if _normalize_stage_id(str(s).strip())}
    )
    observed_stage_ids = sorted(stage_matrix.keys())
    missing_expected_stages = [sid for sid in expected_stage_ids if sid not in observed_stage_ids]
    incomplete_expected_stages = [
        sid
        for sid in expected_stage_ids
        if sid in stage_matrix and (int(stage_matrix[sid]["started"]) <= 0 or int(stage_matrix[sid]["completed"]) <= 0)
    ]
    stage_coverage_complete = not missing_expected_stages and not incomplete_expected_stages

    stage_matrix_list = []
    for sid in observed_stage_ids:
        row = stage_matrix[sid]
        stage_matrix_list.append(
            {
                "stage_id": sid,
                "started": int(row.get("started", 0)),
                "completed": int(row.get("completed", 0)),
                "agents": sorted(str(x) for x in row.get("agents", set())),
            }
        )

    per_agent_stage_list: dict[str, list[dict[str, Any]]] = {}
    for agent, stage_rows in per_agent_stage_matrix.items():
        per_agent_stage_list[agent] = [
            {"stage_id": sid, "started": int(vals.get("started", 0)), "completed": int(vals.get("completed", 0))}
            for sid, vals in sorted(stage_rows.items())
        ]

    return {
        "log_count": len(logs),
        "status_counts": by_status,
        "agent_counts": agent_counts,
        "observed_agents": observed_agents,
        "expected_agents": expected_set,
        "missing_expected_agents": missing_expected,
        "observed_stage_ids": observed_stage_ids,
        "expected_stage_ids": expected_stage_ids,
        "missing_expected_stages": missing_expected_stages,
        "incomplete_expected_stages": incomplete_expected_stages,
        "stage_coverage_complete": stage_coverage_complete,
        "stage_matrix": stage_matrix_list,
        "per_agent_stage_matrix": per_agent_stage_list,
    }


def _to_markdown(report: dict[str, Any]) -> str:
    """
    Relevance: Operates within the orchestration and observability layer.
    Concept: Rendering internal outputs into human-readable artifacts.
    Contribution: Improves interpretability by exposing machine results in analyst-friendly form.
    """

    meta = report.get("metadata", {}) if isinstance(report.get("metadata"), dict) else {}
    summary = report.get("summary", {}) if isinstance(report.get("summary"), dict) else {}
    logs = report.get("logs", []) if isinstance(report.get("logs"), list) else []

    lines: list[str] = []
    lines.append("# Reasoning Log Index")
    lines.append("")
    lines.append("This index consolidates reasoning logs for a run and highlights whether expected stages emitted logs.")
    lines.append("")

    lines.append("## Run Context")
    lines.append("")
    lines.append(f"- Generated (UTC): {meta.get('generated_utc', '')}")
    lines.append(f"- KB: {meta.get('kb', '')}")
    lines.append(f"- KB Ref: {meta.get('kb_ref', '')}")
    lines.append(f"- Artifacts directory: {meta.get('artifacts_dir', '')}")
    lines.append(f"- Log root: {meta.get('reasoning_log_root', '')}")
    lines.append(f"- Run ID filter: {meta.get('run_id_filter', '(none)')}")
    lines.append("")

    lines.append("## Coverage Summary")
    lines.append("")
    lines.append(f"- Logs indexed: {summary.get('log_count', 0)}")
    lines.append(f"- Status counts: {json.dumps(summary.get('status_counts', {}), ensure_ascii=False)}")
    lines.append(f"- Observed agents: {', '.join(summary.get('observed_agents', [])) or '(none)'}")
    lines.append(f"- Expected agents: {', '.join(summary.get('expected_agents', [])) or '(none)'}")
    missing = summary.get("missing_expected_agents", [])
    if missing:
        lines.append(f"- Missing expected agents: {', '.join(missing)}")
        lines.append("- Coverage verdict: incomplete")
    else:
        lines.append("- Missing expected agents: none")
        lines.append("- Coverage verdict: complete")
    lines.append("")

    lines.append("## Stage Coverage")
    lines.append("")
    lines.append(f"- Observed stages: {', '.join(summary.get('observed_stage_ids', [])) or '(none)'}")
    lines.append(f"- Expected stages: {', '.join(summary.get('expected_stage_ids', [])) or '(none)'}")
    missing_stages = summary.get("missing_expected_stages", [])
    incomplete_stages = summary.get("incomplete_expected_stages", [])
    if missing_stages:
        lines.append(f"- Missing expected stages: {', '.join(missing_stages)}")
    else:
        lines.append("- Missing expected stages: none")
    if incomplete_stages:
        lines.append(f"- Incomplete expected stages: {', '.join(incomplete_stages)}")
    else:
        lines.append("- Incomplete expected stages: none")
    lines.append(
        f"- Stage coverage verdict: {'complete' if bool(summary.get('stage_coverage_complete', False)) else 'incomplete'}"
    )
    lines.append("")
    lines.append("| stage_id | started | completed | agents |")
    lines.append("|---|---:|---:|---|")
    for row in summary.get("stage_matrix", []) if isinstance(summary.get("stage_matrix"), list) else []:
        if not isinstance(row, dict):
            continue
        agents = row.get("agents", [])
        agents_s = ", ".join(str(x) for x in agents) if isinstance(agents, list) else ""
        lines.append(
            f"| {row.get('stage_id', '')} | {row.get('started', 0)} | {row.get('completed', 0)} | {agents_s} |"
        )
    lines.append("")

    lines.append("## Run Timeline")
    lines.append("")
    lines.append("| start_utc | end_utc | agent | status | duration_s | key_step |")
    lines.append("|---|---|---|---|---:|---|")
    for item in logs:
        titles = item.get("step_titles", []) if isinstance(item.get("step_titles"), list) else []
        key_step = str(titles[0]).replace("|", "\\|") if titles else ""
        lines.append(
            f"| {item.get('started_utc', '')} | {item.get('ended_utc', '')} | {item.get('agent', '')} | "
            f"{item.get('status', '')} | {item.get('duration_s', 0.0)} | {key_step} |"
        )
    lines.append("")

    lines.append("## Log Table")
    lines.append("")
    lines.append("| agent | status | duration_s | steps | key_steps | summary | log_path |")
    lines.append("|---|---|---:|---:|---|---|---|")
    for item in logs:
        summary_text = str(item.get("summary", "")).strip().replace("|", "\\|")
        titles = item.get("step_titles", []) if isinstance(item.get("step_titles"), list) else []
        key_steps = "; ".join(str(t).strip() for t in titles[:3] if str(t).strip()).replace("|", "\\|")
        lines.append(
            f"| {item.get('agent', '')} | {item.get('status', '')} | {item.get('duration_s', 0.0)} | "
            f"{item.get('step_count', 0)} | {key_steps} | {summary_text} | {item.get('log_path', '')} |"
        )
    lines.append("")

    lines.append("## Agent Details")
    lines.append("")
    if not logs:
        lines.append("- No logs found for this filter.")
    for item in logs:
        lines.append(f"### {item.get('agent', 'unknown')}")
        lines.append("")
        lines.append(f"- Log: {item.get('log_path', '')}")
        lines.append(f"- Run ID: {item.get('run_id', '')}")
        lines.append(f"- Status: {item.get('status', '')}")
        lines.append(f"- Started: {item.get('started_utc', '')}")
        lines.append(f"- Ended: {item.get('ended_utc', '')}")
        lines.append(f"- Duration (s): {item.get('duration_s', 0.0)}")
        lines.append(f"- Steps: {item.get('step_count', 0)}")
        titles = item.get("step_titles", []) if isinstance(item.get("step_titles"), list) else []
        if titles:
            lines.append(f"- Key steps: {'; '.join(str(t) for t in titles[:8])}")
        else:
            lines.append("- Key steps: none parsed")
        lines.append(f"- Summary: {item.get('summary', '')}")

        outputs = item.get("outputs", []) if isinstance(item.get("outputs"), list) else []
        if outputs:
            lines.append("- Declared outputs:")
            for out in outputs[:20]:
                if not isinstance(out, dict):
                    continue
                lines.append(f"  - {out.get('label', '')}: {out.get('path', '')}")
        else:
            lines.append("- Declared outputs: none")
        lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    """
    Relevance: Operates within the orchestration and observability layer.
    Concept: CLI entrypoint orchestration for this script.
    Contribution: Binds parsing, computation, and artifact emission into a reproducible script execution.
    """

    logger = ReasoningLogger("kb-log-indexer")
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--artifacts-dir", required=True, help="Path to artifacts/<kb-slug> directory.")
    ap.add_argument("--kb", default="", help="Optional KB path for report context.")
    ap.add_argument("--kb-ref", default="", help="Optional KB reference filter. Defaults to artifacts directory name.")
    ap.add_argument("--reasoning-log-root", default="artifacts/reasoning-logs")
    ap.add_argument("--run-id", default="", help="Optional run ID filter (exact match).")
    ap.add_argument("--expected-agent", action="append", default=[])
    ap.add_argument("--expected-stage", action="append", default=[])
    ap.add_argument("--exclude-log-path", action="append", default=[])
    ap.add_argument("--output-json", help="Output JSON path.")
    ap.add_argument("--output-md", help="Output Markdown path.")
    args = ap.parse_args()

    repo_root = Path(__file__).resolve().parents[4]
    artifacts_dir = _resolve_candidate_path(args.artifacts_dir, repo_root)
    log_root = _resolve_candidate_path(args.reasoning_log_root, repo_root)
    kb_ref_filter = normalize_kb_ref(args.kb_ref.strip()) or kb_ref_from_artifacts_dir(artifacts_dir)
    if not artifacts_dir.exists():
        log_path = logger.finalize("error", summary=f"Artifacts directory not found: {artifacts_dir}")
        print(f"[LOG] {log_path}", file=sys.stderr)
        raise SystemExit(f"[ERROR] Artifacts directory not found: {artifacts_dir}")

    output_json = Path(args.output_json) if args.output_json else artifacts_dir / "reasoning-log-index.json"
    output_md = Path(args.output_md) if args.output_md else artifacts_dir / "reasoning-log-index.md"

    logger.step(
        "Parsed reasoning-log-index arguments",
        "\n".join(
            [
                f"artifacts_dir={artifacts_dir}",
                f"kb={args.kb}",
                f"kb_ref={kb_ref_filter}",
                f"reasoning_log_root={log_root}",
                f"run_id={args.run_id}",
                f"expected_agents={args.expected_agent}",
                f"expected_stages={args.expected_stage}",
                f"exclude_log_paths={args.exclude_log_path}",
                f"output_json={output_json}",
                f"output_md={output_md}",
            ]
        ),
    )

    excluded = {str(logger.log_path.resolve())}
    excluded.update(str(_resolve_candidate_path(p, repo_root)) for p in args.exclude_log_path)
    logs = _load_logs(
        log_root,
        repo_root=repo_root,
        artifacts_dir=artifacts_dir,
        kb_filter=args.kb.strip(),
        kb_ref_filter=kb_ref_filter,
        run_id=args.run_id or None,
        exclude_log_paths=excluded,
    )
    summary = _summarize(logs, expected_agents=args.expected_agent, expected_stages=args.expected_stage)

    report = {
        "metadata": {
            "generated_utc": dt.datetime.now(dt.UTC).isoformat(),
            "kb": args.kb,
            "kb_ref": kb_ref_filter,
            "artifacts_dir": str(artifacts_dir),
            "reasoning_log_root": str(log_root),
            "run_id_filter": args.run_id or "",
        },
        "summary": summary,
        "logs": logs,
    }

    output_json.parent.mkdir(parents=True, exist_ok=True)
    output_md.parent.mkdir(parents=True, exist_ok=True)
    output_json.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    output_md.write_text(_to_markdown(report), encoding="utf-8")

    print(f"[OK] Wrote JSON log index: {output_json}")
    print(f"[OK] Wrote Markdown log index: {output_md}")
    logger.add_output("reasoning_log_index_json", output_json)
    logger.add_output("reasoning_log_index_md", output_md)
    log_path = logger.finalize(
        "success",
        summary=f"Indexed {len(logs)} reasoning logs ({len(summary.get('missing_expected_agents', []))} missing expected agents).",
    )
    print(f"[LOG] {log_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
