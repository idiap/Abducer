#!/usr/bin/env python3
# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
"""Opt-in, fixed-route maintenance CLI adapter with native public trace sidecars.

The subprocess remains the behavior owner. Byte streams and return codes are
preserved; optional trace failures never change its outcome. Explicit replay is
stricter: only a verified completed receipt may be returned, never re-executed.
Receipts describe process execution, not scientific or promotion authority.
"""
from __future__ import annotations

import argparse
import base64
import fcntl
import hashlib
import json
import os
from pathlib import Path
import re
import signal
import threading
import subprocess
import sys
import tempfile
from dataclasses import asdict, dataclass
from uuid import uuid4

ROOT = Path(__file__).resolve().parents[2]
REGISTRY = ROOT / "proj_skills/repository_adoption_operations.json"
OPERATION = "validate-project-skills"
IMPLEMENTATION = "proj_skills/scripts/validate_proj_skills.py"


class ReplayError(ValueError):
    """An invocation cannot safely be replayed or reused."""


@dataclass(frozen=True)
class InvocationContext:
    """Host-issued identity; retries increment attempt, delivery replay retains it."""

    run_id: str
    invocation_id: str
    attempt: int = 1
    parent_run_id: str | None = None
    parent_event_id: str | None = None

    def __post_init__(self):
        if not isinstance(self.run_id, str) or not isinstance(self.invocation_id, str):
            raise ValueError("run_id and invocation_id must be strings")
        for value in (self.run_id, self.invocation_id, self.parent_run_id, self.parent_event_id):
            if value is not None and (not isinstance(value, str) or not re.fullmatch(r"[A-Za-z0-9._:-]+", value) or value in {".", ".."}):
                raise ValueError("context IDs must be safe nonempty identifiers")
        if type(self.attempt) is not int or self.attempt < 1:
            raise ValueError("attempt must be a positive integer")


