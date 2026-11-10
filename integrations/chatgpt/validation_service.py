# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
# SPDX-License-Identifier: MIT
"""Owned, bounded conceptual-artifact validation through the native validator.

An operation is a private validation receipt, not a research checkpoint. The
child verifies the immutable source, copies only required original dependencies
and the submitted map into a disposable workspace, and executes the existing
native hook/validator adapter. No example map or missing input is synthesized.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import signal
import subprocess
import sys
import time
from uuid import uuid4

from .native_steps import (
    CONCEPTUAL_VALIDATOR_SOURCES,
    _confined,
    validate_hypothesis_map,
)
from .runtime import verify_snapshot
from .store import AccessDenied

MAX_CONTENT_CHARS = 48000
MAX_PROJECT_OPERATIONS = 50
MAX_ACCOUNT_OPERATIONS = 200
MAX_SOURCE_BYTES = 32 * 1024 * 1024
OPERATION_DEADLINE_SECONDS = 20
MAX_RESULT_BYTES = 128 * 1024
_OPERATION_ID = re.compile(r"[a-f0-9]{32}\Z")


def _strict_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("Duplicate JSON member")
        result[key] = value
    return result


def _parse_content(content):
    if not isinstance(content, str) or not 1 <= len(content) <= MAX_CONTENT_CHARS:
        raise ValueError("Conceptual content must contain 1–48000 JSON characters")
    try:
        value = json.loads(
            content,
            object_pairs_hook=_strict_object,
            parse_constant=lambda _: (_ for _ in ()).throw(
                ValueError("Non-JSON number")
            ),
        )
    except (json.JSONDecodeError, RecursionError) as error:
        raise ValueError("Conceptual content must be a bounded JSON object") from error
    if not isinstance(value, dict):
        raise ValueError("Conceptual content must be a JSON object")
    return value


def _table(db):
    db.execute("""
        CREATE TABLE IF NOT EXISTS conceptual_validations(
            id TEXT PRIMARY KEY, subject TEXT NOT NULL, project_id TEXT NOT NULL REFERENCES projects(id),
            created REAL NOT NULL, updated REAL NOT NULL, status TEXT NOT NULL,
            artifact_sha256 TEXT NOT NULL, receipt TEXT
        )
    """)
    db.execute(
        "CREATE INDEX IF NOT EXISTS conceptual_validations_project ON conceptual_validations(project_id,created)"
    )


def _reserve(service, subject, project_id, identity, artifact_sha256):
    """Check role and admission in the same short database transaction."""
    now = time.time()
    with service.store.connection() as db:
        db.execute("PRAGMA busy_timeout=1000")
        db.execute("BEGIN IMMEDIATE")
        service.store._project(db, subject, project_id, True)
        _table(db)
        # A crashed caller cannot retain a permanent admission lock. Its row
        # remains as a failed receipt record; it is never replayed automatically.
        db.execute(
            "UPDATE conceptual_validations SET status='interrupted',updated=? WHERE status='running' AND updated<?",
            (now, now - 60),
        )
        project_count = db.execute(
            "SELECT COUNT(*) FROM conceptual_validations WHERE project_id=?",
            (project_id,),
        ).fetchone()[0]
        account_count = db.execute(
            "SELECT COUNT(*) FROM conceptual_validations WHERE subject=?", (subject,)
        ).fetchone()[0]
        active_project = db.execute(
            "SELECT COUNT(*) FROM conceptual_validations WHERE project_id=? AND status='running'",
            (project_id,),
        ).fetchone()[0]
        active_account = db.execute(
            "SELECT COUNT(*) FROM conceptual_validations WHERE subject=? AND status='running'",
            (subject,),
        ).fetchone()[0]
        if (
            project_count >= MAX_PROJECT_OPERATIONS
            or account_count >= MAX_ACCOUNT_OPERATIONS
        ):
            raise ValueError("Conceptual validation storage quota reached")
        if active_project or active_account >= 2:
            raise ValueError("Conceptual validation already active")
        db.execute(
            "INSERT INTO conceptual_validations VALUES(?,?,?,?,?,?,?,NULL)",
            (identity, subject, project_id, now, now, "running", artifact_sha256),
        )


def _sanitize(value, roots):
    """Bound diagnostics and replace internal absolute paths before publication."""
    if isinstance(value, str):
        for root in roots:
            value = value.replace(str(root), "[workspace]")
        value = re.sub(
            r"(?<![A-Za-z0-9])/[^\s\"'<>:]+(?:/[^\s\"'<>:]*)+", "[path]", value
        )
        return value[:16000]
    if isinstance(value, list):
        return [_sanitize(item, roots) for item in value]
    if isinstance(value, dict):
        return {key: _sanitize(item, roots) for key, item in value.items()}
    return value


def _environment():
    """The validator gets no identity, model or bridge credentials."""
    result = {
        name: os.environ[name]
        for name in ("PATH", "LANG", "LC_ALL")
        if name in os.environ
    }
    result.update(
        PYTHONDONTWRITEBYTECODE="1", PYTHONPATH=str(Path(__file__).resolve().parents[2])
    )
    return result


def validate_conceptual(service, subject: str, project_id: str, content: str) -> dict:
    """Validate an owned map within a bounded per-operation process workspace."""
    started = time.monotonic()
    service.store.project(subject, project_id, write=True)
    _parse_content(content)
    raw = content.encode("utf-8")
    identity, digest = uuid4().hex, hashlib.sha256(raw).hexdigest()
    _reserve(service, subject, project_id, identity, digest)
    root = Path(service.config.data_root).resolve()
    operation = _confined(root, "conceptual-validations/" + identity)
    operation.mkdir(parents=True, mode=0o700)
    input_file = operation / "input.json"
    input_file.write_bytes(raw)
    input_file.chmod(0o600)
    request_file = operation / "request.json"
    source_root = Path(service.config.repository_root).resolve(strict=True)
    request_file.write_text(
        json.dumps(
            {
                "source_root": str(source_root),
                "operation_root": str(operation),
                "expected_source_sha256": getattr(
                    service, "runtime_source_sha256", None
                ),
                "artifact_sha256": digest,
            }
        )
    )
    request_file.chmod(0o600)
    receipt = {
        "receipt_id": identity,
        "project_id": project_id,
        "workflow_id": "conceptual_hypothesis_exploration_workflow",
        "operation": "validate_hypothesis_map",
        "artifact_sha256": digest,
        "source_release": service.catalog.release,
        "native_workflow_executed": False,
        "scientific_truth_verified": False,
    }
    process = None
    try:
        remaining = OPERATION_DEADLINE_SECONDS - (time.monotonic() - started) - 1
        if remaining <= 0:
            raise subprocess.TimeoutExpired("native conceptual validation", 0)
        process = subprocess.Popen(
            [
                sys.executable,
                "-m",
                "integrations.chatgpt.validation_service",
                "--child",
                str(request_file),
            ],
            cwd=operation,
            env=_environment(),
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            start_new_session=True,
        )
        stdout, stderr = process.communicate(timeout=remaining)
        if process.returncode or len(stdout) > MAX_RESULT_BYTES:
            receipt.update(
                status="error",
                error="Native validation process failed",
                diagnostics=stderr.decode("utf-8", errors="replace")[:4000],
            )
        else:
            child = json.loads(stdout)
            if not isinstance(child, dict) or child.get("artifact_sha256") != digest:
                raise ValueError("Native validation result binding mismatch")
            receipt.update(child)
    except subprocess.TimeoutExpired:
        if process is not None:
            os.killpg(process.pid, signal.SIGKILL)
            process.communicate()
        receipt.update(
            status="timed_out",
            error="Native validation exceeded its operation deadline",
        )
    except (OSError, ValueError, json.JSONDecodeError):
        receipt.update(
            status="error", error="Native validation could not produce a bound receipt"
        )
    finally:
        # Descendant processes must not survive a leader's exit and mutate
        # artifacts after publication. A native validation never continues.
        if process is not None:
            try:
                os.killpg(process.pid, signal.SIGKILL)
            except ProcessLookupError:
                pass
        shutil.rmtree(operation / "workspace", ignore_errors=True)
        request_file.unlink(missing_ok=True)
    receipt = _sanitize(
        receipt, [operation, source_root, Path(__file__).resolve().parents[2]]
    )
    receipt["elapsed_seconds"] = round(time.monotonic() - started, 3)
    encoded = json.dumps(receipt, sort_keys=True, allow_nan=False)
    if len(encoded.encode()) > MAX_RESULT_BYTES:
        raise ValueError("Native validation receipt exceeds result budget")
    (operation / "receipt.json").write_text(encoded + "\n")
    (operation / "receipt.json").chmod(0o600)
    with service.store.connection() as db:
        db.execute("PRAGMA busy_timeout=1000")
        db.execute("BEGIN IMMEDIATE")
        service.store._project(db, subject, project_id, True)
        changed = db.execute(
            "UPDATE conceptual_validations SET status=?,updated=?,receipt=? WHERE id=? AND subject=? AND project_id=? AND status='running'",
            (receipt["status"], time.time(), encoded, identity, subject, project_id),
        ).rowcount
        if changed != 1:
            raise ValueError("Validation operation lost its active record")
    return receipt


def list_validations(service, subject: str, project_id: str, limit: int = 20) -> dict:
    """Recover receipt identities without returning submitted maps or diagnostics."""
    if type(limit) is not int or not 1 <= limit <= 50:
        raise ValueError("Validation receipt limit must be 1–50")
    with service.store.connection() as db:
        service.store._project(db, subject, project_id)
        _table(db)
        rows = db.execute(
            "SELECT id AS receipt_id,status,created,artifact_sha256 FROM conceptual_validations WHERE subject=? AND project_id=? ORDER BY created DESC,id DESC LIMIT ?",
            (subject, project_id, limit),
        ).fetchall()
        return {"receipts": [dict(row) for row in rows]}


def get_validation(service, subject: str, project_id: str, receipt_id: str) -> dict:
    """Retrieve only this caller's validation receipt in an accessible project."""
    if not isinstance(receipt_id, str) or not _OPERATION_ID.fullmatch(receipt_id):
        raise AccessDenied("Validation receipt is unavailable")
    with service.store.connection() as db:
        service.store._project(db, subject, project_id)
        _table(db)
        row = db.execute(
            "SELECT receipt,status,artifact_sha256 FROM conceptual_validations WHERE id=? AND subject=? AND project_id=?",
            (receipt_id, subject, project_id),
        ).fetchone()
        if row is None:
            raise AccessDenied("Validation receipt is unavailable")
        return (
            json.loads(row["receipt"])
            if row["receipt"]
            else {
                "receipt_id": receipt_id,
                "project_id": project_id,
                "status": row["status"],
                "artifact_sha256": row["artifact_sha256"],
            }
        )


