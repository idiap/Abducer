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

"""Promote theorem-shaped discovery outputs back into the proof queue."""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
import datetime as dt
from pathlib import Path
from typing import Any

_COMMON_DIR = Path(__file__).resolve().parents[3] / "common"
_PROVE_SCRIPT_DIR = Path(__file__).resolve().parents[3] / "discovery" / "kb-prove-cycle" / "scripts"
_GOVERNOR_SCRIPT_DIR = Path(__file__).resolve().parents[3] / "evaluation" / "kb-discovery-governor" / "scripts"
if str(_COMMON_DIR) not in sys.path:
    sys.path.insert(0, str(_COMMON_DIR))
if str(_PROVE_SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(_PROVE_SCRIPT_DIR))
if str(_GOVERNOR_SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(_GOVERNOR_SCRIPT_DIR))

from kb_context import canonical_artifacts_dir
from kb_context import kb_ref_from_artifacts_dir
from mathematical_layers import build_mathematical_layers
from generate_proof_cycle_summary import refresh_summary_from_sources
from generate_discovery_governor_report import discovery_governor_paths
from generate_discovery_governor_report import branch_decision_index
from generate_discovery_governor_report import expert_package_decision_index
from generate_discovery_governor_report import load_discovery_governor_report
from generate_discovery_governor_report import PROMOTION_ALLOWED_DECISIONS
from expert_packet_fields import normalize_expert_packet_fields
from proof_queue import enqueue_entries
from proof_queue import load_proof_queue
from proof_queue import make_queue_key
from proof_queue import proof_queue_paths
from proof_queue import save_proof_queue
from reasoning_log import ReasoningLogger


def _clean_text(value: Any) -> str:
    return " ".join(str(value or "").strip().split())


def _ensure_dict(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def _ensure_list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def _load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}
    return payload if isinstance(payload, dict) else {}


def _utc_now() -> str:
    return dt.datetime.now(dt.UTC).isoformat()


def _is_schematic_statement(text: str) -> bool:
    normalized = _clean_text(text).lower()
    if not normalized:
        return True
    return any(
        token in normalized
        for token in {
            "source theorem s",
            "target theorem t",
            "regime r",
            "carrier c",
            "invariant i",
            "object d",
            "if source theorem",
        }
    )


def _contains_truncation(text: str) -> bool:
    normalized = _clean_text(text).lower()
    return "..." in normalized or "truncated" in normalized


def _programme_report_paths(artifacts_dir: Path) -> tuple[Path, Path]:
    return (
        artifacts_dir / "discovery-programme-promotions.json",
        artifacts_dir / "discovery-programme-promotions.md",
    )


def _expert_conjecture_report_path(artifacts_dir: Path) -> Path:
    return artifacts_dir / "expert-conjectures.json"


def _majority_value(entries: list[dict[str, Any]], field: str) -> str:
    counter: Counter[str] = Counter()
    for row in entries:
        text = _clean_text(row.get(field))
        if text:
            counter[text] += 1
    return counter.most_common(1)[0][0] if counter else ""


def _first_nonempty_list(entries: list[dict[str, Any]], field: str) -> list[Any]:
    for row in entries:
        values = _ensure_list(row.get(field))
        if values:
            return values
    return []


def _choose_anchor_entry(entries: list[dict[str, Any]]) -> dict[str, Any]:
    if not entries:
        return {}
    return sorted(
        entries,
        key=lambda row: (
            float(row.get("priority", 0.0) or 0.0),
            _clean_text(row.get("queue_id")),
        ),
        reverse=True,
    )[0]


def _concrete_theorem_candidate(execution_report: dict[str, Any]) -> dict[str, Any]:
    execution = _ensure_dict(execution_report.get("execution"))
    for row in _ensure_list(execution.get("theorem_candidates")):
        if not isinstance(row, dict):
            continue
        if _clean_text(row.get("concretization_status")) != "concrete":
            continue
        statement = _clean_text(row.get("statement"))
        if statement and not _is_schematic_statement(statement):
            return row
    return {}


