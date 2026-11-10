# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
"""Acceptance tests for executable, digest-valid discovery operator receipts."""

from __future__ import annotations

import dataclasses
import importlib
import json
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

import agentic.discovery as discovery
import agentic.experiments as experiments
from agentic.discovery.contracts import (
    ContractError,
    Namespace,
    artifact_descriptor,
    canonical_digest,
    stable_identifier,
    validate_instance,
)
from agentic.discovery.conceptual_adjudication import (
    build_adjudication_source_bindings,
    build_blind_packet,
    build_judge_report,
)
from agentic.discovery.hypotheses import build_demo_high_risk_portfolio
from agentic.discovery.literature import (
    LANE_TYPES,
    build_demo_literature_snapshot,
    run_frontier_literature_cycle,
)
from agentic.discovery.receipts import (
    DispatchBlocked,
    DiscoveryOperatorDispatcher,
    OperatorBinding,
    ReceiptStore,
    ValidatorBinding,
    assert_feedback_effective,
    build_operator_request,
    ensure_evaluation_ready,
    request_content_digest,
    validate_operator_receipt_identity,
    verify_current_validator_authority,
)
from agentic.discovery.receipts import _validator_authority_material
from agentic.discovery.workflow import build_reflective_discovery_packet
from agentic.experiments import (
    ExperimentMigrationRequired,
    LOCAL_CAUSAL_AUTHORITY_BOUNDARY,
    compile_experiment_spec,
    triage_probe,
)
from agentic.scripts import discovery_operator_registry as registry_runtime
from agentic.scripts.discovery_operator_registry import load_registry, render_routes
from agentic.scripts.dispatch_discovery_operators import (
    _bindings,
    build_execution_manifest,
    dispatch_request_batch,
    typed_facade_routes_from_registry,
)
from tests.discovery.test_canonical_discovery_cycle import (
    _dialectical_judge,
    _explanatory_judge,
    _ontological_judge,
    _typed_unification,
)


ROOT = Path(__file__).resolve().parents[2]


def _validator(request: dict, artifacts: list[dict], workspace: Path) -> bool:
    """Verify the fixture operator produced JSON bearing its exact request ID."""

    payload = json.loads((workspace / artifacts[0]["path"]).read_text(encoding="utf-8"))
    return payload["request_id"] == request["request_id"]


def _callable_operator(request: dict, workspace: Path) -> dict:
    output = workspace / request["declared_outputs"][0]
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps({"request_id": request["request_id"], "result": "changed ontology"}), encoding="utf-8")
    return {"artifacts": [{"path": request["declared_outputs"][0]}], "explicit_unknowns": ["truth not established"]}


def _binding(function=_callable_operator, *, kind: str = "theory") -> OperatorBinding:
    return OperatorBinding(
        operator_id="reflective-theory-synthesizer",
        version="1.0.0",
        kind=kind,
        function=function,
        validators=(ValidatorBinding("fixture-validator", "1.0.0", function=_validator),),
    )


def _request(workspace: Path, *, required: bool = True, kind: str = "theory") -> dict:
    namespace = Namespace("target-a", "run-a", "branch-a", 4)
    source = workspace / "inputs" / "theory.json"
    source.parent.mkdir(parents=True, exist_ok=True)
    source.write_text('{"theory":"A"}\n', encoding="utf-8")
    return build_operator_request(
        operator_id="reflective-theory-synthesizer",
        operator_version="1.0.0",
        kind=kind,
        namespace=namespace,
        invocation_id="invocation-0001",
        input_artifacts=[artifact_descriptor(source, workspace, namespace)],
        declared_outputs=["outputs/branch-a/synthesis.json"],
        parameters={"reflection_rounds": 3},
        required=required,
        requested_at="2026-07-21T10:00:00Z",
    )


def test_callable_dispatch_hashes_real_outputs_and_independent_validation(tmp_path: Path) -> None:
    request = _request(tmp_path)
    dispatcher = DiscoveryOperatorDispatcher(
        [_binding()], workspace=tmp_path, receipt_store=ReceiptStore(tmp_path / "receipts")
    )
    receipt = dispatcher.dispatch(request)
    assert receipt["status"] == "succeeded"
    assert receipt["input_digest"] == request["input_digest"]
    assert receipt["output_artifacts"][0]["sha256"].startswith("sha256:")
    assert receipt["validator_receipts"][0]["status"] == "passed"
    ensure_evaluation_ready([request], [receipt], workspace=tmp_path)


def test_subprocess_operator_and_validator_are_actually_executed(tmp_path: Path) -> None:
    request = _request(tmp_path)
    operator = tmp_path / "operator_runner.py"
    operator.write_text(
        "import json,pathlib,sys\nr=json.load(sys.stdin)\np=pathlib.Path(r['declared_outputs'][0])\np.parent.mkdir(parents=True,exist_ok=True)\np.write_text(json.dumps({'request_id':r['request_id']}))\nprint(json.dumps({'artifacts':[{'path':str(p)}],'explicit_unknowns':[]}))\n",
        encoding="utf-8",
    )
    validator = tmp_path / "validator.py"
    validator.write_text(
        "import json,sys,pathlib\np=json.load(sys.stdin)\na=p['artifacts'][0]\nr=json.loads(pathlib.Path(a['path']).read_text())\nraise SystemExit(0 if r['request_id']==p['request']['request_id'] else 1)\n",
        encoding="utf-8",
    )
    binding = OperatorBinding(
        "reflective-theory-synthesizer",
        "1.0.0",
        "theory",
        command=(sys.executable, str(operator)),
        validators=(ValidatorBinding("subprocess-validator", "1.0.0", command=(sys.executable, str(validator))),),
    )
    receipt = DiscoveryOperatorDispatcher(
        [binding], workspace=tmp_path, receipt_store=ReceiptStore(tmp_path / "receipts")
    ).dispatch(request)
    assert receipt["status"] == "succeeded"
    assert receipt["exit_code"] == 0


def test_failed_subprocess_receipt_keeps_bounded_sanitized_diagnostic(
    tmp_path: Path,
) -> None:
    request = _request(tmp_path)
    operator = tmp_path / "failing_operator.py"
    operator.write_text(
        "import sys\n"
        "sys.stderr.write('\\x1b[31mdiagnostic-marker\\x1b[0m\\n' + 'x' * 5000)\n"
        "raise SystemExit(7)\n",
        encoding="utf-8",
    )
    binding = OperatorBinding(
        "reflective-theory-synthesizer",
        "1.0.0",
        "theory",
        command=(sys.executable, str(operator)),
        validators=(ValidatorBinding("unused-validator", "1.0.0", function=_validator),),
    )
    receipt = DiscoveryOperatorDispatcher(
        [binding], workspace=tmp_path, receipt_store=ReceiptStore(tmp_path / "receipts")
    ).dispatch(request)

    assert receipt["status"] == "failed"
    assert receipt["exit_code"] == 7
    diagnostic = receipt["error"]["stderr_excerpt"]
    assert diagnostic.startswith("diagnostic-marker ")
    assert diagnostic.endswith("...[truncated]")
    assert len(diagnostic) <= 4096
    assert "\x1b" not in diagnostic and "\n" not in diagnostic
    validate_instance(receipt, "discovery_operator_receipt.schema.json")