def _child(request: dict) -> dict:
    """Verify the release and invoke original validation in the disposable clone."""
    source = Path(request["source_root"]).resolve(strict=True)
    operation = Path(request["operation_root"]).resolve(strict=True)
    raw = (operation / "input.json").read_bytes()
    digest = hashlib.sha256(raw).hexdigest()
    if digest != request["artifact_sha256"]:
        raise ValueError("Validation input changed before execution")
    content = _parse_content(raw.decode("utf-8"))
    manifest = verify_snapshot(source)
    if (
        request.get("expected_source_sha256")
        and manifest["content_sha256"] != request["expected_source_sha256"]
    ):
        raise ValueError("Validation source differs from the service release")
    paths = set(CONCEPTUAL_VALIDATOR_SOURCES) | {"hooks/hooks.json"}
    paths.update(
        name
        for name in manifest["files"]
        if name.startswith("hooks/scripts/") and name.endswith(".py")
    )
    paths.update(
        name
        for name in manifest["files"]
        if name.startswith("registry/tasks/") and name.endswith("/task_registry.json")
    )
    for field in ("kb_path", "source_graph"):
        if field in content:
            dependency = content[field]
            _confined(source, dependency)
            if dependency not in manifest["files"]:
                raise ValueError(
                    "Referenced research input is absent from the verified source snapshot"
                )
            paths.add(dependency)
    if any(path not in manifest["files"] for path in paths):
        raise ValueError(
            "A native validator dependency is absent from the verified source snapshot"
        )
    if sum(manifest["files"][path]["size"] for path in paths) > MAX_SOURCE_BYTES:
        raise ValueError(
            "Native validation dependencies exceed the bounded workspace budget"
        )
    workspace = operation / "workspace"
    workspace.mkdir(mode=0o700)
    for relative in sorted(paths):
        original = _confined(source, relative)
        destination = _confined(workspace, relative)
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(original, destination)
        if (
            hashlib.sha256(destination.read_bytes()).hexdigest()
            != manifest["files"][relative]["sha256"]
        ):
            raise ValueError("Source changed while copying validator dependencies")
    artifact = _confined(workspace, "artifacts/submitted/hypothesis-map.json")
    artifact.parent.mkdir(parents=True, exist_ok=True)
    artifact.write_bytes(raw)
    result = validate_hypothesis_map(
        source_root=source,
        workspace=workspace,
        map_path="artifacts/submitted/hypothesis-map.json",
        timeout_seconds=15,
    )
    result["source_snapshot_sha256"] = manifest["content_sha256"]
    result["source_dependencies"] = [
        {"path": path, "sha256": manifest["files"][path]["sha256"]}
        for path in sorted(paths)
    ]
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--child", type=Path, required=True)
    args = parser.parse_args()
    request = json.loads(args.child.read_text())
    try:
        result = _child(request)
    except Exception as error:
        result = {
            "status": "error",
            "artifact_sha256": request.get("artifact_sha256"),
            "error": str(error)[:2000],
            "native_workflow_executed": False,
            "scientific_truth_verified": False,
        }
    print(json.dumps(result, sort_keys=True, allow_nan=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
