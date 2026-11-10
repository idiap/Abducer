"""Hard resource governance for discovery jobs and branch portfolios.

The governor deliberately separates operational outcomes from epistemic ones.
Deadlines, process crashes, memory pressure, and spend limits can stop a job,
but none of them are evidence for or against a hypothesis.
"""

from __future__ import annotations

import datetime as dt
import json
import os
import platform
import re
import resource
import signal
import subprocess
import threading
import time
from collections import deque
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, BinaryIO, Mapping, Sequence


TERMINAL_STATUSES = {
    "succeeded",
    "deadline_exhausted",
    "cpu_exhausted",
    "out_of_memory",
    "disk_exhausted",
    "network_exhausted",
    "token_exhausted",
    "request_exhausted",
    "spend_exhausted",
    "worker_failed",
    "report_failed",
    "cancelled",
}

RETRYABLE_STATUSES = {
    "deadline_exhausted",
    "cpu_exhausted",
    "out_of_memory",
    "disk_exhausted",
    "network_exhausted",
    "token_exhausted",
    "request_exhausted",
    "spend_exhausted",
    "worker_failed",
    "report_failed",
    "invalid",
    "literature_superseded",
}

_JOB_ID_RE = re.compile(r"^[A-Za-z0-9](?:[A-Za-z0-9._-]{0,126}[A-Za-z0-9])?$")


class BudgetExceeded(RuntimeError):
    """Raised when a hard resource dimension is exhausted."""

    def __init__(self, status: str, dimension: str, used: float, limit: float) -> None:
        if status not in TERMINAL_STATUSES:
            raise ValueError(f"unknown terminal status: {status}")
        self.status = status
        self.dimension = dimension
        self.used = used
        self.limit = limit
        super().__init__(f"{dimension} budget exhausted: used={used!r}, limit={limit!r}")


def validate_job_id(job_id: str) -> str:
    """Return a validated filesystem-safe job identifier.

    Dot segments, separators, hidden names, and ambiguous trailing punctuation
    are rejected even on platforms where they would otherwise resolve.
    """

    if not isinstance(job_id, str) or not _JOB_ID_RE.fullmatch(job_id):
        raise ValueError("job_id must contain only bounded alphanumerics, '.', '_' or '-'")
    if job_id in {".", ".."} or job_id.startswith(".") or ".." in job_id:
        raise ValueError("job_id cannot contain dot path segments")
    if "/" in job_id or "\\" in job_id or "\x00" in job_id:
        raise ValueError("job_id cannot contain a path separator or NUL")
    return job_id


def contained_path(run_directory: Path | str, *parts: str) -> Path:
    """Resolve a path and prove it remains inside ``run_directory``."""

    root = Path(run_directory).resolve()
    candidate = root.joinpath(*parts).resolve()
    try:
        candidate.relative_to(root)
    except ValueError as exc:
        raise ValueError(f"output path escapes run directory: {candidate}") from exc
    return candidate


def branch_run_directory(run_root: Path | str, job_id: str, branch_id: str | None = None) -> Path:
    """Construct (without creating) a contained run or branch directory."""

    safe_job = validate_job_id(job_id)
    path = contained_path(run_root, safe_job)
    if branch_id is not None:
        path = contained_path(path, "branches", validate_job_id(branch_id))
    return path


def _positive_number(value: Any, name: str, *, allow_zero: bool = False) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"{name} must be numeric")
    result = float(value)
    if result < 0 or (not allow_zero and result == 0):
        relation = "non-negative" if allow_zero else "positive"
        raise ValueError(f"{name} must be {relation}")
    return result


