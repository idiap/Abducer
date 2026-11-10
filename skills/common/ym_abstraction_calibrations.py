# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
"""Sealed local Yang--Mills calibration runners for abstraction bridges.

Each calibration is a finite symbolic, countermodel, or theorem-boundary check.
The runners localize false-positive boundaries; they do not establish continuum
Yang--Mills or physics value.  Simulation is accepted only with an exact
theory-commission receipt, and none of the default nine cases needs one.
"""

from __future__ import annotations

import copy
import inspect
import math
from typing import Any, Callable, Mapping

from agentic.discovery.contracts import canonical_digest, stable_identifier
from skills.common.formal_dependency_authority import (
    build_formal_dependency_authority,
    validate_formal_dependency_authority,
)


class YMCalibrationError(ValueError):
    """Raised when a calibration is asserted rather than replayed."""


def _finite_transfer_matrix(payload: Mapping[str, Any]) -> dict[str, Any]:
    eigenvalues = [float(value) for value in payload["eigenvalues"]]
    gap = math.log(eigenvalues[0] / eigenvalues[1])
    return {"computed_gap": round(gap, 12), "finite_dimensional": True, "continuum_authorized": False}


def _massive_gaussian(payload: Mapping[str, Any]) -> dict[str, Any]:
    mass = float(payload["mass"])
    return {"zero_momentum_energy": mass, "positive_gap": mass > 0, "interaction_authorized": False}


def _massless_gaussian(payload: Mapping[str, Any]) -> dict[str, Any]:
    mass = float(payload["mass"])
    return {"zero_momentum_energy": mass, "gapless": mass == 0, "mass_gap_authorized": False}


def _finite_volume_collapse(payload: Mapping[str, Any]) -> dict[str, Any]:
    volumes = [int(value) for value in payload["volumes"]]
    gaps = [round(1.0 / value, 12) for value in volumes]
    return {"volumes": volumes, "gaps": gaps, "strictly_decreasing": gaps == sorted(gaps, reverse=True), "uniform_gap_supported": False}


def _hidden_gapless_sector(payload: Mapping[str, Any]) -> dict[str, Any]:
    visible = [float(value) for value in payload["visible_energies"]]
    hidden = [float(value) for value in payload["hidden_energies"]]
    return {"visible_gap": min(visible), "full_gap": min(hidden + visible), "observable_core_misses_zero_sector": min(hidden) == 0, "full_gap_authorized": False}


def _spatial_only_decay(payload: Mapping[str, Any]) -> dict[str, Any]:
    spatial = [float(value) for value in payload["spatial_correlations"]]
    temporal = [float(value) for value in payload["temporal_correlations"]]
    if len(spatial) < 3 or len(spatial) != len(temporal) or any(value <= 0 for value in spatial + temporal):
        raise YMCalibrationError("spatial/temporal correlation tables must be positive and equally sampled")
    spatial_rates = [round(-math.log(right / left), 12) for left, right in zip(spatial, spatial[1:])]
    temporal_rates = [round(-math.log(right / left), 12) for left, right in zip(temporal, temporal[1:])]
    return {
        "spatial_effective_rates": spatial_rates,
        "temporal_effective_rates": temporal_rates,
        "spatial_decay_positive": all(value > 0 for value in spatial_rates),
        "temporal_gap_supported": all(value > 0 for value in temporal_rates),
        "hamiltonian_gap_inferred": False,
    }


def _topological_boundary(payload: Mapping[str, Any]) -> dict[str, Any]:
    modes = int(payload["declared_local_propagating_modes"])
    states = int(payload["declared_finite_topological_states"])
    return {
        "fixture_consistent": modes == 0 and states > 1,
        "declared_local_propagating_modes": modes,
        "declared_finite_topological_states": states,
        "ym_transfer_authorized": False,
    }


