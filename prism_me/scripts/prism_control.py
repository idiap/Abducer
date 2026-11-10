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
"""Deterministic control plane for Prism ME inside a Codex workspace.

This script serves two closely related roles:

1. It gives humans and skills a small repo-local CLI for inspecting the current
   Prism request state without re-deriving it from prose each time.
2. It acts as the implementation target for Codex lifecycle hooks so the repo
   can add hard-ish operational checks around the skills.

The control plane intentionally sticks to the Python standard library so it can
run inside a fresh Codex environment without extra dependency setup.
"""

from __future__ import annotations

import argparse
from contextlib import contextmanager
import fcntl
import hashlib
import json
import os
import re
import stat
import subprocess
import sys
import tempfile
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

try:
    import tomllib  # type: ignore[attr-defined]
except ModuleNotFoundError:  # pragma: no cover - compatibility fallback
    try:
        import tomli as tomllib  # type: ignore[no-redef]
    except ModuleNotFoundError:  # pragma: no cover - compatibility fallback
        tomllib = None  # type: ignore[assignment]


@dataclass(frozen=True)
class ArtifactSpec:
    """Describe one Prism artifact in the required execution order."""

    filename: str
    stage: str
    skill: str
    required: bool = True


ARTIFACT_SPECS: tuple[ArtifactSpec, ...] = (
    ArtifactSpec("00-skill-coverage-checklist.md", "coverage-ledger", "prism-spec-orchestrator"),
    ArtifactSpec("01-spec.md", "specification", "prism-spec-intake"),
    ArtifactSpec("02-agent-contract.yaml", "contracting", "prism-agent-contract-author"),
    ArtifactSpec("02b-quality-criteria.md", "quality-modeling", "prism-quality-criteria-elicitor"),
    ArtifactSpec("02c-external-surface.md", "external-scoping", "prism-external-reference-scoper", required=False),
    ArtifactSpec("02d-external-capabilities.md", "external-capability-mapping", "prism-external-capability-extractor", required=False),
    ArtifactSpec("02e-agentic-shape.md", "external-shaping", "prism-agentic-shape-forger", required=False),
    ArtifactSpec("03-repo-map.md", "mapping", "prism-repo-cartographer"),
    ArtifactSpec("03b-dependency-map.md", "dependency-mapping", "prism-dependency-cartographer"),
    ArtifactSpec("04-slice-plan.md", "planning", "prism-slice-planner"),
    ArtifactSpec("04b-test-strategy.md", "test-planning", "prism-test-strategy-architect"),
    ArtifactSpec("05-execution-log.md", "execution", "prism-implementation-driver"),
    ArtifactSpec("05b-refinement-loop.md", "reflective-refinement", "prism-reflective-refinement-loop"),
    ArtifactSpec("05c-test-evidence.md", "test-evidence", "prism-generative-validation-runner"),
    ArtifactSpec("06-verification.md", "evaluation", "prism-spec-verification-critic"),
    ArtifactSpec("07-handoff.md", "handoff", "prism-integration-handoff"),
    ArtifactSpec("reasoning-log.md", "reasoning-log", "all"),
)

TODO_FIELD_PATTERN = re.compile(r"^- ([^:]+):\s*(.*)$")

DESTRUCTIVE_PATTERNS: tuple[tuple[re.Pattern[str], str], ...] = (
    (
        re.compile(r"(^|[;&|]\s*)(rm\s+-rf\s+(/|\~|--no-preserve-root))(\s|$)"),
        "Blocked destructive deletion command.",
    ),
    (
        re.compile(r"(^|[;&|]\s*)git\s+reset\s+--hard(\s|$)"),
        "Blocked Git history rewrite. Use a reviewed workflow instead.",
    ),
    (
        re.compile(r"(^|[;&|]\s*)git\s+clean\s+-fd"),
        "Blocked Git clean command because it can discard worktree data.",
    ),
    (
        re.compile(r"(^|[;&|]\s*)git\s+checkout\s+--(\s|$)"),
        "Blocked file-level checkout because it can discard local changes.",
    ),
    (
        re.compile(r"(curl|wget)[^|\\n]*\|\s*(sh|bash)"),
        "Blocked remote shell pipe command.",
    ),
    (
        re.compile(r"(^|[;&|]\s*)(dd|mkfs|diskutil\s+eraseDisk)(\s|$)"),
        "Blocked device-destructive shell command.",
    ),
)

DIRECT_PRISM_WRITE_HINTS: tuple[str, ...] = (
    ".prism/",
    ".codex/",
    "to-do.md",
    "AGENTS.md",
    "agents.md",
)

CONTROL_SURFACE_DELETE_HINTS: tuple[str, ...] = (
    ".prism",
    ".codex",
    "to-do.md",
    "AGENTS.md",
    "agents.md",
    "prism_me",
)

DIRECT_WRITE_OPERATORS: tuple[str, ...] = (
    " > ",
    " >> ",
    " tee ",
    "sed -i",
    "perl -pi",
    "python -c",
    "python3 -c",
    "node -e",
    "ruby -e",
    "touch ",
    "mkdir ",
    "cp ",
    "mv ",
)

TEST_COMMAND_PREFIXES: tuple[str, ...] = (
    "pytest",
    "python -m pytest",
    "python3 -m pytest",
    "uv run pytest",
    "npm test",
    "pnpm test",
    "yarn test",
    "cargo test",
    "go test",
)

# Broad persona reviews are intentionally sparse.  They remain available on
# demand and at release/verification gates, while the automatic edit counter
# acts only as a long-horizon drift check instead of interrupting active slices.
PERSONA_REVIEW_THRESHOLD = 50
PERSONA_REVIEW_ARTIFACT = "05d-persona-review.md"
PERSONA_REVIEW_SKILL = "prism-persona-review-orchestrator"
CONTROL_STATE_FILENAME = "prism_control_state.json"
CONTROL_STATE_LOCK_FILENAME = "prism_control_state.lock"
UNSCOPED_REQUEST_KEY = "__unscoped__"
EDIT_LEASE_PROTOCOL_VERSION = 1
EDIT_LEASE_TTL_SECONDS = 300.0
EDIT_LEASE_CANCELLATION_REASONS = frozenset(
    {"tool_failed_before_mutation", "cancelled_before_execution"}
)
EDIT_LEASE_STATUSES = frozenset(
    {"leased", "committed", "cancelled", "expired_indeterminate"}
)
PERSONA_REVIEW_SECTION = """
## Persona Review Control

- Edit/write cycles recorded: `0`
- Last completed persona review cycle: `0`
- Next automatic persona review: `50`
- Persona review due: `no`
- Persona review artifact:
- Persona review TODO status: `idle`
""".strip()


def _repo_root_from(path: Path) -> Path:
    """Resolve the git root for the given path, falling back to ancestor search."""

    try:
        result = subprocess.run(
            ["git", "rev-parse", "--show-toplevel"],
            cwd=path,
            check=True,
            capture_output=True,
            text=True,
        )
        return Path(result.stdout.strip())
    except Exception:
        current = path.resolve()
        for candidate in (current, *current.parents):
            if (candidate / ".git").exists():
                return candidate
        return current


def _utc_now() -> str:
    """Return a compact UTC timestamp for state tracking."""

    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def _normalize_field_name(name: str) -> str:
    """Normalize bullet-field labels so updates survive punctuation changes."""

    return re.sub(r"[^a-z0-9]+", "_", name.strip().lower()).strip("_")


def _parse_todo_fields(todo_path: Path) -> dict[str, str]:
    """Extract the simple key/value fields from the root Prism to-do file."""

    if not todo_path.exists():
        return {}

    fields: dict[str, str] = {}
    for line in todo_path.read_text(encoding="utf-8").splitlines():
        match = TODO_FIELD_PATTERN.match(line)
        if not match:
            continue
        key = _normalize_field_name(match.group(1))
        fields[key] = match.group(2).strip()
    return fields


def _control_state_path(repo_root: Path) -> Path:
    """Return the repo-local Prism control state file."""

    return repo_root / ".codex" / "state" / CONTROL_STATE_FILENAME


def _control_state_lock_path(repo_root: Path) -> Path:
    """Return the stable sidecar lock path for control-state transactions."""

    return repo_root / ".codex" / "state" / CONTROL_STATE_LOCK_FILENAME


class PrismControlStateError(RuntimeError):
    """Raised when authoritative Prism control state is corrupt or unsafe."""


class PrismEditLeaseError(PrismControlStateError):
    """Raised when an edit cannot safely reserve or commit a review-cycle slot."""