@dataclass(frozen=True)
class ResourceBudget:
    """Hard maxima for one job or branch."""

    budget_id: str
    wall_time_seconds: float
    grace_period_seconds: float
    cpu_seconds: float
    memory_bytes: int
    disk_bytes: int
    network_bytes: int
    token_count: int
    request_count: int
    cost_usd: float
    absolute_deadline: str | None = None

    @classmethod
    def from_mapping(cls, raw: Mapping[str, Any], *, budget_id: str | None = None) -> "ResourceBudget":
        """Parse and strictly validate a budget mapping."""

        identifier = str(budget_id or raw.get("budget_id") or "budget")
        wall = _positive_number(raw.get("wall_time_seconds"), "wall_time_seconds")
        grace = _positive_number(raw.get("grace_period_seconds", 1.0), "grace_period_seconds", allow_zero=True)
        if grace > 30:
            raise ValueError("grace_period_seconds cannot exceed 30")
        cpu = _positive_number(raw.get("cpu_seconds", wall), "cpu_seconds")
        memory = int(_positive_number(raw.get("memory_bytes", 512 * 1024 * 1024), "memory_bytes"))
        disk = int(_positive_number(raw.get("disk_bytes", 64 * 1024 * 1024), "disk_bytes", allow_zero=True))
        network = int(_positive_number(raw.get("network_bytes", 0), "network_bytes", allow_zero=True))
        tokens = int(_positive_number(raw.get("token_count", 0), "token_count", allow_zero=True))
        requests = int(_positive_number(raw.get("request_count", 0), "request_count", allow_zero=True))
        cost = _positive_number(raw.get("cost_usd", 0.0), "cost_usd", allow_zero=True)
        absolute = raw.get("absolute_deadline")
        if absolute is not None:
            _parse_deadline(str(absolute))
        return cls(
            budget_id=identifier,
            wall_time_seconds=wall,
            grace_period_seconds=grace,
            cpu_seconds=cpu,
            memory_bytes=memory,
            disk_bytes=disk,
            network_bytes=network,
            token_count=tokens,
            request_count=requests,
            cost_usd=cost,
            absolute_deadline=str(absolute) if absolute is not None else None,
        )


@dataclass
class ResourceUsage:
    """Observed accountable resource use."""

    wall_time_seconds: float = 0.0
    cpu_seconds: float = 0.0
    peak_memory_bytes: int = 0
    disk_bytes: int = 0
    network_bytes: int = 0
    token_count: int = 0
    request_count: int = 0
    cost_usd: float = 0.0

    def add(self, other: "ResourceUsage") -> None:
        self.wall_time_seconds += other.wall_time_seconds
        self.cpu_seconds += other.cpu_seconds
        self.peak_memory_bytes = max(self.peak_memory_bytes, other.peak_memory_bytes)
        self.disk_bytes += other.disk_bytes
        self.network_bytes += other.network_bytes
        self.token_count += other.token_count
        self.request_count += other.request_count
        self.cost_usd += other.cost_usd


def _parse_deadline(value: str) -> dt.datetime:
    parsed = dt.datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed.tzinfo is None:
        raise ValueError("absolute_deadline must include a timezone")
    return parsed.astimezone(dt.timezone.utc)


def _utc_now() -> dt.datetime:
    return dt.datetime.now(dt.timezone.utc)


def directory_file_sizes(path: Path | str) -> dict[str, int]:
    """Return stable relative paths and sizes for regular files below a root."""

    root = Path(path)
    if not root.exists():
        return {}
    sizes: dict[str, int] = {}
    for candidate in root.rglob("*"):
        try:
            if candidate.is_file() and not candidate.is_symlink():
                sizes[candidate.relative_to(root).as_posix()] = candidate.stat().st_size
        except (FileNotFoundError, PermissionError, OSError):
            continue
    return sizes


def directory_size(path: Path | str) -> int:
    """Return the total byte size of regular files below a contained path."""

    return sum(directory_file_sizes(path).values())


