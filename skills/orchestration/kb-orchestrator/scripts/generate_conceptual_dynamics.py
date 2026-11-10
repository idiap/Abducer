#!/usr/bin/env python3
# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT

"""Build a conceptual-dynamics dashboard from surfaced reasoning logs and stage artifacts."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import math
import re
import sys
from collections import Counter
from collections import defaultdict
from pathlib import Path
from typing import Any

import yaml

_COMMON_DIR = Path(__file__).resolve().parents[3] / "common"
if str(_COMMON_DIR) not in sys.path:
    sys.path.insert(0, str(_COMMON_DIR))

from kb_context import kb_ref_from_artifacts_dir
from kb_context import normalize_kb_ref
from reasoning_log import ReasoningLogger

from generate_reasoning_surface_index import _load_surfaces


STAGE_ORDER = [
    "connect.analyze",
    "connect.generate-phyp",
    "coherence-eval",
    "concept-evolution",
    "entrypoints.rank",
    "entrypoints.pathways",
    "hardness",
    "bridge-plan",
    "conjecture",
    "strategies",
    "proof-sketch",
    "hypothesis-eval",
    "hypothesis-loop",
    "revision-loop",
    "interpretation-reports",
    "conceptual-dynamics",
    "process-graph",
    "reasoning-dynamics",
    "expert-paper",
]

STAGE_REASONING_TYPES = {
    "connect.analyze": ["structural-analysis", "intervention-ranking", "concept-mapping"],
    "connect.generate-phyp": ["hypothesis-generation"],
    "coherence-eval": ["coherence-evaluation", "theory-fit-assessment"],
    "concept-evolution": ["concept-phase-tracing"],
    "entrypoints.rank": ["entrypoint-localization"],
    "entrypoints.pathways": ["pathway-synthesis"],
    "hardness": ["hardness-diagnosis", "obstruction-analysis"],
    "bridge-plan": ["bridge-construction", "interface-design"],
    "conjecture": ["bridge-object-design", "counterfactual-probing"],
    "strategies": ["strategy-diversification", "novelty-search"],
    "proof-sketch": ["proof-formalization", "obligation-analysis"],
    "hypothesis-eval": ["hypothesis-testing", "evidence-weighting"],
    "hypothesis-loop": ["iterative-refutation", "belief-revision"],
    "revision-loop": ["ontology-revision", "representation-repair"],
    "interpretation-reports": ["interpretive-synthesis"],
    "conceptual-dynamics": ["conceptual-monitoring"],
    "process-graph": ["process-visualization"],
    "reasoning-dynamics": ["quantitative-monitoring"],
    "expert-paper": ["expert-synthesis"],
}

TARGET_ROLES = {
    "target_consequence",
    "target_concept",
    "entrypoint_target",
}

OPEN_HYPOTHESIS_STATES = {
    "needs-testing",
    "tentative",
    "inconclusive",
    "provisionally-supported",
    "provisionally-refuted",
    "open",
    "unresolved",
}

OBSERVABILITY_AGENTS = {
    "kb-log-indexer",
    "kb-surface-indexer",
    "kb-conceptual-dynamics",
    "kb-process-graph-visualizer",
    "kb-reasoning-dynamics",
}

PROFILE_KEYS = (
    "implication_signatures",
    "consequence_signatures",
    "antecedent_signatures",
    "claim_signatures",
    "model_signatures",
    "reduction_signatures",
)

CONCEPT_HIGHLIGHT_PRIORITY = {
    "target-concept": 9,
    "invariant": 8,
    "bridge-object": 8,
    "abstraction-family": 7,
    "formalization-commitment": 6,
    "barrier-or-obstruction": 5,
    "entrypoint-anchor": 4,
    "antecedent-concept": 4,
    "representation-change": 3,
    "conceptual": 2,
}

ROLE_HIGHLIGHT_PRIORITY = {
    "target_consequence": 8,
    "target_concept": 8,
    "entrypoint_target": 7,
    "preserved_invariant": 8,
    "conjectured_object": 8,
    "mathematical_object_role": 7,
    "abstraction_family": 7,
    "proof_obligation": 6,
    "candidate_lemma": 6,
    "definitional_commitment": 6,
    "essential_element": 5,
    "barrier_family": 5,
    "support_antecedent": 4,
}

OBJECT_HIGHLIGHT_PRIORITY = {
    "proof_sketch": 9,
    "bridge_program": 8,
    "abstraction_conjecture": 8,
    "strategy": 6,
    "hypothesis": 5,
    "revision_action": 4,
}

STATUS_HIGHLIGHT_PRIORITY = {
    "supported": 9,
    "provisionally-supported": 8,
    "formalized": 7,
    "explored": 6,
    "needs-testing": 5,
    "unresolved": 5,
    "open": 5,
    "tentative": 4,
    "generated": 3,
    "proposed": 3,
    "refuted": 2,
    "provisionally-refuted": 2,
}

GENERIC_CONCEPT_LABELS = {
    "lower-bound",
    "nonuniform-circuits",
    "major-separation",
    "unconditional",
    "target model",
    "proof progress potential",
}

MOJIBAKE_REPLACEMENTS = {
    "â€œ": '"',
    "â€": '"',
    "â€˜": "'",
    "â€™": "'",
    "â€“": "-",
    "â€”": "-",
    "â€¢": "•",
    "â†’": "->",
    "â‰¥": ">=",
    "â‰¤": "<=",
    "â‰ ": "!=",
}


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


def _safe_int(value: Any, default: int = 0) -> int:
    """
    Relevance: Operates within the orchestration and observability layer.
    Concept: Defensive conversion/parsing to keep scoring and reporting robust.
    Contribution: Reduces runtime ambiguity and prevents malformed artifacts from destabilizing the workflow.
    """

    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def _load_json(path: Path) -> dict[str, Any]:
    """
    Relevance: Operates within the orchestration and observability layer.
    Concept: Loading and structuring external artifacts for deterministic processing.
    Contribution: Provides clean, typed inputs so downstream reasoning steps remain auditable.
    """

    if not path.exists():
        return {}
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}
    return payload if isinstance(payload, dict) else {}


def _load_yaml(path: Path) -> dict[str, Any]:
    """
    Relevance: Operates within the orchestration and observability layer.
    Concept: Loading and structuring external artifacts for deterministic processing.
    Contribution: Keeps YAML-derived hypothesis state available to conceptual monitoring.
    """

    if not path.exists():
        return {}
    try:
        payload = yaml.safe_load(path.read_text(encoding="utf-8"))
    except Exception:
        return {}
    return payload if isinstance(payload, dict) else {}


def _normalize_stage_id(raw: str) -> str:
    """
    Relevance: Operates within the orchestration and observability layer.
    Concept: Stable naming helper for stage-aligned metrics.
    Contribution: Keeps surfaced moments and artifact stages joinable under one canonical vocabulary.
    """

    return str(raw or "").strip()


def _profile_terms(profile: Any) -> list[str]:
    """
    Relevance: Operates within the orchestration and observability layer.
    Concept: Extraction of structured mathematical labels from typed artifact payloads.
    Contribution: Surfaces theorem-level antecedents, consequences, and reductions for conceptual monitoring.
    """

    if not isinstance(profile, dict):
        return []
    out: list[str] = []
    for key in PROFILE_KEYS:
        values = profile.get(key, [])
        if not isinstance(values, list):
            continue
        for item in values:
            text = str(item).strip()
            if text:
                out.append(text)
    return out


def _slugify(raw: str) -> str:
    """
    Relevance: Operates within the orchestration and observability layer.
    Concept: Stable naming helper for generated identifiers.
    Contribution: Produces deterministic fallback ids for conceptual objects lacking explicit ids.
    """

    return "".join(ch if ch.isalnum() or ch in "._:-" else "-" for ch in str(raw).strip()).strip("-") or "unknown"


def _canonical_label(value: Any) -> str:
    """
    Relevance: Operates within the orchestration and observability layer.
    Concept: Normalization of input structures into stable internal forms.
    Contribution: Prevents duplicate concept counting caused by whitespace and casing noise.
    """

    return " ".join(str(value or "").split()).strip()


def _clean_display_text(value: Any, *, limit: int = 0) -> str:
    """
    Relevance: Operates within the orchestration and observability layer.
    Concept: Display-oriented normalization of textual mathematical content.
    Contribution: Keeps dashboard excerpts readable and reduces encoding noise in theorem summaries.
    """

    text = " ".join(str(value or "").split()).strip()
    for src, dst in MOJIBAKE_REPLACEMENTS.items():
        text = text.replace(src, dst)
    if limit and len(text) > limit:
        text = text[: max(0, limit - 3)].rstrip() + "..."
    return text


def _clean_display_list(values: Any, *, limit: int = 4, text_limit: int = 220) -> list[str]:
    """
    Relevance: Operates within the orchestration and observability layer.
    Concept: Display-oriented normalization of short content lists.
    Contribution: Gives the HTML renderer compact theorem obligations and lemma chains without raw artifact noise.
    """

    if not isinstance(values, list):
        return []
    out: list[str] = []
    seen: set[str] = set()
    for item in values:
        text = _clean_display_text(item, limit=text_limit)
        if text and text not in seen:
            seen.add(text)
            out.append(text)
        if len(out) >= limit:
            break
    return out


def _statement_delta_payload(delta: Any) -> dict[str, str]:
    """
    Relevance: Operates within the orchestration and observability layer.
    Concept: Compact serialization of theorem-pair deltas for dashboard rendering.
    Contribution: Keeps route-specific mathematical shifts visible in content summaries.
    """

    if not isinstance(delta, dict):
        return {}
    out: dict[str, str] = {}
    limits = {
        "source_problem_family": 120,
        "target_problem_family": 120,
        "source_model": 140,
        "target_model": 140,
        "source_claim_focus": 180,
        "target_claim_focus": 180,
        "route_synopsis": 320,
        "model_shift": 220,
        "threshold_shift": 220,
        "consequence_shift": 260,
        "typed_object_expectation": 180,
        "typing_status": 60,
        "missing_witness_or_transport": 260,
    }
    for key in (
        "source_problem_family",
        "target_problem_family",
        "source_model",
        "target_model",
        "source_claim_focus",
        "target_claim_focus",
        "route_synopsis",
        "model_shift",
        "threshold_shift",
        "consequence_shift",
        "typed_object_expectation",
        "typing_status",
        "missing_witness_or_transport",
    ):
        text = _clean_display_text(delta.get(key, ""), limit=limits.get(key, 220))
        if text:
            out[str(key)] = text
    return out


def _first_nonempty(*values: Any, limit: int = 0) -> str:
    """
    Relevance: Operates within the orchestration and observability layer.
    Concept: Stable fallback selection across multiple possible text sources.
    Contribution: Lets content cards prefer the most informative mathematical wording available.
    """

    for value in values:
        text = _clean_display_text(value, limit=limit)
        if text:
            return text
    return ""


def _extract_text_rows(rows: Any, *, keys: tuple[str, ...], limit: int = 4, text_limit: int = 220) -> list[str]:
    """
    Relevance: Operates within the orchestration and observability layer.
    Concept: Extraction of compact textual items from structured row lists.
    Contribution: Converts obligations, lemmas, and assumptions into card-friendly summaries.
    """

    if not isinstance(rows, list):
        return []
    out: list[str] = []
    seen: set[str] = set()
    for row in rows:
        if isinstance(row, dict):
            text = _first_nonempty(*(row.get(key, "") for key in keys), limit=text_limit)
        else:
            text = _clean_display_text(row, limit=text_limit)
        if text and text not in seen:
            seen.add(text)
            out.append(text)
        if len(out) >= limit:
            break
    return out


def _merge_detail_value(existing: Any, new_value: Any) -> Any:
    """
    Relevance: Operates within the orchestration and observability layer.
    Concept: Non-destructive merge for rich object-detail payloads.
    Contribution: Preserves the most informative content when multiple stages touch the same object.
    """

    if existing in (None, "", [], {}):
        return _json_metric(new_value)
    if new_value in (None, "", [], {}):
        return _json_metric(existing)
    if isinstance(existing, dict) and isinstance(new_value, dict):
        out = {str(k): _json_metric(v) for k, v in existing.items()}
        for key, value in new_value.items():
            key_s = str(key)
            out[key_s] = _merge_detail_value(out.get(key_s), value)
        return out
    if isinstance(existing, list) and isinstance(new_value, list):
        out = list(existing)
        for value in new_value:
            item = _json_metric(value)
            if item not in out:
                out.append(item)
        return out
    if isinstance(existing, str) and isinstance(new_value, str):
        return new_value if len(new_value) > len(existing) else existing
    if isinstance(existing, (int, float)) and isinstance(new_value, (int, float)):
        return max(existing, new_value)
    return _json_metric(existing)


def _merge_detail_dict(existing: Any, new_value: Any) -> dict[str, Any]:
    """
    Relevance: Operates within the orchestration and observability layer.
    Concept: Merge helper for rich content payloads attached to conceptual objects.
    Contribution: Keeps theorem excerpts, obligations, and deltas stable across stage updates.
    """

    base = existing if isinstance(existing, dict) else {}
    extra = new_value if isinstance(new_value, dict) else {}
    out = {str(k): _json_metric(v) for k, v in base.items()}
    for key, value in extra.items():
        out[str(key)] = _merge_detail_value(out.get(str(key)), value)
    return out


def _concept_nature(role: str, label: str) -> str:
    """
    Relevance: Operates within the orchestration and observability layer.
    Concept: Typed classification used to guide interpretability.
    Contribution: Provides a reusable taxonomy for conceptual entities across theorem families.
    """

    role_s = str(role).strip().lower()
    label_s = str(label).strip().lower()
    if role_s in {"preserved_invariant"} or "invariant" in label_s:
        return "invariant"
    if role_s in {"abstraction_family", "abstraction_type"} or "abstraction" in label_s:
        return "abstraction-family"
    if role_s in {"conjectured_object", "mathematical_object_role"}:
        return "bridge-object"
    if role_s in TARGET_ROLES or "consequence" in role_s:
        return "target-concept"
    if role_s == "support_antecedent" or "antecedent" in role_s:
        return "antecedent-concept"
    if role_s in {"essential_element", "barrier_family", "gap_axis"} or any(
        token in label_s for token in ("barrier", "obstruction", "hardness", "impossibility")
    ):
        return "barrier-or-obstruction"
    if role_s in {"conceptual_change", "revision_action_type"} or any(
        token in label_s for token in ("representation", "normal-form", "re-encoding", "revision")
    ):
        return "representation-change"
    if role_s in {"proof_obligation", "candidate_lemma", "definitional_commitment"}:
        return "formalization-commitment"
    if role_s in {"entrypoint_concept", "intervention_focus", "pathway_goal"}:
        return "entrypoint-anchor"
    return "conceptual"


def _hypothesis_nature(kind: str) -> str:
    """
    Relevance: Operates within the orchestration and observability layer.
    Concept: Typed classification used to guide interpretability.
    Contribution: Collapses low-level hypothesis kinds into a stable conceptual taxonomy for dashboards.
    """

    text = str(kind or "").strip().lower()
    if not text:
        return "hypothesis"
    if "bridge" in text:
        return "bridge-hypothesis"
    if "invariant" in text:
        return "invariant-hypothesis"
    if "representation" in text or "normal-form" in text:
        return "representation-hypothesis"
    if "barrier" in text:
        return "barrier-hypothesis"
    if "analogy" in text:
        return "analogy-hypothesis"
    if "definition" in text:
        return "definition-hypothesis"
    return "conceptual-hypothesis"


def _reasoning_types_from_family(family: str) -> list[str]:
    """
    Relevance: Operates within the orchestration and observability layer.
    Concept: Typed classification used to guide interpretability.
    Contribution: Converts proof-strategy family labels into higher-level reasoning regimes.
    """

    text = str(family or "").strip().lower()
    if not text:
        return []
    out: list[str] = []
    if "invariant" in text:
        out.append("invariant-transport")
    if "reduction" in text or "transfer" in text:
        out.append("reduction-transfer")
    if "barrier" in text:
        out.append("barrier-escape")
    if "contradiction" in text or "collapse" in text or "separation" in text:
        out.append("contradiction-impossibility")
    if any(token in text for token in ("construction", "measure", "fixed-point", "generator", "spectral", "integration")):
        out.append("constructive-object-formation")
    return out


def _default_run_id_for_conceptual_view(surfaces: list[dict[str, Any]]) -> tuple[str, str]:
    """
    Relevance: Operates within the orchestration and observability layer.
    Concept: Internal helper implementing one deterministic step of this stage.
    Contribution: Makes direct conceptual-dashboard use stable even when multiple run ids exist for one KB.
    """

    if not surfaces:
        return ("", "no-surfaces")

    orchestrator = [item for item in surfaces if str(item.get("agent", "")).strip() == "kb-orchestrator"]
    end_to_end = [
        item
        for item in orchestrator
        if any(
            token in str(item.get("summary", "")).lower()
            for token in ("intent `pipeline` completed", "intent `abductive-loop` completed")
        )
    ]
    if end_to_end:
        latest = sorted(end_to_end, key=lambda x: (str(x.get("ended_utc", "")), str(x.get("started_utc", ""))))[-1]
        return (str(latest.get("run_id", "")).strip(), "latest-end-to-end")
    if orchestrator:
        latest = sorted(orchestrator, key=lambda x: (str(x.get("ended_utc", "")), str(x.get("started_utc", ""))))[-1]
        return (str(latest.get("run_id", "")).strip(), "latest-orchestrator-run")
    latest_any = sorted(surfaces, key=lambda x: (str(x.get("ended_utc", "")), str(x.get("started_utc", ""))))[-1]
    return (str(latest_any.get("run_id", "")).strip(), "latest-surface-run")


def _artifact_paths(repo_root: Path, artifacts_dir: Path) -> dict[str, Path]:
    """
    Relevance: Operates within the orchestration and observability layer.
    Concept: Stable naming and path-derivation helper for KB-scoped artifact loading.
    Contribution: Keeps conceptual monitoring aligned with canonical stage artifact locations.
    """

    slug = artifacts_dir.name
    phyp_dir = repo_root / "phyp"
    return {
        "analysis": artifacts_dir / "connection-analysis.json",
        "coherence": artifacts_dir / "coherence-report.json",
        "entrypoints": artifacts_dir / "entrypoints.json",
        "pathways": artifacts_dir / "entrypoint-pathways.json",
        "hardness": artifacts_dir / "epistemic-hardness.json",
        "bridges": artifacts_dir / "bridge-plan.json",
        "conjectures": artifacts_dir / "concept-gap-abstractions.json",
        "strategies": artifacts_dir / "proof-strategies.json",
        "proof_sketches": artifacts_dir / "proof-sketches.json",
        "hypothesis_eval": artifacts_dir / "hypothesis-evaluation.json",
        "hypothesis_loop": artifacts_dir / "hypothesis-refutation-loop.json",
        "revision": artifacts_dir / "revision-loop.json",
        "expert_paper": artifacts_dir / "expert-hypothesis-paper.json",
        "phyp": phyp_dir / f"{slug}.proof-hypotheses.yaml",
        "phyp_reviewed": phyp_dir / f"{slug}.hypotheses-reviewed.yaml",
    }


def _artifact_bundle(repo_root: Path, artifacts_dir: Path) -> dict[str, dict[str, Any]]:
    """
    Relevance: Operates within the orchestration and observability layer.
    Concept: Loading and structuring external artifacts for deterministic processing.
    Contribution: Provides the conceptual dashboard with stage outputs even when surfaced moments are sparse.
    """

    paths = _artifact_paths(repo_root, artifacts_dir)
    return {
        "analysis": _load_json(paths["analysis"]),
        "coherence": _load_json(paths["coherence"]),
        "entrypoints": _load_json(paths["entrypoints"]),
        "pathways": _load_json(paths["pathways"]),
        "hardness": _load_json(paths["hardness"]),
        "bridges": _load_json(paths["bridges"]),
        "conjectures": _load_json(paths["conjectures"]),
        "strategies": _load_json(paths["strategies"]),
        "proof_sketches": _load_json(paths["proof_sketches"]),
        "hypothesis_eval": _load_json(paths["hypothesis_eval"]),
        "hypothesis_loop": _load_json(paths["hypothesis_loop"]),
        "revision": _load_json(paths["revision"]),
        "expert_paper": _load_json(paths["expert_paper"]),
        "phyp": _load_yaml(paths["phyp"]),
        "phyp_reviewed": _load_yaml(paths["phyp_reviewed"]),
    }


def _contribution(stage: str, description: str) -> dict[str, Any]:
    """
    Relevance: Operates within the orchestration and observability layer.
    Concept: Internal helper implementing one deterministic step of this stage.
    Contribution: Produces a consistent contribution structure across artifact extractors.
    """

    return {
        "stage": stage,
        "description": description,
        "concepts": [],
        "objects": [],
        "reasoning_types": list(STAGE_REASONING_TYPES.get(stage, [])),
        "proof_strategy_families": [],
        "metrics": {},
        "notes": [],
    }


def _concept(label: str, role: str, stage: str, nature: str = "", source: str = "") -> dict[str, Any]:
    """
    Relevance: Operates within the orchestration and observability layer.
    Concept: Internal helper implementing one deterministic step of this stage.
    Contribution: Makes concept additions uniform across artifact families.
    """

    label_s = _canonical_label(label)
    role_s = str(role).strip() or "concept"
    if not label_s:
        return {}
    return {
        "label": label_s,
        "role": role_s,
        "nature": nature or _concept_nature(role_s, label_s),
        "stage": stage,
        "source": source,
    }


def _obj(
    object_id: str,
    *,
    object_type: str,
    label: str = "",
    nature: str = "",
    stage: str = "",
    kind: str = "",
    state: str = "",
    score: float | None = None,
    generated: bool = False,
    prioritized: bool = False,
    explored: bool = False,
    formalized: bool = False,
    supported: bool = False,
    refuted: bool = False,
    revised: bool = False,
    proof_strategy_family: str = "",
    reasoning_types: list[str] | None = None,
    related_concepts: list[str] | None = None,
    content: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """
    Relevance: Operates within the orchestration and observability layer.
    Concept: Internal helper implementing one deterministic step of this stage.
    Contribution: Normalizes conceptual-object lifecycle updates across different artifact producers.
    """

    object_id_s = str(object_id).strip() or f"{object_type}:{_slugify(label)}"
    return {
        "id": object_id_s,
        "object_type": str(object_type).strip() or "conceptual_object",
        "label": _canonical_label(label) or object_id_s,
        "nature": nature or str(object_type).strip() or "conceptual_object",
        "stage": stage,
        "kind": str(kind).strip(),
        "state": str(state).strip(),
        "score": None if score is None else float(score),
        "generated": bool(generated),
        "prioritized": bool(prioritized),
        "explored": bool(explored),
        "formalized": bool(formalized),
        "supported": bool(supported),
        "refuted": bool(refuted),
        "revised": bool(revised),
        "proof_strategy_family": str(proof_strategy_family).strip(),
        "reasoning_types": [str(x).strip() for x in (reasoning_types or []) if str(x).strip()],
        "related_concepts": [_canonical_label(x) for x in (related_concepts or []) if _canonical_label(x)],
        "content": _merge_detail_dict({}, content or {}),
    }


def _extract_connect_analysis(analysis: dict[str, Any]) -> dict[str, Any]:
    contrib = _contribution("connect.analyze", "Connector analysis and intervention focus.")
    if not analysis:
        return contrib
    stats = analysis.get("stats", {}) if isinstance(analysis.get("stats"), dict) else {}
    concept_graph = analysis.get("concept_graph", {}) if isinstance(analysis.get("concept_graph"), dict) else {}
    contrib["metrics"].update(
        {
            "analysis_statement_count": _safe_int(stats.get("statement_count", 0)),
            "analysis_edge_count": _safe_int(stats.get("edge_count", 0)),
            "analysis_missing_dependency_count": _safe_int(stats.get("missing_dependency_count", 0)),
            "concept_graph_nodes": len(concept_graph.get("nodes", [])) if isinstance(concept_graph.get("nodes"), list) else 0,
            "concept_graph_relations": len(concept_graph.get("relations", []))
            if isinstance(concept_graph.get("relations"), list)
            else 0,
            "connection_candidate_count": len(analysis.get("connection_candidates", []))
            if isinstance(analysis.get("connection_candidates"), list)
            else 0,
            "top_intervention_count": len(analysis.get("top_interventions", []))
            if isinstance(analysis.get("top_interventions"), list)
            else 0,
        }
    )
    for row in analysis.get("top_interventions", []) if isinstance(analysis.get("top_interventions"), list) else []:
        if not isinstance(row, dict):
            continue
        for concept_label in row.get("concept_focus", []) if isinstance(row.get("concept_focus"), list) else []:
            item = _concept(concept_label, "intervention_focus", "connect.analyze", source="analysis.top_interventions")
            if item:
                contrib["concepts"].append(item)
        for term in _profile_terms(row.get("concept_profile")):
            item = _concept(term, "target_concept", "connect.analyze", source="analysis.concept_profile")
            if item:
                contrib["concepts"].append(item)
    for row in (analysis.get("connection_candidates", []) if isinstance(analysis.get("connection_candidates"), list) else [])[:24]:
        if not isinstance(row, dict):
            continue
        for concept_label in row.get("concept_evidence", []) if isinstance(row.get("concept_evidence"), list) else []:
            item = _concept(concept_label, "bridge_evidence_term", "connect.analyze", source="analysis.connection_candidates")
            if item:
                contrib["concepts"].append(item)
        for term in _profile_terms(row.get("from_profile")) + _profile_terms(row.get("to_profile")):
            item = _concept(term, "intervention_focus", "connect.analyze", source="analysis.connection_profiles")
            if item:
                contrib["concepts"].append(item)
    return contrib


def _extract_phyp(phyp: dict[str, Any]) -> dict[str, Any]:
    contrib = _contribution("connect.generate-phyp", "Initial hypothesis inventory.")
    hypotheses = phyp.get("hypotheses", []) if isinstance(phyp.get("hypotheses"), list) else []
    kind_counter: Counter[str] = Counter()
    status_counter: Counter[str] = Counter()
    for row in hypotheses:
        if not isinstance(row, dict):
            continue
        hid = str(row.get("id", "") or row.get("hypothesis_id", "")).strip()
        kind = str(row.get("kind", "")).strip().lower()
        status = str(row.get("status", "")).strip().lower() or "generated"
        kind_counter[kind or "unknown"] += 1
        status_counter[status] += 1
        label = str(row.get("title", "") or row.get("summary", "") or row.get("claim", "")).strip() or hid
        contrib["objects"].append(
            _obj(
                hid,
                object_type="hypothesis",
                label=label,
                nature=_hypothesis_nature(kind),
                stage="connect.generate-phyp",
                kind=kind,
                state=status,
                score=_safe_float(row.get("priority", 0.0), 0.0),
                generated=True,
            )
        )
    contrib["metrics"]["hypothesis_total"] = len(hypotheses)
    contrib["metrics"]["hypothesis_kind_counts"] = dict(kind_counter)
    contrib["metrics"]["hypothesis_status_counts"] = dict(status_counter)
    return contrib


def _extract_coherence(coherence: dict[str, Any]) -> dict[str, Any]:
    contrib = _contribution("coherence-eval", "Coherence and theory-fit assessment.")
    if not coherence:
        return contrib
    profile = coherence.get("coherence_profile", {}) if isinstance(coherence.get("coherence_profile"), dict) else {}
    graph = coherence.get("typed_coherence_graph", {}) if isinstance(coherence.get("typed_coherence_graph"), dict) else {}
    contrib["metrics"].update(
        {
            "coherence_global": _safe_float(profile.get("global_coherence", 0.0)),
            "coherence_consistency": _safe_float(profile.get("consistency", 0.0)),
            "coherence_integration": _safe_float(profile.get("integration", 0.0)),
            "coherence_explanatory_unification": _safe_float(profile.get("explanatory_unification", 0.0)),
            "coherence_tension": _safe_float(profile.get("tension", 0.0)),
            "coherence_graph_nodes": len(graph.get("nodes", [])) if isinstance(graph.get("nodes"), list) else 0,
            "coherence_graph_edges": len(graph.get("edges", [])) if isinstance(graph.get("edges"), list) else 0,
        }
    )
    relation_counts = graph.get("relation_counts", {}) if isinstance(graph.get("relation_counts"), dict) else {}
    if relation_counts:
        contrib["metrics"]["coherence_relation_types"] = {str(k): _safe_int(v) for k, v in relation_counts.items()}
    return contrib


def _extract_entrypoints(entrypoints: dict[str, Any]) -> dict[str, Any]:
    contrib = _contribution("entrypoints.rank", "Entrypoint and phase localization.")
    if not entrypoints:
        return contrib
    tracks = entrypoints.get("concept_tracks", []) if isinstance(entrypoints.get("concept_tracks"), list) else []
    contrib["metrics"]["entrypoint_count"] = len(entrypoints.get("ranked_entrypoints", [])) if isinstance(entrypoints.get("ranked_entrypoints"), list) else 0
    contrib["metrics"]["concept_track_count"] = len(tracks)
    for track in tracks:
        if not isinstance(track, dict):
            continue
        phase = str(track.get("phase", "Unspecified")).strip() or "Unspecified"
        item = _concept(phase, "entrypoint_target", "entrypoints.rank", nature="entrypoint-anchor", source="entrypoints.concept_tracks")
        if item:
            contrib["concepts"].append(item)
    return contrib


def _extract_pathways(pathways: dict[str, Any]) -> dict[str, Any]:
    contrib = _contribution("entrypoints.pathways", "Pathway synthesis over entrypoints.")
    if not pathways:
        return contrib
    rows = pathways.get("pathways", []) if isinstance(pathways.get("pathways"), list) else []
    contrib["metrics"]["pathway_count"] = len(rows)
    for row in rows[:20]:
        if not isinstance(row, dict):
            continue
        goal = str(row.get("goal", "")).strip()
        if goal:
            item = _concept(goal, "pathway_goal", "entrypoints.pathways", source="pathways.goal")
            if item:
                contrib["concepts"].append(item)
    return contrib


def _extract_hardness(hardness: dict[str, Any]) -> dict[str, Any]:
    contrib = _contribution("hardness", "Barrier and hardness articulation.")
    if not hardness:
        return contrib
    elements = hardness.get("essential_elements", []) if isinstance(hardness.get("essential_elements"), list) else []
    programs = hardness.get("anti_barrier_programs", []) if isinstance(hardness.get("anti_barrier_programs"), list) else []
    contrib["metrics"]["hardness_elements"] = len(elements)
    contrib["metrics"]["anti_barrier_programs"] = len(programs)
    for row in elements:
        if not isinstance(row, dict):
            continue
        item = _concept(row.get("name", ""), "essential_element", "hardness", source="hardness.essential_elements")
        if item:
            contrib["concepts"].append(item)
    for row in programs:
        if not isinstance(row, dict):
            continue
        barrier = str(row.get("barrier_family", "")).strip()
        if barrier:
            item = _concept(barrier, "barrier_family", "hardness", source="hardness.anti_barrier_programs")
            if item:
                contrib["concepts"].append(item)
        for change in row.get("minimal_conceptual_changes", []) if isinstance(row.get("minimal_conceptual_changes"), list) else []:
            item = _concept(change, "conceptual_change", "hardness", source="hardness.minimal_conceptual_changes")
            if item:
                contrib["concepts"].append(item)
    concept_comm = hardness.get("concept_communication", {}) if isinstance(hardness.get("concept_communication"), dict) else {}
    for row in concept_comm.get("top_entrypoint_concepts", []) if isinstance(concept_comm.get("top_entrypoint_concepts"), list) else []:
        if not isinstance(row, dict):
            continue
        item = _concept(row.get("concept_label", ""), "entrypoint_concept", "hardness", source="hardness.top_entrypoint_concepts")
        if item:
            contrib["concepts"].append(item)
    for row in concept_comm.get("top_intervention_concepts", []) if isinstance(concept_comm.get("top_intervention_concepts"), list) else []:
        if not isinstance(row, dict):
            continue
        for label in row.get("concept_focus", []) if isinstance(row.get("concept_focus"), list) else []:
            item = _concept(label, "intervention_focus", "hardness", source="hardness.top_intervention_concepts")
            if item:
                contrib["concepts"].append(item)
    return contrib


def _extract_bridges(bridges: dict[str, Any]) -> dict[str, Any]:
    contrib = _contribution("bridge-plan", "Bridge program synthesis.")
    if not bridges:
        return contrib
    programs = bridges.get("bridge_programs", []) if isinstance(bridges.get("bridge_programs"), list) else []
    recommended = {
        str(x).strip()
        for x in (bridges.get("recommended_run_order", []) if isinstance(bridges.get("recommended_run_order"), list) else [])
        if str(x).strip()
    }
    bridge_type_counts: Counter[str] = Counter()
    for row in programs:
        if not isinstance(row, dict):
            continue
        bridge_id = str(row.get("bridge_id", "")).strip()
        bridge_type = str(row.get("bridge_type", "")).strip()
        bridge_type_counts[bridge_type or "unknown"] += 1
        commit = row.get("inferential_commitment", {}) if isinstance(row.get("inferential_commitment"), dict) else {}
        bridge_label = (
            f"{bridge_type}: {commit.get('support_antecedent_schema', '')} => {commit.get('target_consequence_schema', '')}"
            if str(commit.get("support_antecedent_schema", "")).strip() or str(commit.get("target_consequence_schema", "")).strip()
            else (bridge_type or f"{row.get('from_id', '')} -> {row.get('to_id', '')}")
        )
        related = [
            str(commit.get("support_antecedent_schema", "")).strip(),
            str(commit.get("target_consequence_schema", "")).strip(),
            str(commit.get("preserved_invariant", "")).strip(),
        ]
        contrib["objects"].append(
            _obj(
                bridge_id,
                object_type="bridge_program",
                label=bridge_label,
                nature=bridge_type or "bridge_program",
                stage="bridge-plan",
                kind=bridge_type,
                score=_safe_float(row.get("bridge_score", 0.0)),
                generated=True,
                prioritized=bridge_id in recommended,
                related_concepts=related,
                content={
                    "route_synopsis": _first_nonempty((row.get("statement_delta", {}) if isinstance(row.get("statement_delta"), dict) else {}).get("route_synopsis", ""), limit=320),
                    "statement_delta": _statement_delta_payload(row.get("statement_delta", {})),
                    "source_excerpt": _first_nonempty((row.get("statement_delta", {}) if isinstance(row.get("statement_delta"), dict) else {}).get("source_theorem_excerpt", ""), limit=260),
                    "target_excerpt": _first_nonempty((row.get("statement_delta", {}) if isinstance(row.get("statement_delta"), dict) else {}).get("target_theorem_excerpt", ""), limit=260),
                    "bridge_definition": _first_nonempty((row.get("mathematical_program", {}) if isinstance(row.get("mathematical_program"), dict) else {}).get("bridge_question", ""), limit=320),
                    "conditional_claim": _first_nonempty((row.get("mathematical_program", {}) if isinstance(row.get("mathematical_program"), dict) else {}).get("theorem_template", ""), limit=320),
                    "assumptions": _clean_display_list(
                        [
                            (row.get("mathematical_program", {}) if isinstance(row.get("mathematical_program"), dict) else {}).get("source_assumption", ""),
                            (row.get("mathematical_program", {}) if isinstance(row.get("mathematical_program"), dict) else {}).get("target_payoff", ""),
                            (row.get("mathematical_program", {}) if isinstance(row.get("mathematical_program"), dict) else {}).get("invariant_transport", ""),
                        ],
                        limit=3,
                        text_limit=220,
                    ),
                    "obligations": _clean_display_list(
                        (row.get("mathematical_program", {}) if isinstance(row.get("mathematical_program"), dict) else {}).get("inspection_checklist", []),
                        limit=4,
                        text_limit=220,
                    ),
                    "failure_diagnosis": _first_nonempty((row.get("mathematical_program", {}) if isinstance(row.get("mathematical_program"), dict) else {}).get("obstruction_pressure", ""), limit=260),
                    "carrier_kind": _first_nonempty((row.get("statement_delta", {}) if isinstance(row.get("statement_delta"), dict) else {}).get("typed_object_expectation", ""), limit=180),
                    "typing_status": _first_nonempty((row.get("statement_delta", {}) if isinstance(row.get("statement_delta"), dict) else {}).get("typing_status", ""), limit=60),
                },
            )
        )
        for term in row.get("evidence_terms", []) if isinstance(row.get("evidence_terms"), list) else []:
            item = _concept(term, "bridge_evidence_term", "bridge-plan", source="bridges.evidence_terms")
            if item:
                contrib["concepts"].append(item)
        for role, key in (
            ("support_antecedent", "support_antecedent_schema"),
            ("target_consequence", "target_consequence_schema"),
            ("preserved_invariant", "preserved_invariant"),
        ):
            item = _concept(commit.get(key, ""), role, "bridge-plan", source=f"bridges.{key}")
            if item:
                contrib["concepts"].append(item)
    contrib["metrics"]["bridge_program_count"] = len(programs)
    contrib["metrics"]["bridge_type_counts"] = dict(bridge_type_counts)
    return contrib


def _extract_conjectures(conjectures: dict[str, Any]) -> dict[str, Any]:
    contrib = _contribution("conjecture", "Abstraction conjectures and bridge-object shaping.")
    if not conjectures:
        return contrib
    rows = conjectures.get("abstraction_conjectures", []) if isinstance(conjectures.get("abstraction_conjectures"), list) else []
    clusters = conjectures.get("gap_clusters", []) if isinstance(conjectures.get("gap_clusters"), list) else []
    recommended = {
        str(x).strip()
        for x in (conjectures.get("recommended_run_order", []) if isinstance(conjectures.get("recommended_run_order"), list) else [])
        if str(x).strip()
    }
    abstraction_counts: Counter[str] = Counter()
    gap_axis_counts: Counter[str] = Counter()
    counterfactual_count = 0
    for cluster in clusters:
        if not isinstance(cluster, dict):
            continue
        for axis in cluster.get("gap_axes", []) if isinstance(cluster.get("gap_axes"), list) else []:
            if not isinstance(axis, dict):
                continue
            axis_label = str(axis.get("axis", "")).strip()
            if axis_label:
                gap_axis_counts[axis_label] += 1
                item = _concept(axis_label, "gap_axis", "conjecture", source="conjectures.gap_axes")
                if item:
                    contrib["concepts"].append(item)
        for fam in cluster.get("recommended_abstraction_families", []) if isinstance(cluster.get("recommended_abstraction_families"), list) else []:
            item = _concept(fam, "abstraction_family", "conjecture", source="conjectures.recommended_abstraction_families")
            if item:
                contrib["concepts"].append(item)
    for row in rows:
        if not isinstance(row, dict):
            continue
        conjecture_id = str(row.get("conjecture_id", "")).strip()
        abstraction_type = str(row.get("abstraction_type", "")).strip()
        abstraction_counts[abstraction_type or "unknown"] += 1
        counterfactual_count += len(row.get("counterfactual_probes", [])) if isinstance(row.get("counterfactual_probes"), list) else 0
        related = [
            str(row.get("target_consequence_schema", "")).strip(),
            str(row.get("support_antecedent_schema", "")).strip(),
            str(row.get("preserved_invariant", "")).strip(),
            str(row.get("abstraction_label", "")).strip(),
        ]
        contrib["objects"].append(
            _obj(
                conjecture_id,
                object_type="abstraction_conjecture",
                label=str(row.get("abstraction_label", "")).strip() or conjecture_id,
                nature=abstraction_type or "abstraction_conjecture",
                stage="conjecture",
                kind=abstraction_type,
                score=_safe_float(row.get("priority", 0.0)),
                generated=True,
                prioritized=conjecture_id in recommended,
                explored=True,
                related_concepts=related,
                reasoning_types=["bridge-object-design", "counterfactual-probing"],
                content={
                    "route_synopsis": _first_nonempty(
                        (row.get("statement_delta", {}) if isinstance(row.get("statement_delta"), dict) else {}).get("route_synopsis", ""),
                        (row.get("mathematical_specification", {}) if isinstance(row.get("mathematical_specification"), dict) else {}).get("statement_delta", {}).get("route_synopsis", ""),
                        limit=320,
                    ),
                    "statement_delta": _statement_delta_payload(
                        row.get("statement_delta", {})
                        if isinstance(row.get("statement_delta"), dict)
                        else (row.get("mathematical_specification", {}) if isinstance(row.get("mathematical_specification"), dict) else {}).get("statement_delta", {})
                    ),
                    "carrier_kind": _first_nonempty(
                        row.get("carrier_kind", ""),
                        (row.get("mathematical_specification", {}) if isinstance(row.get("mathematical_specification"), dict) else {}).get("carrier_kind", ""),
                        limit=180,
                    ),
                    "typing_status": _first_nonempty(
                        row.get("typing_status", ""),
                        (row.get("mathematical_specification", {}) if isinstance(row.get("mathematical_specification"), dict) else {}).get("typing_status", ""),
                        limit=60,
                    ),
                    "bridge_definition": _first_nonempty(
                        (row.get("definitional_profile", {}) if isinstance(row.get("definitional_profile"), dict) else {}).get("bridging_concept_definition", ""),
                        (row.get("mathematical_specification", {}) if isinstance(row.get("mathematical_specification"), dict) else {}).get("definition_template", ""),
                        limit=360,
                    ),
                    "source_excerpt": _first_nonempty(
                        (
                            row.get("statement_delta", {})
                            if isinstance(row.get("statement_delta"), dict)
                            else (row.get("mathematical_specification", {}) if isinstance(row.get("mathematical_specification"), dict) else {}).get("statement_delta", {})
                        ).get("source_theorem_excerpt", ""),
                        limit=260,
                    ),
                    "target_excerpt": _first_nonempty(
                        (
                            row.get("statement_delta", {})
                            if isinstance(row.get("statement_delta"), dict)
                            else (row.get("mathematical_specification", {}) if isinstance(row.get("mathematical_specification"), dict) else {}).get("statement_delta", {})
                        ).get("target_theorem_excerpt", ""),
                        limit=260,
                    ),
                    "conditional_claim": _first_nonempty(
                        (row.get("mathematical_specification", {}) if isinstance(row.get("mathematical_specification"), dict) else {}).get("conditional_claim", ""),
                        limit=320,
                    ),
                    "assumptions": _clean_display_list(
                        (row.get("mathematical_specification", {}) if isinstance(row.get("mathematical_specification"), dict) else {}).get("assumptions", []),
                        limit=4,
                        text_limit=220,
                    ),
                    "obligations": _clean_display_list(
                        (row.get("mathematical_specification", {}) if isinstance(row.get("mathematical_specification"), dict) else {}).get("proof_obligation_templates", []),
                        limit=4,
                        text_limit=220,
                    ),
                    "failure_diagnosis": _first_nonempty(
                        (row.get("mathematical_specification", {}) if isinstance(row.get("mathematical_specification"), dict) else {}).get("obstruction_template", ""),
                        limit=260,
                    ),
                    "proof_outline": _clean_display_list(
                        (row.get("mathematical_specification", {}) if isinstance(row.get("mathematical_specification"), dict) else {}).get("inspection_focus", []),
                        limit=4,
                        text_limit=220,
                    ),
                    "counterfactual": _first_nonempty(
                        (
                            " / ".join(
                                part
                                for part in (
                                    str(((row.get("counterfactual_probes", [])[0] if isinstance(row.get("counterfactual_probes"), list) and row.get("counterfactual_probes") else {}) if isinstance((row.get("counterfactual_probes", [])[0] if isinstance(row.get("counterfactual_probes"), list) and row.get("counterfactual_probes") else {}), dict) else {}).get("intervention", "")).strip(),
                                    str(((row.get("counterfactual_probes", [])[0] if isinstance(row.get("counterfactual_probes"), list) and row.get("counterfactual_probes") else {}) if isinstance((row.get("counterfactual_probes", [])[0] if isinstance(row.get("counterfactual_probes"), list) and row.get("counterfactual_probes") else {}), dict) else {}).get("expected_bridge_effect", "")).strip(),
                                )
                                if part
                            )
                        ),
                        limit=260,
                    ),
                },
            )
        )
        for role, key in (
            ("conjectured_object", "abstraction_label"),
            ("target_consequence", "target_consequence_schema"),
            ("support_antecedent", "support_antecedent_schema"),
            ("preserved_invariant", "preserved_invariant"),
            ("mathematical_object_role", "mathematical_object_role"),
            ("abstraction_type", "abstraction_type"),
        ):
            item = _concept(row.get(key, ""), role, "conjecture", source=f"conjectures.{key}")
            if item:
                contrib["concepts"].append(item)
        bridge_id = str(row.get("bridge_id", "")).strip()
        if bridge_id:
            contrib["objects"].append(
                _obj(
                    bridge_id,
                    object_type="bridge_program",
                    stage="conjecture",
                    explored=True,
                    prioritized=True,
                )
            )
    contrib["metrics"]["gap_cluster_count"] = len(clusters)
    contrib["metrics"]["abstraction_conjecture_count"] = len(rows)
    contrib["metrics"]["abstraction_type_counts"] = dict(abstraction_counts)
    contrib["metrics"]["gap_axis_counts"] = dict(gap_axis_counts)
    contrib["metrics"]["counterfactual_probe_count"] = counterfactual_count
    return contrib


def _extract_strategies(strategies: dict[str, Any]) -> dict[str, Any]:
    contrib = _contribution("strategies", "Strategy portfolio construction.")
    if not strategies:
        return contrib
    rows = strategies.get("strategies", []) if isinstance(strategies.get("strategies"), list) else []
    phase_counts: Counter[str] = Counter()
    fertility = []
    for idx, row in enumerate(rows):
        if not isinstance(row, dict):
            continue
        strategy_id = str(row.get("strategy_id", "")).strip()
        phase = str(row.get("phase", "")).strip()
        phase_counts[phase or "unknown"] += 1
        fertility.append(_safe_float(row.get("concept_fertility", 0.0)))
        contrib["objects"].append(
            _obj(
                strategy_id,
                object_type="strategy",
                label=str(row.get("name", "")).strip() or strategy_id,
                nature=phase or "strategy",
                stage="strategies",
                score=_safe_float(row.get("strategy_score", 0.0)),
                generated=True,
                prioritized=idx < 3,
                explored=True,
                reasoning_types=["strategy-diversification", "novelty-search"],
                related_concepts=[
                    *(
                        row.get("anchor_concepts", [])
                        if isinstance(row.get("anchor_concepts"), list)
                        else []
                    ),
                    *(
                        row.get("abstraction_concepts", [])
                        if isinstance(row.get("abstraction_concepts"), list)
                        else []
                    ),
                ],
            )
        )
        for concept_label in row.get("anchor_concepts", []) if isinstance(row.get("anchor_concepts"), list) else []:
            item = _concept(concept_label, "entrypoint_concept", "strategies", source="strategies.anchor_concepts")
            if item:
                contrib["concepts"].append(item)
        for concept_label in row.get("abstraction_concepts", []) if isinstance(row.get("abstraction_concepts"), list) else []:
            item = _concept(concept_label, "conjectured_object", "strategies", source="strategies.abstraction_concepts")
            if item:
                contrib["concepts"].append(item)
        for bridge_id in row.get("bridge_ids", []) if isinstance(row.get("bridge_ids"), list) else []:
            contrib["objects"].append(_obj(str(bridge_id), object_type="bridge_program", stage="strategies", explored=True, prioritized=True))
        for hyp_id in row.get("hypothesis_ids", []) if isinstance(row.get("hypothesis_ids"), list) else []:
            contrib["objects"].append(_obj(str(hyp_id), object_type="hypothesis", stage="strategies", explored=True, prioritized=True))
    contrib["metrics"]["strategy_count"] = len(rows)
    contrib["metrics"]["strategy_phase_counts"] = dict(phase_counts)
    contrib["metrics"]["strategy_fertility_avg"] = round(sum(fertility) / len(fertility), 6) if fertility else 0.0
    return contrib


def _extract_proof_sketches(report: dict[str, Any]) -> dict[str, Any]:
    contrib = _contribution("proof-sketch", "Proof-sketch formalization.")
    if not report:
        return contrib
    rows = report.get("proof_sketches", []) if isinstance(report.get("proof_sketches"), list) else []
    family_counts: Counter[str] = Counter()
    obligations = 0
    lemmas = 0
    for row in rows:
        if not isinstance(row, dict):
            continue
        sketch_id = str(row.get("sketch_id", "")).strip()
        family = str(row.get("proof_strategy_family", "")).strip()
        family_counts[family or "unknown"] += 1
        obligations += len(row.get("proof_obligations", [])) if isinstance(row.get("proof_obligations"), list) else 0
        lemmas += len(row.get("candidate_lemmas", [])) if isinstance(row.get("candidate_lemmas"), list) else 0
        contrib["proof_strategy_families"].append(family)
        contrib["reasoning_types"].extend(_reasoning_types_from_family(family))
        contrib["objects"].append(
            _obj(
                sketch_id,
                object_type="proof_sketch",
                label=str(row.get("title", "")).strip() or sketch_id,
                nature=family or "proof_sketch",
                stage="proof-sketch",
                score=_safe_float(row.get("sketch_score", 0.0)),
                generated=True,
                prioritized=True,
                explored=True,
                formalized=True,
                proof_strategy_family=family,
                reasoning_types=["proof-formalization", "obligation-analysis", *_reasoning_types_from_family(family)],
                related_concepts=[
                    str(row.get("conjectured_object", "")).strip(),
                    str(row.get("target_consequence_schema", "")).strip(),
                    str(row.get("support_antecedent_schema", "")).strip(),
                    str(row.get("preserved_invariant", "")).strip(),
                ],
                content={
                    "route_synopsis": _first_nonempty(
                        (row.get("statement_delta", {}) if isinstance(row.get("statement_delta"), dict) else {}).get("route_synopsis", ""),
                        (row.get("mathematical_argument", {}) if isinstance(row.get("mathematical_argument"), dict) else {}).get("statement_delta", {}).get("route_synopsis", ""),
                        limit=320,
                    ),
                    "statement_delta": _statement_delta_payload(
                        (row.get("mathematical_argument", {}) if isinstance(row.get("mathematical_argument"), dict) else {}).get("statement_delta", {})
                        or (row.get("statement_delta", {}) if isinstance(row.get("statement_delta"), dict) else {})
                    ),
                    "carrier_kind": _first_nonempty(row.get("carrier_kind", ""), (row.get("mathematical_argument", {}) if isinstance(row.get("mathematical_argument"), dict) else {}).get("carrier_kind", ""), limit=180),
                    "typing_status": _first_nonempty(row.get("typing_status", ""), (row.get("mathematical_argument", {}) if isinstance(row.get("mathematical_argument"), dict) else {}).get("typing_status", ""), limit=60),
                    "source_excerpt": _first_nonempty(
                        (row.get("mathematical_argument", {}) if isinstance(row.get("mathematical_argument"), dict) else {}).get("source_theorem_excerpt", ""),
                        ((row.get("mathematical_argument", {}) if isinstance(row.get("mathematical_argument"), dict) else {}).get("statement_delta", {}) if isinstance((row.get("mathematical_argument", {}) if isinstance(row.get("mathematical_argument"), dict) else {}).get("statement_delta", {}), dict) else {}).get("source_theorem_excerpt", ""),
                        ((row.get("statement_delta", {}) if isinstance(row.get("statement_delta"), dict) else {})).get("source_theorem_excerpt", ""),
                        limit=260,
                    ),
                    "target_excerpt": _first_nonempty(
                        (row.get("mathematical_argument", {}) if isinstance(row.get("mathematical_argument"), dict) else {}).get("target_theorem_excerpt", ""),
                        ((row.get("mathematical_argument", {}) if isinstance(row.get("mathematical_argument"), dict) else {}).get("statement_delta", {}) if isinstance((row.get("mathematical_argument", {}) if isinstance(row.get("mathematical_argument"), dict) else {}).get("statement_delta", {}), dict) else {}).get("target_theorem_excerpt", ""),
                        ((row.get("statement_delta", {}) if isinstance(row.get("statement_delta"), dict) else {})).get("target_theorem_excerpt", ""),
                        limit=260,
                    ),
                    "bridge_definition": _first_nonempty((row.get("mathematical_argument", {}) if isinstance(row.get("mathematical_argument"), dict) else {}).get("bridge_definition", ""), limit=360),
                    "conditional_claim": _first_nonempty((row.get("mathematical_argument", {}) if isinstance(row.get("mathematical_argument"), dict) else {}).get("proposition", ""), limit=320),
                    "assumptions": _clean_display_list(
                        (row.get("mathematical_argument", {}) if isinstance(row.get("mathematical_argument"), dict) else {}).get("assumptions", []),
                        limit=4,
                        text_limit=220,
                    ),
                    "obligations": _extract_text_rows(row.get("proof_obligations", []), keys=("requirement", "claim_template"), limit=4, text_limit=220),
                    "lemmas": _clean_display_list(
                        [
                            *_extract_text_rows(row.get("candidate_lemmas", []), keys=("statement",), limit=6, text_limit=220),
                            *(
                                (row.get("mathematical_argument", {}) if isinstance(row.get("mathematical_argument"), dict) else {}).get("lemma_chain", [])
                                if isinstance((row.get("mathematical_argument", {}) if isinstance(row.get("mathematical_argument"), dict) else {}).get("lemma_chain", []), list)
                                else []
                            ),
                        ],
                        limit=5,
                        text_limit=220,
                    ),
                    "proof_outline": _clean_display_list(
                        [
                            *_extract_text_rows(row.get("proof_outline_steps", []), keys=("objective", "expected_output"), limit=5, text_limit=200),
                            *(
                                (row.get("mathematical_argument", {}) if isinstance(row.get("mathematical_argument"), dict) else {}).get("inspection_points", [])
                                if isinstance((row.get("mathematical_argument", {}) if isinstance(row.get("mathematical_argument"), dict) else {}).get("inspection_points", []), list)
                                else []
                            ),
                        ],
                        limit=4,
                        text_limit=220,
                    ),
                    "failure_diagnosis": _first_nonempty(
                        (row.get("mathematical_argument", {}) if isinstance(row.get("mathematical_argument"), dict) else {}).get("failure_mode", ""),
                        *((row.get("abort_conditions", []) if isinstance(row.get("abort_conditions"), list) else [])[:1]),
                        limit=260,
                    ),
                    "counterfactual": _first_nonempty(
                        " / ".join(
                            part
                            for part in (
                                str((row.get("counterfactual_test", {}) if isinstance(row.get("counterfactual_test"), dict) else {}).get("intervention", "")).strip(),
                                str((row.get("counterfactual_test", {}) if isinstance(row.get("counterfactual_test"), dict) else {}).get("expected_bridge_effect", "")).strip(),
                            )
                            if part
                        ),
                        limit=260,
                    ),
                },
            )
        )
        for role, key in (
            ("conjectured_object", "conjectured_object"),
            ("target_consequence", "target_consequence_schema"),
            ("support_antecedent", "support_antecedent_schema"),
            ("preserved_invariant", "preserved_invariant"),
        ):
            item = _concept(row.get(key, ""), role, "proof-sketch", source=f"proof_sketches.{key}")
            if item:
                contrib["concepts"].append(item)
        for commitment in row.get("definitional_commitments", []) if isinstance(row.get("definitional_commitments"), list) else []:
            item = _concept(commitment, "definitional_commitment", "proof-sketch", source="proof_sketches.definitional_commitments")
            if item:
                contrib["concepts"].append(item)
        for obligation in row.get("proof_obligations", []) if isinstance(row.get("proof_obligations"), list) else []:
            if not isinstance(obligation, dict):
                continue
            item = _concept(obligation.get("requirement", ""), "proof_obligation", "proof-sketch", source="proof_sketches.proof_obligations")
            if item:
                contrib["concepts"].append(item)
        for lemma in row.get("candidate_lemmas", []) if isinstance(row.get("candidate_lemmas"), list) else []:
            if not isinstance(lemma, dict):
                continue
            item = _concept(lemma.get("statement", ""), "candidate_lemma", "proof-sketch", source="proof_sketches.candidate_lemmas")
            if item:
                contrib["concepts"].append(item)
        for ref_key, ref_type in (
            ("conjecture_id", "abstraction_conjecture"),
            ("strategy_id", "strategy"),
            ("bridge_id", "bridge_program"),
        ):
            ref_id = str(row.get(ref_key, "")).strip()
            if ref_id:
                contrib["objects"].append(
                    _obj(ref_id, object_type=ref_type, stage="proof-sketch", explored=True, prioritized=True, formalized=True)
                )
    contrib["metrics"]["proof_sketch_count"] = len(rows)
    contrib["metrics"]["proof_family_counts"] = dict(family_counts)
    contrib["metrics"]["proof_obligation_count"] = obligations
    contrib["metrics"]["candidate_lemma_count"] = lemmas
    return contrib


def _extract_expert_paper(report: dict[str, Any]) -> dict[str, Any]:
    contrib = _contribution("expert-paper", "Expert-facing synthesis of the strongest theorem-pair routes.")
    if not report:
        return contrib
    bridges = report.get("recommended_bridges", []) if isinstance(report.get("recommended_bridges"), list) else []
    hypotheses = report.get("recommended_hypotheses", []) if isinstance(report.get("recommended_hypotheses"), list) else []
    contrib["metrics"]["recommended_bridge_count"] = len(bridges)
    contrib["metrics"]["recommended_hypothesis_count"] = len(hypotheses)
    for row in bridges:
        if not isinstance(row, dict):
            continue
        bridge_id = str(row.get("bridge_id", "")).strip()
        if not bridge_id:
            continue
        contrib["objects"].append(
            _obj(
                bridge_id,
                object_type="bridge_program",
                label=str(row.get("abstraction_label", "")).strip() or str(row.get("bridge_id", "")).strip(),
                nature=str(row.get("bridge_type", "")).strip() or "bridge_program",
                stage="expert-paper",
                score=_safe_float(row.get("priority", 0.0)),
                prioritized=True,
                explored=True,
                formalized=True,
                proof_strategy_family=str(row.get("proof_strategy_family", "")).strip(),
                related_concepts=[
                    str(row.get("abstraction_label", "")).strip(),
                    str(row.get("support_antecedent_schema", "")).strip(),
                    str(row.get("target_consequence_schema", "")).strip(),
                    str(row.get("preserved_invariant", "")).strip(),
                ],
                content={
                    "route_synopsis": _first_nonempty(row.get("route_synopsis", ""), limit=320),
                    "statement_delta": _statement_delta_payload(row.get("statement_delta", {})),
                    "carrier_kind": _first_nonempty(row.get("carrier_kind", ""), limit=180),
                    "typing_status": _first_nonempty(row.get("typing_status", ""), limit=60),
                    "source_excerpt": _first_nonempty(row.get("source_excerpt", ""), limit=260),
                    "target_excerpt": _first_nonempty(row.get("target_excerpt", ""), limit=260),
                    "bridge_definition": _first_nonempty(row.get("bridge_definition", ""), limit=360),
                    "conditional_claim": _first_nonempty(row.get("conditional_proposition", ""), limit=320),
                    "assumptions": _clean_display_list(row.get("mathematical_assumptions", []), limit=4, text_limit=220),
                    "obligations": _clean_display_list(row.get("proof_obligations", []), limit=4, text_limit=220),
                    "lemmas": _clean_display_list(row.get("candidate_lemmas", []), limit=4, text_limit=220),
                    "proof_outline": _clean_display_list(row.get("expert_actions", []), limit=4, text_limit=220),
                    "failure_diagnosis": _first_nonempty(row.get("failure_diagnosis", ""), limit=260),
                    "counterfactual": _first_nonempty(row.get("negative_route", ""), *((row.get("abort_conditions", []) if isinstance(row.get("abort_conditions"), list) else [])[:1]), limit=260),
                },
            )
        )
    return contrib


def _extract_hypothesis_eval(report: dict[str, Any]) -> dict[str, Any]:
    contrib = _contribution("hypothesis-eval", "Feasibility assessment over the current hypothesis field.")
    if not report:
        return contrib
    summary = report.get("summary", {}) if isinstance(report.get("summary"), dict) else {}
    rows = report.get("results", []) if isinstance(report.get("results"), list) else []
    verdict_counts = summary.get("verdict_counts", {}) if isinstance(summary.get("verdict_counts"), dict) else {}
    next_status_counts = summary.get("next_status_counts", {}) if isinstance(summary.get("next_status_counts"), dict) else {}
    contrib["metrics"]["evaluated_hypothesis_count"] = len(rows)
    contrib["metrics"]["evaluation_verdict_counts"] = {str(k): _safe_int(v) for k, v in verdict_counts.items()}
    contrib["metrics"]["evaluation_next_status_counts"] = {str(k): _safe_int(v) for k, v in next_status_counts.items()}
    for row in rows:
        if not isinstance(row, dict):
            continue
        hid = str(row.get("hypothesis_id", "")).strip()
        kind = str(row.get("kind", "")).strip().lower()
        verdict = str(row.get("verdict", "")).strip().lower()
        next_state = str(row.get("next_status", "")).strip().lower() or verdict
        confidence = _safe_float(row.get("confidence", 0.0))
        priority = _safe_float(row.get("priority", 0.0))
        commitment = row.get("inferential_commitment", {}) if isinstance(row.get("inferential_commitment"), dict) else {}
        supported = next_state in {"supported", "provisionally-supported"} or verdict in {"supported", "provisionally-supported"}
        refuted = next_state in {"refuted", "provisionally-refuted"} or verdict in {"refuted", "provisionally-refuted"}
        contrib["objects"].append(
            _obj(
                hid,
                object_type="hypothesis",
                label=str(row.get("recommended_action", "")).strip() or hid,
                nature=_hypothesis_nature(kind),
                stage="hypothesis-eval",
                kind=kind,
                state=next_state,
                score=max(priority, confidence),
                generated=True,
                prioritized=priority > 0.0,
                explored=True,
                supported=supported,
                refuted=refuted,
                related_concepts=[
                    str(commitment.get("support_antecedent_schema", "")).strip(),
                    str(commitment.get("target_consequence_schema", "")).strip(),
                    str(commitment.get("preserved_invariant", "")).strip(),
                    str(commitment.get("barrier_scope", "")).strip(),
                ],
            )
        )
        for role, key in (
            ("support_antecedent", "support_antecedent_schema"),
            ("target_consequence", "target_consequence_schema"),
            ("preserved_invariant", "preserved_invariant"),
            ("barrier_family", "barrier_scope"),
        ):
            item = _concept(commitment.get(key, ""), role, "hypothesis-eval", source=f"hypothesis_eval.{key}")
            if item:
                contrib["concepts"].append(item)
    return contrib


def _extract_hypothesis_loop(report: dict[str, Any]) -> dict[str, Any]:
    contrib = _contribution("hypothesis-loop", "Iterative support/refutation loop over hypotheses.")
    if not report:
        return contrib
    rounds = report.get("rounds", []) if isinstance(report.get("rounds"), list) else []
    final_summary = report.get("final_summary", {}) if isinstance(report.get("final_summary"), dict) else {}
    belief_revisions = report.get("belief_revision_actions", []) if isinstance(report.get("belief_revision_actions"), list) else []
    contrib["metrics"]["rounds_executed"] = len(rounds)
    contrib["metrics"]["belief_revision_count"] = len(belief_revisions)
    for key in (
        "supported_count",
        "refuted_count",
        "provisionally_supported_count",
        "provisionally_refuted_count",
        "unresolved_count",
        "open_count",
    ):
        contrib["metrics"][key] = _safe_int(final_summary.get(key, 0))

    state_map = {
        "supported": final_summary.get("supported_ids", []),
        "refuted": final_summary.get("refuted_ids", []),
        "provisionally-supported": final_summary.get("provisionally_supported_ids", []),
        "provisionally-refuted": final_summary.get("provisionally_refuted_ids", []),
        "unresolved": final_summary.get("unresolved_ids", []),
    }
    for state, ids in state_map.items():
        if not isinstance(ids, list):
            continue
        for hid in ids:
            hid_s = str(hid).strip()
            if not hid_s:
                continue
            contrib["objects"].append(
                _obj(
                    hid_s,
                    object_type="hypothesis",
                    stage="hypothesis-loop",
                    state=state,
                    explored=True,
                    supported=state in {"supported", "provisionally-supported"},
                    refuted=state in {"refuted", "provisionally-refuted"},
                )
            )

    for row in report.get("promotion_candidates", []) if isinstance(report.get("promotion_candidates"), list) else []:
        if not isinstance(row, dict):
            continue
        hid = str(row.get("hypothesis_id", "")).strip()
        if hid:
            contrib["objects"].append(
                _obj(
                    hid,
                    object_type="hypothesis",
                    stage="hypothesis-loop",
                    score=_safe_float(row.get("priority", 0.0)),
                    prioritized=True,
                    explored=True,
                )
            )
    for row in report.get("refutation_candidates", []) if isinstance(report.get("refutation_candidates"), list) else []:
        if not isinstance(row, dict):
            continue
        hid = str(row.get("hypothesis_id", "")).strip()
        if hid:
            contrib["objects"].append(
                _obj(
                    hid,
                    object_type="hypothesis",
                    stage="hypothesis-loop",
                    score=_safe_float(row.get("priority", 0.0)),
                    prioritized=True,
                    explored=True,
                )
            )
    for row in belief_revisions:
        if not isinstance(row, dict):
            continue
        hid = str(row.get("hypothesis_id", "") or row.get("target_hypothesis_id", "")).strip()
        if hid:
            contrib["objects"].append(_obj(hid, object_type="hypothesis", stage="hypothesis-loop", revised=True, explored=True))
    return contrib


def _extract_revision(report: dict[str, Any]) -> dict[str, Any]:
    contrib = _contribution("revision-loop", "Conceptual repair and representation revision program.")
    if not report:
        return contrib
    summary = report.get("revision_summary", {}) if isinstance(report.get("revision_summary"), dict) else {}
    actions = report.get("revision_actions", []) if isinstance(report.get("revision_actions"), list) else []
    priority = {
        str(item.get("revision_id", "")).strip()
        for item in (report.get("priority_program", []) if isinstance(report.get("priority_program"), list) else [])
        if isinstance(item, dict) and str(item.get("revision_id", "")).strip()
    }
    executable = report.get("executable_revision", {}) if isinstance(report.get("executable_revision"), dict) else {}
    for key in (
        "revision_count",
        "unresolved_hypotheses",
        "provisionally_refuted_hypotheses",
        "low_coherence_hypotheses",
        "conceptual_unresolved_hypotheses",
    ):
        contrib["metrics"][key] = _safe_int(summary.get(key, 0))
    if isinstance(executable.get("operator_counts"), dict):
        contrib["metrics"]["revision_operator_counts"] = {
            str(k): _safe_int(v) for k, v in executable.get("operator_counts", {}).items()
        }
    for row in actions:
        if not isinstance(row, dict):
            continue
        revision_id = str(row.get("revision_id", "")).strip()
        revision_type = str(row.get("revision_type", "")).strip()
        contrib["objects"].append(
            _obj(
                revision_id,
                object_type="revision_action",
                label=str(row.get("action", "")).strip() or revision_id,
                nature=revision_type or "revision_action",
                stage="revision-loop",
                kind=revision_type,
                state="proposed",
                generated=True,
                prioritized=revision_id in priority,
                explored=True,
                revised=True,
                related_concepts=[
                    str(row.get("trigger", "")).strip(),
                    str(row.get("success_criteria", "")).strip(),
                ],
            )
        )
        for role, raw in (
            ("revision_action_type", revision_type),
            ("conceptual_change", str(row.get("trigger", "")).strip()),
        ):
            item = _concept(raw, role, "revision-loop", source="revision.revision_actions")
            if item:
                contrib["concepts"].append(item)
    for hid in executable.get("generated_hypothesis_ids", []) if isinstance(executable.get("generated_hypothesis_ids"), list) else []:
        hid_s = str(hid).strip()
        if hid_s:
            contrib["objects"].append(
                _obj(
                    hid_s,
                    object_type="hypothesis",
                    stage="revision-loop",
                    generated=True,
                    revised=True,
                    state="generated",
                )
            )
    return contrib


def _stage_contributions(bundle: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        _extract_connect_analysis(bundle.get("analysis", {})),
        _extract_phyp(bundle.get("phyp", {})),
        _extract_coherence(bundle.get("coherence", {})),
        _extract_entrypoints(bundle.get("entrypoints", {})),
        _extract_pathways(bundle.get("pathways", {})),
        _extract_hardness(bundle.get("hardness", {})),
        _extract_bridges(bundle.get("bridges", {})),
        _extract_conjectures(bundle.get("conjectures", {})),
        _extract_strategies(bundle.get("strategies", {})),
        _extract_proof_sketches(bundle.get("proof_sketches", {})),
        _extract_hypothesis_eval(bundle.get("hypothesis_eval", {})),
        _extract_hypothesis_loop(bundle.get("hypothesis_loop", {})),
        _extract_revision(bundle.get("revision", {})),
        _extract_expert_paper(bundle.get("expert_paper", {})),
    ]


def _json_metric(value: Any) -> Any:
    if value is None or isinstance(value, (str, int, float, bool)):
        return value
    if isinstance(value, dict):
        return {str(k): _json_metric(v) for k, v in value.items()}
    if isinstance(value, (list, tuple, set)):
        return [_json_metric(v) for v in value]
    return str(value)


def _merge_metric_values(existing: Any, new_value: Any) -> Any:
    if existing is None:
        return _json_metric(new_value)
    if isinstance(existing, (int, float)) and not isinstance(existing, bool) and isinstance(new_value, (int, float)) and not isinstance(new_value, bool):
        return existing + new_value
    if isinstance(existing, dict) and isinstance(new_value, dict):
        out = dict(existing)
        for key, value in new_value.items():
            key_s = str(key)
            out[key_s] = _merge_metric_values(out.get(key_s), value)
        return out
    if isinstance(existing, list) and isinstance(new_value, list):
        out = list(existing)
        for value in new_value:
            item = _json_metric(value)
            if item not in out:
                out.append(item)
        return out
    return _json_metric(new_value)


def _merge_metrics(base: dict[str, Any], extra: dict[str, Any]) -> dict[str, Any]:
    merged = {str(k): _json_metric(v) for k, v in base.items()}
    for key, value in extra.items():
        merged[str(key)] = _merge_metric_values(merged.get(str(key)), value)
    return merged


def _fresh_accumulator() -> dict[str, Any]:
    return {
        "concepts": {},
        "objects": {},
        "reasoning_type_counts": Counter(),
        "proof_strategy_family_counts": Counter(),
        "metric_totals": {},
        "surface_taxonomy_counts": {
            "concept_natures": Counter(),
            "hypothesis_natures": Counter(),
            "concept_roles": Counter(),
            "object_types": Counter(),
            "object_states": Counter(),
            "reasoning_types": Counter(),
            "proof_strategy_families": Counter(),
        },
    }


def _register_concept(acc: dict[str, Any], item: dict[str, Any]) -> None:
    label = _canonical_label(item.get("label", ""))
    if not label:
        return
    role = str(item.get("role", "")).strip() or "concept"
    nature = str(item.get("nature", "")).strip() or _concept_nature(role, label)
    stage = str(item.get("stage", "")).strip()
    source = str(item.get("source", "")).strip()
    concepts = acc["concepts"]
    if label not in concepts:
        concepts[label] = {
            "label": label,
            "roles": {role},
            "natures": {nature},
            "first_stage": stage,
            "last_stage": stage,
            "sources": {source} if source else set(),
            "mentions": 1,
            "is_target": role in TARGET_ROLES or nature == "target-concept",
        }
        return
    record = concepts[label]
    record["roles"].add(role)
    record["natures"].add(nature)
    if source:
        record["sources"].add(source)
    if stage:
        if not record.get("first_stage"):
            record["first_stage"] = stage
        record["last_stage"] = stage
    record["mentions"] = int(record.get("mentions", 0)) + 1
    if role in TARGET_ROLES or nature == "target-concept":
        record["is_target"] = True


def _register_object(acc: dict[str, Any], item: dict[str, Any]) -> None:
    object_id = str(item.get("id", "")).strip()
    if not object_id:
        return
    stage = str(item.get("stage", "")).strip()
    objects = acc["objects"]
    if object_id not in objects:
        objects[object_id] = {
            "id": object_id,
            "object_type": str(item.get("object_type", "")).strip() or "conceptual_object",
            "label": _canonical_label(item.get("label", "")) or object_id,
            "nature": str(item.get("nature", "")).strip() or str(item.get("object_type", "")).strip() or "conceptual_object",
            "kind": str(item.get("kind", "")).strip(),
            "state": str(item.get("state", "")).strip(),
            "score": item.get("score"),
            "generated": bool(item.get("generated", False)),
            "prioritized": bool(item.get("prioritized", False)),
            "explored": bool(item.get("explored", False)),
            "formalized": bool(item.get("formalized", False)),
            "supported": bool(item.get("supported", False)),
            "refuted": bool(item.get("refuted", False)),
            "revised": bool(item.get("revised", False)),
            "proof_strategy_family": str(item.get("proof_strategy_family", "")).strip(),
            "reasoning_types": {str(x).strip() for x in item.get("reasoning_types", []) if str(x).strip()},
            "related_concepts": {_canonical_label(x) for x in item.get("related_concepts", []) if _canonical_label(x)},
            "content": _merge_detail_dict({}, item.get("content", {})),
            "first_stage": stage,
            "last_stage": stage,
            "stages": {stage} if stage else set(),
        }
        return
    record = objects[object_id]
    for key in ("generated", "prioritized", "explored", "formalized", "supported", "refuted", "revised"):
        record[key] = bool(record.get(key, False) or item.get(key, False))
    if item.get("score") is not None:
        current = record.get("score")
        if current is None:
            record["score"] = item.get("score")
        else:
            record["score"] = max(_safe_float(current), _safe_float(item.get("score")))
    for key in ("object_type", "label", "nature", "kind", "state", "proof_strategy_family"):
        value = str(item.get(key, "")).strip()
        if not value:
            continue
        existing = str(record.get(key, "")).strip()
        if not existing or existing in {"conceptual_object", "unknown", "conceptual-hypothesis"}:
            record[key] = value
        elif key == "state":
            record[key] = value
    record["reasoning_types"].update(str(x).strip() for x in item.get("reasoning_types", []) if str(x).strip())
    record["related_concepts"].update(_canonical_label(x) for x in item.get("related_concepts", []) if _canonical_label(x))
    record["content"] = _merge_detail_dict(record.get("content", {}), item.get("content", {}))
    if stage:
        if not record.get("first_stage"):
            record["first_stage"] = stage
        record["last_stage"] = stage
        record["stages"].add(stage)


def _apply_surface_taxonomy(acc: dict[str, Any], taxonomy: dict[str, Any], stage: str) -> None:
    if not isinstance(taxonomy, dict) or not taxonomy:
        return

    counter_keys = {
        "concept_natures",
        "hypothesis_natures",
        "concept_roles",
        "object_types",
        "object_states",
        "reasoning_types",
        "proof_strategy_families",
    }
    for key in counter_keys:
        value = taxonomy.get(key)
        if isinstance(value, dict):
            for item_key, item_value in value.items():
                label = str(item_key).strip()
                if label:
                    acc["surface_taxonomy_counts"][key][label] += max(1, _safe_int(item_value, 1))
        elif isinstance(value, list):
            for item in value:
                label = str(item).strip()
                if label:
                    acc["surface_taxonomy_counts"][key][label] += 1

    concept_specs = [
        ("concepts", "concept", "conceptual"),
        ("target_concepts", "target_concept", "target-concept"),
        ("focus_concepts", "focus_concept", "conceptual"),
        ("barriers", "barrier_family", "barrier-or-obstruction"),
        ("invariants", "preserved_invariant", "invariant"),
        ("abstractions", "abstraction_family", "abstraction-family"),
    ]
    for key, default_role, default_nature in concept_specs:
        values = taxonomy.get(key)
        if not isinstance(values, list):
            continue
        for item in values:
            if isinstance(item, dict):
                concept_item = _concept(
                    item.get("label", "") or item.get("name", "") or item.get("concept", ""),
                    str(item.get("role", "")).strip() or default_role,
                    stage,
                    nature=str(item.get("nature", "")).strip() or default_nature,
                    source=f"surface_taxonomy.{key}",
                )
            else:
                concept_item = _concept(item, default_role, stage, nature=default_nature, source=f"surface_taxonomy.{key}")
            if concept_item:
                _register_concept(acc, concept_item)

    object_rows: list[dict[str, Any]] = []
    for key in ("objects", "conceptual_objects", "bridge_objects"):
        value = taxonomy.get(key)
        if isinstance(value, list):
            object_rows.extend(item for item in value if isinstance(item, dict))
    if isinstance(taxonomy.get("hypotheses"), list):
        object_rows.extend(
            {
                **item,
                "object_type": str(item.get("object_type", "")).strip() or "hypothesis",
                "nature": str(item.get("nature", "")).strip() or _hypothesis_nature(item.get("kind", "")),
            }
            for item in taxonomy.get("hypotheses", [])
            if isinstance(item, dict)
        )
    for item in object_rows:
        _register_object(
            acc,
            _obj(
                str(item.get("id", "") or item.get("object_id", "") or item.get("label", "")).strip(),
                object_type=str(item.get("object_type", "")).strip() or "conceptual_object",
                label=str(item.get("label", "") or item.get("name", "")).strip(),
                nature=str(item.get("nature", "")).strip(),
                stage=stage,
                kind=str(item.get("kind", "")).strip(),
                state=str(item.get("state", "") or item.get("status", "")).strip(),
                score=_safe_float(item.get("score", 0.0)) if item.get("score") is not None else None,
                generated=bool(item.get("generated", True)),
                prioritized=bool(item.get("prioritized", False)),
                explored=bool(item.get("explored", False)),
                formalized=bool(item.get("formalized", False)),
                supported=bool(item.get("supported", False)),
                refuted=bool(item.get("refuted", False)),
                revised=bool(item.get("revised", False)),
                proof_strategy_family=str(item.get("proof_strategy_family", "")).strip(),
                reasoning_types=[str(x) for x in (item.get("reasoning_types", []) if isinstance(item.get("reasoning_types"), list) else [])],
                related_concepts=[str(x) for x in (item.get("related_concepts", []) if isinstance(item.get("related_concepts"), list) else [])],
            ),
        )

    for value in taxonomy.get("reasoning_types", []) if isinstance(taxonomy.get("reasoning_types"), list) else []:
        label = str(value).strip()
        if label:
            acc["reasoning_type_counts"][label] += 1
    for value in taxonomy.get("proof_strategy_families", []) if isinstance(taxonomy.get("proof_strategy_families"), list) else []:
        label = str(value).strip()
        if label:
            acc["proof_strategy_family_counts"][label] += 1


def _apply_contribution(acc: dict[str, Any], contribution: dict[str, Any]) -> None:
    for item in contribution.get("concepts", []) if isinstance(contribution.get("concepts"), list) else []:
        if isinstance(item, dict):
            _register_concept(acc, item)
    for item in contribution.get("objects", []) if isinstance(contribution.get("objects"), list) else []:
        if isinstance(item, dict):
            _register_object(acc, item)
    for label in contribution.get("reasoning_types", []) if isinstance(contribution.get("reasoning_types"), list) else []:
        label_s = str(label).strip()
        if label_s:
            acc["reasoning_type_counts"][label_s] += 1
    for label in contribution.get("proof_strategy_families", []) if isinstance(contribution.get("proof_strategy_families"), list) else []:
        label_s = str(label).strip()
        if label_s:
            acc["proof_strategy_family_counts"][label_s] += 1
    metrics = contribution.get("metrics", {}) if isinstance(contribution.get("metrics"), dict) else {}
    acc["metric_totals"] = _merge_metrics(acc.get("metric_totals", {}), metrics)


def _object_lifecycle_status(item: dict[str, Any]) -> str:
    state = str(item.get("state", "")).strip().lower()
    if state in {
        "supported",
        "refuted",
        "provisionally-supported",
        "provisionally-refuted",
        "unresolved",
        "open",
        "inconclusive",
        "tentative",
        "needs-testing",
        "generated",
        "proposed",
    }:
        return state
    if item.get("refuted", False):
        return "refuted"
    if item.get("supported", False):
        return "supported"
    if item.get("revised", False):
        return "revised"
    if item.get("formalized", False):
        return "formalized"
    if item.get("explored", False):
        return "explored"
    if item.get("prioritized", False):
        return "prioritized"
    if item.get("generated", False):
        return "generated"
    return "registered"


def _preferred_value(values: set[str], fallback: str) -> str:
    ranked = [
        "target-concept",
        "invariant",
        "bridge-object",
        "abstraction-family",
        "barrier-or-obstruction",
        "representation-change",
        "formalization-commitment",
        "entrypoint-anchor",
        "antecedent-concept",
        "conceptual",
    ]
    for item in ranked:
        if item in values:
            return item
    return sorted(values)[0] if values else fallback


def _informative_label(value: Any) -> str:
    """
    Relevance: Operates within the orchestration and observability layer.
    Concept: Filtering placeholder labels before content summarization.
    Contribution: Keeps the conceptual dashboard focused on mathematical content instead of null markers.
    """

    text = _canonical_label(value)
    if text.lower() in {"", "none", "n/a", "unknown", "null"}:
        return ""
    return text


def _concept_summary(record: dict[str, Any]) -> dict[str, Any]:
    """
    Relevance: Operates within the orchestration and observability layer.
    Concept: Compact serialization of a concept record for dashboard consumption.
    Contribution: Makes stage-level concept evolution readable without exposing accumulator internals.
    """

    label = _informative_label(record.get("label", ""))
    nature = _preferred_value(set(record.get("natures", set())), "conceptual")
    roles = sorted(str(x).strip() for x in record.get("roles", set()) if str(x).strip())
    return {
        "label": label,
        "nature": nature,
        "roles": roles[:3],
        "mentions": int(record.get("mentions", 0)),
        "first_stage": str(record.get("first_stage", "")).strip(),
        "last_stage": str(record.get("last_stage", "")).strip(),
    }


def _object_summary(record: dict[str, Any]) -> dict[str, Any]:
    """
    Relevance: Operates within the orchestration and observability layer.
    Concept: Compact serialization of a conceptual object for dashboard consumption.
    Contribution: Keeps proof objects and hypotheses inspectable in a content-oriented summary view.
    """

    status = _object_lifecycle_status(record)
    score = record.get("score")
    related = [
        label
        for label in (_informative_label(x) for x in sorted(record.get("related_concepts", set())))
        if label
    ]
    content = record.get("content", {}) if isinstance(record.get("content"), dict) else {}
    return {
        "id": str(record.get("id", "")).strip(),
        "label": _informative_label(record.get("label", "")) or str(record.get("id", "")).strip(),
        "object_type": str(record.get("object_type", "")).strip() or "conceptual_object",
        "nature": str(record.get("nature", "")).strip() or "conceptual_object",
        "status": status,
        "score": round(_safe_float(score, 0.0), 4) if score is not None else None,
        "proof_strategy_family": str(record.get("proof_strategy_family", "")).strip(),
        "stage": str(record.get("last_stage", "")).strip(),
        "related_concepts": related[:4],
        "content": {
            "route_synopsis": _first_nonempty(content.get("route_synopsis", ""), limit=320),
            "statement_delta": _statement_delta_payload(content.get("statement_delta", {})),
            "carrier_kind": _first_nonempty(content.get("carrier_kind", ""), limit=180),
            "typing_status": _first_nonempty(content.get("typing_status", ""), limit=60),
            "source_excerpt": _first_nonempty(content.get("source_excerpt", ""), limit=260),
            "target_excerpt": _first_nonempty(content.get("target_excerpt", ""), limit=260),
            "bridge_definition": _first_nonempty(content.get("bridge_definition", ""), limit=360),
            "conditional_claim": _first_nonempty(content.get("conditional_claim", ""), limit=320),
            "assumptions": _clean_display_list(content.get("assumptions", []), limit=4, text_limit=220),
            "obligations": _clean_display_list(content.get("obligations", []), limit=4, text_limit=220),
            "lemmas": _clean_display_list(content.get("lemmas", []), limit=4, text_limit=220),
            "proof_outline": _clean_display_list(content.get("proof_outline", []), limit=3, text_limit=200),
            "failure_diagnosis": _first_nonempty(content.get("failure_diagnosis", ""), limit=260),
            "counterfactual": _first_nonempty(content.get("counterfactual", ""), limit=260),
        },
    }


def _concept_priority(record: dict[str, Any]) -> tuple[Any, ...]:
    """
    Relevance: Operates within the orchestration and observability layer.
    Concept: Salience ranking over conceptual entities.
    Contribution: Prefers mathematical targets, invariants, and bridge objects when the dashboard selects highlights.
    """

    nature = _preferred_value(set(record.get("natures", set())), "conceptual")
    label = _informative_label(record.get("label", ""))
    roles = {str(x).strip() for x in record.get("roles", set()) if str(x).strip()}
    role_score = max((ROLE_HIGHLIGHT_PRIORITY.get(role, 0) for role in roles), default=0)
    specificity = min(6, len([token for token in re.split(r"[-_/ ]+", label.lower()) if token]))
    generic_flag = 0 if label.lower() in GENERIC_CONCEPT_LABELS else 1
    return (
        CONCEPT_HIGHLIGHT_PRIORITY.get(nature, 0),
        role_score,
        generic_flag,
        specificity,
        1 if bool(record.get("is_target", False)) else 0,
        int(record.get("mentions", 0)),
        str(record.get("last_stage", "")).strip(),
        label.lower(),
    )


def _object_priority(record: dict[str, Any]) -> tuple[Any, ...]:
    """
    Relevance: Operates within the orchestration and observability layer.
    Concept: Salience ranking over proof-relevant objects.
    Contribution: Ensures the dashboard foregrounds proof sketches, bridges, and mature hypotheses before auxiliary bookkeeping.
    """

    object_type = str(record.get("object_type", "")).strip() or "conceptual_object"
    status = _object_lifecycle_status(record)
    score = _safe_float(record.get("score"), 0.0) if record.get("score") is not None else 0.0
    return (
        OBJECT_HIGHLIGHT_PRIORITY.get(object_type, 0),
        STATUS_HIGHLIGHT_PRIORITY.get(status, 0),
        1 if bool(record.get("formalized", False)) else 0,
        1 if bool(record.get("prioritized", False)) else 0,
        1 if bool(record.get("supported", False)) else 0,
        score,
        _informative_label(record.get("label", "")).lower(),
    )


def _top_concept_summaries(
    acc: dict[str, Any],
    *,
    limit: int = 6,
    stage: str = "",
    natures: set[str] | None = None,
    roles: set[str] | None = None,
    introduced_only: bool = False,
    recent_only: bool = False,
) -> list[dict[str, Any]]:
    """
    Relevance: Operates within the orchestration and observability layer.
    Concept: Content-oriented selection of salient concepts.
    Contribution: Makes stage summaries about mathematical content rather than raw counts.
    """

    selected: list[dict[str, Any]] = []
    for record in acc.get("concepts", {}).values():
        if not isinstance(record, dict):
            continue
        label = _informative_label(record.get("label", ""))
        if not label:
            continue
        natures_set = {str(x).strip() for x in record.get("natures", set()) if str(x).strip()}
        roles_set = {str(x).strip() for x in record.get("roles", set()) if str(x).strip()}
        if introduced_only and str(record.get("first_stage", "")).strip() != stage:
            continue
        if recent_only and str(record.get("last_stage", "")).strip() != stage:
            continue
        if natures and not (natures_set & natures):
            continue
        if roles and not (roles_set & roles):
            continue
        selected.append(record)
    selected.sort(key=_concept_priority, reverse=True)
    return [_concept_summary(record) for record in selected[:limit]]


def _top_object_summaries(
    acc: dict[str, Any],
    *,
    limit: int = 6,
    stage: str = "",
    object_types: set[str] | None = None,
    statuses: set[str] | None = None,
    introduced_only: bool = False,
    recent_only: bool = False,
) -> list[dict[str, Any]]:
    """
    Relevance: Operates within the orchestration and observability layer.
    Concept: Content-oriented selection of salient conceptual objects.
    Contribution: Surfaces bridges, conjectures, proof sketches, and hypotheses that carry the mathematical narrative.
    """

    selected: list[dict[str, Any]] = []
    for record in acc.get("objects", {}).values():
        if not isinstance(record, dict):
            continue
        if introduced_only and str(record.get("first_stage", "")).strip() != stage:
            continue
        if recent_only and str(record.get("last_stage", "")).strip() != stage:
            continue
        object_type = str(record.get("object_type", "")).strip() or "conceptual_object"
        if object_types and object_type not in object_types:
            continue
        status = _object_lifecycle_status(record)
        if statuses and status not in statuses:
            continue
        if not _informative_label(record.get("label", "")) and not str(record.get("id", "")).strip():
            continue
        selected.append(record)
    selected.sort(key=_object_priority, reverse=True)
    return [_object_summary(record) for record in selected[:limit]]


def _top_counter_rows(counter: Counter[str], *, limit: int = 6) -> list[dict[str, Any]]:
    """
    Relevance: Operates within the orchestration and observability layer.
    Concept: Compact serialization of ranked categorical counts.
    Contribution: Makes proof families and reasoning modes easy to render as content highlights.
    """

    return [
        {"label": str(label), "count": int(count)}
        for label, count in counter.most_common(limit)
        if str(label).strip()
    ]


def _object_content_signal(row: dict[str, Any]) -> int:
    """
    Relevance: Operates within the orchestration and observability layer.
    Concept: Lightweight scoring over serialized object summaries.
    Contribution: Lets stage views pick the object whose mathematical payload is most inspectable.
    """

    if not isinstance(row, dict):
        return 0
    content = row.get("content", {}) if isinstance(row.get("content"), dict) else {}
    score = 0
    for key in ("route_synopsis", "source_excerpt", "target_excerpt", "bridge_definition", "conditional_claim", "failure_diagnosis", "counterfactual"):
        if _informative_label(content.get(key, "")):
            score += 2
    delta = content.get("statement_delta", {}) if isinstance(content.get("statement_delta"), dict) else {}
    score += len([1 for value in delta.values() if _informative_label(value)])
    score += len(_clean_display_list(content.get("assumptions", []), limit=6, text_limit=220))
    score += len(_clean_display_list(content.get("obligations", []), limit=6, text_limit=220))
    score += len(_clean_display_list(content.get("lemmas", []), limit=6, text_limit=220))
    score += len(_clean_display_list(content.get("proof_outline", []), limit=6, text_limit=220))
    return score


def _select_dossiers(*groups: list[dict[str, Any]], limit: int = 4) -> list[dict[str, Any]]:
    """
    Relevance: Operates within the orchestration and observability layer.
    Concept: Dedupe-and-rank helper over stage object summaries.
    Contribution: Produces inspectable primary and supporting dossiers for the content-first dashboard.
    """

    ranked: list[dict[str, Any]] = []
    seen: set[str] = set()
    for group in groups:
        for row in group:
            if not isinstance(row, dict):
                continue
            key = str(row.get("id", "")).strip() or str(row.get("label", "")).strip()
            if not key or key in seen:
                continue
            seen.add(key)
            ranked.append(row)
    ranked.sort(
        key=lambda row: (
            _object_content_signal(row),
            OBJECT_HIGHLIGHT_PRIORITY.get(str(row.get("object_type", "")).strip() or "conceptual_object", 0),
            STATUS_HIGHLIGHT_PRIORITY.get(str(row.get("status", "")).strip(), 0),
            _safe_float(row.get("score"), 0.0) if row.get("score") is not None else 0.0,
            str(row.get("label", "")).lower(),
        ),
        reverse=True,
    )
    return ranked[:limit]


def _content_highlights(acc: dict[str, Any], stage: str) -> dict[str, Any]:
    """
    Relevance: Operates within the orchestration and observability layer.
    Concept: Synthesis of stage-local and cumulative mathematical highlights.
    Contribution: Reorients the conceptual dashboard toward content evolution rather than execution telemetry.
    """

    stage_targets = _top_concept_summaries(
        acc,
        stage=stage,
        natures={"target-concept"},
        roles=TARGET_ROLES,
        introduced_only=True,
    )
    stage_invariants = _top_concept_summaries(acc, stage=stage, natures={"invariant"}, introduced_only=True)
    stage_bridge_objects = _top_concept_summaries(
        acc,
        stage=stage,
        natures={"bridge-object", "abstraction-family"},
        introduced_only=True,
    )
    stage_formalizations = _top_concept_summaries(
        acc,
        stage=stage,
        natures={"formalization-commitment"},
        introduced_only=True,
    )

    stage_bridges = _top_object_summaries(acc, stage=stage, object_types={"bridge_program"}, recent_only=True)
    stage_conjectures = _top_object_summaries(acc, stage=stage, object_types={"abstraction_conjecture"}, recent_only=True)
    stage_proof_sketches = _top_object_summaries(acc, stage=stage, object_types={"proof_sketch"}, recent_only=True)
    stage_hypotheses = _top_object_summaries(acc, stage=stage, object_types={"hypothesis"}, recent_only=True)

    proof_family_counts: Counter[str] = Counter()
    reasoning_mode_counts: Counter[str] = Counter()
    for record in acc.get("objects", {}).values():
        if not isinstance(record, dict):
            continue
        if str(record.get("last_stage", "")).strip() != stage:
            continue
        family = str(record.get("proof_strategy_family", "")).strip()
        if family:
            proof_family_counts[family] += 1
        for label in record.get("reasoning_types", set()):
            label_s = str(label).strip()
            if label_s:
                reasoning_mode_counts[label_s] += 1

    leading_targets = _top_concept_summaries(
        acc,
        natures={"target-concept"},
        roles=TARGET_ROLES,
        limit=8,
    )
    leading_invariants = _top_concept_summaries(acc, natures={"invariant"}, limit=8)
    leading_bridge_objects = _top_concept_summaries(acc, natures={"bridge-object", "abstraction-family"}, limit=8)
    leading_formalizations = _top_concept_summaries(acc, natures={"formalization-commitment"}, limit=8)

    leading_bridges = _top_object_summaries(acc, object_types={"bridge_program"}, limit=6)
    leading_conjectures = _top_object_summaries(acc, object_types={"abstraction_conjecture"}, limit=6)
    leading_proof_sketches = _top_object_summaries(acc, object_types={"proof_sketch"}, limit=6)
    supported_hypotheses = _top_object_summaries(acc, object_types={"hypothesis"}, statuses={"supported", "provisionally-supported"}, limit=6)
    frontier_hypotheses = _top_object_summaries(acc, object_types={"hypothesis"}, statuses=OPEN_HYPOTHESIS_STATES, limit=6)
    dossier_candidates = _select_dossiers(
        stage_proof_sketches,
        stage_bridges,
        stage_conjectures,
        stage_hypotheses,
        leading_proof_sketches,
        leading_bridges,
        leading_conjectures,
        supported_hypotheses,
        frontier_hypotheses,
        limit=5,
    )
    primary_dossier = dossier_candidates[0] if dossier_candidates else {}

    headline_parts: list[str] = []
    primary_route = _first_nonempty(
        ((primary_dossier.get("content", {}) if isinstance(primary_dossier.get("content"), dict) else {}).get("route_synopsis", "")),
        ((primary_dossier.get("content", {}) if isinstance(primary_dossier.get("content"), dict) else {}).get("conditional_claim", "")),
        ((primary_dossier.get("content", {}) if isinstance(primary_dossier.get("content"), dict) else {}).get("bridge_definition", "")),
        limit=320,
    )
    if primary_route:
        headline_parts.append(primary_route)
    if stage_targets:
        headline_parts.append("targets " + ", ".join(item["label"] for item in stage_targets[:2]))
    if stage_invariants:
        headline_parts.append("invariants " + ", ".join(item["label"] for item in stage_invariants[:2]))
    if stage_bridge_objects:
        headline_parts.append("bridge objects " + ", ".join(item["label"] for item in stage_bridge_objects[:2]))
    proof_families = _top_counter_rows(proof_family_counts, limit=3)
    if proof_families:
        headline_parts.append("proof families " + ", ".join(item["label"] for item in proof_families))
    if not headline_parts and leading_targets:
        headline_parts.append("dominant targets " + ", ".join(item["label"] for item in leading_targets[:2]))

    return {
        "headline": "; ".join(headline_parts) if headline_parts else "No strong content shift was surfaced at this stage.",
        "introduced_targets": stage_targets,
        "introduced_invariants": stage_invariants,
        "introduced_bridge_objects": stage_bridge_objects,
        "introduced_formalizations": stage_formalizations,
        "stage_bridges": stage_bridges,
        "stage_conjectures": stage_conjectures,
        "stage_proof_sketches": stage_proof_sketches,
        "stage_hypotheses": stage_hypotheses,
        "stage_proof_families": proof_families,
        "stage_reasoning_modes": _top_counter_rows(reasoning_mode_counts, limit=6),
        "leading_targets": leading_targets,
        "leading_invariants": leading_invariants,
        "leading_bridge_objects": leading_bridge_objects,
        "leading_formalizations": leading_formalizations,
        "leading_bridges": leading_bridges,
        "leading_conjectures": leading_conjectures,
        "leading_proof_sketches": leading_proof_sketches,
        "supported_hypotheses": supported_hypotheses,
        "frontier_hypotheses": frontier_hypotheses,
        "primary_dossier": primary_dossier,
        "supporting_dossiers": dossier_candidates[1:],
    }


def _state_snapshot(acc: dict[str, Any]) -> dict[str, Any]:
    concept_natures: Counter[str] = Counter()
    concept_roles: Counter[str] = Counter()
    target_concepts = 0
    for record in acc.get("concepts", {}).values():
        if not isinstance(record, dict):
            continue
        nature = _preferred_value(set(record.get("natures", set())), "conceptual")
        role = sorted(record.get("roles", set()))[0] if record.get("roles") else "concept"
        concept_natures[nature] += 1
        concept_roles[role] += 1
        if bool(record.get("is_target", False)):
            target_concepts += 1

    object_type_counts: Counter[str] = Counter()
    object_status_counts: Counter[str] = Counter()
    hypothesis_natures: Counter[str] = Counter()
    hypothesis_states: Counter[str] = Counter()
    lifecycle_totals: Counter[str] = Counter()
    frontier: list[dict[str, Any]] = []

    for record in acc.get("objects", {}).values():
        if not isinstance(record, dict):
            continue
        object_type = str(record.get("object_type", "")).strip() or "conceptual_object"
        status = _object_lifecycle_status(record)
        object_type_counts[object_type] += 1
        object_status_counts[status] += 1
        for key in ("generated", "prioritized", "explored", "formalized", "supported", "refuted", "revised"):
            if bool(record.get(key, False)):
                lifecycle_totals[key] += 1
        if status in OPEN_HYPOTHESIS_STATES or status in {"proposed", "generated"}:
            lifecycle_totals["open"] += 1
        if bool(record.get("generated", False)) and not bool(record.get("explored", False)):
            lifecycle_totals["unexplored"] += 1
        if object_type == "hypothesis":
            hypothesis_natures[str(record.get("nature", "")).strip() or "hypothesis"] += 1
            hypothesis_states[status] += 1

        score = record.get("score")
        score_f = _safe_float(score, 0.0) if score is not None else 0.0
        is_open_hypothesis = object_type == "hypothesis" and status in OPEN_HYPOTHESIS_STATES
        is_open_bridge = (
            object_type in {"bridge_program", "abstraction_conjecture", "proof_sketch", "strategy"}
            and not bool(record.get("formalized", False))
            and not bool(record.get("supported", False))
            and not bool(record.get("refuted", False))
            and (bool(record.get("prioritized", False)) or bool(record.get("explored", False)))
        )
        if is_open_hypothesis or is_open_bridge:
            frontier.append(
                {
                    "id": record.get("id", ""),
                    "label": record.get("label", ""),
                    "object_type": object_type,
                    "nature": record.get("nature", ""),
                    "status": status,
                    "score": round(score_f, 4) if score is not None else None,
                    "stage": record.get("last_stage", ""),
                    "related_concepts": sorted(record.get("related_concepts", set()))[:6],
                }
            )

    frontier.sort(
        key=lambda item: (
            0 if item.get("object_type", "") == "hypothesis" else 1,
            -_safe_float(item.get("score"), 0.0),
            str(item.get("label", "")).lower(),
        )
    )

    return {
        "concept_count": len(acc.get("concepts", {})),
        "target_concept_count": target_concepts,
        "concept_nature_counts": dict(concept_natures),
        "concept_role_counts": dict(concept_roles),
        "object_count": len(acc.get("objects", {})),
        "object_type_counts": dict(object_type_counts),
        "object_status_counts": dict(object_status_counts),
        "hypothesis_count": int(object_type_counts.get("hypothesis", 0)),
        "hypothesis_nature_counts": dict(hypothesis_natures),
        "hypothesis_state_counts": dict(hypothesis_states),
        "lifecycle_totals": dict(lifecycle_totals),
        "reasoning_type_counts": dict(acc.get("reasoning_type_counts", Counter())),
        "reasoning_type_diversity": len(acc.get("reasoning_type_counts", Counter())),
        "proof_strategy_family_counts": dict(acc.get("proof_strategy_family_counts", Counter())),
        "proof_strategy_diversity": len(acc.get("proof_strategy_family_counts", Counter())),
        "surface_taxonomy_counts": {
            key: dict(value) for key, value in acc.get("surface_taxonomy_counts", {}).items() if value
        },
        "frontier": frontier[:14],
    }


def _normalize_surface_stage(moment: dict[str, Any], agent: str) -> str:
    direct = _normalize_stage_id(moment.get("stage", ""))
    if direct in STAGE_ORDER:
        return direct

    focus = str(moment.get("focus", "")).strip()
    title = str(moment.get("title", "")).strip()
    kind = str(moment.get("kind", "")).strip()
    alias_map = {
        "connect": "connect.analyze",
        "generate-phyp": "connect.generate-phyp",
        "generate phyp": "connect.generate-phyp",
        "coherence": "coherence-eval",
        "entrypoints": "entrypoints.rank",
        "pathways": "entrypoints.pathways",
        "proof-sketches": "proof-sketch",
        "hypothesis-evaluation": "hypothesis-eval",
        "hypothesis-refutation-loop": "hypothesis-loop",
    }
    for raw in (direct, focus, title):
        candidate = str(raw).strip().lower()
        if not candidate:
            continue
        if candidate in STAGE_ORDER:
            return candidate
        if candidate in alias_map:
            return alias_map[candidate]
        for stage in STAGE_ORDER:
            if candidate == stage.lower():
                return stage
            if stage.lower() in candidate:
                return stage
    agent_map = {
        "kb-proof-connector": "connect.generate-phyp" if "hypothesis" in f"{focus} {title}".lower() else "connect.analyze",
        "kb-coherence-evaluator": "coherence-eval",
        "kb-entrypoint-finder": "entrypoints.rank",
        "kb-entrypoint-pathfinder": "entrypoints.pathways",
        "kb-epistemic-hardness": "hardness",
        "kb-concept-bridge-planner": "bridge-plan",
        "kb-gap-abstraction-conjecturer": "conjecture",
        "kb-novel-proof-strategist": "strategies",
        "kb-proof-sketcher": "proof-sketch",
        "kb-hypothesis-evaluator": "hypothesis-eval",
        "kb-hypothesis-refutation-loop": "hypothesis-loop",
        "kb-revision-loop": "revision-loop",
        "kb-expert-paper-generator": "expert-paper",
    }
    if kind in {"stage_delegation", "stage_completion"} and focus in STAGE_ORDER:
        return focus
    return agent_map.get(agent, "")


def _group_surface_moments(surfaces: list[dict[str, Any]]) -> dict[str, list[dict[str, Any]]]:
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for item in surfaces:
        if not isinstance(item, dict):
            continue
        agent = str(item.get("agent", "")).strip() or "unknown"
        if agent in OBSERVABILITY_AGENTS:
            continue
        for moment in item.get("moments", []) if isinstance(item.get("moments"), list) else []:
            if not isinstance(moment, dict):
                continue
            stage = _normalize_surface_stage(moment, agent)
            if not stage:
                continue
            grouped[stage].append(
                {
                    "timestamp": str(moment.get("timestamp", "")).strip(),
                    "agent": agent,
                    "kind": str(moment.get("kind", "")).strip() or "conceptual_move",
                    "title": str(moment.get("title", "")).strip(),
                    "focus": str(moment.get("focus", "")).strip(),
                    "significance": str(moment.get("significance", "")).strip(),
                    "details": [str(x).strip() for x in (moment.get("details", []) if isinstance(moment.get("details"), list) else []) if str(x).strip()],
                    "taxonomy": moment.get("taxonomy", {}) if isinstance(moment.get("taxonomy"), dict) else {},
                    "metrics": moment.get("metrics", {}) if isinstance(moment.get("metrics"), dict) else {},
                    "tags": [str(x).strip() for x in (moment.get("tags", []) if isinstance(moment.get("tags"), list) else []) if str(x).strip()],
                }
            )
    for stage in grouped:
        grouped[stage].sort(key=lambda row: (row.get("timestamp", ""), row.get("agent", ""), row.get("title", "")))
    return grouped


def _snapshot(
    acc: dict[str, Any],
    *,
    stage: str,
    description: str,
    stage_index: int,
    before: dict[str, Any],
    metrics: dict[str, Any],
    surface_events: list[dict[str, Any]],
    has_artifact_contribution: bool,
    cumulative_surface_moment_count: int,
) -> dict[str, Any]:
    state = _state_snapshot(acc)
    state["highlights"] = _content_highlights(acc, stage)
    kind_counts: Counter[str] = Counter()
    focus_counts: Counter[str] = Counter()
    agents = set()
    last_timestamp = ""
    for event in surface_events:
        if not isinstance(event, dict):
            continue
        kind = str(event.get("kind", "")).strip() or "conceptual_move"
        focus = str(event.get("focus", "")).strip()
        agent = str(event.get("agent", "")).strip()
        kind_counts[kind] += 1
        if focus:
            focus_counts[focus] += 1
        if agent:
            agents.add(agent)
        last_timestamp = max(last_timestamp, str(event.get("timestamp", "")).strip())
    delta = {
        "concept_gain": state.get("concept_count", 0) - before.get("concept_count", 0),
        "target_concept_gain": state.get("target_concept_count", 0) - before.get("target_concept_count", 0),
        "object_gain": state.get("object_count", 0) - before.get("object_count", 0),
        "hypothesis_gain": state.get("hypothesis_count", 0) - before.get("hypothesis_count", 0),
        "formalized_gain": state.get("lifecycle_totals", {}).get("formalized", 0) - before.get("lifecycle_totals", {}).get("formalized", 0),
        "supported_gain": state.get("lifecycle_totals", {}).get("supported", 0) - before.get("lifecycle_totals", {}).get("supported", 0),
        "refuted_gain": state.get("lifecycle_totals", {}).get("refuted", 0) - before.get("lifecycle_totals", {}).get("refuted", 0),
        "reasoning_diversity_gain": state.get("reasoning_type_diversity", 0) - before.get("reasoning_type_diversity", 0),
        "proof_family_diversity_gain": state.get("proof_strategy_diversity", 0) - before.get("proof_strategy_diversity", 0),
    }
    return {
        "stage": stage,
        "description": description,
        "stage_index": stage_index,
        "timestamp": last_timestamp,
        "source": {
            "has_artifact_contribution": has_artifact_contribution,
            "surface_moment_count": len(surface_events),
            "surface_agents": sorted(agents),
        },
        "metrics": metrics,
        "delta": delta,
        "surface": {
            "moment_count": len(surface_events),
            "cumulative_moment_count": cumulative_surface_moment_count,
            "kind_counts": dict(kind_counts),
            "top_focuses": [{"focus": focus, "count": count} for focus, count in focus_counts.most_common(8)],
            "qualitative_events": surface_events[:10],
        },
        "state": state,
    }


def _build_conceptual_dynamics(
    *,
    repo_root: Path,
    artifacts_dir: Path,
    surfaces: list[dict[str, Any]],
    kb: str,
    kb_ref: str,
    selected_run_id: str,
    selection_reason: str,
) -> dict[str, Any]:
    bundle = _artifact_bundle(repo_root, artifacts_dir)
    contributions = _stage_contributions(bundle)
    contribution_by_stage: dict[str, dict[str, Any]] = {}
    for item in contributions:
        if not isinstance(item, dict):
            continue
        contribution_by_stage[str(item.get("stage", "")).strip()] = item
    grouped_surfaces = _group_surface_moments(surfaces)

    observed = {stage for stage, item in contribution_by_stage.items() if item}
    observed.update(stage for stage, rows in grouped_surfaces.items() if rows)
    ordered_stages = [stage for stage in STAGE_ORDER if stage in observed]
    ordered_stages.extend(sorted(stage for stage in observed if stage not in STAGE_ORDER))

    acc = _fresh_accumulator()
    timeline: list[dict[str, Any]] = []
    surface_kind_counts: Counter[str] = Counter()
    surface_focus_counts: Counter[str] = Counter()
    cumulative_surface_count = 0
    stage_index_rows: list[dict[str, Any]] = []

    for idx, stage in enumerate(ordered_stages):
        contribution = contribution_by_stage.get(stage, {})
        description = str(contribution.get("description", "")).strip() or "Surfaced conceptual progression."
        before = _state_snapshot(acc)
        has_artifact_contribution = False
        stage_metrics: dict[str, Any] = {}
        if contribution:
            has_artifact_contribution = any(
                bool(contribution.get(key)) for key in ("concepts", "objects", "metrics", "notes", "reasoning_types", "proof_strategy_families")
            )
            _apply_contribution(acc, contribution)
            if isinstance(contribution.get("metrics"), dict):
                stage_metrics = _merge_metrics(stage_metrics, contribution.get("metrics", {}))
        stage_surfaces = grouped_surfaces.get(stage, [])
        for event in stage_surfaces:
            taxonomy = event.get("taxonomy", {}) if isinstance(event.get("taxonomy"), dict) else {}
            metrics = event.get("metrics", {}) if isinstance(event.get("metrics"), dict) else {}
            _apply_surface_taxonomy(acc, taxonomy, stage)
            stage_metrics = _merge_metrics(stage_metrics, metrics)
            surface_kind_counts[str(event.get("kind", "")).strip() or "conceptual_move"] += 1
            focus = str(event.get("focus", "")).strip()
            if focus:
                surface_focus_counts[focus] += 1
        cumulative_surface_count += len(stage_surfaces)
        snapshot = _snapshot(
            acc,
            stage=stage,
            description=description,
            stage_index=idx,
            before=before,
            metrics=stage_metrics,
            surface_events=stage_surfaces,
            has_artifact_contribution=has_artifact_contribution,
            cumulative_surface_moment_count=cumulative_surface_count,
        )
        timeline.append(snapshot)
        stage_index_rows.append(
            {
                "stage": stage,
                "has_artifact_contribution": has_artifact_contribution,
                "surface_moment_count": len(stage_surfaces),
                "concept_count": snapshot.get("state", {}).get("concept_count", 0),
                "hypothesis_count": snapshot.get("state", {}).get("hypothesis_count", 0),
            }
        )

    current = timeline[-1]["state"] if timeline else _state_snapshot(acc)
    return {
        "metadata": {
            "generated_utc": dt.datetime.now(dt.UTC).isoformat(),
            "kb": kb,
            "kb_ref": kb_ref,
            "artifacts_dir": str(artifacts_dir),
            "selected_run_id": selected_run_id,
            "run_selection_reason": selection_reason,
            "surface_count": len(surfaces),
        },
        "summary": {
            "stage_count": len(timeline),
            "surface_count": len(surfaces),
            "surface_moment_count": sum(len(rows) for rows in grouped_surfaces.values()),
            "surface_kind_counts": dict(surface_kind_counts),
            "top_surface_focuses": [{"focus": focus, "count": count} for focus, count in surface_focus_counts.most_common(10)],
            "current": current,
            "stages": stage_index_rows,
        },
        "timeline": timeline,
    }


def _to_markdown(report: dict[str, Any]) -> str:
    meta = report.get("metadata", {}) if isinstance(report.get("metadata"), dict) else {}
    summary = report.get("summary", {}) if isinstance(report.get("summary"), dict) else {}
    current = summary.get("current", {}) if isinstance(summary.get("current"), dict) else {}
    timeline = report.get("timeline", []) if isinstance(report.get("timeline"), list) else []

    def _counter_text(payload: Any, limit: int = 8) -> str:
        if not isinstance(payload, dict) or not payload:
            return "none"
        ordered = sorted(payload.items(), key=lambda item: (-_safe_float(item[1], 0.0), str(item[0])))
        return ", ".join(f"{key}={value}" for key, value in ordered[:limit])

    lines: list[str] = []
    lines.append("# Conceptual Dynamics Dashboard")
    lines.append("")
    lines.append("This report monitors the evolution of conceptual objects, hypotheses, and reasoning styles across the active run.")
    lines.append("")
    lines.append("## Run Context")
    lines.append("")
    lines.append(f"- Generated (UTC): {meta.get('generated_utc', '')}")
    lines.append(f"- KB: {meta.get('kb', '')}")
    lines.append(f"- KB Ref: {meta.get('kb_ref', '')}")
    lines.append(f"- Artifacts directory: {meta.get('artifacts_dir', '')}")
    lines.append(f"- Selected run ID: {meta.get('selected_run_id', '') or '(none)'}")
    lines.append(f"- Run selection reason: {meta.get('run_selection_reason', '')}")
    lines.append("")
    lines.append("## Current State")
    lines.append("")
    lines.append(f"- Concepts: {current.get('concept_count', 0)}")
    lines.append(f"- Target concepts: {current.get('target_concept_count', 0)}")
    lines.append(f"- Concept natures: {_counter_text(current.get('concept_nature_counts', {}))}")
    lines.append(f"- Objects: {current.get('object_count', 0)}")
    lines.append(f"- Hypotheses: {current.get('hypothesis_count', 0)}")
    lines.append(f"- Hypothesis natures: {_counter_text(current.get('hypothesis_nature_counts', {}))}")
    lines.append(f"- Hypothesis states: {_counter_text(current.get('hypothesis_state_counts', {}))}")
    lines.append(f"- Lifecycle totals: {_counter_text(current.get('lifecycle_totals', {}))}")
    lines.append(f"- Reasoning types: {_counter_text(current.get('reasoning_type_counts', {}))}")
    lines.append(f"- Proof strategy families: {_counter_text(current.get('proof_strategy_family_counts', {}))}")
    lines.append(f"- Surface moments: {summary.get('surface_moment_count', 0)}")
    lines.append("")
    lines.append("## Stage Evolution")
    lines.append("")
    lines.append("| stage | concepts | targets | hypotheses | open | formalized | supported | refuted | reasoning_types | proof_families | surfaced_moves |")
    lines.append("|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|")
    for item in timeline:
        if not isinstance(item, dict):
            continue
        state = item.get("state", {}) if isinstance(item.get("state"), dict) else {}
        lifecycle = state.get("lifecycle_totals", {}) if isinstance(state.get("lifecycle_totals"), dict) else {}
        surface = item.get("surface", {}) if isinstance(item.get("surface"), dict) else {}
        lines.append(
            f"| {str(item.get('stage', '')).replace('|', '\\|')} "
            f"| {state.get('concept_count', 0)} "
            f"| {state.get('target_concept_count', 0)} "
            f"| {state.get('hypothesis_count', 0)} "
            f"| {lifecycle.get('open', 0)} "
            f"| {lifecycle.get('formalized', 0)} "
            f"| {lifecycle.get('supported', 0)} "
            f"| {lifecycle.get('refuted', 0)} "
            f"| {state.get('reasoning_type_diversity', 0)} "
            f"| {state.get('proof_strategy_diversity', 0)} "
            f"| {surface.get('moment_count', 0)} |"
        )
    lines.append("")
    lines.append("## Open Frontier")
    lines.append("")
    frontier = current.get("frontier", []) if isinstance(current.get("frontier"), list) else []
    if not frontier:
        lines.append("- none")
    for row in frontier[:12]:
        if not isinstance(row, dict):
            continue
        lines.append(
            f"- {row.get('id', '')}: {row.get('label', '')} "
            f"| type={row.get('object_type', '')} "
            f"| status={row.get('status', '')} "
            f"| stage={row.get('stage', '')}"
            + (f" | score={row.get('score', '')}" if row.get("score") is not None else "")
        )
    lines.append("")
    lines.append("## Surface Focus")
    lines.append("")
    top_focuses = summary.get("top_surface_focuses", []) if isinstance(summary.get("top_surface_focuses"), list) else []
    if not top_focuses:
        lines.append("- none")
    for row in top_focuses[:10]:
        if not isinstance(row, dict):
            continue
        lines.append(f"- {row.get('focus', '')}: {row.get('count', 0)}")
    lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def _render_html(report: dict[str, Any]) -> str:
    json_blob = json.dumps(report, ensure_ascii=False).replace("</", "<\\/")
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Conceptual Dynamics Dashboard</title>
  <style>
    :root {{
      --bg: #f3ede1;
      --bg-2: #fffaf2;
      --card: rgba(255, 252, 246, 0.92);
      --ink: #203243;
      --muted: #607284;
      --line: #d9cdb9;
      --teal: #127475;
      --orange: #cb6d1f;
      --red: #b64949;
      --blue: #3b6ea5;
      --gold: #9f7a19;
      --shadow: 0 18px 42px rgba(49, 57, 68, 0.12);
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      color: var(--ink);
      font-family: "Aptos", "Segoe UI", sans-serif;
      background:
        radial-gradient(circle at top left, rgba(18, 116, 117, 0.08), transparent 30%),
        radial-gradient(circle at top right, rgba(203, 109, 31, 0.08), transparent 26%),
        linear-gradient(180deg, #f9f4ea 0%, #efe5d4 100%);
    }}
    .wrap {{ max-width: 1440px; margin: 0 auto; padding: 28px 24px 40px; }}
    .hero {{
      background: linear-gradient(135deg, rgba(18, 116, 117, 0.92), rgba(36, 52, 69, 0.94));
      color: #f8f6f1;
      border-radius: 28px;
      padding: 28px 32px;
      box-shadow: var(--shadow);
      position: relative;
      overflow: hidden;
    }}
    .hero::after {{
      content: "";
      position: absolute;
      inset: auto -10% -60% auto;
      width: 380px;
      height: 380px;
      background: radial-gradient(circle, rgba(255,255,255,0.16), transparent 70%);
      pointer-events: none;
    }}
    h1 {{
      margin: 0 0 10px;
      font-family: "Cambria", "Georgia", serif;
      font-size: 34px;
      letter-spacing: 0.01em;
    }}
    .hero p {{
      margin: 0;
      max-width: 860px;
      line-height: 1.45;
      color: rgba(248, 246, 241, 0.88);
    }}
    .hero-meta {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
      gap: 10px;
      margin-top: 18px;
      font-size: 13px;
    }}
    .hero-meta div {{
      background: rgba(255,255,255,0.08);
      border: 1px solid rgba(255,255,255,0.08);
      border-radius: 14px;
      padding: 10px 12px;
    }}
    .toolbar, .cards, .grid {{
      margin-top: 18px;
      display: grid;
      gap: 16px;
    }}
    .toolbar {{
      grid-template-columns: 1.5fr auto;
      align-items: center;
    }}
    .panel, .card {{
      background: var(--card);
      border: 1px solid rgba(105, 116, 129, 0.12);
      border-radius: 22px;
      box-shadow: var(--shadow);
      backdrop-filter: blur(4px);
    }}
    .toolbar .panel {{
      padding: 18px 20px;
    }}
    .controls {{
      display: flex;
      align-items: center;
      gap: 10px;
      flex-wrap: wrap;
    }}
    button {{
      border: none;
      border-radius: 999px;
      background: linear-gradient(180deg, #203243, #182634);
      color: #f9f5ef;
      padding: 9px 14px;
      cursor: pointer;
      font-size: 13px;
    }}
    button:hover {{ filter: brightness(1.08); }}
    input[type="range"] {{ width: 100%; accent-color: var(--teal); }}
    .cards {{
      grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
    }}
    .card {{
      padding: 18px 18px 16px;
      min-height: 108px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
    }}
    .label {{
      color: var(--muted);
      font-size: 12px;
      text-transform: uppercase;
      letter-spacing: 0.08em;
    }}
    .value {{
      font-size: 30px;
      line-height: 1;
      font-weight: 700;
      margin-top: 8px;
    }}
    .subtle {{
      color: var(--muted);
      font-size: 13px;
    }}
    .grid {{
      grid-template-columns: repeat(2, minmax(0, 1fr));
    }}
    .panel {{
      padding: 18px 20px 20px;
      min-width: 0;
    }}
    .panel h2 {{
      margin: 0 0 12px;
      font-size: 18px;
      font-family: "Cambria", "Georgia", serif;
    }}
    canvas {{
      width: 100%;
      height: auto;
      border-radius: 14px;
      background: rgba(255,255,255,0.58);
    }}
    .stage-strip {{
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
      margin-top: 12px;
    }}
    .stage-chip {{
      padding: 7px 10px;
      border-radius: 999px;
      background: rgba(18, 116, 117, 0.08);
      border: 1px solid rgba(18, 116, 117, 0.14);
      color: var(--ink);
      cursor: pointer;
      font-size: 12px;
    }}
    .stage-chip.active {{
      background: rgba(18, 116, 117, 0.18);
      border-color: rgba(18, 116, 117, 0.36);
      font-weight: 700;
    }}
    .info-grid {{
      display: grid;
      grid-template-columns: repeat(2, minmax(0, 1fr));
      gap: 16px;
    }}
    .metrics {{
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
    }}
    .metric {{
      padding: 7px 10px;
      border-radius: 12px;
      background: rgba(59, 110, 165, 0.08);
      border: 1px solid rgba(59, 110, 165, 0.14);
      font-size: 12px;
      line-height: 1.4;
    }}
    .metric strong {{
      display: block;
      margin-bottom: 4px;
      color: var(--muted);
      font-size: 10px;
      text-transform: uppercase;
      letter-spacing: 0.07em;
    }}
    .metric small {{
      display: block;
      margin-top: 4px;
      color: var(--muted);
      font-size: 11px;
      line-height: 1.35;
    }}
    .callout {{
      padding: 12px 14px;
      border-radius: 16px;
      background: rgba(18, 116, 117, 0.08);
      border: 1px solid rgba(18, 116, 117, 0.15);
      color: var(--ink);
      line-height: 1.5;
      margin-top: 12px;
    }}
    .object-related {{
      display: block;
      margin-top: 4px;
      color: var(--muted);
      font-size: 11px;
      line-height: 1.35;
    }}
    .dossier-stack {{
      margin-top: 12px;
      display: grid;
      gap: 12px;
    }}
    .dossier-card {{
      border-radius: 18px;
      border: 1px solid rgba(105, 116, 129, 0.14);
      background: rgba(255,255,255,0.58);
      padding: 14px 16px;
    }}
    .dossier-card.primary {{
      background: linear-gradient(180deg, rgba(18, 116, 117, 0.08), rgba(255,255,255,0.72));
      border-color: rgba(18, 116, 117, 0.2);
    }}
    .dossier-head {{
      display: flex;
      align-items: flex-start;
      justify-content: space-between;
      gap: 12px;
    }}
    .dossier-title {{
      font-size: 15px;
      font-weight: 700;
      line-height: 1.35;
    }}
    .dossier-meta {{
      color: var(--muted);
      font-size: 12px;
      line-height: 1.4;
      margin-top: 4px;
    }}
    .dossier-tags {{
      display: flex;
      flex-wrap: wrap;
      gap: 6px;
      margin-top: 10px;
    }}
    .dossier-tag {{
      padding: 5px 9px;
      border-radius: 999px;
      background: rgba(59, 110, 165, 0.08);
      border: 1px solid rgba(59, 110, 165, 0.14);
      color: var(--ink);
      font-size: 11px;
    }}
    .dossier-section {{
      margin-top: 12px;
    }}
    .dossier-section strong {{
      display: block;
      margin-bottom: 6px;
      color: var(--muted);
      font-size: 10px;
      text-transform: uppercase;
      letter-spacing: 0.08em;
    }}
    .dossier-section p {{
      margin: 0;
      font-size: 13px;
      line-height: 1.52;
    }}
    .dossier-grid {{
      display: grid;
      grid-template-columns: repeat(2, minmax(0, 1fr));
      gap: 8px;
    }}
    .dossier-cell {{
      padding: 9px 10px;
      border-radius: 12px;
      background: rgba(59, 110, 165, 0.06);
      border: 1px solid rgba(59, 110, 165, 0.1);
      min-width: 0;
    }}
    .dossier-cell strong {{
      display: block;
      margin-bottom: 4px;
      color: var(--muted);
      font-size: 10px;
      text-transform: uppercase;
      letter-spacing: 0.08em;
    }}
    .dossier-cell span {{
      display: block;
      font-size: 12px;
      line-height: 1.45;
      word-break: break-word;
    }}
    .quote-block {{
      padding: 10px 12px;
      border-left: 3px solid rgba(18, 116, 117, 0.48);
      background: rgba(18, 116, 117, 0.05);
      border-radius: 0 12px 12px 0;
      font-size: 13px;
      line-height: 1.5;
    }}
    .detail-list {{
      margin: 0;
      padding-left: 18px;
      font-size: 13px;
      line-height: 1.52;
    }}
    .detail-list li + li {{
      margin-top: 5px;
    }}
    .events, .frontier-table {{
      margin-top: 12px;
    }}
    .event {{
      padding: 10px 0;
      border-top: 1px solid rgba(105, 116, 129, 0.12);
    }}
    .event:first-child {{ border-top: none; padding-top: 0; }}
    .event-title {{
      font-weight: 700;
      font-size: 14px;
    }}
    .event-meta {{
      color: var(--muted);
      font-size: 12px;
      margin-top: 4px;
    }}
    .event-notes {{
      margin-top: 6px;
      color: var(--ink);
      font-size: 13px;
      line-height: 1.45;
    }}
    table {{
      width: 100%;
      border-collapse: collapse;
      font-size: 13px;
    }}
    th, td {{
      text-align: left;
      padding: 9px 8px;
      border-top: 1px solid rgba(105, 116, 129, 0.12);
      vertical-align: top;
    }}
    th {{
      color: var(--muted);
      font-size: 12px;
      text-transform: uppercase;
      letter-spacing: 0.08em;
      border-top: none;
    }}
    .empty {{
      color: var(--muted);
      font-size: 13px;
      padding: 4px 0 0;
    }}
    @media (max-width: 980px) {{
      .toolbar, .grid, .info-grid, .dossier-grid {{ grid-template-columns: 1fr; }}
    }}
  </style>
</head>
<body>
  <div class="wrap">
    <section class="hero">
      <h1>Conceptual Dynamics Dashboard</h1>
      <p>Replay how target consequences, invariants, bridge objects, and proof sketches accumulate across the run. This view is intentionally content-first: it emphasizes what mathematical ideas came into focus and how proof work sharpened around them.</p>
      <div class="hero-meta">
        <div><strong>KB</strong><br><span id="metaKb"></span></div>
        <div><strong>Run ID</strong><br><span id="metaRun"></span></div>
        <div><strong>Selection</strong><br><span id="metaReason"></span></div>
        <div><strong>Surface Moves</strong><br><span id="metaSurface"></span></div>
      </div>
    </section>

    <section class="toolbar">
      <div class="panel">
        <div class="controls">
          <button id="prevBtn">Prev</button>
          <button id="playBtn">Play</button>
          <button id="nextBtn">Next</button>
          <span class="subtle">Stage <strong id="stageCounter"></strong></span>
        </div>
        <div style="margin-top:12px;">
          <input id="stageRange" type="range" min="0" value="0">
        </div>
      </div>
      <div class="panel">
        <div class="label">Current Stage</div>
        <div class="value" id="stageName" style="font-size:24px;"></div>
        <div class="subtle" id="stageDesc"></div>
      </div>
    </section>

    <section class="cards">
      <div class="card"><div class="label">Key Targets</div><div class="value" id="kpiConcepts">0</div><div class="subtle" id="kpiConceptsSub"></div></div>
      <div class="card"><div class="label">Invariants</div><div class="value" id="kpiTargets">0</div><div class="subtle" id="kpiTargetsSub"></div></div>
      <div class="card"><div class="label">Bridge Objects</div><div class="value" id="kpiHypotheses">0</div><div class="subtle" id="kpiHypothesesSub"></div></div>
      <div class="card"><div class="label">Proof Sketches</div><div class="value" id="kpiOpen">0</div><div class="subtle" id="kpiOpenSub"></div></div>
      <div class="card"><div class="label">Supported Hypotheses</div><div class="value" id="kpiReasoning">0</div><div class="subtle" id="kpiReasoningSub"></div></div>
      <div class="card"><div class="label">Proof Families</div><div class="value" id="kpiProof">0</div><div class="subtle" id="kpiProofSub"></div></div>
    </section>

    <section class="grid">
      <div class="panel">
        <h2>Concept Threads</h2>
        <canvas id="growthChart" width="640" height="260"></canvas>
      </div>
      <div class="panel">
        <h2>Proof Construction</h2>
        <canvas id="lifecycleChart" width="640" height="260"></canvas>
      </div>
      <div class="panel">
        <h2>Active Proof Families</h2>
        <canvas id="reasoningChart" width="640" height="260"></canvas>
      </div>
      <div class="panel">
        <h2>Concept Roles</h2>
        <canvas id="natureChart" width="640" height="260"></canvas>
      </div>
    </section>

    <section class="panel">
      <h2>Stage Trajectory</h2>
      <div id="stageStrip" class="stage-strip"></div>
    </section>

    <section class="grid">
      <div class="panel">
        <h2>Stage Content</h2>
        <div class="info-grid">
          <div>
            <div class="label">Concepts Introduced Here</div>
            <div id="metricsBox" class="metrics" style="margin-top:10px;"></div>
          </div>
          <div>
            <div class="label">Proof Work Here</div>
            <div id="signalsBox" class="metrics" style="margin-top:10px;"></div>
          </div>
        </div>
        <div class="label" style="margin-top:16px;">Stage Narrative</div>
        <div class="events" id="eventsBox"></div>
        <div class="label" style="margin-top:16px;">Primary Mathematical Dossier</div>
        <div id="dossierBox" class="dossier-stack"></div>
      </div>
      <div class="panel">
        <h2>Objects In Play</h2>
        <div id="frontierBody" class="dossier-stack"></div>
      </div>
    </section>
  </div>

  <script>
    const report = {json_blob};
    const fallbackState = (report.summary && report.summary.current) || {{}};
    const timeline = Array.isArray(report.timeline) && report.timeline.length
      ? report.timeline
      : [{{ stage: "summary", description: "No stage-aligned conceptual updates were observed.", state: fallbackState, metrics: {{}}, surface: {{ moment_count: 0, cumulative_moment_count: 0, qualitative_events: [] }}, source: {{ has_artifact_contribution: false, surface_moment_count: 0, surface_agents: [] }}, delta: {{}} }}];

    const meta = report.metadata || {{}};
    document.getElementById("metaKb").textContent = meta.kb_ref || meta.kb || "";
    document.getElementById("metaRun").textContent = meta.selected_run_id || "(none)";
    document.getElementById("metaReason").textContent = meta.run_selection_reason || "";
    document.getElementById("metaSurface").textContent = String((report.summary || {{}}).surface_moment_count || 0);

    const range = document.getElementById("stageRange");
    const playBtn = document.getElementById("playBtn");
    const prevBtn = document.getElementById("prevBtn");
    const nextBtn = document.getElementById("nextBtn");
    range.max = String(Math.max(0, timeline.length - 1));

    function series(selector) {{
      return timeline.map(item => {{
        const value = selector(item);
        return Number.isFinite(value) ? value : 0;
      }});
    }}

    function topPairs(obj, limit = 8) {{
      return Object.entries(obj || {{}})
        .sort((a, b) => (Number(b[1]) - Number(a[1])) || String(a[0]).localeCompare(String(b[0])))
        .slice(0, limit);
    }}

    function metricString(value) {{
      if (value === null || value === undefined || value === "") return "";
      if (typeof value === "number") return Number.isInteger(value) ? String(value) : value.toFixed(3);
      if (Array.isArray(value)) return value.slice(0, 4).join(", ");
      if (typeof value === "object") return `${{Object.keys(value).length}} keys`;
      return String(value);
    }}

    function escapeHtml(value) {{
      return String(value ?? "")
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/\"/g, "&quot;")
        .replace(/'/g, "&#39;");
    }}

    function cleanText(value) {{
      return String(value ?? "").trim();
    }}

    function firstNonEmpty(...values) {{
      for (const value of values) {{
        const text = cleanText(value);
        if (text) return text;
      }}
      return "";
    }}

    function sectionText(title, value, className = "") {{
      const text = cleanText(value);
      if (!text) return "";
      const extra = className ? ` ${{className}}` : "";
      return `<div class="dossier-section${{extra}}"><strong>${{escapeHtml(title)}}</strong><p>${{escapeHtml(text)}}</p></div>`;
    }}

    function sectionQuote(title, value) {{
      const text = cleanText(value);
      if (!text) return "";
      return `<div class="dossier-section"><strong>${{escapeHtml(title)}}</strong><div class="quote-block">${{escapeHtml(text)}}</div></div>`;
    }}

    function sectionList(title, items, limit = 4) {{
      const rows = (Array.isArray(items) ? items : []).map(cleanText).filter(Boolean).slice(0, limit);
      if (!rows.length) return "";
      return `<div class="dossier-section"><strong>${{escapeHtml(title)}}</strong><ul class="detail-list">${{rows.map((row) => `<li>${{escapeHtml(row)}}</li>`).join("")}}</ul></div>`;
    }}

    function deltaCells(delta) {{
      const row = delta && typeof delta === "object" ? delta : {{}};
      const labels = [
        ["source_problem_family", "Source family"],
        ["target_problem_family", "Target family"],
        ["source_model", "Source model"],
        ["target_model", "Target model"],
        ["source_claim_focus", "Source focus"],
        ["target_claim_focus", "Target focus"],
        ["model_shift", "Model shift"],
        ["threshold_shift", "Threshold shift"],
        ["consequence_shift", "Consequence shift"],
        ["typed_object_expectation", "Expected object"],
        ["missing_witness_or_transport", "Missing lemma"],
      ];
      return labels
        .map(([key, title]) => {{
          const text = cleanText(row[key]);
          return text ? `<div class="dossier-cell"><strong>${{escapeHtml(title)}}</strong><span>${{escapeHtml(text)}}</span></div>` : "";
        }})
        .filter(Boolean)
        .join("");
    }}

    function dossierCardHTML(row, options = {{}}) {{
      if (!row || typeof row !== "object") return "";
      const content = row.content && typeof row.content === "object" ? row.content : {{}};
      const primary = Boolean(options.primary);
      const compact = Boolean(options.compact);
      const meta = [
        cleanText(row.object_type),
        cleanText(row.nature),
        cleanText(row.status),
        row.score !== null && row.score !== undefined ? `score=${{Number(row.score).toFixed(3)}}` : "",
        cleanText(row.proof_strategy_family),
      ].filter(Boolean);
      const related = (Array.isArray(row.related_concepts) ? row.related_concepts : []).map(cleanText).filter(Boolean).slice(0, compact ? 3 : 5);
      const title = cleanText(row.label) || cleanText(row.id) || "Unnamed object";
      const subtitle = row.id && row.id !== row.label ? cleanText(row.id) : "";
      const route = firstNonEmpty(content.route_synopsis, content.conditional_claim, content.bridge_definition);
      const delta = deltaCells(content.statement_delta || {{}});
      const assumptions = compact ? (content.assumptions || []).slice(0, 2) : (content.assumptions || []);
      const obligations = compact ? (content.obligations || []).slice(0, 3) : (content.obligations || []);
      const lemmas = compact ? (content.lemmas || []).slice(0, 3) : (content.lemmas || []);
      const outline = compact ? (content.proof_outline || []).slice(0, 2) : (content.proof_outline || []);
      return `
        <article class="dossier-card${{primary ? " primary" : ""}}">
          <div class="dossier-head">
            <div>
              <div class="dossier-title">${{escapeHtml(title)}}</div>
              <div class="dossier-meta">${{escapeHtml(meta.join(" | "))}}</div>
              ${{subtitle ? `<div class="object-related">${{escapeHtml(subtitle)}}</div>` : ""}}
            </div>
          </div>
          ${{related.length ? `<div class="dossier-tags">${{related.map((item) => `<span class="dossier-tag">${{escapeHtml(item)}}</span>`).join("")}}</div>` : ""}}
          ${{sectionText("Route synopsis", route)}}
          ${{sectionQuote("Source theorem", content.source_excerpt)}}
          ${{sectionQuote("Target theorem", content.target_excerpt)}}
          ${{delta ? `<div class="dossier-section"><strong>Mathematical delta</strong><div class="dossier-grid">${{delta}}</div></div>` : ""}}
          ${{(cleanText(content.carrier_kind) || cleanText(content.typing_status) || cleanText(content.bridge_definition) || cleanText(content.conditional_claim))
            ? `<div class="dossier-section"><strong>Candidate object</strong><div class="dossier-grid">${{
                cleanText(content.carrier_kind) ? `<div class="dossier-cell"><strong>Carrier</strong><span>${{escapeHtml(content.carrier_kind)}}</span></div>` : ""
              }}${{
                cleanText(content.typing_status) ? `<div class="dossier-cell"><strong>Typing status</strong><span>${{escapeHtml(content.typing_status)}}</span></div>` : ""
              }}</div>${{
                sectionText("Definition", content.bridge_definition)
              }}${{
                sectionText("Conditional claim", content.conditional_claim)
              }}</div>`
            : ""}}
          ${{sectionList("Admissibility and assumptions", assumptions, compact ? 2 : 4)}}
          ${{sectionList("Proof obligations", obligations, compact ? 3 : 5)}}
          ${{sectionList("Lemma chain", lemmas, compact ? 3 : 5)}}
          ${{sectionList("Proof outline", outline, compact ? 2 : 4)}}
          ${{sectionText("Failure diagnosis", content.failure_diagnosis)}}
          ${{sectionText("Counterfactual probe", content.counterfactual)}}
        </article>
      `;
    }}

    function drawLineChart(canvasId, lines, cursor) {{
      const canvas = document.getElementById(canvasId);
      const ctx = canvas.getContext("2d");
      const w = canvas.width;
      const h = canvas.height;
      const pad = 34;
      ctx.clearRect(0, 0, w, h);
      let ymin = Infinity;
      let ymax = -Infinity;
      for (const line of lines) {{
        for (const v of line.values) {{
          ymin = Math.min(ymin, v);
          ymax = Math.max(ymax, v);
        }}
      }}
      if (!Number.isFinite(ymin) || !Number.isFinite(ymax)) {{ ymin = 0; ymax = 1; }}
      if (Math.abs(ymax - ymin) < 1e-9) ymax = ymin + 1;
      const span = Math.max(1, timeline.length - 1);
      const px = (i) => pad + (w - 2 * pad) * (i / span);
      const py = (v) => h - pad - (h - 2 * pad) * ((v - ymin) / (ymax - ymin));

      ctx.strokeStyle = "#d7d0c4";
      ctx.lineWidth = 1;
      ctx.beginPath(); ctx.moveTo(pad, h - pad); ctx.lineTo(w - pad, h - pad); ctx.stroke();
      ctx.beginPath(); ctx.moveTo(pad, pad); ctx.lineTo(pad, h - pad); ctx.stroke();

      for (const line of lines) {{
        ctx.strokeStyle = line.color;
        ctx.lineWidth = 1.8;
        ctx.beginPath();
        line.values.forEach((v, i) => {{
          const x = px(i);
          const y = py(v);
          if (i === 0) ctx.moveTo(x, y); else ctx.lineTo(x, y);
        }});
        ctx.stroke();
      }}

      const cx = px(cursor);
      ctx.strokeStyle = "#8f9aaa";
      ctx.lineWidth = 1;
      ctx.beginPath(); ctx.moveTo(cx, pad); ctx.lineTo(cx, h - pad); ctx.stroke();

      ctx.font = "11px Aptos, Segoe UI, sans-serif";
      let lx = pad + 6;
      for (const line of lines) {{
        ctx.fillStyle = line.color;
        ctx.fillRect(lx, 8, 10, 10);
        ctx.fillStyle = "#294153";
        ctx.fillText(line.name, lx + 14, 17);
        lx += 18 + ctx.measureText(line.name).width + 12;
      }}
    }}

    function drawBarChart(canvasId, pairs, color) {{
      const canvas = document.getElementById(canvasId);
      const ctx = canvas.getContext("2d");
      const w = canvas.width;
      const h = canvas.height;
      const pad = 34;
      ctx.clearRect(0, 0, w, h);
      const data = pairs.length ? pairs : [["none", 0]];
      const maxV = Math.max(1, ...data.map(item => Number(item[1]) || 0));
      const barW = (w - 2 * pad) / Math.max(1, data.length);
      ctx.strokeStyle = "#d7d0c4";
      ctx.beginPath(); ctx.moveTo(pad, h - pad); ctx.lineTo(w - pad, h - pad); ctx.stroke();
      ctx.font = "10px Aptos, Segoe UI, sans-serif";
      data.forEach((item, i) => {{
        const value = Number(item[1]) || 0;
        const x = pad + i * barW + 4;
        const bh = (h - 2 * pad) * (value / maxV);
        const y = h - pad - bh;
        ctx.fillStyle = color;
        ctx.fillRect(x, y, Math.max(10, barW - 8), bh);
        ctx.fillStyle = "#33485f";
        ctx.save();
        ctx.translate(x + 2, h - pad + 10);
        ctx.rotate(-0.4);
        ctx.fillText(String(item[0]), 0, 0);
        ctx.restore();
      }});
    }}

    function renderStageStrip(idx) {{
      const box = document.getElementById("stageStrip");
      box.innerHTML = "";
      timeline.forEach((item, i) => {{
        const button = document.createElement("button");
        button.className = "stage-chip" + (i === idx ? " active" : "");
        button.textContent = item.stage || `stage-${{i}}`;
        button.addEventListener("click", () => {{
          range.value = String(i);
          renderAt(i);
        }});
        box.appendChild(button);
      }});
    }}

    function joinLabels(items, limit = 3) {{
      return (items || [])
        .slice(0, limit)
        .map((item) => typeof item === "string" ? item : (item.label || item.id || ""))
        .filter(Boolean)
        .join(", ");
    }}

    function renderHighlightChips(boxId, sections) {{
      const box = document.getElementById(boxId);
      box.innerHTML = "";
      let count = 0;
      (sections || []).forEach((section) => {{
        const title = section && section.title ? String(section.title) : "item";
        const items = Array.isArray(section && section.items) ? section.items : [];
        items.slice(0, section.limit || 4).forEach((item) => {{
          const label = typeof item === "string" ? item : (item.label || item.id || "");
          if (!label) return;
          const meta = [];
          if (item.nature) meta.push(String(item.nature));
          if (item.status) meta.push(String(item.status));
          if (item.count !== undefined) meta.push(`count=${{item.count}}`);
          if (item.score !== undefined && item.score !== null) meta.push(`score=${{Number(item.score).toFixed(3)}}`);
          const chip = document.createElement("div");
          chip.className = "metric";
          chip.innerHTML = `<strong>${{escapeHtml(title)}}</strong>${{escapeHtml(label)}}${{meta.length ? `<small>${{escapeHtml(meta.join(" | "))}}</small>` : ""}}`;
          box.appendChild(chip);
          count += 1;
        }});
      }});
      if (!count) {{
        const empty = document.createElement("div");
        empty.className = "empty";
        empty.textContent = "No content highlights were introduced at this stage.";
        box.appendChild(empty);
      }}
    }}

    function renderStageNarrative(item) {{
      const box = document.getElementById("eventsBox");
      box.innerHTML = "";
      const state = item.state || {{}};
      const highlights = state.highlights || {{}};
      const callout = document.createElement("div");
      callout.className = "callout";
      const leadingTargets = joinLabels(highlights.leading_targets, 3) || "none";
      const leadingInvariants = joinLabels(highlights.leading_invariants, 3) || "none";
      const leadingBridgeObjects = joinLabels(highlights.leading_bridge_objects, 3) || "none";
      const leadingFamilies = joinLabels(highlights.stage_proof_families, 3) || joinLabels(topPairs(state.proof_strategy_family_counts || {{}}, 3).map(([label, count]) => ({{ label: `${{label}} (${{count}})` }})), 3) || "none";
      callout.innerHTML = `
        <strong>${{escapeHtml((highlights.headline || item.description || "No stage narrative.").trim())}}</strong>
        <div class="subtle" style="margin-top:8px;">Leading targets: ${{escapeHtml(leadingTargets)}}</div>
        <div class="subtle">Leading invariants: ${{escapeHtml(leadingInvariants)}}</div>
        <div class="subtle">Leading bridge objects: ${{escapeHtml(leadingBridgeObjects)}}</div>
        <div class="subtle">Proof families in view: ${{escapeHtml(leadingFamilies)}}</div>
      `;
      box.appendChild(callout);

      const events = ((item.surface || {{}}).qualitative_events || []).slice(0, 4);
      if (!events.length) return;
      events.forEach((event) => {{
        const row = document.createElement("div");
        row.className = "event";
        const notes = Array.isArray(event.details) ? event.details.filter(Boolean).join(" | ") : "";
        row.innerHTML = `
          <div class="event-title">${{escapeHtml(event.title || "(untitled move)")}}</div>
          <div class="event-meta">${{escapeHtml([event.agent || "", event.kind || "", event.focus || ""].filter(Boolean).join(" | "))}}</div>
          <div class="event-notes">${{escapeHtml(event.significance || "")}}${{notes ? " | " + escapeHtml(notes) : ""}}</div>
        `;
        box.appendChild(row);
      }});
    }}

    function renderStageDossier(item) {{
      const box = document.getElementById("dossierBox");
      box.innerHTML = "";
      const state = item.state || {{}};
      const highlights = state.highlights || {{}};
      const primary = highlights.primary_dossier && typeof highlights.primary_dossier === "object"
        ? highlights.primary_dossier
        : null;
      const supporting = Array.isArray(highlights.supporting_dossiers) ? highlights.supporting_dossiers : [];
      if (!primary) {{
        const empty = document.createElement("div");
        empty.className = "empty";
        empty.textContent = "No theorem-level dossier has been assembled for this stage yet.";
        box.appendChild(empty);
        return;
      }}
      box.insertAdjacentHTML("beforeend", dossierCardHTML(primary, {{ primary: true }}));
      supporting.slice(0, 2).forEach((row) => {{
        const wrapper = document.createElement("div");
        wrapper.innerHTML = dossierCardHTML(row, {{ compact: true }});
        if (wrapper.firstElementChild) box.appendChild(wrapper.firstElementChild);
      }});
    }}

    function dedupeObjects(rows, limit = 12) {{
      const out = [];
      const seen = new Set();
      (rows || []).forEach((row) => {{
        if (!row || typeof row !== "object") return;
        const key = row.id || row.label;
        if (!key || seen.has(key)) return;
        seen.add(key);
        out.push(row);
      }});
      return out.slice(0, limit);
    }}

    function renderObjectsInPlay(rows) {{
      const body = document.getElementById("frontierBody");
      body.innerHTML = "";
      if (!rows.length) {{
        const empty = document.createElement("div");
        empty.className = "empty";
        empty.textContent = "No proof-relevant objects are currently foregrounded.";
        body.appendChild(empty);
        return;
      }}
      rows.forEach((row) => {{
        const wrapper = document.createElement("div");
        wrapper.innerHTML = dossierCardHTML(row, {{ compact: true }});
        if (wrapper.firstElementChild) body.appendChild(wrapper.firstElementChild);
      }});
    }}

    function renderAt(index) {{
      const idx = Math.max(0, Math.min(index, timeline.length - 1));
      const item = timeline[idx] || {{}};
      const state = item.state || {{}};
      const highlights = state.highlights || {{}};
      const conceptNatures = state.concept_nature_counts || {{}};
      const objectTypes = state.object_type_counts || {{}};
      const hypothesisStates = state.hypothesis_state_counts || {{}};
      document.getElementById("stageCounter").textContent = `${{idx + 1}} / ${{timeline.length}}`;
      document.getElementById("stageName").textContent = item.stage || "";
      document.getElementById("stageDesc").textContent = item.description || "";
      document.getElementById("kpiConcepts").textContent = String(state.target_concept_count || 0);
      document.getElementById("kpiConceptsSub").textContent = joinLabels(highlights.leading_targets, 2) || "no dominant targets yet";
      document.getElementById("kpiTargets").textContent = String(conceptNatures["invariant"] || 0);
      document.getElementById("kpiTargetsSub").textContent = joinLabels(highlights.leading_invariants, 2) || "no explicit invariant yet";
      document.getElementById("kpiHypotheses").textContent = String((conceptNatures["bridge-object"] || 0) + (conceptNatures["abstraction-family"] || 0));
      document.getElementById("kpiHypothesesSub").textContent = joinLabels(highlights.leading_bridge_objects, 2) || "no bridge object yet";
      document.getElementById("kpiOpen").textContent = String(objectTypes.proof_sketch || 0);
      document.getElementById("kpiOpenSub").textContent = joinLabels(highlights.leading_proof_sketches, 1) || "no proof sketch yet";
      document.getElementById("kpiReasoning").textContent = String(hypothesisStates.supported || 0);
      document.getElementById("kpiReasoningSub").textContent = joinLabels(highlights.supported_hypotheses, 2) || "no supported hypothesis yet";
      document.getElementById("kpiProof").textContent = String(state.proof_strategy_diversity || 0);
      document.getElementById("kpiProofSub").textContent =
        joinLabels((highlights.stage_proof_families || []).map((row) => ({{ label: row.label }})), 2)
        || joinLabels(topPairs(state.proof_strategy_family_counts || {{}}, 2).map(([label, count]) => ({{ label: `${{label}} (${{count}})` }})), 2)
        || "no proof family yet";

      drawLineChart("growthChart", [
        {{ name: "targets", color: "#cb6d1f", values: series(t => ((((t.state || {{}}).concept_nature_counts || {{}})["target-concept"]) || 0)) }},
        {{ name: "invariants", color: "#127475", values: series(t => ((((t.state || {{}}).concept_nature_counts || {{}})["invariant"]) || 0)) }},
        {{ name: "bridge objects", color: "#3b6ea5", values: series(t => (((((t.state || {{}}).concept_nature_counts || {{}})["bridge-object"]) || 0) + ((((t.state || {{}}).concept_nature_counts || {{}})["abstraction-family"]) || 0))) }},
        {{ name: "formalization", color: "#9f7a19", values: series(t => ((((t.state || {{}}).concept_nature_counts || {{}})["formalization-commitment"]) || 0)) }},
      ], idx);
      drawLineChart("lifecycleChart", [
        {{ name: "bridges", color: "#127475", values: series(t => ((((t.state || {{}}).object_type_counts || {{}}).bridge_program) || 0)) }},
        {{ name: "conjectures", color: "#cb6d1f", values: series(t => ((((t.state || {{}}).object_type_counts || {{}}).abstraction_conjecture) || 0)) }},
        {{ name: "sketches", color: "#3b6ea5", values: series(t => ((((t.state || {{}}).object_type_counts || {{}}).proof_sketch) || 0)) }},
        {{ name: "supported hyp.", color: "#5a9b4b", values: series(t => ((((t.state || {{}}).hypothesis_state_counts || {{}}).supported) || 0)) }},
      ], idx);
      drawBarChart("reasoningChart", topPairs(state.proof_strategy_family_counts || {{}}, 8), "#cb6d1f");
      drawBarChart("natureChart", topPairs(state.concept_role_counts || {{}}, 8), "#127475");

      renderHighlightChips("metricsBox", [
        {{ title: "new target", items: highlights.introduced_targets || [], limit: 4 }},
        {{ title: "new invariant", items: highlights.introduced_invariants || [], limit: 4 }},
        {{ title: "new bridge object", items: highlights.introduced_bridge_objects || [], limit: 4 }},
        {{ title: "new obligation", items: highlights.introduced_formalizations || [], limit: 4 }},
      ]);
      renderHighlightChips("signalsBox", [
        {{ title: "proof family", items: highlights.stage_proof_families || [], limit: 4 }},
        {{ title: "proof sketch", items: highlights.stage_proof_sketches || [], limit: 4 }},
        {{ title: "bridge", items: highlights.stage_bridges || [], limit: 4 }},
        {{ title: "conjecture", items: highlights.stage_conjectures || [], limit: 4 }},
      ]);
      renderStageNarrative(item);
      renderStageDossier(item);
      renderObjectsInPlay(dedupeObjects([
        ...(highlights.supporting_dossiers || []),
        ...(highlights.stage_proof_sketches || []),
        ...(highlights.stage_bridges || []),
        ...(highlights.stage_conjectures || []),
        ...(highlights.leading_proof_sketches || []).slice(0, 3),
        ...(highlights.leading_bridges || []).slice(0, 3),
        ...(highlights.leading_conjectures || []).slice(0, 3),
        ...(highlights.supported_hypotheses || []).slice(0, 3),
        ...(highlights.frontier_hypotheses || []).slice(0, 3),
      ], 12));
      renderStageStrip(idx);
    }}

    let timer = null;
    function stopPlayback() {{
      if (timer) clearInterval(timer);
      timer = null;
      playBtn.textContent = "Play";
    }}
    function togglePlayback() {{
      if (timer) {{
        stopPlayback();
        return;
      }}
      playBtn.textContent = "Pause";
      timer = setInterval(() => {{
        const next = Math.min(timeline.length - 1, Number(range.value) + 1);
        range.value = String(next);
        renderAt(next);
        if (next >= timeline.length - 1) stopPlayback();
      }}, 650);
    }}

    range.addEventListener("input", () => renderAt(Number(range.value)));
    playBtn.addEventListener("click", togglePlayback);
    prevBtn.addEventListener("click", () => {{
      const next = Math.max(0, Number(range.value) - 1);
      range.value = String(next);
      renderAt(next);
    }});
    nextBtn.addEventListener("click", () => {{
      const next = Math.min(timeline.length - 1, Number(range.value) + 1);
      range.value = String(next);
      renderAt(next);
    }});

    renderAt(Number(range.value));
  </script>
</body>
</html>
"""


