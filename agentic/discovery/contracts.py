# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
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
import copy
import functools
import hashlib
import json
import math
import os
import re
import stat
import threading
from collections import OrderedDict
from pathlib import Path
from typing import Any, Mapping, Sequence
from urllib.parse import unquote, urljoin, urlsplit

from jsonschema import Draft202012Validator, FormatChecker
from referencing import Registry, Resource
from referencing.exceptions import NoSuchResource
from referencing.jsonschema import DRAFT202012


ROOT = Path(__file__).resolve().parents[2]
SCHEMA_ROOT = ROOT / "agentic" / "spec"
_IDENTIFIER = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,127}$")
_DIGEST = re.compile(r"^sha256:[0-9a-f]{64}$")


class ContractError(ValueError):
    """Raised when typed discovery data violates an integrity invariant."""


@dataclasses.dataclass(frozen=True, slots=True)
class SchemaValidationIssue:
    """One machine-addressable instance failure from a JSON Schema validator."""

    location: str
    message: str


class SchemaValidationError(ContractError):
    """Carry stable instance locations without making callers parse prose."""

    def __init__(
        self,
        schema_name: str | Path,
        issues: Sequence[SchemaValidationIssue],
    ) -> None:
        if not issues:
            raise ValueError("schema validation error requires at least one issue")
        self.schema_name = str(schema_name)
        self.issues = tuple(issues)
        self.locations = tuple(issue.location for issue in self.issues)
        rendered = "; ".join(
            f"{issue.location}: {issue.message}" for issue in self.issues
        )
        super().__init__("schema validation failed: " + rendered)


class LocalSchemaResolutionError(ValueError):
    """Typed failure to resolve a JSON-Schema document inside local authority."""

    def __init__(self, reason_code: str, message: str) -> None:
        self.reason_code = reason_code
        super().__init__(f"local_schema[{reason_code}]: {message}")


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


def _schema_path(name_or_path: str | Path) -> Path:
    path = Path(name_or_path)
    if not path.is_absolute():
        path = SCHEMA_ROOT / path
    return path


def _schema_boundary(path: Path) -> Path:
    """Choose the exact local authority root for one runtime schema."""

    repository_schema_root = SCHEMA_ROOT.resolve(strict=True)
    candidate = path.absolute()
    try:
        candidate.resolve(strict=False).relative_to(repository_schema_root)
    except ValueError:
        return candidate.parent.resolve(strict=True)
    return repository_schema_root


def _safe_local_schema_file(path: Path, boundary_root: Path) -> Path:
    """Resolve a regular schema file without accepting an in-boundary link.

    macOS exposes ``/var`` through the system-owned ``/private/var`` alias.
    Finding the raw prefix that resolves to the authority root accepts that
    spelling while retaining every component below the root for an explicit
    no-follow check.  A link inside the authority is therefore never erased by
    an eager whole-path ``resolve()``.
    """

    boundary = boundary_root.resolve(strict=True)
    raw = path if path.is_absolute() else boundary / path
    normalized = Path(os.path.abspath(raw))
    parts = normalized.parts
    relative: Path | None = None
    for length in range(len(parts), 0, -1):
        prefix = Path(*parts[:length])
        try:
            if prefix.resolve(strict=True) == boundary:
                relative = Path(*parts[length:])
                break
        except OSError:
            continue
    if relative is None:
        raise LocalSchemaResolutionError(
            "path_escape", f"schema path escapes {boundary}: {path}"
        )
    cursor = boundary
    for index, part in enumerate(relative.parts):
        cursor = cursor / part
        try:
            row = os.stat(cursor, follow_symlinks=False)
        except FileNotFoundError as exc:
            raise LocalSchemaResolutionError(
                "missing", f"schema is missing: {path}"
            ) from exc
        except OSError as exc:
            raise LocalSchemaResolutionError(
                "unavailable", f"schema path is unavailable: {path}"
            ) from exc
        if stat.S_ISLNK(row.st_mode):
            raise LocalSchemaResolutionError(
                "symlink", f"schema path traverses a symlink: {path}"
            )
        if index < len(relative.parts) - 1 and not stat.S_ISDIR(row.st_mode):
            raise LocalSchemaResolutionError(
                "invalid_parent", f"schema parent is not a directory: {path}"
            )
    candidate = boundary / relative
    if not relative.parts:
        row = os.stat(candidate, follow_symlinks=False)
    if not stat.S_ISREG(row.st_mode):
        raise LocalSchemaResolutionError(
            "special_file", f"schema must be a regular file: {path}"
        )
    return candidate