class _BoundedOutputCollector:
    """Drain one subprocess pipe while retaining only a fixed-size byte tail.

    ``communicate()`` retains the complete child output and can move an
    otherwise bounded worker's memory pressure into the ungoverned parent.
    Dedicated drain threads prevent pipe deadlock while the deque keeps parent
    memory independent of how noisy the child is.
    """

    def __init__(self, stream: BinaryIO, limit_bytes: int) -> None:
        self.stream = stream
        self.limit_bytes = limit_bytes
        self.total_bytes = 0
        self.retained_bytes = 0
        self.chunks: deque[bytes] = deque()
        self.error: OSError | None = None
        self._lock = threading.Lock()
        self.thread = threading.Thread(target=self._drain, daemon=True)

    def start(self) -> None:
        self.thread.start()

    def _drain(self) -> None:
        try:
            while True:
                chunk = self.stream.read(64 * 1024)
                if not chunk:
                    break
                with self._lock:
                    self.total_bytes += len(chunk)
                    self.chunks.append(chunk)
                    self.retained_bytes += len(chunk)
                    while self.retained_bytes > self.limit_bytes and self.chunks:
                        excess = self.retained_bytes - self.limit_bytes
                        oldest = self.chunks[0]
                        if len(oldest) <= excess:
                            self.chunks.popleft()
                            self.retained_bytes -= len(oldest)
                        else:
                            self.chunks[0] = oldest[excess:]
                            self.retained_bytes -= excess
        except OSError as exc:
            self.error = exc
        finally:
            try:
                self.stream.close()
            except OSError:
                pass

    def finish(self, *, deadline_monotonic: float) -> tuple[str, int, bool, bool]:
        """Return the bounded tail without ever waiting past an absolute drain deadline."""

        self.thread.join(timeout=max(0.0, deadline_monotonic - time.monotonic()))
        incomplete = self.thread.is_alive()
        if self.error is not None and not incomplete:
            raise self.error
        with self._lock:
            encoded = b"".join(self.chunks)
            total_bytes = self.total_bytes
        return (
            encoded.decode("utf-8", errors="replace"),
            total_bytes,
            total_bytes > self.limit_bytes,
            incomplete,
        )


