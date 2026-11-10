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

"""Typed discovery-calculus prototype for bounded non-LLM search."""

from __future__ import annotations

from dataclasses import asdict
from dataclasses import dataclass
from enum import Enum
from typing import Any

from mathematical_layers import build_mathematical_layers


def _clean_text(value: Any) -> str:
    return " ".join(str(value or "").strip().split())


class BridgeShape(str, Enum):
    """Finite bridge-shape fragment for bounded symbolic discovery search."""

    REALIZATION = "realization"
    TRANSPORT = "transport"
    EQUIVALENCE = "equivalence"
    FACTORIZATION = "factorization"
    OBSTRUCTION = "obstruction"


@dataclass(frozen=True)
class RouteSignature:
    """Typed route state suitable for bounded discovery search."""

    source_statement_id: str
    target_statement_id: str
    source_regime: str
    target_regime: str
    invariant: str
    candidate_object: str
    branch_family: str = ""
    source_excerpt: str = ""
    target_excerpt: str = ""
    multiple_operationalizations: bool = False
    equivalence_pressure: bool = False
    factorization_pressure: bool = False
    negative_pressure: bool = False
    under_typed_carrier: bool = False
    barrier_scope: str = ""


@dataclass(frozen=True)
class SearchReadiness:
    """Assessment of whether non-LLM symbolic search is appropriate yet."""

    mode: str
    score: int
    blockers: tuple[str, ...]
    reasons: tuple[str, ...]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class DiscoveryCandidate:
    """A theorem-sized bridge candidate produced by bounded search."""

    shape: str
    title: str
    theorem_statement: str
    obligations: tuple[str, ...]
    pdl_operations: tuple[str, ...]
    rationale: str
    search_score: float
    mathematical_layers: dict[str, Any]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def assess_symbolic_search_readiness(route: RouteSignature) -> SearchReadiness:
    """Decide whether the discovery state is typed enough for symbolic search."""

    blockers: list[str] = []
    reasons: list[str] = []
    score = 0

    if _clean_text(route.source_statement_id):
        score += 1
    else:
        blockers.append("missing source statement id")
    if _clean_text(route.target_statement_id):
        score += 1
    else:
        blockers.append("missing target statement id")
    if _clean_text(route.source_regime):
        score += 1
    else:
        blockers.append("missing source regime")
    if _clean_text(route.target_regime):
        score += 1
    else:
        blockers.append("missing target regime")
    if _clean_text(route.invariant):
        score += 1
        reasons.append("the preserved invariant is named")
    else:
        blockers.append("missing preserved invariant")
    if _clean_text(route.candidate_object) and not bool(route.under_typed_carrier):
        score += 1
        reasons.append("the bridge carrier is named and not marked under-typed")
    else:
        blockers.append("candidate object is missing or still under-typed")
    if _clean_text(route.source_excerpt):
        score += 1
    if _clean_text(route.target_excerpt):
        score += 1
    if _clean_text(route.branch_family):
        score += 1
        reasons.append("the route already names a discovery branch family")
    if bool(route.multiple_operationalizations):
        score += 1
        reasons.append("multiple operationalizations are live, so typed equivalence search is meaningful")
    elif bool(route.equivalence_pressure):
        score += 1
        reasons.append("the route is explicitly equivalence- or coherence-facing")
    if bool(route.factorization_pressure):
        score += 1
        reasons.append("the route is diagrammatic enough for factorization search")
    if bool(route.negative_pressure):
        score += 1
        reasons.append("negative pressure is explicit, so bounded obstruction search is meaningful")

    if blockers:
        if score >= 6:
            return SearchReadiness(
                mode="hybrid-llm-plus-symbolic",
                score=score,
                blockers=tuple(blockers),
                reasons=tuple(reasons + ["the route is partially typed but still needs LLM mediation on missing fields"]),
            )
        return SearchReadiness(
            mode="llm-first",
            score=score,
            blockers=tuple(blockers),
            reasons=tuple(reasons + ["the route is still too schematic for bounded symbolic search"]),
        )

    return SearchReadiness(
        mode="symbolic-search-ready",
        score=score,
        blockers=tuple(),
        reasons=tuple(reasons + ["the route is typed enough for bounded search over bridge shapes"]),
    )


def _shape_priority(shape: BridgeShape, route: RouteSignature) -> float:
    if shape is BridgeShape.TRANSPORT and route.source_regime != route.target_regime:
        return 0.96
    if shape is BridgeShape.EQUIVALENCE and route.multiple_operationalizations:
        return 0.94
    if shape is BridgeShape.OBSTRUCTION and route.negative_pressure:
        return 0.92
    if shape is BridgeShape.FACTORIZATION and "categorical" in _clean_text(route.branch_family).lower():
        return 0.90
    if shape is BridgeShape.REALIZATION:
        return 0.88
    return 0.75


