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

"""Compile routed discovery outputs into expert-grade theorem packages."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

_COMMON_DIR = Path(__file__).resolve().parents[3] / "common"
_PROVE_SCRIPT_DIR = Path(__file__).resolve().parents[3] / "discovery" / "kb-prove-cycle" / "scripts"
if str(_COMMON_DIR) not in sys.path:
    sys.path.insert(0, str(_COMMON_DIR))
if str(_PROVE_SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(_PROVE_SCRIPT_DIR))

from execute_discovery_branches import discovery_execution_paths
from expert_packet_fields import normalize_expert_packet_fields
from generate_proof_queue_report import compile_pdf
from kb_context import canonical_artifacts_dir
from kb_context import kb_ref_from_artifacts_dir
from mathematical_layers import build_mathematical_layers
from proof_queue import load_proof_queue
from proof_queue import proof_queue_paths
from reasoning_log import ReasoningLogger


_PLACEHOLDER_PATTERNS = (
    "source theorem s",
    "target theorem t",
    "regime r",
    "carrier c",
    "invariant i",
    "object d",
    "candidate bridge object",
    "if source theorem",
    "if target theorem",
)
_GENERIC_OBJECT_NAMES = {
    "candidate bridge object",
    "bridge object",
    "candidate object",
    "object",
    "carrier",
    "map",
    "family",
}


def _clean_text(value: Any) -> str:
    return " ".join(str(value or "").strip().split())


def _ensure_dict(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def _ensure_list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def _safe_float(value: Any, default: float = 0.0) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def _safe_int(value: Any, default: int = 0) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def _latex_escape(value: Any) -> str:
    text = _clean_text(value)
    replacements = {
        "\\": r"\textbackslash{}",
        "&": r"\&",
        "%": r"\%",
        "$": r"\$",
        "#": r"\#",
        "_": r"\_",
        "{": r"\{",
        "}": r"\}",
        "~": r"\textasciitilde{}",
        "^": r"\textasciicircum{}",
    }
    for src, dst in replacements.items():
        text = text.replace(src, dst)
    text = text.replace("->", r"$\rightarrow$ ")
    text = text.replace("`", "'")
    return text


def _load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}
    return payload if isinstance(payload, dict) else {}


def expert_conjecture_paths(artifacts_dir: Path) -> tuple[Path, Path, Path, Path]:
    return (
        artifacts_dir / "expert-conjectures.json",
        artifacts_dir / "expert-conjectures.md",
        artifacts_dir / "expert-conjectures.tex",
        artifacts_dir / "expert-conjectures.pdf",
    )


def _sanitize_id(value: Any) -> str:
    text = _clean_text(value).lower()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return re.sub(r"-{2,}", "-", text).strip("-")


def _contains_truncation(text: Any) -> bool:
    normalized = _clean_text(text).lower()
    return any(token in normalized for token in ("...", "…", "tokens truncated", "truncated"))


def _has_placeholders(text: Any) -> bool:
    normalized = _clean_text(text).lower()
    if not normalized:
        return True
    return any(token in normalized for token in _PLACEHOLDER_PATTERNS)


def _token_overlap(left: Any, right: Any) -> int:
    left_tokens = {
        token
        for token in re.findall(r"[a-z0-9]+", _clean_text(left).lower())
        if len(token) >= 4
    }
    right_tokens = {
        token
        for token in re.findall(r"[a-z0-9]+", _clean_text(right).lower())
        if len(token) >= 4
    }
    return len(left_tokens & right_tokens)


def _named_object(text: Any) -> bool:
    normalized = _clean_text(text)
    lowered = normalized.lower()
    if not normalized or lowered in _GENERIC_OBJECT_NAMES:
        return False
    if _has_placeholders(normalized):
        return False
    return len(normalized.split()) >= 2 or any(
        token in lowered
        for token in (
            "family",
            "map",
            "theorem",
            "lemma",
            "transport",
            "correspondence",
            "obstruction",
            "witness",
            "certificate",
            "gadget",
            "equivalence",
            "normal form",
            "carrier",
        )
    )


def _restricted_regime_mode(target_id: str) -> str:
    target = _sanitize_id(target_id)
    if target == "transport":
        return "transport-lemma"
    if target == "regime-localization":
        return "threshold-version"
    if target in {"alignment", "equivalence-coherence-reframing", "semantic-bridge"}:
        return "equivalence-theorem"
    if target == "barrier-aware-transfer":
        return "no-go-theorem"
    if target in {"constructive-instantiation", "realization", "invariant-discovery"}:
        return "special-case"
    return "special-case"


def _restricted_regime_title(mode: str) -> str:
    return {
        "transport-lemma": "Transport Lemma",
        "threshold-version": "Threshold Version",
        "equivalence-theorem": "Equivalence Theorem",
        "no-go-theorem": "No-Go Theorem",
        "special-case": "Special-Case Theorem",
    }.get(mode, "Restricted-Regime Theorem")


def _unique_texts(values: list[Any]) -> list[str]:
    rows: list[str] = []
    seen: set[str] = set()
    for value in values:
        text = _clean_text(value)
        if not text or text in seen:
            continue
        seen.add(text)
        rows.append(text)
    return rows


def _queue_entry_index(queue: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {
        _clean_text(row.get("queue_id")): row
        for row in _ensure_list(queue.get("entries"))
        if isinstance(row, dict) and _clean_text(row.get("queue_id"))
    }


def _execution_reports(index: dict[str, Any]) -> list[tuple[dict[str, Any], dict[str, Any]]]:
    rows = [row for row in _ensure_list(index.get("executions")) if isinstance(row, dict)]
    reports: list[tuple[dict[str, Any], dict[str, Any]]] = []
    for row in rows:
        report = _load_json(Path(_clean_text(row.get("artifact_json"))))
        if report:
            reports.append((row, report))
    return reports


def _linked_queue_rows(
    *,
    report: dict[str, Any],
    queue_index: dict[str, dict[str, Any]],
) -> list[dict[str, Any]]:
    branch = _ensure_dict(report.get("branch"))
    frontier = _ensure_dict(report.get("local_frontier"))
    queue_ids = [
        _clean_text(row.get("queue_id"))
        for row in _ensure_list(frontier.get("linked_queue_items"))
        if isinstance(row, dict) and _clean_text(row.get("queue_id"))
    ]
    if not queue_ids:
        queue_ids = [_clean_text(value) for value in _ensure_list(branch.get("linked_queue_ids")) if _clean_text(value)]
    rows = [
        queue_index[queue_id]
        for queue_id in queue_ids
        if queue_id in queue_index
    ]
    rows.sort(key=lambda row: _safe_float(row.get("priority")), reverse=True)
    return rows


def _anchor_row(rows: list[dict[str, Any]]) -> dict[str, Any]:
    if not rows:
        return {}
    return sorted(
        rows,
        key=lambda row: (_safe_float(row.get("priority")), _clean_text(row.get("queue_id"))),
        reverse=True,
    )[0]


def _candidate_queue_rows(candidate: dict[str, Any], queue_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    wanted = {
        _clean_text(value)
        for value in _ensure_list(candidate.get("linked_queue_ids"))
        if _clean_text(value)
    }
    if not wanted:
        return queue_rows
    rows = [row for row in queue_rows if _clean_text(row.get("queue_id")) in wanted]
    return rows or queue_rows


def _bridge_object_name(candidate: dict[str, Any], branch: dict[str, Any], queue_rows: list[dict[str, Any]]) -> str:
    return _clean_text(
        candidate.get("candidate_object")
        or _ensure_dict(_anchor_row(queue_rows)).get("candidate_object")
        or branch.get("abstraction_required")
        or branch.get("target_label")
    )


def _bridge_object_kind(candidate: dict[str, Any], branch: dict[str, Any], queue_rows: list[dict[str, Any]]) -> str:
    anchor = _anchor_row(queue_rows)
    return _clean_text(anchor.get("carrier_kind") or branch.get("layer_kind") or candidate.get("candidate_object"))


def _bridge_object_invariant(candidate: dict[str, Any], queue_rows: list[dict[str, Any]]) -> str:
    anchor = _anchor_row(queue_rows)
    return _clean_text(candidate.get("invariant") or anchor.get("preserved_invariant"))


def _bridge_object_definition(name: str, branch: dict[str, Any], queue_rows: list[dict[str, Any]]) -> str:
    invariant = _bridge_object_invariant({}, queue_rows)
    source_excerpt = _clean_text(_ensure_dict(_anchor_row(queue_rows)).get("source_excerpt"))
    required_move = _clean_text(branch.get("required_move"))
    parts = [
        f"`{name}` denotes the structured intermediate object required by this branch.",
        source_excerpt and f"It is meant to organize the source-side content `{source_excerpt}`.",
        invariant and f"It must preserve the invariant `{invariant}`.",
        required_move and f"Its operational role is `{required_move}`.",
    ]
    return _clean_text(" ".join(part for part in parts if part))


def _self_contained_route_synopsis(
    *,
    branch: dict[str, Any],
    candidate: dict[str, Any],
    anchor: dict[str, Any],
    bridge_name: str,
    invariant: str,
) -> str:
    for value in (
        candidate.get("route_synopsis"),
        anchor.get("route_synopsis"),
    ):
        text = _clean_text(value)
        if text and not _contains_truncation(text) and not _has_placeholders(text):
            return text

    source_id = _clean_text(anchor.get("source_statement_id"))
    target_id = _clean_text(anchor.get("target_statement_id"))
    source_excerpt = _clean_text(anchor.get("source_excerpt"))
    target_excerpt = _clean_text(anchor.get("target_excerpt"))
    required_move = _clean_text(branch.get("required_move"))

    parts = [
        source_id
        and source_excerpt
        and f"Start from `{source_id}` with source content `{source_excerpt}`.",
        target_id
        and target_excerpt
        and f"Reach `{target_id}` with target content `{target_excerpt}`.",
        (
            bridge_name
            and invariant
            and f"Use `{bridge_name}` as the local bridge object while preserving `{invariant}`."
        )
        or (bridge_name and f"Use `{bridge_name}` as the local bridge object."),
        required_move and not _has_placeholders(required_move) and f"Branch move: `{required_move}`.",
    ]
    return _clean_text(" ".join(part for part in parts if part))


def _admissibility_conditions(
    *,
    name: str,
    invariant: str,
    branch: dict[str, Any],
    queue_rows: list[dict[str, Any]],
) -> list[str]:
    anchor = _anchor_row(queue_rows)
    source_excerpt = _clean_text(anchor.get("source_excerpt"))
    target_excerpt = _clean_text(anchor.get("target_excerpt"))
    conditions = [
        f"`{name}` is explicitly defined on the route from `{_clean_text(anchor.get('source_statement_id'))}` to `{_clean_text(anchor.get('target_statement_id'))}`.",
        source_excerpt and f"`{name}` absorbs the source-side theorem content `{source_excerpt}`.",
        invariant and f"`{name}` preserves `{invariant}` across the intended transfer.",
        target_excerpt and f"`{name}` is strong enough to materially address `{target_excerpt}`.",
        _clean_text(branch.get("required_move")) and f"`{name}` supports the branch move `{_clean_text(branch.get('required_move'))}`.",
    ]
    return _unique_texts([row for row in conditions if row])


def _lemma_statement(
    *,
    mode: str,
    name: str,
    invariant: str,
    source_excerpt: str,
    target_excerpt: str,
    required_move: str,
) -> str:
    if mode == "transport-lemma":
        return _clean_text(
            f"For every admissible `{name}`, the transport step preserves `{invariant}` strongly enough to move from `{source_excerpt}` toward `{target_excerpt}`."
        )
    if mode == "equivalence-theorem":
        return _clean_text(
            f"For every admissible `{name}`, the target-side operationalization is equivalent to the route-side operationalization in the sense needed to transport `{invariant}` toward `{target_excerpt}`."
        )
    if mode == "no-go-theorem":
        return _clean_text(
            f"If `{required_move}` fails for `{name}`, then no route preserving `{invariant}` can force `{target_excerpt}` from `{source_excerpt}`."
        )
    if mode == "threshold-version":
        return _clean_text(
            f"There exists a threshold regime in which `{name}` already preserves `{invariant}` well enough to imply a restricted version of `{target_excerpt}`."
        )
    return _clean_text(
        f"For every admissible `{name}`, the first route-specific realization step preserves `{invariant}` and prepares the passage from `{source_excerpt}` to `{target_excerpt}`."
    )


def _first_nontrivial_lemma(
    *,
    branch: dict[str, Any],
    candidate: dict[str, Any],
    queue_rows: list[dict[str, Any]],
    mode: str,
) -> dict[str, Any]:
    anchor = _anchor_row(queue_rows)
    name = _bridge_object_name(candidate, branch, queue_rows)
    source_excerpt = _clean_text(anchor.get("source_excerpt"))
    target_excerpt = _clean_text(anchor.get("target_excerpt"))
    invariant = _bridge_object_invariant(candidate, queue_rows)
    title = _clean_text(candidate.get("title")) or f"{_restricted_regime_title(mode)} for {name}"
    return {
        "title": title,
        "statement": _lemma_statement(
            mode=mode,
            name=name,
            invariant=invariant,
            source_excerpt=source_excerpt,
            target_excerpt=target_excerpt,
            required_move=_clean_text(branch.get("required_move")),
        ),
    }


def _negative_barrier_version(
    *,
    mode: str,
    branch: dict[str, Any],
    candidate: dict[str, Any],
    queue_rows: list[dict[str, Any]],
    execution: dict[str, Any],
) -> str:
    anchor = _anchor_row(queue_rows)
    name = _bridge_object_name(candidate, branch, queue_rows)
    invariant = _bridge_object_invariant(candidate, queue_rows)
    target_excerpt = _clean_text(anchor.get("target_excerpt"))
    negative_outputs = _unique_texts(_ensure_list(execution.get("negative_outputs")))
    lead_negative = negative_outputs[0] if negative_outputs else ""
    if mode == "transport-lemma":
        return _clean_text(
            f"No transport from `{name}` preserves `{invariant}` across the intended model shift without extra structure. {lead_negative}"
        )
    if mode == "equivalence-theorem":
        return _clean_text(
            f"Absent an explicit equivalence witness for `{name}`, transport toward `{target_excerpt}` is not licensed. {lead_negative}"
        )
    if mode == "no-go-theorem":
        return _clean_text(
            f"Every attempted realization of `{name}` remains blocked by the current barrier, so `{target_excerpt}` does not follow. {lead_negative}"
        )
    return _clean_text(
        f"If `{name}` cannot be realized with invariant `{invariant}`, the route cannot force `{target_excerpt}`. {lead_negative}"
    )


def _independent_value_claim(*, mode: str, branch: dict[str, Any], candidate: dict[str, Any]) -> str:
    name = _bridge_object_name(candidate, branch, [])
    if mode == "transport-lemma":
        return _clean_text(
            f"A theorem isolating the transport behavior of `{name}` would be independently valuable because it clarifies the exact cross-model obstruction, even if the main problem stays open."
        )
    if mode == "equivalence-theorem":
        return _clean_text(
            f"An equivalence theorem for `{name}` would independently matter because it identifies when two live operationalizations are mathematically interchangeable rather than merely analogous."
        )
    if mode == "no-go-theorem":
        return _clean_text(
            f"A no-go theorem for `{name}` would be independently valuable because it collapses an entire discovery subspace and exposes a genuine barrier theorem."
        )
    if mode == "threshold-version":
        return _clean_text(
            f"A threshold theorem for `{name}` would be independently valuable because it localizes the first nontrivial regime where the route becomes mathematically real."
        )
    return _clean_text(
        f"A concrete special-case theorem for `{name}` would be independently valuable because it converts a broad discovery programme into an inspectable mathematical subresult."
    )


def _regime_and_quantifiers(
    *,
    branch: dict[str, Any],
    candidate: dict[str, Any],
    queue_rows: list[dict[str, Any]],
    mode: str,
) -> dict[str, Any]:
    anchor = _anchor_row(queue_rows)
    name = _bridge_object_name(candidate, branch, queue_rows)
    return {
        "restricted_regime_mode": mode,
        "quantifier_frame": _clean_text(
            f"For every admissible `{name}` attached to the route from `{_clean_text(anchor.get('source_statement_id'))}` to `{_clean_text(anchor.get('target_statement_id'))}`,"
            f" under the discovery branch `{_clean_text(branch.get('target_label'))}`."
        ),
        "source_regime": _clean_text(anchor.get("source_excerpt")),
        "target_regime": _clean_text(anchor.get("target_excerpt")),
        "route_focus": _clean_text(branch.get("required_move")),
    }


def _branch_to_definition(
    *,
    branch: dict[str, Any],
    candidate: dict[str, Any],
    queue_rows: list[dict[str, Any]],
    execution: dict[str, Any],
) -> dict[str, Any]:
    name = _bridge_object_name(candidate, branch, queue_rows)
    lens = _ensure_dict(execution.get("lens_artifacts"))
    concept_definitions = [
        _clean_text(
            f"`{name}`: {_bridge_object_definition(name, branch, queue_rows)}"
        )
    ]
    lemma_statement = _ensure_dict(
        _first_nontrivial_lemma(
            branch=branch,
            candidate=candidate,
            queue_rows=queue_rows,
            mode=_restricted_regime_mode(branch.get("target_id")),
        )
    ).get("statement")
    transport_laws = _unique_texts(_ensure_list(lens.get("transport_obligations")) + [lemma_statement])
    return {
        "concept_definitions": concept_definitions,
        "equivalence_claims": _unique_texts(_ensure_list(lens.get("equivalence_claims"))),
        "transport_laws": transport_laws,
        "commutative_diagram_obligations": _unique_texts(_ensure_list(lens.get("commutativity_obligations"))),
        "coherence_failures": _unique_texts(_ensure_list(lens.get("coherence_failures"))),
    }


def _foundation_search(
    *,
    branch: dict[str, Any],
    execution: dict[str, Any],
    mode: str,
    queue_rows: list[dict[str, Any]],
) -> dict[str, Any]:
    gate = _ensure_dict(execution.get("external_framework_search")) or _ensure_dict(branch.get("external_framework_search"))
    regions = _unique_texts(_ensure_list(gate.get("candidate_framework_regions")))
    target_id = _sanitize_id(branch.get("target_id"))
    if not regions:
        if target_id in {"transport", "barrier-aware-transfer"}:
            regions = ["transport framework", "obstruction family framework"]
        elif target_id in {"categorical-reframing", "alignment"}:
            regions = ["universal-property / factorization framework"]
        elif target_id in {"equivalence-coherence-reframing", "semantic-bridge"}:
            regions = ["equivalence / coherent transport framework"]
        else:
            regions = ["obstruction family framework"]
    anchor = _anchor_row(queue_rows)
    return {
        "recommended": bool(gate.get("recommended")),
        "mode": _clean_text(gate.get("mode")) or "targeted-foundation-search",
        "candidate_framework_regions": regions,
        "local_prerequisites": _unique_texts(_ensure_list(gate.get("local_prerequisites"))),
        "query_templates": _unique_texts(_ensure_list(gate.get("query_templates"))),
        "structural_question": _clean_text(
            gate.get("justification")
            or f"Which framework explains how the route from `{_clean_text(anchor.get('source_statement_id'))}` to `{_clean_text(anchor.get('target_statement_id'))}` can be mediated in `{mode}` form?"
        ),
    }


def _theorem_shaped(text: Any) -> bool:
    normalized = _clean_text(text).lower()
    if not normalized or _has_placeholders(normalized):
        return False
    markers = ("for every", "there exists", "if ", "no ", "whenever")
    return any(marker in normalized for marker in markers)


def _expert_gate(package: dict[str, Any]) -> dict[str, Any]:
    exact_statement = _clean_text(package.get("exact_statement"))
    bridge_object = _ensure_dict(package.get("bridge_object"))
    lemma = _ensure_dict(package.get("first_nontrivial_lemma"))
    target_excerpt = _clean_text(package.get("target_excerpt"))
    criteria = [
        {
            "id": "no_placeholders",
            "label": "No placeholders remain in the theorem statement.",
            "passes": not _has_placeholders(exact_statement),
        },
        {
            "id": "named_object",
            "label": "The bridge object is a named family or map.",
            "passes": _named_object(bridge_object.get("name")),
        },
        {
            "id": "precise_target",
            "label": "The target claim is precise enough to inspect.",
            "passes": bool(target_excerpt) and (_token_overlap(exact_statement, target_excerpt) >= 2 or _clean_text(package.get("target_statement_id")) in exact_statement),
        },
        {
            "id": "theorem_shaped_lemma",
            "label": "The first proof obligation is theorem-shaped.",
            "passes": _theorem_shaped(lemma.get("statement")),
        },
        {
            "id": "falsifier",
            "label": "A falsifier or barrier criterion is explicit.",
            "passes": bool(_clean_text(package.get("negative_barrier_version"))),
        },
        {
            "id": "independent_value",
            "label": "The result matters independently of the main conjecture.",
            "passes": bool(_clean_text(package.get("independent_value_claim"))),
        },
    ]
    hard_failures = [row["label"] for row in criteria if not row["passes"]]
    return {
        "score": sum(1 for row in criteria if row["passes"]),
        "max_score": len(criteria),
        "passes": not hard_failures,
        "criteria": criteria,
        "hard_failures": hard_failures,
    }


def _package_from_candidate(
    *,
    execution_row: dict[str, Any],
    report: dict[str, Any],
    queue_rows: list[dict[str, Any]],
    candidate: dict[str, Any],
    ordinal: int,
) -> dict[str, Any]:
    branch = _ensure_dict(report.get("branch"))
    execution = _ensure_dict(report.get("execution"))
    package_queue_rows = _candidate_queue_rows(candidate, queue_rows)
    anchor = _anchor_row(package_queue_rows)
    mode = _restricted_regime_mode(branch.get("target_id"))
    bridge_name = _bridge_object_name(candidate, branch, package_queue_rows)
    bridge_kind = _bridge_object_kind(candidate, branch, package_queue_rows)
    invariant = _bridge_object_invariant(candidate, package_queue_rows)
    exact_statement = _clean_text(candidate.get("statement")) or _clean_text(branch.get("minimal_theorem_shape"))
    route_synopsis = _self_contained_route_synopsis(
        branch=branch,
        candidate=candidate,
        anchor=anchor,
        bridge_name=bridge_name,
        invariant=invariant,
    )
    first_nontrivial_lemma = _first_nontrivial_lemma(
        branch=branch,
        candidate=candidate,
        queue_rows=package_queue_rows,
        mode=mode,
    )
    negative_barrier_version = _negative_barrier_version(
        mode=mode,
        branch=branch,
        candidate=candidate,
        queue_rows=package_queue_rows,
        execution=execution,
    )
    branch_to_definition = _branch_to_definition(
        branch=branch,
        candidate=candidate,
        queue_rows=package_queue_rows,
        execution=execution,
    )
    packet_fields = normalize_expert_packet_fields(
        mode=mode,
        target_id=branch.get("target_id"),
        bridge_name=bridge_name,
        invariant=invariant,
        first_nontrivial_lemma=first_nontrivial_lemma,
        negative_barrier_version=negative_barrier_version,
        branch_to_definition=branch_to_definition,
        proof_strategy_family=candidate.get("proof_strategy_family"),
        negative_route=candidate.get("negative_route"),
        failure_diagnosis=candidate.get("failure_diagnosis"),
        proof_obligations=candidate.get("proof_obligations"),
        candidate_lemmas=candidate.get("candidate_lemmas"),
        negative_outputs=execution.get("negative_outputs"),
    )
    package = {
        "package_id": f"conjpkg.{_sanitize_id(_clean_text(branch.get('branch_id')))}.{ordinal:02d}",
        "kind": "expert-conjecture",
        "branch_id": _clean_text(branch.get("branch_id")),
        "execution_id": _clean_text(_ensure_dict(report.get("metadata")).get("execution_id")),
        "target_id": _clean_text(branch.get("target_id")),
        "target_label": _clean_text(branch.get("target_label")),
        "routing_priority": _safe_float(branch.get("routing_priority")),
        "title": _clean_text(candidate.get("title")) or f"{_restricted_regime_title(mode)} for {bridge_name}",
        "exact_statement": exact_statement,
        "headline": exact_statement,
        "source_statement_id": _clean_text(anchor.get("source_statement_id")),
        "target_statement_id": _clean_text(anchor.get("target_statement_id")),
        "source_excerpt": _clean_text(anchor.get("source_excerpt")),
        "target_excerpt": _clean_text(anchor.get("target_excerpt")),
        "route_synopsis": route_synopsis,
        "candidate_object": bridge_name,
        "preserved_invariant": invariant,
        "linked_queue_ids": _unique_texts([row.get("queue_id") for row in queue_rows]),
        "linked_bridge_ids": _unique_texts([row.get("bridge_id") for row in queue_rows]),
        "artifact_json": _clean_text(execution_row.get("artifact_json")),
        "artifact_md": _clean_text(execution_row.get("artifact_md")),
        "restricted_regime_mode": mode,
        "regime_and_quantifiers": _regime_and_quantifiers(
            branch=branch,
            candidate=candidate,
            queue_rows=package_queue_rows,
            mode=mode,
        ),
        "bridge_object": {
            "name": bridge_name,
            "definition": _bridge_object_definition(bridge_name, branch, package_queue_rows),
            "kind": bridge_kind,
            "invariant": invariant,
        },
        "admissibility_conditions": _admissibility_conditions(
            name=bridge_name,
            invariant=invariant,
            branch=branch,
            queue_rows=package_queue_rows,
        ),
        "first_nontrivial_lemma": first_nontrivial_lemma,
        "negative_barrier_version": negative_barrier_version,
        "proof_strategy_family": packet_fields.get("proof_strategy_family"),
        "negative_route": packet_fields.get("negative_route"),
        "failure_diagnosis": packet_fields.get("failure_diagnosis"),
        "proof_obligations": packet_fields.get("proof_obligations"),
        "candidate_lemmas": packet_fields.get("candidate_lemmas"),
        "independent_value_claim": _independent_value_claim(mode=mode, branch=branch, candidate=candidate),
        "branch_to_definition": branch_to_definition,
        "foundation_search": _foundation_search(
            branch=branch,
            execution=execution,
            mode=mode,
            queue_rows=package_queue_rows,
        ),
    }
    package["mathematical_layers"] = (
        _ensure_dict(candidate.get("mathematical_layers"))
        or build_mathematical_layers(
            title=package.get("title"),
            exact_statement=package.get("exact_statement"),
            route_synopsis=package.get("route_synopsis"),
            bridge_name=bridge_name,
            invariant=invariant,
            mode=mode,
            source_statement_id=package.get("source_statement_id"),
            target_statement_id=package.get("target_statement_id"),
            source_excerpt=package.get("source_excerpt"),
            target_excerpt=package.get("target_excerpt"),
            admissibility_conditions=package.get("admissibility_conditions"),
            first_nontrivial_lemma_title=_ensure_dict(package.get("first_nontrivial_lemma")).get("title"),
            first_nontrivial_lemma_statement=_ensure_dict(package.get("first_nontrivial_lemma")).get("statement"),
            negative_barrier_version=package.get("negative_barrier_version"),
        )
    )
    package["expert_gate"] = _expert_gate(package)
    return package


def _restricted_programme(
    *,
    execution_row: dict[str, Any],
    report: dict[str, Any],
    queue_rows: list[dict[str, Any]],
    concept_revision: dict[str, Any],
    ordinal: int,
) -> dict[str, Any]:
    branch = _ensure_dict(report.get("branch"))
    anchor = _anchor_row(queue_rows)
    mode = _restricted_regime_mode(branch.get("target_id"))
    label = _clean_text(concept_revision.get("label")) or _clean_text(branch.get("target_label"))
    statement = _clean_text(branch.get("minimal_theorem_shape")) or _clean_text(concept_revision.get("revision"))
    return {
        "programme_id": f"regprog.{_sanitize_id(_clean_text(branch.get('branch_id')))}.{ordinal:02d}",
        "branch_id": _clean_text(branch.get("branch_id")),
        "execution_id": _clean_text(_ensure_dict(report.get("metadata")).get("execution_id")),
        "target_id": _clean_text(branch.get("target_id")),
        "target_label": _clean_text(branch.get("target_label")),
        "routing_priority": _safe_float(branch.get("routing_priority")),
        "restricted_regime_mode": mode,
        "title": f"{_restricted_regime_title(mode)}: {label}",
        "exact_statement": statement,
        "source_statement_id": _clean_text(anchor.get("source_statement_id")),
        "target_statement_id": _clean_text(anchor.get("target_statement_id")),
        "source_excerpt": _clean_text(anchor.get("source_excerpt")),
        "target_excerpt": _clean_text(anchor.get("target_excerpt")),
        "epistemic_gain": _clean_text(concept_revision.get("epistemic_gain")),
        "rationale": _clean_text(concept_revision.get("revision")) or _clean_text(branch.get("required_move")),
        "artifact_json": _clean_text(execution_row.get("artifact_json")),
        "artifact_md": _clean_text(execution_row.get("artifact_md")),
    }


def build_report(*, artifacts_dir: Path, kb_ref: str, repo_root: Path | None = None) -> dict[str, Any]:
    repo_root = (repo_root or Path(__file__).resolve().parents[4]).resolve()
    queue_json, _ = proof_queue_paths(repo_root, kb_ref)
    queue = load_proof_queue(queue_json, kb_ref=kb_ref)
    queue_index = _queue_entry_index(queue)
    execution_index = _load_json(discovery_execution_paths(artifacts_dir)[0])
    reports = _execution_reports(execution_index)

    expert_packages: list[dict[str, Any]] = []
    restricted_programmes: list[dict[str, Any]] = []
    definition_programmes: list[dict[str, Any]] = []
    foundation_search_programmes: list[dict[str, Any]] = []
    ready_for_prove: list[dict[str, Any]] = []
    ready_for_discovery: list[dict[str, Any]] = []

    for execution_row, report in reports:
        branch = _ensure_dict(report.get("branch"))
        execution = _ensure_dict(report.get("execution"))
        queue_rows = _linked_queue_rows(report=report, queue_index=queue_index)
        theorem_candidates = [
            row
            for row in _ensure_list(execution.get("theorem_candidates"))
            if isinstance(row, dict)
        ]
        for ordinal, candidate in enumerate(theorem_candidates, start=1):
            package = _package_from_candidate(
                execution_row=execution_row,
                report=report,
                queue_rows=queue_rows,
                candidate=candidate,
                ordinal=ordinal,
            )
            expert_packages.append(package)
            definition_programmes.append(
                {
                    "package_id": package["package_id"],
                    "branch_id": package["branch_id"],
                    "target_label": package["target_label"],
                    "branch_to_definition": package["branch_to_definition"],
                }
            )
            foundation_search = _ensure_dict(package.get("foundation_search"))
            if foundation_search:
                foundation_search_programmes.append(
                    {
                        "package_id": package["package_id"],
                        "branch_id": package["branch_id"],
                        "target_label": package["target_label"],
                        "foundation_search": foundation_search,
                    }
                )
            if _ensure_dict(package.get("expert_gate")).get("passes"):
                ready_for_prove.append(package)
            else:
                ready_for_discovery.append(package)
        concept_revisions = [
            row
            for row in _ensure_list(execution.get("concept_revisions"))
            if isinstance(row, dict)
        ]
        for ordinal, row in enumerate(concept_revisions, start=1):
            restricted_programmes.append(
                _restricted_programme(
                    execution_row=execution_row,
                    report=report,
                    queue_rows=queue_rows,
                    concept_revision=row,
                    ordinal=ordinal,
                )
            )

    ready_for_prove.sort(key=lambda row: (_safe_float(row.get("routing_priority")), row.get("package_id", "")), reverse=True)
    ready_for_discovery.sort(key=lambda row: (_safe_float(row.get("routing_priority")), row.get("package_id", "")), reverse=True)
    restricted_programmes.sort(key=lambda row: (_safe_float(row.get("routing_priority")), row.get("programme_id", "")), reverse=True)
    foundation_search_programmes.sort(
        key=lambda row: (_safe_float(_ensure_dict(row.get("foundation_search")).get("recommended")), _clean_text(row.get("package_id"))),
        reverse=True,
    )

    summary = (
        "Discovery now compiles branch executions into theorem packages rather than leaving them as abstract branch prompts."
        if ready_for_prove
        else "Discovery produced structurally meaningful theorem packages, but none yet clear the expert-grade promotion gate."
    )
    next_move = (
        "Promote the ready-for-prove expert conjectures into the proof queue and keep the restricted-regime and foundation-search programmes on the discovery frontier."
        if ready_for_prove
        else "Stay in discovery: refine definitions, restricted regimes, and foundation-search targets until at least one package clears the expert-grade gate."
    )
    return {
        "metadata": {
            "kb_ref": kb_ref,
            "execution_count": len(reports),
            "expert_conjecture_count": len(expert_packages),
            "ready_for_prove_count": len(ready_for_prove),
            "ready_for_discovery_count": len(ready_for_discovery),
            "restricted_regime_count": len(restricted_programmes),
            "definition_programme_count": len(definition_programmes),
            "foundation_search_count": len(foundation_search_programmes),
        },
        "expert_conjectures": expert_packages,
        "restricted_regime_programmes": restricted_programmes,
        "definition_programmes": definition_programmes,
        "foundation_search_programmes": foundation_search_programmes,
        "agenda": {
            "ready_for_prove": ready_for_prove,
            "ready_for_discovery": ready_for_discovery,
        },
        "judgment": {
            "summary": summary,
            "next_move": next_move,
        },
    }


def render_markdown(report: dict[str, Any]) -> str:
    meta = _ensure_dict(report.get("metadata"))
    lines = [
        "# Expert Conjectures",
        "",
        f"- KB ref: {meta.get('kb_ref', '')}",
        f"- Executed discovery branches: {meta.get('execution_count', 0)}",
        f"- Expert conjecture packages: {meta.get('expert_conjecture_count', 0)}",
        f"- Ready for prove: {meta.get('ready_for_prove_count', 0)}",
        f"- Ready for discovery: {meta.get('ready_for_discovery_count', 0)}",
        f"- Restricted-regime programmes: {meta.get('restricted_regime_count', 0)}",
        f"- Branch-to-definition programmes: {meta.get('definition_programme_count', 0)}",
        f"- Foundation-search programmes: {meta.get('foundation_search_count', 0)}",
        "",
        "## Judgment",
        "",
        f"- {_ensure_dict(report.get('judgment')).get('summary', '')}",
        f"- Next move: {_ensure_dict(report.get('judgment')).get('next_move', '')}",
        "",
        "## Ready For Prove",
        "",
    ]
    ready_for_prove = [row for row in _ensure_list(_ensure_dict(report.get("agenda")).get("ready_for_prove")) if isinstance(row, dict)]
    if not ready_for_prove:
        lines.append("- No expert-grade conjectures are ready to enter prove.")
    else:
        for row in ready_for_prove:
            gate = _ensure_dict(row.get("expert_gate"))
            lines.append(
                f"- {row.get('package_id', '')}: {row.get('exact_statement', '')} "
                f"(priority {_safe_float(row.get('routing_priority')):.3f}; gate {gate.get('score', 0)}/{gate.get('max_score', 0)})"
            )
    lines.extend(["", "## Ready For Discovery", ""])
    ready_for_discovery = [row for row in _ensure_list(_ensure_dict(report.get("agenda")).get("ready_for_discovery")) if isinstance(row, dict)]
    if not ready_for_discovery:
        lines.append("- No discovery-only theorem packages remain.")
    else:
        for row in ready_for_discovery:
            gate = _ensure_dict(row.get("expert_gate"))
            lines.append(
                f"- {row.get('package_id', '')}: {row.get('exact_statement', '')} "
                f"(priority {_safe_float(row.get('routing_priority')):.3f}; gate failures: {', '.join(_ensure_list(gate.get('hard_failures')))} )"
            )
    lines.extend(["", "## Restricted-Regime Programmes", ""])
    restricted = [row for row in _ensure_list(report.get("restricted_regime_programmes")) if isinstance(row, dict)]
    if not restricted:
        lines.append("- No restricted-regime programmes were generated.")
    else:
        for row in restricted:
            lines.append(
                f"- {row.get('programme_id', '')}: {row.get('title', '')} | {row.get('exact_statement', '')}"
            )
    lines.extend(["", "## Foundation-Search Programmes", ""])
    foundation_rows = [row for row in _ensure_list(report.get("foundation_search_programmes")) if isinstance(row, dict)]
    if not foundation_rows:
        lines.append("- No branch-level foundation-search programmes were generated.")
    else:
        for row in foundation_rows:
            search = _ensure_dict(row.get("foundation_search"))
            lines.append(
                f"- {row.get('package_id', '')}: {', '.join(_ensure_list(search.get('candidate_framework_regions')))}"
            )
            lines.append(f"  Structural question: {search.get('structural_question', '')}")
    lines.extend(["", "## Packages", ""])
    for row in _ensure_list(report.get("expert_conjectures")):
        if not isinstance(row, dict):
            continue
        gate = _ensure_dict(row.get("expert_gate"))
        bridge = _ensure_dict(row.get("bridge_object"))
        lemma = _ensure_dict(row.get("first_nontrivial_lemma"))
        math_layers = _ensure_dict(row.get("mathematical_layers"))
        symbol_rows = [
            f"{_clean_text(item.get('symbol'))}: {_clean_text(item.get('meaning'))}"
            for item in _ensure_list(math_layers.get("symbol_ledger"))
            if isinstance(item, dict) and _clean_text(item.get("symbol"))
        ]
        latex_layer = _ensure_dict(math_layers.get("latex"))
        lean_layer = _ensure_dict(math_layers.get("lean_style"))
        lines.extend(
            [
                f"### {row.get('package_id', '')}",
                "",
                f"- Title: {row.get('title', '')}",
                f"- Exact statement: {row.get('exact_statement', '')}",
                f"- Restricted-regime mode: {row.get('restricted_regime_mode', '')}",
                f"- Bridge object: {bridge.get('name', '')} ({bridge.get('kind', '')})",
                f"- Bridge definition: {bridge.get('definition', '')}",
                f"- Admissibility conditions: {'; '.join(_ensure_list(row.get('admissibility_conditions')))}",
                f"- First nontrivial lemma: {lemma.get('title', '')} | {lemma.get('statement', '')}",
                f"- Negative/barrier version: {row.get('negative_barrier_version', '')}",
                f"- Proof strategy family: {row.get('proof_strategy_family', '')}",
                f"- Negative route: {row.get('negative_route', '')}",
                f"- Failure diagnosis: {row.get('failure_diagnosis', '')}",
                f"- Proof obligations: {'; '.join(_ensure_list(row.get('proof_obligations')))}",
                f"- Candidate lemmas: {'; '.join(_ensure_list(row.get('candidate_lemmas')))}",
                f"- Independent value: {row.get('independent_value_claim', '')}",
                f"- Quantifier signature: {_clean_text(math_layers.get('quantifier_signature'))}",
                f"- Symbol ledger: {'; '.join(symbol_rows)}",
                f"- LaTeX theorem: {_clean_text(latex_layer.get('theorem_statement'))}",
                f"- Lean-style theorem scaffold: {_clean_text(lean_layer.get('theorem_name'))}",
                f"- Expert gate: {gate.get('score', 0)}/{gate.get('max_score', 0)} | passes={gate.get('passes', False)}",
                f"- Hard failures: {', '.join(_ensure_list(gate.get('hard_failures')))}",
                f"- Report: {row.get('artifact_md', '')}",
                "",
            ]
        )
        lean_scaffold = _clean_text(lean_layer.get("scaffold"))
        if lean_scaffold:
            lines.extend(
                [
                    "```lean",
                    str(lean_layer.get("scaffold", "")).strip(),
                    "```",
                    "",
                ]
            )
    return "\n".join(lines).rstrip() + "\n"


def render_tex(report: dict[str, Any]) -> str:
    meta = _ensure_dict(report.get("metadata"))
    ready_rows = "\n".join(
        f"\\item {_latex_escape(row.get('package_id', ''))}: {_latex_escape(row.get('exact_statement', ''))}"
        for row in _ensure_list(_ensure_dict(report.get("agenda")).get("ready_for_prove"))
        if isinstance(row, dict)
    ) or "\\item No expert-grade conjectures are ready to enter prove."
    restricted_rows = "\n".join(
        f"\\item {_latex_escape(row.get('title', ''))}: {_latex_escape(row.get('exact_statement', ''))}"
        for row in _ensure_list(report.get("restricted_regime_programmes"))
        if isinstance(row, dict)
    ) or "\\item No restricted-regime programmes were generated."
    foundation_rows = "\n".join(
        f"\\item {_latex_escape(row.get('package_id', ''))}: {_latex_escape(', '.join(_ensure_list(_ensure_dict(row.get('foundation_search')).get('candidate_framework_regions'))))}"
        for row in _ensure_list(report.get("foundation_search_programmes"))
        if isinstance(row, dict)
    ) or "\\item No branch-level foundation-search programmes were generated."
    package_sections = []
    for row in _ensure_list(report.get("expert_conjectures")):
        if not isinstance(row, dict):
            continue
        bridge = _ensure_dict(row.get("bridge_object"))
        lemma = _ensure_dict(row.get("first_nontrivial_lemma"))
        gate = _ensure_dict(row.get("expert_gate"))
        math_layers = _ensure_dict(row.get("mathematical_layers"))
        latex_layer = _ensure_dict(math_layers.get("latex"))
        package_sections.append(
            "\n".join(
                [
                    f"\\subsection*{{{_latex_escape(row.get('package_id', ''))}}}",
                    "\\begin{itemize}",
                    f"\\item Exact statement: {_latex_escape(row.get('exact_statement', ''))}",
                    f"\\item Restricted-regime mode: {_latex_escape(row.get('restricted_regime_mode', ''))}",
                    f"\\item Bridge object: {_latex_escape(bridge.get('name', ''))} ({_latex_escape(bridge.get('kind', ''))})",
                    f"\\item Bridge definition: {_latex_escape(bridge.get('definition', ''))}",
                    f"\\item First nontrivial lemma: {_latex_escape(lemma.get('statement', ''))}",
                    f"\\item Quantifier signature: {_latex_escape(math_layers.get('quantifier_signature', ''))}",
                    f"\\item LaTeX theorem: {_latex_escape(latex_layer.get('theorem_statement', ''))}",
                    f"\\item Negative/barrier version: {_latex_escape(row.get('negative_barrier_version', ''))}",
                    f"\\item Proof strategy family: {_latex_escape(row.get('proof_strategy_family', ''))}",
                    f"\\item Negative route: {_latex_escape(row.get('negative_route', ''))}",
                    f"\\item Failure diagnosis: {_latex_escape(row.get('failure_diagnosis', ''))}",
                    f"\\item Proof obligations: {_latex_escape('; '.join(_ensure_list(row.get('proof_obligations'))))}",
                    f"\\item Candidate lemmas: {_latex_escape('; '.join(_ensure_list(row.get('candidate_lemmas'))))}",
                    f"\\item Independent value: {_latex_escape(row.get('independent_value_claim', ''))}",
                    f"\\item Expert gate: {int(gate.get('score', 0) or 0)}/{int(gate.get('max_score', 0) or 0)}",
                    "\\end{itemize}",
                ]
            )
        )
    package_blob = "\n\n".join(package_sections) or "\\subsection*{No packages}\\noindent No theorem packages were generated."
    judgment = _ensure_dict(report.get("judgment"))
    return rf"""\documentclass[11pt]{{article}}
