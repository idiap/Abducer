# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
# SPDX-License-Identifier: MIT
"""Durable job supervisor for the hosted Abducer native execution boundary.

Each claimed job gets a separate process group and writable output directory.
Only verified successful outputs advance the project's checkpoint. Crashes,
cancellation, expired leases and stale parents never trigger automatic replay
of potentially paid model calls.
"""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import re
import signal
import subprocess
import sys
import threading
import time
from uuid import uuid4

from .runtime import (
    confined,
    digest_file,
    json_bytes,
    verify_checkpoint,
    verify_snapshot,
)
from .store import Store


def worker_environment() -> dict[str, str]:
    """Pass runtime essentials and model configuration, not service credentials."""
    allowed = (
        "PATH",
        "LANG",
        "LC_ALL",
        "SSL_CERT_FILE",
        "SSL_CERT_DIR",
        "OPENAI_API_KEY",
        "OPENAI_BASE_URL",
        "ABDUCER_MODEL",
        "ABDUCER_MODEL_PROVIDER",
        "ABDUCER_NATIVE_HOOKS_ENABLED",
    )
    environment = {key: os.environ[key] for key in allowed if key in os.environ}
    environment.update(
        {
            # Skill scripts may use bare python/python3 or console entrypoints.
            # Keep these on the supervisor's interpreter, even when its parent
            # process was started with an absolute Python path and ambient PATH.
            "PATH": os.pathsep.join(
                [
                    str(Path(sys.executable).absolute().parent),
                    environment.get("PATH", os.defpath),
                ]
            ),
            "VIRTUAL_ENV": sys.prefix,
            "PYTHON": sys.executable,
            "PYTHONNOUSERSITE": "1",
            "PYTHONDONTWRITEBYTECODE": "1",
            "PYTHONUNBUFFERED": "1",
            "PYTHONPATH": os.pathsep.join(
                filter(
                    None,
                    [
                        str(Path(__file__).resolve().parents[2]),
                        os.environ.get("ABDUCER_REPOSITORY_ROOT"),
                    ],
                )
            ),
        }
    )
    return environment


def terminate_group(process: subprocess.Popen, *, grace_seconds: float = 2) -> None:
    """Stop the entire native process tree, including report subprocesses."""
    try:
        os.killpg(process.pid, signal.SIGTERM)
    except ProcessLookupError:
        pass
    try:
        process.wait(timeout=grace_seconds)
    except subprocess.TimeoutExpired:
        pass
    # Even a normally exited leader may have descendants. Kill the group before
    # accepting its workspace hashes so no late writer can change publication.
    try:
        os.killpg(process.pid, signal.SIGKILL)
    except ProcessLookupError:
        pass
    process.wait()