def enumerate_bridge_shapes(route: RouteSignature) -> list[BridgeShape]:
    """Enumerate the finite bridge-shape search space for a typed route."""

    ordered: list[BridgeShape] = [BridgeShape.REALIZATION]
    if route.source_regime != route.target_regime:
        ordered.append(BridgeShape.TRANSPORT)
    family = _clean_text(route.branch_family).lower()
    if route.multiple_operationalizations or bool(route.equivalence_pressure) or any(
        token in family for token in ("equivalence", "coherence", "alignment", "semantic-bridge")
    ):
        ordered.append(BridgeShape.EQUIVALENCE)
    if bool(route.factorization_pressure) or any(token in family for token in ("categorical", "decomposition", "factorization")):
        ordered.append(BridgeShape.FACTORIZATION)
    if route.negative_pressure or route.under_typed_carrier or bool(_clean_text(route.barrier_scope)):
        ordered.append(BridgeShape.OBSTRUCTION)
    deduped: list[BridgeShape] = []
    for item in ordered:
        if item not in deduped:
            deduped.append(item)
    return deduped


def _shape_mode(shape: BridgeShape) -> str:
    if shape is BridgeShape.TRANSPORT:
        return "transport-lemma"
    if shape is BridgeShape.EQUIVALENCE:
        return "equivalence-theorem"
    if shape is BridgeShape.OBSTRUCTION:
        return "no-go-theorem"
    return "special-case"


def _shape_title(shape: BridgeShape, route: RouteSignature) -> str:
    stem = _clean_text(route.candidate_object) or "bridge object"
    if shape is BridgeShape.REALIZATION:
        return f"Realization theorem for {stem}"
    if shape is BridgeShape.TRANSPORT:
        return f"Transport theorem for {stem}"
    if shape is BridgeShape.EQUIVALENCE:
        return f"Equivalence theorem for {stem}"
    if shape is BridgeShape.FACTORIZATION:
        return f"Factorization theorem for {stem}"
    return f"Obstruction theorem for {stem}"


def _shape_statement(shape: BridgeShape, route: RouteSignature) -> str:
    obj = _clean_text(route.candidate_object) or "bridge object"
    invariant = _clean_text(route.invariant) or "route invariant"
    source = _clean_text(route.source_excerpt) or _clean_text(route.source_statement_id)
    target = _clean_text(route.target_excerpt) or _clean_text(route.target_statement_id)
    if shape is BridgeShape.REALIZATION:
        return _clean_text(
            f"There exists an admissible `{obj}` whose realization internalizes `{source}` while preserving `{invariant}` strongly enough to support `{target}`."
        )
    if shape is BridgeShape.TRANSPORT:
        return _clean_text(
            f"For every admissible `{obj}`, there is a transport law from `{route.source_regime}` to `{route.target_regime}` that preserves `{invariant}` and retains enough strength to activate `{target}`."
        )
    if shape is BridgeShape.EQUIVALENCE:
        return _clean_text(
            f"For every admissible `{obj}`, the route-side and target-side operationalizations are equivalent in the sense needed to transport `{invariant}` toward `{target}`."
        )
    if shape is BridgeShape.FACTORIZATION:
        return _clean_text(
            f"There exists an intermediate typed object built from `{obj}` such that the route from `{source}` to `{target}` factors through theorem-sized maps preserving `{invariant}`."
        )
    return _clean_text(
        f"No admissible `{obj}` can simultaneously preserve `{invariant}` and realize `{target}` under the current route commitments."
    )


def _shape_obligations(shape: BridgeShape, route: RouteSignature) -> tuple[str, ...]:
    obj = _clean_text(route.candidate_object) or "bridge object"
    invariant = _clean_text(route.invariant) or "route invariant"
    if shape is BridgeShape.REALIZATION:
        return (
            f"Define the admissibility predicate for `{obj}`.",
            f"Construct a local witness term for `{obj}` from the source theorem body.",
            f"Show the realization preserves `{invariant}`.",
            "Show the realized carrier is strong enough to activate the target theorem.",
        )
    if shape is BridgeShape.TRANSPORT:
        return (
            f"Define a typed transport map from `{route.source_regime}` to `{route.target_regime}`.",
            f"Prove that the transport preserves `{invariant}`.",
            "Prove that the transported object retains enough quantitative strength for the target payoff.",
        )
    if shape is BridgeShape.EQUIVALENCE:
        return (
            "Define the route-side and target-side operationalizations as explicit types.",
            f"Construct the equivalence witness for `{obj}`.",
            f"Prove transport of `{invariant}` across the equivalence.",
            "Prove the required coherence or naturality law.",
        )
    if shape is BridgeShape.FACTORIZATION:
        return (
            "Name the intermediate object through which the route factors.",
            "Construct the first map from the source-side object into the intermediate object.",
            "Construct the second map from the intermediate object into the target-side object.",
            f"Prove the factorization preserves `{invariant}` and commutes with the intended payoff.",
        )
    return (
        f"State the exact non-realization claim for `{obj}`.",
        f"Name the barrier or contradiction target preventing preservation of `{invariant}`.",
        "Prove that every candidate witness collapses into the named obstruction.",
    )


