"""Theory-requested experiment triage, immutable execution, and validation."""

from __future__ import annotations

import json
import os
import platform
import re
import sys
from pathlib import Path
from typing import Any, Mapping

from agentic.discovery.budgets import ResourceGovernor, contained_path, validate_job_id
from agentic.discovery.contracts import (
    ContractError,
    canonical_digest,
    stable_identifier,
    utc_now,
    validate_payload,
)

from .adapters import AdapterSpecError, execute_adapter, exact_adapter, finite_model_adapter


SCHEMA_ROOT = Path(__file__).resolve().parents[1] / "spec"
TRIAGE_SCHEMA = SCHEMA_ROOT / "dynamic_probe_triage.schema.json"
SPEC_SCHEMA = SCHEMA_ROOT / "dynamic_experiment_spec.schema.json"
RECEIPT_SCHEMA = SCHEMA_ROOT / "dynamic_experiment_receipt.schema.json"
ADAPTER_VERSION = "dynamic-experiment-adapters/1.0.0"
_DIGEST = re.compile(r"^sha256:[0-9a-f]{64}$")


def _nonempty(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def triage_probe(request: Mapping[str, Any]) -> dict[str, Any]:
    """Decide whether a mature theory question warrants a support probe."""

    source = dict(request)
    input_digest = canonical_digest(source, exclude_keys=("input_digest", "triage_id", "created_at"))
    target_id = str(source.get("target_id", ""))
    theory_id = source.get("theory_programme_id")
    programme_digest = source.get("source_theory_programme_digest")
    reflection_digest = source.get("source_reflection_packet_digest")
    question_id = source.get("theoretical_question_id")
    conceptual_ids = sorted(set(str(value) for value in source.get("conceptual_system_ids", []) if _nonempty(value)))
    maturity = source.get("programme_maturity", "unformed")
    question = str(source.get("question", ""))
    expected_change = str(source.get("expected_conceptual_change", ""))
    justification = str(source.get("theory_generated_justification", ""))
    decision_effect = source.get("decision_effect", {})
    methods = sorted(set(source.get("candidate_methods", [])))
    reasons: list[str] = []

    if source.get("probe_needed") is False:
        decision = "no_probe_needed"
        reasons.append("the theory programme explicitly has no decision that requires computational support")
    else:
        mature = maturity in {"mature", "formalization_ready"}
        exact_question = _nonempty(question) and _nonempty(question_id)
        effectful = (
            isinstance(decision_effect, Mapping)
            and _nonempty(decision_effect.get("if_supported"))
            and _nonempty(decision_effect.get("if_not_supported"))
            and decision_effect.get("if_supported") != decision_effect.get("if_not_supported")
            and _nonempty(expected_change)
        )
        theory_bound = (
            _nonempty(theory_id)
            and bool(conceptual_ids)
            and _nonempty(justification)
            and isinstance(programme_digest, str)
            and _DIGEST.fullmatch(programme_digest) is not None
            and isinstance(reflection_digest, str)
            and _DIGEST.fullmatch(reflection_digest) is not None
        )
        if mature and exact_question and effectful and theory_bound and methods:
            decision = "commission"
            reasons.append("a mature theory generated a discriminating support question with two consequential outcomes")
        elif not mature or not exact_question or not theory_bound:
            decision = "immature_question"
            reasons.append("the theory programme, conceptual binding, or exact support question is not mature")
        else:
            decision = "no_probe_needed"
            reasons.append("the proposed computation has no preregistered conceptual decision consequence")

    triage = {
        "schema_version": 1,
        "triage_id": stable_identifier("triage", target_id, theory_id, question_id, input_digest),
        "target_id": target_id,
        "theory_programme_id": theory_id if _nonempty(theory_id) else None,
        "source_theory_programme_digest": (
            programme_digest
            if isinstance(programme_digest, str) and _DIGEST.fullmatch(programme_digest)
            else None
        ),
        "source_reflection_packet_digest": (
            reflection_digest
            if isinstance(reflection_digest, str) and _DIGEST.fullmatch(reflection_digest)
            else None
        ),
        "conceptual_system_ids": conceptual_ids,
        "theoretical_question_id": question_id if _nonempty(question_id) else None,
        "question": question,
        "programme_maturity": maturity,
        "probe_role": source.get("probe_role", "none"),
        "decision": decision,
        "decision_effect": {
            "if_supported": str(decision_effect.get("if_supported", "")),
            "if_not_supported": str(decision_effect.get("if_not_supported", "")),
        },
        "expected_conceptual_change": expected_change,
        "theory_generated_justification": justification,
        "candidate_methods": methods,
        "state_version": int(source.get("state_version", 0)),
        "input_digest": input_digest,
        "reasons": reasons,
        "created_at": utc_now(),
    }
    validate_payload(triage, TRIAGE_SCHEMA)
    return triage


def _environment() -> dict[str, Any]:
    capabilities: dict[str, Any] = {}
    for module in ("sympy",):
        try:
            loaded = __import__(module)
            capabilities[module] = {"available": True, "version": getattr(loaded, "__version__", "unknown")}
        except ImportError:
            capabilities[module] = {"available": False}
    return {
        "python": sys.version.split()[0],
        "implementation": platform.python_implementation(),
        "platform": platform.platform(),
        "capabilities": capabilities,
    }


def current_code_digest() -> str:
    material = []
    for path in sorted(Path(__file__).parent.glob("*.py")):
        material.append({"name": path.name, "text": path.read_text(encoding="utf-8")})
    return canonical_digest(material)


def compile_experiment_spec(triage: Mapping[str, Any], request: Mapping[str, Any]) -> dict[str, Any]:
    """Compile a commissioned triage decision into a frozen experiment spec."""

    validate_payload(dict(triage), TRIAGE_SCHEMA)
    if triage.get("decision") != "commission":
        raise ContractError("only a commissioned triage decision can compile an experiment")
    adapter = request.get("adapter")
    if adapter not in triage.get("candidate_methods", []):
        raise ContractError("selected adapter was not admitted by triage")
    stochastic = bool(request.get("seed_policy", {}).get("stochastic"))
    preregistration = request.get("preregistration", {})
    if stochastic:
        missing = [name for name in ("estimand", "sample_size", "stopping_rule", "uncertainty_method") if not preregistration.get(name)]
        if missing:
            raise ContractError(f"stochastic preregistration missing: {', '.join(missing)}")
    environment = request.get("environment") or _environment()
    spec = {
        "schema_version": 1,
        "experiment_id": str(request.get("experiment_id") or stable_identifier("experiment", triage["triage_id"], adapter, request.get("model"))),
        "branch_id": validate_job_id(str(request.get("branch_id"))),
        "target_id": triage["target_id"],
        "run_id": validate_job_id(str(request.get("run_id"))),
        "state_version": triage["state_version"],
        "theory_programme_id": triage["theory_programme_id"],
        "source_theory_programme_digest": triage[
            "source_theory_programme_digest"
        ],
        "source_reflection_packet_digest": triage[
            "source_reflection_packet_digest"
        ],
        "conceptual_system_ids": list(triage["conceptual_system_ids"]),
        "theoretical_question_id": triage["theoretical_question_id"],
        "probe_role": triage["probe_role"],
        "expected_conceptual_change": triage["expected_conceptual_change"],
        "triage_digest": canonical_digest(triage, exclude_keys=("created_at",)),
        "adapter": adapter,
        "model": dict(request.get("model", {})),
        "preregistration": dict(preregistration),
        "controls": list(request.get("controls", [])),
        "seed_policy": dict(request.get("seed_policy", {"stochastic": False, "policy": "not_applicable"})),
        "resource_budget": dict(request.get("resource_budget", {})),
        "transfer_boundary": str(request.get("transfer_boundary", "")),
        "code_version": str(request.get("code_version", ADAPTER_VERSION)),
        "environment": dict(environment),
        "created_at": str(request.get("created_at") or utc_now()),
    }
    spec["spec_digest"] = canonical_digest(spec, exclude_keys=("spec_digest", "created_at"))
    validate_payload(spec, SPEC_SCHEMA)
    return spec


def experiment_directory(run_directory: Path | str, spec: Mapping[str, Any]) -> Path:
    root = Path(run_directory).resolve()
    branch = validate_job_id(str(spec["branch_id"]))
    experiment = validate_job_id(str(spec["experiment_id"]))
    return contained_path(root, "branches", branch, "experiments", experiment)


def _write_immutable_json(path: Path, payload: Mapping[str, Any]) -> None:
    encoded = json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False) + "\n"
    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        with path.open("x", encoding="utf-8") as stream:
            stream.write(encoded)
            stream.flush()
            os.fsync(stream.fileno())
    except FileExistsError:
        existing = json.loads(path.read_text(encoding="utf-8"))
        if canonical_digest(existing) != canonical_digest(payload):
            raise ContractError(f"immutable experiment artifact conflict: {path}")


