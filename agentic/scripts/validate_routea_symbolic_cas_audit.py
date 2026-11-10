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
"""Validate the Route A symbolic/CAS audit report."""

from __future__ import annotations

import json
from pathlib import Path

from agentic_common import ROOT, clean_text, fail, rel


REPORT = ROOT / "agentic/reports/results_ellaboration/a-finite-schur-feshbach-test-for-reflected-wilson-blocks-an-explicit-four-dimens/routea_symbolic_cas_audit.json"
SKILL = ROOT / "skills/results_ellaboration/routea-symbolic-cas-auditor/SKILL.md"
SCRIPT = ROOT / "skills/results_ellaboration/routea-symbolic-cas-auditor/scripts/audit_routea_symbolic_cas.py"


def require(condition: bool, message: str) -> None:
    if not condition:
        fail(message)


def main() -> int:
    for path in [REPORT, SKILL, SCRIPT]:
        require(path.exists(), f"missing {rel(path)}")
    data = json.loads(REPORT.read_text(encoding="utf-8"))
    require(data.get("schema") == "abducer.routea_symbolic_cas_audit.v1", "unexpected symbolic CAS audit schema")
    require("finite source-collision" in clean_text(data.get("claim_boundary")).lower(), "claim boundary must stay finite/source-collision scoped")
    joined = clean_text(data).lower()
    for marker in [
        "rank_one_schur_feshbach_algebra",
        "same_theory_normalization_counterexample",
        "endpoint_null_channel_incidence_identity",
        "two_sided_endpoint_certificate_logic",
        "geometric_collar_coefficient_obligation_extraction",
        "does not discharge geometric-collar construction",
        "continuum reconstruction",
        "spectral-gap",
    ]:
        require(marker in joined, f"symbolic CAS audit missing `{marker}`")
    checks = data.get("checks", [])
    require(isinstance(checks, list) and len(checks) >= 5, "expected at least five symbolic checks")
    by_object = {clean_text(row.get("mathematical_object")): row for row in checks if isinstance(row, dict)}
    source = by_object.get("finite source-collision normalized reflected Gram block", {})
    require(source.get("status") == "exact_symbolic_certificate", "source-collision block must be exact symbolic certificate")
    source_checks = source.get("checks", {})
    for key in ["A_equals_sigma_bbT", "C_equals_corrected_formula", "det_q_formula", "u_A_u_equals_2sigma", "v_C_v_equals_2tau_over_3", "spurious_sigma2_removed"]:
        require(source_checks.get(key) is True, f"source-collision check `{key}` failed")
    endpoint = by_object.get("zero-diagonal endpoint/null-channel incidence form", {})
    require(endpoint.get("identity") == "2*R12 - 4*R13 - 4*R23", "endpoint null identity mismatch")
    normalization = by_object.get("same-theory normalization quotient gate", {})
    require("-1" in clean_text(normalization.get("entrywise_inverse_eigenvalues")), "normalization counterexample must expose a negative eigenvalue")
    skill_text = SKILL.read_text(encoding="utf-8").lower()
    for marker in ["codex exec protocol", "epistemic discipline", "output contract", "failure/demotion"]:
        require(marker in skill_text, f"{rel(SKILL)} missing `{marker}`")
    print(f"validated {rel(REPORT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
