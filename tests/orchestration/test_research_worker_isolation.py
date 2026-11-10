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

import copy
import json
import os
import socket
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Any

import pytest

from agentic.discovery.contracts import (
    SchemaValidationError,
    canonical_digest,
    validate_payload,
)
from agentic.discovery.research_worker_isolation import (
    ResearchWorkerAdapter,
    ResearchWorkerIntegrityError,
    receipt_summary,
    validate_research_worker_receipt,
)


def _adapter(tmp_path: Path, *, study_id: str = "research-worker-isolation-test") -> ResearchWorkerAdapter:
    return ResearchWorkerAdapter(study_id=study_id, run_root=tmp_path / "runs")


def _probe_payload(
    *,
    read_path: Path,
    write_path: Path,
    port: int = 9,
    secret_name: str = "ABDUCER_ISOLATION_SECRET",
) -> dict[str, Any]:
    return {
        "read_path": str(read_path.resolve()),
        "write_path": str(write_path.resolve()),
        "network_host": "127.0.0.1",
        "network_port": port,
        "secret_name": secret_name,
    }


def _invoke_probe(
    adapter: ResearchWorkerAdapter,
    *,
    role: str,
    context: str,
    payload: dict[str, Any],
    fault_mode: str | None = None,
    budget: dict[str, Any] | None = None,
) -> dict[str, Any]:
    return adapter.invoke(
        role=role,
        operation="isolation_probe",
        invocation_context={"test_case": context},
        payload=payload,
        fault_mode=fault_mode,
        budget=budget,
    )


def _receipt_path(receipt: dict[str, Any]) -> Path:
    return Path(receipt["workspace"]["run_directory"]) / receipt["receipt_ref"]


def _assert_all_authority_denied(value: Any) -> None:
    if isinstance(value, dict):
        for key, item in value.items():
            if key.endswith("_authorized") or key.endswith("_eligible"):
                assert item is False, key
            _assert_all_authority_denied(item)
    elif isinstance(value, list):
        for item in value:
            _assert_all_authority_denied(item)


def test_all_research_roles_emit_reopenable_receipts_with_exact_null_authority(
    tmp_path: Path,
) -> None:
    adapter = _adapter(tmp_path)
    payload = _probe_payload(
        read_path=Path(__file__), write_path=tmp_path / "outside-role-probe.txt"
    )

    receipts = [
        _invoke_probe(
            adapter,
            role=role,
            context=f"role-{role}",
            payload=payload,
        )
        for role in ("candidate", "high_risk", "formal_lens", "judge")
    ]

    assert {row["role"] for row in receipts} == {
        "candidate",
        "high_risk",
        "formal_lens",
        "judge",
    }
    for receipt in receipts:
        assert receipt["outcome_status"] == "accepted"
        path = _receipt_path(receipt)
        reopened = validate_research_worker_receipt(
            json.loads(path.read_text(encoding="utf-8")), receipt_path=path
        )
        assert reopened == receipt
        summary = receipt_summary(receipt, receipt_path=path)
        assert summary["receipt_byte_length"] == len(path.read_bytes())
        assert summary["receipt_file_sha256"].startswith("sha256:")
        assert len(summary["receipt_file_sha256"]) == 71
        _assert_all_authority_denied(receipt)
        _assert_all_authority_denied(summary)