@contextmanager
def _control_state_lock(repo_root: Path):
    """Serialize control-state and Markdown-projection transactions by process."""

    lock_path = _control_state_lock_path(repo_root)
    lock_path.parent.mkdir(parents=True, exist_ok=True)
    with lock_path.open("a+b") as lock_handle:
        fcntl.flock(lock_handle.fileno(), fcntl.LOCK_EX)
        try:
            yield
        finally:
            fcntl.flock(lock_handle.fileno(), fcntl.LOCK_UN)


def _atomic_write_text(path: Path, text: str, *, default_mode: int = 0o600) -> None:
    """Durably replace one regular file without exposing partial contents."""

    path.parent.mkdir(parents=True, exist_ok=True)
    if path.is_symlink():
        raise PrismControlStateError(f"refusing to replace symlinked control file: {path}")

    mode = stat.S_IMODE(path.stat().st_mode) if path.exists() else default_mode
    descriptor, temporary_name = tempfile.mkstemp(
        prefix=f".{path.name}.",
        suffix=".tmp",
        dir=path.parent,
    )
    temporary_path = Path(temporary_name)
    descriptor_open = True
    try:
        os.fchmod(descriptor, mode)
        with os.fdopen(descriptor, "w", encoding="utf-8") as handle:
            descriptor_open = False
            handle.write(text)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary_path, path)
        directory_flags = os.O_RDONLY | getattr(os, "O_DIRECTORY", 0)
        directory_descriptor = os.open(path.parent, directory_flags)
        try:
            os.fsync(directory_descriptor)
        finally:
            os.close(directory_descriptor)
    finally:
        if descriptor_open:
            os.close(descriptor)
        temporary_path.unlink(missing_ok=True)


def _default_review_state() -> dict[str, Any]:
    """Build the default per-request review-cycle state."""

    return {
        "edit_write_cycles": 0,
        "last_completed_review_cycle": 0,
        "review_due": False,
        "review_due_cycle": 0,
        "last_event_at": "",
        "last_completion_at": "",
        "recorded_edit_events": {},
        "edit_lease_protocol_version": 0,
        "edit_leases": {},
    }


def _validate_review_state(review_state: dict[str, Any], *, request_key: str) -> None:
    """Validate one request counter without repairing contradictory authority."""

    merged = _default_review_state()
    merged.update(review_state)

    for field in ("edit_write_cycles", "last_completed_review_cycle", "review_due_cycle"):
        value = merged[field]
        if isinstance(value, bool) or not isinstance(value, int) or value < 0:
            raise PrismControlStateError(
                f"invalid {field} for Prism request {request_key!r}: {value!r}"
            )

    cycles = merged["edit_write_cycles"]
    last_completed = merged["last_completed_review_cycle"]
    due_cycle = merged["review_due_cycle"]
    review_due = merged["review_due"]
    if not isinstance(review_due, bool):
        raise PrismControlStateError(
            f"invalid review_due for Prism request {request_key!r}: {review_due!r}"
        )
    if last_completed > cycles:
        raise PrismControlStateError(
            f"completed review cycle exceeds edit cycle for Prism request {request_key!r}"
        )
    if review_due:
        if not (last_completed < due_cycle <= cycles):
            raise PrismControlStateError(
                f"invalid due-cycle bounds for Prism request {request_key!r}"
            )
    elif due_cycle != 0:
        raise PrismControlStateError(
            f"nonzero due cycle while review is not due for Prism request {request_key!r}"
        )

    recorded_events = merged["recorded_edit_events"]
    if not isinstance(recorded_events, dict):
        raise PrismControlStateError(
            f"invalid recorded_edit_events for Prism request {request_key!r}"
        )
    for event_id, event_cycle in recorded_events.items():
        if not isinstance(event_id, str) or not event_id:
            raise PrismControlStateError(
                f"invalid recorded edit-event identity for Prism request {request_key!r}"
            )
        if (
            isinstance(event_cycle, bool)
            or not isinstance(event_cycle, int)
            or not (1 <= event_cycle <= cycles)
        ):
            raise PrismControlStateError(
                f"invalid recorded edit-event cycle for Prism request {request_key!r}"
            )

    protocol_version = merged["edit_lease_protocol_version"]
    if protocol_version not in {0, EDIT_LEASE_PROTOCOL_VERSION}:
        raise PrismControlStateError(
            f"unsupported edit-lease protocol for Prism request {request_key!r}: "
            f"{protocol_version!r}"
        )
    edit_leases = merged["edit_leases"]
    if not isinstance(edit_leases, dict):
        raise PrismControlStateError(
            f"invalid edit_leases for Prism request {request_key!r}"
        )
    for event_id, lease in edit_leases.items():
        if not isinstance(event_id, str) or not event_id:
            raise PrismControlStateError(
                f"invalid edit-lease identity for Prism request {request_key!r}"
            )
        if not isinstance(lease, dict):
            raise PrismControlStateError(
                f"invalid edit lease {event_id!r} for Prism request {request_key!r}"
            )
        fingerprint = lease.get("fingerprint")
        status = lease.get("status")
        leased_at = lease.get("leased_at")
        expires_at = lease.get("expires_at")
        if (
            not isinstance(fingerprint, str)
            or not re.fullmatch(r"[0-9a-f]{64}", fingerprint)
            or status not in EDIT_LEASE_STATUSES
            or isinstance(leased_at, bool)
            or not isinstance(leased_at, (int, float))
            or isinstance(expires_at, bool)
            or not isinstance(expires_at, (int, float))
            or expires_at < leased_at
        ):
            raise PrismControlStateError(
                f"invalid edit lease {event_id!r} for Prism request {request_key!r}"
            )
        committed_cycle = lease.get("committed_cycle")
        if status == "committed":
            if (
                isinstance(committed_cycle, bool)
                or not isinstance(committed_cycle, int)
                or not (1 <= committed_cycle <= cycles)
                or recorded_events.get(event_id) != committed_cycle
            ):
                raise PrismControlStateError(
                    f"invalid committed edit lease {event_id!r} for Prism request "
                    f"{request_key!r}"
                )
        elif committed_cycle is not None:
            raise PrismControlStateError(
                f"uncommitted edit lease {event_id!r} carries a committed cycle"
            )
        cancellation_reason = lease.get("cancellation_reason")
        if status == "cancelled" and cancellation_reason not in EDIT_LEASE_CANCELLATION_REASONS:
            raise PrismControlStateError(
                f"invalid cancellation reason for edit lease {event_id!r}"
            )
        if lease.get("purpose", "feature_edit") not in {
            "feature_edit",
            "persona_review_record",
        }:
            raise PrismControlStateError(
                f"invalid purpose for edit lease {event_id!r}"
            )


def _validate_control_state(control_state: Any) -> dict[str, Any]:
    """Fail closed when the authoritative state has the wrong shape."""

    if not isinstance(control_state, dict):
        raise PrismControlStateError("Prism control state root must be an object")
    requests = control_state.get("requests")
    if not isinstance(requests, dict):
        raise PrismControlStateError("Prism control state requests must be an object")
    for request_key, review_state in requests.items():
        if not isinstance(request_key, str) or not request_key:
            raise PrismControlStateError("Prism request keys must be non-empty strings")
        if not isinstance(review_state, dict):
            raise PrismControlStateError(
                f"Prism review state for {request_key!r} must be an object"
            )
        _validate_review_state(review_state, request_key=request_key)
    return control_state


def _load_control_state(repo_root: Path) -> dict[str, Any]:
    """Load the repo-local Prism control state."""

    state_path = _control_state_path(repo_root)
    try:
        with state_path.open("r", encoding="utf-8") as handle:
            loaded = json.load(handle)
    except FileNotFoundError:
        return {"requests": {}}
    except (json.JSONDecodeError, UnicodeDecodeError) as exc:
        raise PrismControlStateError(
            f"invalid authoritative Prism control state at {state_path}: {exc}"
        ) from exc
    return _validate_control_state(loaded)


def _save_control_state(repo_root: Path, control_state: dict[str, Any]) -> None:
    """Persist the repo-local Prism control state."""

    _validate_control_state(control_state)
    state_path = _control_state_path(repo_root)
    _atomic_write_text(
        state_path,
        json.dumps(control_state, indent=2, sort_keys=True) + "\n",
    )


def _review_state_for(control_state: dict[str, Any], slug: str | None) -> dict[str, Any]:
    """Return the per-request review-cycle state, creating defaults as needed."""

    key = slug or UNSCOPED_REQUEST_KEY
    requests = control_state.setdefault("requests", {})
    raw_state = requests.get(key)
    if not isinstance(raw_state, dict):
        raw_state = {}

    review_state = _default_review_state()
    review_state.update(raw_state)
    requests[key] = review_state
    return review_state


def _persona_review_artifact_path(repo_root: Path, slug: str | None) -> Path | None:
    """Return the active persona-review artifact path, if a request is active."""

    if not slug:
        return None
    return repo_root / ".prism" / slug / PERSONA_REVIEW_ARTIFACT