class ResourceGovernor:
    """Enforce measured limits and expose every unavailable accounting edge.

    Wall time, CPU, process-group RSS, captured output, and run-directory disk
    growth are measured by this process.  Network, token, request, and monetary
    cost require an adapter to call :meth:`account`; until that happens the
    receipt calls them unavailable rather than pretending environment hints are
    enforcement.
    """

    def __init__(
        self,
        budget: ResourceBudget,
        *,
        run_directory: Path | str | None = None,
        allowed_working_directory: Path | str | None = None,
        capture_limit_bytes: int = 1024 * 1024,
        disk_sample_interval_seconds: float = 0.5,
    ) -> None:
        if capture_limit_bytes <= 0:
            raise ValueError("capture_limit_bytes must be positive")
        if disk_sample_interval_seconds <= 0:
            raise ValueError("disk_sample_interval_seconds must be positive")
        self.budget = budget
        self.run_directory = Path(run_directory).resolve() if run_directory is not None else None
        self.allowed_working_directory = (
            Path(allowed_working_directory).resolve()
            if allowed_working_directory is not None
            else self.run_directory
        )
        self.capture_limit_bytes = int(capture_limit_bytes)
        self.disk_sample_interval_seconds = float(disk_sample_interval_seconds)
        self.started_monotonic = time.monotonic()
        self.started_at = _utc_now()
        relative = self.started_at + dt.timedelta(seconds=budget.wall_time_seconds)
        absolute = _parse_deadline(budget.absolute_deadline) if budget.absolute_deadline else relative
        self.deadline = min(relative, absolute)
        self.deadline_monotonic = self.started_monotonic + max(
            0.0, (self.deadline - self.started_at).total_seconds()
        )
        self.usage = ResourceUsage()
        self.events: list[dict[str, Any]] = []
        self._externally_reported_dimensions: set[str] = set()
        self._disk_baseline_sizes = (
            directory_file_sizes(self.run_directory)
            if self.run_directory is not None
            else {}
        )
        self._last_disk_sample_monotonic = self.started_monotonic

    @classmethod
    def from_mapping(
        cls,
        raw: Mapping[str, Any],
        *,
        run_directory: Path | str | None = None,
        branch_id: str | None = None,
    ) -> "ResourceGovernor":
        """Create a governor, applying a named per-branch override if present."""

        effective = dict(raw)
        if branch_id is not None:
            per_branch = raw.get("per_branch", {})
            if not isinstance(per_branch, Mapping) or branch_id not in per_branch:
                raise ValueError(f"missing independent budget for branch {branch_id!r}")
            branch_raw = per_branch[branch_id]
            if not isinstance(branch_raw, Mapping):
                raise ValueError(f"invalid budget for branch {branch_id!r}")
            for key, value in branch_raw.items():
                effective[key] = value
            effective["budget_id"] = f"{raw.get('budget_id', 'portfolio')}:{branch_id}"
        return cls(ResourceBudget.from_mapping(effective), run_directory=run_directory)

    def remaining_seconds(self) -> float:
        return max(0.0, (self.deadline - _utc_now()).total_seconds())

    def account(
        self,
        *,
        network_bytes: int | None = None,
        token_count: int | None = None,
        request_count: int | None = None,
        cost_usd: float | None = None,
        disk_bytes: int | None = None,
    ) -> None:
        """Atomically account externally observed resources and enforce maxima."""

        increments = tuple(
            value
            for value in (network_bytes, token_count, request_count, cost_usd)
            if value is not None
        )
        if any(value < 0 for value in increments):
            raise ValueError("resource increments cannot be negative")
        for dimension, value in (
            ("network_bytes", network_bytes),
            ("token_count", token_count),
            ("request_count", request_count),
            ("cost_usd", cost_usd),
        ):
            if value is None:
                continue
            self._externally_reported_dimensions.add(dimension)
            setattr(
                self.usage,
                dimension,
                getattr(self.usage, dimension) + (float(value) if dimension == "cost_usd" else int(value)),
            )
        if disk_bytes is not None:
            if disk_bytes < 0:
                raise ValueError("disk_bytes cannot be negative")
            self.usage.disk_bytes = int(disk_bytes)
        else:
            self._sample_disk_usage(force=True)
        self.checkpoint()

    def measurement_boundaries(self) -> dict[str, dict[str, Any]]:
        """Describe which resource dimensions are truly measured or reported."""

        boundaries = {
            "wall_time_seconds": {"status": "measured", "enforced": True},
            "cpu_seconds": {"status": "measured", "enforced": True},
            "peak_memory_bytes": {"status": "measured", "enforced": True},
            "disk_bytes": {
                "status": (
                    "sampled_high_water"
                    if self.run_directory is not None
                    else "unavailable"
                ),
                "enforced": self.run_directory is not None,
                "accounting_root": str(self.run_directory) if self.run_directory is not None else None,
                "sample_interval_seconds": (
                    self.disk_sample_interval_seconds
                    if self.run_directory is not None
                    else None
                ),
                "limitation": (
                    "positive per-file growth observed at sampling boundaries; "
                    "ephemeral create-delete bursts between samples are unavailable"
                    if self.run_directory is not None
                    else "no accounting root was supplied"
                ),
            },
        }
        for dimension in ("network_bytes", "token_count", "request_count", "cost_usd"):
            reported = dimension in self._externally_reported_dimensions
            boundaries[dimension] = {
                "status": "externally_reported" if reported else "unavailable",
                "enforced": reported,
                "reason": (
                    "adapter supplied cumulative usage"
                    if reported
                    else "generic subprocess governance cannot observe this dimension"
                ),
            }
        return boundaries

    def _sample_disk_usage(self, *, force: bool = False) -> int:
        """Measure high-water positive growth below the accounting root."""

        if self.run_directory is None:
            return self.usage.disk_bytes
        now = time.monotonic()
        if (
            not force
            and now - self._last_disk_sample_monotonic
            < self.disk_sample_interval_seconds
        ):
            return self.usage.disk_bytes
        current = directory_file_sizes(self.run_directory)
        growth = sum(
            max(0, size - self._disk_baseline_sizes.get(relative, 0))
            for relative, size in current.items()
        )
        self.usage.disk_bytes = max(self.usage.disk_bytes, growth)
        self._last_disk_sample_monotonic = now
        return self.usage.disk_bytes

    def checkpoint(self) -> None:
        """Enforce all observable resource dimensions immediately."""

        elapsed = time.monotonic() - self.started_monotonic
        self.usage.wall_time_seconds = max(self.usage.wall_time_seconds, elapsed)
        self._sample_disk_usage()
        if _utc_now() >= self.deadline or elapsed >= self.budget.wall_time_seconds:
            raise BudgetExceeded("deadline_exhausted", "wall_time_seconds", elapsed, self.budget.wall_time_seconds)
        checks = (
            ("cpu_exhausted", "cpu_seconds", self.usage.cpu_seconds, self.budget.cpu_seconds),
            ("out_of_memory", "peak_memory_bytes", self.usage.peak_memory_bytes, self.budget.memory_bytes),
            ("network_exhausted", "network_bytes", self.usage.network_bytes, self.budget.network_bytes),
            ("token_exhausted", "token_count", self.usage.token_count, self.budget.token_count),
            ("request_exhausted", "request_count", self.usage.request_count, self.budget.request_count),
            ("spend_exhausted", "cost_usd", self.usage.cost_usd, self.budget.cost_usd),
            ("disk_exhausted", "disk_bytes", self.usage.disk_bytes, self.budget.disk_bytes),
        )
        for status, dimension, used, limit in checks:
            # A zero allowance means the dimension is unavailable, not unbounded.
            if used > limit:
                raise BudgetExceeded(status, dimension, float(used), float(limit))

    def _preexec_limits(self) -> None:
        cpu_soft = max(1, int(self.budget.cpu_seconds))
        cpu_hard = max(cpu_soft, int(self.budget.cpu_seconds + self.budget.grace_period_seconds + 1))
        resource.setrlimit(resource.RLIMIT_CPU, (cpu_soft, cpu_hard))
        resource.setrlimit(resource.RLIMIT_FSIZE, (self.budget.disk_bytes, self.budget.disk_bytes))
        # macOS advertises RLIMIT_AS but rejects finite limits in a pre-exec
        # child.  The parent-side process-group RSS monitor below enforces the
        # same hard maximum there; Linux also gets kernel enforcement.
        if hasattr(resource, "RLIMIT_AS") and platform.system() != "Darwin":
            resource.setrlimit(resource.RLIMIT_AS, (self.budget.memory_bytes, self.budget.memory_bytes))

    @staticmethod
    def _process_group_rss_bytes(process_group_id: int) -> int:
        """Measure aggregate resident memory for one process group."""

        try:
            observed = subprocess.run(
                ["ps", "-axo", "pgid=,rss="],
                check=False,
                capture_output=True,
                text=True,
                timeout=1.0,
            )
        except (OSError, subprocess.SubprocessError):
            return 0
        total_kib = 0
        for line in observed.stdout.splitlines():
            columns = line.split()
            if len(columns) != 2:
                continue
            try:
                pgid, rss_kib = int(columns[0]), int(columns[1])
            except ValueError:
                continue
            if pgid == process_group_id:
                total_kib += rss_kib
        return total_kib * 1024

    @staticmethod
    def _process_group_exists(process_group_id: int) -> bool:
        """Return whether any process still belongs to an isolated POSIX group."""

        if os.name != "posix":
            return False
        try:
            os.killpg(process_group_id, 0)
        except ProcessLookupError:
            return False
        except PermissionError:
            return True
        return True

    @classmethod
    def _terminate_group(cls, process: subprocess.Popen[Any], grace_seconds: float) -> str:
        """Terminate every descendant in the isolated group, even after its leader exits."""

        leader_was_terminal = process.poll() is not None
        if os.name != "posix":
            if leader_was_terminal:
                return "already_terminal"
            process.terminate()
            try:
                return "terminated"
            finally:
                try:
                    process.wait(timeout=max(0.0, grace_seconds))
                except subprocess.TimeoutExpired:
                    process.kill()
                    process.wait(timeout=1.0)
        if not cls._process_group_exists(process.pid):
            return "already_terminal"
        prefix = "descendants_" if leader_was_terminal else ""
        try:
            os.killpg(process.pid, signal.SIGTERM)
        except ProcessLookupError:
            return "already_terminal"
        grace_deadline = time.monotonic() + max(0.0, grace_seconds)
        while time.monotonic() < grace_deadline:
            process.poll()
            if not cls._process_group_exists(process.pid):
                return f"{prefix}terminated"
            time.sleep(min(0.01, max(0.0, grace_deadline - time.monotonic())))
        if cls._process_group_exists(process.pid):
            try:
                os.killpg(process.pid, signal.SIGKILL)
            except ProcessLookupError:
                return f"{prefix}terminated"
        try:
            process.wait(timeout=min(1.0, max(0.05, grace_seconds + 0.05)))
        except subprocess.TimeoutExpired:
            # The direct child is reaped independently from re-parented
            # descendants.  No unbounded wait is permitted here.
            pass
        return f"{prefix}killed"

    def run_process(
        self,
        command: Sequence[str],
        *,
        cwd: Path | str | None = None,
        env: Mapping[str, str] | None = None,
        role: str = "worker",
    ) -> dict[str, Any]:
        """Run a command in an isolated process group under the hard deadline."""

        if not command or not all(isinstance(part, str) and part for part in command):
            raise ValueError("command must be a non-empty sequence of strings")
        if role not in {"worker", "solver", "report_builder"}:
            raise ValueError("role must be worker, solver, or report_builder")
        self.checkpoint()
        workdir = Path(cwd).resolve() if cwd is not None else self.run_directory
        if self.allowed_working_directory is not None and workdir is not None:
            try:
                workdir.relative_to(self.allowed_working_directory)
            except ValueError as exc:
                raise ValueError("subprocess cwd must be inside the allowed working directory") from exc
        if workdir is not None:
            workdir.mkdir(parents=True, exist_ok=True)
        started = _utc_now()
        started_mono = time.monotonic()
        before = resource.getrusage(resource.RUSAGE_CHILDREN)
        child_environment = os.environ.copy()
        if env is not None:
            child_environment.update(env)
        child_environment.update(
            {
                "ABDUCER_ABSOLUTE_DEADLINE": self.deadline.isoformat(),
                "ABDUCER_BUDGET_ID": self.budget.budget_id,
                "ABDUCER_COST_LIMIT_USD": str(self.budget.cost_usd),
                "ABDUCER_NETWORK_LIMIT_BYTES": str(self.budget.network_bytes),
                "ABDUCER_TOKEN_LIMIT": str(self.budget.token_count),
                "ABDUCER_REQUEST_LIMIT": str(self.budget.request_count),
            }
        )
        process = subprocess.Popen(
            list(command),
            cwd=str(workdir) if workdir is not None else None,
            env=child_environment,
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=False,
            start_new_session=True,
            preexec_fn=self._preexec_limits if os.name == "posix" else None,
        )
        if process.stdout is None or process.stderr is None:
            raise RuntimeError("subprocess output pipes were not created")
        stdout_collector = _BoundedOutputCollector(process.stdout, self.capture_limit_bytes)
        stderr_collector = _BoundedOutputCollector(process.stderr, self.capture_limit_bytes)
        stdout_collector.start()
        stderr_collector.start()
        termination = None
        timed_out = False
        memory_exhausted = False
        disk_exhausted = False
        descendant_leak = False
        observed_peak_rss = 0
        while True:
            remaining = self.remaining_seconds()
            if remaining <= 0:
                timed_out = True
                termination = self._terminate_group(process, self.budget.grace_period_seconds)
                break
            try:
                process.wait(timeout=min(0.05, remaining))
                break
            except subprocess.TimeoutExpired:
                observed_rss = self._process_group_rss_bytes(process.pid)
                observed_peak_rss = max(observed_peak_rss, observed_rss)
                self.usage.peak_memory_bytes = max(self.usage.peak_memory_bytes, observed_rss)
                if observed_rss > self.budget.memory_bytes:
                    memory_exhausted = True
                    termination = self._terminate_group(process, self.budget.grace_period_seconds)
                    break
                if self._sample_disk_usage() > self.budget.disk_bytes:
                    disk_exhausted = True
                    termination = self._terminate_group(process, self.budget.grace_period_seconds)
                    break
        if self._process_group_exists(process.pid):
            descendant_leak = process.poll() is not None
            termination = self._terminate_group(process, self.budget.grace_period_seconds)
        # Pipe drainage never gains a fresh relative timeout.  In particular,
        # an inherited descriptor cannot extend the absolute job deadline.
        drain_deadline = self.deadline_monotonic
        stdout, stdout_bytes, stdout_truncated, stdout_drain_incomplete = stdout_collector.finish(
            deadline_monotonic=drain_deadline
        )
        stderr, stderr_bytes, stderr_truncated, stderr_drain_incomplete = stderr_collector.finish(
            deadline_monotonic=drain_deadline
        )
        after = resource.getrusage(resource.RUSAGE_CHILDREN)
        elapsed = time.monotonic() - started_mono
        cpu = max(0.0, (after.ru_utime + after.ru_stime) - (before.ru_utime + before.ru_stime))
        maxrss = max(0, after.ru_maxrss) if after.ru_maxrss > before.ru_maxrss else 0
        peak_bytes = int(maxrss if platform.system() == "Darwin" else maxrss * 1024)
        self.usage.wall_time_seconds = max(self.usage.wall_time_seconds, time.monotonic() - self.started_monotonic)
        self.usage.cpu_seconds += cpu
        self.usage.peak_memory_bytes = max(
            self.usage.peak_memory_bytes, observed_peak_rss, peak_bytes
        )
        self._sample_disk_usage(force=True)

        returncode = process.returncode
        lower_error = stderr.lower()
        if timed_out:
            status = "deadline_exhausted"
        elif memory_exhausted:
            status = "out_of_memory"
        elif disk_exhausted:
            status = "disk_exhausted"
        elif "memoryerror" in lower_error or "cannot allocate memory" in lower_error:
            status = "out_of_memory"
        elif returncode is not None and returncode < 0 and -returncode in {signal.SIGXCPU, signal.SIGKILL}:
            status = "cpu_exhausted" if -returncode == signal.SIGXCPU else "out_of_memory"
        elif (
            returncode is not None
            and returncode < 0
            and hasattr(signal, "SIGXFSZ")
            and -returncode == signal.SIGXFSZ
        ):
            status = "disk_exhausted"
        elif self.usage.disk_bytes > self.budget.disk_bytes or "file too large" in lower_error:
            status = "disk_exhausted"
        elif self.usage.peak_memory_bytes > self.budget.memory_bytes:
            status = "out_of_memory"
        elif self.usage.cpu_seconds > self.budget.cpu_seconds:
            status = "cpu_exhausted"
        elif descendant_leak or stdout_drain_incomplete or stderr_drain_incomplete:
            status = "report_failed" if role == "report_builder" else "worker_failed"
        elif returncode == 0:
            status = "succeeded"
        elif role == "report_builder":
            status = "report_failed"
        else:
            status = "worker_failed"
        event = {
            "event": "process_terminal",
            "role": role,
            "command": list(command),
            "pid": process.pid,
            "started_at": started.isoformat(),
            "completed_at": _utc_now().isoformat(),
            "elapsed_seconds": elapsed,
            "returncode": returncode,
            "status": status,
            "termination": termination,
            "stdout": stdout,
            "stderr": stderr,
            "stdout_bytes": stdout_bytes,
            "stderr_bytes": stderr_bytes,
            "stdout_truncated": stdout_truncated,
            "stderr_truncated": stderr_truncated,
            "stdout_drain_incomplete": stdout_drain_incomplete,
            "stderr_drain_incomplete": stderr_drain_incomplete,
            "descendant_leak_detected": descendant_leak,
            "capture_limit_bytes": self.capture_limit_bytes,
            "resource_measurement": self.measurement_boundaries(),
            "epistemic_effect": "none_operational_outcome_only" if status != "succeeded" else "awaiting_output_validation",
        }
        self.events.append(event)
        return event

    def receipt(self, status: str) -> dict[str, Any]:
        if status not in TERMINAL_STATUSES:
            raise ValueError(f"invalid terminal status: {status}")
        return {
            "budget": asdict(self.budget),
            "usage": asdict(self.usage),
            "status": status,
            "events": list(self.events),
            "deadline": self.deadline.isoformat(),
            "resource_measurement": self.measurement_boundaries(),
        }


