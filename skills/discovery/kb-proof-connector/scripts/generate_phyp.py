#!/usr/bin/env python3
# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
# 
# SPDX-License-Identifier: MIT

"""Generate proof hypotheses (phyp) from connector analysis.

Produces a YAML file under phyp/ with hypothesis types:
- bridge-link: conjectural support links between statements
- intervention-focus: prioritized abductive targets
- definition-introduction
- representation-shift
- intermediate-invariant
- barrier-escape-principle
- analogy-transfer
- normal-form-reduction
"""

from __future__ import annotations

import argparse
import datetime as dt
import re
import sys
from pathlib import Path
from typing import Any

import yaml

_COMMON_DIR = Path(__file__).resolve().parents[3] / "common"
if str(_COMMON_DIR) not in sys.path:
    sys.path.insert(0, str(_COMMON_DIR))

from reasoning_log import ReasoningLogger

STATEMENT_BLOCK_PATTERN = re.compile(r"```yaml\n(.*?)\n```", re.DOTALL)
GENERIC_TAGS = {
    "lower-bound",
    "hardness-vs-randomness",
    "circuit-complexity",
    "proof-complexity",
    "algebraic-method",
    "nonuniform-circuits",
    "uniform-model",
    "oracle-model",
    "randomness",
    "meta-complexity",
}
GENERIC_SIGNATURES = GENERIC_TAGS | {
    "lower-bound",
    "mild-lower-bound",
    "major-separation",
    "restricted-model-lower-bound",
    "query-lower-bound",
    "communication-lower-bound",
    "statement-conclusion",
    "unconditional",
}
ONTOLOGY_COMPLEXITY = "computational-complexity"
ONTOLOGY_MATHEMATICAL_PHYSICS = "mathematical-physics"
ONTOLOGY_FUNCTIONAL_ANALYSIS_SEMIGROUP = "functional-analysis-semigroup"
ONTOLOGY_FUNCTIONAL_ANALYSIS_MEASURE = "functional-analysis-measure-representation"
ONTOLOGY_FUNCTIONAL_ANALYSIS_FIXED_POINT = "functional-analysis-convex-fixed-point"
ONTOLOGY_GENERIC_MATHEMATICS = "generic-mathematics"
MASS_GAP_BRIDGE_FAMILIES = {
    "mass-gap-transfer-bridge",
    "transfer-matrix-to-gap-bridge",
    "correlator-decay-to-gap-bridge",
    "os-to-wightman-to-gap-bridge",
}
SEMIGROUP_BRIDGE_FAMILIES = {
    "resolvent-generation-bridge",
    "closure-density-bridge",
    "yosida-approximation-bridge",
    "contraction-specialization-bridge",
    "dissipativity-bridge",
    "cauchy-problem-bridge",
    "stone-self-adjointness-bridge",
    "spectral-calculus-bridge",
    "unitary-generator-bridge",
}
MEASURE_BRIDGE_FAMILIES = {
    "measure-representation-bridge",
    "regularity-reconstruction-bridge",
    "integration-duality-bridge",
}
FIXED_POINT_BRIDGE_FAMILIES = {
    "fixed-point-subset-bridge",
    "affine-averaging-bridge",
    "finite-intersection-bridge",
}


def _load_yaml_blocks(kb_path: Path) -> dict[str, dict[str, Any]]:
    """
    Relevance: Operates within the relational connector layer.
    Concept: Loading and structuring external artifacts for deterministic processing.
    Contribution: Provides clean, typed inputs so downstream reasoning steps remain auditable.
    """

    content = kb_path.read_text(encoding="utf-8")
    out: dict[str, dict[str, Any]] = {}
    for match in STATEMENT_BLOCK_PATTERN.finditer(content):
        try:
            payload = yaml.safe_load(match.group(1))
        except yaml.YAMLError:
            continue
        if not isinstance(payload, dict):
            continue
        sid = str(payload.get("id", "")).strip()
        kind = str(payload.get("kind", "")).strip().lower()
        if sid and kind:
            out[sid] = payload
    return out


def _derive_kb_slug(kb_path: Path) -> str:
    """
    Relevance: Operates within the relational connector layer.
    Concept: Internal helper implementing one deterministic step of this stage.
    Contribution: Contributes a deterministic transformation that supports end-to-end reasoning reproducibility.
    """

    name = kb_path.name
    if name.endswith(".kb.md"):
        name = name[:-6]
    return name


def _short_text(value: Any, max_chars: int = 180) -> str:
    """
    Relevance: Operates within the relational connector layer.
    Concept: Internal helper implementing one deterministic step of this stage.
    Contribution: Contributes a deterministic transformation that supports end-to-end reasoning reproducibility.
    """

    text = str(value or "").replace("\n", " ").strip()
    if len(text) <= max_chars:
        return text
    return text[: max_chars - 3].rstrip() + "..."


def _clamp01(value: float) -> float:
    """
    Relevance: Operates within the relational connector layer.
    Concept: Internal helper implementing one deterministic step of this stage.
    Contribution: Contributes a deterministic transformation that supports end-to-end reasoning reproducibility.
    """

    return max(0.0, min(1.0, value))


def _contains_token(*values: str) -> bool:
    """
    Relevance: Operates within the relational connector layer.
    Concept: Internal helper implementing one deterministic step of this stage.
    Contribution: Contributes a deterministic transformation that supports end-to-end reasoning reproducibility.
    """

    blob = " ".join(values).lower()
    return any(
        token in blob
        for token in (
            "barrier",
            "relativ",
            "algebr",
            "natural-proof",
            "oracle",
            "reduction",
            "equiv",
            "normal-form",
            "analogy",
            "invariant",
            "representation",
        )
    )


def _as_profile(value: Any) -> dict[str, Any]:
    """
    Relevance: Operates within the relational connector layer.
    Concept: Normalization of profile payloads into stable dictionaries.
    Contribution: Keeps hypothesis generation deterministic when connection-analysis rows omit optional profile fields.
    """

    return value if isinstance(value, dict) else {}


def _as_str_list(value: Any) -> list[str]:
    """
    Relevance: Operates within the relational connector layer.
    Concept: Normalization of heterogeneous payload values into ordered string lists.
    Contribution: Simplifies downstream commitment extraction while preserving auditable string content.
    """

    out: list[str] = []
    if isinstance(value, list):
        for item in value:
            text = str(item).strip()
            if text:
                out.append(text)
        return out
    text = str(value).strip()
    return [text] if text else []


def _pick_specific(values: list[str], fallback: list[str] | None = None) -> str:
    """
    Relevance: Operates within the relational connector layer.
    Concept: Deterministic selection of the most inferentially specific tag available.
    Contribution: Prevents bridge commitments from collapsing back to generic topical labels.
    """

    ordered = [str(v).strip() for v in values if str(v).strip()]
    ordered.sort(
        key=lambda item: (
            1 if item not in GENERIC_SIGNATURES else 0,
            int("implies" in item.lower() or "not-in" in item.lower() or "not-equal" in item.lower() or "collapse" in item.lower() or "separation" in item.lower()),
            int("-lower-bound" in item.lower() and item.lower() != "lower-bound"),
            int(
                any(
                    token in item.lower()
                    for token in (
                        "mcsp",
                        "gapmcsp",
                        "pit",
                        "ips",
                        "permanent",
                        "taut",
                        "acc0",
                        "ac0[p]",
                        "formula",
                        "nonuniform",
                        "communication",
                        "p/poly",
                        "nexp",
                        "ph",
                    )
                )
            ),
            len(item),
        ),
        reverse=True,
    )
    for item in ordered:
        if item not in GENERIC_SIGNATURES:
            return item
    if fallback:
        for item in fallback:
            text = str(item).strip()
            if text:
                return text
    return ordered[0] if ordered else ""


def _shared_values(from_profile: dict[str, Any], to_profile: dict[str, Any], key: str) -> list[str]:
    """
    Relevance: Operates within the relational connector layer.
    Concept: Extraction of overlap signals across paired statement profiles.
    Contribution: Supports invariant discovery by recovering the typed mathematical content shared by a candidate bridge.
    """

    return sorted(set(_as_str_list(from_profile.get(key))) & set(_as_str_list(to_profile.get(key))))


def _bridge_barrier_scope(from_profile: dict[str, Any], to_profile: dict[str, Any]) -> str:
    """
    Relevance: Operates within the relational connector layer.
    Concept: Barrier-scope extraction for bridge hypotheses.
    Contribution: Forces each hypothesis to declare the barrier family it must respect or evade.
    """

    barriers = sorted(set(_as_str_list(from_profile.get("barrier_signals"))) | set(_as_str_list(to_profile.get("barrier_signals"))))
    if not barriers:
        return "none"
    return " + ".join(barriers[:3])


def _candidate_ontology_profile(candidate: dict[str, Any], from_profile: dict[str, Any], to_profile: dict[str, Any]) -> str:
    """
    Relevance: Operates within the relational connector layer.
    Concept: Ontology routing for domain-specific bridge generation.
    Contribution: Ensures bridge templates are chosen from the mathematical domain actually represented by the candidate.
    """

    ontology_profile = str(from_profile.get("ontology_profile") or to_profile.get("ontology_profile") or "").strip()
    if ontology_profile:
        return ontology_profile
    blob = " ".join(
        [
            *(_as_str_list(from_profile.get("core_problems"))),
            *(_as_str_list(to_profile.get("core_problems"))),
            *(_as_str_list(from_profile.get("model_signatures"))),
            *(_as_str_list(to_profile.get("model_signatures"))),
            *(_as_str_list(candidate.get("specific_evidence"))),
            *(_as_str_list(candidate.get("evidence_terms"))),
        ]
    ).lower()
    if any(marker in blob for marker in ("mcsp", "pit", "nexp", "acc0", "p/poly", "ph-collapse")):
        return ONTOLOGY_COMPLEXITY
    if any(marker in blob for marker in ("yang-mills", "wightman", "osterwalder", "schwinger", "mass-gap", "continuum-limit", "reflection-positivity")):
        return ONTOLOGY_MATHEMATICAL_PHYSICS
    if any(
        marker in blob
        for marker in (
            "markov-kakutani-common-fixed-point",
            "common-fixed-point",
            "compact-convex-set",
            "commuting-affine-family",
            "invariant-fixed-point-subset",
            "cesaro-averaging",
            "finite-intersection-property",
            "continuous-affine-self-map-on-compact-convex-set",
        )
    ):
        return ONTOLOGY_FUNCTIONAL_ANALYSIS_FIXED_POINT
    if any(
        marker in blob
        for marker in (
            "riesz-markov-kakutani",
            "riesz representation",
            "regular-borel-measure",
            "regular borel measure",
            "radon-measure",
            "radon measure",
            "positive-linear-functional",
            "positive linear functional",
            "compactly-supported-continuous-functions",
            "vanishing-at-infinity-function-space",
            "integration-pairing-model",
            "signed-measure-decomposition",
            "function-separation-implies-measure-uniqueness",
            "c0-dual-implies-signed-regular-measure",
        )
    ):
        return ONTOLOGY_FUNCTIONAL_ANALYSIS_MEASURE
    if any(
        marker in blob
        for marker in (
            "c0-semigroup",
            "c_0-semigroup",
            "hille-yosida",
            "lumer-phillips",
            "stone theorem",
            "stone-correspondence",
            "one-parameter unitary group",
            "strongly-continuous-unitary-group",
            "self-adjoint",
            "spectral-functional-calculus",
            "yosida-approximation",
            "abstract-cauchy-problem",
            "resolvent",
            "dissipativity",
            "generator-of-exponentially-bounded-c0-semigroup",
            "closed-dense-operator-with-resolvent-power-bounds",
        )
    ):
        return ONTOLOGY_FUNCTIONAL_ANALYSIS_SEMIGROUP
    return ONTOLOGY_GENERIC_MATHEMATICS


def _profile_statement_phase(profile: dict[str, Any]) -> str:
    """
    Relevance: Operates within the relational connector layer.
    Concept: Accessor for statement-local phase metadata propagated from the KB.
    Contribution: Lets bridge typing use explicit phase assignments before falling back to text heuristics.
    """

    return str(profile.get("statement_phase", "")).strip().lower()


def _profile_bridge_roles(profile: dict[str, Any]) -> list[str]:
    """
    Relevance: Operates within the relational connector layer.
    Concept: Accessor for statement-local bridge-role metadata propagated from the KB.
    Contribution: Makes domain-specific bridge family selection depend on authored KB annotations instead of token coincidence.
    """

    return [str(role).strip().lower() for role in _as_str_list(profile.get("bridge_roles")) if str(role).strip()]