class Worker:
    """Claim one job at a time and publish only its authenticated Store lease."""

    def __init__(
        self,
        store: Store,
        *,
        data_root: Path,
        source_root: Path,
        worker_id: str | None = None,
        poll_seconds: float = 0.5,
        command_factory=None,
    ):
        self.store = store
        self.data_root = data_root.resolve()
        self.data_root.mkdir(parents=True, exist_ok=True)
        self.source_root = source_root.resolve(strict=True)
        self.worker_id = worker_id or "worker-" + uuid4().hex
        self.poll_seconds = poll_seconds
        # Injection exists for subprocess boundary tests; production CLI always
        # invokes the fixed native runtime, never a client-supplied command.
        self.command_factory = command_factory or self._command

    @staticmethod
    def _command(request: Path, response: Path) -> list[str]:
        return [
            sys.executable,
            "-m",
            "integrations.chatgpt.runtime",
            "run",
            "--request",
            str(request),
            "--response",
            str(response),
        ]

    def advertise(self):
        """Report provider and hook readiness; a stale heartbeat never authorizes admission."""
        try:
            source = json.loads(
                (self.source_root / ".abducer-source.json").read_text()
            )["content_sha256"]
        except (OSError, ValueError, KeyError):
            return
        provider = os.environ.get("ABDUCER_MODEL_PROVIDER", "api")
        ready = provider == "chatgpt"
        if provider == "api":
            from .provider import ProviderError, provider_settings

            try:
                provider_settings()
                ready = True
            except ProviderError:
                ready = False
        self.store.record_worker(
            self.worker_id,
            source,
            provider,
            provider_ready=ready,
            hooks_enabled=os.environ.get(
                "ABDUCER_NATIVE_HOOKS_ENABLED", "false"
            ).lower()
            == "true",
        )
        return {
            "source_sha256": source,
            "provider": provider,
            "provider_ready": ready,
            "hooks_enabled": os.environ.get(
                "ABDUCER_NATIVE_HOOKS_ENABLED", "false"
            ).lower()
            == "true",
        }

    def run_once(self) -> bool:
        """Consume at most one job. Return false only when the queue is empty."""
        capabilities = self.advertise()
        job = self.store.claim_job(self.worker_id, capabilities=capabilities)
        if job is None:
            return False
        job_id = job["id"]
        process = None
        lease_stop = threading.Event()
        lease_lost = threading.Event()

        def renew_lease():
            while not lease_stop.wait(10):
                try:
                    self.advertise()
                    if not self.store.heartbeat(job_id, self.worker_id):
                        lease_lost.set()
                        return
                except Exception:
                    lease_lost.set()
                    return

        lease_thread = threading.Thread(target=renew_lease, daemon=True)
        lease_thread.start()
        try:
            timeout = job["budget"]["timeout_seconds"]
            selected_provider = job.get("inputs", {}).get("model_provider")
            if selected_provider and selected_provider != os.environ.get(
                "ABDUCER_MODEL_PROVIDER", "api"
            ):
                raise ValueError("Worker model provider differs from the approved plan")
            if (
                job.get("inputs", {}).get("native_hooks_required")
                and os.environ.get("ABDUCER_NATIVE_HOOKS_ENABLED", "false").lower()
                != "true"
            ):
                raise ValueError("The approved plan requires native hooks")
            if (
                isinstance(timeout, bool)
                or not isinstance(timeout, (int, float))
                or not 1 <= timeout <= 7200
            ):
                raise ValueError("Invalid execution deadline")
            deadline = time.monotonic() + timeout
            if not re.fullmatch(r"[A-Za-z0-9_-]{1,128}", job_id):
                raise ValueError("Invalid internal job identity")
            manifest = verify_snapshot(self.source_root)
            if job.get("runtime_source_sha256") != manifest["content_sha256"]:
                raise ValueError(
                    "Worker runtime differs from the exact prepared source snapshot"
                )
            from .catalog import Catalog

            if Catalog(self.source_root).release != job["release"]:
                raise ValueError("Worker source release differs from the prepared plan")
            directory = confined(self.data_root, "jobs/" + job_id)
            directory.mkdir(parents=True, exist_ok=False, mode=0o700)
            request_path, response_path = (
                directory / "request.json",
                directory / "response.json",
            )
            output_relative = "jobs/" + job_id + "/output"
            request_path.write_bytes(
                json_bytes(
                    {
                        "job": job,
                        "source_root": str(self.source_root),
                        "data_root": str(self.data_root),
                        "database_path": str(self.store.path.resolve()),
                        "output_relative_path": output_relative,
                    }
                )
            )
            if (
                time.monotonic() >= deadline
                or lease_lost.is_set()
                or not self.store.heartbeat(job_id, self.worker_id)
            ):
                raise RuntimeError(
                    "Research deadline or authorization expired during preparation"
                )
            # Native stdout is diagnostic only. Keep it in a private file; no
            # model payload, credential or scientific status is inferred from it.
            with (directory / "worker.log").open("wb") as log:
                process = subprocess.Popen(
                    self.command_factory(request_path, response_path),
                    cwd=directory,
                    env=worker_environment(),
                    stdin=subprocess.DEVNULL,
                    stdout=log,
                    stderr=subprocess.STDOUT,
                    start_new_session=True,
                )
                while process.poll() is None:
                    if time.monotonic() >= deadline:
                        raise TimeoutError("Research deadline exceeded")
                    if lease_lost.is_set() or not self.store.heartbeat(
                        job_id, self.worker_id
                    ):
                        raise RuntimeError("Research cancelled or worker lease lost")
                    if log.tell() > 16 * 1024 * 1024:
                        raise RuntimeError(
                            "Research diagnostic output exceeded its budget"
                        )
                    time.sleep(self.poll_seconds)
                status = process.returncode
                terminate_group(process)
                process = None
            # A child can finish between poll intervals, and stopping its
            # descendants can itself consume the remaining budget. Completion
            # never grants authority to publish after the approved deadline.
            if time.monotonic() >= deadline:
                raise TimeoutError("Research deadline exceeded before publication")
            if status != 0:
                # Raw diagnostic exceptions may contain private research or
                # service paths. Keep them private and publish only error class.
                error_type = "NativeExecutionError"
                if response_path.is_file() and response_path.stat().st_size <= 65536:
                    candidate = json.loads(response_path.read_bytes()).get(
                        "error_type", ""
                    )
                    if re.fullmatch(r"[A-Za-z][A-Za-z0-9_]{0,80}", candidate):
                        error_type = candidate
                raise RuntimeError(
                    f"Native research failed ({error_type}); no artifacts were published"
                )
            if (
                not response_path.is_file()
                or response_path.is_symlink()
                or response_path.stat().st_size > 4 * 1024 * 1024
            ):
                raise ValueError("Missing or oversized native result")
            response = json.loads(response_path.read_bytes())
            self._verify_publication(response, job, output_relative)
            if time.monotonic() >= deadline:
                raise TimeoutError("Research deadline exceeded during verification")
            if not self.store.heartbeat(job_id, self.worker_id):
                raise RuntimeError("Worker lease lost before publication")
            if time.monotonic() >= deadline:
                raise TimeoutError("Research deadline exceeded before publication")
            self.store.finish_job(
                job_id,
                self.worker_id,
                response["result"],
                response["artifacts"],
                response["checkpoint"],
                deadline_monotonic=deadline,
            )
        except Exception as exc:
            if process is not None:
                terminate_group(process)
            self.store.fail_job(job_id, self.worker_id, str(exc))
        finally:
            lease_stop.set()
            lease_thread.join(timeout=2)
        return True

    def _verify_publication(
        self, response: dict, job: dict, output_relative: str
    ) -> None:
        """Reopen every artifact and checkpoint after the process group exits."""
        verification = response["result"]["report_verification"]
        if (
            verification.get("status") != "passed"
            or verification.get("scientific_truth_verified") is not False
        ):
            raise ValueError(
                "Native result must preserve scoped scientific verification"
            )
        output = confined(self.data_root, output_relative)
        checkpoint = response["checkpoint"]
        workspace = verify_checkpoint(
            self.data_root,
            checkpoint,
            release=job["release"],
            target_id=job["inputs"]["target_id"],
        )
        if workspace != output / "workspace":
            raise ValueError("Checkpoint does not belong to this job's workspace")
        ids = set()
        for artifact in response["artifacts"]:
            path = confined(self.data_root, artifact["relative_path"])
            if path.parent != output or artifact["id"] in ids:
                raise ValueError("Artifact identity or publication directory mismatch")
            ids.add(artifact["id"])
            if (
                path.stat().st_size != artifact["size"]
                or digest_file(path) != artifact["sha256"]
            ):
                raise ValueError("Artifact changed before publication")
        if not ids:
            raise ValueError("Native execution produced no verified report artifacts")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--database", type=Path)
    parser.add_argument(
        "--data-root", type=Path, default=os.environ.get("ABDUCER_DATA_ROOT")
    )
    parser.add_argument(
        "--source-root", type=Path, default=os.environ.get("ABDUCER_REPOSITORY_ROOT")
    )
    parser.add_argument("--once", action="store_true")
    args = parser.parse_args()
    if args.data_root is None or args.source_root is None:
        parser.error(
            "Set --data-root and --source-root or corresponding ABDUCER environment variables"
        )
    verify_snapshot(args.source_root)
    # Complete package/source loading before advertising a worker heartbeat.
    from .execution_registry import ExecutionRegistry
    from .startup import preload

    registry = ExecutionRegistry(args.source_root)
    setup = preload(registry)
    if setup["packages"]["status"] != "ready":
        parser.error("Runtime dependencies are unavailable; run setup_runtime first")
    database = args.database or args.data_root / "service.sqlite3"
    worker = Worker(
        Store(database), data_root=args.data_root, source_root=args.source_root
    )
    while True:
        found = worker.run_once()
        if args.once:
            return 0
        if not found:
            time.sleep(2)


if __name__ == "__main__":
    raise SystemExit(main())