@dataclass
class PortfolioBudget:
    """Independent branch governors plus a protected unallocated reserve."""

    raw: Mapping[str, Any]
    run_directory: Path
    governors: dict[str, ResourceGovernor] = field(default_factory=dict)

    def __post_init__(self) -> None:
        reserve = _positive_number(self.raw.get("portfolio_reserve_fraction", 0.0), "portfolio_reserve_fraction", allow_zero=True)
        if reserve >= 1:
            raise ValueError("portfolio_reserve_fraction must be below one")
        per_branch = self.raw.get("per_branch")
        if not isinstance(per_branch, Mapping) or not per_branch:
            raise ValueError("portfolio budget requires explicit per_branch budgets")
        additive_dimensions = ("cpu_seconds", "disk_bytes", "network_bytes", "token_count", "request_count", "cost_usd")
        for dimension in additive_dimensions:
            total = float(self.raw.get(dimension, 0.0))
            allocated = sum(float(row.get(dimension, 0.0)) for row in per_branch.values() if isinstance(row, Mapping))
            spendable = total * (1.0 - reserve)
            if allocated > spendable + 1e-12:
                raise ValueError(f"branch {dimension} allocations consume the protected portfolio reserve")
        # Concurrent workers can overlap wall time, but each branch must still
        # fit the portfolio's wall and peak-memory envelopes individually.
        for branch_id, row in per_branch.items():
            if float(row.get("wall_time_seconds", 0.0)) > float(self.raw.get("wall_time_seconds", 0.0)):
                raise ValueError(f"branch {branch_id!r} wall budget exceeds portfolio wall budget")
            if float(row.get("memory_bytes", 0.0)) > float(self.raw.get("memory_bytes", 0.0)):
                raise ValueError(f"branch {branch_id!r} memory budget exceeds portfolio memory budget")

    def governor_for(self, branch_id: str) -> ResourceGovernor:
        branch_id = validate_job_id(branch_id)
        if branch_id not in self.governors:
            branch_dir = contained_path(self.run_directory, "branches", branch_id)
            branch_dir.mkdir(parents=True, exist_ok=True)
            self.governors[branch_id] = ResourceGovernor.from_mapping(
                self.raw,
                run_directory=branch_dir,
                branch_id=branch_id,
            )
        return self.governors[branch_id]

    def aggregate_usage(self) -> ResourceUsage:
        total = ResourceUsage()
        for governor in self.governors.values():
            total.add(governor.usage)
        return total


