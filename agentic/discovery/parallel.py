# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
"""Isolated dependency-aware execution for plural theory hypotheses.

Parallel workers receive deep-copied requests bound to one target, theory
generation, literature snapshot, and portfolio digest. They can write only to a
branch-local namespace and can never commit shared theory state. Every scheduled
attempt receives a typed receipt—even timeout, invalid output, dependency block,
or operational failure. Valid siblings survive, conflicts remain explicit, and
one optional compare-and-swap callback is the sole durable merge boundary.
"""

from __future__ import annotations

import copy
import hashlib
import json
import multiprocessing as mp
import os
import re
import signal
import time
from collections import defaultdict
from typing import Any, Callable, Mapping, Sequence

from .contracts import (
    ContractError,
    canonical_digest,
    safe_relative_path,
    stable_identifier,
    utc_now,
    validate_identifier,
    validate_payload,
)
from .hypotheses import validate_high_risk_portfolio


Worker = Callable[[Mapping[str, Any]], Mapping[str, Any]]
LiteratureResolver = Callable[[], Mapping[str, Any]]
RebaseWorker = Callable[[Mapping[str, Any], Mapping[str, Any]], Mapping[str, Any]]
CASMerge = Callable[[int, Mapping[str, Any]], Any]
SealedEvidenceLoader = Callable[[Mapping[str, Any]], bytes]
RETRYABLE = {"timeout", "failed", "cancelled", "invalid", "dependency_blocked"}

_SEMANTIC_TOKEN = re.compile(r"[A-Za-z][A-Za-z0-9_-]*")
_SEMANTIC_PLACEHOLDERS = {
    "change", "changed", "conceptual", "deepen", "deepening", "delta",
    "item", "new", "placeholder", "something", "thing", "todo", "tbd",
    "unknown", "value",
}
_STRUCTURAL_DELTA_FIELDS = {
    "new_primitives": "primitives",
    "retired_primitives": "primitives",
    "primitive_changes": "primitives",
    "new_relations": "relations",
    "changed_relations": "relations",
    "relation_changes": "relations",
    "mechanism": "mechanism",
    "mechanism_stages": "mechanism",
    "causal_edges": "mechanism",
    "new_explanatory_dependencies": "explanatory_dependencies",
    "understanding_delta": "explanatory_dependencies",
    "changed_assumptions": "assumptions",
    "new_distinctions": "distinctions",
    "preserved_differences": "preserved_differences",
    "transformations": "transformations",
    "synthesis": "synthesis",
    "counterfactuals": "correction_structure",
    "correction_conditions": "correction_structure",
    "falsifiers": "correction_structure",
}


def _without(payload: Mapping[str, Any], *keys: str) -> dict[str, Any]:
    """Copy an envelope while excluding circular digest fields."""

    result = copy.deepcopy(dict(payload))
    for key in keys:
        result.pop(key, None)
    return result


def _request_input_digest(request: Mapping[str, Any]) -> str:
    """Digest immutable branch input while excluding attempt-local identity."""

    return canonical_digest(
        {
            key: value
            for key, value in request.items()
            if key
            not in {
                "input_digest",
                "invocation_id",
                "attempt",
                "artifact_namespace",
            }
        }
    )


def _semantic_content(value: Any) -> Any:
    """Canonicalize content-bearing semantic roles without scoring prose style."""

    if isinstance(value, Mapping):
        return {
            str(key): _semantic_content(item)
            for key, item in sorted(value.items(), key=lambda pair: str(pair[0]))
            if str(key) not in {"id", "digest", "score", "confidence"}
            and _semantic_content(item) not in (None, "", [], {})
        }
    if isinstance(value, (list, tuple, set)):
        rows = [_semantic_content(item) for item in value]
        return [item for item in rows if item not in (None, "", [], {})]
    if isinstance(value, str):
        tokens = [
            token.lower()
            for token in _SEMANTIC_TOKEN.findall(value)
            if token.lower() not in _SEMANTIC_PLACEHOLDERS
        ]
        return " ".join(tokens) if tokens else ""
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        return value
    return None


def _derive_semantic_delta(
    theory_delta: Mapping[str, Any], request: Mapping[str, Any]
) -> dict[str, Any]:
    """Derive structural learning evidence independently of a worker's verdict.

    This is deliberately a conservative runtime gate, not a philosophical
    quality judgment.  A branch counts as learning only when its typed delta
    changes at least two semantic role families and one of them changes the
    proposed ontology, relation topology, mechanism, explanation, or synthesis.
    Identifiers and changed questions are diagnostics, not structural roles.
    Merely echoing the seed, setting a boolean, renaming a mechanism, or adding
    fluent prose cannot enter the Pareto frontier or learning metrics.
    """

    roles: dict[str, Any] = {}
    diagnostics: dict[str, Any] = {}
    mechanism = _semantic_content(theory_delta.get("mechanism_key"))
    baseline_mechanism = _semantic_content(request.get("mechanism_key"))
    if mechanism and mechanism != baseline_mechanism:
        diagnostics["renamed_mechanism_key"] = mechanism

    question = _semantic_content(theory_delta.get("changed_question"))
    baseline_questions = {
        _semantic_content(request.get("maturation_question")),
        _semantic_content(request.get("expected_theory_delta")),
    }
    if question and question not in baseline_questions:
        diagnostics["changed_question"] = question

    baseline_content_digests = {
        canonical_digest(item)
        for item in (
            baseline_mechanism,
            *(_semantic_content(item) for item in request.get("unique_primitives", [])),
            *baseline_questions,
        )
        if item not in (None, "", [], {})
    }

    for field, family in _STRUCTURAL_DELTA_FIELDS.items():
        content = _semantic_content(theory_delta.get(field))
        if (
            content not in (None, "", [], {})
            and canonical_digest(content) not in baseline_content_digests
        ):
            roles.setdefault(family, {})
            if isinstance(roles[family], dict):
                roles[family][field] = content

    ontology = theory_delta.get("ontology")
    if isinstance(ontology, Mapping):
        primitives = _semantic_content(ontology.get("primitives"))
        relations = _semantic_content(ontology.get("relations"))
        baseline_primitives = _semantic_content(request.get("unique_primitives"))
        if primitives and primitives != baseline_primitives:
            roles["primitives"] = {"ontology.primitives": primitives}
        if relations:
            roles["relations"] = {"ontology.relations": relations}

    changed_families = sorted(roles)
    topology_families = {
        "primitives", "relations", "mechanism", "explanatory_dependencies",
        "transformations", "synthesis",
    }
    material = (
        len(changed_families) >= 2
        and bool(topology_families.intersection(changed_families))
    )
    return {
        "authority": "parallel-runtime-derived-structural-delta.v1",
        "baseline_digest": canonical_digest(
            {
                "mechanism_key": request.get("mechanism_key"),
                "maturation_question": request.get("maturation_question"),
                "unique_primitives": request.get("unique_primitives", []),
                "expected_theory_delta": request.get("expected_theory_delta"),
            }
        ),
        "candidate_digest": canonical_digest(dict(theory_delta)),
        "changed_role_families": changed_families,
        "diagnostic_changes": diagnostics,
        "role_evidence_digests": {
            family: canonical_digest(content)
            for family, content in sorted(roles.items())
        },
        "material": material,
        "reason": (
            "multiple explicit typed structural roles changed, including topology"
            if material
            else "worker output did not establish a multi-role typed structural delta"
        ),
        "classification": "provisional_structural_delta_candidate",
        "conceptual_quality_authorized": False,
        "quality_claim_boundary": (
            "Structural materiality only admits a candidate to independent reflective "
            "evaluation; it does not establish learning, depth, relevance, truth, "
            "understanding, or discovery efficacy."
        ),
    }


def _worker_process_entry(
    sender: Any, worker: Worker, request: Mapping[str, Any]
) -> None:
    """Execute one branch behind a process boundary and return one message."""

    try:
        if not hasattr(os, "setsid"):
            raise ContractError("killable workers require POSIX session isolation")
        os.setsid()
        sender.send(
            {
                "kind": "ready",
                "pid": os.getpid(),
                "process_group_id": os.getpgrp(),
                "session_id": os.getsid(0),
            }
        )
        raw = worker(copy.deepcopy(dict(request)))
        if not isinstance(raw, Mapping):
            raise ContractError("worker result must be an object")
        sender.send({"kind": "ok", "payload": copy.deepcopy(dict(raw))})
    except BaseException as exc:  # process-local SystemExit is operational failure
        kind = "contract_error" if isinstance(exc, ContractError) else "error"
        try:
            sender.send(
                {
                    "kind": kind,
                    "error_class": type(exc).__name__,
                    "detail": str(exc),
                }
            )
        except (BrokenPipeError, EOFError, OSError):
            pass
    finally:
        sender.close()


def _terminate_worker(process: Any, process_group_id: int | None) -> None:
    """Stop a worker session, its inherited descendants, and reap its leader."""

    if process_group_id is not None:
        if (
            process_group_id <= 0
            or process_group_id != process.pid
            or process_group_id == os.getpgrp()
        ):
            raise ContractError("refusing to signal a non-worker process group")
        try:
            os.killpg(process_group_id, signal.SIGTERM)
        except ProcessLookupError:
            pass
        except PermissionError:
            # Darwin may report EPERM for a group containing only the exited
            # leader zombie. Continue to join/hard-stop; the final liveness
            # check below remains the fail-closed authority.
            pass
    elif process.is_alive():
        # A worker cannot have invoked user code before the ready receipt, so a
        # pre-ready leader has no authorized descendants to clean up.
        process.terminate()
    process.join(timeout=0.25)
    if process_group_id is not None:
        # Always issue the hard group stop: a leader may have exited while a
        # background child retained the session/process group.
        try:
            os.killpg(process_group_id, signal.SIGKILL)
        except ProcessLookupError:
            pass
        except PermissionError:
            pass
    elif process.is_alive() and hasattr(process, "kill"):
        process.kill()
    process.join(timeout=0.25)
    if process.is_alive():
        raise ContractError(
            "killable worker boundary could not terminate a timed-out branch"
        )


