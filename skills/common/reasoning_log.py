#!/usr/bin/env python3
# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT

"""Shared reasoning log utility for skill scripts.

Creates two clearly separated per-run artifacts:

- internal audit traces in `artifacts/reasoning-logs/<agent-name>/<timestamp>-<pid>.md`
- human-facing conceptual surfaces in
  `artifacts/reasoning-surfaces/<agent-name>/<timestamp>-<pid>.md`
  plus a JSON companion for downstream indexing.
"""

from __future__ import annotations

import datetime as dt
import importlib.util
import json
import os
import re
import sys
from pathlib import Path
from typing import Any
from typing import Iterable


_PDL_SPEC_CACHE: dict[str, Any] | None = None


def _normalized_multiline(text: str | None) -> list[str]:
    """
    Relevance: Operates within the shared utilities layer.
    Concept: Internal helper implementing one deterministic step of this stage.
    Contribution: Normalizes free-form text so both internal and surfaced logs stay stable across callers.
    """

    if not text:
        return []
    return [line.rstrip() for line in str(text).splitlines() if line.rstrip()]


def _slugify(raw: str) -> str:
    """
    Relevance: Operates within the shared utilities layer.
    Concept: Stable naming helper for artifact identifiers.
    Contribution: Keeps generated event types and tags deterministic across runs.
    """

    return re.sub(r"[^A-Za-z0-9._:-]+", "-", str(raw).strip()).strip("-")


def _jsonable(value: Any) -> Any:
    """
    Relevance: Operates within the shared utilities layer.
    Concept: Normalization of input structures into stable internal forms.
    Contribution: Keeps surfaced metadata serializable so prompt-driven conceptual annotations remain portable.
    """

    if value is None or isinstance(value, (str, int, float, bool)):
        return value
    if isinstance(value, Path):
        return str(value)
    if isinstance(value, dict):
        return {str(k): _jsonable(v) for k, v in value.items()}
    if isinstance(value, (list, tuple, set)):
        return [_jsonable(v) for v in value]
    return str(value)


def _load_pdl_spec() -> dict[str, Any]:
    """Load the shared proof-discovery language specification lazily from disk."""

    global _PDL_SPEC_CACHE
    if _PDL_SPEC_CACHE is not None:
        return _PDL_SPEC_CACHE
    module_path = Path(__file__).resolve().with_name("proof_discovery_language.py")
    spec = importlib.util.spec_from_file_location("proof_discovery_language", module_path)
    if not spec or not spec.loader:
        _PDL_SPEC_CACHE = {}
        return _PDL_SPEC_CACHE
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    build_language_spec = getattr(module, "build_language_spec", None)
    if callable(build_language_spec):
        payload = build_language_spec()
        _PDL_SPEC_CACHE = payload if isinstance(payload, dict) else {}
    else:
        _PDL_SPEC_CACHE = {}
    return _PDL_SPEC_CACHE


def _render_pdl_program_lines(program: dict[str, Any]) -> list[str]:
    """Render the compact Markdown lines for one serialized PDL program."""

    module_path = Path(__file__).resolve().with_name("proof_discovery_language.py")
    spec = importlib.util.spec_from_file_location("proof_discovery_language", module_path)
    if not spec or not spec.loader:
        return []
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    renderer = getattr(module, "render_pdl_program_markdown", None)
    if not callable(renderer):
        return []
    rows = renderer(program)
    return rows if isinstance(rows, list) else []


def _pdl_operation_catalog() -> dict[str, dict[str, str]]:
    """Return the shared material-inference operation catalog keyed by operation id."""

    spec = _load_pdl_spec()
    catalog: dict[str, dict[str, str]] = {}
    for row in spec.get("material_inference_operations", []) if isinstance(spec, dict) else []:
        if not isinstance(row, dict):
            continue
        operation_id = _slugify(row.get("id"))
        if not operation_id:
            continue
        catalog[operation_id] = {
            "id": operation_id,
            "symbol": str(row.get("symbol", "")).strip(),
            "form": str(row.get("form", "")).strip(),
            "latex_form": str(row.get("latex_form", "")).strip(),
            "title": str(row.get("title", "")).strip(),
            "effect": str(row.get("effect", "")).strip(),
        }
    return catalog


