# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
# 
# SPDX-License-Identifier: MIT

"""Articulate epistemological hardness for a KB + hard problem."""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path
from typing import Any

import yaml

_COMMON_DIR = Path(__file__).resolve().parents[3] / "common"
if str(_COMMON_DIR) not in sys.path:
    sys.path.insert(0, str(_COMMON_DIR))

from reasoning_log import ReasoningLogger
from contracts import validate_connection_analysis
from contracts import validate_entrypoints
from contracts import validate_pathways
from contracts import validate_phyp

BLOCK_RE = re.compile(r"```yaml\n(.*?)\n```", re.DOTALL)
ID_RE = re.compile(r"`(st\.[A-Za-z0-9._-]+)`")
TOKEN_RE = re.compile(r"[A-Za-z0-9_]+")
LATEX_COMMAND_RE = re.compile(r"\\([A-Za-z]+)")
LATEX_SYMBOL_RE = re.compile(r"(?<![A-Za-z])([A-Za-z](?:_[A-Za-z0-9]+)?)")

STOPWORDS = {
    "a",
    "an",
    "and",
    "as",
    "at",
    "be",
    "by",
    "for",
    "from",
    "if",
    "in",
    "into",
    "is",
    "it",
    "of",
    "on",
    "or",
    "that",
    "the",
    "to",
    "with",
}

RESTRICTED_MODEL_METHOD_TAGS = {
    "circuit-lower-bounds",
    "proof-complexity",
    "communication",
    "algebraic",
}
GRAND_TARGET_SYMBOLS = {
    "pclass",
    "np",
    "conp",
    "ph",
    "nexp",
    "exp",
    "ppoly",
}


def _load_kb(kb_path: Path) -> dict[str, dict[str, Any]]:
    """
    Relevance: Operates within the epistemic hardness analysis layer.
    Concept: Loading and structuring external artifacts for deterministic processing.
    Contribution: Provides clean, typed inputs so downstream reasoning steps remain auditable.
    """

    text = kb_path.read_text(encoding="utf-8")
    out: dict[str, dict[str, Any]] = {}
    for m in BLOCK_RE.finditer(text):
        try:
            d = yaml.safe_load(m.group(1))
        except yaml.YAMLError:
            continue
        if not isinstance(d, dict):
            continue
        sid = str(d.get("id", "")).strip()
        kind = str(d.get("kind", "")).strip().lower()
        if sid and kind:
            out[sid] = d
    return out


def _phase_map(concept_path: Path) -> dict[str, str]:
    """
    Relevance: Operates within the epistemic hardness analysis layer.
    Concept: Typed classification used to guide scoring and prioritization.
    Contribution: Contributes a deterministic transformation that supports end-to-end reasoning reproducibility.
    """

    current = "Unspecified"
    out: dict[str, str] = {}
    for line in concept_path.read_text(encoding="utf-8").splitlines():
        if line.startswith("## "):
            current = line.replace("## ", "", 1).strip()
            continue
        for sid in ID_RE.findall(line):
            out[sid] = current
    return out


def _kind_count(statements: dict[str, dict[str, Any]]) -> Counter:
    """
    Relevance: Operates within the epistemic hardness analysis layer.
    Concept: Typed classification used to guide scoring and prioritization.
    Contribution: Contributes a deterministic transformation that supports end-to-end reasoning reproducibility.
    """

    c = Counter()
    for d in statements.values():
        c[str(d.get("kind", "unknown")).strip().lower()] += 1
    return c


def _dependency_edges(statements: dict[str, dict[str, Any]]) -> tuple[int, int]:
    """
    Relevance: Operates within the epistemic hardness analysis layer.
    Concept: Internal helper implementing one deterministic step of this stage.
    Contribution: Contributes a deterministic transformation that supports end-to-end reasoning reproducibility.
    """

    edge_count = 0
    missing = 0
    ids = set(statements.keys())
    for d in statements.values():
        deps = d.get("depends_on", [])
        if not isinstance(deps, list):
            deps = []
        for dep in deps:
            dep_s = str(dep).strip()
            if not dep_s:
                continue
            if dep_s in ids:
                edge_count += 1
            else:
                missing += 1
    return edge_count, missing


def _normalize_list(value: Any) -> list[str]:
    """
    Relevance: Operates within the epistemic hardness analysis layer.
    Concept: Normalization of input structures into stable internal forms.
    Contribution: Contributes a deterministic transformation that supports end-to-end reasoning reproducibility.
    """

    if isinstance(value, list):
        return [str(x).strip() for x in value if str(x).strip()]
    text = str(value).strip()
    if not text:
        return []
    if "," in text:
        return [chunk.strip() for chunk in text.split(",") if chunk.strip()]
    return [text]