def _physics_bridge_template_family(candidate: dict[str, Any], from_profile: dict[str, Any], to_profile: dict[str, Any]) -> str:
    """
    Relevance: Operates within the relational connector layer.
    Concept: Domain-specific bridge-template typing for mathematical physics.
    Contribution: Promotes Yang-Mills bridge hypotheses from generic connector links into explicit proof-route families.
    """

    roles = set(_profile_bridge_roles(from_profile)) | set(_profile_bridge_roles(to_profile))
    if any(role.startswith("transfer-matrix-to-gap") for role in roles):
        return "transfer-matrix-to-gap-bridge"
    if any(role.startswith("correlator-decay-to-gap") for role in roles):
        return "correlator-decay-to-gap-bridge"
    if any(role.startswith("os-to-wightman-to-gap") for role in roles):
        return "os-to-wightman-to-gap-bridge"
    if any(role.startswith("os-reconstruction") or role == "os-to-wightman-bridge" for role in roles):
        return "os-reconstruction-bridge"
    if any(role.startswith("continuum-limit") for role in roles):
        return "continuum-limit-bridge"

    phases = {phase for phase in (_profile_statement_phase(from_profile), _profile_statement_phase(to_profile)) if phase}
    terms = " ".join(
        [
            str(candidate.get("relation", "")).strip(),
            *(_as_str_list(candidate.get("specific_evidence"))),
            *(_as_str_list(candidate.get("evidence_terms"))),
            *(_as_str_list(from_profile.get("antecedent_signatures"))),
            *(_as_str_list(from_profile.get("claim_signatures"))),
            *(_as_str_list(from_profile.get("implication_signatures"))),
            *(_as_str_list(to_profile.get("claim_signatures"))),
            *(_as_str_list(to_profile.get("consequence_signatures"))),
            *(_as_str_list(from_profile.get("model_signatures"))),
            *(_as_str_list(to_profile.get("model_signatures"))),
            *(_as_str_list(from_profile.get("barrier_signals"))),
            *(_as_str_list(to_profile.get("barrier_signals"))),
            *sorted(phases),
        ]
    ).lower()
    if "wightman-hamiltonian-framework" in phases and "mass-gap-and-spectral-transfer" in phases:
        return "os-to-wightman-to-gap-bridge"
    if "mass-gap-and-spectral-transfer" in phases and any(token in terms for token in ("transfer-matrix", "reflection-positivity")):
        return "transfer-matrix-to-gap-bridge"
    if "mass-gap-and-spectral-transfer" in phases and any(token in terms for token in ("correlator-decay", "exponential-correlation-decay")):
        return "correlator-decay-to-gap-bridge"
    if (
        any(token in terms for token in ("mass-gap", "positive-mass-gap", "spectral-gap", "correlator-decay", "exponential-correlation-decay"))
        and any(token in terms for token in ("transfer-matrix", "hamiltonian", "reflection-positivity", "schwinger"))
    ):
        return "mass-gap-transfer-bridge"
    if any(token in terms for token in ("osterwalder", "os-", "reflection-positivity", "reconstruction", "analytic continuation")) and any(
        token in terms for token in ("wightman", "schwinger", "minkowski")
    ):
        return "os-reconstruction-bridge"
    if any(token in terms for token in ("continuum-limit", "cutoff-removal", "ultraviolet-control", "renormalization-group", "lattice")):
        return "continuum-limit-bridge"
    return ""


def _semigroup_bridge_template_family(candidate: dict[str, Any], from_profile: dict[str, Any], to_profile: dict[str, Any]) -> str:
    """
    Relevance: Operates within the relational connector layer.
    Concept: Domain-specific bridge-template typing for semigroup generation theory.
    Contribution: Promotes Hille-Yosida bridge hypotheses from generic links into explicit proof-route families.
    """

    roles = set(_profile_bridge_roles(from_profile)) | set(_profile_bridge_roles(to_profile))
    if any(role.startswith("generator-recovery") or role.startswith("self-adjointness-witness") or role.startswith("correspondence-bijection") for role in roles):
        return "stone-self-adjointness-bridge"
    if any(role.startswith("spectral-calculus") or role.startswith("functional-calculus") or role.startswith("converse-construction") for role in roles):
        return "spectral-calculus-bridge"
    if any(role.startswith("generator-bridge") or role.startswith("unitary-group-foundation") for role in roles):
        return "unitary-generator-bridge"
    if any(role.startswith("regularity-prerequisite") for role in roles):
        return "closure-density-bridge"
    if any(role.startswith("contraction-specialization") for role in roles):
        return "contraction-specialization-bridge"
    if any(role.startswith("dissipativity-bridge") for role in roles):
        return "dissipativity-bridge"
    if any(role.startswith("evolution-equivalence") for role in roles):
        return "cauchy-problem-bridge"
    if any(role.startswith("approximation-scheme") for role in roles):
        return "yosida-approximation-bridge"
    if any(role.startswith("resolvent-foundation") or role.startswith("core-characterization") for role in roles):
        return "resolvent-generation-bridge"

    terms = " ".join(
        [
            str(candidate.get("relation", "")).strip(),
            *(_as_str_list(candidate.get("specific_evidence"))),
            *(_as_str_list(candidate.get("evidence_terms"))),
            *(_as_str_list(from_profile.get("antecedent_signatures"))),
            *(_as_str_list(from_profile.get("claim_signatures"))),
            *(_as_str_list(from_profile.get("implication_signatures"))),
            *(_as_str_list(to_profile.get("claim_signatures"))),
            *(_as_str_list(to_profile.get("consequence_signatures"))),
            *(_as_str_list(from_profile.get("model_signatures"))),
            *(_as_str_list(to_profile.get("model_signatures"))),
            *(_as_str_list(from_profile.get("barrier_signals"))),
            *(_as_str_list(to_profile.get("barrier_signals"))),
        ]
    ).lower()
    if "yosida" in terms or "approximant" in terms:
        return "yosida-approximation-bridge"
    if any(
        token in terms
        for token in (
            "stone-unitary-group-correspondence",
            "unique-self-adjoint-generator",
            "unitary-group-implies-self-adjoint-generator",
            "self-adjoint-generator-characterization",
        )
    ):
        return "stone-self-adjointness-bridge"
    if any(
        token in terms
        for token in (
            "spectral-functional-calculus",
            "spectral-theorem-enables-unitary-functional-calculus",
            "unitary-group-via-functional-calculus",
            "self-adjoint-spectral-calculus",
        )
    ):
        return "spectral-calculus-bridge"
    if any(
        token in terms
        for token in (
            "one-parameter unitary group",
            "strongly-continuous-unitary-group",
            "unitary-group-definition",
            "generator-definition",
            "differentiable-unitary-orbit-at-zero",
        )
    ):
        return "unitary-generator-bridge"
    if "dissipative" in terms or "surjective-shift" in terms or "range-condition" in terms:
        return "dissipativity-bridge"
    if "abstract-cauchy-problem" in terms or "well-posed" in terms or "mild solution" in terms:
        return "cauchy-problem-bridge"
    if "contraction" in terms and "resolvent" in terms:
        return "contraction-specialization-bridge"
    if any(token in terms for token in ("closed-dense", "domain-closure-density", "closed-densely-defined-generator", "generator-closed-dense")):
        return "closure-density-bridge"
    if any(
        token in terms
        for token in (
            "resolvent-generation-criterion",
            "resolvent-power-bounds",
            "closed-dense-plus-resolvent-powers-imply-c0-generation",
            "generator-of-exponentially-bounded-c0-semigroup",
        )
    ):
        return "resolvent-generation-bridge"
    return ""


def _measure_bridge_template_family(candidate: dict[str, Any], from_profile: dict[str, Any], to_profile: dict[str, Any]) -> str:
    """
    Relevance: Operates within the relational connector layer.
    Concept: Domain-specific bridge-template typing for measure-representation theorems.
    Contribution: Promotes Riesz-Markov-Kakutani bridge hypotheses from generic links into explicit measure-construction and duality routes.
    """

    roles = set(_profile_bridge_roles(from_profile)) | set(_profile_bridge_roles(to_profile))
    if any(role.startswith("measure-bridge") or role.startswith("representation-bijection") for role in roles):
        return "measure-representation-bridge"
    if any(role.startswith("regularity-witness") or role.startswith("compact-open-approximation") or role.startswith("uniqueness-separation") for role in roles):
        return "regularity-reconstruction-bridge"
    if any(role.startswith("integration-realization") or role.startswith("duality-extension") for role in roles):
        return "integration-duality-bridge"

    terms = " ".join(
        [
            str(candidate.get("relation", "")).strip(),
            *(_as_str_list(candidate.get("specific_evidence"))),
            *(_as_str_list(candidate.get("evidence_terms"))),
            *(_as_str_list(from_profile.get("antecedent_signatures"))),
            *(_as_str_list(from_profile.get("claim_signatures"))),
            *(_as_str_list(from_profile.get("implication_signatures"))),
            *(_as_str_list(to_profile.get("claim_signatures"))),
            *(_as_str_list(to_profile.get("consequence_signatures"))),
            *(_as_str_list(from_profile.get("model_signatures"))),
            *(_as_str_list(to_profile.get("model_signatures"))),
            *(_as_str_list(from_profile.get("barrier_signals"))),
            *(_as_str_list(to_profile.get("barrier_signals"))),
        ]
    ).lower()
    if any(
        token in terms
        for token in (
            "positive-functional-implies-regular-measure",
            "regular-borel-measure-representation",
            "functional-measure-correspondence",
            "riesz-markov-kakutani-correspondence",
        )
    ):
        return "measure-representation-bridge"
    if any(
        token in terms
        for token in (
            "function-separation-implies-measure-uniqueness",
            "unique-representing-measure",
            "topological-regularity-reconstruction",
            "compact-open-approximation",
            "regular-borel-measure-definition",
        )
    ):
        return "regularity-reconstruction-bridge"
    if any(
        token in terms
        for token in (
            "regular-measure-implies-positive-functional",
            "integration-defines-positive-functional",
            "signed-regular-measure-duality",
            "c0-dual-implies-signed-regular-measure",
            "dual-norm-total-variation",
        )
    ):
        return "integration-duality-bridge"
    return ""


def _fixed_point_bridge_template_family(candidate: dict[str, Any], from_profile: dict[str, Any], to_profile: dict[str, Any]) -> str:
    """
    Relevance: Operates within the relational connector layer.
    Concept: Domain-specific bridge-template typing for commuting affine fixed-point theorems.
    Contribution: Promotes Markov-Kakutani bridge hypotheses from generic links into explicit averaging, invariant-subset, and compactness-lift routes.
    """

    roles = set(_profile_bridge_roles(from_profile)) | set(_profile_bridge_roles(to_profile))
    if any(role.startswith("affine-averaging") for role in roles):
        return "affine-averaging-bridge"
    if any(role.startswith("fixed-point-subset") or role.startswith("commuting-invariance") or role.startswith("compact-convex-reduction") for role in roles):
        return "fixed-point-subset-bridge"
    if any(role.startswith("finite-intersection") or role.startswith("family-fixed-point") for role in roles):
        return "finite-intersection-bridge"

    terms = " ".join(
        [
            str(candidate.get("relation", "")).strip(),
            *(_as_str_list(candidate.get("specific_evidence"))),
            *(_as_str_list(candidate.get("evidence_terms"))),
            *(_as_str_list(from_profile.get("antecedent_signatures"))),
            *(_as_str_list(from_profile.get("claim_signatures"))),
            *(_as_str_list(from_profile.get("implication_signatures"))),
            *(_as_str_list(to_profile.get("claim_signatures"))),
            *(_as_str_list(to_profile.get("consequence_signatures"))),
            *(_as_str_list(from_profile.get("model_signatures"))),
            *(_as_str_list(to_profile.get("model_signatures"))),
            *(_as_str_list(from_profile.get("barrier_signals"))),
            *(_as_str_list(to_profile.get("barrier_signals"))),
        ]
    ).lower()
    if any(token in terms for token in ("cesaro-averaging", "affine-averaging-implies-single-map-fixed-point", "affine-orbit-averages-in-compact-convex-set")):
        return "affine-averaging-bridge"
    if any(
        token in terms
        for token in (
            "invariant-fixed-point-subset",
            "single-map-fixed-point-implies-invariant-fixed-point-subset",
            "nonempty-compact-convex-fixed-point-subset",
            "commutativity-implies-fixed-point-subset-invariance",
        )
    ):
        return "fixed-point-subset-bridge"
    if any(
        token in terms
        for token in (
            "finite-intersection-property",
            "finite-intersection-property-implies-common-fixed-point",
            "common-fixed-point-for-finite-commuting-family",
            "common-fixed-point-for-commuting-family",
        )
    ):
        return "finite-intersection-bridge"
    return ""