def test_registry_binding_rejects_shell_text_and_missing_validator() -> None:
    registry = load_registry()
    experiment = next(
        row
        for row in registry["operators"]
        if row["operator_id"] == "dynamic-symbolic-simulation-experimenter"
    )
    assert experiment["output_schemas"] == [
        "agentic/spec/dynamic_experiment_receipt_v3.schema.json"
    ]
    reflection = registry["post_synthesis_artifacts"][0]
    assert reflection["producer"] == "canonical-discovery-cycle"
    assert len(reflection["required_inputs"]) == 5
    assert reflection["derivation_contract"]["advertised_as_operator_output"] is False
    assert reflection["schema"] not in experiment["output_schemas"]
    shell = json.loads(json.dumps(registry))
    shell["operators"][0]["command"] = ["sh", "-c", "echo fabricated"]
    with pytest.raises(ContractError, match="shell evaluation"):
        _bindings(shell)
    unvalidated = json.loads(json.dumps(registry))
    unvalidated["operators"][0]["validators"] = []
    with pytest.raises(ContractError, match="independent validators"):
        _bindings(unvalidated)


def test_descendant_producer_is_typed_only_and_legacy_exports_fail_closed() -> None:
    registry = load_registry()
    route = registry["canonical_descendant_experiment_route"]
    assert route["production_status"] == "active_typed_python_api"
    assert route["generic_dispatch_enabled"] is False
    assert route["operator_registry_member"] is False
    assert route["replay_is_producer"] is False
    assert route["replay_command"][2] == (
        "agentic.scripts.validate_world_v3_descendant_chain"
    )
    assert route["route_id"] not in {
        row["operator_id"] for row in registry["operators"]
    }
    assert callable(experiments.run_canonical_descendant_experiment_v3)

    legacy_calls = (
        experiments.compile_experiment_spec,
        experiments.execute_experiment,
        experiments.reexecute_v2_experiment,
        experiments.run_canonical_theory_support_lane,
        experiments.run_canonical_world_support_production,
        experiments.production_causal_operator_binding,
        experiments.CausalArtifactProducerRuntime,
    )
    for call in legacy_calls:
        with pytest.raises(
            ExperimentMigrationRequired, match="history_only_execution_route"
        ):
            call()


def test_central_conceptual_route_is_registered_as_one_typed_facade() -> None:
    registry = load_registry()
    route = registry["canonical_central_conceptual_route"]
    assert route["route_id"] == "central-formal-conceptual-routes-v3"
    assert route["production_status"] == "active_typed_python_api"
    assert route["invocation_mode"] == (
        "typed_python_facade_with_live_store_verified_commit_and_process_wave"
    )
    assert route["generic_dispatch_enabled"] is False
    assert route["operator_registry_member"] is False
    assert route["serializable_cli_available"] is False
    assert route["matched_route_order"] == [
        "categorical",
        "hott",
        "category_then_hott",
        "hott_then_category",
        "capable_nonformal",
    ]
    assert route["central_reflection_intake"] == {
        "source_generation_role": "canonical_input_head_n",
        "descendant_effect_generation_offset": 1,
        "canonical_compare_and_swap_required": True,
        "same_generation_effect_authorized": False,
    }
    assert route["route_id"] not in {
        row["operator_id"] for row in registry["operators"]
    }
    typed_routes = typed_facade_routes_from_registry(registry)
    assert typed_routes[route["route_id"]] is route
    assert route["route_id"] not in {
        binding.operator_id for binding in _bindings(registry)
    }

    for field in (
        "python_api",
        "structural_packet_validator",
        "active_current_validator",
        "route_registry_loader",
    ):
        module_name, symbol = route[field].split(":", maxsplit=1)
        assert callable(getattr(importlib.import_module(module_name), symbol))
    assert callable(discovery.run_central_conceptual_routes)
    assert callable(discovery.decode_central_conceptual_route_packet)
    assert callable(
        discovery.reopen_authoritative_central_conceptual_route_packet
    )

    registry_loader_module, registry_loader_symbol = route[
        "route_registry_loader"
    ].split(":", maxsplit=1)
    route_registry, _ = getattr(
        importlib.import_module(registry_loader_module),
        registry_loader_symbol,
    )()
    assert [
        row["route_id"] for row in route_registry["routes"]
    ] == route["matched_route_order"]
    assert route_registry["authority_boundary"] == route["authority_boundary"]


def test_central_conceptual_route_rejects_validator_and_authority_drift(
    tmp_path: Path,
) -> None:
    registry = load_registry()
    for index, mutation in enumerate(
        (
            lambda route: route.__setitem__(
                "active_current_validator",
                "agentic.discovery:decode_central_conceptual_route_packet",
            ),
            lambda route: route["authority_boundary"].__setitem__(
                "conceptual_merit_authorized", True
            ),
        )
    ):
        drifted = json.loads(json.dumps(registry))
        mutation(drifted["canonical_central_conceptual_route"])
        path = tmp_path / f"drifted-central-route-{index}.json"
        path.write_text(json.dumps(drifted), encoding="utf-8")
        with pytest.raises(
            ValueError,
            match="canonical central conceptual typed facade",
        ):
            load_registry(path)


@pytest.mark.parametrize(
    ("route_key", "label"),
    [
        ("canonical_central_conceptual_route", "central conceptual"),
        ("canonical_descendant_experiment_route", "descendant"),
    ],
)
def test_generic_dispatcher_rejects_typed_facade_rebinding(
    route_key: str, label: str
) -> None:
    registry = load_registry()
    rebound = json.loads(json.dumps(registry))
    row = json.loads(json.dumps(rebound["operators"][0]))
    row["operator_id"] = rebound[route_key]["route_id"]
    rebound["operators"].append(row)
    with pytest.raises(
        ContractError,
        match=f"typed canonical {label} facade cannot be bound",
    ):
        _bindings(rebound)


@pytest.mark.parametrize(
    ("mutate", "expected"),
    [
        (
            lambda registry: registry["operators"][-1]["output_schemas"].append(
                "agentic/spec/dynamic_experiment_reflection_receipt_v1.schema.json"
            ),
            "must advertise exactly its v3 receipt output",
        ),
        (
            lambda registry: registry["post_synthesis_artifacts"][0][
                "required_inputs"
            ].pop(),
            "exact five causal inputs",
        ),
        (
            lambda registry: registry["post_synthesis_artifacts"][0][
                "authority_boundary"
            ].__setitem__("theory_selected", True),
            "forbidden theory authority",
        ),
        (
            lambda registry: registry["post_synthesis_artifacts"][0][
                "dependency_paths"
            ].remove("agentic/experiments/reflection.py"),
            "semantic closure is incomplete",
        ),
    ],
)
def test_registry_rejects_post_synthesis_reflection_contract_drift(
    tmp_path: Path, mutate, expected: str
) -> None:
    registry = load_registry()
    mutate(registry)
    path = tmp_path / "registry.json"
    path.write_text(json.dumps(registry), encoding="utf-8")
    with pytest.raises(ValueError, match=expected):
        load_registry(path)


