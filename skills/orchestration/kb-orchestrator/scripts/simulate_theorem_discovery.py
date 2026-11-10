#!/usr/bin/env python3
# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT

"""Iteratively refine the generative pipeline to replicate theorem-discovery trajectories.

This script performs an optimization loop over orchestration parameters. Each
iteration runs the core generative stages and scores how well the resulting
artifacts reproduce a ground-truth discovery trajectory (statement order,
bridges, and hypothesis support) for a target theorem.
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import re
import sys
from collections import Counter, deque
from pathlib import Path
from typing import Any

import yaml

_COMMON_DIR = Path(__file__).resolve().parents[3] / "common"
if str(_COMMON_DIR) not in sys.path:
    sys.path.insert(0, str(_COMMON_DIR))

from kb_context import canonical_artifacts_dir
from kb_context import resolve_kb_reference
from reasoning_log import ReasoningLogger


STATEMENT_BLOCK_PATTERN = r"```yaml\n(.*?)\n```"
PROOF_STRUCTURE_KINDS = {
    "theorem",
    "lemma",
    "corollary",
    "observation",
    "proposition",
    "derived-construction",
}


def _safe_float(value: Any, default: float = 0.0) -> float:
    """
    Relevance: Operates within the orchestration and observability layer.
    Concept: Defensive conversion/parsing to keep scoring and reporting robust.
    Contribution: Reduces runtime ambiguity and prevents malformed artifacts from destabilizing the workflow.
    """

    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def _load_json(path: Path) -> dict[str, Any]:
    """
    Relevance: Operates within the orchestration and observability layer.
    Concept: Loading and structuring external artifacts for deterministic processing.
    Contribution: Provides clean, typed inputs so downstream scoring stays auditable.
    """

    if not path.exists():
        return {}
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}
    return payload if isinstance(payload, dict) else {}


def _load_yaml(path: Path) -> dict[str, Any]:
    """
    Relevance: Operates within the orchestration and observability layer.
    Concept: Loading and structuring external artifacts for deterministic processing.
    Contribution: Provides clean, typed inputs so downstream scoring stays auditable.
    """

    if not path.exists():
        return {}
    try:
        payload = yaml.safe_load(path.read_text(encoding="utf-8"))
    except Exception:
        return {}
    return payload if isinstance(payload, dict) else {}


def _extract_statements(kb_path: Path) -> dict[str, dict[str, Any]]:
    """
    Relevance: Operates within the orchestration and observability layer.
    Concept: Extraction of structured signals from raw text or artifact payloads.
    Contribution: Recovers theorem/dependency structure required to define and score discovery trajectories.
    """

    import re

    content = kb_path.read_text(encoding="utf-8")
    out: dict[str, dict[str, Any]] = {}
    for match in re.finditer(STATEMENT_BLOCK_PATTERN, content, re.DOTALL):
        try:
            payload = yaml.safe_load(match.group(1))
        except yaml.YAMLError:
            continue
        if not isinstance(payload, dict):
            continue
        sid = str(payload.get("id", "")).strip()
        if not sid:
            continue
        deps = payload.get("depends_on", [])
        payload["depends_on"] = [str(x).strip() for x in deps if str(x).strip()] if isinstance(deps, list) else []
        out[sid] = payload
    return out


def _load_statement_blocks(kb_path: Path) -> tuple[str, list[dict[str, Any]]]:
    """
    Relevance: Operates within the orchestration and observability layer.
    Concept: Structured loading of fenced statement blocks together with source offsets.
    Contribution: Enables proof-structure knockout without destroying surrounding KB prose or metadata.
    """

    import re

    content = kb_path.read_text(encoding="utf-8")
    blocks: list[dict[str, Any]] = []
    for match in re.finditer(STATEMENT_BLOCK_PATTERN, content, re.DOTALL):
        try:
            payload = yaml.safe_load(match.group(1))
        except yaml.YAMLError:
            continue
        if not isinstance(payload, dict):
            continue
        sid = str(payload.get("id", "")).strip()
        if not sid:
            continue
        blocks.append(
            {
                "id": sid,
                "payload": payload,
                "start": match.start(),
                "end": match.end(),
            }
        )
    return content, blocks


def _empty_field_value(field: str) -> Any:
    """
    Relevance: Operates within the orchestration and observability layer.
    Concept: Deterministic masking of structured theorem metadata.
    Contribution: Lets knockout plans remove proof knowledge while keeping YAML schemas valid.
    """

    if field in {"depends_on", "source_ids", "used_symbols", "concept_roles", "bridge_roles", "method_tags"}:
        return []
    return ""


def _redact_text_terms(value: Any, terms: list[str]) -> tuple[Any, int]:
    """
    Relevance: Operates within the orchestration and observability layer.
    Concept: Deterministic redaction of hidden bridge-concept mentions.
    Contribution: Supports simulated ignorance by masking a central concept while leaving the surrounding theorem structure intact.
    """

    text = str(value or "")
    total = 0
    for term in terms:
        needle = str(term).strip()
        if not needle:
            continue
        pattern = re.compile(re.escape(needle), re.IGNORECASE)
        text, count = pattern.subn("[hidden bridge concept]", text)
        total += count
    return text, total


def _parse_edge_spec(value: str) -> tuple[str, str]:
    """
    Relevance: Operates within the orchestration and observability layer.
    Concept: Stable parsing of user-provided edge knockout specs.
    Contribution: Supports precise removal of proof dependencies from the working KB.
    """

    text = str(value).strip()
    if "->" in text:
        left, right = text.split("->", 1)
    elif ":" in text:
        left, right = text.split(":", 1)
    else:
        return "", ""
    return left.strip(), right.strip()


def _build_knockout_spec(
    statements: dict[str, dict[str, Any]],
    target_statement_id: str,
    profile: str,
    knockout_statements: list[str],
    knockout_edges: list[str],
    knockout_fields: list[str],
    bridge_concept_ids: list[str],
    bridge_concept_terms: list[str],
) -> dict[str, Any]:
    """
    Relevance: Operates within the orchestration and observability layer.
    Concept: Construction of a declarative ignorance model over the KB.
    Contribution: Encodes which proof relations remain hidden from the discovery agents during simulation.
    """

    profile_l = str(profile or "none").strip().lower()
    spec: dict[str, Any] = {
        "profile": profile_l or "none",
        "removed_statements": set(),
        "drop_edges": set(),
        "blank_fields": {},
        "redact_text_fields": {},
        "redact_terms": [str(term).strip() for term in bridge_concept_terms if str(term).strip()],
        "bridge_concept_ids": [str(item).strip() for item in bridge_concept_ids if str(item).strip()],
    }

    if profile_l in {"proof-structure", "hille-yosida-proof"}:
        for sid, payload in statements.items():
            kind = str(payload.get("kind", "")).strip().lower()
            if kind in PROOF_STRUCTURE_KINDS:
                spec["blank_fields"].setdefault(sid, set()).update({"depends_on", "proof_sketch", "notes", "bridge_roles"})
        # Keep the target statement visible as the discovery objective but hide the authored proof path.
        spec["blank_fields"].setdefault(str(target_statement_id).strip(), set()).update({"depends_on", "proof_sketch", "notes", "bridge_roles"})

    if profile_l == "target-proof":
        spec["blank_fields"].setdefault(str(target_statement_id).strip(), set()).update({"depends_on", "proof_sketch", "notes", "bridge_roles"})

    if profile_l in {"bridge-concept", "stone-bridge-concept"}:
        concept_id_set = {str(item).strip().lower() for item in bridge_concept_ids if str(item).strip()}
        concept_term_set = {str(item).strip().lower() for item in bridge_concept_terms if str(item).strip()}
        for sid, payload in statements.items():
            sid_l = sid.lower()
            kind = str(payload.get("kind", "")).strip().lower()
            concept_roles = [str(item).strip().lower() for item in payload.get("concept_roles", []) if str(item).strip()] if isinstance(payload.get("concept_roles"), list) else []
            bridge_roles = [str(item).strip().lower() for item in payload.get("bridge_roles", []) if str(item).strip()] if isinstance(payload.get("bridge_roles"), list) else []
            text_blob = " ".join(
                [
                    sid_l,
                    " ".join(concept_roles),
                    " ".join(bridge_roles),
                    str(payload.get("informal", "")),
                    str(payload.get("notes", "")),
                    str(payload.get("latex", "")),
                ]
            ).lower()
            matches_id = bool(concept_id_set.intersection(concept_roles + bridge_roles + [sid_l]))
            matches_term = any(term in text_blob for term in concept_term_set)
            if not matches_id and not matches_term:
                continue
            spec["blank_fields"].setdefault(sid, set()).update({"concept_roles", "bridge_roles", "notes", "proof_sketch"})
            if sid != str(target_statement_id).strip():
                spec["redact_text_fields"].setdefault(sid, set()).add("informal")
            if kind == "definition" and sid != str(target_statement_id).strip():
                spec["removed_statements"].add(sid)

    for sid in knockout_statements:
        text = str(sid).strip()
        if text:
            spec["removed_statements"].add(text)
    for edge in knockout_edges:
        src, dst = _parse_edge_spec(edge)
        if src and dst:
            spec["drop_edges"].add((src, dst))
    for item in knockout_fields:
        text = str(item).strip()
        if not text or ":" not in text:
            continue
        sid, field = text.split(":", 1)
        sid = sid.strip()
        field = field.strip()
        if sid and field:
            spec["blank_fields"].setdefault(sid, set()).add(field)

    return spec


def _materialize_knockout_kb(
    kb_path: Path,
    output_dir: Path,
    target_statement_id: str,
    profile: str,
    knockout_statements: list[str],
    knockout_edges: list[str],
    knockout_fields: list[str],
    bridge_concept_ids: list[str],
    bridge_concept_terms: list[str],
) -> tuple[Path, dict[str, Any]]:
    """
    Relevance: Operates within the orchestration and observability layer.
    Concept: Construction of a working KB under simulated ignorance.
    Contribution: Separates the KB used by the agents from the fully known KB used for ground-truth evaluation.
    """

    content, blocks = _load_statement_blocks(kb_path)
    statements = _extract_statements(kb_path)
    spec = _build_knockout_spec(
        statements=statements,
        target_statement_id=target_statement_id,
        profile=profile,
        knockout_statements=knockout_statements,
        knockout_edges=knockout_edges,
        knockout_fields=knockout_fields,
        bridge_concept_ids=bridge_concept_ids,
        bridge_concept_terms=bridge_concept_terms,
    )
    removed_statements = set(spec.get("removed_statements", set()))
    drop_edges = set(spec.get("drop_edges", set()))
    blank_fields = {sid: set(fields) for sid, fields in (spec.get("blank_fields", {}) or {}).items()}
    redact_text_fields = {sid: set(fields) for sid, fields in (spec.get("redact_text_fields", {}) or {}).items()}
    redact_terms = [str(term).strip() for term in spec.get("redact_terms", []) if str(term).strip()]

    output_dir.mkdir(parents=True, exist_ok=True)
    out_path = output_dir / kb_path.name

    parts: list[str] = []
    cursor = 0
    blanked_fields_count = 0
    dropped_edges_count = 0
    redacted_mentions_count = 0
    for block in blocks:
        parts.append(content[cursor : int(block["start"])])
        cursor = int(block["end"])
        sid = str(block["id"])
        if sid in removed_statements:
            continue

        payload = dict(block["payload"])
        for field in sorted(blank_fields.get(sid, set())):
            if field in payload:
                payload[field] = _empty_field_value(field)
                blanked_fields_count += 1
        if isinstance(payload.get("depends_on"), list):
            filtered: list[str] = []
            for dep in payload.get("depends_on", []):
                dep_s = str(dep).strip()
                if not dep_s:
                    continue
                if dep_s in removed_statements:
                    dropped_edges_count += 1
                    continue
                if (dep_s, sid) in drop_edges:
                    dropped_edges_count += 1
                    continue
                filtered.append(dep_s)
            payload["depends_on"] = filtered
        for field in sorted(redact_text_fields.get(sid, set())):
            if field in payload:
                payload[field], count = _redact_text_terms(payload.get(field, ""), redact_terms)
                redacted_mentions_count += count

        block_yaml = yaml.safe_dump(payload, sort_keys=False).rstrip()
        parts.append(f"```yaml\n{block_yaml}\n```")

    parts.append(content[cursor:])
    out_path.write_text("".join(parts), encoding="utf-8")

    summary = {
        "profile": str(profile or "none").strip().lower() or "none",
        "working_kb": str(out_path),
        "removed_statements": sorted(removed_statements),
        "drop_edges": [{"from_id": src, "to_id": dst} for src, dst in sorted(drop_edges)],
        "blank_fields": {sid: sorted(fields) for sid, fields in sorted(blank_fields.items())},
        "redact_text_fields": {sid: sorted(fields) for sid, fields in sorted(redact_text_fields.items())},
        "bridge_concept_ids": [str(item).strip() for item in spec.get("bridge_concept_ids", []) if str(item).strip()],
        "bridge_concept_terms": redact_terms,
        "blanked_fields_count": blanked_fields_count,
        "dropped_edges_count": dropped_edges_count,
        "redacted_mentions_count": redacted_mentions_count,
    }
    return out_path, summary


def _topo_order(nodes: set[str], deps: dict[str, list[str]]) -> list[str]:
    """
    Relevance: Operates within the orchestration and observability layer.
    Concept: Construction of derived graph/model structures used by later stages.
    Contribution: Computes a canonical dependency-respecting discovery order for ground-truth inference.
    """

    indeg: dict[str, int] = {n: 0 for n in nodes}
    adj: dict[str, set[str]] = {n: set() for n in nodes}
    for n in nodes:
        for d in deps.get(n, []):
            if d in nodes:
                indeg[n] += 1
                adj[d].add(n)
    queue = deque(sorted([n for n, k in indeg.items() if k == 0]))
    out: list[str] = []
    while queue:
        n = queue.popleft()
        out.append(n)
        for nxt in sorted(adj[n]):
            indeg[nxt] -= 1
            if indeg[nxt] == 0:
                queue.append(nxt)
    for n in sorted(nodes):
        if n not in out:
            out.append(n)
    return out


def _infer_ground_truth(statements: dict[str, dict[str, Any]], target_statement_id: str) -> dict[str, Any]:
    """
    Relevance: Operates within the orchestration and observability layer.
    Concept: Ground-truth extraction from KB-native theorem dependencies.
    Contribution: Creates an explicit trajectory target so iterative refinement can optimize toward discovery replication.
    """

    target = str(target_statement_id).strip()
    if target not in statements:
        raise ValueError(f"Target statement not found in KB: {target}")

    reverse: dict[str, set[str]] = {sid: set() for sid in statements}
    for sid, payload in statements.items():
        for dep in payload.get("depends_on", []) if isinstance(payload.get("depends_on"), list) else []:
            if dep in reverse:
                reverse[dep].add(sid)

    # Ancestor closure ending in target.
    ancestors: set[str] = set()
    stack = [target]
    while stack:
        cur = stack.pop()
        ancestors.add(cur)
        cur_deps = statements.get(cur, {}).get("depends_on", [])
        for dep in cur_deps if isinstance(cur_deps, list) else []:
            dep_s = str(dep).strip()
            if dep_s and dep_s in statements and dep_s not in ancestors:
                stack.append(dep_s)

    deps_map = {sid: list(statements.get(sid, {}).get("depends_on", [])) for sid in ancestors}
    base_sequence = _topo_order(ancestors, deps_map)

    # Add immediate theorem-like descendants as "historical spread" after the core theorem.
    descendants = [
        sid
        for sid in sorted(reverse.get(target, set()))
        if str(statements.get(sid, {}).get("kind", "")).strip().lower() in {"theorem", "corollary", "derived-construction"}
    ]
    discovery_sequence = base_sequence + [sid for sid in descendants if sid not in base_sequence]

    key_edges: list[dict[str, str]] = []
    for sid in base_sequence:
        for dep in statements.get(sid, {}).get("depends_on", []) if isinstance(statements.get(sid, {}).get("depends_on"), list) else []:
            dep_s = str(dep).strip()
            if dep_s in ancestors:
                key_edges.append({"from_id": dep_s, "to_id": sid})
    for sid in descendants:
        key_edges.append({"from_id": target, "to_id": sid})

    return {
        "target_statement_id": target,
        "discovery_sequence": discovery_sequence,
        "key_edges": key_edges,
        "source": "inferred-from-kb-dependencies",
    }


def _normalize_ground_truth(raw: dict[str, Any], statements: dict[str, dict[str, Any]], target_statement_id: str) -> dict[str, Any]:
    """
    Relevance: Operates within the orchestration and observability layer.
    Concept: Normalization of input structures into stable internal forms.
    Contribution: Ensures scoring works on a predictable ground-truth schema regardless of input format.
    """

    if not isinstance(raw, dict) or not raw:
        return _infer_ground_truth(statements, target_statement_id)

    target = str(raw.get("target_statement_id", "")).strip() or str(target_statement_id).strip()
    seq = [str(x).strip() for x in raw.get("discovery_sequence", []) if str(x).strip()] if isinstance(raw.get("discovery_sequence"), list) else []
    if not seq:
        seq = _infer_ground_truth(statements, target).get("discovery_sequence", [])

    edges: list[dict[str, str]] = []
    raw_edges = raw.get("key_edges", [])
    if isinstance(raw_edges, list):
        for row in raw_edges:
            if isinstance(row, dict):
                src = str(row.get("from_id", "")).strip()
                dst = str(row.get("to_id", "")).strip()
            elif isinstance(row, (list, tuple)) and len(row) >= 2:
                src = str(row[0]).strip()
                dst = str(row[1]).strip()
            else:
                continue
            if src and dst:
                edges.append({"from_id": src, "to_id": dst})

    if not edges:
        inferred = _infer_ground_truth(statements, target)
        edges = inferred.get("key_edges", [])

    return {
        "target_statement_id": target,
        "discovery_sequence": seq,
        "key_edges": edges,
        "source": str(raw.get("source", "user-provided")).strip() or "user-provided",
    }


def _run_command(
    cmd: list[str],
    logger: ReasoningLogger,
    stage: str,
    workdir: Path,
    accounting_root: Path,
) -> tuple[int, str, dict[str, Any]]:
    """
    Relevance: Operates within the orchestration and observability layer.
    Concept: Bounded execution of fixed internal stages through a user-selected
    Python executable.
    Contribution: The stage scripts are repository-owned, but ``--python`` is
    user supplied.  Therefore even this legacy non-benchmark lane uses the hard
    process-group governor and records its operational receipt; it does not use
    the benchmark attestation/index format or make an external-evidence claim.
    """

    repo = Path(__file__).resolve().parents[4]
    if str(repo) not in sys.path:
        sys.path.insert(0, str(repo))
    from agentic.discovery.budgets import ResourceBudget, ResourceGovernor

    governor = ResourceGovernor(
        ResourceBudget.from_mapping(
            {
                "budget_id": f"legacy-theorem-simulator:{stage}",
                "wall_time_seconds": 300.0,
                "grace_period_seconds": 1.0,
                "cpu_seconds": 300.0,
                "memory_bytes": 2 * 1024 * 1024 * 1024,
                "disk_bytes": 1024 * 1024 * 1024,
                "network_bytes": 0,
                "token_count": 0,
                "request_count": 0,
                "cost_usd": 0.0,
            }
        ),
        run_directory=accounting_root,
        allowed_working_directory=workdir,
        capture_limit_bytes=4 * 1024 * 1024,
        disk_sample_interval_seconds=0.1,
    )
    try:
        event = governor.run_process(
            cmd,
            cwd=workdir,
            role="worker",
            stdout_limit_bytes=4 * 1024 * 1024,
            stderr_limit_bytes=4 * 1024 * 1024,
        )
    except OSError as exc:
        now = dt.datetime.now(dt.timezone.utc).isoformat()
        stderr = f"{type(exc).__name__}: {exc}"
        empty_digest = "sha256:" + hashlib.sha256(b"").hexdigest()
        event = {
            "event": "process_terminal",
            "role": "worker",
            "command": list(cmd),
            "pid": None,
            "started_at": now,
            "completed_at": now,
            "elapsed_seconds": 0.0,
            "status": "worker_failed",
            "returncode": None,
            "terminal_dimension": None,
            "terminal_used": None,
            "terminal_limit": None,
            "termination": "not_started",
            "stdin_bytes": 0,
            "stdin_sha256": empty_digest,
            "stdin_limit_bytes": None,
            "stdin_written_bytes": 0,
            "stdin_write_incomplete": False,
            "stdin_write_error": None,
            "stdout": "",
            "stderr": stderr,
            "stdout_bytes": 0,
            "stderr_bytes": len(stderr.encode("utf-8", errors="replace")),
            "stdout_retained_bytes": 0,
            "stderr_retained_bytes": len(stderr.encode("utf-8", errors="replace")),
            "stdout_sha256": empty_digest,
            "stderr_sha256": "sha256:" + hashlib.sha256(stderr.encode("utf-8", errors="replace")).hexdigest(),
            "stdout_utf8_valid": True,
            "stderr_utf8_valid": True,
            "stdout_truncated": False,
            "stderr_truncated": False,
            "stdout_drain_incomplete": False,
            "stderr_drain_incomplete": False,
            "stdout_limit_bytes": 4 * 1024 * 1024,
            "stderr_limit_bytes": 4 * 1024 * 1024,
            "descendant_leak_detected": False,
            "capture_limit_bytes": governor.capture_limit_bytes,
            "resource_measurement": governor.measurement_boundaries(),
            "epistemic_effect": "none_operational_outcome_only",
        }
        governor.events.append(event)
    output = str(event.get("stdout") or "") + str(event.get("stderr") or "")
    return_code = int(event["returncode"]) if isinstance(event.get("returncode"), int) else (0 if event.get("status") == "succeeded" else 1)
    receipt = governor.receipt(str(event.get("status") or "worker_failed"))
    if return_code != 0:
        logger.step(
            f"Stage failed: {stage}",
            "\n".join(
                [
                    f"return_code={return_code}",
                    f"process_status={event.get('status')}",
                    "command=" + " ".join(cmd),
                    output.strip()[-6000:],
                ]
            ),
        )
    return return_code, output, receipt


def _iter_paths(iter_dir: Path) -> dict[str, Path]:
    """
    Relevance: Operates within the orchestration and observability layer.
    Concept: Stable path-routing for per-iteration artifacts.
    Contribution: Isolates each refinement run to prevent cross-iteration contamination.
    """

    return {
        "analysis": iter_dir / "connection-analysis.json",
        "analysis_md": iter_dir / "connection-analysis.md",
        "concept": iter_dir / "concept-evolution.md",
        "phyp": iter_dir / "proof-hypotheses.yaml",
        "coherence": iter_dir / "coherence-report.json",
        "coherence_md": iter_dir / "coherence-report.md",
        "entrypoints": iter_dir / "entrypoints.json",
        "entrypoints_md": iter_dir / "entrypoints.md",
        "pathways": iter_dir / "entrypoint-pathways.json",
        "pathways_md": iter_dir / "entrypoint-pathways.md",
        "hardness": iter_dir / "epistemic-hardness.json",
        "hardness_md": iter_dir / "epistemic-hardness.md",
        "bridges": iter_dir / "bridge-plan.json",
        "bridges_md": iter_dir / "bridge-plan.md",
        "conjectures": iter_dir / "concept-gap-abstractions.json",
        "conjectures_md": iter_dir / "concept-gap-abstractions.md",
        "strategies": iter_dir / "proof-strategies.json",
        "strategies_md": iter_dir / "proof-strategies.md",
        "novelty_prompt": iter_dir / "novelty-maximizing-prompt.txt",
        "sketches": iter_dir / "proof-sketches.json",
        "sketches_md": iter_dir / "proof-sketches.md",
        "paper_argument": iter_dir / "paper-style-argument.md",
        "hyp_eval": iter_dir / "hypothesis-evaluation.json",
        "hyp_eval_md": iter_dir / "hypothesis-evaluation.md",
    }


def _run_iteration(
    repo: Path,
    python_exe: str,
    kb_path: Path,
    kb_ref: str,
    artifacts_dir: Path,
    config: dict[str, Any],
    iter_index: int,
    logger: ReasoningLogger,
) -> dict[str, Any]:
    """
    Relevance: Operates within the orchestration and observability layer.
    Concept: Primary callable implementing one full refinement iteration.
    Contribution: Executes the generative reasoning chain under a parameter setting for discovery-fit evaluation.
    """

    iter_dir = artifacts_dir / "discovery-simulation" / f"iter-{iter_index:03d}"
    iter_dir.mkdir(parents=True, exist_ok=True)
    paths = _iter_paths(iter_dir)

    scripts = {
        "analyze": repo / "skills" / "discovery" / "kb-proof-connector" / "scripts" / "analyze_kb_graph.py",
        "phyp": repo / "skills" / "discovery" / "kb-proof-connector" / "scripts" / "generate_phyp.py",
        "coherence": repo / "skills" / "discovery" / "kb-coherence-evaluator" / "scripts" / "evaluate_coherence.py",
        "concept": repo / "skills" / "orchestration" / "kb-orchestrator" / "scripts" / "generate_concept_evolution.py",
        "entrypoints": repo / "skills" / "discovery" / "kb-entrypoint-finder" / "scripts" / "recommend_entrypoints.py",
        "pathways": repo / "skills" / "discovery" / "kb-entrypoint-pathfinder" / "scripts" / "synthesize_pathways.py",
        "hardness": repo / "skills" / "discovery" / "kb-epistemic-hardness" / "scripts" / "articulate_hardness.py",
        "bridges": repo / "skills" / "discovery" / "kb-concept-bridge-planner" / "scripts" / "plan_bridges.py",
        "conjecture": repo / "skills" / "discovery" / "kb-gap-abstraction-conjecturer" / "scripts" / "conjecture_gap_abstractions.py",
        "strategies": repo / "skills" / "discovery" / "kb-novel-proof-strategist" / "scripts" / "design_strategies.py",
        "sketches": repo / "skills" / "discovery" / "kb-proof-sketcher" / "scripts" / "generate_proof_sketches.py",
        "hyp_eval": repo / "skills" / "evaluation" / "kb-hypothesis-evaluator" / "scripts" / "evaluate_hypotheses.py",
    }

    stage_cmds: list[tuple[str, list[str]]] = []
    stage_cmds.append(
        (
            "connect.analyze",
            [
                python_exe,
                str(scripts["analyze"]),
                "--kb",
                str(kb_path),
                "--top-k",
                str(config["analyze_top_k"]),
                "--min-similarity",
                str(config["min_similarity"]),
                "--max-connections",
                str(config["max_connections"]),
                "--loop-rounds",
                "3",
                "--allow-intra-component-fallback",
                "--output-json",
                str(paths["analysis"]),
                "--output-md",
                str(paths["analysis_md"]),
            ],
        )
    )
    stage_cmds.append(
        (
            "connect.generate-phyp",
            [
                python_exe,
                str(scripts["phyp"]),
                "--analysis",
                str(paths["analysis"]),
                "--kb",
                str(kb_path),
                "--output",
                str(paths["phyp"]),
                "--top-links",
                str(config["top_links"]),
                "--top-interventions",
                str(config["top_interventions"]),
                "--top-conceptual",
                str(config["top_conceptual"]),
            ],
        )
    )
    stage_cmds.append(
        (
            "coherence-eval",
            [
                python_exe,
                str(scripts["coherence"]),
                "--kb",
                str(kb_path),
                "--analysis",
                str(paths["analysis"]),
                "--phyp",
                str(paths["phyp"]),
                "--output-json",
                str(paths["coherence"]),
                "--output-md",
                str(paths["coherence_md"]),
            ],
        )
    )
    stage_cmds.append(
        (
            "concept-evolution",
            [
                python_exe,
                str(scripts["concept"]),
                "--kb",
                str(kb_path),
                "--analysis",
                str(paths["analysis"]),
                "--phyp",
                str(paths["phyp"]),
                "--output-md",
                str(paths["concept"]),
            ],
        )
    )
    stage_cmds.append(
        (
            "entrypoints.rank",
            [
                python_exe,
                str(scripts["entrypoints"]),
                "--kb",
                str(kb_path),
                "--concept",
                str(paths["concept"]),
                "--analysis",
                str(paths["analysis"]),
                "--phyp",
                str(paths["phyp"]),
                "--coherence-report",
                str(paths["coherence"]),
                "--top-k",
                str(config["entry_top_k"]),
                "--output-json",
                str(paths["entrypoints"]),
                "--output-md",
                str(paths["entrypoints_md"]),
            ],
        )
    )
    stage_cmds.append(
        (
            "entrypoints.pathways",
            [
                python_exe,
                str(scripts["pathways"]),
                "--recommendations",
                str(paths["entrypoints"]),
                "--phyp",
                str(paths["phyp"]),
                "--analysis",
                str(paths["analysis"]),
                "--top-entrypoints",
                str(config["pathway_top_entrypoints"]),
                "--max-hypotheses-per-path",
                str(config["max_hypotheses_per_path"]),
                "--max-links-per-path",
                str(config["max_links_per_path"]),
                "--output-json",
                str(paths["pathways"]),
                "--output-md",
                str(paths["pathways_md"]),
            ],
        )
    )
    stage_cmds.append(
        (
            "hardness",
            [
                python_exe,
                str(scripts["hardness"]),
                "--problem",
                kb_ref,
                "--kb",
                str(kb_path),
                "--concept",
                str(paths["concept"]),
                "--analysis",
                str(paths["analysis"]),
                "--entrypoints",
                str(paths["entrypoints"]),
                "--pathways",
                str(paths["pathways"]),
                "--phyp",
                str(paths["phyp"]),
                "--output-json",
                str(paths["hardness"]),
                "--output-md",
                str(paths["hardness_md"]),
            ],
        )
    )
    stage_cmds.append(
        (
            "bridge-plan",
            [
                python_exe,
                str(scripts["bridges"]),
                "--analysis",
                str(paths["analysis"]),
                "--entrypoints",
                str(paths["entrypoints"]),
                "--pathways",
                str(paths["pathways"]),
                "--phyp",
                str(paths["phyp"]),
                "--coherence-report",
                str(paths["coherence"]),
                "--concept",
                str(paths["concept"]),
                "--top-k",
                str(config["bridge_top_k"]),
                "--output-json",
                str(paths["bridges"]),
                "--output-md",
                str(paths["bridges_md"]),
            ],
        )
    )
    stage_cmds.append(
        (
            "conjecture",
            [
                python_exe,
                str(scripts["conjecture"]),
                "--analysis",
                str(paths["analysis"]),
                "--entrypoints",
                str(paths["entrypoints"]),
                "--pathways",
                str(paths["pathways"]),
                "--bridges",
                str(paths["bridges"]),
                "--phyp",
                str(paths["phyp"]),
                "--hardness",
                str(paths["hardness"]),
                "--top-bridges",
                str(config["conjecture_top_bridges"]),
                "--max-conjectures-per-bridge",
                str(config["max_conjectures_per_bridge"]),
                "--output-json",
                str(paths["conjectures"]),
                "--output-md",
                str(paths["conjectures_md"]),
            ],
        )
    )
    stage_cmds.append(
        (
            "strategies",
            [
                python_exe,
                str(scripts["strategies"]),
                "--entrypoints",
                str(paths["entrypoints"]),
                "--pathways",
                str(paths["pathways"]),
                "--bridges",
                str(paths["bridges"]),
                "--phyp",
                str(paths["phyp"]),
                "--coherence-report",
                str(paths["coherence"]),
                "--conjectures",
                str(paths["conjectures"]),
                "--top-k",
                str(config["strategies_top_k"]),
                "--output-json",
                str(paths["strategies"]),
                "--output-md",
                str(paths["strategies_md"]),
                "--output-prompt",
                str(paths["novelty_prompt"]),
            ],
        )
    )
    stage_cmds.append(
        (
            "proof-sketch",
            [
                python_exe,
                str(scripts["sketches"]),
                "--conjectures",
                str(paths["conjectures"]),
                "--strategies",
                str(paths["strategies"]),
                "--bridges",
                str(paths["bridges"]),
                "--phyp",
                str(paths["phyp"]),
                "--analysis",
                str(paths["analysis"]),
                "--coherence-report",
                str(paths["coherence"]),
                "--hardness",
                str(paths["hardness"]),
                "--kb",
                str(kb_path),
                "--top-k",
                str(config["sketch_top_k"]),
                "--output-json",
                str(paths["sketches"]),
                "--output-md",
                str(paths["sketches_md"]),
                "--output-paper-md",
                str(paths["paper_argument"]),
            ],
        )
    )
    stage_cmds.append(
        (
            "hypothesis-eval",
            [
                python_exe,
                str(scripts["hyp_eval"]),
                "--kb",
                str(kb_path),
                "--phyp",
                str(paths["phyp"]),
                "--analysis",
                str(paths["analysis"]),
                "--coherence-report",
                str(paths["coherence"]),
                "--support-threshold",
                str(config["support_threshold"]),
                "--refute-threshold",
                str(config["refute_threshold"]),
                "--margin",
                str(config["margin"]),
                "--output-json",
                str(paths["hyp_eval"]),
                "--output-md",
                str(paths["hyp_eval_md"]),
            ],
        )
    )

    stage_reports: list[dict[str, Any]] = []
    for stage, cmd in stage_cmds:
        code, output, resource_receipt = _run_command(
            cmd,
            logger=logger,
            stage=stage,
            workdir=repo,
            accounting_root=iter_dir,
        )
        stage_reports.append(
            {
                "stage": stage,
                "return_code": code,
                "command": cmd,
                "tail_output": output.strip()[-1400:],
                "resource_receipt": resource_receipt,
            }
        )
        if code != 0:
            return {
                "iteration": iter_index,
                "config": config,
                "success": False,
                "error_stage": stage,
                "stage_reports": stage_reports,
                "paths": {k: str(v) for k, v in paths.items()},
            }

    return {
        "iteration": iter_index,
        "config": config,
        "success": True,
        "stage_reports": stage_reports,
        "paths": {k: str(v) for k, v in paths.items()},
    }


def _rank_map(rows: list[dict[str, Any]], key: str) -> dict[str, int]:
    """
    Relevance: Operates within the orchestration and observability layer.
    Concept: Internal helper implementing one deterministic step of this stage.
    Contribution: Normalizes ranked artifacts for direct sequence/ordering comparisons against ground truth.
    """

    out: dict[str, int] = {}
    for idx, row in enumerate(rows, start=1):
        if not isinstance(row, dict):
            continue
        sid = str(row.get(key, "")).strip()
        if sid and sid not in out:
            out[sid] = idx
    return out


def _adjust_ground_truth_for_knockout(gt: dict[str, Any], knockout: dict[str, Any]) -> tuple[list[str], list[tuple[str, str]]]:
    """
    Relevance: Operates within the orchestration and observability layer.
    Concept: Ground-truth contraction under simulated ignorance.
    Contribution: Prevents hidden bridge statements from unfairly depressing replication scores when the evaluator itself removed them from agent context.
    """

    seq = [str(x).strip() for x in gt.get("discovery_sequence", []) if str(x).strip()]
    edges = [
        (str(row.get("from_id", "")).strip(), str(row.get("to_id", "")).strip())
        for row in gt.get("key_edges", [])
        if isinstance(row, dict) and str(row.get("from_id", "")).strip() and str(row.get("to_id", "")).strip()
    ]
    removed = {str(item).strip() for item in knockout.get("removed_statements", []) if str(item).strip()}
    if not removed:
        return seq, edges

    filtered_seq = [sid for sid in seq if sid not in removed]
    preserved_edges = {(src, dst) for src, dst in edges if src not in removed and dst not in removed}
    incoming: dict[str, set[str]] = {sid: set() for sid in removed}
    outgoing: dict[str, set[str]] = {sid: set() for sid in removed}
    for src, dst in edges:
        if dst in removed and src not in removed:
            incoming.setdefault(dst, set()).add(src)
        if src in removed and dst not in removed:
            outgoing.setdefault(src, set()).add(dst)
    for hidden in removed:
        for src in incoming.get(hidden, set()):
            for dst in outgoing.get(hidden, set()):
                if src != dst:
                    preserved_edges.add((src, dst))
    return filtered_seq, sorted(preserved_edges)


def _hidden_concept_recovery_score(artifacts: dict[str, Any], knockout: dict[str, Any]) -> float:
    """
    Relevance: Operates within the orchestration and observability layer.
    Concept: Recovery signal for a deliberately hidden bridge concept.
    Contribution: Rewards the pipeline when conjectures and proof sketches reconstruct the missing concept at the processed-artifact level.
    """

    terms = [str(item).strip().lower() for item in knockout.get("bridge_concept_terms", []) if str(item).strip()]
    if not terms:
        return 0.0
    token_pattern = re.compile(r"[a-z0-9]+")
    stop = {"the", "and", "for", "with", "into", "from", "this", "that", "bridge", "concept", "hidden"}
    tokens: set[str] = set()
    for term in terms:
        for token in token_pattern.findall(term):
            if len(token) >= 4 and token not in stop:
                tokens.add(token)
    if not tokens:
        return 0.0

    texts: list[str] = []
    for row in artifacts.get("conjectures", {}).get("abstraction_conjectures", []) if isinstance(artifacts.get("conjectures", {}).get("abstraction_conjectures"), list) else []:
        if isinstance(row, dict):
            texts.append(
                " ".join(
                    [
                        str(row.get("abstraction_label", "")),
                        str(row.get("abstraction_type", "")),
                        str(row.get("mathematical_object_role", "")),
                        str(row.get("target_consequence_schema", "")),
                        str(row.get("preserved_invariant", "")),
                    ]
                ).lower()
            )
    for row in artifacts.get("sketches", {}).get("proof_sketches", []) if isinstance(artifacts.get("sketches", {}).get("proof_sketches"), list) else []:
        if isinstance(row, dict):
            texts.append(
                " ".join(
                    [
                        str(row.get("family", "")),
                        str(row.get("title", "")),
                        str(row.get("target_consequence", "")),
                        str(row.get("antecedent", "")),
                        str(row.get("invariant", "")),
                    ]
                ).lower()
            )
    for hid, hyp in artifacts.get("hypothesis_by_id", {}).items():
        if not isinstance(hyp, dict):
            continue
        texts.append(
            " ".join(
                [
                    str(hid),
                    str(hyp.get("kind", "")),
                    str(hyp.get("label", "")),
                    str(hyp.get("hypothesis_latex", "")),
                    str(hyp.get("informal", "")),
                ]
            ).lower()
        )

    best = 0.0
    for text in texts:
        present = sum(1 for token in tokens if token in text)
        best = max(best, present / max(1, len(tokens)))
    return round(max(0.0, min(1.0, best)), 6)


def _score_replication(
    gt: dict[str, Any],
    artifacts: dict[str, Any],
    knockout: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """
    Relevance: Operates within the orchestration and observability layer.
    Concept: Quantitative evaluation of discovery-trajectory replication.
    Contribution: Produces a single discovery-fit objective used to drive iterative refinement.
    """

    knockout = knockout or {}
    target = str(gt.get("target_statement_id", "")).strip()
    seq, edges = _adjust_ground_truth_for_knockout(gt, knockout)

    ranked_entry = artifacts.get("entrypoints", {}).get("ranked_entrypoints", [])
    ranked_entry = ranked_entry if isinstance(ranked_entry, list) else []
    rank = _rank_map(ranked_entry, "statement_id")

    target_rank = rank.get(target, 10**9)
    target_rank_score = 0.0 if target_rank >= 10**9 else 1.0 / (1.0 + 0.30 * (target_rank - 1))

    top_n = max(8, len(seq) + 4)
    top_ids = [str(row.get("statement_id", "")).strip() for row in ranked_entry[:top_n] if isinstance(row, dict)]
    sequence_hit = 0.0
    if seq:
        sequence_hit = len([sid for sid in seq if sid in set(top_ids)]) / len(seq)

    bridge_rows = artifacts.get("bridges", {}).get("bridge_programs", [])
    bridge_rows = bridge_rows if isinstance(bridge_rows, list) else []
    bridge_edges = {
        (str(row.get("from_id", "")).strip(), str(row.get("to_id", "")).strip())
        for row in bridge_rows
        if isinstance(row, dict) and str(row.get("from_id", "")).strip() and str(row.get("to_id", "")).strip()
    }
    pathway_rows = artifacts.get("pathways", {}).get("pathways", [])
    pathway_rows = pathway_rows if isinstance(pathway_rows, list) else []
    pathway_edges: set[tuple[str, str]] = set()
    for row in pathway_rows:
        if not isinstance(row, dict):
            continue
        for link in row.get("supporting_links", []) if isinstance(row.get("supporting_links"), list) else []:
            if not isinstance(link, dict):
                continue
            src = str(link.get("from_id", "")).strip()
            dst = str(link.get("to_id", "")).strip()
            if src and dst:
                pathway_edges.add((src, dst))

    # Discovery replication should respect partial-order constraints from the
    # ground-truth dependency edges, not adjacent positions in one linearized
    # sequence (multiple valid linearizations may exist).
    order_checks = 0
    order_correct = 0
    for a, b in edges:
        ranked_order_ok = a in rank and b in rank and rank[a] < rank[b]
        graph_order_ok = (a, b) in bridge_edges or (a, b) in pathway_edges
        if a in rank or b in rank or graph_order_ok:
            order_checks += 1
            if ranked_order_ok or graph_order_ok:
                order_correct += 1
    sequence_order = (order_correct / order_checks) if order_checks > 0 else 0.0

    edge_hits = len([edge for edge in edges if edge in bridge_edges])
    edge_coverage = (edge_hits / len(edges)) if edges else 0.0

    eval_rows = artifacts.get("hyp_eval", {}).get("results", [])
    eval_rows = eval_rows if isinstance(eval_rows, list) else []
    gt_touch_total = 0
    gt_touch_supported = 0
    gt_edge_total = 0
    gt_edge_supported = 0
    gt_edge_set = set(edges)
    gt_nodes = set(seq)
    for row in eval_rows:
        if not isinstance(row, dict):
            continue
        hid = str(row.get("hypothesis_id", "")).strip()
        verdict = str(row.get("verdict", "")).strip().lower()
        hyp = artifacts.get("hypothesis_by_id", {}).get(hid, {})
        src = str(hyp.get("support_statement_id", "")).strip()
        dst = str(hyp.get("target_statement_id", "")).strip()
        kind = str(hyp.get("kind", "")).strip().lower()
        if src in gt_nodes or dst in gt_nodes:
            gt_touch_total += 1
            if verdict in {"supported", "provisionally-supported"}:
                gt_touch_supported += 1
        if kind == "bridge-link" and (src, dst) in gt_edge_set:
            gt_edge_total += 1
            if verdict in {"supported", "provisionally-supported"}:
                gt_edge_supported += 1

    broad_hyp_support = (gt_touch_supported / gt_touch_total) if gt_touch_total > 0 else 0.0
    edge_hyp_support = (gt_edge_supported / gt_edge_total) if gt_edge_total > 0 else broad_hyp_support
    hypothesis_support = 0.65 * edge_hyp_support + 0.35 * broad_hyp_support

    strategy_count = len(artifacts.get("strategies", {}).get("strategies", []) if isinstance(artifacts.get("strategies", {}).get("strategies"), list) else [])
    conjecture_count = len(artifacts.get("conjectures", {}).get("abstraction_conjectures", []) if isinstance(artifacts.get("conjectures", {}).get("abstraction_conjectures"), list) else [])
    sketch_count = len(artifacts.get("sketches", {}).get("proof_sketches", []) if isinstance(artifacts.get("sketches", {}).get("proof_sketches"), list) else [])
    bridge_count = len(bridge_rows)
    activation = (
        int(bridge_count > 0)
        + int(conjecture_count > 0)
        + int(strategy_count > 0)
        + int(sketch_count > 0)
    ) / 4.0

    coherence = artifacts.get("coherence", {}).get("coherence_profile", {})
    coherence_global = _safe_float(coherence.get("global_coherence", 0.0), 0.0)
    coherence_score = max(0.0, min(1.0, coherence_global))
    hidden_concept_recovery = 0.0
    if str(knockout.get("profile", "none")).strip().lower() in {"bridge-concept", "stone-bridge-concept"}:
        hidden_concept_recovery = _hidden_concept_recovery_score(artifacts, knockout)

    if hidden_concept_recovery > 0.0:
        replication_score = max(
            0.0,
            min(
                1.0,
                0.17 * target_rank_score
                + 0.17 * sequence_hit
                + 0.14 * sequence_order
                + 0.18 * edge_coverage
                + 0.12 * hypothesis_support
                + 0.12 * hidden_concept_recovery
                + 0.05 * activation
                + 0.05 * coherence_score,
            ),
        )
    else:
        replication_score = max(
            0.0,
            min(
                1.0,
                0.20 * target_rank_score
                + 0.19 * sequence_hit
                + 0.16 * sequence_order
                + 0.21 * edge_coverage
                + 0.13 * hypothesis_support
                + 0.06 * activation
                + 0.05 * coherence_score,
            ),
        )

    return {
        "replication_score": round(replication_score, 6),
        "components": {
            "target_rank_score": round(target_rank_score, 6),
            "sequence_hit": round(sequence_hit, 6),
            "sequence_order": round(sequence_order, 6),
            "edge_coverage": round(edge_coverage, 6),
            "hypothesis_support": round(hypothesis_support, 6),
            "edge_hypothesis_support": round(edge_hyp_support, 6),
            "broad_hypothesis_support": round(broad_hyp_support, 6),
            "hidden_concept_recovery": round(hidden_concept_recovery, 6),
            "activation": round(activation, 6),
            "coherence_score": round(coherence_score, 6),
        },
        "counts": {
            "entrypoints_ranked": len(ranked_entry),
            "bridge_programs": bridge_count,
            "conjectures": conjecture_count,
            "strategies": strategy_count,
            "proof_sketches": sketch_count,
            "gt_touching_hypotheses": gt_touch_total,
            "gt_touching_hypotheses_supported": gt_touch_supported,
            "gt_edge_hypotheses": gt_edge_total,
            "gt_edge_hypotheses_supported": gt_edge_supported,
            "gt_edges_total": len(edges),
            "gt_edges_hit": edge_hits,
            "target_rank": target_rank if target_rank < 10**9 else -1,
        },
    }


def _load_iteration_artifacts(paths: dict[str, str]) -> dict[str, Any]:
    """
    Relevance: Operates within the orchestration and observability layer.
    Concept: Loading and structuring external artifacts for deterministic processing.
    Contribution: Aggregates per-iteration outputs into a single scoring payload.
    """

    p = {k: Path(v) for k, v in paths.items()}
    phyp = _load_yaml(p["phyp"])
    hypotheses = phyp.get("hypotheses", []) if isinstance(phyp.get("hypotheses"), list) else []
    hyp_by_id = {str(h.get("id", "")).strip(): h for h in hypotheses if isinstance(h, dict) and str(h.get("id", "")).strip()}
    return {
        "entrypoints": _load_json(p["entrypoints"]),
        "bridges": _load_json(p["bridges"]),
        "conjectures": _load_json(p["conjectures"]),
        "strategies": _load_json(p["strategies"]),
        "sketches": _load_json(p["sketches"]),
        "coherence": _load_json(p["coherence"]),
        "hyp_eval": _load_json(p["hyp_eval"]),
        "hypothesis_by_id": hyp_by_id,
    }


def _config_pool(defaults: dict[str, Any]) -> list[dict[str, Any]]:
    """
    Relevance: Operates within the orchestration and observability layer.
    Concept: Deterministic candidate-configuration generation for iterative refinement.
    Contribution: Supplies diverse generative parameter settings so the loop can improve discovery fit.
    """

    def with_updates(**kwargs: Any) -> dict[str, Any]:
        cfg = dict(defaults)
        cfg.update(kwargs)
        return cfg

    return [
        with_updates(),
        with_updates(min_similarity=0.10),
        with_updates(min_similarity=0.08, max_connections=60),
        with_updates(top_links=30, top_conceptual=18),
        with_updates(top_links=24, top_interventions=16),
        with_updates(entry_top_k=14, pathway_top_entrypoints=10),
        with_updates(entry_top_k=20, pathway_top_entrypoints=10),
        with_updates(bridge_top_k=30, conjecture_top_bridges=16),
        with_updates(bridge_top_k=25, conjecture_top_bridges=12, max_conjectures_per_bridge=4),
        with_updates(strategies_top_k=8, sketch_top_k=8),
        with_updates(strategies_top_k=4, sketch_top_k=4),
        with_updates(min_similarity=0.14, top_links=16, top_conceptual=8),
        with_updates(min_similarity=0.09, top_links=28, bridge_top_k=30, conjecture_top_bridges=18),
    ]


def _to_markdown(report: dict[str, Any]) -> str:
    """
    Relevance: Operates within the orchestration and observability layer.
    Concept: Rendering internal outputs into human-readable artifacts.
    Contribution: Exposes optimization dynamics and discovery-fit diagnostics in analyst-friendly form.
    """

    lines: list[str] = []
    lines.append("# Theorem Discovery Simulation")
    lines.append("")
    meta = report.get("metadata", {})
    lines.append("## Summary")
    lines.append("")
    lines.append(f"- KB: {meta.get('kb', '')}")
    lines.append(f"- Working KB: {meta.get('working_kb', '')}")
    lines.append(f"- Target statement: {meta.get('target_statement_id', '')}")
    lines.append(f"- Ground truth source: {meta.get('ground_truth_source', '')}")
    lines.append(f"- Knockout profile: {meta.get('knockout_profile', 'none')}")
    lines.append(f"- Iterations requested: {meta.get('iterations_requested', 0)}")
    lines.append(f"- Iterations executed: {meta.get('iterations_executed', 0)}")
    lines.append(f"- Success threshold: {meta.get('success_threshold', 0.0)}")
    lines.append(f"- Replicated: {meta.get('replicated', False)}")
    lines.append(f"- Best replication score: {meta.get('best_replication_score', 0.0)}")
    lines.append("")

    knockout = report.get("knockout", {}) if isinstance(report.get("knockout"), dict) else {}
    if knockout:
        lines.append("## Knockout")
        lines.append("")
        lines.append(f"- Profile: `{knockout.get('profile', 'none')}`")
        lines.append(f"- Blanked fields: {int(knockout.get('blanked_fields_count', 0) or 0)}")
        lines.append(f"- Dropped edges: {int(knockout.get('dropped_edges_count', 0) or 0)}")
        lines.append(f"- Redacted mentions: {int(knockout.get('redacted_mentions_count', 0) or 0)}")
        bridge_ids = knockout.get("bridge_concept_ids", []) if isinstance(knockout.get("bridge_concept_ids"), list) else []
        bridge_terms = knockout.get("bridge_concept_terms", []) if isinstance(knockout.get("bridge_concept_terms"), list) else []
        if bridge_ids:
            lines.append("- Hidden bridge concepts:")
            for item in bridge_ids:
                lines.append(f"  - `{item}`")
        if bridge_terms:
            lines.append("- Hidden bridge terms:")
            for item in bridge_terms:
                lines.append(f"  - `{item}`")
        removed = knockout.get("removed_statements", []) if isinstance(knockout.get("removed_statements"), list) else []
        if removed:
            lines.append("- Removed statements:")
            for sid in removed:
                lines.append(f"  - `{sid}`")
        lines.append("")

    gt = report.get("ground_truth", {})
    lines.append("## Ground Truth")
    lines.append("")
    lines.append(f"- Target: `{gt.get('target_statement_id', '')}`")
    seq = gt.get("discovery_sequence", []) if isinstance(gt.get("discovery_sequence"), list) else []
    lines.append(f"- Discovery sequence length: {len(seq)}")
    if seq:
        lines.append("- Sequence:")
        for sid in seq:
            lines.append(f"  - `{sid}`")
    lines.append("")

    lines.append("## Iterations")
    lines.append("")
    lines.append("| iter | score | target-rank | edge-hit | bridges | conjectures | sketches | status |")
    lines.append("|---|---:|---:|---:|---:|---:|---:|---|")
    for row in report.get("iterations", []):
        score = row.get("score", {})
        comps = score.get("components", {}) if isinstance(score, dict) else {}
        cnt = score.get("counts", {}) if isinstance(score, dict) else {}
        lines.append(
            "| {i} | {s:.4f} | {tr:.4f} | {eh:.4f} | {b} | {c} | {sk} | {st} |".format(
                i=row.get("iteration", 0),
                s=_safe_float(score.get("replication_score", 0.0), 0.0),
                tr=_safe_float(comps.get("target_rank_score", 0.0), 0.0),
                eh=_safe_float(comps.get("edge_coverage", 0.0), 0.0),
                b=int(cnt.get("bridge_programs", 0) or 0),
                c=int(cnt.get("conjectures", 0) or 0),
                sk=int(cnt.get("proof_sketches", 0) or 0),
                st="ok" if row.get("success", False) else f"failed:{row.get('error_stage', '')}",
            )
        )
    lines.append("")

    best = report.get("best_iteration", {})
    lines.append("## Best Iteration")
    lines.append("")
    if isinstance(best, dict) and best:
        lines.append(f"- Iteration: {best.get('iteration', 0)}")
        lines.append(f"- Replication score: {_safe_float((best.get('score', {}) or {}).get('replication_score', 0.0), 0.0):.6f}")
        lines.append("- Config:")
        cfg = best.get("config", {}) if isinstance(best.get("config"), dict) else {}
        for k in sorted(cfg):
            lines.append(f"  - `{k}`: {cfg[k]}")
        lines.append("- Artifact root:")
        lines.append(f"  - `{best.get('iter_dir', '')}`")
    else:
        lines.append("- No successful iteration.")
    lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    """
    Relevance: Operates within the orchestration and observability layer.
    Concept: CLI entrypoint orchestration for this script.
    Contribution: Runs iterative discovery-fit refinement and emits reproducible optimization artifacts.
    """

    logger = ReasoningLogger("kb-discovery-simulator")
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--kb", default="", help="Path to KB markdown file. Required outside benchmark-manifest mode.")
    ap.add_argument("--benchmark-manifest", default="", help="Frozen benchmark manifest evaluated without exposing truth to discovery inputs.")
    ap.add_argument("--benchmark-capture-output", default="", help="Run a live hidden-task matrix and write the preregistered capture path.")
    ap.add_argument("--benchmark-runner-command", default="", help="JSON argv for a runner that accepts one hidden-task request on stdin and emits one JSON result on stdout.")
    ap.add_argument("--benchmark-runner-dependency", action="append", default=[], help="Exact runner script/module dependency to seal in addition to file-valued argv entries.")
    ap.add_argument("--human-evidence-verifier-command", default="", help="JSON argv for an external authority that authenticates a rating artifact/descriptor request on stdin.")
    ap.add_argument("--human-evidence-verifier-dependency", action="append", default=[], help="Exact verifier script/module dependency to seal in addition to file-valued argv entries.")
    ap.add_argument("--human-evidence-trust-anchor", default="", help="Caller-controlled JSON trust anchor for the governed human-evidence verifier; never read from the evidence manifest.")
    ap.add_argument("--benchmark-run-id", default="", help="Required immutable run identifier for external benchmark commands.")
    ap.add_argument("--benchmark-execution-root", default="agentic/runs/discovery_benchmark_processes")
    ap.add_argument("--benchmark-process-grace-seconds", type=float, default=0.25)
    ap.add_argument("--benchmark-process-memory-bytes", type=int, default=512 * 1024 * 1024)
    ap.add_argument("--benchmark-process-disk-bytes", type=int, default=64 * 1024 * 1024)
    ap.add_argument("--benchmark-process-input-bytes", type=int, default=1024 * 1024)
    ap.add_argument("--benchmark-process-stdout-bytes", type=int, default=1024 * 1024)
    ap.add_argument("--benchmark-process-stderr-bytes", type=int, default=256 * 1024)
    ap.add_argument("--human-verifier-wall-seconds", type=float, default=10.0)
    ap.add_argument("--require-replicated", action="store_true", help="Return nonzero when benchmark validity or replication thresholds are unmet.")
    ap.add_argument("--kb-ref", default="", help="Optional canonical KB reference.")
    ap.add_argument("--artifacts-dir", default="", help="Optional canonical artifacts path.")
    ap.add_argument("--ground-truth", default="", help="Optional YAML/JSON ground-truth file.")
    ap.add_argument("--target-statement-id", default="st.thm.hille-yosida-general")
    ap.add_argument(
        "--knockout-profile",
        choices=("none", "target-proof", "proof-structure", "hille-yosida-proof", "bridge-concept", "stone-bridge-concept"),
        default="none",
        help="Optional ignorance model that blanks proof structure in a working KB copy.",
    )
    ap.add_argument(
        "--knockout-statement",
        action="append",
        default=[],
        help="Statement id to remove from the working KB (repeatable).",
    )
    ap.add_argument(
        "--knockout-edge",
        action="append",
        default=[],
        help="Dependency edge to remove from the working KB, formatted as src->dst (repeatable).",
    )
    ap.add_argument(
        "--knockout-field",
        action="append",
        default=[],
        help="Statement field to blank in the working KB, formatted as statement_id:field (repeatable).",
    )
    ap.add_argument(
        "--bridge-concept-id",
        action="append",
        default=[],
        help="Concept or statement identifier for the bridge concept to hide (repeatable).",
    )
    ap.add_argument(
        "--bridge-concept-term",
        action="append",
        default=[],
        help="Literal term to redact when hiding the bridge concept (repeatable).",
    )
    ap.add_argument("--iterations", type=int, default=8)
    ap.add_argument("--success-threshold", type=float, default=0.88)
    ap.add_argument("--python", default=sys.executable)
    ap.add_argument("--output-json", default="")
    ap.add_argument("--output-md", default="")
    ap.add_argument("--emit-inferred-ground-truth", action=argparse.BooleanOptionalAction, default=True)
    args = ap.parse_args()

    repo = Path(__file__).resolve().parents[4]
    if args.benchmark_manifest:
        if str(repo) not in sys.path:
            sys.path.insert(0, str(repo))
        from agentic.discovery.benchmark import (
            BenchmarkIntegrityError,
            capture_live_hidden_task_outputs,
            evaluate_benchmark_manifest,
        )
        from agentic.discovery.benchmark_process import ExternalBenchmarkProcessAdapter, ExternalBenchmarkProcessError

        manifest_path = Path(args.benchmark_manifest)
        if not manifest_path.is_absolute():
            manifest_path = (repo / manifest_path).resolve()
        try:
            try:
                manifest_payload = json.loads(manifest_path.read_text(encoding="utf-8"))
            except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
                raise BenchmarkIntegrityError(
                    f"benchmark_manifest_load_failed: {type(exc).__name__}: {exc}"
                ) from exc
            if not isinstance(manifest_payload, dict) or not manifest_payload.get("benchmark_id"):
                raise BenchmarkIntegrityError("benchmark manifest lacks benchmark_id")
            execution_root = Path(args.benchmark_execution_root)
            if not execution_root.is_absolute():
                execution_root = (repo / execution_root).resolve()
            try:
                execution_root.relative_to(repo)
            except ValueError as exc:
                raise BenchmarkIntegrityError("benchmark execution root must remain inside the repository") from exc
            if (args.benchmark_runner_command or args.human_evidence_verifier_command) and not args.benchmark_run_id:
                raise BenchmarkIntegrityError("--benchmark-run-id is required for external benchmark processes")
            if bool(args.human_evidence_verifier_command) != bool(args.human_evidence_trust_anchor):
                raise BenchmarkIntegrityError(
                    "human verifier command and separately configured trust anchor are both required"
                )
            adapter_kwargs = {
                "benchmark_id": str(manifest_payload["benchmark_id"]), "benchmark_run_id": args.benchmark_run_id,
                "run_root": execution_root, "grace_period_seconds": args.benchmark_process_grace_seconds,
                "memory_bytes": args.benchmark_process_memory_bytes, "disk_bytes": args.benchmark_process_disk_bytes,
                "input_limit_bytes": args.benchmark_process_input_bytes, "stdout_limit_bytes": args.benchmark_process_stdout_bytes,
                "stderr_limit_bytes": args.benchmark_process_stderr_bytes, "verifier_wall_time_seconds": args.human_verifier_wall_seconds,
            }
            if args.benchmark_capture_output or args.benchmark_runner_command:
                if not args.benchmark_capture_output or not args.benchmark_runner_command:
                    raise BenchmarkIntegrityError(
                        "live capture requires both --benchmark-capture-output and --benchmark-runner-command"
                    )
                try:
                    runner_argv = json.loads(args.benchmark_runner_command)
                except json.JSONDecodeError as exc:
                    raise BenchmarkIntegrityError(
                        f"benchmark_runner_command_manifest_invalid: {exc}"
                    ) from exc
                if not isinstance(runner_argv, list) or not runner_argv or not all(
                    isinstance(item, str) and item for item in runner_argv
                ):
                    raise BenchmarkIntegrityError("benchmark runner command must be a non-empty JSON argv")

                runner_dependencies = [
                    str((repo / item).resolve()) if not Path(item).is_absolute() else item
                    for item in args.benchmark_runner_dependency
                ]
                runner_adapter = ExternalBenchmarkProcessAdapter(
                    command=runner_argv,
                    approved_dependency_paths=runner_dependencies,
                    role="benchmark_runner",
                    **adapter_kwargs,
                )

                capture_path = Path(args.benchmark_capture_output)
                if not capture_path.is_absolute():
                    capture_path = (repo / capture_path).resolve()
                try:
                    capture = capture_live_hidden_task_outputs(manifest_path, runner_adapter.hidden_runner, output_path=capture_path)
                finally:
                    runner_adapter.finalize()
                print(json.dumps(capture, indent=2, sort_keys=True))
                return 0

            verifier = None
            trust_anchor = None
            if args.human_evidence_verifier_command:
                try:
                    verifier_argv = json.loads(args.human_evidence_verifier_command)
                except json.JSONDecodeError as exc:
                    raise BenchmarkIntegrityError(
                        f"human_verifier_command_manifest_invalid: {exc}"
                    ) from exc
                if not isinstance(verifier_argv, list) or not verifier_argv or not all(
                    isinstance(item, str) and item for item in verifier_argv
                ):
                    raise BenchmarkIntegrityError("human verifier command must be a non-empty JSON argv")

                verifier_dependencies = [
                    str((repo / item).resolve()) if not Path(item).is_absolute() else item
                    for item in args.human_evidence_verifier_dependency
                ]
                verifier_adapter = ExternalBenchmarkProcessAdapter(
                    command=verifier_argv,
                    approved_dependency_paths=verifier_dependencies,
                    role="human_evidence_verifier",
                    **adapter_kwargs,
                )
                verifier = verifier_adapter.verifier
                trust_anchor_path = Path(args.human_evidence_trust_anchor)
                if not trust_anchor_path.is_absolute():
                    trust_anchor_path = (repo / trust_anchor_path).resolve()
                try:
                    trust_anchor = json.loads(trust_anchor_path.read_text(encoding="utf-8"))
                except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
                    raise BenchmarkIntegrityError(
                        f"human_evidence_trust_anchor_load_failed: {type(exc).__name__}: {exc}"
                    ) from exc
                if not isinstance(trust_anchor, dict):
                    raise BenchmarkIntegrityError("human evidence trust anchor must be a JSON object")

            try:
                benchmark = evaluate_benchmark_manifest(
                    manifest_path,
                    human_evidence_verifier=verifier,
                    human_evidence_trust_anchor=trust_anchor,
                )
            finally:
                if args.human_evidence_verifier_command:
                    verifier_adapter.finalize()
        except ExternalBenchmarkProcessError as exc:
            print(json.dumps({"status": "external_process_operational_failure", "receipt": exc.receipt}, sort_keys=True), file=sys.stderr)
            return 4
        except BenchmarkIntegrityError as exc:
            print(
                json.dumps(
                    {
                        "status": "benchmark_integrity_error",
                        "error_type": type(exc).__name__,
                        "message": str(exc),
                        "epistemic_effect": "none_operational_outcome_only",
                    },
                    sort_keys=True,
                ),
                file=sys.stderr,
            )
            return 2
        except (OSError, UnicodeDecodeError, json.JSONDecodeError, ValueError) as exc:
            print(
                json.dumps(
                    {
                        "status": "benchmark_configuration_error",
                        "error_type": type(exc).__name__,
                        "message": str(exc),
                        "epistemic_effect": "none_operational_outcome_only",
                    },
                    sort_keys=True,
                ),
                file=sys.stderr,
            )
            return 2
        print(json.dumps(benchmark, indent=2, sort_keys=True))
        if benchmark.get("human_evidence", {}).get("status") == "verifier_operational_failure":
            return 4
        if args.require_replicated and not benchmark["replicated"]:
            return 3
        return 0
    if not args.kb:
        ap.error("--kb is required unless --benchmark-manifest is supplied")
    kb_path = Path(args.kb)
    if not kb_path.exists():
        log_path = logger.finalize("error", summary=f"KB not found: {kb_path}")
        print(f"[LOG] {log_path}", file=sys.stderr)
        raise SystemExit(f"[ERROR] KB not found: {kb_path}")

    try:
        kb_ctx = resolve_kb_reference(kb_path, explicit_kb_ref=args.kb_ref)
    except ValueError as exc:
        log_path = logger.finalize("error", summary=str(exc))
        print(f"[LOG] {log_path}", file=sys.stderr)
        raise SystemExit(f"[ERROR] {exc}")
    kb_ref = str(kb_ctx.get("kb_ref", "")).strip()
    artifacts_dir = canonical_artifacts_dir(repo, kb_ref)
    if args.artifacts_dir:
        requested = Path(args.artifacts_dir)
        if not requested.is_absolute():
            requested = (repo / requested).resolve()
        if requested != artifacts_dir:
            log_path = logger.finalize(
                "error",
                summary=(
                    "Non-canonical artifacts directory rejected. "
                    f"expected={artifacts_dir} requested={requested}"
                ),
            )
            print(f"[LOG] {log_path}", file=sys.stderr)
            raise SystemExit(
                "[ERROR] artifacts are associated with the reference KB name. "
                f"Use canonical path: {artifacts_dir}"
            )

    sim_dir = artifacts_dir / "discovery-simulation"
    sim_dir.mkdir(parents=True, exist_ok=True)
    out_json = Path(args.output_json) if args.output_json else sim_dir / "simulation-report.json"
    out_md = Path(args.output_md) if args.output_md else sim_dir / "simulation-report.md"

    statements = _extract_statements(kb_path)
    raw_gt: dict[str, Any] = {}
    if args.ground_truth:
        raw_gt = _load_yaml(Path(args.ground_truth))
        if not raw_gt:
            raw_gt = _load_json(Path(args.ground_truth))
    gt = _normalize_ground_truth(raw=raw_gt, statements=statements, target_statement_id=args.target_statement_id)
    if args.emit_inferred_ground_truth:
        (sim_dir / "ground-truth.resolved.yaml").write_text(yaml.safe_dump(gt, sort_keys=False), encoding="utf-8")

    working_kb_path = kb_path
    knockout_summary: dict[str, Any] = {
        "profile": str(args.knockout_profile or "none").strip().lower() or "none",
        "working_kb": str(kb_path),
        "removed_statements": [],
        "drop_edges": [],
        "blank_fields": {},
        "blanked_fields_count": 0,
        "dropped_edges_count": 0,
    }
    if (
        knockout_summary["profile"] != "none"
        or args.knockout_statement
        or args.knockout_edge
        or args.knockout_field
        or args.bridge_concept_id
        or args.bridge_concept_term
    ):
        working_kb_path, knockout_summary = _materialize_knockout_kb(
            kb_path=kb_path,
            output_dir=sim_dir / "working-kb",
            target_statement_id=gt.get("target_statement_id", ""),
            profile=args.knockout_profile,
            knockout_statements=args.knockout_statement,
            knockout_edges=args.knockout_edge,
            knockout_fields=args.knockout_field,
            bridge_concept_ids=args.bridge_concept_id,
            bridge_concept_terms=args.bridge_concept_term,
        )

    knockout_active = knockout_summary.get("profile", "none") != "none"
    defaults = {
        "analyze_top_k": 20,
        "min_similarity": 0.12,
        "max_connections": 40,
        "top_links": 20,
        "top_interventions": 12,
        "top_conceptual": 12,
        "entry_top_k": 20,
        "pathway_top_entrypoints": 8,
        "max_hypotheses_per_path": 4,
        "max_links_per_path": 3,
        "bridge_top_k": 20,
        "conjecture_top_bridges": 12,
        "max_conjectures_per_bridge": 3,
        "strategies_top_k": 6,
        "sketch_top_k": 6,
        "support_threshold": 0.60 if knockout_active else 0.62,
        "refute_threshold": 0.60 if knockout_active else 0.62,
        "margin": 0.06 if knockout_active else 0.08,
    }
    pool = _config_pool(defaults)
    max_iter = max(1, args.iterations)

    logger.step(
        "Initialized discovery simulation",
        "\n".join(
            [
                f"kb={kb_path}",
                f"working_kb={working_kb_path}",
                f"kb_ref={kb_ref}",
                f"target_statement_id={gt.get('target_statement_id', '')}",
                f"ground_truth_source={gt.get('source', '')}",
                f"knockout_profile={knockout_summary.get('profile', 'none')}",
                f"iterations={max_iter}",
                f"success_threshold={max(0.0, min(1.0, args.success_threshold))}",
                f"python={args.python}",
                f"simulation_dir={sim_dir}",
            ]
        ),
    )

    success_threshold = max(0.0, min(1.0, args.success_threshold))
    iteration_rows: list[dict[str, Any]] = []
    best_row: dict[str, Any] = {}
    best_score = -1.0

    for idx in range(1, max_iter + 1):
        config = dict(pool[(idx - 1) % len(pool)])
        if idx > len(pool) and best_row.get("config"):
            # Deterministic local refinement around current best.
            config.update(best_row["config"])
            if idx % 2 == 0:
                config["min_similarity"] = max(0.06, _safe_float(config.get("min_similarity", 0.12)) - 0.01)
            else:
                config["top_links"] = min(40, int(config.get("top_links", 20)) + 2)

        iter_result = _run_iteration(
            repo=repo,
            python_exe=args.python,
            kb_path=working_kb_path,
            kb_ref=kb_ref,
            artifacts_dir=artifacts_dir,
            config=config,
            iter_index=idx,
            logger=logger,
        )

        if iter_result.get("success", False):
            artifacts = _load_iteration_artifacts(iter_result.get("paths", {}))
            score = _score_replication(gt=gt, artifacts=artifacts, knockout=knockout_summary)
            iter_row = {
                **iter_result,
                "score": score,
                "iter_dir": str(sim_dir / f"iter-{idx:03d}"),
            }
            current_score = _safe_float(score.get("replication_score", 0.0), 0.0)
            if current_score > best_score:
                best_score = current_score
                best_row = iter_row
        else:
            iter_row = {
                **iter_result,
                "score": {
                    "replication_score": 0.0,
                    "components": {},
                    "counts": {},
                },
                "iter_dir": str(sim_dir / f"iter-{idx:03d}"),
            }
            current_score = 0.0

        iteration_rows.append(iter_row)
        logger.step(
            f"Simulation iteration {idx}",
            "\n".join(
                [
                    f"success={iter_row.get('success', False)}",
                    f"replication_score={current_score:.6f}",
                    "config="
                    + ",".join(f"{k}={v}" for k, v in sorted(config.items())),
                ]
            ),
        )

        if current_score >= success_threshold:
            logger.step(
                "Stopping early: discovery replication reached threshold",
                f"iteration={idx}\nscore={current_score:.6f}\nthreshold={success_threshold:.6f}",
            )
            break

    replicated = best_score >= success_threshold
    report = {
        "metadata": {
            "kb": str(kb_path),
            "working_kb": str(working_kb_path),
            "kb_ref": kb_ref,
            "target_statement_id": gt.get("target_statement_id", ""),
            "ground_truth_source": gt.get("source", ""),
            "knockout_profile": knockout_summary.get("profile", "none"),
            "iterations_requested": max_iter,
            "iterations_executed": len(iteration_rows),
            "success_threshold": success_threshold,
            "best_replication_score": round(max(0.0, best_score), 6),
            "replicated": replicated,
            "simulation_dir": str(sim_dir),
        },
        "ground_truth": gt,
        "knockout": knockout_summary,
        "best_iteration": best_row,
        "iterations": iteration_rows,
    }

    out_json.parent.mkdir(parents=True, exist_ok=True)
    out_md.parent.mkdir(parents=True, exist_ok=True)
    out_json.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    out_md.write_text(_to_markdown(report), encoding="utf-8")
    logger.add_output("discovery_simulation_json", out_json)
    logger.add_output("discovery_simulation_md", out_md)
    if args.emit_inferred_ground_truth:
        logger.add_output("discovery_ground_truth_resolved", sim_dir / "ground-truth.resolved.yaml")
    if str(knockout_summary.get("working_kb", "")).strip():
        logger.add_output("discovery_working_kb", Path(str(knockout_summary["working_kb"])))

    print(f"[OK] Wrote discovery simulation JSON: {out_json}")
    print(f"[OK] Wrote discovery simulation Markdown: {out_md}")
    if best_row:
        print(
            "[OK] Best iteration: {i} (score={s:.6f})".format(
                i=best_row.get("iteration", 0),
                s=_safe_float((best_row.get("score", {}) or {}).get("replication_score", 0.0), 0.0),
            )
        )
    print(f"[OK] Replicated: {replicated}")
    log_path = logger.finalize(
        "success",
        summary=(
            f"Discovery simulation completed with best replication score {max(0.0, best_score):.6f} "
            f"({'replicated' if replicated else 'not yet replicated'})."
        ),
    )
    print(f"[LOG] {log_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