def _bridge_template_family(candidate: dict[str, Any], commitments: dict[str, Any]) -> str:
    """
    Relevance: Operates within the relational connector layer.
    Concept: Template-family inference for bridge and conceptual hypotheses.
    Contribution: Keeps the generated phyp aligned with domain-specific proof routes instead of generic relation labels.
    """

    from_profile = _as_profile(candidate.get("from_profile"))
    to_profile = _as_profile(candidate.get("to_profile"))
    ontology_profile = _candidate_ontology_profile(candidate, from_profile, to_profile)
    if ontology_profile == ONTOLOGY_MATHEMATICAL_PHYSICS:
        family = _physics_bridge_template_family(candidate, from_profile, to_profile)
        if family:
            return family
    if ontology_profile == ONTOLOGY_FUNCTIONAL_ANALYSIS_FIXED_POINT:
        family = _fixed_point_bridge_template_family(candidate, from_profile, to_profile)
        if family:
            return family
    if ontology_profile == ONTOLOGY_FUNCTIONAL_ANALYSIS_MEASURE:
        family = _measure_bridge_template_family(candidate, from_profile, to_profile)
        if family:
            return family
    if ontology_profile == ONTOLOGY_FUNCTIONAL_ANALYSIS_SEMIGROUP:
        family = _semigroup_bridge_template_family(candidate, from_profile, to_profile)
        if family:
            return family
    relation = str(candidate.get("relation", "")).strip().lower()
    if commitments.get("barrier_scope", "none") != "none":
        return "barrier-aware-bridge"
    if relation == "definitional-expansion":
        return "definitional-bridge"
    if relation == "potential-equivalence":
        return "equivalence-bridge"
    return "structural-support-bridge"


def _bridge_invariant(candidate: dict[str, Any], from_profile: dict[str, Any], to_profile: dict[str, Any]) -> tuple[str, list[str]]:
    """
    Relevance: Operates within the relational connector layer.
    Concept: Extraction of preserved invariants for bridge hypotheses.
    Contribution: Converts a raw connector edge into a mathematically testable claim about what structure survives across the bridge.
    """

    shared_problems = _shared_values(from_profile, to_profile, "core_problems")
    shared_models = _shared_values(from_profile, to_profile, "model_signatures")
    shared_claims = _shared_values(from_profile, to_profile, "claim_signatures")
    shared_consequences = _shared_values(from_profile, to_profile, "consequence_signatures")
    shared_reductions = _shared_values(from_profile, to_profile, "reduction_signatures")
    shared_classes = _shared_values(from_profile, to_profile, "complexity_classes")
    basis = [str(x).strip() for x in candidate.get("specific_evidence", []) if str(x).strip()]
    ontology_profile = _candidate_ontology_profile(candidate, from_profile, to_profile)
    if ontology_profile == ONTOLOGY_MATHEMATICAL_PHYSICS:
        family = _physics_bridge_template_family(candidate, from_profile, to_profile)
        physics_basis = (
            shared_problems
            + shared_models
            + shared_claims
            + shared_consequences
            + _as_str_list(from_profile.get("antecedent_signatures"))
            + _as_str_list(to_profile.get("consequence_signatures"))
            + basis
        )
        ordered_basis = [item for item in _sort_unique(physics_basis) if item]
        if family == "os-reconstruction-bridge":
            target_models = _as_str_list(to_profile.get("model_signatures"))
            wightman_models = [item for item in target_models if "wightman" in item.lower()]
            model = _pick_specific(wightman_models or target_models or shared_models or _as_str_list(from_profile.get("model_signatures")))
            return f"OS reconstruction interface in {model or 'OS-Euclidean-QFT'}", ordered_basis[:6]
        if family == "os-to-wightman-to-gap-bridge":
            target_models = _as_str_list(to_profile.get("model_signatures"))
            wightman_models = [item for item in target_models if "wightman" in item.lower() or "hamiltonian" in item.lower()]
            model = _pick_specific(wightman_models or target_models or shared_models or _as_str_list(from_profile.get("model_signatures")))
            return f"OS-to-Wightman mass-gap transfer in {model or 'Wightman-QFT'}", ordered_basis[:6]
        if family == "transfer-matrix-to-gap-bridge":
            target_models = _as_str_list(to_profile.get("model_signatures"))
            spectral_models = [item for item in target_models if "transfer" in item.lower() or "hamiltonian" in item.lower()]
            model = _pick_specific(spectral_models or target_models or shared_models or _as_str_list(from_profile.get("model_signatures")))
            return f"transfer-matrix spectral witness in {model or 'reflection-positive-transfer-matrix'}", ordered_basis[:6]
        if family == "correlator-decay-to-gap-bridge":
            target_models = _as_str_list(to_profile.get("model_signatures"))
            decay_models = [item for item in target_models if "schwinger" in item.lower() or "decay" in item.lower() or "hamiltonian" in item.lower()]
            model = _pick_specific(decay_models or target_models or shared_models or _as_str_list(from_profile.get("model_signatures")))
            return f"correlator-decay mass-gap witness in {model or 'Schwinger-function-decay'}", ordered_basis[:6]
        if family == "mass-gap-transfer-bridge":
            model = _pick_specific(shared_models or _as_str_list(to_profile.get("model_signatures")) + _as_str_list(from_profile.get("model_signatures")))
            return f"mass-gap witness transfer in {model or 'Hamiltonian-mass-gap'}", ordered_basis[:6]
        if family == "continuum-limit-bridge":
            model = _pick_specific(shared_models or _as_str_list(to_profile.get("model_signatures")) + _as_str_list(from_profile.get("model_signatures")))
            return f"continuum-limit control in {model or 'continuum-limit'}", ordered_basis[:6]
    if ontology_profile == ONTOLOGY_FUNCTIONAL_ANALYSIS_MEASURE:
        family = _measure_bridge_template_family(candidate, from_profile, to_profile)
        measure_basis = (
            shared_problems
            + shared_models
            + shared_claims
            + shared_consequences
            + _as_str_list(from_profile.get("antecedent_signatures"))
            + _as_str_list(to_profile.get("consequence_signatures"))
            + basis
        )
        ordered_basis = [item for item in _sort_unique(measure_basis) if item]
        if family == "measure-representation-bridge":
            model = _pick_specific(shared_models or _as_str_list(to_profile.get("model_signatures")) + _as_str_list(from_profile.get("model_signatures")))
            return f"regular-Borel representation in {model or 'locally-compact-Hausdorff-space'}", ordered_basis[:6]
        if family == "regularity-reconstruction-bridge":
            model = _pick_specific(shared_models or _as_str_list(to_profile.get("model_signatures")) + _as_str_list(from_profile.get("model_signatures")))
            return f"compact-open regularity control in {model or 'regular-Borel-measure-model'}", ordered_basis[:6]
        if family == "integration-duality-bridge":
            model = _pick_specific(shared_models or _as_str_list(to_profile.get("model_signatures")) + _as_str_list(from_profile.get("model_signatures")))
            return f"integration duality pairing in {model or 'integration-pairing-model'}", ordered_basis[:6]
    if ontology_profile == ONTOLOGY_FUNCTIONAL_ANALYSIS_FIXED_POINT:
        family = _fixed_point_bridge_template_family(candidate, from_profile, to_profile)
        fp_basis = (
            shared_problems
            + shared_models
            + shared_claims
            + shared_consequences
            + _as_str_list(from_profile.get("antecedent_signatures"))
            + _as_str_list(to_profile.get("consequence_signatures"))
            + basis
        )
        ordered_basis = [item for item in _sort_unique(fp_basis) if item]
        if family == "affine-averaging-bridge":
            model = _pick_specific(shared_models or _as_str_list(to_profile.get("model_signatures")) + _as_str_list(from_profile.get("model_signatures")))
            return f"averaged affine orbit stabilization in {model or 'compact-convex-subset'}", ordered_basis[:6]
        if family == "fixed-point-subset-bridge":
            model = _pick_specific(shared_models or _as_str_list(to_profile.get("model_signatures")) + _as_str_list(from_profile.get("model_signatures")))
            return f"nonempty compact-convex fixed-point subset in {model or 'invariant-fixed-point-subset'}", ordered_basis[:6]
        if family == "finite-intersection-bridge":
            model = _pick_specific(shared_models or _as_str_list(to_profile.get("model_signatures")) + _as_str_list(from_profile.get("model_signatures")))
            return f"finite-intersection lift in {model or 'finite-intersection-compactness'}", ordered_basis[:6]
    if ontology_profile == ONTOLOGY_FUNCTIONAL_ANALYSIS_SEMIGROUP:
        family = _semigroup_bridge_template_family(candidate, from_profile, to_profile)
        semigroup_basis = (
            shared_problems
            + shared_models
            + shared_claims
            + shared_consequences
            + _as_str_list(from_profile.get("antecedent_signatures"))
            + _as_str_list(to_profile.get("consequence_signatures"))
            + basis
        )
        ordered_basis = [item for item in _sort_unique(semigroup_basis) if item]
        if family == "stone-self-adjointness-bridge":
            model = _pick_specific(shared_models or _as_str_list(to_profile.get("model_signatures")) + _as_str_list(from_profile.get("model_signatures")))
            return f"self-adjoint generator recovery in {model or 'strongly-continuous-unitary-group'}", ordered_basis[:6]
        if family == "spectral-calculus-bridge":
            model = _pick_specific(shared_models or _as_str_list(to_profile.get("model_signatures")) + _as_str_list(from_profile.get("model_signatures")))
            return f"spectral functional-calculus realization in {model or 'spectral-functional-calculus'}", ordered_basis[:6]
        if family == "unitary-generator-bridge":
            model = _pick_specific(shared_models or _as_str_list(to_profile.get("model_signatures")) + _as_str_list(from_profile.get("model_signatures")))
            return f"unitary orbit infinitesimal control in {model or 'strongly-continuous-unitary-group'}", ordered_basis[:6]
        if family == "resolvent-generation-bridge":
            model = _pick_specific(shared_models or _as_str_list(to_profile.get("model_signatures")) + _as_str_list(from_profile.get("model_signatures")))
            return f"resolvent growth control in {model or 'resolvent-generation-criterion'}", ordered_basis[:6]
        if family == "closure-density-bridge":
            return "closed densely defined generator regularity", ordered_basis[:6]
        if family == "yosida-approximation-bridge":
            model = _pick_specific(shared_models or _as_str_list(to_profile.get("model_signatures")) + _as_str_list(from_profile.get("model_signatures")))
            return f"Yosida approximation convergence in {model or 'Yosida-approximation-scheme'}", ordered_basis[:6]
        if family == "contraction-specialization-bridge":
            return "first-resolvent contraction witness", ordered_basis[:6]
        if family == "dissipativity-bridge":
            return "dissipative range-surjectivity criterion", ordered_basis[:6]
        if family == "cauchy-problem-bridge":
            return "generator-to-well-posed-evolution correspondence", ordered_basis[:6]

    if shared_problems:
        problem = shared_problems[0]
        if shared_models:
            if ontology_profile == ONTOLOGY_COMPLEXITY:
                return f"{problem} complexity profile in {shared_models[0]}", ([problem] + shared_models + basis)[:6]
            if ontology_profile == ONTOLOGY_MATHEMATICAL_PHYSICS:
                return f"{problem} structural profile in {shared_models[0]}", ([problem] + shared_models + basis)[:6]
            return f"{problem} mathematical profile in {shared_models[0]}", ([problem] + shared_models + basis)[:6]
        return f"{problem} semantic object", ([problem] + basis)[:6]
    if shared_consequences:
        consequence = _pick_specific(shared_consequences, fallback=shared_consequences)
        return f"consequence schema {consequence}", ([consequence] + basis)[:6]
    if shared_claims:
        claim = _pick_specific(shared_claims, fallback=shared_claims)
        if "lower-bound" in claim:
            return f"{claim} witness complexity", ([claim] + basis)[:6]
        return f"claim schema {claim}", ([claim] + basis)[:6]
    if shared_models:
        model = _pick_specific(shared_models, fallback=shared_models)
        if ontology_profile == ONTOLOGY_COMPLEXITY:
            return f"{model} complexity measure", ([model] + basis)[:6]
        if ontology_profile == ONTOLOGY_MATHEMATICAL_PHYSICS:
            return f"{model} structural control", ([model] + basis)[:6]
        return f"{model} mathematical structure", ([model] + basis)[:6]
    if shared_reductions:
        reduction = _pick_specific(shared_reductions, fallback=shared_reductions)
        return f"{reduction} preservation", ([reduction] + basis)[:6]
    if shared_classes:
        cls = _pick_specific(shared_classes, fallback=shared_classes)
        if ontology_profile == ONTOLOGY_COMPLEXITY:
            return f"{cls} class-theoretic consequence", ([cls] + basis)[:6]
        return f"{cls} consequence", ([cls] + basis)[:6]
    relation = str(candidate.get("relation", "potential-support")).replace("-", " ").strip()
    return f"{relation or 'support'} interface", basis[:6]