def _render_request_template(template_path: Path, output_path: Path, slug: str) -> None:
    """Render a request-scoped template by replacing the slug placeholder."""

    rendered = template_path.read_text(encoding="utf-8").replace("<request-slug>", slug)
    _atomic_write_text(output_path, rendered, default_mode=0o644)


def _replace_bullet_fields(text: str, label_to_value: dict[str, str]) -> str:
    """Replace simple `- Label: value` fields in a Markdown control file."""

    replacements = {
        _normalize_field_name(label): (label, value)
        for label, value in label_to_value.items()
    }
    lines = text.splitlines()
    seen: set[str] = set()

    for index, line in enumerate(lines):
        match = TODO_FIELD_PATTERN.match(line)
        if not match:
            continue
        key = _normalize_field_name(match.group(1))
        if key not in replacements:
            continue
        label, value = replacements[key]
        lines[index] = f"- {label}: {value}"
        seen.add(key)

    missing = [pair for key, pair in replacements.items() if key not in seen]
    if missing:
        if lines and lines[-1] != "":
            lines.append("")
        for label, value in missing:
            lines.append(f"- {label}: {value}")

    return "\n".join(lines) + "\n"


def _ensure_todo_review_section(todo_path: Path) -> str:
    """Return to-do contents with the persona-review section present."""

    if not todo_path.exists():
        return ""

    text = todo_path.read_text(encoding="utf-8")
    if "## Persona Review Control" in text:
        return text

    suffix = "" if text.endswith("\n") else "\n"
    return f"{text}{suffix}\n{PERSONA_REVIEW_SECTION}\n"


def _ensure_persona_review_artifact(repo_root: Path, slug: str | None) -> Path | None:
    """Create the persona-review artifact when a request workspace exists."""

    artifact_path = _persona_review_artifact_path(repo_root, slug)
    if artifact_path is None:
        return None

    request_root = artifact_path.parent
    if not request_root.exists():
        return None

    if artifact_path.exists():
        return artifact_path

    template_path = repo_root / "prism_me" / "shared" / "templates" / PERSONA_REVIEW_ARTIFACT
    if not template_path.exists():
        return None

    _render_request_template(template_path, artifact_path, slug)
    return artifact_path


def _update_persona_review_artifact(
    artifact_path: Path | None,
    *,
    status: str | None = None,
    trigger_cycle: int | None = None,
    trigger_source: str | None = None,
    review_due_state: str | None = None,
) -> None:
    """Update the simple control fields in the persona-review artifact."""

    if artifact_path is None or not artifact_path.exists():
        return

    updates: dict[str, str] = {}
    if status is not None:
        updates["Status"] = f"`{status}`"
    if trigger_cycle is not None:
        updates["Trigger Cycle"] = f"`{trigger_cycle}`"
    if trigger_source is not None:
        updates["Trigger source"] = trigger_source
    if review_due_state is not None:
        updates["Review due state"] = review_due_state
    if not updates:
        return

    text = artifact_path.read_text(encoding="utf-8")
    updated = _replace_bullet_fields(text, updates)
    _atomic_write_text(artifact_path, updated, default_mode=0o644)


def _sync_persona_review_controls_from_state(
    repo_root: Path,
    slug: str | None,
    review_state: dict[str, Any],
) -> None:
    """Sync Markdown projections from the exact locked state snapshot."""

    todo_path = repo_root / "to-do.md"
    if not todo_path.exists():
        return

    cycles = int(review_state.get("edit_write_cycles", 0))
    last_completed = int(review_state.get("last_completed_review_cycle", 0))
    review_due = bool(review_state.get("review_due", False) and slug)
    next_cycle = last_completed + PERSONA_REVIEW_THRESHOLD
    artifact_display = (
        f".prism/{slug}/{PERSONA_REVIEW_ARTIFACT}" if slug else ""
    )

    if review_due:
        todo_status = f"`due at cycle {int(review_state.get('review_due_cycle', cycles))}`"
    elif cycles == 0:
        todo_status = "`idle`"
    elif cycles == last_completed:
        todo_status = f"`completed through cycle {last_completed}`"
    else:
        todo_status = f"`tracking toward cycle {next_cycle}`"

    text = _ensure_todo_review_section(todo_path)
    updated = _replace_bullet_fields(
        text,
        {
            "Request slug": slug or "",
            "Workspace": f".prism/{slug}" if slug else "",
            "Edit/write cycles recorded": f"`{cycles}`",
            "Last completed persona review cycle": f"`{last_completed}`",
            "Next automatic persona review": f"`{next_cycle}`",
            "Persona review due": "`yes`" if review_due else "`no`",
            "Persona review artifact": artifact_display,
            "Persona review TODO status": todo_status,
            "Persona review": artifact_display,
        },
    )
    _atomic_write_text(todo_path, updated, default_mode=0o644)


def _sync_persona_review_controls(repo_root: Path, slug: str | None) -> None:
    """Lock and reconcile root/persona-review projections from authoritative state."""

    with _control_state_lock(repo_root):
        control_state = _load_control_state(repo_root)
        review_state = _review_state_for(control_state, slug)
        _ensure_persona_review_artifact(repo_root, slug)
        _sync_persona_review_controls_from_state(repo_root, slug, review_state)


def _record_edit_cycle(
    repo_root: Path,
    slug: str | None,
    *,
    event_id: str | None = None,
) -> tuple[dict[str, Any], bool, bool]:
    """Atomically record one uniquely identified edit/write cycle."""

    with _control_state_lock(repo_root):
        control_state = _load_control_state(repo_root)
        review_state = _review_state_for(control_state, slug)
        triggered, recorded = _record_edit_cycle_locked(
            review_state,
            slug,
            event_id=event_id,
        )

        _save_control_state(repo_root, control_state)

        if slug:
            artifact_path = _ensure_persona_review_artifact(repo_root, slug)
            if triggered:
                _update_persona_review_artifact(
                    artifact_path,
                    status="review-due",
                    trigger_cycle=int(review_state["review_due_cycle"]),
                    trigger_source="control-stack edit/write threshold",
                    review_due_state="due",
                )
            _sync_persona_review_controls_from_state(repo_root, slug, review_state)

        return dict(review_state), triggered, recorded


def _record_edit_cycle_locked(
    review_state: dict[str, Any],
    slug: str | None,
    *,
    event_id: str | None,
) -> tuple[bool, bool]:
    """Record one cycle in a caller-held control-state transaction."""

    recorded_events = review_state.setdefault("recorded_edit_events", {})
    if event_id is not None and event_id in recorded_events:
        return False, False

    review_state["edit_write_cycles"] = int(review_state.get("edit_write_cycles", 0)) + 1
    review_state["last_event_at"] = _utc_now()
    if event_id is not None:
        recorded_events[event_id] = int(review_state["edit_write_cycles"])

    threshold_cycle = (
        int(review_state.get("last_completed_review_cycle", 0))
        + PERSONA_REVIEW_THRESHOLD
    )
    triggered = bool(
        slug
        and not bool(review_state.get("review_due", False))
        and int(review_state["edit_write_cycles"]) >= threshold_cycle
    )
    if triggered:
        review_state["review_due"] = True
        review_state["review_due_cycle"] = threshold_cycle
    return triggered, True