def _statement_id_from_node(node_id: str, node_lookup: dict[str, dict[str, Any]]) -> str:
    """
    Relevance: Operates within the epistemic hardness analysis layer.
    Concept: Internal helper implementing one deterministic step of this stage.
    Contribution: Contributes a deterministic transformation that supports end-to-end reasoning reproducibility.
    """

    node = str(node_id).strip()
    if node.startswith("statement:"):
        return node.split("statement:", 1)[1].strip()
    if node.startswith("barrier:"):
        payload = node_lookup.get(node, {})
        sid = str(payload.get("statement_id", "")).strip()
        if sid:
            return sid
        return node.split("barrier:", 1)[1].strip()
    return ""


def _tokenize_structural(value: str) -> set[str]:
    """
    Relevance: Operates within the epistemic hardness analysis layer.
    Concept: Extraction of structured signals from raw text or artifact payloads.
    Contribution: Produces low-noise tags used by structural classification steps.
    """

    out: set[str] = set()
    for token in TOKEN_RE.findall(str(value).lower()):
        tok = token.strip("_")
        if len(tok) <= 1 or tok in STOPWORDS:
            continue
        out.add(tok)
    return out


def _latex_symbol_tokens(latex: str) -> set[str]:
    """
    Relevance: Operates within the epistemic hardness analysis layer.
    Concept: Extraction of structured signals from raw text or artifact payloads.
    Contribution: Captures symbolic complexity-class references without relying on free-text lexical heuristics.
    """

    out: set[str] = set()
    for cmd in LATEX_COMMAND_RE.findall(str(latex)):
        c = cmd.strip().lower()
        if c and c not in STOPWORDS:
            out.add(c)
    for sym in LATEX_SYMBOL_RE.findall(str(latex)):
        s = sym.strip().lower()
        if s and s not in STOPWORDS:
            out.add(s)
    return out


def _analysis_structural_maps(analysis: dict[str, Any]) -> tuple[dict[str, set[str]], dict[str, set[str]], dict[str, set[str]]]:
    """
    Relevance: Operates within the epistemic hardness analysis layer.
    Concept: Construction of derived graph/model structures used by later stages.
    Contribution: Imports typed concept-graph evidence to avoid ad-hoc lexical classification.
    """

    method_map: dict[str, set[str]] = {}
    symbol_map: dict[str, set[str]] = {}
    blocked_by_barrier: dict[str, set[str]] = {}

    concept_graph = analysis.get("concept_graph", {}) if isinstance(analysis.get("concept_graph"), dict) else {}
    nodes = concept_graph.get("nodes", []) if isinstance(concept_graph.get("nodes"), list) else []
    relations = concept_graph.get("relations", []) if isinstance(concept_graph.get("relations"), list) else []
    node_lookup = {
        str(node.get("id", "")).strip(): node
        for node in nodes
        if isinstance(node, dict) and str(node.get("id", "")).strip()
    }

    for rel in relations:
        if not isinstance(rel, dict):
            continue
        from_node = str(rel.get("from", "")).strip()
        to_node = str(rel.get("to", "")).strip()
        relation = str(rel.get("relation", "")).strip().lower()
        sid_from = _statement_id_from_node(from_node, node_lookup)
        sid_to = _statement_id_from_node(to_node, node_lookup)

        if relation == "uses" and sid_from and to_node.startswith("method:"):
            tag = to_node.split("method:", 1)[1].strip().lower()
            if tag:
                method_map.setdefault(sid_from, set()).add(tag)
        if relation in {"uses", "defines"} and sid_from and to_node.startswith("concept:"):
            concept_label = to_node.split("concept:", 1)[1].strip().lower()
            if concept_label:
                symbol_map.setdefault(sid_from, set()).add(concept_label)
        if relation in {"obstructs", "blocks"} and sid_to:
            blocker_sid = _statement_id_from_node(from_node, node_lookup)
            if blocker_sid:
                blocked_by_barrier.setdefault(sid_to, set()).add(blocker_sid)
        if relation == "defines" and sid_from and to_node.startswith("barrier:"):
            blocked_by_barrier.setdefault(sid_from, set())

    return method_map, symbol_map, blocked_by_barrier


def _statement_method_tags(stmt: dict[str, Any], method_map: dict[str, set[str]]) -> set[str]:
    """
    Relevance: Operates within the epistemic hardness analysis layer.
    Concept: Extraction of structured signals from raw text or artifact payloads.
    Contribution: Unifies statement-native tags with concept-graph-derived method tags.
    """

    sid = str(stmt.get("id", "")).strip()
    tags = {str(t).strip().lower() for t in _normalize_list(stmt.get("method_tags")) if str(t).strip()}
    tags |= set(method_map.get(sid, set()))
    return {t for t in tags if t}