def _shape_operations(shape: BridgeShape) -> tuple[str, ...]:
    if shape is BridgeShape.REALIZATION:
        return ("ext", "conc", "route")
    if shape is BridgeShape.TRANSPORT:
        return ("foc", "tr", "route")
    if shape is BridgeShape.EQUIVALENCE:
        return ("foc", "conc", "tr", "route")
    if shape is BridgeShape.FACTORIZATION:
        return ("foc", "fac", "comp", "route")
    return ("foc", "obs", "rev", "route")


def _shape_rationale(shape: BridgeShape, route: RouteSignature) -> str:
    if shape is BridgeShape.TRANSPORT:
        return _clean_text(
            f"The source and target regimes differ (`{route.source_regime}` -> `{route.target_regime}`), so bounded search should test typed transport laws before asking the LLM for new abstractions."
        )
    if shape is BridgeShape.EQUIVALENCE:
        return "Multiple operationalizations are live, so a symbolic equivalence/coherence search can test whether the route is merely renaming the same object."
    if shape is BridgeShape.FACTORIZATION:
        return "The branch family is diagrammatic enough that a finite factorization search is more appropriate than more prose-first route generation."
    if shape is BridgeShape.OBSTRUCTION:
        return "Negative pressure is explicit, so symbolic search should test a theorem-shaped impossibility candidate instead of only refining the constructive route."
    return "The carrier is already named, so the first bounded search step is to test a realization theorem rather than ask for another abstraction."


def build_candidates_for_shapes(
    route: RouteSignature,
    shapes: list[BridgeShape] | tuple[BridgeShape, ...],
    *,
    max_candidates: int = 5,
) -> list[DiscoveryCandidate]:
    """Build theorem packets for an externally supplied bridge-shape result."""

    candidates: list[DiscoveryCandidate] = []
    for shape in list(shapes)[: max(0, int(max_candidates))]:
        title = _shape_title(shape, route)
        statement = _shape_statement(shape, route)
        mode = _shape_mode(shape)
        layers = build_mathematical_layers(
            title=title,
            exact_statement=statement,
            route_synopsis=(
                f"Move from `{route.source_statement_id}` in `{route.source_regime}` toward `{route.target_statement_id}` in `{route.target_regime}`."
            ),
            bridge_name=route.candidate_object,
            invariant=route.invariant,
            mode=mode,
            source_statement_id=route.source_statement_id,
            target_statement_id=route.target_statement_id,
            source_excerpt=route.source_excerpt,
            target_excerpt=route.target_excerpt,
            admissibility_conditions=[f"`{route.candidate_object}` is explicitly defined in the current route."],
            first_nontrivial_lemma_title=title,
            first_nontrivial_lemma_statement=_shape_obligations(shape, route)[0],
            negative_barrier_version=_shape_statement(BridgeShape.OBSTRUCTION, route)
            if shape is not BridgeShape.OBSTRUCTION
            else statement,
        )
        candidates.append(
            DiscoveryCandidate(
                shape=shape.value,
                title=title,
                theorem_statement=statement,
                obligations=_shape_obligations(shape, route),
                pdl_operations=_shape_operations(shape),
                rationale=_shape_rationale(shape, route),
                search_score=_shape_priority(shape, route),
                mathematical_layers=layers,
            )
        )
    candidates.sort(key=lambda row: row.search_score, reverse=True)
    return candidates[: max(0, int(max_candidates))]


def bounded_bridge_search(route: RouteSignature, *, max_candidates: int = 5) -> list[DiscoveryCandidate]:
    """Enumerate theorem-sized bridge candidates in a finite typed fragment."""

    readiness = assess_symbolic_search_readiness(route)
    if readiness.mode == "llm-first":
        return []
    return build_candidates_for_shapes(
        route,
        enumerate_bridge_shapes(route),
        max_candidates=max_candidates,
    )