def main() -> int:
    logger = ReasoningLogger("kb-conceptual-dynamics")
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--artifacts-dir", required=True, help="Path to artifacts/<kb-ref> directory.")
    ap.add_argument("--kb", default="", help="Optional KB path for report context.")
    ap.add_argument("--kb-ref", default="", help="Optional KB reference filter.")
    ap.add_argument("--reasoning-surface-root", default="artifacts/reasoning-surfaces")
    ap.add_argument("--run-id", default="", help="Optional exact run ID.")
    ap.add_argument("--output-json", default="")
    ap.add_argument("--output-md", default="")
    ap.add_argument("--output-html", default="")
    args = ap.parse_args()

    repo_root = Path(__file__).resolve().parents[4]
    artifacts_dir = Path(args.artifacts_dir)
    if not artifacts_dir.is_absolute():
        artifacts_dir = (repo_root / artifacts_dir).resolve()
    surface_root = Path(args.reasoning_surface_root)
    if not surface_root.is_absolute():
        surface_root = (repo_root / surface_root).resolve()
    kb_ref = normalize_kb_ref(args.kb_ref.strip()) or kb_ref_from_artifacts_dir(artifacts_dir)

    output_json = Path(args.output_json) if args.output_json else artifacts_dir / "conceptual-dynamics.json"
    output_md = Path(args.output_md) if args.output_md else artifacts_dir / "conceptual-dynamics.md"
    output_html = Path(args.output_html) if args.output_html else artifacts_dir / "conceptual-dynamics.html"

    logger.step(
        "Parsed conceptual-dynamics arguments",
        "\n".join(
            [
                f"artifacts_dir={artifacts_dir}",
                f"kb={args.kb}",
                f"kb_ref={kb_ref}",
                f"reasoning_surface_root={surface_root}",
                f"run_id={args.run_id}",
                f"output_json={output_json}",
                f"output_md={output_md}",
                f"output_html={output_html}",
            ]
        ),
        surface_focus="conceptual-dynamics",
        surface_stage="conceptual-dynamics",
    )

    if not artifacts_dir.exists():
        log_path = logger.finalize("error", summary=f"Artifacts directory not found: {artifacts_dir}")
        print(f"[LOG] {log_path}", file=sys.stderr)
        raise SystemExit(f"[ERROR] Artifacts directory not found: {artifacts_dir}")

    excluded = {str(logger.surface_json_path.resolve())}
    candidate_surfaces = _load_surfaces(
        surface_root,
        repo_root=repo_root,
        artifacts_dir=artifacts_dir,
        kb_filter=args.kb.strip(),
        kb_ref_filter=kb_ref,
        run_id=None,
        exclude_surface_paths=excluded,
    )
    if args.run_id:
        selected_run_id = args.run_id.strip()
        selection_reason = "explicit-run-id"
    else:
        selected_run_id, selection_reason = _default_run_id_for_conceptual_view(candidate_surfaces)
    surfaces = (
        _load_surfaces(
            surface_root,
            repo_root=repo_root,
            artifacts_dir=artifacts_dir,
            kb_filter=args.kb.strip(),
            kb_ref_filter=kb_ref,
            run_id=selected_run_id or None,
            exclude_surface_paths=excluded,
        )
        if selected_run_id
        else candidate_surfaces
    )

    report = _build_conceptual_dynamics(
        repo_root=repo_root,
        artifacts_dir=artifacts_dir,
        surfaces=surfaces,
        kb=args.kb.strip(),
        kb_ref=kb_ref,
        selected_run_id=selected_run_id,
        selection_reason=selection_reason,
    )

    logger.step(
        "Computed conceptual dynamics",
        "\n".join(
            [
                f"stages={report.get('summary', {}).get('stage_count', 0)}",
                f"surfaces={report.get('summary', {}).get('surface_count', 0)}",
                f"concepts={report.get('summary', {}).get('current', {}).get('concept_count', 0)}",
                f"hypotheses={report.get('summary', {}).get('current', {}).get('hypothesis_count', 0)}",
            ]
        ),
        surface_focus="conceptual-dynamics",
        surface_stage="conceptual-dynamics",
        surface_metrics={
            "stage_count": report.get("summary", {}).get("stage_count", 0),
            "surface_count": report.get("summary", {}).get("surface_count", 0),
            "concept_count": report.get("summary", {}).get("current", {}).get("concept_count", 0),
            "hypothesis_count": report.get("summary", {}).get("current", {}).get("hypothesis_count", 0),
        },
        surface_taxonomy={"reasoning_types": ["conceptual-monitoring"]},
    )

    output_json.parent.mkdir(parents=True, exist_ok=True)
    output_md.parent.mkdir(parents=True, exist_ok=True)
    output_html.parent.mkdir(parents=True, exist_ok=True)
    output_json.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    output_md.write_text(_to_markdown(report), encoding="utf-8")
    output_html.write_text(_render_html(report), encoding="utf-8")

    print(f"[OK] Wrote conceptual dynamics JSON: {output_json}")
    print(f"[OK] Wrote conceptual dynamics Markdown: {output_md}")
    print(f"[OK] Wrote conceptual dynamics HTML: {output_html}")

    logger.add_output("conceptual_dynamics_json", output_json)
    logger.add_output("conceptual_dynamics_md", output_md)
    logger.add_output("conceptual_dynamics_html", output_html)
    log_path = logger.finalize(
        "success",
        summary=(
            f"Generated conceptual dynamics for {report.get('summary', {}).get('stage_count', 0)} stages "
            f"and {report.get('summary', {}).get('surface_moment_count', 0)} surfaced moves."
        ),
    )
    print(f"[LOG] {log_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