def selective_retry_schedule(
    branch_results: Sequence[Mapping[str, Any]],
    *,
    dependency_invalidations: Mapping[str, Sequence[str]] | None = None,
) -> list[dict[str, Any]]:
    """Schedule only failed/invalid/stale branches or explicitly invalidated dependants."""

    invalidations = dependency_invalidations or {}
    by_id = {str(row.get("branch_id")): row for row in branch_results}
    retry: dict[str, dict[str, Any]] = {}
    failed_ids: set[str] = set()
    for branch_id, row in by_id.items():
        status = str(row.get("status"))
        validated = bool(row.get("validated", False))
        literature_current = bool(row.get("literature_current", True))
        if status in RETRYABLE_STATUSES or not validated or not literature_current:
            reason = status if status in RETRYABLE_STATUSES else ("invalid" if not validated else "literature_superseded")
            retry[branch_id] = {"branch_id": branch_id, "reason": reason, "preserve_successful_siblings": True}
            failed_ids.add(branch_id)
    for failed_id in sorted(failed_ids):
        for dependant in invalidations.get(failed_id, ()):
            if dependant in by_id:
                retry.setdefault(
                    dependant,
                    {
                        "branch_id": dependant,
                        "reason": f"dependency_invalidated:{failed_id}",
                        "preserve_successful_siblings": True,
                    },
                )
    return [retry[key] for key in sorted(retry)]


def partial_result_partition(branch_results: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    """Retain validated successes independently from retryable failures."""

    retained = [
        dict(row)
        for row in branch_results
        if row.get("status") == "succeeded" and row.get("validated") is True and row.get("literature_current", True) is True
    ]
    return {
        "retained_successes": retained,
        "retry_schedule": selective_retry_schedule(branch_results),
        "partial_failure": bool(retained) and len(retained) != len(branch_results),
    }


def write_structured_job_log(path: Path | str, payload: Mapping[str, Any]) -> None:
    """Persist the full structured log without accepting an escaping path."""

    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    encoded = json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False) + "\n"
    target.write_text(encoded, encoding="utf-8")