def _edit_fingerprint(payload: dict[str, Any]) -> str:
    """Bind a lease to the exact edit tool and canonical structured input."""

    authority = {
        "tool_name": _hook_tool_name(payload).strip().lower(),
        "tool_input": _hook_tool_input(payload),
    }
    encoded = json.dumps(
        authority,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def _expire_edit_leases(review_state: dict[str, Any], *, now: float) -> bool:
    """Make expired uncertainty explicit instead of silently freeing a slot."""

    changed = False
    for lease in review_state.setdefault("edit_leases", {}).values():
        if lease.get("status") == "leased" and float(lease["expires_at"]) <= now:
            lease["status"] = "expired_indeterminate"
            lease["resolved_at"] = now
            changed = True
    return changed


def _indeterminate_edit_lease_ids(review_state: dict[str, Any]) -> list[str]:
    """Return unresolved leases whose mutation outcome is unknown."""

    return sorted(
        event_id
        for event_id, lease in review_state.setdefault("edit_leases", {}).items()
        if lease.get("status") == "expired_indeterminate"
    )


def _reserve_edit_lease(
    repo_root: Path,
    slug: str | None,
    *,
    event_id: str,
    fingerprint: str,
    now: float | None = None,
    ttl_seconds: float = EDIT_LEASE_TTL_SECONDS,
    purpose: str = "feature_edit",
) -> tuple[dict[str, Any], dict[str, Any], bool]:
    """Atomically reserve one threshold-aware Edit/Write cycle capability."""

    if not slug:
        raise PrismEditLeaseError("an active Prism request is required before editing")
    if not event_id:
        raise PrismEditLeaseError("Edit/Write hooks require a stable event identity")
    if not re.fullmatch(r"[0-9a-f]{64}", fingerprint):
        raise PrismEditLeaseError("Edit/Write hooks require a canonical fingerprint")
    if ttl_seconds <= 0:
        raise PrismEditLeaseError("edit-lease TTL must be positive")
    if purpose not in {"feature_edit", "persona_review_record"}:
        raise PrismEditLeaseError(f"unregistered edit-lease purpose: {purpose!r}")
    instant = time.time() if now is None else now

    with _control_state_lock(repo_root):
        control_state = _load_control_state(repo_root)
        review_state = _review_state_for(control_state, slug)
        if int(review_state.get("edit_lease_protocol_version", 0)) == 0:
            review_state["edit_lease_protocol_version"] = EDIT_LEASE_PROTOCOL_VERSION
        expired = _expire_edit_leases(review_state, now=instant)
        leases = review_state.setdefault("edit_leases", {})
        existing = leases.get(event_id)
        if existing is not None:
            if existing.get("fingerprint") != fingerprint:
                raise PrismEditLeaseError(
                    "edit event identity was reused with different tool input"
                )
            if existing.get("purpose", "feature_edit") != purpose:
                raise PrismEditLeaseError(
                    "edit event identity was reused for a different mutation purpose"
                )
            if existing.get("status") in {"leased", "committed"}:
                _save_control_state(repo_root, control_state)
                return dict(review_state), dict(existing), False
            raise PrismEditLeaseError(
                f"edit event {event_id!r} is already {existing.get('status')}"
            )

        indeterminate = _indeterminate_edit_lease_ids(review_state)
        if indeterminate:
            if expired:
                _save_control_state(repo_root, control_state)
            raise PrismEditLeaseError(
                "unresolved expired edit leases block new mutations: "
                + ", ".join(indeterminate)
            )
        review_due = bool(review_state.get("review_due", False))
        if review_due and purpose != "persona_review_record":
            raise PrismEditLeaseError("persona review is due before another feature edit")

        active_leases = sum(
            lease.get("status") == "leased" for lease in leases.values()
        )
        if review_due and active_leases:
            raise PrismEditLeaseError(
                "another persona-review recording edit is already leased"
            )
        threshold_cycle = (
            int(review_state.get("last_completed_review_cycle", 0))
            + PERSONA_REVIEW_THRESHOLD
        )
        if (
            not review_due
            and int(review_state.get("edit_write_cycles", 0)) + active_leases
            >= threshold_cycle
        ):
            raise PrismEditLeaseError(
                "the next review-boundary edit slot is already leased"
            )

        lease = {
            "fingerprint": fingerprint,
            "status": "leased",
            "leased_at": instant,
            "expires_at": instant + ttl_seconds,
            "committed_cycle": None,
            "purpose": purpose,
        }
        leases[event_id] = lease
        _save_control_state(repo_root, control_state)
        return dict(review_state), dict(lease), True


def _commit_edit_lease(
    repo_root: Path,
    slug: str | None,
    *,
    event_id: str,
    fingerprint: str,
    now: float | None = None,
    allow_protocol_bootstrap: bool = False,
) -> tuple[dict[str, Any], bool, bool]:
    """Commit an exact lease, accepting one activation edit for migration."""

    if not slug:
        raise PrismEditLeaseError("an active Prism request is required before editing")
    if not event_id:
        raise PrismEditLeaseError("Edit/Write hooks require a stable event identity")
    instant = time.time() if now is None else now

    with _control_state_lock(repo_root):
        control_state = _load_control_state(repo_root)
        review_state = _review_state_for(control_state, slug)
        protocol_version = int(review_state.get("edit_lease_protocol_version", 0))
        leases = review_state.setdefault("edit_leases", {})
        existing = leases.get(event_id)

        if protocol_version == 0:
            if not allow_protocol_bootstrap:
                raise PrismEditLeaseError("edit-lease protocol has not been activated")
            review_state["edit_lease_protocol_version"] = EDIT_LEASE_PROTOCOL_VERSION
            existing = {
                "fingerprint": fingerprint,
                "status": "leased",
                "leased_at": instant,
                "expires_at": instant,
                "committed_cycle": None,
                "bootstrap": True,
            }
            leases[event_id] = existing
        elif existing is None:
            raise PrismEditLeaseError("Edit/Write post-hook has no matching pre-edit lease")

        if existing.get("fingerprint") != fingerprint:
            raise PrismEditLeaseError("Edit/Write post-hook fingerprint does not match its lease")
        if existing.get("status") == "committed":
            return dict(review_state), False, False
        if existing.get("status") == "cancelled":
            raise PrismEditLeaseError("a cancelled edit lease cannot be committed")
        if existing.get("status") not in {"leased", "expired_indeterminate"}:
            raise PrismEditLeaseError("edit lease has an invalid commit state")

        triggered, recorded = _record_edit_cycle_locked(
            review_state,
            slug,
            event_id=event_id,
        )
        existing["status"] = "committed"
        existing["committed_cycle"] = review_state["recorded_edit_events"][event_id]
        existing["resolved_at"] = instant
        _save_control_state(repo_root, control_state)

        artifact_path = _ensure_persona_review_artifact(repo_root, slug)
        if triggered:
            _update_persona_review_artifact(
                artifact_path,
                status="review-due",
                trigger_cycle=int(review_state["review_due_cycle"]),
                trigger_source="control-stack edit/write threshold",
                review_due_state="due",
            )
        _sync_persona_review_controls_from_state(repo_root, slug, review_state)
        return dict(review_state), triggered, recorded


def _cancel_edit_lease(
    repo_root: Path,
    slug: str | None,
    *,
    event_id: str,
    fingerprint: str,
    reason: str,
    now: float | None = None,
) -> tuple[dict[str, Any], bool]:
    """Resolve a known no-mutation outcome using a closed trusted reason set."""

    if reason not in EDIT_LEASE_CANCELLATION_REASONS:
        raise PrismEditLeaseError(f"untrusted edit-lease cancellation reason: {reason!r}")
    if not slug:
        raise PrismEditLeaseError("an active Prism request is required")
    instant = time.time() if now is None else now
    with _control_state_lock(repo_root):
        control_state = _load_control_state(repo_root)
        review_state = _review_state_for(control_state, slug)
        _expire_edit_leases(review_state, now=instant)
        lease = review_state.setdefault("edit_leases", {}).get(event_id)
        if lease is None:
            raise PrismEditLeaseError("cannot cancel an unknown edit lease")
        if lease.get("fingerprint") != fingerprint:
            raise PrismEditLeaseError("edit-lease cancellation fingerprint mismatch")
        if lease.get("status") == "cancelled":
            if lease.get("cancellation_reason") != reason:
                raise PrismEditLeaseError("edit lease was cancelled for a different reason")
            return dict(review_state), False
        if lease.get("status") == "committed":
            raise PrismEditLeaseError("a committed edit lease cannot be cancelled")
        if lease.get("status") not in {"leased", "expired_indeterminate"}:
            raise PrismEditLeaseError("edit lease has an invalid cancellation state")
        lease["status"] = "cancelled"
        lease["cancellation_reason"] = reason
        lease["resolved_at"] = instant
        _save_control_state(repo_root, control_state)
        return dict(review_state), True


def _mark_persona_review_complete(
    repo_root: Path,
    slug: str | None,
    *,
    reviewed_through_cycle: int | None = None,
) -> tuple[dict[str, Any] | None, Path | None, bool]:
    """Atomically complete one due review; repeated completion is a no-op."""

    if not slug:
        return None, None, False

    with _control_state_lock(repo_root):
        control_state = _load_control_state(repo_root)
        review_state = _review_state_for(control_state, slug)
        artifact_path = _ensure_persona_review_artifact(repo_root, slug)
        if not bool(review_state.get("review_due", False)):
            _sync_persona_review_controls_from_state(repo_root, slug, review_state)
            return dict(review_state), artifact_path, False

        current_cycle = int(review_state.get("edit_write_cycles", 0))
        due_cycle = int(review_state.get("review_due_cycle", 0))
        completed_cycle = current_cycle if reviewed_through_cycle is None else reviewed_through_cycle
        if isinstance(completed_cycle, bool) or not isinstance(completed_cycle, int):
            raise PrismControlStateError("reviewed-through cycle must be an integer")
        if not (due_cycle <= completed_cycle <= current_cycle):
            raise PrismControlStateError(
                "reviewed-through cycle must cover the due boundary without exceeding the current cycle"
            )

        review_state["last_completed_review_cycle"] = completed_cycle
        review_state["review_due"] = False
        review_state["review_due_cycle"] = 0
        review_state["last_completion_at"] = _utc_now()
        _save_control_state(repo_root, control_state)

        _update_persona_review_artifact(
            artifact_path,
            status="completed",
            trigger_cycle=completed_cycle,
            review_due_state="completed",
        )
        _sync_persona_review_controls_from_state(repo_root, slug, review_state)
        return dict(review_state), artifact_path, True


def _discover_request_slug(repo_root: Path, explicit_slug: str | None = None) -> str | None:
    """Determine the active request slug from explicit input, to-do, or workspace state."""

    if explicit_slug:
        return explicit_slug

    todo_fields = _parse_todo_fields(repo_root / "to-do.md")
    todo_slug = todo_fields.get("request_slug", "").strip()
    if todo_slug:
        return todo_slug

    prism_root = repo_root / ".prism"
    if not prism_root.exists():
        return None

    slugs = sorted(path.name for path in prism_root.iterdir() if path.is_dir())
    if len(slugs) == 1:
        return slugs[0]
    return None


def _artifact_state(workspace_path: Path) -> tuple[list[ArtifactSpec], list[ArtifactSpec]]:
    """Return the present and missing required artifacts for a workspace."""

    present: list[ArtifactSpec] = []
    missing_required: list[ArtifactSpec] = []
    for spec in ARTIFACT_SPECS:
        if (workspace_path / spec.filename).exists():
            present.append(spec)
        elif spec.required:
            missing_required.append(spec)
    return present, missing_required


SEMANTIC_ARTIFACT_GATES: tuple[
    tuple[str, str, str, dict[str, frozenset[str]]], ...
] = (
    (
        "05-execution-log.md",
        "execution",
        "prism-implementation-driver",
        {"status": frozenset({"completed"})},
    ),
    (
        "05b-refinement-loop.md",
        "reflective-refinement",
        "prism-reflective-refinement-loop",
        {"status": frozenset({"completed"})},
    ),
    (
        "05c-test-evidence.md",
        "test-evidence",
        "prism-generative-validation-runner",
        {"status": frozenset({"completed", "accepted"})},
    ),
    (
        "06-verification.md",
        "evaluation",
        "prism-spec-verification-critic",
        {
            "status": frozenset({"completed", "accepted"}),
            "release_gate": frozenset({"pass", "passed", "release"}),
        },
    ),
    (
        "07-handoff.md",
        "handoff",
        "prism-integration-handoff",
        {
            "status": frozenset({"completed", "accepted"}),
            "readiness": frozenset({"ready"}),
        },
    ),
)


def _normalize_metadata_value(value: str) -> str:
    """Normalize one top-block Markdown control value without reading prose."""

    normalized = value.strip()
    if normalized.startswith("`") and normalized.endswith("`") and len(normalized) >= 2:
        normalized = normalized[1:-1].strip()
    return normalized.lower().replace("_", "-").replace(" ", "-")


def _top_metadata_fields(path: Path) -> tuple[dict[str, str], list[str]]:
    """Parse unique bullet fields before the first level-two Markdown section."""

    fields: dict[str, str] = {}
    problems: list[str] = []
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except (OSError, UnicodeDecodeError) as exc:
        return {}, [f"{path.name}: unreadable metadata: {exc}"]
    for line in lines:
        if line.startswith("## "):
            break
        match = TODO_FIELD_PATTERN.match(line)
        if not match:
            continue
        key = _normalize_field_name(match.group(1))
        if key in fields:
            problems.append(f"{path.name}: duplicate top metadata field {key!r}")
            continue
        fields[key] = _normalize_metadata_value(match.group(2))
    return fields, problems


def _semantic_artifact_readiness(
    workspace_path: Path,
) -> tuple[ArtifactSpec | None, list[str], list[str]]:
    """Return the first semantically unfinished artifact and complete diagnostics."""

    first_unready: ArtifactSpec | None = None
    unready_artifacts: list[str] = []
    problems: list[str] = []
    for filename, stage, skill, requirements in SEMANTIC_ARTIFACT_GATES:
        path = workspace_path / filename
        if not path.exists():
            continue
        fields, parse_problems = _top_metadata_fields(path)
        reasons = list(parse_problems)
        for field, accepted_values in requirements.items():
            actual = fields.get(field)
            if actual not in accepted_values:
                rendered = ", ".join(sorted(accepted_values))
                reasons.append(
                    f"{filename}: {field!r} must be one of [{rendered}], got "
                    f"{actual if actual is not None else '<missing>'!r}"
                )
        if reasons:
            unready_artifacts.append(filename)
            problems.extend(reasons)
            if first_unready is None:
                first_unready = ArtifactSpec(filename, stage, skill)
    return first_unready, unready_artifacts, problems


def _format_workspace_path(repo_root: Path, workspace_path: Path | None) -> str:
    """Format a repo-relative workspace path for human output."""

    if workspace_path is None:
        return "(not initialized)"
    try:
        return str(workspace_path.relative_to(repo_root))
    except ValueError:
        return str(workspace_path)


def collect_state(repo_root: Path, explicit_slug: str | None = None) -> dict[str, Any]:
    """Compute the control state for the active Prism request, if any."""

    todo_path = repo_root / "to-do.md"
    todo_fields = _parse_todo_fields(todo_path)
    slug = _discover_request_slug(repo_root, explicit_slug)
    workspace_path = repo_root / ".prism" / slug if slug else None
    workspace_exists = workspace_path.exists() if workspace_path else False

    present_specs: list[ArtifactSpec] = []
    missing_specs: list[ArtifactSpec] = []
    if workspace_exists and workspace_path is not None:
        present_specs, missing_specs = _artifact_state(workspace_path)

    next_spec = missing_specs[0] if missing_specs else None
    unready_artifacts: list[str] = []
    artifact_readiness_problems: list[str] = []
    current_stage = "workspace-not-initialized"
    if workspace_exists:
        if next_spec is None and workspace_path is not None:
            next_spec, unready_artifacts, artifact_readiness_problems = (
                _semantic_artifact_readiness(workspace_path)
            )
        current_stage = next_spec.stage if next_spec else "handoff-complete"

    control_state = _load_control_state(repo_root)
    review_state = _review_state_for(control_state, slug)
    edit_cycles = int(review_state.get("edit_write_cycles", 0)) if slug else 0
    last_persona_review_cycle = int(review_state.get("last_completed_review_cycle", 0)) if slug else 0
    persona_review_due = bool(review_state.get("review_due", False) and workspace_exists and slug)
    persona_review_artifact = (
        f".prism/{slug}/{PERSONA_REVIEW_ARTIFACT}" if slug and workspace_exists else None
    )
    edit_leases = review_state.get("edit_leases", {})
    lease_observation_time = time.time()
    outstanding_edit_leases = sorted(
        event_id
        for event_id, lease in edit_leases.items()
        if (
            isinstance(lease, dict)
            and lease.get("status") == "leased"
            and float(lease.get("expires_at", 0.0)) > lease_observation_time
        )
    )
    indeterminate_edit_leases = sorted(
        event_id
        for event_id, lease in edit_leases.items()
        if isinstance(lease, dict)
        and (
            lease.get("status") == "expired_indeterminate"
            or (
                lease.get("status") == "leased"
                and float(lease.get("expires_at", 0.0)) <= lease_observation_time
            )
        )
    )

    if persona_review_due:
        current_stage = "persona-review-due"
        next_spec = ArtifactSpec(
            PERSONA_REVIEW_ARTIFACT,
            "persona-review",
            PERSONA_REVIEW_SKILL,
            required=False,
        )

    state = {
        "repo_root": str(repo_root),
        "todo_path": str(todo_path),
        "todo_fields": todo_fields,
        "request_slug": slug,
        "workspace_exists": workspace_exists,
        "workspace_path": str(workspace_path) if workspace_path else None,
        "workspace_path_display": _format_workspace_path(repo_root, workspace_path),
        "present_artifacts": [spec.filename for spec in present_specs],
        "missing_required_artifacts": [spec.filename for spec in missing_specs],
        "current_stage": current_stage,
        "next_skill": next_spec.skill if next_spec else None,
        "next_artifact": next_spec.filename if next_spec else None,
        "unready_artifacts": unready_artifacts,
        "artifact_readiness_problems": artifact_readiness_problems,
        "handoff_ready": bool(workspace_exists and not missing_specs and not next_spec),
        "coverage_checklist_present": bool(workspace_path and (workspace_path / "00-skill-coverage-checklist.md").exists()),
        "reasoning_log_present": bool(workspace_path and (workspace_path / "reasoning-log.md").exists()),
        "edit_write_cycles": edit_cycles,
        "last_persona_review_cycle": last_persona_review_cycle,
        "next_persona_review_cycle": last_persona_review_cycle + PERSONA_REVIEW_THRESHOLD,
        "persona_review_due": persona_review_due,
        "persona_review_due_cycle": int(review_state.get("review_due_cycle", 0)) if slug else 0,
        "persona_review_artifact": persona_review_artifact,
        "edit_lease_protocol_version": int(
            review_state.get("edit_lease_protocol_version", 0)
        ),
        "outstanding_edit_leases": outstanding_edit_leases,
        "indeterminate_edit_leases": indeterminate_edit_leases,
    }

    if slug:
        state["todo_sync_ok"] = bool(
            todo_fields.get("request_slug", "").strip() == slug
            and todo_fields.get("workspace", "").strip() in ("", f".prism/{slug}/", f".prism/{slug}")
        )
    else:
        state["todo_sync_ok"] = None
    return state


def _format_todo_sync(value: bool | None) -> str:
    """Render the to-do synchronization state for human output."""

    if value is None:
        return "not-applicable"
    return "ok" if value else "needs attention"


def format_status_text(state: dict[str, Any]) -> str:
    """Render the current Prism state in a compact human-readable form."""

    lines = [
        f"Repo: {state['repo_root']}",
        f"Request slug: {state['request_slug'] or '(none)'}",
        f"Workspace: {state['workspace_path_display']}",
        f"Current stage: {state['current_stage']}",
        f"Next skill: {state['next_skill'] or '(none)'}",
        f"Next artifact: {state['next_artifact'] or '(none)'}",
        f"to-do sync: {_format_todo_sync(state['todo_sync_ok'])}",
        f"Edit/write cycles: {state['edit_write_cycles']}",
        f"Last persona review cycle: {state['last_persona_review_cycle']}",
        f"Next automatic persona review: {state['next_persona_review_cycle']}",
        f"Persona review due: {'yes' if state['persona_review_due'] else 'no'}",
    ]
    missing = state["missing_required_artifacts"]
    if missing:
        lines.append("Missing required artifacts:")
        for artifact in missing:
            lines.append(f"- {artifact}")
    else:
        lines.append("Missing required artifacts: none")
    if state["unready_artifacts"]:
        lines.append("Semantically unready artifacts:")
        for artifact in state["unready_artifacts"]:
            lines.append(f"- {artifact}")
    lines.append(f"Handoff ready: {'yes' if state['handoff_ready'] else 'no'}")
    if state["outstanding_edit_leases"]:
        lines.append(
            "Outstanding edit leases: " + ", ".join(state["outstanding_edit_leases"])
        )
    if state["indeterminate_edit_leases"]:
        lines.append(
            "Indeterminate edit leases: " + ", ".join(state["indeterminate_edit_leases"])
        )
    return "\n".join(lines)


def build_additional_context(state: dict[str, Any]) -> str:
    """Create short developer context that the hooks can inject into Codex."""

    base = [
        "This repository uses the Prism ME control stack.",
        "Start request work with explicit `prism-spec-orchestrator`.",
        "Check request state with `python3 prism_me/scripts/prism_control.py status`.",
        "Use `python3 prism_me/scripts/prism_control.py next` when the next stage is unclear.",
    ]
    if not state["workspace_exists"]:
        base.append("No active Prism workspace is initialized yet. Use `bash prism_me/scripts/init_request.sh <request-slug>` before deeper skill work.")
        return " ".join(base)

    base.append(
        f"Active request slug: `{state['request_slug']}`. "
        f"Current stage: `{state['current_stage']}`. "
        f"Next skill: `{state['next_skill']}`. "
        f"Next artifact: `{state['next_artifact']}`."
    )
    base.append(
        f"Edit/write cycles: `{state['edit_write_cycles']}`. "
        f"Last persona review cycle: `{state['last_persona_review_cycle']}`. "
        f"Next automatic review: `{state['next_persona_review_cycle']}`."
    )
    if state["persona_review_due"]:
        base.append(
            f"Persona review is due at cycle `{state['persona_review_due_cycle']}`. "
            f"Run `{PERSONA_REVIEW_SKILL}`, update `{state['persona_review_artifact']}`, "
            "sync `to-do.md`, then run `python3 prism_me/scripts/prism_control.py review-complete`."
        )
    base.append("Keep `to-do.md` and `.prism/<request-slug>/00-skill-coverage-checklist.md` synchronized with the real stage before claiming completion.")
    return " ".join(base)


def _hook_output(event_name: str, additional_context: str, system_message: str | None = None) -> dict[str, Any]:
    """Build a valid hook JSON payload for context-injection events."""

    output: dict[str, Any] = {
        "hookSpecificOutput": {
            "hookEventName": event_name,
            "additionalContext": additional_context,
        }
    }
    if system_message:
        output["systemMessage"] = system_message
    return output


def _deny(reason: str) -> dict[str, Any]:
    """Build a valid deny payload for shell interception hooks."""

    return {
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "deny",
            "permissionDecisionReason": reason,
        }
    }


