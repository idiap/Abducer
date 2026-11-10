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

"""Execute active routed discovery branches as persistent local search runs."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import sys
from pathlib import Path
from typing import Any

_COMMON_DIR = Path(__file__).resolve().parents[3] / "common"
_GOVERNOR_SCRIPT_DIR = Path(__file__).resolve().parents[3] / "evaluation" / "kb-discovery-governor" / "scripts"
_REPO_ROOT = Path(__file__).resolve().parents[4]
for _path in (_REPO_ROOT, _COMMON_DIR, _GOVERNOR_SCRIPT_DIR):
    if str(_path) not in sys.path:
        sys.path.insert(0, str(_path))

from agentic.discovery.contracts import ContractError
from agentic.discovery.contracts import canonical_digest
from discovery_branch_queue import discovery_branch_paths
from discovery_branch_queue import load_discovery_branch_state
from discovery_branch_queue import record_discovery_branch_execution
from discovery_branch_queue import save_discovery_branch_state
from discovery_branch_queue import select_discovery_branches
from discovery_calculus import RouteSignature
from generate_discovery_governor_report import apply_governor_to_branch_state
from generate_discovery_governor_report import discovery_governor_paths
from generate_discovery_governor_report import load_discovery_governor_report
from kb_context import canonical_artifacts_dir
from kb_context import kb_ref_from_artifacts_dir
from lean_discovery import run_lean_search
from mathematical_layers import build_mathematical_layers
from problem_mathlib import load_mathlib_index
from problem_mathlib import mathlib_paths
from problem_mathlib import search_mathlib
from proof_queue import load_proof_queue
from proof_queue import proof_queue_paths
from reasoning_log import ReasoningLogger


def _utc_now() -> str:
    """Return a UTC timestamp suitable for execution metadata."""

    return dt.datetime.now(dt.UTC).isoformat()


def _clean_text(value: Any) -> str:
    """Normalize free-form values into a single stable line."""

    return " ".join(str(value or "").strip().split())


def _ensure_dict(value: Any) -> dict[str, Any]:
    """Coerce arbitrary payloads into dictionary form."""

    return value if isinstance(value, dict) else {}


def _ensure_list(value: Any) -> list[Any]:
    """Coerce arbitrary payloads into list form."""

    return value if isinstance(value, list) else []


def discovery_execution_paths(artifacts_dir: Path) -> tuple[Path, Path]:
    """Return the canonical index paths for branch-execution artifacts."""

    root = artifacts_dir / "discovery-branch-executions"
    return root / "index.json", root / "index.md"


def _execution_root(artifacts_dir: Path) -> Path:
    """Return the directory that stores one artifact pair per branch execution."""

    return artifacts_dir / "discovery-branch-executions"


def _next_execution_id(execution_root: Path, *, kb_ref: str) -> str:
    """Allocate the next stable execution identifier for a problem-scoped branch run."""

    prefix = f"discexec.{_clean_text(kb_ref)}."
    current = 0
    if execution_root.exists():
        for path in execution_root.glob("*.json"):
            if path.stem == "index":
                continue
            name = path.stem
            if not name.startswith(prefix):
                continue
            suffix = name[len(prefix) :]
            if suffix.isdigit():
                current = max(current, int(suffix))
    return f"{prefix}{current + 1:03d}"


def _load_json(path: Path) -> dict[str, Any]:
    """Load a JSON object from disk, defaulting to an empty mapping when absent."""

    if not path.exists():
        return {}
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}
    return payload if isinstance(payload, dict) else {}


def _load_execution_index(path: Path, *, kb_ref: str) -> dict[str, Any]:
    """Load or initialize the persistent execution index for discovery branches."""

    payload = _load_json(path)
    if not payload:
        now = _utc_now()
        return {
            "metadata": {
                "kb_ref": _clean_text(kb_ref),
                "generated_utc": now,
                "updated_utc": now,
                "execution_count": 0,
                "last_run_execution_count": 0,
                "last_run_lean_route_count": 0,
                "last_run_lean_candidate_count": 0,
                "last_run_lean_build_success_count": 0,
            },
            "executions": [],
        }
    payload.setdefault("metadata", {})
    payload.setdefault("executions", [])
    if not isinstance(payload["metadata"], dict):
        payload["metadata"] = {}
    if not isinstance(payload["executions"], list):
        payload["executions"] = []
    payload["metadata"]["kb_ref"] = _clean_text(payload["metadata"].get("kb_ref") or kb_ref)
    payload["metadata"].setdefault("last_run_execution_count", 0)
    payload["metadata"].setdefault("last_run_lean_route_count", 0)
    payload["metadata"].setdefault("last_run_lean_candidate_count", 0)
    payload["metadata"].setdefault("last_run_lean_build_success_count", 0)
    return payload


def _normalize_completed_local_passes(branch_state: dict[str, Any]) -> None:
    """Collapse already-executed in-progress branches into completed state before selecting new work."""

    for row in _ensure_list(branch_state.get("branches")):
        if not isinstance(row, dict):
            continue
        status = _clean_text(row.get("status")).lower()
        if status == "in_progress" and _clean_text(row.get("last_execution_id")):
            row["status"] = "completed"


def _activate_pending_branches(branch_state: dict[str, Any], *, limit: int) -> list[dict[str, Any]]:
    """Promote the next pending routed layers when no explicit active frontier remains."""

    rows = select_discovery_branches(branch_state, statuses={"pending"}, limit=limit)
    for row in rows:
        row["status"] = "active"
        row["activation_reason"] = _clean_text(row.get("activation_reason")) or (
            "Promoted from pending after the previous active discovery round completed."
        )
        row["updated_utc"] = _utc_now()
    return rows


def _save_execution_index(index: dict[str, Any], *, json_path: Path, md_path: Path) -> None:
    """Persist the execution index in machine-readable and narrative form."""

    meta = _ensure_dict(index.get("metadata"))
    executions = [row for row in _ensure_list(index.get("executions")) if isinstance(row, dict)]
    meta["updated_utc"] = _utc_now()
    meta["execution_count"] = len(executions)
    index["metadata"] = meta
    json_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.write_text(json.dumps(index, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    md_path.write_text(render_execution_index_markdown(index), encoding="utf-8")


def render_execution_index_markdown(index: dict[str, Any]) -> str:
    """Render a compact summary of executed discovery branches."""

    meta = _ensure_dict(index.get("metadata"))
    executions = [row for row in _ensure_list(index.get("executions")) if isinstance(row, dict)]
    lines = [
        "# Discovery Branch Executions",
        "",
        f"- KB ref: {meta.get('kb_ref', '')}",
        f"- Updated (UTC): {meta.get('updated_utc', '')}",
        f"- Executions: {meta.get('execution_count', 0)}",
        f"- Latest run executions: {meta.get('last_run_execution_count', 0)}",
        f"- Lean routes evaluated: {meta.get('lean_route_count', 0)}",
        f"- Lean theorem candidates: {meta.get('lean_candidate_count', 0)}",
        f"- Lean build successes: {meta.get('lean_build_success_count', 0)}",
        f"- Latest run Lean routes: {meta.get('last_run_lean_route_count', 0)}",
        f"- Latest run Lean theorem candidates: {meta.get('last_run_lean_candidate_count', 0)}",
        f"- Latest run Lean build successes: {meta.get('last_run_lean_build_success_count', 0)}",
        "",
        "| Pass ID | Branch | Status | Delta | Priority | Linked queue items | Report |",
        "|---|---|---|---|---:|---:|---|",
    ]
    for row in executions:
        lines.append(
            "| "
            f"{row.get('execution_id', '')} | {row.get('branch_id', '')} | {row.get('status', '')} | "
            f"{row.get('state_delta_kind', '')} | {float(row.get('routing_priority', 0.0) or 0.0):.3f} | {int(row.get('linked_queue_count', 0) or 0)} | {row.get('artifact_md', '')} |"
        )
    if not executions:
        lines.append("| - | - | - | - | - | - | - |")
    lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def _queue_entry_index(queue: dict[str, Any]) -> dict[str, dict[str, Any]]:
    """Index proof-queue rows by queue identifier for branch-local lookup."""

    return {
        _clean_text(row.get("queue_id")): row
        for row in _ensure_list(queue.get("entries"))
        if isinstance(row, dict) and _clean_text(row.get("queue_id"))
    }


def _search_terms(branch: dict[str, Any]) -> list[str]:
    """Build local InformalMathLib search terms from the branch target and obstruction vocabulary."""

    terms: list[str] = []
    for value in [
        branch.get("target_label"),
        *_ensure_list(branch.get("linked_breakthrough_families")),
        *_ensure_list(branch.get("linked_obstruction_classes")),
    ]:
        text = _clean_text(value)
        if text and text not in terms:
            terms.append(text)
    return terms[:8]


def _top_queue_rows(branch: dict[str, Any], queue_index: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    """Return the linked queue rows for one branch ordered by local proof pressure."""

    rows = [
        queue_index[queue_id]
        for queue_id in _ensure_list(branch.get("linked_queue_ids"))
        if queue_id in queue_index
    ]
    rows.sort(key=lambda row: float(row.get("priority", 0.0) or 0.0), reverse=True)
    return rows


def _candidate_claims(branch: dict[str, Any], queue_rows: list[dict[str, Any]]) -> list[str]:
    """Synthesize theorem-shaped next claims from the routed branch target and linked queue rows."""

    minimal_shape = _clean_text(branch.get("minimal_theorem_shape"))
    required_move = _clean_text(branch.get("required_move"))
    claims: list[str] = []
    if minimal_shape:
        claims.append(minimal_shape)
    for row in queue_rows[:2]:
        bridge_id = _clean_text(row.get("bridge_id"))
        target = _clean_text(row.get("target_statement_id"))
        route_lemma = _clean_text(row.get("missing_route_lemma"))
        candidate_object = _clean_text(row.get("candidate_object"))
        if route_lemma:
            claims.append(
                _clean_text(
                    f"For {bridge_id} toward {target}, isolate the executable discovery claim `{route_lemma}`"
                    f" through the branch focus `{_clean_text(branch.get('target_id'))}`."
                )
            )
        elif candidate_object:
            claims.append(
                _clean_text(
                    f"For {bridge_id} toward {target}, make `{candidate_object}` explicit enough to support the move:"
                    f" {required_move or minimal_shape}."
                )
            )
    deduped: list[str] = []
    for claim in claims:
        if claim and claim not in deduped:
            deduped.append(claim)
    return deduped[:4]


def _is_schematic_statement(text: str) -> bool:
    """Detect theorem statements that still depend on generic placeholders rather than local content."""

    normalized = _clean_text(text).lower()
    if not normalized:
        return True
    schematic_tokens = {
        "source theorem s",
        "target theorem t",
        "regime r",
        "carrier c",
        "invariant i",
        "object d",
        "if source theorem",
        "if target theorem",
    }
    return any(token in normalized for token in schematic_tokens)


def _is_generic_candidate_object(text: Any) -> bool:
    normalized = _clean_text(text).lower()
    if not normalized:
        return True
    generic_markers = {
        "candidate bridge object",
        "bridge object",
        "candidate object",
        "object",
        "carrier",
        "map",
        "family",
        "unspecified witness family",
    }
    return normalized in generic_markers or "unspecified" in normalized or "placeholder" in normalized


def _candidate_mode(branch: dict[str, Any], candidate: dict[str, Any]) -> str:
    search_shape = _clean_text(candidate.get("search_shape")).lower()
    target_id = _clean_text(branch.get("target_id")).lower()
    if search_shape == "transport" or target_id == "transport":
        return "transport-lemma"
    if search_shape == "equivalence" or target_id in {"equivalence-coherence-reframing", "alignment", "semantic-bridge"}:
        return "equivalence-theorem"
    if search_shape == "obstruction" or target_id == "barrier-aware-transfer":
        return "no-go-theorem"
    if target_id == "regime-localization":
        return "threshold-version"
    return "special-case"


def _candidate_layers(candidate: dict[str, Any], branch: dict[str, Any], queue_row: dict[str, Any]) -> dict[str, Any]:
    existing = _ensure_dict(candidate.get("mathematical_layers"))
    if existing.get("latex") and existing.get("lean_style"):
        return existing
    mode = _candidate_mode(branch, candidate)
    layers = build_mathematical_layers(
        title=_clean_text(candidate.get("title")),
        exact_statement=_clean_text(candidate.get("statement")),
        route_synopsis=_clean_text(candidate.get("route_synopsis"))
        or _clean_text(queue_row.get("route_synopsis"))
        or _clean_text(branch.get("required_move")),
        bridge_name=_clean_text(candidate.get("candidate_object")) or _clean_text(queue_row.get("candidate_object")),
        invariant=_clean_text(candidate.get("invariant")) or _clean_text(queue_row.get("preserved_invariant")),
        mode=mode,
        source_statement_id=_clean_text(queue_row.get("source_statement_id")),
        target_statement_id=_clean_text(queue_row.get("target_statement_id")),
        source_excerpt=_clean_text(queue_row.get("source_excerpt")),
        target_excerpt=_clean_text(queue_row.get("target_excerpt")),
        admissibility_conditions=[
            _clean_text(candidate.get("motivation")) or _clean_text(branch.get("required_move")) or "The bridge object is explicit in the current route."
        ],
        first_nontrivial_lemma_title=_clean_text(candidate.get("title")),
        first_nontrivial_lemma_statement=(
            _ensure_list(candidate.get("obligations")) or [_clean_text(branch.get("required_move"))]
        )[0],
        negative_barrier_version=_clean_text(branch.get("negative_outputs")[0] if _ensure_list(branch.get("negative_outputs")) else ""),
    )
    candidate["mathematical_layers"] = layers
    return layers


def _source_regime(row: dict[str, Any]) -> str:
    delta = _ensure_dict(row.get("statement_delta"))
    return _clean_text(delta.get("source_model")) or _clean_text(row.get("source_regime")) or "route-side-regime"


def _target_regime(row: dict[str, Any]) -> str:
    delta = _ensure_dict(row.get("statement_delta"))
    return _clean_text(delta.get("target_model")) or _clean_text(row.get("target_regime")) or "target-side-regime"


def _equivalence_pressure(branch: dict[str, Any]) -> bool:
    target_id = _clean_text(branch.get("target_id")).lower()
    lens = _ensure_dict(branch.get("lens_artifacts"))
    return target_id in {"equivalence-coherence-reframing", "alignment", "semantic-bridge"} or bool(
        _ensure_list(lens.get("equivalence_claims")) or _ensure_list(lens.get("coherence_failures"))
    )


def _factorization_pressure(branch: dict[str, Any]) -> bool:
    target_id = _clean_text(branch.get("target_id")).lower()
    lens = _ensure_dict(branch.get("lens_artifacts"))
    return target_id in {"categorical-reframing", "route-decomposition", "hybridization-of-partial-bridges"} or bool(
        _ensure_list(lens.get("diagram_candidates"))
        or _ensure_list(lens.get("commutativity_obligations"))
        or _ensure_list(lens.get("universal_property_candidates"))
    )


def _route_signature_rows(branch: dict[str, Any], queue_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in queue_rows[:3]:
        candidate_object = _clean_text(row.get("candidate_object"))
        route = RouteSignature(
            source_statement_id=_clean_text(row.get("source_statement_id")),
            target_statement_id=_clean_text(row.get("target_statement_id")),
            source_regime=_source_regime(row),
            target_regime=_target_regime(row),
            invariant=_clean_text(row.get("preserved_invariant")),
            candidate_object=candidate_object,
            branch_family=_clean_text(branch.get("target_id")) or _clean_text(branch.get("target_label")),
            source_excerpt=_clean_text(row.get("source_excerpt")),
            target_excerpt=_clean_text(row.get("target_excerpt")),
            multiple_operationalizations=bool(_equivalence_pressure(branch)),
            equivalence_pressure=bool(_equivalence_pressure(branch)),
            factorization_pressure=bool(_factorization_pressure(branch)),
            negative_pressure=bool(
                _clean_text(row.get("negative_route"))
                or _ensure_list(branch.get("linked_obstruction_classes"))
                or _ensure_list(branch.get("negative_outputs"))
            ),
            under_typed_carrier=_is_generic_candidate_object(candidate_object),
            barrier_scope=_clean_text(row.get("barrier_scope"))
            or ", ".join(_ensure_list(branch.get("linked_obstruction_classes"))[:2]),
        )
        rows.append(
            {
                "queue_id": _clean_text(row.get("queue_id")),
                "bridge_id": _clean_text(row.get("bridge_id")),
                "route": route,
                "queue_row": row,
            }
        )
    return rows


def _merge_theorem_candidates(*candidates: dict[str, Any]) -> list[dict[str, Any]]:
    merged: list[dict[str, Any]] = []
    seen: set[tuple[str, str]] = set()
    for candidate in candidates:
        title = _clean_text(candidate.get("title"))
        statement = _clean_text(candidate.get("statement"))
        key = (title, statement)
        if not title and not statement:
            continue
        if key in seen:
            continue
        seen.add(key)
        merged.append(candidate)
    return merged


def _lean_symbolic_search(
    *,
    repo_root: Path,
    kb_ref: str,
    execution_id: str,
    branch: dict[str, Any],
    queue_rows: list[dict[str, Any]],
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    route_rows = _route_signature_rows(branch, queue_rows)
    if not route_rows:
        return (
            {
                "engine": "lean-via-lake",
                "available": False,
                "reason": "No typed queue rows were available for Lean-backed symbolic search.",
                "routes": [],
                "candidates": [],
            },
            [],
        )

    search = run_lean_search(
        repo_root,
        kb_ref=kb_ref,
        execution_id=execution_id,
        routes=route_rows,
        max_candidates_per_route=4,
    )
    queue_index = {row["queue_id"]: row for row in route_rows}
    candidates: list[dict[str, Any]] = []
    for row in _ensure_list(search.get("candidates")):
        if not isinstance(row, dict):
            continue
        queue_id = _clean_text(row.get("queue_id"))
        route_row = queue_index.get(queue_id)
        if route_row is None:
            continue
        candidate_payload = _ensure_dict(row.get("candidate"))
        theorem_candidate = {
            "title": _clean_text(candidate_payload.get("title")),
            "statement": _clean_text(candidate_payload.get("theorem_statement")),
            "motivation": _clean_text(candidate_payload.get("rationale")),
            "candidate_object": _clean_text(route_row["route"].candidate_object),
            "invariant": _clean_text(route_row["route"].invariant),
            "linked_queue_ids": [queue_id],
            "linked_bridge_id": _clean_text(route_row.get("bridge_id")),
            "concretization_status": "concrete",
            "concretization_score": max(4, int(round(float(candidate_payload.get("search_score", 0.0) or 0.0) * 5))),
            "origin": "lean-bounded-search",
            "search_shape": _clean_text(candidate_payload.get("shape")),
            "search_score": float(candidate_payload.get("search_score", 0.0) or 0.0),
            "obligations": _ensure_list(candidate_payload.get("obligations")),
            "pdl_operations": _ensure_list(candidate_payload.get("pdl_operations")),
            "rationale": _clean_text(candidate_payload.get("rationale")),
            "route_synopsis": _clean_text(route_row["queue_row"].get("route_synopsis")),
            "mathematical_layers": _ensure_dict(candidate_payload.get("mathematical_layers")),
        }
        candidates.append(theorem_candidate)
    return search, candidates


def _theorem_candidates(branch: dict[str, Any], queue_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Materialize branch outputs as theorem candidates suitable for prove promotion."""

    target_id = _clean_text(branch.get("target_id")).lower()
    lens_artifacts = _ensure_dict(branch.get("lens_artifacts"))
    candidates: list[dict[str, Any]] = []
    for row in queue_rows[:3]:
        source_excerpt = _clean_text(row.get("source_excerpt"))
        target_excerpt = _clean_text(row.get("target_excerpt"))
        candidate_object = _clean_text(row.get("candidate_object")) or "candidate bridge object"
        invariant = _clean_text(row.get("preserved_invariant")) or "route invariant"
        route_lemma = _clean_text(row.get("missing_route_lemma")) or _clean_text(branch.get("required_move"))
        if not source_excerpt or not target_excerpt or not candidate_object:
            continue
        if target_id == "categorical-reframing":
            statement = _clean_text(
                f"There exists a mediating object built from `{candidate_object}` such that the route from `{source_excerpt}` to `{target_excerpt}` factors through typed morphisms preserving `{invariant}` and making the relevant square commute."
            )
            title = _clean_text(f"Commutative factorization theorem for {candidate_object}")
        elif target_id == "equivalence-coherence-reframing":
            statement = _clean_text(
                f"There exists an equivalence witness identifying `{candidate_object}` with the target-side object class relevant to `{target_excerpt}`, and `{invariant}` transports coherently along that witness."
            )
            title = _clean_text(f"Equivalence and coherent transport theorem for {candidate_object}")
        else:
            statement = _clean_text(
                f"There exists an admissible `{candidate_object}` such that `{source_excerpt}` can be organized into a route preserving `{invariant}` and thereby supports `{target_excerpt}`."
            )
            title = _clean_text(route_lemma or f"{branch.get('target_label', '')} theorem for {candidate_object}")
        if _is_schematic_statement(statement):
            continue
        concreteness_score = sum(
            1
            for value in [source_excerpt, target_excerpt, candidate_object, invariant, title]
            if _clean_text(value)
        )
        candidates.append(
            {
                "title": title,
                "statement": statement,
                "motivation": _clean_text(branch.get("required_move")) or route_lemma,
                "candidate_object": candidate_object,
                "invariant": invariant,
                "linked_queue_ids": [_clean_text(row.get("queue_id"))],
                "linked_bridge_id": _clean_text(row.get("bridge_id")),
                "concretization_status": "concrete" if concreteness_score >= 4 else "partial",
                "concretization_score": concreteness_score,
                "lens_evidence": {
                    "diagram_candidates": len(_ensure_list(lens_artifacts.get("diagram_candidates"))),
                    "equivalence_claims": len(_ensure_list(lens_artifacts.get("equivalence_claims"))),
                },
                "origin": "heuristic-lens",
            }
        )
        _candidate_layers(candidates[-1], branch, row)
    return candidates


