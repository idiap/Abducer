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
"""Emit one bounded cohere-fast YM adaptive-frontier inference packet."""
from __future__ import annotations

import copy
import hashlib
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "hooks/scripts"))

from cohere_fast_intake import parse_invocation  # noqa: E402
from agentic.orchestration.cohere_fast_runner import (  # noqa: E402
    CohereFastRunner,
    canonical_digest,
)
from agentic.discovery.contracts import validate_instance  # noqa: E402
from skills.common.ym_abstraction_calibrations import (  # noqa: E402
    run_ym_calibration,
    validate_ym_calibration,
)

TARGET = (
    "Yang-Mills existence and mass gap: identify a conceptually distinct, "
    "falsifiable physical-sector route after quarantine of the finite "
    "endpoint source-table branch"
)
ARCHIVE_DIGEST = (
    "sha256:67d573694581c1eb3bc2737c95cb9df48d5f03a551375510055ba3e2770d0bec"
)
LATEST = (
    "agentic/reports/discovery_marathon/targets/"
    "yang-mills-existence-and-mass-gap-target/latest.json"
)
PILOT = (
    "agentic/reports/discovery_marathon/targets/"
    "yang-mills-existence-and-mass-gap-target/proof_objects/"
    "endpoint_source_table_pilot.json"
)
DEMOTION = (
    "agentic/reports/discovery_marathon/targets/"
    "yang-mills-existence-and-mass-gap-target/proof_objects/"
    "endpoint_route_demotion_packet.json"
)
LOCKIN = (
    "agentic/reports/proof_lockin/targets/"
    "yang-mills-existence-and-mass-gap-target/latest.json"
)
KB = "KB/yang-mills-existence-and-mass-gap.kb.md"


def file_digest(relative: str) -> str:
    return "sha256:" + hashlib.sha256((ROOT / relative).read_bytes()).hexdigest()


def source(member_path: str, member_digest: str) -> dict:
    return {
        "archive_sha256": ARCHIVE_DIGEST,
        "member_path": member_path,
        "member_sha256": "sha256:" + member_digest,
    }


