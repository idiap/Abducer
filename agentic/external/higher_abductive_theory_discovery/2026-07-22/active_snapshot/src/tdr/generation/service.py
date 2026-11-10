"""Diverse, typed candidate generation with conservative normalization."""

from __future__ import annotations

import re
from typing import Any

from tdr.domain.models import HypothesisPackage, stable_id
from .provider import DeterministicProvider, GeneratorProvider


MODES = ("local", "bridge", "mechanism", "mutation")


def _dominant_defect(defects: list[dict[str, Any]]) -> dict[str, Any]:
    if not defects:
        return {"kind": "underdetermined", "source_field": "unknown", "severity": 0.2}
    return max(defects, key=lambda item: float(item.get("severity", 0.0)))


def _normalize(text: str) -> str:
    return re.sub(r"\W+", " ", text.lower()).strip()


def _build_candidate(
    mode: str,
    index: int,
    pressures: list[dict[str, Any]],
    reflections: list[dict[str, Any]],
    defects: list[dict[str, Any]],
    provider_proposal: dict[str, Any] | None = None,
) -> HypothesisPackage:
    defect = _dominant_defect(defects)
    pressure_ids = [str(item.get("pressure_id")) for item in pressures if item.get("pressure_id")]
    reflection_ids = [str(item.get("reflection_id")) for item in reflections if item.get("reflection_id")]
    locus = ", ".join(str(item.get("description", "pressure")) for item in pressures[:2]) or "the scoped pressure"
    kind = str(defect.get("kind", "coherence"))
    moves = {
        "local": f"Adjoin the minimal typed witness resolving the {kind} defect at {locus}",
        "bridge": f"Construct a scope-indexed interpretation functor with a higher coherence cell for {kind}",
        "mechanism": f"Introduce a mediating dynamics whose invariant recovers both presentations of {kind}",
        "mutation": f"Replace object-first representation by a contextual relation grammar exposing {kind} as data",
    }
    formal_move = str((provider_proposal or {}).get("proposal") or moves[mode])
    title = f"{mode.capitalize()} {kind} candidate {index + 1}"
    return HypothesisPackage(
        candidate_id=stable_id("candidate", [mode, formal_move, pressure_ids, reflection_ids]),
        mode=mode,
        title=title,
        pressure_ids=pressure_ids,
        reflection_ids=reflection_ids,
        formal_move=formal_move,
        atlas_patch={
            "operation": {"local": "adjoin", "bridge": "add_morphism", "mechanism": "add_dynamics", "mutation": "change_grammar"}[mode],
            "defect_kind": kind,
            "objects": defect.get("required_objects", []),
            "morphisms": defect.get("required_morphisms", []),
        },
        assumptions=["declared scopes are compatible", f"the {kind} diagnosis is non-metaphorical"],
        consequences=[
            f"the dominant {kind} obligation becomes expressible",
            "at least one source fragment is recovered as a restriction",
            "a held-out comparison can discriminate the proposal",
        ],
        falsifiers=[
            "no typed model exists",
            "the construction collapses a protected distinction",
            "the return map yields no new derivation, observable, or operation",
        ],
        return_paths=[
            {"target": "mathematical model", "method": "finite witness or proof-assistant instance"},
            {"target": "concrete consequence", "method": "derive a held-out equation, algorithm, or measurement"},
        ],
        relevance_vector={},
        validation_tasks=[
            {"type": "type_check", "cost": 0.15},
            {"type": "model_search", "cost": 0.25},
            {"type": "scope_stress", "cost": 0.2},
        ],
        uncertainty={"diagnosis": 0.35, "formalization": 0.5, "concrete_return": 0.55},
    )


def generate_candidates(payload: dict[str, Any], provider: GeneratorProvider | None = None) -> list[HypothesisPackage]:
    pressures = [dict(item) for item in payload.get("pressures", [])]
    reflections = [dict(item) for item in payload.get("reflections", [])]
    defects = [dict(item) for item in payload.get("defects", [])]
    modes = [mode for mode in payload.get("modes", MODES) if mode in MODES]
    if not modes:
        modes = list(MODES)
    provider = provider or DeterministicProvider()
    provider_outputs = provider.generate(
        "Propose a typed theory completion",
        {"modes": modes, "pressures": pressures, "reflections": reflections, "defects": defects},
        seed=int(payload.get("seed", 0)),
        n=len(modes),
    )
    candidates: list[HypothesisPackage] = []
    seen: set[str] = set()
    for index, mode in enumerate(modes):
        proposal = provider_outputs[index] if index < len(provider_outputs) else None
        candidate = _build_candidate(mode, index, pressures, reflections, defects, proposal)
        key = _normalize(candidate.formal_move)
        if key in seen or not candidate.atlas_patch or not candidate.validation_tasks:
            continue
        seen.add(key)
        candidates.append(candidate)
    return candidates