def _run_killable_wave(
    wave_requests: Sequence[Mapping[str, Any]],
    worker: Worker,
    *,
    max_workers: int,
    portfolio_deadline: float,
) -> list[dict[str, Any]]:
    """Run a bounded wave in forked workers and return only after all are reaped."""

    if not wave_requests:
        return []
    if "fork" not in mp.get_all_start_methods():
        raise ContractError(
            "parallel execution requires a killable 'fork' process boundary; "
            "this platform cannot safely enforce branch timeouts"
        )
    context = mp.get_context("fork")
    queued = [copy.deepcopy(dict(item)) for item in wave_requests]
    active: dict[str, dict[str, Any]] = {}
    outcomes: list[dict[str, Any]] = []

    while queued or active:
        now = time.monotonic()
        while queued and len(active) < max_workers and now < portfolio_deadline:
            request = queued.pop(0)
            receiver, sender = context.Pipe(duplex=False)
            started_at = utc_now()
            started_monotonic = time.monotonic()
            process = context.Process(
                target=_worker_process_entry,
                args=(sender, worker, request),
                name=f"parallel-{request['branch_id']}",
            )
            try:
                process.start()
                sender.close()
                active[str(request["branch_id"])] = {
                    "request": request,
                    "receiver": receiver,
                    "process": process,
                    "started_at": started_at,
                    "started_monotonic": started_monotonic,
                    "process_group_id": None,
                    "session_ready": False,
                }
            except BaseException as exc:
                sender.close()
                receiver.close()
                outcomes.append(
                    {
                        "request": request,
                        "started_at": started_at,
                        "elapsed": time.monotonic() - started_monotonic,
                        "message": {
                            "kind": "error",
                            "error_class": type(exc).__name__,
                            "detail": str(exc),
                        },
                    }
                )
            now = time.monotonic()

        progressed = False
        for branch_id, state in list(active.items()):
            request = state["request"]
            receiver = state["receiver"]
            process = state["process"]
            now = time.monotonic()
            branch_deadline = min(
                portfolio_deadline,
                state["started_monotonic"]
                + float(request["budget"]["wall_seconds"]),
            )
            message: dict[str, Any] | None = None
            timed_out = False
            if receiver.poll():
                try:
                    received = receiver.recv()
                    if isinstance(received, dict) and received.get("kind") == "ready":
                        group_id = received.get("process_group_id")
                        session_id = received.get("session_id")
                        if (
                            isinstance(group_id, bool)
                            or not isinstance(group_id, int)
                            or group_id != process.pid
                            or session_id != process.pid
                            or received.get("pid") != process.pid
                        ):
                            message = {
                                "kind": "error",
                                "error_class": "WorkerIsolationError",
                                "detail": "worker did not enter its own process group/session",
                            }
                        else:
                            state["process_group_id"] = group_id
                            state["session_ready"] = True
                            progressed = True
                            continue
                    message = (
                        received
                        if isinstance(received, dict)
                        else {
                            "kind": "error",
                            "error_class": "InvalidWorkerMessage",
                            "detail": "worker process returned a non-object message",
                        }
                    )
                except (EOFError, OSError) as exc:
                    message = {
                        "kind": "error",
                        "error_class": type(exc).__name__,
                        "detail": str(exc),
                    }
            elif not process.is_alive():
                message = {
                    "kind": "error",
                    "error_class": "WorkerProcessExit",
                    "detail": f"worker exited with code {process.exitcode} without a result",
                }
            elif now >= branch_deadline:
                timed_out = True
                message = {
                    "kind": "timeout",
                    "error_class": (
                        "portfolio_wall_time_exceeded"
                        if now >= portfolio_deadline
                        else "branch_wall_time_exceeded"
                    ),
                    "detail": "worker was terminated at its absolute deadline",
                }

            if message is None:
                continue
            # A result never authorizes background work. Group cleanup is done
            # for success, error, and timeout alike before any receipt is issued.
            _terminate_worker(process, state.get("process_group_id"))
            receiver.close()
            outcomes.append(
                {
                    "request": request,
                    "started_at": state["started_at"],
                    "elapsed": time.monotonic() - state["started_monotonic"],
                    "message": message,
                }
            )
            del active[branch_id]
            progressed = True

        if time.monotonic() >= portfolio_deadline and queued:
            for request in queued:
                outcomes.append(
                    {
                        "request": request,
                        "started_at": utc_now(),
                        "elapsed": 0.0,
                        "message": {
                            "kind": "timeout",
                            "error_class": "portfolio_wall_time_exceeded",
                            "detail": "portfolio deadline elapsed before branch launch",
                        },
                    }
                )
            queued.clear()
            progressed = True
        if not progressed and active:
            time.sleep(0.002)
    return outcomes


def run_bounded_killable_request_wave(
    wave_requests: Sequence[Mapping[str, Any]],
    worker: Worker,
    *,
    max_workers: int,
    portfolio_wall_seconds: float,
) -> list[dict[str, Any]]:
    """Execute one public, bounded, killable request wave.

    This is the narrow process primitive shared by discovery producers that do
    not need the hypothesis-portfolio reducer.  Callers must precommit unique
    ``branch_id`` values and a per-request ``budget.wall_seconds``.  The wrapper
    deep-copies every request, imposes one absolute portfolio deadline, reaps
    every worker process group, and returns terminal outcomes in request order.

    Returned messages are operational evidence only.  They do not establish
    provider, model, human, cognitive, semantic, or evaluator independence, and
    callers remain responsible for validating and receipt-binding output
    content before it can enter a discovery artifact.
    """

    if (
        isinstance(max_workers, bool)
        or not isinstance(max_workers, int)
        or max_workers < 1
    ):
        raise ContractError("bounded request wave requires max_workers >= 1")
    if (
        isinstance(portfolio_wall_seconds, bool)
        or not isinstance(portfolio_wall_seconds, (int, float))
        or not 0 < float(portfolio_wall_seconds) <= 3600
    ):
        raise ContractError(
            "bounded request wave portfolio_wall_seconds must be in (0, 3600]"
        )
    requests = [copy.deepcopy(dict(item)) for item in wave_requests]
    branch_ids: list[str] = []
    for request in requests:
        branch_id = str(request.get("branch_id", ""))
        validate_identifier(branch_id, "bounded request wave branch_id")
        budget = request.get("budget")
        if not isinstance(budget, Mapping):
            raise ContractError(
                "bounded request wave requires a budget object per request"
            )
        wall_seconds = budget.get("wall_seconds")
        if (
            isinstance(wall_seconds, bool)
            or not isinstance(wall_seconds, (int, float))
            or not 0 < float(wall_seconds) <= float(portfolio_wall_seconds)
        ):
            raise ContractError(
                "request wall_seconds must be positive and no larger than "
                "the portfolio deadline"
            )
        branch_ids.append(branch_id)
    if len(branch_ids) != len(set(branch_ids)):
        raise ContractError("bounded request wave branch IDs must be unique")

    requested_order = {
        branch_id: index for index, branch_id in enumerate(branch_ids)
    }
    outcomes = _run_killable_wave(
        requests,
        worker,
        max_workers=min(max_workers, len(requests) or 1),
        portfolio_deadline=time.monotonic() + float(portfolio_wall_seconds),
    )
    outcomes.sort(
        key=lambda row: requested_order[str(row["request"]["branch_id"])]
    )
    return outcomes


def _seed_signature(seed: Mapping[str, Any]) -> str:
    """Deduplicate by genealogy, primitive mechanism, and maturation question."""

    # Never trust a caller-supplied signature as the equivalence decision. The
    # explicit structural fields are recomputed so disguised duplicates cannot
    # buy a second worker merely by changing a digest string.
    return canonical_digest(
        {
            "mechanism_key": seed.get("mechanism_key"),
            "maturation_question": " ".join(
                str(seed.get("maturation_question", "")).lower().split()
            ),
            "genealogy": sorted(seed.get("genealogy", [])),
            "unique_primitives": sorted(seed.get("unique_primitives", [])),
        }
    )


def _topological_waves(
    branch_ids: Sequence[str], dependencies: Mapping[str, Sequence[str]]
) -> list[list[str]]:
    """Return deterministic barrier waves and reject cycles or unknown parents."""

    nodes = set(branch_ids)
    parents: dict[str, set[str]] = {
        branch_id: set(dependencies.get(branch_id, ())) for branch_id in branch_ids
    }
    unknown = sorted(
        {
            parent
            for branch_parents in parents.values()
            for parent in branch_parents
            if parent not in nodes
        }
    )
    if unknown:
        raise ContractError(
            f"dependency DAG cites unknown branches: {', '.join(unknown)}"
        )
    waves: list[list[str]] = []
    completed: set[str] = set()
    while len(completed) < len(nodes):
        ready = sorted(
            branch_id
            for branch_id in nodes - completed
            if parents[branch_id].issubset(completed)
        )
        if not ready:
            unresolved = sorted(nodes - completed)
            raise ContractError(
                f"dependency DAG contains a cycle among: {', '.join(unresolved)}"
            )
        waves.append(ready)
        completed.update(ready)
    return waves


