#!/usr/bin/env python3
# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT

"""Persist a KB-scoped tree of explored search-space dimensions and route history."""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

_COMMON_DIR = Path(__file__).resolve().parents[3] / "common"
if str(_COMMON_DIR) not in sys.path:
    sys.path.insert(0, str(_COMMON_DIR))

from kb_context import kb_ref_from_artifacts_dir
from kb_context import normalize_kb_ref
from reasoning_log import ReasoningLogger
from search_space_tree import build_route_dimensions
from search_space_tree import compute_revisit_signal
from search_space_tree import load_search_space_state
from search_space_tree import route_content_fingerprint
from search_space_tree import route_signature


def _ensure_dict(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def _ensure_list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def _clean_text(value: Any, fallback: str = "") -> str:
    text = str(value or "").strip()
    return " ".join(text.split()) if text else fallback


def _safe_float(value: Any, default: float = 0.0) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def _load_json(path: Path) -> dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}
    return payload if isinstance(payload, dict) else {}


def _artifact_if_exists(artifacts_dir: Path, name: str) -> dict[str, Any]:
    path = artifacts_dir / name
    return _load_json(path) if path.exists() else {}


def _stable_digest(payload: Any) -> str:
    text = json.dumps(payload, sort_keys=True, ensure_ascii=False, separators=(",", ":"))
    return hashlib.sha1(text.encode("utf-8")).hexdigest()[:16]


def _group_by(rows: list[dict[str, Any]], key: str) -> dict[str, list[dict[str, Any]]]:
    out: dict[str, list[dict[str, Any]]] = {}
    for row in rows:
        value = _clean_text(row.get(key))
        if value:
            out.setdefault(value, []).append(row)
    return out


def _hypothesis_lookup(hyp_eval: dict[str, Any], hyp_loop: dict[str, Any]) -> dict[str, dict[str, Any]]:
    lookup: dict[str, dict[str, Any]] = {}
    for row in _ensure_list(hyp_eval.get("results")):
        if isinstance(row, dict) and _clean_text(row.get("hypothesis_id")):
            lookup[_clean_text(row.get("hypothesis_id"))] = row
    final_summary = _ensure_dict(hyp_loop.get("final_summary"))
    for hid in _ensure_list(final_summary.get("supported_ids")):
        hid_s = _clean_text(hid)
        if hid_s:
            lookup.setdefault(hid_s, {"hypothesis_id": hid_s})
            lookup[hid_s]["verdict"] = lookup[hid_s].get("verdict") or "supported"
            lookup[hid_s]["next_status"] = lookup[hid_s].get("next_status") or "supported"
    for hid in _ensure_list(final_summary.get("refuted_ids")):
        hid_s = _clean_text(hid)
        if hid_s:
            lookup.setdefault(hid_s, {"hypothesis_id": hid_s})
            lookup[hid_s]["verdict"] = lookup[hid_s].get("verdict") or "refuted"
            lookup[hid_s]["next_status"] = lookup[hid_s].get("next_status") or "refuted"
    for hid in _ensure_list(final_summary.get("unresolved_ids")):
        hid_s = _clean_text(hid)
        if hid_s:
            lookup.setdefault(hid_s, {"hypothesis_id": hid_s})
            lookup[hid_s]["verdict"] = lookup[hid_s].get("verdict") or "inconclusive"
            lookup[hid_s]["next_status"] = lookup[hid_s].get("next_status") or "needs-testing"
    return lookup


def _status_counts(hypothesis_ids: list[str], hypothesis_lookup: dict[str, dict[str, Any]]) -> dict[str, int]:
    counts = {"supported": 0, "refuted": 0, "open": 0, "inconclusive": 0}
    for hid in hypothesis_ids:
        row = hypothesis_lookup.get(hid, {})
        verdict = _clean_text(row.get("verdict"))
        next_status = _clean_text(row.get("next_status"))
        if verdict == "supported" or next_status == "supported":
            counts["supported"] += 1
        elif verdict == "refuted" or next_status == "refuted":
            counts["refuted"] += 1
        elif verdict == "inconclusive":
            counts["inconclusive"] += 1
            counts["open"] += 1
        elif next_status in {"needs-testing", "open", "unresolved"}:
            counts["open"] += 1
    return counts