def _statement_symbol_vocab(stmt: dict[str, Any], symbol_map: dict[str, set[str]]) -> set[str]:
    """
    Relevance: Operates within the epistemic hardness analysis layer.
    Concept: Extraction of structured signals from raw text or artifact payloads.
    Contribution: Builds a typed symbol vocabulary for structural complexity-class classification.
    """

    sid = str(stmt.get("id", "")).strip()
    symbols: set[str] = set()
    for field in ("used_symbols", "concept_roles"):
        for item in _normalize_list(stmt.get(field)):
            symbols |= _tokenize_structural(item)
    symbols |= set(symbol_map.get(sid, set()))
    symbols |= _latex_symbol_tokens(str(stmt.get("latex", "")))
    return symbols


def _is_barrier_statement(
    stmt: dict[str, Any],
    method_tags: set[str],
    blocked_by_barrier: dict[str, set[str]],
) -> bool:
    """
    Relevance: Operates within the epistemic hardness analysis layer.
    Concept: Typed classification used to guide scoring and prioritization.
    Contribution: Identifies barrier statements from explicit structure rather than id token matching.
    """

    sid = str(stmt.get("id", "")).strip()
    if bool(stmt.get("is_barrier")):
        return True
    if str(stmt.get("barrier_family", "")).strip():
        return True
    if "barrier-analysis" in method_tags:
        return True
    if sid in blocked_by_barrier:
        return True
    return False


def _barrier_family(stmt: dict[str, Any], method_tags: set[str], symbols: set[str]) -> str:
    """
    Relevance: Operates within the epistemic hardness analysis layer.
    Concept: Typed classification used to guide scoring and prioritization.
    Contribution: Assigns barrier families using explicit metadata and concept-level symbols.
    """

    explicit = str(stmt.get("barrier_family", "")).strip().lower()
    if explicit:
        return explicit
    if "relativization" in method_tags or "oracle" in symbols:
        return "relativization"
    if "natural-proofs" in method_tags or ("natural" in symbols and "proof" in symbols):
        return "natural-proofs"
    if "algebrization" in method_tags:
        return "algebrization"
    if "barrier-analysis" in method_tags:
        return "generic-barrier"
    return "untyped-barrier"


def _severity(score: float) -> str:
    """
    Relevance: Operates within the epistemic hardness analysis layer.
    Concept: Internal helper implementing one deterministic step of this stage.
    Contribution: Contributes a deterministic transformation that supports end-to-end reasoning reproducibility.
    """

    if score >= 0.75:
        return "high"
    if score >= 0.45:
        return "medium"
    return "moderate"


def _short_text(value: Any, limit: int = 180) -> str:
    """
    Relevance: Operates within the epistemic hardness analysis layer.
    Concept: Internal helper implementing one deterministic step of this stage.
    Contribution: Converts statement payloads into compact human-readable concept labels.
    """

    text = " ".join(str(value or "").split())
    if len(text) <= limit:
        return text
    return text[: max(0, limit - 3)].rstrip() + "..."


def _statement_concept_row(
    sid: str,
    statements: dict[str, dict[str, Any]],
    phase_of: dict[str, str],
) -> dict[str, Any]:
    """
    Relevance: Operates within the epistemic hardness analysis layer.
    Concept: Extraction of structured signals from raw text or artifact payloads.
    Contribution: Links statement identifiers to concept-rich labels and phases.
    """

    stmt = statements.get(sid, {})
    concept_label = _short_text(stmt.get("informal") or stmt.get("latex") or sid, 220)
    return {
        "statement_id": sid,
        "kind": str(stmt.get("kind", "unknown")).strip().lower() or "unknown",
        "phase": str(phase_of.get(sid, "Unspecified")).strip() or "Unspecified",
        "concept_label": concept_label,
    }