\usepackage[margin=1in]{{geometry}}
\usepackage{{hyperref}}
\usepackage[T1]{{fontenc}}
\usepackage[utf8]{{inputenc}}
\title{{Expert Conjectures}}
\author{{Abducer}}
\date{{}}
\begin{{document}}
\maketitle

\noindent
\textbf{{KB ref:}} {_latex_escape(meta.get('kb_ref', ''))}\\
\textbf{{Executed discovery branches:}} {int(meta.get('execution_count', 0) or 0)}\\
\textbf{{Expert conjecture packages:}} {int(meta.get('expert_conjecture_count', 0) or 0)}\\
\textbf{{Ready for prove:}} {int(meta.get('ready_for_prove_count', 0) or 0)}\\
\textbf{{Ready for discovery:}} {int(meta.get('ready_for_discovery_count', 0) or 0)}\\
\textbf{{Restricted-regime programmes:}} {int(meta.get('restricted_regime_count', 0) or 0)}

\section*{{Judgment}}
\begin{{itemize}}
\item {_latex_escape(judgment.get('summary', ''))}
\item Next move: {_latex_escape(judgment.get('next_move', ''))}
\end{{itemize}}

\section*{{Ready For Prove}}
\begin{{itemize}}
{ready_rows}
\end{{itemize}}