def _is_destructive_command(command: str) -> str | None:
    """Return a deny reason when a command matches a blocked destructive pattern."""

    normalized = command.strip()
    if re.search(r"(^|[;&|]\s*)rm\b", normalized) and any(
        hint in command for hint in CONTROL_SURFACE_DELETE_HINTS
    ):
        return "Blocked deletion of Prism control surfaces."

    for pattern, reason in DESTRUCTIVE_PATTERNS:
        if pattern.search(normalized):
            return reason
    return None


def _is_control_command(command: str) -> bool:
    """Return whether the command is an approved Prism control-plane command."""

    return any(
        token in command
        for token in (
            "prism_me/scripts/prism_control.py",
            "prism_me/scripts/init_request.sh",
            "prism_me/scripts/init_external_harmonization.sh",
            "prism_me/scripts/init_vscode_onboarding.sh",
        )
    )


def _is_direct_prism_mutation(command: str) -> bool:
    """Heuristically detect ad hoc shell writes into Prism control surfaces."""

    if _is_control_command(command):
        return False

    touches_control_surface = any(hint in command for hint in DIRECT_PRISM_WRITE_HINTS)
    if not touches_control_surface:
        return False

    return any(operator in command for operator in DIRECT_WRITE_OPERATORS)


def _looks_like_test_command(command: str) -> bool:
    """Return whether the shell command appears to run a test or validation step."""

    stripped = command.strip()
    return any(stripped.startswith(prefix) for prefix in TEST_COMMAND_PREFIXES)


