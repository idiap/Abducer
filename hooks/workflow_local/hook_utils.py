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

"""Shared deterministic hook helpers."""

from __future__ import annotations

import fnmatch
import hashlib
import json
import os
import sys
import tempfile
import datetime as dt
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
TRACE_DIR = ROOT / "agentic" / "traces" / "hook_runs"
DESTRUCTIVE_COMMAND_MARKERS = ("rm -rf", "git reset --hard", "git checkout --", "mkfs", "dd if=")
PROTECTED_PREFIXES = ("agentic/", "registry/", "hooks/", "skills/control-plane/looper-", "docs/looper-")
WORKFLOW_REGISTRY = ROOT / "agentic" / "registries" / "workflow_contracts.yaml"
NAMED_WORKFLOW_REGISTRY = ROOT / "agentic" / "registries" / "named_workflow_contracts.yaml"


def read_payload() -> dict:
    text = sys.stdin.read().strip()
    if not text:
        return {}
    try:
        payload = json.loads(text)
    except json.JSONDecodeError:
        return {"raw": text}
    return payload if isinstance(payload, dict) else {"payload": payload}


def emit(**payload: object) -> None:
    print(json.dumps(payload, sort_keys=True))


def trace(hook_name: str, payload: dict, result: dict) -> None:
    if os.environ.get("ABDUCER_DISABLE_HOOK_TRACE", "").lower() in {"1", "true", "yes"}:
        return
    TRACE_DIR.mkdir(parents=True, exist_ok=True)
    legacy_view = {"hook": hook_name, "payload": payload, "result": result}
    path = TRACE_DIR / f"latest-{hook_name}.json"
    # Preserve the exact legacy view while publishing it atomically.
    fd, raw_tmp = tempfile.mkstemp(prefix=f".{path.name}.", dir=TRACE_DIR)
    tmp = Path(raw_tmp)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as stream:
            stream.write(json.dumps(legacy_view, indent=2, sort_keys=True) + "\n")
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(tmp, path)
    finally:
        if tmp.exists():
            tmp.unlink()

    # Tracing is observability-only: a store failure must never change a hook
    # allow/block decision. Only bounded summaries and references are copied.
    try:
        scripts_dir = ROOT / "agentic" / "scripts"
        if str(scripts_dir) not in sys.path:
            sys.path.insert(0, str(scripts_dir))
        from public_reasoning_trace_store import append_event

        receipt = payload.get("activation_receipt")
        receipt = receipt if isinstance(receipt, dict) else {}
        workflow_id = str(payload.get("workflow_id") or result.get("workflow_id") or "uncontrolled").strip()
        workflow_version = str(payload.get("workflow_version") or "unversioned").strip()
        target = str(payload.get("target", payload.get("target_id", "unspecified"))).strip() or "unspecified"
        run_id = str(payload.get("run_id") or payload.get("trace_run_id") or receipt.get("id") or "hook-unscoped").strip()
        decision = str(result.get("decision", "observed")).strip()
        family_by_hook = {
            "user_prompt_submit_intake": "activation",
            "pre_skill_use_policy": "authorization",
            "post_skill_use_review": "validation",
            "pre_tool_use_policy": "tool_control",
            "stop_artifact_check": "exit",
        }
        family = family_by_hook.get(hook_name, "authorization")
        disposition = {
            "accept": "accepted",
            "warn": "warned",
            "block": "blocked",
            "fail": "failed",
        }.get(decision, "observed")
        artifact_status = "not_checked"
        if hook_name == "post_skill_use_review":
            artifact_status = "integrity_valid" if decision == "accept" else "integrity_invalid"
        attempt = int(payload.get("attempt", 1) or 1)
        step_id = payload.get("step_id", payload.get("step"))
        idempotency_material = {
            "hook": hook_name,
            "run_id": run_id,
            "workflow_id": workflow_id,
            "step_id": step_id,
            "skill": payload.get("skill"),
            "attempt": attempt,
            "decision": decision,
        }
        event_id = "evt-hook-" + hashlib.sha256(
            json.dumps(idempotency_material, sort_keys=True, separators=(",", ":")).encode("utf-8")
        ).hexdigest()[:24]
        evidence = []
        raw_paths = payload.get("expected_artifacts", [])
        if isinstance(raw_paths, str):
            raw_paths = [raw_paths]
        digests = result.get("receipt", {}).get("artifact_digests", {}) if isinstance(result.get("receipt"), dict) else {}
        for raw in raw_paths if isinstance(raw_paths, list) else []:
            raw_s = str(raw)
            if safe_repo_artifact(raw_s) is not None:
                evidence.append({
                    "relation": "background",
                    "path": raw_s,
                    "digest": digests.get(raw_s),
                    "receipt_id": result.get("receipt", {}).get("id") if isinstance(result.get("receipt"), dict) else None,
                    "artifact_type": str(payload.get("output_type", payload.get("artifact_type", "artifact"))) or "artifact",
                    "external": False,
                })
        trace_root = os.environ.get("ABDUCER_PUBLIC_REASONING_TRACE_ROOT", "").strip()
        stored = append_event(
            {
                "schema_version": "2.0.0",
                "event_id": event_id,
                "run_id": run_id,
                "workflow_id": workflow_id,
                "workflow_version": workflow_version,
                "profile_id": payload.get("profile_id"),
                "target": target,
                "activation_receipt_id": receipt.get("id"),
                "timestamp_utc": dt.datetime.now(dt.UTC).isoformat(),
                "phase": hook_name,
                "step_id": str(step_id) if step_id not in (None, "") else None,
                "skill": str(payload.get("skill")) if payload.get("skill") else None,
                "attempt": attempt,
                "branch": str(payload.get("branch")) if payload.get("branch") else None,
                "event_family": family,
                "causal_parent_event_ids": list(payload.get("trace_parent_event_ids", [])) if isinstance(payload.get("trace_parent_event_ids", []), list) else [],
                "parent_artifact_ids": list(payload.get("parent_artifact_ids", [])) if isinstance(payload.get("parent_artifact_ids", []), list) else [],
                "artifact_validation_status": artifact_status,
                "claim_epistemic_status": "not_applicable",
                "workflow_disposition": disposition,
                "public_inference": {
                    "question": "",
                    "premises": [],
                    "operator": "control_plane_decision",
                    "warrant": str(result.get("reason", "")),
                    "conclusion": decision,
                    "assumptions": [],
                    "alternatives": [],
                    "falsifiers": [],
                    "uncertainty": "Control bookkeeping supplies no scientific claim authority.",
                    "scope": {"regime": "control-plane", "model": "", "before": "", "after": ""},
                    "trace_completeness": "not_applicable",
                },
                "evidence": evidence,
                "authority": {
                    "exercised": [f"hook:{hook_name}"],
                    "absent": ["scientific_correctness", "novelty", "proof_acceptance"],
                    "prohibitions_checked": ["no_control_to_epistemic_promotion"],
                },
                "control": {
                    "decision": decision,
                    "reason": str(result.get("reason", "")),
                    "output_epistemic_status": str(result.get("epistemic_status", payload.get("epistemic_status", ""))),
                    "gate_status": str(payload.get("gate_status", "")),
                    "open_obligation_count": len(payload.get("open_obligations", [])) if isinstance(payload.get("open_obligations", []), list) else 0,
                    "downstream_consequence": str(result.get("downstream_consequence", "")),
                },
                "idempotency_key": event_id,
            },
            store_root=Path(trace_root) if trace_root else ROOT / "agentic" / "traces" / "public_reasoning",
            latest_name=hook_name,
            link_to_latest=True,
        )
        # A reasoned conditional N/A is a first-class lifecycle observation,
        # not a successful skill execution and not an omitted row.
        skipped_rows = payload.get("skipped_steps", [])
        if hook_name == "pre_skill_use_policy" and isinstance(skipped_rows, list):
            for index, row in enumerate(skipped_rows):
                if not isinstance(row, dict) or not row.get("step_id") or not row.get("reason"):
                    continue
                skip = dict(stored)
                skip.pop("sequence", None)
                skip.pop("timestamp_utc", None)
                skip["event_id"] = "evt-skip-" + hashlib.sha256(
                    f"{run_id}|{row['step_id']}|{row['reason']}|{index}".encode("utf-8")
                ).hexdigest()[:24]
                skip["phase"] = "conditional_skip"
                skip["step_id"] = str(row["step_id"])
                skip["skill"] = str(row.get("skill")) if row.get("skill") else None
                skip["event_family"] = "skip"
                skip["causal_parent_event_ids"] = [str(stored["event_id"])]
                skip["artifact_validation_status"] = "not_checked"
                skip["claim_epistemic_status"] = "not_applicable"
                skip["workflow_disposition"] = "skipped"
                skip["public_inference"] = {
                    "question": "",
                    "premises": [],
                    "operator": "conditional_disposition",
                    "warrant": str(row["reason"]),
                    "conclusion": "skipped",
                    "assumptions": [], "alternatives": [], "falsifiers": [],
                    "uncertainty": "A skip records workflow disposition, not scientific correctness.",
                    "scope": {"regime": "control-plane", "model": "", "before": "", "after": ""},
                    "trace_completeness": "not_applicable",
                }
                skip["evidence"] = []
                skip["control"] = {"decision": "skip", "reason": str(row["reason"])}
                skip["idempotency_key"] = skip["event_id"]
                stored = append_event(
                    skip,
                    store_root=Path(trace_root) if trace_root else ROOT / "agentic" / "traces" / "public_reasoning",
                    latest_name="conditional_skip",
                )
    except Exception:
        # Do not create a second observability channel here: hooks may run in
        # constrained hosts. The compatibility view above remains available.
        pass


