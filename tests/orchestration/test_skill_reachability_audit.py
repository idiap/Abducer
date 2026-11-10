# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
"""Regression tests for commit-backed discovery-skill reachability.

The acceptance cycle is a stable registry/subprocess exercise checked into the
repository.  These tests deliberately distinguish executable receipts from the
stronger claim that their exact bytes caused a semantic event in the current
canonical transaction commit.
"""

from __future__ import annotations

import copy
import json
import shutil
import subprocess
import sys
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "agentic/scripts"))

from agentic.discovery.contracts import ContractError, canonical_digest  # noqa: E402
from run_skill_reachability_audit import build_reachability_report, comparison_projection  # noqa: E402
from agentic.discovery.cycle import run_canonical_discovery_cycle  # noqa: E402
from tests.discovery.test_canonical_discovery_cycle import CanonicalExercise  # noqa: E402

CORE_OPERATORS = {
    "frontier-literature-assimilator", "high-risk-hypothesis-forger",
    "parallel-hypothesis-portfolio", "reflective-conceptual-discovery",
    "reflective-theory-synthesizer", "blind-conceptual-preference-adjudicator",
}


@pytest.fixture(scope="module")
def canonical(tmp_path_factory) -> dict:
    """Generate real current receipts/commit rather than trust a mutable publication.

    The local fixture exercises the six core skill routes. Conditional formal,
    experiment and causal-planner operators remain unexercised; their registration
    must never turn into inferred execution or consumption.
    """
    base = tmp_path_factory.mktemp("skill-reachability")
    exercise = CanonicalExercise(base, live=True, experiment=False)
    cycle = run_canonical_discovery_cycle(**exercise.cycle_kwargs())
    path = base / "cycle.json"
    path.write_text(json.dumps(cycle), encoding="utf-8")
    return {"cycle": path, "state": exercise.state_root,
            "workspace": exercise.workspace, "receipts": exercise.workspace / "operator-receipts",
            "target": exercise.target_id, "run": exercise.run_id}


def _operator_rows(report: dict) -> list[dict]:
    return [row for row in report["skills"] if row["operator"]]


def test_all_six_routes_are_feedback_effective_only_through_exact_commit(canonical) -> None:
    report = build_reachability_report(
        receipt_root=canonical["receipts"],
        artifact_root=canonical["workspace"],
        canonical_cycle_path=canonical["cycle"],
        canonical_state_root=canonical["state"],
        target_id=canonical["target"],
        run_id="run-canonical-cycle",
    )

    # The live registry also declares conditional routes which this fixture does
    # not execute. Check exact core coverage without promoting those other routes.
    registry = json.loads((ROOT / "agentic/registries/discovery_operator_registry.yaml").read_text())
    rows = {row["skill_id"]: row for row in _operator_rows(report)}
    assert set(rows) == {row["operator_id"] for row in registry["operators"]}
    assert {name for name, row in rows.items() if row["levels"]["feedback_effective"]} == CORE_OPERATORS
    assert all(rows[name]["attained_level"] == "feedback_effective" for name in CORE_OPERATORS)
    assert all(not row["levels"]["consumed"] for name, row in rows.items() if name not in CORE_OPERATORS)
    assert report["all_operators_feedback_effective"] is False
    assert report["evidence_errors"] == []
    assert report["canonical_authorization"]["manifest_digest"].startswith("sha256:")


def test_hand_authored_feedback_booleans_cannot_establish_consumption(tmp_path: Path, canonical) -> None:
    projection = json.loads(canonical["cycle"].read_text(encoding="utf-8"))
    fake_feedback = tmp_path / "claimed-feedback.json"
    fake_feedback.write_text(
        json.dumps({"feedback_edges": projection["feedback_edges"]}), encoding="utf-8"
    )

    report = build_reachability_report(
        receipt_root=canonical["receipts"],
        artifact_root=canonical["workspace"],
        feedback_path=fake_feedback,
    )

    assert report["legacy_feedback_edge_count"] == len(projection["feedback_edges"]) == 9
    assert report["legacy_feedback_authoritative"] is False
    assert report["all_operators_feedback_effective"] is False
    assert {row["skill_id"] for row in _operator_rows(report) if row["levels"]["exercised"]} == CORE_OPERATORS
    assert all(not row["levels"]["consumed"] for row in _operator_rows(report))


def test_receipt_request_or_output_drift_breaks_canonical_feedback_binding(
    tmp_path: Path, canonical,
) -> None:
    copied_workspace = tmp_path / "workspace"
    shutil.copytree(canonical["workspace"], copied_workspace)
    receipt_path = next((copied_workspace / "operator-receipts").rglob("attempt-1.json"))
    receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
    receipt["request_id"] = "opreq.tampered-but-schema-valid"
    receipt_path.write_text(json.dumps(receipt), encoding="utf-8")

    report = build_reachability_report(
        receipt_root=copied_workspace / "operator-receipts",
        artifact_root=copied_workspace,
        canonical_cycle_path=canonical["cycle"],
        canonical_state_root=canonical["state"],
    )

    assert report["all_operators_feedback_effective"] is False
    assert any("request_identity" in error for error in report["evidence_errors"])


