"""Meaning profiles, essential fragmentation, and plural reflection."""

from __future__ import annotations

from typing import Any

from tdr.domain.models import FragmentationSite, MEANING_FIELDS, MeaningProfile, ReflectionRecord, bounded, stable_id


LENSES = {
    "hermeneutic": "How does the concept acquire sense within each theory's whole?",
    "phenomenological-operational": "What is given, measured, or enacted before formal abstraction?",
    "constitutive": "Which conditions make the object or evidence possible?",
    "dialectical-immanent": "Which internal opposition drives the theory beyond its current form?",
    "genealogical": "Which historical choices became invisible constraints?",
    "pragmatic": "What inferential and practical work does the concept perform?",
    "structural-realist": "Which relations survive changes of representation?",
    "modal-counterfactual": "What varies across nearby possible worlds, and what remains necessary?",
}

OPERATORS = (
    "Suspend",
    "PrimitiveShift",
    "DependencyInvert",
    "ContextInternalize",
    "LevelShift",
    "IdentityRevise",
    "InvariantExtract",
    "ObstructionReify",
    "Dualize",
    "BoundaryProbe",
    "Counterworld",
    "OperationalReanchor",
)

REPAIRS = (
    "lexical normalization",
    "unit and notation alignment",
    "definitional extension",
    "known equivalence",
    "conservative interpretation",
    "scope restriction",
)


def profile_meaning(payload: dict[str, Any]) -> MeaningProfile:
    concept_id = str(payload.get("concept_id") or "unknown-concept")
    theory_id = str(payload.get("theory_id") or "unknown-theory")
    components = dict(payload.get("components") or {})
    uncertainty: dict[str, float] = dict(payload.get("uncertainty") or {})
    normalized: dict[str, list[str]] = {}
    for field_name in MEANING_FIELDS:
        value = payload.get(field_name, components.get(field_name))
        if value in (None, "", []):
            normalized[field_name] = ["unknown"]
            uncertainty.setdefault(field_name, 1.0)
        elif isinstance(value, str):
            normalized[field_name] = [value]
            uncertainty.setdefault(field_name, 0.35)
        else:
            normalized[field_name] = [str(item) for item in value]
            uncertainty.setdefault(field_name, 0.2)
    return MeaningProfile(
        profile_id=str(payload.get("profile_id") or stable_id("meaning", [concept_id, theory_id, normalized])),
        concept_id=concept_id,
        theory_id=theory_id,
        evidence=list(payload.get("evidence", [])),
        uncertainty={key: bounded(value, 1.0) for key, value in uncertainty.items()},
        **normalized,
    )


def _tokens(values: Any) -> set[str]:
    if not isinstance(values, list):
        values = [values]
    tokens: set[str] = set()
    for value in values:
        tokens.update(word.strip(".,:;()[]{}").lower() for word in str(value).split() if word)
    return tokens - {"unknown", "the", "a", "an", "of", "and", "to", "in"}


def _distance(left: Any, right: Any) -> float:
    a, b = _tokens(left), _tokens(right)
    if not a and not b:
        return 0.0
    return 1.0 - len(a & b) / max(1, len(a | b))


def detect_fragmentation(payload: dict[str, Any]) -> FragmentationSite:
    profiles = [dict(item) for item in payload.get("profiles", [])]
    if len(profiles) < 2:
        raise ValueError("at least two meaning profiles are required")
    left, right = profiles[0], profiles[1]
    mismatch = {field_name: round(_distance(left.get(field_name, []), right.get(field_name, [])), 4) for field_name in MEANING_FIELDS}
    attempts: list[dict[str, Any]] = []
    explicit_repairs = dict(payload.get("repair_results") or {})
    repair_effect = 0.0
    for index, repair in enumerate(REPAIRS):
        success = bool(explicit_repairs.get(repair, False))
        reduction = float(explicit_repairs.get(f"{repair}:reduction", 0.05 if success else 0.0))
        repair_effect += max(0.0, reduction)
        attempts.append({"repair": repair, "success": success, "estimated_reduction": bounded(reduction)})
    raw = sum(mismatch.values()) / len(mismatch)
    residual = bounded(raw - repair_effect)
    protected_left = set(left.get("protected_distinctions", []))
    protected_right = set(right.get("protected_distinctions", []))
    protected_losses = sorted((protected_left ^ protected_right) - {"unknown"})
    impact = bounded(payload.get("downstream_impact", 0.5), 0.5)
    essentiality = bounded(residual * (0.55 + 0.45 * impact) + min(0.25, 0.08 * len(protected_losses)))
    review = bool(protected_losses) or bool(payload.get("changes_operational_commitments"))
    return FragmentationSite(
        site_id=str(payload.get("site_id") or stable_id("site", [left.get("profile_id"), right.get("profile_id"), mismatch])),
        concept_ids=[str(left.get("concept_id")), str(right.get("concept_id"))],
        theory_ids=[str(left.get("theory_id")), str(right.get("theory_id"))],
        mismatch_vector=mismatch,
        cheap_repairs_attempted=attempts,
        residual_fragmentation=residual,
        essentiality=essentiality,
        protected_losses=protected_losses,
        downstream_targets=[str(item) for item in payload.get("downstream_targets", [])],
        human_review_required=review,
    )


