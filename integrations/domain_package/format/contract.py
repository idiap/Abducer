# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
"""Domain package v1 validation. No imports or execution of package code.

This module and its schemas are pinned by exporters. The platform owns the
canonical copy; validation requires neither a server nor a source checkout.
"""
from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path, PurePosixPath
import re
import unicodedata
from urllib.parse import urlsplit
from typing import Any, Mapping

from jsonschema import Draft202012Validator
from packaging.specifiers import InvalidSpecifier, SpecifierSet
from packaging.version import Version

COLLECTIONS = ("repository", "reports", "skills", "data-sources")
SCHEMA_ROOT = Path(__file__).parent


class PackageValidationError(ValueError):
    """An archive or resource violates the portable format."""


def schema(name: str) -> dict[str, Any]:
    """Load one pinned schema by its allow-listed contract name."""
    if name not in {"manifest", *COLLECTIONS, "worker-request", "worker-result"}:
        raise PackageValidationError("unknown schema")
    return json.loads((SCHEMA_ROOT / f"{name}-v1.schema.json").read_text())


def validate_document(value: Any, kind: str) -> None:
    """Reject a resource whose structure violates its collection schema."""
    errors = sorted(Draft202012Validator(schema(kind)).iter_errors(value), key=lambda e: str(e.path))
    if errors:
        error = errors[0]
        raise PackageValidationError(f"{kind} at {list(error.path)}: {error.message}")


def archive_path(value: str) -> str:
    """Require one canonical, portable, archive-relative regular-file path."""
    if not isinstance(value, str) or not value or unicodedata.normalize("NFC", value) != value:
        raise PackageValidationError("noncanonical archive path")
    parts = value.split("/")
    if (parts[0] not in COLLECTIONS or len(parts) < 2
            or any(p in {"", ".", ".."} for p in parts)
            or any(unicodedata.category(c) == "Cc" for c in value)
            or any(c in '\\:<>"|?*' for c in value)
            or any(len(p.encode("utf-8")) > 255 for p in parts)
            or any(p.endswith((".", " ")) for p in parts)
            or any(re.match(r"^(CON|PRN|AUX|NUL|COM[1-9]|LPT[1-9])(?:\.|$)", p, re.I) for p in parts)):
        raise PackageValidationError(f"unsafe archive path: {value!r}")
    return PurePosixPath(value).as_posix()


def _unique(values: list[Any], label: str) -> set[Any]:
    """Require unique identifiers and return the validated identity set."""
    if len(values) != len(set(values)):
        raise PackageValidationError(f"duplicate {label}")
    return set(values)