def _self_contained_programme_headline(
    *,
    theorem_candidate: dict[str, Any],
    programme: dict[str, Any],
    branch_id: str,
    candidate_object: str,
) -> str:
    headline = _clean_text(theorem_candidate.get("title"))
    if headline and not _is_schematic_statement(headline) and not _contains_truncation(headline):
        return headline
    label = _clean_text(programme.get("target_label")) or f"Discovery programme {branch_id}"
    label = label.removesuffix(" Prompt")
    if candidate_object:
        return _clean_text(f"{label} theorem for {candidate_object}")
    return label


def _self_contained_route_synopsis(
    *,
    theorem_candidate: dict[str, Any],
    programme: dict[str, Any],
    source_id: str,
    target_id: str,
    source_excerpt: str,
    target_excerpt: str,
    candidate_object: str,
    invariant: str,
) -> str:
    motivation = _clean_text(theorem_candidate.get("motivation"))
    if motivation and not _is_schematic_statement(motivation) and not _contains_truncation(motivation):
        return motivation
    branch_move = _clean_text(programme.get("rationale")) or "Refine the routed discovery branch into a theorem-shaped local packet."
    lines = [
        f"Start from `{source_id}` with source content `{source_excerpt}`.",
        f"Reach `{target_id}` with target content `{target_excerpt}`.",
    ]
    if candidate_object:
        bridge_line = f"Use `{candidate_object}` as the local bridge object"
        if invariant:
            bridge_line += f" while preserving `{invariant}`"
        lines.append(bridge_line + ".")
    lines.append(f"Branch move: `{branch_move}`.")
    return _clean_text(" ".join(lines))