def _prompt_requests_bypass(prompt: str) -> bool:
    """Detect blunt instructions to bypass the Prism control surfaces."""

    lowered = prompt.lower()
    keywords = ("skip", "ignore", "bypass", "disable")
    targets = ("prism", "orchestrator", "coverage checklist", "to-do.md", "verification", "handoff")
    return any(word in lowered for word in keywords) and any(target in lowered for target in targets)


def _prompt_needs_prism_context(prompt: str) -> bool:
    """Detect prompts that are likely about skill work or Prism-governed changes."""

    return bool(
        re.search(
            r"\b(prism|skill|skills|agent contract|quality criteria|slice plan|test strategy|handoff|coverage checklist)\b",
            prompt,
            re.IGNORECASE,
        )
    )


def _load_hook_payload() -> dict[str, Any]:
    """Read one JSON object from stdin for hook execution."""

    raw = sys.stdin.read().strip()
    return json.loads(raw) if raw else {}


def _hook_tool_input(payload: dict[str, Any]) -> dict[str, Any]:
    """Return the structured tool input from a hook payload."""

    tool_input = payload.get("tool_input", {})
    return tool_input if isinstance(tool_input, dict) else {}


def _hook_tool_name(payload: dict[str, Any]) -> str:
    """Return the tool name from a hook payload when available."""

    for key in ("tool_name", "toolName", "tool", "name"):
        value = payload.get(key)
        if isinstance(value, str) and value:
            return value
    return ""


def _hook_event_id(payload: dict[str, Any]) -> str | None:
    """Extract an explicit delivery identity; never guess from mutable contents."""

    for key in ("event_id", "hook_event_id", "invocation_id"):
        value = payload.get(key)
        if isinstance(value, str) and value:
            return f"{key}:{value}"

    tool_use_id = payload.get("tool_use_id") or payload.get("toolUseId")
    if not isinstance(tool_use_id, str) or not tool_use_id:
        return None
    session_id = payload.get("session_id") or payload.get("sessionId") or "unspecified-session"
    if not isinstance(session_id, str) or not session_id:
        session_id = "unspecified-session"
    return f"session_tool:{session_id}:{tool_use_id}"