def _sort_unique(values: list[str]) -> list[str]:
    """
    Relevance: Operates within the relational connector layer.
    Concept: Stable de-duplication preserving specificity ordering.
    Contribution: Prevents bridge commitments from being inflated by repeated evidence markers.
    """

    return _sort_values(values)


def _sort_values(values: list[str]) -> list[str]:
    """
    Relevance: Operates within the relational connector layer.
    Concept: Stable ordering helper for human-readable commitment payloads.
    Contribution: Keeps domain-specific invariant bases concise and reproducible.
    """

    seen: set[str] = set()
    ordered: list[str] = []
    for item in values:
        text = str(item).strip()
        if not text or text in seen:
            continue
        seen.add(text)
        ordered.append(text)
    ordered.sort(key=lambda item: (len(item), item), reverse=True)
    return ordered


def _inferential_commitments(candidate: dict[str, Any]) -> dict[str, Any]:
    """
    Relevance: Operates within the relational connector layer.
    Concept: Construction of explicit antecedent/consequence/invariant commitments for a candidate bridge.
    Contribution: Turns connector candidates into abductive objects that can be assessed as mathematical proof moves rather than loose associations.
    """

    from_profile = _as_profile(candidate.get("from_profile"))
    to_profile = _as_profile(candidate.get("to_profile"))
    ontology_profile = _candidate_ontology_profile(candidate, from_profile, to_profile)
    preserved_invariant, invariant_basis = _bridge_invariant(candidate, from_profile, to_profile)
    support_antecedent = _pick_specific(
        _as_str_list(from_profile.get("antecedent_signatures")),
        fallback=_as_str_list(from_profile.get("implication_signatures")) + _as_str_list(from_profile.get("claim_signatures")),
    )
    target_candidates = _as_str_list(to_profile.get("consequence_signatures"))
    if ontology_profile == ONTOLOGY_FUNCTIONAL_ANALYSIS_FIXED_POINT:
        fixed_point_candidates = [
            item
            for item in target_candidates
            if any(
                token in item.lower()
                for token in (
                    "fixed-point",
                    "common-fixed-point",
                    "invariant-fixed-point-subset",
                    "finite-commuting-family",
                )
            )
        ]
        target_consequence = _pick_specific(fixed_point_candidates or target_candidates, fallback=_as_str_list(to_profile.get("claim_signatures")))
    elif ontology_profile == ONTOLOGY_FUNCTIONAL_ANALYSIS_MEASURE:
        representation_candidates = [
            item
            for item in target_candidates
            if any(
                token in item.lower()
                for token in (
                    "representation",
                    "correspondence",
                    "unique-representing-measure",
                    "signed-regular-measure-duality",
                    "dual-norm-total-variation",
                )
            )
        ]
        target_consequence = _pick_specific(representation_candidates or target_candidates, fallback=_as_str_list(to_profile.get("claim_signatures")))
    else:
        target_consequence = _pick_specific(
            target_candidates,
            fallback=_as_str_list(to_profile.get("claim_signatures")),
        )
    if not target_consequence:
        target_consequence = _pick_specific(
            _as_str_list(to_profile.get("implication_signatures")),
            fallback=_as_str_list(to_profile.get("claim_signatures")),
        )
    return {
        "support_antecedent_schema": support_antecedent or "unconditional",
        "target_consequence_schema": target_consequence or "statement-conclusion",
        "preserved_invariant": preserved_invariant,
        "invariant_basis": invariant_basis,
        "barrier_scope": _bridge_barrier_scope(from_profile, to_profile),
    }