def protected_path(raw: str) -> bool:
    return any(str(raw).startswith(prefix) for prefix in PROTECTED_PREFIXES)


def has_evidence_marker(payload: dict) -> bool:
    text = json.dumps(payload, sort_keys=True).lower()
    return "lint-" in text or "todo" in text or "decision" in text or "evidence" in text


def _load_object(path: Path) -> dict[str, Any]:
    """Load the repository's JSON-compatible YAML registries."""

    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}
    return value if isinstance(value, dict) else {}


def workflow_contracts() -> dict[str, dict[str, Any]]:
    """Return canonical workflows, tolerating both legacy and split registries."""

    root = _load_object(WORKFLOW_REGISTRY)
    documents = [root]
    # Version 2 may use an explicit pointer.  Keep the conventional path as a
    # fallback so hooks do not depend on the projection mechanism.
    pointer = (
        root.get("named_workflow_contracts")
        or root.get("named_workflow_registry")
        or root.get("named_workflows_path")
    )
    named_path = ROOT / str(pointer) if pointer else NAMED_WORKFLOW_REGISTRY
    if named_path != WORKFLOW_REGISTRY and named_path.exists():
        documents.append(_load_object(named_path))

    contracts: dict[str, dict[str, Any]] = {}
    for document in documents:
        rows = document.get("workflows", document.get("named_workflows", []))
        if not isinstance(rows, list):
            continue
        for row in rows:
            if isinstance(row, dict) and row.get("id"):
                contracts[str(row["id"])] = row
                for alias in row.get("aliases", []):
                    contracts.setdefault(str(alias), row)
    return contracts


