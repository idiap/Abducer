# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
"""Production sealing for experiment-world causal producer evidence.

The world-matrix contract accepts a producer binding only when five distinct
files can be reopened: the digest-bound request, the dispatcher receipt, the
live artifact, its immutable per-attempt history, and a separately committed
clock/path witness.  This module is the production counterpart of the old test
harness.  It invokes an argv-only registered operator, an independently
registered argv-only validator, and returns concrete paths suitable for the
canonical transaction store.

The runtime validates local protocol execution only.  It does not make the
producer external, independent, physically authoritative, or capable of
changing the theory.  Domain builders and the canonical commit chain retain
those authority decisions.
"""

from __future__ import annotations

import contextlib
import copy
import fcntl
import json
import os
import re
import stat
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterator, Mapping

from agentic.discovery.contracts import (
    ContractError,
    Namespace,
    canonical_digest,
    canonical_json,
    fsync_directory,
    stable_identifier,
    validate_identifier,
)
from agentic.discovery.receipts import (
    DiscoveryOperatorDispatcher,
    OperatorBinding,
    ReceiptStore,
    build_operator_request,
    validate_operator_receipt_identity,
    validate_operator_request_identity,
)

from .world_matrix import (
    CommittedCausalEvidencePaths,
    CommittedCausalEvidenceResolver,
    build_experiment_causal_producer_binding,
    build_governed_clock_evidence,
)


CAUSAL_ARTIFACT_OPERATOR_ID = "canonical-causal-artifact-producer"
CAUSAL_ARTIFACT_OPERATOR_VERSION = "1.0.0"
CAUSAL_ARTIFACT_VALIDATOR_ID = "canonical-causal-artifact-producer-validator"
CAUSAL_ARTIFACT_VALIDATOR_VERSION = "1.0.0"
CAUSAL_ARTIFACT_OPERATOR_KIND = "support_probe"
LOCAL_CAUSAL_AUTHORITY_BOUNDARY = (
    "local dispatcher and byte validator evidence only; no external "
    "independence, physical-target, proof, theory-selection, or theory-mutation authority"
)


@dataclass(frozen=True, slots=True)
class SealedCausalArtifact:
    """One real producer invocation and its concrete committed evidence paths."""

    binding: Mapping[str, Any]
    evidence_paths: CommittedCausalEvidencePaths
    producer_request: Mapping[str, Any]
    producer_receipt: Mapping[str, Any]


def _read_regular_file(path: Path) -> bytes:
    flags = os.O_RDONLY | getattr(os, "O_CLOEXEC", 0) | getattr(os, "O_NOFOLLOW", 0)
    descriptor = -1
    try:
        descriptor = os.open(path, flags)
        metadata = os.fstat(descriptor)
        if not stat.S_ISREG(metadata.st_mode) or metadata.st_nlink != 1:
            raise ContractError(f"immutable evidence is not one singly linked file: {path}")
        chunks: list[bytes] = []
        while True:
            chunk = os.read(descriptor, 1024 * 1024)
            if not chunk:
                break
            chunks.append(chunk)
        return b"".join(chunks)
    except OSError as exc:
        raise ContractError(f"immutable evidence path cannot be reopened: {path}") from exc
    finally:
        if descriptor >= 0:
            os.close(descriptor)


def _write_create_only(path: Path, data: bytes) -> None:
    """Atomically create one single-link file or accept an identical retry."""

    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    try:
        with os.fdopen(descriptor, "wb") as stream:
            stream.write(data)
            stream.flush()
            os.fsync(stream.fileno())
        try:
            os.link(temporary, path, follow_symlinks=False)
        except FileExistsError:
            if _read_regular_file(path) != data:
                raise ContractError(f"immutable causal evidence collision at {path}")
        fsync_directory(path.parent)
    finally:
        try:
            os.unlink(temporary)
        except FileNotFoundError:
            pass


def _write_first_wins(path: Path, data: bytes) -> bytes:
    """Persist the first immutable allocation and reopen it on exact-key races."""

    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    try:
        with os.fdopen(descriptor, "wb") as stream:
            stream.write(data)
            stream.flush()
            os.fsync(stream.fileno())
        try:
            os.link(temporary, path, follow_symlinks=False)
            fsync_directory(path.parent)
            return data
        except FileExistsError:
            return _read_regular_file(path)
    finally:
        try:
            os.unlink(temporary)
        except FileNotFoundError:
            pass