def _looks_like_edit_or_write_tool(payload: dict[str, Any]) -> bool:
    """Heuristically detect edit/write-style hook payloads."""

    tool_name = _hook_tool_name(payload).lower()
    if tool_name in {"edit", "write", "multiedit"}:
        return True

    tool_input = _hook_tool_input(payload)
    edit_keys = {"file_path", "path", "content", "old_string", "new_string"}
    return any(key in tool_input for key in edit_keys) and "command" not in tool_input


def _is_persona_review_recording_edit(
    payload: dict[str, Any], repo_root: Path, slug: str | None
) -> bool:
    """Recognize only the three exact files needed to record a due review."""

    if not slug:
        return False
    raw_path = _hook_tool_input(payload).get("file_path")
    if not isinstance(raw_path, str) or not raw_path.strip():
        raw_path = _hook_tool_input(payload).get("path")
    if not isinstance(raw_path, str) or not raw_path.strip():
        return False
    candidate = Path(raw_path)
    if not candidate.is_absolute():
        candidate = repo_root / candidate
    candidate = candidate.resolve()
    allowed = {
        (repo_root / ".prism" / slug / PERSONA_REVIEW_ARTIFACT).resolve(),
        (repo_root / ".prism" / slug / "reasoning-log.md").resolve(),
        (repo_root / "to-do.md").resolve(),
    }
    return candidate in allowed


def command_status(args: argparse.Namespace) -> int:
    """Print the current Prism control state."""

    repo_root = _repo_root_from(Path(args.repo_root or os.getcwd()))
    state = collect_state(repo_root, args.request_slug)
    if args.json:
        json.dump(state, sys.stdout, indent=2, sort_keys=True)
        sys.stdout.write("\n")
    else:
        print(format_status_text(state))
    return 0


def command_next(args: argparse.Namespace) -> int:
    """Print the next recommended Prism step."""

    repo_root = _repo_root_from(Path(args.repo_root or os.getcwd()))
    state = collect_state(repo_root, args.request_slug)

    if not state["workspace_exists"]:
        print("Next: initialize a request workspace with `bash prism_me/scripts/init_request.sh <request-slug>`.")
        return 0

    if state["persona_review_due"]:
        print(
            "Next: "
            f"{PERSONA_REVIEW_SKILL} -> .prism/{state['request_slug']}/{PERSONA_REVIEW_ARTIFACT} "
            "(finish with `python3 prism_me/scripts/prism_control.py review-complete`)."
        )
        return 0

    if state["next_skill"] and state["next_artifact"]:
        print(
            "Next: "
            f"{state['next_skill']} -> .prism/{state['request_slug']}/{state['next_artifact']}"
        )
        return 0

    print("Next: the required Prism artifact chain is complete; verify handoff readiness and reconcile any deferred items.")
    return 0


def command_validate(args: argparse.Namespace) -> int:
    """Validate the repo-local control files and active request state."""

    repo_root = _repo_root_from(Path(args.repo_root or os.getcwd()))
    problems: list[str] = []

    agents_path = repo_root / "AGENTS.md"
    todo_path = repo_root / "to-do.md"
    config_path = repo_root / ".codex" / "config.toml"
    hooks_path = repo_root / ".codex" / "hooks.json"
    rules_path = repo_root / ".codex" / "rules" / "prism-me.rules"
    script_path = repo_root / "prism_me" / "scripts" / "prism_control.py"
    state_path = _control_state_path(repo_root)

    for path in (agents_path, todo_path, config_path, hooks_path, rules_path, script_path):
        if not path.exists():
            problems.append(f"Missing required control file: {path}")

    if config_path.exists():
        if tomllib is not None:
            try:
                with config_path.open("rb") as handle:
                    tomllib.load(handle)
            except Exception as exc:
                problems.append(f"Invalid TOML in {config_path}: {exc}")

    if hooks_path.exists():
        try:
            with hooks_path.open("r", encoding="utf-8") as handle:
                json.load(handle)
        except Exception as exc:
            problems.append(f"Invalid JSON in {hooks_path}: {exc}")

    if state_path.exists():
        try:
            with state_path.open("r", encoding="utf-8") as handle:
                json.load(handle)
        except Exception as exc:
            problems.append(f"Invalid JSON in {state_path}: {exc}")

    state = collect_state(repo_root, args.request_slug)
    if state["workspace_exists"] and not state["coverage_checklist_present"]:
        problems.append("Active Prism workspace is missing 00-skill-coverage-checklist.md")
    if state["workspace_exists"] and not state["reasoning_log_present"]:
        problems.append("Active Prism workspace is missing reasoning-log.md")
    if state["workspace_exists"] and state["persona_review_artifact"]:
        artifact_path = repo_root / state["persona_review_artifact"]
        if not artifact_path.exists():
            problems.append("Active Prism workspace is missing 05d-persona-review.md")
    problems.extend(
        problem
        for problem in state["artifact_readiness_problems"]
        if "duplicate top metadata field" in problem or "unreadable metadata" in problem
    )

    report = {
        "repo_root": str(repo_root),
        "valid": not problems,
        "problems": problems,
        "state": state,
    }

    if args.json:
        json.dump(report, sys.stdout, indent=2, sort_keys=True)
        sys.stdout.write("\n")
    else:
        print(f"Repo: {repo_root}")
        print(f"Valid: {'yes' if not problems else 'no'}")
        if problems:
            print("Problems:")
            for problem in problems:
                print(f"- {problem}")
        else:
            print("Problems: none")
    return 0 if not problems else 1


def command_review_complete(args: argparse.Namespace) -> int:
    """Mark the active persona review complete and reset the threshold counter."""

    repo_root = _repo_root_from(Path(args.repo_root or os.getcwd()))
    state = collect_state(repo_root, args.request_slug)
    if not state["workspace_exists"] or not state["request_slug"]:
        print("No active Prism request workspace is available for persona-review completion.")
        return 1

    review_state, artifact_path, completed = _mark_persona_review_complete(
        repo_root,
        state["request_slug"],
        reviewed_through_cycle=args.reviewed_through_cycle,
    )
    if review_state is None:
        print("Persona-review completion could not be recorded.")
        return 1

    artifact_display = (
        str(artifact_path.relative_to(repo_root))
        if artifact_path is not None and artifact_path.exists()
        else "(artifact unavailable)"
    )
    if completed:
        print(
            "Persona review marked complete: "
            f"cycle {review_state['last_completed_review_cycle']} -> {artifact_display}"
        )
    else:
        print(
            "Persona review already complete: "
            f"cycle {review_state['last_completed_review_cycle']} -> {artifact_display}"
        )
    return 0


def command_lease_cancel(args: argparse.Namespace) -> int:
    """Resolve a reserved or indeterminate lease known not to have mutated state."""

    repo_root = _repo_root_from(Path(args.repo_root or os.getcwd()))
    state = collect_state(repo_root, args.request_slug)
    try:
        _review_state, cancelled = _cancel_edit_lease(
            repo_root,
            state["request_slug"],
            event_id=args.event_id,
            fingerprint=args.fingerprint,
            reason=args.reason,
        )
    except PrismEditLeaseError as exc:
        print(f"Edit lease cancellation failed: {exc}", file=sys.stderr)
        return 1
    verb = "cancelled" if cancelled else "already cancelled"
    print(f"Edit lease {verb}: {args.event_id}")
    return 0


def command_hook_session_start(_args: argparse.Namespace) -> int:
    """Hook entrypoint for SessionStart."""

    payload = _load_hook_payload()
    repo_root = _repo_root_from(Path(payload.get("cwd") or os.getcwd()))
    state = collect_state(repo_root)
    if state["request_slug"]:
        _sync_persona_review_controls(repo_root, state["request_slug"])
    json.dump(_hook_output("SessionStart", build_additional_context(state)), sys.stdout)
    sys.stdout.write("\n")
    return 0


def command_hook_user_prompt_submit(_args: argparse.Namespace) -> int:
    """Hook entrypoint for UserPromptSubmit."""

    payload = _load_hook_payload()
    prompt = payload.get("prompt", "")
    if _prompt_requests_bypass(prompt):
        json.dump(
            {
                "decision": "block",
                "reason": "This workspace enforces Prism control surfaces. Restate the request without asking Codex to bypass them.",
            },
            sys.stdout,
        )
        sys.stdout.write("\n")
        return 0

    repo_root = _repo_root_from(Path(payload.get("cwd") or os.getcwd()))
    state = collect_state(repo_root)
    pack_present = (repo_root / "prism_me" / "skill-pack.yaml").exists()
    if pack_present or state["workspace_exists"] or _prompt_needs_prism_context(prompt):
        json.dump(_hook_output("UserPromptSubmit", build_additional_context(state)), sys.stdout)
        sys.stdout.write("\n")
    return 0