def build_packet(activation: dict) -> dict:
    run_id = activation["run_id"]
    claims = [
        {
            "claim": (
                "The finite post-H,K endpoint branch remains quarantined: "
                "the same-regulator source table and cutoff-uniform tail bound "
                "are absent, so no endpoint sign or Clay-level conclusion is licensed."
            ),
            "status": "sourced",
            "ceiling": "candidate",
        },
        {
            "claim": (
                "A viable conceptual frontier is a two-axis physical-sector carrier "
                "V_{alpha,p}: alpha controls geometric resolution while p orders "
                "actual inclusion of centered gauge-invariant Wilson-net spans on "
                "one fixed SU(3) heat-kernel regulator trajectory."
            ),
            "status": "candidate",
            "ceiling": "candidate",
        },
        {
            "claim": (
                "For actually nested V_{alpha,p}, the projected transfer-operator "
                "Rayleigh supremum at one fixed physical time t0 is nondecreasing in p, "
                "so its physical mass estimate is nonincreasing, provided the actual "
                "OS quotient images are nested and use the same transfer contraction. "
                "No such monotonicity is inferred from the numerical order of alpha."
            ),
            "status": "candidate",
            "ceiling": "candidate",
        },
        {
            "claim": (
                "Conditionally, a common fixed-time quadratic-form bound on a dense, "
                "vacuum-orthogonal recovered union extends to the whole physical "
                "sector by continuity. Equivalently, a common exclusion of [0,m) "
                "extends because spectral projections are bounded."
            ),
            "status": "candidate",
            "ceiling": "candidate",
        },
        {
            "claim": (
                "Strict regulator-level OS positivity margins are unnecessary; "
                "nonnegativity, or a certified vanishing negative defect, together "
                "with convergence of reflection forms is the closed-cone condition."
            ),
            "status": "candidate",
            "ceiling": "candidate",
        },
        {
            "claim": (
                "A nonzero OS norm is the minimal anti-vacuity witness. A surviving "
                "connected higher cumulant is a separate, stronger non-Gaussian or "
                "interacting witness and cannot substitute for density or the gap."
            ),
            "status": "candidate",
            "ceiling": "candidate",
        },
        {
            "claim": (
                "A functional inequality for auxiliary Langevin or sampling dynamics "
                "does not constrain the Hamiltonian spectrum without an intertwining "
                "theorem; using it directly would be a proxy shift."
            ),
            "status": "candidate",
            "ceiling": "candidate",
        },
        {
            "claim": (
                "No alpha-indexed recovery errors, physical-sector transfer matrices, "
                "density residuals, nontriviality witnesses, or common physical mass "
                "floor are currently available. The route remains unproved."
            ),
            "status": "sourced",
            "ceiling": "candidate",
        },
        {
            "claim": (
                "A sealed direct-sum calibration has a positive visible-sector gap "
                "but a zero full gap, demonstrating that the alpha=1 finite carrier "
                "can only falsify or characterize visibility until density is proved."
            ),
            "status": "independently_supported",
            "ceiling": "candidate",
        },
        {
            "claim": (
                "Sealed finite-volume and noncommuting-limit calibrations show that "
                "positive finite-regulator estimates need uniform volume/cutoff control "
                "and an explicit order-of-limits theorem."
            ),
            "status": "independently_supported",
            "ceiling": "candidate",
        },
        {
            "claim": (
                "Fixed-rank recovery obstruction: if M regulated carrier vectors "
                "recover coherently to a common continuum Hilbert space, their limit "
                "span is closed and has dimension at most M; it cannot be dense when "
                "the vacuum-orthogonal physical sector has dimension greater than M."
            ),
            "status": "candidate",
            "ceiling": "candidate",
        },
        {
            "claim": (
                "For the three-channel alpha=1,p=1 carrier, coherent recovery therefore "
                "cannot prove density in an infinite-dimensional physical sector, while "
                "failure of coherent recovery triggers proxy-shift or noncommuting-limit "
                "quarantine. Any viable density route must let inclusion degree p grow."
            ),
            "status": "candidate",
            "ceiling": "candidate",
        },
    ]
    obligations = [
        "Fix one cutoff/volume trajectory and a theory-preserving discretization of each Wilson net.",
        "For each geometric alpha, construct inclusion-ordered centered V_{alpha,p} and prove density of the recovered p-union in the vacuum-orthogonal continuum OS Hilbert space.",
        "Choose and justify an unbounded carrier-growth law p=p(n), with approximation, Gram-conditioning, and recovery errors controlled along the diagonal limit.",
        "Certify convergence and nonnegativity of every recovered finite reflection matrix; separately prove semigroup/Hamiltonian convergence.",
        "Control recovery and time-translation intertwining errors so refinement, cutoff, and volume limits commute.",
        "At one fixed physical time t0, prove a common lower mass floor over geometric alpha, inclusion degree p, cutoff, and volume from multi-step physical transfer data.",
        "Provide a nonzero recovered OS vector and separately audit any interaction witness.",
        "Discharge continuum Schwinger, OS regularity, clustering, large-field, topology, and RG-basin obligations.",
        "Run an independent audit before raising the candidate claim ceiling.",
    ]
    return {
        "artifact_type": "DomainEvidencePacket",
        "workflow_id": "cohere_fast",
        "domain_id": "ym",
        "run_id": run_id,
        "schema_version": "1.0",
        "claims": claims,
        "provenance": [
            source(
                "skills/programs/yang-mills/ym-build-observable-core/SKILL.md",
                "7a5bab37df46ff5672934156a9a11918930ab71667517d55d4c23fe01e330eac",
            ),
            source(
                "skills/programs/yang-mills/ym-build-representation-calculus/SKILL.md",
                "21c8e01691d47948f2de8f5612d0d5533dd16be8ce5965cec936f660a67da2d6",
            ),
            source(
                "skills/programs/yang-mills/ym-reconstruct-os-gap/SKILL.md",
                "626f78e888a236c5b1846f5bf0d1a1d87ecb8532652b1479c33885bf5dba2e45",
            ),
            source(
                "skills/programs/yang-mills/ym-audit-frontier/SKILL.md",
                "1799aab7bd1c3b99343cec991987523e985ce3095b02e3d595d2da718058b73e",
            ),
        ],
        "integrity_status": "digest_verified",
        "proof_status": "candidate",
        "publication_status": "not_ready",
        "open_obligations": obligations,
        "activation_receipt_id": activation["id"],
        "subworkflow_id": "adaptive-frontier",
        "claim_ceiling": "candidate",
        "refinement_revision": 4,
        "route_disposition": (
            "frontier_specification_accepted_proof_promotion_quarantined"
        ),
        "scope": {
            "gauge_group": "SU(3)",
            "regulator_family": "heat-kernel lattice gauge theory",
            "theory_identity_rule": (
                "alpha may refine the Wilson-net test space but may not change the "
                "action, coupling trajectory, observable normalization, or recovery convention"
            ),
            "nonclaims": [
                "continuum construction",
                "OS/Wightman reconstruction",
                "observable density",
                "nontriviality",
                "positive mass gap",
            ],
        },
        "evidence_locators": [
            {"path": LATEST, "digest": file_digest(LATEST), "role": "latest YM state"},
            {"path": PILOT, "digest": file_digest(PILOT), "role": "blocked endpoint pilot"},
            {"path": DEMOTION, "digest": file_digest(DEMOTION), "role": "pivot control"},
            {"path": LOCKIN, "digest": file_digest(LOCKIN), "role": "release control"},
            {"path": KB, "digest": file_digest(KB), "role": "OS and gap knowledge base"},
            {
                "path": "skills/common/ym_abstraction_calibrations.py",
                "digest": file_digest("skills/common/ym_abstraction_calibrations.py"),
                "role": "sealed restricted-model falsifier runners",
            },
        ],
        "candidate_carrier": {
            "name": "two-axis geometric/algebraic physical-sector spectral carrier",
            "spaces": (
                "V_{alpha,p} is a finite span of centered gauge-invariant Wilson nets; "
                "p is ordered only when actual OS images are included, while alpha "
                "labels geometric resolution and need not be monotone by inclusion"
            ),
            "regulated_images": (
                "J_{n,alpha,p}V_{alpha,p} in the reflection-positive quotient H_{a_n,L_n}^{OS}"
            ),
            "transfer_quantity": (
                "rho_{alpha,p,n}(tau_n)=sup <psi,T_n(tau_n)psi>/||psi||^2 over "
                "nonzero psi in J_{n,alpha,p}V_{alpha,p}, where tau_n=k_n a_{t,n} "
                "converges to fixed physical t0 and the same normalized positive "
                "self-adjoint contraction is used at each n"
            ),
            "physical_mass_quantity": (
                "m_{alpha,p,n}^{phys}(tau_n)=-log(rho_{alpha,p,n}(tau_n))/tau_n"
            ),
            "monotonicity": (
                "if J_{n,alpha,p}V_{alpha,p} is actually nested as p grows in one OS quotient with "
                "the same centering, null quotient, and T_n(tau_n), then rho is "
                "nondecreasing and m is nonincreasing in p; alpha alone carries no inclusion order"
            ),
            "promotion_condition": (
                "dense recovered p-union for the admitted alpha family, commuting limits, same-theory recovery, "
                "vacuum uniqueness or exclusion of zero modes, a nonzero carrier, "
                "and a common positive mass floor over alpha, p, n, and volume"
            ),
        },
        "alpha_parameterization": {
            "status": "candidate_calibration_not_inherited_definition",
            "model": "epsilon_n=a_n/rho_0 and r_{alpha,n}=rho_0*epsilon_n^alpha",
            "consequence": (
                "alpha=1 gives r/a=1, so a one-cell shape repertoire does not grow; "
                "for 0<alpha<1, r/a=(rho_0/a)^(1-alpha) grows along cutoff removal"
            ),
            "control_rule": (
                "vary alpha only on one fixed theory trajectory and predeclare the "
                "observable construction; never infer density from radius scaling alone"
            ),
        },
        "alpha_refinement_thought_experiment": {
            "controlled_variable": "geometric alpha only; regulator, trajectory, scale setting, centering, and observable rule stay fixed",
            "rows": [
                {
                    "alpha": "1",
                    "observable_content": "bounded one-cell pilot; three predeclared centered SU(3) character channels at p=1",
                    "recovery_error": "not_computed",
                    "os_negative_defect": "not_computed",
                    "density_residual": "open",
                    "nonzero_os_norm": "not_computed",
                    "connected_cumulant_marker": "not_computed",
                    "physical_mass_floor": "not_computed",
                },
                {
                    "alpha": "0<alpha<1",
                    "observable_content": "degree-growing loop shapes are permitted, but actual p-nesting and recovery must be certified",
                    "recovery_error": "not_computed",
                    "os_negative_defect": "not_computed",
                    "density_residual": "open",
                    "nonzero_os_norm": "not_computed",
                    "connected_cumulant_marker": "not_computed",
                    "physical_mass_floor": "not_computed",
                },
                {
                    "alpha": "admitted-family limit",
                    "observable_content": "a norm-dense local Wilson-net p-union, if proved",
                    "recovery_error": "requires uniform limit control",
                    "os_negative_defect": "requires a closed-cone limit",
                    "density_residual": "must tend to zero",
                    "nonzero_os_norm": "must survive",
                    "connected_cumulant_marker": "separate interaction obligation",
                    "physical_mass_floor": "must retain one common m>0",
                },
            ],
            "observed_outcome": "missing_carrier_data",
            "gate_result": "quarantine_proof_promotion",
        },
        "conditional_lemma": {
            "title": "Dense-carrier spectral exclusion",
            "statement": (
                "Let H>=0 have vacuum Omega and let D be dense in Omega-perp. "
                "If every vector in D has spectral measure disjoint from [0,m) "
                "for one common m>0, then E_H([0,m)) vanishes on Omega-perp. "
                "This also excludes additional zero-energy states."
            ),
            "public_derivation": [
                "The support condition gives E_H([0,m))psi=0 for psi in D.",
                "A spectral projection is bounded.",
                "Continuity extends the equality from dense D to Omega-perp.",
                "A common quadratic-form bound for T(t0)=exp(-t0 H) on dense linear D also extends by continuity and yields the same exclusion.",
                "A compressed bound at fixed alpha or for one vector is insufficient.",
            ],
            "status": "conditional_candidate_not_applied",
        },
        "alternatives": [
            {
                "route": "repeat finite endpoint source-table search",
                "decision": "deferred",
                "reason": "no evaluator or analytic interval proof is available",
            },
            {
                "route": "auxiliary stochastic-semigroup functional inequality",
                "decision": "rejected",
                "reason": "proxy shift without an intertwining theorem",
            },
            {
                "route": "two-axis alpha/p physical transfer carrier",
                "decision": "selected_candidate",
                "reason": "directly tests density and uniformity on the physical carrier",
            },
        ],
        "falsifiers": [
            {"id": "uniformity_gap", "test": "m_alpha tends to zero"},
            {"id": "proxy_shift", "test": "the theory or evolution changes with alpha"},
            {"id": "missing_carrier", "test": "recovered nets are OS-null or not dense"},
            {"id": "noncommuting_limits", "test": "the relevant limits disagree"},
            {"id": "positivity_loss", "test": "a negative reflection defect survives"},
            {"id": "triviality", "test": "all centered recovered vectors vanish"},
        ],
        "next_bounded_action": (
            "At alpha=1 and p=1, freeze three centered spatial-plaquette SU(3) character "
            "channels (charge-even fundamental, adjoint, charge-even sextet). Produce "
            "their OS Gram and fixed-physical-time transfer matrices, null-quotient "
            "ledger, recovery residuals against fixed-physical Wilson loops, and "
            "Rayleigh bounds. A lower bound on rho can falsify; promotion requires a "
            "rigorous upper bound and eventual p-density."
        ),
        "restricted_model_status": {
            "cases": [
                "finite_transfer_matrix",
                "hidden_gapless_direct_sum",
                "finite_volume_gap_collapse",
                "regulated_4d_lattice",
                "noncommuting_limit_order",
            ],
            "result": "all exact replays passed; none authorizes target promotion",
            "route_effect": (
                "finite visible-sector transfer data are retained as falsifiers and "
                "recovery diagnostics, never as a substitute for density or uniform limits"
            ),
        },
        "fixed_rank_obstruction": {
            "statement": (
                "Let W_n be regulated carrier spaces with dim(W_n)<=M. If their "
                "recovered basis vectors converge in one continuum Hilbert space, "
                "the recovered limit carrier W has dim(W)<=M and is closed. Thus W "
                "is not dense whenever dim(H_physical)>M."
            ),
            "proof_outline": [
                "The limits of at most M recovered basis vectors span W.",
                "A span generated by at most M vectors has dimension at most M.",
                "Every finite-dimensional subspace of a Hilbert space is closed.",
                "A proper closed subspace is not dense.",
                "If recovered vectors do not converge coherently, the same-theory recovery gate fails instead.",
            ],
            "alpha1_application": (
                "M=3 for the charge-even fundamental, adjoint, and charge-even "
                "sextet pilot; density is impossible if the physical sector has "
                "dimension greater than three"
            ),
            "status": "conditional_candidate",
            "route_decision": "force_unbounded_p_growth",
        },
        "density_quantifier_contract": (
            "For every continuum physical vector psi and tolerance epsilon>0, "
            "there must exist an inclusion degree p and n0 such that for all n>=n0 "
            "a same-theory recovered vector from V_{alpha,p,n} approximates psi within epsilon."
        ),
        "ten_cycle_run": {
            "cycle_count": 10,
            "status": "bounded_inference_complete",
            "promotion_authorized": False,
            "consolidated_decision": (
                "retain the two-axis alpha/p carrier only as a conditional route; "
                "force unbounded p-growth, explicit Gram/recovery stability, physical-time "
                "transfer complement control, and uniform limit order before proof promotion"
            ),
        },
    }