def _bridge_link_payload(
    candidate: dict[str, Any],
    commitments: dict[str, Any],
    from_id: str,
    to_id: str,
) -> dict[str, Any]:
    """
    Relevance: Operates within the relational connector layer.
    Concept: Domain-aware rendering of bridge-link hypotheses.
    Contribution: Expresses bridge hypotheses as proof-route templates rather than generic graph edges.
    """

    family = _bridge_template_family(candidate, commitments)
    relation = str(candidate.get("relation", "potential-support"))
    antecedent = commitments["support_antecedent_schema"]
    consequence = commitments["target_consequence_schema"]
    invariant = commitments["preserved_invariant"]
    barrier = commitments["barrier_scope"]

    if family == "stone-self-adjointness-bridge":
        return {
            "template_family": family,
            "hypothesis_latex": (
                f"\\text{{If }} {from_id} \\text{{ supplies a Stone self-adjointness bridge preserving }}"
                f" \\texttt{{{invariant}}} \\text{{ from }}\\texttt{{{antecedent}}}"
                f" \\text{{ toward }}\\texttt{{{consequence}}}\\text{{ for }} {to_id},"
                " \\text{ then the hidden generator-to-self-adjoint realization route becomes testable.}"
            ),
            "informal": (
                f"Treat {from_id} as a conjectural Stone self-adjointness bridge for {to_id}; the move should recover a self-adjoint generator from unitary-orbit data while preserving `{invariant}` and targeting `{consequence}` under barrier scope `{barrier}`."
            ),
            "validation_protocol": [
                f"State the unitary-group or orbit-differentiability ingredient contributed by {from_id}.",
                f"Check whether `{invariant}` suffices to recover a densely defined self-adjoint generator for {to_id}.",
                "Verify that the bridge yields a genuine uniqueness or self-adjointness statement, not only a formal derivative notation.",
                f"Run kb-deduce on {to_id} and record whether a self-adjoint-generator consequence becomes derivable or conditionally derivable.",
                f"Run kb-abduce on {to_id} to isolate the remaining domain or spectral lemmas after adding {from_id}.",
            ],
            "falsifier": (
                f"Reject bridge {from_id}->{to_id} if unitary-orbit data cannot be upgraded into a self-adjoint generator, if `{invariant}` fails to transfer, or if the move yields no Stone-specific deductive gain."
            ),
        }
    if family == "spectral-calculus-bridge":
        return {
            "template_family": family,
            "hypothesis_latex": (
                f"\\text{{If }} {from_id} \\text{{ supplies a spectral-calculus bridge preserving }}"
                f" \\texttt{{{invariant}}} \\text{{ from }}\\texttt{{{antecedent}}}"
                f" \\text{{ toward }}\\texttt{{{consequence}}}\\text{{ for }} {to_id},"
                " \\text{ then the self-adjoint-to-unitary realization route becomes testable.}"
            ),
            "informal": (
                f"Treat {from_id} as a conjectural spectral-calculus bridge for {to_id}; the move should turn self-adjoint or spectral data into a one-parameter unitary group while preserving `{invariant}` and targeting `{consequence}`."
            ),
            "validation_protocol": [
                f"State the spectral theorem or functional-calculus ingredient contributed by {from_id}.",
                f"Check whether `{invariant}` survives the passage from self-adjoint data to exponentiated unitary dynamics in {to_id}.",
                "Verify that the bridge yields a strongly continuous unitary group, not only a formal exponential expression.",
                f"Run kb-deduce on {to_id} and record whether a unitary-group realization becomes derivable or conditionally derivable.",
                f"Run kb-abduce on {to_id} to isolate the remaining continuity or spectral-measure lemmas after adding {from_id}.",
            ],
            "falsifier": (
                f"Reject bridge {from_id}->{to_id} if the spectral theorem cannot be converted into a genuine unitary one-parameter group, if `{invariant}` fails, or if no spectral-calculus-specific deductive gain appears."
            ),
        }
    if family == "unitary-generator-bridge":
        return {
            "template_family": family,
            "hypothesis_latex": (
                f"\\text{{If }} {from_id} \\text{{ supplies a unitary-generator bridge preserving }}"
                f" \\texttt{{{invariant}}} \\text{{ from }}\\texttt{{{antecedent}}}"
                f" \\text{{ toward }}\\texttt{{{consequence}}}\\text{{ for }} {to_id},"
                " \\text{ then the infinitesimal-orbit route becomes testable.}"
            ),
            "informal": (
                f"Treat {from_id} as a conjectural unitary-generator bridge for {to_id}; the move should expose the infinitesimal operator carried by a strongly continuous unitary orbit while preserving `{invariant}`."
            ),
            "validation_protocol": [
                f"Identify the orbit or derivative-at-zero ingredient contributed by {from_id}.",
                f"Check whether `{invariant}` is sufficient to define a dense operator domain associated with {to_id}.",
                "Verify that the bridge yields a mathematically meaningful infinitesimal generator, not only a restatement of the group law.",
                f"Run kb-deduce on {to_id} and record whether a generator-recovery consequence becomes derivable.",
                f"Run kb-abduce on {to_id} to isolate the remaining self-adjointness or continuity lemmas after adding {from_id}.",
            ],
            "falsifier": (
                f"Reject bridge {from_id}->{to_id} if no infinitesimal operator is recovered from the unitary orbit, if `{invariant}` fails, or if the move yields no generator-specific deductive gain."
            ),
        }
    if family == "measure-representation-bridge":
        return {
            "template_family": family,
            "hypothesis_latex": (
                f"\\text{{If }} {from_id} \\text{{ supplies a measure-representation bridge preserving }}"
                f" \\texttt{{{invariant}}} \\text{{ from }}\\texttt{{{antecedent}}}"
                f" \\text{{ toward }}\\texttt{{{consequence}}}\\text{{ for }} {to_id},"
                " \\text{ then the positive-functional-to-measure route becomes testable.}"
            ),
            "informal": (
                f"Treat {from_id} as a conjectural measure-representation bridge for {to_id}; the move should turn positive functional data into a unique regular Borel measure while preserving `{invariant}` and targeting `{consequence}` under barrier scope `{barrier}`."
            ),
            "validation_protocol": [
                f"State the positivity and function-space ingredient contributed by {from_id}.",
                f"Check whether `{invariant}` is strong enough to force a regular Borel measure representing {to_id}.",
                "Verify that the bridge yields a genuinely countably additive regular measure, not only a finitely additive set function.",
                f"Run kb-deduce on {to_id} and record whether a representation-by-measure consequence becomes derivable or conditionally derivable.",
                f"Run kb-abduce on {to_id} to isolate the remaining regularity or approximation lemmas after adding {from_id}.",
            ],
            "falsifier": (
                f"Reject bridge {from_id}->{to_id} if positivity cannot be upgraded into a regular Borel measure, if `{invariant}` fails, or if the move yields no measure-representation-specific deductive gain."
            ),
        }
    if family == "affine-averaging-bridge":
        return {
            "template_family": family,
            "hypothesis_latex": (
                f"\\text{{If }} {from_id} \\text{{ supplies an affine-averaging bridge preserving }}"
                f" \\texttt{{{invariant}}} \\text{{ from }}\\texttt{{{antecedent}}}"
                f" \\text{{ toward }}\\texttt{{{consequence}}}\\text{{ for }} {to_id},"
                " \\text{ then the single-map fixed-point route becomes testable.}"
            ),
            "informal": (
                f"Treat {from_id} as a conjectural affine-averaging bridge for {to_id}; the move should convert affine orbit averages into a genuine fixed-point witness while preserving `{invariant}` and targeting `{consequence}` under barrier scope `{barrier}`."
            ),
            "validation_protocol": [
                f"State the averaging or orbit-compactness ingredient contributed by {from_id}.",
                f"Check whether `{invariant}` is sufficient to turn approximate fixed points into an actual fixed point for {to_id}.",
                "Verify that the bridge produces a fixed point rather than only a sequence of averaged approximants.",
                f"Run kb-deduce on {to_id} and record whether the single-map fixed-point consequence becomes derivable or conditionally derivable.",
                f"Run kb-abduce on {to_id} to isolate the remaining compactness or continuity lemmas after adding {from_id}.",
            ],
            "falsifier": (
                f"Reject bridge {from_id}->{to_id} if affine averaging never yields a genuine fixed point, if `{invariant}` fails, or if the move yields no averaging-specific deductive gain."
            ),
        }
    if family == "fixed-point-subset-bridge":
        return {
            "template_family": family,
            "hypothesis_latex": (
                f"\\text{{If }} {from_id} \\text{{ supplies a fixed-point-subset bridge preserving }}"
                f" \\texttt{{{invariant}}} \\text{{ toward }}\\texttt{{{consequence}}}\\text{{ for }} {to_id},"
                " \\text{ then the invariant fixed-point subset route becomes testable.}"
            ),
            "informal": (
                f"Treat {from_id} as a conjectural fixed-point-subset bridge for {to_id}; the move should expose a nonempty compact convex fixed-point subset and show that the commuting family preserves it while preserving `{invariant}`."
            ),
            "validation_protocol": [
                f"Identify the fixed-point subset or commutativity ingredient contributed by {from_id}.",
                f"Check whether `{invariant}` supports a nonempty compact convex fixed-point subset for {to_id}.",
                "Verify that the bridge yields a genuinely invariant fixed-point subset, not just the existence of one fixed point for one map.",
                f"Run kb-deduce on {to_id} and record whether the invariant-subset consequence becomes derivable.",
                f"Run kb-abduce on {to_id} to isolate the remaining family-preservation lemmas after adding {from_id}.",
            ],
            "falsifier": (
                f"Reject bridge {from_id}->{to_id} if no invariant fixed-point subset is produced, if `{invariant}` fails, or if the move yields no subset-specific deductive gain."
            ),
        }
    if family == "finite-intersection-bridge":
        return {
            "template_family": family,
            "hypothesis_latex": (
                f"\\text{{If }} {from_id} \\text{{ supplies a finite-intersection bridge preserving }}"
                f" \\texttt{{{invariant}}} \\text{{ from }}\\texttt{{{antecedent}}}"
                f" \\text{{ toward }}\\texttt{{{consequence}}}\\text{{ for }} {to_id},"
                " \\text{ then the family-level common fixed-point route becomes testable.}"
            ),
            "informal": (
                f"Treat {from_id} as a conjectural finite-intersection bridge for {to_id}; the move should lift finite common fixed-point data through compactness into the full family consequence `{consequence}` while preserving `{invariant}`."
            ),
            "validation_protocol": [
                f"State the finite-intersection or compactness ingredient contributed by {from_id}.",
                f"Check whether `{invariant}` survives the passage from finite commuting subfamilies to the whole family in {to_id}.",
                "Verify that the bridge uses a genuine compactness or finite-intersection argument, not only a repetition of the theorem conclusion.",
                f"Run kb-deduce on {to_id} and record whether the common-fixed-point consequence becomes derivable.",
                f"Run kb-abduce on {to_id} to isolate the remaining compactness obligations after adding {from_id}.",
            ],
            "falsifier": (
                f"Reject bridge {from_id}->{to_id} if finite-family fixed-point data does not lift to the whole family, if `{invariant}` fails, or if the move yields no compactness-specific deductive gain."
            ),
        }
    if family == "regularity-reconstruction-bridge":
        return {
            "template_family": family,
            "hypothesis_latex": (
                f"\\text{{If }} {from_id} \\text{{ supplies a regularity-reconstruction bridge preserving }}"
                f" \\texttt{{{invariant}}} \\text{{ toward }}\\texttt{{{consequence}}}\\text{{ for }} {to_id},"
                " \\text{ then the compact-open regularity route becomes testable.}"
            ),
            "informal": (
                f"Treat {from_id} as a conjectural regularity-reconstruction bridge for {to_id}; the move should reconstruct inner/outer regularity and uniqueness through compact-open approximation while preserving `{invariant}`."
            ),
            "validation_protocol": [
                f"Identify the compact-open approximation or separation ingredient contributed by {from_id}.",
                f"Check whether `{invariant}` supports inner/outer regularity or uniqueness for the representing measure in {to_id}.",
                "Verify that the bridge uses genuine topological regularity and not only a restatement of the theorem conclusion.",
                f"Run kb-deduce on {to_id} and record whether regularity or uniqueness obligations are discharged.",
                f"Run kb-abduce on {to_id} to isolate the remaining approximation lemmas after adding {from_id}.",
            ],
            "falsifier": (
                f"Reject bridge {from_id}->{to_id} if compact-open arguments do not sharpen regularity or uniqueness, if `{invariant}` fails, or if no regularity-specific deductive gain appears."
            ),
        }
    if family == "integration-duality-bridge":
        return {
            "template_family": family,
            "hypothesis_latex": (
                f"\\text{{If }} {from_id} \\text{{ supplies an integration-duality bridge preserving }}"
                f" \\texttt{{{invariant}}} \\text{{ from }}\\texttt{{{antecedent}}}"
                f" \\text{{ toward }}\\texttt{{{consequence}}}\\text{{ for }} {to_id},"
                " \\text{ then the measure-to-functional duality route becomes testable.}"
            ),
            "informal": (
                f"Treat {from_id} as a conjectural integration-duality bridge for {to_id}; the move should convert a regular measure into an integral representation or signed-dual statement while preserving `{invariant}` and targeting `{consequence}`."
            ),
            "validation_protocol": [
                f"State the integration or signed-measure ingredient contributed by {from_id}.",
                f"Check whether `{invariant}` survives the passage from measure data to the dual functional statement in {to_id}.",
                "Verify that the bridge yields a genuine continuous linear functional or signed-measure decomposition, not only a formal integral symbol.",
                f"Run kb-deduce on {to_id} and record whether a duality or integration consequence becomes derivable.",
                f"Run kb-abduce on {to_id} to isolate the remaining continuity or variation lemmas after adding {from_id}.",
            ],
            "falsifier": (
                f"Reject bridge {from_id}->{to_id} if the integral pairing does not produce the target duality statement, if `{invariant}` fails, or if the move yields no integration-duality-specific gain."
            ),
        }
    if family == "resolvent-generation-bridge":
        return {
            "template_family": family,
            "hypothesis_latex": (
                f"\\text{{If }} {from_id} \\text{{ supplies a resolvent-generation bridge preserving }}"
                f" \\texttt{{{invariant}}} \\text{{ from }}\\texttt{{{antecedent}}}"
                f" \\text{{ toward }}\\texttt{{{consequence}}}\\text{{ for }} {to_id},"
                " \\text{ then the Hille-Yosida generation route becomes testable.}"
            ),
            "informal": (
                f"Treat {from_id} as a conjectural resolvent-generation bridge for {to_id}; the move should convert resolvent-side control into a generator characterization while preserving `{invariant}` and targeting `{consequence}` under barrier scope `{barrier}`."
            ),
            "validation_protocol": [
                f"State the resolvent estimate or semigroup-generation ingredient contributed by {from_id}.",
                f"Check whether `{invariant}` survives when transporting resolvent-side control toward {to_id}.",
                "Verify that the bridge yields a genuine generation criterion, not only a loose operator-theoretic analogy.",
                f"Run kb-deduce on {to_id} and record whether a generation consequence becomes derivable or conditionally derivable.",
                f"Run kb-abduce on {to_id} to isolate the remaining regularity or approximation lemmas after adding {from_id}.",
            ],
            "falsifier": (
                f"Reject bridge {from_id}->{to_id} if resolvent control cannot be upgraded into a generator statement, if `{invariant}` fails to transfer, or if the move yields no generation-specific deductive gain."
            ),
        }
    if family == "closure-density-bridge":
        return {
            "template_family": family,
            "hypothesis_latex": (
                f"\\text{{If }} {from_id} \\text{{ supplies a closure-density bridge preserving }}"
                f" \\texttt{{{invariant}}} \\text{{ toward }}\\texttt{{{consequence}}}\\text{{ for }} {to_id},"
                " \\text{ then the regularity prerequisite for generation becomes testable.}"
            ),
            "informal": (
                f"Treat {from_id} as a conjectural closure-density bridge for {to_id}; the move should expose closedness and density as a reusable generator regularity interface while preserving `{invariant}`."
            ),
            "validation_protocol": [
                f"Identify the closedness or density ingredient contributed by {from_id}.",
                f"Check whether `{invariant}` yields a closed densely defined operator condition for {to_id}.",
                "Verify that the bridge reduces domain regularity obligations rather than restating them.",
                f"Run kb-deduce on {to_id} and record whether generator-regularity obligations are discharged.",
                f"Run kb-abduce on {to_id} to isolate the remaining resolvent-side conditions after adding {from_id}.",
            ],
            "falsifier": (
                f"Reject bridge {from_id}->{to_id} if closedness and density do not become materially easier to establish, if `{invariant}` fails, or if no regularity-specific deductive gain appears."
            ),
        }
    if family == "yosida-approximation-bridge":
        return {
            "template_family": family,
            "hypothesis_latex": (
                f"\\text{{If }} {from_id} \\text{{ supplies a Yosida-approximation bridge preserving }}"
                f" \\texttt{{{invariant}}} \\text{{ toward }}\\texttt{{{consequence}}}\\text{{ for }} {to_id},"
                " \\text{ then the approximation-based construction route becomes testable.}"
            ),
            "informal": (
                f"Treat {from_id} as a conjectural Yosida-approximation bridge for {to_id}; the move should turn resolvent data into bounded approximants whose limit preserves `{invariant}` and supports `{consequence}`."
            ),
            "validation_protocol": [
                f"State the approximant family contributed by {from_id}.",
                f"Check whether `{invariant}` is preserved under approximation and limiting passage toward {to_id}.",
                "Verify that the bridge yields semigroup construction or convergence evidence, not only a formal approximation schema.",
                f"Run kb-deduce on {to_id} and record whether an approximation-driven proof path becomes derivable.",
                f"Run kb-abduce on {to_id} to isolate the remaining convergence lemmas after adding {from_id}.",
            ],
            "falsifier": (
                f"Reject bridge {from_id}->{to_id} if approximants do not converge in a way that supports generation, if `{invariant}` fails under the limit, or if no approximation-specific gain appears."
            ),
        }
    if family == "contraction-specialization-bridge":
        return {
            "template_family": family,
            "hypothesis_latex": (
                f"\\text{{If }} {from_id} \\text{{ supplies a contraction-specialization bridge preserving }}"
                f" \\texttt{{{invariant}}} \\text{{ toward }}\\texttt{{{consequence}}}\\text{{ for }} {to_id},"
                " \\text{ then the contraction-semigroup route becomes testable.}"
            ),
            "informal": (
                f"Treat {from_id} as a conjectural contraction-specialization bridge for {to_id}; the move should reduce high-order resolvent structure to the contraction case while preserving `{invariant}` and supporting `{consequence}`."
            ),
            "validation_protocol": [
                f"Identify the contraction-specific resolvent ingredient contributed by {from_id}.",
                f"Check whether `{invariant}` survives the specialization to the contraction regime.",
                "Verify that the bridge yields a genuine contraction-generation criterion rather than a restatement of the general theorem.",
                f"Run kb-deduce on {to_id} and record whether a contraction proof route becomes derivable.",
                f"Run kb-abduce on {to_id} to isolate remaining dissipativity or range lemmas after adding {from_id}.",
            ],
            "falsifier": (
                f"Reject bridge {from_id}->{to_id} if contraction specialization does not simplify the theorem, if `{invariant}` fails, or if the move yields no contraction-specific deductive gain."
            ),
        }
    if family == "dissipativity-bridge":
        return {
            "template_family": family,
            "hypothesis_latex": (
                f"\\text{{If }} {from_id} \\text{{ supplies a dissipativity bridge preserving }}"
                f" \\texttt{{{invariant}}} \\text{{ toward }}\\texttt{{{consequence}}}\\text{{ for }} {to_id},"
                " \\text{ then the Lumer-Phillips route becomes testable.}"
            ),
            "informal": (
                f"Treat {from_id} as a conjectural dissipativity bridge for {to_id}; the move should convert operator dissipativity and a range condition into contraction-generation control while preserving `{invariant}`."
            ),
            "validation_protocol": [
                f"State the dissipativity and range-surjectivity ingredient contributed by {from_id}.",
                f"Check whether `{invariant}` supports a contraction-generation step toward {to_id}.",
                "Verify that the bridge yields a Lumer-Phillips-style criterion rather than a generic operator comparison.",
                f"Run kb-deduce on {to_id} and record whether a dissipativity route becomes derivable.",
                f"Run kb-abduce on {to_id} to isolate remaining semigroup or resolvent lemmas after adding {from_id}.",
            ],
            "falsifier": (
                f"Reject bridge {from_id}->{to_id} if dissipativity and surjectivity do not improve generation control, if `{invariant}` fails, or if no dissipativity-specific deductive gain appears."
            ),
        }
    if family == "cauchy-problem-bridge":
        return {
            "template_family": family,
            "hypothesis_latex": (
                f"\\text{{If }} {from_id} \\text{{ supplies a Cauchy-problem bridge preserving }}"
                f" \\texttt{{{invariant}}} \\text{{ toward }}\\texttt{{{consequence}}}\\text{{ for }} {to_id},"
                " \\text{ then the evolution-equivalence route becomes testable.}"
            ),
            "informal": (
                f"Treat {from_id} as a conjectural Cauchy-problem bridge for {to_id}; the move should translate generator information into well-posed evolution semantics while preserving `{invariant}`."
            ),
            "validation_protocol": [
                f"State the semigroup or generator ingredient contributed by {from_id}.",
                f"Check whether `{invariant}` survives the passage from operator data to Cauchy-problem well-posedness.",
                "Verify that the bridge yields unique mild-solution control, not only an analogy with evolution equations.",
                f"Run kb-deduce on {to_id} and record whether a well-posedness consequence becomes derivable.",
                f"Run kb-abduce on {to_id} to isolate the remaining semigroup or regularity lemmas after adding {from_id}.",
            ],
            "falsifier": (
                f"Reject bridge {from_id}->{to_id} if no genuine well-posedness consequence follows, if `{invariant}` fails under the semantic translation, or if the move yields no evolution-specific deductive gain."
            ),
        }

    if family == "transfer-matrix-to-gap-bridge":
        return {
            "template_family": family,
            "hypothesis_latex": (
                f"\\text{{If }} {from_id} \\text{{ supplies a transfer-matrix-to-gap bridge preserving }}"
                f" \\texttt{{{invariant}}} \\text{{ from }}\\texttt{{{antecedent}}}"
                f" \\text{{ toward }}\\texttt{{{consequence}}}\\text{{ for }} {to_id},"
                " \\text{ then the transfer-matrix-to-Hamiltonian mass-gap route becomes testable.}"
            ),
            "informal": (
                f"Treat {from_id} as a conjectural transfer-matrix-to-gap bridge for {to_id}; the move should transport reflection-positivity or transfer-matrix control into a Hamiltonian mass-gap witness while preserving `{invariant}` and targeting `{consequence}` under barrier scope `{barrier}`."
            ),
            "validation_protocol": [
                f"Identify the reflection-positivity or transfer-matrix ingredient contributed by {from_id}.",
                f"Check whether `{invariant}` survives the passage from transfer-matrix control to a Hamiltonian mass-gap claim in {to_id}.",
                "Verify that the bridge yields a positive self-adjoint transfer operator or Hamiltonian witness, not only qualitative spectral language.",
                f"Run kb-deduce on {to_id} and record whether a Hamiltonian mass-gap consequence becomes derivable or conditionally derivable.",
                f"Run kb-abduce on {to_id} to isolate the remaining spectral lemmas after adding {from_id}.",
            ],
            "falsifier": (
                f"Reject bridge {from_id}->{to_id} if transfer-matrix control cannot be converted into a Hamiltonian mass-gap witness, if `{invariant}` fails to transfer, or if the move yields no transfer-matrix-specific deductive gain."
            ),
        }
    if family == "correlator-decay-to-gap-bridge":
        return {
            "template_family": family,
            "hypothesis_latex": (
                f"\\text{{If }} {from_id} \\text{{ supplies a correlator-decay-to-gap bridge preserving }}"
                f" \\texttt{{{invariant}}} \\text{{ from }}\\texttt{{{antecedent}}}"
                f" \\text{{ toward }}\\texttt{{{consequence}}}\\text{{ for }} {to_id},"
                " \\text{ then the Euclidean-decay-to-mass-gap route becomes testable.}"
            ),
            "informal": (
                f"Treat {from_id} as a conjectural correlator-decay-to-gap bridge for {to_id}; the move should convert Euclidean correlator decay into a mass-gap witness while preserving `{invariant}` and targeting `{consequence}` under barrier scope `{barrier}`."
            ),
            "validation_protocol": [
                f"Identify the correlator-decay or Schwinger-function decay ingredient contributed by {from_id}.",
                f"Check whether `{invariant}` remains visible when turning decay estimates into a positive mass-gap claim for {to_id}.",
                "Verify that the bridge yields a quantitative mass-gap witness rather than only qualitative decay language.",
                f"Run kb-deduce on {to_id} and record whether a mass-gap consequence becomes derivable or conditionally derivable.",
                f"Run kb-abduce on {to_id} to isolate the remaining spectral or reconstruction lemmas after adding {from_id}.",
            ],
            "falsifier": (
                f"Reject bridge {from_id}->{to_id} if correlator decay cannot be upgraded into a genuine mass-gap witness, if `{invariant}` fails to transfer, or if the move yields no correlator-decay-specific deductive gain."
            ),
        }
    if family == "os-to-wightman-to-gap-bridge":
        return {
            "template_family": family,
            "hypothesis_latex": (
                f"\\text{{If }} {from_id} \\text{{ supplies an OS-to-Wightman-to-gap bridge preserving }}"
                f" \\texttt{{{invariant}}} \\text{{ from }}\\texttt{{{antecedent}}}"
                f" \\text{{ toward }}\\texttt{{{consequence}}}\\text{{ for }} {to_id},"
                " \\text{ then the reconstruction-plus-spectrum route to a mass gap becomes testable.}"
            ),
            "informal": (
                f"Treat {from_id} as a conjectural OS-to-Wightman-to-gap bridge for {to_id}; the move should reconstruct Wightman/Hamiltonian data from OS-positive Euclidean input and then transfer that control into a mass-gap witness while preserving `{invariant}` under barrier scope `{barrier}`."
            ),
            "validation_protocol": [
                f"State the OS, reflection-positivity, and reconstruction hypotheses contributed by {from_id}.",
                f"Check whether `{invariant}` survives both the Euclidean-to-Wightman transfer and the subsequent mass-gap step toward {to_id}.",
                "Verify that the bridge yields a positive self-adjoint Hamiltonian or equivalent Wightman-side spectral witness supporting a genuine mass gap.",
                f"Run kb-deduce on {to_id} and classify whether the reconstruction-plus-gap route becomes theorem-backed.",
                f"Run kb-abduce on {to_id} to identify remaining Euclidean or spectral premises after adding {from_id}.",
            ],
            "falsifier": (
                f"Reject bridge {from_id}->{to_id} if OS data fail to produce a Wightman/Hamiltonian witness, if `{invariant}` is lost across the two-step transfer, or if the move stays purely formal."
            ),
        }
    if family == "continuum-limit-bridge":
        return {
            "template_family": family,
            "hypothesis_latex": (
                f"\\text{{If }} {from_id} \\text{{ supplies a continuum-limit bridge preserving }}"
                f" \\texttt{{{invariant}}} \\text{{ while lifting }}\\texttt{{{antecedent}}}"
                f" \\text{{ toward }}\\texttt{{{consequence}}}\\text{{ for }} {to_id},"
                " \\text{ then the lattice-to-continuum proof route becomes testable.}"
            ),
            "informal": (
                f"Treat {from_id} as a conjectural continuum-limit bridge for {to_id}; the move should carry cutoff or lattice control into the continuum regime, preserve `{invariant}`, and support the consequence `{consequence}` under barrier scope `{barrier}`."
            ),
            "validation_protocol": [
                f"State the regularized or lattice regime in {from_id} and the continuum target regime in {to_id}.",
                f"Check whether renormalization, cutoff-removal, or tightness arguments preserve `{invariant}` across the limit map.",
                f"Verify that barrier scope `{barrier}` is reduced rather than reintroduced by the continuum passage.",
                f"Run kb-deduce on {to_id} and record whether continuum-limit obligations become theorem-level rather than heuristic.",
                f"Run kb-abduce on {to_id} to isolate the remaining analytic inputs after adding the continuum bridge {from_id}->{to_id}.",
            ],
            "falsifier": (
                f"Reject bridge {from_id}->{to_id} if no mathematically explicit continuum passage is identified, if `{invariant}` is lost under cutoff removal, or if the barrier scope `{barrier}` remains unresolved."
            ),
        }
    if family == "os-reconstruction-bridge":
        return {
            "template_family": family,
            "hypothesis_latex": (
                f"\\text{{If }} {from_id} \\text{{ realizes an OS-reconstruction bridge preserving }}"
                f" \\texttt{{{invariant}}} \\text{{ from }}\\texttt{{{antecedent}}}"
                f" \\text{{ toward }}\\texttt{{{consequence}}}\\text{{ for }} {to_id},"
                " \\text{ then the Euclidean-to-Wightman proof route becomes conditionally derivable.}"
            ),
            "informal": (
                f"Treat {from_id} as an OS-reconstruction bridge for {to_id}; the move should convert Euclidean data into a Wightman realization, preserve `{invariant}`, and force `{consequence}` while respecting barrier scope `{barrier}`."
            ),
            "validation_protocol": [
                f"State the OS axioms, reflection positivity, and reconstruction hypotheses contributed by {from_id}.",
                f"Check whether analytic continuation or reconstruction preserves `{invariant}` when moving toward {to_id}.",
                "Verify that the bridge produces a positive self-adjoint Hamiltonian or equivalent Wightman-side realization, not only a formal correspondence.",
                f"Run kb-deduce on {to_id} and classify whether the reconstruction step becomes theorem-backed.",
                f"Run kb-abduce on {to_id} to identify remaining Euclidean or spectral premises after adding {from_id}.",
            ],
            "falsifier": (
                f"Reject bridge {from_id}->{to_id} if the OS axioms do not yield a genuine Wightman-side object, if `{invariant}` fails under reconstruction, or if the move stays purely formal."
            ),
        }
    if family == "mass-gap-transfer-bridge":
        return {
            "template_family": family,
            "hypothesis_latex": (
                f"\\text{{If }} {from_id} \\text{{ supplies a mass-gap transfer bridge preserving }}"
                f" \\texttt{{{invariant}}} \\text{{ from }}\\texttt{{{antecedent}}}"
                f" \\text{{ toward }}\\texttt{{{consequence}}}\\text{{ for }} {to_id},"
                " \\text{ then the correlator-to-spectrum proof route becomes testable.}"
            ),
            "informal": (
                f"Treat {from_id} as a conjectural mass-gap transfer bridge for {to_id}; the move should transport transfer-matrix, spectral-gap, or correlator-decay control while preserving `{invariant}` and targeting `{consequence}` under barrier scope `{barrier}`."
            ),
            "validation_protocol": [
                f"Identify the spectral-gap, transfer-matrix, or correlator-decay input contributed by {from_id}.",
                f"Check whether `{invariant}` remains visible when translating between decay statements and Hamiltonian mass-gap consequences in {to_id}.",
                "Verify that the bridge yields a positive-mass-gap witness rather than only qualitative decay language.",
                f"Run kb-deduce on {to_id} and record whether a mass-gap consequence becomes derivable or conditionally derivable.",
                f"Run kb-abduce on {to_id} to isolate the missing spectral or reconstruction lemmas after adding {from_id}.",
            ],
            "falsifier": (
                f"Reject bridge {from_id}->{to_id} if correlator decay cannot be converted into a spectral-gap witness, if `{invariant}` fails to transfer, or if the move yields no mass-gap-specific deductive gain."
            ),
        }
    return {
        "template_family": family,
        "hypothesis_latex": (
            f"\\text{{If }} {from_id} \\text{{ supports antecedent schema }} "
            f"\\texttt{{{antecedent}}} \\text{{ and preserves }} "
            f"\\texttt{{{invariant}}} \\text{{ toward consequence schema }} "
            f"\\texttt{{{consequence}}} \\text{{ for }} {to_id},"
            f" \\text{{ then a proof pathway toward }} {to_id} \\text{{ becomes conditionally derivable.}}"
        ),
        "informal": (
            f"Treat {from_id} as a conjectural support bridge for {to_id}; "
            f"the bridge assumes antecedent schema `{antecedent}`, "
            f"aims at consequence `{consequence}`, preserves "
            f"`{invariant}`, and must respect barrier scope "
            f"`{barrier}`."
        ),
        "validation_protocol": [
            f"Add tentative dependency {to_id} depends_on {from_id} in a scratch KB copy.",
            f"Check whether `{invariant}` is preserved after instantiating {from_id}->{to_id}.",
            f"Verify that the instantiated move remains valid under barrier scope `{barrier}`.",
            f"Run kb-deduce on {to_id} and classify entailed/conditionally-entailed/not-derived.",
            f"Run kb-abduce on {to_id} to identify remaining missing premises after adding {from_id}.",
        ],
        "falsifier": (
            f"If deduction still cannot progress, if `{invariant}` fails,"
            f" or if abduction does not improve coverage for {to_id},"
            f" reject bridge {from_id}->{to_id}."
        ),
    }