def _build_entry_from_expert_conjecture(package: dict[str, Any]) -> dict[str, Any]:
    bridge = _clean_text(package.get("branch_id"))
    linked_bridges = [_clean_text(value) for value in _ensure_list(package.get("linked_bridge_ids")) if _clean_text(value)]
    bridge_id = linked_bridges[0] if len(linked_bridges) == 1 else bridge
    exact_statement = _clean_text(package.get("exact_statement"))
    bridge_object = _ensure_dict(package.get("bridge_object"))
    first_lemma = _ensure_dict(package.get("first_nontrivial_lemma"))
    source_id = _clean_text(package.get("source_statement_id"))
    target_id = _clean_text(package.get("target_statement_id")) or bridge
    title = _clean_text(package.get("title")) or exact_statement
    packet_fields = normalize_expert_packet_fields(
        mode=package.get("restricted_regime_mode"),
        target_id=package.get("target_id"),
        bridge_name=bridge_object.get("name") or package.get("candidate_object"),
        invariant=bridge_object.get("invariant") or package.get("preserved_invariant"),
        first_nontrivial_lemma=first_lemma,
        negative_barrier_version=package.get("negative_barrier_version"),
        branch_to_definition=_ensure_dict(package.get("branch_to_definition")),
        proof_strategy_family=package.get("proof_strategy_family"),
        negative_route=package.get("negative_route"),
        failure_diagnosis=package.get("failure_diagnosis"),
        proof_obligations=package.get("proof_obligations"),
        candidate_lemmas=package.get("candidate_lemmas"),
    )
    entry = {
        "queue_key": make_queue_key(
            bridge_id=bridge_id or bridge,
            target_statement_id=target_id,
            claim_slug=f"expert-conjecture-{_clean_text(package.get('package_id'))}",
            claim_text=exact_statement,
        ),
        "title": title[:240],
        "priority": float(package.get("routing_priority", 0.0) or 0.0),
        "bridge_id": bridge_id or bridge,
        "claim_type": "expert-conjecture",
        "claim_text": exact_statement,
        "conjecture_statement": exact_statement,
        "source_statement_id": source_id,
        "target_statement_id": target_id,
        "source_excerpt": _clean_text(package.get("source_excerpt")),
        "target_excerpt": _clean_text(package.get("target_excerpt")),
        "route_synopsis": _clean_text(package.get("route_synopsis")),
        "candidate_object": _clean_text(bridge_object.get("name")) or _clean_text(package.get("candidate_object")),
        "carrier_kind": _clean_text(bridge_object.get("kind")),
        "bridge_object_definition": _clean_text(bridge_object.get("definition")),
        "preserved_invariant": _clean_text(bridge_object.get("invariant")) or _clean_text(package.get("preserved_invariant")),
        "missing_route_lemma": _clean_text(first_lemma.get("title")) or _clean_text(first_lemma.get("statement")),
        "first_nontrivial_lemma_title": _clean_text(first_lemma.get("title")),
        "first_nontrivial_lemma_statement": _clean_text(first_lemma.get("statement")),
        "discovery_branch_id": bridge,
        "linked_queue_ids": [_clean_text(value) for value in _ensure_list(package.get("linked_queue_ids")) if _clean_text(value)],
        "linked_bridge_ids": linked_bridges,
        "restricted_regime_mode": _clean_text(package.get("restricted_regime_mode")),
        "regime_and_quantifiers": _ensure_dict(package.get("regime_and_quantifiers")),
        "admissibility_conditions": _ensure_list(package.get("admissibility_conditions")),
        "proof_strategy_family": _clean_text(packet_fields.get("proof_strategy_family")),
        "negative_route": _clean_text(packet_fields.get("negative_route")),
        "failure_diagnosis": _clean_text(packet_fields.get("failure_diagnosis")),
        "proof_obligations": _ensure_list(packet_fields.get("proof_obligations")),
        "candidate_lemmas": _ensure_list(packet_fields.get("candidate_lemmas")),
        "independent_value_claim": _clean_text(package.get("independent_value_claim")),
        "negative_barrier_version": _clean_text(package.get("negative_barrier_version")),
        "expert_gate": _ensure_dict(package.get("expert_gate")),
        "branch_to_definition": _ensure_dict(package.get("branch_to_definition")),
        "foundation_search": _ensure_dict(package.get("foundation_search")),
        "theorem_package_id": _clean_text(package.get("package_id")),
        "concretization_status": "expert-grade",
        "concretization_score": int(_ensure_dict(package.get("expert_gate")).get("score", 0) or 0),
        "state_delta_kind": "expert-conjecture",
        "why_now": [
            "This conjecture cleared the expert-grade concretization gate after branch execution.",
            f"It packages the discovery branch `{bridge}` as a theorem an expert can inspect.",
            f"The first theorem-shaped obligation is `{_clean_text(first_lemma.get('title')) or _clean_text(first_lemma.get('statement'))}`.",
        ],
        "exploration_policy": "resume-from-expert-conjecture",
        "reopen_on_refresh": True,
    }
    entry["mathematical_layers"] = (
        _ensure_dict(package.get("mathematical_layers"))
        or build_mathematical_layers(
            title=title,
            exact_statement=exact_statement,
            route_synopsis=entry.get("route_synopsis"),
            bridge_name=entry.get("candidate_object"),
            invariant=entry.get("preserved_invariant"),
            mode=entry.get("restricted_regime_mode"),
            source_statement_id=source_id,
            target_statement_id=target_id,
            source_excerpt=entry.get("source_excerpt"),
            target_excerpt=entry.get("target_excerpt"),
            admissibility_conditions=entry.get("admissibility_conditions"),
            first_nontrivial_lemma_title=entry.get("first_nontrivial_lemma_title"),
            first_nontrivial_lemma_statement=entry.get("first_nontrivial_lemma_statement"),
            negative_barrier_version=entry.get("negative_barrier_version"),
        )
    )
    return entry