def _current_authority_fixture(tmp_path: Path) -> tuple[ValidatorBinding, dict, Path]:
    """Build a portable copy of one production validator's declared closure."""

    binding = _bindings(load_registry())[0].validators[0]
    authority, _, _ = _validator_authority_material(binding, tmp_path)
    repository = tmp_path / "repository"
    for row in authority["files"]:
        if row["path_scope"] != "repository_relative":
            continue
        source = ROOT / row["runtime_path"]
        destination = repository / row["runtime_path"]
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, destination)
    verify_current_validator_authority(
        authority, binding, repository_root=repository
    )
    return binding, authority, repository


@pytest.mark.parametrize("failure_mode", ["mutation", "deletion"])
def test_current_validator_authority_rejects_dependency_byte_drift(
    tmp_path: Path, failure_mode: str
) -> None:
    binding, authority, repository = _current_authority_fixture(tmp_path)
    dependency = repository / "agentic/discovery/contracts.py"
    if failure_mode == "mutation":
        dependency.write_bytes(dependency.read_bytes() + b"\n# authority mutation\n")
        message = "differs from sealed authority"
    else:
        dependency.unlink()
        message = "dependency is missing"
    with pytest.raises(ContractError, match=message):
        verify_current_validator_authority(
            authority, binding, repository_root=repository
        )


@pytest.mark.parametrize("failure_mode", ["extra", "duplicate"])
def test_current_validator_authority_requires_an_exact_dependency_bijection(
    tmp_path: Path, failure_mode: str
) -> None:
    binding, authority, repository = _current_authority_fixture(tmp_path)
    changed = json.loads(json.dumps(authority))
    row = dict(
        next(
            item
            for item in changed["files"]
            if item["path_scope"] == "repository_relative"
        )
    )
    if failure_mode == "extra":
        row["path_scope"] = "repository_relative"
        row["runtime_path"] = "agentic/spec/canonical_discovery_cycle.schema.json"
    changed["files"].append(row)
    with pytest.raises(ContractError, match="repeats local path|differs from registry"):
        verify_current_validator_authority(
            changed, binding, repository_root=repository
        )


@pytest.mark.parametrize(
    ("field", "expected"),
    [
        ("validator_id", "approved registry binding"),
        ("version", "approved registry binding"),
        ("argv", "command differs"),
        ("entry_module", "entry module differs"),
        ("missing_dependency", "closure differs from registry"),
    ],
)
def test_current_validator_authority_rejects_registry_identity_drift(
    tmp_path: Path, field: str, expected: str
) -> None:
    binding, authority, repository = _current_authority_fixture(tmp_path)
    changed_authority = json.loads(json.dumps(authority))
    changed_binding = binding
    if field == "validator_id":
        changed_binding = dataclasses.replace(binding, validator_id="different-validator")
    elif field == "version":
        changed_binding = dataclasses.replace(binding, version="9.9.9")
    elif field == "argv":
        changed_binding = dataclasses.replace(binding, command=(*binding.command, "--changed"))
    elif field == "entry_module":
        changed_authority["runtime_identity"]["entry_module"] = "agentic.scripts.other"
    elif field == "missing_dependency":
        changed_binding = dataclasses.replace(
            binding, dependency_paths=binding.dependency_paths[:-1]
        )
    with pytest.raises(ContractError, match=expected):
        verify_current_validator_authority(
            changed_authority, changed_binding, repository_root=repository
        )


@pytest.mark.parametrize(
    ("dependency_paths", "expected"),
    [
        (["../agentic/discovery/contracts.py"], "unsafe path"),
        (["agentic/discovery/contracts.py"] * 2, "duplicate paths"),
        (["agentic/discovery/does_not_exist.py"], "does not exist"),
    ],
)
def test_registry_rejects_traversal_duplicate_and_missing_dependencies(
    tmp_path: Path, dependency_paths: list[str], expected: str
) -> None:
    registry = load_registry()
    registry["operators"][0]["validators"][0]["dependency_paths"] = dependency_paths
    path = tmp_path / "registry.json"
    path.write_text(json.dumps(registry), encoding="utf-8")
    with pytest.raises(ValueError, match=expected):
        load_registry(path)


def test_batch_receipts_cannot_escape_caller_workspace(tmp_path: Path) -> None:
    with pytest.raises(ContractError, match="receipt root must remain"):
        dispatch_request_batch(
            [],
            load_registry(),
            workspace=tmp_path,
            receipt_root=tmp_path.parent / "outside-route-receipts",
        )


def test_disabled_required_operator_blocks_instead_of_claiming_skip(tmp_path: Path) -> None:
    request = _request(tmp_path)
    dispatcher = DiscoveryOperatorDispatcher(
        [_binding()], workspace=tmp_path, receipt_store=ReceiptStore(tmp_path / "receipts")
    )
    receipt = dispatcher.dispatch(request, skip_reason="operator disabled by policy")
    assert receipt["status"] == "failed"
    with pytest.raises(DispatchBlocked, match="no successful receipt"):
        ensure_evaluation_ready([request], [receipt], workspace=tmp_path)


def test_optional_operator_may_be_justifiably_skipped(tmp_path: Path) -> None:
    request = _request(tmp_path, required=False)
    receipt = DiscoveryOperatorDispatcher(
        [_binding()], workspace=tmp_path, receipt_store=ReceiptStore(tmp_path / "receipts")
    ).dispatch(request, skip_reason="theory did not request a support probe")
    assert receipt["status"] == "skipped"
    assert receipt["explicit_unknowns"] == ["theory did not request a support probe"]
    ensure_evaluation_ready([request], [receipt], workspace=tmp_path)


def test_fake_operator_name_cannot_satisfy_dispatch(tmp_path: Path) -> None:
    request = _request(tmp_path)
    request["operator"]["operator_id"] = "invented-skill-name"
    request["input_digest"] = canonical_digest(
        {
            "identity": request["identity"],
            "operator": request["operator"],
            "parameters": request["parameters"],
            "input_artifacts": request["input_artifacts"],
            "declared_outputs": request["declared_outputs"],
        }
    )
    request["request_digest"] = request_content_digest(request)
    request["request_id"] = stable_identifier("opreq", request["request_digest"])
    receipt = DiscoveryOperatorDispatcher(
        [_binding()], workspace=tmp_path, receipt_store=ReceiptStore(tmp_path / "receipts")
    ).dispatch(request)
    assert receipt["status"] == "failed"
    assert "not executable/registered" in receipt["error"]["message"]