def run_reflection(payload: dict[str, Any]) -> ReflectionRecord:
    site = dict(payload.get("site") or {})
    profiles = [dict(item) for item in payload.get("profiles", [])]
    if not site:
        raise ValueError("fragmentation site is required")
    concept = " / ".join(site.get("concept_ids", ["contested concept"]))
    theories = " and ".join(site.get("theory_ids", ["the compared theories"]))
    losses = list(site.get("protected_losses", [])) or ["loss of a native inferential distinction"]
    highest = sorted((site.get("mismatch_vector") or {}).items(), key=lambda item: (-float(item[1]), str(item[0])))[:3]
    pressure_fields = [name for name, score in highest if score > 0]
    lens_outputs: dict[str, dict[str, Any]] = {}
    for lens, question in LENSES.items():
        lens_outputs[lens] = {
            "question": question,
            "interpretation": f"Under the {lens} lens, {concept} should be compared through {', '.join(pressure_fields) or 'its native role'}, not name identity alone.",
            "preserve": losses,
            "risk": f"The {lens} redescription may privilege one sense used in {theories}.",
            "source_grounded": bool(profiles),
        }
    redescriptions = [
        {
            "operator": "PrimitiveShift",
            "description": f"Treat the relation coordinating {concept} as primitive and recover the former objects as contextual presentations.",
            "cost": "changes the primitive ontology",
        },
        {
            "operator": "ContextInternalize",
            "description": f"Index {concept} by regime and represent translations as structure-preserving context changes.",
            "cost": "adds contextual structure",
        },
        {
            "operator": "InvariantExtract",
            "description": f"Keep both native concepts and identify only the relations invariant under validated translations.",
            "cost": "conservative but may unify less",
        },
    ]
    counterworlds = [
        f"A world where the two uses of {concept} agree extensionally but support different interventions.",
        f"A boundary regime where the proposed translation preserves equations but reverses explanatory dependence.",
    ]
    formal = [f"type the {item} mismatch and state its preservation obligation" for item in pressure_fields] or ["type the proposed context change"]
    concrete = [f"construct a discriminating example for {item}" for item in pressure_fields] or ["construct a model separating the redescriptions"]
    return ReflectionRecord(
        reflection_id=str(payload.get("reflection_id") or stable_id("reflection", [site.get("site_id"), lens_outputs])),
        site_id=str(site.get("site_id", "unknown-site")),
        lens_outputs=lens_outputs,
        convergence=["name identity is insufficient", "scope and operation must travel with the concept"],
        contradictions=["primitive-ontology revision conflicts with conservative retention"],
        redescriptions=redescriptions,
        preserved_commitments=losses,
        anticipated_losses=losses,
        counterworlds=counterworlds,
        formal_obligations=formal,
        concrete_obligations=concrete,
        source_refs=[ref for profile in profiles for ref in profile.get("evidence", [])],
    )


def diagnose_defect(payload: dict[str, Any]) -> list[dict[str, Any]]:
    site = dict(payload.get("site") or {})
    reflection = dict(payload.get("reflection") or {})
    mismatches = site.get("mismatch_vector") or {}
    candidates: list[dict[str, Any]] = []
    mapping = {
        "identity_criteria": "representability",
        "inferential_commitments": "coherence",
        "scale_and_scope": "descent",
        "operational_anchors": "factorization",
        "explanatory_role": "adjunction",
        "protected_distinctions": "obstruction",
        "modal_commitments": "meta-theory",
    }
    for field_name, score in sorted(mismatches.items(), key=lambda item: (-float(item[1]), str(item[0]))):
        if float(score) < 0.35:
            continue
        kind = mapping.get(field_name, "coherence")
        candidates.append({
            "defect_id": stable_id("defect", [site.get("site_id"), field_name, kind]),
            "kind": kind,
            "source_field": field_name,
            "severity": bounded(score),
            "required_objects": [f"context for {theory}" for theory in site.get("theory_ids", [])],
            "required_morphisms": [f"typed comparison preserving {field_name}"],
            "obligations": [f"prove whether the {field_name} square commutes up to declared equivalence"],
            "metaphorical": not bool(site.get("theory_ids")) or not bool(reflection.get("formal_obligations")),
        })
    if not candidates:
        candidates.append({
            "defect_id": stable_id("defect", site),
            "kind": "underdetermined",
            "source_field": "unknown",
            "severity": 0.25,
            "required_objects": [],
            "required_morphisms": [],
            "obligations": ["supply typed objects and a discriminating diagram"],
            "metaphorical": True,
        })
    return candidates