def _attach_governor_metadata(entry: dict[str, Any], decision: dict[str, Any], *, package_id: str = "") -> dict[str, Any]:
    if not entry or not decision:
        return entry
    entry["governor_decision"] = _clean_text(decision.get("decision"))
    entry["governor_value_score"] = float(decision.get("value_score", 0.0) or 0.0)
    entry["governor_value_band"] = _clean_text(decision.get("value_band"))
    entry["governor_rationale"] = _clean_text(decision.get("rationale"))
    entry["governor_major_subresult_candidate"] = bool(
        _ensure_dict(decision.get("major_subresult_assessment")).get("qualifies")
    )
    entry["governor_major_subresult_score"] = int(
        _ensure_dict(decision.get("major_subresult_assessment")).get("score_total", 0) or 0
    )
    if package_id:
        entry["governor_package_id"] = _clean_text(package_id)
    return entry


def _build_programme_entry(
    programme: dict[str, Any],
    branch: dict[str, Any],
    linked_entries: list[dict[str, Any]],
    execution_report: dict[str, Any],
) -> dict[str, Any]:
    anchor = _choose_anchor_entry(linked_entries)
    branch_id = _clean_text(programme.get("branch_id"))
    target_id = _clean_text(anchor.get("target_statement_id")) or branch_id
    source_id = _clean_text(anchor.get("source_statement_id"))
    candidate_object = _majority_value(linked_entries, "candidate_object")
    carrier_kind = _majority_value(linked_entries, "carrier_kind")
    bridge_object_definition = _majority_value(linked_entries, "bridge_object_definition")
    invariant = _majority_value(linked_entries, "preserved_invariant")
    proof_strategy_family = _majority_value(linked_entries, "proof_strategy_family")
    negative_route = _majority_value(linked_entries, "negative_route")
    failure_diagnosis = _majority_value(linked_entries, "failure_diagnosis")
    proof_obligations = _first_nonempty_list(linked_entries, "proof_obligations")
    candidate_lemmas = _first_nonempty_list(linked_entries, "candidate_lemmas")
    source_excerpt = _clean_text(anchor.get("source_excerpt"))
    target_excerpt = _clean_text(anchor.get("target_excerpt"))
    theorem_candidate = _concrete_theorem_candidate(execution_report)
    if not theorem_candidate:
        return {}
    linked_queue_ids = [_clean_text(value) for value in _ensure_list(branch.get("linked_queue_ids")) if _clean_text(value)]
    linked_bridges = sorted(
        {
            _clean_text(row.get("bridge_id"))
            for row in linked_entries
            if _clean_text(row.get("bridge_id"))
        }
    )
    candidate_object = _clean_text(theorem_candidate.get("candidate_object")) or candidate_object
    invariant = _clean_text(theorem_candidate.get("invariant")) or invariant
    headline = _self_contained_programme_headline(
        theorem_candidate=theorem_candidate,
        programme=programme,
        branch_id=branch_id,
        candidate_object=candidate_object,
    )
    title_prefix = _clean_text(programme.get("target_label")) or f"Discovery programme {branch_id}"
    title = headline if headline.lower().startswith(title_prefix.lower()) else _clean_text(f"{title_prefix}: {headline}")
    conjecture = _clean_text(theorem_candidate.get("statement")) or headline or _clean_text(programme.get("rationale"))
    route_synopsis = _self_contained_route_synopsis(
        theorem_candidate=theorem_candidate,
        programme=programme,
        source_id=source_id,
        target_id=target_id,
        source_excerpt=source_excerpt,
        target_excerpt=target_excerpt,
        candidate_object=candidate_object,
        invariant=invariant,
    )
    entry = {
        "queue_key": make_queue_key(
            bridge_id=branch_id,
            target_statement_id=target_id,
            claim_slug=f"branch-programme-{branch_id}",
            claim_text=conjecture,
        ),
        "title": title[:240],
        "priority": float(programme.get("routing_priority", 0.0) or 0.0),
        "bridge_id": branch_id,
        "claim_type": "branch-programme",
        "claim_text": conjecture,
        "conjecture_statement": conjecture,
        "source_statement_id": source_id,
        "target_statement_id": target_id,
        "source_excerpt": source_excerpt,
        "target_excerpt": target_excerpt,
        "route_synopsis": route_synopsis,
        "candidate_object": candidate_object,
        "carrier_kind": carrier_kind,
        "bridge_object_definition": bridge_object_definition,
        "preserved_invariant": invariant,
        "proof_strategy_family": proof_strategy_family,
        "missing_route_lemma": headline,
        "negative_route": negative_route,
        "failure_diagnosis": failure_diagnosis,
        "proof_obligations": proof_obligations or [headline],
        "candidate_lemmas": candidate_lemmas or [headline],
        "discovery_branch_id": branch_id,
        "linked_queue_ids": linked_queue_ids,
        "linked_bridge_ids": linked_bridges,
        "concretization_status": _clean_text(theorem_candidate.get("concretization_status")),
        "concretization_score": int(theorem_candidate.get("concretization_score", 0) or 0),
        "state_delta_kind": _clean_text(_ensure_dict(_ensure_dict(execution_report.get("execution")).get("state_delta")).get("delta_kind")),
        "why_now": [
            "This programme was promoted from a discovery branch only after a concrete theorem candidate was emitted.",
            f"It refines {len(linked_queue_ids)} blocked queue items through the branch `{branch_id}`.",
            f"The current prove target is `{headline}`.",
        ],
        "exploration_policy": "resume-from-discovery-programme",
        "reopen_on_refresh": True,
    }
    entry["mathematical_layers"] = build_mathematical_layers(
        title=title,
        exact_statement=conjecture,
        route_synopsis=route_synopsis,
        bridge_name=candidate_object,
        invariant=invariant,
        mode=_clean_text(programme.get("restricted_regime_mode")) or "special-case",
        source_statement_id=source_id,
        target_statement_id=target_id,
        source_excerpt=source_excerpt,
        target_excerpt=target_excerpt,
        admissibility_conditions=[],
        first_nontrivial_lemma_title=headline,
        first_nontrivial_lemma_statement=headline,
        negative_barrier_version=negative_route or failure_diagnosis,
    )
    return entry