def _conceptual_payload(
    candidate: dict[str, Any],
    commitments: dict[str, Any],
    src: str,
    dst: str,
    kind: str,
) -> dict[str, Any]:
    """
    Relevance: Operates within the relational connector layer.
    Concept: Domain-aware rendering of conceptual hypotheses.
    Contribution: Keeps conceptual discovery hypotheses tied to explicit mathematical bridge families.
    """

    family = _bridge_template_family(candidate, commitments)
    invariant = commitments["preserved_invariant"]
    antecedent = commitments["support_antecedent_schema"]
    consequence = commitments["target_consequence_schema"]
    barrier = commitments["barrier_scope"]
    relation = str(candidate.get("relation", "potential-support")).strip().lower() or "potential-support"

    if family in SEMIGROUP_BRIDGE_FAMILIES or family in MEASURE_BRIDGE_FAMILIES or family in FIXED_POINT_BRIDGE_FAMILIES:
        label = family.replace("-bridge", "").replace("-", " ")
        return {
            "template_family": family,
            "hypothesis_latex": (
                f"\\text{{Conceptual move }}({kind})\\text{{ links }}{src}\\text{{ to }}{dst}"
                f" \\text{{ through a {label} interface preserving }}\\texttt{{{invariant}}}."
            ),
            "informal": (
                f"Test {kind} from {src} to {dst} as a {label} move; it should preserve `{invariant}`, lift antecedent `{antecedent}` toward consequence `{consequence}`, and reduce barrier scope `{barrier}`."
            ),
            "validation_protocol": [
                f"Instantiate {kind} assumption connecting {src} -> {dst} in a scratch branch.",
                f"State the mathematical transport mechanism associated with the {label} move explicitly.",
                f"Check whether `{invariant}` is preserved while turning `{antecedent}` into `{consequence}`.",
                "Run kb-deduce and record entailment delta.",
                "Run coherence-eval and retain only if coherence_delta_global is non-negative.",
            ],
            "falsifier": (
                f"Reject if the {label} move remains informal, if `{invariant}` is lost, or if the intended domain-specific consequence does not become more derivable."
            ),
            "relation": relation,
        }

    if family == "transfer-matrix-to-gap-bridge":
        return {
            "template_family": family,
            "hypothesis_latex": (
                f"\\text{{Conceptual move }}({kind})\\text{{ links }}{src}\\text{{ to }}{dst}"
                f" \\text{{ by transporting transfer-matrix control through }}\\texttt{{{invariant}}}."
            ),
            "informal": (
                f"Test {kind} from {src} to {dst} as a transfer-matrix-to-gap bridge; it should preserve `{invariant}`, convert reflection-positivity or transfer-matrix control into a mass-gap witness, and support `{consequence}`."
            ),
            "validation_protocol": [
                f"Instantiate {kind} assumption connecting {src} -> {dst} in a scratch branch.",
                "State the transfer-matrix or reflection-positivity ingredient explicitly.",
                f"Check whether `{invariant}` is preserved across the transfer-matrix-to-Hamiltonian passage.",
                "Run kb-deduce and record entailment delta.",
                "Run coherence-eval and retain only if coherence_delta_global is non-negative.",
            ],
            "falsifier": (
                f"Reject if no Hamiltonian gap witness is produced, if `{invariant}` is lost, or if the move yields no transfer-matrix-specific entailment gain."
            ),
            "relation": relation,
        }
    if family == "correlator-decay-to-gap-bridge":
        return {
            "template_family": family,
            "hypothesis_latex": (
                f"\\text{{Conceptual move }}({kind})\\text{{ links }}{src}\\text{{ to }}{dst}"
                f" \\text{{ by upgrading correlator decay through }}\\texttt{{{invariant}}}."
            ),
            "informal": (
                f"Test {kind} from {src} to {dst} as a correlator-decay-to-gap bridge; it should preserve `{invariant}`, convert Euclidean decay control into a mass-gap witness, and support `{consequence}`."
            ),
            "validation_protocol": [
                f"Instantiate {kind} assumption connecting {src} -> {dst} in a scratch branch.",
                "State the correlator-decay ingredient explicitly.",
                f"Check whether `{invariant}` survives the decay-to-gap transfer.",
                "Run kb-deduce and record entailment delta.",
                "Run coherence-eval and retain only if coherence_delta_global is non-negative.",
            ],
            "falsifier": (
                f"Reject if correlator decay cannot be upgraded into a mass-gap witness, if `{invariant}` is lost, or if the move yields no correlator-decay-specific entailment gain."
            ),
            "relation": relation,
        }
    if family == "os-to-wightman-to-gap-bridge":
        return {
            "template_family": family,
            "hypothesis_latex": (
                f"\\text{{Conceptual move }}({kind})\\text{{ links }}{src}\\text{{ to }}{dst}"
                f" \\text{{ through OS-to-Wightman transfer preserving }}\\texttt{{{invariant}}}."
            ),
            "informal": (
                f"Test {kind} from {src} to {dst} as an OS-to-Wightman-to-gap bridge; it should preserve `{invariant}`, convert Euclidean OS data into Wightman/Hamiltonian structure, and then support `{consequence}` as a mass-gap route."
            ),
            "validation_protocol": [
                f"Instantiate {kind} assumption connecting {src} -> {dst} in a scratch branch.",
                "State the OS, reconstruction, and spectral-transfer ingredients explicitly.",
                f"Check whether `{invariant}` is preserved across both the Euclidean-to-Wightman step and the gap-transfer step.",
                "Run kb-deduce and record entailment delta.",
                "Run coherence-eval and retain only if coherence_delta_global is non-negative.",
            ],
            "falsifier": (
                f"Reject if the move stays purely reconstructive without yielding a gap witness, if `{invariant}` fails across the two-step transfer, or if the intended mass-gap consequence remains absent."
            ),
            "relation": relation,
        }
    if family == "continuum-limit-bridge":
        return {
            "template_family": family,
            "hypothesis_latex": (
                f"\\text{{Conceptual move }}({kind})\\text{{ treats }}{src}\\text{{ as a continuum-limit bridge toward }}{dst}"
                f" \\text{{ by preserving }}\\texttt{{{invariant}}}\\text{{ across cutoff removal.}}"
            ),
            "informal": (
                f"Test {kind} from {src} to {dst} as a continuum-limit bridge; it should preserve `{invariant}`, convert regularized control into continuum control, and expose what survives barrier scope `{barrier}`."
            ),
            "validation_protocol": [
                f"Instantiate {kind} assumption connecting {src} -> {dst} in a scratch branch.",
                f"Specify the limit object and prove that `{invariant}` survives the passage.",
                f"Check whether barrier scope `{barrier}` is reduced by the re-expression.",
                "Run kb-deduce and record entailment delta.",
                "Run coherence-eval and retain only if coherence_delta_global is non-negative.",
            ],
            "falsifier": (
                f"Reject if no explicit continuum object is produced, if `{invariant}` fails under cutoff removal, or if barrier scope `{barrier}` remains untouched."
            ),
            "relation": relation,
        }
    if family == "os-reconstruction-bridge":
        return {
            "template_family": family,
            "hypothesis_latex": (
                f"\\text{{Conceptual move }}({kind})\\text{{ links }}{src}\\text{{ to }}{dst}"
                f" \\text{{ through an OS-reconstruction interface preserving }}\\texttt{{{invariant}}}."
            ),
            "informal": (
                f"Test {kind} from {src} to {dst} as an OS-reconstruction bridge; it should preserve `{invariant}`, turn Euclidean data into Wightman-side structure, and support `{consequence}`."
            ),
            "validation_protocol": [
                f"Instantiate {kind} assumption connecting {src} -> {dst} in a scratch branch.",
                "State the OS, reflection-positivity, and analytic-continuation ingredients explicitly.",
                f"Check whether `{invariant}` is preserved across the Euclidean-to-Wightman transfer.",
                "Run kb-deduce and record entailment delta.",
                "Run coherence-eval and retain only if coherence_delta_global is non-negative.",
            ],
            "falsifier": (
                f"Reject if the move yields only formal correspondence, if `{invariant}` fails under reconstruction, or if the intended Wightman-side consequence is still absent."
            ),
            "relation": relation,
        }
    if family == "mass-gap-transfer-bridge":
        return {
            "template_family": family,
            "hypothesis_latex": (
                f"\\text{{Conceptual move }}({kind})\\text{{ links }}{src}\\text{{ to }}{dst}"
                f" \\text{{ by transferring a mass-gap witness preserving }}\\texttt{{{invariant}}}."
            ),
            "informal": (
                f"Test {kind} from {src} to {dst} as a mass-gap transfer bridge; it should preserve `{invariant}`, transport spectral or correlator-decay control, and move toward `{consequence}` under barrier scope `{barrier}`."
            ),
            "validation_protocol": [
                f"Instantiate {kind} assumption connecting {src} -> {dst} in a scratch branch.",
                "State the transfer-matrix, spectral-gap, or correlator-decay ingredient explicitly.",
                f"Check whether `{invariant}` survives the decay-to-spectrum transfer.",
                "Run kb-deduce and record entailment delta.",
                "Run coherence-eval and retain only if coherence_delta_global is non-negative.",
            ],
            "falsifier": (
                f"Reject if no mass-gap witness is transported, if `{invariant}` is lost, or if the move yields no mass-gap-specific entailment gain."
            ),
            "relation": relation,
        }
    return {
        "template_family": family,
        "hypothesis_latex": (
            f"\\text{{Conceptual move }}({kind})\\text{{ links }}{src}\\text{{ to }}{dst}"
            f" \\text{{ by preserving }}\\texttt{{{invariant}}}"
            f" \\text{{ toward }}\\texttt{{{consequence}}}."
        ),
        "informal": (
            f"Test {kind} from {src} to {dst}; it should preserve "
            f"`{invariant}`, support antecedent "
            f"`{antecedent}`, and move toward "
            f"`{consequence}` under barrier scope "
            f"`{barrier}`."
        ),
        "validation_protocol": [
            f"Instantiate {kind} assumption connecting {src} -> {dst} in a scratch branch.",
            f"State the preserved invariant `{invariant}` explicitly and test it on both sides.",
            f"Check whether barrier scope `{barrier}` blocks or constrains the conceptual move.",
            "Run kb-deduce and record entailment delta.",
            "Run coherence-eval and retain only if coherence_delta_global is non-negative.",
        ],
        "falsifier": (
            f"Reject if `{invariant}` cannot be maintained, if barrier scope "
            f"`{barrier}` blocks the move, or if the move yields no entailment gain "
            "or introduces negative global coherence delta."
        ),
        "relation": relation,
    }


