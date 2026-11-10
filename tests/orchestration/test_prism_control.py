# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
from __future__ import annotations

from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
import json
import multiprocessing
from pathlib import Path
import time

import pytest

from prism_me.scripts import prism_control


SLUG = "concurrency-request"


def _record_worker(repo_root: str, slug: str, event_id: str) -> tuple[int, bool, bool]:
    state, triggered, recorded = prism_control._record_edit_cycle(
        Path(repo_root),
        slug,
        event_id=event_id,
    )
    return int(state["edit_write_cycles"]), triggered, recorded


def _complete_worker(repo_root: str, slug: str) -> tuple[int, bool]:
    state, _artifact, completed = prism_control._mark_persona_review_complete(
        Path(repo_root),
        slug,
    )
    assert state is not None
    return int(state["last_completed_review_cycle"]), completed


def _reserve_worker(repo_root: str, slug: str, event_id: str) -> tuple[str, bool, str]:
    try:
        _state, _lease, created = prism_control._reserve_edit_lease(
            Path(repo_root),
            slug,
            event_id=event_id,
            fingerprint=(event_id.encode("utf-8").hex() + "0" * 64)[:64],
            now=100.0,
            ttl_seconds=30.0,
        )
    except prism_control.PrismEditLeaseError as exc:
        return event_id, False, str(exc)
    return event_id, created, ""


def _repo(tmp_path: Path, *, slug: str = SLUG) -> Path:
    (tmp_path / ".prism" / slug).mkdir(parents=True)
    (tmp_path / "to-do.md").write_text(
        "# TODO\n\n"
        "- Request slug: concurrency-request\n"
        "- Workspace: .prism/concurrency-request\n",
        encoding="utf-8",
    )
    return tmp_path


def _loaded(repo_root: Path) -> dict[str, object]:
    return json.loads(prism_control._control_state_path(repo_root).read_text(encoding="utf-8"))


def _fingerprint(marker: str) -> str:
    return (marker.encode("utf-8").hex() + "0" * 64)[:64]


def _write_complete_artifact_chain(repo_root: Path, *, slug: str = SLUG) -> None:
    workspace = repo_root / ".prism" / slug
    for spec in prism_control.ARTIFACT_SPECS:
        path = workspace / spec.filename
        if spec.filename == "05-execution-log.md":
            body = "# Execution Log\n\n- Status: `completed`\n\n## Evidence\n"
        elif spec.filename == "05b-refinement-loop.md":
            body = "# Refinement\n\n- Status: `completed`\n\n## Evidence\n"
        elif spec.filename == "05c-test-evidence.md":
            body = "# Tests\n\n- Status: `accepted`\n\n## Evidence\n"
        elif spec.filename == "06-verification.md":
            body = (
                "# Verification\n\n- Status: `completed`\n"
                "- Release Gate: `pass`\n\n## Evidence\n"
            )
        elif spec.filename == "07-handoff.md":
            body = (
                "# Handoff\n\n- Status: `completed`\n"
                "- Readiness: `ready`\n\n## Evidence\n"
            )
        else:
            body = f"# {spec.filename}\n"
        path.write_text(body, encoding="utf-8")


def test_parallel_unique_hook_events_increment_exactly_once(tmp_path: Path) -> None:
    repo_root = _repo(tmp_path)
    event_count = prism_control.PERSONA_REVIEW_THRESHOLD + 22
    context = multiprocessing.get_context("spawn")
    with ProcessPoolExecutor(max_workers=8, mp_context=context) as pool:
        results = list(
            pool.map(
                _record_worker,
                [str(repo_root)] * event_count,
                [SLUG] * event_count,
                [f"event-{index}" for index in range(event_count)],
            )
        )

    state = _loaded(repo_root)["requests"][SLUG]
    assert state["edit_write_cycles"] == event_count
    assert state["review_due"] is True
    assert state["review_due_cycle"] == prism_control.PERSONA_REVIEW_THRESHOLD
    assert len(state["recorded_edit_events"]) == event_count
    assert sum(triggered for _cycle, triggered, _recorded in results) == 1