def _build_concept_communication(
    statements: dict[str, dict[str, Any]],
    phase_of: dict[str, str],
    analysis: dict[str, Any],
    entrypoints: dict[str, Any],
    pathways: dict[str, Any],
    barrier_ids: list[str],
) -> dict[str, Any]:
    """
    Relevance: Operates within the epistemic hardness analysis layer.
    Concept: Construction of derived graph/model structures used by later stages.
    Contribution: Produces an explicit concept communication trace for reports and logs.
    """

    top_entrypoints = [
        item
        for item in (entrypoints.get("ranked_entrypoints", []) if isinstance(entrypoints.get("ranked_entrypoints"), list) else [])
        if isinstance(item, dict)
    ][:8]
    top_interventions = [
        item
        for item in (analysis.get("top_interventions", []) if isinstance(analysis.get("top_interventions"), list) else [])
        if isinstance(item, dict)
    ][:8]
    top_pathways = [
        item
        for item in (pathways.get("pathways", []) if isinstance(pathways.get("pathways"), list) else [])
        if isinstance(item, dict)
    ][:6]

    phase_pressure = Counter()
    entrypoint_rows: list[dict[str, Any]] = []
    for item in top_entrypoints:
        sid = str(item.get("statement_id", "")).strip()
        if not sid:
            continue
        phase = str(item.get("phase", "")).strip() or str(phase_of.get(sid, "Unspecified")).strip() or "Unspecified"
        phase_pressure[phase] += 1
        row = _statement_concept_row(sid=sid, statements=statements, phase_of=phase_of)
        row["entry_score"] = round(float(item.get("entry_score", 0.0) or 0.0), 4)
        row["rationale"] = _short_text(item.get("rationale", ""), 260)
        entrypoint_rows.append(row)

    intervention_rows: list[dict[str, Any]] = []
    for item in top_interventions:
        sid = str(item.get("statement_id", "")).strip()
        if not sid:
            continue
        row = _statement_concept_row(sid=sid, statements=statements, phase_of=phase_of)
        row["intervention_score"] = round(float(item.get("score", 0.0) or 0.0), 4)
        row["rationale"] = _short_text(item.get("rationale", ""), 220)
        row["concept_focus"] = [
            str(x).strip()
            for x in (item.get("concept_focus", []) if isinstance(item.get("concept_focus"), list) else [])
            if str(x).strip()
        ][:8]
        partner = str(item.get("best_cross_component_partner", "")).strip()
        if partner:
            row["best_cross_component_partner"] = partner
        intervention_rows.append(row)

    pathway_rows: list[dict[str, Any]] = []
    for item in top_pathways:
        sid = str(item.get("entry_statement_id", "")).strip()
        entry_label = _statement_concept_row(sid=sid, statements=statements, phase_of=phase_of) if sid else {}
        pathway_rows.append(
            {
                "path_id": str(item.get("path_id", "")).strip(),
                "entry_statement_id": sid,
                "entry_phase": str(item.get("entry_phase", "")).strip() or str(entry_label.get("phase", "Unspecified")),
                "entry_concept_label": str(entry_label.get("concept_label", "")).strip(),
                "pathway_score": round(float(item.get("pathway_score", 0.0) or 0.0), 4),
                "goal": _short_text(item.get("goal", ""), 240),
                "supporting_hypothesis_ids": [
                    str(h.get("id", "")).strip()
                    for h in (item.get("supporting_hypotheses", []) if isinstance(item.get("supporting_hypotheses"), list) else [])[:3]
                    if isinstance(h, dict) and str(h.get("id", "")).strip()
                ],
            }
        )

    barrier_set = {sid for sid in barrier_ids if sid}
    entrypoint_set = {str(item.get("statement_id", "")).strip() for item in top_entrypoints if isinstance(item, dict)}
    front_rows: list[dict[str, Any]] = []
    for candidate in analysis.get("connection_candidates", []) if isinstance(analysis.get("connection_candidates"), list) else []:
        if not isinstance(candidate, dict):
            continue
        src = str(candidate.get("from_id", "")).strip()
        dst = str(candidate.get("to_id", "")).strip()
        if not src or not dst:
            continue
        if src in barrier_set and dst in entrypoint_set:
            barrier_id, linked_id = src, dst
        elif dst in barrier_set and src in entrypoint_set:
            barrier_id, linked_id = dst, src
        else:
            continue
        front_rows.append(
            {
                "barrier_statement_id": barrier_id,
                "linked_entrypoint_id": linked_id,
                "score": round(float(candidate.get("score", 0.0) or 0.0), 4),
                "bridge_type": _short_text(candidate.get("semantic_relation", "") or candidate.get("bridge_type", ""), 80),
            }
        )
    front_rows.sort(key=lambda x: float(x.get("score", 0.0)), reverse=True)

    return {
        "phase_pressure": dict(phase_pressure),
        "top_entrypoint_concepts": entrypoint_rows,
        "top_intervention_concepts": intervention_rows,
        "pathway_concepts": pathway_rows,
        "barrier_connection_fronts": front_rows[:10],
    }