def build_hypotheses(
    analysis: dict[str, Any],
    statement_map: dict[str, dict[str, Any]],
    kb_slug: str,
    top_links: int,
    top_interventions: int,
    top_conceptual: int,
) -> list[dict[str, Any]]:
    """
    Relevance: Operates within the relational connector layer.
    Concept: Primary callable implementing a stage-level behavior.
    Contribution: Contributes a deterministic transformation that supports end-to-end reasoning reproducibility.
    """

    top_intervention_ids = {
        item.get("statement_id")
        for item in analysis.get("top_interventions", [])[: max(0, top_interventions)]
        if isinstance(item, dict)
    }

    hypotheses: list[dict[str, Any]] = []
    counter = 1

    for candidate in analysis.get("connection_candidates", [])[: max(0, top_links)]:
        if not isinstance(candidate, dict):
            continue
        from_id = str(candidate.get("from_id", "")).strip()
        to_id = str(candidate.get("to_id", "")).strip()
        if not from_id or not to_id:
            continue

        source_stmt = statement_map.get(from_id, {})
        target_stmt = statement_map.get(to_id, {})
        base_score = float(candidate.get("score", 0.0) or 0.0)
        anchor_bonus = 0.10 if (from_id in top_intervention_ids or to_id in top_intervention_ids) else 0.0
        priority = _clamp01(0.9 * base_score + anchor_bonus)

        evidence_terms = [str(x) for x in candidate.get("evidence_terms", []) if str(x).strip()]
        relation = str(candidate.get("relation", "potential-support"))
        commitments = _inferential_commitments(candidate)
        payload = _bridge_link_payload(candidate, commitments, from_id, to_id)

        hypotheses.append(
            {
                "id": f"phyp.{kb_slug}.{counter:03d}",
                "kind": "bridge-link",
                "status": "tentative",
                "priority": round(priority, 4),
                "target_statement_id": to_id,
                "support_statement_id": from_id,
                "relation": relation,
                "template_family": payload["template_family"],
                "hypothesis_latex": payload["hypothesis_latex"],
                "informal": payload["informal"],
                "source_context": {
                    "support_kind": str(source_stmt.get("kind", "unknown")),
                    "target_kind": str(target_stmt.get("kind", "unknown")),
                    "support_preview": _short_text(source_stmt.get("informal") or source_stmt.get("latex")),
                    "target_preview": _short_text(target_stmt.get("informal") or target_stmt.get("latex")),
                },
                "evidence_terms": evidence_terms,
                "support_antecedent_schema": commitments["support_antecedent_schema"],
                "target_consequence_schema": commitments["target_consequence_schema"],
                "preserved_invariant": commitments["preserved_invariant"],
                "invariant_basis": commitments["invariant_basis"],
                "barrier_scope": commitments["barrier_scope"],
                "validation_protocol": payload["validation_protocol"],
                "falsifier": payload["falsifier"],
                "provenance": {
                    "analysis_score": round(base_score, 4),
                    "similarity": round(float(candidate.get("similarity", 0.0) or 0.0), 4),
                    "component_gain": round(float(candidate.get("component_gain", 0.0) or 0.0), 4),
                },
            }
        )
        counter += 1

    for item in analysis.get("top_interventions", [])[: max(0, top_interventions)]:
        if not isinstance(item, dict):
            continue
        sid = str(item.get("statement_id", "")).strip()
        if not sid:
            continue
        stmt = statement_map.get(sid, {})
        metrics = item.get("metrics", {}) if isinstance(item.get("metrics"), dict) else {}
        priority = _clamp01(float(item.get("score", 0.0) or 0.0) + 0.15)

        partner = item.get("best_cross_component_partner")
        partner_text = f" with bridge candidate {partner}" if partner else ""

        hypotheses.append(
            {
                "id": f"phyp.{kb_slug}.{counter:03d}",
                "kind": "intervention-focus",
                "status": "tentative",
                "priority": round(priority, 4),
                "target_statement_id": sid,
                "hypothesis_latex": (
                    f"\\text{{Focusing abductive search on }} {sid}{partner_text}"
                    " \\text{ will maximize proof-payoff in the next loop round.}"
                ),
                "informal": (
                    f"Prioritize abductive effort on {sid}{partner_text}; this is expected to yield"
                    " high-value proof progress compared with lower-ranked targets."
                ),
                "source_context": {
                    "target_kind": str(stmt.get("kind", "unknown")),
                    "target_preview": _short_text(stmt.get("informal") or stmt.get("latex")),
                    "section": str(item.get("section", "Unspecified")),
                },
                "metrics": {
                    "downstream_impact": int(metrics.get("downstream_impact", 0) or 0),
                    "upstream_support": int(metrics.get("upstream_support", 0) or 0),
                    "betweenness": float(metrics.get("betweenness", 0.0) or 0.0),
                    "unresolved_dependencies": int(metrics.get("unresolved_dependencies", 0) or 0),
                    "cross_component_potential": float(metrics.get("cross_component_potential", 0.0) or 0.0),
                },
                "validation_protocol": [
                    f"Run kb-abduce with target {sid} and collect top 3 minimal hypothesis sets.",
                    "Score hypotheses by coverage, compatibility, and simplicity.",
                    "Run kb-deduce on retained sets and keep only those that increase derivable consequences.",
                ],
                "falsifier": (
                    "If the target produces no improved deductive yield after one loop round, "
                    "demote its priority in the next iteration."
                ),
                "rationale": str(item.get("rationale", "")),
            }
        )
        counter += 1

    conceptual_added = 0
    for candidate in analysis.get("connection_candidates", []):
        if conceptual_added >= max(0, top_conceptual):
            break
        if not isinstance(candidate, dict):
            continue
        src = str(candidate.get("from_id", "")).strip()
        dst = str(candidate.get("to_id", "")).strip()
        if not src or not dst:
            continue
        src_stmt = statement_map.get(src, {})
        dst_stmt = statement_map.get(dst, {})
        src_kind = str(src_stmt.get("kind", ""))
        dst_kind = str(dst_stmt.get("kind", ""))
        relation = str(candidate.get("relation", "potential-support")).strip().lower()
        base_score = float(candidate.get("score", 0.0) or 0.0)
        evidence_terms = [str(x) for x in candidate.get("evidence_terms", []) if str(x).strip()]
        commitments = _inferential_commitments(candidate)
        template_family = _bridge_template_family(candidate, commitments)

        if template_family in {"os-reconstruction-bridge", "os-to-wightman-to-gap-bridge"}:
            kind = "representation-shift"
        elif template_family == "cauchy-problem-bridge":
            kind = "representation-shift"
        elif template_family == "continuum-limit-bridge":
            kind = "barrier-escape-principle"
        elif template_family == "closure-density-bridge":
            kind = "barrier-escape-principle"
        elif template_family in MASS_GAP_BRIDGE_FAMILIES:
            kind = "intermediate-invariant"
        elif template_family in {
            "resolvent-generation-bridge",
            "yosida-approximation-bridge",
            "contraction-specialization-bridge",
            "dissipativity-bridge",
        }:
            kind = "intermediate-invariant"
        elif relation in {"potential-equivalence", "definitional-expansion"} or _contains_token(src, dst, relation):
            if src_kind == "definition":
                kind = "definition-introduction"
            elif relation in {"potential-equivalence", "definitional-expansion"}:
                kind = "normal-form-reduction"
            else:
                kind = "representation-shift"
        elif relation in {"method-transfer", "analogy-transfer"}:
            kind = "analogy-transfer"
        elif commitments["barrier_scope"] != "none" or _contains_token(src, dst, "barrier"):
            kind = "barrier-escape-principle"
        else:
            kind = "intermediate-invariant"

        conceptual_added += 1
        priority = _clamp01(0.82 * base_score + 0.12)
        payload = _conceptual_payload(candidate, commitments, src, dst, kind)
        hypotheses.append(
            {
                "id": f"phyp.{kb_slug}.{counter:03d}",
                "kind": kind,
                "status": "tentative",
                "priority": round(priority, 4),
                "target_statement_id": dst,
                "support_statement_id": src,
                "relation": payload["relation"],
                "template_family": payload["template_family"],
                "hypothesis_latex": payload["hypothesis_latex"],
                "informal": payload["informal"],
                "source_context": {
                    "support_kind": src_kind or "unknown",
                    "target_kind": dst_kind or "unknown",
                    "support_preview": _short_text(src_stmt.get("informal") or src_stmt.get("latex")),
                    "target_preview": _short_text(dst_stmt.get("informal") or dst_stmt.get("latex")),
                },
                "evidence_terms": evidence_terms[:8],
                "support_antecedent_schema": commitments["support_antecedent_schema"],
                "target_consequence_schema": commitments["target_consequence_schema"],
                "preserved_invariant": commitments["preserved_invariant"],
                "invariant_basis": commitments["invariant_basis"],
                "barrier_scope": commitments["barrier_scope"],
                "validation_protocol": payload["validation_protocol"],
                "falsifier": payload["falsifier"],
                "provenance": {
                    "analysis_score": round(base_score, 4),
                    "similarity": round(float(candidate.get("similarity", 0.0) or 0.0), 4),
                    "component_gain": round(float(candidate.get("component_gain", 0.0) or 0.0), 4),
                },
            }
        )
        counter += 1

    hypotheses.sort(key=lambda h: float(h.get("priority", 0.0)), reverse=True)
    return hypotheses