def build_promotions(*, repo_root: Path, artifacts_dir: Path, kb_ref: str) -> dict[str, Any]:
    governor_json, _governor_md = discovery_governor_paths(artifacts_dir)
    governor_report = load_discovery_governor_report(governor_json, kb_ref=kb_ref)
    package_governance = expert_package_decision_index(governor_report)
    branch_governance = branch_decision_index(governor_report)
    expert_report = _load_json(_expert_conjecture_report_path(artifacts_dir))
    if expert_report:
        considered = 0
        suppressed = 0
        promoted_entries: list[dict[str, Any]] = []
        for package in _ensure_list(_ensure_dict(expert_report.get("agenda")).get("ready_for_prove")):
            if not isinstance(package, dict) or not bool(_ensure_dict(package.get("expert_gate")).get("passes")):
                continue
            considered += 1
            package_id = _clean_text(package.get("package_id"))
            decision = _ensure_dict(package_governance.get(package_id))
            if decision and _clean_text(decision.get("decision")) not in PROMOTION_ALLOWED_DECISIONS:
                suppressed += 1
                continue
            promoted = _build_entry_from_expert_conjecture(package)
            if promoted and decision:
                promoted = _attach_governor_metadata(promoted, decision, package_id=package_id)
            if promoted:
                promoted_entries.append(promoted)
        return {
            "metadata": {
                "kb_ref": kb_ref,
                "programme_count": len(promoted_entries),
                "source": "expert-conjectures",
                "considered_count": considered,
                "suppressed_by_governor": suppressed,
            },
            "entries": promoted_entries,
        }

    synthesis = _load_json(artifacts_dir / "discovery-branch-synthesis.json")
    branch_state = _load_json(artifacts_dir / "discovery-branch-queue.json")
    queue_json, _ = proof_queue_paths(repo_root, kb_ref)
    proof_queue = load_proof_queue(queue_json, kb_ref=kb_ref)

    branches_by_id = {
        _clean_text(row.get("branch_id")): row
        for row in _ensure_list(branch_state.get("branches"))
        if isinstance(row, dict)
    }
    queue_entries_by_id = {
        _clean_text(row.get("queue_id")): row
        for row in _ensure_list(proof_queue.get("entries"))
        if isinstance(row, dict)
    }
    promoted_entries: list[dict[str, Any]] = []
    considered = 0
    suppressed = 0
    for programme in _ensure_list(_ensure_dict(synthesis.get("agenda")).get("ready_for_prove")):
        if not isinstance(programme, dict):
            continue
        branch_id = _clean_text(programme.get("branch_id"))
        decision = _ensure_dict(branch_governance.get(branch_id))
        if decision:
            considered += 1
            if _clean_text(decision.get("decision")) not in {"deepen", "major_subresult_candidate"}:
                suppressed += 1
                continue
        branch = _ensure_dict(branches_by_id.get(branch_id))
        execution_report = _load_json(Path(_clean_text(programme.get("artifact_json")))) if _clean_text(programme.get("artifact_json")) else {}
        linked_entries = [
            _ensure_dict(queue_entries_by_id.get(_clean_text(queue_id)))
            for queue_id in _ensure_list(branch.get("linked_queue_ids"))
            if _clean_text(queue_entries_by_id.get(_clean_text(queue_id), {}).get("queue_id"))
        ]
        promoted = _build_programme_entry(programme, branch, linked_entries, execution_report)
        if promoted and decision:
            promoted = _attach_governor_metadata(promoted, decision)
        if promoted:
            promoted_entries.append(promoted)
    return {
        "metadata": {
            "kb_ref": kb_ref,
            "programme_count": len(promoted_entries),
            "source": "discovery-branch-synthesis",
            "considered_count": considered,
            "suppressed_by_governor": suppressed,
        },
        "entries": promoted_entries,
    }