def build_event(activation: dict) -> dict:
    event_id = "evt-" + activation["command_digest"].split(":", 1)[1][:24]
    return {
        "schema_version": "2.0.0",
        "event_id": event_id,
        "run_id": activation["run_id"],
        "workflow_id": "cohere_fast",
        "workflow_version": activation["workflow_version"],
        "profile_id": None,
        "domain_id": "ym",
        "subworkflow_id": "adaptive-frontier",
        "parent_run_id": None,
        "parent_event_id": None,
        "execution_kind": "live",
        "claim_level": "C2",
        "target": TARGET,
        "activation_receipt_id": activation["id"],
        "sequence": 1,
        "timestamp_utc": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "phase": "adaptive-frontier",
        "step_id": "adaptive-frontier",
        "skill": "ym-build-observable-core",
        "attempt": 1,
        "branch": "two-axis-physical-sector-spectral-carrier",
        "event_family": "public_inference",
        "causal_parent_event_ids": [],
        "parent_artifact_ids": [],
        "artifact_validation_status": "integrity_valid",
        "claim_epistemic_status": "conjectural",
        "workflow_disposition": "accepted",
        "public_inference": {
            "question": (
                "What distinct YM route remains after endpoint quarantine, "
                "and what would falsify it?"
            ),
            "premises": [
                {
                    "type": "artifact",
                    "statement": (
                        "The endpoint branch lacks same-regulator intervals and a uniform tail."
                    ),
                },
                {
                    "type": "constraint",
                    "statement": (
                        "A Clay-facing route must preserve one theory across all limits."
                    ),
                },
                {
                    "type": "fact",
                    "statement": (
                        "A common spectral exclusion on a dense carrier extends by "
                        "continuity of spectral projections."
                    ),
                },
                {
                    "type": "artifact",
                    "statement": (
                        "Sealed restricted-model replays exhibit hidden gapless sectors, "
                        "finite-volume collapse, and noncommuting limits without target promotion."
                    ),
                },
                {
                    "type": "claim",
                    "statement": (
                        "A coherently recovered fixed-rank carrier has a closed finite-dimensional "
                        "limit span and cannot be dense in a larger physical sector."
                    ),
                },
            ],
            "operator": "two_axis_carrier_abstraction_and_falsifier_projection",
            "warrant": (
                "Geometric resolution alpha and algebraic inclusion p must be separated. "
                "Only actual p-inclusion makes the fixed-time mass floor adversarial; "
                "alpha variation instead tests UV proxy and recovery behavior."
            ),
            "conclusion": (
                "Select the two-axis alpha/p physical transfer carrier as a candidate; "
                "quarantine proof promotion pending uniform mass, recovery, density, "
                "positivity, nontriviality, and limit compatibility. Restricted-model "
                "success authorizes falsifier use only, and density requires unbounded p-growth."
            ),
            "assumptions": [
                "One SU(3) heat-kernel trajectory is used for every alpha.",
                "Only p is ordered by actual inclusion after identical centering and OS quotienting; alpha has no assumed inclusion order.",
                "One normalized positive self-adjoint T_n(tau_n) represents physical Euclidean-time evolution, with tau_n=k_n a_{t,n} approaching fixed t0 and rounding error recorded.",
            ],
            "alternatives": [
                {
                    "candidate": "Another endpoint iteration",
                    "disposition": "deferred",
                    "reason": "No new evaluator is available.",
                },
                {
                    "candidate": "Langevin-semigroup Poincare route",
                    "disposition": "rejected",
                    "reason": "It changes the dynamical carrier without an intertwiner.",
                },
                {
                    "candidate": "Two-axis alpha/p physical transfer carrier",
                    "disposition": "accepted",
                    "reason": "It exposes density and uniformity failures directly.",
                },
            ],
            "falsifiers": [
                "The mass floor collapses as the inclusion degree p grows.",
                "Recovered Wilson nets are not dense or become OS-null.",
                "The carrier rank stays uniformly bounded while the physical sector is larger.",
                "The cutoff, volume, alpha, and reconstruction limits disagree.",
                "The theory or evolution operator changes across alpha.",
            ],
            "uncertainty": (
                "No alpha-indexed fixed-time matrices or uniform bounds are available; "
                "this is a candidate route, not evidence for a mass gap."
            ),
            "scope": {
                "regime": "regulated-to-continuum candidate bridge",
                "model": "four-dimensional SU(3) heat-kernel lattice Yang-Mills",
                "before": "artifact-blocked endpoint and one-observable decay routes",
                "after": "geometric alpha separated from inclusion degree p, with explicit falsifiers",
            },
            "trace_completeness": "complete",
        },
        "evidence": [
            {
                "relation": "constrains",
                "path": LATEST,
                "digest": file_digest(LATEST),
                "receipt_id": None,
                "artifact_type": "YMDiscoveryState",
                "external": False,
            },
            {
                "relation": "constrains",
                "path": PILOT,
                "digest": file_digest(PILOT),
                "receipt_id": None,
                "artifact_type": "EndpointSourceTablePilot",
                "external": False,
            },
            {
                "relation": "supports",
                "path": KB,
                "digest": file_digest(KB),
                "receipt_id": None,
                "artifact_type": "KnowledgeBase",
                "external": False,
            },
            {
                "relation": "supports",
                "path": "skills/common/ym_abstraction_calibrations.py",
                "digest": file_digest("skills/common/ym_abstraction_calibrations.py"),
                "receipt_id": None,
                "artifact_type": "YMCalibrationRunnerRegistry",
                "external": False,
            },
        ],
        "authority": {
            "exercised": [
                "bounded-domain-frontier-selection",
                "candidate-abstraction",
                "falsifier-definition",
            ],
            "absent": [
                "proof-acceptance",
                "independent-audit",
                "continuum-promotion",
                "publication-release",
            ],
            "prohibitions_checked": [
                "no cross-workflow write",
                "no finite-to-continuum promotion",
                "no stochastic-to-Hamiltonian proxy substitution",
            ],
        },
        "gate": {
            "route_artifact": "accepted",
            "proof_promotion": "quarantined",
            "reason": "All alpha-indexed measurements and compatibility proofs are open.",
        },
        "presentation_hints": {
            "expert_focus": [
                "carrier",
                "monotonicity",
                "limit order",
                "falsifiers",
                "claim ceiling",
            ]
        },
        "idempotency_key": activation["command_digest"],
    }


