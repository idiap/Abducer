"""Context-indexed relevance gates, vector estimates, and Pareto selection."""

from __future__ import annotations

from typing import Any

from tdr.domain.models import bounded


DIMENSIONS = (
    "unblocking",
    "explanatory",
    "unification",
    "predictive",
    "transport",
    "pragmatic",
    "necessity",
    "robustness",
)
PENALTIES = ("complexity", "fragility", "auxiliaries", "risk")


def _explicit_or(value: dict[str, Any], name: str, fallback: float) -> float:
    explicit = value.get("metrics", {}).get(name)
    return bounded(fallback if explicit is None else explicit, fallback)


def evaluate_candidate(payload: dict[str, Any]) -> dict[str, Any]:
    candidate = dict(payload.get("candidate") or payload)
    context = dict(payload.get("context") or {})
    dependency = dict(payload.get("dependency_graph") or {})
    consequences = candidate.get("consequences", [])
    return_paths = candidate.get("return_paths", [])
    tasks = candidate.get("validation_tasks", [])
    pressure_ids = candidate.get("pressure_ids", [])
    patch = candidate.get("atlas_patch", {})
    mode = candidate.get("mode", "local")

    pressure_gate = bool(pressure_ids) and bool(context.get("question") or context.get("context_id") or payload.get("allow_implicit_context"))
    leverage_gate = bool(patch) and bool(consequences)
    return_gate = bool(return_paths) and any(item.get("method") for item in return_paths if isinstance(item, dict))

    reachable = len(set(dependency.get("reachable_from_pressure", [])))
    total_nodes = max(1, len(set(dependency.get("nodes", []))))
    raw = {
        "unblocking": min(1.0, 0.25 + 0.16 * len(pressure_ids) + reachable / total_nodes),
        "explanatory": min(1.0, 0.2 + 0.16 * sum("why" in str(item).lower() or "recover" in str(item).lower() for item in consequences)),
        "unification": min(1.0, 0.2 + 0.15 * len(patch.get("objects", [])) + (0.25 if mode in {"bridge", "mutation"} else 0.0)),
        "predictive": min(1.0, 0.15 + 0.18 * sum("held-out" in str(item).lower() or "novel" in str(item).lower() for item in consequences)),
        "transport": min(1.0, 0.15 + 0.18 * len(patch.get("morphisms", [])) + (0.25 if mode == "bridge" else 0.0)),
        "pragmatic": min(1.0, 0.12 + 0.18 * len(return_paths)),
        "necessity": min(1.0, 0.2 + 0.2 * bool(candidate.get("falsifiers")) + 0.15 * len(pressure_ids)),
        "robustness": min(1.0, 0.15 + 0.12 * len(tasks)),
    }
    vector = {name: round(_explicit_or(payload, name, score), 4) for name, score in raw.items()}
    assumptions = candidate.get("assumptions", [])
    uncertainty = candidate.get("uncertainty", {})
    penalties_raw = {
        "complexity": min(1.0, 0.1 + 0.08 * len(patch.get("objects", [])) + 0.08 * len(patch.get("morphisms", [])) + (0.25 if mode == "mutation" else 0.0)),
        "fragility": sum(float(value) for value in uncertainty.values()) / max(1, len(uncertainty)),
        "auxiliaries": min(1.0, 0.12 * len(assumptions)),
        "risk": 0.45 if mode == "mutation" else 0.2,
    }
    penalties = {name: round(_explicit_or(payload, name, score), 4) for name, score in penalties_raw.items()}
    weights = {name: float(context.get("relevance_weights", {}).get(name, 1.0)) for name in DIMENSIONS}
    penalty_weights = {name: float(context.get("penalty_weights", {}).get(name, 0.5)) for name in PENALTIES}
    positive = sum(weights[name] * vector[name] for name in DIMENSIONS) / max(1e-9, sum(weights.values()))
    negative = sum(penalty_weights[name] * penalties[name] for name in PENALTIES) / max(1e-9, sum(penalty_weights.values()))
    priority_index = round(bounded(positive - 0.45 * negative), 4)
    return {
        "candidate_id": candidate.get("candidate_id"),
        "gates": {
            "pressure": {"passed": pressure_gate, "reason": "addresses localized pressure" if pressure_gate else "no localized contextual pressure"},
            "leverage": {"passed": leverage_gate, "reason": "structural consequences declared" if leverage_gate else "no structural leverage"},
            "return": {"passed": return_gate, "reason": "concrete return path declared" if return_gate else "no concrete return path"},
        },
        "eligible": pressure_gate and leverage_gate and return_gate,
        "relevance_vector": vector,
        "penalties": penalties,
        "priority_index": priority_index,
        "epistemic_warning": "Priority guides validation effort; it is not evidence of truth or novelty.",
    }


def _dominates(left: dict[str, Any], right: dict[str, Any]) -> bool:
    lv, rv = left["relevance_vector"], right["relevance_vector"]
    lp, rp = left["penalties"], right["penalties"]
    no_worse = all(lv[name] >= rv[name] for name in DIMENSIONS) and all(lp[name] <= rp[name] for name in PENALTIES)
    strictly = any(lv[name] > rv[name] for name in DIMENSIONS) or any(lp[name] < rp[name] for name in PENALTIES)
    return no_worse and strictly


def pareto_frontier(evaluations: list[dict[str, Any]]) -> list[dict[str, Any]]:
    eligible = [item for item in evaluations if item.get("eligible")]
    frontier = [item for index, item in enumerate(eligible) if not any(_dominates(other, item) for j, other in enumerate(eligible) if j != index)]
    return sorted(frontier, key=lambda item: (-float(item.get("priority_index", 0.0)), str(item.get("candidate_id"))))