def test_requested_target_and_run_must_match_the_canonical_cycle(canonical) -> None:
    with pytest.raises(ContractError, match="requested target_id"):
        build_reachability_report(
            receipt_root=canonical["receipts"],
            artifact_root=canonical["workspace"],
            canonical_cycle_path=canonical["cycle"],
            canonical_state_root=canonical["state"],
            target_id="wrong-target",
            run_id="run-canonical-cycle",
        )


def test_cli_check_mode_is_read_only_and_rejects_stale_projection(
    tmp_path: Path, canonical,
) -> None:
    json_output = tmp_path / "reachability.json"
    markdown_output = tmp_path / "reachability.md"
    base = [
        sys.executable,
        "agentic/scripts/run_skill_reachability_audit.py",
        "--receipt-root",
        str(canonical["receipts"]),
        "--artifact-root",
        str(canonical["workspace"]),
        "--canonical-cycle",
        str(canonical["cycle"]),
        "--canonical-state-root",
        str(canonical["state"]),
        "--target-id",
        canonical["target"],
        "--run-id",
        "run-canonical-cycle",
        "--json-output",
        str(json_output),
        "--markdown-output",
        str(markdown_output),
    ]
    generated = subprocess.run(base, cwd=ROOT, capture_output=True, text=True)
    assert generated.returncode == 0, generated.stderr
    # The optional all-registered-operators gate must still reject because three
    # conditional routes lack execution receipts in this bounded core fixture.
    required = subprocess.run([*base, "--require-feedback-effective"], cwd=ROOT, capture_output=True, text=True)
    assert required.returncode == 1
    before = (json_output.read_bytes(), markdown_output.read_bytes())
    checked = subprocess.run(
        [*base, "--check"], cwd=ROOT, capture_output=True, text=True
    )
    assert checked.returncode == 0, checked.stderr
    assert before == (json_output.read_bytes(), markdown_output.read_bytes())

    markdown_output.write_text("stale\n", encoding="utf-8")
    stale = subprocess.run(
        [*base, "--check"], cwd=ROOT, capture_output=True, text=True
    )
    assert stale.returncode == 2
    assert "stale" in stale.stderr


@pytest.fixture(scope="module")
def audit_report(canonical) -> dict:
    """Keep one genuine issued projection for adversarial saved-report probes."""
    return build_reachability_report(
        receipt_root=canonical["receipts"], artifact_root=canonical["workspace"],
        canonical_cycle_path=canonical["cycle"], canonical_state_root=canonical["state"],
    )


def _reseal_report(report) -> None:
    """Model a self-consistent but altered saved report, not just corrupt bytes."""
    authorization = report["canonical_authorization"]
    authorization["present_investment_decision_digest"] = canonical_digest(authorization["present_investment_decision"])
    original = copy.deepcopy(authorization)
    original.pop("portable_projection_digest")
    original.pop("verifier_issued_projection_digest")
    for field in ("transaction_root", "commit_path", "manifest_path", "projection_path"):
        if not Path(original[field]).is_absolute():
            original[field] = str((ROOT / original[field]).resolve())
    authorization["verifier_issued_projection_digest"] = canonical_digest(original)
    authorization["portable_projection_digest"] = canonical_digest(authorization, exclude_keys=("portable_projection_digest",))


def test_check_rejects_corrupt_saved_portable_digest(audit_report) -> None:
    changed = copy.deepcopy(audit_report)
    changed["canonical_authorization"]["portable_projection_digest"] = "sha256:" + "0" * 64
    with pytest.raises(ContractError, match="portable projection digest"):
        comparison_projection(changed)


@pytest.mark.parametrize("mutation", ["decision", "identity", "json-type", "evidence"])
def test_check_retains_decisions_identities_types_and_evidence_after_rehash(audit_report, mutation) -> None:
    changed = copy.deepcopy(audit_report)
    authorization = changed["canonical_authorization"]
    if mutation == "decision":
        authorization["present_investment_decision"]["active_investment_gate"] = "block"
    elif mutation == "identity":
        authorization["run_id"] = "another-run"
    elif mutation == "json-type":
        # Python True == 1; canonical JSON equality must still reject this edit.
        authorization["present_investment_decision"]["authoritative"] = 1
    else:
        changed["skills"][0]["levels"]["consumed"] = not changed["skills"][0]["levels"]["consumed"]
    _reseal_report(changed)
    assert canonical_digest(comparison_projection(changed)) != canonical_digest(comparison_projection(audit_report))