def validate_experiment_receipt(
    receipt: Mapping[str, Any],
    spec: Mapping[str, Any],
    *,
    work_directory: Path | None = None,
) -> None:
    """Independently validate receipt identity and adapter certificate semantics."""

    validate_payload(dict(spec), SPEC_SCHEMA)
    validate_payload(dict(receipt), RECEIPT_SCHEMA)
    if receipt["spec_digest"] != spec["spec_digest"]:
        raise ContractError("experiment receipt is stale for this specification")
    for field in (
        "experiment_id",
        "branch_id",
        "target_id",
        "run_id",
        "state_version",
        "theory_programme_id",
        "source_theory_programme_digest",
        "source_reflection_packet_digest",
        "theoretical_question_id",
        "adapter",
    ):
        if receipt[field] != spec[field]:
            raise ContractError(f"receipt/spec mismatch for {field}")
    if receipt["conceptual_system_ids"] != spec["conceptual_system_ids"]:
        raise ContractError("receipt/spec conceptual system mismatch")
    if receipt["status"] == "counterexample" and receipt["certificate"] is None:
        raise ContractError("counterexample outcome requires a replayable certificate")
    if spec["adapter"] == "finite_model" and receipt["status"] in {"succeeded", "counterexample"}:
        completeness = receipt.get("completeness") or {}
        if completeness.get("complete") is not True:
            raise ContractError("decisive finite result lacks completeness or a decisive verified witness")
    if spec["seed_policy"].get("stochastic"):
        if not receipt.get("uncertainty_analysis") or not receipt.get("certificate", {}).get("seed_policy"):
            raise ContractError("stochastic result lacks uncertainty analysis or seed replay certificate")
    # Independently replay every decisive dependency-free adapter.  Operational
    # outcomes are deliberately not replayed into epistemic outcomes.
    if receipt["status"] in {"succeeded", "counterexample"} and spec["adapter"] in {
        "exact",
        "finite_model",
        "numeric",
        "sweep",
        "sympy",
    }:
        validation_governor = ResourceGovernor.from_mapping(spec["resource_budget"])
        replayed = execute_adapter(spec, validation_governor, work_directory or Path.cwd())
        for field in ("status", "epistemic_outcome", "result", "certificate", "uncertainty_analysis", "completeness"):
            if canonical_digest(replayed.get(field)) != canonical_digest(receipt.get(field)):
                raise ContractError(f"independent adapter replay mismatch for {field}")
    elif receipt["status"] == "succeeded" and spec["adapter"] == "lean":
        if work_directory is None:
            raise ContractError("Lean receipt validation requires its immutable work directory")
        validation_governor = ResourceGovernor.from_mapping(spec["resource_budget"], run_directory=work_directory)
        replayed = execute_adapter(spec, validation_governor, work_directory)
        if replayed["status"] != "succeeded" or replayed.get("certificate", {}).get("proposition") != receipt.get("certificate", {}).get("proposition"):
            raise ContractError("independent Lean kernel replay failed")
    expected_output = canonical_digest(
        {
            "result": receipt["result"],
            "certificate": receipt["certificate"],
            "uncertainty_analysis": receipt["uncertainty_analysis"],
            "completeness": receipt["completeness"],
        }
    )
    if receipt["output_digest"] != expected_output:
        raise ContractError("experiment output digest mismatch")
    if receipt["validator"]["checked_digest"] != expected_output or receipt["validator"]["status"] != "valid":
        raise ContractError("experiment validator did not validate the exact output")
    linked = {row["conceptual_system_id"] for row in receipt["reflective_assimilation"]}
    if linked != set(spec["conceptual_system_ids"]):
        raise ContractError("every linked conceptual system must receive an assimilation recommendation")