def _pdl_judgment_catalog() -> dict[str, dict[str, str]]:
    """Return the shared catalog of PDL judgments keyed by form."""

    spec = _load_pdl_spec()
    catalog: dict[str, dict[str, str]] = {}
    if not isinstance(spec, dict):
        return catalog
    for field in ("judgments", "operational_judgments"):
        for row in spec.get(field, []):
            if not isinstance(row, dict):
                continue
            form = str(row.get("form", "")).strip()
            if not form:
                continue
            catalog[form] = {
                "form": form,
                "meaning": str(row.get("meaning", "")).strip(),
            }
    return catalog


def _pdl_control_object_catalog() -> dict[str, dict[str, str]]:
    """Return the shared control-object catalog keyed by object id."""

    spec = _load_pdl_spec()
    catalog: dict[str, dict[str, str]] = {}
    for row in spec.get("control_objects", []) if isinstance(spec, dict) else []:
        if not isinstance(row, dict):
            continue
        object_id = _slugify(row.get("id"))
        if not object_id:
            continue
        catalog[object_id] = {
            "id": object_id,
            "title": str(row.get("title", "")).strip(),
            "role": str(row.get("role", "")).strip(),
        }
    return catalog


def _normalize_pdl_payload(payload: dict[str, Any] | None) -> dict[str, Any]:
    """Normalize an optional PDL payload into a stable surfaced-log shape."""

    if not isinstance(payload, dict):
        return {}
    operation_catalog = _pdl_operation_catalog()
    judgment_catalog = _pdl_judgment_catalog()
    control_catalog = _pdl_control_object_catalog()

    program = payload.get("program")
    normalized_program = program if isinstance(program, dict) else {}

    operations: list[dict[str, Any]] = []
    for raw in payload.get("operations", []) if isinstance(payload.get("operations"), list) else []:
        if isinstance(raw, str):
            operation_id = _slugify(raw)
            base = dict(operation_catalog.get(operation_id, {"id": operation_id}))
            if base:
                operations.append(base)
            continue
        if not isinstance(raw, dict):
            continue
        operation_id = _slugify(raw.get("id") or raw.get("symbol") or raw.get("title"))
        base = dict(operation_catalog.get(operation_id, {"id": operation_id}))
        merged = {**base, **_jsonable(raw)}
        merged["id"] = operation_id
        operations.append(merged)

    judgments: list[dict[str, Any]] = []
    for raw in payload.get("judgments", []) if isinstance(payload.get("judgments"), list) else []:
        if isinstance(raw, str):
            base = dict(judgment_catalog.get(raw.strip(), {"form": raw.strip()}))
            if base:
                judgments.append(base)
            continue
        if not isinstance(raw, dict):
            continue
        form = str(raw.get("form", "")).strip()
        base = dict(judgment_catalog.get(form, {"form": form}))
        merged = {**base, **_jsonable(raw)}
        judgments.append(merged)

    control_objects: list[dict[str, Any]] = []
    for raw in payload.get("control_objects", []) if isinstance(payload.get("control_objects"), list) else []:
        if isinstance(raw, str):
            object_id = _slugify(raw)
            base = dict(control_catalog.get(object_id, {"id": object_id, "title": raw.strip()}))
            control_objects.append(base)
            continue
        if not isinstance(raw, dict):
            continue
        object_id = _slugify(raw.get("id") or raw.get("title"))
        base = dict(control_catalog.get(object_id, {"id": object_id}))
        merged = {**base, **_jsonable(raw)}
        merged["id"] = object_id
        control_objects.append(merged)

    normalized = {
        "program": normalized_program,
        "operations": operations,
        "judgments": judgments,
        "control_objects": control_objects,
        "epistemic_state": _jsonable(payload.get("epistemic_state", {})),
    }
    return normalized if any(normalized.values()) else {}


