# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
"""Crash, resume, concurrency, and tamper tests for YM publication."""

from __future__ import annotations

import json
import os
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import pytest

from agentic.discovery.contracts import (
    canonical_digest,
    canonical_json,
    file_digest,
    stable_identifier,
    validate_payload,
)


ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = ROOT / "agentic" / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import run_ym_canonical_parent_cycle_20260721 as runner  # noqa: E402
import validate_ym_canonical_parent_cycle_20260721 as validator  # noqa: E402


def test_unseen_claim_maps_to_question_without_a_positive_semantic_warrant() -> None:
    snapshot = {
        "sources": [{
            "source_id": "unseen-negative-regression",
            "claims": ["Synthetic claim for routing regression only."],
            "limitations": ["No positive support is authorized."],
        }],
        "coverage_limits": ["Synthetic routing input, not research evidence."],
    }
    assert runner._theory_mappings(snapshot)[0]["relation"] == "leaves_open"
    warrants = runner._ym_semantic_source_warrants(snapshot)
    assert len(warrants) == 1
    assert warrants[0]["relation"] == "unresolved"


def _sealed_parent_support() -> dict:
    packet = {
        "theoretical_programme": {
            "programme_id": "programme-1",
            "definitions_to_build": ["D1"],
        },
        "support_probe": {
            "disposition": "commissioned",
            "theory_programme_id": "programme-1",
            "theoretical_question_id": runner.PROBE_QUESTION_ID,
            "conceptual_system_ids": [runner.SYNTHESIS_SYSTEM_ID],
            "theoretical_question": runner.PROBE_QUESTION,
        },
    }
    packet["packet_digest"] = canonical_digest(packet)
    return packet


def test_registered_probe_claim_is_derived_only_from_exact_sealed_parent() -> None:
    packet = _sealed_parent_support()
    claim = runner._registered_theory_claim_from_parent(
        packet,
        expected_programme_id="programme-1",
        expected_conceptual_system_ids=[runner.SYNTHESIS_SYSTEM_ID],
    )
    core = {key: value for key, value in claim.items() if key != "claim_digest"}
    assert claim["claim_id"] == runner.PROBE_QUESTION_ID
    assert claim["statement"] == runner.PROBE_QUESTION
    assert claim["source_reflection_packet_digest"] == packet["packet_digest"]
    assert claim["claim_digest"] == canonical_digest(core)


@pytest.mark.parametrize(
    ("mutation", "message"),
    [
        (lambda packet: packet["support_probe"].update(theoretical_question=None), "wrong programme, system, or question"),
        (lambda packet: packet["support_probe"].update(theoretical_question_id="wrong-question"), "wrong programme, system, or question"),
        (lambda packet: packet["support_probe"].update(theory_programme_id="cross-theory"), "wrong programme, system, or question"),
        (lambda packet: packet["support_probe"].update(conceptual_system_ids=[runner.SYNTHESIS_SYSTEM_ID, runner.SYNTHESIS_SYSTEM_ID]), "duplicates a conceptual-system"),
        (lambda packet: packet.update(packet_digest=canonical_digest("forged-parent")), "packet digest mismatch"),
    ],
)
def test_registered_probe_claim_rejects_missing_duplicate_wrong_identity_digest_and_question(
    mutation, message: str
) -> None:
    packet = _sealed_parent_support()
    mutation(packet)
    if "packet digest" not in message:
        packet["packet_digest"] = canonical_digest(
            packet, exclude_keys=("packet_digest",)
        )
    with pytest.raises(runner.YMCanonicalCycleError, match=message):
        runner._registered_theory_claim_from_parent(
            packet,
            expected_programme_id="programme-1",
            expected_conceptual_system_ids=[runner.SYNTHESIS_SYSTEM_ID],
        )