def _has_underspecification(bridge: dict[str, Any], conjectures: list[dict[str, Any]], proofs: list[dict[str, Any]]) -> bool:
    if _clean_text(_ensure_dict(bridge.get("statement_delta")).get("typing_status")) == "underspecified":
        return True
    for row in [*conjectures, *proofs]:
        typing_status = _clean_text(row.get("typing_status"))
        label = _clean_text(row.get("abstraction_label") or row.get("conjectured_object"))
        carrier = _clean_text(row.get("carrier_kind"))
        if typing_status and typing_status != "typed":
            return True
        if "unspecified" in label.lower() or "underspecified" in label.lower():
            return True
        if "unspecified" in carrier.lower() or "underspecified" in carrier.lower():
            return True
    return False


def _route_outcome(
    *,
    hypothesis_counts: dict[str, int],
    conjecture_count: int,
    proof_count: int,
    underspecified: bool,
    prior_branch: dict[str, Any] | None,
    content_fingerprint: str,
    run_id: str,
) -> str:
    if hypothesis_counts.get("supported", 0) > 0:
        return "promising"
    if hypothesis_counts.get("refuted", 0) > 0 and hypothesis_counts.get("supported", 0) == 0:
        return "refuted"
    current = "underspecified" if underspecified else "open" if (conjecture_count or proof_count) else "unexplored"
    prior = prior_branch if isinstance(prior_branch, dict) else {}
    same_content = _clean_text(prior.get("content_fingerprint")) == _clean_text(content_fingerprint)
    prior_outcome = _clean_text(prior.get("latest_outcome"))
    prior_run = _clean_text(prior.get("last_seen_run_id"))
    if current in {"open", "underspecified"} and same_content and prior_outcome in {"open", "underspecified", "stalled"} and prior_run and prior_run != run_id:
        return "stalled"
    return current


def _exploration_policy(outcome: str) -> str:
    if outcome == "promising":
        return "resume-with-deeper-proof"
    if outcome == "open":
        return "continue"
    if outcome == "underspecified":
        return "re-encode-before-retrying"
    if outcome == "stalled":
        return "deprioritize-until-new-representation"
    if outcome == "refuted":
        return "hold"
    return "await-more-structure"


def _route_priority(bridge: dict[str, Any], expert_row: dict[str, Any], proofs: list[dict[str, Any]]) -> float:
    if expert_row:
        return _safe_float(expert_row.get("priority"))
    proof_best = max((_safe_float(row.get("sketch_score")) for row in proofs if isinstance(row, dict)), default=0.0)
    return max(_safe_float(bridge.get("effective_bridge_score")), proof_best, _safe_float(bridge.get("bridge_score")))


