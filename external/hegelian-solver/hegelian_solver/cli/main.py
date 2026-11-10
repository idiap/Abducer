# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT

"""Command line interface for Hegelian Solver.

Every pipeline stage is reachable two ways: end-to-end via `run` (full orchestrated pass,
including the reflective refinement loop), or standalone via one subcommand per stage
(`classify-failure`, `mine-discovery`, `propose`, `verify`, `rank`, `explain`,
`reasoning-log`, `report`, `graph inspect|export`) so a single stage can be exercised or
debugged without running the whole solver. `mechanism *` subcommands do the same for the
abductive mechanism reasoning packets (`schemas/mechanisms.py`), and
`list-use-cases`/`validate-use-cases`/`run-suite` drive the 65-case regression corpus in
`use_cases.py`. Each `command_*` function is a thin adapter: load typed input with
`read_structured`/`model_validate`, call the corresponding library function, print with
`_print`.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from hegelian_solver.creativity import validate_creativity_analysis
from hegelian_solver.discovery import mine_discovery_signals
from hegelian_solver.domain import domain_profile
from hegelian_solver.failures import classify_failures
from hegelian_solver.formalizer import formalize_concept
from hegelian_solver.graph import ConceptGraph
from hegelian_solver.io import read_structured, to_plain
from hegelian_solver.mechanisms import (
    load_mechanism_dossier,
    load_mechanism_dossiers,
    mechanism_validation_packet,
    mechanism_validation_packet_from_dossier,
)
from hegelian_solver.operators import propose_candidates
from hegelian_solver.orchestrator import DEFAULT_MAX_ITERATIONS, run_solver
from hegelian_solver.ranker import rank_candidates
from hegelian_solver.reports import write_html_report
from hegelian_solver.schemas import (
    ConceptualCreativityAnalysis,
    DiscoverySignal,
    FailureCertificate,
    MechanismAbductionPacket,
    MechanismCounterfactualCritique,
    MechanismRequirementsPacket,
    MechanismTodoPacket,
    ReasoningLog,
    TransformationCandidate,
)
from hegelian_solver.schemas.json_schema import export_json_schemas
from hegelian_solver.use_cases import (
    DEFAULT_USE_CASE_RUNS_DIR,
    DEFAULT_USE_CASES_PATH,
    load_use_cases,
    run_use_case_suite,
    validate_use_cases,
)
from hegelian_solver.validators import validate_candidates


def _print(payload: Any, human: bool = False) -> None:
    plain = to_plain(payload)
    if human:
        if isinstance(plain, dict) and "explanation" in plain:
            print(plain["explanation"])
            return
        print(json.dumps(plain, indent=2, sort_keys=True))
        return
    print(json.dumps(plain, indent=2, sort_keys=True))


def _load_concept(path: str):
    raw = read_structured(path)
    profile = domain_profile(raw)
    return formalize_concept(raw, profile)


def command_run(args: argparse.Namespace) -> None:
    trace = run_solver(args.concept_file, output_dir=args.output_dir, max_iterations=args.max_iterations)
    _print(trace.model_dump(mode="json"), human=args.human)


def command_classify_failure(args: argparse.Namespace) -> None:
    concept = _load_concept(args.concept_file)
    _print([item.model_dump(mode="json") for item in classify_failures(concept)])


def command_mine_discovery(args: argparse.Namespace) -> None:
    concept = _load_concept(args.concept_file)
    _print([item.model_dump(mode="json") for item in mine_discovery_signals(concept)])


def _load_triggers(path: str) -> list[FailureCertificate | DiscoverySignal]:
    payload = read_structured(path)
    items = payload if isinstance(payload, list) else payload.get("triggers", payload.get("items", [payload]))
    triggers: list[FailureCertificate | DiscoverySignal] = []
    for item in items:
        if "failed_obligation" in item:
            triggers.append(FailureCertificate.model_validate(item))
        else:
            triggers.append(DiscoverySignal.model_validate(item))
    return triggers


def command_propose(args: argparse.Namespace) -> None:
    concept = _load_concept(args.concept_file)
    triggers = _load_triggers(args.triggers_file)
    candidates = propose_candidates(concept, triggers)
    _print([item.model_dump(mode="json") for item in candidates])


def command_verify(args: argparse.Namespace) -> None:
    concept = _load_concept(args.concept_file)
    payload = read_structured(args.candidates_file)
    items = payload if isinstance(payload, list) else payload.get("candidates", [payload])
    candidates = [TransformationCandidate.model_validate(item) for item in items]
    packets = validate_candidates(concept, candidates)
    _print([item.model_dump(mode="json") for item in packets])


def command_rank(args: argparse.Namespace) -> None:
    candidates_payload = read_structured(args.candidates_file)
    validation_payload = read_structured(args.validation_file)
    candidates = [
        TransformationCandidate.model_validate(item)
        for item in (
            candidates_payload
            if isinstance(candidates_payload, list)
            else candidates_payload.get("candidates", [candidates_payload])
        )
    ]
    from hegelian_solver.schemas import ValidationPacket

    packets = [
        ValidationPacket.model_validate(item)
        for item in (
            validation_payload
            if isinstance(validation_payload, list)
            else validation_payload.get("validation_packets", [validation_payload])
        )
    ]
    _print([item.model_dump(mode="json") for item in rank_candidates(candidates, packets)])


def command_explain(args: argparse.Namespace) -> None:
    trace = read_structured(args.trace_file)
    if isinstance(trace, dict) and "explanation" in trace:
        print(trace["explanation"])
    else:
        _print(trace)


def _load_reasoning_log(path: str) -> ReasoningLog:
    payload = read_structured(path)
    if isinstance(payload, dict) and "reasoning_log" in payload:
        return ReasoningLog.model_validate(payload["reasoning_log"])
    return ReasoningLog.model_validate(payload)


def command_reasoning_log(args: argparse.Namespace) -> None:
    log = _load_reasoning_log(args.input_file)
    _print(log.model_dump(mode="json"), human=args.human)


def command_creativity(args: argparse.Namespace) -> None:
    payload = read_structured(args.input_file)
    if isinstance(payload, dict) and "creativity_analyses" in payload:
        items = payload["creativity_analyses"]
    elif isinstance(payload, dict) and "reasoning_log" in payload:
        items = payload["reasoning_log"].get("creativity_analyses", [])
    elif isinstance(payload, list):
        items = payload
    else:
        items = []
    analyses = [ConceptualCreativityAnalysis.model_validate(item) for item in items]

    if args.validate:
        violations = {
            analysis.candidate_id: issues
            for analysis in analyses
            if (issues := validate_creativity_analysis(analysis))
        }
        _print({"valid": not violations, "analyzed": len(analyses), "violations": violations})
        if violations:
            raise RuntimeError(f"{len(violations)} creativity analyses failed validation")
        return

    _print([analysis.model_dump(mode="json") for analysis in analyses])


def command_report(args: argparse.Namespace) -> None:
    log = _load_reasoning_log(args.input_file)
    if args.mechanisms:
        dossiers = load_mechanism_dossiers(args.mechanisms)
        log = log.model_copy(
            update={"mechanisms": [dossier.model_dump(mode="json", by_alias=True) for dossier in dossiers]}
        )
    output = args.output or str(Path(args.input_file).with_suffix(".html"))
    path = write_html_report(log, output)
    _print({"written": str(path)})


def _load_packet(path: str, key: str, model):
    payload = read_structured(path)
    if isinstance(payload, dict) and key in payload:
        payload = payload[key]
    return model.model_validate(payload)


def command_mechanism_abduce(args: argparse.Namespace) -> None:
    packet = _load_packet(args.packet_file, "mechanism_abduction_packet", MechanismAbductionPacket)
    _print(packet.model_dump(mode="json"))


def command_mechanism_requirements(args: argparse.Namespace) -> None:
    packet = _load_packet(args.packet_file, "mechanism_requirements_packet", MechanismRequirementsPacket)
    _print(packet.model_dump(mode="json"))


def command_mechanism_critique(args: argparse.Namespace) -> None:
    packet = _load_packet(args.packet_file, "mechanism_counterfactual_critique", MechanismCounterfactualCritique)
    _print(packet.model_dump(mode="json"))


def command_mechanism_todos(args: argparse.Namespace) -> None:
    packet = _load_packet(args.packet_file, "mechanism_todo_packet", MechanismTodoPacket)
    _print(packet.model_dump(mode="json", by_alias=True))


def command_mechanism_validation_packet(args: argparse.Namespace) -> None:
    requirements = _load_packet(args.requirements_file, "mechanism_requirements_packet", MechanismRequirementsPacket)
    critique = (
        _load_packet(args.critique_file, "mechanism_counterfactual_critique", MechanismCounterfactualCritique)
        if args.critique_file
        else None
    )
    todos = _load_packet(args.todos_file, "mechanism_todo_packet", MechanismTodoPacket) if args.todos_file else None
    packet = mechanism_validation_packet(requirements, critique, todos)
    _print(packet.model_dump(mode="json"))


def command_mechanism_dossier(args: argparse.Namespace) -> None:
    payload = read_structured(args.dossier_file)
    if isinstance(payload, dict) and "mechanism_examples" in payload:
        dossiers = load_mechanism_dossiers(args.dossier_file)
        if args.id:
            matches = [item for item in dossiers if item.id == args.id]
            if not matches:
                raise ValueError(f"no mechanism dossier with id `{args.id}` in {args.dossier_file}")
            dossier = matches[0]
        elif len(dossiers) == 1:
            dossier = dossiers[0]
        else:
            raise ValueError(f"{args.dossier_file} has {len(dossiers)} dossiers; pass --id to select one")
    else:
        dossier = load_mechanism_dossier(payload)
    if args.validation_packet:
        packet = mechanism_validation_packet_from_dossier(dossier)
        _print(packet.model_dump(mode="json"))
    else:
        _print(dossier.model_dump(mode="json", by_alias=True))


def command_graph(args: argparse.Namespace) -> None:
    graph = ConceptGraph.load(args.graph_file)
    if args.graph_command == "inspect":
        payload = {
            "nodes": len(graph.nodes),
            "edges": len(graph.edges),
            "active_frontier": [node.id for node in graph.active_frontier()],
            "open_residual_limits": graph.open_residual_limits(),
            "rejected_candidates": len(graph.rejected_candidates),
        }
    else:
        payload = graph.to_dict()
    _print(payload)


def command_schema(args: argparse.Namespace) -> None:
    paths = export_json_schemas(args.output_dir)
    _print({"written": [str(path) for path in paths]})


def command_list_use_cases(args: argparse.Namespace) -> None:
    cases = load_use_cases(args.path)
    _print(
        {
            "source_path": str(args.path),
            "total": len(cases),
            "items": [
                {
                    "id": item["id"],
                    "name": item["name"],
                    "domain": item["domain"],
                    "source_refs": item.get("source_refs", []),
                }
                for item in cases
            ],
        }
    )


def command_validate_use_cases(args: argparse.Namespace) -> None:
    errors = validate_use_cases(args.path)
    _print({"source_path": str(args.path), "valid": not errors, "error_count": len(errors), "errors": errors})
    if errors:
        raise RuntimeError(f"{len(errors)} use-case validation errors")


def command_run_suite(args: argparse.Namespace) -> None:
    result = run_use_case_suite(path=args.path, output_dir=args.output_dir, limit=args.limit)
    _print(result)
    if result.failed:
        raise RuntimeError(f"{result.failed} use cases failed")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="hegelian-solver")
    subparsers = parser.add_subparsers(dest="command", required=True)

    run = subparsers.add_parser("run", help="execute a full orchestrated pass")
    run.add_argument("concept_file")
    run.add_argument("--output-dir", default="data")
    run.add_argument("--human", action="store_true")
    run.add_argument(
        "--max-iterations",
        type=int,
        default=DEFAULT_MAX_ITERATIONS,
        help="cap on the reflective refinement loop's propose/validate/rank iterations",
    )
    run.set_defaults(func=command_run)

    classify = subparsers.add_parser("classify-failure")
    classify.add_argument("concept_file")
    classify.set_defaults(func=command_classify_failure)

    discover = subparsers.add_parser("mine-discovery")
    discover.add_argument("concept_file")
    discover.set_defaults(func=command_mine_discovery)

    propose = subparsers.add_parser("propose")
    propose.add_argument("concept_file")
    propose.add_argument("triggers_file")
    propose.set_defaults(func=command_propose)

    verify = subparsers.add_parser("verify")
    verify.add_argument("concept_file")
    verify.add_argument("candidates_file")
    verify.set_defaults(func=command_verify)

    rank = subparsers.add_parser("rank")
    rank.add_argument("candidates_file")
    rank.add_argument("validation_file")
    rank.set_defaults(func=command_rank)

    explain = subparsers.add_parser("explain")
    explain.add_argument("trace_file")
    explain.set_defaults(func=command_explain)

    reasoning_log = subparsers.add_parser("reasoning-log")
    reasoning_log.add_argument("input_file")
    reasoning_log.add_argument("--human", action="store_true")
    reasoning_log.set_defaults(func=command_reasoning_log)

    creativity = subparsers.add_parser(
        "creativity", help="inspect conceptual creativity analyses from a trace or reasoning log"
    )
    creativity.add_argument("input_file")
    creativity.add_argument(
        "--validate", action="store_true", help="check required-explicit fields instead of printing the analyses"
    )
    creativity.set_defaults(func=command_creativity)

    report = subparsers.add_parser("report")
    report.add_argument("input_file")
    report.add_argument("--output")
    report.add_argument("--mechanisms", help="optional mechanism_examples file to attach to the report")
    report.set_defaults(func=command_report)

    mechanism = subparsers.add_parser("mechanism", help="abductive mechanism reasoning artifacts")
    mechanism_sub = mechanism.add_subparsers(dest="mechanism_command", required=True)

    mechanism_abduce = mechanism_sub.add_parser("abduce", help="validate a mechanism_abduction_packet")
    mechanism_abduce.add_argument("packet_file")
    mechanism_abduce.set_defaults(func=command_mechanism_abduce)

    mechanism_requirements = mechanism_sub.add_parser(
        "requirements", help="validate a mechanism_requirements_packet"
    )
    mechanism_requirements.add_argument("packet_file")
    mechanism_requirements.set_defaults(func=command_mechanism_requirements)

    mechanism_critique = mechanism_sub.add_parser(
        "critique", help="validate a mechanism_counterfactual_critique"
    )
    mechanism_critique.add_argument("packet_file")
    mechanism_critique.set_defaults(func=command_mechanism_critique)

    mechanism_todos = mechanism_sub.add_parser("todos", help="validate a mechanism_todo_packet")
    mechanism_todos.add_argument("packet_file")
    mechanism_todos.set_defaults(func=command_mechanism_todos)

    mechanism_validation = mechanism_sub.add_parser(
        "validation-packet", help="build a ValidationPacket from mechanism requirements/critique/todos"
    )
    mechanism_validation.add_argument("requirements_file")
    mechanism_validation.add_argument("--critique-file")
    mechanism_validation.add_argument("--todos-file")
    mechanism_validation.set_defaults(func=command_mechanism_validation_packet)

    mechanism_dossier = mechanism_sub.add_parser(
        "dossier", help="inspect a full mechanism dossier (abduction+requirements+critique+todos)"
    )
    mechanism_dossier.add_argument("dossier_file")
    mechanism_dossier.add_argument("--id", help="select one dossier id from a mechanism_examples file")
    mechanism_dossier.add_argument(
        "--validation-packet", action="store_true", help="print the linked ValidationPacket instead of the dossier"
    )
    mechanism_dossier.set_defaults(func=command_mechanism_dossier)

    graph = subparsers.add_parser("graph")
    graph_sub = graph.add_subparsers(dest="graph_command", required=True)
    inspect = graph_sub.add_parser("inspect")
    inspect.add_argument("graph_file")
    inspect.set_defaults(func=command_graph)
    export = graph_sub.add_parser("export")
    export.add_argument("graph_file")
    export.set_defaults(func=command_graph)

    schema = subparsers.add_parser("schema")
    schema.add_argument("output_dir")
    schema.set_defaults(func=command_schema)

    list_use_cases = subparsers.add_parser("list-use-cases", help="list spec-instantiated use cases")
    list_use_cases.add_argument("--path", default=str(DEFAULT_USE_CASES_PATH))
    list_use_cases.set_defaults(func=command_list_use_cases)

    validate_use_case_cmd = subparsers.add_parser(
        "validate-use-cases", help="validate formal/material/epistemic use-case blocks"
    )
    validate_use_case_cmd.add_argument("--path", default=str(DEFAULT_USE_CASES_PATH))
    validate_use_case_cmd.set_defaults(func=command_validate_use_cases)

    suite = subparsers.add_parser("run-suite", help="run the spec-instantiated use-case suite")
    suite.add_argument("--path", default=str(DEFAULT_USE_CASES_PATH))
    suite.add_argument("--output-dir", default=str(DEFAULT_USE_CASE_RUNS_DIR))
    suite.add_argument("--limit", type=int)
    suite.set_defaults(func=command_run_suite)
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        args.func(args)
        return 0
    except Exception as exc:  # pragma: no cover - user-facing CLI guard
        print(f"hegelian-solver: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
