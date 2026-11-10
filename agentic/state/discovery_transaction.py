"""Atomic, versioned, recoverable persistence for discovery transitions.

Each target/run owns one advisory lock and an immutable sequence of commit
directories.  A commit stages state plus branch-local artifacts, fsyncs every
file, journals intent, atomically renames the complete directory, then advances a
small compare-and-swap pointer.  Recovery derives truth from verified immutable
manifests, so interruption can expose either the prior generation or the complete
next one—never a mixed collection of files.

Workers never receive a shared-state writer.  They may write content-addressed
results only inside their branch namespace against a frozen input digest; a
single reducer later merges validated siblings through ``commit``.

Verification and recovery traverse from the configured store root with
directory descriptors, reject links and special files, and reuse one exact byte
snapshot for each manifest, state, journal, and artifact.  Unauthenticated
staging entries are quarantined; recursive cleanup is allowed only after a
prepared journal and the staged manifest authenticate the same direct child.
"""

from __future__ import annotations

import contextlib
import copy
import dataclasses
import fcntl
import json
import os
import re
import stat
import tempfile
import threading
import uuid
from pathlib import Path
from typing import Any, Callable, Iterator, Mapping, Sequence

from agentic.discovery.contracts import (
    ContractError,
    Namespace,
    bytes_digest,
    canonical_digest,
    canonical_json,
    fsync_directory,
    safe_relative_path,
    stable_identifier,
    utc_now,
    validate_digest,
    validate_identifier,
)


class ConcurrentRunError(ContractError):
    """Raised when a non-blocking runner finds the target/run already locked."""


class CompareAndSwapError(ContractError):
    """Raised when the caller's expected state generation is stale."""


class IdempotencyConflict(ContractError):
    """Raised when one idempotency key is reused with different frozen inputs."""


class StateCorruptionError(ContractError):
    """Raised when an immutable commit fails digest or namespace validation."""


class VerifiedArtifactContextError(ContractError):
    """Raised when a verified-byte capability is forged, stale, or misused."""


class InjectedFailure(RuntimeError):
    """Test-only crash marker raised at a named durability boundary."""


@dataclasses.dataclass(frozen=True, slots=True)
class CommitArtifact:
    """One branch-local artifact merged by the single-writer transaction."""

    relative_path: str
    content: bytes | Path
    namespace: Namespace


@dataclasses.dataclass(frozen=True, slots=True)
class CommitResult:
    """Address of one verified immutable commit."""

    generation: int
    commit_id: str
    commit_path: Path
    manifest_digest: str
    idempotent: bool = False


@dataclasses.dataclass(frozen=True, slots=True)
class VerifiedCommit:
    """Fully reopened identity and state of one immutable commit.

    ``commit_path`` is deliberately runtime-local and must never be serialized
    into a causal artifact.  Portable references persist the remaining content
    identities and derive the path again from the receiving store.
    """

    generation: int
    prior_generation: int
    commit_id: str
    commit_path: Path
    manifest: Mapping[str, Any]
    manifest_digest: str
    state: Mapping[str, Any]
    state_file_digest: str
    state_semantic_digest: str


@dataclasses.dataclass(frozen=True, slots=True)
class _NormalizedCommitArtifact:
    """Frozen artifact bytes and the exact descriptor persisted in a commit."""

    relative_path: Path
    data: bytes
    descriptor: Mapping[str, Any]


@dataclasses.dataclass(frozen=True, slots=True)
class _NormalizedTransition:
    """Complete proposed transition identity used for CAS and idempotency.

    Idempotency is safe only when a retry proposes the same prior generation,
    deterministic state bytes, semantic state, and canonical artifact vector.
    Freezing these values before acquiring the lock also prevents a mutable
    caller object or source ``Path`` from changing between comparison and write.
    """

    expected_generation: int
    next_generation: int
    state_data: bytes
    state_digest: str
    state_semantic_digest: str
    artifacts: tuple[_NormalizedCommitArtifact, ...]

    @property
    def artifact_vector(self) -> list[dict[str, Any]]:
        """Return a path-ordered, JSON-ready transition artifact identity."""

        return [
            dict(row.descriptor)
            for row in sorted(
                self.artifacts,
                key=lambda item: item.relative_path.as_posix(),
            )
        ]


@dataclasses.dataclass(frozen=True, slots=True)
class _VerifiedCommitSnapshot:
    """One commit reopened once through descriptor-anchored immutable bytes."""

    commit_path: Path
    manifest: dict[str, Any]
    manifest_data: bytes
    state: dict[str, Any]
    state_data: bytes
    artifacts: Mapping[str, bytes]


@dataclasses.dataclass(frozen=True, slots=True)
class _SealedVerifiedCommitSnapshot:
    """Internally immutable projection retained by a verified-byte context."""

    generation: int
    commit_path: Path
    manifest_data: bytes
    state_data: bytes
    artifact_paths: tuple[str, ...]
    artifacts: tuple[tuple[str, bytes], ...]


def _verified_commit_from_snapshot(snapshot: _VerifiedCommitSnapshot) -> VerifiedCommit:
    """Project one already verified byte snapshot into its public identity."""

    manifest = snapshot.manifest
    state_file_digest = bytes_digest(snapshot.state_data)
    state_semantic_digest = canonical_digest(snapshot.state)
    if state_file_digest != manifest["state_digest"]:
        raise StateCorruptionError(f"state digest mismatch: {snapshot.commit_path}")
    if state_semantic_digest != manifest["state_semantic_digest"]:
        raise StateCorruptionError(
            f"state semantic digest mismatch: {snapshot.commit_path}"
        )
    return VerifiedCommit(
        generation=manifest["generation"],
        prior_generation=manifest["prior_generation"],
        commit_id=manifest["commit_id"],
        commit_path=snapshot.commit_path,
        manifest=copy.deepcopy(manifest),
        manifest_digest=bytes_digest(snapshot.manifest_data),
        state=copy.deepcopy(snapshot.state),
        state_file_digest=state_file_digest,
        state_semantic_digest=state_semantic_digest,
    )


def _seal_verified_commit_snapshot(
    snapshot: _VerifiedCommitSnapshot,
) -> _SealedVerifiedCommitSnapshot:
    """Discard mutable parsed objects at the long-lived capability boundary."""

    return _SealedVerifiedCommitSnapshot(
        generation=snapshot.manifest["generation"],
        commit_path=snapshot.commit_path,
        manifest_data=memoryview(snapshot.manifest_data).tobytes(),
        state_data=memoryview(snapshot.state_data).tobytes(),
        artifact_paths=tuple(row["path"] for row in snapshot.manifest["artifacts"]),
        artifacts=tuple(
            (path, memoryview(data).tobytes())
            for path, data in sorted(snapshot.artifacts.items())
        ),
    )