def _build_route_rows(
    *,
    bridges: list[dict[str, Any]],
    conjectures: list[dict[str, Any]],
    proofs: list[dict[str, Any]],
    expert_lookup: dict[str, dict[str, Any]],
    hypothesis_lookup: dict[str, dict[str, Any]],
    state: dict[str, Any],
    kb_ref: str,
    run_id: str,
    generated_utc: str,
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    conjectures_by_bridge = _group_by(conjectures, "bridge_id")
    proofs_by_bridge = _group_by(proofs, "bridge_id")
    proofs_by_conjecture = _group_by(proofs, "conjecture_id")
    prior_branches = _ensure_dict(state.get("branches"))
    updated_branches = {str(k): dict(v) for k, v in prior_branches.items() if isinstance(v, dict)}
    route_rows: list[dict[str, Any]] = []

    for bridge in bridges:
        if not isinstance(bridge, dict) or not _clean_text(bridge.get("bridge_id")):
            continue
        bridge_id = _clean_text(bridge.get("bridge_id"))
        bridge_commitment = _ensure_dict(bridge.get("inferential_commitment"))
        bridge_delta = _ensure_dict(bridge.get("statement_delta"))
        bridge_conjectures = [row for row in conjectures_by_bridge.get(bridge_id, []) if isinstance(row, dict)]
        bridge_proofs = [row for row in proofs_by_bridge.get(bridge_id, []) if isinstance(row, dict)]
        expert_row = expert_lookup.get(bridge_id, {})

        dimensions = build_route_dimensions(
            source_statement_id=_clean_text(bridge.get("from_id")),
            target_statement_id=_clean_text(bridge.get("to_id")),
            bridge_type=_clean_text(bridge.get("bridge_type"), "structural route"),
            statement_delta=bridge_delta,
            inferential_commitment=bridge_commitment,
        )
        route_sig = _clean_text(_ensure_dict(bridge.get("search_space_state")).get("route_signature")) or route_signature(dimensions)
        base_fingerprint = _clean_text(_ensure_dict(bridge.get("search_space_state")).get("content_fingerprint")) or route_content_fingerprint(
            route_signature_value=route_sig,
            statement_delta=bridge_delta,
            bridge_object_label=_clean_text(bridge_delta.get("typed_object_expectation")),
        )
        object_labels = sorted({_clean_text(row.get("abstraction_label") or row.get("conjectured_object")) for row in [*bridge_conjectures, *bridge_proofs] if _clean_text(row.get("abstraction_label") or row.get("conjectured_object"))})
        proof_families = sorted({_clean_text(row.get("proof_strategy_family")) for row in bridge_proofs if _clean_text(row.get("proof_strategy_family"))})
        realization_fingerprint = _stable_digest({"base": base_fingerprint, "objects": object_labels, "proofs": proof_families})

        hypothesis_ids: list[str] = []
        bridge_hyp = _clean_text(bridge_commitment.get("hypothesis_id"))
        if bridge_hyp:
            hypothesis_ids.append(bridge_hyp)
        for row in bridge_proofs:
            for hid in _ensure_list(row.get("hypothesis_ids")):
                hid_s = _clean_text(hid)
                if hid_s and hid_s not in hypothesis_ids:
                    hypothesis_ids.append(hid_s)
        for hid in _ensure_list(expert_row.get("linked_hypothesis_ids")):
            hid_s = _clean_text(hid)
            if hid_s and hid_s not in hypothesis_ids:
                hypothesis_ids.append(hid_s)

        counts = _status_counts(hypothesis_ids, hypothesis_lookup)
        prior_branch = _ensure_dict(updated_branches.get(route_sig))
        outcome = _route_outcome(
            hypothesis_counts=counts,
            conjecture_count=len(bridge_conjectures),
            proof_count=len(bridge_proofs),
            underspecified=_has_underspecification(bridge, bridge_conjectures, bridge_proofs),
            prior_branch=prior_branch,
            content_fingerprint=base_fingerprint,
            run_id=run_id,
        )
        revisit = compute_revisit_signal(prior_branch, base_fingerprint)
        priority = _route_priority(bridge, expert_row, bridge_proofs)
        policy = _exploration_policy(outcome)
        visit_count = int(prior_branch.get("visit_count", 0) or 0) + (0 if _clean_text(prior_branch.get("last_seen_run_id")) == run_id else 1)
        run_row = {
            "run_id": run_id,
            "seen_utc": generated_utc,
            "outcome": outcome,
            "priority": round(priority, 4),
            "conjecture_ids": [_clean_text(row.get("conjecture_id")) for row in bridge_conjectures if _clean_text(row.get("conjecture_id"))],
            "proof_sketch_ids": [_clean_text(row.get("sketch_id")) for row in bridge_proofs if _clean_text(row.get("sketch_id"))],
            "hypothesis_ids": hypothesis_ids,
            "content_fingerprint": base_fingerprint,
            "realization_fingerprint": realization_fingerprint,
        }
        run_history = [row for row in _ensure_list(prior_branch.get("run_history")) if isinstance(row, dict)]
        if run_history and _clean_text(run_history[-1].get("run_id")) == run_id:
            run_history[-1] = run_row
        else:
            run_history.append(run_row)
        updated_branches[route_sig] = {
            "route_signature": route_sig,
            "kb_ref": kb_ref,
            "bridge_id": bridge_id,
            "source_statement_id": dimensions["source_statement_id"],
            "target_statement_id": dimensions["target_statement_id"],
            "bridge_type": dimensions["bridge_type"],
            "dimensions": dimensions,
            "route_synopsis": _clean_text(bridge_delta.get("route_synopsis"), dimensions["route_label"]),
            "content_fingerprint": base_fingerprint,
            "realization_fingerprint": realization_fingerprint,
            "latest_outcome": outcome,
            "exploration_policy": policy,
            "priority": round(priority, 4),
            "visit_count": visit_count,
            "first_seen_utc": _clean_text(prior_branch.get("first_seen_utc"), generated_utc),
            "last_seen_utc": generated_utc,
            "last_seen_run_id": run_id,
            "hypothesis_counts": counts,
            "conjecture_count": len(bridge_conjectures),
            "proof_sketch_count": len(bridge_proofs),
            "run_history": run_history[-12:],
        }

        route_rows.append(
            {
                "route_signature": route_sig,
                "bridge_id": bridge_id,
                "priority": round(priority, 4),
                "outcome": outcome,
                "exploration_policy": policy,
                "revisit_status": _clean_text(revisit.get("revisit_status")),
                "visit_count": visit_count,
                "bridge_score": round(_safe_float(bridge.get("bridge_score")), 4),
                "effective_bridge_score": round(_safe_float(bridge.get("effective_bridge_score"), _safe_float(bridge.get("bridge_score"))), 4),
                "source_statement_id": dimensions["source_statement_id"],
                "target_statement_id": dimensions["target_statement_id"],
                "bridge_type": dimensions["bridge_type"],
                "dimensions": dimensions,
                "route_synopsis": _clean_text(bridge_delta.get("route_synopsis"), dimensions["route_label"]),
                "hypothesis_counts": counts,
                "conjectures": [
                    {
                        "conjecture_id": _clean_text(conj.get("conjecture_id")),
                        "label": _clean_text(conj.get("abstraction_label"), "candidate object"),
                        "abstraction_type": _clean_text(conj.get("abstraction_type")),
                        "carrier_kind": _clean_text(conj.get("carrier_kind")),
                        "typing_status": _clean_text(conj.get("typing_status"), "untyped"),
                        "proofs": [
                            {
                                "sketch_id": _clean_text(psk.get("sketch_id")),
                                "title": _clean_text(psk.get("title"), _clean_text(psk.get("sketch_id"), "proof sketch")),
                                "proof_strategy_family": _clean_text(psk.get("proof_strategy_family"), "untyped family"),
                                "sketch_score": round(_safe_float(psk.get("sketch_score")), 4),
                            }
                            for psk in proofs_by_conjecture.get(_clean_text(conj.get("conjecture_id")), [])
                            if isinstance(psk, dict)
                        ],
                    }
                    for conj in bridge_conjectures
                ],
                "proof_sketch_count": len(bridge_proofs),
            }
        )

    route_rows.sort(key=lambda row: (row.get("priority", 0.0), row.get("effective_bridge_score", 0.0)), reverse=True)
    metadata = _ensure_dict(state.get("metadata"))
    seen_run_ids = [_clean_text(item) for item in _ensure_list(metadata.get("seen_run_ids")) if _clean_text(item)]
    if run_id and run_id not in seen_run_ids:
        seen_run_ids.append(run_id)
    new_state = {
        "metadata": {
            **metadata,
            "state_version": 1,
            "kb_ref": kb_ref,
            "created_utc": _clean_text(metadata.get("created_utc"), generated_utc),
            "updated_utc": generated_utc,
            "branch_count": len(updated_branches),
            "run_count": len(seen_run_ids),
            "seen_run_ids": seen_run_ids[-20:],
        },
        "branches": updated_branches,
    }
    return route_rows, new_state


def _empty_stats() -> dict[str, int]:
    return {
        "route_count": 0,
        "conjecture_count": 0,
        "proof_sketch_count": 0,
        "supported_hypothesis_count": 0,
        "refuted_hypothesis_count": 0,
        "open_hypothesis_count": 0,
    }


def _make_node(kind: str, label: str, dimension: str = "", value: str = "") -> dict[str, Any]:
    return {"kind": kind, "label": label, "dimension": dimension, "value": value, "stats": _empty_stats(), "children": []}


def _find_or_create_child(parent: dict[str, Any], *, kind: str, label: str, dimension: str = "", value: str = "") -> dict[str, Any]:
    for child in _ensure_list(parent.get("children")):
        if isinstance(child, dict) and _clean_text(child.get("kind")) == kind and _clean_text(child.get("dimension")) == dimension and _clean_text(child.get("value")) == value:
            return child
    child = _make_node(kind, label, dimension, value)
    parent.setdefault("children", []).append(child)
    return child


def _aggregate_tree_stats(node: dict[str, Any]) -> dict[str, Any]:
    stats = {key: int(_ensure_dict(node.get("stats")).get(key, 0) or 0) for key in _empty_stats()}
    for child in _ensure_list(node.get("children")):
        if not isinstance(child, dict):
            continue
        child_stats = _aggregate_tree_stats(child)
        for key in stats:
            stats[key] += int(child_stats.get(key, 0) or 0)
    node["stats"] = stats
    return stats


def _build_tree(route_rows: list[dict[str, Any]]) -> dict[str, Any]:
    root = _make_node("root", "search-space")
    for route in route_rows:
        dims = _ensure_dict(route.get("dimensions"))
        problem_node = _find_or_create_child(root, kind="dimension", label=_clean_text(dims.get("source_problem_family"), "unspecified"), dimension="problem-family", value=_clean_text(dims.get("source_problem_family"), "unspecified"))
        model_node = _find_or_create_child(problem_node, kind="dimension", label=_clean_text(dims.get("model_shift"), "model shift not yet typed"), dimension="model-shift", value=_clean_text(dims.get("model_shift"), "model shift not yet typed"))
        payoff_node = _find_or_create_child(model_node, kind="dimension", label=_clean_text(dims.get("target_payoff"), "target payoff not yet typed"), dimension="target-payoff", value=_clean_text(dims.get("target_payoff"), "target payoff not yet typed"))
        invariant_node = _find_or_create_child(payoff_node, kind="dimension", label=_clean_text(dims.get("preserved_invariant"), "support-to-target interface"), dimension="invariant", value=_clean_text(dims.get("preserved_invariant"), "support-to-target interface"))
        route_node = _find_or_create_child(invariant_node, kind="route", label=f"{route.get('source_statement_id', '')} -> {route.get('target_statement_id', '')}", dimension="route", value=_clean_text(route.get("route_signature")))
        route_node["details"] = {
            "bridge_id": _clean_text(route.get("bridge_id")),
            "priority": route.get("priority", 0.0),
            "outcome": _clean_text(route.get("outcome")),
            "policy": _clean_text(route.get("exploration_policy")),
            "visit_count": int(route.get("visit_count", 0) or 0),
            "route_synopsis": _clean_text(route.get("route_synopsis")),
        }
        route_node["stats"] = {
            "route_count": 1,
            "conjecture_count": len(_ensure_list(route.get("conjectures"))),
            "proof_sketch_count": int(route.get("proof_sketch_count", 0) or 0),
            "supported_hypothesis_count": int(_ensure_dict(route.get("hypothesis_counts")).get("supported", 0) or 0),
            "refuted_hypothesis_count": int(_ensure_dict(route.get("hypothesis_counts")).get("refuted", 0) or 0),
            "open_hypothesis_count": int(_ensure_dict(route.get("hypothesis_counts")).get("open", 0) or 0),
        }
        route_node["children"] = []
        for conjecture in _ensure_list(route.get("conjectures")):
            if not isinstance(conjecture, dict):
                continue
            object_node = _find_or_create_child(route_node, kind="candidate-object", label=_clean_text(conjecture.get("label"), "candidate object"), dimension="candidate-object", value=_clean_text(conjecture.get("conjecture_id")) or _clean_text(conjecture.get("label"), "candidate object"))
            object_node["details"] = {
                "conjecture_id": _clean_text(conjecture.get("conjecture_id")),
                "abstraction_type": _clean_text(conjecture.get("abstraction_type")),
                "carrier_kind": _clean_text(conjecture.get("carrier_kind")),
            }
            object_node["stats"] = {"route_count": 0, "conjecture_count": 1, "proof_sketch_count": len(_ensure_list(conjecture.get("proofs"))), "supported_hypothesis_count": 0, "refuted_hypothesis_count": 0, "open_hypothesis_count": 0}
            object_node["children"] = []
            for proof in _ensure_list(conjecture.get("proofs")):
                if not isinstance(proof, dict):
                    continue
                proof_node = _find_or_create_child(object_node, kind="proof-sketch", label=_clean_text(proof.get("title"), _clean_text(proof.get("sketch_id"), "proof sketch")), dimension="proof-family", value=_clean_text(proof.get("sketch_id")))
                proof_node["details"] = {"sketch_id": _clean_text(proof.get("sketch_id")), "proof_strategy_family": _clean_text(proof.get("proof_strategy_family")), "sketch_score": proof.get("sketch_score", 0.0)}
                proof_node["stats"] = {"route_count": 0, "conjecture_count": 0, "proof_sketch_count": 1, "supported_hypothesis_count": 0, "refuted_hypothesis_count": 0, "open_hypothesis_count": 0}
                proof_node["children"] = []
    _aggregate_tree_stats(root)
    return root


def _frontier(route_rows: list[dict[str, Any]]) -> dict[str, list[dict[str, Any]]]:
    resume: list[dict[str, Any]] = []
    deprioritized: list[dict[str, Any]] = []
    for row in route_rows:
        item = {
            "route_signature": _clean_text(row.get("route_signature")),
            "bridge_id": _clean_text(row.get("bridge_id")),
            "label": f"{row.get('source_statement_id', '')} -> {row.get('target_statement_id', '')}",
            "priority": round(_safe_float(row.get("priority")), 4),
            "outcome": _clean_text(row.get("outcome")),
            "policy": _clean_text(row.get("exploration_policy")),
            "visit_count": int(row.get("visit_count", 0) or 0),
            "route_synopsis": _clean_text(row.get("route_synopsis")),
        }
        (deprioritized if item["policy"] in {"deprioritize-until-new-representation", "hold"} else resume).append(item)
    resume.sort(key=lambda row: row.get("priority", 0.0), reverse=True)
    deprioritized.sort(key=lambda row: row.get("priority", 0.0), reverse=True)
    return {"resume": resume[:10], "deprioritized": deprioritized[:10]}


def _build_report(*, artifacts_dir: Path, kb_ref: str, run_id: str, state_path: Path, state: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    generated_utc = dt.datetime.now(dt.UTC).isoformat()
    bridge_report = _artifact_if_exists(artifacts_dir, "bridge-plan.json")
    conjecture_report = _artifact_if_exists(artifacts_dir, "concept-gap-abstractions.json")
    proof_report = _artifact_if_exists(artifacts_dir, "proof-sketches.json")
    hyp_eval_report = _artifact_if_exists(artifacts_dir, "hypothesis-evaluation.json")
    hyp_loop_report = _artifact_if_exists(artifacts_dir, "hypothesis-refutation-loop.json")
    expert_report = _artifact_if_exists(artifacts_dir, "expert-hypothesis-paper.json")
    bridges = [row for row in _ensure_list(bridge_report.get("bridge_programs")) if isinstance(row, dict)]
    conjectures = [row for row in _ensure_list(conjecture_report.get("abstraction_conjectures")) if isinstance(row, dict)]
    proofs = [row for row in _ensure_list(proof_report.get("proof_sketches")) if isinstance(row, dict)]
    expert_lookup = { _clean_text(row.get("bridge_id")): row for row in _ensure_list(expert_report.get("bridge_portfolio")) if isinstance(row, dict) and _clean_text(row.get("bridge_id")) }
    hypothesis_lookup = _hypothesis_lookup(hyp_eval_report, hyp_loop_report)
    route_rows, new_state = _build_route_rows(
        bridges=bridges,
        conjectures=conjectures,
        proofs=proofs,
        expert_lookup=expert_lookup,
        hypothesis_lookup=hypothesis_lookup,
        state=state,
        kb_ref=kb_ref,
        run_id=run_id,
        generated_utc=generated_utc,
    )
    report = {
        "metadata": {
            "kb_ref": kb_ref,
            "generated_utc": generated_utc,
            "run_id": run_id,
            "artifacts_dir": str(artifacts_dir),
            "state_path": str(state_path),
            "route_count": len(route_rows),
            "state_branch_count": len(_ensure_dict(new_state.get("branches"))),
            "loaded_artifacts": {
                "bridge-plan": bool(bridges),
                "concept-gap-abstractions": bool(conjectures),
                "proof-sketches": bool(proofs),
                "hypothesis-evaluation": bool(hypothesis_lookup),
                "expert-paper": bool(expert_lookup),
            },
        },
        "frontier": _frontier(route_rows),
        "routes": route_rows,
        "tree": _build_tree(route_rows),
        "persistence": {
            "state_branch_count": len(_ensure_dict(new_state.get("branches"))),
            "run_count": int(_ensure_dict(new_state.get("metadata")).get("run_count", 0) or 0),
        },
    }
    return report, new_state


def _render_tree_markdown(node: dict[str, Any], depth: int = 0) -> list[str]:
    indent = "  " * depth
    label = _clean_text(node.get("label"), "node")
    details = _ensure_dict(node.get("details"))
    stats = _ensure_dict(node.get("stats"))
    suffix = ""
    if _clean_text(node.get("kind")) == "route":
        suffix = f" [outcome={_clean_text(details.get('outcome'))}; policy={_clean_text(details.get('policy'))}; visits={int(details.get('visit_count', 0) or 0)}]"
    elif _clean_text(node.get("kind")) == "dimension":
        suffix = f" [routes={int(stats.get('route_count', 0) or 0)}]"
    lines = [f"{indent}- {label}{suffix}"]
    for child in _ensure_list(node.get("children")):
        if isinstance(child, dict):
            lines.extend(_render_tree_markdown(child, depth + 1))
    return lines


def _to_markdown(report: dict[str, Any]) -> str:
    meta = _ensure_dict(report.get("metadata"))
    frontier = _ensure_dict(report.get("frontier"))
    lines = [
        "# Search-Space Tree",
        "",
        "## Summary",
        "",
        f"- KB reference: {meta.get('kb_ref', '')}",
        f"- Run ID: {meta.get('run_id', '')}",
        f"- Generated UTC: {meta.get('generated_utc', '')}",
        f"- Route count: {meta.get('route_count', 0)}",
        f"- Persistent state path: {meta.get('state_path', '')}",
        f"- Persistent branches tracked: {_ensure_dict(report.get('persistence')).get('state_branch_count', 0)}",
        "",
        "## Resume Frontier",
        "",
    ]
    resume = _ensure_list(frontier.get("resume"))
    if not resume:
        lines.append("- No bridge-level routes are available yet; the tree will deepen once bridge planning artifacts exist.")
    else:
        for row in resume:
            lines.append(f"- {row.get('bridge_id', '')}: {row.get('label', '')} (priority={row.get('priority', 0.0)}, outcome={row.get('outcome', '')}, policy={row.get('policy', '')})")
            lines.append(f"  - {row.get('route_synopsis', '')}")
    lines.extend(["", "## Deprioritized Frontier", ""])
    deprioritized = _ensure_list(frontier.get("deprioritized"))
    if not deprioritized:
        lines.append("- No routes are currently marked as deprioritized or held.")
    else:
        for row in deprioritized:
            lines.append(f"- {row.get('bridge_id', '')}: {row.get('label', '')} (priority={row.get('priority', 0.0)}, outcome={row.get('outcome', '')}, visits={row.get('visit_count', 0)})")
    lines.extend(["", "## Tree", ""])
    lines.extend(_render_tree_markdown(_ensure_dict(report.get("tree"))))
    return "\n".join(lines) + "\n"


def main() -> int:
    logger = ReasoningLogger("kb-search-space-tree")
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--artifacts-dir", required=True, help="Path to artifacts/<kb-ref> directory.")
    ap.add_argument("--kb-ref", default="", help="Optional canonical KB reference.")
    ap.add_argument("--run-id", default="", help="Optional orchestrator run ID.")
    ap.add_argument("--state-json", default="", help="Optional persistent search-space state JSON path.")
    ap.add_argument("--output-json", default="", help="Output path for search-space tree JSON.")
    ap.add_argument("--output-md", default="", help="Output path for search-space tree Markdown.")
    args = ap.parse_args()

    repo_root = Path(__file__).resolve().parents[4]
    artifacts_dir = Path(args.artifacts_dir)
    if not artifacts_dir.is_absolute():
        artifacts_dir = (repo_root / artifacts_dir).resolve()
    kb_ref = normalize_kb_ref(args.kb_ref) or kb_ref_from_artifacts_dir(artifacts_dir)
    run_id = _clean_text(args.run_id or logger.run_id, logger.run_id)
    state_path = Path(args.state_json) if args.state_json else repo_root / "artifacts" / "search-space-state" / f"{kb_ref}.json"
    output_json = Path(args.output_json) if args.output_json else artifacts_dir / "search-space-tree.json"
    output_md = Path(args.output_md) if args.output_md else artifacts_dir / "search-space-tree.md"
    if not state_path.is_absolute():
        state_path = (repo_root / state_path).resolve()
    if not output_json.is_absolute():
        output_json = (repo_root / output_json).resolve()
    if not output_md.is_absolute():
        output_md = (repo_root / output_md).resolve()

    logger.step("Parsed search-space-tree arguments", "\n".join([f"artifacts_dir={artifacts_dir}", f"kb_ref={kb_ref}", f"run_id={run_id}", f"state_json={state_path}", f"output_json={output_json}", f"output_md={output_md}"]), surface_focus="search-space-tree", surface_stage="search-space-tree")
    if not artifacts_dir.exists():
        log_path = logger.finalize("error", summary=f"Artifacts directory not found: {artifacts_dir}")
        print(f"[LOG] {log_path}", file=sys.stderr)
        raise SystemExit(f"[ERROR] Artifacts directory not found: {artifacts_dir}")

    state = load_search_space_state(state_path, kb_ref=kb_ref)
    report, new_state = _build_report(artifacts_dir=artifacts_dir, kb_ref=kb_ref, run_id=run_id, state_path=state_path, state=state)
    output_json.parent.mkdir(parents=True, exist_ok=True)
    output_md.parent.mkdir(parents=True, exist_ok=True)
    state_path.parent.mkdir(parents=True, exist_ok=True)
    output_json.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    output_md.write_text(_to_markdown(report), encoding="utf-8")
    state_path.write_text(json.dumps(new_state, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    logger.step("Built persistent search-space tree", "\n".join([f"route_count={_ensure_dict(report.get('metadata')).get('route_count', 0)}", f"resume_frontier={len(_ensure_list(_ensure_dict(report.get('frontier')).get('resume')))}", f"state_branch_count={_ensure_dict(report.get('persistence')).get('state_branch_count', 0)}"]), surface_focus="search-space-tree", surface_stage="search-space-tree", surface_metrics={"route_count": _ensure_dict(report.get("metadata")).get("route_count", 0), "resume_frontier_count": len(_ensure_list(_ensure_dict(report.get("frontier")).get("resume"))), "state_branch_count": _ensure_dict(report.get("persistence")).get("state_branch_count", 0)}, surface_taxonomy={"reasoning_types": ["search-space-persistence", "search-space-tree"]})
    logger.add_output("search_space_tree_json", output_json)
    logger.add_output("search_space_tree_md", output_md)
    logger.add_output("search_space_state_json", state_path)
    log_path = logger.finalize("success", summary=f"Generated persistent search-space tree with {_ensure_dict(report.get('metadata')).get('route_count', 0)} route branches.")
    print(f"[OK] Wrote search-space tree JSON: {output_json}")
    print(f"[OK] Wrote search-space tree Markdown: {output_md}")
    print(f"[OK] Updated persistent state: {state_path}")
    print(f"[LOG] {log_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