def matching_named_workflows(trigger_facts: dict[str, Any]) -> list[dict[str, Any]]:
    """Return canonical workflows whose deterministic trigger facts match.

    Prompt intake may recommend these workflows, but recommendation is not an
    activation receipt and cannot authorize a later skill invocation.
    """

    matches: list[dict[str, Any]] = []
    seen: set[str] = set()
    for workflow in workflow_contracts().values():
        workflow_id = str(workflow.get("id", ""))
        if not workflow_id or workflow_id in seen or not workflow.get("version"):
            continue
        seen.add(workflow_id)
        trigger = workflow.get("trigger")
        if not isinstance(trigger, dict):
            continue
        all_of = [str(item) for item in trigger.get("all_of", [])]
        any_of = [str(item) for item in trigger.get("any_of", [])]
        none_of = [str(item) for item in trigger.get("none_of", [])]
        if not all(bool(trigger_facts.get(fact)) for fact in all_of):
            continue
        if any_of and not any(bool(trigger_facts.get(fact)) for fact in any_of):
            continue
        if any(bool(trigger_facts.get(fact)) for fact in none_of):
            continue
        matches.append(
            {
                "workflow_id": workflow_id,
                "workflow_version": workflow["version"],
                "activation": workflow.get("activation"),
                "cost_profile": workflow.get("cost_profile"),
                "matched_facts": sorted(
                    fact for fact in {*all_of, *any_of} if trigger_facts.get(fact)
                ),
            }
        )
    return sorted(matches, key=lambda row: row["workflow_id"])