def _bytes(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()


def _digest(data):
    return hashlib.sha256(data).hexdigest()


def _write(path, data):
    """Replace a whole artifact atomically; interruption cannot publish partial JSON."""
    fd, name = tempfile.mkstemp(prefix=".pending-", dir=path.parent)
    try:
        with os.fdopen(fd, "wb") as stream:
            stream.write(data)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(name, path)
        directory_fd = os.open(path.parent, os.O_RDONLY)
        try:
            os.fsync(directory_fd)
        finally:
            os.close(directory_fd)
    finally:
        if os.path.exists(name):
            os.unlink(name)


def _resolve(operation_id):
    """Registration enables a reviewed fixed route, never an arbitrary import."""
    registry = json.loads(REGISTRY.read_text())
    rows = [row for row in registry["operations"] if row["operation_id"] == operation_id]
    if (registry["schema_version"] != "abducer.repository-adoption-operations/v1"
            or operation_id != OPERATION or len(rows) != 1
            or rows[0]["implementation"] != IMPLEMENTATION
            or rows[0]["adapter"] != "proj_skills/scripts/repository_adoption_adapter.py"
            or rows[0]["invocation_mode"] != "cli"):
        raise ValueError("operation has no reviewed callable binding")
    return ROOT / IMPLEMENTATION, rows[0]


def _emit(root, request, result_path, result_digest, result):
    """Use native v2 identity/status rules, with portable correlation in control."""
    # Import only for explicitly requested tracing; source CLI needs no installation.
    from importlib.util import module_from_spec, spec_from_file_location
    spec = spec_from_file_location("adoption_native_store", ROOT / "agentic/scripts/public_reasoning_trace_store.py")
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    context = request["context"]
    event = {
        "run_id": context["run_id"], "workflow_id": "repository-adoption-maintenance",
        "workflow_version": "1", "target": OPERATION, "phase": "validation",
        "step_id": context["invocation_id"], "attempt": context["attempt"], "skill": None,
        "execution_kind": "live", "event_family": "exit",
        "idempotency_key": context["invocation_id"],
        "parent_run_id": context["parent_run_id"], "parent_event_id": context["parent_event_id"],
        "artifact_validation_status": "integrity_valid", "claim_epistemic_status": "not_applicable",
        "workflow_disposition": "completed" if result.returncode == 0 else "failed",
        "control": {"operation_id": OPERATION, "invocation_context": context,
                    "request_sha256": _digest(_bytes(request)), "exit_code": result.returncode,
                    "terminal_result": {"path": str(result_path), "sha256": result_digest}},
        "evidence": [{"relation": "supports", "path": str(result_path), "digest": result_digest,
                      "artifact_type": "maintenance-cli-result", "external": True}],
        "authority": {"exercised": [], "absent": ["scientific-validation", "release-promotion"],
                      "prohibitions_checked": ["fixed-reviewed-cli-only"]},
    }
    if context["parent_event_id"] and context["parent_run_id"] in (None, context["run_id"]):
        event["causal_parent_event_ids"] = [context["parent_event_id"]]
    # A host may reuse a scientific run ID while opting into maintenance tracing.
    # Keep the native schema/store implementation, but never share its scientific
    # runs/ directory. Receipts stay at the original location for durable replay.
    event_root = root / "repository-adoption"
    if any(path.is_symlink() for path in (event_root, event_root / "runs", event_root / "runs" / context["run_id"])):
        raise ValueError("maintenance event namespace must not redirect through a symlink")
    module.append_event(event, store_root=event_root)


def _replay(directory, request, command):
    """Verify context and content joins before returning durable original bytes."""
    try:
        manifest = json.loads((directory / "invocation.json").read_bytes())
        if _bytes(manifest["request"]) != _bytes(request) or manifest["status"] != "completed":
            raise ReplayError("context mismatch or invocation has no completed receipt")
        data = (directory / "result.json").read_bytes()
        if _digest(data) != manifest["result_sha256"]:
            raise ReplayError("terminal result digest mismatch")
        payload = json.loads(data)
        if _bytes(payload["request"]) != _bytes(request):
            raise ReplayError("terminal result belongs to another invocation")
        if type(payload["returncode"]) is not int:
            raise ReplayError("invalid return code")
        return subprocess.CompletedProcess(command, payload["returncode"],
            base64.b64decode(payload["stdout_base64"], validate=True),
            base64.b64decode(payload["stderr_base64"], validate=True))
    except (OSError, KeyError, ValueError, TypeError) as exc:
        raise ReplayError(f"replay rejected: {exc}") from exc


class _Termination(BaseException):
    """Carry an external signal through child cleanup before preserving termination."""

    def __init__(self, signum):
        self.signum = signum


def _execute(command, *, cwd=None):
    """Own the child lifetime, including a host terminating only the adapter PID."""
    def interrupted(signum, _frame):
        raise _Termination(signum)

    previous = {}
    process = None
    try:
        # Only the main thread can register handlers. Leave host custom handlers
        # authoritative; ordinary CLI termination must not orphan the validator.
        if threading.current_thread() is threading.main_thread():
            for signum in (signal.SIGTERM, signal.SIGHUP):
                if signal.getsignal(signum) == signal.SIG_DFL:
                    previous[signum] = signal.getsignal(signum)
                    signal.signal(signum, interrupted)
        process = subprocess.Popen(command, cwd=cwd, stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE, start_new_session=True)
        stdout, stderr = process.communicate()
        return subprocess.CompletedProcess(command, process.returncode, stdout, stderr)
    except BaseException as exc:
        if process is not None and process.poll() is None:
            try:
                os.killpg(process.pid, signal.SIGTERM)
                try:
                    process.communicate(timeout=1)
                except subprocess.TimeoutExpired:
                    os.killpg(process.pid, signal.SIGKILL)
                    process.communicate()
            except Exception:
                # Cleanup races must not replace the owner's original exception.
                pass
        if isinstance(exc, _Termination):
            signal.signal(exc.signum, signal.SIG_DFL)
            os.kill(os.getpid(), exc.signum)
        raise
    finally:
        for signum, handler in previous.items():
            signal.signal(signum, handler)


def invoke(operation_id: str, argv: list[str], *, cwd: Path | None = None,
           trace_root: Path | None = None, context: InvocationContext | None = None,
           replay: bool = False) -> subprocess.CompletedProcess:
    """Call the registered legacy CLI once, or explicitly replay a verified receipt.

    Tracing is optional, never a replacement for any mandatory receipt mechanism.
    A missing/crashed receipt is not permission to retry an uncertain invocation;
    callers must select a fresh attempt explicitly. No trace root means no writes.
    Native events use trace_root/repository-adoption; existing scientific runs
    remain outside this maintenance namespace. Receipt locations are unchanged.
    Unavailable optional storage executes without a receipt; it does not promise
    durable exactly-once delivery across calls. Receipts detect corruption/context
    substitution, not a malicious writer able to replace all local evidence.
    """
    implementation, metadata = _resolve(operation_id)
    command = [sys.executable, str(implementation), *argv]
    if replay and (trace_root is None or context is None):
        raise ReplayError("replay requires explicit trace root and host context")
    if trace_root is None:
        return _execute(command, cwd=cwd)
    context = context or InvocationContext("run-" + uuid4().hex, "inv-" + uuid4().hex)
    request = {"operation_id": operation_id, "registered_operation": metadata, "argv": list(argv),
               "cwd": str(Path(cwd or Path.cwd()).resolve()), "context": asdict(context),
               "implementation_sha256": _digest(implementation.read_bytes())}
    root = Path(trace_root).resolve()
    directory = root / "invocations" / context.run_id / context.invocation_id / str(context.attempt)
    lock = None
    try:
        directory.mkdir(parents=True, exist_ok=True)
        lock = (directory / ".lock").open("a+b")
        fcntl.flock(lock.fileno(), fcntl.LOCK_EX)
    except OSError as exc:
        if lock is not None:
            lock.close()
        if replay:
            raise ReplayError(f"replay storage unavailable: {exc}") from exc
        return _execute(command, cwd=cwd)
    try:
        if replay:
            return _replay(directory, request, command)
        manifest_path = directory / "invocation.json"
        if manifest_path.exists():
            raise ReplayError("identity already used; request explicit replay or a fresh attempt")
        try:
            _write(manifest_path, _bytes({"request": request, "status": "started"}))
        except OSError:
            # Reservation failure disables optional telemetry, not the owner CLI.
            return _execute(command, cwd=cwd)
        result = _execute(command, cwd=cwd)
        try:
            payload = {"request": request, "returncode": result.returncode,
                       "stdout_base64": base64.b64encode(result.stdout).decode(),
                       "stderr_base64": base64.b64encode(result.stderr).decode()}
            data = _bytes(payload)
            path = directory / "result.json"
            _write(path, data)
            _write(manifest_path, _bytes({"request": request, "status": "completed", "result_sha256": _digest(data)}))
            _emit(root, request, path, _digest(data), result)
        except Exception:
            # Even a broken optional sink/diagnostic cannot replace legacy results.
            # Do not catch BaseException: cancellation still propagates normally.
            pass
        return result
    finally:
        lock.close()


def main(argv=None):
    """Split adapter options at -- so malformed legacy arguments stay untouched."""
    values = list(sys.argv[1:] if argv is None else argv)
    boundary = values.index("--") if "--" in values else len(values)
    own, legacy = values[:boundary], values[boundary + 1:]
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("operation_id", choices=[OPERATION])
    parser.add_argument("--trace-root", type=Path)
    parser.add_argument("--run-id")
    parser.add_argument("--invocation-id")
    parser.add_argument("--attempt", type=int, default=1)
    parser.add_argument("--parent-run-id")
    parser.add_argument("--parent-event-id")
    parser.add_argument("--replay", action="store_true")
    args = parser.parse_args(own)
    if bool(args.run_id) != bool(args.invocation_id):
        parser.error("--run-id and --invocation-id must be supplied together")
    if args.replay and not (args.run_id and args.trace_root):
        parser.error("--replay requires --trace-root, --run-id and --invocation-id")
    context = InvocationContext(args.run_id or "run-" + uuid4().hex,
        args.invocation_id or "inv-" + uuid4().hex, args.attempt, args.parent_run_id, args.parent_event_id)
    result = invoke(args.operation_id, legacy, trace_root=args.trace_root, context=context, replay=args.replay)
    sys.stdout.buffer.write(result.stdout)
    sys.stderr.buffer.write(result.stderr)
    if result.returncode < 0:
        # Preserve signal termination as observed by a subprocess host.
        import signal
        signal.signal(-result.returncode, signal.SIG_DFL)
        os.kill(os.getpid(), -result.returncode)
    return result.returncode


if __name__ == "__main__":
    raise SystemExit(main())