def command_hook_pre_tool_use(_args: argparse.Namespace) -> int:
    """Hook entrypoint for PreToolUse."""

    payload = _load_hook_payload()
    if _looks_like_edit_or_write_tool(payload):
        repo_root = _repo_root_from(Path(payload.get("cwd") or os.getcwd()))
        state = collect_state(repo_root)
        event_id = _hook_event_id(payload)
        if event_id is None:
            json.dump(_deny("Edit/Write hooks require a stable event identity."), sys.stdout)
            sys.stdout.write("\n")
            return 0
        try:
            review_state, _lease, created = _reserve_edit_lease(
                repo_root,
                state["request_slug"],
                event_id=event_id,
                fingerprint=_edit_fingerprint(payload),
                purpose=(
                    "persona_review_record"
                    if _is_persona_review_recording_edit(
                        payload, repo_root, state["request_slug"]
                    )
                    else "feature_edit"
                ),
            )
        except PrismEditLeaseError as exc:
            json.dump(_deny(str(exc)), sys.stdout)
            sys.stdout.write("\n")
            return 0
        action = "reserved" if created else "reused"
        json.dump(
            _hook_output(
                "PreToolUse",
                f"Prism {action} edit lease {event_id}; committed cycles remain "
                f"{review_state['edit_write_cycles']} until the matching post-hook.",
            ),
            sys.stdout,
        )
        sys.stdout.write("\n")
        return 0

    command = _hook_tool_input(payload).get("command", "")

    destructive_reason = _is_destructive_command(command)
    if destructive_reason:
        json.dump(_deny(destructive_reason), sys.stdout)
        sys.stdout.write("\n")
        return 0

    if _is_direct_prism_mutation(command):
        json.dump(
            _deny(
                "Blocked ad hoc shell mutation of Prism control files. "
                "Use `bash prism_me/scripts/init_request.sh <request-slug>`, "
                "`bash prism_me/scripts/init_external_harmonization.sh <request-slug>`, "
                "or `python3 prism_me/scripts/prism_control.py ...` instead."
            ),
            sys.stdout,
        )
        sys.stdout.write("\n")
        return 0

    return 0


def command_hook_post_tool_use(_args: argparse.Namespace) -> int:
    """Hook entrypoint for PostToolUse."""

    payload = _load_hook_payload()
    tool_input = _hook_tool_input(payload)
    command = str(tool_input.get("command", "")).strip()
    repo_root = _repo_root_from(Path(payload.get("cwd") or os.getcwd()))
    state = collect_state(repo_root)
    slug = state["request_slug"]

    if _looks_like_edit_or_write_tool(payload):
        event_id = _hook_event_id(payload)
        if event_id is None:
            json.dump(
                _hook_output(
                    "PostToolUse",
                    "ERROR: an Edit/Write completed without a stable event identity; "
                    "the mutation outcome cannot be reconciled safely.",
                ),
                sys.stdout,
            )
            sys.stdout.write("\n")
            return 1
        try:
            review_state, triggered, _recorded = _commit_edit_lease(
                repo_root,
                slug,
                event_id=event_id,
                fingerprint=_edit_fingerprint(payload),
                allow_protocol_bootstrap=True,
            )
        except PrismEditLeaseError as exc:
            json.dump(
                _hook_output(
                    "PostToolUse",
                    f"ERROR: Prism could not reconcile the completed Edit/Write: {exc}",
                    system_message="Prism edit lease reconciliation failed; stop further mutations.",
                ),
                sys.stdout,
            )
            sys.stdout.write("\n")
            return 1

        if triggered:
            artifact_display = f".prism/{slug}/{PERSONA_REVIEW_ARTIFACT}"
            json.dump(
                _hook_output(
                    "PostToolUse",
                    f"Edit cycle {review_state['edit_write_cycles']} triggered persona review. "
                    f"Run `{PERSONA_REVIEW_SKILL}`, update `{artifact_display}`, sync `to-do.md`, "
                    "and finish with `python3 prism_me/scripts/prism_control.py review-complete`.",
                ),
                sys.stdout,
            )
            sys.stdout.write("\n")
            return 0

        return 0

    if "init_request.sh" in command:
        if slug:
            _ensure_persona_review_artifact(repo_root, slug)
            _sync_persona_review_controls(repo_root, slug)
        json.dump(
            _hook_output(
                "PostToolUse",
                "A Prism request workspace was initialized. Start with `prism-spec-orchestrator`, then sync `to-do.md`, the coverage checklist, and the persona-review control fields before moving deeper.",
            ),
            sys.stdout,
        )
        sys.stdout.write("\n")
        return 0

    if "init_external_harmonization.sh" in command:
        json.dump(
            _hook_output(
                "PostToolUse",
                "External harmonization was initialized. Route through `prism-external-reference-scoper`, `prism-external-capability-extractor`, and `prism-agentic-shape-forger` before deeper contract or implementation work.",
            ),
            sys.stdout,
        )
        sys.stdout.write("\n")
        return 0

    if _looks_like_test_command(command):
        if state["workspace_exists"]:
            message = (
                f"Record the latest check result in `.prism/{state['request_slug']}/05c-test-evidence.md` "
                "and keep `to-do.md` aligned with the real test and persona-review state."
            )
        else:
            message = (
                "A test or validation command just ran. If this work belongs to a Prism request, "
                "initialize or select the request workspace before the result disappears into chat history."
            )
        json.dump(_hook_output("PostToolUse", message), sys.stdout)
        sys.stdout.write("\n")
        return 0

    return 0


def build_parser() -> argparse.ArgumentParser:
    """Create the CLI argument parser."""

    parser = argparse.ArgumentParser(description="Prism ME Codex control plane")
    subparsers = parser.add_subparsers(dest="command", required=True)

    status = subparsers.add_parser("status", help="Show current Prism request state")
    status.add_argument("--repo-root", help="Repo root override")
    status.add_argument("--request-slug", help="Explicit request slug")
    status.add_argument("--json", action="store_true", help="Emit JSON")
    status.set_defaults(func=command_status)

    next_cmd = subparsers.add_parser("next", help="Show the next recommended Prism step")
    next_cmd.add_argument("--repo-root", help="Repo root override")
    next_cmd.add_argument("--request-slug", help="Explicit request slug")
    next_cmd.set_defaults(func=command_next)

    validate = subparsers.add_parser("validate", help="Validate the repo-local control stack")
    validate.add_argument("--repo-root", help="Repo root override")
    validate.add_argument("--request-slug", help="Explicit request slug")
    validate.add_argument("--json", action="store_true", help="Emit JSON")
    validate.set_defaults(func=command_validate)

    review_complete = subparsers.add_parser("review-complete", help="Mark the active persona review complete")
    review_complete.add_argument("--repo-root", help="Repo root override")
    review_complete.add_argument("--request-slug", help="Explicit request slug")
    review_complete.add_argument(
        "--reviewed-through-cycle",
        type=int,
        help="Explicit highest edit cycle covered by the completed review",
    )
    review_complete.set_defaults(func=command_review_complete)

    lease_cancel = subparsers.add_parser(
        "lease-cancel",
        help="Resolve an Edit/Write lease after a trusted no-mutation outcome",
    )
    lease_cancel.add_argument("--repo-root", help="Repo root override")
    lease_cancel.add_argument("--request-slug", help="Explicit request slug")
    lease_cancel.add_argument(
        "--event-id",
        required=True,
        help="Exact normalized lease identity shown by Prism status",
    )
    lease_cancel.add_argument(
        "--fingerprint",
        required=True,
        help="Exact SHA-256 edit fingerprint bound by the pre-hook",
    )
    lease_cancel.add_argument(
        "--reason",
        required=True,
        choices=sorted(EDIT_LEASE_CANCELLATION_REASONS),
    )
    lease_cancel.set_defaults(func=command_lease_cancel)

    hook_session = subparsers.add_parser("hook-session-start", help="Codex SessionStart hook entrypoint")
    hook_session.set_defaults(func=command_hook_session_start)

    hook_prompt = subparsers.add_parser("hook-user-prompt-submit", help="Codex UserPromptSubmit hook entrypoint")
    hook_prompt.set_defaults(func=command_hook_user_prompt_submit)

    hook_pre = subparsers.add_parser("hook-pre-tool-use", help="Codex PreToolUse hook entrypoint")
    hook_pre.set_defaults(func=command_hook_pre_tool_use)

    hook_post = subparsers.add_parser("hook-post-tool-use", help="Codex PostToolUse hook entrypoint")
    hook_post.set_defaults(func=command_hook_post_tool_use)

    return parser


def main(argv: list[str] | None = None) -> int:
    """Run the Prism ME control CLI."""

    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