def validate_manifest(manifest: Mapping[str, Any], *, python_version: str = "3.12") -> None:
    """Validate archive paths, identity closure, runtime compatibility and hook declarations."""
    validate_document(manifest, "manifest")
    files = _unique([archive_path(f["path"]) for f in manifest["files"]], "file path")
    _unique([p.casefold() for p in files], "case-insensitive file path")
    folded_files = {path.casefold() for path in files}
    prefixes = {}
    for path in files:
        for prefix in (PurePosixPath(path), *PurePosixPath(path).parents):
            name = prefix.as_posix()
            if prefixes.setdefault(name.casefold(), name) != name:
                raise PackageValidationError("case-insensitive directory alias")
    for path in files:
        if any(parent.as_posix().casefold() in folded_files for parent in PurePosixPath(path).parents):
            raise PackageValidationError("file/directory path collision")
    collections = manifest["collections"]
    identities = {k: _unique([r["id"] for r in collections[k]], f"{k} identity") for k in COLLECTIONS}
    documents = set()
    for kind, resources in collections.items():
        for resource in resources:
            document = archive_path(resource["document"])
            if not document.startswith(kind + "/") or document not in files:
                raise PackageValidationError("missing or misplaced resource document")
            if document in documents:
                raise PackageValidationError("shared resource document identity")
            documents.add(document)
            _unique(resource["files"], "resource file reference")
            for path in resource["files"]:
                if archive_path(path) not in files:
                    raise PackageValidationError("missing resource file target")
            for ref in resource["references"]:
                if ref["id"] not in identities[ref["collection"]]:
                    raise PackageValidationError("missing logical reference target")
    runtime = manifest["runtime"]
    try:
        compatible = Version(python_version) in SpecifierSet(runtime["python"])
    except (InvalidSpecifier, ValueError) as exc:
        raise PackageValidationError("invalid runtime compatibility") from exc
    if not compatible:
        raise PackageValidationError("incompatible Python runtime")
    def repository_file(path: str) -> None:
        """Require a declared runtime path beneath the repository collection."""
        if archive_path(path) not in files or not path.startswith("repository/"):
            raise PackageValidationError("runtime file must be in package repository")
    if runtime["requirements_lock"] is not None:
        repository_file(runtime["requirements_lock"])
    hooks = runtime["entrypoints"]
    _unique([h["id"] for h in hooks], "entrypoint identity")
    by_id = {h["id"]: h for h in hooks}
    for hook in hooks:
        repository_file(hook["file"])
        if not hook["file"].endswith(".py"):
            raise PackageValidationError("unsupported entrypoint file")
    def require_hook(hook_id: str, operation: str) -> None:
        """Require an existing entrypoint with the requested operation role."""
        if hook_id not in by_id or by_id[hook_id]["operation"] != operation:
            raise PackageValidationError("missing or incompatible entrypoint")
    _unique([w["id"] for w in runtime["workflows"]], "workflow identity")
    for workflow in runtime["workflows"]:
        if workflow["repository_id"] not in identities["repository"]:
            raise PackageValidationError("workflow repository is missing")
        repository_file(workflow["entry_file"])
        if not workflow["entry_file"].endswith(".prism"):
            raise PackageValidationError("unsupported workflow entrypoint")
        require_hook(workflow["prepare_hook"], "prepare")
        if workflow.get("execute_hook") is not None:
            require_hook(workflow["execute_hook"], "execute")
            if workflow["verify_hook"] is None:
                raise PackageValidationError("native execution requires a verification hook")
        if workflow["verify_hook"] is not None:
            require_hook(workflow["verify_hook"], "verify")
        _unique(workflow["modes"], "workflow mode")
        if not workflow["modes"]:
            raise PackageValidationError("workflow has no supported mode")
        for key in ("input_schema", "output_schema"):
            try:
                Draft202012Validator.check_schema(workflow[key])
            except Exception as exc:
                raise PackageValidationError("invalid workflow schema") from exc
            # Network schema resolution is never an upload side effect.
            def check_refs(value: Any) -> None:
                """Reject workflow schema references that would resolve outside the document."""
                if isinstance(value, dict):
                    for k, v in value.items():
                        if k in {"$ref", "$dynamicRef"} and (not isinstance(v, str) or not v.startswith("#")):
                            raise PackageValidationError("workflow schemas must be self-contained")
                        check_refs(v)
                elif isinstance(value, list):
                    for v in value:
                        check_refs(v)
            check_refs(workflow[key])
    for hook_id in runtime["planning_hooks"]:
        require_hook(hook_id, "plan")


def _json(raw: bytes) -> Any:
    """Decode unambiguous finite JSON without consulting any external resource."""
    def invalid_constant(value):
        """Reject non-finite numeric literals before they enter a resource document."""
        raise PackageValidationError("non-finite JSON number")

    def finite_float(value):
        """Reject numeric overflow while decoding a JSON floating-point value."""
        number = float(value)
        if not math.isfinite(number):
            invalid_constant(value)
        return number

    def pairs(items):
        """Build an object while rejecting repeated JSON member names."""
        result = {}
        for key, value in items:
            if key in result:
                raise PackageValidationError("duplicate JSON object key")
            result[key] = value
        return result
    try:
        return json.loads(raw, object_pairs_hook=pairs, parse_constant=invalid_constant, parse_float=finite_float)
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise PackageValidationError("invalid JSON document") from exc