def test_channel_specific_probe_discloses_backend_limits_and_scrubs_secrets(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    adapter = _adapter(tmp_path, study_id="research-worker-channel-test")
    outside_write = tmp_path / "outside-worker-workspace.txt"
    secret_name = "ABDUCER_ISOLATION_SECRET"
    monkeypatch.setenv(secret_name, "must-not-cross-env-i")

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as listener:
        listener.bind(("127.0.0.1", 0))
        listener.listen(1)
        listener.settimeout(2.0)
        port = int(listener.getsockname()[1])
        with ThreadPoolExecutor(max_workers=1) as pool:
            accepted = pool.submit(listener.accept)
            receipt = _invoke_probe(
                adapter,
                role="candidate",
                context="channel-probe",
                payload=_probe_payload(
                    read_path=Path(__file__),
                    write_path=outside_write,
                    port=port,
                    secret_name=secret_name,
                ),
            )
            kernel = receipt["isolation_assurance"]["deny_by_construction"]
            try:
                connection, _address = accepted.result(timeout=2.5)
            except (TimeoutError, socket.timeout):
                connected = False
            else:
                connected = True
                connection.close()

    assert receipt["outcome_status"] == "accepted"
    output = receipt["response_payload"]["output"]
    channels = receipt["isolation_assurance"]["channels"]
    assert output["read_succeeded"] is True
    assert output["secret_environment_present"] is False
    execution = receipt["process_event"]["resource_limit_execution"]
    assert execution["replacement_environment_used"] is True
    outer_environment_names = [
        row["name"]
        for row in receipt["process_event"]["supervision_attempt"]["request"][
            "environment_bindings"
        ]
    ]
    assert secret_name not in outer_environment_names
    assert receipt["environment_authority"]["allowed_names"] == sorted(
        receipt["response_payload"]["environment_observation"]["names"]
    )

    forged_binding = copy.deepcopy(receipt)
    forged_binding["environment_authority"]["bindings"][0][
        "value_sha256"
    ] = "sha256:" + "f" * 64
    forged_binding["environment_authority"]["content_digest"] = canonical_digest(
        {
            key: value
            for key, value in forged_binding["environment_authority"].items()
            if key != "content_digest"
        }
    )
    forged_binding["content_digest"] = canonical_digest(
        {
            key: value
            for key, value in forged_binding.items()
            if key != "content_digest"
        }
    )
    with pytest.raises(
        ResearchWorkerIntegrityError,
        match="exact replacement policy",
    ):
        validate_research_worker_receipt(
            forged_binding,
            require_live_authority=False,
        )

    missing_requirement = copy.deepcopy(receipt)
    missing_requirement["request_payload"].pop("isolation_requirement")
    with pytest.raises(SchemaValidationError):
        validate_payload(
            missing_requirement,
            "research_worker_execution_receipt.schema.json",
        )
    assert channels["filesystem_read"] in {
        "host_read_scope_unrestricted",
        "kernel_sibling_run_data_denied_host_read_scope_unrestricted",
    }
    assert channels["environment"] == "env_i_allowlist_enforced"
    if kernel:
        assert output["write_succeeded"] is False
        assert output["network_connection_succeeded"] is False
        assert connected is False
        assert channels["filesystem_write"] == "kernel_workspace_only"
        assert channels["network"] == "kernel_denied"
        assert outside_write.exists() is False
    else:
        assert output["write_succeeded"] is True
        assert output["network_connection_succeeded"] is True
        assert connected is True
        assert channels["filesystem_write"] == "protocol_workspace_only"
        assert channels["network"] == "unavailable_no_kernel_network_policy"
        assert outside_write.read_text(encoding="utf-8") == "isolation-probe"
    assert receipt["isolation_assurance"]["hidden_input_independence_authorized"] is False
    assert receipt["isolation_assurance"]["cognitive_independence_authorized"] is False
    assert receipt["isolation_assurance"]["semantic_independence_authorized"] is False


def test_process_only_fallback_is_honest_and_kernel_requirement_fails_before_spawn(
    tmp_path: Path,
) -> None:
    adapter = _adapter(tmp_path, study_id="research-worker-fallback-test")
    adapter.backend = {
        "backend": "process_group_only",
        "executable": None,
        "probe_status": "unavailable",
        "fallback_reason": "forced process-only regression backend",
    }
    adapter.require_kernel_isolation = True
    receipt = _invoke_probe(
        adapter,
        role="judge",
        context="require-kernel",
        payload=_probe_payload(
            read_path=Path(__file__), write_path=tmp_path / "must-not-run.txt"
        ),
    )

    assert receipt["outcome_status"] == "operational_failure"
    assert receipt["protocol_status"] == "isolation_unavailable"
    assert receipt["failure"]["error_type"] == "KernelIsolationUnavailable"
    assert receipt["process_event"]["pid"] is None
    assert receipt["process_event"]["termination"] == "not_started"
    assert receipt["isolation_assurance"]["status"] == "process_only_strongest_available"
    assert receipt["isolation_assurance"]["deny_by_construction"] is False
    assert receipt["isolation_assurance"]["channels"]["network"] == (
        "unavailable_no_kernel_network_policy"
    )
    assert (tmp_path / "must-not-run.txt").exists() is False


def test_kernel_requirement_changes_invocation_identity_and_cannot_reuse_process_only_success(
    tmp_path: Path,
) -> None:
    adapter = _adapter(tmp_path, study_id="research-worker-isolation-identity-test")
    adapter.backend = {
        "backend": "process_group_only",
        "executable": None,
        "probe_status": "unavailable",
        "fallback_reason": "forced process-only identity regression backend",
    }
    payload = _probe_payload(
        read_path=Path(__file__), write_path=tmp_path / "process-only-first-run.txt"
    )

    accepted = _invoke_probe(
        adapter,
        role="candidate",
        context="same-logical-request",
        payload=payload,
    )
    assert accepted["outcome_status"] == "accepted"
    assert accepted["request_payload"]["isolation_requirement"][
        "kernel_isolation_required"
    ] is False

    adapter.require_kernel_isolation = True
    rejected = _invoke_probe(
        adapter,
        role="candidate",
        context="same-logical-request",
        payload=payload,
    )

    assert rejected["outcome_status"] == "operational_failure"
    assert rejected["protocol_status"] == "isolation_unavailable"
    assert rejected["invocation_id"] != accepted["invocation_id"]
    assert rejected["receipt_id"] != accepted["receipt_id"]
    assert rejected["request_payload"]["isolation_requirement"][
        "kernel_isolation_required"
    ] is True
    with pytest.raises(
        ResearchWorkerIntegrityError, match="required isolation identity"
    ):
        validate_research_worker_receipt(
            accepted,
            require_live_authority=False,
            required_kernel_isolation=True,
        )
    assert validate_research_worker_receipt(
        rejected,
        require_live_authority=False,
        required_kernel_isolation=True,
    ) == rejected

    forged = copy.deepcopy(accepted)
    forged_requirement = forged["request_payload"]["isolation_requirement"]
    forged_requirement["kernel_isolation_required"] = True
    forged_requirement["minimum_accepted_status"] = "kernel_policy_enforced"
    forged_requirement["content_digest"] = canonical_digest(
        {
            key: value
            for key, value in forged_requirement.items()
            if key != "content_digest"
        }
    )
    forged["content_digest"] = canonical_digest(
        {key: value for key, value in forged.items() if key != "content_digest"}
    )
    with pytest.raises(ResearchWorkerIntegrityError, match="request bytes are not exact"):
        validate_research_worker_receipt(
            forged,
            require_live_authority=False,
            required_kernel_isolation=True,
        )


@pytest.mark.parametrize(
    ("fault_mode", "expected_outcome", "expected_protocol"),
    [
        ("exit_nonzero", "operational_failure", "process_failed"),
        ("invalid_json", "protocol_failure", "invalid_json"),
    ],
)
def test_crash_and_protocol_faults_preserve_immutable_failure_receipts(
    tmp_path: Path,
    fault_mode: str,
    expected_outcome: str,
    expected_protocol: str,
) -> None:
    adapter = _adapter(tmp_path, study_id=f"research-worker-{fault_mode}-test")
    receipt = _invoke_probe(
        adapter,
        role="high_risk",
        context=fault_mode,
        payload=_probe_payload(
            read_path=Path(__file__), write_path=tmp_path / f"{fault_mode}.txt"
        ),
        fault_mode=fault_mode,
    )

    assert receipt["outcome_status"] == expected_outcome
    assert receipt["protocol_status"] == expected_protocol
    assert receipt["response_payload"] is None
    assert receipt["failure"] is not None
    path = _receipt_path(receipt)
    assert validate_research_worker_receipt(
        json.loads(path.read_text(encoding="utf-8")),
        receipt_path=path,
        require_live_authority=False,
    ) == receipt
    assert receipt_summary(receipt, receipt_path=path)["receipt_digest"] == receipt[
        "content_digest"
    ]


def test_timeout_terminates_worker_group_and_persists_typed_receipt(tmp_path: Path) -> None:
    adapter = _adapter(tmp_path, study_id="research-worker-timeout-test")
    budget = copy.deepcopy(adapter.default_budget())
    budget.update(
        {
            "budget_id": "research-worker-timeout-budget.v1",
            "wall_time_seconds": 0.1,
            "grace_period_seconds": 0.05,
            "cpu_seconds": 1.0,
        }
    )
    receipt = _invoke_probe(
        adapter,
        role="formal_lens",
        context="hang-timeout",
        payload=_probe_payload(
            read_path=Path(__file__), write_path=tmp_path / "timeout.txt"
        ),
        fault_mode="hang",
        budget=budget,
    )

    assert receipt["outcome_status"] == "operational_failure"
    assert receipt["process_status"] in {"deadline_exhausted", "worker_failed"}
    assert receipt["failure"]["stage"] == "process_execution"
    assert receipt["process_event"]["termination"] in {"terminated", "killed"}
    assert receipt["resource_receipt"]["usage"]["wall_time_seconds"] < 5.0
    assert _receipt_path(receipt).is_file()


def test_receipt_summary_detects_noncanonical_file_and_caller_mapping_tamper(
    tmp_path: Path,
) -> None:
    adapter = _adapter(tmp_path, study_id="research-worker-tamper-test")
    receipt = _invoke_probe(
        adapter,
        role="candidate",
        context="tamper",
        payload=_probe_payload(
            read_path=Path(__file__), write_path=tmp_path / "tamper.txt"
        ),
    )
    path = _receipt_path(receipt)

    forged_mapping = copy.deepcopy(receipt)
    forged_mapping["authority_boundaries"]["truth_authorized"] = True
    with pytest.raises(ResearchWorkerIntegrityError):
        receipt_summary(forged_mapping, receipt_path=path)

    original_bytes = path.read_bytes()
    path.write_bytes(original_bytes + b" \n")
    with pytest.raises(ResearchWorkerIntegrityError, match="canonical JSON bytes"):
        receipt_summary(receipt, receipt_path=path)


def test_receipt_path_substitution_is_rejected(tmp_path: Path) -> None:
    adapter = _adapter(tmp_path, study_id="research-worker-path-test")
    receipt = _invoke_probe(
        adapter,
        role="judge",
        context="path-substitution",
        payload=_probe_payload(
            read_path=Path(__file__), write_path=tmp_path / "path.txt"
        ),
    )
    substituted = tmp_path / "substituted-receipt.json"
    substituted.write_bytes(_receipt_path(receipt).read_bytes())

    with pytest.raises(ResearchWorkerIntegrityError, match="path mismatch"):
        receipt_summary(receipt, receipt_path=substituted)