def _decode_sealed_json_object(data: bytes, *, label: str) -> dict[str, Any]:
    """Decode an immutable, previously verified snapshot into a fresh mapping."""

    try:
        value = json.loads(data.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise StateCorruptionError(f"sealed {label} bytes are invalid") from exc
    if not isinstance(value, dict):
        raise StateCorruptionError(f"sealed {label} is not an object")
    return value


def _verified_commit_from_sealed_snapshot(
    snapshot: _SealedVerifiedCommitSnapshot,
) -> VerifiedCommit:
    """Project a sealed context snapshot into a fresh public value."""

    manifest = _decode_sealed_json_object(snapshot.manifest_data, label="manifest")
    state = _decode_sealed_json_object(snapshot.state_data, label="state")
    state_file_digest = bytes_digest(snapshot.state_data)
    state_semantic_digest = canonical_digest(state)
    if (
        manifest.get("generation") != snapshot.generation
        or tuple(row.get("path") for row in manifest.get("artifacts", ()))
        != snapshot.artifact_paths
        or state_file_digest != manifest.get("state_digest")
        or state_semantic_digest != manifest.get("state_semantic_digest")
    ):
        raise StateCorruptionError(
            f"sealed commit snapshot identity changed: {snapshot.commit_path}"
        )
    return VerifiedCommit(
        generation=manifest["generation"],
        prior_generation=manifest["prior_generation"],
        commit_id=manifest["commit_id"],
        commit_path=snapshot.commit_path,
        manifest=manifest,
        manifest_digest=bytes_digest(snapshot.manifest_data),
        state=state,
        state_file_digest=state_file_digest,
        state_semantic_digest=state_semantic_digest,
    )


def _normalize_verified_artifact_paths(relative_paths: Sequence[str]) -> tuple[str, ...]:
    """Validate and deduplicate one exact artifact selection."""

    if isinstance(relative_paths, (str, bytes)):
        raise ContractError("relative_paths must be a sequence of artifact paths")
    requested: list[str] = []
    seen: set[str] = set()
    for raw_path in relative_paths:
        if not isinstance(raw_path, str):
            raise ContractError("verified artifact paths must be strings")
        relative = safe_relative_path(raw_path)
        normalized = relative.as_posix()
        if normalized != raw_path:
            raise ContractError(f"verified artifact path is not canonical: {raw_path!r}")
        if normalized in seen:
            raise ContractError(f"duplicate verified artifact path: {normalized}")
        seen.add(normalized)
        requested.append(normalized)
    return tuple(requested)


class VerifiedArtifactContext:
    """One lock-scoped immutable-prefix verification and byte authority.

    The store constructs this context only after recovery has verified every
    commit, manifest, state, and artifact through anchored no-follow reads.  A
    caller may select any number of commits and exact artifact batches without
    rescanning the filesystem.  The enclosing store lock remains held until
    the context manager exits, preventing a concurrent append from changing
    which generation is current during a causal replay.

    Context methods fail after exit.  Returned identities, mappings, and bytes
    are copies, so callers cannot mutate the authoritative cached snapshots.
    """

    __slots__ = (
        "__store",
        "__target_id",
        "__run_id",
        "__snapshots",
        "__lease_id",
    )

    def __new__(cls, *_args: Any, **_kwargs: Any) -> VerifiedArtifactContext:
        raise VerifiedArtifactContextError(
            "verified artifact contexts must be minted by their store"
        )

    def __init_subclass__(cls, **kwargs: Any) -> None:
        raise TypeError("VerifiedArtifactContext is sealed and cannot be subclassed")

    def __setattr__(self, name: str, value: Any) -> None:
        raise AttributeError("VerifiedArtifactContext is internally immutable")

    @property
    def target_id(self) -> str:
        """Return the namespace target fixed when the store minted the context."""

        self._require_active()
        return self.__target_id

    @property
    def run_id(self) -> str:
        """Return the namespace run fixed when the store minted the context."""

        self._require_active()
        return self.__run_id

    def _require_active(self) -> None:
        try:
            store = self.__store
            target_id = self.__target_id
            run_id = self.__run_id
            snapshots = self.__snapshots
            lease_id = self.__lease_id
        except AttributeError as exc:
            raise VerifiedArtifactContextError(
                "verified artifact context was not store-minted"
            ) from exc
        if type(store) is not DiscoveryTransactionStore:
            raise VerifiedArtifactContextError(
                "verified artifact context has no valid minting store"
            )
        store._assert_verified_artifact_context_lease(
            context=self,
            lease_id=lease_id,
            target_id=target_id,
            run_id=run_id,
            snapshots=snapshots,
        )

    def assert_owned_by(self, store: Any) -> None:
        """Require this live capability to belong to the exact store instance."""

        if type(self) is not VerifiedArtifactContext:
            raise VerifiedArtifactContextError(
                "verified artifact context has an unsupported runtime type"
            )
        self._require_active()
        if self.__store is not store:
            raise VerifiedArtifactContextError(
                "verified artifact context belongs to a different store instance"
            )

    @property
    def current_generation(self) -> int:
        """Return the immutable prefix head captured by this context."""

        self._require_active()
        return self.__snapshots[-1].generation if self.__snapshots else 0

    def _snapshot(self, generation: int) -> _SealedVerifiedCommitSnapshot:
        self._require_active()
        if isinstance(generation, bool) or not isinstance(generation, int) or generation <= 0:
            raise ContractError("verified artifact generation must be a positive integer")
        for snapshot in self.__snapshots:
            if snapshot.generation == generation:
                return snapshot
        raise ContractError(f"unknown generation: {generation}")

    def read_commit(self, generation: int) -> VerifiedCommit:
        """Return one commit identity from the cached verified prefix."""

        return _verified_commit_from_sealed_snapshot(self._snapshot(generation))

    def artifact_paths(self, generation: int) -> tuple[str, ...]:
        """Return the exact path-ordered artifact vector for one commit."""

        return self._snapshot(generation).artifact_paths

    def read_artifacts(
        self,
        generation: int,
        relative_paths: Sequence[str],
    ) -> tuple[VerifiedCommit, dict[str, bytes]]:
        """Select one manifest-covered byte batch without another store scan."""

        requested = _normalize_verified_artifact_paths(relative_paths)
        snapshot = self._snapshot(generation)
        manifest_paths = set(snapshot.artifact_paths)
        artifact_map = dict(snapshot.artifacts)
        missing = [
            path
            for path in requested
            if path not in manifest_paths or path not in artifact_map
        ]
        if missing:
            raise ContractError(
                f"requested artifact is not manifest-covered: {missing[0]}"
            )
        return _verified_commit_from_sealed_snapshot(snapshot), {
            path: memoryview(artifact_map[path]).tobytes()
            for path in requested
        }


@dataclasses.dataclass(frozen=True, slots=True)
class _VerifiedArtifactContextLease:
    """Store-owned authority record for one live verified-byte capability."""

    context: VerifiedArtifactContext
    lease_id: str
    target_id: str
    run_id: str
    owner_thread_id: int
    snapshots: tuple[_SealedVerifiedCommitSnapshot, ...]


@dataclasses.dataclass(frozen=True, slots=True)
class _ValidatedJournal:
    """A journal whose names and identities are safe to use for recovery."""

    name: str
    payload: dict[str, Any]
    data: bytes


_STAGE_NAME = re.compile(
    r"^(?P<generation>[0-9]{12})-(?P<transaction>commit\.[0-9a-f]{24})-"
    r"(?P<nonce>[0-9a-f]{32})$"
)


def _directory_open_flags() -> int:
    """Return the strongest portable flags for an anchored directory open."""

    return (
        os.O_RDONLY
        | getattr(os, "O_CLOEXEC", 0)
        | getattr(os, "O_DIRECTORY", 0)
        | getattr(os, "O_NOFOLLOW", 0)
    )


def _regular_open_flags() -> int:
    """Avoid following links and avoid blocking if a file is raced to a FIFO."""

    return (
        os.O_RDONLY
        | getattr(os, "O_CLOEXEC", 0)
        | getattr(os, "O_NOFOLLOW", 0)
        | getattr(os, "O_NONBLOCK", 0)
    )


def _stat_identity(value: os.stat_result) -> tuple[int, int, int, int, int, int, int]:
    """Fields that must stay stable while one immutable file is snapshotted."""

    return (
        value.st_dev,
        value.st_ino,
        value.st_mode,
        value.st_nlink,
        value.st_size,
        value.st_mtime_ns,
        value.st_ctime_ns,
    )


def _atomic_write_at(directory_fd: int, name: str, data: bytes) -> None:
    """Atomically replace one direct child without resolving a pathname parent."""

    temporary = f".{name}.{uuid.uuid4().hex}.tmp"
    descriptor = os.open(
        temporary,
        os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, "O_CLOEXEC", 0),
        0o600,
        dir_fd=directory_fd,
    )
    try:
        view = memoryview(data)
        while view:
            written = os.write(descriptor, view)
            view = view[written:]
        os.fsync(descriptor)
    finally:
        os.close(descriptor)
    try:
        os.replace(
            temporary,
            name,
            src_dir_fd=directory_fd,
            dst_dir_fd=directory_fd,
        )
        os.fsync(directory_fd)
    finally:
        try:
            os.unlink(temporary, dir_fd=directory_fd)
        except FileNotFoundError:
            pass


def _write_file_fsync(path: Path, data: bytes) -> None:
    """Create/truncate a file and persist its bytes before any rename."""

    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("wb") as stream:
        stream.write(data)
        stream.flush()
        os.fsync(stream.fileno())


def _atomic_write(path: Path, data: bytes) -> None:
    """Replace one small control file atomically and fsync its directory."""

    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    try:
        with os.fdopen(descriptor, "wb") as stream:
            stream.write(data)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
        fsync_directory(path.parent)
    finally:
        try:
            os.unlink(temporary)
        except FileNotFoundError:
            pass


def _json_bytes(payload: Any) -> bytes:
    """Render human-readable deterministic JSON for durable files."""

    return json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False).encode("utf-8") + b"\n"


