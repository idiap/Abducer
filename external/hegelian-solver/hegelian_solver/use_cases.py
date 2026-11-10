# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT

"""Spec-derived use-case corpus loading, validation, and execution.

The 65 fixtures in `examples/use_cases/spec_use_cases.yaml` are the framework's regression
corpus across math/physics/LM domains. `validate_use_case_payload` enforces the "public
reasoning fitness" bar every case must clear (declared formal/material/epistemic blocks,
at least one task, at least one piece of negative evidence) before it's allowed to run.
`run_use_case_suite` then runs every validated case through `orchestrator.run_solver`,
writing each case's full artifact set under its own subdirectory and a `suite_result.json`
summary — this is what `hegelian-solver run-suite` and `hegelian-solver validate-use-cases`
call.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from hegelian_solver.io import read_structured, write_structured
from hegelian_solver.orchestrator import run_solver
from hegelian_solver.schemas import DomainName, UseCaseSuiteItem, UseCaseSuiteResult


DEFAULT_USE_CASES_PATH = Path(__file__).parent / "examples" / "use_cases" / "spec_use_cases.yaml"
DEFAULT_USE_CASE_RUNS_DIR = Path("data") / "use_case_runs"
REQUIRED_EPISTEMIC_BLOCKS = ("formal_analysis", "material_analysis", "epistemic_profile")
REQUIRED_DOMAIN_VALUES = {
    "mathematical_concept",
    "physical_concept",
    "language_model_concept",
    "generic_concept",
}


def _use_case_list(payload: Any) -> list[dict[str, Any]]:
    if isinstance(payload, dict):
        items = payload.get("use_cases")
    else:
        items = payload
    if not isinstance(items, list):
        raise ValueError("use-case manifest must contain a `use_cases` list")
    for index, item in enumerate(items):
        if not isinstance(item, dict):
            raise ValueError(f"use_cases[{index}] must be an object")
    return items


def load_use_cases(path: str | Path = DEFAULT_USE_CASES_PATH) -> list[dict[str, Any]]:
    """Load the spec-instantiated use-case manifest."""

    return _use_case_list(read_structured(path))


def validate_use_case_payload(raw: dict[str, Any], *, index: int | None = None) -> list[str]:
    """Return validation errors for one use case.

    The checks intentionally focus on public reasoning fitness: every case must
    expose a formal account, a material/evidence account, and an epistemic profile.
    """

    prefix = f"use_cases[{index}]" if index is not None else str(raw.get("id", "use_case"))
    errors: list[str] = []
    for field in ("id", "name", "domain", "role", "tasks", "source_refs"):
        if not raw.get(field):
            errors.append(f"{prefix}: missing non-empty `{field}`")
    if raw.get("domain") not in REQUIRED_DOMAIN_VALUES:
        errors.append(f"{prefix}: unsupported domain `{raw.get('domain')}`")
    if not isinstance(raw.get("tasks"), list) or not raw.get("tasks"):
        errors.append(f"{prefix}: `tasks` must be a non-empty list")
    if not any(raw.get(field) for field in ("reported_failures", "counterexamples", "examples", "anomalies")):
        errors.append(
            f"{prefix}: needs at least one reported failure, anomaly, example, or counterexample"
        )
    for block in REQUIRED_EPISTEMIC_BLOCKS:
        value = raw.get(block)
        if not isinstance(value, dict) or not value:
            errors.append(f"{prefix}: `{block}` must be a non-empty object")
    epistemic = raw.get("epistemic_profile", {})
    if isinstance(epistemic, dict):
        if not any(epistemic.get(field) for field in ("knowns", "assumptions", "unknowns")):
            errors.append(f"{prefix}: epistemic profile must name knowns, assumptions, or unknowns")
        if not epistemic.get("uncertainty"):
            errors.append(f"{prefix}: epistemic profile must declare uncertainty")
    material = raw.get("material_analysis", {})
    if isinstance(material, dict) and not any(material.get(field) for field in ("evidence", "practice")):
        errors.append(f"{prefix}: material analysis must cite evidence or practice")
    formal = raw.get("formal_analysis", {})
    if isinstance(formal, dict) and not any(formal.get(field) for field in ("operator", "obligations")):
        errors.append(f"{prefix}: formal analysis must declare an operator or obligations")
    return errors


def validate_use_cases(path: str | Path = DEFAULT_USE_CASES_PATH) -> list[str]:
    """Validate the full manifest and return all public-reasoning defects."""

    cases = load_use_cases(path)
    errors: list[str] = []
    seen: set[str] = set()
    for index, raw in enumerate(cases):
        case_id = str(raw.get("id", f"use_cases[{index}]"))
        if case_id in seen:
            errors.append(f"use_cases[{index}]: duplicate id `{case_id}`")
        seen.add(case_id)
        errors.extend(validate_use_case_payload(raw, index=index))
    return errors


def _domain_counts(cases: list[dict[str, Any]]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for raw in cases:
        domain = str(raw.get("domain", "unknown"))
        counts[domain] = counts.get(domain, 0) + 1
    return counts


def _artifact_paths(case_dir: Path, run_id: str) -> dict[str, str]:
    return {
        "trace_file": str(case_dir / "traces" / f"{run_id}.json"),
        "reasoning_log_file": str(case_dir / "reasoning_logs" / f"{run_id}.json"),
        "report_file": str(case_dir / "reports" / f"{run_id}.html"),
    }


def run_use_case_suite(
    *,
    path: str | Path = DEFAULT_USE_CASES_PATH,
    output_dir: str | Path = DEFAULT_USE_CASE_RUNS_DIR,
    limit: int | None = None,
) -> UseCaseSuiteResult:
    """Run every validated spec use case through the deterministic solver."""

    source_path = Path(path)
    target = Path(output_dir)
    cases = load_use_cases(source_path)
    if limit is not None:
        cases = cases[:limit]
    validation_errors = validate_use_cases(source_path)
    if limit is not None:
        validation_errors = [
            error
            for error in validation_errors
            if any(f"use_cases[{index}]" in error for index in range(limit))
        ]
    if validation_errors:
        raise ValueError("use-case validation failed: " + "; ".join(validation_errors[:10]))

    items: list[UseCaseSuiteItem] = []
    for raw in cases:
        case_dir = target / str(raw["id"])
        try:
            trace = run_solver(raw, output_dir=case_dir)
            index = trace.reasoning_log.get("machine_index", {})
            fme = index.get("formal_material_epistemic", {})
            items.append(
                UseCaseSuiteItem(
                    id=str(raw["id"]),
                    name=str(raw["name"]),
                    domain=raw["domain"],  # type: ignore[arg-type]
                    status="passed",
                    run_id=trace.run_id,
                    output_dir=str(case_dir),
                    final_status=trace.reasoning_log.get("final_status"),
                    failure_count=len(trace.failures),
                    discovery_signal_count=len(trace.discovery_signals),
                    candidate_count=len(trace.candidates),
                    validation_packet_count=len(trace.validation_packets),
                    ranking_decision_count=len(trace.ranking_decisions),
                    formal_material_epistemic={
                        "formal": bool(fme.get("formal")),
                        "material": bool(fme.get("material")),
                        "epistemic": bool(fme.get("epistemic")),
                    },
                    **_artifact_paths(case_dir, trace.run_id),
                )
            )
        except Exception as exc:  # pragma: no cover - retained in suite summary for diagnostics
            items.append(
                UseCaseSuiteItem(
                    id=str(raw.get("id", "unknown")),
                    name=str(raw.get("name", "unknown")),
                    domain=raw.get("domain", "generic_concept") if raw.get("domain") in REQUIRED_DOMAIN_VALUES else "generic_concept",  # type: ignore[arg-type]
                    status="failed",
                    output_dir=str(case_dir),
                    error=str(exc),
                )
            )

    passed = sum(1 for item in items if item.status == "passed")
    result = UseCaseSuiteResult(
        source_path=str(source_path),
        output_dir=str(target),
        total=len(items),
        passed=passed,
        failed=len(items) - passed,
        domain_counts=_domain_counts(cases),
        validation_errors=[],
        items=items,
    )
    write_structured(target / "suite_result.json", result)
    return result