def _regulated_lattice_boundary(payload: Mapping[str, Any]) -> dict[str, Any]:
    cutoff = float(payload["declared_cutoff"])
    volume = int(payload["declared_volume"])
    return {
        "fixture_well_formed": cutoff > 0 and volume > 0,
        "declared_cutoff": cutoff,
        "declared_volume": volume,
        "continuum_limit_proved": False,
        "uniform_gap_proved": False,
    }


def _noncommuting_limits(payload: Mapping[str, Any]) -> dict[str, Any]:
    # f(a,V)=a/(a+1/V): a->0 first gives 0; V->infinity first gives 1.
    if payload != {"numerator": "a", "denominator": "a + 1/V", "a_domain": "a>0", "volume_domain": "V>0"}:
        raise YMCalibrationError("noncommuting-limit runner accepts only its exact sealed rational family")
    finite_samples = [
        {"a": a, "volume": volume, "value": a / (a + 1.0 / volume)}
        for a, volume in ((0.5, 2), (0.25, 4), (0.125, 8))
    ]
    return {
        "expression": "a/(a+1/V)",
        "finite_samples": finite_samples,
        "cutoff_then_volume": 0.0,
        "volume_then_cutoff": 1.0,
        "limits_commute": False,
        "interchange_authorized": False,
    }


CALIBRATION_REGISTRY: dict[str, dict[str, Any]] = {
    "finite_transfer_matrix": {"runner_id": "ym.finite-transfer-matrix.v1", "kind": "symbolic", "runner": _finite_transfer_matrix, "input": {"eigenvalues": [1.0, 0.5]}},
    "massive_gaussian": {"runner_id": "ym.massive-gaussian.v1", "kind": "symbolic", "runner": _massive_gaussian, "input": {"mass": 1.0}},
    "massless_gaussian": {"runner_id": "ym.massless-gaussian.v1", "kind": "countermodel", "runner": _massless_gaussian, "input": {"mass": 0.0}},
    "finite_volume_gap_collapse": {"runner_id": "ym.finite-volume-collapse.v1", "kind": "countermodel", "runner": _finite_volume_collapse, "input": {"volumes": [2, 4, 8, 16]}},
    "hidden_gapless_direct_sum": {"runner_id": "ym.hidden-gapless-sector.v1", "kind": "countermodel", "runner": _hidden_gapless_sector, "input": {"visible_energies": [1.0, 2.0], "hidden_energies": [0.0, 0.5]}},
    "spatial_only_decay": {"runner_id": "ym.spatial-only-decay.v1", "kind": "countermodel", "runner": _spatial_only_decay, "input": {"spatial_correlations": [1.0, 0.36787944117144233, 0.1353352832366127], "temporal_correlations": [1.0, 1.0, 1.0]}},
    "topological_theory": {"runner_id": "ym.topological-boundary.v1", "kind": "boundary_fixture", "runner": _topological_boundary, "input": {"declared_local_propagating_modes": 0, "declared_finite_topological_states": 2}},
    "regulated_4d_lattice": {"runner_id": "ym.regulated-lattice-boundary.v1", "kind": "boundary_fixture", "runner": _regulated_lattice_boundary, "input": {"declared_cutoff": 0.25, "declared_volume": 16}},
    "noncommuting_limit_order": {"runner_id": "ym.noncommuting-limits.v1", "kind": "symbolic", "runner": _noncommuting_limits, "input": {"numerator": "a", "denominator": "a + 1/V", "a_domain": "a>0", "volume_domain": "V>0"}},
}


def _callable_digest(callable_: Callable[..., Any]) -> str:
    return canonical_digest({"module": callable_.__module__, "qualname": callable_.__qualname__, "source": inspect.getsource(callable_)})