def build_trace(activation: dict, events: list[dict]) -> dict:
    return {
        "schema_version": "2.0.0",
        "run_id": activation["run_id"],
        "workflow_id": "cohere_fast",
        "workflow_version": activation["workflow_version"],
        "profile_id": None,
        "domain_id": "ym",
        "subworkflow_id": "adaptive-frontier",
        "parent_run_id": None,
        "execution_kind": "live",
        "target": TARGET,
        "trigger_facts": {
            "explicit_invocation": "cohere-fast ym adaptive-frontier",
            "prior_route": "finite endpoint source-table branch quarantined",
        },
        "approved_budget": {"bounded_steps": 1, "claim_ceiling": "candidate"},
        "activation_receipt_id": activation["id"],
        "status": "completed",
        "events": events,
    }


def summary(run_id: str) -> str:
    return (
        r"""# Cohere-fast YM adaptive frontier: two-axis spectral carrier

Run: `__RUN_ID__`

Disposition: frontier specification accepted; proof promotion quarantined
Claim ceiling: candidate

## Outcome

Separate geometric resolution \(\alpha\) from algebraic inclusion degree \(p\).
For each admitted alpha, order centered gauge-invariant Wilson-net spaces by
actual inclusion after recovery and OS quotienting:

\[
V_{\alpha,1} \subset V_{\alpha,2} \subset \cdots.
\]

on one fixed SU(3) heat-kernel cutoff/volume trajectory. Choose integer
\(k_n\) so the actual separation \(\tau_n=k_n a_{t,n}\) approaches one fixed
physical time \(t_0>0\). For Euclidean-time transfer on the OS quotient, define

\[
\rho_{\alpha,p,n}(\tau_n)=\sup_{0\ne\psi\in J_{n,\alpha,p}V_{\alpha,p}}
\frac{\langle\psi,T_n(\tau_n)\psi\rangle}{\|\psi\|^2},\qquad
m^{\rm phys}_{\alpha,p,n}(\tau_n)=-\frac{1}{\tau_n}
\log\rho_{\alpha,p,n}(\tau_n).
\]

If the actual OS quotient images are nested with identical centering and null
quotient, and use the same positive self-adjoint \(T_n(\tau_n)\), then rho is
nondecreasing and the mass estimate is nonincreasing in p. No monotonicity is
inferred from numerical alpha. The meaningful candidate gate is

\[
\inf_{\alpha,p}\liminf_n m^{\rm phys}_{\alpha,p,n}(\tau_n)>0,
\]

together with same-theory recovery, density in the vacuum-orthogonal OS
Hilbert space, reflection-form convergence, a nonzero carrier, and commuting
cutoff, volume, refinement, and reconstruction limits.

## Conditional bridge

If a dense set of vacuum-orthogonal OS vectors has spectral support outside
\([0,m)\) for one common \(m>0\), boundedness of the spectral projection
\(E_H([0,m))\) extends its vanishing to the closure and excludes additional
zero modes. The run does not prove
the hypotheses.

## Alpha=1 falsifier calibration

As a candidate calibration, set \(\epsilon_n=a_n/\rho_0\) and
\(r_{\alpha,n}=\rho_0\epsilon_n^\alpha\). Then alpha=1 has \(r/a=1\):
its shape repertoire stays one-cell and cannot establish density merely by
cutoff refinement. It should test UV collapse and recovery against
fixed-physical Wilson loops. Values \(0<\alpha<1\) permit a growing number of
lattice cells but still require a genuine p-density proof.

## Critical refinements

- Strict OS positivity margins are unnecessary; nonnegativity and convergence
  of reflection forms are the relevant closed-cone properties.
- Nonzero OS norm is the minimal anti-vacuity witness. A connected higher
  cumulant is a separate interaction/non-Gaussian witness.
- A functional inequality for auxiliary Langevin dynamics is rejected unless
  it is rigorously intertwined with physical Euclidean-time transfer.
- Changing the regulator, normalization, recovery map, or evolution while
  refining alpha is a proxy shift.

## Current gate and next action

No alpha-indexed recovery ledger, OS/transfer matrices, density residuals,
nontriviality witness, or common physical mass floor is present. Freeze
alpha=1 and p=1 with three centered spatial-plaquette SU(3) character channels:
charge-even fundamental, adjoint, and charge-even sextet. Produce their OS Gram
and fixed-physical-time transfer matrices, null-quotient and time-rounding
ledgers, and recovery residuals against fixed-physical Wilson loops. A
trial-vector lower bound on rho can falsify a proposed gap; promotion requires
a rigorous upper bound and, eventually, p-density.
"""
    ).replace("__RUN_ID__", run_id)


