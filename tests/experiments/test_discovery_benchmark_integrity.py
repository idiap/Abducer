# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
"""Synthetic-boundary and live hidden-task benchmark integrity tests."""

from __future__ import annotations

import copy
import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import pytest

import agentic.discovery.benchmark as benchmark_module
from agentic.discovery.benchmark import (
    BenchmarkIntegrityError,
    REQUIRED_LIVE_CONDITIONS,
    RUBRIC_DIMENSIONS,
    build_human_evidence_trust_anchor,
    capture_live_hidden_task_outputs,
    evaluate_benchmark_manifest,
    scan_leakage,
)
from agentic.discovery.benchmark_process import ExternalBenchmarkProcessAdapter


ROOT = Path(__file__).resolve().parents[2]
FIXTURES = ROOT / "tests/fixtures/discovery_benchmarks"


def test_synthetic_manifest_passes_protocol_but_never_claims_replication() -> None:
    report = evaluate_benchmark_manifest(FIXTURES / "frozen.json")
    assert report["case_count"] == 3
    assert report["domain_count"] == 3
    assert report["protocol_valid"] is True
    assert report["synthetic_fixture_passed"] is True
    assert report["efficacy_authorized"] is False
    assert report["replicated"] is False
    assert all(row["human_rating_status"] == "not_human_synthetic_fixture" for row in report["cases"])


def test_decoys_detect_all_four_leakage_channels() -> None:
    payload = json.loads((FIXTURES / "decoys.json").read_text(encoding="utf-8"))
    for case in payload["cases"]:
        assert case["channel"] in scan_leakage(case["text"], payload["ground_truth"])


def test_working_kbs_do_not_expose_truth_labels_or_paths() -> None:
    manifest = json.loads((FIXTURES / "frozen.json").read_text(encoding="utf-8"))
    for case in manifest["cases"]:
        truth = json.loads((FIXTURES / case["ground_truth"]).read_text(encoding="utf-8"))
        working = (FIXTURES / case["working_kb"]).read_text(encoding="utf-8")
        assert scan_leakage(working, truth) == set()


def test_synthetic_leak_future_source_budget_and_fake_creativity_fail(tmp_path: Path) -> None:
    copied = tmp_path / "bench"
    shutil.copytree(FIXTURES, copied)
    manifest = json.loads((copied / "frozen.json").read_text(encoding="utf-8"))
    first = manifest["cases"][0]
    packet_path = copied / first["case_packet"]
    original = json.loads(packet_path.read_text(encoding="utf-8"))

    packet = copy.deepcopy(original)
    packet["candidate_output"]["generation_inputs"].append("resolvent-compatible dilation")
    packet_path.write_text(json.dumps(packet), encoding="utf-8")
    with pytest.raises(BenchmarkIntegrityError, match="generation inputs"):
        evaluate_benchmark_manifest(copied / "frozen.json")

    packet = copy.deepcopy(original)
    packet["time_slice"]["pre_cutoff_sources"][0]["publication_date"] = "2025-01-01"
    packet_path.write_text(json.dumps(packet), encoding="utf-8")
    with pytest.raises(BenchmarkIntegrityError, match="future source"):
        evaluate_benchmark_manifest(copied / "frozen.json")

    packet = copy.deepcopy(original)
    packet["conservative_baseline"]["resource_budget"]["tokens"] += 1
    packet_path.write_text(json.dumps(packet), encoding="utf-8")
    with pytest.raises(BenchmarkIntegrityError, match="matched budgets"):
        evaluate_benchmark_manifest(copied / "frozen.json")

    packet = copy.deepcopy(original)
    packet["aggressive_portfolio"]["hypotheses"][0]["mechanism"] = ""
    packet_path.write_text(json.dumps(packet), encoding="utf-8")
    with pytest.raises(BenchmarkIntegrityError, match="shock alone"):
        evaluate_benchmark_manifest(copied / "frozen.json")