\section*{{Restricted-Regime Programmes}}
\begin{{itemize}}
{restricted_rows}
\end{{itemize}}

\section*{{Foundation-Search Programmes}}
\begin{{itemize}}
{foundation_rows}
\end{{itemize}}

\section*{{Packages}}
{package_blob}

\end{{document}}
"""


def write_report(
    report: dict[str, Any],
    *,
    output_json: Path,
    output_md: Path,
    output_tex: Path,
    output_pdf: Path,
    compile: bool = True,
    latex_engine: str = "auto",
) -> None:
    output_json.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    output_md.write_text(render_markdown(report), encoding="utf-8")
    output_tex.write_text(render_tex(report), encoding="utf-8")
    if compile:
        compile_pdf(output_tex, output_pdf, preferred_engine=latex_engine)


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate expert-grade conjecture packages from discovery branches.")
    parser.add_argument("--artifacts-dir", required=True, help="Path to artifacts/<kb-ref>.")
    parser.add_argument("--kb-ref", default="", help="Optional KB reference override.")
    parser.add_argument("--latex-engine", default="auto", help="Preferred LaTeX engine for PDF generation.")
    args = parser.parse_args()

    artifacts_dir = Path(args.artifacts_dir).expanduser().resolve()
    repo_root = Path(__file__).resolve().parents[4]
    kb_ref = _clean_text(args.kb_ref) or kb_ref_from_artifacts_dir(artifacts_dir)
    if not kb_ref:
        raise SystemExit("Unable to determine kb_ref from artifacts directory; pass --kb-ref.")
    artifacts_dir = canonical_artifacts_dir(repo_root, kb_ref) if not artifacts_dir.exists() else artifacts_dir

    logger = ReasoningLogger("kb-expert-conjecture-generator", repo_root=repo_root)
    report = build_report(artifacts_dir=artifacts_dir, kb_ref=kb_ref, repo_root=repo_root)
    output_json, output_md, output_tex, output_pdf = expert_conjecture_paths(artifacts_dir)
    write_report(
        report,
        output_json=output_json,
        output_md=output_md,
        output_tex=output_tex,
        output_pdf=output_pdf,
        latex_engine=args.latex_engine,
    )
    logger.step(
        "Generated expert conjectures",
        details="\n".join(
            [
                f"kb_ref={kb_ref}",
                f"expert_conjecture_count={int(_ensure_dict(report.get('metadata')).get('expert_conjecture_count', 0) or 0)}",
                f"ready_for_prove_count={int(_ensure_dict(report.get('metadata')).get('ready_for_prove_count', 0) or 0)}",
            ]
        ),
    )
    logger.add_output("expert_conjectures_json", output_json)
    logger.add_output("expert_conjectures_md", output_md)
    logger.add_output("expert_conjectures_tex", output_tex)
    logger.add_output("expert_conjectures_pdf", output_pdf)
    logger.finalize(
        status="success",
        summary=f"Generated {int(_ensure_dict(report.get('metadata')).get('expert_conjecture_count', 0) or 0)} expert conjecture packages for `{kb_ref}`.",
    )
    print(f"[OK] Wrote expert conjectures JSON: {output_json}")
    print(f"[OK] Wrote expert conjectures Markdown: {output_md}")
    print(f"[OK] Wrote expert conjectures TeX: {output_tex}")
    print(f"[OK] Wrote expert conjectures PDF: {output_pdf}")
    print(f"[LOG] {logger.log_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