def alpha1_pilot_spec() -> str:
    return r"""# Alpha=1, p=1 physical-sector carrier pilot

Disposition: bounded falsifier/recovery experiment

Claim ceiling: candidate
Current executability: needs external mathematical and lattice data

## Fixed theory and basis

Use one finite-volume SU(3) heat-kernel lattice measure, one declared coupling
and scale-setting trajectory, one link-reflection plane, one vacuum-subtraction
rule, and no post-hoc observable replacement.

On the first positive-time slice, let (U_p) be a spatial plaquette holonomy.
Use three real class functions:

\[
\phi_{3+}(U)=\frac{1}{3}\operatorname{Re}\operatorname{tr}U,
\quad
\phi_8(U)=\frac{|\operatorname{tr}U|^2-1}{8},
\]

\[
\phi_{6+}(U)=\frac{1}{6}\operatorname{Re}
\left(\frac{(\operatorname{tr}U)^2+\operatorname{tr}(U^2)}{2}\right).
\]

For each channel (R\in\{3+,8,6+\}), form a centered zero-momentum sum

\[
F_R=|\mathcal P^+|^{-1/2}\sum_{p\in\mathcal P^+}
(\phi_R(U_p)-\langle\phi_R(U_p)\rangle).
\]

This is only a three-dimensional (A_1^{++}) visible sector. It is not an
observable-density claim.

## Reflection and fixed-time transfer matrices

For actual physical separation \(\tau_n=k_n a_{t,n}\to t_0>0\), compute

\[
G_{RS}=\langle\Theta F_R F_S\rangle,
\qquad
K_{RS}(\tau_n)=\langle\Theta F_R\,\tau_{k_n}F_S\rangle.
\]

Certify (G\succeq0), quotient only directions whose Gram interval contains
zero under a predeclared rule, retain raw eigenvalue and whitening ledgers, and
solve

\[
K(\tau_n)c=\lambda Gc.
\]

Within this finite carrier, \(\lambda_{\max}\) is the Rayleigh supremum and
\(-\tau_n^{-1}\log\lambda_{\max}\) is a visible-sector mass estimate. It does
not exclude lower-energy states outside the carrier. A trial subspace gives a
lower bound on the full supremum and can falsify a claimed gap; proof requires
a uniform upper bound over an eventually dense inclusion-ordered union.

## Fixed-physical recovery test

Predeclare centered Wilson-loop targets (Q_1,Q_2) with physical side lengths
\(\rho_0\) and (2\rho_0\). Compute

\[
H_{qq'}=\langle\Theta Q_qQ_{q'}\rangle,
\qquad B_{Rq}=\langle\Theta F_RQ_q\rangle,
\]

and the OS projection residual

\[
E_{\rm rec}=H-B^\dagger G^+B\succeq0.
\]

After quotienting null target directions, report the relative residual

\[
\varepsilon_{\rm rec}=\|H^{-1/2}E_{\rm rec}H^{-1/2}\|_2^{1/2}.
\]

At alpha=1 the candidate scaling (r_{\alpha,n}=\rho_0(a_n/\rho_0)^\alpha)
gives (r/a=1). A recovery residual bounded away from zero therefore exposes
UV-proxy collapse and rejects this carrier without rejecting the broader YM
program.

## Decisive falsifiers

- A certified negative eigenvalue of (G), or loss of finite reflection positivity.
- Gram-rank collapse or divergent whitening that hides vanishing raw overlap.
- Fixed-physical recovery residuals that remain nonzero or worsen with cutoff removal.
- Visible energies scaling as (a^{-1}), indicating a cutoff excitation.
- Incompatible cutoff/volume limits or physical-time calibration.
- Mixing matrices from different actions, scale settings, centering rules, or observables.
- Any claim that the three-dimensional visible sector is already Hilbert-dense.

## Missing inputs

The repository has no tuned heat-kernel trajectory, lattice configurations or
exact four-dimensional contraction engine, interval-valued (G,K,B,H\) tables,
scale-setting result, continuum recovery maps, density proof, uniform OS
passage, or common positive physical mass bound. The pilot is therefore a
validator-facing computation contract, not an executed physics result.
"""