def _decode_json_object(data: bytes, *, label: str) -> dict[str, Any]:
    try:
        value = json.loads(data.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ContractError(f"{label} is not valid JSON") from exc
    if not isinstance(value, dict):
        raise ContractError(f"{label} must be one JSON object")
    return value


def production_causal_operator_binding() -> OperatorBinding:
    """Load the sole production binding from the validated registry."""

    from agentic.scripts.discovery_operator_registry import load_registry
    from agentic.scripts.dispatch_discovery_operators import (
        operator_bindings_from_registry,
    )

    matches = [
        binding
        for binding in operator_bindings_from_registry(load_registry())
        if binding.operator_id == CAUSAL_ARTIFACT_OPERATOR_ID
    ]
    if len(matches) != 1:
        raise ContractError(
            "validated registry must contain exactly one causal artifact producer"
        )
    binding = matches[0]
    if (
        binding.version != CAUSAL_ARTIFACT_OPERATOR_VERSION
        or binding.kind != CAUSAL_ARTIFACT_OPERATOR_KIND
        or len(binding.validators) != 1
        or binding.validators[0].validator_id != CAUSAL_ARTIFACT_VALIDATOR_ID
        or binding.validators[0].version != CAUSAL_ARTIFACT_VALIDATOR_VERSION
    ):
        raise ContractError("causal artifact registry identity drifted")
    return binding


class CausalArtifactProducerRuntime:
    """Execute and seal typed local producer evidence without shared memory."""

    def __init__(
        self,
        *,
        workspace: Path,
        namespace: Namespace,
    ) -> None:
        self.workspace = workspace.resolve()
        self.namespace = namespace
        self.evidence_root = Path(".canonical-causal-evidence")
        receipt_root = self.workspace / self.evidence_root / "receipts"
        self.dispatcher = DiscoveryOperatorDispatcher(
            [production_causal_operator_binding()],
            workspace=self.workspace,
            receipt_store=ReceiptStore(receipt_root),
        )

    @contextlib.contextmanager
    def _invocation_lock(
        self,
        *,
        relative_base: Path,
        invocation_id: str,
    ) -> Iterator[None]:
        """Serialize one durable invocation across threads and local processes."""

        lock_path = self.workspace / relative_base / "locks" / f"{invocation_id}.lock"
        lock_path.parent.mkdir(parents=True, exist_ok=True)
        with lock_path.open("a+b") as stream:
            fcntl.flock(stream.fileno(), fcntl.LOCK_EX)
            try:
                yield
            finally:
                fcntl.flock(stream.fileno(), fcntl.LOCK_UN)

    def _receipt_attempts(
        self,
        *,
        invocation_id: str,
        request: Mapping[str, Any],
    ) -> list[tuple[int, dict[str, Any], Path]]:
        """Reopen every immutable attempt for one exact persisted request."""

        namespace = self.namespace
        directory = (
            self.dispatcher.receipt_store.root
            / namespace.target_id
            / namespace.run_id
            / namespace.branch_id
            / f"state-{namespace.state_version}"
            / invocation_id
        )
        if not directory.exists():
            return []
        if directory.is_symlink() or not directory.is_dir():
            raise ContractError("causal receipt attempt root is not a real directory")
        attempts: list[tuple[int, dict[str, Any], Path]] = []
        for path in sorted(directory.iterdir(), key=lambda item: item.name):
            match = re.fullmatch(r"attempt-([1-9][0-9]*)\.json", path.name)
            if match is None:
                raise ContractError(
                    f"causal receipt attempt root contains an unexpected entry: {path.name}"
                )
            attempt = int(match.group(1))
            receipt = _decode_json_object(
                _read_regular_file(path),
                label=f"causal receipt attempt {attempt}",
            )
            validate_operator_receipt_identity(receipt, request)
            if receipt.get("attempt") != attempt:
                raise ContractError("causal receipt path and attempt identity differ")
            attempts.append((attempt, receipt, path.resolve(strict=True)))
        if [row[0] for row in attempts] != list(range(1, len(attempts) + 1)):
            raise ContractError("causal receipt attempts are not one contiguous history")
        return attempts

    def resolver(
        self, *sealed: SealedCausalArtifact
    ) -> CommittedCausalEvidenceResolver:
        """Build a concrete resolver over an explicitly supplied evidence set."""

        return CommittedCausalEvidenceResolver(
            tuple(item.evidence_paths for item in sealed)
        )

    def seal(
        self,
        *,
        stage_id: str,
        producer_role: str,
        artifact_id: str,
        artifact: Mapping[str, Any],
        causal_parameters: Mapping[str, Any] | None = None,
    ) -> SealedCausalArtifact:
        """Run one registered producer and seal its complete causal evidence."""

        validate_identifier(stage_id, "stage_id")
        validate_identifier(producer_role, "producer_role")
        validate_identifier(artifact_id, "artifact_id")
        value = copy.deepcopy(dict(artifact))
        artifact_digest = canonical_digest(value)
        parameters = copy.deepcopy(dict(causal_parameters or {}))
        reserved = {
            "causal_stage_id",
            "producer_role",
            "artifact_id",
            "artifact_digest",
            "artifact_value",
            "evidence_authority_id",
            "authority_boundary",
        }
        collision = sorted(reserved.intersection(parameters))
        if collision:
            raise ContractError(f"causal producer parameter collision: {collision[0]}")
        invocation_id = stable_identifier(
            "causal-producer-invocation",
            self.namespace.as_dict(),
            stage_id,
            producer_role,
            artifact_id,
            artifact_digest,
            canonical_digest(parameters),
        )
        evidence_authority_id = stable_identifier(
            "causal-evidence-authority", invocation_id
        )
        relative_base = (
            self.evidence_root
            / self.namespace.target_id
            / self.namespace.run_id
            / self.namespace.branch_id
            / f"state-{self.namespace.state_version}"
        )
        output_path = (
            relative_base / "artifacts" / f"{invocation_id}.json"
        ).as_posix()
        request_parameters: dict[str, Any] = {
            "causal_stage_id": stage_id,
            "producer_role": producer_role,
            "artifact_id": artifact_id,
            "artifact_digest": artifact_digest,
            "artifact_value": value,
            "evidence_authority_id": evidence_authority_id,
            "authority_boundary": LOCAL_CAUSAL_AUTHORITY_BOUNDARY,
        }
        for key, item in parameters.items():
            request_parameters[key] = copy.deepcopy(item)
        request_path = (
            self.workspace / relative_base / "requests" / f"{invocation_id}.json"
        ).resolve()
        with self._invocation_lock(
            relative_base=relative_base,
            invocation_id=invocation_id,
        ):
            candidate = build_operator_request(
                operator_id=CAUSAL_ARTIFACT_OPERATOR_ID,
                operator_version=CAUSAL_ARTIFACT_OPERATOR_VERSION,
                kind=CAUSAL_ARTIFACT_OPERATOR_KIND,
                namespace=self.namespace,
                invocation_id=invocation_id,
                input_artifacts=[],
                declared_outputs=[output_path],
                parameters=request_parameters,
            )
            request_bytes = _write_first_wins(
                request_path,
                canonical_json(candidate),
            )
            request = _decode_json_object(
                request_bytes,
                label="durable causal producer request",
            )
            validate_operator_request_identity(request)
            for field in (
                "invocation_id",
                "operator",
                "identity",
                "required",
                "parameters",
                "input_artifacts",
                "declared_outputs",
                "input_digest",
            ):
                if request.get(field) != candidate.get(field):
                    raise ContractError(
                        f"durable causal producer request changed semantic field {field}"
                    )

            attempts = self._receipt_attempts(
                invocation_id=invocation_id,
                request=request,
            )
            successful = [row for row in attempts if row[1].get("status") == "succeeded"]
            if successful:
                _, receipt, receipt_path = successful[-1]
            else:
                attempt = len(attempts) + 1
                receipt = self.dispatcher.dispatch(request, attempt=attempt)
                receipt_path = self.dispatcher.receipt_store.path_for(receipt).resolve(
                    strict=True
                )
            if receipt.get("status") != "succeeded":
                raise ContractError(
                    "causal artifact producer failed: "
                    + str(
                        receipt.get("error", {}).get(
                            "message", receipt.get("status")
                        )
                    )
                )
            if len(receipt.get("output_history_artifacts", [])) != 1:
                raise ContractError(
                    "causal producer receipt lacks one immutable output history"
                )
            history_descriptor = receipt["output_history_artifacts"][0]
            history_path = (self.workspace / history_descriptor["path"]).resolve(
                strict=True
            )
            artifact_path = (self.workspace / output_path).resolve(strict=True)
            clock_path = (
                self.workspace / relative_base / "clocks" / f"{invocation_id}.json"
            ).resolve()
            binding = build_experiment_causal_producer_binding(
                stage_id=stage_id,
                producer_role=producer_role,
                artifact_id=artifact_id,
                artifact_value=value,
                artifact_bytes=_read_regular_file(history_path),
                producer_request=request,
                producer_request_bytes=request_bytes,
                producer_receipt=receipt,
                producer_receipt_bytes=_read_regular_file(receipt_path),
                declared_output_path=output_path,
                sealed_at=receipt["completed_at"],
                clock_authority_id="canonical-local-governed-utc-clock",
                evidence_authority_id=evidence_authority_id,
            )
            evidence_paths = CommittedCausalEvidencePaths(
                evidence_authority_id=evidence_authority_id,
                producer_request_path=request_path,
                producer_receipt_path=receipt_path,
                artifact_path=artifact_path,
                immutable_history_path=history_path,
                governed_clock_path=clock_path,
            )
            clock = build_governed_clock_evidence(
                binding,
                evidence_paths=evidence_paths,
            )
            _write_create_only(clock_path, canonical_json(clock))
            CommittedCausalEvidenceResolver((evidence_paths,)).resolve(binding)
            return SealedCausalArtifact(
                binding=binding,
                evidence_paths=evidence_paths,
                producer_request=request,
                producer_receipt=receipt,
            )


__all__ = [
    "CAUSAL_ARTIFACT_OPERATOR_ID",
    "CAUSAL_ARTIFACT_OPERATOR_KIND",
    "CAUSAL_ARTIFACT_OPERATOR_VERSION",
    "CAUSAL_ARTIFACT_VALIDATOR_ID",
    "CAUSAL_ARTIFACT_VALIDATOR_VERSION",
    "CausalArtifactProducerRuntime",
    "LOCAL_CAUSAL_AUTHORITY_BOUNDARY",
    "SealedCausalArtifact",
    "production_causal_operator_binding",
]