class DiscoveryTransactionStore:
    """Single-writer state store isolated by exact target and run identity."""

    def __init__(self, root: Path, *, target_id: str, run_id: str) -> None:
        self.root = root.resolve()
        self.target_id = validate_identifier(target_id, "target_id")
        self.run_id = validate_identifier(run_id, "run_id")
        self.run_root = self.root / "targets" / self.target_id / "runs" / self.run_id
        self.commits_dir = self.run_root / "commits"
        self.staging_dir = self.run_root / ".staging"
        self.staging_quarantine_dir = self.run_root / ".staging-quarantine"
        self.journal_dir = self.run_root / "journal"
        self.journal_quarantine_dir = self.run_root / "journal-quarantine"
        self.branch_results_dir = self.run_root / "branch-results"
        self.pointer_path = self.run_root / "state-pointer.json"
        self.allocations_path = self.run_root / "allocations.json"
        self.lock_path = self.run_root / "run.lock"
        self._local_lock = threading.Lock()
        self._verified_context_registry_lock = threading.Lock()
        self._active_verified_context_lease: _VerifiedArtifactContextLease | None = None
        for directory in (
            self.commits_dir,
            self.staging_dir,
            self.staging_quarantine_dir,
            self.journal_dir,
            self.journal_quarantine_dir,
            self.branch_results_dir,
        ):
            directory.mkdir(parents=True, exist_ok=True)

    @contextlib.contextmanager
    def lock(self, *, blocking: bool = True) -> Iterator[None]:
        """Acquire the per-run cross-process lock and always release on signals."""

        self._reject_store_access_during_verified_context()
        acquired = self._local_lock.acquire(blocking=blocking)
        if not acquired:
            raise ConcurrentRunError(
                f"run is already locked: {self.target_id}/{self.run_id}"
            )
        try:
            self._reject_store_access_during_verified_context()
            self.lock_path.parent.mkdir(parents=True, exist_ok=True)
            with self.lock_path.open("a+b") as stream:
                flags = fcntl.LOCK_EX | (0 if blocking else fcntl.LOCK_NB)
                try:
                    fcntl.flock(stream.fileno(), flags)
                except BlockingIOError as exc:
                    raise ConcurrentRunError(
                        f"run is already locked: {self.target_id}/{self.run_id}"
                    ) from exc
                try:
                    yield
                finally:
                    fcntl.flock(stream.fileno(), fcntl.LOCK_UN)
        finally:
            self._local_lock.release()

    def _reject_store_access_during_verified_context(self) -> None:
        """Fail immediately when any thread owns this store's byte capability."""

        with self._verified_context_registry_lock:
            if self._active_verified_context_lease is not None:
                raise VerifiedArtifactContextError(
                    "nested store access inside a verified artifact context is forbidden"
                )

    def _register_verified_artifact_context_lease(
        self,
        *,
        context: VerifiedArtifactContext,
        lease_id: str,
        snapshots: tuple[_SealedVerifiedCommitSnapshot, ...],
    ) -> None:
        """Register the sole live context while the store lock is held."""

        lease = _VerifiedArtifactContextLease(
            context=context,
            lease_id=lease_id,
            target_id=self.target_id,
            run_id=self.run_id,
            owner_thread_id=threading.get_ident(),
            snapshots=snapshots,
        )
        with self._verified_context_registry_lock:
            if self._active_verified_context_lease is not None:
                raise VerifiedArtifactContextError(
                    "verified artifact context is already active for this store"
                )
            self._active_verified_context_lease = lease

    def _assert_verified_artifact_context_lease(
        self,
        *,
        context: VerifiedArtifactContext,
        lease_id: str,
        target_id: str,
        run_id: str,
        snapshots: tuple[_SealedVerifiedCommitSnapshot, ...],
    ) -> None:
        """Validate context identity and immutable bindings against store state."""

        with self._verified_context_registry_lock:
            lease = self._active_verified_context_lease
            if lease is None:
                raise VerifiedArtifactContextError("verified artifact context is closed")
            if (
                lease.context is not context
                or lease.lease_id != lease_id
                or lease.target_id != target_id
                or lease.run_id != run_id
                or lease.snapshots is not snapshots
            ):
                raise VerifiedArtifactContextError(
                    "verified artifact context binding is forged or mutated"
                )
            if lease.owner_thread_id != threading.get_ident():
                raise VerifiedArtifactContextError(
                    "verified artifact context cannot cross its owning thread"
                )

    def _revoke_verified_artifact_context_lease(
        self,
        *,
        context: VerifiedArtifactContext,
        lease_id: str,
    ) -> None:
        """Remove one exact active lease without trusting mutable context slots."""

        with self._verified_context_registry_lock:
            lease = self._active_verified_context_lease
            if (
                lease is None
                or lease.context is not context
                or lease.lease_id != lease_id
            ):
                raise VerifiedArtifactContextError(
                    "verified artifact context lease changed before revocation"
                )
            self._active_verified_context_lease = None

    @staticmethod
    def _hit(failpoint: str | Callable[[str], None] | None, name: str) -> None:
        """Invoke deterministic test failpoints at every durability boundary."""

        if callable(failpoint):
            failpoint(name)
        elif failpoint == name:
            raise InjectedFailure(name)

    def _open_directory_at(self, parent_fd: int, name: str, *, label: str) -> int:
        """Open one directory component without following or racing a link."""

        try:
            before = os.stat(name, dir_fd=parent_fd, follow_symlinks=False)
        except OSError as exc:
            raise StateCorruptionError(f"cannot inspect {label}: {exc}") from exc
        if not stat.S_ISDIR(before.st_mode):
            raise StateCorruptionError(f"{label} is not a real directory")
        try:
            descriptor = os.open(name, _directory_open_flags(), dir_fd=parent_fd)
        except OSError as exc:
            raise StateCorruptionError(f"cannot open {label} without following links: {exc}") from exc
        after = os.fstat(descriptor)
        if (
            not stat.S_ISDIR(after.st_mode)
            or (before.st_dev, before.st_ino) != (after.st_dev, after.st_ino)
        ):
            os.close(descriptor)
            raise StateCorruptionError(f"{label} changed during directory open")
        return descriptor

    @contextlib.contextmanager
    def _open_anchored_directory(self, path: Path) -> Iterator[int]:
        """Traverse below the configured root one no-follow component at a time."""

        try:
            relative = path.relative_to(self.root)
        except ValueError as exc:
            raise StateCorruptionError(f"store path escaped its root: {path}") from exc
        try:
            descriptor = os.open(self.root, _directory_open_flags())
        except OSError as exc:
            raise StateCorruptionError(f"cannot open store root without following links: {exc}") from exc
        try:
            root_stat = os.fstat(descriptor)
            if not stat.S_ISDIR(root_stat.st_mode):
                raise StateCorruptionError("store root is not a real directory")
            for component in relative.parts:
                child = self._open_directory_at(
                    descriptor,
                    component,
                    label=f"directory component {component!r} below {path}",
                )
                os.close(descriptor)
                descriptor = child
            yield descriptor
        finally:
            os.close(descriptor)

    def _snapshot_regular_at(self, parent_fd: int, name: str, *, label: str) -> bytes:
        """Read a one-link regular file once from the same verified descriptor."""

        try:
            entry_before = os.stat(name, dir_fd=parent_fd, follow_symlinks=False)
        except OSError as exc:
            raise StateCorruptionError(f"cannot inspect {label}: {exc}") from exc
        if not stat.S_ISREG(entry_before.st_mode) or entry_before.st_nlink != 1:
            raise StateCorruptionError(f"{label} is not a one-link regular file")
        try:
            descriptor = os.open(name, _regular_open_flags(), dir_fd=parent_fd)
        except OSError as exc:
            raise StateCorruptionError(f"cannot open {label} without following links: {exc}") from exc
        try:
            opened_before = os.fstat(descriptor)
            if (
                not stat.S_ISREG(opened_before.st_mode)
                or opened_before.st_nlink != 1
                or (entry_before.st_dev, entry_before.st_ino)
                != (opened_before.st_dev, opened_before.st_ino)
            ):
                raise StateCorruptionError(f"{label} changed during file open")
            chunks: list[bytes] = []
            while True:
                chunk = os.read(descriptor, 1024 * 1024)
                if not chunk:
                    break
                chunks.append(chunk)
            data = b"".join(chunks)
            opened_after = os.fstat(descriptor)
            if (
                _stat_identity(opened_before) != _stat_identity(opened_after)
                or len(data) != opened_after.st_size
            ):
                raise StateCorruptionError(f"{label} changed while it was read")
        finally:
            os.close(descriptor)
        try:
            entry_after = os.stat(name, dir_fd=parent_fd, follow_symlinks=False)
        except OSError as exc:
            raise StateCorruptionError(f"{label} disappeared after it was read: {exc}") from exc
        if (entry_after.st_dev, entry_after.st_ino) != (
            opened_after.st_dev,
            opened_after.st_ino,
        ):
            raise StateCorruptionError(f"{label} path was substituted during its read")
        return data

    @staticmethod
    def _decode_json_object(data: bytes, *, label: str) -> dict[str, Any]:
        """Decode an already-frozen JSON snapshot and require an object."""

        try:
            payload = json.loads(data.decode("utf-8"))
        except (UnicodeError, json.JSONDecodeError) as exc:
            raise StateCorruptionError(f"cannot decode {label}: {exc}") from exc
        if not isinstance(payload, dict):
            raise StateCorruptionError(f"{label} is not an object")
        return payload

    def _snapshot_regular_path(self, path: Path, *, label: str) -> bytes:
        """Snapshot a store file with every intermediate component anchored."""

        with self._open_anchored_directory(path.parent) as parent_fd:
            return self._snapshot_regular_at(parent_fd, path.name, label=label)

    def _load_json_bytes(self, path: Path) -> tuple[dict[str, Any], bytes]:
        """Read JSON through one no-follow regular-file descriptor snapshot."""

        data = self._snapshot_regular_path(path, label=f"control file {path}")
        return self._decode_json_object(data, label=f"control file {path}"), data

    def _load_json(self, path: Path) -> dict[str, Any]:
        return self._load_json_bytes(path)[0]

    def _snapshot_artifact_tree(
        self,
        directory_fd: int,
        *,
        prefix: Path = Path(),
        expected_device: int,
    ) -> dict[str, bytes]:
        """Enumerate every artifact exactly, rejecting links and special files."""

        before_names = sorted(os.listdir(directory_fd))
        snapshots: dict[str, bytes] = {}
        for name in before_names:
            relative = prefix / name
            label = f"commit artifact {relative.as_posix()}"
            try:
                entry = os.stat(name, dir_fd=directory_fd, follow_symlinks=False)
            except OSError as exc:
                raise StateCorruptionError(f"cannot inspect {label}: {exc}") from exc
            if entry.st_dev != expected_device:
                raise StateCorruptionError(f"{label} crosses the commit filesystem")
            if stat.S_ISDIR(entry.st_mode):
                child_fd = self._open_directory_at(directory_fd, name, label=label)
                try:
                    child_snapshots = self._snapshot_artifact_tree(
                        child_fd,
                        prefix=relative,
                        expected_device=expected_device,
                    )
                finally:
                    os.close(child_fd)
                entry_after = self._entry_at(directory_fd, name)
                if entry_after is None or (
                    entry_after.st_dev,
                    entry_after.st_ino,
                ) != (entry.st_dev, entry.st_ino):
                    raise StateCorruptionError(
                        f"{label} was substituted during artifact enumeration"
                    )
                snapshots.update(child_snapshots)
            elif stat.S_ISREG(entry.st_mode):
                snapshots[relative.as_posix()] = self._snapshot_regular_at(
                    directory_fd,
                    name,
                    label=label,
                )
                entry_after = self._entry_at(directory_fd, name)
                if entry_after is None or (
                    entry_after.st_dev,
                    entry_after.st_ino,
                ) != (entry.st_dev, entry.st_ino):
                    raise StateCorruptionError(
                        f"{label} was substituted during artifact enumeration"
                    )
            else:
                raise StateCorruptionError(f"{label} is a link or special file")
        if sorted(os.listdir(directory_fd)) != before_names:
            raise StateCorruptionError("commit artifact directory changed during enumeration")
        return snapshots

    def _validate_journal(
        self,
        *,
        name: str,
        payload: dict[str, Any],
        data: bytes,
    ) -> _ValidatedJournal:
        """Reject every journal name that could influence recovery path traversal."""

        required = {
            "schema_version",
            "transaction_id",
            "target_id",
            "run_id",
            "generation",
            "stage_directory",
            "commit_directory",
            "manifest_digest",
            "status",
        }
        if required - payload.keys() or payload.get("schema_version") != "1.0.0":
            raise StateCorruptionError("journal is missing required versioned fields")
        transaction_id = payload.get("transaction_id")
        try:
            validate_identifier(transaction_id, "journal transaction_id")
            validate_digest(payload.get("manifest_digest"))
        except ContractError as exc:
            raise StateCorruptionError(f"journal identity is invalid: {exc}") from exc
        generation = payload.get("generation")
        if isinstance(generation, bool) or not isinstance(generation, int) or generation <= 0:
            raise StateCorruptionError("journal generation must be a positive integer")
        if name != f"{transaction_id}.json":
            raise StateCorruptionError("journal filename does not match its transaction")
        if payload.get("target_id") != self.target_id or payload.get("run_id") != self.run_id:
            raise StateCorruptionError("journal target/run identity mismatch")
        expected_commit = f"generation-{generation:012d}-{transaction_id}"
        if payload.get("commit_directory") != expected_commit:
            raise StateCorruptionError("journal commit directory is not its exact direct child")
        stage_name = payload.get("stage_directory")
        expected_stage_prefix = f"{generation:012d}-{transaction_id}-"
        if (
            not isinstance(stage_name, str)
            or not _STAGE_NAME.fullmatch(stage_name)
            or not stage_name.startswith(expected_stage_prefix)
        ):
            raise StateCorruptionError("journal stage directory is not an exact direct child")
        if payload.get("status") not in {"prepared", "committed", "rolled_back"}:
            raise StateCorruptionError("journal status is invalid")
        return _ValidatedJournal(name=name, payload=payload, data=data)

    def _quarantine_entry_at(
        self,
        source_fd: int,
        *,
        source_name: str,
        destination: Path,
        kind: str,
    ) -> str:
        """Move an entry itself—not any link target—into a sibling quarantine."""

        quarantine_name = f"{kind}.{uuid.uuid4().hex}"
        with self._open_anchored_directory(destination) as destination_fd:
            try:
                os.replace(
                    source_name,
                    quarantine_name,
                    src_dir_fd=source_fd,
                    dst_dir_fd=destination_fd,
                )
                os.fsync(source_fd)
                os.fsync(destination_fd)
            except OSError as exc:
                raise StateCorruptionError(f"cannot quarantine invalid {kind}: {exc}") from exc
        return quarantine_name

    def _scan_journals(self) -> dict[str, _ValidatedJournal]:
        """Freeze every journal or quarantine the first invalid directory entry."""

        with self._open_anchored_directory(self.journal_dir) as journal_fd:
            names = sorted(os.listdir(journal_fd))
            journals: dict[str, _ValidatedJournal] = {}
            for name in names:
                try:
                    data = self._snapshot_regular_at(
                        journal_fd,
                        name,
                        label=f"transaction journal {name!r}",
                    )
                    payload = self._decode_json_object(
                        data,
                        label=f"transaction journal {name!r}",
                    )
                    journal = self._validate_journal(name=name, payload=payload, data=data)
                except StateCorruptionError as exc:
                    quarantined = self._quarantine_entry_at(
                        journal_fd,
                        source_name=name,
                        destination=self.journal_quarantine_dir,
                        kind="journal",
                    )
                    raise StateCorruptionError(
                        f"invalid journal {name!r} quarantined as {quarantined}: {exc}"
                    ) from exc
                if journal.payload["transaction_id"] in journals:
                    raise StateCorruptionError("duplicate transaction journal identity")
                journals[journal.payload["transaction_id"]] = journal
            if sorted(os.listdir(journal_fd)) != names:
                raise StateCorruptionError("journal directory changed during enumeration")
            return journals

    def _verify_commit_at(
        self,
        commits_fd: int,
        name: str,
        journals: Mapping[str, _ValidatedJournal],
    ) -> _VerifiedCommitSnapshot:
        """Verify a commit from content, not from names asserted by its manifest.

        A manifest is only an index.  Authority comes from recomputing the
        content-derived commit identifier, checking the exact artifact set, and
        tying the visible directory back to the journal record that made it
        durable.  This deliberately rejects a coordinated rewrite of state,
        artifacts, and manifest that merely refreshes their local digests.
        """

        path = self.commits_dir / name
        commit_fd = self._open_directory_at(commits_fd, name, label=f"commit {name!r}")
        try:
            top_level = sorted(os.listdir(commit_fd))
            unexpected = set(top_level) - {"manifest.json", "state.json", "artifacts"}
            if unexpected or not {"manifest.json", "state.json"}.issubset(top_level):
                raise StateCorruptionError(
                    f"commit top-level coverage mismatch: {sorted(unexpected)}"
                )
            manifest_data = self._snapshot_regular_at(
                commit_fd,
                "manifest.json",
                label=f"commit manifest {name!r}",
            )
            state_data = self._snapshot_regular_at(
                commit_fd,
                "state.json",
                label=f"commit state {name!r}",
            )
            manifest = self._decode_json_object(
                manifest_data,
                label=f"commit manifest {name!r}",
            )
            state = self._decode_json_object(state_data, label=f"commit state {name!r}")
            actual_artifacts: dict[str, bytes] = {}
            if "artifacts" in top_level:
                artifacts_fd = self._open_directory_at(
                    commit_fd,
                    "artifacts",
                    label=f"commit artifacts {name!r}",
                )
                try:
                    actual_artifacts = self._snapshot_artifact_tree(
                        artifacts_fd,
                        expected_device=os.fstat(commit_fd).st_dev,
                    )
                finally:
                    os.close(artifacts_fd)
            if sorted(os.listdir(commit_fd)) != top_level:
                raise StateCorruptionError(f"commit directory changed during verification: {path}")
        finally:
            os.close(commit_fd)
        required = {
            "schema_version",
            "commit_id",
            "generation",
            "target_id",
            "run_id",
            "prior_generation",
            "idempotency_key",
            "request_digest",
            "state_digest",
            "state_semantic_digest",
            "artifacts",
        }
        if required - manifest.keys():
            raise StateCorruptionError(f"commit manifest missing fields: {path}")
        try:
            validate_digest(manifest["request_digest"])
            validate_digest(manifest["state_digest"])
            validate_digest(manifest["state_semantic_digest"])
            validate_identifier(manifest["commit_id"], "commit_id")
            validate_identifier(manifest["idempotency_key"], "idempotency_key")
        except ContractError as exc:
            raise StateCorruptionError(f"commit manifest identity is invalid: {path}") from exc
        generation = manifest.get("generation")
        prior_generation = manifest.get("prior_generation")
        if (
            isinstance(generation, bool)
            or not isinstance(generation, int)
            or generation <= 0
            or isinstance(prior_generation, bool)
            or not isinstance(prior_generation, int)
            or prior_generation < 0
        ):
            raise StateCorruptionError(f"commit generation is invalid: {path}")
        if manifest["target_id"] != self.target_id or manifest["run_id"] != self.run_id:
            raise StateCorruptionError(f"commit identity mismatch: {path}")
        if bytes_digest(state_data) != manifest["state_digest"]:
            raise StateCorruptionError(f"state digest mismatch: {path}")
        if (
            state.get("target_id") != self.target_id
            or state.get("run_id") != self.run_id
            or state.get("generation") != manifest["generation"]
        ):
            raise StateCorruptionError(f"state namespace/generation mismatch: {path}")
        if canonical_digest(state) != manifest["state_semantic_digest"]:
            raise StateCorruptionError(f"state semantic digest mismatch: {path}")
        if not isinstance(manifest["artifacts"], list):
            raise StateCorruptionError(f"commit artifacts are not a list: {path}")
        seen_paths: set[str] = set()
        artifact_identity: list[dict[str, Any]] = []
        for descriptor in manifest["artifacts"]:
            if not isinstance(descriptor, dict):
                raise StateCorruptionError(f"commit artifact descriptor is not an object: {path}")
            try:
                relative = safe_relative_path(descriptor["path"])
                validate_digest(descriptor["sha256"])
                namespace = Namespace.from_mapping(descriptor["namespace"])
            except (KeyError, TypeError, ContractError) as exc:
                raise StateCorruptionError(f"invalid artifact descriptor: {path}") from exc
            size_bytes = descriptor.get("size_bytes")
            if isinstance(size_bytes, bool) or not isinstance(size_bytes, int) or size_bytes < 0:
                raise StateCorruptionError(f"invalid artifact size: {descriptor.get('path')}")
            relative_text = relative.as_posix()
            if relative_text in seen_paths:
                raise StateCorruptionError(f"duplicate manifest artifact: {relative_text}")
            seen_paths.add(relative_text)
            artifact_data = actual_artifacts.get(relative_text)
            if (
                artifact_data is None
                or bytes_digest(artifact_data) != descriptor["sha256"]
                or len(artifact_data) != size_bytes
            ):
                raise StateCorruptionError(f"artifact digest mismatch: {descriptor['path']}")
            if namespace.target_id != self.target_id or namespace.run_id != self.run_id:
                raise StateCorruptionError(f"artifact crossed target/run namespace: {descriptor['path']}")
            expected_prefix = Path("branches") / namespace.branch_id
            try:
                relative.relative_to(expected_prefix)
            except ValueError as exc:
                raise StateCorruptionError(
                    f"artifact is outside its branch namespace: {descriptor['path']}"
                ) from exc
            artifact_identity.append(
                {
                    "path": relative_text,
                    "sha256": descriptor["sha256"],
                    "namespace": namespace.as_dict(),
                }
            )

        actual_paths = set(actual_artifacts)
        if actual_paths != seen_paths:
            raise StateCorruptionError(
                f"manifest artifact coverage mismatch: missing={sorted(seen_paths - actual_paths)}, "
                f"unmanifested={sorted(actual_paths - seen_paths)}"
            )

        expected_commit_id = stable_identifier(
            "commit",
            self.target_id,
            self.run_id,
            manifest["generation"],
            manifest["idempotency_key"],
            manifest["request_digest"],
            bytes_digest(state_data),
            artifact_identity,
        )
        if manifest["commit_id"] != expected_commit_id:
            raise StateCorruptionError(f"content-derived commit ID mismatch: {path}")
        expected_directory = f"generation-{manifest['generation']:012d}-{expected_commit_id}"
        if path.name != expected_directory:
            raise StateCorruptionError(f"commit directory identity mismatch: {path}")

        journal = journals.get(expected_commit_id)
        if journal is None:
            raise StateCorruptionError(f"visible commit lacks its durability journal: {path}")
        manifest_digest = bytes_digest(manifest_data)
        journal_identity = (
            journal.payload.get("transaction_id"),
            journal.payload.get("target_id"),
            journal.payload.get("run_id"),
            journal.payload.get("generation"),
            journal.payload.get("commit_directory"),
            journal.payload.get("manifest_digest"),
        )
        expected_journal_identity = (
            expected_commit_id,
            self.target_id,
            self.run_id,
            manifest["generation"],
            path.name,
            manifest_digest,
        )
        if journal_identity != expected_journal_identity or journal.payload.get("status") not in {
            "prepared",
            "committed",
        }:
            raise StateCorruptionError(f"commit journal anchor mismatch: {path}")
        return _VerifiedCommitSnapshot(
            commit_path=path,
            manifest=manifest,
            manifest_data=manifest_data,
            state=state,
            state_data=state_data,
            artifacts=dict(actual_artifacts),
        )

    def _valid_commits(
        self,
        journals: Mapping[str, _ValidatedJournal] | None = None,
    ) -> list[_VerifiedCommitSnapshot]:
        """Discover commits exactly and keep one verified byte snapshot each."""

        journal_snapshots = self._scan_journals() if journals is None else journals
        with self._open_anchored_directory(self.commits_dir) as commits_fd:
            names = sorted(os.listdir(commits_fd))
            commits: list[_VerifiedCommitSnapshot] = []
            for name in names:
                try:
                    entry = os.stat(name, dir_fd=commits_fd, follow_symlinks=False)
                except OSError as exc:
                    raise StateCorruptionError(f"cannot inspect commit entry {name!r}: {exc}") from exc
                if not stat.S_ISDIR(entry.st_mode):
                    raise StateCorruptionError(f"commit entry {name!r} is a link or special file")
                commits.append(self._verify_commit_at(commits_fd, name, journal_snapshots))
            if sorted(os.listdir(commits_fd)) != names:
                raise StateCorruptionError("commit directory changed during discovery")
        commits.sort(key=lambda item: item.manifest["generation"])
        expected = 1
        for snapshot in commits:
            manifest = snapshot.manifest
            if manifest["generation"] != expected or manifest["prior_generation"] != expected - 1:
                raise StateCorruptionError("immutable commit generations are not contiguous")
            expected += 1
        return commits

    def _pointer_for(
        self,
        path: Path,
        manifest: Mapping[str, Any],
        *,
        manifest_digest: str,
    ) -> dict[str, Any]:
        return {
            "schema_version": "1.0.0",
            "target_id": self.target_id,
            "run_id": self.run_id,
            "generation": manifest["generation"],
            "commit_id": manifest["commit_id"],
            "commit_directory": path.name,
            "manifest_digest": manifest_digest,
        }

    def _atomic_write_path(self, path: Path, data: bytes) -> None:
        """Write a store control file through an anchored parent descriptor."""

        with self._open_anchored_directory(path.parent) as parent_fd:
            _atomic_write_at(parent_fd, path.name, data)

    def _repair_pointer_locked(self, commits: Sequence[_VerifiedCommitSnapshot]) -> None:
        """Rebuild a corrupted/stale pointer from verified immutable commits."""

        if not commits:
            if self.pointer_path.exists():
                quarantine = self.run_root / f"state-pointer.corrupt.{uuid.uuid4().hex}.json"
                os.replace(self.pointer_path, quarantine)
                fsync_directory(self.run_root)
            return
        latest = commits[-1]
        desired = self._pointer_for(
            latest.commit_path,
            latest.manifest,
            manifest_digest=bytes_digest(latest.manifest_data),
        )
        current: dict[str, Any] | None = None
        if self.pointer_path.exists():
            try:
                current = self._load_json(self.pointer_path)
            except StateCorruptionError:
                current = None
        if current != desired:
            if self.pointer_path.exists() and current is None:
                quarantine = self.run_root / f"state-pointer.corrupt.{uuid.uuid4().hex}.json"
                os.replace(self.pointer_path, quarantine)
            self._atomic_write_path(self.pointer_path, _json_bytes(desired))

    @staticmethod
    def _entry_at(directory_fd: int, name: str) -> os.stat_result | None:
        """Return a direct child's no-follow stat, or ``None`` if it is absent."""

        try:
            return os.stat(name, dir_fd=directory_fd, follow_symlinks=False)
        except FileNotFoundError:
            return None
        except OSError as exc:
            raise StateCorruptionError(f"cannot inspect directory entry {name!r}: {exc}") from exc

    def _remove_directory_contents(self, directory_fd: int, *, expected_device: int) -> None:
        """Remove private staging contents without ever following a link target."""

        for name in sorted(os.listdir(directory_fd)):
            entry = self._entry_at(directory_fd, name)
            if entry is None:
                raise StateCorruptionError("staging entry disappeared during cleanup")
            if entry.st_dev != expected_device:
                raise StateCorruptionError("staging cleanup crossed a filesystem boundary")
            if stat.S_ISDIR(entry.st_mode):
                child_fd = self._open_directory_at(
                    directory_fd,
                    name,
                    label=f"private staging directory {name!r}",
                )
                try:
                    self._remove_directory_contents(
                        child_fd,
                        expected_device=expected_device,
                    )
                finally:
                    os.close(child_fd)
                os.rmdir(name, dir_fd=directory_fd)
            else:
                # unlink removes the directory entry itself.  A symlink, FIFO,
                # socket, or hard link can never redirect cleanup to its target.
                os.unlink(name, dir_fd=directory_fd)
        if os.listdir(directory_fd):
            raise StateCorruptionError("staging directory changed during cleanup")

    def _discard_authenticated_stage(
        self,
        staging_fd: int,
        journal: _ValidatedJournal,
    ) -> None:
        """Delete only the direct staging child proven by this journal/manifest."""

        payload = journal.payload
        stage_name = payload["stage_directory"]
        stage_entry = self._entry_at(staging_fd, stage_name)
        if stage_entry is None or not stat.S_ISDIR(stage_entry.st_mode):
            raise StateCorruptionError("journal staging target is absent, linked, or special")
        stage_fd = self._open_directory_at(
            staging_fd,
            stage_name,
            label=f"journal staging directory {stage_name!r}",
        )
        try:
            manifest_data = self._snapshot_regular_at(
                stage_fd,
                "manifest.json",
                label=f"staged manifest for {payload['transaction_id']}",
            )
            manifest = self._decode_json_object(
                manifest_data,
                label=f"staged manifest for {payload['transaction_id']}",
            )
        finally:
            os.close(stage_fd)
        manifest_identity = (
            manifest.get("commit_id"),
            manifest.get("target_id"),
            manifest.get("run_id"),
            manifest.get("generation"),
            bytes_digest(manifest_data),
        )
        expected_identity = (
            payload["transaction_id"],
            self.target_id,
            self.run_id,
            payload["generation"],
            payload["manifest_digest"],
        )
        if manifest_identity != expected_identity:
            raise StateCorruptionError("journal does not authenticate the staged manifest")

        # First rename the verified inode to a private direct child.  If the
        # source name was swapped between validation and rename, the inode check
        # fails before any recursive deletion occurs.
        cleanup_name = f".deleting.{uuid.uuid4().hex}"
        os.replace(
            stage_name,
            cleanup_name,
            src_dir_fd=staging_fd,
            dst_dir_fd=staging_fd,
        )
        os.fsync(staging_fd)
        cleanup_entry = self._entry_at(staging_fd, cleanup_name)
        if cleanup_entry is None or (
            cleanup_entry.st_dev,
            cleanup_entry.st_ino,
        ) != (stage_entry.st_dev, stage_entry.st_ino):
            raise StateCorruptionError("staging target was substituted before cleanup")
        cleanup_fd = self._open_directory_at(
            staging_fd,
            cleanup_name,
            label="renamed private staging directory",
        )
        try:
            self._remove_directory_contents(
                cleanup_fd,
                expected_device=cleanup_entry.st_dev,
            )
        finally:
            os.close(cleanup_fd)
        os.rmdir(cleanup_name, dir_fd=staging_fd)
        os.fsync(staging_fd)

    def _rewrite_journal_at(
        self,
        journal_fd: int,
        journal: _ValidatedJournal,
        payload: Mapping[str, Any],
    ) -> None:
        """Replace a journal only if its previously validated bytes are current."""

        current = self._snapshot_regular_at(
            journal_fd,
            journal.name,
            label=f"transaction journal {journal.name!r}",
        )
        if current != journal.data:
            raise StateCorruptionError("journal changed before recovery update")
        _atomic_write_at(journal_fd, journal.name, _json_bytes(payload))

    def _recover_verified_commits_locked(self) -> list[_VerifiedCommitSnapshot]:
        """Recover with validated journals and descriptor-anchored direct children.

        Pre-journal orphan stages are moved intact to quarantine.  Recursive
        deletion is reserved for a prepared journal whose exact staged manifest
        authenticates the direct child; invalid payloads or links fail closed.
        """

        journals = self._scan_journals()
        commits = self._valid_commits(journals)
        visible_names = {snapshot.commit_path.name for snapshot in commits}
        with self._open_anchored_directory(self.journal_dir) as journal_fd, self._open_anchored_directory(
            self.staging_dir
        ) as staging_fd:
            for transaction_id in sorted(journals):
                journal = journals[transaction_id]
                payload = journal.payload
                final_name = payload["commit_directory"]
                stage_name = payload["stage_directory"]
                stage_entry = self._entry_at(staging_fd, stage_name)
                if final_name in visible_names:
                    if stage_entry is not None:
                        raise StateCorruptionError("visible commit still has a staging alias")
                    if payload["status"] != "committed":
                        updated = copy.deepcopy(payload)
                        updated["status"] = "committed"
                        updated["recovered_at"] = utc_now()
                        self._rewrite_journal_at(journal_fd, journal, updated)
                    continue
                if payload["status"] == "rolled_back" and stage_entry is None:
                    continue
                if payload["status"] != "prepared" or stage_entry is None:
                    if stage_entry is not None:
                        self._quarantine_entry_at(
                            staging_fd,
                            source_name=stage_name,
                            destination=self.staging_quarantine_dir,
                            kind="staging",
                        )
                    quarantined = self._quarantine_entry_at(
                        journal_fd,
                        source_name=journal.name,
                        destination=self.journal_quarantine_dir,
                        kind="journal",
                    )
                    raise StateCorruptionError(
                        f"inconsistent journal quarantined as {quarantined}"
                    )
                try:
                    self._discard_authenticated_stage(staging_fd, journal)
                except StateCorruptionError as exc:
                    if self._entry_at(staging_fd, stage_name) is not None:
                        self._quarantine_entry_at(
                            staging_fd,
                            source_name=stage_name,
                            destination=self.staging_quarantine_dir,
                            kind="staging",
                        )
                    quarantined = self._quarantine_entry_at(
                        journal_fd,
                        source_name=journal.name,
                        destination=self.journal_quarantine_dir,
                        kind="journal",
                    )
                    raise StateCorruptionError(
                        f"unsafe staged transaction quarantined as {quarantined}: {exc}"
                    ) from exc
                updated = copy.deepcopy(payload)
                updated["status"] = "rolled_back"
                updated["recovered_at"] = utc_now()
                self._rewrite_journal_at(journal_fd, journal, updated)

            # Stages created before a journal was durable are not authenticated
            # deletion targets.  Quarantine the entry itself so recovery leaves
            # no active staging while preserving its bytes for diagnosis.
            for orphan_name in sorted(os.listdir(staging_fd)):
                self._quarantine_entry_at(
                    staging_fd,
                    source_name=orphan_name,
                    destination=self.staging_quarantine_dir,
                    kind="staging-orphan",
                )
        self._repair_pointer_locked(commits)
        return commits

    def _recover_locked(self) -> int:
        """Recover and return the generation of the verified immutable suffix."""

        commits = self._recover_verified_commits_locked()
        return commits[-1].manifest["generation"] if commits else 0

    def recover(self) -> int:
        """Recover after crash/SIGINT/SIGTERM and return the visible generation."""

        with self.lock():
            return self._recover_locked()

    def current_generation(self) -> int:
        """Return the verified generation, repairing control metadata if needed."""

        with self.lock():
            return self._recover_locked()

    @contextlib.contextmanager
    def verified_artifact_context(self) -> Iterator[VerifiedArtifactContext]:
        """Yield one lock-scoped verified immutable-prefix byte context.

        This is the authority-preserving route for multi-generation replay: it
        performs recovery and full verification once, keeps the store lock for
        the causal read, and serves every subsequent selection from the same
        immutable byte snapshots.
        """

        with self.lock():
            snapshots = tuple(
                _seal_verified_commit_snapshot(row)
                for row in self._recover_verified_commits_locked()
            )
            lease_id = uuid.uuid4().hex
            context = object.__new__(VerifiedArtifactContext)
            object.__setattr__(context, "_VerifiedArtifactContext__store", self)
            object.__setattr__(
                context,
                "_VerifiedArtifactContext__target_id",
                self.target_id,
            )
            object.__setattr__(
                context,
                "_VerifiedArtifactContext__run_id",
                self.run_id,
            )
            object.__setattr__(
                context,
                "_VerifiedArtifactContext__snapshots",
                snapshots,
            )
            object.__setattr__(
                context,
                "_VerifiedArtifactContext__lease_id",
                lease_id,
            )
            self._register_verified_artifact_context_lease(
                context=context,
                lease_id=lease_id,
                snapshots=snapshots,
            )
            try:
                yield context
            finally:
                self._revoke_verified_artifact_context_lease(
                    context=context,
                    lease_id=lease_id,
                )

    def read_state(self, generation: int | None = None) -> dict[str, Any] | None:
        """Read a verified immutable state; generation zero has no state object."""

        with self.lock():
            current = self._recover_locked()
            selected = current if generation is None else generation
            if selected == 0:
                return None
            for snapshot in self._valid_commits():
                if snapshot.manifest["generation"] == selected:
                    return copy.deepcopy(snapshot.state)
            raise ContractError(f"unknown generation: {selected}")

    def read_verified_commit(self, generation: int | None = None) -> VerifiedCommit:
        """Reopen one commit from immutable content rather than the CAS pointer.

        Recovery may repair the convenience pointer, but selection and identity
        come only from the complete verified commit sequence.  Generation zero
        has no commit and is therefore rejected instead of returning a nullable
        wrapper.
        """

        with self.verified_artifact_context() as context:
            selected = context.current_generation if generation is None else generation
            if isinstance(selected, bool) or not isinstance(selected, int) or selected <= 0:
                raise ContractError("verified commit generation must be a positive integer")
            return context.read_commit(selected)

    def read_verified_artifacts(
        self,
        generation: int,
        relative_paths: Sequence[str],
    ) -> tuple[VerifiedCommit, dict[str, bytes]]:
        """Return an exact manifest-covered artifact batch from one verification.

        Recovery, commit verification, selection, and artifact collection all
        run under one store lock.  The returned bytes come from the artifact map
        already captured by ``_verify_commit_at``; this method never reopens an
        artifact pathname after validation.
        """

        with self.verified_artifact_context() as context:
            return context.read_artifacts(generation, relative_paths)

    def allocate_identity(self, kind: str) -> str:
        """Allocate monotonic cycle/invocation IDs independently of file counts."""

        if kind not in {"cycle", "invocation"}:
            raise ContractError("identity kind must be cycle or invocation")
        with self.lock():
            self._recover_locked()
            counters = {"schema_version": "1.0.0", "cycle": 0, "invocation": 0}
            if self.allocations_path.exists():
                counters = self._load_json(self.allocations_path)
            counters[kind] = int(counters.get(kind, 0)) + 1
            self._atomic_write_path(self.allocations_path, _json_bytes(counters))
            return f"{kind}-{counters[kind]:012d}"

    def _normalize_transition(
        self,
        *,
        expected_generation: int,
        state: Mapping[str, Any],
        artifacts: Sequence[CommitArtifact],
    ) -> _NormalizedTransition:
        """Freeze and validate every byte participating in one transition."""

        if (
            isinstance(expected_generation, bool)
            or not isinstance(expected_generation, int)
            or expected_generation < 0
        ):
            raise ContractError("expected_generation must be a non-negative integer")
        next_generation = expected_generation + 1
        frozen_state = copy.deepcopy(dict(state))
        if (
            frozen_state.get("target_id") != self.target_id
            or frozen_state.get("run_id") != self.run_id
            or frozen_state.get("generation") != next_generation
        ):
            raise ContractError("state identity and next generation must match the transaction")

        normalized_artifacts: list[_NormalizedCommitArtifact] = []
        seen_paths: set[str] = set()
        for artifact in artifacts:
            namespace = artifact.namespace
            if namespace.target_id != self.target_id or namespace.run_id != self.run_id:
                raise ContractError("artifact target/run does not match transaction")
            if namespace.state_version != expected_generation:
                raise ContractError("artifact is not bound to the frozen prior state generation")
            relative = safe_relative_path(artifact.relative_path)
            required_prefix = Path("branches") / namespace.branch_id
            try:
                relative.relative_to(required_prefix)
            except ValueError as exc:
                raise ContractError(
                    f"artifact path must be branch-local under {required_prefix}: {relative}"
                ) from exc
            relative_text = relative.as_posix()
            if relative_text in seen_paths:
                raise ContractError(f"duplicate artifact path: {relative}")
            seen_paths.add(relative_text)
            data = (
                artifact.content.read_bytes()
                if isinstance(artifact.content, Path)
                else artifact.content
            )
            if not isinstance(data, bytes):
                raise ContractError("artifact content must be bytes or a Path")
            normalized_artifacts.append(
                _NormalizedCommitArtifact(
                    relative_path=relative,
                    data=data,
                    descriptor={
                        "path": relative_text,
                        "sha256": bytes_digest(data),
                        "size_bytes": len(data),
                        "namespace": namespace.as_dict(),
                    },
                )
            )

        state_data = _json_bytes(frozen_state)
        return _NormalizedTransition(
            expected_generation=expected_generation,
            next_generation=next_generation,
            state_data=state_data,
            state_digest=bytes_digest(state_data),
            state_semantic_digest=canonical_digest(frozen_state),
            artifacts=tuple(normalized_artifacts),
        )

    def _find_idempotent(
        self,
        commits: Sequence[_VerifiedCommitSnapshot],
        key: str,
        request_digest: str,
        transition: _NormalizedTransition,
    ) -> CommitResult | None:
        """Return only an exact replay; reject every same-key transition drift."""

        for snapshot in commits:
            path = snapshot.commit_path
            manifest = snapshot.manifest
            if manifest["idempotency_key"] != key:
                continue
            mismatches: list[str] = []
            expected_fields = {
                "prior_generation": transition.expected_generation,
                "generation": transition.next_generation,
                "request_digest": request_digest,
                "state_digest": transition.state_digest,
                "state_semantic_digest": transition.state_semantic_digest,
            }
            mismatches.extend(
                field
                for field, expected in expected_fields.items()
                if manifest.get(field) != expected
            )
            if snapshot.state_data != transition.state_data:
                mismatches.append("state_bytes")
            manifest_vector = sorted(
                [dict(row) for row in manifest.get("artifacts", [])],
                key=lambda row: str(row.get("path", "")),
            )
            if manifest_vector != transition.artifact_vector:
                mismatches.append("artifact_vector")
            if mismatches:
                raise IdempotencyConflict(
                    f"idempotency key {key!r} was used with a different proposed "
                    f"transition: {', '.join(sorted(set(mismatches)))}"
                )
            return CommitResult(
                generation=manifest["generation"],
                commit_id=manifest["commit_id"],
                commit_path=path,
                manifest_digest=bytes_digest(snapshot.manifest_data),
                idempotent=True,
            )
        return None

    def commit(
        self,
        *,
        expected_generation: int,
        state: Mapping[str, Any],
        artifacts: Sequence[CommitArtifact],
        idempotency_key: str,
        request_digest: str,
        failpoint: str | Callable[[str], None] | None = None,
    ) -> CommitResult:
        """Commit one complete next generation using CAS and a durable journal."""

        validate_identifier(idempotency_key, "idempotency_key")
        validate_digest(request_digest)
        # Normalize before looking for a prior key so idempotency compares the
        # transition actually requested, not only a caller-supplied digest.
        transition = self._normalize_transition(
            expected_generation=expected_generation,
            state=state,
            artifacts=artifacts,
        )
        with self.lock():
            current = self._recover_locked()
            commits = self._valid_commits()
            existing = self._find_idempotent(
                commits,
                idempotency_key,
                request_digest,
                transition,
            )
            if existing is not None:
                return existing
            if current != expected_generation:
                raise CompareAndSwapError(
                    f"compare-and-swap failed: expected {expected_generation}, current {current}"
                )
            next_generation = transition.next_generation
            state_data = transition.state_data
            artifact_request = [
                {
                    "path": row.descriptor["path"],
                    "sha256": row.descriptor["sha256"],
                    "namespace": row.descriptor["namespace"],
                }
                for row in transition.artifacts
            ]
            commit_id = stable_identifier(
                "commit",
                self.target_id,
                self.run_id,
                next_generation,
                idempotency_key,
                request_digest,
                bytes_digest(state_data),
                artifact_request,
            )
            stage_name = f"{next_generation:012d}-{commit_id}-{uuid.uuid4().hex}"
            stage = self.staging_dir / stage_name
            final_name = f"generation-{next_generation:012d}-{commit_id}"
            final = self.commits_dir / final_name
            stage.mkdir()
            _write_file_fsync(stage / "state.json", state_data)
            self._hit(failpoint, "after_state_write")
            descriptors: list[dict[str, Any]] = []
            for index, row in enumerate(transition.artifacts, 1):
                destination = stage / "artifacts" / row.relative_path
                _write_file_fsync(destination, row.data)
                descriptors.append(dict(row.descriptor))
                self._hit(failpoint, f"after_artifact_write:{index}")
            manifest = {
                "schema_version": "1.0.0",
                "commit_id": commit_id,
                "generation": next_generation,
                "prior_generation": expected_generation,
                "target_id": self.target_id,
                "run_id": self.run_id,
                "created_at": utc_now(),
                "idempotency_key": idempotency_key,
                "request_digest": request_digest,
                "state_digest": transition.state_digest,
                "state_semantic_digest": transition.state_semantic_digest,
                "artifacts": descriptors,
            }
            manifest_data = _json_bytes(manifest)
            manifest_digest = bytes_digest(manifest_data)
            _write_file_fsync(stage / "manifest.json", manifest_data)
            self._hit(failpoint, "after_manifest_write")
            # Persist nested directory entries before exposing the staged tree.
            for directory, _, _ in os.walk(stage, topdown=False):
                fsync_directory(Path(directory))
            journal = {
                "schema_version": "1.0.0",
                "transaction_id": commit_id,
                "target_id": self.target_id,
                "run_id": self.run_id,
                "generation": next_generation,
                "stage_directory": stage_name,
                "commit_directory": final_name,
                "manifest_digest": manifest_digest,
                "status": "prepared",
                "prepared_at": utc_now(),
            }
            journal_path = self.journal_dir / f"{commit_id}.json"
            self._atomic_write_path(journal_path, _json_bytes(journal))
            self._hit(failpoint, "after_journal_prepared")
            with self._open_anchored_directory(self.staging_dir) as staging_fd, self._open_anchored_directory(
                self.commits_dir
            ) as commits_fd:
                os.replace(
                    stage_name,
                    final_name,
                    src_dir_fd=staging_fd,
                    dst_dir_fd=commits_fd,
                )
                os.fsync(staging_fd)
                os.fsync(commits_fd)
            self._hit(failpoint, "after_commit_rename")
            pointer = self._pointer_for(
                final,
                manifest,
                manifest_digest=manifest_digest,
            )
            self._atomic_write_path(self.pointer_path, _json_bytes(pointer))
            self._hit(failpoint, "after_pointer_write")
            journal["status"] = "committed"
            journal["committed_at"] = utc_now()
            self._atomic_write_path(journal_path, _json_bytes(journal))
            self._hit(failpoint, "after_journal_complete")
            return CommitResult(
                generation=next_generation,
                commit_id=commit_id,
                commit_path=final,
                manifest_digest=manifest_digest,
            )

    def rollback(
        self,
        *,
        expected_generation: int,
        to_generation: int,
        reason: str,
        idempotency_key: str,
    ) -> CommitResult:
        """Rollback by committing a new generation that records its provenance."""

        if not reason.strip():
            raise ContractError("rollback reason is required")
        prior = self.read_state(to_generation)
        if prior is None:
            raise ContractError("cannot roll back to generation zero without an explicit initial state")
        state = copy.deepcopy(prior)
        state["generation"] = expected_generation + 1
        state["rollback"] = {
            "restored_from_generation": to_generation,
            "replaced_generation": expected_generation,
            "reason": reason,
        }
        request_digest = canonical_digest(
            {"to_generation": to_generation, "expected_generation": expected_generation, "reason": reason}
        )
        return self.commit(
            expected_generation=expected_generation,
            state=state,
            artifacts=(),
            idempotency_key=idempotency_key,
            request_digest=request_digest,
        )

    def store_branch_result(
        self,
        *,
        wave_id: str,
        branch_id: str,
        invocation_id: str,
        frozen_inputs_digest: str,
        status: str,
        payload: Mapping[str, Any],
    ) -> Path:
        """Persist a content-addressed branch result without touching shared state."""

        for value, field in ((wave_id, "wave_id"), (branch_id, "branch_id"), (invocation_id, "invocation_id")):
            validate_identifier(value, field)
        if status not in {"validated", "failed", "timed_out"}:
            raise ContractError("branch result status must be validated, failed, or timed_out")
        envelope = {
            "schema_version": "1.0.0",
            "identity": {"target_id": self.target_id, "run_id": self.run_id, "branch_id": branch_id},
            "wave_id": wave_id,
            "invocation_id": invocation_id,
            "frozen_inputs_digest": frozen_inputs_digest,
            "status": status,
            "payload": copy.deepcopy(dict(payload)),
        }
        digest = canonical_digest(envelope).removeprefix("sha256:")
        path = self.branch_results_dir / wave_id / branch_id / f"{invocation_id}-{digest}.json"
        with self.lock():
            path.parent.mkdir(parents=True, exist_ok=True)
            data = _json_bytes(envelope)
            if path.exists() and path.read_bytes() != data:
                raise StateCorruptionError(f"content-addressed branch result collision: {path}")
            if not path.exists():
                _atomic_write(path, data)
        return path

    def read_branch_result(
        self, path: Path, *, wave_id: str, branch_id: str, frozen_inputs_digest: str
    ) -> dict[str, Any]:
        """Read a branch result only under its exact frozen namespace."""

        resolved = path.resolve()
        expected_root = (self.branch_results_dir / wave_id / branch_id).resolve()
        try:
            resolved.relative_to(expected_root)
        except ValueError as exc:
            raise ContractError("worker attempted sibling/global namespace read") from exc
        payload = self._load_json(resolved)
        identity = payload.get("identity", {})
        if identity != {"target_id": self.target_id, "run_id": self.run_id, "branch_id": branch_id}:
            raise ContractError("branch result identity mismatch")
        if payload.get("wave_id") != wave_id or payload.get("frozen_inputs_digest") != frozen_inputs_digest:
            raise ContractError("branch result does not match frozen wave inputs")
        return payload

    def plan_retry(
        self, *, wave_id: str, branch_ids: Sequence[str], frozen_inputs_digest: str
    ) -> list[str]:
        """Retry only failed/missing branches unless the wave inputs changed."""

        retry: list[str] = []
        for branch_id in branch_ids:
            validate_identifier(branch_id, "branch_id")
            paths = sorted((self.branch_results_dir / wave_id / branch_id).glob("*.json"))
            matching: list[dict[str, Any]] = []
            changed_inputs = False
            for path in paths:
                payload = self._load_json(path)
                if payload.get("frozen_inputs_digest") == frozen_inputs_digest:
                    matching.append(payload)
                else:
                    changed_inputs = True
            if changed_inputs and not matching:
                retry.append(branch_id)
            elif not any(result.get("status") == "validated" for result in matching):
                retry.append(branch_id)
        return retry