def receipt_staleness(receipt: Mapping[str, Any], current_spec: Mapping[str, Any]) -> dict[str, Any]:
    """Explain whether model, decision rule, code, or environment invalidates a receipt."""

    reasons = []
    expected_spec = canonical_digest(current_spec, exclude_keys=("spec_digest", "created_at"))
    if receipt.get("spec_digest") != expected_spec:
        reasons.append("spec_or_preregistration_changed")
    if receipt.get("code_digest") != current_code_digest():
        reasons.append("adapter_code_changed")
    expected_environment = canonical_digest(current_spec.get("environment", {}))
    if receipt.get("environment_digest") != expected_environment:
        reasons.append("environment_changed")
    return {"stale": bool(reasons), "reasons": reasons}


def execute_experiment(spec: Mapping[str, Any], run_directory: Path | str) -> dict[str, Any]:
    """Execute once in a branch-scoped immutable directory and return a receipt."""

    validate_payload(dict(spec), SPEC_SCHEMA)
    expected_digest = canonical_digest(spec, exclude_keys=("spec_digest", "created_at"))
    if spec.get("spec_digest") != expected_digest:
        raise ContractError("experiment spec digest is invalid")
    workdir = experiment_directory(run_directory, spec)
    workdir.mkdir(parents=True, exist_ok=True)
    preregistration_path = workdir / "preregistration.json"
    spec_path = workdir / "spec.json"
    receipt_path = workdir / "receipt.json"
    code_manifest_path = workdir / "code-manifest.json"
    code_digest = current_code_digest()
    environment_digest = canonical_digest(spec["environment"])
    _write_immutable_json(preregistration_path, dict(spec["preregistration"]))
    _write_immutable_json(spec_path, dict(spec))
    _write_immutable_json(
        code_manifest_path,
        {
            "adapter_version": spec["code_version"],
            "code_digest": code_digest,
            "environment": spec["environment"],
            "environment_digest": environment_digest,
        },
    )
    if receipt_path.exists():
        existing = json.loads(receipt_path.read_text(encoding="utf-8"))
        validate_experiment_receipt(existing, spec, work_directory=workdir)
        if receipt_staleness(existing, spec)["stale"]:
            raise ContractError("existing experiment receipt is stale")
        return existing

    governor = ResourceGovernor.from_mapping(spec["resource_budget"], run_directory=workdir)
    started_at = utc_now()
    try:
        output = execute_adapter(spec, governor, workdir)
        failure = None
    except AdapterSpecError as exc:
        output = {
            "status": "invalid_spec",
            "epistemic_outcome": "not_evaluated",
            "result": {"error": str(exc)},
            "certificate": None,
            "uncertainty_analysis": None,
            "completeness": None,
        }
        failure = {"kind": "invalid_spec", "message": str(exc), "epistemic_effect": "none"}
    output_digest = canonical_digest(
        {
            "result": output["result"],
            "certificate": output["certificate"],
            "uncertainty_analysis": output["uncertainty_analysis"],
            "completeness": output["completeness"],
        }
    )
    recommendation = {
        "supports_within_scope": "Reflect on whether the bounded support sharpens the named mechanism without treating it as theorem proof.",
        "falsifies_claim": "Revisit the originating premise and conceptual mechanism using the verified scoped counterexample.",
        "maps_boundary": "Assimilate the mapped validity boundary and revise the theory's domain claims.",
        "inconclusive": "Preserve the theory and record the operational or finite-scope limit; do not infer falsification.",
        "not_evaluated": "Record the operational outcome only; the theory remains epistemically unchanged.",
    }[output["epistemic_outcome"]]
    receipt = {
        "schema_version": 1,
        "receipt_id": stable_identifier("experiment-receipt", spec["experiment_id"], spec["spec_digest"], output_digest),
        "experiment_id": spec["experiment_id"],
        "branch_id": spec["branch_id"],
        "target_id": spec["target_id"],
        "run_id": spec["run_id"],
        "state_version": spec["state_version"],
        "theory_programme_id": spec["theory_programme_id"],
        "source_theory_programme_digest": spec[
            "source_theory_programme_digest"
        ],
        "source_reflection_packet_digest": spec[
            "source_reflection_packet_digest"
        ],
        "conceptual_system_ids": list(spec["conceptual_system_ids"]),
        "theoretical_question_id": spec["theoretical_question_id"],
        "adapter": spec["adapter"],
        "status": output["status"],
        "epistemic_outcome": output["epistemic_outcome"],
        "spec_digest": spec["spec_digest"],
        "code_digest": code_digest,
        "environment_digest": environment_digest,
        "started_at": started_at,
        "completed_at": utc_now(),
        "resource_usage": governor.receipt("succeeded" if output["status"] in {"succeeded", "counterexample"} else "worker_failed"),
        "result": output["result"],
        "certificate": output["certificate"],
        "uncertainty_analysis": output["uncertainty_analysis"],
        "completeness": output["completeness"],
        "validator": {"validator_id": "dynamic-experiment-independent-validator", "version": "1.0.0", "status": "valid", "checked_digest": output_digest},
        "output_digest": output_digest,
        "transfer_boundary": spec["transfer_boundary"],
        "reflective_assimilation": [
            {
                "conceptual_system_id": conceptual_id,
                "recommendation": recommendation,
                "authority_boundary": "reflective_assimilation_required_runtime_does_not_select_theory_or_prove_theorem",
            }
            for conceptual_id in spec["conceptual_system_ids"]
        ],
        "failure": failure,
    }
    validate_experiment_receipt(receipt, spec, work_directory=workdir)
    _write_immutable_json(receipt_path, receipt)
    return receipt