def build_restricted_calibration() -> tuple[dict, str]:
    case_ids = [
        "finite_transfer_matrix",
        "hidden_gapless_direct_sum",
        "finite_volume_gap_collapse",
        "regulated_4d_lattice",
        "noncommuting_limit_order",
    ]
    rows = [run_ym_calibration(case_id) for case_id in case_ids]
    validations = [validate_ym_calibration(row) for row in rows]
    artifact = {
        "schema_version": "1.0",
        "artifact_type": "YMRestrictedCarrierCalibration",
        "workflow_id": "cohere_fast",
        "domain_id": "ym",
        "case_count": len(rows),
        "cases": rows,
        "validations": validations,
        "promotion_authorized": False,
        "inference": {
            "finite_transfer_matrix": (
                "A finite positive transfer gap is internally computable but carries "
                "no continuum authority."
            ),
            "hidden_gapless_direct_sum": (
                "A positive visible-sector gap can coexist with a hidden zero-energy "
                "sector, so the finite alpha=1 carrier cannot certify the full gap."
            ),
            "finite_volume_gap_collapse": (
                "Positive finite-volume gaps can decrease to zero; volume-uniformity is required."
            ),
            "regulated_4d_lattice": (
                "A well-formed cutoff/volume fixture does not prove a continuum limit or uniform gap."
            ),
            "noncommuting_limit_order": (
                "Cutoff and volume limits can disagree, so their interchange needs a theorem."
            ),
        },
        "disposition": "supports_falsifier_contract_only",
    }
    markdown = """# Restricted-model calibration of the alpha=1 carrier

All five sealed local replays passed, and every replay retained
`promotion_authorized: false`.

- A finite transfer matrix has a computable positive gap but no continuum authority.
- A visible gapped block can coexist with a hidden zero-energy sector.
- Positive finite-volume gaps can collapse as volume grows.
- A regulated four-dimensional lattice fixture proves neither continuum existence nor a uniform gap.
- Cutoff and volume limits can fail to commute.

The alpha=1 pilot is therefore useful for falsification, recovery diagnostics,
and visibility analysis. Even exact finite matrices cannot promote the YM gap
without density, same-theory continuum recovery, and uniform limit control.
"""
    return artifact, markdown


def fixed_rank_obstruction() -> str:
    return r"""# Fixed-rank recovery obstruction

Status: conditional candidate theorem
Consequence: the alpha=1, p=1 pilot cannot be an observable-density proof

## Proposition

Let \(\mathcal H\) be the candidate continuum OS Hilbert space and let
\(W_n\) be regulated carrier spaces with \(\dim W_n\le M\). Suppose a fixed
choice of at most \(M\) carrier generators is transported by same-theory
recovery maps into \(\mathcal H\), and every recovered generator converges in
the Hilbert norm. Then the limiting carrier

\[
W=\operatorname{span}\{\psi_1,\ldots,\psi_M\}
\]

has dimension at most \(M\), is closed, and cannot be dense in any physical
sector of dimension greater than \(M\).

## Proof

The recovered limits provide at most \(M\) vectors, so their span has dimension
at most \(M\). Every finite-dimensional subspace of a Hilbert space is closed.
If the physical sector has dimension greater than \(M\), this closed subspace is
proper and therefore not dense.

The conclusion is unchanged if one formulates recovery by strongly convergent
orthogonal projections of rank at most \(M\): a strong limit cannot acquire
rank greater than the common finite bound. If no coherent limit exists, the
same-theory recovery or limit-commutation gate fails instead.

## Application to alpha=1, p=1

The pilot carrier has exactly three declared channels: charge-even fundamental,
adjoint, and charge-even sextet. Hence coherent recovery gives a continuum
carrier of dimension at most three. Conditional on the vacuum-orthogonal YM
sector having dimension greater than three, this carrier cannot be dense.

This is a structural obstruction, not a Yang--Mills existence or mass-gap
theorem. It fixes the role of the pilot: it may test reflection positivity,
UV collapse, recovery, and visible transfer behavior, but never global density.

## Required quantifier order for the viable route

A density claim needs an unbounded inclusion degree. Schematically,

\[
\forall\psi\in\mathcal H_{\perp\Omega}\;\forall\varepsilon>0\;
\exists p\;\exists n_0\;\forall n\ge n_0\;\exists v_{p,n}\in V_{\alpha,p,n}:
\|J_{n,\alpha,p}v_{p,n}-\psi\|<\varepsilon.
\]

The spectral estimate must then be uniform over this growing family, while
Gram conditioning, recovery error, physical-time calibration, cutoff, and
volume errors remain controlled. A convenient finite carrier with fixed p
cannot replace this diagonal-limit obligation.

## Next bounded derivation target

Specify a predeclared growth law \(p=p(n)\to\infty\) and an error decomposition

\[
\delta_{\rm total}=\delta_{\rm approximation}(p)
+\delta_{\rm recovery}(p,n)+\delta_{\rm Gram}(p,n)
+\delta_{\rm time}(n)+\delta_{\rm volume}(n),
\]

then determine which rates are sufficient for density and for a uniform
fixed-physical-time transfer upper bound. No such rates are currently supplied.
"""