def test_concurrent_duplicate_hook_event_is_idempotent(tmp_path: Path) -> None:
    repo_root = _repo(tmp_path)
    context = multiprocessing.get_context("spawn")
    with ProcessPoolExecutor(max_workers=8, mp_context=context) as pool:
        results = list(
            pool.map(
                _record_worker,
                [str(repo_root)] * 16,
                [SLUG] * 16,
                ["same-delivery"] * 16,
            )
        )

    state = _loaded(repo_root)["requests"][SLUG]
    assert state["edit_write_cycles"] == 1
    assert sum(recorded for _cycle, _triggered, recorded in results) == 1

    prism_control._record_edit_cycle(repo_root, SLUG, event_id="second-delivery")
    assert _loaded(repo_root)["requests"][SLUG]["edit_write_cycles"] == 2


def test_atomic_state_never_exposes_partial_json(tmp_path: Path) -> None:
    repo_root = _repo(tmp_path)
    prism_control._record_edit_cycle(repo_root, SLUG, event_id="initial")
    failures: list[BaseException] = []

    def reader() -> None:
        deadline = time.monotonic() + 2.0
        while time.monotonic() < deadline:
            try:
                json.loads(
                    prism_control._control_state_path(repo_root).read_text(encoding="utf-8")
                )
            except BaseException as exc:  # pragma: no cover - assertion reports exact race
                failures.append(exc)
                return

    with ThreadPoolExecutor(max_workers=5) as pool:
        reader_future = pool.submit(reader)
        writer_futures = [
            pool.submit(
                prism_control._record_edit_cycle,
                repo_root,
                SLUG,
                event_id=f"writer-{index}",
            )
            for index in range(40)
        ]
        for future in writer_futures:
            future.result()
        reader_future.result()

    assert failures == []
    assert _loaded(repo_root)["requests"][SLUG]["edit_write_cycles"] == 41


def test_corrupt_state_fails_closed_without_counter_reset(tmp_path: Path) -> None:
    repo_root = _repo(tmp_path)
    state_path = prism_control._control_state_path(repo_root)
    state_path.parent.mkdir(parents=True)
    corrupt_bytes = b'{"requests":{"broken":'
    state_path.write_bytes(corrupt_bytes)

    with pytest.raises(prism_control.PrismControlStateError, match="invalid authoritative"):
        prism_control._record_edit_cycle(repo_root, SLUG, event_id="must-not-reset")

    assert state_path.read_bytes() == corrupt_bytes


def test_review_complete_is_idempotent_when_not_due(tmp_path: Path) -> None:
    repo_root = _repo(tmp_path)
    for index in range(prism_control.PERSONA_REVIEW_THRESHOLD):
        prism_control._record_edit_cycle(repo_root, SLUG, event_id=f"event-{index}")

    first, _artifact, completed = prism_control._mark_persona_review_complete(repo_root, SLUG)
    assert completed is True
    assert first is not None
    first_timestamp = first["last_completion_at"]

    second, _artifact, completed_again = prism_control._mark_persona_review_complete(
        repo_root,
        SLUG,
    )
    assert completed_again is False
    assert second is not None
    assert second["edit_write_cycles"] == first["edit_write_cycles"]
    assert second["last_completed_review_cycle"] == first["last_completed_review_cycle"]
    assert second["last_completion_at"] == first_timestamp