def run_ym_calibration(
    case_id: str, *, theory_commission: Mapping[str, Any] | None = None
) -> dict[str, Any]:
    entry = CALIBRATION_REGISTRY[case_id]
    if entry["kind"] == "simulation" and theory_commission is None:
        raise YMCalibrationError("simulation calibration requires an exact theory commission")
    if theory_commission is not None:
        required = {"theory_programme_digest", "reflection_packet_digest", "question_digest", "status"}
        if set(theory_commission) != required or theory_commission["status"] != "commissioned":
            raise YMCalibrationError("theory commission is incomplete")
    input_payload = copy.deepcopy(entry["input"])
    input_digest = canonical_digest(input_payload)
    output_payload = {
        "case_id": case_id,
        "runner_kind": entry["kind"],
        "result": entry["runner"](input_payload),
        "promotion_authorized": False,
        "authority_boundary": "Local calibration of a restricted or false-positive case only.",
    }
    output_digest = canonical_digest(output_payload)
    evidence = {
        "evidence_id": f"calibration.{case_id}",
        "artifact_path": "skills/common/ym_abstraction_calibrations.py",
        "claim": "A registry-bound local runner replayed the declared restricted-model boundary.",
        "payload": output_payload,
        "content_digest": output_digest,
    }
    receipt = {
        "validator_id": "ym-local-calibration-replay-validator.v1",
        "validator_version": "1.0.0",
        "runner_id": entry["runner_id"],
        "runner_version": "1.0.0",
        "runner_kind": entry["kind"],
        "runner_executable_digest": _callable_digest(entry["runner"]),
        "validated_input_digest": input_digest,
        "validated_output_digest": output_digest,
        "validated_evidence_digest": canonical_digest(evidence),
        "dependency_authority_digest": build_formal_dependency_authority()["content_digest"],
        "status": "passed",
    }
    receipt["receipt_id"] = stable_identifier("ym-calibration-receipt", receipt)
    return {
        "case_id": case_id,
        "predicted_outcome": "The runner must recover a restricted-model or false-positive boundary without target promotion.",
        "pass_condition": "Exact replay matches and promotion_authorized remains false.",
        "runner_id": entry["runner_id"], "runner_version": "1.0.0", "runner_kind": entry["kind"],
        "theory_commission": copy.deepcopy(theory_commission),
        "dependency_authority": build_formal_dependency_authority(),
        "input": input_payload, "input_digest": input_digest,
        "output": output_payload, "output_digest": output_digest,
        "result_status": "passed", "evidence": evidence, "validator_receipt": receipt,
    }


def run_ym_calibration_matrix() -> list[dict[str, Any]]:
    return [run_ym_calibration(case_id) for case_id in sorted(CALIBRATION_REGISTRY)]


def validate_ym_calibration(row: Mapping[str, Any]) -> dict[str, Any]:
    case_id = str(row["case_id"])
    entry = CALIBRATION_REGISTRY.get(case_id)
    validate_formal_dependency_authority(row["dependency_authority"])
    if entry is None or row["runner_id"] != entry["runner_id"] or row["runner_version"] != "1.0.0" or row["runner_kind"] != entry["kind"]:
        raise YMCalibrationError("calibration runner is not the registered case implementation")
    if row["input"] != entry["input"] or row["input_digest"] != canonical_digest(row["input"]):
        raise YMCalibrationError("calibration input is not the sealed registered case input")
    if entry["kind"] == "simulation" and row.get("theory_commission") is None:
        raise YMCalibrationError("simulation calibration lacks a theory commission")
    if row["result_status"] != "passed":
        if any(row.get(field) is not None for field in ("output", "output_digest", "evidence", "validator_receipt")):
            raise YMCalibrationError("non-passed calibration cannot carry completed output authority")
        return {"status": row["result_status"], "case_id": case_id}
    expected = run_ym_calibration(case_id, theory_commission=row.get("theory_commission"))
    if dict(row) != expected:
        raise YMCalibrationError("calibration row is not an exact registered replay")
    return {"status": "passed", "case_id": case_id, "output_digest": row["output_digest"]}


__all__ = [
    "CALIBRATION_REGISTRY", "YMCalibrationError", "run_ym_calibration",
    "run_ym_calibration_matrix", "validate_ym_calibration",
]