def build_ten_cycles() -> list[dict]:
    return [
        {
            "cycle": 1,
            "title": "Fixed-rank recovery obstruction",
            "question": "Can the three-channel alpha=1,p=1 carrier ever establish observable density?",
            "result": (
                "No, conditionally on coherent Hilbert-norm recovery and a physical sector "
                "of dimension greater than three. Its limit span is closed and has rank at most three."
            ),
            "warrant": "A span of at most three recovered limits is finite-dimensional and closed.",
            "falsifiers": [
                "The alleged physical sector has dimension at most three.",
                "The recovery maps do not converge coherently, which instead fails the recovery gate.",
            ],
            "next_obligation": "Let inclusion degree p grow without bound.",
            "status": "conditional_obstruction",
        },
        {
            "cycle": 2,
            "title": "Diagonal carrier-growth lemma",
            "question": "Can fixed-p recovery estimates be assembled into one p(n) tending to infinity?",
            "result": (
                "Yes conditionally. If approximation error A(p) tends to zero and recovery "
                "error R(p,n) tends to zero for each fixed p, a nondecreasing diagonal "
                "schedule p(n) can be chosen so A(p(n))+R(p(n),n) tends to zero."
            ),
            "warrant": (
                "Choose N_p so R(p,n)<=1/p for n>=N_p, make N_p increasing, and set "
                "p(n) to the largest p with N_p<=n."
            ),
            "falsifiers": [
                "A(p) does not tend to zero.",
                "For some fixed p, recovery error fails to vanish with cutoff removal.",
            ],
            "next_obligation": "Control Gram conditioning and all other errors on the same diagonal schedule.",
            "status": "conditional_lemma",
        },
        {
            "cycle": 3,
            "title": "Gram-rank stability gate",
            "question": "When does increasing p preserve the intended OS quotient rather than amplify null directions?",
            "result": (
                "For fixed p, rank is stable if the exact limiting Gram matrix has smallest "
                "retained eigenvalue gamma_p>0 and the matrix error is eventually below gamma_p/2. "
                "Along p(n), the ratio ||Delta G||/gamma_p must still tend to zero."
            ),
            "warrant": "Weyl eigenvalue bounds prevent a perturbation smaller than gamma_p/2 from crossing zero.",
            "falsifiers": [
                "gamma_p collapses faster than Gram errors.",
                "Whitening factors diverge and conceal vanishing raw OS norm.",
            ],
            "next_obligation": "Record raw eigenvalue intervals and couple p-growth to a conditioning budget.",
            "status": "candidate_gate",
        },
        {
            "cycle": 4,
            "title": "Recovery residual to density",
            "question": "What does the Schur recovery residual actually prove?",
            "result": (
                "Vanishing normalized residuals for every member of a separately dense target "
                "dictionary imply density of the carrier union in the dictionary closure. "
                "Residuals for two Wilson loops alone do not imply Hilbert-space density."
            ),
            "warrant": (
                "The Schur complement is the squared OS distance to the carrier projection; "
                "density follows only after quantifying over a dense target family."
            ),
            "falsifiers": [
                "The target dictionary is not independently dense.",
                "Residual convergence is only pointwise with no diagonal schedule.",
            ],
            "next_obligation": "Predeclare a countable Wilson-net target dictionary and its density theorem.",
            "status": "conditional_bridge",
        },
        {
            "cycle": 5,
            "title": "Visible Ritz bound polarity",
            "question": "Can finite generalized eigenvalues certify the physical transfer gap?",
            "result": (
                "Not alone. A trial carrier gives a lower bound on the full transfer Rayleigh "
                "supremum, so it can falsify a proposed upper bound. Gap promotion needs an upper "
                "bound including the carrier complement and off-diagonal leakage."
            ),
            "warrant": "A supremum over a subspace cannot exceed the supremum over the full physical sector.",
            "falsifiers": [
                "A computed trial value exceeds exp(-m*tau), refuting the proposed mass floor m.",
                "Complement or leakage estimates remain uncontrolled.",
            ],
            "next_obligation": "Bound the complement transfer norm and carrier-complement coupling.",
            "status": "polarity_correction",
        },
        {
            "cycle": 6,
            "title": "Transfer complement obstruction",
            "question": "What finite-data inequality would suffice for a full transfer upper bound?",
            "result": (
                "With physical-sector decomposition W plus W-perp, bounds q_W, q_C, and b on "
                "the two diagonal transfer blocks and off-diagonal block imply an operator upper "
                "bound given by the largest eigenvalue of [[q_W,b],[b,q_C]]."
            ),
            "warrant": (
                "The quadratic form is dominated by the corresponding two-by-two scalar majorant; "
                "its largest eigenvalue bounds the full contraction."
            ),
            "falsifiers": [
                "No q_C<1 is available on the complement.",
                "Leakage b does not vanish or remain below the reserved margin.",
            ],
            "next_obligation": "Produce a noncircular complement estimate; density alone at finite p is insufficient.",
            "status": "conditional_operator_bound",
        },
        {
            "cycle": 7,
            "title": "OS closed-cone versus semigroup convergence",
            "question": "Does convergence of reflection-positive Gram matrices construct the continuum Hamiltonian?",
            "result": (
                "No. Entrywise convergence of every recovered finite reflection matrix preserves "
                "OS nonnegativity, but Hamiltonian transfer also requires a consistent strongly "
                "continuous time-translation semigroup and convergence across physical times."
            ),
            "warrant": "Closedness of the PSD cone preserves positivity but supplies no semigroup law or generator convergence.",
            "falsifiers": [
                "Positive-time matrices are mutually inconsistent.",
                "The limiting translations lack strong continuity or the semigroup composition law.",
            ],
            "next_obligation": "Add multi-time correlation consistency and semigroup convergence to the recovery packet.",
            "status": "boundary_separation",
        },
        {
            "cycle": 8,
            "title": "Nontriviality witness separation",
            "question": "Which witnesses prevent a vacuous or Gaussian limit?",
            "result": (
                "A nonzero recovered OS norm prevents the carrier from vanishing. A surviving "
                "connected higher cumulant is a stronger non-Gaussian witness. Neither proves "
                "density, OS reconstruction, or a positive gap."
            ),
            "warrant": "These witnesses answer different logical questions and cannot substitute for one another.",
            "falsifiers": [
                "All centered recovered norms vanish.",
                "The connected witness survives only after a proxy normalization or theory change.",
            ],
            "next_obligation": "Track norm survival and interaction witnesses as separate fields through the same trajectory.",
            "status": "obligation_factorization",
        },
        {
            "cycle": 9,
            "title": "Geometric alpha versus algebraic p",
            "question": "Which refinement variable can plausibly support density?",
            "result": (
                "At alpha=1 in the candidate radius model, the number of lattice cells per shape "
                "stays bounded, making the pilot a UV-proxy falsifier. Values 0<alpha<1 permit "
                "growing shapes, but only explicit p-inclusion supplies the monotone density axis."
            ),
            "warrant": "Geometric scale and algebraic closure are independent controls and must not be conflated.",
            "falsifiers": [
                "Changing alpha also changes the action, normalization, or recovery convention.",
                "Growing geometric radius fails to enlarge the OS carrier after quotienting.",
            ],
            "next_obligation": "Predeclare an alpha family and a separate degree-growth law p(n).",
            "status": "route_refinement",
        },
        {
            "cycle": 10,
            "title": "Consolidated YM route decision",
            "question": "After ten bounded cycles, what remains viable and what is blocked?",
            "result": (
                "Retain the two-axis alpha/p spectral-carrier route as a conditional research "
                "programme. The fixed-rank pilot is demoted to falsification. Proof promotion "
                "is blocked until actual same-theory SU(3) matrices, unbounded p-density, Gram "
                "stability, complement transfer control, OS semigroup convergence, and uniform "
                "cutoff/volume limits are supplied."
            ),
            "warrant": "Every finite or conceptual shortcut encountered has a named countermodel or missing transfer gate.",
            "falsifiers": [
                "The required data cannot be produced without changing theory.",
                "The mass floor collapses under p, volume, or cutoff refinement.",
                "The recovered carrier is null, nondense, or limit-order dependent.",
            ],
            "next_obligation": (
                "Produce the first actual alpha=1 Gram/recovery table and, independently, a "
                "quantitative p(n) error schedule; otherwise keep the route quarantined."
            ),
            "status": "conditional_route_retained_proof_blocked",
        },
    ]