def _live_manifest(root: Path) -> Path:
    (root / "tasks").mkdir(parents=True)
    (root / "truth").mkdir()
    tasks = []
    for index, domain in enumerate(("domain-a", "domain-b", "domain-c"), start=1):
        case_id = f"case-{index}"
        task_ref = f"tasks/{case_id}.json"
        truth_ref = f"truth/{case_id}.json"
        (root / task_ref).write_text(
            json.dumps({"case_id": case_id, "open_question": f"Question {index}"}),
            encoding="utf-8",
        )
        (root / truth_ref).write_text(
            json.dumps(
                {
                    "labels": [f"withheld-label-{index}"],
                    "aliases": [],
                    "latex_signatures": [],
                    "dependency_edges": [],
                    "forbidden_artifact_markers": [truth_ref],
                    "expected": {"conceptual_transformation_ids": [f"transform-{index}"]},
                }
            ),
            encoding="utf-8",
        )
        tasks.append(
            {"case_id": case_id, "domain": domain, "task_packet": task_ref, "ground_truth": truth_ref}
        )
    manifest = {
        "schema_version": "2.0.0",
        "benchmark_mode": "live_external_hidden_task",
        "benchmark_id": "live-external-test-v1",
        "split": "external_hidden",
        "ground_truth_authorship": {
            "author_id": "external-task-authority",
            "independent_of_system": True,
        },
        "configuration_provenance": {
            "selected_from_splits": ["train", "development"],
            "frozen_scores_observed": False,
        },
        "minimum_domains": 3,
        "conditions": list(REQUIRED_LIVE_CONDITIONS),
        "repetitions": 5,
        "resource_budget": {"tokens": 100, "wall_seconds": 5, "cost_units": 1},
        "condition_randomization_seed": "sealed-order-17",
        "output_capture": "capture.json",
        "minimum_standardized_effect": 0.3,
        "preregistration": {
            "registered_before_capture": True,
            "protocol_id": "registry:test-live-v1",
            "analysis_plan_digest": "sha256:" + "a" * 64,
        },
        "tasks": tasks,
    }
    path = root / "manifest.json"
    path.write_text(json.dumps(manifest, sort_keys=True), encoding="utf-8")
    return path


def _capture_live(path: Path) -> dict:
    def runner(request: dict) -> dict:
        assert "ground_truth" not in json.dumps(request)
        return {
            "candidate_output": {
                "conceptual_transformation_ids": [],
                "condition_execution": request["condition"],
                "reflection": f"run-{request['repetition']}",
            },
            "resource_usage": {"tokens": 80, "wall_seconds": 1.0, "cost_units": 0.8},
            "generation_input_refs": [f"tasks/{request['case_id']}.json"],
        }

    return capture_live_hidden_task_outputs(path, runner)