def test_unbound_output_path_and_failed_validator_are_failures(tmp_path: Path) -> None:
    request = _request(tmp_path)

    def rogue(req: dict, workspace: Path) -> dict:
        path = workspace / "outputs" / "branch-a" / "rogue.json"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("{}", encoding="utf-8")
        return {"artifacts": [{"path": "outputs/branch-a/rogue.json"}]}

    receipt = DiscoveryOperatorDispatcher(
        [_binding(rogue)], workspace=tmp_path, receipt_store=ReceiptStore(tmp_path / "receipts")
    ).dispatch(request)
    assert receipt["status"] == "failed"
    assert receipt["output_artifacts"] == []

    request2 = _request(tmp_path)
    bad_validator = ValidatorBinding("bad-validator", "1.0.0", function=lambda *_: False)
    binding = OperatorBinding(
        "reflective-theory-synthesizer",
        "1.0.0",
        "theory",
        function=_callable_operator,
        validators=(bad_validator,),
    )
    receipt2 = DiscoveryOperatorDispatcher(
        [binding], workspace=tmp_path, receipt_store=ReceiptStore(tmp_path / "receipts-2")
    ).dispatch(request2)
    assert receipt2["status"] == "failed"
    assert receipt2["validator_receipts"][0]["status"] == "failed"


def test_tampered_input_or_consumed_output_blocks_evaluation(tmp_path: Path) -> None:
    request = _request(tmp_path)
    dispatcher = DiscoveryOperatorDispatcher(
        [_binding()], workspace=tmp_path, receipt_store=ReceiptStore(tmp_path / "receipts")
    )
    receipt = dispatcher.dispatch(request)
    # Mutable presentation paths are not authority after dispatch; the exact
    # attempt-local history is.  Replacing the former cannot rewrite history.
    (tmp_path / receipt["output_artifacts"][0]["path"]).write_text("tampered", encoding="utf-8")
    ensure_evaluation_ready([request], [receipt], workspace=tmp_path)
    (tmp_path / receipt["output_history_artifacts"][0]["path"]).write_text(
        "tampered", encoding="utf-8"
    )
    with pytest.raises(DispatchBlocked, match="digest mismatch"):
        ensure_evaluation_ready([request], [receipt], workspace=tmp_path)


def test_retry_preserves_unique_output_history_and_validator_authority(tmp_path: Path) -> None:
    request = _request(tmp_path)
    calls = 0

    def changing(req: dict, workspace: Path) -> dict:
        nonlocal calls
        calls += 1
        path = workspace / req["declared_outputs"][0]
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps({"request_id": req["request_id"], "attempt_value": calls}))
        return {"artifacts": [{"path": req["declared_outputs"][0]}]}

    dispatcher = DiscoveryOperatorDispatcher(
        [_binding(changing)],
        workspace=tmp_path,
        receipt_store=ReceiptStore(tmp_path / "receipts"),
    )
    first = dispatcher.dispatch(request, attempt=1)
    second = dispatcher.dispatch(request, attempt=2)
    assert first["output_artifacts"][0]["path"] == second["output_artifacts"][0]["path"]
    assert first["output_history_artifacts"][0]["path"] != second["output_history_artifacts"][0]["path"]
    assert json.loads((tmp_path / first["output_history_artifacts"][0]["path"]).read_text())["attempt_value"] == 1
    assert json.loads((tmp_path / second["output_history_artifacts"][0]["path"]).read_text())["attempt_value"] == 2
    authority = second["validator_receipts"][0]["validator_authority"]
    assert authority["authority_digest"] == second["validator_receipts"][0]["validator_code_digest"]
    assert (
        "undeclared transitive imports beyond explicit dependency paths"
        in authority["coverage"]["excluded"]
    )
    assert authority["files"] and all(row["snapshot_descriptor"] for row in authority["files"])


def test_generic_receipt_rejects_declared_only_import_overclaim(
    tmp_path: Path,
) -> None:
    """Generic receipt replay must apply the same import ceiling as theory gate."""

    request = _request(tmp_path)
    receipt = DiscoveryOperatorDispatcher(
        [_binding()],
        workspace=tmp_path,
        receipt_store=ReceiptStore(tmp_path / "receipts"),
    ).dispatch(request)
    validator = receipt["validator_receipts"][0]
    authority = validator["validator_authority"]
    authority["coverage"]["excluded"].remove(
        "undeclared transitive imports beyond explicit dependency paths"
    )
    authority["authority_digest"] = canonical_digest(
        authority, exclude_keys=("authority_digest",)
    )
    validator["validator_code_digest"] = authority["authority_digest"]
    validator["receipt_digest"] = canonical_digest(
        validator, exclude_keys=("receipt_digest",)
    )
    receipt["receipt_id"] = stable_identifier(
        "opreceipt",
        receipt["request_id"],
        receipt["attempt"],
        canonical_digest(
            {
                key: value
                for key, value in receipt.items()
                if key not in {"receipt_id", "receipt_digest"}
            }
        ),
    )
    receipt["receipt_digest"] = canonical_digest(
        {
            key: value
            for key, value in receipt.items()
            if key != "receipt_digest"
        }
    )

    with pytest.raises(ContractError, match="overclaims undeclared imports"):
        validate_operator_receipt_identity(receipt, request)


def test_every_parallel_attempt_receives_an_independent_receipt(tmp_path: Path) -> None:
    requests = []
    bindings = []
    for index in range(3):
        branch = f"branch-{index}"
        namespace = Namespace("target-a", "run-a", branch, 1)
        source = tmp_path / "inputs" / f"{branch}.json"
        source.parent.mkdir(parents=True, exist_ok=True)
        source.write_text("{}", encoding="utf-8")
        request = build_operator_request(
            operator_id=f"worker-{index}", operator_version="1.0.0", kind="hypothesis",
            namespace=namespace, invocation_id=f"invocation-{index}",
            input_artifacts=[artifact_descriptor(source, tmp_path, namespace)],
            declared_outputs=[f"outputs/{branch}/result.json"], required=True,
        )
        requests.append(request)

        def worker(req: dict, workspace: Path, *, fail=index == 1) -> dict:
            if fail:
                raise RuntimeError("branch-local failure")
            path = workspace / req["declared_outputs"][0]
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(json.dumps({"request_id": req["request_id"]}), encoding="utf-8")
            return {"artifacts": [{"path": req["declared_outputs"][0]}], "explicit_unknowns": []}

        bindings.append(
            OperatorBinding(
                f"worker-{index}", "1.0.0", "hypothesis", function=worker,
                validators=(ValidatorBinding(f"validator-{index}", "1.0.0", function=_validator),),
            )
        )
    receipts = DiscoveryOperatorDispatcher(
        bindings, workspace=tmp_path, receipt_store=ReceiptStore(tmp_path / "receipts")
    ).dispatch_many(requests)
    assert [receipt["status"] for receipt in receipts] == ["succeeded", "failed", "succeeded"]
    assert all(ReceiptStore(tmp_path / "receipts").path_for(receipt).exists() for receipt in receipts)
    assert all(receipt["identity"]["branch_id"] == f"branch-{index}" for index, receipt in enumerate(receipts))