def render_ten_cycles(cycles: list[dict]) -> str:
    lines = [
        "# Ten cohere-fast YM inference cycles",
        "",
        "Claim ceiling: candidate",
        "",
        "Final disposition: conditional route retained; proof promotion blocked",
        "",
    ]
    for cycle in cycles:
        lines.extend(
            [
                f"## Cycle {cycle['cycle']:02d}: {cycle['title']}",
                "",
                f"**Question.** {cycle['question']}",
                "",
                f"**Result.** {cycle['result']}",
                "",
                f"**Warrant.** {cycle['warrant']}",
                "",
                "**Falsifiers.**",
                "",
                *[f"- {item}" for item in cycle["falsifiers"]],
                "",
                f"**Next obligation.** {cycle['next_obligation']}",
                "",
                f"Status: `{cycle['status']}`",
                "",
            ]
        )
    return "\n".join(lines)


def build_cycle_events(activation: dict, cycles: list[dict]) -> list[dict]:
    base = build_event(activation)
    events = []
    digest = activation["command_digest"].split(":", 1)[1]
    for cycle in cycles:
        event = copy.deepcopy(base)
        number = cycle["cycle"]
        event["event_id"] = f"evt-{digest[:20]}-{number:02d}"
        event["sequence"] = number
        event["branch"] = f"ym-cohere-fast-cycle-{number:02d}"
        event["public_inference"]["question"] = cycle["question"]
        event["public_inference"]["operator"] = "bounded_ym_inference_cycle"
        event["public_inference"]["warrant"] = cycle["warrant"]
        event["public_inference"]["conclusion"] = cycle["result"]
        event["public_inference"]["falsifiers"] = list(cycle["falsifiers"])
        event["public_inference"]["uncertainty"] = (
            f"Cycle status is {cycle['status']}; no cycle raises the candidate claim ceiling."
        )
        event["obligation"] = {
            "requirement": cycle["next_obligation"],
            "status": "open" if number < 10 else "blocked_external_or_proof_input",
        }
        event["gate"] = {
            "cycle": number,
            "cycle_status": cycle["status"],
            "proof_promotion": "blocked",
        }
        events.append(event)
    return events


def validate(request: dict, packet: dict, events: list[dict], trace: dict) -> None:
    validate_instance(request, "cohere_fast_artifacts.schema.json")
    validate_instance(packet, "cohere_fast_artifacts.schema.json")
    for event in events:
        validate_instance(event, "public_reasoning_event.schema.json")
    validate_instance(trace, "public_reasoning_trace.schema.json")


def main() -> int:
    os.environ.setdefault("ABDUCER_ENABLE_COHERE_FAST", "1")
    activation = parse_invocation(
        "cohere-fast ym adaptive-frontier", target=TARGET
    )
    request = {
        "artifact_type": "DomainRunRequest",
        "workflow_id": "cohere_fast",
        "domain_id": "ym",
        "run_id": activation["run_id"],
        "schema_version": "1.0",
        "target": TARGET,
        "activation_receipt_digest": canonical_digest(activation),
    }
    packet = build_packet(activation)
    cycles = build_ten_cycles()
    events = build_cycle_events(activation, cycles)
    trace = build_trace(activation, events)
    calibration, calibration_markdown = build_restricted_calibration()
    validate(request, packet, events, trace)

    def execute(child: dict, input_packet: dict) -> dict:
        if child["id"] != "adaptive-frontier":
            raise ValueError("this bounded run accepts only adaptive-frontier")
        if input_packet["run_id"] != activation["run_id"]:
            raise ValueError("run binding mismatch")
        cycle_artifacts = {
            f"adaptive-frontier/cycles/cycle-{cycle['cycle']:02d}.json": json.dumps(
                cycle, indent=2, sort_keys=True
            )
            + "\n"
            for cycle in cycles
        }
        return {
            "state": "accepted",
            "packet": packet,
            "artifacts": {
                "activation-receipt.json": json.dumps(
                    activation, indent=2, sort_keys=True
                )
                + "\n",
                "request.json": json.dumps(request, indent=2, sort_keys=True) + "\n",
                "adaptive-frontier/domain-evidence-packet.json": json.dumps(
                    packet, indent=2, sort_keys=True
                )
                + "\n",
                "adaptive-frontier/public-reasoning-event.json": json.dumps(
                    events[0], indent=2, sort_keys=True
                )
                + "\n",
                "adaptive-frontier/public-reasoning-trace.json": json.dumps(
                    trace, indent=2, sort_keys=True
                )
                + "\n",
                "adaptive-frontier/spectral-carrier-refinement.md": summary(
                    activation["run_id"]
                ),
                "adaptive-frontier/alpha1-pilot-spec.md": alpha1_pilot_spec(),
                "adaptive-frontier/restricted-model-calibration.json": json.dumps(
                    calibration, indent=2, sort_keys=True
                )
                + "\n",
                "adaptive-frontier/restricted-model-calibration.md": calibration_markdown,
                "adaptive-frontier/fixed-rank-obstruction.md": fixed_rank_obstruction(),
                "adaptive-frontier/ten-cycle-series.json": json.dumps(
                    {"schema_version": "1.0", "cycles": cycles},
                    indent=2,
                    sort_keys=True,
                )
                + "\n",
                "adaptive-frontier/ten-cycle-series.md": render_ten_cycles(cycles),
                **cycle_artifacts,
            },
        }

    result = CohereFastRunner(ROOT / "artifacts").run(
        activation, request, execute
    )
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