def _add_authenticated_ratings(path: Path, capture: dict) -> tuple[dict, object]:
    ratings = []
    disclosures = [
        {"rater_id": rater, "independent_of_system": True, "conflict_disclosed": True}
        for rater in ("expert-1", "expert-2")
    ]
    condition_score = {
        "full_discovery": 5,
        "baseline_conservative": 2,
        "baseline_literature_only": 3,
        "ablation_no_reflection": 3,
        "ablation_no_literature": 2,
        "ablation_no_parallel": 3,
    }
    for row in capture["outputs"]:
        base = condition_score[row["condition"]]
        # Variation is independent of condition enough to avoid degenerate effects.
        adjustment = 1 if (row["repetition"] + int(row["case_id"].split("-")[-1])) % 4 == 0 else 0
        for rater_index, rater in enumerate(("expert-1", "expert-2")):
            score = max(1, min(5, base - (1 if rater_index and adjustment else 0)))
            ratings.append(
                {
                    "output_id": row["output_id"],
                    "rater_id": rater,
                    "scores": {dimension: score for dimension in RUBRIC_DIMENSIONS},
                }
            )
    packet = {
        "schema_version": "1.0.0",
        "benchmark_id": capture["benchmark_id"],
        "capture_digest": capture["content_digest"],
        "condition_labels_hidden": True,
        "minimum_raters_per_output": 2,
        "minimum_agreement": 0.7,
        "adjudication_policy": "A third blind expert adjudicates material disagreement.",
        "rater_disclosures": disclosures,
        "ratings": ratings,
    }
    raw = json.dumps(packet, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ratings_path = path.parent / "human-ratings.json"
    ratings_path.write_bytes(raw)
    descriptor = {
        "artifact_ref": "human-ratings.json",
        "sha256": "sha256:" + hashlib.sha256(raw).hexdigest(),
        "byte_length": len(raw),
        "media_type": "application/json",
        "authority_id": "external-blinding-service-v1",
    }
    manifest = json.loads(path.read_text(encoding="utf-8"))
    manifest["human_evidence"] = descriptor
    path.write_text(json.dumps(manifest, sort_keys=True), encoding="utf-8")

    def verifier(supplied_raw: bytes, supplied_descriptor: dict) -> dict:
        return {
            "authenticated": supplied_raw == raw,
            "blinding_verified": True,
            "independent_raters_verified": True,
            "ratings_immutable": True,
            "artifact_sha256": "sha256:" + hashlib.sha256(supplied_raw).hexdigest(),
            "authority_id": supplied_descriptor["authority_id"],
        }

    return descriptor, verifier


def test_live_capture_runs_full_equal_budget_matrix_and_fails_closed_without_humans(tmp_path: Path) -> None:
    manifest = _live_manifest(tmp_path)
    capture = _capture_live(manifest)
    assert capture["truth_loaded_during_capture"] is False
    assert len(capture["outputs"]) == 3 * 5 * len(REQUIRED_LIVE_CONDITIONS)
    assert {row["allocated_budget"]["tokens"] for row in capture["outputs"]} == {100}
    report = evaluate_benchmark_manifest(manifest)
    assert report["protocol_valid"] is True
    assert report["human_evidence"]["status"] == "absent"
    assert report["efficacy_authorized"] is False
    assert report["replicated"] is False


def test_in_process_verifier_and_missing_trust_anchor_cannot_authorize_efficacy(tmp_path: Path) -> None:
    manifest = _live_manifest(tmp_path)
    capture = _capture_live(manifest)
    _descriptor, verifier = _add_authenticated_ratings(manifest, capture)

    unverified = evaluate_benchmark_manifest(manifest)
    assert unverified["human_evidence"]["status"] == "verifier_absent"
    assert unverified["efficacy_authorized"] is False

    report = evaluate_benchmark_manifest(manifest, human_evidence_verifier=verifier)
    assert report["human_evidence"]["status"] == "trust_anchor_absent"
    assert report["efficacy_authorized"] is False
    anchor = build_human_evidence_trust_anchor(
        trust_anchor_id="configured-separately",
        authority_id="external-blinding-service-v1",
        benchmark_id="live-external-test-v1",
        verifier_command_authority_digest="sha256:" + "f" * 64,
    )
    ungoverned = evaluate_benchmark_manifest(
        manifest,
        human_evidence_verifier=verifier,
        human_evidence_trust_anchor=anchor,
    )
    assert ungoverned["human_evidence"]["status"] == "verifier_execution_unavailable"
    assert ungoverned["efficacy_authorized"] is False
    assert ungoverned["replicated"] is False


@pytest.mark.expensive
def test_governed_cli_capture_and_caller_anchor_remain_protocol_only() -> None:
    repo = Path(__file__).resolve().parents[2]
    simulator = repo / "skills/orchestration/kb-orchestrator/scripts/simulate_theorem_discovery.py"
    with tempfile.TemporaryDirectory(prefix=".benchmark-cli-", dir=repo) as raw:
        root = Path(raw)
        manifest = _live_manifest(root)
        execution_root = root / "processes"
        runner_code = (
            "import json,sys; r=json.load(sys.stdin); "
            "print(json.dumps({'candidate_output':{'conceptual_transformation_ids':[],"
            "'condition_execution':r['condition'],'reflection':'run-'+str(r['repetition'])},"
            "'resource_usage':{'tokens':80,'wall_seconds':1.0,'cost_units':.8},"
            "'generation_input_refs':['tasks/'+r['case_id']+'.json']}))"
        )
        capture_run = subprocess.run(
            [
                sys.executable,
                str(simulator),
                "--benchmark-manifest",
                str(manifest),
                "--benchmark-capture-output",
                str(root / "capture.json"),
                "--benchmark-runner-command",
                json.dumps([sys.executable, "-c", runner_code]),
                "--benchmark-run-id",
                "cli-capture",
                "--benchmark-execution-root",
                str(execution_root),
            ],
            cwd=repo,
            text=True,
            capture_output=True,
            timeout=180,
            check=False,
        )
        assert capture_run.returncode == 0, capture_run.stderr
        capture = json.loads((root / "capture.json").read_text(encoding="utf-8"))
        assert len(capture["outputs"]) == 90
        capture_index = json.loads(
            (execution_root / "cli-capture/indices/benchmark_runner.json").read_text(encoding="utf-8")
        )
        assert capture_index["receipt_count"] == 90
        assert capture_index["accounting_boundary"]["isolation"] == (
            "local_subprocess_protocol_only_no_hiddenness_or_external_efficacy"
        )
        assert {row["isolation_status"] for row in capture["outputs"]} == {
            "unisolated_protocol_only"
        }
        assert not any(row["external_efficacy_eligible"] for row in capture["outputs"])
        _add_authenticated_ratings(manifest, capture)

        verifier_code = (
            "import hashlib,json,sys; r=json.load(sys.stdin); raw=r['artifact_utf8'].encode(); d=r['descriptor']; "
            "print(json.dumps({'authenticated':True,'blinding_verified':True,"
            "'independent_raters_verified':True,'ratings_immutable':True,"
            "'artifact_sha256':'sha256:'+hashlib.sha256(raw).hexdigest(),"
            "'authority_id':d['authority_id']}))"
        )
        authority_probe = ExternalBenchmarkProcessAdapter(
            command=[sys.executable, "-c", verifier_code],
            role="human_evidence_verifier",
            benchmark_id="live-external-test-v1",
            benchmark_run_id="cli-verifier",
            run_root=execution_root,
        )
        anchor = build_human_evidence_trust_anchor(
            trust_anchor_id="external-review-registry-v1",
            authority_id="external-blinding-service-v1",
            benchmark_id="live-external-test-v1",
            verifier_command_authority_digest=authority_probe.command_authority["content_digest"],
        )
        anchor_path = root / "trust-anchor.json"
        anchor_path.write_text(json.dumps(anchor, sort_keys=True), encoding="utf-8")
        verification_run = subprocess.run(
            [
                sys.executable,
                str(simulator),
                "--benchmark-manifest",
                str(manifest),
                "--human-evidence-verifier-command",
                json.dumps([sys.executable, "-c", verifier_code]),
                "--human-evidence-trust-anchor",
                str(anchor_path),
                "--benchmark-run-id",
                "cli-verifier",
                "--benchmark-execution-root",
                str(execution_root),
            ],
            cwd=repo,
            text=True,
            capture_output=True,
            timeout=60,
            check=False,
        )
        assert verification_run.returncode == 0, verification_run.stderr
        report = json.loads(verification_run.stdout)
        assert report["governed_process_capture"] is True
        assert report["externally_governed_capture"] is False
        assert report["capture_isolation_status"] == "local_subprocess_protocol_only"
        assert report["human_evidence"]["status"] == "authenticated_protocol_only"
        assert report["human_evidence"]["trust_anchor_digest"] == anchor["content_digest"]
        assert report["authentication_verified"] is True
        assert report["caller_policy_eligible"] is True
        assert report["external_authority_eligible"] is False
        assert report["positive_efficacy_gate_status"] == "positive_caller_policy_only"
        assert report["replication_gate_status"] == "passed_caller_policy_only"
        assert report["efficacy_authorized"] is False
        assert report["replicated"] is False
        assert set(report["effect_estimates"]) == set(REQUIRED_LIVE_CONDITIONS) - {"full_discovery"}
        assert all(row["n_pairs"] == 15 for row in report["effect_estimates"].values())

        replicated_run = subprocess.run(
            [
                sys.executable,
                str(simulator),
                "--benchmark-manifest",
                str(manifest),
                "--human-evidence-verifier-command",
                json.dumps([sys.executable, "-c", verifier_code]),
                "--human-evidence-trust-anchor",
                str(anchor_path),
                "--benchmark-run-id",
                "cli-verifier",
                "--benchmark-execution-root",
                str(execution_root),
                "--require-replicated",
            ],
            cwd=repo,
            text=True,
            capture_output=True,
            timeout=60,
            check=False,
        )
        assert replicated_run.returncode == 3
        replicated_report = json.loads(replicated_run.stdout)
        assert replicated_report["replication_gate_status"] == "passed_caller_policy_only"
        assert replicated_report["replicated"] is False

        reopened = ExternalBenchmarkProcessAdapter(
            command=[sys.executable, "-c", verifier_code],
            role="human_evidence_verifier",
            benchmark_id="live-external-test-v1",
            benchmark_run_id="cli-verifier",
            run_root=execution_root,
        )
        wrong_anchor = build_human_evidence_trust_anchor(
            trust_anchor_id="wrong-registry",
            authority_id="external-blinding-service-v1",
            benchmark_id="live-external-test-v1",
            verifier_command_authority_digest="sha256:" + "e" * 64,
        )
        refused = evaluate_benchmark_manifest(
            manifest,
            human_evidence_verifier=reopened.verifier,
            human_evidence_trust_anchor=wrong_anchor,
        )
        assert refused["human_evidence"]["status"] == "trust_anchor_mismatch"
        assert refused["efficacy_authorized"] is False
        assert refused["replicated"] is False

        def forged_callback(raw_bytes: bytes, descriptor: dict) -> dict:
            forged = reopened.verifier(raw_bytes, descriptor)
            forged["authenticated"] = False
            return forged

        with pytest.raises(BenchmarkIntegrityError, match="governed response receipt"):
            evaluate_benchmark_manifest(
                manifest,
                human_evidence_verifier=forged_callback,
                human_evidence_trust_anchor=anchor,
            )


def test_effect_and_replication_statuses_keep_negative_null_and_underpowered_distinct() -> None:
    def estimate(
        *, n: int, lower: float, effect: float | None, degenerate: bool = False
    ) -> dict:
        return {
            "n_pairs": n,
            "confidence_interval_95": [lower, max(lower, 0.1)],
            "standardized_effect_size": effect,
            "degenerate_variance": degenerate,
        }

    positive = estimate(n=5, lower=0.1, effect=0.5)
    negative = estimate(n=5, lower=-0.3, effect=-0.4)
    null = estimate(n=5, lower=0.0, effect=None, degenerate=True)
    underpowered = estimate(n=4, lower=0.1, effect=0.5)

    assert benchmark_module._positive_effect_gate_status(
        {"baseline_conservative": negative}, 0.3
    ) == "null_or_negative"
    assert benchmark_module._positive_effect_gate_status(
        {"baseline_conservative": null}, 0.3
    ) == "null_or_negative"
    assert benchmark_module._positive_effect_gate_status(
        {"baseline_conservative": underpowered}, 0.3
    ) == "underpowered"
    assert benchmark_module._replication_gate_status(
        {"baseline_conservative": positive, "ablation_no_parallel": negative}, 0.3
    ) == "not_replicated"
    assert benchmark_module._replication_gate_status(
        {"baseline_conservative": positive, "ablation_no_parallel": underpowered}, 0.3
    ) == "underpowered"


def test_live_manifest_rejects_missing_ablation_or_too_few_repetitions(tmp_path: Path) -> None:
    manifest_path = _live_manifest(tmp_path)
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["conditions"].remove("ablation_no_parallel")
    manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
    with pytest.raises(BenchmarkIntegrityError, match="requires full"):
        capture_live_hidden_task_outputs(manifest_path, lambda request: {})
    manifest["conditions"] = list(REQUIRED_LIVE_CONDITIONS)
    manifest["repetitions"] = 1
    manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
    with pytest.raises(BenchmarkIntegrityError, match="at least 5"):
        capture_live_hidden_task_outputs(manifest_path, lambda request: {})