def test_literature_receipt_requires_actual_search_provenance(tmp_path: Path) -> None:
    request = _request(tmp_path, kind="literature_search")
    request["operator"]["operator_id"] = "reflective-theory-synthesizer"

    def searched(req: dict, workspace: Path) -> dict:
        result = _callable_operator(req, workspace)
        result["search_provenance"] = {
            "queries": ["conceptual unification P versus NP 2026"],
            "providers": ["Crossref", "arXiv"],
            "completed_at": "2026-07-21T10:05:00Z",
            "coverage_cutoff": "2026-07-21T00:00:00Z",
            "inclusion_policy": "peer reviewed or primary preprint; target-specific claims only",
            "source_count": 3,
            "content_digest": canonical_digest(["doi:1", "arxiv:2", "doi:3"]),
        }
        return result

    receipt = DiscoveryOperatorDispatcher(
        [_binding(searched, kind="literature_search")],
        workspace=tmp_path,
        receipt_store=ReceiptStore(tmp_path / "receipts"),
    ).dispatch(request)
    assert receipt["status"] == "succeeded"
    assert receipt["search_provenance"]["source_count"] == 3

    request2 = _request(tmp_path, kind="literature_search")
    failed = DiscoveryOperatorDispatcher(
        [_binding(_callable_operator, kind="literature_search")],
        workspace=tmp_path,
        receipt_store=ReceiptStore(tmp_path / "receipts-2"),
    ).dispatch(request2)
    assert failed["status"] == "failed"


def _literature_envelope(snapshot: dict) -> dict:
    """Return complete claim-level mappings for one already frozen snapshot."""

    mappings = []
    for index, source in enumerate(snapshot["sources"]):
        mappings.append(
            {
                "source_id": source["source_id"],
                "theory_object_ids": [f"concept-{index}"],
                "object_kinds": ["concept", "schedule"],
                "relation": "reframes" if index == 0 else "leaves_open",
                "exact_claim": source["claims"][0],
                "source_limitation": source["limitations"][0],
                "conceptual_change": (
                    "Open a relation-first conceptual branch."
                    if index == 0
                    else "Justified no change in this disjoint fixture regime."
                ),
                "event_type": "spawn" if index == 0 else "justified_no_change",
                "coverage_limits": list(snapshot["coverage_limits"]),
                "confidence": "medium",
            }
        )
    return {"snapshot": snapshot, "theory_mappings": mappings}


def _local_literature_envelope(target_id: str) -> tuple[dict, dict]:
    """Return a frozen local-only snapshot and complete claim-level mappings."""

    snapshot = build_demo_literature_snapshot(target_id=target_id)
    return snapshot, _literature_envelope(snapshot)


def _executed_provider_snapshot(target_id: str) -> dict:
    """Build a current fixture snapshot through six actually invoked provider adapters."""

    theory_digest = canonical_digest({"target": target_id, "state": 7})
    request = {
        "target_id": target_id,
        "claim_scope": "route execution fixture",
        "theory_state_digest": theory_digest,
        "coverage_cutoff": "2026-07-21T00:00:00Z",
        "coverage_limits": ["Only the six exact fixture provider lanes were executed."],
        "search_lanes": [
            {
                "lane_type": lane_type,
                "queries": [f"{target_id} exact {lane_type}"],
                "inclusion_policy": "Include the exact target-scoped fixture record.",
                "exclusion_policy": "Exclude target mismatch and duplicate versions.",
            }
            for lane_type in LANE_TYPES
        ],
    }
    providers = {}
    for index, lane_type in enumerate(LANE_TYPES):

        def provider(_request: dict, *, index: int = index, lane_type: str = lane_type) -> dict:
            return {
                "provider": f"executed-fixture-{lane_type}",
                "index": f"fixture-index-{lane_type}",
                "execution_mode": "live",
                "status": "completed",
                "coverage_cutoff": "2026-07-21T00:00:00Z",
                "sources": [
                    {
                        "work_identity": f"route-work-{index}",
                        "title": f"Route source {index}",
                        "authors": [f"Route Author {index}"],
                        "publication_date": f"202{index}",
                        "source_version": "v1",
                        "source_type": "primary",
                        "url": f"https://example.test/route/{index}",
                        "correction_status": "none_known",
                        "decision_relevant": True,
                        "claims": [f"Exact route claim {index}."],
                        "limitations": [f"Fixture regime {index} only."],
                    }
                ],
            }

        providers[lane_type] = provider
    return run_frontier_literature_cycle(request, providers=providers)


