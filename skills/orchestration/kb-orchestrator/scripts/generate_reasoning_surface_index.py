#!/usr/bin/env python3
# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT

"""Aggregate human-facing reasoning surfaces into a run-level conceptual index."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any

_COMMON_DIR = Path(__file__).resolve().parents[3] / "common"
if str(_COMMON_DIR) not in sys.path:
    sys.path.insert(0, str(_COMMON_DIR))

from kb_context import kb_ref_from_artifacts_dir
from kb_context import kb_ref_from_kb_filename
from kb_context import normalize_kb_ref
from reasoning_log import ReasoningLogger


def _resolve_candidate_path(raw: str, repo_root: Path) -> Path:
    """
    Relevance: Operates within the orchestration and observability layer.
    Concept: Internal helper implementing one deterministic step of this stage.
    Contribution: Normalizes relative and absolute paths so KB-scoped filtering remains deterministic.
    """

    p = Path(str(raw).strip())
    if not p.is_absolute():
        p = repo_root / p
    return p.resolve()


def _is_under(path: Path, root: Path) -> bool:
    """
    Relevance: Operates within the orchestration and observability layer.
    Concept: Internal helper implementing one deterministic step of this stage.
    Contribution: Provides path-containment checks for KB-scoped artifact isolation.
    """

    try:
        path.resolve().relative_to(root.resolve())
        return True
    except ValueError:
        return False


def _safe_list(value: Any) -> list[Any]:
    """
    Relevance: Operates within the orchestration and observability layer.
    Concept: Defensive conversion/parsing to keep reporting robust.
    Contribution: Prevents malformed surfaced logs from destabilizing run-level summaries.
    """

    return value if isinstance(value, list) else []


def _load_surface(path: Path) -> dict[str, Any]:
    """
    Relevance: Operates within the orchestration and observability layer.
    Concept: Loading and structuring external artifacts for deterministic processing.
    Contribution: Produces a normalized surfaced-log payload for downstream conceptual indexing.
    """

    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"Surface payload is not an object: {path}")

    context = payload.get("context", {})
    if not isinstance(context, dict):
        context = {}
    outputs = payload.get("outputs", [])
    if not isinstance(outputs, list):
        outputs = []
    moments = payload.get("moments", [])
    if not isinstance(moments, list):
        moments = []

    agent = str(payload.get("agent", "")).strip() or path.parent.name
    run_id = str(payload.get("run_id", "")).strip() or path.stem
    item = {
        "agent": agent,
        "run_id": run_id,
        "status": str(payload.get("status", "unknown")).strip() or "unknown",
        "started_utc": str(payload.get("started_utc", "")).strip(),
        "ended_utc": str(payload.get("ended_utc", "")).strip(),
        "duration_s": payload.get("duration_s", 0.0),
        "summary": str(payload.get("summary", "")).strip(),
        "internal_log_path": str(payload.get("internal_log_path", "")).strip(),
        "surface_markdown_path": str(payload.get("surface_markdown_path", "")).strip(),
        "surface_json_path": str(path.resolve()),
        "context": context,
        "outputs": outputs,
        "moments": moments,
        "moment_count": len(moments),
    }
    return item


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
    Contribution: Keeps surfaced indexing aligned with KB/run scoping semantics already used by reasoning logs.
    """

    item_run_id = str(item.get("run_id", "")).strip()
    if run_id and item_run_id != run_id:
        return False

    context = item.get("context", {}) if isinstance(item.get("context"), dict) else {}
    if kb_filter:
        kb_value = str(context.get("kb", "")).strip()
        if kb_value:
            if kb_value != kb_filter:
                kb_abs = _resolve_candidate_path(kb_value, repo_root)
                kb_abs_filter = _resolve_candidate_path(kb_filter, repo_root)
                if kb_abs != kb_abs_filter:
                    return False

    if kb_ref_filter:
        surface_kb_ref = normalize_kb_ref(str(context.get("kb_ref", "")).strip())
        if not surface_kb_ref:
            kb_value = str(context.get("kb", "")).strip()
            if kb_value:
                surface_kb_ref = kb_ref_from_kb_filename(Path(kb_value))
        if surface_kb_ref and surface_kb_ref != kb_ref_filter:
            return False

    artifacts_kv = str(context.get("artifacts_dir", "")).strip()
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

    if run_id:
        return True

    return not bool(artifacts_kv or outputs)