def _read_local_schema_bytes(path: Path, boundary_root: Path) -> tuple[Path, bytes]:
    """Read one exact schema object through a no-follow descriptor."""

    safe = _safe_local_schema_file(path, boundary_root)
    before = os.stat(safe, follow_symlinks=False)
    flags = os.O_RDONLY
    if hasattr(os, "O_NOFOLLOW"):
        flags |= os.O_NOFOLLOW
    try:
        descriptor = os.open(safe, flags)
    except OSError as exc:
        raise LocalSchemaResolutionError(
            "concurrent_change", f"schema changed or became linked: {path}"
        ) from exc
    try:
        opened = os.fstat(descriptor)

        def identity(value: os.stat_result) -> tuple[int, ...]:
            return (
                value.st_dev,
                value.st_ino,
                stat.S_IFMT(value.st_mode),
                value.st_size,
                value.st_mtime_ns,
                value.st_ctime_ns,
            )

        if identity(before) != identity(opened):
            raise LocalSchemaResolutionError(
                "concurrent_change", f"schema changed while opening: {path}"
            )
        chunks: list[bytes] = []
        while chunk := os.read(descriptor, 1024 * 1024):
            chunks.append(chunk)
        after = os.fstat(descriptor)
        named_after = os.stat(safe, follow_symlinks=False)
        if identity(opened) != identity(after) or identity(after) != identity(named_after):
            raise LocalSchemaResolutionError(
                "concurrent_change", f"schema changed while reading: {path}"
            )
        return safe, b"".join(chunks)
    finally:
        os.close(descriptor)


def resolve_local_schema_reference(
    reference: str,
    *,
    source_path: Path,
    boundary_root: Path,
    schema_root: Path | None = None,
) -> Path | None:
    """Resolve a fragment, document-relative path, or absolute local reference.

    Network references and basename fallbacks are intentionally absent.  The
    only URI authority mapped to repository bytes is the exact
    ``https://abducer.local/spec|schemas/...`` namespace; ``file:`` and raw
    absolute paths must remain inside ``boundary_root``.
    """

    if not isinstance(reference, str) or not reference:
        raise LocalSchemaResolutionError("invalid_reference", "schema reference is empty")
    document = reference.split("#", 1)[0]
    if not document:
        return None
    if "\\" in document:
        raise LocalSchemaResolutionError(
            "invalid_reference", f"schema reference contains a backslash: {reference}"
        )
    parsed = urlsplit(document)
    if parsed.query:
        raise LocalSchemaResolutionError(
            "invalid_reference", f"schema reference contains a query: {reference}"
        )
    decoded_path = unquote(parsed.path)
    if "\x00" in decoded_path:
        raise LocalSchemaResolutionError(
            "invalid_reference", f"schema reference contains NUL: {reference}"
        )
    if parsed.scheme in {"http", "https"}:
        if parsed.scheme != "https" or parsed.netloc != "abducer.local":
            raise LocalSchemaResolutionError(
                "remote_reference", f"remote schema reference is forbidden: {reference}"
            )
        local_root = (schema_root or SCHEMA_ROOT).resolve(strict=True)
        prefixes = ("/spec/", "/schemas/")
        prefix = next((item for item in prefixes if decoded_path.startswith(item)), None)
        if prefix is None:
            raise LocalSchemaResolutionError(
                "invalid_local_id", f"unknown absolute local schema ID: {reference}"
            )
        suffix = decoded_path[len(prefix) :]
        if not suffix:
            raise LocalSchemaResolutionError(
                "invalid_local_id", f"absolute local schema ID has no document: {reference}"
            )
        candidate = local_root / suffix
    elif parsed.scheme == "file":
        if parsed.netloc not in {"", "localhost"}:
            raise LocalSchemaResolutionError(
                "remote_reference", f"non-local file URI is forbidden: {reference}"
            )
        candidate = Path(decoded_path)
    elif parsed.scheme or parsed.netloc:
        raise LocalSchemaResolutionError(
            "remote_reference", f"non-local schema reference is forbidden: {reference}"
        )
    elif Path(decoded_path).is_absolute():
        candidate = Path(decoded_path)
    else:
        candidate = source_path.parent / decoded_path
    return _safe_local_schema_file(candidate, boundary_root)