def _defer_stale_branch_programmes(queue: dict[str, Any], *, active_branch_ids: set[str]) -> int:
    deferred = 0
    for row in _ensure_list(queue.get("entries")):
        if not isinstance(row, dict):
            continue
        if _clean_text(row.get("claim_type")) not in {"branch-programme", "expert-conjecture"}:
            continue
        branch_id = _clean_text(row.get("discovery_branch_id"))
        if branch_id in active_branch_ids:
            continue
        status = _clean_text(row.get("status")).lower()
        if status not in {"pending", "in_progress", "deferred"}:
            continue
        reason = (
            "Retired because an expert-grade discovery packet now carries the active prove frontier."
            if _clean_text(row.get("claim_type")) == "branch-programme"
            else "Retired because the latest discovery-to-theorem pass no longer promotes this expert packet on the active prove frontier."
        )
        row["status"] = "deferred"
        row["retired_from_active_frontier"] = True
        row["retired_reason"] = reason
        row["deferred_by"] = "inactive-discovery-frontier"
        row["deferred_reason"] = reason
        row["updated_utc"] = _utc_now()
        row["resolution_summary"] = reason
        deferred += 1
    return deferred


def apply_promotions(
    *,
    repo_root: Path,
    artifacts_dir: Path,
    kb_ref: str,
    report: dict[str, Any],
) -> tuple[dict[str, Any], int, int, int, tuple[Path, Path]]:
    queue_json, queue_md = proof_queue_paths(repo_root, kb_ref)
    queue = load_proof_queue(queue_json, kb_ref=kb_ref)
    added, updated = enqueue_entries(queue, _ensure_list(report.get("entries")))
    deferred = _defer_stale_branch_programmes(
        queue,
        active_branch_ids={
            _clean_text(row.get("discovery_branch_id"))
            for row in _ensure_list(report.get("entries"))
            if isinstance(row, dict)
        },
    )
    save_proof_queue(queue, json_path=queue_json, md_path=queue_md)
    refresh_summary_from_sources(
        repo_root=repo_root,
        artifacts_dir=artifacts_dir,
        kb_ref=kb_ref,
        queue=queue,
    )
    return queue, added, updated, deferred, (queue_json, queue_md)