def _load_surfaces(
    surface_root: Path,
    repo_root: Path,
    artifacts_dir: Path,
    kb_filter: str = "",
    kb_ref_filter: str = "",
    run_id: str | None = None,
    exclude_surface_paths: set[str] | None = None,
) -> list[dict[str, Any]]:
    """
    Relevance: Operates within the orchestration and observability layer.
    Concept: Loading and structuring external artifacts for deterministic processing.
    Contribution: Collects surfaced reasoning artifacts for a single KB/run without mixing unrelated sessions.
    """

    surfaces: list[dict[str, Any]] = []
    if not surface_root.exists():
        return surfaces

    exclude = {str(Path(p).resolve()) for p in (exclude_surface_paths or set())}
    for path in sorted(surface_root.glob("*/*.json")):
        if not path.is_file():
            continue
        if str(path.resolve()) in exclude:
            continue
        try:
            item = _load_surface(path)
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
        surfaces.append(item)

    surfaces.sort(key=lambda x: str(x.get("started_utc", "")))
    return surfaces


def _timeline(surfaces: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """
    Relevance: Operates within the orchestration and observability layer.
    Concept: Extraction of structured signals from raw text or artifact payloads.
    Contribution: Produces a conceptual movement timeline over surfaced reasoning moments.
    """

    events: list[dict[str, Any]] = []
    for item in surfaces:
        agent = str(item.get("agent", "")).strip() or "unknown"
        for moment in _safe_list(item.get("moments")):
            if not isinstance(moment, dict):
                continue
            events.append(
                {
                    "timestamp": str(moment.get("timestamp", "")).strip(),
                    "agent": agent,
                    "kind": str(moment.get("kind", "")).strip() or "conceptual_move",
                    "focus": str(moment.get("focus", "")).strip(),
                    "title": str(moment.get("title", "")).strip(),
                    "significance": str(moment.get("significance", "")).strip(),
                    "stage": str(moment.get("stage", "")).strip(),
                }
            )
    events.sort(key=lambda x: (x.get("timestamp", ""), x.get("agent", ""), x.get("title", "")))
    return events


def _summarize(surfaces: list[dict[str, Any]], expected_agents: list[str]) -> dict[str, Any]:
    """
    Relevance: Operates within the orchestration and observability layer.
    Concept: Internal helper implementing one deterministic step of this stage.
    Contribution: Condenses surfaced conceptual movement into run-level coverage and focus metrics.
    """

    status_counts: dict[str, int] = {}
    agent_counts: dict[str, int] = {}
    moment_kind_counter: Counter[str] = Counter()
    focus_counter: Counter[str] = Counter()

    for item in surfaces:
        status = str(item.get("status", "unknown")).strip().lower() or "unknown"
        status_counts[status] = status_counts.get(status, 0) + 1
        agent = str(item.get("agent", "unknown")).strip() or "unknown"
        agent_counts[agent] = agent_counts.get(agent, 0) + 1
        for moment in _safe_list(item.get("moments")):
            if not isinstance(moment, dict):
                continue
            kind = str(moment.get("kind", "")).strip() or "conceptual_move"
            focus = str(moment.get("focus", "")).strip()
            moment_kind_counter[kind] += 1
            if focus:
                focus_counter[focus] += 1

    observed_agents = sorted(agent_counts.keys())
    expected_set = sorted({str(a).strip() for a in expected_agents if str(a).strip()})
    missing_expected = [a for a in expected_set if a not in observed_agents]

    return {
        "surface_count": len(surfaces),
        "status_counts": status_counts,
        "agent_counts": agent_counts,
        "observed_agents": observed_agents,
        "expected_agents": expected_set,
        "missing_expected_agents": missing_expected,
        "moment_kind_counts": dict(moment_kind_counter),
        "top_focuses": [{"focus": focus, "count": count} for focus, count in focus_counter.most_common(12)],
        "total_moment_count": sum(moment_kind_counter.values()),
    }


def _to_markdown(report: dict[str, Any]) -> str:
    """
    Relevance: Operates within the orchestration and observability layer.
    Concept: Rendering internal outputs into human-readable artifacts.
    Contribution: Produces a KB-scoped conceptual view of the reasoning dynamics separate from audit logs.
    """

    meta = report.get("metadata", {}) if isinstance(report.get("metadata"), dict) else {}
    summary = report.get("summary", {}) if isinstance(report.get("summary"), dict) else {}
    timeline = report.get("timeline", []) if isinstance(report.get("timeline"), list) else []
    surfaces = report.get("surfaces", []) if isinstance(report.get("surfaces"), list) else []

    lines: list[str] = []
    lines.append("# Reasoning Surface Index")
    lines.append("")
    lines.append("This index is the human-facing conceptual view over surfaced reasoning logs for the selected run.")
    lines.append("")
    lines.append("## Run Context")
    lines.append("")
    lines.append(f"- Generated (UTC): {meta.get('generated_utc', '')}")
    lines.append(f"- KB: {meta.get('kb', '')}")
    lines.append(f"- KB Ref: {meta.get('kb_ref', '')}")
    lines.append(f"- Artifacts directory: {meta.get('artifacts_dir', '')}")
    lines.append(f"- Surface root: {meta.get('reasoning_surface_root', '')}")
    lines.append(f"- Run ID filter: {meta.get('run_id_filter', '(none)')}")
    lines.append("")

    lines.append("## Coverage Summary")
    lines.append("")
    lines.append(f"- Surfaces indexed: {summary.get('surface_count', 0)}")
    lines.append(f"- Total surfaced moments: {summary.get('total_moment_count', 0)}")
    lines.append(f"- Status counts: {json.dumps(summary.get('status_counts', {}), ensure_ascii=False)}")
    lines.append(f"- Observed agents: {', '.join(summary.get('observed_agents', [])) or '(none)'}")
    missing = summary.get("missing_expected_agents", [])
    if missing:
        lines.append(f"- Missing expected agents: {', '.join(missing)}")
    else:
        lines.append("- Missing expected agents: none")
    moment_kind_counts = summary.get("moment_kind_counts", {})
    if isinstance(moment_kind_counts, dict) and moment_kind_counts:
        kind_pairs = [f"{key}={moment_kind_counts[key]}" for key in sorted(moment_kind_counts.keys())]
        lines.append(f"- Surface movement kinds: {', '.join(kind_pairs)}")
    else:
        lines.append("- Surface movement kinds: none")
    top_focuses = summary.get("top_focuses", [])
    if isinstance(top_focuses, list) and top_focuses:
        focus_text = ", ".join(f"{item.get('focus', '')} ({item.get('count', 0)})" for item in top_focuses[:8] if isinstance(item, dict))
        lines.append(f"- Dominant conceptual foci: {focus_text or '(none)'}")
    else:
        lines.append("- Dominant conceptual foci: none")
    lines.append("")

    lines.append("## Conceptual Timeline")
    lines.append("")
    lines.append("| timestamp | agent | kind | focus | move | why_it_matters |")
    lines.append("|---|---|---|---|---|---|")
    for event in timeline:
        if not isinstance(event, dict):
            continue
        lines.append(
            f"| {str(event.get('timestamp', '')).replace('|', '\\|')} "
            f"| {str(event.get('agent', '')).replace('|', '\\|')} "
            f"| {str(event.get('kind', '')).replace('|', '\\|')} "
            f"| {str(event.get('focus', '')).replace('|', '\\|')} "
            f"| {str(event.get('title', '')).replace('|', '\\|')} "
            f"| {str(event.get('significance', '')).replace('|', '\\|')} |"
        )
    lines.append("")

    lines.append("## Agent Surfaces")
    lines.append("")
    if not surfaces:
        lines.append("- No surfaced logs found for this filter.")
        lines.append("")
    for item in surfaces:
        if not isinstance(item, dict):
            continue
        lines.append(f"### {item.get('agent', 'unknown')}")
        lines.append("")
        lines.append(f"- Surface log: {item.get('surface_markdown_path', '')}")
        lines.append(f"- Internal log: {item.get('internal_log_path', '')}")
        lines.append(f"- Status: {item.get('status', '')}")
        lines.append(f"- Summary: {item.get('summary', '')}")
        lines.append(f"- Surfaced moments: {item.get('moment_count', 0)}")
        moments = _safe_list(item.get("moments"))
        if moments:
            lines.append("- First surfaced moves:")
            for moment in moments[:5]:
                if not isinstance(moment, dict):
                    continue
                lines.append(
                    f"  - {moment.get('kind', '')}: {moment.get('title', '')}"
                    + (f" | focus={moment.get('focus', '')}" if str(moment.get("focus", "")).strip() else "")
                )
        else:
            lines.append("- First surfaced moves: none")
        lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    """
    Relevance: Operates within the orchestration and observability layer.
    Concept: CLI entrypoint orchestration for this script.
    Contribution: Binds surfaced-log loading, summarization, and artifact emission into a reproducible run.
    """

    logger = ReasoningLogger("kb-surface-indexer")
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--artifacts-dir", required=True, help="Path to artifacts/<kb-slug> directory.")
    ap.add_argument("--kb", default="", help="Optional KB path for report context.")
    ap.add_argument("--kb-ref", default="", help="Optional KB reference filter. Defaults to artifacts directory name.")
    ap.add_argument("--reasoning-surface-root", default="artifacts/reasoning-surfaces")
    ap.add_argument("--run-id", default="", help="Optional run ID filter (exact match).")
    ap.add_argument("--expected-agent", action="append", default=[])
    ap.add_argument("--exclude-surface-path", action="append", default=[])
    ap.add_argument("--output-json", help="Output JSON path.")
    ap.add_argument("--output-md", help="Output Markdown path.")
    args = ap.parse_args()

    repo_root = Path(__file__).resolve().parents[4]
    artifacts_dir = _resolve_candidate_path(args.artifacts_dir, repo_root)
    surface_root = _resolve_candidate_path(args.reasoning_surface_root, repo_root)
    kb_ref_filter = normalize_kb_ref(args.kb_ref.strip()) or kb_ref_from_artifacts_dir(artifacts_dir)
    if not artifacts_dir.exists():
        log_path = logger.finalize("error", summary=f"Artifacts directory not found: {artifacts_dir}")
        print(f"[LOG] {log_path}", file=sys.stderr)
        raise SystemExit(f"[ERROR] Artifacts directory not found: {artifacts_dir}")

    output_json = Path(args.output_json) if args.output_json else artifacts_dir / "reasoning-surface-index.json"
    output_md = Path(args.output_md) if args.output_md else artifacts_dir / "reasoning-surface-index.md"

    logger.step(
        "Parsed reasoning-surface-index arguments",
        "\n".join(
            [
                f"artifacts_dir={artifacts_dir}",
                f"kb={args.kb}",
                f"kb_ref={kb_ref_filter}",
                f"reasoning_surface_root={surface_root}",
                f"run_id={args.run_id}",
                f"expected_agents={args.expected_agent}",
                f"exclude_surface_paths={args.exclude_surface_path}",
                f"output_json={output_json}",
                f"output_md={output_md}",
            ]
        ),
    )

    excluded = {str(logger.surface_json_path.resolve())}
    excluded.update(str(_resolve_candidate_path(p, repo_root)) for p in args.exclude_surface_path)
    surfaces = _load_surfaces(
        surface_root,
        repo_root=repo_root,
        artifacts_dir=artifacts_dir,
        kb_filter=args.kb.strip(),
        kb_ref_filter=kb_ref_filter,
        run_id=args.run_id or None,
        exclude_surface_paths=excluded,
    )
    report = {
        "metadata": {
            "generated_utc": dt.datetime.now(dt.UTC).isoformat(),
            "kb": args.kb,
            "kb_ref": kb_ref_filter,
            "artifacts_dir": str(artifacts_dir),
            "reasoning_surface_root": str(surface_root),
            "run_id_filter": args.run_id or "",
        },
        "summary": _summarize(surfaces, expected_agents=args.expected_agent),
        "timeline": _timeline(surfaces),
        "surfaces": surfaces,
    }

    output_json.parent.mkdir(parents=True, exist_ok=True)
    output_md.parent.mkdir(parents=True, exist_ok=True)
    output_json.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    output_md.write_text(_to_markdown(report), encoding="utf-8")

    print(f"[OK] Wrote JSON surface index: {output_json}")
    print(f"[OK] Wrote Markdown surface index: {output_md}")
    logger.add_output("reasoning_surface_index_json", output_json)
    logger.add_output("reasoning_surface_index_md", output_md)
    log_path = logger.finalize(
        "success",
        summary=f"Indexed {len(surfaces)} surfaced reasoning logs ({report.get('summary', {}).get('total_moment_count', 0)} moments).",
    )
    print(f"[LOG] {log_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