def _build_report(
    problem: str,
    statements: dict[str, dict[str, Any]],
    phase_of: dict[str, str],
    analysis: dict[str, Any],
    entrypoints: dict[str, Any],
    pathways: dict[str, Any],
    phyp: dict[str, Any],
) -> dict[str, Any]:
    """
    Relevance: Operates within the epistemic hardness analysis layer.
    Concept: Construction of derived graph/model structures used by later stages.
    Contribution: Creates the structural substrate that enables cross-stage scoring and interpretation.
    """

    kind_count = _kind_count(statements)
    edge_count, missing_dep = _dependency_edges(statements)
    n = max(1, len(statements))

    method_map, symbol_map, blocked_by_barrier = _analysis_structural_maps(analysis)
    theorem_ids = [sid for sid, d in statements.items() if str(d.get("kind", "")).lower() == "theorem"]
    theorem_method_tags = {sid: _statement_method_tags(statements[sid], method_map) for sid in theorem_ids}
    theorem_symbols = {sid: _statement_symbol_vocab(statements[sid], symbol_map) for sid in theorem_ids}

    restricted_lb_ids = [
        sid
        for sid in theorem_ids
        if bool(theorem_method_tags.get(sid, set()) & RESTRICTED_MODEL_METHOD_TAGS)
    ]
    grand_target_ids = [
        sid
        for sid in theorem_ids
        if bool(theorem_symbols.get(sid, set()) & GRAND_TARGET_SYMBOLS)
    ]
    barrier_ids = [
        sid
        for sid in theorem_ids
        if _is_barrier_statement(statements[sid], theorem_method_tags.get(sid, set()), blocked_by_barrier)
    ]

    top_ep = entrypoints.get("ranked_entrypoints", [])[:10]
    distinct_phases = {str(x.get("phase", "Unspecified")) for x in top_ep if isinstance(x, dict)}

    conn_count = len(analysis.get("connection_candidates", []))
    hyp_count = len(phyp.get("hypotheses", []))
    pathway_count = len(pathways.get("pathways", []))

    sparsity = 1.0 - min(1.0, edge_count / n)
    barrier_pressure = min(1.0, len(barrier_ids) / max(1, len(theorem_ids)))
    asymmetry = min(1.0, len(restricted_lb_ids) / max(1, len(grand_target_ids)))
    strategy_dispersion = min(1.0, len(distinct_phases) / 8.0)
    bridge_dependence = min(1.0, (conn_count / max(1, n)) * 0.5 + (hyp_count / max(1, n)) * 0.5)

    barrier_families: dict[str, list[str]] = {}
    for sid in barrier_ids:
        fam = _barrier_family(
            statements.get(sid, {}),
            theorem_method_tags.get(sid, set()),
            theorem_symbols.get(sid, set()),
        )
        barrier_families.setdefault(fam, []).append(sid)

    conceptual_hypothesis_count = sum(
        1
        for h in phyp.get("hypotheses", [])
        if isinstance(h, dict)
        and str(h.get("kind", "")).strip().lower()
        in {
            "definition-introduction",
            "representation-shift",
            "intermediate-invariant",
            "barrier-escape-principle",
            "analogy-transfer",
            "normal-form-reduction",
        }
    )

    essential_elements = [
        {
            "name": "Sparse Explicit Dependency Structure",
            "severity": _severity(sparsity),
            "score": round(sparsity, 4),
            "diagnosis": "Most canonical statements are not yet wired by formal depends_on links, so proof navigation is underdetermined.",
            "evidence": {
                "statement_count": n,
                "dependency_edges": edge_count,
                "missing_dependency_refs": missing_dep,
            },
            "evidence_ids": [],
        },
        {
            "name": "Barrier Stack Constraints",
            "severity": _severity(barrier_pressure),
            "score": round(barrier_pressure, 4),
            "diagnosis": "Multiple barrier theorems constrain broad proof templates and force barrier-aware method design.",
            "evidence": {
                "barrier_theorems": len(barrier_ids),
                "total_theorems": len(theorem_ids),
            },
            "evidence_ids": barrier_ids[:8],
        },
        {
            "name": "Asymmetric Lower-Bound Evidence",
            "severity": _severity(asymmetry),
            "score": round(asymmetry, 4),
            "diagnosis": "The KB has strong restricted-model lower bounds but relatively fewer direct bridges to full separation targets.",
            "evidence": {
                "restricted_lower_bounds": len(restricted_lb_ids),
                "grand_target_related_theorems": len(grand_target_ids),
            },
            "evidence_ids": (restricted_lb_ids[:5] + grand_target_ids[:5])[:10],
        },
        {
            "name": "Bridge-Hypothesis Dependence",
            "severity": _severity(bridge_dependence),
            "score": round(bridge_dependence, 4),
            "diagnosis": "Progress currently depends on conjectural bridges/hypotheses to connect otherwise weakly linked conceptual regions.",
            "evidence": {
                "connection_candidates": conn_count,
                "proof_hypotheses": hyp_count,
                "pathway_count": pathway_count,
            },
            "evidence_ids": [
                str(x.get("statement_id", ""))
                for x in analysis.get("top_interventions", [])[:6]
                if isinstance(x, dict)
            ],
        },
        {
            "name": "Plural, Underdetermined Strategy Space",
            "severity": _severity(strategy_dispersion),
            "score": round(strategy_dispersion, 4),
            "diagnosis": "Top entry points span multiple conceptual phases, indicating no single dominant route and high epistemic underdetermination.",
            "evidence": {
                "distinct_top_entrypoint_phases": sorted(distinct_phases),
                "top_entrypoints_used": len(top_ep),
            },
            "evidence_ids": [
                str(x.get("statement_id", ""))
                for x in top_ep[:8]
                if isinstance(x, dict)
            ],
        },
    ]

    essential_elements.sort(key=lambda x: x["score"], reverse=True)

    anti_barrier_programs = []
    for idx, (family, ids) in enumerate(sorted(barrier_families.items(), key=lambda kv: len(kv[1]), reverse=True), start=1):
        anti_barrier_programs.append(
            {
                "program_id": f"anti-barrier.{idx:03d}",
                "barrier_family": family,
                "barrier_ids": ids[:8],
                "minimal_conceptual_changes": [
                    "Introduce intermediate invariant that is not preserved by the barrier regime.",
                    "Search for representation-shift that maps target to a non-barrier proof model.",
                    "Use analogy-transfer from a neighboring regime with stronger lower-bound behavior.",
                ],
                "research_program": [
                    "Generate barrier-escape-principle hypotheses tied to top unresolved targets.",
                    "Run deduction checks on re-encoded target statements in scratch KB branches.",
                    "Retain only changes with non-negative coherence delta and positive entailment gain.",
                ],
            }
        )

    concept_communication = _build_concept_communication(
        statements=statements,
        phase_of=phase_of,
        analysis=analysis,
        entrypoints=entrypoints,
        pathways=pathways,
        barrier_ids=barrier_ids,
    )

    return {
        "problem": problem,
        "kb_stats": {
            "statement_count": n,
            "kind_count": dict(kind_count),
            "dependency_edges": edge_count,
            "missing_dependency_refs": missing_dep,
            "top_entrypoint_count": len(top_ep),
            "concept_phases_in_top_entrypoints": len(distinct_phases),
            "conceptual_hypothesis_count": conceptual_hypothesis_count,
            "barrier_family_count": len(barrier_families),
        },
        "epistemic_difficulty_summary": (
            f"{problem} is hard in this KB because global targets are framed across multiple incompatible proof regimes, "
            "barrier theorems restrict generic techniques, and explicit dependencies are sparse, forcing hypothesis-driven bridge construction."
        ),
        "concept_communication": concept_communication,
        "essential_elements": essential_elements,
        "anti_barrier_programs": anti_barrier_programs,
        "recommended_focus": [
            "Prioritize top-2 high-severity elements first in the abductive loop.",
            "Convert top bridge hypotheses into scratch dependency tests and run deduce checks.",
            "Backfill explicit depends_on links for highest-ranked entrypoint clusters.",
            "For each barrier family, run the paired anti-barrier program and keep only coherence-positive re-encodings.",
        ],
    }