class ReasoningLogger:
    """Append-only logger with separate internal and surfaced reasoning channels.

    The internal channel is the durable audit trail used by orchestration utilities.
    The surfaced channel is a human-oriented conceptual rendering of the same run,
    designed to make reasoning dynamics easier to inspect in notebooks, IDEs, and
    generated reports.
    """

    def __init__(
        self,
        agent_name: str,
        repo_root: Path | None = None,
        run_id: str | None = None,
        *,
        workflow_id: str = "",
        workflow_version: str = "",
        profile_id: str | None = None,
        target: str = "",
        step_id: str | None = None,
        attempt: int = 1,
    ) -> None:
        """
        Relevance: Operates within the shared utilities layer.
        Concept: Internal helper implementing one deterministic step of this stage.
        Contribution: Contributes a deterministic transformation that supports end-to-end reasoning reproducibility.
        """

        self.agent_name = agent_name.strip() or "unknown-agent"
        self.repo_root = repo_root or Path(__file__).resolve().parents[2]
        timestamp = dt.datetime.now(dt.UTC).strftime("%Y%m%dT%H%M%SZ")
        pid = os.getpid()
        env_run_id = os.environ.get("ABDUCER_RUN_ID", "").strip()
        resolved_run_id = (run_id or env_run_id or f"{timestamp}-{pid}").strip()
        self.run_id = re.sub(r"[^A-Za-z0-9._-]+", "-", resolved_run_id).strip("-") or f"{timestamp}-{pid}"
        self.workflow_id = str(workflow_id).strip() or "legacy-reasoning-logger"
        self.workflow_version = str(workflow_version).strip() or "unversioned"
        self.profile_id = str(profile_id).strip() if profile_id else None
        self.target = str(target).strip() or self.agent_name
        self.step_id = str(step_id).strip() if step_id else None
        self.attempt = max(1, int(attempt))
        self._public_event_ids: list[str] = []

        self.log_dir = self.repo_root / "artifacts" / "reasoning-logs" / self.agent_name
        self.log_dir.mkdir(parents=True, exist_ok=True)
        self.log_path = self.log_dir / f"{timestamp}-{pid}.md"

        self.surface_dir = self.repo_root / "artifacts" / "reasoning-surfaces" / self.agent_name
        self.surface_dir.mkdir(parents=True, exist_ok=True)
        self.surface_md_path = self.surface_dir / f"{timestamp}-{pid}.md"
        self.surface_json_path = self.surface_dir / f"{timestamp}-{pid}.json"

        self._lines: list[str] = []
        self._outputs: list[tuple[str, str]] = []
        self._kv: dict[str, Any] = {}
        self._started = dt.datetime.now(dt.UTC)

        self._surface_payload: dict[str, Any] = {
            "agent": self.agent_name,
            "run_id": self.run_id,
            "started_utc": self._started.isoformat(),
            "internal_log_path": str(self.log_path),
            "surface_markdown_path": str(self.surface_md_path),
            "surface_json_path": str(self.surface_json_path),
            "context": {},
            "outputs": [],
            "moments": [],
            "status": "running",
            "summary": "",
            "ended_utc": "",
            "duration_s": 0.0,
        }
        self._surface_payload["context"].update(
            {
                "workflow_id": self.workflow_id,
                "workflow_version": self.workflow_version,
                "profile_id": self.profile_id,
                "target": self.target,
                "step_id": self.step_id,
                "attempt": self.attempt,
            }
        )

        self._lines.append(f"# Reasoning Log: {self.agent_name}")
        self._lines.append("")
        self._lines.append(f"- Started (UTC): {self._started.isoformat()}")
        self._lines.append(f"- Run ID: {self.run_id}")
        self._lines.append(f"- Log file: {self.log_path}")
        self._lines.append(f"- Surface log (Markdown): {self.surface_md_path}")
        self._lines.append(f"- Surface log (JSON): {self.surface_json_path}")
        self._lines.append("")
        self._flush_all()

    @property
    def surface_path(self) -> Path:
        """
        Relevance: Operates within the shared utilities layer.
        Concept: Primary callable implementing a stage-level behavior.
        Contribution: Exposes the human-facing surface artifact to callers that want to reference it explicitly.
        """

        return self.surface_md_path

    def _flush(self) -> None:
        # Persist after every update so partial traces survive stage failures.
        """
        Relevance: Operates within the shared utilities layer.
        Concept: Internal helper implementing one deterministic step of this stage.
        Contribution: Contributes a deterministic transformation that supports end-to-end reasoning reproducibility.
        """

        self.log_path.write_text("\n".join(self._lines).rstrip() + "\n", encoding="utf-8")

    def _flush_all(self) -> None:
        """Flush both audit log and surface files; attempts both even if one raises.

        Relevance: Operates within the shared utilities layer.
        Concept: Internal helper implementing one deterministic step of this stage.
        Contribution: Prevents partial-flush state divergence by ensuring both files are
        always attempted together and any error is reported after both are tried.
        """

        exc_log = exc_surface = None
        try:
            self._flush()
        except Exception as exc:
            exc_log = exc
        try:
            self._flush_surface()
        except Exception as exc:
            exc_surface = exc
        if exc_log:
            raise exc_log
        if exc_surface:
            raise exc_surface

    def _flush_surface(self) -> None:
        """
        Relevance: Operates within the shared utilities layer.
        Concept: Rendering internal outputs into human-readable artifacts.
        Contribution: Keeps the surfaced conceptual log incrementally inspectable during long runs.
        """

        self.surface_json_path.write_text(
            json.dumps(self._surface_payload, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
        self.surface_md_path.write_text(self._render_surface_markdown(), encoding="utf-8")

    def _surface_kind_from_title(self, title: str) -> str:
        """
        Relevance: Operates within the shared utilities layer.
        Concept: Typed classification used to guide interpretability.
        Contribution: Gives human-facing surfaces a stable vocabulary for reasoning moves across scripts.
        """

        title_s = str(title).strip()
        if title_s.startswith("Running stage:"):
            return "stage_delegation"
        if title_s.startswith("Completed stage:"):
            return "stage_completion"
        if title_s.startswith("Parsed "):
            return "epistemic_framing"
        if title_s.startswith("Loaded "):
            return "evidence_loading"
        if title_s.startswith("Generated ") or title_s.startswith("Built "):
            return "artifact_synthesis"
        if title_s.startswith("Computed ") or title_s.startswith("Ranked "):
            return "result_synthesis"
        if "No child log marker" in title_s:
            return "observability_gap"
        return "reasoning_move"

    def _surface_focus_from_title(self, title: str) -> str:
        """
        Relevance: Operates within the shared utilities layer.
        Concept: Internal helper implementing one deterministic step of this stage.
        Contribution: Extracts a concise conceptual focus so surfaced logs read like an epistemic trajectory.
        """

        title_s = str(title).strip()
        for prefix in ("Running stage:", "Completed stage:"):
            if title_s.startswith(prefix):
                return title_s.split(":", 1)[1].strip()
        return title_s

    def _surface_significance_for_kind(self, kind: str) -> str:
        """
        Relevance: Operates within the shared utilities layer.
        Concept: Rendering internal outputs into human-readable artifacts.
        Contribution: Adds lightweight conceptual interpretation without requiring every caller to hand-author it.
        """

        mapping = {
            "stage_delegation": "Hands the next inferential move to a specialized stage.",
            "stage_completion": "Closes a stage and makes its outputs available for downstream reasoning.",
            "epistemic_framing": "Fixes the local epistemic frame: scope, inputs, and constraints.",
            "evidence_loading": "Brings relevant evidence into scope for the next reasoning move.",
            "artifact_synthesis": "Produces a new artifact that sharpens the current conceptual state.",
            "result_synthesis": "Condenses current evidence into a usable ranked or computed result.",
            "observability_gap": "Highlights a visibility gap between execution and trace capture.",
            "artifact_emitted": "Makes a produced artifact inspectable and reusable by later stages.",
            "run_result": "Records the run-level outcome and whether the current reasoning trajectory closed successfully.",
            "reasoning_move": "Records a meaningful step in the ongoing discovery trajectory.",
            "conceptual_move": "Surfaces a human-facing conceptual interpretation of the current reasoning state.",
        }
        return mapping.get(kind, "Surfaces the current reasoning move in a form designed for human inspection.")

    def _append_surface_moment(
        self,
        *,
        title: str,
        details: str | None = None,
        focus: str = "",
        significance: str = "",
        kind: str = "conceptual_move",
        tags: Iterable[str] | None = None,
        stage: str = "",
        taxonomy: dict[str, Any] | None = None,
        metrics: dict[str, Any] | None = None,
        pdl: dict[str, Any] | None = None,
    ) -> None:
        """
        Relevance: Operates within the shared utilities layer.
        Concept: Rendering internal outputs into human-readable artifacts.
        Contribution: Maintains a separate conceptual surface that can be indexed independently of audit traces.
        """

        timestamp = dt.datetime.now(dt.UTC).isoformat()
        clean_tags = [_slugify(tag) for tag in (tags or []) if _slugify(tag)]
        moment = {
            "timestamp": timestamp,
            "kind": _slugify(kind) or "conceptual_move",
            "title": str(title).strip(),
            "focus": str(focus).strip(),
            "significance": str(significance).strip(),
            "details": _normalized_multiline(details),
            "tags": clean_tags,
            "stage": str(stage).strip(),
            "taxonomy": _jsonable(taxonomy or {}),
            "metrics": _jsonable(metrics or {}),
            "pdl": _normalize_pdl_payload(pdl),
        }
        self._surface_payload.setdefault("moments", []).append(moment)
        self._flush_surface()

    def _render_surface_markdown(self) -> str:
        """
        Relevance: Operates within the shared utilities layer.
        Concept: Rendering internal outputs into human-readable artifacts.
        Contribution: Produces a parallel, human-oriented log that emphasizes conceptual dynamics over raw trace syntax.
        """

        lines: list[str] = []
        lines.append(f"# Reasoning Surface: {self.agent_name}")
        lines.append("")
        lines.append("This artifact is the human-facing conceptual surface of the internal reasoning trace.")
        lines.append("")
        lines.append("## Run Context")
        lines.append("")
        lines.append(f"- Started (UTC): {self._surface_payload.get('started_utc', '')}")
        lines.append(f"- Run ID: {self.run_id}")
        lines.append(f"- Internal reasoning log: {self.log_path}")
        lines.append(f"- Surface JSON: {self.surface_json_path}")
        context = self._surface_payload.get("context", {})
        if isinstance(context, dict) and context:
            for key in sorted(context.keys()):
                lines.append(f"- {key}: {context[key]}")
        lines.append("")

        lines.append("## Conceptual Dynamics")
        lines.append("")
        moments = self._surface_payload.get("moments", [])
        if not isinstance(moments, list) or not moments:
            lines.append("- No surfaced reasoning moments recorded yet.")
            lines.append("")
        else:
            for moment in moments:
                if not isinstance(moment, dict):
                    continue
                lines.append(f"### {moment.get('kind', 'conceptual_move')} @ {moment.get('timestamp', '')}")
                lines.append("")
                lines.append(f"- Move: {moment.get('title', '')}")
                focus = str(moment.get("focus", "")).strip()
                if focus:
                    lines.append(f"- Focus: {focus}")
                significance = str(moment.get("significance", "")).strip()
                if significance:
                    lines.append(f"- Why it matters: {significance}")
                stage = str(moment.get("stage", "")).strip()
                if stage:
                    lines.append(f"- Stage: {stage}")
                tags = moment.get("tags", [])
                if isinstance(tags, list) and tags:
                    lines.append(f"- Tags: {', '.join(str(tag) for tag in tags if str(tag).strip())}")
                metrics = moment.get("metrics", {})
                if isinstance(metrics, dict) and metrics:
                    metric_blob = ", ".join(
                        f"{str(key)}={metrics[key]}"
                        for key in sorted(metrics.keys())
                        if str(key).strip()
                    )
                    if metric_blob:
                        lines.append(f"- Metrics: {metric_blob}")
                taxonomy = moment.get("taxonomy", {})
                if isinstance(taxonomy, dict) and taxonomy:
                    keys = [str(key).strip() for key in taxonomy.keys() if str(key).strip()]
                    if keys:
                        lines.append(f"- Taxonomy keys: {', '.join(sorted(keys))}")
                detail_lines = moment.get("details", [])
                if isinstance(detail_lines, list) and detail_lines:
                    lines.append("- Notes:")
                    for detail in detail_lines:
                        detail_s = str(detail).strip()
                        if detail_s:
                            lines.append(f"  - {detail_s}")
                pdl = moment.get("pdl", {})
                if isinstance(pdl, dict) and pdl:
                    program = pdl.get("program", {})
                    if isinstance(program, dict) and program:
                        lines.append("- PDL program:")
                        for row in _render_pdl_program_lines(program):
                            row_s = str(row).rstrip()
                            if not row_s or row_s.startswith("## "):
                                continue
                            lines.append(f"  {row_s}")
                    operations = pdl.get("operations", [])
                    if isinstance(operations, list) and operations:
                        lines.append("- Material inferences:")
                        for row in operations:
                            if not isinstance(row, dict):
                                continue
                            form = str(row.get("form", "")).strip() or str(row.get("id", "")).strip()
                            title = str(row.get("title", "")).strip()
                            detail = str(row.get("detail", "")).strip() or str(row.get("effect", "")).strip()
                            rendered = form
                            if title:
                                rendered = f"{rendered} | {title}"
                            if detail:
                                rendered = f"{rendered} | {detail}"
                            if rendered.strip():
                                lines.append(f"  - {rendered}")
                    judgments = pdl.get("judgments", [])
                    if isinstance(judgments, list) and judgments:
                        lines.append("- Judgments:")
                        for row in judgments:
                            if not isinstance(row, dict):
                                continue
                            form = str(row.get("form", "")).strip()
                            meaning = str(row.get("meaning", "")).strip()
                            detail = str(row.get("detail", "")).strip()
                            rendered = form
                            if meaning:
                                rendered = f"{rendered} | {meaning}"
                            if detail:
                                rendered = f"{rendered} | {detail}"
                            if rendered.strip():
                                lines.append(f"  - {rendered}")
                    control_objects = pdl.get("control_objects", [])
                    if isinstance(control_objects, list) and control_objects:
                        labels = [
                            str(row.get("title", "")).strip() or str(row.get("id", "")).strip()
                            for row in control_objects
                            if isinstance(row, dict) and (str(row.get("title", "")).strip() or str(row.get("id", "")).strip())
                        ]
                        if labels:
                            lines.append(f"- Control objects: {', '.join(labels)}")
                    epistemic_state = pdl.get("epistemic_state", {})
                    if isinstance(epistemic_state, dict) and epistemic_state:
                        state_blob = ", ".join(
                            f"{str(key)}={epistemic_state[key]}"
                            for key in sorted(epistemic_state.keys())
                            if str(key).strip()
                        )
                        if state_blob:
                            lines.append(f"- Epistemic state: {state_blob}")
                lines.append("")

        status = str(self._surface_payload.get("status", "")).strip()
        if status:
            lines.append("## Run Result")
            lines.append("")
            lines.append(f"- Status: {status}")
            ended = str(self._surface_payload.get("ended_utc", "")).strip()
            if ended:
                lines.append(f"- Ended (UTC): {ended}")
            duration_s = self._surface_payload.get("duration_s", 0.0)
            lines.append(f"- Duration (s): {duration_s}")
            summary = str(self._surface_payload.get("summary", "")).strip()
            if summary:
                lines.append(f"- Summary: {summary}")
            lines.append("")

        outputs = self._surface_payload.get("outputs", [])
        lines.append("## Surfaced Outputs")
        lines.append("")
        if not isinstance(outputs, list) or not outputs:
            lines.append("- No outputs declared yet.")
        else:
            for item in outputs:
                if not isinstance(item, dict):
                    continue
                label = str(item.get("label", "")).strip()
                path = str(item.get("path", "")).strip()
                if label and path:
                    lines.append(f"- {label}: {path}")

        return "\n".join(lines).rstrip() + "\n"

    def step(
        self,
        title: str,
        details: str | None = None,
        *,
        surface_visible: bool = True,
        surface_title: str | None = None,
        surface_focus: str | None = None,
        surface_significance: str | None = None,
        surface_kind: str | None = None,
        surface_tags: Iterable[str] | None = None,
        surface_stage: str | None = None,
        surface_taxonomy: dict[str, Any] | None = None,
        surface_metrics: dict[str, Any] | None = None,
        surface_pdl: dict[str, Any] | None = None,
    ) -> None:
        """
        Relevance: Operates within the shared utilities layer.
        Concept: Primary callable implementing a stage-level behavior.
        Contribution: Contributes a deterministic transformation that supports end-to-end reasoning reproducibility.
        """

        ts = dt.datetime.now(dt.UTC).isoformat()
        self._lines.append(f"## Step @ {ts}")
        self._lines.append("")
        self._lines.append(f"- {title}")
        if details:
            for line in str(details).splitlines():
                self._lines.append(f"- {line}")
        self._lines.append("")
        self._flush()

        if surface_visible:
            kind = str(surface_kind or self._surface_kind_from_title(title)).strip() or "reasoning_move"
            focus = str(surface_focus or self._surface_focus_from_title(title)).strip()
            significance = str(surface_significance or self._surface_significance_for_kind(kind)).strip()
            stage = str(surface_stage or "").strip()
            if not stage and focus and kind in {"stage_delegation", "stage_completion"}:
                stage = focus
            self._append_surface_moment(
                title=surface_title or title,
                details=details,
                focus=focus,
                significance=significance,
                kind=kind,
                tags=surface_tags,
                stage=stage,
                taxonomy=surface_taxonomy,
                metrics=surface_metrics,
                pdl=surface_pdl,
            )

    def surface(
        self,
        title: str,
        details: str | None = None,
        *,
        focus: str = "",
        significance: str = "",
        kind: str = "conceptual_move",
        tags: Iterable[str] | None = None,
        stage: str = "",
        taxonomy: dict[str, Any] | None = None,
        metrics: dict[str, Any] | None = None,
        pdl: dict[str, Any] | None = None,
    ) -> None:
        """
        Relevance: Operates within the shared utilities layer.
        Concept: Primary callable implementing a stage-level behavior.
        Contribution: Allows generative or analyst-authored stages to add explicit human-facing epistemic interpretation.
        """

        self._append_surface_moment(
            title=title,
            details=details,
            focus=focus or title,
            significance=significance or self._surface_significance_for_kind(kind),
            kind=kind,
            tags=tags,
            stage=stage,
            taxonomy=taxonomy,
            metrics=metrics,
            pdl=pdl,
        )

    def _portable_path(self, raw: str | Path) -> tuple[str, bool]:
        """Return a repository-relative path where possible and an external flag."""

        path = Path(str(raw))
        if not path.is_absolute():
            return path.as_posix(), False
        try:
            return path.resolve().relative_to(self.repo_root.resolve()).as_posix(), False
        except ValueError:
            return path.as_posix(), True

    def public_inference(
        self,
        *,
        question: str,
        conclusion: str,
        premises: Iterable[dict[str, Any]] = (),
        operator: str = "",
        warrant: str = "",
        assumptions: Iterable[str] = (),
        alternatives: Iterable[dict[str, Any]] = (),
        falsifiers: Iterable[str] = (),
        uncertainty: str = "",
        scope: dict[str, str] | None = None,
        evidence: Iterable[dict[str, Any]] = (),
        claim_epistemic_status: str = "unknown",
        artifact_validation_status: str = "not_checked",
        workflow_disposition: str = "observed",
        authority_exercised: Iterable[str] = (),
        authority_absent: Iterable[str] = (),
        prohibitions_checked: Iterable[str] = (),
        event_family: str = "public_inference",
        phase: str = "reasoning",
        causal_parent_event_ids: Iterable[str] | None = None,
        trace_completeness: str | None = None,
        idempotency_key: str | None = None,
        obligation: dict[str, Any] | None = None,
        handoff: dict[str, Any] | None = None,
        failure: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Emit one bounded public inference without changing legacy log formats.

        Missing premises, warrant, or evidence are represented explicitly as an
        incomplete trace. They are never inferred from a title or filename.
        """

        normalized_evidence: list[dict[str, Any]] = []
        for row in evidence:
            if not isinstance(row, dict) or not row.get("path"):
                continue
            portable, external = self._portable_path(row["path"])
            normalized_evidence.append(
                {
                    "relation": str(row.get("relation", "background")),
                    "path": portable,
                    "digest": row.get("digest"),
                    "receipt_id": row.get("receipt_id"),
                    "artifact_type": str(row.get("artifact_type", "artifact")),
                    "external": bool(row.get("external", external)),
                }
            )
        normalized_premises = [_jsonable(row) for row in premises if isinstance(row, dict)]
        completeness = trace_completeness or (
            "complete" if normalized_premises and str(warrant).strip() and normalized_evidence else "trace_incomplete"
        )
        counter = len(self._public_event_ids) + 1
        key = idempotency_key or f"public-inference-{counter:04d}"
        material = f"{self.run_id}|{self.workflow_id}|{self.step_id}|{self.attempt}|{event_family}|{key}"
        import hashlib
        event_id = "evt-logger-" + hashlib.sha256(material.encode("utf-8")).hexdigest()[:24]
        parent_ids = list(causal_parent_event_ids) if causal_parent_event_ids is not None else self._public_event_ids[-1:]
        payload: dict[str, Any] = {
            "schema_version": "2.0.0",
            "event_id": event_id,
            "run_id": self.run_id,
            "workflow_id": self.workflow_id,
            "workflow_version": self.workflow_version,
            "profile_id": self.profile_id,
            "target": self.target,
            "phase": str(phase).strip() or "reasoning",
            "step_id": self.step_id,
            "skill": self.agent_name,
            "attempt": self.attempt,
            "branch": None,
            "event_family": event_family,
            "causal_parent_event_ids": parent_ids,
            "parent_artifact_ids": [],
            "artifact_validation_status": artifact_validation_status,
            "claim_epistemic_status": claim_epistemic_status,
            "workflow_disposition": workflow_disposition,
            "public_inference": {
                "question": str(question).strip(),
                "premises": normalized_premises,
                "operator": str(operator).strip(),
                "warrant": str(warrant).strip(),
                "conclusion": str(conclusion).strip(),
                "assumptions": [str(item) for item in assumptions],
                "alternatives": [_jsonable(row) for row in alternatives if isinstance(row, dict)],
                "falsifiers": [str(item) for item in falsifiers],
                "uncertainty": str(uncertainty).strip(),
                "scope": {
                    "regime": str((scope or {}).get("regime", "")),
                    "model": str((scope or {}).get("model", "")),
                    "before": str((scope or {}).get("before", "")),
                    "after": str((scope or {}).get("after", "")),
                },
                "trace_completeness": completeness,
            },
            "evidence": normalized_evidence,
            "authority": {
                "exercised": [str(item) for item in authority_exercised],
                "absent": [str(item) for item in authority_absent],
                "prohibitions_checked": [str(item) for item in prohibitions_checked],
            },
            "idempotency_key": key,
        }
        if obligation is not None:
            payload["obligation"] = _jsonable(obligation)
        if handoff is not None:
            payload["handoff"] = _jsonable(handoff)
        if failure is not None:
            payload["failure"] = _jsonable(failure)

        # The implementation module belongs to the installed/source package;
        # repo_root only selects where this run's artifacts are persisted.
        scripts_dir = Path(__file__).resolve().parents[2] / "agentic" / "scripts"
        if str(scripts_dir) not in sys.path:
            sys.path.insert(0, str(scripts_dir))
        from public_reasoning_trace_store import append_event

        stored = append_event(
            payload,
            store_root=self.repo_root / "agentic" / "traces" / "public_reasoning",
            latest_name=f"logger-{_slugify(self.agent_name)}",
        )
        self._public_event_ids.append(str(stored["event_id"]))
        self._append_surface_moment(
            title=f"Public inference: {conclusion}",
            details=f"question={question}\noperator={operator}\ntrace_completeness={completeness}",
            focus=str(question).strip() or str(conclusion).strip(),
            significance=str(warrant).strip() or "Public rationale is incomplete; inspect the declared gap.",
            kind="public_inference",
            tags=[event_family, claim_epistemic_status, completeness],
            stage=str(phase),
        )
        return stored

    def add_output(self, label: str, path: str | Path) -> None:
        # `add_output` feeds both human log readability and downstream indexers.
        """
        Relevance: Operates within the shared utilities layer.
        Concept: Primary callable implementing a stage-level behavior.
        Contribution: Contributes a deterministic transformation that supports end-to-end reasoning reproducibility.
        """

        p = str(path)
        self._outputs.append((label, p))
        self._surface_payload.setdefault("outputs", []).append({"label": str(label), "path": p})
        self._lines.append(f"- Output: {label} -> {p}")
        self._flush()
        self._append_surface_moment(
            title=f"Declared output: {label}",
            details=f"path={p}",
            focus=str(label).strip(),
            significance=self._surface_significance_for_kind("artifact_emitted"),
            kind="artifact_emitted",
            tags=["output", label],
        )

    def add_kv(self, key: str, value: Any) -> None:
        """
        Relevance: Operates within the shared utilities layer.
        Concept: Primary callable implementing a stage-level behavior.
        Contribution: Contributes a deterministic transformation that supports end-to-end reasoning reproducibility.
        """

        self._kv[str(key)] = value
        self._surface_payload.setdefault("context", {})[str(key)] = value
        self._lines.append(f"- {key}: {value}")
        self._flush_all()

    def finalize(self, status: str, summary: str | None = None) -> Path:
        """
        Relevance: Operates within the shared utilities layer.
        Concept: Primary callable implementing a stage-level behavior.
        Contribution: Contributes a deterministic transformation that supports end-to-end reasoning reproducibility.
        """

        ended = dt.datetime.now(dt.UTC)
        duration = (ended - self._started).total_seconds()

        self._lines.append("")
        self._lines.append("## Run Result")
        self._lines.append("")
        self._lines.append(f"- Status: {status}")
        self._lines.append(f"- Ended (UTC): {ended.isoformat()}")
        self._lines.append(f"- Duration (s): {duration:.3f}")

        if summary:
            self._lines.append(f"- Summary: {summary}")

        if self._outputs:
            self._lines.append("")
            self._lines.append("## Declared Outputs")
            self._lines.append("")
            for label, p in self._outputs:
                self._lines.append(f"- {label}: {p}")

        self._surface_payload["status"] = str(status).strip() or "unknown"
        self._surface_payload["ended_utc"] = ended.isoformat()
        self._surface_payload["duration_s"] = round(duration, 3)
        self._surface_payload["summary"] = str(summary or "").strip()
        self._append_surface_moment(
            title="Run finalized",
            details=f"status={status}\nsummary={summary or ''}",
            focus=self.agent_name,
            significance=self._surface_significance_for_kind("run_result"),
            kind="run_result",
            tags=["run-result", status],
        )

        self._flush_all()
        return self.log_path