def build_parallel_manifest(
    high_risk_portfolio: Mapping[str, Any],
    *,
    base_theory_state_version: int,
    branch_seeds: Sequence[Mapping[str, Any]] | None = None,
    dependencies: Mapping[str, Sequence[str]] | None = None,
    resource_budget: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    """Freeze inputs, structurally deduplicate seeds, and build DAG barrier waves."""

    validate_high_risk_portfolio(high_risk_portfolio)
    if (
        isinstance(base_theory_state_version, bool)
        or not isinstance(base_theory_state_version, int)
        or base_theory_state_version < 0
    ):
        raise ContractError("base_theory_state_version must be non-negative")
    seeds = [
        copy.deepcopy(dict(item))
        for item in (
            branch_seeds
            if branch_seeds is not None
            else high_risk_portfolio["parallel_branch_seeds"]
        )
    ]
    if not seeds:
        raise ContractError("parallel portfolio requires at least one branch seed")

    # Keep the first deterministic representative and record all correlated
    # seeds. Dependency references are redirected to the representative.
    by_signature: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for seed in seeds:
        by_signature[_seed_signature(seed)].append(seed)
    representatives: list[dict[str, Any]] = []
    duplicate_groups: list[list[str]] = []
    alias: dict[str, str] = {}
    for signature, group in sorted(by_signature.items()):
        ordered = sorted(group, key=lambda item: str(item["branch_id"]))
        representative = ordered[0]
        representatives.append(representative)
        for seed in ordered:
            alias[str(seed["branch_id"])] = str(representative["branch_id"])
        if len(ordered) > 1:
            duplicate_groups.append(
                [str(item["branch_id"]) for item in ordered]
            )
    branch_ids = [str(item["branch_id"]) for item in representatives]
    if len(branch_ids) != len(set(branch_ids)):
        raise ContractError("branch IDs must be unique after structural deduplication")

    raw_dependencies = dict(dependencies or {})
    normalized_dependencies: dict[str, list[str]] = {}
    for branch_id in branch_ids:
        source_parents = raw_dependencies.get(branch_id, ())
        normalized_dependencies[branch_id] = sorted(
            {
                alias.get(str(parent), str(parent))
                for parent in source_parents
                if alias.get(str(parent), str(parent)) != branch_id
            }
        )
    wave_ids = _topological_waves(branch_ids, normalized_dependencies)

    budget = {
        "wall_seconds": float((resource_budget or {}).get("wall_seconds", 300.0)),
        "max_workers": int((resource_budget or {}).get("max_workers", 4)),
        "cost_units": float((resource_budget or {}).get("cost_units", 100.0)),
        "storage_bytes": int(
            (resource_budget or {}).get("storage_bytes", 100_000_000)
        ),
    }
    if (
        budget["wall_seconds"] <= 0
        or budget["max_workers"] <= 0
        or budget["cost_units"] < 0
        or budget["storage_bytes"] < 0
    ):
        raise ContractError("parallel resource budgets must be bounded and non-negative")
    per_branch_cost = budget["cost_units"] / max(len(representatives), 1)
    per_branch_storage = budget["storage_bytes"] // max(len(representatives), 1)
    portfolio_id = stable_identifier(
        "parallel-portfolio",
        high_risk_portfolio["portfolio_id"],
        base_theory_state_version,
        [item["branch_id"] for item in representatives],
        normalized_dependencies,
    )
    requests: list[dict[str, Any]] = []
    for seed in sorted(representatives, key=lambda item: str(item["branch_id"])):
        branch_id = str(seed["branch_id"])
        namespace = (
            f"agentic/runs/parallel/{portfolio_id}/{branch_id}/attempt-1"
        )
        safe_relative_path(namespace)
        frozen = {
            "target_id": high_risk_portfolio["target_id"],
            "theory_digest": high_risk_portfolio["theory_state_digest"],
            "literature_digest": high_risk_portfolio[
                "literature_snapshot_digest"
            ],
            "portfolio_digest": high_risk_portfolio["content_digest"],
        }
        request_core: dict[str, Any] = {
            "invocation_id": stable_identifier(
                "parallel-invocation", portfolio_id, branch_id, 1, frozen
            ),
            "attempt": 1,
            "branch_id": branch_id,
            "hypothesis_id": str(seed["hypothesis_id"]),
            "corner_family": str(seed.get("corner_family") or "unknown_corner"),
            "mechanism_key": str(seed["mechanism_key"]),
            "maturation_question": str(seed["maturation_question"]),
            "unique_primitives": list(seed["unique_primitives"]),
            "genealogy": list(seed.get("genealogy") or [seed["hypothesis_id"]]),
            "seed_digest": canonical_digest(seed),
            "is_wildcard": bool(seed.get("is_wildcard", False)),
            "depends_on_branch_ids": normalized_dependencies[branch_id],
            "artifact_namespace": namespace,
            "allowed_skills": list(
                seed.get(
                    "allowed_skills",
                    [
                        "reflective-theory-synthesizer",
                        "high-risk-hypothesis-forger",
                    ],
                )
            ),
            "forbidden_shared_reads": sorted(
                set(
                    seed.get("forbidden_cross_branch_context", [])
                    + [
                        "agentic/reports/latest",
                        "agentic/reports/latest.json",
                        "agentic/state/current",
                        "another branch artifact namespace",
                    ]
                )
            ),
            "budget": {
                "wall_seconds": float(
                    seed.get("budget", {}).get(
                        "wall_seconds", budget["wall_seconds"]
                    )
                ),
                "cost_units": float(
                    seed.get("budget", {}).get("cost_units", per_branch_cost)
                ),
                "storage_bytes": int(
                    seed.get("budget", {}).get(
                        "storage_bytes", per_branch_storage
                    )
                ),
            },
            "stop_conditions": list(
                seed.get(
                    "stop_conditions",
                    [
                        "maturation question answered",
                        "correction condition triggered",
                        "absolute branch budget exhausted",
                    ],
                )
            ),
            "expected_theory_delta": str(
                seed.get(
                    "expected_theory_delta",
                    (
                        "A named change to primitives, mechanism, understanding, "
                        "genealogy, or a reusable negative result."
                    ),
                )
            ),
            "frozen_inputs": frozen,
        }
        # Input identity excludes the digest itself and therefore remains stable
        # across replay and selective retry.
        request_core["input_digest"] = _request_input_digest(request_core)
        requests.append(request_core)

    request_by_id = {item["branch_id"]: item for item in requests}
    edges = [
        {"parent": parent, "child": child}
        for child, parents in sorted(normalized_dependencies.items())
        for parent in parents
    ]
    diversity: list[dict[str, Any]] = []
    for left_index, left in enumerate(representatives):
        for right in representatives[left_index + 1 :]:
            diversity.append(
                {
                    "left_branch_id": left["branch_id"],
                    "right_branch_id": right["branch_id"],
                    "same_mechanism": (
                        left.get("mechanism_key") == right.get("mechanism_key")
                    ),
                    "same_genealogy": bool(
                        set(left.get("genealogy", []))
                        & set(right.get("genealogy", []))
                    ),
                    "same_maturation_question": (
                        " ".join(
                            str(left.get("maturation_question", "")).lower().split()
                        )
                        == " ".join(
                            str(right.get("maturation_question", "")).lower().split()
                        )
                    ),
                    "independent": (
                        left.get("mechanism_key") != right.get("mechanism_key")
                        and _seed_signature(left) != _seed_signature(right)
                    ),
                }
            )
    waves = [
        {
            "wave_id": f"wave-{index + 1:03d}",
            "purpose": "blind_divergence" if index == 0 else "maturation",
            "depends_on_wave_ids": (
                [] if index == 0 else [f"wave-{index:03d}"]
            ),
            "branch_ids": wave,
            "validation_barrier": {
                "valid_branch_ids": [],
                "failed_branch_ids": [],
                "invalid_branch_ids": [],
                "blocked_branch_ids": [],
                "partial_success_preserved": True,
            },
        }
        for index, wave in enumerate(wave_ids)
    ]
    return {
        "schema_version": "1.0",
        "portfolio_id": portfolio_id,
        "target_id": high_risk_portfolio["target_id"],
        "base_theory_state_version": base_theory_state_version,
        "base_theory_digest": high_risk_portfolio["theory_state_digest"],
        "literature_snapshot_id": high_risk_portfolio[
            "literature_snapshot_id"
        ],
        "literature_snapshot_digest": high_risk_portfolio[
            "literature_snapshot_digest"
        ],
        "high_risk_portfolio_digest": high_risk_portfolio["content_digest"],
        "created_at": utc_now(),
        "dependency_dag": {
            "nodes": sorted(branch_ids),
            "edges": edges,
            "deduplicated_branch_ids": sorted(
                {
                    branch_id
                    for group in duplicate_groups
                    for branch_id in group[1:]
                }
            ),
            "duplicate_groups": sorted(duplicate_groups),
        },
        "resource_budget": budget,
        "diversity_matrix": diversity,
        "branch_requests": [
            request_by_id[branch_id] for branch_id in sorted(request_by_id)
        ],
        "waves": waves,
    }


def validate_parallel_manifest(manifest: Mapping[str, Any]) -> None:
    """Reject mutable, digest-invalid, or dependency-invalid work before fan-out."""

    required = {
        "portfolio_id",
        "target_id",
        "base_theory_state_version",
        "base_theory_digest",
        "literature_snapshot_id",
        "literature_snapshot_digest",
        "dependency_dag",
        "resource_budget",
        "branch_requests",
        "waves",
    }
    missing = sorted(required - manifest.keys())
    if missing:
        raise ContractError(
            f"parallel manifest is missing: {', '.join(missing)}"
        )
    requests = list(manifest["branch_requests"])
    if not requests:
        raise ContractError("parallel manifest has no branch requests")
    branch_ids = [str(item.get("branch_id") or "") for item in requests]
    if any(not branch_id for branch_id in branch_ids) or len(branch_ids) != len(
        set(branch_ids)
    ):
        raise ContractError("parallel manifest branch IDs must be non-empty and unique")
    invocations = [str(item.get("invocation_id") or "") for item in requests]
    namespaces = [str(item.get("artifact_namespace") or "") for item in requests]
    if len(invocations) != len(set(invocations)) or len(namespaces) != len(
        set(namespaces)
    ):
        raise ContractError(
            "parallel manifest invocation IDs and artifact namespaces must be unique"
        )
    for request in requests:
        safe_relative_path(request["artifact_namespace"])
        if request.get("input_digest") != _request_input_digest(request):
            raise ContractError(
                f"branch {request['branch_id']} immutable input digest mismatch"
            )
        frozen = request.get("frozen_inputs", {})
        if (
            frozen.get("target_id") != manifest["target_id"]
            or frozen.get("theory_digest") != manifest["base_theory_digest"]
            or frozen.get("literature_digest")
            != manifest["literature_snapshot_digest"]
        ):
            raise ContractError(
                f"branch {request['branch_id']} is not bound to the manifest's frozen basis"
            )
        forbidden = " ".join(request.get("forbidden_shared_reads", [])).lower()
        if "latest" not in forbidden or "another branch" not in forbidden:
            raise ContractError(
                f"branch {request['branch_id']} lacks shared/mutable read prohibitions"
            )
    dependencies = {
        request["branch_id"]: list(request.get("depends_on_branch_ids", []))
        for request in requests
    }
    expected_waves = _topological_waves(branch_ids, dependencies)
    rendered_waves = [list(wave["branch_ids"]) for wave in manifest["waves"]]
    if rendered_waves != expected_waves:
        raise ContractError(
            "rendered waves do not match the deterministic dependency DAG"
        )


def _receipt(
    request: Mapping[str, Any],
    *,
    started_at: str,
    status: str,
    output_digest: str | None = None,
    theory_delta_ref: str | None = None,
    failure_class: str | None = None,
    failure_detail: str | None = None,
    validator_receipt_ids: Sequence[str] = (),
    wall_seconds: float = 0.0,
    cost_units: float = 0.0,
    storage_bytes: int = 0,
    reused_success: bool = False,
) -> dict[str, Any]:
    """Create the same complete receipt shape for every attempt outcome."""

    return {
        "receipt_id": stable_identifier(
            "parallel-receipt",
            request["invocation_id"],
            request["attempt"],
            status,
            output_digest,
        ),
        "invocation_id": request["invocation_id"],
        "attempt": request["attempt"],
        "branch_id": request["branch_id"],
        "input_digest": request["input_digest"],
        "started_at": started_at,
        "completed_at": utc_now(),
        "status": status,
        "output_digest": output_digest,
        "theory_delta_ref": theory_delta_ref,
        "failure_class": failure_class,
        "failure_detail": failure_detail,
        "resource_usage": {
            "wall_seconds": round(max(0.0, wall_seconds), 6),
            "cost_units": max(0.0, float(cost_units)),
            "storage_bytes": max(0, int(storage_bytes)),
        },
        "validator_receipt_ids": list(validator_receipt_ids),
        "reused_success": reused_success,
    }


def _normalize_result(
    raw: Mapping[str, Any], request: Mapping[str, Any]
) -> dict[str, Any]:
    """Validate a worker delta without allowing it to rewrite frozen identity."""

    for field, expected in (
        ("target_id", request["frozen_inputs"]["target_id"]),
        ("theory_digest", request["frozen_inputs"]["theory_digest"]),
        ("literature_digest", request["frozen_inputs"]["literature_digest"]),
    ):
        if field in raw and raw[field] != expected:
            raise ContractError(
                f"worker {request['branch_id']} returned mismatched {field}"
            )
    theory_delta = raw.get("theory_delta")
    if not isinstance(theory_delta, Mapping) or not theory_delta:
        raise ContractError("worker result lacks a non-empty typed theory_delta")
    claims = raw.get("claims", [])
    if not isinstance(claims, list):
        raise ContractError("worker claims must be a list")
    normalized_claims: list[dict[str, Any]] = []
    for index, claim in enumerate(claims):
        if not isinstance(claim, Mapping):
            raise ContractError("each worker claim must be an object")
        proposition = str(claim.get("proposition") or "").strip()
        stance = str(claim.get("stance") or "uncertain")
        if not proposition or stance not in {"support", "oppose", "uncertain"}:
            raise ContractError("claims need a proposition and typed stance")
        normalized_claims.append(
            {
                "claim_id": str(
                    claim.get("claim_id")
                    or stable_identifier(
                        "branch-claim",
                        request["branch_id"],
                        proposition,
                        stance,
                        index,
                    )
                ),
                "proposition": proposition,
                "stance": stance,
                "epistemic_status": str(
                    claim.get("epistemic_status") or "conjectural"
                ),
            }
        )
    semantic_delta = _derive_semantic_delta(theory_delta, request)
    claimed_learning = raw.get("conceptual_learning")
    if claimed_learning is not None and not isinstance(claimed_learning, bool):
        raise ContractError("worker conceptual_learning claim must be boolean when present")
    result: dict[str, Any] = {
        "branch_id": request["branch_id"],
        "invocation_id": request["invocation_id"],
        "input_digest": request["input_digest"],
        "target_id": request["frozen_inputs"]["target_id"],
        "theory_digest": request["frozen_inputs"]["theory_digest"],
        "literature_digest": request["frozen_inputs"]["literature_digest"],
        "literature_status": "current",
        "theory_delta": copy.deepcopy(dict(theory_delta)),
        "claims": normalized_claims,
        "genealogy": list(
            raw.get("genealogy")
            or request["genealogy"]
        ),
        "worker_claimed_conceptual_learning": claimed_learning,
        "semantic_delta": semantic_delta,
        "conceptual_learning": bool(semantic_delta["material"]),
        "conceptual_learning_claim_boundary": (
            "Compatibility field: true means only a runtime-derived provisional "
            "structural candidate; independent reflective evaluation is still required."
        ),
        "corner_family": request["corner_family"],
        "mechanism_key": request["mechanism_key"],
        "is_dissent": bool(raw.get("is_dissent", False)),
        "is_wildcard": bool(request["is_wildcard"]),
        "synthesis_parent_ids": list(raw.get("synthesis_parent_ids", [])),
        "resource_usage": {
            "cost_units": float(
                raw.get("resource_usage", {}).get("cost_units", 0.0)
            ),
            "storage_bytes": int(
                raw.get("resource_usage", {}).get("storage_bytes", 0)
            ),
        },
        "rebase_receipt_id": None,
    }
    usage = result["resource_usage"]
    if usage["cost_units"] < 0 or usage["storage_bytes"] < 0:
        raise ContractError("worker resource usage cannot be negative")
    if usage["cost_units"] > float(request["budget"]["cost_units"]):
        raise ContractError("worker exceeded its branch cost budget")
    if usage["storage_bytes"] > int(request["budget"]["storage_bytes"]):
        raise ContractError("worker exceeded its branch storage budget")
    result["output_digest"] = canonical_digest(
        _without(result, "output_digest")
    )
    return result


def _next_attempt_request(
    request: Mapping[str, Any], previous_attempt: int
) -> dict[str, Any]:
    """Create an idempotent selective-retry identity without changing inputs."""

    retry = copy.deepcopy(dict(request))
    retry["attempt"] = previous_attempt + 1
    retry["invocation_id"] = stable_identifier(
        "parallel-invocation",
        request["branch_id"],
        request["input_digest"],
        retry["attempt"],
    )
    retry["artifact_namespace"] = (
        str(request["artifact_namespace"]).rsplit("/attempt-", 1)[0]
        + f"/attempt-{retry['attempt']}"
    )
    safe_relative_path(retry["artifact_namespace"])
    return retry


def _claim_edges(
    results: Sequence[Mapping[str, Any]],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[str]]:
    """Preserve opposition and contradiction instead of majority flattening."""

    by_proposition: dict[str, dict[str, list[str]]] = defaultdict(
        lambda: defaultdict(list)
    )
    for result in results:
        for claim in result["claims"]:
            key = " ".join(claim["proposition"].lower().split())
            by_proposition[key][claim["stance"]].append(result["branch_id"])
    opposition: list[dict[str, Any]] = []
    contradictions: list[dict[str, Any]] = []
    dissent: set[str] = {
        result["branch_id"] for result in results if result.get("is_dissent")
    }
    for proposition, stances in sorted(by_proposition.items()):
        supporters = sorted(set(stances.get("support", [])))
        opponents = sorted(set(stances.get("oppose", [])))
        if supporters and opponents:
            edge = {
                "proposition": proposition,
                "support_branch_ids": supporters,
                "oppose_branch_ids": opponents,
            }
            opposition.append(edge)
            contradictions.append(
                {**edge, "resolution": "retained_for_reflective_synthesis"}
            )
            # The minority is dissent, but ties preserve both sides.
            if len(opponents) <= len(supporters):
                dissent.update(opponents)
            if len(supporters) <= len(opponents):
                dissent.update(supporters)
    return opposition, contradictions, sorted(dissent)


def _merge_proposal(
    manifest: Mapping[str, Any],
    results: Sequence[Mapping[str, Any]],
    failures: Sequence[Mapping[str, Any]],
) -> dict[str, Any]:
    """Build one non-scalar, conflict-preserving proposal for the reducer."""

    opposition, contradictions, dissent = _claim_edges(results)
    ancestry = [
        {
            "parent_id": parent,
            "child_branch_id": result["branch_id"],
            "relation": "matured_from",
        }
        for result in results
        for parent in result["genealogy"]
    ]
    synthesis = [
        {
            "parent_branch_id": parent,
            "child_branch_id": result["branch_id"],
            "relation": "explicit_synthesis",
        }
        for result in results
        for parent in result.get("synthesis_parent_ids", [])
    ]
    duplicates = [
        {
            "representative_branch_id": group[0],
            "duplicate_branch_id": duplicate,
        }
        for group in manifest["dependency_dag"]["duplicate_groups"]
        for duplicate in group[1:]
    ]
    ledger_events = [
        {
            "event_id": stable_identifier(
                "parallel-learning-event",
                manifest["portfolio_id"],
                result["branch_id"],
                result["output_digest"],
            ),
            "event_type": (
                "parallel_conceptual_learning"
                if result["conceptual_learning"]
                else "parallel_valid_no_learning"
            ),
            "branch_id": result["branch_id"],
            "output_digest": result["output_digest"],
            "theory_delta": result["theory_delta"],
        }
        for result in results
    ]
    ledger_events.extend(
        {
            "event_id": stable_identifier(
                "parallel-operational-event",
                failure["branch_id"],
                failure["status"],
                failure["receipt_id"],
            ),
            "event_type": "parallel_operational_failure",
            "branch_id": failure["branch_id"],
            "status": failure["status"],
            "failure_class": failure["failure_class"],
        }
        for failure in failures
    )
    return {
        "ancestry_edges": ancestry,
        "opposition_edges": opposition,
        "synthesis_edges": synthesis,
        "duplicate_edges": duplicates,
        "contradiction_edges": contradictions,
        # Every validated conceptually learning result remains Pareto-eligible;
        # no scheduler order or scalar score selects a winner here.
        "pareto_frontier_ids": sorted(
            result["branch_id"]
            for result in results
            if result["conceptual_learning"]
        ),
        "retained_dissent_ids": dissent,
        "retained_wildcard_ids": sorted(
            result["branch_id"]
            for result in results
            if result.get("is_wildcard")
        ),
        "proposed_ledger_events": ledger_events,
    }


def _resolve_literature(
    manifest: Mapping[str, Any], resolver: LiteratureResolver | None
) -> dict[str, Any]:
    """Resolve a current snapshot only outside workers and at wave barriers."""

    if resolver is None:
        return {
            "snapshot_id": manifest["literature_snapshot_id"],
            "content_digest": manifest["literature_snapshot_digest"],
        }
    resolved = copy.deepcopy(dict(resolver()))
    if not resolved.get("snapshot_id") or not resolved.get("content_digest"):
        raise ContractError(
            "literature resolver must return snapshot_id and content_digest"
        )
    return resolved


def _static_wave_projection(waves: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    """Return the immutable scheduling part of waves, excluding run barriers."""

    return [
        {
            "wave_id": wave.get("wave_id"),
            "purpose": wave.get("purpose"),
            "depends_on_wave_ids": list(wave.get("depends_on_wave_ids", [])),
            "branch_ids": list(wave.get("branch_ids", [])),
        }
        for wave in waves
    ]


def _raw_sha256(payload: bytes) -> str:
    return "sha256:" + hashlib.sha256(payload).hexdigest()


def _load_sealed_prior_run(
    prior_run: Mapping[str, Any] | None,
    descriptor: Mapping[str, Any] | None,
    loader: SealedEvidenceLoader | None,
) -> tuple[dict[str, Any] | None, dict[str, Any] | None]:
    """Load prior evidence through an explicit immutable byte boundary.

    A caller mapping is never reuse authority. It may be supplied as a
    convenience assertion, but only bytes returned by the sealed loader are
    parsed and validated as the authoritative prior packet.
    """

    if prior_run is None and descriptor is None and loader is None:
        return None, None
    if descriptor is None or loader is None:
        raise ContractError(
            "prior reuse requires an exact artifact descriptor and sealed byte loader"
        )
    artifact_ref = str(descriptor.get("artifact_ref") or "")
    safe_relative_path(artifact_ref)
    expected_digest = str(descriptor.get("sha256") or "")
    expected_length = descriptor.get("byte_length")
    loader_id = str(descriptor.get("loader_id") or "")
    if (
        not re.fullmatch(r"sha256:[a-f0-9]{64}", expected_digest)
        or isinstance(expected_length, bool)
        or not isinstance(expected_length, int)
        or expected_length <= 0
        or descriptor.get("media_type") != "application/json"
        or not loader_id
    ):
        raise ContractError("sealed prior evidence descriptor is incomplete")
    raw = loader(copy.deepcopy(dict(descriptor)))
    if not isinstance(raw, bytes):
        raise ContractError("sealed prior evidence loader must return exact bytes")
    if len(raw) != expected_length or _raw_sha256(raw) != expected_digest:
        raise ContractError("sealed prior evidence bytes do not match descriptor")
    try:
        loaded = json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ContractError(f"sealed prior evidence is not canonical JSON: {exc}") from exc
    if not isinstance(loaded, dict):
        raise ContractError("sealed prior evidence must decode to an object")
    if prior_run is not None and canonical_digest(prior_run) != canonical_digest(loaded):
        raise ContractError("caller prior_run differs from sealed evidence bytes")
    normalized = {
        "artifact_ref": artifact_ref,
        "sha256": expected_digest,
        "byte_length": expected_length,
        "media_type": "application/json",
        "loader_id": loader_id,
        "loaded_packet_content_digest": loaded.get("content_digest"),
    }
    return loaded, normalized


def _validate_prior_run_for_reuse(
    prior_run: Mapping[str, Any], manifest: Mapping[str, Any]
) -> None:
    """Fail closed unless a complete sealed prior packet matches current inputs."""

    try:
        validate_parallel_portfolio(prior_run)
    except (ContractError, KeyError, TypeError, ValueError) as exc:
        raise ContractError(f"prior_run failed full portfolio validation: {exc}") from exc
    for key in (
        "portfolio_id",
        "target_id",
        "base_theory_state_version",
        "base_theory_digest",
        "literature_snapshot_id",
        "literature_snapshot_digest",
        "dependency_dag",
        "resource_budget",
        "diversity_matrix",
    ):
        if prior_run.get(key) != manifest.get(key):
            raise ContractError(
                f"prior_run does not match the exact current input manifest field {key}"
            )
    if _static_wave_projection(prior_run.get("waves", [])) != _static_wave_projection(
        manifest.get("waves", [])
    ):
        raise ContractError("prior_run scheduling waves differ from the current manifest")

    current_requests = {
        str(item.get("branch_id")): item
        for item in manifest.get("branch_requests", [])
    }
    previous_requests = {
        str(item.get("branch_id")): item
        for item in prior_run.get("branch_requests", [])
    }
    if set(current_requests) != set(previous_requests):
        raise ContractError("prior_run branch set differs from the current manifest")
    for branch_id, current in current_requests.items():
        previous = previous_requests[branch_id]
        if (
            current.get("input_digest") != previous.get("input_digest")
            or _request_input_digest(current) != _request_input_digest(previous)
        ):
            raise ContractError(
                f"prior_run branch {branch_id} does not match the exact current input"
            )


def _matched_control_request(request: Mapping[str, Any]) -> dict[str, Any]:
    control = copy.deepcopy(dict(request))
    control["benchmark_condition"] = "matched_budget_conservative_control"
    control["control_of_invocation_id"] = request["invocation_id"]
    control["invocation_id"] = stable_identifier(
        "parallel-control-invocation", request["invocation_id"]
    )
    control["artifact_namespace"] = (
        f"{request['artifact_namespace']}/matched-budget-control"
    )
    safe_relative_path(control["artifact_namespace"])
    control["input_digest"] = _request_input_digest(control)
    return control


def _run_matched_budget_control(
    manifest: Mapping[str, Any],
    base_requests: Mapping[str, Mapping[str, Any]],
    worker: Worker | None,
) -> dict[str, Any]:
    """Execute an auditable conservative control with the same opportunity budget."""

    allocated = {
        "wall_seconds": float(manifest["resource_budget"]["wall_seconds"]),
        "cost_units": sum(
            float(item["budget"]["cost_units"]) for item in base_requests.values()
        ),
        "storage_bytes": sum(
            int(item["budget"]["storage_bytes"]) for item in base_requests.values()
        ),
        "branch_count": len(base_requests),
    }
    if worker is None:
        control = {
            "status": "not_run",
            "reason": "no matched-budget conservative control worker was supplied",
            "allocation_matches_full_condition": False,
            "allocated_budget": allocated,
            "branch_requests": [],
            "attempt_receipts": [],
            "branch_results": [],
            "structural_corner_coverage": 0,
        }
        control["content_digest"] = canonical_digest(control)
        return control

    requests = {
        branch_id: _matched_control_request(request)
        for branch_id, request in base_requests.items()
    }
    receipts: list[dict[str, Any]] = []
    results: list[dict[str, Any]] = []
    successful: set[str] = set()
    deadline = time.monotonic() + allocated["wall_seconds"]
    for wave in manifest["waves"]:
        wave_requests: list[dict[str, Any]] = []
        for branch_id in wave["branch_ids"]:
            request = requests[branch_id]
            if not set(request["depends_on_branch_ids"]).issubset(successful):
                receipts.append(
                    _receipt(
                        request,
                        started_at=utc_now(),
                        status="dependency_blocked",
                        failure_class="upstream_control_not_valid",
                        failure_detail="matched control parent did not pass its barrier",
                    )
                )
            else:
                wave_requests.append(request)
        for outcome in _run_killable_wave(
            wave_requests,
            worker,
            max_workers=max(
                1,
                min(
                    int(manifest["resource_budget"]["max_workers"]),
                    len(wave_requests) or 1,
                ),
            ),
            portfolio_deadline=deadline,
        ):
            request = outcome["request"]
            message = outcome["message"]
            elapsed = float(outcome["elapsed"])
            if message.get("kind") != "ok":
                status = "timeout" if message.get("kind") == "timeout" else "failed"
                receipts.append(
                    _receipt(
                        request,
                        started_at=outcome["started_at"],
                        status=status,
                        failure_class=str(message.get("error_class") or "control_failure"),
                        failure_detail=str(message.get("detail") or "control failed"),
                        wall_seconds=elapsed,
                    )
                )
                continue
            try:
                result = _normalize_result(message["payload"], request)
            except (ContractError, KeyError, TypeError, ValueError) as exc:
                receipts.append(
                    _receipt(
                        request,
                        started_at=outcome["started_at"],
                        status="invalid",
                        failure_class="output_contract_violation",
                        failure_detail=str(exc),
                        wall_seconds=elapsed,
                    )
                )
                continue
            validator_id = stable_identifier(
                "branch-validator", request["invocation_id"], result["output_digest"]
            )
            theory_delta_ref = (
                f"{request['artifact_namespace']}/theory-delta."
                f"{result['output_digest'].removeprefix('sha256:')[:16]}.json"
            )
            receipts.append(
                _receipt(
                    request,
                    started_at=outcome["started_at"],
                    status="completed",
                    output_digest=result["output_digest"],
                    theory_delta_ref=theory_delta_ref,
                    validator_receipt_ids=[validator_id],
                    wall_seconds=elapsed,
                    cost_units=result["resource_usage"]["cost_units"],
                    storage_bytes=result["resource_usage"]["storage_bytes"],
                )
            )
            results.append(result)
            successful.add(request["branch_id"])

    corners = {
        item["corner_family"]
        for item in results
        if item["semantic_delta"]["material"]
    }
    control = {
        "status": "completed",
        "reason": None,
        "allocation_matches_full_condition": True,
        "allocated_budget": allocated,
        "branch_requests": sorted(requests.values(), key=lambda item: item["branch_id"]),
        "attempt_receipts": sorted(receipts, key=lambda item: item["branch_id"]),
        "branch_results": sorted(results, key=lambda item: item["branch_id"]),
        "structural_corner_coverage": len(corners),
        "metric_boundary": (
            "Executed equal opportunity budget; coverage counts provisional structural "
            "candidates, not conceptual quality or discovery efficacy."
        ),
    }
    control["content_digest"] = canonical_digest(control)
    return control


def run_parallel_hypothesis_portfolio(
    manifest: Mapping[str, Any],
    worker: Worker,
    *,
    prior_run: Mapping[str, Any] | None = None,
    prior_evidence_descriptor: Mapping[str, Any] | None = None,
    sealed_prior_loader: SealedEvidenceLoader | None = None,
    matched_budget_control_worker: Worker | None = None,
    literature_resolver: LiteratureResolver | None = None,
    rebase_worker: RebaseWorker | None = None,
    cas_merge: CASMerge | None = None,
) -> dict[str, Any]:
    """Execute DAG waves with partial success, selective retry, and one merge."""

    plan = copy.deepcopy(dict(manifest))
    validate_parallel_manifest(plan)
    prior_run, reuse_evidence = _load_sealed_prior_run(
        prior_run, prior_evidence_descriptor, sealed_prior_loader
    )
    if prior_run is not None:
        _validate_prior_run_for_reuse(prior_run, plan)
    requests = {
        item["branch_id"]: copy.deepcopy(dict(item))
        for item in plan["branch_requests"]
    }
    waves = copy.deepcopy(list(plan["waves"]))
    overall_started = time.monotonic()
    deadline = overall_started + float(plan["resource_budget"]["wall_seconds"])
    receipts: list[dict[str, Any]] = []
    results: list[dict[str, Any]] = []
    successful_branches: set[str] = set()
    failed_branches: set[str] = set()
    invalid_branches: set[str] = set()
    blocked_branches: set[str] = set()
    prior_receipts = {
        item["branch_id"]: item
        for item in (prior_run or {}).get("attempt_receipts", [])
    }
    prior_results = {
        item["branch_id"]: item
        for item in (prior_run or {}).get("branch_results", [])
    }
    superseded = False
    newest_literature = {
        "snapshot_id": plan["literature_snapshot_id"],
        "content_digest": plan["literature_snapshot_digest"],
    }
    next_dependency_ready_wave: str | None = None

    for wave_index, wave in enumerate(waves):
        # Literature is read once at the barrier, never inside a branch.
        before_wave = _resolve_literature(plan, literature_resolver)
        if (
            before_wave["content_digest"]
            != plan["literature_snapshot_digest"]
        ):
            superseded = True
            newest_literature = before_wave
            next_dependency_ready_wave = wave["wave_id"]
            break
        wave_requests: list[dict[str, Any]] = []
        for branch_id in wave["branch_ids"]:
            request = requests[branch_id]
            parents = set(request["depends_on_branch_ids"])
            if not parents.issubset(successful_branches):
                now = utc_now()
                blocked = _receipt(
                    request,
                    started_at=now,
                    status="dependency_blocked",
                    failure_class="upstream_branch_not_valid",
                    failure_detail=(
                        "Dependent hypothesis cannot run until every parent "
                        "passes the previous barrier."
                    ),
                )
                receipts.append(blocked)
                blocked_branches.add(branch_id)
                wave["validation_barrier"]["blocked_branch_ids"].append(
                    branch_id
                )
                continue
            previous = prior_receipts.get(branch_id)
            previous_result = prior_results.get(branch_id)
            if (
                previous
                and previous_result
                and previous["status"] in {"completed", "reused"}
                and previous["input_digest"] == request["input_digest"]
                and previous_result.get("literature_digest")
                == request["frozen_inputs"]["literature_digest"]
                and previous_result.get("literature_status") == "current"
            ):
                reused_request = copy.deepcopy(request)
                reused_request["attempt"] = int(previous["attempt"])
                reused_request["invocation_id"] = previous["invocation_id"]
                reused = _receipt(
                    reused_request,
                    started_at=utc_now(),
                    status="reused",
                    output_digest=previous_result["output_digest"],
                    theory_delta_ref=previous["theory_delta_ref"],
                    validator_receipt_ids=previous["validator_receipt_ids"],
                    reused_success=True,
                )
                receipts.append(reused)
                results.append(copy.deepcopy(dict(previous_result)))
                successful_branches.add(branch_id)
                wave["validation_barrier"]["valid_branch_ids"].append(branch_id)
                continue
            if previous and previous["status"] in RETRYABLE:
                request = _next_attempt_request(
                    request, int(previous["attempt"])
                )
                requests[branch_id] = request
            wave_requests.append(request)

        outcomes = _run_killable_wave(
            wave_requests,
            worker,
            max_workers=max(
                1,
                min(
                    int(plan["resource_budget"]["max_workers"]),
                    len(wave_requests) or 1,
                ),
            ),
            portfolio_deadline=deadline,
        )
        for outcome in outcomes:
            request = outcome["request"]
            started_at = outcome["started_at"]
            elapsed = float(outcome["elapsed"])
            message = outcome["message"]
            branch_id = request["branch_id"]
            if message.get("kind") == "timeout":
                receipt = _receipt(
                    request,
                    started_at=started_at,
                    status="timeout",
                    failure_class=str(message.get("error_class") or "deadline_exceeded"),
                    failure_detail=str(message.get("detail") or "worker timed out"),
                    wall_seconds=elapsed,
                )
                receipts.append(receipt)
                failed_branches.add(branch_id)
                wave["validation_barrier"]["failed_branch_ids"].append(branch_id)
                continue
            if message.get("kind") == "contract_error":
                receipt = _receipt(
                    request,
                    started_at=started_at,
                    status="invalid",
                    failure_class="output_contract_violation",
                    failure_detail=str(message.get("detail") or "worker contract error"),
                    wall_seconds=elapsed,
                )
                receipts.append(receipt)
                invalid_branches.add(branch_id)
                wave["validation_barrier"]["invalid_branch_ids"].append(branch_id)
                continue
            if message.get("kind") != "ok":
                receipt = _receipt(
                    request,
                    started_at=started_at,
                    status="failed",
                    failure_class=str(message.get("error_class") or "WorkerProcessError"),
                    failure_detail=str(message.get("detail") or "worker process failed"),
                    wall_seconds=elapsed,
                )
                receipts.append(receipt)
                failed_branches.add(branch_id)
                wave["validation_barrier"]["failed_branch_ids"].append(branch_id)
                continue
            try:
                raw_result = message["payload"]
                result = _normalize_result(raw_result, request)
                validator_id = stable_identifier(
                    "branch-validator",
                    request["invocation_id"],
                    result["output_digest"],
                )
                theory_delta_ref = (
                    f"{request['artifact_namespace']}/theory-delta."
                    f"{result['output_digest'].removeprefix('sha256:')[:16]}.json"
                )
                safe_relative_path(theory_delta_ref)
                receipt = _receipt(
                    request,
                    started_at=started_at,
                    status="completed",
                    output_digest=result["output_digest"],
                    theory_delta_ref=theory_delta_ref,
                    validator_receipt_ids=[validator_id],
                    wall_seconds=elapsed,
                    cost_units=result["resource_usage"]["cost_units"],
                    storage_bytes=result["resource_usage"]["storage_bytes"],
                )
                receipts.append(receipt)
                results.append(result)
                successful_branches.add(branch_id)
                wave["validation_barrier"]["valid_branch_ids"].append(branch_id)
            except ContractError as exc:
                receipt = _receipt(
                    request,
                    started_at=started_at,
                    status="invalid",
                    failure_class="output_contract_violation",
                    failure_detail=str(exc),
                    wall_seconds=elapsed,
                )
                receipts.append(receipt)
                invalid_branches.add(branch_id)
                wave["validation_barrier"]["invalid_branch_ids"].append(
                    branch_id
                )
            except Exception as exc:
                receipt = _receipt(
                    request,
                    started_at=started_at,
                    status="failed",
                    failure_class=type(exc).__name__,
                    failure_detail=str(exc),
                    wall_seconds=elapsed,
                )
                receipts.append(receipt)
                failed_branches.add(branch_id)
                wave["validation_barrier"]["failed_branch_ids"].append(branch_id)

        after_wave = _resolve_literature(plan, literature_resolver)
        if (
            after_wave["content_digest"]
            != plan["literature_snapshot_digest"]
        ):
            superseded = True
            newest_literature = after_wave
            next_dependency_ready_wave = (
                waves[wave_index + 1]["wave_id"]
                if wave_index + 1 < len(waves)
                else None
            )
            # A frozen wave may finish, but no additional budget is spent after
            # supersession. Survivors must explicitly rebase before merge.
            break

    rebase_receipts: list[str] = []
    required_rebase = sorted(successful_branches) if superseded else []
    rebased: list[str] = []
    rebase_blocked: list[str] = []
    if superseded:
        for result in results:
            branch_id = result["branch_id"]
            if rebase_worker is None:
                result["literature_status"] = "literature_superseded"
                rebase_blocked.append(branch_id)
                continue
            try:
                rebased_delta = copy.deepcopy(
                    dict(
                        rebase_worker(
                            copy.deepcopy(result),
                            copy.deepcopy(newest_literature),
                        )
                    )
                )
                if (
                    rebased_delta.get("literature_digest")
                    != newest_literature["content_digest"]
                ):
                    raise ContractError(
                        "rebase worker did not bind the newest literature digest"
                    )
                receipt_id = stable_identifier(
                    "parallel-rebase",
                    branch_id,
                    plan["literature_snapshot_digest"],
                    newest_literature["content_digest"],
                    rebased_delta,
                )
                # The worker receipt remains immutable and continues to name the
                # original output.  Rebased content receives its own digest and
                # receipt instead of rewriting execution history.
                result["pre_rebase_output_digest"] = result["output_digest"]
                result["pre_search_genealogy"] = list(result["genealogy"])
                result["theory_delta"] = copy.deepcopy(
                    rebased_delta.get("theory_delta", result["theory_delta"])
                )
                result["semantic_delta"] = _derive_semantic_delta(
                    result["theory_delta"], requests[branch_id]
                )
                result["conceptual_learning"] = bool(
                    result["semantic_delta"]["material"]
                )
                result["literature_digest"] = newest_literature[
                    "content_digest"
                ]
                result["literature_status"] = "rebased"
                result["rebase_receipt_id"] = receipt_id
                result["rebased_output_digest"] = canonical_digest(
                    _without(result, "output_digest")
                )
                rebase_receipts.append(receipt_id)
                rebased.append(branch_id)
            except Exception:
                result["literature_status"] = "literature_superseded"
                rebase_blocked.append(branch_id)
    literature_rebase_status = "current"
    if superseded and rebase_blocked:
        literature_rebase_status = "rebase_blocked"
    elif superseded:
        literature_rebase_status = "rebased"

    failures = [
        item
        for item in receipts
        if item["status"]
        in {"timeout", "failed", "cancelled", "invalid", "dependency_blocked"}
    ]
    merge = _merge_proposal(plan, results, failures)
    merged_branch_ids = sorted(
        result["branch_id"]
        for result in results
        if result["literature_status"] in {"current", "rebased"}
    )
    reducer_core: dict[str, Any] = {
        "reducer_id": "parallel-theory-reducer.v1",
        "expected_state_version": plan["base_theory_state_version"],
        "committed_state_version": None,
        "compare_and_swap_status": (
            "blocked_rebase" if rebase_blocked else "not_executed"
        ),
        "merged_branch_ids": merged_branch_ids,
    }
    if cas_merge is not None and not rebase_blocked and merged_branch_ids:
        try:
            # This is intentionally the only call capable of committing shared
            # state. Workers and validators have no reducer handle.
            outcome = cas_merge(
                int(plan["base_theory_state_version"]), copy.deepcopy(merge)
            )
            if isinstance(outcome, bool):
                committed_version = (
                    plan["base_theory_state_version"] + 1 if outcome else None
                )
            elif isinstance(outcome, int):
                committed_version = outcome
            elif isinstance(outcome, Mapping):
                committed_version = outcome.get("committed_state_version")
            else:
                committed_version = None
            if (
                isinstance(committed_version, bool)
                or not isinstance(committed_version, int)
                or committed_version
                != plan["base_theory_state_version"] + 1
            ):
                raise ContractError(
                    "CAS callback rejected the expected generation or returned "
                    "a non-successor version"
                )
            reducer_core["committed_state_version"] = committed_version
            reducer_core["compare_and_swap_status"] = "committed"
        except Exception:
            reducer_core["committed_state_version"] = None
            reducer_core["compare_and_swap_status"] = "conflict"
    reducer_core["content_digest"] = canonical_digest(reducer_core)

    retry_ids = sorted(
        {
            item["branch_id"]
            for item in failures
            if item["status"] in RETRYABLE
        }
    )
    corners = {
        result["corner_family"]
        for result in results
        if result["literature_status"] in {"current", "rebased"}
        and result["semantic_delta"]["material"]
    }
    independent_learning = sum(
        1
        for result in results
        if result["conceptual_learning"]
        and result["literature_status"] in {"current", "rebased"}
    )
    matched_control = _run_matched_budget_control(
        plan, requests, matched_budget_control_worker
    )
    baseline_coverage = int(matched_control["structural_corner_coverage"])
    comparison_authorized = bool(
        matched_control["status"] == "completed"
        and matched_control["allocation_matches_full_condition"]
    )
    packet: dict[str, Any] = {
        "schema_version": "1.0",
        "portfolio_id": plan["portfolio_id"],
        "target_id": plan["target_id"],
        "base_theory_state_version": plan["base_theory_state_version"],
        "base_theory_digest": plan["base_theory_digest"],
        "literature_snapshot_id": plan["literature_snapshot_id"],
        "literature_snapshot_digest": plan[
            "literature_snapshot_digest"
        ],
        "created_at": plan["created_at"],
        "dependency_dag": plan["dependency_dag"],
        "resource_budget": plan["resource_budget"],
        "diversity_matrix": plan["diversity_matrix"],
        "branch_requests": sorted(
            requests.values(), key=lambda item: item["branch_id"]
        ),
        "waves": waves,
        "attempt_receipts": sorted(
            receipts,
            key=lambda item: (
                item["branch_id"],
                item["attempt"],
                item["invocation_id"],
            ),
        ),
        "branch_results": sorted(
            results, key=lambda item: item["branch_id"]
        ),
        "partial_failure_ledger": {
            "preserved_branch_ids": sorted(successful_branches),
            "retry_branch_ids": retry_ids,
            "invalidated_by_dependency_ids": sorted(blocked_branches),
            "operational_failures": failures,
            "reuse_evidence": (
                None
                if reuse_evidence is None
                else {
                    **reuse_evidence,
                    "reused_branch_ids": sorted(
                        item["branch_id"]
                        for item in receipts
                        if item["status"] == "reused"
                    ),
                }
            ),
        },
        "literature_rebase": {
            "frozen_snapshot_id": plan["literature_snapshot_id"],
            "frozen_snapshot_digest": plan[
                "literature_snapshot_digest"
            ],
            "newest_snapshot_id": newest_literature["snapshot_id"],
            "newest_snapshot_digest": newest_literature["content_digest"],
            "status": literature_rebase_status,
            "rebase_receipt_ids": sorted(rebase_receipts),
            "required_branch_ids": required_rebase,
            "rebased_branch_ids": sorted(rebased),
            "blocked_branch_ids": sorted(rebase_blocked),
        },
        "merge_proposal": merge,
        "reducer_receipt": reducer_core,
        "portfolio_metrics": {
            "conceptual_corner_coverage": len(corners),
            "independent_learning_count": independent_learning,
            "successful_branch_count": len(successful_branches),
            "attempted_branch_count": len(
                [
                    item
                    for item in receipts
                    if item["status"] != "dependency_blocked"
                ]
            ),
            "matched_budget_baseline_corner_coverage": baseline_coverage,
            "matched_budget_improvement": (
                comparison_authorized and len(corners) > baseline_coverage
            ),
            "matched_budget_comparison_authorized": comparison_authorized,
            "matched_budget_control": matched_control,
            "structural_delta_candidate_count": independent_learning,
            "metric_claim_boundary": (
                "Coverage and candidate counts are structural scheduler diagnostics; "
                "they do not establish conceptual learning or efficacy."
            ),
            "worker_count_is_progress": False,
        },
        "next_dependency_ready_wave": next_dependency_ready_wave,
    }
    packet["content_digest"] = canonical_digest(
        _without(packet, "content_digest")
    )
    validate_parallel_portfolio(packet)
    return packet


def validate_parallel_portfolio(packet: Mapping[str, Any]) -> None:
    """Audit frozen identity, DAG barriers, receipts, retries, rebase, and CAS."""

    validate_payload(
        dict(packet), "parallel_hypothesis_portfolio.schema.json"
    )
    if packet["content_digest"] != canonical_digest(
        _without(packet, "content_digest")
    ):
        raise ContractError("parallel portfolio content digest mismatch")
    validate_parallel_manifest(packet)
    requests = {item["branch_id"]: item for item in packet["branch_requests"]}
    if len(requests) != len(packet["branch_requests"]):
        raise ContractError("branch requests need unique branch IDs")
    invocations = [
        item["invocation_id"] for item in packet["branch_requests"]
    ]
    if len(invocations) != len(set(invocations)):
        raise ContractError("branch invocation IDs must be unique")
    namespaces = [
        item["artifact_namespace"] for item in packet["branch_requests"]
    ]
    if len(namespaces) != len(set(namespaces)):
        raise ContractError("every branch requires a distinct artifact namespace")
    common = {
        (
            item["frozen_inputs"]["target_id"],
            item["frozen_inputs"]["theory_digest"],
            item["frozen_inputs"]["literature_digest"],
            item["frozen_inputs"]["portfolio_digest"],
        )
        for item in packet["branch_requests"]
    }
    if len(common) != 1:
        raise ContractError("workers did not receive one common frozen input basis")
    for request in packet["branch_requests"]:
        safe_relative_path(request["artifact_namespace"])
        forbidden = " ".join(request["forbidden_shared_reads"]).lower()
        if "latest" not in forbidden or "another branch" not in forbidden:
            raise ContractError(
                f"branch {request['branch_id']} lacks mutable/shared read prohibitions"
            )
        if request["frozen_inputs"]["target_id"] != packet["target_id"]:
            raise ContractError("branch target differs from portfolio target")
        if (
            request["frozen_inputs"]["theory_digest"]
            != packet["base_theory_digest"]
            or request["frozen_inputs"]["literature_digest"]
            != packet["literature_snapshot_digest"]
        ):
            raise ContractError("branch request is not bound to frozen theory/literature")

    wave_of: dict[str, int] = {}
    for index, wave in enumerate(packet["waves"]):
        for branch_id in wave["branch_ids"]:
            if branch_id in wave_of:
                raise ContractError("a branch appears in more than one DAG wave")
            wave_of[branch_id] = index
    for edge in packet["dependency_dag"]["edges"]:
        if wave_of.get(edge["parent"], -1) >= wave_of.get(edge["child"], -1):
            raise ContractError(
                "dependent hypotheses may not execute in the same or earlier wave"
            )

    receipts_by_invocation: dict[tuple[str, int], list[Mapping[str, Any]]] = defaultdict(list)
    for receipt in packet["attempt_receipts"]:
        receipts_by_invocation[
            (receipt["invocation_id"], int(receipt["attempt"]))
        ].append(receipt)
    if any(len(items) != 1 for items in receipts_by_invocation.values()):
        raise ContractError("every attempt must have exactly one receipt")
    results = {item["branch_id"]: item for item in packet["branch_results"]}
    if len(results) != len(packet["branch_results"]):
        raise ContractError("branch results need unique branch IDs")
    for branch_id, result in results.items():
        request = requests.get(branch_id)
        if request is None:
            raise ContractError("branch result names an unknown branch")
        for field, expected in (
            ("input_digest", request["input_digest"]),
            ("target_id", packet["target_id"]),
            ("theory_digest", packet["base_theory_digest"]),
        ):
            if result.get(field) != expected:
                raise ContractError(
                    f"branch result {branch_id} does not bind exact {field}"
                )
        derived = _derive_semantic_delta(result.get("theory_delta", {}), request)
        if result.get("semantic_delta") != derived:
            raise ContractError(
                f"branch result {branch_id} semantic delta was not independently derived"
            )
        if result.get("conceptual_learning") is not bool(derived["material"]):
            raise ContractError(
                f"branch result {branch_id} conceptual learning disagrees with semantic delta"
            )
        if result.get("literature_status") == "rebased":
            expected_rebased = canonical_digest(
                _without(result, "output_digest", "rebased_output_digest")
            )
            if result.get("rebased_output_digest") != expected_rebased:
                raise ContractError(f"branch result {branch_id} rebase digest mismatch")
            if result.get("pre_rebase_output_digest") != result.get("output_digest"):
                raise ContractError(f"branch result {branch_id} lost its pre-rebase digest")
        else:
            original = _without(result, "output_digest")
            if result.get("literature_status") == "literature_superseded":
                original["literature_status"] = "current"
            if result.get("output_digest") != canonical_digest(original):
                raise ContractError(f"branch result {branch_id} output digest mismatch")
    for receipt in packet["attempt_receipts"]:
        expected_receipt_id = stable_identifier(
            "parallel-receipt",
            receipt["invocation_id"],
            receipt["attempt"],
            receipt["status"],
            receipt["output_digest"],
        )
        if receipt.get("receipt_id") != expected_receipt_id:
            raise ContractError("attempt receipt identity is not content-bound")
        if receipt["status"] in {"completed", "reused"}:
            result = results.get(receipt["branch_id"])
            if result is None:
                raise ContractError("successful receipt lacks an independently consumable result")
            if receipt["output_digest"] != result["output_digest"]:
                raise ContractError("successful receipt and result digest differ")
            if (
                receipt["input_digest"] != result["input_digest"]
                or receipt["invocation_id"] != result["invocation_id"]
            ):
                raise ContractError("successful receipt and result identity differ")
            expected_validator = stable_identifier(
                "branch-validator",
                result["invocation_id"],
                result["output_digest"],
            )
            if receipt.get("validator_receipt_ids") != [expected_validator]:
                raise ContractError("successful result lacks its exact validator receipt")
            if not receipt.get("theory_delta_ref"):
                raise ContractError("successful result lacks an immutable theory-delta reference")
            safe_relative_path(receipt["theory_delta_ref"])
        elif receipt["output_digest"] is not None:
            raise ContractError("failed/invalid execution cannot claim a valid output digest")
    preserved = set(
        packet["partial_failure_ledger"]["preserved_branch_ids"]
    )
    successful = {
        item["branch_id"]
        for item in packet["attempt_receipts"]
        if item["status"] in {"completed", "reused"}
    }
    if not successful.issubset(preserved):
        raise ContractError("partial-failure ledger erased a valid sibling")
    retry_ids = set(packet["partial_failure_ledger"]["retry_branch_ids"])
    successful_inputs = {
        (item["branch_id"], item["input_digest"])
        for item in packet["attempt_receipts"]
        if item["status"] in {"completed", "reused"}
    }
    if any(
        branch_id in retry_ids
        for branch_id, _input_digest in successful_inputs
    ):
        raise ContractError("selective retry would repurchase successful current work")
    reused_ids = {
        item["branch_id"]
        for item in packet["attempt_receipts"]
        if item["status"] == "reused"
    }
    reuse_evidence = packet["partial_failure_ledger"].get("reuse_evidence")
    if reused_ids:
        if not isinstance(reuse_evidence, Mapping):
            raise ContractError("reused branches lack sealed prior evidence provenance")
        if set(reuse_evidence.get("reused_branch_ids", [])) != reused_ids:
            raise ContractError("sealed prior evidence does not cover every reused branch")
        if not re.fullmatch(
            r"sha256:[a-f0-9]{64}", str(reuse_evidence.get("sha256") or "")
        ):
            raise ContractError("sealed prior evidence digest is invalid")
        if reuse_evidence.get("loaded_packet_content_digest") is None:
            raise ContractError("sealed prior evidence lacks loaded packet identity")
    elif reuse_evidence is not None:
        raise ContractError("unused prior evidence cannot be presented as reuse authority")

    rebase = packet["literature_rebase"]
    if (
        rebase["newest_snapshot_digest"]
        != rebase["frozen_snapshot_digest"]
    ):
        required = set(rebase["required_branch_ids"])
        rebased = set(rebase["rebased_branch_ids"])
        blocked = set(rebase["blocked_branch_ids"])
        if required != rebased | blocked:
            raise ContractError(
                "every survivor must be explicitly rebased or explicitly blocked"
            )
        if blocked and packet["reducer_receipt"][
            "compare_and_swap_status"
        ] not in {"blocked_rebase", "conflict"}:
            raise ContractError(
                "unrebased survivors cannot enter synthesis or promotion"
            )
    reducer = packet["reducer_receipt"]
    if reducer["compare_and_swap_status"] == "committed":
        if (
            reducer["committed_state_version"]
            != reducer["expected_state_version"] + 1
        ):
            raise ContractError("CAS commit must advance exactly one state generation")
    if reducer["compare_and_swap_status"] == "conflict" and reducer[
        "committed_state_version"
    ] is not None:
        raise ContractError("stale CAS conflict cannot claim a committed generation")
    conflict_branches = {
        branch_id
        for edge in packet["merge_proposal"]["contradiction_edges"]
        for key in ("support_branch_ids", "oppose_branch_ids")
        for branch_id in edge.get(key, [])
    }
    if conflict_branches and not (
        conflict_branches
        & set(packet["merge_proposal"]["retained_dissent_ids"])
    ):
        raise ContractError("conflict reducer flattened every dissenter")
    expected_wildcards = {
        result["branch_id"]
        for result in packet["branch_results"]
        if result.get("is_wildcard")
    }
    if expected_wildcards != set(
        packet["merge_proposal"]["retained_wildcard_ids"]
    ):
        raise ContractError(
            "merge proposal failed to retain every valid protected wildcard"
        )
    expected_frontier = {
        result["branch_id"]
        for result in packet["branch_results"]
        if result["semantic_delta"]["material"]
    }
    if expected_frontier != set(packet["merge_proposal"]["pareto_frontier_ids"]):
        raise ContractError("Pareto frontier trusts a non-derived learning claim")
    expected_learning_count = sum(
        result["semantic_delta"]["material"]
        and result["literature_status"] in {"current", "rebased"}
        for result in packet["branch_results"]
    )
    if packet["portfolio_metrics"]["independent_learning_count"] != expected_learning_count:
        raise ContractError("independent learning count is not semantic-delta derived")
    control = packet["portfolio_metrics"].get("matched_budget_control")
    if not isinstance(control, Mapping):
        raise ContractError("matched-budget control receipt is missing")
    if control.get("content_digest") != canonical_digest(
        _without(control, "content_digest")
    ):
        raise ContractError("matched-budget control digest mismatch")
    control_authorized = bool(
        control.get("status") == "completed"
        and control.get("allocation_matches_full_condition") is True
    )
    if packet["portfolio_metrics"].get(
        "matched_budget_comparison_authorized"
    ) is not control_authorized:
        raise ContractError("matched-budget comparison authority is inconsistent")
    baseline_coverage = int(control.get("structural_corner_coverage", 0))
    if packet["portfolio_metrics"][
        "matched_budget_baseline_corner_coverage"
    ] != baseline_coverage:
        raise ContractError("baseline coverage was not derived from executed control")
    expected_improvement = bool(
        control_authorized
        and packet["portfolio_metrics"]["conceptual_corner_coverage"]
        > baseline_coverage
    )
    if packet["portfolio_metrics"]["matched_budget_improvement"] is not expected_improvement:
        raise ContractError("matched-budget improvement was not derived from control")
    for receipt in packet["attempt_receipts"]:
        request = requests.get(receipt["branch_id"])
        if request is None:
            raise ContractError("attempt receipt names an unknown branch")
        usage = receipt["resource_usage"]
        if (
            usage.get("cost_units", 0) > request["budget"]["cost_units"]
            or usage.get("storage_bytes", 0)
            > request["budget"]["storage_bytes"]
        ):
            raise ContractError(
                "attempt receipt exceeds its frozen branch resource budget"
            )
    if packet["portfolio_metrics"]["worker_count_is_progress"]:
        raise ContractError("worker count alone cannot count as discovery progress")


__all__ = [
    "build_parallel_manifest",
    "run_bounded_killable_request_wave",
    "run_parallel_hypothesis_portfolio",
    "validate_parallel_manifest",
    "validate_parallel_portfolio",
]