def main() -> int:
    """
    Relevance: Operates within the relational connector layer.
    Concept: CLI entrypoint orchestration for this script.
    Contribution: Binds parsing, computation, and artifact emission into a reproducible script execution.
    """

    logger = ReasoningLogger("kb-proof-connector")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--analysis", required=True, help="Path to connection-analysis JSON.")
    parser.add_argument("--kb", required=True, help="Path to KB markdown file.")
    parser.add_argument("--output", required=True, help="Output YAML path under phyp/.")
    parser.add_argument("--top-links", type=int, default=20, help="Number of bridge-link hypotheses.")
    parser.add_argument(
        "--top-interventions",
        type=int,
        default=10,
        help="Number of intervention-focus hypotheses.",
    )
    parser.add_argument(
        "--top-conceptual",
        type=int,
        default=12,
        help="Number of conceptual-discovery hypotheses to generate.",
    )
    args = parser.parse_args()
    logger.step(
        "Parsed proof-hypothesis arguments",
        "\n".join(
            [
                f"analysis={args.analysis}",
                f"kb={args.kb}",
                f"output={args.output}",
                f"top_links={args.top_links}",
                f"top_interventions={args.top_interventions}",
                f"top_conceptual={args.top_conceptual}",
            ]
        ),
    )

    analysis_path = Path(args.analysis)
    kb_path = Path(args.kb)
    output_path = Path(args.output)

    if not analysis_path.exists():
        log_path = logger.finalize("error", summary=f"Analysis file not found: {analysis_path}")
        print(f"[LOG] {log_path}", file=sys.stderr)
        raise SystemExit(f"[ERROR] Analysis file not found: {analysis_path}")
    if not kb_path.exists():
        log_path = logger.finalize("error", summary=f"KB file not found: {kb_path}")
        print(f"[LOG] {log_path}", file=sys.stderr)
        raise SystemExit(f"[ERROR] KB file not found: {kb_path}")

    analysis = yaml.safe_load(analysis_path.read_text(encoding="utf-8"))
    if not isinstance(analysis, dict):
        log_path = logger.finalize("error", summary="Analysis content must be a JSON/YAML object.")
        print(f"[LOG] {log_path}", file=sys.stderr)
        raise SystemExit("[ERROR] Analysis content must be a JSON/YAML object.")

    statement_map = _load_yaml_blocks(kb_path)
    kb_slug = _derive_kb_slug(kb_path)

    hypotheses = build_hypotheses(
        analysis=analysis,
        statement_map=statement_map,
        kb_slug=kb_slug,
        top_links=max(0, args.top_links),
        top_interventions=max(0, args.top_interventions),
        top_conceptual=max(0, args.top_conceptual),
    )

    payload = {
        "metadata": {
            "kb": str(kb_path),
            "analysis": str(analysis_path),
            "generated_utc": dt.datetime.now(dt.UTC).isoformat(),
            "hypothesis_count": len(hypotheses),
            "top_links": max(0, args.top_links),
            "top_interventions": max(0, args.top_interventions),
            "top_conceptual": max(0, args.top_conceptual),
        },
        "hypotheses": hypotheses,
    }
    logger.step(
        "Inferential commitments in generated hypotheses",
        "\n".join(
            [
                f"{str(item.get('id', '')).strip()}:{str(item.get('kind', '')).strip()}:"
                f"{str(item.get('support_antecedent_schema', '')).strip()}=>"
                f"{str(item.get('target_consequence_schema', '')).strip()}:"
                f"invariant={str(item.get('preserved_invariant', '')).strip()}:"
                f"barrier={str(item.get('barrier_scope', '')).strip()}"
                for item in hypotheses[:8]
                if isinstance(item, dict)
            ]
        ),
    )

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        yaml.safe_dump(payload, sort_keys=False, allow_unicode=False, width=1000),
        encoding="utf-8",
    )
    logger.add_output("proof_hypotheses_yaml", output_path)

    print(f"[OK] Wrote proof hypotheses: {output_path}")
    print(f"[OK] Hypothesis count: {len(hypotheses)}")
    log_path = logger.finalize(
        "success",
        summary=f"Generated {len(hypotheses)} proof hypotheses for KB slug {kb_slug}.",
    )
    print(f"[LOG] {log_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
