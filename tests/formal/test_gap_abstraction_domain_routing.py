# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT

"""
Regression tests for domain-aware abstraction conjecturing.

Concept: The abstraction layer should use typed bridge context to choose mathematical object families.
Contribution: Prevents semigroup/operator-theory KBs from leaking into complexity-style pseudorandomness templates.
"""

from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
CONJECTURE_SCRIPTS = ROOT / "skills" / "discovery" / "kb-gap-abstraction-conjecturer" / "scripts"
if str(CONJECTURE_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(CONJECTURE_SCRIPTS))

from conjecture_gap_abstractions import _template_scores


def test_template_scores_do_not_treat_operator_generator_as_pseudorandom() -> None:
    """
    Concept: Validates that the word `generator` inside Stone-style operator theory does not trigger complexity-only templates.
    Contribution: Keeps abstraction conjectures mathematically faithful when multiple domains reuse the same lexical token.
    """

    context = {
        "bridge_type": "stone-self-adjointness-bridge",
        "terms": [
            "strongly-continuous-unitary-group",
            "unique-self-adjoint-generator",
            "spectral theorem",
            "functional calculus",
            "generator-definition",
        ],
        "gap_axes": ["missing-intermediate-abstraction", "transfer-mechanism-gap"],
        "conceptual_kinds": [],
        "target_consequence_schema": "stone-self-adjoint-correspondence",
        "preserved_invariant": "self-adjoint generator recovery in strongly-continuous-unitary-group",
        "model_terms": ["strongly-continuous-unitary-group", "self-adjoint-spectral-calculus"],
    }

    scores = _template_scores(context)

    assert scores["pseudorandom-object"] == 0.0
    assert scores["self-adjoint-generator-core"] > 0.0
    assert scores["spectral-measure-interface"] > 0.0


def test_template_scores_route_riesz_context_to_measure_families() -> None:
    """
    Concept: Validates that measure-representation contexts produce measure-side abstraction families instead of generic probabilistic templates.
    Contribution: Keeps discovery prompts focused on regularity and representation objects rather than loose uses of the token `measure`.
    """

    context = {
        "bridge_type": "measure-representation-bridge",
        "terms": [
            "riesz-markov-kakutani-correspondence",
            "positive-functional-implies-regular-measure",
            "regular-borel-measure-model",
            "compact-open-approximation",
            "positive-linear-functional-on-cc-space",
        ],
        "gap_axes": ["missing-intermediate-abstraction", "transfer-mechanism-gap", "barrier-pressure"],
        "conceptual_kinds": [],
        "target_consequence_schema": "regular-borel-measure-representation",
        "preserved_invariant": "regular-Borel representation in locally-compact-Hausdorff-space",
        "model_terms": ["locally-compact-Hausdorff-space", "regular-Borel-measure-model"],
    }

    scores = _template_scores(context)

    assert scores["pseudorandom-object"] == 0.0
    assert scores["measure-functional-interface"] > 0.0
    assert scores["regular-borel-envelope"] > 0.0


def test_template_scores_route_markov_kakutani_context_to_fixed_point_families() -> None:
    """
    Concept: Validates that convex fixed-point contexts produce invariant-subset and compactness abstractions instead of generic reduction templates.
    Contribution: Keeps discovery prompts focused on the actual bridge object in the Markov-Kakutani proof.
    """

    context = {
        "bridge_type": "fixed-point-subset-bridge",
        "terms": [
            "markov-kakutani-common-fixed-point",
            "invariant-fixed-point-subset",
            "commutativity-implies-fixed-point-subset-invariance",
            "finite-intersection-property-implies-common-fixed-point",
            "compact-convex-set",
        ],
        "gap_axes": ["missing-intermediate-abstraction", "transfer-mechanism-gap", "barrier-pressure"],
        "conceptual_kinds": [],
        "target_consequence_schema": "common-fixed-point-for-commuting-family",
        "preserved_invariant": "nonempty compact-convex fixed-point subset in invariant-fixed-point-subset",
        "model_terms": ["commuting-affine-self-map-family", "invariant-fixed-point-subset"],
    }

    scores = _template_scores(context)

    assert scores["pseudorandom-object"] == 0.0
    assert scores["invariant-fixed-point-core"] > 0.0
    assert scores["finite-intersection-lift"] > 0.0