def _to_markdown(report: dict[str, Any]) -> str:
    """
    Relevance: Operates within the epistemic hardness analysis layer.
    Concept: Rendering internal outputs into human-readable artifacts.
    Contribution: Improves interpretability by exposing machine results in analyst-friendly form.
    """

    lines = []
    lines.append(f"# Epistemic Hardness: {report['problem']}")
    lines.append("")
    lines.append("## Summary")
    lines.append("")
    lines.append(report["epistemic_difficulty_summary"])
    lines.append("")

    stats = report.get("kb_stats", {})
    lines.append("## KB Stats")
    lines.append("")
    lines.append(f"- Statements: {stats.get('statement_count', 0)}")
    lines.append(f"- Dependency edges: {stats.get('dependency_edges', 0)}")
    lines.append(f"- Missing dependency refs: {stats.get('missing_dependency_refs', 0)}")
    lines.append(f"- Top entry points considered: {stats.get('top_entrypoint_count', 0)}")
    lines.append(f"- Concept phases in top entry points: {stats.get('concept_phases_in_top_entrypoints', 0)}")
    lines.append(f"- Conceptual hypotheses: {stats.get('conceptual_hypothesis_count', 0)}")
    lines.append(f"- Barrier families: {stats.get('barrier_family_count', 0)}")
    lines.append("")

    concept_comm = report.get("concept_communication", {}) if isinstance(report.get("concept_communication"), dict) else {}
    phase_pressure = concept_comm.get("phase_pressure", {}) if isinstance(concept_comm.get("phase_pressure"), dict) else {}
    lines.append("## Concept Communication Trace")
    lines.append("")
    if phase_pressure:
        phase_blob = ", ".join(
            f"{phase}={count}"
            for phase, count in sorted(phase_pressure.items(), key=lambda kv: int(kv[1]), reverse=True)
        )
        lines.append(f"- Phase pressure (top entrypoints): {phase_blob}")
    else:
        lines.append("- Phase pressure (top entrypoints): unavailable")
    lines.append("")
    lines.append("### Entrypoint Concept Anchors")
    entrypoint_rows = concept_comm.get("top_entrypoint_concepts", []) if isinstance(concept_comm.get("top_entrypoint_concepts"), list) else []
    if not entrypoint_rows:
        lines.append("- none")
    for row in entrypoint_rows[:6]:
        lines.append(
            f"- `{row.get('statement_id', '')}` [{row.get('kind', 'unknown')}] "
            f"phase={row.get('phase', 'Unspecified')} score={row.get('entry_score', 0.0)}"
        )
        label = str(row.get("concept_label", "")).strip()
        if label:
            lines.append(f"  - concept: {label}")
    lines.append("")

    lines.append("### Intervention Concept Anchors")
    intervention_rows = concept_comm.get("top_intervention_concepts", []) if isinstance(concept_comm.get("top_intervention_concepts"), list) else []
    if not intervention_rows:
        lines.append("- none")
    for row in intervention_rows[:6]:
        lines.append(
            f"- `{row.get('statement_id', '')}` [{row.get('kind', 'unknown')}] "
            f"score={row.get('intervention_score', 0.0)} partner={row.get('best_cross_component_partner', '')}"
        )
        rationale = str(row.get("rationale", "")).strip()
        if rationale:
            lines.append(f"  - rationale: {rationale}")
        focus = row.get("concept_focus", []) if isinstance(row.get("concept_focus"), list) else []
        if focus:
            lines.append(f"  - concepts: {', '.join(str(x) for x in focus[:6])}")
    lines.append("")

    lines.append("### Pathway Concept Anchors")
    pathway_rows = concept_comm.get("pathway_concepts", []) if isinstance(concept_comm.get("pathway_concepts"), list) else []
    if not pathway_rows:
        lines.append("- none")
    for row in pathway_rows[:5]:
        lines.append(
            f"- `{row.get('path_id', '')}` phase={row.get('entry_phase', 'Unspecified')} "
            f"score={row.get('pathway_score', 0.0)} entry={row.get('entry_statement_id', '')}"
        )
        goal = str(row.get("goal", "")).strip()
        if goal:
            lines.append(f"  - goal: {goal}")
    lines.append("")

    lines.append("### Barrier Connection Fronts")
    barrier_fronts = concept_comm.get("barrier_connection_fronts", []) if isinstance(concept_comm.get("barrier_connection_fronts"), list) else []
    if not barrier_fronts:
        lines.append("- none")
    for row in barrier_fronts[:6]:
        lines.append(
            f"- barrier `{row.get('barrier_statement_id', '')}` <-> entry `{row.get('linked_entrypoint_id', '')}` "
            f"(score={row.get('score', 0.0)}, type={row.get('bridge_type', '') or 'bridge'})"
        )
    lines.append("")

    lines.append("## Essential Elements")
    lines.append("")
    lines.append("| element | severity | score | key evidence |")
    lines.append("|---|---|---|---|")
    for el in report.get("essential_elements", []):
        ev = el.get("evidence", {})
        ev_text = ", ".join(f"{k}={v}" for k, v in list(ev.items())[:3])
        lines.append(f"| {el['name']} | {el['severity']} | {el['score']} | {ev_text} |")
    lines.append("")

    for el in report.get("essential_elements", []):
        lines.append(f"### {el['name']}")
        lines.append(f"- Severity: {el['severity']} ({el['score']})")
        lines.append(f"- Diagnosis: {el['diagnosis']}")
        ids = el.get("evidence_ids", [])
        if ids:
            lines.append(f"- Evidence IDs: {', '.join(ids)}")
        lines.append("")

    lines.append("## Anti-Barrier Programs")
    lines.append("")
    for p in report.get("anti_barrier_programs", []):
        lines.append(f"### {p['program_id']} - {p['barrier_family']}")
        if p.get("barrier_ids"):
            lines.append(f"- Barrier IDs: {', '.join(p['barrier_ids'])}")
        lines.append("- Minimal conceptual changes:")
        for step in p.get("minimal_conceptual_changes", []):
            lines.append(f"  - {step}")
        lines.append("- Research program:")
        for step in p.get("research_program", []):
            lines.append(f"  - {step}")
        lines.append("")

    lines.append("## Recommended Focus")
    lines.append("")
    for i, rec in enumerate(report.get("recommended_focus", []), start=1):
        lines.append(f"{i}. {rec}")

    return "\n".join(lines) + "\n"


