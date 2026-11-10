# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
# SPDX-License-Identifier: MIT
"""Immutable source snapshots and a subprocess entrypoint for native research.

The scientific implementation remains in the existing domain-package adapter.
This module supplies a confined source snapshot and persists the exact verified
workspace for later invocations. A checkpoint never bypasses canonical gates.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import os
from pathlib import Path, PurePosixPath
import shutil
import stat
import tempfile

from .provider import HostedServices

SOURCE_MANIFEST = ".abducer-source.json"
TARGETS = {"p-vs-np-target", "yang-mills-existence-and-mass-gap-target"}
PYTHON_LAUNCHERS = (
    ".venv/bin/python",
    ".venv/bin/python3",
    ".venv-pmp/bin/python",
    ".venv-pmp/bin/python3",
)
_PYTHON_LAUNCHER = b"""#!/bin/sh
# Generated Abducer compatibility entrypoint; no virtual environment is copied.
# The operator bootstrap or native supervisor supplies the managed interpreter.
case "${PYTHON-}" in
    /*) ;;
    *) printf '%s\\n' 'Abducer requires PYTHON to name an absolute managed interpreter.' >&2; exit 126 ;;
esac
if [ ! -f "$PYTHON" ] || [ ! -x "$PYTHON" ] || [ "$PYTHON" -ef "$0" ]; then
    printf '%s\\n' 'Abducer PYTHON must be executable and must not point to this launcher.' >&2
    exit 126
fi
exec "$PYTHON" "$@"
"""


def json_bytes(value) -> bytes:
    return (json.dumps(value, sort_keys=True, allow_nan=False) + "\n").encode()


def digest_file(path: Path) -> str:
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def confined(root: Path, value: str) -> Path:
    """Reject noncanonical paths, symlinks and escapes before reading bytes."""
    if not isinstance(value, str) or not value or "\\" in value:
        raise ValueError("Invalid confined path")
    path = PurePosixPath(value)
    if path.is_absolute() or any(p in {"", ".", ".."} for p in value.split("/")):
        raise ValueError("Invalid confined path")
    candidate = root.joinpath(*path.parts)
    for part in (candidate, *candidate.parents):
        if part == root.parent:
            break
        if part.is_symlink():
            raise ValueError("Symlinks are not allowed in research storage")
    candidate.resolve().relative_to(root.resolve())
    return candidate


def tree_manifest(root: Path, *, exclude_manifest: bool = False) -> dict:
    """Record all regular workspace bytes, refusing links and device files."""
    rows = {}
    for path in sorted(root.rglob("*")):
        relative = path.relative_to(root).as_posix()
        if exclude_manifest and relative == SOURCE_MANIFEST:
            continue
        info = path.lstat()
        if stat.S_ISLNK(info.st_mode):
            raise ValueError("Snapshot contains a symlink")
        if stat.S_ISDIR(info.st_mode):
            continue
        if not stat.S_ISREG(info.st_mode):
            raise ValueError("Snapshot contains a nonregular file")
        rows[relative] = {"sha256": digest_file(path), "size": info.st_size}
    return rows


def install_python_launchers(snapshot: Path) -> dict[str, dict]:
    """Add interpreter aliases to a fresh, unpublished POSIX source snapshot.

    Historical skill commands can retain their authored environment paths while
    using the operator-selected Python. These are regular, hashable launchers,
    not copied virtual environments. Callers must reseal their snapshot after
    adding them; this helper must never target an active immutable deployment.
    Every path is checked before writing so an authored file is never replaced.
    """
    if snapshot.is_symlink():
        raise ValueError("Snapshot destination must not be a symlink")
    snapshot = snapshot.resolve(strict=True)
    if not snapshot.is_dir():
        raise ValueError("Snapshot destination must be a directory")
    destinations = {}
    for relative in PYTHON_LAUNCHERS:
        path = confined(snapshot, relative)
        if path.exists():
            raise ValueError(
                "Python launcher collides with a snapshot file: " + relative
            )
        for parent in path.parents:
            if parent == snapshot:
                break
            if parent.exists() and not parent.is_dir():
                raise ValueError("Python launcher parent is not a directory")
        destinations[relative] = path
    descriptors = {}
    for relative, path in destinations.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        # Exclusive creation also refuses a collision arising after preflight.
        with path.open("xb") as stream:
            stream.write(_PYTHON_LAUNCHER)
        path.chmod(0o755)
        descriptors[relative] = {
            "sha256": digest_file(path),
            "size": len(_PYTHON_LAUNCHER),
        }
    return descriptors


def build_snapshot(source_root: Path, output: Path) -> dict:
    """Publish the existing exporter's explicit source selection atomically.

    The source must be a Git checkout; unrelated untracked files, environments,
    credentials and unselected runs never enter the snapshot. Installed worker
    images use the resulting manifest and do not need Git at runtime.
    """
    from integrations.domain_package.export import excluded, source_inventory

    source_root = source_root.resolve(strict=True)
    output = output.absolute()
    if output.exists():
        raise ValueError("Snapshot destination already exists")
    selected, revision = source_inventory(source_root)
    # Domain export omits the client plugin; the hosted catalog needs only its
    # generated metadata, not checkout resolvers or host configuration files.
    additions = [
        "plugins/abducer/source-skills.json",
        "plugins/abducer/workflows.json",
        # Explicit authored guides may be deployed before their first commit.
        "docs/integrations/chatgpt-native-execution.md",
        "docs/integrations/chatgpt-hook-fidelity.md",
    ]
    paths = sorted(
        set(selected) | {p for p in additions if (source_root / p).is_file()}
    )
    if set(paths).intersection(PYTHON_LAUNCHERS):
        raise ValueError("Generated Python launchers collide with authored sources")
    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(
        prefix="abducer-source-", dir=output.parent
    ) as temporary:
        snapshot = Path(temporary) / "source"
        snapshot.mkdir()
        descriptors = {}
        for relative in paths:
            if excluded(relative):
                raise ValueError("Excluded path in source selection")
            source = confined(source_root, relative)
            before = source.stat()
            if not stat.S_ISREG(before.st_mode):
                raise ValueError("Source selection must contain regular files")
            destination = snapshot / relative
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source, destination)
            after = source.stat()
            if (before.st_size, before.st_mtime_ns, before.st_ctime_ns) != (
                after.st_size,
                after.st_mtime_ns,
                after.st_ctime_ns,
            ):
                raise ValueError("Source changed while creating the snapshot")
            descriptors[relative] = {
                "sha256": digest_file(destination),
                "size": before.st_size,
            }
        # Compare the selector's own inventory. An explicitly allowed guide may
        # already be tracked, so subtracting additions can hide real membership.
        if source_inventory(source_root) != (selected, revision):
            raise ValueError("Source inventory changed during snapshot creation")
        launchers = install_python_launchers(snapshot)
        descriptors.update(launchers)
        manifest = {
            "version": 1,
            "revision": revision,
            "python_launchers": list(launchers),
            "files": descriptors,
            "content_sha256": hashlib.sha256(json_bytes(descriptors)).hexdigest(),
        }
        (snapshot / SOURCE_MANIFEST).write_bytes(json_bytes(manifest))
        snapshot.rename(output)
    return manifest


def verify_snapshot(root: Path) -> dict:
    """Require a declared immutable release rather than copying a checkout."""
    root = root.resolve(strict=True)
    manifest_path = confined(root, SOURCE_MANIFEST)
    if not manifest_path.is_file():
        raise ValueError("Build a runtime source snapshot before starting workers")
    manifest = json.loads(manifest_path.read_bytes())
    actual = tree_manifest(root, exclude_manifest=True)
    if (
        manifest.get("version") != 1
        or actual != manifest.get("files")
        or hashlib.sha256(json_bytes(actual)).hexdigest()
        != manifest.get("content_sha256")
    ):
        raise ValueError("Runtime source snapshot differs from its release manifest")
    return manifest


def verify_checkpoint(
    data_root: Path, checkpoint: dict, *, release: str, target_id: str
) -> Path:
    """Reopen a successful immutable workspace and its recorded inventory."""
    if (
        checkpoint.get("source_release") != release
        or checkpoint.get("binding", {}).get("target_id") != target_id
    ):
        raise ValueError("Checkpoint belongs to another release or target")
    workspace = confined(data_root, checkpoint["workspace_relative_path"])
    manifest_path = confined(data_root, checkpoint["workspace_manifest_path"])
    if digest_file(manifest_path) != checkpoint["workspace_manifest_sha256"]:
        raise ValueError("Checkpoint manifest changed")
    if tree_manifest(workspace) != json.loads(manifest_path.read_bytes()):
        raise ValueError("Checkpoint workspace changed")
    return workspace


def run_native(request: dict, *, services=None) -> dict:
    """Run prepare/execute/verify from the preserved native adapter.

    This function is only called in a fresh child process because the existing
    adapter loads source-bound Python modules. The worker handles cancellation,
    wall-clock enforcement and lease loss outside that process.
    """
    job = request["job"]
    if job["workflow_id"] != "discovery_marathon_loop":
        raise ValueError("Only the registered native discovery workflow is executable")
    inputs = job["inputs"]
    target = inputs["target_id"]
    if target not in TARGETS:
        raise ValueError("Target is not registered for native initialization")
    data_root = Path(request["data_root"]).resolve(strict=True)
    output = confined(data_root, request["output_relative_path"])
    output.mkdir(parents=True, exist_ok=False, mode=0o700)
    source_root = Path(request["source_root"]).resolve(strict=True)
    release_manifest = verify_snapshot(source_root)
    if job.get("runtime_source_sha256") != release_manifest["content_sha256"]:
        raise ValueError("Runtime differs from the exact prepared source snapshot")
    parent = job.get("parent_checkpoint")
    if parent:
        if parent.get("runtime_source_sha256") != release_manifest["content_sha256"]:
            raise ValueError(
                "Checkpoint runtime release changed; explicit migration is required"
            )
        original = verify_checkpoint(
            data_root, parent, release=job["release"], target_id=target
        )
        binding = dict(parent["binding"])
        binding.pop("initialize", None)
        initial_cycles = parent["cycle_count"]
    else:
        original = source_root
        binding = {"target_id": target, "run_id": "new", "initialize": True}
        initial_cycles = 0
    staging = output / "input"
    source = staging / "runtime"
    source.parent.mkdir()
    shutil.copytree(original, source)
    (staging / "marathon-binding.json").write_bytes(
        json_bytes({"version": 2, "runs": [binding]})
    )
    module_path = source / "integrations/domain_package/marathon_runtime.py"
    spec = importlib.util.spec_from_file_location(
        "abducer_hosted_native_adapter", module_path
    )
    if spec is None or spec.loader is None:
        raise ValueError("Native adapter cannot be loaded from the source snapshot")
    adapter = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(adapter)
    if services is None:
        events = output / "events.jsonl"

        def event(kind, payload):
            with events.open("a") as stream:
                stream.write(json.dumps({"kind": kind, "payload": payload}) + "\n")

        provider = os.environ.get("ABDUCER_MODEL_PROVIDER", "api")
        if provider == "chatgpt":
            from .chatgpt_model import ChatGPTServices
            from .store import Store

            services = ChatGPTServices(
                store=Store(
                    request.get("database_path", data_root / "service.sqlite3")
                ),
                job_id=job["id"],
                worker_id=job["worker_id"],
                budget=job["budget"],
                allow_public_network=inputs.get("allow_public_network") is True,
                event=event,
            )
        elif provider == "api":
            services = HostedServices(
                job["budget"],
                allow_public_network=inputs.get("allow_public_network") is True,
                event=event,
            )
        else:
            raise ValueError("Unknown configured model provider")
    prepared = adapter.prepare(
        workflow_id=job["workflow_id"],
        inputs={"target_id": target, "run_id": binding["run_id"]},
        mode="live",
        run_id=job["id"],
        run_root=output,
        network_authority=inputs.get("allow_public_network") is True,
        public_fetch=services.public_fetch,
        on_reasoning=lambda **kwargs: None,
    )
    state = prepared["state"]
    if state["initial_cycle_count"] != initial_cycles:
        raise ValueError("Checkpoint cycle count differs from native state")
    if os.environ.get("ABDUCER_NATIVE_HOOKS_ENABLED", "false").lower() == "true":
        from .hooked_marathon import run_hooked

        execution = run_hooked(
            adapter,
            state=state,
            services=services,
            source_root=source_root,
            prompt="Run the approved bounded Discovery Marathon for " + target,
        )
    else:
        execution = adapter.execute(state=state, services=services)
    verified = adapter.verify(state=state, execution=execution, services=services)[
        "result"
    ]
    if (
        verified["report_verification"].get("status") != "passed"
        or verified["report_verification"].get("scientific_truth_verified") is not False
    ):
        raise ValueError("Native output did not retain its scoped verification")
    # Input is disposable; the committed workspace is the exact output from
    # this invocation, not the original export or a report-only reconstruction.
    shutil.rmtree(staging)
    workspace = output / "workspace"
    manifest_path = output / "workspace-manifest.json"
    manifest_path.write_bytes(json_bytes(tree_manifest(workspace)))
    checkpoint = {
        "source_release": job["release"],
        "runtime_source_sha256": release_manifest["content_sha256"],
        "workspace_relative_path": workspace.relative_to(data_root).as_posix(),
        "workspace_manifest_path": manifest_path.relative_to(data_root).as_posix(),
        "workspace_manifest_sha256": digest_file(manifest_path),
        "binding": state["binding"],
        "cycle_count": execution["cycle_count"],
    }
    artifacts = []
    for name, descriptor in verified["structured_value"]["report_artifacts"].items():
        path = confined(output, name)
        if digest_file(path) != descriptor["sha256"]:
            raise ValueError("Verified report changed before publication")
        artifacts.append(
            {
                "id": hashlib.sha256((job["id"] + "/" + name).encode()).hexdigest(),
                "name": name,
                "relative_path": path.relative_to(data_root).as_posix(),
                "sha256": descriptor["sha256"],
                "media_type": descriptor["media_type"],
                "size": path.stat().st_size,
            }
        )
    result = {
        "structured_value": verified["structured_value"],
        "report_verification": verified["report_verification"],
        "model_calls": getattr(services, "calls", None),
    }
    if "native_hook_coverage" in execution:
        result["native_hook_coverage"] = execution["native_hook_coverage"]
    return {"result": result, "artifacts": artifacts, "checkpoint": checkpoint}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    snapshot = sub.add_parser("snapshot")
    snapshot.add_argument("--source-root", type=Path, required=True)
    snapshot.add_argument("--output", type=Path, required=True)
    run = sub.add_parser("run")
    run.add_argument("--request", type=Path, required=True)
    run.add_argument("--response", type=Path, required=True)
    args = parser.parse_args()
    if args.command == "snapshot":
        manifest = build_snapshot(args.source_root, args.output)
        print(
            json.dumps(
                {
                    "source_revision": manifest["revision"],
                    "files": len(manifest["files"]),
                    "sha256": manifest["content_sha256"],
                }
            )
        )
        return 0
    try:
        response = run_native(json.loads(args.request.read_bytes()))
        args.response.write_bytes(json_bytes(response))
        return 0
    except Exception as exc:
        # Native validation messages may contain research content. Keep them in
        # private diagnostics only; the parent publishes a bounded failure type.
        args.response.write_bytes(
            json_bytes({"error_type": type(exc).__name__, "error": str(exc)[:4000]})
        )
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