def render_markdown(report: dict[str, Any], *, added: int, updated: int, deferred: int) -> str:
    meta = _ensure_dict(report.get("metadata"))
    lines = [
        "# Discovery Programme Promotions",
        "",
        f"- KB ref: {meta.get('kb_ref', '')}",
        f"- Programmes considered: {meta.get('programme_count', 0)}",
        f"- Added to proof queue: {added}",
        f"- Refreshed in proof queue: {updated}",
        f"- Deferred stale branch-programmes: {deferred}",
        "",
    ]
    for row in _ensure_list(report.get("entries")):
        if not isinstance(row, dict):
            continue
        lines.extend(
            [
                f"## {_clean_text(row.get('discovery_branch_id'))}",
                "",
                f"- Claim type: {row.get('claim_type', '')}",
                f"- Priority: {float(row.get('priority', 0.0) or 0.0):.3f}",
                f"- Conjecture: {row.get('conjecture_statement', '')}",
                f"- Route synopsis: {row.get('route_synopsis', '')}",
                f"- Candidate object: {row.get('candidate_object', '')}",
                f"- Invariant: {row.get('preserved_invariant', '')}",
                f"- Linked queue ids: {', '.join(_ensure_list(row.get('linked_queue_ids')))}",
                f"- Linked bridge ids: {', '.join(_ensure_list(row.get('linked_bridge_ids')))}",
                "",
            ]
        )
    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Promote theorem-shaped discovery programmes back into the proof queue.")
    parser.add_argument("--artifacts-dir", required=True, help="Path to artifacts/<kb-ref>.")
    parser.add_argument("--kb-ref", default="", help="Optional KB reference override.")
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parents[4]
    artifacts_dir = Path(args.artifacts_dir).expanduser().resolve()
    kb_ref = _clean_text(args.kb_ref) or kb_ref_from_artifacts_dir(artifacts_dir)
    if not kb_ref:
        raise SystemExit("Unable to determine kb_ref from artifacts directory; pass --kb-ref.")
    if not artifacts_dir.exists():
        artifacts_dir = canonical_artifacts_dir(repo_root, kb_ref)

    logger = ReasoningLogger("kb-discovery-programme-promoter", repo_root=repo_root)
    report = build_promotions(repo_root=repo_root, artifacts_dir=artifacts_dir, kb_ref=kb_ref)
    queue, added, updated, deferred, (queue_json, queue_md) = apply_promotions(
        repo_root=repo_root,
        artifacts_dir=artifacts_dir,
        kb_ref=kb_ref,
        report=report,
    )

    report_json, report_md = _programme_report_paths(artifacts_dir)
    report_json.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    report_md.write_text(render_markdown(report, added=added, updated=updated, deferred=deferred), encoding="utf-8")

    logger.step(
        "Promoted discovery programmes into the proof queue",
        details="\n".join(
            [
                f"kb_ref={kb_ref}",
                f"programme_count={int(_ensure_dict(report.get('metadata')).get('programme_count', 0) or 0)}",
                f"added={added}",
                f"updated={updated}",
                f"deferred={deferred}",
            ]
        ),
    )
    logger.add_output("discovery_programme_promotions_json", report_json)
    logger.add_output("discovery_programme_promotions_md", report_md)
    logger.add_output("proof_queue_json", queue_json)
    logger.add_output("proof_queue_md", queue_md)
    logger.finalize(
        status="success",
        summary=f"Promoted {added} discovery programmes, refreshed {updated}, and deferred {deferred} stale branch-programme entries for `{kb_ref}`.",
    )
    print(f"[OK] Wrote promotion JSON: {report_json}")
    print(f"[OK] Wrote promotion Markdown: {report_md}")
    print(f"[OK] Updated proof queue JSON: {queue_json}")
    print(f"[OK] Updated proof queue Markdown: {queue_md}")
    print(f"[LOG] {logger.log_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