def main() -> int:
    """
    Relevance: Operates within the epistemic hardness analysis layer.
    Concept: CLI entrypoint orchestration for this script.
    Contribution: Binds parsing, computation, and artifact emission into a reproducible script execution.
    """

    logger = ReasoningLogger("kb-epistemic-hardness")
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--problem", required=True)
    ap.add_argument("--kb", required=True)
    ap.add_argument("--concept", required=True)
    ap.add_argument("--analysis", required=True)
    ap.add_argument("--entrypoints", required=True)
    ap.add_argument("--pathways", required=True)
    ap.add_argument("--phyp", required=True)
    ap.add_argument("--output-json")
    ap.add_argument("--output-md")
    args = ap.parse_args()
    logger.step(
        "Parsed hardness arguments",
        "\n".join(
            [
                f"problem={args.problem}",
                f"kb={args.kb}",
                f"concept={args.concept}",
                f"analysis={args.analysis}",
                f"entrypoints={args.entrypoints}",
                f"pathways={args.pathways}",
                f"phyp={args.phyp}",
                f"output_json={args.output_json or ''}",
                f"output_md={args.output_md or ''}",
            ]
        ),
    )

    kb_path = Path(args.kb)
    concept_path = Path(args.concept)
    analysis_path = Path(args.analysis)
    entrypoints_path = Path(args.entrypoints)
    pathways_path = Path(args.pathways)
    phyp_path = Path(args.phyp)

    for p in [kb_path, concept_path, analysis_path, entrypoints_path, pathways_path, phyp_path]:
        if not p.exists():
            log_path = logger.finalize("error", summary=f"Missing input: {p}")
            print(f"[LOG] {log_path}", file=sys.stderr)
            raise SystemExit(f"[ERROR] Missing input: {p}")

    statements = _load_kb(kb_path)
    phase_of = _phase_map(concept_path)
    try:
        analysis = validate_connection_analysis(json.loads(analysis_path.read_text(encoding="utf-8")), name="analysis")
        entrypoints = validate_entrypoints(json.loads(entrypoints_path.read_text(encoding="utf-8")), name="entrypoints")
        pathways = validate_pathways(json.loads(pathways_path.read_text(encoding="utf-8")), name="pathways")
        phyp = validate_phyp(yaml.safe_load(phyp_path.read_text(encoding="utf-8")), name="phyp")
    except ValueError as exc:
        log_path = logger.finalize("error", summary=str(exc))
        print(f"[LOG] {log_path}", file=sys.stderr)
        raise SystemExit(f"[ERROR] {exc}")

    report = _build_report(
        problem=args.problem,
        statements=statements,
        phase_of=phase_of,
        analysis=analysis,
        entrypoints=entrypoints,
        pathways=pathways,
        phyp=phyp,
    )
    concept_comm = report.get("concept_communication", {}) if isinstance(report.get("concept_communication"), dict) else {}
    logger.step(
        "Built concept communication trace",
        "\n".join(
            [
                f"phase_pressure={json.dumps(concept_comm.get('phase_pressure', {}), ensure_ascii=False)}",
                "top_entrypoint_concepts="
                + ", ".join(
                    str(item.get("statement_id", "")).strip()
                    for item in (concept_comm.get("top_entrypoint_concepts", []) if isinstance(concept_comm.get("top_entrypoint_concepts"), list) else [])[:5]
                    if str(item.get("statement_id", "")).strip()
                ),
                "top_intervention_concepts="
                + ", ".join(
                    str(item.get("statement_id", "")).strip()
                    for item in (concept_comm.get("top_intervention_concepts", []) if isinstance(concept_comm.get("top_intervention_concepts"), list) else [])[:5]
                    if str(item.get("statement_id", "")).strip()
                ),
            ]
        ),
    )

    if args.output_json:
        out = Path(args.output_json)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print(f"[OK] Wrote JSON: {out}")
        logger.add_output("epistemic_hardness_json", out)

    md = _to_markdown(report)
    if args.output_md:
        out = Path(args.output_md)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(md, encoding="utf-8")
        print(f"[OK] Wrote Markdown: {out}")
        logger.add_output("epistemic_hardness_md", out)

    print(f"[OK] Essential elements: {len(report.get('essential_elements', []))}")
    if report.get("essential_elements"):
        top = report["essential_elements"][0]
        print(f"[OK] Top hardness element: {top['name']} ({top['severity']}, score={top['score']})")
        logger.step(
            "Computed top hardness element",
            f"name={top['name']}\nseverity={top['severity']}\nscore={top['score']}",
        )
    log_path = logger.finalize(
        "success",
        summary=f"Computed {len(report.get('essential_elements', []))} epistemic hardness elements.",
    )
    print(f"[LOG] {log_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