@pytest.fixture(scope="module")
def recovered_publication(tmp_path_factory: pytest.TempPathFactory) -> dict:
    output_root = tmp_path_factory.mktemp("ym-publication-recovery")
    original_writer = runner._write_immutable_bytes
    injected = {"raised": False}

    def fail_during_report_write(path: Path, encoded: bytes) -> Path:
        if (
            not injected["raised"]
            and path.parent.resolve() == output_root.resolve()
            and path.name == "conceptual_generation_trace.json"
            and (output_root / "canonical_cycle_result.json").is_file()
        ):
            injected["raised"] = True
            raise OSError("injected post-commit report-write failure")
        return original_writer(path, encoded)

    runner._write_immutable_bytes = fail_during_report_write
    try:
        with pytest.raises(OSError, match="injected post-commit"):
            runner.CycleExecution(output_root).run()
    finally:
        runner._write_immutable_bytes = original_writer

    result_path = output_root / "canonical_cycle_result.json"
    result = json.loads(result_path.read_text(encoding="utf-8"))
    status_path = output_root / runner.PUBLICATION_STATUS_NAME
    failures = sorted((output_root / runner.PUBLICATION_FAILURE_DIR).glob("*.json"))
    assert result["committed_state_version"] == 1
    assert not os.path.lexists(status_path)
    assert len(failures) == 1
    failure = json.loads(failures[0].read_text(encoding="utf-8"))
    validate_payload(failure, "ym_canonical_publication_failure.schema.json")
    assert failure["failed_stage"] == "report_write"
    assert failure["commit_id"] == result["commit_id"]
    assert failure["canonical_result_digest"] == file_digest(result_path)
    assert failure["epistemic_effect"] == "none_operational_outcome_only"

    commit_glob = list(
        (output_root / "state").glob(
            "targets/*/runs/*/commits/generation-*-commit.*"
        )
    )
    journal_glob = list((output_root / "state").glob("targets/*/runs/*/journal/*.json"))
    partial_bytes = {
        path.name: path.read_bytes()
        for path in output_root.iterdir()
        if path.is_file() and path.name in runner.PUBLICATION_FILE_ROLES
    }
    outcome = runner.resume_or_validate_publication(output_root)
    resumed = json.loads(result_path.read_text(encoding="utf-8"))
    assert outcome["status"] == "resumed_publication"
    assert resumed["commit_id"] == result["commit_id"]
    assert resumed["manifest_digest"] == result["manifest_digest"]
    assert resumed["state_digest"] == result["state_digest"]
    assert len(list((output_root / "state").glob("targets/*/runs/*/commits/generation-*-commit.*"))) == len(commit_glob) == 1
    assert len(list((output_root / "state").glob("targets/*/runs/*/journal/*.json"))) == len(journal_glob) == 1
    assert all((output_root / name).read_bytes() == encoded for name, encoded in partial_bytes.items())
    summary = validator.validate(output_root)
    assert summary["status"] == "validated"
    assert summary["publication_files"] == 13
    assert summary["publication_failure_receipts"] == 1
    return {
        "root": output_root,
        "result": resumed,
        "failure_count": 1,
    }


@pytest.mark.skip(
    reason="User-deferred: publication fixture lacks genuine citation evidence for YM21-R01. "
    "See .prism/idiap-software-disclosure/09-publication-migration.md."
)
def test_exact_retry_and_concurrent_complete_validation_are_write_free(
    recovered_publication: dict,
) -> None:
    output_root = recovered_publication["root"]
    observed = {
        relative: (
            (output_root / relative).read_bytes(),
            (output_root / relative).stat().st_mtime_ns,
        )
        for relative in [*runner.PUBLICATION_FILE_ROLES, runner.PUBLICATION_STATUS_NAME]
    }
    with ThreadPoolExecutor(max_workers=2) as pool:
        outcomes = list(
            pool.map(
                lambda _index: runner.resume_or_validate_publication(output_root),
                range(2),
            )
        )
    assert [row["status"] for row in outcomes] == [
        "validated_existing",
        "validated_existing",
    ]
    assert all(
        (output_root / relative).read_bytes() == before
        and (output_root / relative).stat().st_mtime_ns == mtime
        for relative, (before, mtime) in observed.items()
    )


def _rehash_status(output_root: Path, status: dict) -> dict:
    result = json.loads((output_root / "canonical_cycle_result.json").read_text())
    status["publication_id"] = stable_identifier(
        "ympub",
        runner.TARGET_ID,
        runner.RUN_ID,
        result["cycle_id"],
        result["commit_id"],
        result["manifest_digest"],
        result["state_digest"],
        status["core_validation_authorization_basis_digest"],
        canonical_digest(status["files"]),
    )
    status.pop("content_digest", None)
    status["content_digest"] = canonical_digest(status)
    return status