def schema_document_references(value: Any) -> tuple[str, ...]:
    """Return every distinct external-document ``$ref`` in stable order."""

    references: set[str] = set()

    def walk(item: Any) -> None:
        if isinstance(item, Mapping):
            for key, child in item.items():
                if key == "$ref" and isinstance(child, str) and child.split("#", 1)[0]:
                    references.add(child)
                else:
                    walk(child)
        elif isinstance(item, list):
            for child in item:
                walk(child)

    walk(value)
    return tuple(sorted(references))


def schema_resource_ids(value: Any, base_uri: str) -> tuple[str, ...]:
    """Collect effective schema IDs, including nested resource identifiers."""

    identifiers: list[str] = []

    def walk(item: Any, inherited: str) -> None:
        if isinstance(item, Mapping):
            current = inherited
            raw_id = item.get("$id")
            if raw_id is not None:
                if not isinstance(raw_id, str) or not raw_id:
                    raise LocalSchemaResolutionError(
                        "invalid_id", "JSON-Schema $id must be a non-empty string"
                    )
                current = urljoin(inherited, raw_id)
                parsed = urlsplit(current)
                if parsed.fragment:
                    raise LocalSchemaResolutionError(
                        "invalid_id", f"JSON-Schema $id must identify a document: {raw_id}"
                    )
                identifiers.append(current)
            for child in item.values():
                walk(child, current)
        elif isinstance(item, list):
            for child in item:
                walk(child, inherited)

    walk(value, base_uri)
    return tuple(identifiers)


def _schema_reference_bindings(
    value: Any, base_uri: str
) -> tuple[tuple[str, str], ...]:
    """Bind each external reference to its effective (possibly nested) base."""

    bindings: list[tuple[str, str]] = []

    def walk(item: Any, inherited: str) -> None:
        if isinstance(item, Mapping):
            current = inherited
            raw_id = item.get("$id")
            if isinstance(raw_id, str) and raw_id:
                current = urljoin(inherited, raw_id)
            reference = item.get("$ref")
            if isinstance(reference, str) and reference.split("#", 1)[0]:
                bindings.append(
                    (reference, urljoin(current, reference.split("#", 1)[0]))
                )
            for key, child in item.items():
                if key not in {"$id", "$ref"}:
                    walk(child, current)
        elif isinstance(item, list):
            for child in item:
                walk(child, inherited)

    walk(value, base_uri)
    return tuple(bindings)