def _reflective_route_request(target_id: str, run_id: str, state_version: int) -> dict:
    """Build an explicit conceptual fixture independent of the local-only literature route."""

    corners = [
        "ontology_inversion",
        "missing_mediator",
        "relation_first",
        "scale_reversal",
        "cross_field_transfer",
        "unification_conjecture",
        "negative_theory",
        "counter_consensus",
    ]
    hypotheses = []
    for index, corner in enumerate(corners):
        hypotheses.append(
            {
                "hypothesis_id": f"route-hypothesis.{index}",
                "corner_family": corner,
                "concept_lifecycle_state": "literature_rebased",
                "maturation_status": "parallel_ready",
                "truth_status": "conjectural",
                "intuitive_leap": f"Treat pressure {index} through {corner}.",
                "new_primitives_relations_or_mechanisms": [
                    f"route-primitive-{index}",
                    f"route-relation-{index}",
                ],
                "target_pressures_addressed": [
                    f"route-pressure-{index}",
                    "shared-root-pressure",
                ],
                "protected_successes": ["preserve the exact target"],
                "assumptions_or_invariants_risked": [f"assumption-{index}"],
                "explanatory_upside": f"Expose hidden dependence {index}.",
                "unification_upside": f"Relate pressure {index} to the common root.",
                "value_if_right": f"Reorganize route family {index}.",
                "learning_value_if_wrong": f"Eliminate mechanism family {index}.",
                "probability_status": "open",
                "conceptual_distance": f"Change primitive family {index}.",
                "literature_relation": "apparently_open",
                "literature_source_ids": [f"external-source.{index}"],
                "non_claim_boundary": "This seed is neither a proof nor a novelty claim.",
                "maturation_question": f"Which invariant makes mechanism {index} non-vacuous?",
                "correction_conditions": [f"Retire if witness {index} collapses to the incumbent."],
                "boundary_case": f"Boundary {index} must preserve the exact target.",
                "branch_independence_signature": {
                    "unique_primitives": [f"route-primitive-{index}"],
                    "unique_mechanism": f"route-mechanism-{index}",
                    "forbidden_cross_branch_context": ["sibling conclusions during blind divergence"],
                    "overlaps_with_hypothesis_ids": [],
                },
            }
        )
    return {
        "target_id": target_id,
        "run_id": run_id,
        "branch_id": "root",
        "state_version": state_version,
        "discovery_charter": {
            "essential_question": "What relation explains the recurring obstruction without weakening the target?",
            "desired_understanding": "Explain recurrent route failures while preserving their differences.",
            "bottleneck_diagnosis": "conceptual",
            "bottleneck_evidence": "Several mature routes fail at the same unrepresented interface.",
            "target_commitments": ["preserve the exact target"],
            "relevance_horizon": "A successful concept would reorganize several essential routes.",
            "incumbent_framework": "object-first local decomposition",
            "conceptual_opacity": "The common obstruction has no explicit relational carrier.",
            "non_claim_boundary": "No theorem, empirical law, or novelty is established.",
        },
        "conceptual_genealogy": {
            "inherited_concepts": ["local route", "witness", "barrier"],
            "historical_or_logical_formation": ["Local decomposition made route failures primary."],
            "protected_successes": ["exact target"],
            "rejected_or_retired_ancestors": ["universal bridge"],
            "hidden_assumptions": ["local objects are the primary explanatory units"],
        },
        # This explicitly represents a separately validated external search. It
        # is not derived from the static local-only assimilation fixture above.
        "literature_basis": {
            "selected_snapshot_id": "external-search.route-current",
            "snapshot_target_id": target_id,
            "selected_snapshot_digest": canonical_digest({"external_search_fixture": target_id}),
            "search_completed_utc": "2026-07-21T10:00:00Z",
            "freshness_status": "current",
            "search_receipt_ids": ["external-search-receipt.route-1"],
            "assimilation_packet_ref": "external/assimilation/route-1.json",
            "source_to_theory_delta_summary": ["A source reframed the barrier as a carrier mismatch."],
            "literature_generated_questions": ["Can a carrier preserve regime differences?"],
            "coverage_limitations": ["This is an executable contract fixture, not a recency claim."],
            "superseded_snapshot_ids": [],
        },
        "root_tensions": [
            {
                "tension_id": "tension.route",
                "opposed_commitments": ["route-local distinction", "global recurrence"],
                "strongest_form_of_each_side": ["Formal objects differ.", "The failure relation recurs."],
                "minimal_incompatibility_or_missing_mediation": "No carrier preserves both.",
                "regime": "all essential routes",
                "why_root_level": "The missing relation blocks explanation before proof work.",
            }
        ],
        "high_risk_portfolio": {
            "portfolio_id": "route-reflective-portfolio",
            "hypotheses": hypotheses,
            "selected_hypothesis_ids": [item["hypothesis_id"] for item in hypotheses],
            "protected_wildcard_ids": ["route-hypothesis.0", "route-hypothesis.1"],
            "control_hypothesis_ids": ["route-hypothesis.7"],
        },
        "explicit_unknowns": ["Whether the proposed relation admits a nontrivial formal model."],
    }


def _experiment_envelope(target_id: str, run_id: str, state_version: int) -> dict:
    """Build one mature, exact, theory-commissioned support probe."""

    programme_digest = canonical_digest({"programme_id": "route-theory-programme"})
    reflection_digest = canonical_digest({"packet_id": "route-reflection-packet"})
    claim = {
        "claim_id": "route-exact-question",
        "claim_kind": "model_consequence",
        "target_relation": "toy_or_proxy",
        "statement": "Does the exact finite invariant equal the proposed value?",
        "theory_programme_id": "route-theory-programme",
        "conceptual_system_ids": ["route-conceptual-system"],
        "source_theory_programme_digest": programme_digest,
        "source_reflection_packet_digest": reflection_digest,
    }
    claim["claim_digest"] = canonical_digest(claim)
    envelope = {
        "triage_request": {
            "target_id": target_id,
            "theory_programme_id": "route-theory-programme",
            "source_theory_programme_digest": programme_digest,
            "source_reflection_packet_digest": reflection_digest,
            "conceptual_system_ids": ["route-conceptual-system"],
            "registered_theory_claims": [claim],
            "theoretical_question_id": "route-exact-question",
            "question": "Does the exact finite invariant equal the proposed value?",
            "programme_maturity": "mature",
            "probe_role": "discriminator",
            "decision_effect": {
                "if_supported": "retain the invariant mechanism",
                "if_not_supported": "revise the invariant mechanism",
            },
            "expected_conceptual_change": "decide whether the invariant is primitive or derived",
            "theory_generated_justification": "reflection isolated the equality as a discriminator",
            "candidate_methods": ["exact"],
            "state_version": state_version,
        },
        "experiment_request": {
            "run_id": run_id,
            "branch_id": "root",
            "adapter": "exact",
            "model": {"operation": "equality", "left": "1/3 + 1/6", "right": "1/2"},
            "preregistration": {
                "hypothesis": "the declared exact equality holds",
                "decision_rule": {"comparator": "==", "threshold": 1},
                "stopping_rule": "stop after the declared exact evaluation",
                "analysis_plan": "evaluate the frozen expression and apply the decision rule",
                "registered_at": "2026-07-21T10:00:00Z",
            },
            "controls": [
                {
                    "control_id": "route-control",
                    "variable": "arithmetic_domain",
                    "value": "rational",
                    "role": "held_fixed",
                }
            ],
            "seed_policy": {"stochastic": False, "policy": "not_applicable"},
            "resource_budget": {
                "budget_id": "route-probe-budget",
                "wall_time_seconds": 5.0,
                "grace_period_seconds": 0.1,
                "cpu_seconds": 2.0,
                "memory_bytes": 268435456,
                "disk_bytes": 8388608,
                "network_bytes": 0,
                "token_count": 0,
                "request_count": 0,
                "cost_usd": 0.0,
            },
            "transfer_boundary": "The certificate applies only to the declared exact expression.",
        },
    }
    triage = triage_probe(envelope["triage_request"])
    assert triage["decision"] == "commission"
    envelope["experiment_spec"] = compile_experiment_spec(
        triage,
        envelope["experiment_request"],
    )
    return envelope