@pytest.mark.skip(
    reason="User-deferred: publication fixture lacks genuine citation evidence for YM21-R01. "
    "See .prism/idiap-software-disclosure/09-publication-migration.md."
)
def test_rehashed_semantic_tamper_and_noncanonical_status_fail_closed(
    recovered_publication: dict,
) -> None:
    output_root = recovered_publication["root"]
    acceptance_path = output_root / "acceptance_report.json"
    status_path = output_root / runner.PUBLICATION_STATUS_NAME
    acceptance_bytes = acceptance_path.read_bytes()
    status_bytes = status_path.read_bytes()
    acceptance = json.loads(acceptance_bytes)
    acceptance["authority_boundary"] = "forged but descriptor-consistent acceptance"
    acceptance_path.write_bytes(canonical_json(acceptance) + b"\n")
    status = json.loads(status_bytes)
    descriptor = next(
        row for row in status["files"] if row["path"] == "acceptance_report.json"
    )
    descriptor["sha256"] = file_digest(acceptance_path)
    descriptor["size_bytes"] = acceptance_path.stat().st_size
    status_path.write_bytes(canonical_json(_rehash_status(output_root, status)) + b"\n")
    forged_bytes = acceptance_path.read_bytes()
    with pytest.raises(validator.CanonicalValidationError, match="did not replay"):
        runner.resume_or_validate_publication(output_root)
    assert acceptance_path.read_bytes() == forged_bytes

    acceptance_path.write_bytes(acceptance_bytes)
    status_path.write_bytes(status_bytes + b"\n")
    with pytest.raises(validator.CanonicalValidationError, match="not canonical"):
        runner.resume_or_validate_publication(output_root)
    status_path.write_bytes(status_bytes)
    assert validator.validate(output_root)["status"] == "validated"


@pytest.mark.skip(
    reason="User-deferred: publication fixture lacks genuine citation evidence for YM21-R01. "
    "See .prism/idiap-software-disclosure/09-publication-migration.md."
)
def test_conflicting_partial_is_never_overwritten_and_post_status_failure_is_not_misreported(
    recovered_publication: dict,
) -> None:
    output_root = recovered_publication["root"]
    status_path = output_root / runner.PUBLICATION_STATUS_NAME
    acceptance_path = output_root / "acceptance_report.json"
    status_bytes = status_path.read_bytes()
    acceptance_bytes = acceptance_path.read_bytes()
    before_failures = len(list((output_root / runner.PUBLICATION_FAILURE_DIR).glob("*.json")))

    status_path.unlink()
    acceptance_path.write_bytes(b"{}\n")
    with pytest.raises(runner.YMCanonicalCycleError, match="immutable artifact conflict"):
        runner.resume_or_validate_publication(output_root)
    assert acceptance_path.read_bytes() == b"{}\n"
    acceptance_path.write_bytes(acceptance_bytes)
    assert not os.path.lexists(status_path)

    original_validate = validator.validate

    def fail_only_after_status(
        root: Path, *, require_publication: bool = True
    ) -> dict:
        if require_publication:
            raise validator.CanonicalValidationError("injected post-status validation failure")
        return original_validate(root, require_publication=False)

    validator.validate = fail_only_after_status
    try:
        with pytest.raises(validator.CanonicalValidationError, match="post-status"):
            runner.resume_or_validate_publication(output_root)
    finally:
        validator.validate = original_validate
    assert status_path.read_bytes() == status_bytes
    assert len(list((output_root / runner.PUBLICATION_FAILURE_DIR).glob("*.json"))) == before_failures + 1
    assert validator.validate(output_root)["status"] == "validated"


@pytest.mark.skip(
    reason="User-deferred: publication fixture lacks genuine citation evidence for YM21-R01. "
    "See .prism/idiap-software-disclosure/09-publication-migration.md."
)
def test_dangling_status_symlink_is_stale_complete_not_resumable(
    recovered_publication: dict,
    tmp_path: Path,
) -> None:
    output_root = recovered_publication["root"]
    status_path = output_root / runner.PUBLICATION_STATUS_NAME
    status_bytes = status_path.read_bytes()
    status_path.unlink()
    status_path.symlink_to(tmp_path / "missing-status.json")
    try:
        with pytest.raises(validator.CanonicalValidationError, match="absent or unsafe"):
            runner.resume_or_validate_publication(output_root)
        assert status_path.is_symlink()
    finally:
        status_path.unlink()
        status_path.write_bytes(status_bytes)
    assert validator.validate(output_root)["status"] == "validated"


def test_missing_projection_with_committed_pointer_fails_before_second_run(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    pointer = (
        tmp_path
        / "state"
        / "targets"
        / runner.TARGET_ID
        / "runs"
        / runner.RUN_ID
        / "state-pointer.json"
    )
    pointer.parent.mkdir(parents=True)
    pointer.write_text("{}\n", encoding="utf-8")
    monkeypatch.setattr(sys, "argv", ["run-ym", "--output-root", str(tmp_path)])
    assert runner.main() == 1
    assert not (tmp_path / "canonical_cycle_result.json").exists()
