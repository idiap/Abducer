# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
# 
# SPDX-License-Identifier: MIT

"""Analyze a KB as a relational proof graph and rank intervention points.

The script reads fenced YAML statement blocks from a KB markdown file, builds a
directed dependency graph (`depends_on`), and returns:
- high-information intervention points
- high-value cross-component connection candidates
- a staged abductive loop plan
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter, deque
from pathlib import Path
from typing import Any

import yaml

_COMMON_DIR = Path(__file__).resolve().parents[3] / "common"
if str(_COMMON_DIR) not in sys.path:
    sys.path.insert(0, str(_COMMON_DIR))

from reasoning_log import ReasoningLogger

STATEMENT_BLOCK_PATTERN = re.compile(r"```yaml\n(.*?)\n```", re.DOTALL)
HEADING_PATTERN = re.compile(r"(?m)^#\s+(.+?)\s*$")
TOKEN_PATTERN = re.compile(r"[A-Za-z][A-Za-z0-9_]*")
ID_TOKEN_PATTERN = re.compile(r"[A-Za-z0-9]+")
LATEX_COMMAND_PATTERN = re.compile(r"\\([A-Za-z]+)")
LATEX_SYMBOL_PATTERN = re.compile(r"(?<![A-Za-z])([A-Za-z](?:_[A-Za-z0-9]+)?)")

STOPWORDS = {
    "a",
    "an",
    "all",
    "as",
    "at",
    "be",
    "by",
    "if",
    "in",
    "is",
    "it",
    "its",
    "not",
    "of",
    "on",
    "or",
    "to",
    "we",
    "the",
    "and",
    "for",
    "with",
    "that",
    "this",
    "from",
    "into",
    "such",
    "then",
    "there",
    "exists",
    "forall",
    "where",
    "have",
    "has",
    "let",
    "iff",
    "left",
    "right",
    "text",
    "mathrm",
    "mathbf",
    "begin",
    "end",
    "proof",
    "show",
    "over",
    "under",
    "true",
    "false",
    "using",
    "given",
    "suppose",
    "assume",
    "thus",
    "hence",
}

PREMISE_KINDS = {"definition", "axiom", "lemma", "theorem"}
TARGET_KINDS = {"theorem", "lemma", "corollary", "conjecture", "observation"}

METHOD_TOKEN_MAP = {
    "derandom": "derandomization",
    "pit": "derandomization",
    "pseudorandom": "derandomization",
    "communication": "communication",
    "lifting": "communication",
    "proof": "proof-complexity",
    "resolution": "proof-complexity",
    "frege": "proof-complexity",
    "algebraic": "algebraic",
    "polynomial": "algebraic",
    "circuit": "circuit-lower-bounds",
    "lower": "circuit-lower-bounds",
    "magnification": "meta-complexity",
    "meta": "meta-complexity",
    "reduction": "reduction",
    "complete": "reduction",
}

CLASS_CONCEPT_MAP = {
    "e": "E",
    "pclass": "P",
    "np": "NP",
    "conp": "coNP",
    "ppoly": "P/poly",
    "bpp": "BPP",
    "ph": "PH",
    "exp": "EXP",
    "nexp": "NEXP",
    "rp": "RP",
    "szk": "SZK",
    "vp": "VP",
    "vnp": "VNP",
    "ntime": "NTIME",
    "dtime": "DTIME",
}

PROBLEM_CONCEPT_MAP = {
    "sat": "SAT",
    "taut": "TAUT",
    "mcsp": "MCSP",
    "gapmcsp": "Gap-MCSP",
    "mktp": "MKTP",
    "pit": "PIT",
    "php": "PHP",
    "clique": "CLIQUE",
    "parity": "PARITY",
    "permanent": "Permanent",
    "circuitsat": "Circuit-SAT",
}

REGIME_CONCEPT_MAP = {
    "circuit": "circuit-complexity",
    "proof": "proof-complexity",
    "resolution": "proof-complexity",
    "frege": "proof-complexity",
    "communication": "communication-complexity",
    "lifting": "communication-complexity",
    "query": "query-complexity",
    "nonuniform": "nonuniform-model",
    "uniform": "uniform-model",
    "derandom": "derandomization",
    "random": "randomness",
    "oracle": "oracle-method",
    "algebraic": "algebraic-method",
    "magnification": "hardness-magnification",
    "meta": "meta-complexity",
    "reduction": "reduction-framework",
    "complete": "completeness-framework",
}

TARGET_CLASS_TAGS = {"P", "NP", "coNP", "P/poly", "PH", "NEXP", "EXP", "E", "BPP", "SZK", "VP", "VNP"}
TARGET_PROBLEM_TAGS = {"SAT", "MCSP", "Gap-MCSP", "PIT", "TAUT", "PHP", "CLIQUE", "PARITY", "Permanent", "Circuit-SAT"}
TARGET_REGIME_TAGS = {
    "circuit-complexity",
    "proof-complexity",
    "communication-complexity",
    "derandomization",
    "hardness-magnification",
    "meta-complexity",
    "reduction-framework",
}
MODEL_SIGNATURE_PRIORITY = [
    "ACC0-circuits",
    "AC0[p]-circuits",
    "AC0-circuits",
    "NC1-circuits",
    "formula-size",
    "monotone-circuits",
    "nonuniform-circuits",
    "arithmetic-circuits",
    "bounded-depth-frege",
    "extended-frege",
    "frege",
    "resolution",
    "IPS",
    "black-box-PIT",
    "oracle-model",
    "extension-oracle",
    "communication-protocol",
    "decision-tree",
    "Cook-Reckhow-proof-system",
    "PRG-construction",
    "PRF-assumption",
]
PROBLEM_SIGNATURE_PRIORITY = ["Gap-MCSP", "MCSP", "PIT", "Circuit-SAT", "SAT", "Permanent", "TAUT", "PHP", "CLIQUE", "PARITY"]
CLASS_SIGNATURE_PRIORITY = ["P", "NP", "coNP", "P/poly", "PH", "BPP", "RP", "E", "EXP", "NEXP", "SZK", "VP", "VNP"]

ONTOLOGY_COMPLEXITY = "computational-complexity"
ONTOLOGY_MATHEMATICAL_PHYSICS = "mathematical-physics"
ONTOLOGY_FUNCTIONAL_ANALYSIS_SEMIGROUP = "functional-analysis-semigroup"
ONTOLOGY_FUNCTIONAL_ANALYSIS_MEASURE = "functional-analysis-measure-representation"
ONTOLOGY_FUNCTIONAL_ANALYSIS_FIXED_POINT = "functional-analysis-convex-fixed-point"
ONTOLOGY_GENERIC_MATHEMATICS = "generic-mathematics"

GENERIC_METHOD_TOKEN_MAP = {
    "algebra": "algebraic-method",
    "analytic": "analytic-method",
    "analysis": "analytic-method",
    "combin": "combinatorial-method",
    "geometr": "geometric-method",
    "topolog": "topological-method",
    "variat": "variational-method",
    "probabil": "probabilistic-method",
}

PHYSICS_METHOD_TOKEN_MAP = {
    "construct": "constructive-qft",
    "wightman": "axiomatic-qft",
    "osterwalder": "axiomatic-qft",
    "schrader": "axiomatic-qft",
    "euclidean": "euclidean-qft",
    "lattice": "lattice-gauge-theory",
    "gauge": "gauge-theory",
    "renormal": "renormalization-group",
    "instanton": "geometric-analysis",
    "selfdual": "geometric-analysis",
    "self_dual": "geometric-analysis",
    "asd": "geometric-analysis",
    "probabil": "probabilistic-method",
    "variat": "variational-method",
    "transfer": "spectral-analysis",
    "reflection": "spectral-analysis",
    "hamiltonian": "spectral-analysis",
    "pde": "classical-pde-analysis",
}

PHYSICS_REGIME_CONCEPT_MAP = {
    "construct": "constructive-qft",
    "axiomatic": "axiomatic-qft",
    "wightman": "axiomatic-qft",
    "osterwalder": "euclidean-qft",
    "schrader": "euclidean-qft",
    "euclidean": "euclidean-qft",
    "lattice": "lattice-gauge-theory",
    "renormal": "renormalization-group",
    "gauge": "gauge-theory",
    "geometr": "geometric-analysis",
    "instanton": "geometric-analysis",
    "probabil": "probabilistic-method",
    "variat": "variational-method",
    "transfer": "spectral-analysis",
    "reflection": "spectral-analysis",
    "hamiltonian": "spectral-analysis",
    "classical": "classical-pde-analysis",
    "minkowski": "classical-pde-analysis",
}

PHYSICS_OBJECT_CONCEPT_MAP = {
    "yang": "Yang-Mills",
    "wightman": "Wightman-QFT",
    "osterwalder": "OS-axioms",
    "schrader": "OS-axioms",
    "lattice": "lattice-gauge-theory",
    "wilson": "Wilson-lattice-gauge-theory",
    "continuum": "continuum-limit",
    "massgap": "mass-gap",
    "instanton": "instanton",
    "bundle": "principal-bundle",
    "connection": "connection",
    "curvature": "curvature",
    "transfer": "transfer-matrix",
    "hamiltonian": "Hamiltonian",
    "correlator": "Schwinger-function",
    "schwinger": "Schwinger-function",
    "vacuum": "vacuum-state",
    "reflection": "reflection-positivity",
    "renormal": "renormalization-group",
}

PHYSICS_TARGET_OBJECT_TAGS = {
    "Yang-Mills",
    "mass-gap",
    "continuum-limit",
    "Wightman-QFT",
    "OS-axioms",
    "lattice-gauge-theory",
    "transfer-matrix",
    "reflection-positivity",
    "renormalization-group",
}

PHYSICS_TARGET_REGIME_TAGS = {
    "constructive-qft",
    "axiomatic-qft",
    "euclidean-qft",
    "lattice-gauge-theory",
    "renormalization-group",
    "geometric-analysis",
    "spectral-analysis",
    "classical-pde-analysis",
}

SEMIGROUP_METHOD_TOKEN_MAP = {
    "semigroup": "semigroup-generation",
    "generator": "generator-analysis",
    "unitary": "unitary-group-analysis",
    "stone": "stone-correspondence",
    "resolvent": "resolvent-estimate",
    "laplace": "laplace-transform",
    "dissipat": "dissipativity",
    "yosida": "yosida-approximation",
    "cauchy": "abstract-cauchy-problem",
    "contraction": "contraction-theory",
    "spectral": "spectral-analysis",
    "functional": "functional-calculus",
    "selfadjoint": "spectral-analysis",
    "self-adjoint": "spectral-analysis",
    "skewadjoint": "spectral-analysis",
    "skew-adjoint": "spectral-analysis",
    "hilbert": "hilbert-space-analysis",
    "dense": "domain-regularity",
    "closed": "domain-regularity",
}

SEMIGROUP_REGIME_CONCEPT_MAP = {
    "semigroup": "semigroup-generation",
    "generator": "generator-analysis",
    "unitary": "unitary-group-analysis",
    "stone": "stone-correspondence",
    "resolvent": "resolvent-estimate",
    "laplace": "laplace-transform",
    "dissipat": "dissipativity",
    "yosida": "yosida-approximation",
    "cauchy": "abstract-cauchy-problem",
    "contraction": "contraction-theory",
    "spectral": "spectral-analysis",
    "functional": "functional-calculus",
    "selfadjoint": "spectral-analysis",
    "self-adjoint": "spectral-analysis",
    "skewadjoint": "spectral-analysis",
    "skew-adjoint": "spectral-analysis",
    "hilbert": "hilbert-space-analysis",
    "dense": "domain-regularity",
    "closed": "domain-regularity",
}

SEMIGROUP_OBJECT_CONCEPT_MAP = {
    "semigroup": "C0-semigroup",
    "c0": "C0-semigroup",
    "generator": "generator",
    "unitary": "unitary-group",
    "stone": "Stone-correspondence",
    "resolvent": "resolvent",
    "cauchy": "abstract-Cauchy-problem",
    "dissipat": "dissipativity",
    "yosida": "Yosida-approximation",
    "contraction": "contraction-semigroup",
    "banach": "Banach-space",
    "hilbert": "Hilbert-space",
    "selfadjoint": "self-adjoint-operator",
    "self-adjoint": "self-adjoint-operator",
    "skewadjoint": "skew-adjoint-operator",
    "skew-adjoint": "skew-adjoint-operator",
    "spectral": "spectral-measure",
    "functional": "functional-calculus",
    "hamiltonian": "Hamiltonian",
    "operator": "unbounded-operator",
}

SEMIGROUP_TARGET_OBJECT_TAGS = {
    "C0-semigroup",
    "generator",
    "unitary-group",
    "Stone-correspondence",
    "resolvent",
    "abstract-Cauchy-problem",
    "Yosida-approximation",
    "contraction-semigroup",
    "dissipativity",
    "Hilbert-space",
    "self-adjoint-operator",
    "spectral-measure",
    "functional-calculus",
    "Hamiltonian",
}

SEMIGROUP_TARGET_REGIME_TAGS = {
    "semigroup-generation",
    "unitary-group-analysis",
    "stone-correspondence",
    "resolvent-estimate",
    "laplace-transform",
    "dissipativity",
    "yosida-approximation",
    "abstract-cauchy-problem",
    "contraction-theory",
    "spectral-analysis",
    "functional-calculus",
    "hilbert-space-analysis",
    "domain-regularity",
}

MEASURE_METHOD_TOKEN_MAP = {
    "riesz": "measure-representation",
    "markov": "measure-representation",
    "kakutani": "measure-representation",
    "measure": "measure-representation",
    "radon": "measure-representation",
    "borel": "measure-representation",
    "regular": "regularity-reconstruction",
    "positive": "positivity-method",
    "functional": "duality-method",
    "dual": "duality-method",
    "integration": "integration-representation",
    "integral": "integration-representation",
    "urysohn": "compact-open-approximation",
    "support": "compact-open-approximation",
    "compact": "compact-open-approximation",
    "locally": "topological-regularity",
    "hausdorff": "topological-regularity",
    "c0": "function-space-duality",
    "signed": "signed-measure-decomposition",
    "variation": "signed-measure-decomposition",
}

MEASURE_REGIME_CONCEPT_MAP = {
    "riesz": "measure-representation",
    "markov": "measure-representation",
    "kakutani": "measure-representation",
    "measure": "measure-representation",
    "radon": "measure-representation",
    "regular": "regularity-reconstruction",
    "positive": "positivity-method",
    "integration": "integration-representation",
    "integral": "integration-representation",
    "urysohn": "compact-open-approximation",
    "support": "compact-open-approximation",
    "compact": "compact-open-approximation",
    "dual": "function-space-duality",
    "functional": "function-space-duality",
    "signed": "signed-measure-decomposition",
    "variation": "signed-measure-decomposition",
    "locally": "topological-regularity",
    "hausdorff": "topological-regularity",
}

MEASURE_OBJECT_CONCEPT_MAP = {
    "riesz": "Riesz-Markov-Kakutani",
    "markov": "Riesz-Markov-Kakutani",
    "kakutani": "Riesz-Markov-Kakutani",
    "measure": "regular-Borel-measure",
    "radon": "Radon-measure",
    "borel": "regular-Borel-measure",
    "functional": "positive-linear-functional",
    "positive": "positive-linear-functional",
    "integration": "integration-pairing",
    "dual": "C0-dual",
    "variation": "total-variation",
    "locally": "locally-compact-Hausdorff-space",
    "hausdorff": "locally-compact-Hausdorff-space",
}

MEASURE_TARGET_OBJECT_TAGS = {
    "Riesz-Markov-Kakutani",
    "regular-Borel-measure",
    "Radon-measure",
    "positive-linear-functional",
    "integration-pairing",
    "C_c-space",
    "C0-dual",
    "total-variation",
    "locally-compact-Hausdorff-space",
}

MEASURE_TARGET_REGIME_TAGS = {
    "measure-representation",
    "regularity-reconstruction",
    "integration-representation",
    "compact-open-approximation",
    "function-space-duality",
    "positivity-method",
    "signed-measure-decomposition",
    "topological-regularity",
}

FIXED_POINT_METHOD_TOKEN_MAP = {
    "markov": "commuting-fixed-point",
    "kakutani": "commuting-fixed-point",
    "fixed": "fixed-point-analysis",
    "affine": "affine-map-analysis",
    "convex": "convex-geometry",
    "compact": "compactness-method",
    "commut": "commuting-family-analysis",
    "average": "affine-averaging",
    "cesaro": "affine-averaging",
    "invariant": "invariant-subset-method",
    "intersection": "finite-intersection-compactness",
    "locally": "topological-vector-space-analysis",
}

FIXED_POINT_REGIME_CONCEPT_MAP = {
    "markov": "commuting-fixed-point",
    "kakutani": "commuting-fixed-point",
    "fixed": "fixed-point-analysis",
    "affine": "affine-map-analysis",
    "convex": "convex-geometry",
    "compact": "compactness-method",
    "commut": "commuting-family-analysis",
    "average": "affine-averaging",
    "cesaro": "affine-averaging",
    "invariant": "invariant-subset-method",
    "intersection": "finite-intersection-compactness",
    "locally": "topological-vector-space-analysis",
}

FIXED_POINT_OBJECT_CONCEPT_MAP = {
    "markov": "Markov-Kakutani",
    "kakutani": "Markov-Kakutani",
    "fixed": "common-fixed-point",
    "affine": "affine-self-map",
    "convex": "compact-convex-set",
    "compact": "compact-convex-set",
    "commut": "commuting-affine-family",
    "average": "Cesaro-averaging",
    "cesaro": "Cesaro-averaging",
    "invariant": "invariant-fixed-point-subset",
    "intersection": "finite-intersection-property",
    "family": "commuting-affine-family",
    "subset": "invariant-fixed-point-subset",
}

FIXED_POINT_TARGET_OBJECT_TAGS = {
    "Markov-Kakutani",
    "common-fixed-point",
    "compact-convex-set",
    "commuting-affine-family",
    "invariant-fixed-point-subset",
    "Cesaro-averaging",
    "finite-intersection-property",
}

FIXED_POINT_TARGET_REGIME_TAGS = {
    "commuting-fixed-point",
    "fixed-point-analysis",
    "affine-map-analysis",
    "convex-geometry",
    "compactness-method",
    "commuting-family-analysis",
    "affine-averaging",
    "invariant-subset-method",
    "finite-intersection-compactness",
    "topological-vector-space-analysis",
}


def _text_forms(raw_text: str) -> tuple[str, str, str]:
    """
    Relevance: Operates within the relational connector layer.
    Concept: Normalization of textual inputs into multiple matching views.
    Contribution: Lets the connector extract theorem schemas and model signatures without relying on brittle token overlap.
    """

    raw = str(raw_text).lower()
    clean = re.sub(r"[^a-z0-9/+\-\[\]^=<>]+", " ", raw).strip()
    compact = re.sub(r"[^a-z0-9]+", "", raw)
    return raw, clean, compact


def _contains_any_pattern(raw: str, clean: str, compact: str, patterns: list[str] | tuple[str, ...]) -> bool:
    """
    Relevance: Operates within the relational connector layer.
    Concept: Pattern-trigger helper for typed mathematical signature extraction.
    Contribution: Centralizes controlled matching so ontology features are derived from normalized structures rather than ad hoc lexical heuristics.
    """

    for pattern in patterns:
        p = str(pattern).strip().lower()
        if not p:
            continue
        if p in raw:
            return True
        p_clean = re.sub(r"[^a-z0-9/+\-\[\]^=<>]+", " ", p).strip()
        if p_clean and p_clean in clean:
            return True
        p_compact = re.sub(r"[^a-z0-9]+", "", p)
        if p_compact and p_compact in compact:
            return True
    return False


def _preferred_value(values: list[str], priority: list[str]) -> str:
    """
    Relevance: Operates within the relational connector layer.
    Concept: Deterministic selection of a representative mathematical object.
    Contribution: Produces stable, human-readable signatures such as `PHP-resolution-lower-bound` instead of unordered concept bags.
    """

    pool = {str(v).strip() for v in values if str(v).strip()}
    for item in priority:
        if item in pool:
            return item
    return sorted(pool)[0] if pool else ""


def _front_matter_metadata(kb_content: str) -> dict[str, Any]:
    """
    Relevance: Operates within the relational connector layer.
    Concept: Extraction of KB-level metadata used to select the reasoning ontology.
    Contribution: Prevents domain-specific signature extraction from defaulting to the P-vs-NP ontology for unrelated KBs.
    """

    lines = kb_content.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}
    yaml_lines: list[str] = []
    for line in lines[1:]:
        if line.strip() == "---":
            break
        yaml_lines.append(line)
    if not yaml_lines:
        return {}
    try:
        payload = yaml.safe_load("\n".join(yaml_lines))
    except yaml.YAMLError:
        return {}
    return payload if isinstance(payload, dict) else {}


def _resolve_ontology_profile(kb_content: str) -> str:
    """
    Relevance: Operates within the relational connector layer.
    Concept: Typed classification used to guide ontology selection.
    Contribution: Routes each KB through a domain-appropriate concept extractor instead of reusing one hard-coded problem ontology.
    """

    meta = _front_matter_metadata(kb_content)
    domain = str(meta.get("domain", "")).strip().lower()
    subdomain = str(meta.get("subdomain", "")).strip().lower()
    title = str(meta.get("title", "")).strip().lower()
    kb_id = str(meta.get("kb_id", "")).strip().lower()
    joined = " ".join(part for part in [domain, subdomain, title, kb_id] if part)
    content_l = kb_content.lower()

    if any(term in joined for term in ("computational-complexity", "complexity", "p-vs-np", "p vs np")):
        return ONTOLOGY_COMPLEXITY
    if any(
        term in joined
        for term in (
            "mathematical-physics",
            "yang-mills",
            "mass gap",
            "mass-gap",
            "gauge theory",
            "quantum field theory",
        )
    ):
        return ONTOLOGY_MATHEMATICAL_PHYSICS
    if any(
        term in joined
        for term in (
            "functional-analysis-convex-fixed-point",
            "convex fixed point",
            "markov-kakutani fixed-point",
            "markov-kakutani fixed point",
            "commuting affine",
            "common fixed point",
            "compact convex",
            "locally convex",
        )
    ):
        return ONTOLOGY_FUNCTIONAL_ANALYSIS_FIXED_POINT
    if any(
        term in joined
        for term in (
            "functional-analysis-measure-representation",
            "measure representation",
            "riesz-markov-kakutani",
            "riesz representation",
            "regular borel measure",
            "radon measure",
            "positive linear functional",
            "compactly supported continuous",
            "vanishing at infinity",
        )
    ):
        return ONTOLOGY_FUNCTIONAL_ANALYSIS_MEASURE
    if any(
        term in joined
        for term in (
            "functional-analysis-semigroup",
            "functional-analysis-semigroup-theory",
            "semigroup theory",
            "c0-semigroup",
            "hille-yosida",
            "lumer-phillips",
            "stone theorem",
            "stone's theorem",
            "one-parameter unitary group",
            "one parameter unitary group",
        )
    ):
        return ONTOLOGY_FUNCTIONAL_ANALYSIS_SEMIGROUP
    if any(
        term in content_l
        for term in (
            "\\np",
            "\\ppoly",
            "\\ph",
            "np-hard",
            "np-complete",
            "acc^0",
            "mcsp",
            "p/poly",
            "polynomial hierarchy",
            "circuit size",
        )
    ):
        return ONTOLOGY_COMPLEXITY
    if any(
        term in content_l
        for term in (
            "yang-mills",
            "wightman",
            "osterwalder",
            "schrader",
            "mass gap",
            "lattice gauge",
            "reflection positivity",
            "continuum limit",
        )
    ):
        return ONTOLOGY_MATHEMATICAL_PHYSICS
    if any(
        term in content_l
        for term in (
            "markov-kakutani fixed-point",
            "markov-kakutani fixed point",
            "commuting family of continuous affine",
            "common fixed point",
            "compact convex subset",
            "cesaro average",
            "fixed-point subset",
            "operatorname{fix}",
        )
    ):
        return ONTOLOGY_FUNCTIONAL_ANALYSIS_FIXED_POINT
    if any(
        term in content_l
        for term in (
            "riesz-markov-kakutani",
            "riesz representation",
            "regular borel measure",
            "radon measure",
            "positive linear functional",
            "compactly supported continuous",
            "compact support",
            "vanishing at infinity",
            "c_0(x)",
            "c0(x)",
        )
    ):
        return ONTOLOGY_FUNCTIONAL_ANALYSIS_MEASURE
    if any(
        term in content_l
        for term in (
            "c_0-semigroup",
            "c0-semigroup",
            "hille-yosida",
            "lumer-phillips",
            "yosida approximation",
            "abstract cauchy problem",
            "resolvent operator",
            "dissipative",
            "one-parameter unitary group",
            "one parameter unitary group",
            "strongly continuous unitary group",
            "stone's theorem",
            "stone theorem",
            "self-adjoint operator",
            "spectral theorem",
            "functional calculus",
        )
    ):
        return ONTOLOGY_FUNCTIONAL_ANALYSIS_SEMIGROUP
    return ONTOLOGY_GENERIC_MATHEMATICS


def _target_tag_sets_for_profile(ontology_profile: str) -> tuple[set[str], set[str], set[str]]:
    """
    Relevance: Operates within the relational connector layer.
    Concept: Domain-aware relevance targets for intervention ranking.
    Contribution: Keeps ranking aligned with the mathematical objects that matter in the active KB domain.
    """

    if ontology_profile == ONTOLOGY_COMPLEXITY:
        return TARGET_CLASS_TAGS, TARGET_PROBLEM_TAGS, TARGET_REGIME_TAGS
    if ontology_profile == ONTOLOGY_MATHEMATICAL_PHYSICS:
        return set(), PHYSICS_TARGET_OBJECT_TAGS, PHYSICS_TARGET_REGIME_TAGS
    if ontology_profile == ONTOLOGY_FUNCTIONAL_ANALYSIS_FIXED_POINT:
        return set(), FIXED_POINT_TARGET_OBJECT_TAGS, FIXED_POINT_TARGET_REGIME_TAGS
    if ontology_profile == ONTOLOGY_FUNCTIONAL_ANALYSIS_MEASURE:
        return set(), MEASURE_TARGET_OBJECT_TAGS, MEASURE_TARGET_REGIME_TAGS
    if ontology_profile == ONTOLOGY_FUNCTIONAL_ANALYSIS_SEMIGROUP:
        return set(), SEMIGROUP_TARGET_OBJECT_TAGS, SEMIGROUP_TARGET_REGIME_TAGS
    return set(), set(), set(GENERIC_METHOD_TOKEN_MAP.values())


def _infer_model_signatures(
    source_tokens: set[str],
    raw: str,
    clean: str,
    compact: str,
    ontology_profile: str,
) -> list[str]:
    """
    Relevance: Operates within the relational connector layer.
    Concept: Extraction of concrete computational/proof models from statements.
    Contribution: Elevates models like `ACC0-circuits`, `IPS`, and `bounded-depth-frege` into first-class reasoning objects.
    """

    models: set[str] = set()

    if ontology_profile == ONTOLOGY_MATHEMATICAL_PHYSICS:
        if _contains_any_pattern(raw, clean, compact, ["compact simple", "compact lie group", "gauge group"]):
            models.add("compact-simple-gauge-group")
        if _contains_any_pattern(raw, clean, compact, ["principal bundle", "connection"]):
            models.add("principal-bundle-connection")
        if _contains_any_pattern(raw, clean, compact, ["curvature", "bianchi identity"]):
            models.add("curvature-formulation")
        if _contains_any_pattern(raw, clean, compact, ["wightman"]):
            models.add("Wightman-QFT")
        if _contains_any_pattern(raw, clean, compact, ["osterwalder", "schrader", "os axioms", "euclidean qft"]):
            models.add("OS-Euclidean-QFT")
        if _contains_any_pattern(raw, clean, compact, ["lattice gauge theory", "wilson action", "wilson formulation"]):
            models.add("Wilson-lattice-gauge-theory")
        if _contains_any_pattern(raw, clean, compact, ["reflection positivity", "transfer matrix"]):
            models.add("reflection-positive-transfer-matrix")
        if _contains_any_pattern(raw, clean, compact, ["continuum limit"]):
            models.add("continuum-limit")
        if _contains_any_pattern(raw, clean, compact, ["renormalisation group", "renormalization group", "ultraviolet stability"]):
            models.add("rigorous-renormalization-group")
        if _contains_any_pattern(raw, clean, compact, ["minkowski", "temporal gauge", "yang-mills-higgs equations", "hyperbolic pde"]):
            models.add("classical-Yang-Mills-PDE")
        if _contains_any_pattern(raw, clean, compact, ["instanton", "self-dual", "anti-self-dual", "adhm"]):
            models.add("instanton-moduli")
        if _contains_any_pattern(raw, clean, compact, ["mass gap", "spectrum condition", "hamiltonian"]):
            models.add("Hamiltonian-mass-gap")
        if _contains_any_pattern(raw, clean, compact, ["correlator decay", "schwinger function", "exponential decay"]):
            models.add("Schwinger-function-decay")
        return sorted(models)

    if ontology_profile == ONTOLOGY_FUNCTIONAL_ANALYSIS_SEMIGROUP:
        if _contains_any_pattern(raw, clean, compact, ["banach space", "l(x)", "bounded operators"]):
            models.add("operator-theoretic-Banach-space")
        if _contains_any_pattern(raw, clean, compact, ["hilbert space", "inner product space", "unitary on h"]):
            models.add("operator-theoretic-Hilbert-space")
        if _contains_any_pattern(raw, clean, compact, ["c_0-semigroup", "c0-semigroup", "strongly continuous semigroup"]):
            models.add("C0-semigroup-model")
        if _contains_any_pattern(raw, clean, compact, ["one-parameter unitary group", "one parameter unitary group", "strongly continuous unitary group", "u(t+s)=u(t)u(s)"]):
            models.add("strongly-continuous-unitary-group")
        if _contains_any_pattern(raw, clean, compact, ["generator", "domain d(a)", "graph convergence"]):
            models.add("unbounded-generator-graph")
        if _contains_any_pattern(raw, clean, compact, ["resolvent", "lambda i - a", "(lambda i-a)^-1", "(lambda i - a)^-1"]):
            models.add("resolvent-generation-criterion")
        if _contains_any_pattern(raw, clean, compact, ["contraction semigroup", "||t(t)|| <= 1", "norm monotonicity"]):
            models.add("contraction-generation-regime")
        if _contains_any_pattern(raw, clean, compact, ["abstract cauchy problem", "mild solution", "u'(t)=au(t)"]):
            models.add("abstract-cauchy-evolution")
        if _contains_any_pattern(raw, clean, compact, ["yosida approximation", "approximants", "a_lambda"]):
            models.add("Yosida-approximation-scheme")
        if _contains_any_pattern(raw, clean, compact, ["dissipative", "surjective", "range condition"]):
            models.add("dissipative-range-condition")
        if _contains_any_pattern(raw, clean, compact, ["self-adjoint", "selfadjoint", "skew-adjoint", "skewadjoint", "hermitian operator"]):
            models.add("self-adjoint-spectral-calculus")
        if _contains_any_pattern(raw, clean, compact, ["spectral theorem", "functional calculus", "projection-valued measure", "e^{it a}", "exp(it a)", "borel functional calculus"]):
            models.add("spectral-functional-calculus")
        return sorted(models)

    if ontology_profile == ONTOLOGY_FUNCTIONAL_ANALYSIS_FIXED_POINT:
        if _contains_any_pattern(raw, clean, compact, ["locally convex topological vector space", "locally convex space", "topological vector space"]):
            models.add("locally-convex-topological-vector-space")
        if _contains_any_pattern(raw, clean, compact, ["compact convex subset", "compact convex set", "nonempty compact convex"]):
            models.add("compact-convex-subset")
        if _contains_any_pattern(raw, clean, compact, ["commuting family", "pairwise commuting", "st = ts", "commuting affine self-maps"]):
            models.add("commuting-affine-self-map-family")
        if _contains_any_pattern(raw, clean, compact, ["continuous affine self-map", "affine self-map", "single affine self-map"]):
            models.add("single-affine-self-map")
        if _contains_any_pattern(raw, clean, compact, ["fix(t)", "operatorname{fix}", "fixed-point subset", "set of fixed points"]):
            models.add("invariant-fixed-point-subset")
        if _contains_any_pattern(raw, clean, compact, ["cesaro average", "cesaro averages", "a_n(x)", "1/n", "orbit average"]):
            models.add("cesaro-averaging-scheme")
        if _contains_any_pattern(raw, clean, compact, ["finite intersection property", "finite intersection", "compactness and the finite intersection property"]):
            models.add("finite-intersection-compactness")
        if _contains_any_pattern(raw, clean, compact, ["common fixed point", "fixed by every t", "common-fixed-point"]):
            models.add("common-fixed-point-correspondence")
        return sorted(models)

    if ontology_profile == ONTOLOGY_FUNCTIONAL_ANALYSIS_MEASURE:
        if _contains_any_pattern(raw, clean, compact, ["locally compact hausdorff", "lch space", "locally compact space"]) :
            models.add("locally-compact-Hausdorff-space")
        if _contains_any_pattern(raw, clean, compact, ["c_c(x)", "cc(x)", "compactly supported continuous", "compact support"]) :
            models.add("compactly-supported-continuous-functions")
        if _contains_any_pattern(raw, clean, compact, ["c_0(x)", "c0(x)", "vanishing at infinity", "vanish at infinity"]) :
            models.add("vanishing-at-infinity-function-space")
        if _contains_any_pattern(raw, clean, compact, ["positive linear functional", "positive functional", "linear functional on c_c", "linear functional on c_0"]) :
            models.add("positive-functional-model")
        if _contains_any_pattern(raw, clean, compact, ["regular borel measure", "regular b" , "radon measure", "regular measure"]) :
            models.add("regular-Borel-measure-model")
        if _contains_any_pattern(raw, clean, compact, ["integral against", "integration against", "f dmu", "fdmu", "d\\mu"]) :
            models.add("integration-pairing-model")
        if _contains_any_pattern(raw, clean, compact, ["signed measure", "complex measure", "total variation", "jordan decomposition"]) :
            models.add("signed-measure-decomposition")
        if _contains_any_pattern(raw, clean, compact, ["riesz-markov-kakutani", "representation theorem", "represented by integration"]) :
            models.add("measure-representation-correspondence")
        return sorted(models)

    if ontology_profile == ONTOLOGY_GENERIC_MATHEMATICS:
        if _contains_any_pattern(raw, clean, compact, ["group", "lie group"]):
            models.add("group-theoretic-structure")
        if _contains_any_pattern(raw, clean, compact, ["manifold", "bundle"]):
            models.add("geometric-structure")
        if _contains_any_pattern(raw, clean, compact, ["measure", "probability", "random"]):
            models.add("probability-measure-model")
        if _contains_any_pattern(raw, clean, compact, ["operator", "hilbert space", "spectrum"]):
            models.add("operator-theoretic-model")
        return sorted(models)

    if _contains_any_pattern(raw, clean, compact, ["deterministic turing machine", "dtime"]):
        models.add("deterministic-TM")
    if _contains_any_pattern(raw, clean, compact, ["nondeterministic turing machine", "ntime", "verifier"]):
        models.add("nondeterministic-verifier")
    if _contains_any_pattern(raw, clean, compact, ["probabilistic polynomial-time", "bpp", "randomized"]):
        models.add("randomized-computation")

    has_acc0 = "acc0" in compact
    has_ac0p = "ac0p" in compact or _contains_any_pattern(raw, clean, compact, ["ac^0[p]", "mod_q", "mod q"])
    has_ac0 = ("ac0" in compact or _contains_any_pattern(raw, clean, compact, ["ac^0"])) and not has_acc0 and not has_ac0p
    has_nc1 = "nc1" in compact or _contains_any_pattern(raw, clean, compact, ["nc^1"])

    if has_acc0:
        models.add("ACC0-circuits")
    if has_ac0p:
        models.add("AC0[p]-circuits")
    if has_ac0:
        models.add("AC0-circuits")
    if has_nc1:
        models.add("NC1-circuits")

    if _contains_any_pattern(raw, clean, compact, ["p/poly", "circuit family", "polynomial-size circuits", "nonuniform"]):
        models.add("nonuniform-circuits")
    if _contains_any_pattern(raw, clean, compact, ["boolean formula", "formula size", "formulas"]):
        models.add("formula-size")
    if _contains_any_pattern(raw, clean, compact, ["monotone circuit", "monotone circuits"]):
        models.add("monotone-circuits")
    if _contains_any_pattern(raw, clean, compact, ["arithmetic circuit", "permanent", "vp", "vnp"]):
        models.add("arithmetic-circuits")
    if _contains_any_pattern(raw, clean, compact, ["resolution", "resolution refutation"]):
        models.add("resolution")
    if _contains_any_pattern(raw, clean, compact, ["bounded-depth frege", "depth frege"]):
        models.add("bounded-depth-frege")
    elif _contains_any_pattern(raw, clean, compact, ["extended frege"]):
        models.add("extended-frege")
    elif _contains_any_pattern(raw, clean, compact, ["frege"]):
        models.add("frege")
    if _contains_any_pattern(raw, clean, compact, ["ips", "ideal proof system"]):
        models.add("IPS")
    if _contains_any_pattern(raw, clean, compact, ["black-box", "hitting set"]) and "pit" in compact:
        models.add("black-box-PIT")
    if _contains_any_pattern(raw, clean, compact, ["oracle", "relativis"]):
        models.add("oracle-model")
    if _contains_any_pattern(raw, clean, compact, ["extension oracle", "low-degree extension"]):
        models.add("extension-oracle")
    if _contains_any_pattern(raw, clean, compact, ["communication complexity", "protocol", "gadget"]):
        models.add("communication-protocol")
    if _contains_any_pattern(raw, clean, compact, ["decision tree", "query complexity", "bit-queries"]):
        models.add("decision-tree")
    if _contains_any_pattern(raw, clean, compact, ["cook reckhow", "proof system", "taut"]):
        models.add("Cook-Reckhow-proof-system")
    if _contains_any_pattern(raw, clean, compact, ["prg", "pseudorandom generator"]):
        models.add("PRG-construction")
    if _contains_any_pattern(raw, clean, compact, ["prf", "pseudorandom function"]):
        models.add("PRF-assumption")

    return sorted(models)


def _infer_reduction_signatures(
    raw: str,
    clean: str,
    compact: str,
) -> list[str]:
    """
    Relevance: Operates within the relational connector layer.
    Concept: Extraction of reduction and transfer mechanisms.
    Contribution: Distinguishes `many-one`, `local`, `randomized`, and lifting-style moves that matter for proof search and hardness transfer.
    """

    reductions: set[str] = set()
    if _contains_any_pattern(raw, clean, compact, ["leq_m^p", "many-one", "karp reduction"]):
        reductions.add("many-one-reduction")
    if _contains_any_pattern(raw, clean, compact, ["turing reduction", "oracle reduction"]):
        reductions.add("turing-reduction")
    if _contains_any_pattern(raw, clean, compact, ["truth-table reduction", "truth table reduction"]):
        reductions.add("truth-table-reduction")
    if _contains_any_pattern(raw, clean, compact, ["local reduction", "local polynomial-time"]):
        reductions.add("local-reduction")
    if _contains_any_pattern(raw, clean, compact, ["randomised reduction", "randomized reduction", "bpp reductions", "rp^mcsp"]):
        reductions.add("randomized-reduction")
    if _contains_any_pattern(raw, clean, compact, ["lifting theorem", "gadget", "f circ g", "composition with a gadget"]):
        reductions.add("query-to-communication-lifting")
    if _contains_any_pattern(raw, clean, compact, ["worst-case-to-average-case", "xor", "direct-product"]):
        reductions.add("worst-case-to-average-case")
    if _contains_any_pattern(raw, clean, compact, ["oracle access", "relativis"]):
        reductions.add("oracle-relativization")
    return sorted(reductions)


def _infer_barrier_signals(
    raw: str,
    clean: str,
    compact: str,
    barrier_family: str,
    is_barrier: bool,
    ontology_profile: str,
) -> list[str]:
    """
    Relevance: Operates within the relational connector layer.
    Concept: Extraction of explicit barrier-theorem markers.
    Contribution: Keeps barrier annotations tied to genuine barrier language instead of leaking from generic algebraic or natural-language phrases.
    """

    barriers: set[str] = set()

    if ontology_profile == ONTOLOGY_MATHEMATICAL_PHYSICS:
        if _contains_any_pattern(raw, clean, compact, ["continuum limit", "continuum-limit"]):
            barriers.add("continuum-limit")
        if _contains_any_pattern(raw, clean, compact, ["path integral", "quantum measure", "construct the quantum theory"]):
            barriers.add("quantum-measure-construction")
        if _contains_any_pattern(raw, clean, compact, ["ultraviolet", "uv stability", "renormalisation", "renormalization"]):
            barriers.add("ultraviolet-control")
        if _contains_any_pattern(raw, clean, compact, ["infrared cutoff", "cutoff removal"]):
            barriers.add("cutoff-removal")
        if _contains_any_pattern(raw, clean, compact, ["gauge fixing", "gribov", "modulo gauge"]):
            barriers.add("gauge-control")
        if _contains_any_pattern(raw, clean, compact, ["does not by itself", "remains open", "does not construct", "does not extend directly"]):
            barriers.add("open-construction-gap")
        if barrier_family:
            barriers.add(barrier_family)
        if is_barrier:
            barriers.add("barrier")
        return sorted(barriers)

    if ontology_profile == ONTOLOGY_FUNCTIONAL_ANALYSIS_SEMIGROUP:
        if _contains_any_pattern(raw, clean, compact, ["resolvent power", "all n in n", "(lambda i - a)^-n", "(lambda i-a)^-n"]):
            barriers.add("powers-of-resolvent-verification")
        if _contains_any_pattern(raw, clean, compact, ["closed and d(a) is dense", "closed and densely defined", "graph convergence"]):
            barriers.add("domain-closure-density")
        if _contains_any_pattern(raw, clean, compact, ["compact convergence", "bounded time intervals", "approximants", "limit"]):
            barriers.add("approximation-limit-control")
        if _contains_any_pattern(raw, clean, compact, ["unbounded operator", "domain", "closure"]):
            barriers.add("unbounded-operator-domain-control")
        if _contains_any_pattern(raw, clean, compact, ["derivative at zero", "differentiable at zero", "limit h downarrow 0", "(u(h)x-x)/h"]):
            barriers.add("orbit-differentiability-control")
        if _contains_any_pattern(raw, clean, compact, ["spectral theorem", "functional calculus", "projection-valued measure", "borel functional calculus"]):
            barriers.add("spectral-calculus-interface")
        if barrier_family:
            barriers.add(barrier_family)
        if is_barrier:
            barriers.add("barrier")
        return sorted(barriers)

    if ontology_profile == ONTOLOGY_FUNCTIONAL_ANALYSIS_FIXED_POINT:
        if _contains_any_pattern(raw, clean, compact, ["cesaro average", "cesaro averages", "orbit average", "accumulation point of averages"]):
            barriers.add("single-map-fixed-point-extraction")
        if _contains_any_pattern(raw, clean, compact, ["fix(t)", "fixed-point subset", "set of fixed points", "invariant subset"]):
            barriers.add("invariant-subset-propagation")
        if _contains_any_pattern(raw, clean, compact, ["finite intersection property", "finite intersection", "compactness"]):
            barriers.add("finite-intersection-compactness")
        if barrier_family:
            barriers.add(barrier_family)
        if is_barrier:
            barriers.add("barrier")
        return sorted(barriers)

    if ontology_profile == ONTOLOGY_FUNCTIONAL_ANALYSIS_MEASURE:
        if _contains_any_pattern(raw, clean, compact, ["inner regular", "outer regular", "regular borel", "regular measure"]):
            barriers.add("topological-regularity-reconstruction")
        if _contains_any_pattern(raw, clean, compact, ["positive functional", "sigma-additive", "countably additive", "premeasure"]):
            barriers.add("positivity-to-sigma-additivity")
        if _contains_any_pattern(raw, clean, compact, ["urysohn", "compact support", "compactly supported continuous", "approximate indicator"]):
            barriers.add("compact-open-approximation")
        if _contains_any_pattern(raw, clean, compact, ["signed measure", "jordan decomposition", "total variation", "complex measure"]):
            barriers.add("signed-decomposition-control")
        if barrier_family:
            barriers.add(barrier_family)
        if is_barrier:
            barriers.add("barrier")
        return sorted(barriers)

    if _contains_any_pattern(raw, clean, compact, ["relativising", "relativizing", "relativisation", "relativization"]):
        barriers.add("relativization")
    if _contains_any_pattern(raw, clean, compact, ["natural proofs", "natural proof", "constructive large useful"]):
        barriers.add("natural-proofs")
    if _contains_any_pattern(raw, clean, compact, ["algebrising", "algebrizing", "algebrisation", "algebrization", "non-algebrising", "non-algebrizing"]):
        barriers.add("algebrization")
    if barrier_family:
        barriers.add(barrier_family)
    if is_barrier:
        barriers.add("barrier")
    return sorted(barriers)


def _infer_claim_signatures(
    complexity_classes: list[str],
    core_problems: list[str],
    model_signatures: list[str],
    reduction_signatures: list[str],
    barrier_signals: list[str],
    method_tags: list[str],
    raw: str,
    clean: str,
    compact: str,
    ontology_profile: str,
) -> list[str]:
    """
    Relevance: Operates within the relational connector layer.
    Concept: Extraction of statement-level mathematical claim forms.
    Contribution: Surfaces the actual theorem content being used, such as `PH-collapse` or `PHP-resolution-lower-bound`.
    """

    claims: set[str] = set()

    if ontology_profile == ONTOLOGY_MATHEMATICAL_PHYSICS:
        if _contains_any_pattern(raw, clean, compact, ["construct", "construction", "constructed nonperturbatively", "there exist nontrivial interacting qft"]):
            claims.add("constructive-existence")
        if _contains_any_pattern(raw, clean, compact, ["mass gap", "positive mass gap", "spectral gap"]):
            claims.add("mass-gap")
        if _contains_any_pattern(raw, clean, compact, ["osterwalder", "schrader", "reconstruction", "equivalence with wightman"]):
            claims.add("OS-reconstruction")
        if _contains_any_pattern(raw, clean, compact, ["reflection positivity", "transfer matrix"]):
            claims.add("reflection-positivity-transfer")
        if _contains_any_pattern(raw, clean, compact, ["continuum limit", "cutoff removal"]):
            claims.add("continuum-limit-control")
        if _contains_any_pattern(raw, clean, compact, ["exponential decay", "correlator decay", "schwinger functions decay"]):
            claims.add("exponential-correlation-decay")
        if _contains_any_pattern(raw, clean, compact, ["ultraviolet stability", "renormalisation-group analysis", "renormalization-group analysis"]):
            claims.add("ultraviolet-stability")
        if _contains_any_pattern(raw, clean, compact, ["instanton", "adhm", "self-dual", "anti-self-dual"]):
            claims.add("instanton-classification")
        if _contains_any_pattern(raw, clean, compact, ["minimise the yang-mills functional", "minimising sequences", "yang-mills connections as limits"]):
            claims.add("yang-mills-minimizer-existence")
        if _contains_any_pattern(raw, clean, compact, ["global smooth solutions", "global existence", "well-posedness"]):
            claims.add("classical-global-well-posedness")
        if _contains_any_pattern(raw, clean, compact, ["morse-bott", "moduli of bundles", "moduli spaces"]):
            claims.add("moduli-space-structure")
        if _contains_any_pattern(raw, clean, compact, ["classical"]):
            claims.add("classical-theory-result")
        return _sort_signatures(claims)

    if ontology_profile == ONTOLOGY_FUNCTIONAL_ANALYSIS_SEMIGROUP:
        if _contains_any_pattern(raw, clean, compact, ["c_0-semigroup", "c0-semigroup", "strongly continuous semigroup"]) and _contains_any_pattern(raw, clean, compact, ["t(0)=i", "t(t+s)=t(t)t(s)", "downarrow 0"]):
            claims.add("c0-semigroup-definition")
        if _contains_any_pattern(raw, clean, compact, ["one-parameter unitary group", "one parameter unitary group", "strongly continuous unitary group"]) and _contains_any_pattern(raw, clean, compact, ["u(0)=i", "u(t+s)=u(t)u(s)", "continuous in the strong operator topology", "strongly continuous"]):
            claims.add("unitary-group-definition")
        if _contains_any_pattern(raw, clean, compact, ["define ax := lim", "generator is the right derivative", "domain d(a)"]):
            claims.add("generator-definition")
        if _contains_any_pattern(raw, clean, compact, ["self-adjoint operator", "a=a^*", "densely defined self-adjoint", "selfadjoint"]):
            claims.add("self-adjoint-operator-definition")
        if _contains_any_pattern(raw, clean, compact, ["resolvent set", "bounded inverse", "(lambda i - a)^-1", "(lambda i-a)^-1"]):
            claims.add("resolvent-definition")
        if _contains_any_pattern(raw, clean, compact, ["a is closed and d(a) is dense", "generator imposes strong domain regularity", "closure and density"]):
            claims.add("generator-closed-dense")
        if _contains_any_pattern(raw, clean, compact, ["generator is symmetric", "is symmetric on its natural domain", "<ax,y> = <x,ay>", "langle ax,y rangle = langle x,ay rangle"]):
            claims.add("generator-symmetry")
        if _contains_any_pattern(raw, clean, compact, ["spectral theorem", "functional calculus", "e^{it a}", "exp(it a)", "projection-valued measure"]):
            claims.add("spectral-calculus-unitary-realization")
        if _contains_any_pattern(raw, clean, compact, ["generator is self-adjoint", "self-adjoint generator", "infinitesimal generator is self-adjoint", "skew-adjoint generator"]):
            claims.add("self-adjoint-generator-characterization")
        if _contains_any_pattern(raw, clean, compact, ["stone's theorem", "stone theorem", "there exists a unique self-adjoint operator", "iff there exists a unique self-adjoint operator", "one-parameter unitary groups correspond to self-adjoint operators"]):
            claims.add("stone-unitary-group-correspondence")
        if _contains_any_pattern(raw, clean, compact, ["generates a c_0-semigroup", "generates a c0-semigroup"]) and _contains_any_pattern(raw, clean, compact, ["iff", "if and only if"]) and _contains_any_pattern(raw, clean, compact, ["(omega,+infty) subset rho(a)", "(omega, +infty) subset rho(a)", "(lambda i - a)^-n", "(lambda i-a)^-n"]):
            claims.add("semigroup-generation-characterization")
        if _contains_any_pattern(raw, clean, compact, ["contraction c_0-semigroup", "contraction c0-semigroup", "||t(t)|| <= 1"]) and _contains_any_pattern(raw, clean, compact, ["iff", "if and only if"]):
            claims.add("contraction-generation-characterization")
        if _contains_any_pattern(raw, clean, compact, ["dissipative", "surjective for some lambda_0", "lumer-phillips"]):
            claims.add("dissipativity-characterization")
        if _contains_any_pattern(raw, clean, compact, ["abstract cauchy problem", "unique mild solution", "equivalent"]) and _contains_any_pattern(raw, clean, compact, ["generates a c_0-semigroup", "u'(t)=au(t)"]):
            claims.add("cauchy-problem-equivalence")
        if _contains_any_pattern(raw, clean, compact, ["yosida approximation", "a_lambda", "bounded generators", "approximants converge"]):
            claims.add("yosida-approximation-convergence")
        if _contains_any_pattern(raw, clean, compact, ["generator is unique", "generator uniqueness", "uniqueness of the generator"]):
            claims.add("generator-uniqueness")
        if _contains_any_pattern(raw, clean, compact, ["resolvent monotonicity", "1/lambda", "norm monotonicity"]):
            claims.add("contraction-resolvent-monotonicity")
        if _contains_any_pattern(raw, clean, compact, ["translation group", "shift group", "u_t f(x)=f(x+t)", "momentum operator"]):
            claims.add("unitary-group-example")
        if _contains_any_pattern(raw, clean, compact, ["schrodinger", "schrödinger", "hamiltonian", "time evolution in quantum mechanics"]):
            claims.add("quantum-time-evolution")
        return _sort_signatures(claims)

    if ontology_profile == ONTOLOGY_FUNCTIONAL_ANALYSIS_FIXED_POINT:
        if _contains_any_pattern(raw, clean, compact, ["compact convex subset", "compact convex set", "nonempty compact convex"]):
            claims.add("compact-convex-set-definition")
        if _contains_any_pattern(raw, clean, compact, ["commuting family", "continuous affine self-maps", "pairwise commuting", "st = ts"]):
            claims.add("commuting-affine-family-definition")
        if _contains_any_pattern(raw, clean, compact, ["fix(t)", "operatorname{fix}", "fixed-point subset", "set of fixed points"]):
            claims.add("invariant-fixed-point-subset-definition")
        if _contains_any_pattern(raw, clean, compact, ["a_n(x)", "1/n", "cesaro averages", "orbit average", "convex combination of iterates"]):
            claims.add("cesaro-average-preservation")
        if _contains_any_pattern(raw, clean, compact, ["single affine self-map", "t has a fixed point", "continuous affine self-map has a fixed point"]):
            claims.add("single-affine-map-fixed-point")
        if _contains_any_pattern(raw, clean, compact, ["fix(t) is nonempty", "fix(t) is compact and convex", "fixed-point subset is nonempty compact convex"]):
            claims.add("fixed-point-subset-structure")
        if _contains_any_pattern(raw, clean, compact, ["s(fix(t)) subseteq fix(t)", "preserves the fixed-point subset", "commuting maps preserve"]):
            claims.add("commuting-preserves-fixed-point-subset")
        if _contains_any_pattern(raw, clean, compact, ["finite commuting family", "finite subfamily", "common fixed point for every finite"]):
            claims.add("finite-family-common-fixed-point")
        if _contains_any_pattern(raw, clean, compact, ["markov-kakutani", "common fixed point", "fixed by every t in f"]):
            claims.add("markov-kakutani-common-fixed-point")
        if _contains_any_pattern(raw, clean, compact, ["compact interval", "[0,1]", "example"]) and _contains_any_pattern(raw, clean, compact, ["common fixed point"]):
            claims.add("common-fixed-point-example")
        return _sort_signatures(claims)

    if ontology_profile == ONTOLOGY_FUNCTIONAL_ANALYSIS_MEASURE:
        if _contains_any_pattern(raw, clean, compact, ["locally compact hausdorff", "lch space", "locally compact hausdorff space"]):
            claims.add("locally-compact-hausdorff-definition")
        if _contains_any_pattern(raw, clean, compact, ["c_c(x)", "cc(x)", "compactly supported continuous", "compact support"]) :
            claims.add("cc-space-definition")
        if _contains_any_pattern(raw, clean, compact, ["f = 1 on k", "supp(f) subseteq u", "compact subset of x with k compact and u open", "0 <= f <= 1"]):
            claims.add("compact-open-approximation-lemma")
        if _contains_any_pattern(raw, clean, compact, ["positive linear functional", "positive functional"]) :
            claims.add("positive-functional-definition")
        if _contains_any_pattern(raw, clean, compact, ["regular borel measure", "radon measure", "inner regular", "outer regular"]) :
            claims.add("regular-borel-measure-definition")
        if _contains_any_pattern(raw, clean, compact, ["defines a positive linear functional", "integration against a regular borel measure defines", "phi_mu(f)", "positive by integration"]) :
            claims.add("integration-defines-positive-functional")
        if _contains_any_pattern(raw, clean, compact, ["there exists a unique regular borel measure", "there exists a unique radon measure", "represented by a measure", "positive linear functional is represented by", "represented by a unique regular borel measure"]) :
            claims.add("positive-functional-measure-existence")
        if _contains_any_pattern(
            raw,
            clean,
            compact,
            [
                "functions in c_c(x) separate",
                "uniqueness of the measure",
                "if integrals agree for all f",
                "if integrals agree for all f in c_c(x)",
                "uniquely determined by integration",
                "determined by c_c",
                "then mu = nu",
                "then \\mu = \\nu",
                "then mu=nu",
            ],
        ):
            claims.add("uniqueness-from-cc-separation")
        if _contains_any_pattern(raw, clean, compact, ["riesz-markov-kakutani", "representation theorem", "correspondence between positive linear functionals and regular borel measures"]) :
            claims.add("riesz-markov-kakutani-correspondence")
        if _contains_any_pattern(raw, clean, compact, ["c_0(x)^*", "dual of c_0(x)", "finite signed regular borel measure", "signed regular measure"]) :
            claims.add("c0-dual-measure-representation")
        if _contains_any_pattern(raw, clean, compact, ["total variation equals", "dual norm", "norm equals total variation"]) :
            claims.add("total-variation-norm-identity")
        if _contains_any_pattern(raw, clean, compact, ["dirac measure", "evaluation at x", "delta_x"]) :
            claims.add("dirac-evaluation-example")
        return _sort_signatures(claims)

    if ontology_profile == ONTOLOGY_GENERIC_MATHEMATICS:
        if _contains_any_pattern(raw, clean, compact, ["there exists", "there exist", "existence"]):
            claims.add("existence")
        if _contains_any_pattern(raw, clean, compact, ["classification", "classified", "complete classification"]):
            claims.add("classification")
        if _contains_any_pattern(raw, clean, compact, ["if and only if", "iff", "equivalent"]):
            claims.add("equivalence")
        if _contains_any_pattern(raw, clean, compact, ["isomorphic", "bijection", "correspondence"]):
            claims.add("structural-correspondence")
        return _sort_signatures(claims)

    classes = set(complexity_classes)
    problems = set(core_problems)
    models = set(model_signatures)
    reductions = set(reduction_signatures)
    barriers = set(barrier_signals)
    methods = set(method_tags)

    lead_problem = _preferred_value(core_problems, PROBLEM_SIGNATURE_PRIORITY)
    lead_model = _preferred_value(model_signatures, MODEL_SIGNATURE_PRIORITY)

    np_complete = _contains_any_pattern(raw, clean, compact, ["np-complete", "np complete"])
    np_hard = _contains_any_pattern(raw, clean, compact, ["np-hard", "np hard", "np-hardness"])
    collapse = _contains_any_pattern(raw, clean, compact, ["collapse", "collapses"])
    separation = _contains_any_pattern(
        raw,
        clean,
        compact,
        ["notsubseteq", "does not have polynomial-size", "separation", "lower bound", "superpolynomial", "exponential-size", "requires"],
    )
    equivalence = _contains_any_pattern(raw, clean, compact, ["iff", "if and only if", "equivalence"])

    if np_complete:
        claims.add("NP-completeness")
        if lead_problem:
            claims.add(f"{lead_problem}-NP-complete")
    if np_hard:
        claims.add("NP-hardness")
        if lead_problem:
            claims.add(f"{lead_problem}-NP-hard")
    if collapse and "PH" in classes:
        claims.add("PH-collapse")
    if separation:
        if "P" in classes and "NP" in classes:
            claims.add("P-vs-NP-separation")
        if "NP" in classes and "P/poly" in classes:
            claims.add("NP-vs-P/poly-separation")
        if "NEXP" in classes and "ACC0-circuits" in models:
            claims.add("NEXP-vs-ACC0")
        elif "NEXP" in classes and "nonuniform-circuits" in models:
            claims.add("NEXP-circuit-separation")
    if _contains_any_pattern(
        raw,
        clean,
        compact,
        ["lower bound", "superpolynomial", "exponential-size", "barely-superlinear", "does not have polynomial-size", "requires circuit size"],
    ):
        claims.add("lower-bound")
        if lead_problem and lead_model:
            claims.add(f"{lead_problem}-{lead_model}-lower-bound")
        if "formula-size" in models:
            claims.add("formula-size-lower-bound")
        if "nonuniform-circuits" in models:
            claims.add("nonuniform-circuit-lower-bound")
        if "arithmetic-circuits" in models:
            claims.add("arithmetic-circuit-lower-bound")
        if "resolution" in models or "frege" in models or "bounded-depth-frege" in models or "Cook-Reckhow-proof-system" in models:
            claims.add("proof-size-lower-bound")
        if "IPS" in models:
            claims.add("IPS-size-lower-bound")
        if "communication-protocol" in models:
            claims.add("communication-lower-bound")
        if "decision-tree" in models:
            claims.add("query-lower-bound")
        if "monotone-circuits" in models:
            claims.add("monotone-circuit-lower-bound")
        if "ACC0-circuits" in models:
            claims.add("ACC0-lower-bound")
        if "AC0[p]-circuits" in models:
            claims.add("AC0[p]-lower-bound")
        if "AC0-circuits" in models:
            claims.add("AC0-lower-bound")
        if _contains_any_pattern(raw, clean, compact, ["uniformly random", "random boolean function", "almost all functions"]):
            claims.add("random-function-lower-bound")
        if _contains_any_pattern(raw, clean, compact, ["barely-superlinear", "slightly beyond known frontiers", "n^ 1+varepsilon", "n^1+varepsilon"]):
            claims.add("near-threshold-lower-bound")
        if _contains_any_pattern(raw, clean, compact, ["superpolynomial"]):
            claims.add("superpolynomial-lower-bound")
        if _contains_any_pattern(raw, clean, compact, ["exponential-size", "exp(", "2^"]):
            claims.add("exponential-lower-bound")
    if "natural-proofs" in barriers:
        claims.add("natural-proofs-barrier")
    if "relativization" in barriers:
        claims.add("relativization-barrier")
    if "algebrization" in barriers:
        claims.add("algebrization-barrier")
    if equivalence and _contains_any_pattern(raw, clean, compact, ["proof system", "polynomially bounded", "taut"]):
        claims.add("proof-system-characterization")
    if "query-to-communication-lifting" in reductions:
        claims.add("lifting-theorem")
    if "hardness-magnification" in methods or _contains_any_pattern(raw, clean, compact, ["hardness magnification", "magnification"]):
        claims.add("hardness-magnification")
    if _contains_any_pattern(raw, clean, compact, ["hardness vs randomness", "pseudorandom generator", "derandomisation", "derandomization"]):
        claims.add("hardness-vs-randomness")
    if "PIT" in problems and _contains_any_pattern(raw, clean, compact, ["lower bounds", "permanent", "nexp"]):
        claims.add("PIT-lower-bound-interface")
    if "MCSP" in problems and "local-reduction" in reductions and _contains_any_pattern(raw, clean, compact, ["not np-complete", "not np complete"]):
        claims.add("MCSP-local-nonhardness")
    if "MCSP" in problems and np_hard:
        claims.add("MCSP-NP-hardness")

    return sorted(claims)


def _signature_specificity(value: str) -> tuple[int, int]:
    """
    Relevance: Operates within the relational connector layer.
    Concept: Ranking heuristic over typed mathematical signatures.
    Contribution: Helps the framework prefer theorem-family and model-specific signatures over generic topical placeholders.
    """

    text = str(value).strip()
    lower = text.lower()
    score = 0
    if lower in {"lower-bound", "mild-lower-bound", "major-separation", "restricted-model-lower-bound", "query-lower-bound"}:
        score -= 3
    if "implies" in lower or "not-in" in lower or "not-equal" in lower or "collapse" in lower or "separation" in lower:
        score += 4
    if "-lower-bound" in lower and lower != "lower-bound":
        score += 3
    if any(
        token in lower
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
            "frege",
            "resolution",
            "p/poly",
            "nexp",
            "ph",
        )
    ):
        score += 3
    if any(token in lower for token in ("near-threshold", "superpolynomial", "exponential", "many-one", "local-reduction")):
        score += 2
    return score, len(text)


def _sort_signatures(values: set[str] | list[str]) -> list[str]:
    """
    Relevance: Operates within the relational connector layer.
    Concept: Stable ordering of signatures by inferential specificity.
    Contribution: Ensures downstream selection keeps the most mathematically informative schema instead of whichever string sorts first alphabetically.
    """

    uniq = {str(v).strip() for v in values if str(v).strip()}
    return sorted(uniq, key=lambda item: (_signature_specificity(item)[0], _signature_specificity(item)[1], item), reverse=True)


def _clean_evidence_terms(values: set[str] | list[str], limit: int = 6) -> list[str]:
    """
    Relevance: Operates within the relational connector layer.
    Concept: Sanitization of bridge evidence for reporting and downstream hypothesis generation.
    Contribution: Filters out token debris while preserving compact mathematical labels such as `OS`, `NP`, or `AC0`.
    """

    cleaned: list[str] = []
    seen: set[str] = set()
    ordered = _sort_signatures(values)
    for raw in ordered:
        term = str(raw).strip()
        if not term:
            continue
        lower = term.lower()
        if re.fullmatch(r"[a-z]", lower):
            continue
        if len(term) < 3 and not (term.isupper() or any(ch.isdigit() for ch in term) or "-" in term or "/" in term):
            continue
        if lower in {"concept", "method", "support", "target", "statement-conclusion"}:
            continue
        if term in seen:
            continue
        seen.add(term)
        cleaned.append(term)
        if len(cleaned) >= max(1, limit):
            break
    return cleaned


def _specific_lower_bound_signatures(
    core_problems: list[str],
    model_signatures: list[str],
    claim_signatures: list[str],
) -> list[str]:
    """
    Relevance: Operates within the relational connector layer.
    Concept: Normalization of lower-bound language into model- and problem-specific theorem schemas.
    Contribution: Prevents the framework from collapsing distinct lower-bound obligations into one generic placeholder.
    """

    problems = set(core_problems)
    models = set(model_signatures)
    claims = set(claim_signatures)
    candidates: set[str] = set()

    for claim in claims:
        if claim.endswith("-lower-bound") and claim != "lower-bound":
            candidates.add(claim)

    if "near-threshold-lower-bound" in claims:
        if "Gap-MCSP" in problems and "formula-size" in models:
            candidates.add("GapMCSP-near-threshold-formula-lower-bound")
        if "Gap-MCSP" in problems and "nonuniform-circuits" in models:
            candidates.add("GapMCSP-near-threshold-nonuniform-circuit-lower-bound")
        if "MCSP" in problems and "formula-size" in models:
            candidates.add("MCSP-near-threshold-formula-lower-bound")
        if "MCSP" in problems and "nonuniform-circuits" in models:
            candidates.add("MCSP-near-threshold-nonuniform-circuit-lower-bound")

    if "exponential-lower-bound" in claims:
        if "ACC0-circuits" in models:
            candidates.add("ACC0-exponential-lower-bound")
        if "AC0[p]-circuits" in models:
            candidates.add("AC0[p]-exponential-lower-bound")
        if "formula-size" in models:
            candidates.add("formula-size-exponential-lower-bound")
        if "nonuniform-circuits" in models:
            candidates.add("nonuniform-circuit-exponential-lower-bound")

    if "superpolynomial-lower-bound" in claims:
        if "IPS" in models:
            candidates.add("IPS-superpolynomial-lower-bound")
        if "formula-size" in models:
            candidates.add("formula-size-superpolynomial-lower-bound")
        if "nonuniform-circuits" in models:
            candidates.add("nonuniform-circuit-superpolynomial-lower-bound")

    return _sort_signatures(candidates)


def _infer_antecedent_signatures(
    kind: str,
    complexity_classes: list[str],
    core_problems: list[str],
    model_signatures: list[str],
    reduction_signatures: list[str],
    claim_signatures: list[str],
    implication_signatures: list[str],
    raw: str,
    clean: str,
    compact: str,
    ontology_profile: str,
) -> list[str]:
    """
    Relevance: Operates within the relational connector layer.
    Concept: Extraction of theorem antecedent schemas.
    Contribution: Records what must hold before a statement yields its mathematical consequence, which is essential for proof search.
    """

    antecedents: set[str] = set()
    kind_l = str(kind).strip().lower()
    is_theorem_like = kind_l in {"theorem", "lemma", "corollary", "observation", "conjecture"}

    if ontology_profile == ONTOLOGY_MATHEMATICAL_PHYSICS:
        claims = set(claim_signatures)
        implications = set(implication_signatures)
        barriers = set()
        if "OS-axioms-imply-Wightman-QFT" in implications or "OS-reconstruction" in claims:
            antecedents.add("OS-axioms-and-reflection-positivity")
        if "transfer-matrix-gap-implies-correlator-decay" in implications or "reflection-positivity-transfer" in claims:
            antecedents.add("reflection-positivity-and-transfer-matrix")
        if "ultraviolet-stability" in claims or "continuum-limit-control" in claims:
            antecedents.add("multiscale-renormalization-control")
        if "instanton-classification" in claims:
            antecedents.add("self-duality-and-finite-action")
        if "yang-mills-minimizer-existence" in claims:
            antecedents.add("compact-four-manifold-variational-setup")
        if "classical-global-well-posedness" in claims:
            antecedents.add("smooth-finite-energy-initial-data")
        if _contains_any_pattern(raw, clean, compact, ["assumptions", "hypotheses"]) and not antecedents:
            antecedents.add("analytic-assumption-bundle")
        if is_theorem_like and not antecedents:
            antecedents.add("unconditional")
        return _sort_signatures(antecedents)

    if ontology_profile == ONTOLOGY_FUNCTIONAL_ANALYSIS_SEMIGROUP:
        claims = set(claim_signatures)
        implications = set(implication_signatures)
        if "unitary-group-definition" in claims or "unitary-group-implies-self-adjoint-generator" in implications:
            antecedents.add("strongly-continuous-unitary-group")
        if "self-adjoint-operator-definition" in claims or "self-adjoint-operator-implies-unitary-group" in implications:
            antecedents.add("self-adjoint-operator-on-hilbert-space")
        if "spectral-calculus-unitary-realization" in claims or "spectral-theorem-enables-unitary-functional-calculus" in implications:
            antecedents.add("spectral-theorem-and-functional-calculus")
        if "self-adjoint-generator-characterization" in claims:
            antecedents.add("differentiable-unitary-orbit-at-zero")
        if "generator-symmetry" in claims:
            antecedents.add("differentiable-unitary-orbit-at-zero")
        if "stone-unitary-group-correspondence" in claims:
            antecedents.add("strongly-continuous-unitary-group")
        if "semigroup-generation-characterization" in claims or "closed-dense-plus-resolvent-powers-imply-c0-generation" in implications:
            antecedents.add("closed-dense-operator-with-resolvent-power-bounds")
        if "contraction-generation-characterization" in claims or "closed-dense-plus-first-resolvent-bound-imply-contraction-generation" in implications:
            antecedents.add("closed-dense-operator-with-first-resolvent-bound")
        if "dissipativity-characterization" in claims or "dissipativity-plus-range-condition-imply-contraction-generation" in implications:
            antecedents.add("densely-defined-dissipative-operator-with-surjective-shift")
        if "cauchy-problem-equivalence" in claims or "c0-generation-iff-cauchy-well-posedness" in implications:
            antecedents.add("closed-operator-or-semigroup-generator")
        if "generator-closed-dense" in claims or "c0-generation-implies-closed-dense-generator" in implications:
            antecedents.add("generator-of-c0-semigroup")
        if "yosida-approximation-convergence" in claims or "resolvent-approximants-converge-to-generated-semigroup" in implications:
            antecedents.add("resolvent-family-at-large-lambda")
        if "generator-uniqueness" in claims:
            antecedents.add("shared-semigroup-orbit-data")
        if "contraction-resolvent-monotonicity" in claims:
            antecedents.add("contraction-semigroup-generator")
        if is_theorem_like and not antecedents:
            antecedents.add("unconditional")
        return _sort_signatures(antecedents)

    if ontology_profile == ONTOLOGY_FUNCTIONAL_ANALYSIS_FIXED_POINT:
        claims = set(claim_signatures)
        implications = set(implication_signatures)
        if "compact-convex-set-definition" in claims:
            antecedents.add("nonempty-compact-convex-subset")
        if "commuting-affine-family-definition" in claims or "commutativity-implies-fixed-point-subset-invariance" in implications:
            antecedents.add("commuting-affine-family-on-compact-convex-set")
        if "invariant-fixed-point-subset-definition" in claims or "single-map-fixed-point-implies-invariant-fixed-point-subset" in implications:
            antecedents.add("single-affine-self-map-on-compact-convex-set")
        if "cesaro-average-preservation" in claims or "affine-averaging-implies-single-map-fixed-point" in implications:
            antecedents.add("continuous-affine-self-map-on-compact-convex-set")
        if "single-affine-map-fixed-point" in claims:
            antecedents.add("continuous-affine-self-map-on-compact-convex-set")
        if "fixed-point-subset-structure" in claims:
            antecedents.add("single-affine-self-map-with-fixed-point")
        if "commuting-preserves-fixed-point-subset" in claims:
            antecedents.add("nonempty-invariant-fixed-point-subset")
        if "finite-family-common-fixed-point" in claims or "finite-intersection-property-implies-common-fixed-point" in implications:
            antecedents.add("finite-commuting-affine-subfamily")
        if "markov-kakutani-common-fixed-point" in claims:
            antecedents.add("commuting-affine-family-on-compact-convex-set")
        if is_theorem_like and not antecedents:
            antecedents.add("unconditional")
        return _sort_signatures(antecedents)

    if ontology_profile == ONTOLOGY_FUNCTIONAL_ANALYSIS_MEASURE:
        claims = set(claim_signatures)
        implications = set(implication_signatures)
        if "positive-functional-definition" in claims or "positive-functional-implies-regular-measure" in implications:
            antecedents.add("positive-linear-functional-on-cc-space")
        if "regular-borel-measure-definition" in claims or "regular-measure-implies-positive-functional" in implications:
            antecedents.add("regular-borel-measure-on-lch-space")
        if "compact-open-approximation-lemma" in claims or "uniqueness-from-cc-separation" in claims:
            antecedents.add("compact-open-approximation-on-lch-space")
        if "uniqueness-from-cc-separation" in claims:
            antecedents.add("regular-borel-measure-on-lch-space")
        if "c0-dual-measure-representation" in claims:
            antecedents.add("continuous-linear-functional-on-c0")
        if "riesz-markov-kakutani-correspondence" in claims:
            antecedents.add("positive-linear-functional-on-cc-space")
        if is_theorem_like and not antecedents:
            antecedents.add("unconditional")
        return _sort_signatures(antecedents)

    if ontology_profile == ONTOLOGY_GENERIC_MATHEMATICS:
        if _contains_any_pattern(raw, clean, compact, ["assume", "suppose", "let"]) and is_theorem_like:
            antecedents.add("local-hypothesis-bundle")
        if is_theorem_like and not antecedents:
            antecedents.add("unconditional")
        return _sort_signatures(antecedents)

    classes = set(complexity_classes)
    problems = set(core_problems)
    reductions = set(reduction_signatures)
    claims = set(claim_signatures)
    implications = set(implication_signatures)
    specific_lower_bounds = _specific_lower_bound_signatures(core_problems, model_signatures, claim_signatures)

    if "NP-in-P/poly-implies-PH-collapse" in implications:
        antecedents.add("NP-in-P/poly")
    if "PIT-in-P-implies-lower-bounds" in implications:
        antecedents.add("PIT-in-P")
    if "hardness-implies-PRG" in implications:
        antecedents.add("worst-case-to-average-case-hardness")
    if "E-hardness-implies-BPP-equals-P" in implications:
        antecedents.add("E-exponential-hardness")
    if "hardness-yields-BPP-derandomization" in implications:
        antecedents.add("hardness-assumption")
    if "poly-bounded-proofs-iff-NP-equals-coNP" in implications:
        antecedents.add("poly-bounded-proof-system")
    if "IPS-lower-bounds-imply-arithmetic-lower-bounds" in implications:
        antecedents.add("IPS-superpolynomial-lower-bound")
    if "GapMCSP-lower-bounds-imply-NP-not-in-P/poly" in implications:
        if specific_lower_bounds:
            antecedents.update(specific_lower_bounds[:2])
        else:
            antecedents.add("GapMCSP-near-threshold-lower-bound")
    if "mild-lower-bounds-imply-major-separation" in implications:
        if specific_lower_bounds:
            antecedents.update(specific_lower_bounds[:2])
        else:
            antecedents.add("mild-lower-bound")
    if "query-lower-bounds-imply-communication-lower-bounds" in implications:
        antecedents.add("query-lower-bound")
    if "local-reductions-preclude-MCSP-NP-completeness" in implications:
        antecedents.add("local-reduction-to-MCSP")
    if "assumptions-imply-MCSP-NP-hardness" in implications:
        antecedents.add("cryptographic-and-complexity-assumptions")

    if "NP-hardness" in claims and "many-one-reduction" in reductions:
        antecedents.add("poly-time-many-one-reduction")
    if "NP-hardness" in claims and "randomized-reduction" in reductions:
        antecedents.add("randomized-reduction")
    if "MCSP-local-nonhardness" in claims:
        antecedents.add("local-reduction")
    if _contains_any_pattern(raw, clean, compact, ["assuming", "assumptions", "hypotheses"]) and not antecedents:
        antecedents.add("assumption-bundle")
    if _contains_any_pattern(raw, clean, compact, ["if there exists a function in"]) and "E" in classes:
        antecedents.add("explicit-hard-function")
    if _contains_any_pattern(raw, clean, compact, ["if there exists", "if"]) and "PIT" in problems:
        antecedents.add("PIT-derandomization-assumption")

    if is_theorem_like and not antecedents:
        antecedents.add("unconditional")
    return _sort_signatures(antecedents)


def _infer_consequence_signatures(
    kind: str,
    complexity_classes: list[str],
    core_problems: list[str],
    model_signatures: list[str],
    claim_signatures: list[str],
    implication_signatures: list[str],
    raw: str,
    clean: str,
    compact: str,
    ontology_profile: str,
) -> list[str]:
    """
    Relevance: Operates within the relational connector layer.
    Concept: Extraction of theorem consequence schemas.
    Contribution: Makes explicit what inferential payoff a statement provides once its antecedent is satisfied.
    """

    consequences: set[str] = set()
    kind_l = str(kind).strip().lower()
    is_theorem_like = kind_l in {"theorem", "lemma", "corollary", "observation", "conjecture"}

    if ontology_profile == ONTOLOGY_MATHEMATICAL_PHYSICS:
        claims = set(claim_signatures)
        implications = set(implication_signatures)
        if "OS-axioms-imply-Wightman-QFT" in implications or "OS-reconstruction" in claims:
            consequences.add("Wightman-QFT-realization")
        if "transfer-matrix-gap-implies-correlator-decay" in implications or "reflection-positivity-transfer" in claims:
            consequences.add("positive-self-adjoint-Hamiltonian")
        if "mass-gap" in claims:
            consequences.add("positive-mass-gap")
        if "constructive-existence" in claims:
            consequences.add("rigorous-Yang-Mills-construction")
        if "exponential-correlation-decay" in claims:
            consequences.add("spectral-gap-signature")
        if "continuum-limit-control" in claims:
            consequences.add("continuum-limit-candidate")
        if "classical-global-well-posedness" in claims:
            consequences.add("global-classical-solution-theory")
        if "moduli-space-structure" in claims:
            consequences.add("moduli-space-control")
        if is_theorem_like and not consequences and claims:
            consequences.update(_sort_signatures(claims)[:2])
        return _sort_signatures(consequences)

    if ontology_profile == ONTOLOGY_FUNCTIONAL_ANALYSIS_SEMIGROUP:
        claims = set(claim_signatures)
        implications = set(implication_signatures)
        if "unitary-group-definition" in claims:
            consequences.add("strongly-continuous-unitary-group")
        if "self-adjoint-operator-definition" in claims:
            consequences.add("self-adjoint-operator-on-hilbert-space")
        if "spectral-calculus-unitary-realization" in claims or "spectral-theorem-enables-unitary-functional-calculus" in implications:
            consequences.add("unitary-group-via-functional-calculus")
        if "generator-symmetry" in claims:
            consequences.add("symmetric-generator")
        if "self-adjoint-generator-characterization" in claims or "unitary-group-implies-self-adjoint-generator" in implications:
            consequences.add("unique-self-adjoint-generator")
        if "stone-unitary-group-correspondence" in claims:
            consequences.add("stone-self-adjoint-correspondence")
        if "quantum-time-evolution" in claims:
            consequences.add("Hamiltonian-time-evolution-model")
        if "semigroup-generation-characterization" in claims or "closed-dense-plus-resolvent-powers-imply-c0-generation" in implications:
            consequences.add("generator-of-exponentially-bounded-c0-semigroup")
        if "contraction-generation-characterization" in claims or "closed-dense-plus-first-resolvent-bound-imply-contraction-generation" in implications:
            consequences.add("generator-of-contraction-c0-semigroup")
        if "dissipativity-characterization" in claims or "dissipativity-plus-range-condition-imply-contraction-generation" in implications:
            consequences.add("contraction-semigroup-via-dissipativity")
        if "cauchy-problem-equivalence" in claims or "c0-generation-iff-cauchy-well-posedness" in implications:
            consequences.add("well-posed-abstract-cauchy-problem")
        if "generator-closed-dense" in claims or "c0-generation-implies-closed-dense-generator" in implications:
            consequences.add("closed-densely-defined-generator")
        if "yosida-approximation-convergence" in claims or "resolvent-approximants-converge-to-generated-semigroup" in implications:
            consequences.add("bounded-generator-approximation-scheme")
        if "generator-uniqueness" in claims:
            consequences.add("unique-generator-for-semigroup")
        if "contraction-resolvent-monotonicity" in claims:
            consequences.add("resolvent-monotonicity")
        if is_theorem_like and not consequences and claims:
            consequences.update(_sort_signatures(claims)[:2])
        return _sort_signatures(consequences)

    if ontology_profile == ONTOLOGY_FUNCTIONAL_ANALYSIS_FIXED_POINT:
        claims = set(claim_signatures)
        implications = set(implication_signatures)
        if "compact-convex-set-definition" in claims:
            consequences.add("nonempty-compact-convex-subset")
        if "commuting-affine-family-definition" in claims:
            consequences.add("commuting-affine-family-on-compact-convex-set")
        if "invariant-fixed-point-subset-definition" in claims:
            consequences.add("invariant-fixed-point-subset")
        if "cesaro-average-preservation" in claims:
            consequences.add("affine-orbit-averages-in-compact-convex-set")
        if "single-affine-map-fixed-point" in claims or "affine-averaging-implies-single-map-fixed-point" in implications:
            consequences.add("single-map-fixed-point")
        if "fixed-point-subset-structure" in claims or "single-map-fixed-point-implies-invariant-fixed-point-subset" in implications:
            consequences.add("nonempty-compact-convex-fixed-point-subset")
        if "commuting-preserves-fixed-point-subset" in claims or "commutativity-implies-fixed-point-subset-invariance" in implications:
            consequences.add("invariant-fixed-point-subset-under-commuting-family")
        if "finite-family-common-fixed-point" in claims or "finite-intersection-property-implies-common-fixed-point" in implications:
            consequences.add("common-fixed-point-for-finite-commuting-family")
        if "markov-kakutani-common-fixed-point" in claims:
            consequences.add("common-fixed-point-for-commuting-family")
        if is_theorem_like and not consequences and claims:
            consequences.update(_sort_signatures(claims)[:2])
        return _sort_signatures(consequences)

    if ontology_profile == ONTOLOGY_FUNCTIONAL_ANALYSIS_MEASURE:
        claims = set(claim_signatures)
        implications = set(implication_signatures)
        if "regular-borel-measure-definition" in claims:
            consequences.add("regular-borel-measure-on-lch-space")
        if "compact-open-approximation-lemma" in claims:
            consequences.add("compact-open-regularity-witness")
        if "positive-functional-definition" in claims:
            consequences.add("positive-linear-functional-on-cc-space")
        if "integration-defines-positive-functional" in claims or "regular-measure-implies-positive-functional" in implications:
            consequences.add("positive-functional-via-integration")
        if "positive-functional-measure-existence" in claims or "positive-functional-implies-regular-measure" in implications:
            consequences.add("regular-borel-measure-representation")
        if "uniqueness-from-cc-separation" in claims or "function-separation-implies-measure-uniqueness" in implications:
            consequences.add("unique-representing-measure")
        if "riesz-markov-kakutani-correspondence" in claims:
            consequences.add("regular-borel-measure-representation")
            consequences.add("unique-representing-measure")
            consequences.add("functional-measure-correspondence")
        if "c0-dual-measure-representation" in claims or "c0-dual-implies-signed-regular-measure" in implications:
            consequences.add("signed-regular-measure-duality")
        if "total-variation-norm-identity" in claims or "total-variation-equals-dual-norm" in implications:
            consequences.add("dual-norm-total-variation")
        if is_theorem_like and not consequences and claims:
            consequences.update(_sort_signatures(claims)[:2])
        return _sort_signatures(consequences)

    if ontology_profile == ONTOLOGY_GENERIC_MATHEMATICS:
        claims = set(claim_signatures)
        if is_theorem_like and claims:
            consequences.update(_sort_signatures(claims)[:2])
        return _sort_signatures(consequences)

    classes = set(complexity_classes)
    problems = set(core_problems)
    claims = set(claim_signatures)
    implications = set(implication_signatures)
    specific_lower_bounds = _specific_lower_bound_signatures(core_problems, model_signatures, claim_signatures)

    if "NP-in-P/poly-implies-PH-collapse" in implications:
        consequences.add("PH-collapse-to-Sigma2")
    if "PIT-in-P-implies-lower-bounds" in implications:
        consequences.add("NEXP-vs-P/poly-or-Permanent-lower-bound")
    if "hardness-implies-PRG" in implications:
        consequences.add("PRG-for-poly-size-circuits")
    if "E-hardness-implies-BPP-equals-P" in implications:
        consequences.add("BPP-equals-P")
    if "hardness-yields-BPP-derandomization" in implications:
        consequences.add("BPP-derandomization")
    if "poly-bounded-proofs-iff-NP-equals-coNP" in implications:
        consequences.add("NP-equals-coNP")
    if "IPS-lower-bounds-imply-arithmetic-lower-bounds" in implications:
        consequences.add("Permanent-arithmetic-circuit-lower-bound")
    if "GapMCSP-lower-bounds-imply-NP-not-in-P/poly" in implications:
        consequences.add("NP-not-in-P/poly")
    if "mild-lower-bounds-imply-major-separation" in implications:
        consequences.add("major-separation")
    if "query-lower-bounds-imply-communication-lower-bounds" in implications:
        consequences.add("communication-lower-bound")
    if "local-reductions-preclude-MCSP-NP-completeness" in implications:
        consequences.add("MCSP-not-NP-complete")
    if "assumptions-imply-MCSP-NP-hardness" in implications:
        consequences.add("MCSP-NP-hardness")
    if "P-vs-NP-separation" in claims:
        consequences.add("P-not-equal-NP")
    if "NP-vs-P/poly-separation" in claims:
        consequences.add("NP-not-in-P/poly")
    if "NEXP-vs-ACC0" in claims:
        consequences.add("NEXP-not-in-ACC0")
    if "proof-system-characterization" in claims and "TAUT" in problems:
        consequences.add("TAUT-proof-system-characterization")
    if "random-function-lower-bound" in claims:
        consequences.add("almost-all-functions-are-hard")
    if "lower-bound" in claims and not consequences:
        if specific_lower_bounds:
            consequences.update(specific_lower_bounds[:2])
        else:
            consequences.add("restricted-model-lower-bound")
    if "NP-completeness" in claims:
        consequences.add("NP-complete-classification")
    if "NP-hardness" in claims and "MCSP" in problems:
        consequences.add("MCSP-hardness-transfer")

    if is_theorem_like and not consequences and claims:
        consequences.update(_sort_signatures(claims)[:2])
    return _sort_signatures(consequences)


def _infer_implication_signatures(
    complexity_classes: list[str],
    core_problems: list[str],
    model_signatures: list[str],
    reduction_signatures: list[str],
    claim_signatures: list[str],
    raw: str,
    clean: str,
    compact: str,
    ontology_profile: str,
) -> list[str]:
    """
    Relevance: Operates within the relational connector layer.
    Concept: Extraction of theorem schemas expressed as implication patterns.
    Contribution: Gives the framework a more precise target for abductive bridge search than broad regime labels alone.
    """

    implications: set[str] = set()

    if ontology_profile == ONTOLOGY_MATHEMATICAL_PHYSICS:
        claims = set(claim_signatures)
        if "OS-reconstruction" in claims and _contains_any_pattern(raw, clean, compact, ["wightman", "equivalence"]):
            implications.add("OS-axioms-imply-Wightman-QFT")
        if "reflection-positivity-transfer" in claims and _contains_any_pattern(raw, clean, compact, ["mass gap", "exponential decay", "correlator decay"]):
            implications.add("transfer-matrix-gap-implies-correlator-decay")
        if "constructive-existence" in claims and _contains_any_pattern(raw, clean, compact, ["without ultraviolet cutoffs", "continuum limit", "cutoff removal"]):
            implications.add("lattice-continuum-control-implies-constructive-QFT")
        if "mass-gap" in claims and _contains_any_pattern(raw, clean, compact, ["correlator decay", "exponential decay", "signature"]):
            implications.add("correlator-decay-signals-mass-gap")
        return _sort_signatures(implications)

    if ontology_profile == ONTOLOGY_FUNCTIONAL_ANALYSIS_SEMIGROUP:
        claims = set(claim_signatures)
        if "stone-unitary-group-correspondence" in claims and _contains_any_pattern(raw, clean, compact, ["iff", "if and only if"]):
            implications.add("unitary-group-implies-self-adjoint-generator")
            implications.add("self-adjoint-operator-implies-unitary-group")
        if "stone-unitary-group-correspondence" in claims and _contains_any_pattern(raw, clean, compact, ["unique self-adjoint operator", "unique selfadjoint operator"]):
            implications.add("unitary-group-implies-unique-self-adjoint-generator")
        if "spectral-calculus-unitary-realization" in claims:
            implications.add("spectral-theorem-enables-unitary-functional-calculus")
        if "semigroup-generation-characterization" in claims and _contains_any_pattern(raw, clean, compact, ["iff", "if and only if"]):
            implications.add("closed-dense-plus-resolvent-powers-imply-c0-generation")
        if "contraction-generation-characterization" in claims and _contains_any_pattern(raw, clean, compact, ["iff", "if and only if"]):
            implications.add("closed-dense-plus-first-resolvent-bound-imply-contraction-generation")
        if "dissipativity-characterization" in claims:
            implications.add("dissipativity-plus-range-condition-imply-contraction-generation")
        if "cauchy-problem-equivalence" in claims and _contains_any_pattern(raw, clean, compact, ["equivalent", "iff", "if and only if"]):
            implications.add("c0-generation-iff-cauchy-well-posedness")
        if "yosida-approximation-convergence" in claims:
            implications.add("resolvent-approximants-converge-to-generated-semigroup")
        if "generator-closed-dense" in claims:
            implications.add("c0-generation-implies-closed-dense-generator")
        return _sort_signatures(implications)

    if ontology_profile == ONTOLOGY_FUNCTIONAL_ANALYSIS_FIXED_POINT:
        claims = set(claim_signatures)
        if "cesaro-average-preservation" in claims:
            implications.add("affine-averaging-implies-single-map-fixed-point")
        if "single-affine-map-fixed-point" in claims:
            implications.add("single-map-fixed-point-implies-invariant-fixed-point-subset")
        if "fixed-point-subset-structure" in claims:
            implications.add("single-map-fixed-point-implies-invariant-fixed-point-subset")
        if "commuting-preserves-fixed-point-subset" in claims:
            implications.add("commutativity-implies-fixed-point-subset-invariance")
        if "finite-family-common-fixed-point" in claims:
            implications.add("finite-intersection-property-implies-common-fixed-point")
        if "markov-kakutani-common-fixed-point" in claims:
            implications.add("finite-intersection-property-implies-common-fixed-point")
        return _sort_signatures(implications)

    if ontology_profile == ONTOLOGY_FUNCTIONAL_ANALYSIS_MEASURE:
        claims = set(claim_signatures)
        if "positive-functional-measure-existence" in claims:
            implications.add("positive-functional-implies-regular-measure")
        if "riesz-markov-kakutani-correspondence" in claims:
            implications.add("positive-functional-implies-regular-measure")
        if "compact-open-approximation-lemma" in claims:
            implications.add("compact-open-approximation-supports-regularity")
        if "integration-defines-positive-functional" in claims:
            implications.add("regular-measure-implies-positive-functional")
        if "uniqueness-from-cc-separation" in claims:
            implications.add("function-separation-implies-measure-uniqueness")
        if "c0-dual-measure-representation" in claims:
            implications.add("c0-dual-implies-signed-regular-measure")
        if "total-variation-norm-identity" in claims:
            implications.add("total-variation-equals-dual-norm")
        return _sort_signatures(implications)

    if ontology_profile == ONTOLOGY_GENERIC_MATHEMATICS:
        if _contains_any_pattern(raw, clean, compact, ["if and only if", "iff"]):
            implications.add("equivalence-schema")
        return _sort_signatures(implications)

    classes = set(complexity_classes)
    problems = set(core_problems)
    models = set(model_signatures)
    reductions = set(reduction_signatures)
    claims = set(claim_signatures)

    if "NP" in classes and "P/poly" in classes and "PH" in classes and "PH-collapse" in claims:
        implications.add("NP-in-P/poly-implies-PH-collapse")
    if "PIT" in problems and _contains_any_pattern(raw, clean, compact, ["pit in pclass", "pit in p", "pitinpclass", "pitinp"]) and _contains_any_pattern(
        raw,
        clean,
        compact,
        ["nexp", "permanent", "lower bounds", "one of the following"],
    ):
        implications.add("PIT-in-P-implies-lower-bounds")
    if _contains_any_pattern(raw, clean, compact, ["pseudorandom generator", "fooling polynomial-size circuits"]) and _contains_any_pattern(
        raw,
        clean,
        compact,
        ["hardness", "worst-case-to-average-case", "explicit function"],
    ):
        implications.add("hardness-implies-PRG")
    if "E" in classes and "BPP" in classes and "P" in classes and _contains_any_pattern(raw, clean, compact, ["bpp=pclass", "bpp = pclass", "bpp collapses to pclass"]):
        implications.add("E-hardness-implies-BPP-equals-P")
    if "proof-system-characterization" in claims and "NP" in classes and "coNP" in classes:
        implications.add("poly-bounded-proofs-iff-NP-equals-coNP")
    if "IPS" in models and _contains_any_pattern(raw, clean, compact, ["permanent", "vp", "vnp", "arithmetic circuits"]):
        implications.add("IPS-lower-bounds-imply-arithmetic-lower-bounds")
    if "Gap-MCSP" in problems and "NP" in classes and "P/poly" in classes and _contains_any_pattern(raw, clean, compact, ["notsubseteq", "major consequences"]):
        implications.add("GapMCSP-lower-bounds-imply-NP-not-in-P/poly")
    if "hardness-magnification" in claims and _contains_any_pattern(raw, clean, compact, ["major lower bound", "major consequences", "strong model"]):
        implications.add("mild-lower-bounds-imply-major-separation")
    if "MCSP" in problems and _contains_any_pattern(raw, clean, compact, ["szk", "reduces to mcsp"]):
        implications.add("SZK-reduces-to-MCSP")
    if "MCSP-local-nonhardness" in claims:
        implications.add("local-reductions-preclude-MCSP-NP-completeness")
    if "MCSP-NP-hardness" in claims and _contains_any_pattern(raw, clean, compact, ["assuming", "hypotheses", "assumptions"]):
        implications.add("assumptions-imply-MCSP-NP-hardness")
    if "query-to-communication-lifting" in reductions and "communication-protocol" in models and "decision-tree" in models:
        implications.add("query-lower-bounds-imply-communication-lower-bounds")
    if "IPS-lower-bounds-imply-arithmetic-lower-bounds" in implications or (
        "arithmetic-circuits" in models and _contains_any_pattern(raw, clean, compact, ["implies", "consequences"])
    ):
        implications.add("proof-lower-bounds-imply-circuit-lower-bounds")
    if "BPP" in classes and "P" in classes and _contains_any_pattern(raw, clean, compact, ["bpp=pclass", "collapse of bpp to pclass"]):
        implications.add("hardness-yields-BPP-derandomization")

    return sorted(implications)


def _specificity_score(profile: dict[str, Any]) -> float:
    """
    Relevance: Operates within the relational connector layer.
    Concept: Measurement of how mathematically specific a statement profile is.
    Contribution: Prioritizes statements with explicit theorem schemas and model commitments over generic topical tags.
    """

    claim_count = len(profile.get("claim_signatures", []))
    model_count = len(profile.get("model_signatures", []))
    reduction_count = len(profile.get("reduction_signatures", []))
    implication_count = len(profile.get("implication_signatures", []))
    antecedent_count = len(profile.get("antecedent_signatures", []))
    consequence_count = len(profile.get("consequence_signatures", []))
    return _clamp01(
        0.24 * min(1.0, claim_count / 2.0)
        + 0.18 * min(1.0, model_count / 2.0)
        + 0.10 * min(1.0, reduction_count / 1.0)
        + 0.20 * min(1.0, implication_count / 1.0)
        + 0.14 * min(1.0, antecedent_count / 1.0)
        + 0.14 * min(1.0, consequence_count / 1.0)
    )


def _map_concepts(source: set[str], mapping: dict[str, str]) -> set[str]:
    """
    Relevance: Operates within the relational connector layer.
    Concept: Internal helper implementing one deterministic step of this stage.
    Contribution: Projects low-level tokens into a typed mathematical concept ontology.
    """

    out: set[str] = set()
    for token in source:
        t = str(token).strip().lower()
        if not t:
            continue
        for stem, concept in mapping.items():
            if t == stem or (len(stem) >= 5 and t.startswith(stem)):
                out.add(concept)
    return out


def _profile_score(profile: dict[str, Any], kind: str, ontology_profile: str) -> float:
    """
    Relevance: Operates within the relational connector layer.
    Concept: Quantitative evaluation of hypotheses or theory-graph properties.
    Contribution: Encodes mathematical centrality preferences for intervention ranking.
    """

    kind_l = str(kind).strip().lower()
    kind_weight = 0.45
    if kind_l == "theorem":
        kind_weight = 1.0
    elif kind_l in {"lemma", "corollary"}:
        kind_weight = 0.85
    elif kind_l == "observation":
        kind_weight = 0.75
    elif kind_l in {"definition", "axiom"}:
        kind_weight = 0.55

    classes = set(profile.get("complexity_classes", []))
    problems = set(profile.get("core_problems", []))
    regimes = set(profile.get("proof_regimes", []))
    barriers = set(profile.get("barrier_signals", []))
    specificity_relevance = _specificity_score(profile)
    implication_relevance = min(1.0, len(profile.get("implication_signatures", [])))

    target_classes, target_problems, target_regimes = _target_tag_sets_for_profile(ontology_profile)
    class_relevance = min(1.0, len(classes & target_classes) / 2.0) if target_classes else 0.0
    problem_relevance = min(1.0, len(problems & target_problems) / 2.0) if target_problems else 0.0
    regime_relevance = min(1.0, len(regimes & target_regimes) / 2.0) if target_regimes else 0.0
    barrier_relevance = 1.0 if barriers else 0.0

    return _clamp01(
        0.34 * kind_weight
        + 0.24 * specificity_relevance
        + 0.18 * implication_relevance
        + 0.10 * class_relevance
        + 0.07 * problem_relevance
        + 0.05 * regime_relevance
        + 0.02 * barrier_relevance
    )


def _concept_focus(profile: dict[str, Any], limit: int = 4) -> list[str]:
    """
    Relevance: Operates within the relational connector layer.
    Concept: Extraction of structured signals from raw text or artifact payloads.
    Contribution: Produces compact, human-readable mathematical concept anchors.
    """

    focus: list[str] = []
    for key in (
        "implication_signatures",
        "antecedent_signatures",
        "consequence_signatures",
        "claim_signatures",
        "model_signatures",
        "reduction_signatures",
        "complexity_classes",
        "core_problems",
        "proof_regimes",
        "barrier_signals",
    ):
        for concept in profile.get(key, []):
            c = str(concept).strip()
            if c and c not in focus:
                focus.append(c)
            if len(focus) >= limit:
                return focus
    return focus


def _profile_overlap(a: dict[str, Any], b: dict[str, Any]) -> dict[str, float]:
    """
    Relevance: Operates within the relational connector layer.
    Concept: Quantitative evaluation of hypotheses or theory-graph properties.
    Contribution: Computes typed concept alignment between statement profiles.
    """

    claim_overlap = _jaccard(set(a.get("claim_signatures", [])), set(b.get("claim_signatures", [])))
    model_overlap = _jaccard(set(a.get("model_signatures", [])), set(b.get("model_signatures", [])))
    reduction_overlap = _jaccard(set(a.get("reduction_signatures", [])), set(b.get("reduction_signatures", [])))
    implication_overlap = _jaccard(set(a.get("implication_signatures", [])), set(b.get("implication_signatures", [])))
    antecedent_overlap = _jaccard(set(a.get("antecedent_signatures", [])), set(b.get("antecedent_signatures", [])))
    consequence_overlap = _jaccard(set(a.get("consequence_signatures", [])), set(b.get("consequence_signatures", [])))
    class_overlap = _jaccard(set(a.get("complexity_classes", [])), set(b.get("complexity_classes", [])))
    problem_overlap = _jaccard(set(a.get("core_problems", [])), set(b.get("core_problems", [])))
    regime_overlap = _jaccard(set(a.get("proof_regimes", [])), set(b.get("proof_regimes", [])))
    barrier_overlap = _jaccard(set(a.get("barrier_signals", [])), set(b.get("barrier_signals", [])))
    ontology_overlap = _jaccard(set(a.get("all_tags", [])), set(b.get("all_tags", [])))
    overall = _clamp01(
        0.18 * claim_overlap
        + 0.16 * model_overlap
        + 0.12 * reduction_overlap
        + 0.16 * implication_overlap
        + 0.10 * antecedent_overlap
        + 0.10 * consequence_overlap
        + 0.10 * class_overlap
        + 0.08 * problem_overlap
        + 0.08 * regime_overlap
        + 0.04 * barrier_overlap
        + 0.01 * ontology_overlap
    )
    return {
        "overall": overall,
        "claim_overlap": claim_overlap,
        "model_overlap": model_overlap,
        "reduction_overlap": reduction_overlap,
        "implication_overlap": implication_overlap,
        "antecedent_overlap": antecedent_overlap,
        "consequence_overlap": consequence_overlap,
        "class_overlap": class_overlap,
        "problem_overlap": problem_overlap,
        "regime_overlap": regime_overlap,
        "barrier_overlap": barrier_overlap,
        "ontology_overlap": ontology_overlap,
    }


def _candidate_profile_snapshot(profile: dict[str, Any]) -> dict[str, Any]:
    """
    Relevance: Operates within the relational connector layer.
    Concept: Stable projection of rich statement profiles into connector-candidate payloads.
    Contribution: Keeps downstream bridge generation and reporting deterministic across both inferred and declared edges.
    """

    return {
        "claim_signatures": profile.get("claim_signatures", []),
        "model_signatures": profile.get("model_signatures", []),
        "reduction_signatures": profile.get("reduction_signatures", []),
        "implication_signatures": profile.get("implication_signatures", []),
        "antecedent_signatures": profile.get("antecedent_signatures", []),
        "consequence_signatures": profile.get("consequence_signatures", []),
        "core_problems": profile.get("core_problems", []),
        "complexity_classes": profile.get("complexity_classes", []),
        "barrier_signals": profile.get("barrier_signals", []),
        "statement_phase": profile.get("statement_phase", ""),
        "bridge_roles": profile.get("bridge_roles", []),
        "ontology_profile": profile.get("ontology_profile", ""),
    }


def _nearest_heading(position: int, headings: list[tuple[int, str]]) -> str:
    """
    Relevance: Operates within the relational connector layer.
    Concept: Internal helper implementing one deterministic step of this stage.
    Contribution: Contributes a deterministic transformation that supports end-to-end reasoning reproducibility.
    """

    current = "Unspecified"
    for start, title in headings:
        if start > position:
            break
        current = title
    return current


def _normalize_list(value: Any) -> list[str]:
    """
    Relevance: Operates within the relational connector layer.
    Concept: Normalization of input structures into stable internal forms.
    Contribution: Reduces runtime ambiguity and prevents malformed artifacts from destabilizing the workflow.
    """

    if value is None:
        return []
    if isinstance(value, list):
        return [str(x).strip() for x in value if str(x).strip()]
    text = str(value).strip()
    if not text:
        return []
    if "," in text:
        return [chunk.strip() for chunk in text.split(",") if chunk.strip()]
    return [text]


def _clean_notes_text(notes: str) -> str:
    """
    Relevance: Operates within the relational connector layer.
    Concept: Sanitization of metadata-heavy note fields before semantic extraction.
    Contribution: Prevents section headers and citation scaffolding from contaminating mathematical concept profiles.
    """

    cleaned: list[str] = []
    for raw_line in str(notes).splitlines():
        line = raw_line.strip()
        if not line:
            continue
        if ":" in line:
            key, value = line.split(":", 1)
            key_l = key.strip().lower()
            if key_l in {"parsed_env", "section", "source_citation", "source_marker", "normalization"}:
                continue
            if key_l == "label":
                line = value.strip()
        cleaned.append(line)
    return " ".join(cleaned)


def _tokenize(text: str) -> set[str]:
    """
    Relevance: Operates within the relational connector layer.
    Concept: Lightweight semantic feature computation for graph reasoning heuristics.
    Contribution: Contributes a deterministic transformation that supports end-to-end reasoning reproducibility.
    """

    text = text.replace("\\", " ")
    text = text.replace("{", " ").replace("}", " ")
    tokens = set()
    for token in TOKEN_PATTERN.findall(text.lower()):
        if len(token) < 2:
            continue
        if token in STOPWORDS:
            continue
        tokens.add(token)
    return tokens


def _id_signature(statement_id: str) -> set[str]:
    """
    Relevance: Operates within the relational connector layer.
    Concept: Lightweight semantic feature computation for graph reasoning heuristics.
    Contribution: Contributes a deterministic transformation that supports end-to-end reasoning reproducibility.
    """

    out: set[str] = set()
    raw = statement_id.lower().replace("st.", "")
    for token in ID_TOKEN_PATTERN.findall(raw):
        if len(token) <= 2 or token in {"def", "thm", "lem", "obs", "item"}:
            continue
        out.add(token)
    return out


def _method_tags(tokens: set[str], id_tokens: set[str], ontology_profile: str) -> set[str]:
    """
    Relevance: Operates within the relational connector layer.
    Concept: Internal helper implementing one deterministic step of this stage.
    Contribution: Contributes a deterministic transformation that supports end-to-end reasoning reproducibility.
    """

    if ontology_profile == ONTOLOGY_COMPLEXITY:
        mapping = METHOD_TOKEN_MAP
    elif ontology_profile == ONTOLOGY_MATHEMATICAL_PHYSICS:
        mapping = PHYSICS_METHOD_TOKEN_MAP
    elif ontology_profile == ONTOLOGY_FUNCTIONAL_ANALYSIS_FIXED_POINT:
        mapping = FIXED_POINT_METHOD_TOKEN_MAP
    elif ontology_profile == ONTOLOGY_FUNCTIONAL_ANALYSIS_MEASURE:
        mapping = MEASURE_METHOD_TOKEN_MAP
    elif ontology_profile == ONTOLOGY_FUNCTIONAL_ANALYSIS_SEMIGROUP:
        mapping = SEMIGROUP_METHOD_TOKEN_MAP
    else:
        mapping = GENERIC_METHOD_TOKEN_MAP

    tags: set[str] = set()
    for tok in tokens | id_tokens:
        for stem, tag in mapping.items():
            if stem in tok:
                tags.add(tag)
    return tags


def _latex_symbol_tokens(latex: str) -> set[str]:
    """
    Relevance: Operates within the relational connector layer.
    Concept: Extraction of structured signals from raw text or artifact payloads.
    Contribution: Adds symbol-level mathematical semantics beyond plain lexical overlap.
    """

    out: set[str] = set()
    for cmd in LATEX_COMMAND_PATTERN.findall(latex):
        c = cmd.strip().lower()
        if c and c not in STOPWORDS:
            out.add(c)
    for sym in LATEX_SYMBOL_PATTERN.findall(latex):
        s = sym.strip().lower()
        if s and s not in STOPWORDS and len(s) > 0:
            out.add(s)
    return out


def _concept_role_tokens(roles: list[str]) -> set[str]:
    """
    Relevance: Operates within the relational connector layer.
    Concept: Extraction of structured signals from raw text or artifact payloads.
    Contribution: Captures coarse symbol-role alignment signals from concept role annotations.
    """

    out: set[str] = set()
    for role in roles:
        r = str(role).strip().lower()
        if not r:
            continue
        for tok in re.split(r"[^a-z0-9_]+", r):
            if tok and tok not in STOPWORDS and len(tok) > 1:
                out.add(tok)
    return out


def _infer_concept_profile(
    tokens: set[str],
    id_tokens: set[str],
    latex_symbols: set[str],
    role_tokens: set[str],
    statement_phase: str,
    bridge_roles: list[str],
    method_tags: set[str],
    raw_text: str,
    section: str,
    kind: str,
    barrier_family: str,
    is_barrier: bool,
    ontology_profile: str,
) -> dict[str, Any]:
    """
    Relevance: Operates within the relational connector layer.
    Concept: Extraction of structured signals from raw text or artifact payloads.
    Contribution: Produces a typed mathematical profile used across scoring, logs, and reports.
    """

    phase_tokens = _tokenize(statement_phase)
    bridge_role_tokens = _concept_role_tokens(bridge_roles)
    source_tokens = set(tokens) | set(id_tokens) | set(latex_symbols) | set(role_tokens) | set(phase_tokens) | set(bridge_role_tokens) | set(method_tags)
    section_tokens = _tokenize(section)
    raw, clean, compact = _text_forms(raw_text)
    if ontology_profile == ONTOLOGY_COMPLEXITY:
        complexity_classes = sorted(_map_concepts(source_tokens, CLASS_CONCEPT_MAP))
        core_problems = sorted(_map_concepts(source_tokens, PROBLEM_CONCEPT_MAP))
        proof_regimes = sorted(_map_concepts(source_tokens | section_tokens, REGIME_CONCEPT_MAP))
    elif ontology_profile == ONTOLOGY_MATHEMATICAL_PHYSICS:
        complexity_classes = []
        core_problem_set = set(_map_concepts(source_tokens | section_tokens, PHYSICS_OBJECT_CONCEPT_MAP))
        if _contains_any_pattern(raw, clean, compact, ["mass gap", "mass-gap"]):
            core_problem_set.add("mass-gap")
        if _contains_any_pattern(raw, clean, compact, ["yang-mills"]):
            core_problem_set.add("Yang-Mills")
        if _contains_any_pattern(raw, clean, compact, ["continuum limit"]):
            core_problem_set.add("continuum-limit")
        proof_regimes = sorted(_map_concepts(source_tokens | section_tokens, PHYSICS_REGIME_CONCEPT_MAP))
        core_problems = sorted(core_problem_set)
    elif ontology_profile == ONTOLOGY_FUNCTIONAL_ANALYSIS_FIXED_POINT:
        complexity_classes = []
        core_problem_set = set(_map_concepts(source_tokens | section_tokens, FIXED_POINT_OBJECT_CONCEPT_MAP))
        if _contains_any_pattern(raw, clean, compact, ["markov-kakutani", "common fixed point theorem"]):
            core_problem_set.add("Markov-Kakutani")
        if _contains_any_pattern(raw, clean, compact, ["common fixed point", "fixed by every t"]):
            core_problem_set.add("common-fixed-point")
        if _contains_any_pattern(raw, clean, compact, ["compact convex subset", "compact convex set"]):
            core_problem_set.add("compact-convex-set")
        if _contains_any_pattern(raw, clean, compact, ["commuting family", "continuous affine self-maps", "pairwise commuting"]):
            core_problem_set.add("commuting-affine-family")
        if _contains_any_pattern(raw, clean, compact, ["fix(t)", "fixed-point subset", "set of fixed points"]):
            core_problem_set.add("invariant-fixed-point-subset")
        if _contains_any_pattern(raw, clean, compact, ["cesaro average", "orbit average", "a_n(x)"]):
            core_problem_set.add("Cesaro-averaging")
        if _contains_any_pattern(raw, clean, compact, ["finite intersection property", "finite intersection"]):
            core_problem_set.add("finite-intersection-property")
        proof_regimes = sorted(set(method_tags) | _map_concepts(source_tokens | section_tokens, FIXED_POINT_REGIME_CONCEPT_MAP))
        core_problems = sorted(core_problem_set)
    elif ontology_profile == ONTOLOGY_FUNCTIONAL_ANALYSIS_MEASURE:
        complexity_classes = []
        core_problem_set = set(_map_concepts(source_tokens | section_tokens, MEASURE_OBJECT_CONCEPT_MAP))
        if _contains_any_pattern(raw, clean, compact, ["riesz-markov-kakutani", "representation theorem"]):
            core_problem_set.add("Riesz-Markov-Kakutani")
        if _contains_any_pattern(raw, clean, compact, ["regular borel measure", "radon measure", "regular measure"]):
            core_problem_set.add("regular-Borel-measure")
        if _contains_any_pattern(raw, clean, compact, ["positive linear functional", "positive functional"]):
            core_problem_set.add("positive-linear-functional")
        if _contains_any_pattern(raw, clean, compact, ["c_c(x)", "cc(x)", "compactly supported continuous", "compact support"]):
            core_problem_set.add("C_c-space")
        if _contains_any_pattern(raw, clean, compact, ["c_0(x)", "c0(x)", "vanishing at infinity"]):
            core_problem_set.add("C0-dual")
        if _contains_any_pattern(raw, clean, compact, ["locally compact hausdorff", "lch space"]):
            core_problem_set.add("locally-compact-Hausdorff-space")
        if _contains_any_pattern(raw, clean, compact, ["integration against", "represented by integration", "d\\mu"]):
            core_problem_set.add("integration-pairing")
        if _contains_any_pattern(raw, clean, compact, ["total variation", "jordan decomposition", "signed measure"]):
            core_problem_set.add("total-variation")
        proof_regimes = sorted(set(method_tags) | _map_concepts(source_tokens | section_tokens, MEASURE_REGIME_CONCEPT_MAP))
        core_problems = sorted(core_problem_set)
    elif ontology_profile == ONTOLOGY_FUNCTIONAL_ANALYSIS_SEMIGROUP:
        complexity_classes = []
        core_problem_set = set(_map_concepts(source_tokens | section_tokens, SEMIGROUP_OBJECT_CONCEPT_MAP))
        if _contains_any_pattern(raw, clean, compact, ["c_0-semigroup", "c0-semigroup"]):
            core_problem_set.add("C0-semigroup")
        if _contains_any_pattern(raw, clean, compact, ["one-parameter unitary group", "one parameter unitary group", "strongly continuous unitary group"]):
            core_problem_set.add("unitary-group")
        if _contains_any_pattern(raw, clean, compact, ["generator", "d(a)"]):
            core_problem_set.add("generator")
        if _contains_any_pattern(raw, clean, compact, ["resolvent", "rho(a)", "(lambda i - a)^-1", "(lambda i-a)^-1"]):
            core_problem_set.add("resolvent")
        if _contains_any_pattern(raw, clean, compact, ["abstract cauchy problem", "mild solution"]):
            core_problem_set.add("abstract-Cauchy-problem")
        if _contains_any_pattern(raw, clean, compact, ["yosida approximation", "approximants"]):
            core_problem_set.add("Yosida-approximation")
        if _contains_any_pattern(raw, clean, compact, ["contraction semigroup", "||t(t)|| <= 1"]):
            core_problem_set.add("contraction-semigroup")
        if _contains_any_pattern(raw, clean, compact, ["self-adjoint operator", "selfadjoint", "skew-adjoint", "skewadjoint"]):
            core_problem_set.add("self-adjoint-operator")
        if _contains_any_pattern(raw, clean, compact, ["spectral theorem", "functional calculus", "projection-valued measure"]):
            core_problem_set.add("spectral-theorem")
        if _contains_any_pattern(raw, clean, compact, ["stone's theorem", "stone theorem"]):
            core_problem_set.add("Stone-correspondence")
        proof_regimes = sorted(set(method_tags) | _map_concepts(source_tokens | section_tokens, SEMIGROUP_REGIME_CONCEPT_MAP))
        core_problems = sorted(core_problem_set)
    else:
        complexity_classes = []
        core_problems = []
        proof_regimes = sorted(set(method_tags) | _map_concepts(source_tokens | section_tokens, GENERIC_METHOD_TOKEN_MAP))
    barrier_signals = _infer_barrier_signals(raw, clean, compact, barrier_family, is_barrier, ontology_profile)
    model_signatures = _infer_model_signatures(source_tokens, raw, clean, compact, ontology_profile)
    reduction_signatures = _infer_reduction_signatures(raw, clean, compact)
    claim_signatures = _infer_claim_signatures(
        complexity_classes=complexity_classes,
        core_problems=core_problems,
        model_signatures=model_signatures,
        reduction_signatures=reduction_signatures,
        barrier_signals=barrier_signals,
        method_tags=sorted(method_tags),
        raw=raw,
        clean=clean,
        compact=compact,
        ontology_profile=ontology_profile,
    )
    implication_signatures = _infer_implication_signatures(
        complexity_classes=complexity_classes,
        core_problems=core_problems,
        model_signatures=model_signatures,
        reduction_signatures=reduction_signatures,
        claim_signatures=claim_signatures,
        raw=raw,
        clean=clean,
        compact=compact,
        ontology_profile=ontology_profile,
    )
    antecedent_signatures = _infer_antecedent_signatures(
        kind=kind,
        complexity_classes=complexity_classes,
        core_problems=core_problems,
        model_signatures=model_signatures,
        reduction_signatures=reduction_signatures,
        claim_signatures=claim_signatures,
        implication_signatures=implication_signatures,
        raw=raw,
        clean=clean,
        compact=compact,
        ontology_profile=ontology_profile,
    )
    consequence_signatures = _infer_consequence_signatures(
        kind=kind,
        complexity_classes=complexity_classes,
        core_problems=core_problems,
        model_signatures=model_signatures,
        claim_signatures=claim_signatures,
        implication_signatures=implication_signatures,
        raw=raw,
        clean=clean,
        compact=compact,
        ontology_profile=ontology_profile,
    )
    specific_tags = sorted(
        set(claim_signatures)
        | set(model_signatures)
        | set(reduction_signatures)
        | set(implication_signatures)
        | set(antecedent_signatures)
        | set(consequence_signatures)
    )
    all_tags = sorted(
        set(specific_tags) | set(complexity_classes) | set(core_problems) | set(proof_regimes) | set(barrier_signals)
    )
    profile = {
        "claim_signatures": claim_signatures,
        "model_signatures": model_signatures,
        "reduction_signatures": reduction_signatures,
        "implication_signatures": implication_signatures,
        "antecedent_signatures": antecedent_signatures,
        "consequence_signatures": consequence_signatures,
        "specific_tags": specific_tags,
        "complexity_classes": complexity_classes,
        "core_problems": core_problems,
        "proof_regimes": proof_regimes,
        "barrier_signals": barrier_signals,
        "statement_phase": statement_phase,
        "bridge_roles": bridge_roles,
        "all_tags": all_tags,
        "focus": _concept_focus(
            {
                "claim_signatures": claim_signatures,
                "model_signatures": model_signatures,
                "reduction_signatures": reduction_signatures,
                "implication_signatures": implication_signatures,
                "antecedent_signatures": antecedent_signatures,
                "consequence_signatures": consequence_signatures,
                "complexity_classes": complexity_classes,
                "core_problems": core_problems,
                "proof_regimes": proof_regimes,
                "barrier_signals": barrier_signals,
            }
        ),
        "specificity_score": round(
            _specificity_score(
                {
                    "claim_signatures": claim_signatures,
                    "model_signatures": model_signatures,
                    "reduction_signatures": reduction_signatures,
                    "implication_signatures": implication_signatures,
                    "antecedent_signatures": antecedent_signatures,
                    "consequence_signatures": consequence_signatures,
                }
            ),
            6,
        ),
        "profile_score": round(
            _profile_score(
                {
                    "claim_signatures": claim_signatures,
                    "model_signatures": model_signatures,
                    "reduction_signatures": reduction_signatures,
                    "implication_signatures": implication_signatures,
                    "antecedent_signatures": antecedent_signatures,
                    "consequence_signatures": consequence_signatures,
                    "complexity_classes": complexity_classes,
                    "core_problems": core_problems,
                    "proof_regimes": proof_regimes,
                    "barrier_signals": barrier_signals,
                },
                kind=kind,
                ontology_profile=ontology_profile,
            ),
            6,
        ),
        "ontology_profile": ontology_profile,
    }
    return profile


def _chargram_counter(tokens: set[str], n: int = 3) -> Counter[str]:
    """
    Relevance: Operates within the relational connector layer.
    Concept: Lightweight semantic feature computation for graph reasoning heuristics.
    Contribution: Provides deterministic pseudo-embedding similarity without external model dependencies.
    """

    grams: Counter[str] = Counter()
    for token in tokens:
        t = f"^{token}$"
        if len(t) <= n:
            grams[t] += 1
            continue
        for i in range(len(t) - n + 1):
            grams[t[i : i + n]] += 1
    return grams


def _cosine_counter(a: Counter[str], b: Counter[str]) -> float:
    """
    Relevance: Operates within the relational connector layer.
    Concept: Lightweight semantic feature computation for graph reasoning heuristics.
    Contribution: Supplies normalized similarity for theorem-family signature matching.
    """

    if not a or not b:
        return 0.0
    dot = 0.0
    for key, val in a.items():
        dot += float(val) * float(b.get(key, 0))
    if dot <= 0:
        return 0.0
    na = sum(float(v) ** 2 for v in a.values()) ** 0.5
    nb = sum(float(v) ** 2 for v in b.values()) ** 0.5
    if na <= 0 or nb <= 0:
        return 0.0
    return max(0.0, min(1.0, dot / (na * nb)))


def _theorem_family_embedding_similarity(sig_a: set[str], sig_b: set[str]) -> float:
    """
    Relevance: Operates within the relational connector layer.
    Concept: Lightweight semantic feature computation for graph reasoning heuristics.
    Contribution: Approximates theorem-family embedding similarity for deeper cross-vocabulary matches.
    """

    return _cosine_counter(_chargram_counter(sig_a), _chargram_counter(sig_b))


def _equivalence_or_reduction_signal(tokens_a: set[str], tokens_b: set[str], id_a: set[str], id_b: set[str]) -> float:
    """
    Relevance: Operates within the relational connector layer.
    Concept: Internal helper implementing one deterministic step of this stage.
    Contribution: Contributes a deterministic transformation that supports end-to-end reasoning reproducibility.
    """

    markers = {"equivalent", "iff", "reduction", "reduces", "complete", "simulation", "normal", "canonical"}
    overlap = (tokens_a & tokens_b) | (id_a & id_b)
    marker_hits = sum(1 for t in overlap if any(m in t for m in markers))
    if marker_hits <= 0:
        return 0.0
    return min(1.0, 0.35 + 0.15 * marker_hits)


def _definitional_expansion_signal(
    a: dict[str, Any],
    b: dict[str, Any],
    structural_similarity: float,
    symbol_alignment: float,
) -> float:
    """
    Relevance: Operates within the relational connector layer.
    Concept: Internal helper implementing one deterministic step of this stage.
    Contribution: Contributes a deterministic transformation that supports end-to-end reasoning reproducibility.
    """

    if structural_similarity < 0.08:
        return 0.0
    kinds = {str(a.get("kind", "")).lower(), str(b.get("kind", "")).lower()}
    if "definition" not in kinds:
        return 0.0
    return _clamp01(0.30 + 0.45 * structural_similarity + 0.25 * symbol_alignment)


def _clamp01(value: float) -> float:
    """
    Relevance: Operates within the relational connector layer.
    Concept: Internal helper implementing one deterministic step of this stage.
    Contribution: Contributes a deterministic transformation that supports end-to-end reasoning reproducibility.
    """

    return max(0.0, min(1.0, value))


def _extract_statements(
    kb_content: str,
    ontology_profile: str,
) -> tuple[dict[str, dict[str, Any]], list[str]]:
    """
    Relevance: Operates within the relational connector layer.
    Concept: Extraction of structured signals from raw text or artifact payloads.
    Contribution: Provides clean, typed inputs so downstream reasoning steps remain auditable.
    """

    headings = [(m.start(), m.group(1).strip()) for m in HEADING_PATTERN.finditer(kb_content)]
    statements: dict[str, dict[str, Any]] = {}
    duplicates: list[str] = []

    for match in STATEMENT_BLOCK_PATTERN.finditer(kb_content):
        try:
            payload = yaml.safe_load(match.group(1))
        except yaml.YAMLError:
            continue
        if not isinstance(payload, dict):
            continue

        statement_id = str(payload.get("id", "")).strip()
        kind = str(payload.get("kind", "")).strip().lower()
        if not statement_id or not kind:
            continue

        if statement_id in statements:
            duplicates.append(statement_id)
            continue

        latex = str(payload.get("latex", "")).strip()
        informal = str(payload.get("informal", "")).strip()
        notes = str(payload.get("notes", "")).strip()
        cleaned_notes = _clean_notes_text(notes)
        combined = " ".join([latex, informal, cleaned_notes])
        tokens = _tokenize(combined)
        id_tokens = _id_signature(statement_id)
        latex_symbols = _latex_symbol_tokens(latex)
        used_symbols = _normalize_list(payload.get("used_symbols"))
        concept_roles = _normalize_list(payload.get("concept_roles"))
        statement_phase = str(payload.get("statement_phase", "")).strip().lower()
        bridge_roles = [str(role).strip().lower() for role in _normalize_list(payload.get("bridge_roles")) if str(role).strip()]
        role_tokens = _concept_role_tokens(concept_roles + bridge_roles + ([statement_phase] if statement_phase else []))
        method_tags = {str(tag).strip().lower() for tag in _normalize_list(payload.get("method_tags")) if str(tag).strip()}
        method_tags |= _method_tags(tokens, id_tokens, ontology_profile)
        explicit_barrier_family = str(payload.get("barrier_family", "")).strip().lower()
        explicit_barrier_flag = bool(payload.get("is_barrier")) or bool(explicit_barrier_family)
        structured_barrier_flag = any("barrier" in role.lower() for role in concept_roles + bridge_roles)
        section = _nearest_heading(match.start(), headings)
        family_signature = sorted(set(id_tokens) | set(method_tags) | set(latex_symbols) | set(role_tokens))
        concept_profile = _infer_concept_profile(
            tokens=tokens,
            id_tokens=id_tokens,
            latex_symbols=latex_symbols,
            role_tokens=role_tokens,
            statement_phase=statement_phase,
            bridge_roles=bridge_roles,
            method_tags=method_tags,
            raw_text=" ".join(
                [
                    statement_id,
                    latex,
                    informal,
                    cleaned_notes,
                    " ".join(concept_roles),
                    statement_phase,
                    " ".join(bridge_roles),
                    " ".join(sorted(method_tags)),
                ]
            ),
            section=section,
            kind=kind,
            barrier_family=explicit_barrier_family,
            is_barrier=bool(explicit_barrier_flag or structured_barrier_flag),
            ontology_profile=ontology_profile,
        )

        statements[statement_id] = {
            "id": statement_id,
            "kind": kind,
            "status": str(payload.get("status", "tentative")).strip().lower(),
            "depends_on": _normalize_list(payload.get("depends_on")),
            "source_ids": _normalize_list(payload.get("source_ids")),
            "used_symbols": sorted(set(used_symbols + concept_roles)),
            "concept_roles": concept_roles,
            "statement_phase": statement_phase,
            "bridge_roles": bridge_roles,
            "latex_symbols": sorted(latex_symbols),
            "role_tokens": sorted(role_tokens),
            "section": section,
            "tokens": tokens,
            "id_tokens": id_tokens,
            "method_tags": sorted(method_tags),
            "family_signature": family_signature,
            "text": combined,
            "barrier_family": explicit_barrier_family,
            "is_barrier": bool(explicit_barrier_flag or structured_barrier_flag),
            "concept_profile": concept_profile,
        }

    return statements, duplicates


def _weak_components(nodes: list[str], adjacency: dict[str, set[str]], reverse: dict[str, set[str]]) -> tuple[dict[str, int], dict[int, int]]:
    """
    Relevance: Operates within the relational connector layer.
    Concept: Internal helper implementing one deterministic step of this stage.
    Contribution: Contributes a deterministic transformation that supports end-to-end reasoning reproducibility.
    """

    component_of: dict[str, int] = {}
    component_sizes: dict[int, int] = {}
    component_id = 0

    for node in nodes:
        if node in component_of:
            continue
        queue = deque([node])
        component_of[node] = component_id
        size = 0

        while queue:
            current = queue.popleft()
            size += 1
            neighbors = adjacency[current] | reverse[current]
            for neighbor in neighbors:
                if neighbor not in component_of:
                    component_of[neighbor] = component_id
                    queue.append(neighbor)

        component_sizes[component_id] = size
        component_id += 1

    return component_of, component_sizes


def _reachability_counts(nodes: list[str], adjacency: dict[str, set[str]]) -> dict[str, int]:
    """
    Relevance: Operates within the relational connector layer.
    Concept: Internal helper implementing one deterministic step of this stage.
    Contribution: Contributes a deterministic transformation that supports end-to-end reasoning reproducibility.
    """

    counts: dict[str, int] = {}
    for node in nodes:
        visited = {node}
        queue = deque([node])
        while queue:
            current = queue.popleft()
            for nxt in adjacency[current]:
                if nxt not in visited:
                    visited.add(nxt)
                    queue.append(nxt)
        counts[node] = max(0, len(visited) - 1)
    return counts


def _betweenness_directed(nodes: list[str], adjacency: dict[str, set[str]]) -> dict[str, float]:
    """
    Relevance: Operates within the relational connector layer.
    Concept: Internal helper implementing one deterministic step of this stage.
    Contribution: Contributes a deterministic transformation that supports end-to-end reasoning reproducibility.
    """

    cb = {node: 0.0 for node in nodes}
    n = len(nodes)

    for source in nodes:
        stack: list[str] = []
        predecessors = {node: [] for node in nodes}
        sigma = {node: 0.0 for node in nodes}
        sigma[source] = 1.0
        dist = {node: -1 for node in nodes}
        dist[source] = 0

        queue = deque([source])
        while queue:
            v = queue.popleft()
            stack.append(v)
            for w in adjacency[v]:
                if dist[w] < 0:
                    queue.append(w)
                    dist[w] = dist[v] + 1
                if dist[w] == dist[v] + 1:
                    sigma[w] += sigma[v]
                    predecessors[w].append(v)

        delta = {node: 0.0 for node in nodes}
        while stack:
            w = stack.pop()
            for v in predecessors[w]:
                if sigma[w] > 0:
                    delta[v] += (sigma[v] / sigma[w]) * (1.0 + delta[w])
            if w != source:
                cb[w] += delta[w]

    if n > 2:
        norm = float((n - 1) * (n - 2))
        for node in cb:
            cb[node] /= norm

    return cb


def _jaccard(a: set[str], b: set[str]) -> float:
    """
    Relevance: Operates within the relational connector layer.
    Concept: Lightweight semantic feature computation for graph reasoning heuristics.
    Contribution: Contributes a deterministic transformation that supports end-to-end reasoning reproducibility.
    """

    if not a or not b:
        return 0.0
    union = a | b
    if not union:
        return 0.0
    return len(a & b) / len(union)


def _normalize_metric(values: dict[str, float | int]) -> dict[str, float]:
    """
    Relevance: Operates within the relational connector layer.
    Concept: Normalization of input structures into stable internal forms.
    Contribution: Reduces runtime ambiguity and prevents malformed artifacts from destabilizing the workflow.
    """

    if not values:
        return {}
    vmax = max(float(v) for v in values.values())
    if vmax <= 0:
        return {k: 0.0 for k in values}
    return {k: float(v) / vmax for k, v in values.items()}


def _phase_progression_score(profile: dict[str, Any]) -> float:
    """
    Relevance: Operates within the relational connector layer.
    Concept: Approximate progression score over statement phases.
    Contribution: Helps orient candidates from foundational material toward later theorem and derivation phases.
    """

    phase = str(profile.get("statement_phase", "")).strip().lower()
    if not phase:
        return 0.5
    if phase.startswith("foundational-definitions"):
        return 0.10
    if phase.startswith("foundational"):
        return 0.18
    if "regularity" in phase:
        return 0.24
    if "problem-semantics" in phase or "semantics" in phase:
        return 0.40
    if phase.startswith("core"):
        return 0.55
    if "equivalent" in phase:
        return 0.65
    if "proof-technology" in phase:
        return 0.72
    if "canonical-examples" in phase or "example" in phase:
        return 0.82
    if "derived" in phase:
        return 0.88
    return 0.5


def _directional_profile_signal(source_profile: dict[str, Any], target_profile: dict[str, Any]) -> float:
    """
    Relevance: Operates within the relational connector layer.
    Concept: Direction-sensitive compatibility between source consequences and target antecedents.
    Contribution: Improves edge orientation for discovery candidates when theorem-like statements are mutually related.
    """

    if not isinstance(source_profile, dict) or not isinstance(target_profile, dict):
        return 0.0
    source_consequences = set(source_profile.get("consequence_signatures", []))
    source_claims = set(source_profile.get("claim_signatures", []))
    target_antecedents = set(target_profile.get("antecedent_signatures", []))
    target_claims = set(target_profile.get("claim_signatures", []))
    target_barriers = set(target_profile.get("barrier_signals", []))
    return _clamp01(
        0.46 * _jaccard(source_consequences, target_antecedents)
        + 0.26 * _jaccard(source_claims, target_antecedents)
        + 0.18 * _jaccard(source_consequences, target_claims)
        + 0.10 * _jaccard(source_claims, target_barriers)
    )


def _orientation(a: dict[str, Any], b: dict[str, Any], foundation: dict[str, float]) -> tuple[str, str]:
    """
    Relevance: Operates within the relational connector layer.
    Concept: Internal helper implementing one deterministic step of this stage.
    Contribution: Contributes a deterministic transformation that supports end-to-end reasoning reproducibility.
    """

    a_kind = a["kind"]
    b_kind = b["kind"]
    a_profile = a.get("concept_profile", {}) if isinstance(a.get("concept_profile"), dict) else {}
    b_profile = b.get("concept_profile", {}) if isinstance(b.get("concept_profile"), dict) else {}

    if a_kind in PREMISE_KINDS and b_kind in TARGET_KINDS and a_kind != b_kind:
        return a["id"], b["id"]
    if b_kind in PREMISE_KINDS and a_kind in TARGET_KINDS and a_kind != b_kind:
        return b["id"], a["id"]

    a_to_b = _directional_profile_signal(a_profile, b_profile)
    b_to_a = _directional_profile_signal(b_profile, a_profile)
    if abs(a_to_b - b_to_a) >= 0.08:
        if a_to_b > b_to_a:
            return a["id"], b["id"]
        return b["id"], a["id"]

    a_phase = _phase_progression_score(a_profile)
    b_phase = _phase_progression_score(b_profile)
    if abs(a_phase - b_phase) >= 0.08:
        if a_phase <= b_phase:
            return a["id"], b["id"]
        return b["id"], a["id"]

    if foundation[a["id"]] >= foundation[b["id"]]:
        return a["id"], b["id"]
    return b["id"], a["id"]


def _compatibility(kind_a: str, kind_b: str) -> float:
    """
    Relevance: Operates within the relational connector layer.
    Concept: Internal helper implementing one deterministic step of this stage.
    Contribution: Contributes a deterministic transformation that supports end-to-end reasoning reproducibility.
    """

    if kind_a in PREMISE_KINDS and kind_b in TARGET_KINDS:
        return 1.0
    if kind_b in PREMISE_KINDS and kind_a in TARGET_KINDS:
        return 1.0
    if kind_a == kind_b:
        return 0.7
    return 0.55


def _build_concept_graph(
    statements: dict[str, dict[str, Any]],
    adjacency: dict[str, set[str]],
    connection_candidates: list[dict[str, Any]],
) -> dict[str, Any]:
    """
    Relevance: Operates within the relational connector layer.
    Concept: Construction of derived graph/model structures used by later stages.
    Contribution: Creates the structural substrate that enables cross-stage scoring and interpretation.
    """

    nodes: dict[str, dict[str, Any]] = {}
    edges: list[dict[str, Any]] = []

    for sid, stmt in statements.items():
        snode = f"statement:{sid}"
        nodes[snode] = {"id": snode, "type": "statement", "statement_id": sid, "kind": stmt.get("kind", "")}
        profile = stmt.get("concept_profile", {}) if isinstance(stmt.get("concept_profile"), dict) else {}
        for claim in profile.get("claim_signatures", []):
            cnode = f"claim:{claim}"
            if cnode not in nodes:
                nodes[cnode] = {"id": cnode, "type": "claim-signature", "label": claim}
            edges.append({"from": snode, "to": cnode, "relation": "asserts", "weight": 0.84})
        for antecedent in profile.get("antecedent_signatures", []):
            anode = f"antecedent:{antecedent}"
            if anode not in nodes:
                nodes[anode] = {"id": anode, "type": "antecedent-signature", "label": antecedent}
            edges.append({"from": snode, "to": anode, "relation": "requires", "weight": 0.82})
        for consequence in profile.get("consequence_signatures", []):
            cnode2 = f"consequence:{consequence}"
            if cnode2 not in nodes:
                nodes[cnode2] = {"id": cnode2, "type": "consequence-signature", "label": consequence}
            edges.append({"from": snode, "to": cnode2, "relation": "yields", "weight": 0.84})
        for implication in profile.get("implication_signatures", []):
            inode = f"implication:{implication}"
            if inode not in nodes:
                nodes[inode] = {"id": inode, "type": "implication-signature", "label": implication}
            edges.append({"from": snode, "to": inode, "relation": "instantiates", "weight": 0.86})
        for model in profile.get("model_signatures", []):
            mnode2 = f"model:{model}"
            if mnode2 not in nodes:
                nodes[mnode2] = {"id": mnode2, "type": "model-signature", "label": model}
            edges.append({"from": snode, "to": mnode2, "relation": "works_in", "weight": 0.80})
        for reduction in profile.get("reduction_signatures", []):
            rnode2 = f"reduction:{reduction}"
            if rnode2 not in nodes:
                nodes[rnode2] = {"id": rnode2, "type": "reduction-signature", "label": reduction}
            edges.append({"from": snode, "to": rnode2, "relation": "reduces_via", "weight": 0.82})
        for sym in stmt.get("used_symbols", []):
            cnode = f"concept:{sym}"
            if cnode not in nodes:
                nodes[cnode] = {"id": cnode, "type": "concept", "label": sym}
            edges.append({"from": snode, "to": cnode, "relation": "uses", "weight": 0.60})
            if str(stmt.get("kind", "")).lower() == "definition":
                edges.append({"from": snode, "to": cnode, "relation": "defines", "weight": 0.80})
        for cls in profile.get("complexity_classes", []):
            cnode = f"class:{cls}"
            if cnode not in nodes:
                nodes[cnode] = {"id": cnode, "type": "complexity-class", "label": cls}
            edges.append({"from": snode, "to": cnode, "relation": "uses", "weight": 0.78})
        for prb in profile.get("core_problems", []):
            pnode = f"problem:{prb}"
            if pnode not in nodes:
                nodes[pnode] = {"id": pnode, "type": "problem", "label": prb}
            edges.append({"from": snode, "to": pnode, "relation": "uses", "weight": 0.74})
        for reg in profile.get("proof_regimes", []):
            rnode = f"regime:{reg}"
            if rnode not in nodes:
                nodes[rnode] = {"id": rnode, "type": "proof-regime", "label": reg}
            edges.append({"from": snode, "to": rnode, "relation": "uses", "weight": 0.70})
        for barr in profile.get("barrier_signals", []):
            bnode2 = f"barrier-signal:{barr}"
            if bnode2 not in nodes:
                nodes[bnode2] = {"id": bnode2, "type": "barrier-signal", "label": barr}
            edges.append({"from": snode, "to": bnode2, "relation": "uses", "weight": 0.72})
        for tag in stmt.get("method_tags", []):
            mnode = f"method:{tag}"
            if mnode not in nodes:
                nodes[mnode] = {"id": mnode, "type": "method", "label": tag}
            edges.append({"from": snode, "to": mnode, "relation": "uses", "weight": 0.55})
        if bool(stmt.get("is_barrier")):
            bnode = f"barrier:{sid}"
            nodes[bnode] = {"id": bnode, "type": "barrier", "statement_id": sid}
            edges.append({"from": snode, "to": bnode, "relation": "defines", "weight": 0.75})

    for src, targets in adjacency.items():
        for dst in targets:
            if src in statements and dst in statements:
                edges.append({"from": f"statement:{src}", "to": f"statement:{dst}", "relation": "generalizes", "weight": 0.55})

    theorem_ids = [sid for sid, s in statements.items() if str(s.get("kind", "")).lower() == "theorem"]
    barrier_ids = [sid for sid, s in statements.items() if bool(s.get("is_barrier"))]
    for bid in barrier_ids:
        barrier_stmt = statements[bid]
        barrier_symbol_vocab = set(barrier_stmt.get("used_symbols", [])) | set(barrier_stmt.get("latex_symbols", []))
        barrier_methods = set(barrier_stmt.get("method_tags", []))
        barrier_family = set(barrier_stmt.get("family_signature", []))
        for tid in theorem_ids:
            if tid == bid:
                continue
            theorem_stmt = statements[tid]
            theorem_symbol_vocab = set(theorem_stmt.get("used_symbols", [])) | set(theorem_stmt.get("latex_symbols", []))
            theorem_methods = set(theorem_stmt.get("method_tags", []))
            theorem_family = set(theorem_stmt.get("family_signature", []))

            symbol_overlap = _jaccard(barrier_symbol_vocab, theorem_symbol_vocab)
            method_overlap = _jaccard(barrier_methods, theorem_methods)
            family_overlap = _jaccard(barrier_family, theorem_family)
            structural_overlap = _clamp01(0.45 * symbol_overlap + 0.35 * method_overlap + 0.20 * family_overlap)
            if structural_overlap < 0.08:
                continue
            edges.append(
                {
                    "from": f"barrier:{bid}",
                    "to": f"statement:{tid}",
                    "relation": "obstructs",
                    "weight": round(0.30 + 0.50 * structural_overlap, 4),
                }
            )

    for cand in connection_candidates:
        src = str(cand.get("from_id", "")).strip()
        dst = str(cand.get("to_id", "")).strip()
        if src not in statements or dst not in statements:
            continue
        relation = str(cand.get("relation", "")).strip().lower()
        if relation in {"potential-equivalence", "definitional-expansion"}:
            rel = "reexpresses"
        elif relation == "implication-schema-transfer":
            rel = "reframes"
        elif relation in {"method-transfer", "analogy-transfer", "model-transfer", "conceptual-transfer"}:
            rel = "analogy_to"
        else:
            continue
        edges.append(
            {
                "from": f"statement:{src}",
                "to": f"statement:{dst}",
                "relation": rel,
                "weight": round(_safe_float(cand.get("score"), 0.0), 4),
            }
        )

    rel_counts = Counter(str(e.get("relation", "")).strip().lower() for e in edges)
    return {
        "nodes": list(nodes.values()),
        "relations": edges,
        "relation_counts": dict(rel_counts),
    }


def _safe_float(value: Any, default: float = 0.0) -> float:
    """
    Relevance: Operates within the relational connector layer.
    Concept: Defensive conversion/parsing to keep scoring and reporting robust.
    Contribution: Reduces runtime ambiguity and prevents malformed artifacts from destabilizing the workflow.
    """

    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def analyze_kb(
    kb_path: Path,
    top_k: int,
    min_similarity: float,
    max_connections: int,
    loop_rounds: int,
    include_statuses: set[str],
    allow_intra_component_fallback: bool = True,
) -> dict[str, Any]:
    """Run connector analysis and produce intervention/bridge candidates.

    The output mixes:
    - structural graph signals (dependencies/components/reachability),
    - semantic signals (symbols/methods/family/equivalence proxies),
    - heuristic bridge scoring for abductive prioritization.
    """
    kb_content = kb_path.read_text(encoding="utf-8")
    ontology_profile = _resolve_ontology_profile(kb_content)
    raw_statements, duplicates = _extract_statements(kb_content, ontology_profile=ontology_profile)
    filtered_out_status_counts: Counter[str] = Counter()
    statements: dict[str, dict[str, Any]] = {}
    for sid, payload in raw_statements.items():
        status = str(payload.get("status", "tentative")).strip().lower()
        if status in include_statuses:
            statements[sid] = payload
        else:
            filtered_out_status_counts[status or "unknown"] += 1

    if not statements:
        raise ValueError("No statement YAML blocks with id/kind were found in KB.")

    nodes = sorted(statements.keys())
    adjacency = {node: set() for node in nodes}
    reverse = {node: set() for node in nodes}
    missing_dependencies = {node: [] for node in nodes}

    for node in nodes:
        for dep in statements[node]["depends_on"]:
            if dep in statements:
                adjacency[dep].add(node)
                reverse[node].add(dep)
            else:
                missing_dependencies[node].append(dep)

    component_of, component_sizes = _weak_components(nodes, adjacency, reverse)
    max_component_size = max(component_sizes.values()) if component_sizes else 1

    downstream = _reachability_counts(nodes, adjacency)
    upstream = _reachability_counts(nodes, reverse)
    betweenness = _betweenness_directed(nodes, adjacency)
    unresolved = {node: len(missing_dependencies[node]) for node in nodes}

    downstream_norm = _normalize_metric(downstream)
    upstream_norm = _normalize_metric(upstream)
    betweenness_norm = _normalize_metric(betweenness)
    unresolved_norm = _normalize_metric(unresolved)

    token_counter = Counter()
    for node in nodes:
        token_counter.update(statements[node]["tokens"])

    cross_component_potential: dict[str, float] = {node: 0.0 for node in nodes}
    cross_component_partner: dict[str, str | None] = {node: None for node in nodes}

    cross_component_candidates: list[dict[str, Any]] = []
    intra_component_candidates: list[dict[str, Any]] = []
    for i, a_id in enumerate(nodes):
        a = statements[a_id]
        for b_id in nodes[i + 1 :]:
            b = statements[b_id]
            same_component = component_of[a_id] == component_of[b_id]
            if same_component and not allow_intra_component_fallback:
                continue

            symbol_vocab_a = set(a.get("used_symbols", [])) | set(a.get("latex_symbols", []))
            symbol_vocab_b = set(b.get("used_symbols", [])) | set(b.get("latex_symbols", []))
            role_alignment = _jaccard(set(a.get("role_tokens", [])), set(b.get("role_tokens", [])))
            symbol_alignment = _clamp01(0.70 * _jaccard(symbol_vocab_a, symbol_vocab_b) + 0.30 * role_alignment)
            method_overlap = _jaccard(set(a.get("method_tags", [])), set(b.get("method_tags", [])))
            concept_profile_a = a.get("concept_profile", {}) if isinstance(a.get("concept_profile"), dict) else {}
            concept_profile_b = b.get("concept_profile", {}) if isinstance(b.get("concept_profile"), dict) else {}
            concept_overlap = _profile_overlap(concept_profile_a, concept_profile_b)
            specific_overlap = _jaccard(
                set(concept_profile_a.get("specific_tags", [])),
                set(concept_profile_b.get("specific_tags", [])),
            )
            family_id_overlap = _jaccard(set(a.get("id_tokens", [])), set(b.get("id_tokens", [])))
            family_sig_overlap = _jaccard(set(a.get("family_signature", [])), set(b.get("family_signature", [])))
            family_embedding = _theorem_family_embedding_similarity(
                set(a.get("family_signature", [])),
                set(b.get("family_signature", [])),
            )
            family_overlap = _clamp01(0.40 * family_id_overlap + 0.30 * family_sig_overlap + 0.30 * family_embedding)
            equiv_reduction = _equivalence_or_reduction_signal(
                a.get("tokens", set()),
                b.get("tokens", set()),
                a.get("id_tokens", set()),
                b.get("id_tokens", set()),
            )
            structural_similarity = _clamp01(
                0.28 * symbol_alignment
                + 0.24 * method_overlap
                + 0.20 * family_overlap
                + 0.14 * concept_overlap["overall"]
                + 0.14 * specific_overlap
                + 0.08 * equiv_reduction
            )
            if structural_similarity < min_similarity:
                continue
            lexical_support_overlap = _jaccard(a["tokens"], b["tokens"])
            definitional_expansion = _definitional_expansion_signal(a, b, structural_similarity, symbol_alignment)
            semantic_score = _clamp01(
                0.22 * symbol_alignment
                + 0.16 * method_overlap
                + 0.16 * family_overlap
                + 0.18 * concept_overlap["overall"]
                + 0.20 * specific_overlap
                + 0.10 * equiv_reduction
                + 0.06 * definitional_expansion
            )

            comp_gain = (
                0.0
                if same_component
                else (component_sizes[component_of[a_id]] + component_sizes[component_of[b_id]]) / (2.0 * max_component_size)
            )
            influence = max(downstream_norm[a_id], downstream_norm[b_id])
            compat = _compatibility(a["kind"], b["kind"])
            theorem_bias = 1.0 if ("theorem" in {a.get("kind", ""), b.get("kind", "")}) else 0.78
            # Composite bridge value used for ranking candidate connections.
            score = (
                0.34 * semantic_score
                + 0.20 * comp_gain
                + 0.14 * influence
                + 0.12 * compat
                + 0.10 * structural_similarity
                + 0.10 * max(equiv_reduction, definitional_expansion)
            ) * theorem_bias
            if same_component:
                # Keep intra-component candidates available as fallback but penalize them.
                score *= 0.84

            structured_evidence = (
                set(a.get("used_symbols", [])) & set(b.get("used_symbols", []))
            ) | (
                set(a.get("method_tags", [])) & set(b.get("method_tags", []))
            ) | (
                set(a.get("family_signature", [])) & set(b.get("family_signature", []))
            )
            specific_evidence = (
                set(concept_profile_a.get("specific_tags", [])) & set(concept_profile_b.get("specific_tags", []))
            )
            concept_evidence = specific_evidence | (
                set(concept_profile_a.get("all_tags", [])) & set(concept_profile_b.get("all_tags", []))
            )
            evidence = _clean_evidence_terms(structured_evidence, limit=6)
            if concept_evidence:
                evidence = _clean_evidence_terms(list(concept_evidence) + evidence, limit=6)
            if not evidence:
                evidence = _clean_evidence_terms(
                    sorted(a["tokens"] & b["tokens"], key=lambda t: (token_counter[t], t), reverse=True),
                    limit=6,
                )
            from_id, to_id = _orientation(a, b, {n: downstream_norm[n] - upstream_norm[n] for n in nodes})
            oriented_from_profile = concept_profile_a if from_id == a["id"] else concept_profile_b
            oriented_to_profile = concept_profile_b if to_id == b["id"] else concept_profile_a
            relation = "potential-support"
            if equiv_reduction >= 0.45:
                relation = "potential-equivalence"
            elif definitional_expansion >= 0.40:
                relation = "definitional-expansion"
            elif concept_overlap["implication_overlap"] >= 0.35:
                relation = "implication-schema-transfer"
            elif concept_overlap["model_overlap"] >= 0.40:
                relation = "model-transfer"
            elif method_overlap >= 0.30:
                relation = "method-transfer"
            elif concept_overlap["overall"] >= 0.45 and concept_overlap["regime_overlap"] >= 0.35:
                relation = "conceptual-transfer"
            elif family_overlap >= 0.30 and symbol_alignment < 0.20:
                relation = "analogy-transfer"

            candidate = {
                "from_id": from_id,
                "to_id": to_id,
                "score": round(score, 4),
                "similarity": round(structural_similarity, 4),
                "structural_similarity": round(structural_similarity, 4),
                "lexical_support_overlap": round(lexical_support_overlap, 4),
                "semantic_score": round(semantic_score, 4),
                "concept_alignment": round(concept_overlap["overall"], 4),
                "specific_alignment": round(specific_overlap, 4),
                "concept_claim_overlap": round(concept_overlap["claim_overlap"], 4),
                "concept_model_overlap": round(concept_overlap["model_overlap"], 4),
                "concept_reduction_overlap": round(concept_overlap["reduction_overlap"], 4),
                "concept_implication_overlap": round(concept_overlap["implication_overlap"], 4),
                "concept_antecedent_overlap": round(concept_overlap["antecedent_overlap"], 4),
                "concept_consequence_overlap": round(concept_overlap["consequence_overlap"], 4),
                "concept_class_overlap": round(concept_overlap["class_overlap"], 4),
                "concept_problem_overlap": round(concept_overlap["problem_overlap"], 4),
                "concept_regime_overlap": round(concept_overlap["regime_overlap"], 4),
                "concept_barrier_overlap": round(concept_overlap["barrier_overlap"], 4),
                "symbol_role_alignment": round(symbol_alignment, 4),
                "role_alignment": round(role_alignment, 4),
                "method_overlap": round(method_overlap, 4),
                "theorem_family_overlap": round(family_overlap, 4),
                "theorem_family_embedding_similarity": round(family_embedding, 4),
                "equivalence_reduction_signal": round(equiv_reduction, 4),
                "definitional_expansion": round(definitional_expansion, 4),
                "component_gain": round(comp_gain, 4),
                "compatibility": round(compat, 4),
                "theorem_bias": round(theorem_bias, 4),
                "evidence_terms": evidence,
                "specific_evidence": _clean_evidence_terms(specific_evidence, limit=6),
                "concept_evidence": _clean_evidence_terms(concept_evidence, limit=6),
                "from_profile": {
                    "claim_signatures": oriented_from_profile.get("claim_signatures", []),
                    "model_signatures": oriented_from_profile.get("model_signatures", []),
                    "reduction_signatures": oriented_from_profile.get("reduction_signatures", []),
                    "implication_signatures": oriented_from_profile.get("implication_signatures", []),
                    "antecedent_signatures": oriented_from_profile.get("antecedent_signatures", []),
                    "consequence_signatures": oriented_from_profile.get("consequence_signatures", []),
                    "core_problems": oriented_from_profile.get("core_problems", []),
                    "complexity_classes": oriented_from_profile.get("complexity_classes", []),
                    "barrier_signals": oriented_from_profile.get("barrier_signals", []),
                    "statement_phase": oriented_from_profile.get("statement_phase", ""),
                    "bridge_roles": oriented_from_profile.get("bridge_roles", []),
                    "ontology_profile": oriented_from_profile.get("ontology_profile", ""),
                },
                "to_profile": {
                    "claim_signatures": oriented_to_profile.get("claim_signatures", []),
                    "model_signatures": oriented_to_profile.get("model_signatures", []),
                    "reduction_signatures": oriented_to_profile.get("reduction_signatures", []),
                    "implication_signatures": oriented_to_profile.get("implication_signatures", []),
                    "antecedent_signatures": oriented_to_profile.get("antecedent_signatures", []),
                    "consequence_signatures": oriented_to_profile.get("consequence_signatures", []),
                    "core_problems": oriented_to_profile.get("core_problems", []),
                    "complexity_classes": oriented_to_profile.get("complexity_classes", []),
                    "barrier_signals": oriented_to_profile.get("barrier_signals", []),
                    "statement_phase": oriented_to_profile.get("statement_phase", ""),
                    "bridge_roles": oriented_to_profile.get("bridge_roles", []),
                    "ontology_profile": oriented_to_profile.get("ontology_profile", ""),
                },
                "relation": relation,
                "component_relation": "intra-component" if same_component else "cross-component",
            }
            if same_component:
                intra_component_candidates.append(candidate)
            else:
                cross_component_candidates.append(candidate)
                a_potential = structural_similarity * (component_sizes[component_of[b_id]] / max_component_size)
                b_potential = structural_similarity * (component_sizes[component_of[a_id]] / max_component_size)
                if a_potential > cross_component_potential[a_id]:
                    cross_component_potential[a_id] = round(a_potential, 6)
                    cross_component_partner[a_id] = b_id
                if b_potential > cross_component_potential[b_id]:
                    cross_component_potential[b_id] = round(b_potential, 6)
                    cross_component_partner[b_id] = a_id

    cross_component_candidates.sort(key=lambda item: item["score"], reverse=True)
    intra_component_candidates.sort(key=lambda item: item["score"], reverse=True)
    if cross_component_candidates:
        selected_intra: list[dict[str, Any]] = []
        if allow_intra_component_fallback and intra_component_candidates:
            top_cross_score = _safe_float(cross_component_candidates[0].get("score"), 0.0)
            intra_quota = min(len(intra_component_candidates), max(3, max_connections // 4))
            for item in intra_component_candidates:
                score = _safe_float(item.get("score"), 0.0)
                relation = str(item.get("relation", "")).strip().lower()
                if score >= max(0.20, 0.55 * top_cross_score) or relation in {
                    "definitional-expansion",
                    "implication-schema-transfer",
                    "potential-equivalence",
                }:
                    selected_intra.append(item)
                if len(selected_intra) >= intra_quota:
                    break
        cross_quota = max_connections - len(selected_intra)
        connection_candidates = cross_component_candidates[: max(0, cross_quota)] + selected_intra
        connection_candidates.sort(key=lambda item: item["score"], reverse=True)
        connection_candidates = connection_candidates[:max_connections]
        candidate_generation_mode = "hybrid" if selected_intra else "cross-component"
    elif allow_intra_component_fallback:
        connection_candidates = intra_component_candidates[:max_connections]
        candidate_generation_mode = "intra-component-fallback"
    else:
        connection_candidates = []
        candidate_generation_mode = "none"

    # Authored depends_on links are first-class structural evidence and should
    # not disappear just because they are topologically local. Inject them with
    # a conservative score floor so bridge planning can still see explicit
    # proof dependencies under simulated ignorance.
    existing_by_edge = {
        (str(item.get("from_id", "")).strip(), str(item.get("to_id", "")).strip()): item
        for item in connection_candidates
        if isinstance(item, dict)
    }
    dependency_candidates: list[dict[str, Any]] = []
    for dst in nodes:
        dst_stmt = statements[dst]
        for src in dst_stmt["depends_on"]:
            if src not in statements:
                continue
            edge = (src, dst)
            if edge in existing_by_edge:
                existing = existing_by_edge[edge]
                existing["relation"] = "declared-dependency"
                existing["score"] = round(max(_safe_float(existing.get("score"), 0.0), 0.34), 4)
                existing["component_relation"] = "authored-dependency"
                continue
            src_stmt = statements[src]
            from_profile = src_stmt["concept_profile"]
            to_profile = dst_stmt["concept_profile"]
            overlap = _profile_overlap(from_profile, to_profile)
            evidence_terms = _clean_evidence_terms(
                list(set(from_profile.get("specific_tags", [])) & set(to_profile.get("specific_tags", [])))
                + list(set(from_profile.get("all_tags", [])) & set(to_profile.get("all_tags", []))),
                limit=6,
            )
            if not evidence_terms:
                evidence_terms = _clean_evidence_terms(list(set(src_stmt["tokens"]) & set(dst_stmt["tokens"])), limit=6)
            dependency_candidates.append(
                {
                    "from_id": src,
                    "to_id": dst,
                    "score": round(max(0.34, 0.22 + 0.18 * _safe_float(overlap.get("overall"), 0.0)), 4),
                    "similarity": round(max(0.24, _safe_float(overlap.get("overall"), 0.0)), 4),
                    "structural_similarity": round(max(0.24, _safe_float(overlap.get("overall"), 0.0)), 4),
                    "lexical_support_overlap": 0.0,
                    "semantic_score": round(max(0.28, 0.55 * _safe_float(overlap.get("overall"), 0.0) + 0.45 * _safe_float(overlap.get("implication_overlap"), 0.0)), 4),
                    "concept_alignment": round(max(0.30, _safe_float(overlap.get("overall"), 0.0)), 4),
                    "specific_alignment": round(max(0.25, _safe_float(overlap.get("consequence_overlap"), 0.0), _safe_float(overlap.get("implication_overlap"), 0.0)), 4),
                    "concept_claim_overlap": round(_safe_float(overlap.get("claim_overlap"), 0.0), 4),
                    "concept_model_overlap": round(_safe_float(overlap.get("model_overlap"), 0.0), 4),
                    "concept_reduction_overlap": round(_safe_float(overlap.get("reduction_overlap"), 0.0), 4),
                    "concept_implication_overlap": round(_safe_float(overlap.get("implication_overlap"), 0.0), 4),
                    "concept_antecedent_overlap": round(_safe_float(overlap.get("antecedent_overlap"), 0.0), 4),
                    "concept_consequence_overlap": round(_safe_float(overlap.get("consequence_overlap"), 0.0), 4),
                    "concept_class_overlap": round(_safe_float(overlap.get("class_overlap"), 0.0), 4),
                    "concept_problem_overlap": round(_safe_float(overlap.get("problem_overlap"), 0.0), 4),
                    "concept_regime_overlap": round(_safe_float(overlap.get("regime_overlap"), 0.0), 4),
                    "concept_barrier_overlap": round(_safe_float(overlap.get("barrier_overlap"), 0.0), 4),
                    "symbol_role_alignment": round(0.30, 4),
                    "role_alignment": round(_jaccard(set(src_stmt.get("role_tokens", [])), set(dst_stmt.get("role_tokens", []))), 4),
                    "method_overlap": round(_jaccard(set(src_stmt.get("method_tags", [])), set(dst_stmt.get("method_tags", []))), 4),
                    "theorem_family_overlap": round(_safe_float(overlap.get("claim_overlap"), 0.0), 4),
                    "theorem_family_embedding_similarity": round(max(0.28, _safe_float(overlap.get("overall"), 0.0)), 4),
                    "equivalence_reduction_signal": 0.0,
                    "definitional_expansion": 0.0,
                    "component_gain": 0.0,
                    "compatibility": 1.0,
                    "theorem_bias": 0.9,
                    "evidence_terms": evidence_terms,
                    "specific_evidence": evidence_terms,
                    "concept_evidence": evidence_terms,
                    "from_profile": _candidate_profile_snapshot(from_profile),
                    "to_profile": _candidate_profile_snapshot(to_profile),
                    "relation": "declared-dependency",
                    "component_relation": "authored-dependency",
                }
            )
    if dependency_candidates:
        connection_candidates.extend(dependency_candidates)
        connection_candidates.sort(key=lambda item: item["score"], reverse=True)
        deduped_candidates: list[dict[str, Any]] = []
        seen_edges: set[tuple[str, str]] = set()
        for item in connection_candidates:
            edge = (str(item.get("from_id", "")).strip(), str(item.get("to_id", "")).strip())
            if not edge[0] or not edge[1] or edge in seen_edges:
                continue
            seen_edges.add(edge)
            deduped_candidates.append(item)
        connection_candidates = deduped_candidates[:max_connections]

    cross_norm = _normalize_metric(cross_component_potential)
    concept_incident_raw: dict[str, float] = {node: 0.0 for node in nodes}
    barrier_interface_raw: dict[str, float] = {node: 0.0 for node in nodes}
    for cand in connection_candidates:
        src = str(cand.get("from_id", "")).strip()
        dst = str(cand.get("to_id", "")).strip()
        if not src or not dst:
            continue
        concept_signal = _clamp01(
            0.40 * _safe_float(cand.get("semantic_score"), 0.0)
            + 0.25 * _safe_float(cand.get("concept_alignment"), 0.0)
            + 0.35 * _safe_float(cand.get("specific_alignment"), 0.0)
        )
        for sid in [src, dst]:
            if sid in concept_incident_raw:
                concept_incident_raw[sid] += concept_signal
                if _safe_float(cand.get("concept_barrier_overlap"), 0.0) > 0:
                    barrier_interface_raw[sid] = max(
                        barrier_interface_raw[sid],
                        _safe_float(cand.get("concept_barrier_overlap"), 0.0),
                    )

    concept_incident_norm = _normalize_metric(concept_incident_raw)
    concept_diversity_norm = _normalize_metric(
        {
            node: (
                1.5
                * len(
                    (
                        statements[node].get("concept_profile", {})
                        if isinstance(statements[node].get("concept_profile"), dict)
                        else {}
                    ).get("specific_tags", [])
                )
                + len(
                    (
                        statements[node].get("concept_profile", {})
                        if isinstance(statements[node].get("concept_profile"), dict)
                        else {}
                    ).get("all_tags", [])
                )
            )
            for node in nodes
        }
    )
    specificity_raw = {
        node: _safe_float(
            (
                statements[node].get("concept_profile", {})
                if isinstance(statements[node].get("concept_profile"), dict)
                else {}
            ).get("specificity_score", 0.0),
            0.0,
        )
        for node in nodes
    }
    theory_relevance_raw = {
        node: _safe_float(
            (
                statements[node].get("concept_profile", {})
                if isinstance(statements[node].get("concept_profile"), dict)
                else {}
            ).get("profile_score", 0.0),
            0.0,
        )
        for node in nodes
    }
    specificity_norm = _normalize_metric(specificity_raw)
    theory_relevance_norm = _normalize_metric(theory_relevance_raw)
    barrier_interface_norm = _normalize_metric(barrier_interface_raw)

    interventions: list[dict[str, Any]] = []
    for node in nodes:
        profile = statements[node].get("concept_profile", {}) if isinstance(statements[node].get("concept_profile"), dict) else {}
        concept_focus = _concept_focus(profile, limit=5)
        score = (
            0.16 * downstream_norm[node]
            + 0.10 * betweenness_norm[node]
            + 0.08 * unresolved_norm[node]
            + 0.12 * cross_norm.get(node, 0.0)
            + 0.22 * concept_incident_norm.get(node, 0.0)
            + 0.10 * concept_diversity_norm.get(node, 0.0)
            + 0.12 * theory_relevance_norm.get(node, 0.0)
            + 0.10 * specificity_norm.get(node, 0.0)
        )

        reasons = []
        if unresolved[node] > 0:
            reasons.append(f"{unresolved[node]} unresolved dependencies")
        if downstream[node] > 0:
            reasons.append(f"supports {downstream[node]} downstream statements")
        if betweenness[node] > 0:
            reasons.append("high bridge centrality")
        partner = cross_component_partner.get(node)
        if partner:
            reasons.append(f"cross-component structural bridge with {partner}")
        if concept_focus:
            reasons.append("concept focus: " + ", ".join(concept_focus[:4]))
        if barrier_interface_norm.get(node, 0.0) > 0:
            reasons.append("barrier-interface relevance")
        if not reasons:
            reasons.append("candidate bridge based on relational context")

        interventions.append(
            {
                "statement_id": node,
                "kind": statements[node]["kind"],
                "section": statements[node]["section"],
                "score": round(score, 4),
                "metrics": {
                    "downstream_impact": downstream[node],
                    "upstream_support": upstream[node],
                    "betweenness": round(betweenness[node], 6),
                    "unresolved_dependencies": unresolved[node],
                    "cross_component_potential": round(cross_norm.get(node, 0.0), 4),
                    "concept_incident_signal": round(concept_incident_norm.get(node, 0.0), 4),
                    "concept_diversity": round(concept_diversity_norm.get(node, 0.0), 4),
                    "theory_relevance": round(theory_relevance_norm.get(node, 0.0), 4),
                    "specificity_signal": round(specificity_norm.get(node, 0.0), 4),
                    "barrier_interface": round(barrier_interface_norm.get(node, 0.0), 4),
                },
                "concept_focus": concept_focus,
                "concept_profile": {
                    "claim_signatures": profile.get("claim_signatures", []),
                    "model_signatures": profile.get("model_signatures", []),
                    "reduction_signatures": profile.get("reduction_signatures", []),
                    "implication_signatures": profile.get("implication_signatures", []),
                    "antecedent_signatures": profile.get("antecedent_signatures", []),
                    "consequence_signatures": profile.get("consequence_signatures", []),
                    "complexity_classes": profile.get("complexity_classes", []),
                    "core_problems": profile.get("core_problems", []),
                    "proof_regimes": profile.get("proof_regimes", []),
                    "barrier_signals": profile.get("barrier_signals", []),
                },
                "missing_dependencies": missing_dependencies[node],
                "best_cross_component_partner": partner,
                "rationale": "; ".join(reasons),
            }
        )

    interventions.sort(key=lambda item: item["score"], reverse=True)
    top_interventions = interventions[:top_k]
    concept_graph = _build_concept_graph(statements, adjacency, connection_candidates)
    semantic_avg = 0.0
    concept_alignment_avg = 0.0
    specificity_alignment_avg = 0.0
    concept_profile_coverage = 0.0
    specific_profile_coverage = 0.0
    if connection_candidates:
        semantic_avg = sum(_safe_float(c.get("semantic_score"), 0.0) for c in connection_candidates) / len(connection_candidates)
        concept_alignment_avg = (
            sum(_safe_float(c.get("concept_alignment"), 0.0) for c in connection_candidates) / len(connection_candidates)
        )
        specificity_alignment_avg = (
            sum(_safe_float(c.get("specific_alignment"), 0.0) for c in connection_candidates) / len(connection_candidates)
        )
    if nodes:
        profiled = sum(
            1
            for node in nodes
            if isinstance(statements[node].get("concept_profile"), dict)
            and bool((statements[node]["concept_profile"]).get("all_tags"))
        )
        concept_profile_coverage = profiled / len(nodes)
        specific_profiled = sum(
            1
            for node in nodes
            if isinstance(statements[node].get("concept_profile"), dict)
            and bool((statements[node]["concept_profile"]).get("specific_tags"))
        )
        specific_profile_coverage = specific_profiled / len(nodes)

    loop_plan: list[dict[str, Any]] = []
    seed_targets = [item["statement_id"] for item in top_interventions[: min(6, len(top_interventions))]]
    seed_connections = [
        {"from_id": item["from_id"], "to_id": item["to_id"], "score": item["score"]}
        for item in connection_candidates[: min(10, len(connection_candidates))]
    ]

    for round_index in range(1, max(1, loop_rounds) + 1):
        if round_index == 1:
            loop_plan.append(
                {
                    "round": round_index,
                    "objective": "Prioritize intervention targets by graph influence and unresolved dependencies.",
                    "targets": seed_targets,
                    "action": "Run kb-abduce on each target to propose missing-premise hypotheses.",
                }
            )
        elif round_index == 2:
            round2_objective = "Test high-value cross-component links as abductive support hypotheses."
            if candidate_generation_mode == "intra-component-fallback":
                round2_objective = (
                    "Test high-value intra-component transfer links (fallback mode) as abductive support hypotheses."
                )
            loop_plan.append(
                {
                    "round": round_index,
                    "objective": round2_objective,
                    "candidate_connections": seed_connections,
                    "action": "Convert top links into conjectural dependencies and run kb-deduce for consequence checks.",
                }
            )
        else:
            loop_plan.append(
                {
                    "round": round_index,
                    "objective": "Refine and retain only hypotheses with best explanatory and deductive payoff.",
                    "action": "Re-score interventions, drop contradicted links, and keep top surviving pathways.",
                }
            )

    return {
        "kb_path": str(kb_path),
        "stats": {
            "ontology_profile": ontology_profile,
            "included_statuses": sorted(include_statuses),
            "statement_count": len(nodes),
            "filtered_out_count": len(raw_statements) - len(nodes),
            "filtered_out_status_counts": dict(filtered_out_status_counts),
            "edge_count": sum(len(v) for v in adjacency.values()),
            "component_count": len(component_sizes),
            "candidate_generation_mode": candidate_generation_mode,
            "cross_component_candidate_count": len(cross_component_candidates),
            "intra_component_candidate_count": len(intra_component_candidates),
            "missing_dependency_count": sum(unresolved.values()),
            "duplicate_statement_ids_skipped": duplicates,
            "avg_semantic_connection_score": round(semantic_avg, 4),
            "avg_concept_alignment": round(concept_alignment_avg, 4),
            "avg_specificity_alignment": round(specificity_alignment_avg, 4),
            "concept_profile_coverage": round(concept_profile_coverage, 4),
            "specific_profile_coverage": round(specific_profile_coverage, 4),
            "concept_node_count": len(concept_graph.get("nodes", [])),
        },
        "top_interventions": top_interventions,
        "connection_candidates": connection_candidates,
        "concept_graph": concept_graph,
        "abductive_loop_plan": loop_plan,
    }


def _to_markdown(report: dict[str, Any]) -> str:
    """
    Relevance: Operates within the relational connector layer.
    Concept: Rendering internal outputs into human-readable artifacts.
    Contribution: Improves interpretability by exposing machine results in analyst-friendly form.
    """

    lines: list[str] = []
    lines.append(f"# KB Connection Analysis: `{report['kb_path']}`")
    lines.append("")
    stats = report["stats"]
    lines.append("## Stats")
    lines.append("")
    lines.append(f"- Ontology profile: {stats.get('ontology_profile', ONTOLOGY_GENERIC_MATHEMATICS)}")
    lines.append(f"- Included statuses: {', '.join(stats.get('included_statuses', []))}")
    lines.append(f"- Statements: {stats['statement_count']}")
    lines.append(f"- Filtered out statements: {stats.get('filtered_out_count', 0)}")
    lines.append(f"- Dependency edges: {stats['edge_count']}")
    lines.append(f"- Components: {stats['component_count']}")
    lines.append(f"- Candidate generation mode: {stats.get('candidate_generation_mode', 'cross-component')}")
    lines.append(f"- Cross-component candidates (pre-trim): {stats.get('cross_component_candidate_count', 0)}")
    lines.append(f"- Intra-component candidates (pre-trim): {stats.get('intra_component_candidate_count', 0)}")
    lines.append(f"- Missing dependencies: {stats['missing_dependency_count']}")
    lines.append(f"- Avg semantic connection score: {stats.get('avg_semantic_connection_score', 0.0)}")
    lines.append(f"- Avg concept alignment: {stats.get('avg_concept_alignment', 0.0)}")
    lines.append(f"- Avg specificity alignment: {stats.get('avg_specificity_alignment', 0.0)}")
    lines.append(f"- Concept profile coverage: {stats.get('concept_profile_coverage', 0.0)}")
    lines.append(f"- Specific profile coverage: {stats.get('specific_profile_coverage', 0.0)}")
    lines.append(f"- Concept graph nodes: {stats.get('concept_node_count', 0)}")
    lines.append("")

    lines.append("## Top Intervention Points")
    lines.append("")
    lines.append("| statement_id | kind | score | unresolved | downstream | theory_relevance | specificity | concept_focus | partner |")
    lines.append("|---|---|---|---|---|---|---|---|---|")
    for item in report["top_interventions"]:
        m = item["metrics"]
        lines.append(
            "| {sid} | {kind} | {score} | {missing} | {downstream} | {theory} | {specificity} | {focus} | {partner} |".format(
                sid=item["statement_id"],
                kind=item["kind"],
                score=item["score"],
                missing=m["unresolved_dependencies"],
                downstream=m["downstream_impact"],
                theory=m.get("theory_relevance", 0.0),
                specificity=m.get("specificity_signal", 0.0),
                focus=", ".join(item.get("concept_focus", [])[:4]),
                partner=item["best_cross_component_partner"] or "-",
            )
        )
    lines.append("")

    lines.append("## Mathematical Concept Profiles (Interventions)")
    lines.append("")
    for item in report["top_interventions"][:12]:
        profile = item.get("concept_profile", {}) if isinstance(item.get("concept_profile"), dict) else {}
        lines.append(f"### {item['statement_id']}")
        lines.append(f"- Concept focus: {', '.join(item.get('concept_focus', [])[:6]) or '-'}")
        lines.append(
            "- Claim signatures: "
            + (", ".join(profile.get("claim_signatures", [])[:8]) if isinstance(profile.get("claim_signatures"), list) else "-")
        )
        lines.append(
            "- Antecedent signatures: "
            + (", ".join(profile.get("antecedent_signatures", [])[:8]) if isinstance(profile.get("antecedent_signatures"), list) else "-")
        )
        lines.append(
            "- Consequence signatures: "
            + (", ".join(profile.get("consequence_signatures", [])[:8]) if isinstance(profile.get("consequence_signatures"), list) else "-")
        )
        lines.append(
            "- Model signatures: "
            + (", ".join(profile.get("model_signatures", [])[:8]) if isinstance(profile.get("model_signatures"), list) else "-")
        )
        lines.append(
            "- Reduction signatures: "
            + (", ".join(profile.get("reduction_signatures", [])[:8]) if isinstance(profile.get("reduction_signatures"), list) else "-")
        )
        lines.append(
            "- Implication signatures: "
            + (", ".join(profile.get("implication_signatures", [])[:8]) if isinstance(profile.get("implication_signatures"), list) else "-")
        )
        lines.append(
            "- Complexity classes: "
            + (", ".join(profile.get("complexity_classes", [])[:8]) if isinstance(profile.get("complexity_classes"), list) else "-")
        )
        lines.append(
            "- Core problems: "
            + (", ".join(profile.get("core_problems", [])[:8]) if isinstance(profile.get("core_problems"), list) else "-")
        )
        lines.append(
            "- Proof regimes: "
            + (", ".join(profile.get("proof_regimes", [])[:8]) if isinstance(profile.get("proof_regimes"), list) else "-")
        )
        lines.append(
            "- Barrier signals: "
            + (", ".join(profile.get("barrier_signals", [])[:8]) if isinstance(profile.get("barrier_signals"), list) else "-")
        )
        lines.append("")

    lines.append("## Top Connection Candidates")
    lines.append("")
    lines.append("| from_id | to_id | score | structural_similarity | semantic | concept_alignment | specific_alignment | relation | concept_evidence |")
    lines.append("|---|---|---|---|---|---|---|---|---|")
    for item in report["connection_candidates"][:20]:
        lines.append(
            "| {from_id} | {to_id} | {score} | {similarity} | {semantic} | {concept} | {specific} | {relation} | {terms} |".format(
                from_id=item["from_id"],
                to_id=item["to_id"],
                score=item["score"],
                similarity=item["similarity"],
                semantic=item.get("semantic_score", 0.0),
                concept=item.get("concept_alignment", 0.0),
                specific=item.get("specific_alignment", 0.0),
                relation=item.get("relation", "potential-support"),
                terms=", ".join(item.get("specific_evidence", [])[:4] or item.get("concept_evidence", [])[:4] or item["evidence_terms"]),
            )
        )
    lines.append("")

    lines.append("## Abductive Loop Plan")
    lines.append("")
    for step in report["abductive_loop_plan"]:
        lines.append(f"### Round {step['round']}")
        lines.append(f"- Objective: {step['objective']}")
        if "targets" in step:
            lines.append(f"- Targets: {', '.join(step['targets'])}")
        if "candidate_connections" in step:
            pairs = [f"{c['from_id']}->{c['to_id']} ({c['score']})" for c in step["candidate_connections"][:6]]
            lines.append(f"- Candidate connections: {', '.join(pairs)}")
        lines.append(f"- Action: {step['action']}")
        lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    """
    Relevance: Operates within the relational connector layer.
    Concept: CLI entrypoint orchestration for this script.
    Contribution: Binds parsing, computation, and artifact emission into a reproducible script execution.
    """

    logger = ReasoningLogger("kb-proof-connector")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--kb", required=True, help="Path to KB markdown file.")
    parser.add_argument("--top-k", type=int, default=15, help="Number of intervention points to keep.")
    parser.add_argument(
        "--min-similarity",
        type=float,
        default=0.12,
        help="Minimum structure-first similarity for cross-component links.",
    )
    parser.add_argument(
        "--max-connections",
        type=int,
        default=40,
        help="Maximum connection candidates to keep.",
    )
    parser.add_argument(
        "--loop-rounds",
        type=int,
        default=3,
        help="Number of abductive loop rounds to include in plan.",
    )
    parser.add_argument(
        "--include-status",
        action="append",
        choices=["accepted", "tentative", "rejected"],
        default=["accepted", "tentative"],
        help="Statement statuses to include in graph analysis (repeatable).",
    )
    parser.add_argument(
        "--allow-intra-component-fallback",
        action=argparse.BooleanOptionalAction,
        default=True,
        help=(
            "When no cross-component links are available, allow high-similarity intra-component "
            "candidate links so downstream generative stages remain populated."
        ),
    )
    parser.add_argument("--output-json", help="Optional path to save JSON report.")
    parser.add_argument("--output-md", help="Optional path to save Markdown report.")
    args = parser.parse_args()
    logger.step(
        "Parsed graph-analysis arguments",
        "\n".join(
            [
                f"kb={args.kb}",
                f"top_k={args.top_k}",
                f"min_similarity={args.min_similarity}",
                f"max_connections={args.max_connections}",
                f"loop_rounds={args.loop_rounds}",
                f"include_status={args.include_status}",
                f"allow_intra_component_fallback={args.allow_intra_component_fallback}",
                f"output_json={args.output_json or ''}",
                f"output_md={args.output_md or ''}",
            ]
        ),
    )

    kb_path = Path(args.kb)
    if not kb_path.exists():
        log_path = logger.finalize("error", summary=f"KB file not found: {kb_path}")
        print(f"[LOG] {log_path}", file=sys.stderr)
        raise SystemExit(f"[ERROR] KB file not found: {kb_path}")

    try:
        report = analyze_kb(
            kb_path=kb_path,
            top_k=max(1, args.top_k),
            min_similarity=max(0.0, min(1.0, args.min_similarity)),
            max_connections=max(1, args.max_connections),
            loop_rounds=max(1, args.loop_rounds),
            include_statuses={s.strip().lower() for s in args.include_status if str(s).strip()},
            allow_intra_component_fallback=bool(args.allow_intra_component_fallback),
        )
    except Exception as exc:
        log_path = logger.finalize("error", summary=str(exc))
        print(f"[LOG] {log_path}", file=sys.stderr)
        print(f"[ERROR] {exc}", file=sys.stderr)
        return 1
    logger.step(
        "Built KB connection analysis",
        f"statement_count={report['stats']['statement_count']}\nconnection_candidates={len(report['connection_candidates'])}",
    )
    top_interventions = report.get("top_interventions", []) if isinstance(report.get("top_interventions"), list) else []
    top_links = report.get("connection_candidates", []) if isinstance(report.get("connection_candidates"), list) else []
    logger.step(
        "Concept intervention trace",
        "\n".join(
            [
                "top_interventions="
                + "; ".join(
                    f"{str(item.get('statement_id', '')).strip()}:{float(item.get('score', 0.0) or 0.0):.4f}"
                    for item in top_interventions[:6]
                    if isinstance(item, dict) and str(item.get("statement_id", "")).strip()
                ),
                "top_intervention_concepts="
                + "; ".join(
                    f"{str(item.get('statement_id', '')).strip()}[{', '.join(item.get('concept_focus', [])[:4])}]"
                    for item in top_interventions[:6]
                    if isinstance(item, dict) and str(item.get("statement_id", "")).strip()
                ),
                "top_connections="
                + "; ".join(
                    f"{str(item.get('from_id', '')).strip()}->{str(item.get('to_id', '')).strip()}:"
                    f"{float(item.get('score', 0.0) or 0.0):.4f}:"
                    f"{'/'.join(item.get('specific_evidence', [])[:3] or item.get('concept_evidence', [])[:3] or item.get('evidence_terms', [])[:3])}"
                    for item in top_links[:6]
                    if isinstance(item, dict)
                    and str(item.get("from_id", "")).strip()
                    and str(item.get("to_id", "")).strip()
                ),
            ]
        ),
    )

    if args.output_json:
        out_json = Path(args.output_json)
        out_json.parent.mkdir(parents=True, exist_ok=True)
        out_json.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print(f"[OK] Wrote JSON report: {out_json}")
        logger.add_output("connection_analysis_json", out_json)

    markdown = _to_markdown(report)
    if args.output_md:
        out_md = Path(args.output_md)
        out_md.parent.mkdir(parents=True, exist_ok=True)
        out_md.write_text(markdown, encoding="utf-8")
        print(f"[OK] Wrote Markdown report: {out_md}")
        logger.add_output("connection_analysis_md", out_md)

    print(f"[OK] Statement count: {report['stats']['statement_count']}")
    print(f"[OK] Connection candidates: {len(report['connection_candidates'])}")
    print(f"[OK] Top intervention points: {len(report['top_interventions'])}")
    log_path = logger.finalize(
        "success",
        summary=f"Computed {len(report['top_interventions'])} intervention points and {len(report['connection_candidates'])} candidate links.",
    )
    print(f"[LOG] {log_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