def test_parallel_route_blocks_local_only_hypothesis_investment(tmp_path: Path) -> None:
    registry = load_registry()
    namespace = Namespace("local-route-target", "local-route-run", "root", 2)
    local_snapshot = build_demo_literature_snapshot(target_id=namespace.target_id)
    local_portfolio = build_demo_high_risk_portfolio(local_snapshot)
    envelope_path = tmp_path / "inputs/local-parallel.json"
    envelope_path.parent.mkdir(parents=True, exist_ok=True)
    envelope_path.write_text(
        json.dumps({"high_risk_portfolio": local_portfolio}, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    request = build_operator_request(
        operator_id="parallel-hypothesis-portfolio",
        operator_version="1.0.0",
        kind="hypothesis",
        namespace=namespace,
        invocation_id="local-parallel-block",
        input_artifacts=[artifact_descriptor(envelope_path, tmp_path, namespace)],
        declared_outputs=["outputs/local-parallel.json"],
        required=True,
        requested_at="2026-07-21T10:00:00Z",
    )
    binding = next(
        item for item in _bindings(registry) if item.operator_id == "parallel-hypothesis-portfolio"
    )
    rejected = subprocess.run(
        binding.command,
        cwd=tmp_path,
        input=json.dumps(request).encode(),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    assert rejected.returncode == 2
    assert b"completed, non-local literature rebase" in rejected.stderr
    receipts, _ = dispatch_request_batch(
        [request],
        registry,
        workspace=tmp_path,
        receipt_root=tmp_path / "receipts",
    )
    assert receipts[0]["status"] == "failed"
    assert receipts[0]["exit_code"] == 2


def test_generic_registered_routes_execute_validate_and_emit_receipts(tmp_path: Path) -> None:
    """Exercise every standalone route; formal compilation is lineage-bound."""

    registry = load_registry()
    operator_ids = [row["operator_id"] for row in registry["operators"]]
    dispatchable_operator_ids = {
        row["operator_id"]
        for row in registry["operators"]
        if row.get("dispatch_enabled", True)
    }
    lineage_bound_operator_ids = {"formal-claim-producer"}
    standalone_operator_ids = dispatchable_operator_ids - lineage_bound_operator_ids
    assert lineage_bound_operator_ids <= dispatchable_operator_ids
    routes_doc = ROOT / "docs/research-methods/discovery-operator-routes.md"
    assert routes_doc.read_text(encoding="utf-8") == render_routes(registry)
    assert all(f"## {operator_id}" in routes_doc.read_text(encoding="utf-8") for operator_id in operator_ids)
    namespace = Namespace("route-target", "route-run", "root", 7)
    receipts = []
    requests = []

    def run(
        operator_id: str,
        kind: str,
        envelope: dict | None,
        output_name: str,
        parameters: dict,
    ) -> dict:
        index = len(receipts)
        invocation_id = f"route-invocation-{index}"
        input_artifacts = []
        if envelope is not None:
            input_path = tmp_path / "inputs" / f"{index}-{operator_id}.json"
            input_path.parent.mkdir(parents=True, exist_ok=True)
            input_path.write_text(
                json.dumps(envelope, indent=2, sort_keys=True) + "\n",
                encoding="utf-8",
            )
            input_artifacts = [artifact_descriptor(input_path, tmp_path, namespace)]
        declared_output = (
            f".canonical-causal-evidence/{namespace.target_id}/{namespace.run_id}/"
            f"{namespace.branch_id}/state-{namespace.state_version}/artifacts/"
            f"{invocation_id}.json"
            if operator_id == "canonical-causal-artifact-producer"
            else f"outputs/{index}-{output_name}.json"
        )
        request = build_operator_request(
            operator_id=operator_id,
            operator_version=next(
                row["version"]
                for row in registry["operators"]
                if row["operator_id"] == operator_id
            ),
            kind=kind,
            namespace=namespace,
            invocation_id=invocation_id,
            input_artifacts=input_artifacts,
            declared_outputs=[declared_output],
            parameters=parameters,
            required=True,
            requested_at="2026-07-21T10:00:00Z",
        )
        requests.append(request)
        batch_receipts, batch_manifest = dispatch_request_batch(
            [request],
            registry,
            workspace=tmp_path,
            receipt_root=tmp_path / "receipts",
        )
        receipt = batch_receipts[0]
        assert batch_manifest["feedback_committed"] is False
        validate_instance(receipt, "discovery_operator_receipt.schema.json")
        assert receipt["status"] == "succeeded", receipt.get("error")
        assert receipt["validator_receipts"] and all(
            item["status"] == "passed" for item in receipt["validator_receipts"]
        )
        receipts.append(receipt)
        return json.loads((tmp_path / receipt["output_artifacts"][0]["path"]).read_text(encoding="utf-8"))

    current_snapshot = _executed_provider_snapshot(namespace.target_id)
    literature_envelope = _literature_envelope(current_snapshot)
    assimilation = run(
        "frontier-literature-assimilator",
        "literature_assimilation",
        literature_envelope,
        "assimilation",
        {},
    )
    assert assimilation["selected_snapshot"]["provenance_mode"] == "live"
    assert assimilation["resolution"]["active_investment_gate"] == "pass"
    assert assimilation["hypothesis_rebase_status"] == "current"

    charter = {
        "target_id": namespace.target_id,
        "target_statement": "Explain the exact target pressure without replacing it by an easier proxy.",
        "theory_state_digest": current_snapshot["theory_state_digest"],
        "root_tensions": ["Local witnesses do not explain global recurrence."],
        "target_commitments": ["Preserve the exact target and quantifier order."],
        "protected_successes": ["Recover verified boundary cases."],
        "forbidden_target_drift": "Do not substitute a finite-only or average-case proxy.",
    }
    portfolio = run(
        "high-risk-hypothesis-forger",
        "hypothesis",
        {
            "charter": charter,
            "literature_snapshot": current_snapshot,
            "assimilation_packet": assimilation,
        },
        "high-risk-portfolio",
        {"requested_count": 10, "relevance_floor": 0.70},
    )
    assert len(portfolio["hypotheses"]) == 10
    assert all(
        item["literature_rebase_receipt"]["status"] == "completed"
        for item in portfolio["hypotheses"]
    )

    parallel = run(
        "parallel-hypothesis-portfolio",
        "hypothesis",
        {
            "high_risk_portfolio": portfolio,
            "branch_seeds": portfolio["parallel_branch_seeds"][:3],
            "dissent_branch_ids": [portfolio["parallel_branch_seeds"][2]["branch_id"]],
            "resource_budget": {
                "wall_seconds": 20,
                "max_workers": 3,
                "cost_units": 12,
                "storage_bytes": 100000,
                "matched_budget_baseline_corner_coverage": 1,
            },
        },
        "parallel-portfolio",
        {},
    )
    assert len(parallel["attempt_receipts"]) == 3

    reflective_input = _reflective_route_request(
        namespace.target_id, namespace.run_id, namespace.state_version
    )
    reflective_preview = build_reflective_discovery_packet(reflective_input)
    reflective_input.update(
        {
            "generation_mode": "operator_generated",
            "conceptual_systems": [
                _typed_unification(row)
                for row in reflective_preview["conceptual_systems"]
            ],
            "reflection_rounds": reflective_preview["reflection_rounds"],
        }
    )
    parent_packet = run(
        "reflective-conceptual-discovery",
        "theory",
        reflective_input,
        "reflective-parent",
        {"stage": "full"},
    )
    synthesis_packet = run(
        "reflective-theory-synthesizer",
        "theory",
        reflective_input,
        "reflective-synthesis",
        {"stage": "reflect"},
    )
    assert len(parent_packet["reflection_rounds"]) >= 2
    assert (
        synthesis_packet["provisional_synthesis"]["preferred_system_id"]
        is None
    )

    parent_receipt = next(
        receipt
        for receipt in receipts
        if receipt["operator"]["operator_id"]
        == "reflective-conceptual-discovery"
    )
    systems = parent_packet["conceptual_systems"]
    rounds = parent_packet["reflection_rounds"]
    frozen_genealogy: list[dict] = []
    proposer_receipt_ids = [parent_receipt["receipt_id"]]
    source_bindings = build_adjudication_source_bindings(
        run_id=namespace.run_id,
        state_version=namespace.state_version,
        theory_state_digest=current_snapshot["theory_state_digest"],
        literature_snapshot_digest=current_snapshot["content_digest"],
        high_risk_portfolio_digest=portfolio["content_digest"],
        systems=systems,
        reflection_rounds=rounds,
        frozen_genealogy=frozen_genealogy,
        proposer_receipt_ids=proposer_receipt_ids,
    )
    blind_packet, candidate_bindings = build_blind_packet(
        target_id=namespace.target_id,
        stage_id="route-conceptual-adjudication",
        target_charter={
            "root_tensions": [
                "Local construction and global interpretation still lack one typed mediator."
            ],
            "target_statement": reflective_input["discovery_charter"][
                "essential_question"
            ],
            "protected_successes": reflective_input["discovery_charter"][
                "target_commitments"
            ],
            "non_claims": [
                reflective_input["discovery_charter"]["non_claim_boundary"]
            ],
        },
        systems=systems,
        reflection_rounds=rounds,
        proposer_identity="reflective-conceptual-discovery",
        source_bindings=source_bindings,
        counterbalance_seed="seven-route-smoke-adjudication",
    )
    judge_reports = [
        build_judge_report(
            blind_packet,
            adjudicator_id=f"seven-route-{lens}-judge",
            perspective=lens,
            lens_family=lens,
            version="1.0.0",
            judge=judge,
            created_at=parent_receipt["completed_at"],
        )
        for lens, judge in (
            ("ontological", _ontological_judge),
            ("dialectical", _dialectical_judge),
            ("explanatory", _explanatory_judge),
        )
    ]
    adjudication = run(
        "blind-conceptual-preference-adjudicator",
        "evaluation",
        {
            "blind_packet": blind_packet,
            "judge_reports": judge_reports,
            "systems": systems,
            "reflection_rounds": rounds,
            "frozen_genealogy": frozen_genealogy,
            "candidate_bindings": candidate_bindings,
            "theory_state_digest": current_snapshot["theory_state_digest"],
            "literature_snapshot_digest": current_snapshot["content_digest"],
            "high_risk_portfolio_digest": portfolio["content_digest"],
            "proposer_receipt_ids": proposer_receipt_ids,
            "previous_evidence": None,
            "previous_evidence_digest": None,
            "created_at": parent_receipt["completed_at"],
        },
        "conceptual-adjudication",
        {"stage": "blind-preference"},
    )
    assert adjudication["stage_id"] == "route-conceptual-adjudication"

    assert {receipt["operator"]["operator_id"] for receipt in receipts} == standalone_operator_ids
    ensure_evaluation_ready(requests, receipts, workspace=tmp_path)
    manifest = build_execution_manifest(registry, receipts, request_count=len(requests))
    assert {row["operator_id"] for row in manifest["executions"]} == standalone_operator_ids
    assert len(manifest["feedback_edge_candidates"]) == len(standalone_operator_ids)
    assert manifest["feedback_committed"] is False
    assert all(
        edge["consumed"] is False and edge["state_edge_committed"] is False
        for edge in manifest["feedback_edge_candidates"]
    )
    assert all((tmp_path / receipt["output_artifacts"][0]["path"]).is_file() for receipt in receipts)

    # Rehashing an output that demotes a live snapshot must not fool the
    # independent validator: integrity is necessary, not sufficient.
    literature_index = next(
        index
        for index, receipt in enumerate(receipts)
        if receipt["operator"]["operator_id"] == "frontier-literature-assimilator"
    )
    literature_path = tmp_path / receipts[literature_index]["output_artifacts"][0]["path"]
    laundered = json.loads(literature_path.read_text(encoding="utf-8"))
    laundered["resolution"]["active_investment_gate"] = "blocked_local_only"
    laundered["hypothesis_rebase_status"] = "provisional_local_only"
    unsigned = dict(laundered)
    unsigned.pop("content_digest")
    laundered["content_digest"] = canonical_digest(unsigned)
    literature_path.write_text(json.dumps(laundered, sort_keys=True) + "\n", encoding="utf-8")
    validator_command = next(
        row for row in registry["operators"] if row["operator_id"] == "frontier-literature-assimilator"
    )["validators"][0]["command"]
    rejected = subprocess.run(
        validator_command,
        cwd=tmp_path,
        input=json.dumps(
            {
                "request": requests[literature_index],
                "artifacts": [artifact_descriptor(literature_path, tmp_path, namespace)],
            }
        ).encode(),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    assert rejected.returncode != 0
    assert b"provenance authority" in rejected.stderr


def test_reachability_requires_consumption_and_feedback_effect(tmp_path: Path) -> None:
    request = _request(tmp_path)
    receipt = DiscoveryOperatorDispatcher(
        [_binding()], workspace=tmp_path, receipt_store=ReceiptStore(tmp_path / "receipts")
    ).dispatch(request)
    with pytest.raises(DispatchBlocked, match="feedback-effective"):
        assert_feedback_effective([receipt], [])
    assert_feedback_effective(
        [receipt],
        [{
            "producer_receipt_id": receipt["receipt_id"],
            "consumer_event_id": "devent.abc",
            "consumed": True,
            "state_edge_committed": True,
        }],
    )


# REUSE-IgnoreStart
def test_route_generation_preserves_spdx_header_but_rejects_stale_body(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Disclosure metadata may vary independently of the registry projection."""
    path = tmp_path / "routes.md"
    monkeypatch.setattr(registry_runtime, "ROUTES_DOC_PATH", path)
    registry = load_registry()
    body = render_routes(registry)
    preamble = (
        "<!--\nSPDX-FileCopyrightText: 2026 Original Holder\n"
        "SPDX-FileContributor: Prior Author <prior@example.org>\n"
        "SPDX-License-Identifier: MIT\n-->\n"
    )
    path.write_text(preamble + body, encoding="utf-8")
    assert render_routes(registry) == preamble + body
    path.write_text(preamble + "stale registry projection\n", encoding="utf-8")
    assert render_routes(registry) != path.read_text(encoding="utf-8")
    assert render_routes(registry).startswith(preamble)


# REUSE-IgnoreEnd