def workflow_context(
    payload: dict[str, Any], *, require_step: bool = True
) -> tuple[dict[str, Any] | None, dict[str, Any] | None, str | None]:
    """Resolve and validate workflow identity, target, and step from a payload."""

    workflow_id = str(payload.get("workflow_id", "")).strip()
    if not workflow_id:
        return None, None, "Controlled invocation requires `workflow_id`."
    workflow = workflow_contracts().get(workflow_id)
    if workflow is None:
        return None, None, f"Unknown workflow `{workflow_id}`."

    supplied_version = str(payload.get("workflow_version", "")).strip()
    expected_version = str(workflow.get("version", "")).strip()
    if not supplied_version:
        return workflow, None, "Controlled invocation requires `workflow_version`."
    if expected_version and supplied_version != expected_version:
        return workflow, None, f"Workflow version mismatch: expected `{expected_version}`, got `{supplied_version}`."

    active = workflow
    profile_ref = str(payload.get("profile_id", "")).strip()
    if profile_ref:
        profiles = workflow.get("profiles", [])
        profile = next(
            (
                row
                for row in profiles
                if isinstance(row, dict)
                and profile_ref in {str(row.get("id", "")), *(str(alias) for alias in row.get("aliases", []))}
            ),
            None,
        )
        if profile is None:
            return workflow, None, f"Unknown profile `{profile_ref}` for workflow `{workflow_id}`."
        profile_version = str(payload.get("profile_version", "")).strip()
        expected_profile_version = str(profile.get("version", "")).strip()
        if not profile_version:
            return workflow, None, "Profile invocation requires `profile_version`."
        if expected_profile_version and profile_version != expected_profile_version:
            return workflow, None, (
                f"Profile version mismatch: expected `{expected_profile_version}`, got `{profile_version}`."
            )
        activation = payload.get("profile_activation_evidence")
        if not isinstance(activation, dict) or not activation or activation.get("activated") is False:
            return workflow, None, "Profile invocation requires activated, structured `profile_activation_evidence`."
        active = dict(workflow)
        active["target_scope"] = profile.get("target_scope", workflow.get("target_scope", ["*"]))
        profile_steps = list(profile.get("steps", []))
        tail_ref = str(profile.get("validation_tail_start", "")).strip()
        if tail_ref:
            base_steps = workflow.get("steps", [])
            tail_index = next(
                (
                    index
                    for index, row in enumerate(base_steps)
                    if isinstance(row, dict)
                    and tail_ref in {str(row.get("id", "")), str(row.get("order", ""))}
                ),
                None,
            )
            if tail_index is not None:
                profile_steps.extend(base_steps[tail_index:])
        active["steps"] = profile_steps
        active["_active_profile_id"] = profile.get("id")
        active["_active_profile"] = profile

    target = str(payload.get("target", payload.get("target_id", ""))).strip()
    if not target:
        return workflow, None, "Controlled invocation requires `target`."
    target_class = str(payload.get("target_class", "")).strip()
    scope = active.get("target_scope", ["*"])
    if isinstance(scope, str):
        scope = [scope]
    if scope and isinstance(scope, list):
        patterns = [str(item) for item in scope]
        candidates = [target, target_class] if target_class else [target]
        if not any(
            pattern in {"*", "all", "any"}
            or any(fnmatch.fnmatchcase(candidate, pattern) for candidate in candidates)
            for pattern in patterns
        ):
            return workflow, None, f"Target `{target}` is outside workflow `{workflow_id}` scope."

    steps = active.get("steps", [])
    step_ref = payload.get("step_id", payload.get("step"))
    if not require_step:
        return active, None, None
    if step_ref in (None, ""):
        return workflow, None, "Controlled invocation requires `step_id`."
    step = next(
        (
            row
            for row in steps
            if isinstance(row, dict)
            and str(step_ref) in {str(row.get("id", "")), str(row.get("order", ""))}
        ),
        None,
    )
    if step is None and profile_ref:
        profile = active["_active_profile"]
        skill = str(payload.get("skill", ""))
        specialist_refs = {"specialist", skill, f"specialist:{skill}"}
        if skill in {str(item) for item in profile.get("specialist_skills", [])} and str(step_ref) in specialist_refs:
            prerequisite_ids: list[str] = []
            after_ref = str(profile.get("specialist_after", "")).strip()
            for profile_step in profile.get("steps", []):
                if not isinstance(profile_step, dict):
                    continue
                prerequisite_ids.append(str(profile_step.get("id", profile_step.get("order", ""))))
                if after_ref and after_ref in {
                    str(profile_step.get("id", "")),
                    str(profile_step.get("order", "")),
                }:
                    break
            step = {
                "id": f"specialist:{skill}",
                "skill": skill,
                "mode": "profile_specialist",
                "produces": [profile.get("specialist_output", "ResultCandidatePacket")],
                "prerequisites": prerequisite_ids,
            }
    if step is None:
        return workflow, None, f"Step `{step_ref}` is not declared by workflow `{workflow_id}`."
    return active, step, None


