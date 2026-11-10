"""Canonical data and identity contracts shared by discovery subsystems.

Receipts are useful only when all producers agree on bytes, identities, and schema
semantics.  This module therefore owns canonical JSON SHA-256 digests, strict
target/run/branch/state namespaces, safe workspace paths, and Draft 2020-12 JSON
Schema validation.  It contains no discovery policy: callers use these primitives
to prove that an artifact is the exact one produced in the claimed execution.
"""

from __future__ import annotations

import dataclasses
import datetime as dt
import hashlib
import json
import math
import os
import re
from pathlib import Path
from typing import Any, Mapping, Sequence

from jsonschema import Draft202012Validator, FormatChecker


ROOT = Path(__file__).resolve().parents[2]
SCHEMA_ROOT = ROOT / "agentic" / "spec"
_IDENTIFIER = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,127}$")
_DIGEST = re.compile(r"^sha256:[0-9a-f]{64}$")


class ContractError(ValueError):
    """Raised when typed discovery data violates an integrity invariant."""


def utc_now() -> str:
    """Return a timezone-explicit, second-resolution UTC timestamp."""

    return dt.datetime.now(dt.UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _reject_non_finite(value: Any, path: str = "$") -> None:
    """Reject NaN and infinities before JSON encoding.

    Python's default JSON encoder accepts these non-standard values.  Allowing
    them would make hashes language-dependent, so canonical payloads reject them.
    """

    if isinstance(value, float) and not math.isfinite(value):
        raise ContractError(f"non-finite number at {path}")
    if isinstance(value, Mapping):
        for key, child in value.items():
            if not isinstance(key, str):
                raise ContractError(f"non-string object key at {path}")
            _reject_non_finite(child, f"{path}.{key}")
    elif isinstance(value, (list, tuple)):
        for index, child in enumerate(value):
            _reject_non_finite(child, f"{path}[{index}]")


def canonical_json(value: Any) -> bytes:
    """Encode JSON to the stable UTF-8 representation used by every digest."""

    _reject_non_finite(value)
    try:
        text = json.dumps(
            value,
            ensure_ascii=False,
            allow_nan=False,
            sort_keys=True,
            separators=(",", ":"),
        )
    except (TypeError, ValueError) as exc:
        raise ContractError(f"payload is not canonical-JSON encodable: {exc}") from exc
    return text.encode("utf-8")


def canonical_digest(value: Any, *, exclude_keys: Sequence[str] = ()) -> str:
    """Return a tagged SHA-256 digest, optionally omitting named mapping keys.

    ``exclude_keys`` is applied recursively.  It is intended for self-hashed
    records such as ledger events where ``event_hash`` must be excluded at every
    nesting level by one shared, explicit rule.
    """

    excluded = frozenset(exclude_keys)

    def filtered(item: Any) -> Any:
        if isinstance(item, Mapping):
            return {key: filtered(child) for key, child in item.items() if key not in excluded}
        if isinstance(item, (list, tuple)):
            return [filtered(child) for child in item]
        return item

    return "sha256:" + hashlib.sha256(canonical_json(filtered(value))).hexdigest()


def stable_identifier(prefix: str, *parts: Any) -> str:
    """Build a readable, content-addressed identifier from canonical parts."""

    validate_identifier(prefix, "identifier prefix")
    digest = canonical_digest(list(parts)).removeprefix("sha256:")[:24]
    return f"{prefix}.{digest}"


def bytes_digest(data: bytes) -> str:
    """Return a tagged SHA-256 digest of exact artifact bytes."""

    return "sha256:" + hashlib.sha256(data).hexdigest()


def file_digest(path: Path) -> str:
    """Hash a file without loading an arbitrarily large artifact into memory."""

    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return "sha256:" + digest.hexdigest()


def validate_digest(value: str) -> None:
    """Reject malformed or non-SHA-256 digest strings."""

    if not isinstance(value, str) or not _DIGEST.fullmatch(value):
        raise ContractError(f"invalid canonical digest: {value!r}")


def validate_identifier(value: str, field: str) -> str:
    """Validate a namespace identifier and exclude mutable-pointer aliases."""

    if not isinstance(value, str) or not _IDENTIFIER.fullmatch(value):
        raise ContractError(f"invalid {field}: {value!r}")
    if value.lower() in {"latest", "current", "global", ".", ".."}:
        raise ContractError(f"mutable/global alias is forbidden for {field}: {value!r}")
    return value


@dataclasses.dataclass(frozen=True, slots=True)
class Namespace:
    """Identity binding carried by requests, receipts, artifacts, and events."""

    target_id: str
    run_id: str
    branch_id: str
    state_version: int

    def __post_init__(self) -> None:
        validate_identifier(self.target_id, "target_id")
        validate_identifier(self.run_id, "run_id")
        validate_identifier(self.branch_id, "branch_id")
        if isinstance(self.state_version, bool) or not isinstance(self.state_version, int) or self.state_version < 0:
            raise ContractError("state_version must be a non-negative integer")

    @classmethod
    def from_mapping(cls, payload: Mapping[str, Any]) -> "Namespace":
        """Construct a namespace from a strict mapping."""

        required = {"target_id", "run_id", "branch_id", "state_version"}
        missing = required - payload.keys()
        if missing:
            raise ContractError(f"namespace missing fields: {sorted(missing)}")
        return cls(**{field: payload[field] for field in required})

    def as_dict(self) -> dict[str, Any]:
        """Return the schema-shaped namespace representation."""

        return dataclasses.asdict(self)

    def assert_matches(self, other: "Namespace", *, context: str = "artifact") -> None:
        """Require exact namespace equality, including frozen state generation."""

        if self != other:
            raise ContractError(
                f"{context} namespace mismatch: expected {self.as_dict()}, got {other.as_dict()}"
            )


def safe_relative_path(
    raw: str, root: Path | str | None = None, *, forbid_latest: bool = True
) -> Path:
    """Parse a safe path; with ``root``, resolve it inside that directory."""

    if not isinstance(raw, str) or not raw.strip():
        raise ContractError("artifact path must be a non-empty string")
    path = Path(raw)
    if path.is_absolute() or any(part in {"", ".", ".."} for part in path.parts):
        raise ContractError(f"unsafe artifact path: {raw!r}")
    if forbid_latest and any(part.lower() in {"latest", "latest.json", "current"} for part in path.parts):
        raise ContractError(f"mutable latest/current path is forbidden: {raw!r}")
    if root is None:
        return path
    resolved_root = Path(root).resolve()
    resolved = (resolved_root / path).resolve()
    try:
        resolved.relative_to(resolved_root)
    except ValueError as exc:
        raise ContractError(f"artifact escapes root: {raw!r}") from exc
    return resolved


def resolve_workspace_path(workspace: Path, raw: str, *, must_exist: bool = False) -> Path:
    """Resolve a safe relative path and prove it remains inside ``workspace``."""

    relative = safe_relative_path(raw)
    root = workspace.resolve()
    path = (root / relative).resolve()
    try:
        path.relative_to(root)
    except ValueError as exc:
        raise ContractError(f"artifact escapes workspace: {raw!r}") from exc
    if must_exist and (not path.exists() or not path.is_file()):
        raise ContractError(f"artifact does not exist: {raw!r}")
    return path


def load_json(path: Path) -> Any:
    """Read JSON with a contract-focused error rather than an opaque traceback."""

    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ContractError(f"cannot load JSON {path}: {exc}") from exc


def load_schema(name_or_path: str | Path) -> dict[str, Any]:
    """Load and meta-validate one repository JSON Schema."""

    path = Path(name_or_path)
    if not path.is_absolute():
        path = SCHEMA_ROOT / path
    schema = load_json(path)
    if not isinstance(schema, dict):
        raise ContractError(f"schema must be an object: {path}")
    try:
        Draft202012Validator.check_schema(schema)
    except Exception as exc:  # jsonschema exposes several schema error subclasses.
        raise ContractError(f"invalid JSON Schema {path}: {exc}") from exc
    return schema


def validate_schema_file(name_or_path: str | Path) -> dict[str, Any]:
    """Meta-validate and return a schema (public compatibility entrypoint)."""

    return load_schema(name_or_path)


def validate_instance(instance: Any, schema_name: str | Path) -> None:
    """Validate an instance and report every error in stable path order."""

    schema = load_schema(schema_name)
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    errors = sorted(validator.iter_errors(instance), key=lambda error: list(error.absolute_path))
    if errors:
        rendered = []
        for error in errors:
            location = "$" + "".join(
                f"[{part}]" if isinstance(part, int) else f".{part}" for part in error.absolute_path
            )
            rendered.append(f"{location}: {error.message}")
        raise ContractError("schema validation failed: " + "; ".join(rendered))


def validate_payload(instance: Any, schema_name: str | Path) -> None:
    """Validate typed payload data (public compatibility entrypoint)."""

    validate_instance(instance, schema_name)


def artifact_descriptor(path: Path, workspace: Path, namespace: Namespace) -> dict[str, Any]:
    """Describe an existing immutable artifact with bytes digest and namespace."""

    resolved = path.resolve()
    try:
        relative = resolved.relative_to(workspace.resolve())
    except ValueError as exc:
        raise ContractError(f"artifact is outside workspace: {path}") from exc
    safe_relative_path(relative.as_posix())
    if not resolved.is_file():
        raise ContractError(f"artifact is not a file: {path}")
    return {
        "path": relative.as_posix(),
        "sha256": file_digest(resolved),
        "size_bytes": resolved.stat().st_size,
        "namespace": namespace.as_dict(),
    }


def verify_artifact_descriptor(
    descriptor: Mapping[str, Any], workspace: Path, expected_namespace: Namespace
) -> Path:
    """Verify path, namespace, size, and exact bytes declared by an artifact."""

    namespace = Namespace.from_mapping(descriptor.get("namespace", {}))
    expected_namespace.assert_matches(namespace)
    path = resolve_workspace_path(workspace, descriptor.get("path", ""), must_exist=True)
    claimed = descriptor.get("sha256")
    validate_digest(claimed)
    actual = file_digest(path)
    if actual != claimed:
        raise ContractError(f"artifact digest mismatch for {descriptor.get('path')}: {claimed} != {actual}")
    if descriptor.get("size_bytes") != path.stat().st_size:
        raise ContractError(f"artifact size mismatch for {descriptor.get('path')}")
    return path


def fsync_directory(path: Path) -> None:
    """Persist directory-entry updates required by crash-safe rename protocols."""

    descriptor = os.open(path, os.O_RDONLY)
    try:
        os.fsync(descriptor)
    finally:
        os.close(descriptor)


def semantic_token_set(value: Any) -> set[str]:
    """Extract normalized content tokens for deterministic diversity checks."""

    if isinstance(value, Mapping):
        text = " ".join(str(child) for key, child in sorted(value.items()) if key not in {"id", "timestamp"})
    elif isinstance(value, Sequence) and not isinstance(value, (str, bytes, bytearray)):
        text = " ".join(map(str, value))
    else:
        text = str(value)
    return set(re.findall(r"[a-z0-9]+", text.lower()))


def jaccard_similarity(left: Any, right: Any) -> float:
    """Compute deterministic lexical overlap used only as a conservative guard."""

    lhs, rhs = semantic_token_set(left), semantic_token_set(right)
    if not lhs and not rhs:
        return 1.0
    return len(lhs & rhs) / max(1, len(lhs | rhs))


def adjudicate_quality_case(case: Mapping[str, Any]) -> dict[str, Any]:
    """Evaluate one blinded adversarial discovery-quality case deterministically.

    The evaluator receives only ``case_payload``; expected judgments live in a
    separate fixture field.  These guards are intentionally necessary rather
    than sufficient for discovery quality: they reject known category errors
    without pretending to score philosophical depth as a single scalar.
    """

    case_id = validate_identifier(case.get("case_id"), "case_id")
    category = case.get("category")
    payload = case.get("case_payload")
    if not isinstance(category, str) or not isinstance(payload, Mapping):
        raise ContractError("quality case requires category and blinded case_payload")
    reasons: list[str] = []
    decision = "accept"

    if category in {"philosophical_vapour", "shallow_cycle"}:
        if payload.get("claimed_learning") and not payload.get("semantic_mutations"):
            decision, reasons = "reject", ["no_semantic_mutation"]
    elif category == "unification_by_erasure":
        if len(payload.get("component_concepts", [])) >= 2 and not payload.get("preserved_differences"):
            decision, reasons = "reject", ["differences_erased"]
    elif category in {"relevance_drift", "wrong_target_global_latest"}:
        if payload.get("requested_target_id") != payload.get("artifact_target_id"):
            decision, reasons = "reject", ["target_identity_mismatch"]
        elif payload.get("goal_contribution") is False:
            decision, reasons = "reject", ["no_target_contribution"]
    elif category == "premature_convergence":
        if payload.get("decision") == "complete" and payload.get("unresolved_critical_obligations", 0) > 0:
            decision, reasons = "reject", ["critical_obligations_unresolved"]
    elif category in {"false_breakthrough", "fabricated_certificate"}:
        claimed = payload.get("claimed_digest")
        actual = payload.get("actual_digest")
        if claimed is not None and claimed != actual:
            decision, reasons = "reject", ["certificate_digest_mismatch"]
        elif payload.get("truth_status") == "established" and (
            payload.get("evidence_status") != "validated" or not payload.get("validator_receipt_ids")
        ):
            decision, reasons = "reject", ["established_without_validation"]
    elif category == "proxy_drift":
        if payload.get("same_theory") is not True:
            decision, reasons = "reject", ["proxy_not_source_theory"]
    elif category == "stale_evidence":
        if str(payload.get("snapshot_cutoff", "")) < str(payload.get("required_cutoff", "")):
            decision, reasons = "reject", ["literature_snapshot_stale"]
    elif category in {"structurally_duplicate_branches", "correlated_parallel_branches"}:
        branches = payload.get("branches", [])
        signatures = [branch.get("structural_signature") for branch in branches if isinstance(branch, Mapping)]
        duplicate_signature = len(signatures) != len(set(signatures))
        dependency_clusters = [
            branch.get("dependency_cluster")
            for branch in branches
            if isinstance(branch, Mapping) and branch.get("dependency_cluster") is not None
        ]
        correlated_seed = len(dependency_clusters) != len(set(dependency_clusters))
        excessive_overlap = any(
            jaccard_similarity(branches[i], branches[j]) >= 0.85
            for i in range(len(branches))
            for j in range(i + 1, len(branches))
        )
        if duplicate_signature or correlated_seed or excessive_overlap:
            decision, reasons = "reject", ["parallel_branches_not_structurally_diverse"]
    elif category == "literature_supersession":
        if (
            str(payload.get("new_coverage_cutoff", "")) > str(payload.get("frozen_coverage_cutoff", ""))
            and payload.get("affected_branch_ids")
        ):
            decision, reasons = "rebase", ["newer_literature_affects_branch"]
    elif category == "partial_worker_failure":
        statuses = [worker.get("status") for worker in payload.get("workers", []) if isinstance(worker, Mapping)]
        if "validated" in statuses and any(status in {"failed", "timed_out"} for status in statuses):
            decision, reasons = "retain_valid_siblings", ["partial_failure_is_branch_local"]
    elif category == "paraphrase_loop":
        digests = payload.get("semantic_digests", [])
        if len(digests) >= 3 and len(set(digests)) == 1:
            decision, reasons = "reject", ["semantic_plateau"]
    elif category == "pseudo_radical_hypothesis":
        if payload.get("risk_label") == "radical" and not (
            payload.get("premise_inversion") or payload.get("new_primitive") or payload.get("forbidden_conjunction")
        ):
            decision, reasons = "reject", ["risk_rhetoric_without_conceptual_discontinuity"]
    else:
        raise ContractError(f"unsupported quality-case category: {category}")

    receipt_core = {
        "schema_version": "1.0.0",
        "rubric_version": "discovery-quality-1.0.0",
        "case_id": case_id,
        "category": category,
        "case_digest": canonical_digest(payload),
        "decision": decision,
        "reason_codes": sorted(reasons),
    }
    return {
        **receipt_core,
        "adjudication_receipt_id": stable_identifier("quality", receipt_core),
        "adjudication_digest": canonical_digest(receipt_core),
    }