def _concept_revisions(branch: dict[str, Any], queue_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Emit concept revisions when the branch changes discovery framing but not yet the prove frontier."""

    target_id = _clean_text(branch.get("target_id")).lower()
    queue_ids = [_clean_text(row.get("queue_id")) for row in queue_rows if _clean_text(row.get("queue_id"))]
    if target_id == "categorical-reframing":
        return [
            {
                "label": "route-as-commutative-diagram",
                "revision": "Reinterpret the blocked route as a commutative-square and factorization problem instead of a single missing bridge lemma.",
                "epistemic_gain": "Turns a vague bridge request into explicit morphism, mediation, and non-commutation obligations.",
                "linked_queue_ids": queue_ids,
            }
        ]
    if target_id == "equivalence-coherence-reframing":
        return [
            {
                "label": "route-as-equivalence-problem",
                "revision": "Treat the live operationalizations as a candidate equivalence/coherence problem instead of assuming they are interchangeable.",
                "epistemic_gain": "Separates identity, equivalence, and transport obligations and exposes coherence failures directly.",
                "linked_queue_ids": queue_ids,
            }
        ]
    if target_id in {"invariant-discovery", "regime-localization", "problem-representation-shift", "route-decomposition", "hybridization-of-partial-bridges"}:
        return [
            {
                "label": target_id,
                "revision": _clean_text(branch.get("required_move")),
                "epistemic_gain": _clean_text(branch.get("rationale")) or "Refines the discovery programme before prove resumes.",
                "linked_queue_ids": queue_ids,
            }
        ]
    return []


def _mathematical_packet_contract(branch: dict[str, Any]) -> dict[str, Any]:
    """Describe the native theorem packet that prompt-led discovery branches should emit."""

    return {
        "required": True,
        "applies_when": "the branch emits a theorem-sized claim, theorem candidate, or route-local lemma",
        "representation_kind": "informal-latex-lean-style",
        "required_layers": ["informal", "latex", "lean_style"],
        "required_fields": [
            "quantifier_signature",
            "object_signature",
            "symbol_ledger",
            "latex.theorem_statement",
            "lean_style.scaffold",
        ],
        "lean_style_status": "non-executable-scaffold-unless-explicitly-formalized",
        "notation_rule": (
            "Do not use equivalence, transport, coherence, factorization, or commutativity language without naming "
            "the carrier, witness/map, invariant-preservation law, and theorem type in notation."
        ),
        "branch_target": _clean_text(branch.get("target_label")) or _clean_text(branch.get("target_id")),
    }


def _state_delta(branch: dict[str, Any], theorem_candidates: list[dict[str, Any]], concept_revisions: list[dict[str, Any]]) -> dict[str, Any]:
    """Classify whether a branch pass produced a concrete state delta or only analysis."""

    promotable_theorems = [
        row for row in theorem_candidates if _clean_text(row.get("concretization_status")) == "concrete"
    ]
    delta_kind = "analysis-only"
    if promotable_theorems:
        delta_kind = "theorem-candidate"
    elif concept_revisions:
        delta_kind = "concept-revision"
    return {
        "delta_kind": delta_kind,
        "has_state_delta": bool(promotable_theorems or concept_revisions),
        "promotable_theorem_count": len(promotable_theorems),
        "concept_revision_count": len(concept_revisions),
        "max_concretization_score": max(
            (int(row.get("concretization_score", 0) or 0) for row in theorem_candidates),
            default=0,
        ),
        "summary": (
            "This branch pass emitted at least one concrete theorem candidate ready for prove promotion."
            if promotable_theorems
            else "This branch pass changed the conceptual framing but did not yet emit a prove-ready theorem candidate."
            if concept_revisions
            else "This branch pass remained analytic and did not yet change the discovery state."
        ),
    }


def _branch_summary(branch: dict[str, Any], queue_rows: list[dict[str, Any]]) -> str:
    """Produce the branch-level execution summary that records what this run is trying to change."""

    target_label = _clean_text(branch.get("target_label"))
    linked = len(queue_rows)
    required_move = _clean_text(branch.get("required_move"))
    obstruction_text = ", ".join(_ensure_list(branch.get("linked_obstruction_classes"))[:3])
    return _clean_text(
        f"Executed discovery branch `{_clean_text(branch.get('branch_id'))}` for `{target_label}` over {linked} linked blocked queue items."
        f" The run keeps the search on `{required_move}`"
        f" and uses obstruction classes `{obstruction_text or 'current blocked frontier'}` as the local pressure map."
    )


def build_branch_execution_report(
    *,
    repo_root: Path,
    execution_id: str,
    kb_ref: str,
    branch: dict[str, Any],
    queue_rows: list[dict[str, Any]],
    mathlib_hits: list[dict[str, Any]],
) -> dict[str, Any]:
    """Build the persistent report for one executed discovery branch."""

    summary = _branch_summary(branch, queue_rows)
    heuristic_candidates = _theorem_candidates(branch, queue_rows)
    lean_search, lean_candidates = _lean_symbolic_search(
        repo_root=repo_root,
        kb_ref=kb_ref,
        execution_id=execution_id,
        branch=branch,
        queue_rows=queue_rows,
    )
    theorem_candidates = _merge_theorem_candidates(*heuristic_candidates, *lean_candidates)
    concept_revisions = _concept_revisions(branch, queue_rows)
    state_delta = _state_delta(branch, theorem_candidates, concept_revisions)
    status = "completed-state-delta" if bool(state_delta.get("has_state_delta")) else "completed-analysis-pass"
    return {
        "metadata": {
            "execution_id": execution_id,
            "kb_ref": _clean_text(kb_ref),
            "generated_utc": _utc_now(),
            "branch_id": _clean_text(branch.get("branch_id")),
            "status": status,
        },
        "branch": {
            "branch_id": _clean_text(branch.get("branch_id")),
            "status_before_execution": _clean_text(branch.get("status")),
            "layer_kind": _clean_text(branch.get("layer_kind")),
            "epistemic_lens": _clean_text(branch.get("epistemic_lens")),
            "target_id": _clean_text(branch.get("target_id")),
            "target_label": _clean_text(branch.get("target_label")),
            "routing_priority": float(branch.get("routing_priority", 0.0) or 0.0),
            "dispatch_rank": int(branch.get("dispatch_rank", 0) or 0),
            "dispatch_round": int(branch.get("dispatch_round", 0) or 0),
            "required_move": _clean_text(branch.get("required_move")),
            "abstraction_required": _clean_text(branch.get("abstraction_required")),
            "minimal_theorem_shape": _clean_text(branch.get("minimal_theorem_shape")),
            "spawn_reason": _clean_text(branch.get("spawn_reason")),
            "rationale": _clean_text(branch.get("rationale")),
        },
        "local_frontier": {
            "linked_queue_count": len(queue_rows),
            "linked_queue_items": [
                {
                    "queue_id": _clean_text(row.get("queue_id")),
                    "bridge_id": _clean_text(row.get("bridge_id")),
                    "priority": float(row.get("priority", 0.0) or 0.0),
                    "title": _clean_text(row.get("title")),
                    "claim_type": _clean_text(row.get("claim_type")),
                    "conjecture_statement": _clean_text(row.get("conjecture_statement")),
                    "candidate_object": _clean_text(row.get("candidate_object")),
                    "preserved_invariant": _clean_text(row.get("preserved_invariant")),
                    "missing_route_lemma": _clean_text(row.get("missing_route_lemma")),
                }
                for row in queue_rows[:6]
            ],
            "mathlib_hits": [
                {
                    "result_id": _clean_text(row.get("result_id")),
                    "title": _clean_text(row.get("title")),
                    "outcome": _clean_text(row.get("outcome")),
                    "summary": _clean_text(row.get("summary")),
                    "artifact_path": _clean_text(row.get("artifact_path")),
                }
                for row in mathlib_hits
            ],
        },
        "execution": {
            "summary": summary,
            "candidate_claims": _candidate_claims(branch, queue_rows),
            "theorem_candidates": theorem_candidates,
            "concept_revisions": concept_revisions,
            "lean_symbolic_search": lean_search,
            "mathematical_packet_contract": _mathematical_packet_contract(branch),
            "state_delta": state_delta,
            "required_questions": [
                _clean_text(value)
                for value in _ensure_list(branch.get("required_questions"))
                if _clean_text(value)
            ],
            "expected_deliverables": [
                _clean_text(value)
                for value in _ensure_list(branch.get("expected_deliverables"))
                if _clean_text(value)
            ],
            "stop_criteria": [
                _clean_text(value)
                for value in _ensure_list(branch.get("stop_criteria"))
                if _clean_text(value)
            ],
            "search_modes": [
                _clean_text(value)
                for value in _ensure_list(branch.get("search_modes"))
                if _clean_text(value)
            ],
            "anti_patterns": [
                _clean_text(value)
                for value in _ensure_list(branch.get("anti_patterns"))
                if _clean_text(value)
            ],
            "routing_heuristic": _ensure_dict(branch.get("routing_heuristic")),
            "lens_artifacts": _ensure_dict(branch.get("lens_artifacts")),
            "negative_outputs": [
                _clean_text(value)
                for value in _ensure_list(branch.get("negative_outputs"))
                if _clean_text(value)
            ],
            "sample_theorem_targets": [
                _clean_text(value)
                for value in _ensure_list(branch.get("sample_theorem_targets"))
                if _clean_text(value)
            ],
            "external_framework_search": _ensure_dict(branch.get("external_framework_search")),
        },
    }


def render_branch_execution_markdown(report: dict[str, Any]) -> str:
    """Render a discovery branch pass, distinguishing state-delta runs from analysis-only passes."""

    meta = _ensure_dict(report.get("metadata"))
    branch = _ensure_dict(report.get("branch"))
    frontier = _ensure_dict(report.get("local_frontier"))
    execution = _ensure_dict(report.get("execution"))
    lines = [
        f"# {'Discovery Branch State Delta' if _clean_text(meta.get('status')) == 'completed-state-delta' else 'Discovery Branch Analysis Pass'}: {meta.get('execution_id', '')}",
        "",
        f"- KB ref: {meta.get('kb_ref', '')}",
        f"- Branch: {meta.get('branch_id', '')}",
        f"- Generated (UTC): {meta.get('generated_utc', '')}",
        f"- Status: {meta.get('status', '')}",
        "",
        "## Branch",
        "",
        f"- Kind: {branch.get('layer_kind', '')}",
        f"- Epistemic lens: {branch.get('epistemic_lens', '')}",
        f"- Target: {branch.get('target_label', '')}",
        f"- Routing priority: {float(branch.get('routing_priority', 0.0) or 0.0):.3f}",
        f"- Required move: {branch.get('required_move', '')}",
        f"- Abstraction required: {branch.get('abstraction_required', '')}",
        f"- Minimal theorem shape: {branch.get('minimal_theorem_shape', '')}",
        f"- Spawn reason: {branch.get('spawn_reason', '')}",
        f"- Rationale: {branch.get('rationale', '')}",
        "",
        "## Local Frontier",
        "",
        f"- Linked queue items: {int(frontier.get('linked_queue_count', 0) or 0)}",
        "",
    ]
    for row in _ensure_list(frontier.get("linked_queue_items")):
        if not isinstance(row, dict):
            continue
        lines.extend(
            [
                f"### {row.get('queue_id', '')}",
                "",
                f"- Bridge: {row.get('bridge_id', '')}",
                f"- Priority: {float(row.get('priority', 0.0) or 0.0):.3f}",
                f"- Claim type: {row.get('claim_type', '')}",
                f"- Candidate object: {row.get('candidate_object', '')}",
                f"- Invariant: {row.get('preserved_invariant', '')}",
                f"- Route lemma: {row.get('missing_route_lemma', '')}",
                f"- Conjecture: {row.get('conjecture_statement', '')}",
                "",
            ]
        )
    lines.extend(
        [
            "## Local InformalMathLib Hints",
            "",
        ]
    )
    hits = [row for row in _ensure_list(frontier.get("mathlib_hits")) if isinstance(row, dict)]
    if not hits:
        lines.append("- No local InformalMathLib hits for this branch search.")
        lines.append("")
    else:
        for row in hits:
            lines.append(
                f"- `{row.get('result_id', '')}` | {row.get('title', '')} | {row.get('outcome', '')}"
            )
            if _clean_text(row.get("summary")):
                lines.append(f"  Summary: {row.get('summary', '')}")
            if _clean_text(row.get("artifact_path")):
                lines.append(f"  Artifact: {row.get('artifact_path', '')}")
        lines.append("")
    lines.extend(
        [
            "## Execution Summary",
            "",
            f"- {execution.get('summary', '')}",
            "",
            "## State Delta",
            "",
        ]
    )
    state_delta = _ensure_dict(execution.get("state_delta"))
    lines.extend(
        [
            f"- Kind: {state_delta.get('delta_kind', '')}",
            f"- Has state delta: {state_delta.get('has_state_delta', False)}",
            f"- Promotable theorem candidates: {state_delta.get('promotable_theorem_count', 0)}",
            f"- Concept revisions: {state_delta.get('concept_revision_count', 0)}",
            f"- Max concretization score: {state_delta.get('max_concretization_score', 0)}",
            f"- Summary: {state_delta.get('summary', '')}",
            "",
            "## Candidate Claims",
            "",
        ]
    )
    for item in _ensure_list(execution.get("candidate_claims")):
        lines.append(f"- {item}")
    lines.extend(
        [
            "",
            "## Theorem Candidates",
            "",
        ]
    )
    theorem_candidates = [row for row in _ensure_list(execution.get("theorem_candidates")) if isinstance(row, dict)]
    if not theorem_candidates:
        lines.append("- No concrete theorem candidates were emitted in this pass.")
        lines.append("")
    else:
        for row in theorem_candidates:
            native_layers = _ensure_dict(row.get("mathematical_layers"))
            latex_layer = _ensure_dict(native_layers.get("latex"))
            lean_layer = _ensure_dict(native_layers.get("lean_style"))
            lines.extend(
                [
                    f"### {row.get('title', '')}",
                    "",
                    f"- Statement: {row.get('statement', '')}",
                    f"- Candidate object: {row.get('candidate_object', '')}",
                    f"- Invariant: {row.get('invariant', '')}",
                    f"- Origin: {row.get('origin', '')}",
                    f"- Search shape: {row.get('search_shape', '')}",
                    f"- Concretization: {row.get('concretization_status', '')} ({row.get('concretization_score', 0)})",
                    f"- Motivation: {row.get('motivation', '')}",
                    "",
                ]
            )
            if native_layers:
                lines.extend(
                    [
                        f"- Quantifier signature: {native_layers.get('quantifier_signature', '')}",
                        f"- LaTeX theorem: {latex_layer.get('theorem_statement', '')}",
                        f"- Lean-style scaffold: {lean_layer.get('theorem_name', '')}",
                        "",
                    ]
                )
    lines.extend(
        [
            "## Lean Search",
            "",
        ]
    )
    lean_search = _ensure_dict(execution.get("lean_symbolic_search"))
    if not lean_search:
        lines.append("- No Lean-backed symbolic search was recorded for this branch execution.")
        lines.append("")
    else:
        lines.extend(
            [
                f"- Engine: {lean_search.get('engine', '')}",
                f"- Available: {lean_search.get('available', False)}",
                f"- Build ok: {lean_search.get('build_ok', False)}",
                f"- Module: {lean_search.get('module_name', '')}",
                f"- Module path: {lean_search.get('module_path', '')}",
                f"- Stdout: {lean_search.get('stdout_excerpt', '')}",
                f"- Stderr: {lean_search.get('stderr_excerpt', '')}",
                "",
            ]
        )
        for row in _ensure_list(lean_search.get("routes")):
            if not isinstance(row, dict):
                continue
            lines.extend(
                [
                    f"- Queue {row.get('queue_id', '')}: readiness={_ensure_dict(row.get('readiness')).get('mode', '')} "
                    f"(score={row.get('lean_readiness_score', row.get('readiness', {}).get('score', 0))}) "
                    f"| shapes={', '.join(_ensure_list(row.get('search_shapes')))} "
                    f"| candidates={row.get('candidate_count', 0)}",
                ]
            )
        lines.append("")
    lines.extend(
        [
            "## Concept Revisions",
            "",
        ]
    )
    concept_revisions = [row for row in _ensure_list(execution.get("concept_revisions")) if isinstance(row, dict)]
    if not concept_revisions:
        lines.append("- No concept revisions were emitted in this pass.")
        lines.append("")
    else:
        for row in concept_revisions:
            lines.append(f"- {row.get('label', '')}: {row.get('revision', '')}")
            lines.append(f"  Epistemic gain: {row.get('epistemic_gain', '')}")
        lines.append("")
    lines.extend(
        [
            "## Native Mathematical Packet Contract",
            "",
        ]
    )
    packet_contract = _ensure_dict(execution.get("mathematical_packet_contract"))
    if not packet_contract:
        lines.append("- No packet contract recorded for this branch execution.")
        lines.append("")
    else:
        lines.extend(
            [
                f"- Required: {packet_contract.get('required', False)}",
                f"- Applies when: {packet_contract.get('applies_when', '')}",
                f"- Representation kind: {packet_contract.get('representation_kind', '')}",
                f"- Required layers: {', '.join(_ensure_list(packet_contract.get('required_layers')))}",
                f"- Required fields: {', '.join(_ensure_list(packet_contract.get('required_fields')))}",
                f"- Lean-style status: {packet_contract.get('lean_style_status', '')}",
                f"- Notation rule: {packet_contract.get('notation_rule', '')}",
                "",
            ]
        )
    lines.extend(
        [
            "## Required Questions",
            "",
        ]
    )
    for item in _ensure_list(execution.get("required_questions")):
        lines.append(f"- {item}")
    lines.extend(
        [
            "",
            "## Expected Deliverables",
            "",
        ]
    )
    for item in _ensure_list(execution.get("expected_deliverables")):
        lines.append(f"- {item}")
    lines.extend(
        [
            "",
            "## Sample Theorem Targets",
            "",
        ]
    )
    for item in _ensure_list(execution.get("sample_theorem_targets")):
        lines.append(f"- {item}")
    lines.extend(
        [
            "",
            "## Lens Artifacts",
            "",
        ]
    )
    heuristic = _ensure_dict(execution.get("routing_heuristic"))
    if heuristic:
        lines.append(
            f"- Routing heuristic: recommended={heuristic.get('recommended', False)} | score={heuristic.get('score', 0)}/{heuristic.get('threshold', 0)}"
        )
        lines.append(f"- Decision rule: {heuristic.get('decision_rule', '')}")
        lines.append(f"- Rationale: {heuristic.get('rationale', '')}")
        active_criteria = [
            _clean_text(row.get("detail"))
            for row in _ensure_list(heuristic.get("criteria"))
            if isinstance(row, dict) and bool(row.get("active")) and _clean_text(row.get("detail"))
        ]
        if active_criteria:
            lines.append("- Active criteria:")
            for item in active_criteria:
                lines.append(f"  - {item}")
        active_anti_triggers = [
            _clean_text(row.get("detail"))
            for row in _ensure_list(heuristic.get("anti_triggers"))
            if isinstance(row, dict) and bool(row.get("active")) and _clean_text(row.get("detail"))
        ]
        if active_anti_triggers:
            lines.append("- Active anti-triggers:")
            for item in active_anti_triggers:
                lines.append(f"  - {item}")
    lens_artifacts = _ensure_dict(execution.get("lens_artifacts"))
    for label, field in (
        ("Diagram candidates", "diagram_candidates"),
        ("Commutativity obligations", "commutativity_obligations"),
        ("Universal property candidates", "universal_property_candidates"),
        ("Equivalence claims", "equivalence_claims"),
        ("Transport obligations", "transport_obligations"),
        ("Coherence failures", "coherence_failures"),
    ):
        values = [item for item in _ensure_list(lens_artifacts.get(field)) if _clean_text(item)]
        if not values:
            continue
        lines.append(f"- {label}:")
        for item in values:
            lines.append(f"  - {item}")
    negative_outputs = [item for item in _ensure_list(execution.get("negative_outputs")) if _clean_text(item)]
    if negative_outputs:
        lines.append("- Negative outputs:")
        for item in negative_outputs:
            lines.append(f"  - {item}")
    lines.extend(
        [
            "",
            "## Stop Criteria",
            "",
        ]
    )
    for item in _ensure_list(execution.get("stop_criteria")):
        lines.append(f"- {item}")
    lines.extend(
        [
            "",
            "## External Framework Search Gate",
            "",
        ]
    )
    gate = _ensure_dict(execution.get("external_framework_search"))
    lines.append(f"- Recommended: {bool(gate.get('recommended', False))}")
    lines.append(f"- Mode: {gate.get('mode', '')}")
    lines.append(f"- Justification: {gate.get('justification', '')}")
    if _ensure_list(gate.get("candidate_framework_regions")):
        lines.append(f"- Candidate framework regions: {', '.join(_ensure_list(gate.get('candidate_framework_regions')))}")
    if _ensure_list(gate.get("local_prerequisites")):
        lines.append("- Local prerequisites before browsing:")
        for item in _ensure_list(gate.get("local_prerequisites")):
            lines.append(f"  - {item}")
    lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def execute_active_discovery_branches(
    *,
    repo_root: Path,
    artifacts_dir: Path,
    kb_ref: str,
    limit: int,
    exact_branch_id: str = "",
    expected_branch_digest: str = "",
) -> tuple[dict[str, Any], dict[str, Any], tuple[Path, Path], list[dict[str, str]]]:
    """Run active branches, or one content-bound branch for authoritative callers.

    ``exact_branch_id`` bypasses governor reselection and pending activation so
    a verified canonical schedule cannot accidentally fan out to a different
    local branch.  Selection is by exact ID and row digest only; titles and
    hypothesis prose never participate.
    """

    branch_json, branch_md = discovery_branch_paths(artifacts_dir)
    branch_state = load_discovery_branch_state(branch_json, kb_ref=kb_ref)
    normalized_exact_branch_id = _clean_text(exact_branch_id)
    if normalized_exact_branch_id:
        matches = [
            row
            for row in _ensure_list(branch_state.get("branches"))
            if isinstance(row, dict) and _clean_text(row.get("branch_id")) == normalized_exact_branch_id
        ]
        if len(matches) != 1:
            raise ContractError(
                f"authoritative discovery selector requires exactly one local branch `{normalized_exact_branch_id}`"
            )
        exact_row = matches[0]
        status = _clean_text(exact_row.get("status")).lower()
        if status not in {"active", "pending"}:
            raise ContractError(
                f"authoritative discovery branch `{normalized_exact_branch_id}` is not executable from status `{status}`"
            )
        if not _clean_text(expected_branch_digest):
            raise ContractError("authoritative discovery selector requires an expected branch-row digest")
        if canonical_digest(exact_row) != _clean_text(expected_branch_digest):
            raise ContractError(
                f"authoritative discovery branch `{normalized_exact_branch_id}` changed after binding preflight"
            )
        active_rows = [exact_row]
    else:
        governor_json, _governor_md = discovery_governor_paths(artifacts_dir)
        governor_report = load_discovery_governor_report(governor_json, kb_ref=kb_ref)
        if _ensure_list(governor_report.get("branch_decisions")):
            apply_governor_to_branch_state(branch_state, report=governor_report, activate_top_k=max(1, limit))
        _normalize_completed_local_passes(branch_state)
        active_rows = select_discovery_branches(branch_state, statuses={"active"}, limit=limit)
        if not active_rows:
            active_rows = _activate_pending_branches(branch_state, limit=limit)

    queue_json, _ = proof_queue_paths(repo_root, kb_ref)
    queue = load_proof_queue(queue_json, kb_ref=kb_ref)
    queue_index = _queue_entry_index(queue)

    mathlib_json, _ = mathlib_paths(repo_root, kb_ref)
    mathlib = load_mathlib_index(mathlib_json, kb_ref=kb_ref)

    index_json, index_md = discovery_execution_paths(artifacts_dir)
    execution_index = _load_execution_index(index_json, kb_ref=kb_ref)
    execution_root = _execution_root(artifacts_dir)
    execution_root.mkdir(parents=True, exist_ok=True)

    outputs: list[dict[str, str]] = []
    current_lean_route_count = 0
    current_lean_candidate_count = 0
    current_lean_build_success_count = 0
    for branch in active_rows:
        execution_id = _next_execution_id(execution_root, kb_ref=kb_ref)
        queue_rows = _top_queue_rows(branch, queue_index)
        mathlib_hits = search_mathlib(mathlib, _search_terms(branch), limit=5)
        report = build_branch_execution_report(
            repo_root=repo_root,
            execution_id=execution_id,
            kb_ref=kb_ref,
            branch=branch,
            queue_rows=queue_rows,
            mathlib_hits=mathlib_hits,
        )
        json_path = execution_root / f"{execution_id}.json"
        md_path = execution_root / f"{execution_id}.md"
        json_path.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        md_path.write_text(render_branch_execution_markdown(report), encoding="utf-8")
        outputs.append({"branch_id": _clean_text(branch.get("branch_id")), "json": str(json_path), "md": str(md_path)})
        lean_search = _ensure_dict(_ensure_dict(report.get("execution")).get("lean_symbolic_search"))
        current_lean_route_count += len(_ensure_list(lean_search.get("routes")))
        current_lean_candidate_count += len(_ensure_list(lean_search.get("candidates")))
        if bool(lean_search.get("build_ok")):
            current_lean_build_success_count += 1

        execution_index.setdefault("executions", [])
        execution_index["executions"].append(
            {
                "execution_id": execution_id,
                "branch_id": _clean_text(branch.get("branch_id")),
                "status": _clean_text(_ensure_dict(report.get("metadata")).get("status")),
                "routing_priority": float(branch.get("routing_priority", 0.0) or 0.0),
                "linked_queue_count": len(queue_rows),
                "state_delta_kind": _clean_text(_ensure_dict(_ensure_dict(report.get("execution")).get("state_delta")).get("delta_kind")),
                "artifact_json": str(json_path),
                "artifact_md": str(md_path),
                "updated_utc": _utc_now(),
            }
        )
        record_discovery_branch_execution(
            branch_state,
            branch_id=_clean_text(branch.get("branch_id")),
            execution_id=execution_id,
            status="completed",
            summary=_clean_text(_ensure_dict(report.get("execution")).get("summary")),
            artifact_json=str(json_path),
            artifact_md=str(md_path),
        )

    execution_index["executions"] = sorted(
        [row for row in _ensure_list(execution_index.get("executions")) if isinstance(row, dict)],
        key=lambda row: (_clean_text(row.get("updated_utc")), _clean_text(row.get("execution_id"))),
        reverse=True,
    )
    lean_route_count = 0
    lean_candidate_count = 0
    lean_build_success_count = 0
    for row in execution_index["executions"]:
        report = _load_json(Path(_clean_text(row.get("artifact_json"))))
        lean_search = _ensure_dict(_ensure_dict(report.get("execution")).get("lean_symbolic_search"))
        lean_route_count += len(_ensure_list(lean_search.get("routes")))
        lean_candidate_count += len(_ensure_list(lean_search.get("candidates")))
        if bool(lean_search.get("build_ok")):
            lean_build_success_count += 1
    execution_index.setdefault("metadata", {})
    execution_index["metadata"]["lean_route_count"] = lean_route_count
    execution_index["metadata"]["lean_candidate_count"] = lean_candidate_count
    execution_index["metadata"]["lean_build_success_count"] = lean_build_success_count
    execution_index["metadata"]["last_run_execution_count"] = len(outputs)
    execution_index["metadata"]["last_run_lean_route_count"] = current_lean_route_count
    execution_index["metadata"]["last_run_lean_candidate_count"] = current_lean_candidate_count
    execution_index["metadata"]["last_run_lean_build_success_count"] = current_lean_build_success_count
    _save_execution_index(execution_index, json_path=index_json, md_path=index_md)
    save_discovery_branch_state(branch_state, json_path=branch_json, md_path=branch_md)
    return branch_state, execution_index, (index_json, index_md), outputs


def main() -> int:
    """Execute the currently active discovery branches for one problem."""

    parser = argparse.ArgumentParser(description="Execute active routed discovery branches.")
    parser.add_argument("--artifacts-dir", required=True, help="Path to artifacts/<kb-ref>.")
    parser.add_argument("--kb-ref", default="", help="Optional KB reference override.")
    parser.add_argument("--limit", type=int, default=4, help="Maximum number of active branches to execute.")
    args = parser.parse_args()

    artifacts_dir = Path(args.artifacts_dir).expanduser().resolve()
    repo_root = Path(__file__).resolve().parents[4]
    kb_ref = _clean_text(args.kb_ref) or kb_ref_from_artifacts_dir(artifacts_dir)
    if not kb_ref:
        raise SystemExit("Unable to determine kb_ref from artifacts directory; pass --kb-ref.")
    artifacts_dir = canonical_artifacts_dir(repo_root, kb_ref) if not artifacts_dir.exists() else artifacts_dir

    logger = ReasoningLogger("kb-discovery-branch-executor", repo_root=repo_root)
    logger.step(
        "Executing active discovery branches",
        details="\n".join(
            [
                f"kb_ref={kb_ref}",
                f"artifacts_dir={artifacts_dir}",
                f"limit={max(1, args.limit)}",
            ]
        ),
    )

    branch_state, execution_index, execution_paths, outputs = execute_active_discovery_branches(
        repo_root=repo_root,
        artifacts_dir=artifacts_dir,
        kb_ref=kb_ref,
        limit=max(1, args.limit),
    )
    logger.step(
        "Executed discovery branches",
        details="\n".join(
            [
                f"executed={len(outputs)}",
                f"branch_count={int(_ensure_dict(branch_state.get('metadata')).get('branch_count', 0) or 0)}",
                f"active_count={int(_ensure_dict(branch_state.get('metadata')).get('active_count', 0) or 0)}",
                f"execution_count={int(_ensure_dict(execution_index.get('metadata')).get('execution_count', 0) or 0)}",
            ]
        ),
    )
    logger.add_output("discovery_branch_execution_index_json", execution_paths[0])
    logger.add_output("discovery_branch_execution_index_md", execution_paths[1])
    for row in outputs:
        branch_key = _clean_text(row.get("branch_id")).replace(".", "_").replace("-", "_")
        logger.add_output(f"discovery_branch_execution_{branch_key}_md", Path(row["md"]))
    logger.finalize(
        status="success",
        summary=f"Executed {len(outputs)} active discovery branches for `{kb_ref}`.",
    )

    print(f"[OK] Wrote discovery branch execution index JSON: {execution_paths[0]}")
    print(f"[OK] Wrote discovery branch execution index Markdown: {execution_paths[1]}")
    for row in outputs:
        print(f"[OK] Wrote branch execution Markdown: {row['md']}")
    print(f"[LOG] {logger.log_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