def test_parallel_review_complete_and_edit_linearize(tmp_path: Path) -> None:
    repo_root = _repo(tmp_path)
    for index in range(prism_control.PERSONA_REVIEW_THRESHOLD):
        prism_control._record_edit_cycle(repo_root, SLUG, event_id=f"event-{index}")

    context = multiprocessing.get_context("spawn")
    with ProcessPoolExecutor(max_workers=2, mp_context=context) as pool:
        edit = pool.submit(_record_worker, str(repo_root), SLUG, "racing-edit")
        completion = pool.submit(_complete_worker, str(repo_root), SLUG)
        edit.result()
        completion.result()

    state = _loaded(repo_root)["requests"][SLUG]
    assert state["edit_write_cycles"] == prism_control.PERSONA_REVIEW_THRESHOLD + 1
    assert state["last_completed_review_cycle"] in {
        prism_control.PERSONA_REVIEW_THRESHOLD,
        prism_control.PERSONA_REVIEW_THRESHOLD + 1,
    }
    assert (state["review_due"], state["review_due_cycle"]) == (False, 0)


def test_duplicate_retry_repairs_markdown_without_increment(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    repo_root = _repo(tmp_path)
    original_sync = prism_control._sync_persona_review_controls_from_state
    failed = False

    def fail_once(*args: object, **kwargs: object) -> None:
        nonlocal failed
        if not failed:
            failed = True
            raise OSError("injected projection failure")
        original_sync(*args, **kwargs)

    monkeypatch.setattr(prism_control, "_sync_persona_review_controls_from_state", fail_once)
    with pytest.raises(OSError, match="injected projection failure"):
        prism_control._record_edit_cycle(repo_root, SLUG, event_id="retryable-event")

    prism_control._record_edit_cycle(repo_root, SLUG, event_id="retryable-event")
    state = _loaded(repo_root)["requests"][SLUG]
    assert state["edit_write_cycles"] == 1
    assert "Edit/write cycles recorded: `1`" in (repo_root / "to-do.md").read_text(
        encoding="utf-8"
    )


def test_exact_threshold_trigger_occurs_once(tmp_path: Path) -> None:
    repo_root = _repo(tmp_path)
    triggers: list[bool] = []
    event_count = prism_control.PERSONA_REVIEW_THRESHOLD + 10
    for index in range(event_count):
        _state, triggered, _recorded = prism_control._record_edit_cycle(
            repo_root,
            SLUG,
            event_id=f"event-{index}",
        )
        triggers.append(triggered)

    state = _loaded(repo_root)["requests"][SLUG]
    boundary = prism_control.PERSONA_REVIEW_THRESHOLD - 1
    assert triggers[:boundary] == [False] * boundary
    assert triggers[boundary] is True
    assert triggers[boundary + 1 :] == [False] * (event_count - boundary - 1)
    assert state["review_due_cycle"] == prism_control.PERSONA_REVIEW_THRESHOLD


def test_default_persona_review_policy_is_sparse_but_explicit() -> None:
    assert prism_control.PERSONA_REVIEW_THRESHOLD == 50


def test_two_request_slugs_do_not_cross_contaminate(tmp_path: Path) -> None:
    repo_root = _repo(tmp_path)
    other_slug = "other-request"
    (repo_root / ".prism" / other_slug).mkdir(parents=True)
    context = multiprocessing.get_context("spawn")
    with ProcessPoolExecutor(max_workers=8, mp_context=context) as pool:
        list(
            pool.map(
                _record_worker,
                [str(repo_root)] * 24,
                [SLUG] * 13 + [other_slug] * 11,
                [f"event-{index}" for index in range(24)],
            )
        )

    requests = _loaded(repo_root)["requests"]
    assert requests[SLUG]["edit_write_cycles"] == 13
    assert requests[other_slug]["edit_write_cycles"] == 11
    assert set(requests[SLUG]["recorded_edit_events"]).isdisjoint(
        requests[other_slug]["recorded_edit_events"]
    )


def test_parallel_preleases_cannot_cross_review_boundary(tmp_path: Path) -> None:
    repo_root = _repo(tmp_path)
    for index in range(prism_control.PERSONA_REVIEW_THRESHOLD - 1):
        prism_control._record_edit_cycle(repo_root, SLUG, event_id=f"prior-{index}")

    event_ids = [f"lease-{index}" for index in range(16)]
    context = multiprocessing.get_context("spawn")
    with ProcessPoolExecutor(max_workers=8, mp_context=context) as pool:
        results = list(
            pool.map(
                _reserve_worker,
                [str(repo_root)] * len(event_ids),
                [SLUG] * len(event_ids),
                event_ids,
            )
        )

    winners = [event_id for event_id, created, error in results if created and not error]
    assert len(winners) == 1
    state = _loaded(repo_root)["requests"][SLUG]
    assert state["edit_write_cycles"] == prism_control.PERSONA_REVIEW_THRESHOLD - 1
    assert [lease["status"] for lease in state["edit_leases"].values()] == ["leased"]

    winner = winners[0]
    committed, triggered, recorded = prism_control._commit_edit_lease(
        repo_root,
        SLUG,
        event_id=winner,
        fingerprint=_fingerprint(winner),
        now=101.0,
    )
    assert (triggered, recorded) == (True, True)
    assert committed["edit_write_cycles"] == prism_control.PERSONA_REVIEW_THRESHOLD


def test_duplicate_lease_and_commit_delivery_are_idempotent(tmp_path: Path) -> None:
    repo_root = _repo(tmp_path)
    event_id = "duplicate-edit"
    fingerprint = _fingerprint(event_id)
    _state, _lease, created = prism_control._reserve_edit_lease(
        repo_root,
        SLUG,
        event_id=event_id,
        fingerprint=fingerprint,
        now=10.0,
    )
    assert created is True
    _state, _lease, created_again = prism_control._reserve_edit_lease(
        repo_root,
        SLUG,
        event_id=event_id,
        fingerprint=fingerprint,
        now=11.0,
    )
    assert created_again is False

    first, _triggered, recorded = prism_control._commit_edit_lease(
        repo_root,
        SLUG,
        event_id=event_id,
        fingerprint=fingerprint,
        now=12.0,
    )
    second, triggered_again, recorded_again = prism_control._commit_edit_lease(
        repo_root,
        SLUG,
        event_id=event_id,
        fingerprint=fingerprint,
        now=13.0,
    )
    assert first["edit_write_cycles"] == second["edit_write_cycles"] == 1
    assert (triggered_again, recorded_again) == (False, False)


def test_fingerprint_mismatch_and_unleased_post_fail_closed(tmp_path: Path) -> None:
    repo_root = _repo(tmp_path)
    event_id = "bound-edit"
    prism_control._reserve_edit_lease(
        repo_root,
        SLUG,
        event_id=event_id,
        fingerprint=_fingerprint(event_id),
        now=20.0,
    )
    with pytest.raises(prism_control.PrismEditLeaseError, match="fingerprint"):
        prism_control._commit_edit_lease(
            repo_root,
            SLUG,
            event_id=event_id,
            fingerprint="f" * 64,
            now=21.0,
        )
    with pytest.raises(prism_control.PrismEditLeaseError, match="no matching"):
        prism_control._commit_edit_lease(
            repo_root,
            SLUG,
            event_id="unleased-edit",
            fingerprint="e" * 64,
            now=21.0,
            allow_protocol_bootstrap=True,
        )
    assert _loaded(repo_root)["requests"][SLUG]["edit_write_cycles"] == 0


def test_expired_lease_blocks_until_late_post_resolves_it(tmp_path: Path) -> None:
    repo_root = _repo(tmp_path)
    event_id = "slow-edit"
    fingerprint = _fingerprint(event_id)
    prism_control._reserve_edit_lease(
        repo_root,
        SLUG,
        event_id=event_id,
        fingerprint=fingerprint,
        now=30.0,
        ttl_seconds=1.0,
    )
    with pytest.raises(prism_control.PrismEditLeaseError, match="unresolved expired"):
        prism_control._reserve_edit_lease(
            repo_root,
            SLUG,
            event_id="later-edit",
            fingerprint=_fingerprint("later-edit"),
            now=32.0,
        )
    persisted = _loaded(repo_root)["requests"][SLUG]["edit_leases"][event_id]
    assert persisted["status"] == "expired_indeterminate"

    state, _triggered, recorded = prism_control._commit_edit_lease(
        repo_root,
        SLUG,
        event_id=event_id,
        fingerprint=fingerprint,
        now=33.0,
    )
    assert recorded is True
    assert state["edit_leases"][event_id]["status"] == "committed"
    _state, _lease, created = prism_control._reserve_edit_lease(
        repo_root,
        SLUG,
        event_id="later-edit",
        fingerprint=_fingerprint("later-edit"),
        now=34.0,
    )
    assert created is True


def test_explicit_cancellation_uses_closed_reasons_and_frees_slot(tmp_path: Path) -> None:
    repo_root = _repo(tmp_path)
    event_id = "abandoned-edit"
    fingerprint = _fingerprint(event_id)
    prism_control._reserve_edit_lease(
        repo_root,
        SLUG,
        event_id=event_id,
        fingerprint=fingerprint,
        now=40.0,
    )
    with pytest.raises(prism_control.PrismEditLeaseError, match="untrusted"):
        prism_control._cancel_edit_lease(
            repo_root,
            SLUG,
            event_id=event_id,
            fingerprint=fingerprint,
            reason="probably_safe",
            now=41.0,
        )
    _state, cancelled = prism_control._cancel_edit_lease(
        repo_root,
        SLUG,
        event_id=event_id,
        fingerprint=fingerprint,
        reason="cancelled_before_execution",
        now=41.0,
    )
    assert cancelled is True
    _state, cancelled_again = prism_control._cancel_edit_lease(
        repo_root,
        SLUG,
        event_id=event_id,
        fingerprint=fingerprint,
        reason="cancelled_before_execution",
        now=42.0,
    )
    assert cancelled_again is False
    assert _loaded(repo_root)["requests"][SLUG]["edit_write_cycles"] == 0


def test_only_one_unleased_bootstrap_commit_is_allowed(tmp_path: Path) -> None:
    repo_root = _repo(tmp_path)
    prism_control._commit_edit_lease(
        repo_root,
        SLUG,
        event_id="bootstrap-edit",
        fingerprint=_fingerprint("bootstrap-edit"),
        now=50.0,
        allow_protocol_bootstrap=True,
    )
    with pytest.raises(prism_control.PrismEditLeaseError, match="no matching"):
        prism_control._commit_edit_lease(
            repo_root,
            SLUG,
            event_id="second-unleased-edit",
            fingerprint=_fingerprint("second-unleased-edit"),
            now=51.0,
            allow_protocol_bootstrap=True,
        )


def test_stage_requires_semantic_completion_not_file_existence(tmp_path: Path) -> None:
    repo_root = _repo(tmp_path)
    _write_complete_artifact_chain(repo_root)
    execution = repo_root / ".prism" / SLUG / "05-execution-log.md"
    execution.write_text(
        "# Execution Log\n\n- Status: `in_progress`\n\n## Evidence\n",
        encoding="utf-8",
    )
    state = prism_control.collect_state(repo_root, SLUG)
    assert state["current_stage"] == "execution"
    assert state["next_artifact"] == "05-execution-log.md"
    assert state["handoff_ready"] is False

    execution.write_text(
        "# Execution Log\n\n- Status: `completed`\n\n## Evidence\n",
        encoding="utf-8",
    )
    complete = prism_control.collect_state(repo_root, SLUG)
    assert complete["current_stage"] == "handoff-complete"
    assert complete["unready_artifacts"] == []
    assert complete["handoff_ready"] is True


@pytest.mark.parametrize(
    ("filename", "body", "expected_stage"),
    [
        ("05b-refinement-loop.md", "- Status: `draft`", "reflective-refinement"),
        ("05c-test-evidence.md", "- Status: `draft`", "test-evidence"),
        (
            "06-verification.md",
            "- Status: `completed`\n- Release Gate: `hold`",
            "evaluation",
        ),
        (
            "07-handoff.md",
            "- Status: `completed`\n- Readiness: `partial`",
            "handoff",
        ),
    ],
)
def test_each_semantic_gate_blocks_handoff(
    tmp_path: Path,
    filename: str,
    body: str,
    expected_stage: str,
) -> None:
    repo_root = _repo(tmp_path)
    _write_complete_artifact_chain(repo_root)
    (repo_root / ".prism" / SLUG / filename).write_text(
        f"# Artifact\n\n{body}\n\n## Evidence\n",
        encoding="utf-8",
    )
    state = prism_control.collect_state(repo_root, SLUG)
    assert state["current_stage"] == expected_stage
    assert state["handoff_ready"] is False


def test_duplicate_top_metadata_is_rejected_even_if_later_value_is_complete(
    tmp_path: Path,
) -> None:
    repo_root = _repo(tmp_path)
    _write_complete_artifact_chain(repo_root)
    (repo_root / ".prism" / SLUG / "06-verification.md").write_text(
        "# Verification\n\n"
        "- Status: `draft`\n"
        "- Status: `completed`\n"
        "- Release Gate: `pass`\n\n"
        "## Evidence\n",
        encoding="utf-8",
    )
    state = prism_control.collect_state(repo_root, SLUG)
    assert state["current_stage"] == "evaluation"
    assert any(
        "duplicate top metadata field 'status'" in problem
        for problem in state["artifact_readiness_problems"]
    )


def test_due_review_allows_only_exact_review_recording_paths(tmp_path: Path) -> None:
    repo_root = _repo(tmp_path)
    for index in range(prism_control.PERSONA_REVIEW_THRESHOLD):
        prism_control._record_edit_cycle(repo_root, SLUG, event_id=f"due-{index}")

    with pytest.raises(prism_control.PrismEditLeaseError, match="feature edit"):
        prism_control._reserve_edit_lease(
            repo_root,
            SLUG,
            event_id="blocked-feature",
            fingerprint=_fingerprint("blocked-feature"),
            now=60.0,
        )

    state, lease, created = prism_control._reserve_edit_lease(
        repo_root,
        SLUG,
        event_id="review-record",
        fingerprint=_fingerprint("review-record"),
        now=60.0,
        purpose="persona_review_record",
    )
    assert created is True
    assert lease["purpose"] == "persona_review_record"
    assert state["edit_write_cycles"] == prism_control.PERSONA_REVIEW_THRESHOLD
    committed, _triggered, recorded = prism_control._commit_edit_lease(
        repo_root,
        SLUG,
        event_id="review-record",
        fingerprint=_fingerprint("review-record"),
        now=61.0,
    )
    assert recorded is True
    assert committed["review_due"] is True
    completed, _artifact, changed = prism_control._mark_persona_review_complete(
        repo_root,
        SLUG,
        reviewed_through_cycle=prism_control.PERSONA_REVIEW_THRESHOLD + 1,
    )
    assert changed is True
    assert completed is not None and completed["review_due"] is False


@pytest.mark.parametrize(
    ("relative_path", "allowed"),
    [
        (f".prism/{SLUG}/05d-persona-review.md", True),
        (f".prism/{SLUG}/reasoning-log.md", True),
        ("to-do.md", True),
        ("agentic/discovery/cycle.py", False),
        (f".prism/{SLUG}/../other/05d-persona-review.md", False),
    ],
)
def test_review_record_path_classifier_is_exact(
    tmp_path: Path,
    relative_path: str,
    allowed: bool,
) -> None:
    repo_root = _repo(tmp_path)
    payload = {
        "tool_name": "Edit",
        "tool_input": {"file_path": relative_path},
    }
    assert (
        prism_control._is_persona_review_recording_edit(payload, repo_root, SLUG)
        is allowed
    )
