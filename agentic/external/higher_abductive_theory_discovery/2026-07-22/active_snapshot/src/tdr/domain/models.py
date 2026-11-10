"""Canonical records and serialization for the discovery system.

The runtime accepts plain dictionaries at its public boundary, while these
records provide stable internal semantics and JSON-safe serialization.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field, is_dataclass
from datetime import datetime, timezone
from enum import Enum
import hashlib
import json
from typing import Any, Iterable, Mapping
from uuid import uuid4


SCHEMA_VERSION = "1.0"


class Lifecycle(str, Enum):
    STAGED = "staged"
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    SUPERSEDED = "superseded"


class ResultStatus(str, Enum):
    COMPLETED = "completed"
    PARTIAL = "partial"
    BLOCKED = "blocked"
    INVALID = "invalid"


class RunPhase(str, Enum):
    NEW = "NEW"
    SCOPED = "SCOPED"
    MAPPED = "MAPPED"
    PRESSURED = "PRESSURED"
    FRAGMENTED = "FRAGMENTED"
    REFLECTED = "REFLECTED"
    GENERATED = "GENERATED"
    GATED = "GATED"
    FORMALIZED = "FORMALIZED"
    INSTANTIATED = "INSTANTIATED"
    TESTED = "TESTED"
    SYNTHESIZED = "SYNTHESIZED"
    REPRESENTATION_REVIEW = "REPRESENTATION_REVIEW"
    BLOCKED = "BLOCKED"


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def stable_id(prefix: str, value: Any | None = None) -> str:
    if value is None:
        return f"{prefix}-{uuid4().hex[:12]}"
    payload = canonical_json(value).encode("utf-8")
    return f"{prefix}-{hashlib.sha256(payload).hexdigest()[:12]}"


def jsonable(value: Any) -> Any:
    if is_dataclass(value):
        return {key: jsonable(item) for key, item in asdict(value).items()}
    if isinstance(value, Enum):
        return value.value
    if isinstance(value, Mapping):
        return {str(key): jsonable(item) for key, item in value.items()}
    if isinstance(value, (list, tuple, set)):
        return [jsonable(item) for item in value]
    return value


def canonical_json(value: Any) -> str:
    return json.dumps(jsonable(value), sort_keys=True, separators=(",", ":"), ensure_ascii=False)


@dataclass(slots=True)
class Provenance:
    source_set: list[str] = field(default_factory=list)
    skill_version: str = "0.1.0"
    model_id: str = "deterministic-local"
    prompt_hash: str = ""
    parameters: dict[str, Any] = field(default_factory=dict)
    seed: int = 0
    parent_artifacts: list[str] = field(default_factory=list)
    created_at: str = field(default_factory=utc_now)


@dataclass(slots=True)
class EvidenceRef:
    artifact_id: str
    locator: str
    evidence_type: str
    reliability: float

    def __post_init__(self) -> None:
        if self.evidence_type not in {"proof", "paper", "data", "simulation", "expert", "conjecture"}:
            raise ValueError(f"unsupported evidence_type: {self.evidence_type}")
        if not 0.0 <= self.reliability <= 1.0:
            raise ValueError("reliability must be in [0, 1]")


@dataclass(slots=True)
class ResearchContext:
    context_id: str
    question: str
    goals: list[str]
    scope: dict[str, Any]
    protected_commitments: list[str]
    success_criteria: list[str]
    stop_criteria: list[str]
    budgets: dict[str, float]
    schema_version: str = SCHEMA_VERSION
    lifecycle: str = Lifecycle.STAGED.value
    provenance: Provenance = field(default_factory=Provenance)


@dataclass(slots=True)
class TheoryFragment:
    fragment_id: str
    name: str
    sorts: list[str]
    symbols: dict[str, str]
    axioms: list[str]
    claims: list[dict[str, Any]]
    models: list[str]
    observables: list[str]
    regime: dict[str, Any]
    source_refs: list[dict[str, Any]]
    schema_version: str = SCHEMA_VERSION
    lifecycle: str = Lifecycle.STAGED.value
    provenance: Provenance = field(default_factory=Provenance)


@dataclass(slots=True)
class TheoryMorphism:
    morphism_id: str
    source_fragment_id: str
    target_fragment_id: str
    symbol_map: dict[str, str]
    scope_map: dict[str, Any]
    obligations: list[str]
    total_on_declared_domain: bool
    schema_version: str = SCHEMA_VERSION
    lifecycle: str = Lifecycle.STAGED.value
    provenance: Provenance = field(default_factory=Provenance)


@dataclass(slots=True)
class HigherCell:
    cell_id: str
    left_morphism_id: str
    right_morphism_id: str
    witness_kind: str
    witness: str
    obligations: list[str]
    schema_version: str = SCHEMA_VERSION
    lifecycle: str = Lifecycle.STAGED.value
    provenance: Provenance = field(default_factory=Provenance)


@dataclass(slots=True)
class PressureItem:
    pressure_id: str
    kind: str
    description: str
    locus: list[str]
    evidence: list[dict[str, Any]]
    severity: float
    downstream_impact: float
    reliability: float
    preferred_solution: str | None = None
    schema_version: str = SCHEMA_VERSION
    lifecycle: str = Lifecycle.STAGED.value
    provenance: Provenance = field(default_factory=Provenance)


MEANING_FIELDS = (
    "referential_role",
    "inferential_commitments",
    "identity_criteria",
    "modal_commitments",
    "operational_anchors",
    "scale_and_scope",
    "explanatory_role",
    "pragmatic_uses",
    "protected_distinctions",
)


@dataclass(slots=True)
class MeaningProfile:
    profile_id: str
    concept_id: str
    theory_id: str
    referential_role: list[str]
    inferential_commitments: list[str]
    identity_criteria: list[str]
    modal_commitments: list[str]
    operational_anchors: list[str]
    scale_and_scope: list[str]
    explanatory_role: list[str]
    pragmatic_uses: list[str]
    protected_distinctions: list[str]
    evidence: list[dict[str, Any]]
    uncertainty: dict[str, float]
    schema_version: str = SCHEMA_VERSION
    lifecycle: str = Lifecycle.STAGED.value
    provenance: Provenance = field(default_factory=Provenance)


@dataclass(slots=True)
class FragmentationSite:
    site_id: str
    concept_ids: list[str]
    theory_ids: list[str]
    mismatch_vector: dict[str, float]
    cheap_repairs_attempted: list[dict[str, Any]]
    residual_fragmentation: float
    essentiality: float
    protected_losses: list[str]
    downstream_targets: list[str]
    human_review_required: bool
    schema_version: str = SCHEMA_VERSION
    lifecycle: str = Lifecycle.STAGED.value
    provenance: Provenance = field(default_factory=Provenance)


@dataclass(slots=True)
class ReflectionRecord:
    reflection_id: str
    site_id: str
    lens_outputs: dict[str, dict[str, Any]]
    convergence: list[str]
    contradictions: list[str]
    redescriptions: list[dict[str, Any]]
    preserved_commitments: list[str]
    anticipated_losses: list[str]
    counterworlds: list[str]
    formal_obligations: list[str]
    concrete_obligations: list[str]
    source_refs: list[dict[str, Any]]
    schema_version: str = SCHEMA_VERSION
    lifecycle: str = Lifecycle.STAGED.value
    provenance: Provenance = field(default_factory=Provenance)


@dataclass(slots=True)
class HypothesisPackage:
    candidate_id: str
    mode: str
    title: str
    pressure_ids: list[str]
    reflection_ids: list[str]
    formal_move: str
    atlas_patch: dict[str, Any]
    assumptions: list[str]
    consequences: list[str]
    falsifiers: list[str]
    return_paths: list[dict[str, Any]]
    relevance_vector: dict[str, float]
    validation_tasks: list[dict[str, Any]]
    uncertainty: dict[str, float]
    novelty_status: str = "conjectural"
    schema_version: str = SCHEMA_VERSION
    lifecycle: str = Lifecycle.STAGED.value
    provenance: Provenance = field(default_factory=Provenance)


@dataclass(slots=True)
class ValidationOutcome:
    validation_id: str
    candidate_id: str
    validator_role: str
    check_type: str
    status: str
    findings: list[str]
    obligations_remaining: list[str]
    evidence_artifacts: list[str]
    falsifying_conditions: list[str]
    realized_value: dict[str, float]
    schema_version: str = SCHEMA_VERSION
    lifecycle: str = Lifecycle.STAGED.value
    provenance: Provenance = field(default_factory=Provenance)


@dataclass(slots=True)
class SkillResult:
    status: str
    artifacts: list[dict[str, Any]] = field(default_factory=list)
    claims: list[dict[str, Any]] = field(default_factory=list)
    uncertainties: list[dict[str, Any]] = field(default_factory=list)
    next: list[dict[str, Any]] = field(default_factory=list)
    provenance: dict[str, Any] = field(default_factory=dict)
    messages: list[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        allowed = {item.value for item in ResultStatus}
        if self.status not in allowed:
            raise ValueError(f"invalid SkillResult status: {self.status}")

    def to_dict(self) -> dict[str, Any]:
        return jsonable(self)


@dataclass(slots=True)
class RunState:
    run_id: str
    context_id: str
    phase: str = RunPhase.NEW.value
    revision: int = 0
    artifact_ids: list[str] = field(default_factory=list)
    history: list[dict[str, Any]] = field(default_factory=list)
    failures: list[dict[str, Any]] = field(default_factory=list)
    budget_remaining: dict[str, float] = field(default_factory=dict)
    awaiting_human_review: bool = False
    terminal_reason: str | None = None


def require_fields(payload: Mapping[str, Any], fields: Iterable[str]) -> list[str]:
    return [name for name in fields if name not in payload or payload[name] in (None, "", [])]


def bounded(value: Any, default: float = 0.0) -> float:
    try:
        return max(0.0, min(1.0, float(value)))
    except (TypeError, ValueError):
        return default


def result(
    status: ResultStatus | str,
    *,
    artifacts: Iterable[Any] = (),
    claims: Iterable[dict[str, Any]] = (),
    uncertainties: Iterable[dict[str, Any]] = (),
    next_actions: Iterable[dict[str, Any]] = (),
    messages: Iterable[str] = (),
    skill: str = "",
    inputs: Any = None,
    seed: int = 0,
) -> SkillResult:
    status_value = status.value if isinstance(status, ResultStatus) else status
    prompt_hash = hashlib.sha256(canonical_json(inputs or {}).encode()).hexdigest()
    return SkillResult(
        status=status_value,
        artifacts=[jsonable(item) for item in artifacts],
        claims=list(claims),
        uncertainties=list(uncertainties),
        next=list(next_actions),
        provenance=jsonable(
            Provenance(
                skill_version="0.1.0",
                model_id="deterministic-local",
                prompt_hash=prompt_hash,
                seed=seed,
                parameters={"skill": skill},
            )
        ),
        messages=list(messages),
    )