@functools.lru_cache(maxsize=512)
def _meta_validated_schema_bytes(encoded: bytes) -> dict[str, Any]:
    """Parse and meta-validate exact bytes once; changed bytes are a new key."""

    try:
        schema = json.loads(encoded.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ContractError(f"cannot parse JSON Schema bytes: {exc}") from exc
    if not isinstance(schema, dict):
        raise ContractError("schema must be a JSON object")
    try:
        Draft202012Validator.check_schema(schema)
    except Exception as exc:  # jsonschema exposes several schema error subclasses.
        raise ContractError(f"invalid JSON Schema: {exc}") from exc
    return schema


def load_schema(name_or_path: str | Path) -> dict[str, Any]:
    """Load and meta-validate exact schema bytes with mutation-safe caching."""

    path = _schema_path(name_or_path)
    boundary = _schema_boundary(path)
    try:
        _, encoded = _read_local_schema_bytes(path, boundary)
        return copy.deepcopy(_meta_validated_schema_bytes(encoded))
    except LocalSchemaResolutionError as exc:
        raise ContractError(f"cannot load JSON Schema {path}: {exc}") from exc
    except OSError as exc:
        raise ContractError(f"cannot load JSON Schema {path}: {exc}") from exc


def validate_schema_file(name_or_path: str | Path) -> dict[str, Any]:
    """Meta-validate and return a schema (public compatibility entrypoint)."""

    return load_schema(name_or_path)


def _local_schema_registry(root_path: Path) -> Registry[Any]:
    """Build an exact closed registry with duplicate-ID and alias detection."""

    boundary = _schema_boundary(root_path)
    schema_root = SCHEMA_ROOT.resolve(strict=True)
    queue = [_safe_local_schema_file(root_path, boundary)]
    documents: dict[Path, dict[str, Any]] = {}
    aliases: dict[str, Path] = {}
    identifiers: dict[str, Path] = {}

    def bind(alias: str, path: Path, *, identifier: bool = False) -> None:
        prior = (identifiers if identifier else aliases).get(alias)
        if prior is not None and prior != path:
            raise LocalSchemaResolutionError(
                "duplicate_id" if identifier else "duplicate_alias",
                f"schema URI {alias!r} names both {prior} and {path}",
            )
        (identifiers if identifier else aliases)[alias] = path
        alias_prior = aliases.get(alias)
        if alias_prior is not None and alias_prior != path:
            raise LocalSchemaResolutionError(
                "duplicate_alias", f"schema URI {alias!r} is ambiguous"
            )
        aliases[alias] = path

    while queue:
        path = queue.pop()
        if path in documents:
            continue
        schema = load_schema(path)
        documents[path] = schema
        file_uri = path.as_uri()
        bind(file_uri, path)
        try:
            relative = path.relative_to(schema_root).as_posix()
        except ValueError:
            pass
        else:
            bind(f"https://abducer.local/spec/{relative}", path)
            bind(f"https://abducer.local/schemas/{relative}", path)
        ids = schema_resource_ids(schema, file_uri)
        for identifier in ids:
            if identifier in identifiers:
                raise LocalSchemaResolutionError(
                    "duplicate_id",
                    f"schema ID {identifier!r} occurs more than once in the closure",
                )
            bind(identifier, path, identifier=True)
        root_id = schema.get("$id")
        base_uri = (
            urljoin(file_uri, root_id)
            if isinstance(root_id, str) and root_id
            else file_uri
        )
        for reference, reference_uri in _schema_reference_bindings(schema, base_uri):
            target = resolve_local_schema_reference(
                reference,
                source_path=path,
                boundary_root=boundary,
                schema_root=schema_root,
            )
            if target is None:
                continue
            bind(reference_uri, target)
            if target not in documents:
                queue.append(target)

    def unavailable(uri: str) -> Resource[Any]:
        raise NoSuchResource(ref=uri)

    registry: Registry[Any] = Registry(retrieve=unavailable)
    for alias, path in sorted(aliases.items()):
        resource = Resource.from_contents(
            documents[path], default_specification=DRAFT202012
        )
        registry = registry.with_resource(alias, resource)
    return registry.crawl()


_JSON_STRUCTURE_CACHE: OrderedDict[tuple[str, str, str], None] = OrderedDict()
_JSON_STRUCTURE_CACHE_LOCK = threading.Lock()


def _plain_json(value: Any) -> bool:
    if type(value) is dict:
        return all(type(key) is str and _plain_json(child) for key, child in value.items())
    if type(value) is list:
        return all(_plain_json(child) for child in value)
    return value is None or type(value) in {str, int, float, bool}


def validate_instance(
    instance: Any, schema_name: str | Path, *, cache_json_structure: bool = False
) -> None:
    """Validate an instance and report every error in stable path order."""

    try:
        schema_path = _safe_local_schema_file(
            _schema_path(schema_name), _schema_boundary(_schema_path(schema_name))
        )
        schema = load_schema(schema_path)
        validation_schema = copy.deepcopy(schema)
        if "$id" not in validation_schema:
            validation_schema["$id"] = schema_path.as_uri()
        registry = _local_schema_registry(schema_path)
        cache_key = None
        if cache_json_structure and _plain_json(instance):
            # Reopen the entire local schema closure on every call. Only a
            # successful structural check of identical JSON under identical
            # schemas is reusable; receipt files and live authority still replay.
            cache_key = (
                schema_path.as_uri(),
                canonical_digest({uri: resource.contents for uri, resource in registry.items()}),
                canonical_digest(instance),
            )
            with _JSON_STRUCTURE_CACHE_LOCK:
                if cache_key in _JSON_STRUCTURE_CACHE:
                    _JSON_STRUCTURE_CACHE.move_to_end(cache_key)
                    return
        validator = Draft202012Validator(
            validation_schema,
            format_checker=FormatChecker(),
            registry=registry,
        )
        errors = sorted(
            validator.iter_errors(instance),
            key=lambda error: list(error.absolute_path),
        )
    except Exception as exc:
        raise ContractError(
            f"schema reference resolution failed for {schema_name}: {exc}"
        ) from exc
    if errors:
        issues = tuple(
            SchemaValidationIssue(
                location="$"
                + "".join(
                    f"[{part}]" if isinstance(part, int) else f".{part}"
                    for part in error.absolute_path
                ),
                message=error.message,
            )
            for error in errors
        )
        raise SchemaValidationError(schema_name, issues)
    if cache_key is not None:
        with _JSON_STRUCTURE_CACHE_LOCK:
            _JSON_STRUCTURE_CACHE[cache_key] = None
            while len(_JSON_STRUCTURE_CACHE) > 256:
                _JSON_STRUCTURE_CACHE.popitem(last=False)


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