def declared_types(step: dict[str, Any], field: str) -> set[str]:
    values = step.get(field, [])
    if isinstance(values, (str, dict)):
        values = [values]
    result: set[str] = set()
    for value in values if isinstance(values, list) else []:
        if isinstance(value, dict):
            value = value.get("type", value.get("artifact_type", ""))
        if value:
            result.add(str(value))
    return result


def safe_repo_artifact(raw: object) -> Path | None:
    path = Path(str(raw))
    if path.is_absolute() or ".." in path.parts:
        return None
    resolved = (ROOT / path).resolve()
    return resolved if resolved == ROOT or ROOT in resolved.parents else None


def receipt_id(payload: dict[str, Any], decision: str) -> str:
    material = json.dumps({"payload": payload, "decision": decision}, sort_keys=True, separators=(",", ":"))
    return "hook-receipt-" + hashlib.sha256(material.encode("utf-8")).hexdigest()[:16]


def _content_id(prefix: str, payload: dict[str, Any]) -> str:
    material = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    return prefix + hashlib.sha256(material.encode("utf-8")).hexdigest()[:16]


def make_activation_receipt(
    *,
    workflow_id: str,
    workflow_version: str,
    target: str,
    target_class: str,
    trigger_facts: dict[str, Any],
    authorized_by: str,
    evidence: dict[str, Any],
) -> dict[str, Any]:
    """Create the deterministic activation receipt expected by controlled hooks."""

    receipt: dict[str, Any] = {
        "status": "activated",
        "workflow_id": workflow_id,
        "workflow_version": workflow_version,
        "target": target,
        "target_class": target_class,
        "trigger_facts": trigger_facts,
        "authorized_by": authorized_by,
        "evidence": evidence,
    }
    receipt["id"] = _content_id("workflow-activation-", receipt)
    return receipt