def validate_payloads(manifest: Mapping[str, Any], payloads: Mapping[str, bytes], *, python_version: str = "3.12") -> dict[str, list[dict[str, Any]]]:
    """Validate a bounded payload snapshot supplied by the importer/exporter.

    ZIP streaming and deployment consumption limits belong to the archive reader.
    This function receives bytes only and cannot execute a hook or install a lock.
    """
    validate_manifest(manifest, python_version=python_version)
    expected = {f["path"]: f for f in manifest["files"]}
    if set(payloads) != set(expected):
        raise PackageValidationError("payload inventory mismatch")
    for path, raw in payloads.items():
        row = expected[path]
        if len(raw) != row["size"] or hashlib.sha256(raw).hexdigest() != row["sha256"]:
            raise PackageValidationError(f"payload digest or size mismatch: {path}")
    return validate_documents(manifest, payloads, python_version=python_version)


def validate_documents(manifest: Mapping[str, Any], payloads: Mapping[str, bytes], *, python_version: str = "3.12") -> dict[str, list[dict[str, Any]]]:
    """Validate document relationships after a bounded reader verifies payload hashes.

    The caller must first validate exact inventory, byte lengths and digests.
    Only collection document bytes are read here, allowing streaming importers
    to avoid materializing large datasets or attachments in memory.
    """
    validate_manifest(manifest, python_version=python_version)
    expected = {f["path"]: f for f in manifest["files"]}
    result = {kind: [] for kind in COLLECTIONS}
    for kind in COLLECTIONS:
        for resource in manifest["collections"][kind]:
            doc = _json(payloads[resource["document"]])
            validate_document(doc, kind)
            if doc["id"] != resource["id"]:
                raise PackageValidationError("resource document identity mismatch")
            allowed = set(resource["files"])
            def linked_file(path: str) -> None:
                """Require a referenced payload in the resource file closure and expected collection."""
                if path not in allowed:
                    raise PackageValidationError("undeclared local file relationship")
            if kind == "data-sources":
                _unique([f["id"] for f in doc["local_files"]] + [f["id"] for f in doc["remote_references"]], "source file identity")
                for file in doc["local_files"]:
                    linked_file(file["file"])
                for ref in doc["remote_references"]:
                    uri = urlsplit(ref["uri"])
                    if uri.scheme not in {"https", "http", "s3", "gs", "ftp"} or not uri.netloc or uri.username or uri.password:
                        raise PackageValidationError("unsupported or credential-bearing remote reference")
            elif kind == "reports":
                versions = _unique([r["version"] for r in doc["revisions"]], "report revision")
                if doc["version"] in versions or any(v >= doc["version"] for v in versions):
                    raise PackageValidationError("report revision ordering is inconsistent")
                runs = _unique([r["id"] for r in doc["runs"]], "historical run identity")
                outputs = _unique([o["id"] for o in doc["outputs"]], "historical output identity")
                _unique([s["id"] for s in doc["sections"]], "report section identity")
                _unique([s["ordinal"] for s in doc["sections"]], "report section ordinal")
                _unique([a["link"] for a in doc["attachments"]], "attachment link")
                for output in doc["outputs"]:
                    if output["run_id"] not in runs:
                        raise PackageValidationError("missing historical run")
                for section in doc["sections"]:
                    if section["output_id"] is not None and section["output_id"] not in outputs:
                        raise PackageValidationError("missing historical output")
                for attachment in doc["attachments"]:
                    linked_file(attachment["file"])
                for provenance in doc["provenance"]:
                    linked_file(provenance["file"])
                    if expected[provenance["file"]]["sha256"] != provenance["sha256"]:
                        raise PackageValidationError("original provenance digest mismatch")
            result[kind].append(doc)
    return result