def validate_activation_receipt(
    payload: dict[str, Any], workflow: dict[str, Any]
) -> str | None:
    """Return an error when controlled execution lacks a bound activation receipt."""

    receipt = payload.get("activation_receipt")
    if not isinstance(receipt, dict):
        return "Controlled workflow execution requires a structured `activation_receipt`."
    expected = {
        "status": "activated",
        "workflow_id": str(workflow.get("id", "")),
        "workflow_version": str(workflow.get("version", "")),
        "target": str(payload.get("target", payload.get("target_id", ""))).strip(),
        "target_class": str(payload.get("target_class", "")).strip(),
        "trigger_facts": receipt.get("trigger_facts"),
        "authorized_by": receipt.get("authorized_by"),
        "evidence": receipt.get("evidence"),
    }
    if any(receipt.get(key) != value for key, value in expected.items()):
        return "Activation receipt is not bound to the active workflow version and target."
    if not isinstance(receipt.get("trigger_facts"), dict):
        return "Activation receipt requires structured trigger facts."
    if not str(receipt.get("authorized_by", "")).strip():
        return "Activation receipt requires a named authorizer."
    if not isinstance(receipt.get("evidence"), dict) or not receipt["evidence"]:
        return "Activation receipt requires explicit activation evidence."
    unsigned = {key: value for key, value in receipt.items() if key != "id"}
    if receipt.get("id") != _content_id("workflow-activation-", unsigned):
        return "Activation receipt content digest is invalid."
    return None


def make_skill_receipt(fields: dict[str, Any]) -> dict[str, Any]:
    """Bind a post-skill receipt to its workflow, target, producer, and artifacts."""

    receipt = dict(fields)
    receipt["id"] = _content_id("hook-receipt-", receipt)
    return receipt


def valid_skill_receipt(
    receipt: object,
    *,
    workflow: dict[str, Any],
    target: str,
) -> bool:
    if not isinstance(receipt, dict) or receipt.get("status") != "accepted":
        return False
    if receipt.get("workflow_id") != workflow.get("id"):
        return False
    if receipt.get("workflow_version") != workflow.get("version"):
        return False
    if receipt.get("target") != target:
        return False
    if not receipt.get("step_id") or not receipt.get("skill") or not receipt.get("artifact_type"):
        return False
    paths = receipt.get("artifact_paths")
    digests = receipt.get("artifact_digests")
    if not isinstance(paths, list) or not paths or not isinstance(digests, dict):
        return False
    if any(path not in digests for path in paths):
        return False
    for raw in paths:
        artifact = safe_repo_artifact(raw)
        if artifact is None or not artifact.exists() or digests.get(raw) != file_digest(artifact):
            return False
    unsigned = {key: value for key, value in receipt.items() if key != "id"}
    return receipt.get("id") == _content_id("hook-receipt-", unsigned)


def file_digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def validate_artifact_envelope(
    envelope: object,
    *,
    workflow: dict[str, Any],
    target: str,
    output_type: str,
    epistemic_status: str,
) -> str | None:
    """Validate the shared named-workflow envelope and its binding fields."""

    if not isinstance(envelope, dict):
        return "Named-workflow artifacts must contain a JSON object envelope."
    required = {
        "artifact_type",
        "workflow_id",
        "workflow_version",
        "target",
        "epistemic_status",
        "payload",
    }
    allowed = required | {"provenance"}
    if required - set(envelope):
        return "Named-workflow artifact envelope is missing required fields."
    if set(envelope) - allowed:
        return "Named-workflow artifact envelope has undeclared fields."
    expected = {
        "artifact_type": output_type,
        "workflow_id": workflow.get("id"),
        "workflow_version": workflow.get("version"),
        "target": target,
        "epistemic_status": epistemic_status,
    }
    if any(envelope.get(key) != value for key, value in expected.items()):
        return "Named-workflow artifact envelope is not bound to the completion context."
    if not isinstance(envelope.get("payload"), dict):
        return "Named-workflow artifact payload must be an object."
    provenance = envelope.get("provenance", [])
    if not isinstance(provenance, list) or any(not isinstance(item, str) or not item for item in provenance):
        return "Named-workflow artifact provenance must be a list of non-empty strings."
    return None
