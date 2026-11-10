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
"""Run the complete receipt-backed YM21 theory-first canonical parent cycle.

Literature acquisition and replay are different authority boundaries.  This
runner consumes only a separately sealed six-lane live acquisition, replays it
without renewing any timestamp, and binds both the normalized snapshot and the
original provider-response bytes.  The preserved 2026-07-21 capture remains
historical surveillance only.  The symbolic experiment is commissioned only
after reflection and remains bounded support; it cannot select a theory or
promote a Yang--Mills claim.
"""

from __future__ import annotations

import argparse
import copy
import fcntl
import hashlib
import json
import os
import re
import stat
import sys
import tempfile
from contextlib import contextmanager
from datetime import datetime
from pathlib import Path
from typing import Any, Mapping, Sequence


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
SCRIPT_ROOT = ROOT / "agentic/scripts"
if str(SCRIPT_ROOT) not in sys.path:
    sys.path.insert(0, str(SCRIPT_ROOT))

from agentic.discovery.contracts import (  # noqa: E402
    ContractError,
    Namespace,
    artifact_descriptor,
    canonical_digest,
    canonical_json,
    file_digest,
    fsync_directory,
    load_json,
    stable_identifier,
    validate_payload,
    verify_artifact_descriptor,
)
from agentic.discovery.cycle import run_canonical_discovery_cycle  # noqa: E402
from agentic.discovery.ledger import initial_state  # noqa: E402
from agentic.discovery.literature import (  # noqa: E402
    DEFAULT_LITERATURE_FRESHNESS_SECONDS,
    LANE_TYPES,
    assimilate_literature,
    bind_source_semantic_warrants,
    build_theory_object_catalog,
    derive_claim_mappings,
    derive_hypothesis_rebase,
    replay_literature_counterfactuals,
    run_frontier_literature_cycle,
    validate_snapshot,
)
from agentic.discovery.literature_acquisition import (  # noqa: E402
    LiteratureAcquisitionError,
    build_source_routing_precommit_certificate,
    load_tool_response_artifact,
    validate_capture_acquisition_bundle,
    validate_source_routing_consumption,
)
from agentic.discovery.receipts import (  # noqa: E402
    DiscoveryOperatorDispatcher,
    ReceiptStore,
    build_operator_request,
)
from agentic.experiments import compile_experiment_spec, triage_probe  # noqa: E402
from agentic.scripts.discovery_operator_registry import load_registry  # noqa: E402
from agentic.scripts.dispatch_discovery_operators import _bindings as registry_bindings  # noqa: E402
from agentic.scripts.run_discovery_operator_protocol import (  # noqa: E402
    prepare_proposal_field_free_high_risk_envelope,
)
from agentic.discovery.hypotheses import (  # noqa: E402
    validate_proposal_field_free_high_risk_elicitation,
)
from evaluate_ym_conceptual_quality_20260721 import (  # noqa: E402
    build_evidence as build_conceptual_quality_evidence,
)
from integrate_ym_representational_dynamics_20260721 import (  # noqa: E402
    BROAD_FRONTIER_CAPTURE,
    DEFAULT_LITERATURE,
    DIRECT_CHALLENGER_ID,
    DIRECT_CLAIM_MAPPING_EXPECTATIONS,
    REPORT_ROOT,
    RIVAL_SEEDS,
    TARGET_ID,
    VERSION,
    bind_registered_canonical_runtime,
    sha256_file,
    validate_frontier_search_capture,
)


RUN_ID = "ym21-canonical-parent-20260721"
STATE_VERSION = 0
REQUESTED_AT = "2026-07-21T22:40:00+02:00"
DEFAULT_OUTPUT_ROOT = REPORT_ROOT / "canonical_parent_cycle"
PARENT_CONCEPTUAL_QUALITY_EVIDENCE_NAME = (
    "independent_conceptual_quality_evidence.parent.json"
)
SYNTHESIS_CONCEPTUAL_QUALITY_EVIDENCE_NAME = (
    "independent_conceptual_quality_evidence.synthesis.json"
)
CONCEPTUAL_QUALITY_REFINEMENT_HISTORY_NAME = (
    "conceptual_quality_refinement_history.json"
)
YM_PROPOSAL_FIELD_FREE_PROMPTS = (
    "Interrogate one neglected distinction in the exact target pressure. This instruction "
    "supplies no primitive, relation, mechanism, candidate answer, or evaluation score.",
    "Probe a conceptual corner where the current descriptions may fail to connect. Preserve "
    "the exact target and protected successes; no proposed explanatory structure is supplied.",
    "Ask what the target would force us to understand if familiar decompositions were "
    "temporarily suspended. Do not infer a preferred ontology or expected answer from this prompt.",
)
CURRENT_FRONTIER_CAPTURE = BROAD_FRONTIER_CAPTURE.with_name(
    "frontier_search_live_capture_20260722.json"
)
CURRENT_FRONTIER_ACQUISITION = BROAD_FRONTIER_CAPTURE.with_name(
    "frontier_search_live_acquisition_20260722.json"
)
CURRENT_FRONTIER_CAPTURE_DATE = "2026-07-22"
CURRENT_SURVEILLANCE_TAGS = frozenset(
    {
        "correction",
        "supersession",
        "withdrawal",
        "bounded_lattice",
        "conceptual_genealogy",
        "adjacent_field",
        "target_mismatch",
    }
)
CURRENT_ACQUISITION_UNAVAILABLE = "current_literature_acquisition_unavailable"
CURRENT_ACQUISITION_INVALID = "current_literature_acquisition_invalid"
PUBLICATION_STATUS_NAME = "publication_status.json"
PUBLICATION_FAILURE_DIR = "publication_failures"
PUBLICATION_FILE_ROLES: dict[str, str] = {
    "canonical_cycle_result.json": "canonical_core",
    "operator_requests.json": "operator_index",
    "operator_receipts.json": "operator_index",
    "artifact_roles.json": "role_index",
    "frozen_provider_source_catalog.json": "frozen_provenance",
    "frozen_live_capture_binding.json": "frozen_provenance",
    "conceptual_generation_trace.json": "causal_trace",
    "literature_routing_counterfactuals.json": "causal_trace",
    PARENT_CONCEPTUAL_QUALITY_EVIDENCE_NAME: "conceptual_evidence",
    SYNTHESIS_CONCEPTUAL_QUALITY_EVIDENCE_NAME: "conceptual_evidence",
    CONCEPTUAL_QUALITY_REFINEMENT_HISTORY_NAME: "refinement_evidence",
    "acceptance_report.json": "acceptance_report",
    "acceptance_report.md": "acceptance_report",
}
SIX_OPERATORS = {
    "frontier-literature-assimilator",
    "high-risk-hypothesis-forger",
    "parallel-hypothesis-portfolio",
    "reflective-conceptual-discovery",
    "dynamic-symbolic-simulation-experimenter",
    "reflective-theory-synthesizer",
}
SYNTHESIS_SYSTEM_ID = "ym21-system-spectral-descent-transport-groupoid"
PROBE_QUESTION_ID = "ym21-question-toy-descent-composition"
PROBE_QUESTION = (
    "Do two declared finite toy regulator paths with local distortion products "
    "2/3*3/4 and 5/8 have equal transport, as path-independent descent would require?"
)

YM_THEORY_MATCH_TERMS: dict[str, tuple[str, ...]] = {
    "YM21-R01": (
        "local observable net",
        "operator algebra",
        "phase space compactness",
        "nuclearity",
    ),
    "YM21-R02": (
        "reflection positivity",
        "schwinger functions",
        "osterwalder schrader",
        "spectral measure",
    ),
    "YM21-R03": (
        "higher form",
        "generalized symmetry",
        "anomaly",
        "theta",
    ),
    "YM21-R04": (
        "stochastic quantization",
        "langevin",
        "markov process",
        "gauge covariant renormalisation",
    ),
    "YM21-R05": (
        "gauge orbit",
        "transport inequality",
        "concentration",
        "coercivity",
    ),
    "YM21-R06": (
        "resurgent",
        "borel",
        "transseries",
        "asymptotic freedom",
    ),
    "YM21-R07": (
        "wilson loop",
        "area law",
        "loop space",
        "duality",
    ),
    "YM21-R08": (
        "hamiltonian",
        "transfer operator",
        "spectral gap",
        "mass gap",
        "resolvent",
    ),
    "YM21-R09": (
        "observable completeness",
        "recovery",
        "local algebra",
        "homotopy aqft",
    ),
    "YM21-R10": (
        "lattice",
        "retained kernel",
        "renormalization group",
        "strong coupling",
        "block",
    ),
}

# The authored R01--R10 deck is an incumbent comparison, not the live theory
# vocabulary.  These many-to-many affinities transfer its already audited
# source axes onto the proposal-field-free corner families without claiming
# that either side is semantically identical.  Every generated corner must be
# represented so a selected candidate cannot silently escape literature
# routing merely because it has a new identifier.
GENERATED_CORNER_LEGACY_AUDIT_AXES: dict[str, tuple[str, ...]] = {
    "ontology_inversion": ("YM21-R03", "YM21-R09"),
    "missing_mediator": ("YM21-R01", "YM21-R02", "YM21-R09"),
    "relation_process_first": ("YM21-R04",),
    "scale_regime_reversal": ("YM21-R08",),
    "cross_field_transfer": ("YM21-R01", "YM21-R05"),
    "unification_conjecture": ("YM21-R03", "YM21-R07"),
    "negative_theory": ("YM21-R03", "YM21-R07"),
    "counter_consensus": ("YM21-R02",),
    "emergence_stabilization": ("YM21-R06",),
    "conservative_control": ("YM21-R10",),
}


class YMCanonicalCycleError(RuntimeError):
    """Raised when a target-specific cycle invariant fails."""


def _registered_theory_claim_from_parent(
    parent_packet: Mapping[str, Any],
    *,
    expected_programme_id: str,
    expected_conceptual_system_ids: Sequence[str],
) -> dict[str, Any]:
    """Derive the only probe claim from the sealed reflective support question.

    The target runner is not allowed to restate the question independently after
    reflection.  Programme, system, question, and digest authority all come from
    one validated parent packet, so a matching-looking caller-authored claim
    cannot commission the experiment.
    """

    packet = copy.deepcopy(dict(parent_packet))
    packet_digest = packet.get("packet_digest")
    if packet_digest != canonical_digest(packet, exclude_keys=("packet_digest",)):
        raise YMCanonicalCycleError("parent reflective packet digest mismatch")
    programme = packet.get("theoretical_programme")
    support = packet.get("support_probe")
    if not isinstance(programme, Mapping) or not isinstance(support, Mapping):
        raise YMCanonicalCycleError("parent reflective programme or support question is missing")
    conceptual_ids = list(support.get("conceptual_system_ids", []))
    expected_ids = sorted(str(value) for value in expected_conceptual_system_ids)
    if len(conceptual_ids) != len(set(conceptual_ids)):
        raise YMCanonicalCycleError("parent support question duplicates a conceptual-system identity")
    if (
        support.get("disposition") != "commissioned"
        or programme.get("programme_id") != expected_programme_id
        or support.get("theory_programme_id") != expected_programme_id
        or sorted(conceptual_ids) != expected_ids
        or support.get("theoretical_question_id") != PROBE_QUESTION_ID
        or support.get("theoretical_question") != PROBE_QUESTION
    ):
        raise YMCanonicalCycleError(
            "parent reflective support question has the wrong programme, system, or question identity"
        )
    core = {
        "claim_id": support["theoretical_question_id"],
        "claim_kind": "model_consequence",
        "target_relation": "toy_or_proxy",
        "statement": support["theoretical_question"],
        "theory_programme_id": support["theory_programme_id"],
        "conceptual_system_ids": expected_ids,
        "source_theory_programme_digest": canonical_digest(programme),
        "source_reflection_packet_digest": packet_digest,
    }
    return {**core, "claim_digest": canonical_digest(core)}


def _write_immutable_bytes(path: Path, encoded: bytes) -> Path:
    """Publish exact bytes atomically without ever replacing prior evidence."""

    path.parent.mkdir(parents=True, exist_ok=True)
    if path.is_symlink():
        raise YMCanonicalCycleError(f"immutable artifact cannot be a symlink: {path}")
    if path.exists():
        if path.read_bytes() != encoded:
            raise YMCanonicalCycleError(f"immutable artifact conflict: {path}")
        return path
    descriptor, temporary_name = tempfile.mkstemp(
        dir=path.parent,
        prefix=f".{path.name}.tmp-",
    )
    temporary_path = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "wb") as stream:
            stream.write(encoded)
            stream.flush()
            os.fsync(stream.fileno())
        try:
            os.link(temporary_path, path)
        except FileExistsError:
            if path.is_symlink() or path.read_bytes() != encoded:
                raise YMCanonicalCycleError(f"immutable artifact conflict: {path}")
        fsync_directory(path.parent)
    finally:
        temporary_path.unlink(missing_ok=True)
    return path


def _write_immutable_json(path: Path, payload: Any) -> Path:
    return _write_immutable_bytes(path, canonical_json(payload) + b"\n")


def _canonical_source_from_dated(row: Mapping[str, Any]) -> dict[str, Any]:
    url = str(row["url"])
    arxiv_id = url.rsplit("/", 1)[-1] if "arxiv.org/abs/" in url else None
    raw_type = str(row.get("source_type", ""))
    source_type = (
        "retraction"
        if row.get("source_status") == "withdrawn"
        else "preprint"
        if "preprint" in raw_type and "journal" not in raw_type
        else "survey"
        if "review" in raw_type
        else "primary"
        if "research" in raw_type or arxiv_id
        else "other"
    )
    claims = [str(item) for item in row.get("reported_claims", [])]
    claims.extend(
        str(item["author_stated_claim"])
        for item in row.get("claim_audit", [])
        if str(item.get("author_stated_claim", "")).strip()
    )
    return {
        "source_id": row["source_id"],
        "work_identity": f"arxiv:{arxiv_id}" if arxiv_id else f"url:{url}",
        "title": row["title"],
        "authors": list(row["authors"]),
        "publication_date": row["publication_date"],
        "source_version": row["source_version"],
        "source_type": source_type,
        "url": url,
        "doi": None,
        "arxiv_id": arxiv_id,
        "correction_status": (
            "retracted"
            if row.get("source_status") == "withdrawn"
            else "unknown"
            if "unverified" in str(row.get("claim_status", ""))
            else "none_known"
        ),
        "decision_relevant": True,
        "claims": sorted(set(claims)),
        "limitations": [
            str(row["transfer_boundary"]),
            f"Dated capture status: {row['claim_status']}; no source claim is validated by retrieval.",
        ],
    }


ADDITIONAL_SOURCES: dict[str, dict[str, Any]] = {
    "nature-review-2026-douglas": {
        "title": "The Yang-Mills Millennium problem",
        "authors": ["Michael R. Douglas"],
        "publication_date": "2026-01-06",
        "source_version": "Nature Reviews Physics 8 (2026)",
        "source_type": "survey",
        "url": "https://www.nature.com/articles/s42254-025-00909-2",
        "claims": [
            "A rigorous four-dimensional continuum construction remains missing, with stochastic and strong-coupling approaches among the promising programmes."
        ],
        "limitations": [
            "A current expert review positions the frontier but is not a proof or an exhaustive impossibility result."
        ],
    },
    "zenodo-19614728": {
        "title": "Mass Gap and Nontriviality for Four-Dimensional Yang-Mills via Lattice Coercivity and a Symmetry-Forced Haar Measure",
        "authors": ["Harold D. Kirk"],
        "publication_date": "2026-04-16",
        "source_version": "2.0",
        "source_type": "preprint",
        "url": "https://zenodo.org/records/19614728",
        "claims": [
            "Lattice coercivity yields a volume-uniform Poincare inequality along the claimed weak-coupling continuum corridor.",
            "Complete analyticity and uniform clustering produce a lattice mass-gap estimate.",
            "A subsequential continuum limit satisfies Osterwalder-Schrader requirements and retains a positive mass gap.",
            "A symmetry-forced Haar marginal establishes nontriviality of the continuum theory."
        ],
        "limitations": [
            "These are author-stated repository claims; coercivity constants, continuum tightness, OS axioms, and nontriviality have not been independently audited here."
        ],
    },
    "preprints-202604.0332-v1": {
        "title": "A Non-Perturbative Proof of the Yang-Mills Mass Gap via Null-Cone Equal-Weight Decomposition and Construction of the Hilbert-Polya Operator",
        "authors": ["Jiazheng Liu"],
        "publication_date": "2026-04-06",
        "source_version": "v1",
        "source_type": "preprint",
        "url": "https://www.preprints.org/manuscript/202604.0332/v1",
        "claims": [
            "The manuscript claims a Wightman-compatible nonperturbative Yang-Mills construction and positive mass gap.",
            "The manuscript claims asymptotic freedom and a Hilbert-Polya operator through a null-cone equal-weight decomposition."
        ],
        "limitations": [
            "The platform marks this manuscript non-peer-reviewed; its analytic construction and operator claims remain unverified."
        ],
    },
    "ssrn-4819820": {
        "title": "Yang Mills Mass Gap Solution",
        "authors": ["Jonathan Wilson"],
        "publication_date": "2024-05-07",
        "source_version": "SSRN 4819820",
        "source_type": "preprint",
        "url": "https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4819820",
        "claims": [
            "The abstract claims a rigorous Yang-Mills mass-gap solution using Gribov-Zwanziger structure, resurgence, spectral analysis, and Osterwalder-Schrader reconstruction."
        ],
        "limitations": [
            "Only the primary abstract was inspected; the direct solution claim is unverified and cannot alter official target status."
        ],
    },
    "philarchive-nielsen-2026-v9": {
        "title": "The Definitive Proof of the Four-Dimensional Yang-Mills Mass Gap",
        "authors": ["Jennifer L. Nielsen"],
        "publication_date": "2026-02-19",
        "source_version": "v9",
        "source_type": "preprint",
        "url": "https://philarchive.org/archive/NIETEO-12v9",
        "claims": [
            "The paper claims continuum construction, scale-uniform contraction, confinement, and a positive four-dimensional mass gap."
        ],
        "limitations": [
            "The direct proof claim is unverified; every uniformity, noncircularity, and target-identity step requires independent checking."
        ],
    },
    "arxiv-2307.00788-v7": {
        "title": "Positive mass gap of quantum Yang-Mills Fields",
        "authors": ["Adrian P. C. Lim"],
        "publication_date": "2023-07-03",
        "source_version": "v7 (2025-01-13)",
        "source_type": "preprint",
        "url": "https://arxiv.org/abs/2307.00788",
        "arxiv_id": "2307.00788",
        "claims": [
            "The current abstract claims a Wightman Yang-Mills theory and a positive infimum over representation-indexed mass gaps."
        ],
        "limitations": [
            "The construction, representation infimum, and relation to the exact Clay target remain unverified."
        ],
    },
    "yangmills-dev-odusanya-2026": {
        "title": "Yang-Mills Mass Gap - Constructive Proof",
        "authors": ["Oliver Odusanya"],
        "publication_date": "2026",
        "source_version": "site observed 2026-07-21",
        "source_type": "other",
        "url": "https://yangmills.dev/",
        "claims": [
            "The site claims a constructive lattice-to-continuum resolution through a multi-paper Balaban-RG programme."
        ],
        "limitations": [
            "A programme site is useful for surveillance but supplies no independent validation or stable theorem-level review."
        ],
    },
    "recognition-washburn-2026": {
        "title": "Yang-Mills Mass Gap: Unconditional Lattice Gap and an AF-free Continuum Construction",
        "authors": ["Jonathan Washburn"],
        "publication_date": "2026",
        "source_version": "site observed 2026-07-21",
        "source_type": "preprint",
        "url": "https://recognitionphysics.org/papers/yang-mills.html",
        "claims": [
            "The programme claims a volume-uniform lattice gap and norm-resolvent continuum construction without an asymptotic-freedom bridge."
        ],
        "limitations": [
            "The direct claim is unverified; fixed-region convergence, continuum identity, and spectral transfer require independent proof."
        ],
    },
    "ssrn-6004114": {
        "title": "The Vacuum has Steps: A Constructive, Geometric Route to the Yang-Mills Mass Gap, told from the Inside",
        "authors": ["Emmanouil Karolos Cizek"],
        "publication_date": "2026-01-26",
        "source_version": "SSRN 6004114",
        "source_type": "other",
        "url": "https://papers.ssrn.com/sol3/papers.cfm?abstract_id=6004114",
        "claims": [
            "The paper presents an explanatory overview of a constructive geometric programme and its proof burdens rather than a standalone technical solution."
        ],
        "limitations": [
            "The eight-page overview is programme genealogy, not theorem evidence for the Clay target."
        ],
    },
    "zenodo-19423313": {
        "title": "The Yang-Mills Mass Gap: From Proof Attempts to Dissolution by Recontextualisation",
        "authors": ["John Henry Watt"],
        "publication_date": "2026-04-04",
        "source_version": "record 19423313",
        "source_type": "other",
        "url": "https://zenodo.org/records/19423313",
        "claims": [
            "The essay argues that the continuum formulation removes the discrete mechanism responsible for lattice spectral separation."
        ],
        "limitations": [
            "This is a dissenting conceptual position, not an accepted no-gap theorem or target-status authority."
        ],
    },
    "arxiv-2204.12737": {
        "title": "A stochastic analysis approach to lattice Yang-Mills at strong coupling",
        "authors": ["Hao Shen", "Rongchan Zhu", "Xiangchan Zhu"],
        "publication_date": "2022-04-27",
        "source_version": "arXiv 2204.12737",
        "source_type": "primary",
        "url": "https://arxiv.org/abs/2204.12737",
        "arxiv_id": "2204.12737",
        "claims": [
            "Strong-coupling lattice Yang-Mills satisfies rigorous functional inequalities and decay estimates in the paper's bounded regime."
        ],
        "limitations": [
            "The result is lattice strong coupling and does not establish the weak-coupling continuum four-dimensional Clay target."
        ],
    },
}


def _additional_source(source_id: str, row: Mapping[str, Any]) -> dict[str, Any]:
    url = str(row["url"])
    payload = {
        "source_id": source_id,
        "work_identity": (
            f"arxiv:{row['arxiv_id']}" if row.get("arxiv_id") else f"url:{url}"
        ),
        "title": row["title"],
        "authors": list(row["authors"]),
        "publication_date": row["publication_date"],
        "source_version": row["source_version"],
        "source_type": row["source_type"],
        "url": url,
        "doi": None,
        "arxiv_id": row.get("arxiv_id"),
        "correction_status": (
            "none_known" if row["source_type"] in {"primary", "survey"} else "unknown"
        ),
        "decision_relevant": True,
        "claims": list(row["claims"]),
        "limitations": list(row["limitations"]),
    }
    return payload


def build_provider_source_catalog(
    broad_capture: Mapping[str, Any], dated_literature: Mapping[str, Any]
) -> dict[str, dict[str, Any]]:
    """Build source records only for raw results explicitly dispositioned in scope."""

    dated = {
        row["source_id"]: _canonical_source_from_dated(row)
        for row in dated_literature["sources"]
    }
    additions = {
        source_id: _additional_source(source_id, row)
        for source_id, row in ADDITIONAL_SOURCES.items()
    }
    available = {**dated, **additions}
    included_ids = {
        row["source_id"]
        for row in broad_capture["raw_results"]
        if str(row["disposition"]).startswith("included")
    }
    missing = included_ids - set(available)
    if missing:
        raise YMCanonicalCycleError(f"included raw results lack source metadata: {sorted(missing)}")
    catalog = {source_id: copy.deepcopy(available[source_id]) for source_id in sorted(included_ids)}
    if set(catalog) != included_ids:
        raise YMCanonicalCycleError("provider catalog/raw inclusion boundary drift")
    return catalog


def _read_no_follow_bytes(path: Path, *, label: str) -> bytes:
    """Read one authority artifact once, rejecting links and concurrent drift."""

    flags = os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0)
    try:
        descriptor = os.open(path, flags)
    except OSError as exc:
        reason = (
            CURRENT_ACQUISITION_UNAVAILABLE
            if not os.path.lexists(path)
            else CURRENT_ACQUISITION_INVALID
        )
        raise YMCanonicalCycleError(f"{reason}: {label}: {exc}") from exc
    try:
        before = os.fstat(descriptor)
        if not stat.S_ISREG(before.st_mode):
            raise YMCanonicalCycleError(
                f"{CURRENT_ACQUISITION_INVALID}: {label} is not a regular file"
            )
        chunks: list[bytes] = []
        while True:
            chunk = os.read(descriptor, 1024 * 1024)
            if not chunk:
                break
            chunks.append(chunk)
        after = os.fstat(descriptor)
    finally:
        os.close(descriptor)
    if (before.st_dev, before.st_ino, before.st_size) != (
        after.st_dev,
        after.st_ino,
        after.st_size,
    ):
        raise YMCanonicalCycleError(
            f"{CURRENT_ACQUISITION_INVALID}: {label} changed while read"
        )
    payload = b"".join(chunks)
    if len(payload) != before.st_size:
        raise YMCanonicalCycleError(
            f"{CURRENT_ACQUISITION_INVALID}: {label} byte count drift"
        )
    return payload


def _read_no_follow_json(path: Path, *, label: str) -> tuple[dict[str, Any], bytes]:
    encoded = _read_no_follow_bytes(path, label=label)
    try:
        payload = json.loads(encoded)
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise YMCanonicalCycleError(
            f"{CURRENT_ACQUISITION_INVALID}: {label} is not JSON"
        ) from exc
    if not isinstance(payload, dict):
        raise YMCanonicalCycleError(
            f"{CURRENT_ACQUISITION_INVALID}: {label} must be a JSON object"
        )
    return payload, encoded


def _capture_time(value: Any, *, label: str) -> datetime:
    try:
        parsed = datetime.fromisoformat(str(value).replace("Z", "+00:00"))
    except ValueError as exc:
        raise YMCanonicalCycleError(
            f"{CURRENT_ACQUISITION_INVALID}: {label} is not an ISO date-time"
        ) from exc
    if parsed.tzinfo is None:
        raise YMCanonicalCycleError(
            f"{CURRENT_ACQUISITION_INVALID}: {label} must be timezone-aware"
        )
    return parsed


def _portable_authority_path(path: Path) -> str:
    resolved = path.resolve()
    try:
        return str(resolved.relative_to(ROOT))
    except ValueError:
        return str(resolved)


def load_current_frontier_acquisition(
    *,
    theory_state_digest: str | None = None,
    capture_path: Path = CURRENT_FRONTIER_CAPTURE,
    acquisition_path: Path = CURRENT_FRONTIER_ACQUISITION,
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    """Load one genuine current acquisition or fail before theory investment.

    The normalized snapshot alone is insufficient.  The capture must bind one
    immutable provider-response byte artifact per differentiated lane, and the
    acquisition timestamps, queries, included source set, and lane receipts
    must agree exactly.  This function never executes a provider.
    """

    capture, capture_bytes = _read_no_follow_json(
        capture_path, label="2026-07-22 frontier capture"
    )
    try:
        validate_frontier_search_capture(capture)
    except Exception as exc:
        raise YMCanonicalCycleError(
            f"{CURRENT_ACQUISITION_INVALID}: frontier capture contract failed: {exc}"
        ) from exc
    started = _capture_time(capture.get("capture_started_at"), label="capture start")
    completed = _capture_time(
        capture.get("capture_completed_at"), label="capture completion"
    )
    if (
        started.date().isoformat() != CURRENT_FRONTIER_CAPTURE_DATE
        or completed.date().isoformat() != CURRENT_FRONTIER_CAPTURE_DATE
        or started > completed
    ):
        raise YMCanonicalCycleError(
            f"{CURRENT_ACQUISITION_INVALID}: capture is not an ordered 2026-07-22 acquisition"
        )
    observed_tags = {
        str(tag)
        for row in capture["raw_results"]
        for tag in row.get("surveillance_tags", [])
    }
    missing_tags = sorted(CURRENT_SURVEILLANCE_TAGS - observed_tags)
    if missing_tags:
        raise YMCanonicalCycleError(
            f"{CURRENT_ACQUISITION_INVALID}: capture misses surveillance tags {missing_tags}"
        )
    target_mismatches = [
        row
        for row in capture["raw_results"]
        if "target_mismatch" in row.get("surveillance_tags", [])
    ]
    if not target_mismatches or any(
        str(row["disposition"]).startswith("included") for row in target_mismatches
    ):
        raise YMCanonicalCycleError(
            f"{CURRENT_ACQUISITION_INVALID}: target-mismatch surveillance must remain excluded"
        )
    response_descriptors = capture.get("provider_response_artifacts")
    lane_ids = {str(row["lane_id"]) for row in capture["lanes"]}
    if (
        not isinstance(response_descriptors, list)
        or len(response_descriptors) != len(LANE_TYPES)
        or {str(row.get("lane_id")) for row in response_descriptors} != lane_ids
    ):
        raise YMCanonicalCycleError(
            f"{CURRENT_ACQUISITION_INVALID}: capture requires exactly six provider-response byte descriptors"
        )

    acquisition, acquisition_bytes = _read_no_follow_json(
        acquisition_path, label="2026-07-22 normalized live acquisition"
    )
    try:
        validate_snapshot(acquisition)
    except Exception as exc:
        raise YMCanonicalCycleError(
            f"{CURRENT_ACQUISITION_INVALID}: normalized acquisition failed validation: {exc}"
        ) from exc
    if (
        acquisition["target_id"] != TARGET_ID
        or acquisition["provenance_mode"] != "live"
        or acquisition["validation_status"] != "validated"
        or any(
            row["execution_mode"] != "live" or row["status"] != "completed"
            for row in acquisition["lane_receipts"]
        )
    ):
        raise YMCanonicalCycleError(
            f"{CURRENT_ACQUISITION_INVALID}: normalized acquisition is not the exact six-lane live target acquisition"
        )
    if theory_state_digest is not None and acquisition["theory_state_digest"] != theory_state_digest:
        raise YMCanonicalCycleError(
            f"{CURRENT_ACQUISITION_INVALID}: acquisition theory-state digest mismatch"
        )
    if (
        acquisition["search_started_at"] != capture["capture_started_at"]
        or acquisition["search_completed_at"] != capture["capture_completed_at"]
        or acquisition["coverage_cutoff"] != capture["coverage_cutoff"]
    ):
        raise YMCanonicalCycleError(
            f"{CURRENT_ACQUISITION_INVALID}: capture/acquisition temporal boundary drift"
        )

    try:
        authority_root = capture_path.parent.resolve(strict=True)
        artifacts_by_path: dict[str, tuple[dict[str, Any], bytes]] = {}
        for descriptor in response_descriptors:
            descriptor_path = str(descriptor["path"])
            artifacts_by_path[descriptor_path] = load_tool_response_artifact(
                Path(descriptor_path), authority_root=authority_root
            )
        strict_authority = validate_capture_acquisition_bundle(
            capture=capture,
            acquisition=acquisition,
            artifacts_by_path=artifacts_by_path,
            version_graphs=list(capture["version_lineages"]),
        )
    except (LiteratureAcquisitionError, OSError) as exc:
        raise YMCanonicalCycleError(
            f"{CURRENT_ACQUISITION_INVALID}: {exc}"
        ) from exc
    authority = {
        "capture_sha256": hashlib.sha256(capture_bytes).hexdigest(),
        "acquisition_sha256": hashlib.sha256(acquisition_bytes).hexdigest(),
        "provider_response_artifacts": sorted(
            copy.deepcopy(response_descriptors), key=lambda row: str(row["lane_id"])
        ),
        "validated_acquisition_authority": strict_authority,
    }
    return capture, acquisition, authority


def _replay_current_frontier_acquisition(
    acquisition: Mapping[str, Any],
) -> dict[str, Any]:
    """Replay one validated acquisition without invoking time or provider code."""

    request = {
        "target_id": acquisition["target_id"],
        "claim_scope": acquisition["claim_scope"],
        "theory_state_digest": acquisition["theory_state_digest"],
        "coverage_cutoff": acquisition["coverage_cutoff"],
        "inclusion_policy": acquisition["inclusion_policy"],
        "exclusion_policy": acquisition["exclusion_policy"],
        "coverage_limits": list(acquisition["coverage_limits"]),
        "search_lanes": [
            {
                "lane_id": receipt["lane_id"],
                "lane_type": receipt["lane_type"],
                "queries": list(receipt["queries"]),
                "provider": receipt["provider"],
                "index": receipt["index"],
                "coverage_cutoff": receipt["coverage_cutoff"],
                "inclusion_policy": receipt["inclusion_policy"],
                "exclusion_policy": receipt["exclusion_policy"],
            }
            for receipt in acquisition["lane_receipts"]
        ],
    }
    replay = run_frontier_literature_cycle(
        request, frozen_response_snapshot=acquisition
    )
    if replay["provenance_mode"] != "frozen_response_replay":
        raise YMCanonicalCycleError(
            f"{CURRENT_ACQUISITION_INVALID}: current acquisition did not enter non-renewing replay"
        )
    return replay


def _current_frontier_binding(
    *,
    capture_path: Path,
    acquisition_path: Path,
    capture: Mapping[str, Any],
    acquisition: Mapping[str, Any],
    authority: Mapping[str, Any],
) -> dict[str, Any]:
    historical, historical_bytes = _read_no_follow_json(
        BROAD_FRONTIER_CAPTURE, label="historical 2026-07-21 frontier capture"
    )
    validate_frontier_search_capture(historical)
    return {
        "binding_version": "3.0",
        "capture_path": _portable_authority_path(capture_path),
        "capture_id": capture["capture_id"],
        "capture_sha256": authority["capture_sha256"],
        "raw_result_count": len(capture["raw_results"]),
        "included_source_count": len(acquisition["sources"]),
        "excluded_raw_result_ids": [
            row["result_id"]
            for row in capture["raw_results"]
            if not str(row["disposition"]).startswith("included")
        ],
        "adapter_boundary": capture["provider"]["execution_boundary"],
        "acquisition_path": _portable_authority_path(acquisition_path),
        "acquisition_snapshot_id": acquisition["snapshot_id"],
        "acquisition_snapshot_digest": acquisition["content_digest"],
        "acquisition_sha256": authority["acquisition_sha256"],
        "acquisition_started_at": acquisition["search_started_at"],
        "acquisition_completed_at": acquisition["search_completed_at"],
        "acquisition_validator_receipt_ids": [
            row["receipt_id"] for row in acquisition["validator_receipts"]
        ],
        "provider_response_artifacts": copy.deepcopy(
            authority["provider_response_artifacts"]
        ),
        "validated_acquisition_authority": copy.deepcopy(
            authority["validated_acquisition_authority"]
        ),
        "surveillance_tags": sorted(CURRENT_SURVEILLANCE_TAGS),
        "consumption_mode": "frozen_response_replay",
        "present_use_requires_governed_freshness_resolution": True,
        "historical_capture": {
            "capture_path": _portable_authority_path(BROAD_FRONTIER_CAPTURE),
            "capture_id": historical["capture_id"],
            "capture_sha256": hashlib.sha256(historical_bytes).hexdigest(),
            "authority": "historical_only_nonrenewing_no_present_investment",
        },
    }


def expected_current_frontier_provenance(
    *,
    theory_state_digest: str | None = None,
    capture_path: Path = CURRENT_FRONTIER_CAPTURE,
    acquisition_path: Path = CURRENT_FRONTIER_ACQUISITION,
) -> tuple[dict[str, Any], dict[str, Any]]:
    """Return the exact source catalog and immutable acquisition binding."""

    capture, acquisition, authority = load_current_frontier_acquisition(
        theory_state_digest=theory_state_digest,
        capture_path=capture_path,
        acquisition_path=acquisition_path,
    )
    return (
        {"sources": copy.deepcopy(acquisition["sources"])},
        _current_frontier_binding(
            capture_path=capture_path,
            acquisition_path=acquisition_path,
            capture=capture,
            acquisition=acquisition,
            authority=authority,
        ),
    )


def build_current_literature_snapshot(
    *,
    theory_state_digest: str,
    output_root: Path,
    capture_path: Path = CURRENT_FRONTIER_CAPTURE,
    acquisition_path: Path = CURRENT_FRONTIER_ACQUISITION,
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    """Replay the current sealed acquisition; never relabel historical bytes."""

    del output_root
    capture, acquisition, authority = load_current_frontier_acquisition(
        theory_state_digest=theory_state_digest,
        capture_path=capture_path,
        acquisition_path=acquisition_path,
    )
    snapshot = _replay_current_frontier_acquisition(acquisition)
    raw_mappings = _theory_mappings(snapshot)
    raw_warrants = _ym_semantic_source_warrants(snapshot)
    validate_source_routing_consumption(
        authority=authority["validated_acquisition_authority"],
        sources=snapshot["sources"],
        stage="pre_warrant_binding",
        theory_mappings=raw_mappings,
        semantic_warrants=raw_warrants,
        require_complete_mapping=True,
    )
    snapshot = bind_source_semantic_warrants(
        snapshot,
        raw_warrants,
        authority_id="ym21-source-claim-audit.v1",
    )
    validate_snapshot(snapshot)
    validate_source_routing_consumption(
        authority=authority["validated_acquisition_authority"],
        sources=snapshot["sources"],
        stage="post_warrant_binding",
        theory_mappings=raw_mappings,
        semantic_warrants=[
            {**warrant, "source_id": source["source_id"]}
            for source in snapshot["sources"]
            for warrant in source.get("semantic_warrants", [])
        ],
        require_complete_mapping=True,
    )
    binding = _current_frontier_binding(
        capture_path=capture_path,
        acquisition_path=acquisition_path,
        capture=capture,
        acquisition=acquisition,
        authority=authority,
    )
    return snapshot, binding, {"sources": copy.deepcopy(acquisition["sources"])}


def _theory_mappings(snapshot: Mapping[str, Any]) -> list[dict[str, Any]]:
    """Map every observed claim without treating versioned claims as support.

    The current acquisition can contain a different number and order of claims
    for every source.  Version-lineage status is therefore interpreted by
    source identity here and is enforced again by the acquisition routing gate:
    superseded v1/v2 records create correction pressure only, current v3 creates
    an unverified audit question only, and an unseen source is admitted as an
    unresolved target-scope observation instead of crashing the cycle.
    """

    sources = {row["source_id"]: row for row in snapshot["sources"]}
    coverage = list(snapshot["coverage_limits"])
    mappings: list[dict[str, Any]] = []

    dated = load_json(DEFAULT_LITERATURE)
    challenger = next(
        (
            row
            for row in dated["sources"]
            if row["source_id"] == DIRECT_CHALLENGER_ID
        ),
        None,
    )
    oracle = load_json(DIRECT_CLAIM_MAPPING_EXPECTATIONS)
    effects = {row["claim_id"]: row for row in oracle["claim_mappings"]}
    challenger_audits = {
        _exact_claim_key(row["author_stated_claim"]): row
        for row in (challenger or {}).get("claim_audit", [])
    }
    if DIRECT_CHALLENGER_ID in sources:
        source = sources[DIRECT_CHALLENGER_ID]
        for claim in source["claims"]:
            audit = challenger_audits.get(_exact_claim_key(claim))
            effect = effects.get(audit["claim_id"]) if audit else None
            targets = (
                sorted({audit["claim_id"], *effect["affected_rival_ids"]})
                if audit and effect
                else ["YM21-TARGET-SCOPE"]
            )
            mappings.append(
                {
                    "source_id": DIRECT_CHALLENGER_ID,
                    "theory_object_ids": targets,
                    "object_kinds": ["genealogy", "proof_obligation", "schedule"],
                    "relation": "leaves_open",
                    "exact_claim": claim,
                    "source_limitation": source["limitations"][0],
                    "conceptual_change": (
                        f"Open an unverified claim-specific audit: {audit['required_obligation']} "
                        f"Rationale: {effect['rationale']} Counterfactual: {effect['counterfactual_test']}"
                        if audit and effect
                        else "The current claim has no exact frozen audit match and remains an unresolved target-scope question."
                    ),
                    "event_type": "new_question" if audit and effect else "justified_no_change",
                    "coverage_limits": coverage,
                    "confidence": "low",
                }
            )

    mapping_policy: dict[str, tuple[list[str], str, str, str, str]] = {
        "clay-ym-current": (["YM21-R02", "YM21-R08", "YM21-R10"], "contradicts", "demote", "high", "official open-status pressure"),
        "nature-review-2026-douglas": (["YM21-R04", "YM21-R05", "YM21-R10"], "reframes", "reframe", "medium", "current review boundary"),
        "arxiv-2204.12737": (["YM21-R04", "YM21-R05", "YM21-R10"], "reframes", "reframe", "high", "bounded strong-coupling result"),
        "zenodo-18837540": (["YM21-R01", "YM21-R05", "YM21-R10"], "reframes", "reframe", "low", "superseded v1 correction context"),
        "zenodo-19614728": (["YM21-R02", "YM21-R05", "YM21-R08", "YM21-R10"], "reframes", "reframe", "low", "superseded v2 correction context"),
        "zenodo-21479499": (["YM21-R02", "YM21-R05", "YM21-R08", "YM21-R10"], "leaves_open", "new_question", "low", "current unverified v3 claim audit"),
        "arxiv-2506.00284-withdrawn": (["YM21-R10"], "contradicts", "retire", "high", "withdrawal evidence"),
        "preprints-202506.2241-withdrawn": (["YM21-R08", "YM21-R10"], "contradicts", "retire", "high", "withdrawal evidence"),
        "cambridge-67cb65676dde43c908f9dab6-retracted": (["YM21-R08", "YM21-R10"], "contradicts", "retire", "high", "retraction evidence"),
    }
    already = {DIRECT_CHALLENGER_ID} if DIRECT_CHALLENGER_ID in sources else set()
    for source_id, source in sorted(sources.items()):
        if source_id in already:
            continue
        policy = mapping_policy.get(source_id)
        if policy is None:
            policy = (
                ["YM21-TARGET-SCOPE"],
                "leaves_open",
                "justified_no_change",
                "low",
                "unseen source admitted without a source-specific semantic policy",
            )
        targets, relation, event_type, confidence, policy_boundary = policy
        for claim in source["claims"]:
            mappings.append(
                {
                    "source_id": source_id,
                    "theory_object_ids": list(targets),
                    "object_kinds": ["genealogy", "proof_obligation", "schedule"],
                    "relation": relation,
                    "exact_claim": claim,
                    "source_limitation": source["limitations"][0],
                    "conceptual_change": (
                        f"{policy_boundary}; {event_type} only the named objects after respecting this exact boundary: "
                        f"{source['limitations'][0]}"
                    ),
                    "event_type": event_type,
                    "coverage_limits": coverage,
                    "confidence": confidence,
                }
            )
    mapped = {row["source_id"] for row in mappings}
    if mapped != set(sources):
        raise YMCanonicalCycleError("decision-relevant live sources are not causally closed")
    return sorted(
        mappings,
        key=lambda row: (
            str(row["source_id"]),
            _exact_claim_key(row["exact_claim"]),
            tuple(row["theory_object_ids"]),
        ),
    )


def _ym_semantic_source_warrants(
    snapshot: Mapping[str, Any],
    *,
    generated_portfolio: Mapping[str, Any] | None = None,
) -> list[dict[str, Any]]:
    """Translate the existing claim audit into bounded source-level warrants.

    The translation is an internal target-specific interpretation, not a source
    truth or theorem judgment.  Claims absent from the audit are retained as
    explicit unresolved records rather than silently falling through.
    """

    candidate_by_corner = (
        _generated_candidate_index(generated_portfolio)
        if generated_portfolio is not None
        else None
    )
    expected_generated_ids = (
        {
            str(candidate["hypothesis_id"])
            for candidate in candidate_by_corner.values()
        }
        if candidate_by_corner is not None
        else set()
    )
    valid_ids = {"YM21-TARGET-SCOPE", *YM_THEORY_MATCH_TERMS}
    warrants: list[dict[str, Any]] = []
    covered: set[tuple[str, str]] = set()
    relation_map = {
        "contradicts": "contradicts",
        "leaves_open": "leaves_open",
        "supports": "entails",
        "absorbs": "entails",
        "sharpens": "entails",
        "transfers": "entails",
        "reframes": "unresolved",
    }
    for mapping in _theory_mappings(snapshot):
        key = (
            str(mapping["source_id"]),
            _exact_claim_key(mapping["exact_claim"]),
        )
        covered.add(key)
        audited_axes = set(mapping["theory_object_ids"]) & set(YM_THEORY_MATCH_TERMS)
        if candidate_by_corner is None:
            targets = sorted(
                set(mapping["theory_object_ids"]) & valid_ids
            ) or ["YM21-TARGET-SCOPE"]
            authority_id = "ym21-source-claim-audit.v1"
            warrant_text = mapping["conceptual_change"]
        else:
            targets = sorted(
                {
                    str(candidate_by_corner[corner]["hypothesis_id"])
                    for corner, legacy_axes in GENERATED_CORNER_LEGACY_AUDIT_AXES.items()
                    if audited_axes & set(legacy_axes)
                }
            ) or ["YM21-TARGET-SCOPE"]
            authority_id = "ym21-generated-candidate-source-claim-audit.v2"
            warrant_text = (
                "Internal candidate-axis translation of the frozen YM claim audit; "
                "the source does not assert identity between the incumbent audit axis "
                "and the generated candidate. "
                + str(mapping["conceptual_change"])
            )
        warrants.append(
            {
                "source_id": mapping["source_id"],
                "exact_claim": mapping["exact_claim"],
                "theory_object_ids": targets,
                # An unaudited question is unresolved at the warrant layer.
                # `leaves_open` is a mapping effect, and cannot be a semantic
                # warrant for a retracted/withdrawn negative-only source.
                "relation": (
                    "unresolved"
                    if mapping["relation"] == "leaves_open"
                    else relation_map.get(mapping["relation"], "unresolved")
                ),
                "warrant_text": warrant_text,
                "evidence_locator": (
                    f"frozen source {mapping['source_id']} exact claim and target audit"
                ),
                "authority_id": authority_id,
            }
        )
    for source in snapshot["sources"]:
        for exact_claim in source["claims"]:
            key = (str(source["source_id"]), _exact_claim_key(exact_claim))
            if key in covered:
                continue
            warrants.append(
                {
                    "source_id": source["source_id"],
                    "exact_claim": exact_claim,
                    "theory_object_ids": ["YM21-TARGET-SCOPE"],
                    "relation": "unresolved",
                    "warrant_text": (
                        "No claim-specific target relation was supplied by the frozen "
                        "YM audit; preserve this claim as unresolved."
                    ),
                    "evidence_locator": f"frozen source {source['source_id']} claim list",
                    "authority_id": (
                        "ym21-generated-candidate-source-claim-audit.v2"
                        if candidate_by_corner is not None
                        else "ym21-source-claim-audit.v1"
                    ),
                }
            )
    if candidate_by_corner is not None:
        bound_ids = {
            str(theory_object_id)
            for warrant in warrants
            for theory_object_id in warrant["theory_object_ids"]
            if theory_object_id != "YM21-TARGET-SCOPE"
        }
        if bound_ids != expected_generated_ids:
            raise YMCanonicalCycleError(
                "generated candidate/source-warrant binding is not exhaustive: "
                f"missing={sorted(expected_generated_ids - bound_ids)}, "
                f"extra={sorted(bound_ids - expected_generated_ids)}"
            )
    return warrants


def _exact_claim_key(value: Any) -> str:
    """Return the same case/whitespace identity used by the generic mapper."""

    return " ".join(str(value).split()).casefold()


def _generated_candidate_index(
    portfolio: Mapping[str, Any],
) -> dict[str, dict[str, Any]]:
    """Return the exact one-candidate-per-corner proposal-field-free index."""

    if portfolio.get("generation_provenance", {}).get("mode") not in {
        "proposal_field_free_authored_operator",
        "proposal_field_free_provider",
    }:
        raise YMCanonicalCycleError(
            "YM generated-ID binding requires a proposal-field-free portfolio"
        )
    candidates = [dict(row) for row in portfolio.get("hypotheses", [])]
    by_corner = {str(row.get("corner_family")): row for row in candidates}
    if (
        len(candidates) != len(GENERATED_CORNER_LEGACY_AUDIT_AXES)
        or len(by_corner) != len(candidates)
        or set(by_corner) != set(GENERATED_CORNER_LEGACY_AUDIT_AXES)
    ):
        raise YMCanonicalCycleError(
            "proposal-field-free YM selection must contain exactly one candidate "
            "for every generated conceptual corner"
        )
    identifiers = [str(row.get("hypothesis_id")) for row in candidates]
    if len(set(identifiers)) != len(identifiers) or not all(
        identifier.startswith("hypothesis.") for identifier in identifiers
    ):
        raise YMCanonicalCycleError(
            "proposal-field-free YM candidates require unique generated hypothesis IDs"
        )
    return by_corner


def _snapshot_theory_object_ids(snapshot: Mapping[str, Any]) -> set[str]:
    """Collect only structured theory IDs carried by exact source warrants."""

    return {
        str(theory_object_id)
        for source in snapshot.get("sources", [])
        for warrant in source.get("semantic_warrants", [])
        for theory_object_id in warrant.get("theory_object_ids", [])
    }


def _ym_theory_catalog(snapshot: Mapping[str, Any]) -> dict[str, Any]:
    """Freeze the live generated vocabulary, with historical replay fallback."""

    source_bound_ids = _snapshot_theory_object_ids(snapshot)
    generated_ids = sorted(
        theory_object_id
        for theory_object_id in source_bound_ids
        if theory_object_id.startswith("hypothesis.")
    )
    legacy_ids = sorted(source_bound_ids & set(YM_THEORY_MATCH_TERMS))
    if generated_ids and legacy_ids:
        raise YMCanonicalCycleError(
            "live YM theory vocabulary mixes generated and legacy incumbent IDs"
        )
    theory_objects = [
        {
            "theory_object_id": "YM21-TARGET-SCOPE",
            "object_kind": "concept",
            "label": "Four-dimensional pure Yang--Mills target scope",
            "match_terms": ["yang mills", "pure gauge"],
            "scope_anchor": True,
        }
    ]
    if generated_ids:
        theory_objects.extend(
            {
                "theory_object_id": theory_object_id,
                "object_kind": "hypothesis",
                "label": (
                    "Proposal-field-free generated YM candidate "
                    + theory_object_id.split(".", 1)[-1][:12]
                ),
                "match_terms": [theory_object_id.replace(".", " ")],
                "scope_anchor": False,
            }
            for theory_object_id in generated_ids
        )
    else:
        titles = {str(seed["id"]): str(seed["title"]) for seed in RIVAL_SEEDS}
        theory_objects.extend(
            {
                "theory_object_id": theory_object_id,
                "object_kind": "hypothesis",
                "label": titles[theory_object_id],
                "match_terms": list(match_terms),
                "scope_anchor": False,
            }
            for theory_object_id, match_terms in sorted(YM_THEORY_MATCH_TERMS.items())
        )
    return build_theory_object_catalog(
        target_id=TARGET_ID,
        theory_state_digest=str(snapshot["theory_state_digest"]),
        theory_objects=theory_objects,
    )


def _derived_hypothesis_rebase(
    mapping_derivation: Mapping[str, Any],
) -> list[dict[str, Any]]:
    """Derive every rebase row from the claim-mapping receipt, never a source-ID table."""

    mapped_ids = {
        str(theory_object_id)
        for mapping in mapping_derivation.get("theory_mappings", [])
        for theory_object_id in mapping.get("theory_object_ids", [])
    }
    generated_ids = sorted(
        theory_object_id
        for theory_object_id in mapped_ids
        if theory_object_id.startswith("hypothesis.")
    )
    if generated_ids and mapped_ids & set(YM_THEORY_MATCH_TERMS):
        raise YMCanonicalCycleError(
            "generated hypothesis rebase contains legacy incumbent IDs"
        )
    hypotheses = (
        [
            {
                "hypothesis_id": hypothesis_id,
                "genealogy": [
                    hypothesis_id,
                    "ym21-proposal-field-free-generated-candidate",
                ],
            }
            for hypothesis_id in generated_ids
        ]
        if generated_ids
        else [
            {
                "hypothesis_id": str(seed["id"]),
                "genealogy": [
                    str(seed["id"]),
                    "ym21-pre-targeted-repair-intuition",
                ],
            }
            for seed in RIVAL_SEEDS
        ]
    )
    return derive_hypothesis_rebase(
        mapping_derivation,
        hypotheses,
    )


_SNAPSHOT_EVIDENCE_ONLY_PORTFOLIO_PATHS = (
    "portfolio_id",
    "literature_snapshot_id",
    "literature_snapshot_digest",
    "content_digest",
    "generation_provenance.proposal_request_digest",
    "hypotheses[*].literature_rebase_receipt.receipt_id",
    "hypotheses[*].literature_rebase_receipt.snapshot_id",
    "hypotheses[*].literature_rebase_receipt.snapshot_digest",
)


def _authoritative_portfolio_projection(
    portfolio: Mapping[str, Any],
) -> dict[str, Any]:
    """Remove only the enumerated request/snapshot evidence from a portfolio.

    Everything else is theory-authoritative for the rebinding check, including
    every candidate field, genealogy entry, correction, ontology delta,
    premortem, portfolio policy, and parallel branch seed.  New fields therefore
    fail closed unless they are explicitly reviewed as evidence-only here.
    """

    projection = copy.deepcopy(dict(portfolio))
    try:
        for field in (
            "portfolio_id",
            "literature_snapshot_id",
            "literature_snapshot_digest",
            "content_digest",
        ):
            projection.pop(field)
        projection["generation_provenance"].pop("proposal_request_digest")
        for hypothesis in projection["hypotheses"]:
            receipt = hypothesis["literature_rebase_receipt"]
            for field in ("receipt_id", "snapshot_id", "snapshot_digest"):
                receipt.pop(field)
    except (KeyError, TypeError) as exc:
        raise YMCanonicalCycleError(
            "generated portfolio lacks an enumerated evidence-binding field"
        ) from exc
    return projection


def _evidence_only_portfolio_values(
    portfolio: Mapping[str, Any],
) -> dict[str, Any]:
    """Expose every deliberately excluded field so rebinding remains auditable."""

    try:
        values: dict[str, Any] = {
            field: copy.deepcopy(portfolio[field])
            for field in (
                "portfolio_id",
                "literature_snapshot_id",
                "literature_snapshot_digest",
                "content_digest",
            )
        }
        values["generation_provenance.proposal_request_digest"] = copy.deepcopy(
            portfolio["generation_provenance"]["proposal_request_digest"]
        )
        for hypothesis in portfolio["hypotheses"]:
            hypothesis_id = str(hypothesis["hypothesis_id"])
            receipt = hypothesis["literature_rebase_receipt"]
            for field in ("receipt_id", "snapshot_id", "snapshot_digest"):
                values[
                    f"hypotheses[{hypothesis_id}].literature_rebase_receipt.{field}"
                ] = copy.deepcopy(receipt[field])
    except (KeyError, TypeError) as exc:
        raise YMCanonicalCycleError(
            "generated portfolio lacks an enumerated evidence-binding field"
        ) from exc
    return values


def _semantic_exploration_selection(study: Mapping[str, Any]) -> dict[str, Any]:
    """Project ranking onto global content and slot identities, not evidence IDs."""

    repetitions = {
        int(row["repetition_index"]): row for row in study["repetitions"]
    }
    routing = study["exploration_selection"]
    ranking: list[dict[str, Any]] = []
    for ranked in routing["ranking"]:
        index = int(ranked["repetition_index"])
        repetition = repetitions.get(index)
        if repetition is None:
            raise YMCanonicalCycleError("exploration ranking names a missing repetition")
        if (
            ranked["repetition_digest"] != repetition["content_digest"]
            or ranked["portfolio_digest"]
            != repetition["portfolio"]["content_digest"]
            or ranked["semantic_content_id"]
            != repetition["semantic_content_id"]
        ):
            raise YMCanonicalCycleError(
                "exploration ranking does not bind its exact repetition and portfolio"
            )
        ranking.append(
            {
                "repetition_index": index,
                "schedule_slot_id": repetition["schedule_slot_id"],
                "semantic_content_id": repetition["semantic_content_id"],
                "semantic_output_id": repetition["semantic_output_id"],
                "authoritative_portfolio_digest": canonical_digest(
                    _authoritative_portfolio_projection(repetition["portfolio"])
                ),
                "routing_score": ranked["routing_score"],
            }
        )
    selected_index = routing["selected_repetition_index"]
    selected = repetitions.get(int(selected_index)) if selected_index is not None else None
    if selected is not None and (
        routing["selected_repetition_digest"] != selected["content_digest"]
        or routing["selected_portfolio_digest"]
        != selected["portfolio"]["content_digest"]
        or routing["selected_semantic_content_id"]
        != selected["semantic_content_id"]
    ):
        raise YMCanonicalCycleError(
            "exploration selection does not bind its exact repetition and portfolio"
        )
    return {
        key: copy.deepcopy(value)
        for key, value in routing.items()
        if key
        not in {
            "ranking",
            "selected_repetition_digest",
            "selected_portfolio_digest",
        }
    } | {
        "ranking": ranking,
        "selected_schedule_slot_id": (
            selected["schedule_slot_id"] if selected is not None else None
        ),
        "selected_semantic_content_id": (
            selected["semantic_content_id"] if selected is not None else None
        ),
        "selected_semantic_output_id": (
            selected["semantic_output_id"] if selected is not None else None
        ),
    }


def _semantic_repetition_schedule(study: Mapping[str, Any]) -> dict[str, Any]:
    """Project every snapshot-independent prompt, output, and scoring semantic.

    Exact request digests are intentionally absent because they rebind to the
    final literature snapshot.  Generator/adjudicator authorities, complete
    proposal content, blind ratings, ranking order, and selection policy remain
    present and therefore fail closed on any non-evidence drift.
    """

    repetitions = []
    for repetition in study["repetitions"]:
        if repetition["semantic_repetition_id"] != repetition["semantic_output_id"]:
            raise YMCanonicalCycleError(
                "semantic repetition compatibility alias drifted"
            )
        if repetition["repetition_id"] != repetition["evidence_repetition_id"]:
            raise YMCanonicalCycleError("legacy repetition_id evidence alias drifted")
        repetitions.append(
            {
                "repetition_index": repetition["repetition_index"],
                "schedule_slot_id": repetition["schedule_slot_id"],
                "semantic_content_id": repetition["semantic_content_id"],
                "semantic_output_id": repetition["semantic_output_id"],
                "semantic_repetition_id": repetition["semantic_repetition_id"],
                "prompt_seal": {
                    field: copy.deepcopy(repetition["prompt_seal"][field])
                    for field in (
                        "prompt_id",
                        "semantic_prompt_id",
                        "hidden_prompt_digest",
                        "known_authored_seed_audit",
                    )
                },
                "provider_receipt": {
                    key: copy.deepcopy(value)
                    for key, value in repetition["provider_receipt"].items()
                    if key != "request_digest"
                },
                "provider_output": copy.deepcopy(repetition["provider_output"]),
                "authored_template_copy_control": copy.deepcopy(
                    repetition["authored_template_copy_control"]
                ),
                "blind_adjudication": {
                    key: copy.deepcopy(value)
                    for key, value in repetition["blind_adjudication"].items()
                    if key != "request_digest"
                },
                "authoritative_portfolio": _authoritative_portfolio_projection(
                    repetition["portfolio"]
                ),
            }
        )
    return {
        "study_schema_version": study["schema_version"],
        "generation_mode": study["generation_mode"],
        "generator_authority": copy.deepcopy(study["generator_authority"]),
        "adjudicator_authority": copy.deepcopy(study["adjudicator_authority"]),
        "authority_separation": study["authority_separation"],
        "protocol": copy.deepcopy(study["protocol"]),
        "hidden_prompt_seals": [
            {
                field: copy.deepcopy(prompt[field])
                for field in (
                    "prompt_id",
                    "semantic_prompt_id",
                    "target_id",
                    "theory_state_digest",
                    "hidden_prompt_digest",
                    "known_authored_seed_audit",
                )
            }
            for prompt in study["hidden_prompt_seals"]
        ],
        "repetitions": repetitions,
        "exploration_selection": _semantic_exploration_selection(study),
    }


def _mapping_key_projection(portfolio: Mapping[str, Any]) -> list[dict[str, str]]:
    """Bind downstream routing keys to generated IDs, never legacy YM aliases."""

    by_corner = _generated_candidate_index(portfolio)
    return [
        {
            "corner_family": corner,
            "hypothesis_id": str(by_corner[corner]["hypothesis_id"]),
            "mechanism_key": str(by_corner[corner]["mechanism_key"]),
        }
        for corner in sorted(by_corner)
    ]


def _genealogy_projection(portfolio: Mapping[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "hypothesis_id": str(row["hypothesis_id"]),
            "genealogy": copy.deepcopy(row["genealogy"]),
        }
        for row in portfolio["hypotheses"]
    ]


def _verified_upstream_artifact(
    envelope: Mapping[str, Any],
    workspace: Path,
    role: str,
    expected_namespace: Namespace,
) -> dict[str, Any]:
    """Verify one descriptor against the cycle-owned namespace before load."""

    try:
        descriptor = envelope["proposal_field_free_upstream"][f"{role}_artifact"]
        expected_target = str(envelope["selected_portfolio"]["target_id"])
        if expected_namespace.target_id != expected_target:
            raise ContractError(
                f"{role} expected namespace target differs from selected portfolio"
            )
        path = verify_artifact_descriptor(
            descriptor,
            workspace,
            expected_namespace,
        )
        artifact = load_json(path)
        if not isinstance(artifact, Mapping):
            raise ContractError(f"{role} artifact must contain a JSON object")
        if artifact.get("content_digest") != canonical_digest(
            {
                key: value
                for key, value in artifact.items()
                if key != "content_digest"
            }
        ):
            raise ContractError(f"{role} artifact content digest mismatch")
    except (ContractError, KeyError, TypeError, ValueError) as exc:
        raise YMCanonicalCycleError(
            f"{role} artifact descriptor verification failed: {exc}"
        ) from exc
    return copy.deepcopy(dict(artifact))


def _selection_artifact(
    envelope: Mapping[str, Any],
    workspace: Path,
    expected_namespace: Namespace,
) -> dict[str, Any]:
    selection = _verified_upstream_artifact(
        envelope,
        workspace,
        "selection",
        expected_namespace,
    )
    if selection.get("study_artifact") != envelope["proposal_field_free_upstream"][
        "study_artifact"
    ]:
        raise YMCanonicalCycleError(
            "selection artifact does not bind the verified study descriptor"
        )
    return selection


def _study_artifact(
    envelope: Mapping[str, Any],
    workspace: Path,
    expected_namespace: Namespace,
) -> dict[str, Any]:
    study = _verified_upstream_artifact(
        envelope,
        workspace,
        "study",
        expected_namespace,
    )
    try:
        validate_payload(study, "seed_free_high_risk_elicitation.schema.json")
    except ContractError as exc:
        raise YMCanonicalCycleError(
            f"study artifact schema verification failed: {exc}"
        ) from exc
    return study


def _stable_selection_projection(
    selection: Mapping[str, Any], study: Mapping[str, Any]
) -> dict[str, Any]:
    """Validate selection causality and retain every snapshot-independent field."""

    if selection.get("schema_version") != "3.0":
        raise YMCanonicalCycleError("selection artifact is not the v3 identity contract")
    selected_index = int(selection["selected_repetition_index"])
    try:
        selected = study["repetitions"][selected_index]
    except (IndexError, KeyError, TypeError) as exc:
        raise YMCanonicalCycleError("selection names a missing repetition") from exc
    expected_controls = {
        "repeated_diversity_status": study["repeated_diversity"]["status"],
        "known_authored_copy_controls_passed": all(
            row["authored_template_copy_control"]["status"] == "passed"
            for row in study["repetitions"]
        ),
        "selection_status": study["exploration_selection"]["status"],
        "selection_policy_digest": study["exploration_selection"][
            "selection_policy_digest"
        ],
    }
    if selection["protocol_controls"] != expected_controls:
        raise YMCanonicalCycleError("selection protocol controls or policy drifted")
    if selection["exploration_selection"] != study["exploration_selection"]:
        raise YMCanonicalCycleError("selection ranking or policy differs from study")
    if (
        selection["study_id"] != study["study_id"]
        or selection["study_content_digest"] != study["content_digest"]
        or selection["selected_repetition_digest"] != selected["content_digest"]
        or selection["selected_portfolio_digest"]
        != selected["portfolio"]["content_digest"]
        or selection["selected_provider_output_digest"]
        != selected["provider_output"]["proposal_digest"]
        or selection["selected_raw_response_digest"]
        != selected["provider_output"]["raw_response_digest"]
        or selection["selected_proposals_digest"]
        != canonical_digest(selected["provider_output"]["proposals"])
        or selection["selected_generation_provenance"]
        != selected["portfolio"]["generation_provenance"]
    ):
        raise YMCanonicalCycleError(
            "selection does not bind the exact study repetition and provider output"
        )
    if (
        selection["selected_schedule_slot_id"] != selected["schedule_slot_id"]
        or selection["selected_semantic_content_id"]
        != selected["semantic_content_id"]
        or selection["selected_semantic_output_id"]
        != selected["semantic_output_id"]
        or selection["selected_semantic_repetition_id"]
        != selected["semantic_output_id"]
        or selection["selected_evidence_repetition_id"]
        != selected["evidence_repetition_id"]
        or selection["selected_repetition_id"]
        != selected["evidence_repetition_id"]
    ):
        raise YMCanonicalCycleError(
            "selection does not bind semantic-content, schedule-slot, semantic-output, and exact-evidence identities"
        )
    replay_inputs = selection["replay_inputs"]
    stable_prompts = [
        {
            key: copy.deepcopy(value)
            for key, value in prompt.items()
            if key not in {"literature_snapshot_digest", "content_digest"}
        }
        for prompt in replay_inputs["hidden_prompts"]
    ]
    stable_provenance = {
        key: copy.deepcopy(value)
        for key, value in selection["selected_generation_provenance"].items()
        if key != "proposal_request_digest"
    }
    return {
        "schema_version": selection["schema_version"],
        "study_status": selection["study_status"],
        "protocol_controls": copy.deepcopy(selection["protocol_controls"]),
        "exploration_selection": _semantic_exploration_selection(study),
        "selected_repetition_index": selected_index,
        "selected_schedule_slot_id": selection["selected_schedule_slot_id"],
        "selected_semantic_content_id": selection[
            "selected_semantic_content_id"
        ],
        "selected_semantic_output_id": selection["selected_semantic_output_id"],
        "selected_semantic_repetition_id": selection[
            "selected_semantic_repetition_id"
        ],
        "selected_provider_output_digest": selection[
            "selected_provider_output_digest"
        ],
        "selected_raw_response_digest": selection["selected_raw_response_digest"],
        "selected_proposals_digest": selection["selected_proposals_digest"],
        "selected_generation_provenance": stable_provenance,
        "eligibility": copy.deepcopy(selection["eligibility"]),
        "replay_inputs": {
            "hidden_prompts": stable_prompts,
            "counterbalance_seed": replay_inputs["counterbalance_seed"],
            "authored_incumbent_comparison_proposals_digest": canonical_digest(
                replay_inputs["authored_incumbent_comparison_proposals"]
            ),
        },
        "authority": selection["authority"],
        "claim_boundary": selection["claim_boundary"],
    }


def _assert_stable_generated_selection(
    preflight_envelope: Mapping[str, Any],
    final_envelope: Mapping[str, Any],
    *,
    preflight_workspace: Path,
    final_workspace: Path,
    expected_namespace: Namespace,
) -> dict[str, Any]:
    """Prove exact deck/slot identity while exact evidence identity rebinds."""

    preflight_portfolio = preflight_envelope["selected_portfolio"]
    final_portfolio = final_envelope["selected_portfolio"]
    preflight_study = _study_artifact(
        preflight_envelope,
        preflight_workspace,
        expected_namespace,
    )
    final_study = _study_artifact(
        final_envelope,
        final_workspace,
        expected_namespace,
    )
    preflight_selection = _selection_artifact(
        preflight_envelope,
        preflight_workspace,
        expected_namespace,
    )
    final_selection = _selection_artifact(
        final_envelope,
        final_workspace,
        expected_namespace,
    )
    for label, envelope, study, selection in (
        ("preflight", preflight_envelope, preflight_study, preflight_selection),
        ("final", final_envelope, final_study, final_selection),
    ):
        descriptors = envelope["proposal_field_free_upstream"]
        if descriptors["study_artifact"]["namespace"] != descriptors[
            "selection_artifact"
        ]["namespace"]:
            raise YMCanonicalCycleError(
                f"{label} study/selection descriptor namespaces differ"
            )
        replay_inputs = selection["replay_inputs"]
        try:
            validate_proposal_field_free_high_risk_elicitation(
                study,
                charter=envelope["charter"],
                literature_snapshot=envelope["literature_snapshot"],
                hidden_prompts=replay_inputs["hidden_prompts"],
                counterbalance_seed=str(replay_inputs["counterbalance_seed"]),
                authored_incumbent_comparison_proposals=replay_inputs[
                    "authored_incumbent_comparison_proposals"
                ],
            )
        except ContractError as exc:
            raise YMCanonicalCycleError(
                f"{label} study failed exact generator/adjudicator replay: {exc}"
            ) from exc
    preflight_snapshot_digest = preflight_envelope["literature_snapshot"][
        "content_digest"
    ]
    final_snapshot_digest = final_envelope["literature_snapshot"]["content_digest"]
    if preflight_snapshot_digest == final_snapshot_digest:
        raise YMCanonicalCycleError(
            "two-phase generated-ID binding did not produce a distinct final snapshot"
        )

    preflight_schedule = _semantic_repetition_schedule(preflight_study)
    final_schedule = _semantic_repetition_schedule(final_study)
    if preflight_schedule != final_schedule:
        raise YMCanonicalCycleError(
            "precommitted semantic prompt/repetition schedule changed after evidence rebinding"
        )
    schedule_slot_ids = [
        str(row["schedule_slot_id"])
        for row in final_schedule["repetitions"]
    ]
    semantic_output_ids = [
        str(row["semantic_output_id"])
        for row in final_schedule["repetitions"]
    ]
    if len(set(schedule_slot_ids)) != len(schedule_slot_ids):
        raise YMCanonicalCycleError("schedule-slot identity collision")
    if len(set(semantic_output_ids)) != len(semantic_output_ids):
        raise YMCanonicalCycleError("semantic-output identity collision")

    preflight_selection_projection = _stable_selection_projection(
        preflight_selection, preflight_study
    )
    final_selection_projection = _stable_selection_projection(
        final_selection, final_study
    )
    if preflight_selection_projection != final_selection_projection:
        raise YMCanonicalCycleError(
            "adjudication ranking or selection-policy semantics changed after evidence rebinding"
        )

    preflight_evidence_ids = [
        str(row["evidence_repetition_id"])
        for row in preflight_study["repetitions"]
    ]
    final_evidence_ids = [
        str(row["evidence_repetition_id"])
        for row in final_study["repetitions"]
    ]
    if len(set([*preflight_evidence_ids, *final_evidence_ids])) != (
        len(preflight_evidence_ids) + len(final_evidence_ids)
    ):
        raise YMCanonicalCycleError(
            "evidence repetition identities did not rebind uniquely"
        )
    for label, selection, study in (
        ("preflight", preflight_selection, preflight_study),
        ("final", final_selection, final_study),
    ):
        selected_index = int(selection["selected_repetition_index"])
        selected_repetition = study["repetitions"][selected_index]
        if (
            selection["selected_repetition_id"]
            != selection["selected_evidence_repetition_id"]
            or selection["selected_schedule_slot_id"]
            != selected_repetition["schedule_slot_id"]
            or selection["selected_semantic_content_id"]
            != selected_repetition["semantic_content_id"]
            or selection["selected_semantic_output_id"]
            != selected_repetition["semantic_output_id"]
            or selection["selected_semantic_repetition_id"]
            != selected_repetition["semantic_output_id"]
            or selection["selected_evidence_repetition_id"]
            != selected_repetition["evidence_repetition_id"]
        ):
            raise YMCanonicalCycleError(
                f"{label} selection does not bind its semantic/evidence repetition"
            )
    if (
        preflight_selection["selected_repetition_index"]
        != final_selection["selected_repetition_index"]
        or preflight_selection["selected_schedule_slot_id"]
        != final_selection["selected_schedule_slot_id"]
        or preflight_selection["selected_semantic_content_id"]
        != final_selection["selected_semantic_content_id"]
        or preflight_selection["selected_semantic_output_id"]
        != final_selection["selected_semantic_output_id"]
        or preflight_selection["selected_evidence_repetition_id"]
        == final_selection["selected_evidence_repetition_id"]
    ):
        raise YMCanonicalCycleError(
            "generated repetition selection did not preserve semantics and rebind evidence"
        )

    preflight_authoritative = _authoritative_portfolio_projection(
        preflight_portfolio
    )
    final_authoritative = _authoritative_portfolio_projection(final_portfolio)
    preflight_mapping_keys = _mapping_key_projection(preflight_portfolio)
    final_mapping_keys = _mapping_key_projection(final_portfolio)
    preflight_genealogy = _genealogy_projection(preflight_portfolio)
    final_genealogy = _genealogy_projection(final_portfolio)
    preflight_branches = copy.deepcopy(preflight_portfolio["parallel_branch_seeds"])
    final_branches = copy.deepcopy(final_portfolio["parallel_branch_seeds"])
    preflight_proposals = copy.deepcopy(preflight_envelope["selected_proposals"])
    final_proposals = copy.deepcopy(final_envelope["selected_proposals"])
    legacy_identifiers = _legacy_routing_identifiers(
        {
            "preflight_authoritative_portfolio": preflight_authoritative,
            "final_authoritative_portfolio": final_authoritative,
            "preflight_provider_candidates": preflight_proposals,
            "final_provider_candidates": final_proposals,
            "preflight_mapping_keys": preflight_mapping_keys,
            "final_mapping_keys": final_mapping_keys,
        }
    )
    if legacy_identifiers:
        raise YMCanonicalCycleError(
            "generated binding contains legacy YM routing identifiers: "
            f"{sorted(legacy_identifiers)}"
        )
    if preflight_mapping_keys != final_mapping_keys:
        raise YMCanonicalCycleError("generated hypothesis mapping keys changed")
    if preflight_proposals != final_proposals:
        raise YMCanonicalCycleError("selected provider candidate deck changed")
    if preflight_genealogy != final_genealogy:
        raise YMCanonicalCycleError("generated hypothesis genealogy changed")
    if preflight_branches != final_branches:
        raise YMCanonicalCycleError("generated parallel branch seeds changed")
    if preflight_authoritative != final_authoritative:
        raise YMCanonicalCycleError(
            "authoritative generated portfolio changed outside enumerated evidence fields"
        )

    preflight_evidence = _evidence_only_portfolio_values(preflight_portfolio)
    final_evidence = _evidence_only_portfolio_values(final_portfolio)
    if set(preflight_evidence) != set(final_evidence):
        raise YMCanonicalCycleError("evidence-only portfolio field set changed")
    unchanged_evidence = sorted(
        path
        for path in preflight_evidence
        if preflight_evidence[path] == final_evidence[path]
    )
    if unchanged_evidence:
        raise YMCanonicalCycleError(
            "snapshot/request evidence fields did not rebind: "
            f"{unchanged_evidence}"
        )

    receipt: dict[str, Any] = {
        "schema_version": "3.0",
        "validated_namespace": expected_namespace.as_dict(),
        "preflight_snapshot_digest": preflight_snapshot_digest,
        "final_snapshot_digest": final_snapshot_digest,
        "preflight_selection_digest": preflight_selection["content_digest"],
        "final_selection_digest": final_selection["content_digest"],
        "selected_repetition_index": final_selection["selected_repetition_index"],
        "selected_schedule_slot_id": final_selection["selected_schedule_slot_id"],
        "selected_semantic_content_id": final_selection[
            "selected_semantic_content_id"
        ],
        "selected_semantic_output_id": final_selection[
            "selected_semantic_output_id"
        ],
        "selected_semantic_repetition_id": final_selection[
            "selected_semantic_repetition_id"
        ],
        "preflight_selected_evidence_repetition_id": preflight_selection[
            "selected_evidence_repetition_id"
        ],
        "final_selected_evidence_repetition_id": final_selection[
            "selected_evidence_repetition_id"
        ],
        "selected_hypothesis_ids": [
            row["hypothesis_id"] for row in final_mapping_keys
        ],
        "semantic_repetition_schedule": final_schedule,
        "selection_semantic_projection": final_selection_projection,
        "selected_provider_candidate_projection": final_proposals,
        "authoritative_portfolio_projection": final_authoritative,
        "candidate_projection": copy.deepcopy(final_authoritative["hypotheses"]),
        "genealogy_projection": final_genealogy,
        "parallel_branch_seed_projection": final_branches,
        "mapping_key_projection": final_mapping_keys,
        "semantic_selection_signature": final_mapping_keys,
        "selected_proposals_digest": canonical_digest(final_proposals),
        "authoritative_portfolio_projection_digest": canonical_digest(
            final_authoritative
        ),
        "semantic_repetition_schedule_digest": canonical_digest(final_schedule),
        "selection_semantic_projection_digest": canonical_digest(
            final_selection_projection
        ),
        "mapping_key_projection_digest": canonical_digest(final_mapping_keys),
        "evidence_only_portfolio_paths": list(
            _SNAPSHOT_EVIDENCE_ONLY_PORTFOLIO_PATHS
        ),
        "preflight_evidence_binding": preflight_evidence,
        "final_evidence_binding": final_evidence,
        "semantic_identity_stable": True,
        "global_semantic_content_identity_stable": True,
        "evidence_identity_rebound": True,
        "stable_after_snapshot_rebinding": True,
        "stability_basis": (
            "Exact global proposal-content keys, precommitted schedule slots, slot-conditioned "
            "semantic outputs, prompts, generator and "
            "adjudicator authorities, blind ratings, ranking and selection policy, every "
            "portfolio after only enumerated evidence exclusions, genealogy, parallel "
            "branch seeds, and generated mapping key; exact request/snapshot evidence "
            "and evidence repetition identities must rebind."
        ),
        "authority_boundary": (
            "Stability is deterministic replay evidence only; it does not establish "
            "creativity, novelty, truth, or physics value."
        ),
    }
    receipt["content_digest"] = canonical_digest(receipt)
    return receipt


def _legacy_routing_identifiers(value: Any) -> set[str]:
    if isinstance(value, str):
        return {value} if re.fullmatch(r"YM21-R\d+", value) else set()
    if isinstance(value, Mapping):
        return {
            identifier
            for item in value.values()
            for identifier in _legacy_routing_identifiers(item)
        }
    if isinstance(value, Sequence) and not isinstance(value, (str, bytes, bytearray)):
        return {
            identifier
            for item in value
            for identifier in _legacy_routing_identifiers(item)
        }
    return set()


def _assert_generated_live_routing(
    *,
    portfolio: Mapping[str, Any],
    theory_catalog: Mapping[str, Any],
    mapping_derivation: Mapping[str, Any],
    hypothesis_rebase: Sequence[Mapping[str, Any]],
    assimilation: Mapping[str, Any],
    routing_trace: Mapping[str, Any] | None = None,
) -> None:
    """Prove every live literature surface is closed over selected generated IDs."""

    candidate_ids = {
        str(row["hypothesis_id"])
        for row in _generated_candidate_index(portfolio).values()
    }
    catalog_ids = {
        str(row["theory_object_id"])
        for row in theory_catalog["theory_objects"]
        if not row["scope_anchor"]
    }
    mapping_ids = {
        str(theory_object_id)
        for row in mapping_derivation["theory_mappings"]
        for theory_object_id in row["theory_object_ids"]
        if theory_object_id != "YM21-TARGET-SCOPE"
    }
    rebase_ids = {str(row["hypothesis_id"]) for row in hypothesis_rebase}
    assimilation_ids = {
        str(theory_object_id)
        for row in assimilation["theory_mappings"]
        for theory_object_id in row["theory_object_ids"]
        if theory_object_id != "YM21-TARGET-SCOPE"
    }
    observed = {
        "catalog": catalog_ids,
        "mapping": mapping_ids,
        "rebase": rebase_ids,
        "assimilation": assimilation_ids,
    }
    if any(identifiers != candidate_ids for identifiers in observed.values()):
        raise YMCanonicalCycleError(
            "live literature routing is not an exact generated-ID closure: "
            + "; ".join(
                f"{name}:missing={sorted(candidate_ids - identifiers)},"
                f"extra={sorted(identifiers - candidate_ids)}"
                for name, identifiers in observed.items()
                if identifiers != candidate_ids
            )
        )
    surfaces: list[Any] = [
        theory_catalog,
        mapping_derivation,
        list(hypothesis_rebase),
        assimilation,
    ]
    if routing_trace is not None:
        surfaces.append(routing_trace)
    legacy_ids = {
        identifier
        for surface in surfaces
        for identifier in _legacy_routing_identifiers(surface)
    }
    if legacy_ids:
        raise YMCanonicalCycleError(
            "legacy authored-incumbent IDs remain in live routing: "
            + ", ".join(sorted(legacy_ids))
        )


def _literature_counterfactual_worlds(
    snapshot: Mapping[str, Any],
) -> list[dict[str, Any]]:
    """Declare all five required replay operations, including an exact null."""

    source_ids = sorted(str(row["source_id"]) for row in snapshot["sources"])
    worlds = [
        {
            "world_id": f"delete-{source_id}",
            "operation": "delete_source",
            "source_id": source_id,
            "expected_effect": "change",
        }
        for source_id in source_ids
    ]
    worlds.extend(
        [
            {
                "world_id": "no-literature",
                "operation": "no_literature",
                "expected_effect": "change",
            },
            {
                "world_id": "direct-claim-superseded",
                "operation": "supersede_source",
                "source_id": DIRECT_CHALLENGER_ID,
                "source_version": "synthetic-superseded-counterfactual",
                "replacement_claim": (
                    "A superseding audit withdraws the continuum and spectral conclusions "
                    "and leaves an open comparison question."
                ),
                "expected_effect": "change",
            },
            {
                "world_id": "direct-claim-contradictory",
                "operation": "contradict_source",
                "source_id": DIRECT_CHALLENGER_ID,
                "contradictory_claim": (
                    "A target-preserving counterexample contradicts and rules out the "
                    "claimed continuum-to-spectral transfer."
                ),
                "expected_effect": "change",
            },
            {
                "world_id": "coverage-only-null",
                "operation": "coverage_only_change",
                "coverage_limit": (
                    "Synthetic provenance-only qualification with no source or claim change."
                ),
                "expected_effect": "null",
            },
        ]
    )
    return worlds


LATEST_SOURCE_PRIORITY: dict[str, list[str]] = {
    "YM21-R01": ["arxiv-1906.00999", DIRECT_CHALLENGER_ID],
    "YM21-R02": [DIRECT_CHALLENGER_ID, "zenodo-19614728", "nature-review-2026-douglas"],
    "YM21-R03": ["arxiv-1412.5148", "arxiv-1703.00501", "zenodo-19423313"],
    "YM21-R04": ["arxiv-2204.12737", "arxiv-2503.03060", DIRECT_CHALLENGER_ID],
    "YM21-R05": ["zenodo-19614728", "arxiv-2204.12737", DIRECT_CHALLENGER_ID],
    "YM21-R06": [DIRECT_CHALLENGER_ID, "recognition-washburn-2026"],
    "YM21-R07": ["arxiv-1412.5148", "zenodo-19423313", DIRECT_CHALLENGER_ID],
    "YM21-R08": [DIRECT_CHALLENGER_ID, "preprints-202604.0332-v1", "arxiv-2307.00788-v7"],
    "YM21-R09": ["arxiv-1906.00999", "arxiv-1410.0664", DIRECT_CHALLENGER_ID],
    "YM21-R10": ["clay-ym-current", DIRECT_CHALLENGER_ID, "zenodo-19614728", "nature-review-2026-douglas"],
}


def _quality_axes(seed: Mapping[str, Any]) -> dict[str, float]:
    unique_axis = {
        "YM21-R01": "conceptual_distance",
        "YM21-R02": "coherence",
        "YM21-R03": "unification_potential",
        "YM21-R04": "learning_if_false",
        "YM21-R05": "tractability",
        "YM21-R06": "value_if_true",
        "YM21-R07": "explanatory_upside",
        "YM21-R08": "generativity",
        "YM21-R09": "literature_distance",
    }.get(seed["id"])
    if seed.get("control"):
        return {
            "essential_relevance": 0.99,
            "conceptual_distance": 0.18,
            "explanatory_upside": 0.48,
            "unification_potential": 0.42,
            "generativity": 0.52,
            "coherence": 0.88,
            "literature_distance": 0.20,
            "tractability": 0.72,
            "learning_if_false": 0.66,
            "value_if_true": 0.75,
        }
    axes = {
        "essential_relevance": 0.95,
        "conceptual_distance": 0.86,
        "explanatory_upside": float(seed["v"]),
        "unification_potential": max(0.80, float(seed["v"]) - 0.04),
        "generativity": max(0.80, float(seed["l"])),
        "coherence": 0.78,
        "literature_distance": 0.58,
        "tractability": max(0.05, 1.0 - float(seed["c"])),
        "learning_if_false": float(seed["l"]),
        "value_if_true": float(seed["v"]),
    }
    if unique_axis:
        axes[unique_axis] = 0.99
    return axes


def _authored_domain_template_incumbent_comparison_proposals(
    snapshot: Mapping[str, Any],
) -> list[dict[str, Any]]:
    """Build the YM-authored equal-count incumbent deck, never the live generator.

    These target-specific RIVAL_SEEDS preserve the previous scientific content
    as a blinded incumbent comparison.  Generation opportunity and literature
    exposure are not matched.  The proposal-field-free condition is generated
    separately and is the only deck eligible for upstream selection.
    """

    available = {row["source_id"] for row in snapshot["sources"]}
    proposals: list[dict[str, Any]] = []
    for seed in RIVAL_SEEDS:
        source_ids = [source_id for source_id in LATEST_SOURCE_PRIORITY[seed["id"]] if source_id in available]
        mechanism_key = re.sub(r"[^a-z0-9]+", "-", str(seed["title"]).lower()).strip("-")
        proposals.append(
            {
                "hypothesis_id": seed["id"],
                "corner_family": seed["corner"],
                "intuition_provenance": {
                    "mode": "blind_intuition_first",
                    "trigger": "Operational divergence pass over the frozen YM root tensions, before this invocation assigns source relations.",
                    "pre_literature_statement": (
                        f"Operationally blind within this generator invocation, not a historical pre-search claim: {seed['intuition']}"
                    ),
                },
                "intuitive_leap": seed["intuition"],
                "mechanism": seed["mechanism"],
                "mechanism_key": mechanism_key,
                "ontology_delta": {
                    "new_primitives": list(seed["new"]),
                    "new_relations": [f"ym21_relation_{seed['id'].lower().replace('-', '_')}"],
                    "removed_or_retyped": (
                        ["retained_boundary_kernel_as_parent", "defect_count_as_primary_explanation"]
                        if not seed.get("control")
                        else []
                    ),
                    "affordance": seed["value"],
                },
                "target_pressures_addressed": [
                    "Construct the nontrivial four-dimensional continuum theory without assuming the desired spectral gap.",
                    "Explain how a positive physical scale survives regulator removal and OS/Hamiltonian interpretation."
                ],
                "target_commitments": [
                    "pure four-dimensional Yang-Mills for a compact simple gauge group",
                    "nontrivial continuum identity and gauge-invariant observable meaning",
                    "positive Hamiltonian spectral gap above the vacuum"
                ],
                "protected_successes": [
                    "finite lattice gauge invariance and reflection-positive comparators",
                    "rigorous lower-dimensional and strong-coupling boundary results"
                ],
                "assumptions_or_invariants_risked": [
                    "No finite-volume, strong-coupling, Higgs, or stochastic proxy may replace the exact Clay target.",
                    seed["corrections"][0],
                ],
                "explanatory_upside": seed["value"],
                "unification_upside": (
                    "If coherent, connect construction, continuum identity, and spectral interpretation while preserving their separate proof burdens."
                ),
                "value_if_right": seed["value"],
                "learning_value_if_wrong": seed["learning"],
                "risk_axes": {
                    "probability_of_truth": float(seed["p"]),
                    "failure_risk": 1.0 - float(seed["p"]),
                    "maturation_cost": float(seed["c"]),
                },
                "quality_axes": _quality_axes(seed),
                "maturation_question": seed["question"],
                "correction_conditions": list(seed["corrections"]),
                "boundary_case": seed["corrections"][0],
                "premortem": {
                    "failure_signatures": list(seed["corrections"]),
                    "earliest_decisive_theory_test": seed["question"],
                    "disposition": "artifact_sprint" if seed.get("wildcard") else "falsifier_sprint" if seed.get("control") else "invest",
                },
                "branch_independence_signature": {
                    "unique_primitives": list(seed["new"]),
                    "unique_mechanism": seed["mechanism"],
                    "forbidden_cross_branch_context": [
                        "Sibling branch conclusions before independent maturation",
                        "Mutable global latest aliases or unbound literature claims"
                    ],
                    "required_context": [
                        "Frozen exact YM target charter",
                        "Frozen live snapshot digest",
                        "Claim-specific source limitations"
                    ],
                    "overlaps_with_hypothesis_ids": [],
                },
                "genealogy": [seed["id"], "ym21-pre-targeted-repair-intuition"],
                "literature_relation": (
                    "partly_anticipated" if any(source_id in {DIRECT_CHALLENGER_ID, "zenodo-19614728"} for source_id in source_ids)
                    else "cross_field_bridge"
                ),
                "literature_source_ids": source_ids,
                "is_wildcard": bool(seed.get("wildcard")),
                "is_control": bool(seed.get("control")),
            }
        )
    return proposals


def _charter(snapshot: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "target_id": TARGET_ID,
        "target_statement": (
            "Construct a nontrivial quantum Yang-Mills theory on R4 for every compact simple gauge group "
            "and prove a positive mass gap above the vacuum without changing the target's quantifiers or identity."
        ),
        "theory_state_digest": snapshot["theory_state_digest"],
        "root_tensions": [
            "Finite lattice coercivity or clustering does not by itself identify a nontrivial continuum theory with uniform physical scale.",
            "Euclidean reflection positivity and decay do not automatically yield a complete physical observable core and Hamiltonian gap.",
            "Regulator universality, weak/strong coupling identity, and nontriviality are distinct burdens often compressed into one bridge.",
            "Incumbent retained-kernel language may articulate estimates while failing to expose the correct explanatory primitive."
        ],
        "target_commitments": [
            "Preserve pure four-dimensional Yang-Mills, compact simple gauge group scope, and continuum nontriviality.",
            "Preserve an actual positive Hamiltonian spectral gap, not a finite-volume or stochastic proxy.",
            "Keep construction, OS reconstruction, universality, and spectral inference as separately auditable obligations."
        ],
        "protected_successes": [
            "Retain rigorous finite-lattice, lower-dimensional, and strong-coupling results only inside their proven regimes.",
            "Retain gauge invariance, reflection positivity, and exact observable semantics whenever a route genuinely supplies them."
        ],
        "forbidden_target_drift": (
            "No Higgs, abelian, lower-dimensional, finite-volume, strong-coupling-only, stochastic-generator, "
            "or definitionally gap-assuming substitute may stand in for the exact target."
        ),
        "target_supports_six_corners": True,
        "wildcards_available": True,
    }


def _structural_identity(
    system_id: str,
    *,
    primitives: list[str],
    relations: list[str],
    mechanism: str,
    question: str,
    genealogy: list[str],
) -> dict[str, Any]:
    """Build stable typed identity for one supplied YM conceptual system."""

    return {
        "primitive_ids": [
            stable_identifier("ym21-primitive", system_id, item) for item in primitives
        ],
        "relation_ids": [
            stable_identifier("ym21-relation", system_id, item) for item in relations
        ],
        "mechanism_id": stable_identifier("ym21-mechanism", system_id, mechanism),
        "maturation_question_id": stable_identifier("ym21-question", system_id, question),
        "genealogy_ids": list(genealogy),
    }


def _literature_routed_seeds(
    portfolio: Mapping[str, Any],
    assimilation: Mapping[str, Any],
    *,
    count: int = 4,
    allow_empty_mappings: bool = False,
    include_source_removals: bool = True,
    routing_authority: Mapping[str, Any] | None = None,
    routing_sources: Sequence[Mapping[str, Any]] = (),
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    """Rank branch seeds from exact source impacts and audit source removal.

    Three high-impact routes and the strongest remaining wildcard are retained.
    No hypothesis ID appears in the selection rule.  Leave-one-source-out
    reranking records whether recent literature changes either membership or
    ordering, making literature causality testable rather than narrative.
    """

    seeds = [dict(row) for row in portfolio.get("parallel_branch_seeds", [])]
    mappings = [dict(row) for row in assimilation.get("theory_mappings", [])]
    if len(seeds) < count or (not mappings and not allow_empty_mappings):
        raise YMCanonicalCycleError("literature routing requires a plural portfolio and exact theory mappings")
    routing_certificate = None
    if routing_authority is not None:
        routing_certificate = validate_source_routing_consumption(
            authority=routing_authority,
            sources=routing_sources,
            stage="parallel_scheduling",
            theory_mappings=mappings,
            require_complete_mapping=True,
        )
    event_weight = {
        "demote": 9,
        "split": 8,
        "new_question": 7,
        "reframe": 6,
        "reprioritize": 5,
    }
    confidence_weight = {"high": 3, "medium": 2, "low": 1, "unknown": 0}

    def rank(excluded_source: str | None = None) -> list[dict[str, Any]]:
        rows = []
        for seed in seeds:
            hypothesis_id = str(seed["hypothesis_id"])
            impacts = [
                row
                for row in mappings
                if row.get("source_id") != excluded_source
                and hypothesis_id in row.get("theory_object_ids", [])
            ]
            source_ids = sorted({str(row["source_id"]) for row in impacts})
            score = sum(
                event_weight.get(str(row.get("event_type")), 1)
                + confidence_weight.get(str(row.get("confidence")), 0)
                for row in impacts
            ) + 2 * len(source_ids) + len({str(row.get("event_type")) for row in impacts})
            rows.append(
                {
                    "hypothesis_id": hypothesis_id,
                    "branch_id": seed["branch_id"],
                    "corner_family": seed["corner_family"],
                    "is_wildcard": bool(seed.get("is_wildcard")),
                    "impact_score": score,
                    "source_ids": source_ids,
                    "mapping_ids": sorted(str(row["mapping_id"]) for row in impacts),
                }
            )
        return sorted(rows, key=lambda row: (-row["impact_score"], row["hypothesis_id"]))

    def select(ranked: list[dict[str, Any]]) -> list[str]:
        primary = [row for row in ranked if not row["is_wildcard"]][: count - 1]
        used = {row["hypothesis_id"] for row in primary}
        wildcard = next(
            (row for row in ranked if row["is_wildcard"] and row["hypothesis_id"] not in used),
            None,
        )
        if wildcard is not None:
            primary.append(wildcard)
        for row in ranked:
            if len(primary) >= count:
                break
            if row["hypothesis_id"] not in {item["hypothesis_id"] for item in primary}:
                primary.append(row)
        return [row["hypothesis_id"] for row in primary]

    baseline_rank = rank()
    selected_ids = select(baseline_rank)
    by_id = {str(row["hypothesis_id"]): row for row in seeds}
    if any(item not in by_id for item in selected_ids):
        raise YMCanonicalCycleError("literature routing selected a missing portfolio seed")
    counterfactuals = []
    for source_id in (
        sorted({str(row["source_id"]) for row in mappings})
        if include_source_removals
        else []
    ):
        reranked = rank(source_id)
        counterfactual_ids = select(reranked)
        counterfactuals.append(
            {
                "removed_source_id": source_id,
                "selected_hypothesis_ids": counterfactual_ids,
                "route_changed": counterfactual_ids != selected_ids,
                "baseline_rank": [row["hypothesis_id"] for row in baseline_rank],
                "counterfactual_rank": [row["hypothesis_id"] for row in reranked],
            }
        )
    trace = {
        "schema_version": "1.0.0",
        "routing_id": stable_identifier(
            "ym21-literature-routing",
            assimilation.get("packet_id"),
            portfolio.get("portfolio_id"),
            selected_ids,
        ),
        "assimilation_digest": canonical_digest(assimilation),
        "portfolio_digest": canonical_digest(portfolio),
        "selection_policy": "top_three_nonwildcard_source_impacts_plus_strongest_remaining_wildcard",
        "ranked_impacts": baseline_rank,
        "selected_hypothesis_ids": selected_ids,
        "source_removal_counterfactuals": counterfactuals,
        "source_removal_changes_route": any(row["route_changed"] for row in counterfactuals),
        "source_routing_certificate": routing_certificate,
        "authority_boundary": (
            "Routing demonstrates a causal scheduling effect of recorded literature mappings only; it does not validate a source claim or certify novelty."
        ),
    }
    trace["content_digest"] = canonical_digest(trace)
    return [by_id[item] for item in selected_ids], trace


def _counterfactual_snapshot(
    snapshot: Mapping[str, Any],
    *,
    scenario_id: str,
    excluded_source_ids: set[str],
    source_overrides: Mapping[str, Mapping[str, Any]] | None = None,
) -> dict[str, Any]:
    """Re-execute all six lanes over one explicitly synthetic source scenario."""

    source_overrides = dict(source_overrides or {})
    sources = {str(row["source_id"]): copy.deepcopy(dict(row)) for row in snapshot["sources"]}
    lane_type_by_id = {str(row["lane_id"]): str(row["lane_type"]) for row in snapshot["lane_receipts"]}
    sources_by_lane: dict[str, list[dict[str, Any]]] = {lane_type: [] for lane_type in LANE_TYPES}
    for source_id, source in sources.items():
        if source_id in excluded_source_ids:
            continue
        source.update(copy.deepcopy(dict(source_overrides.get(source_id, {}))))
        source.pop("content_digest", None)
        lane_ids = list(source.pop("lane_ids", []))
        for lane_id in lane_ids:
            lane_type = lane_type_by_id[str(lane_id)]
            sources_by_lane[lane_type].append(copy.deepcopy(source))

    providers: dict[str, Any] = {}
    for lane_type in LANE_TYPES:
        def provider(
            request: Mapping[str, Any],
            *,
            lane_type: str = lane_type,
        ) -> dict[str, Any]:
            return {
                "provider": f"synthetic-literature-counterfactual/{scenario_id}/{lane_type}",
                "index": "frozen baseline source set transformed by a declared counterfactual",
                "execution_mode": "local_only",
                "status": "completed",
                "coverage_cutoff": snapshot["coverage_cutoff"],
                "sources": copy.deepcopy(sources_by_lane[lane_type]),
            }

        providers[lane_type] = provider
    lanes = []
    receipt_by_type = {str(row["lane_type"]): row for row in snapshot["lane_receipts"]}
    for lane_type in LANE_TYPES:
        baseline = receipt_by_type[lane_type]
        lanes.append(
            {
                "lane_id": stable_identifier("ym21-counterfactual-lane", scenario_id, lane_type),
                "lane_type": lane_type,
                "queries": list(baseline["queries"]),
                "inclusion_policy": snapshot["inclusion_policy"],
                "exclusion_policy": snapshot["exclusion_policy"],
            }
        )
    return run_frontier_literature_cycle(
        {
            "target_id": snapshot["target_id"],
            "claim_scope": f"Synthetic causal replay only: {scenario_id}",
            "theory_state_digest": snapshot["theory_state_digest"],
            "coverage_cutoff": snapshot["coverage_cutoff"],
            "inclusion_policy": snapshot["inclusion_policy"],
            "exclusion_policy": snapshot["exclusion_policy"],
            "coverage_limits": [
                f"Scenario {scenario_id} is a synthetic counterfactual over the frozen capture, not new literature evidence.",
                "It tests whether the recorded mapping/assimilation/routing pipeline is causally sensitive to changed source inputs.",
            ],
            "search_lanes": lanes,
        },
        providers=providers,
        max_workers=6,
    )


def _counterfactual_branch_projection(
    selected_seeds: Sequence[Mapping[str, Any]], assimilation: Mapping[str, Any]
) -> dict[str, Any]:
    """Rerun the registered branch-maturation rule over counterfactual mappings."""

    mappings = list(assimilation.get("theory_mappings", []))
    branch_rows = []
    for seed in selected_seeds:
        hypothesis_id = str(seed["hypothesis_id"])
        impacts = [row for row in mappings if hypothesis_id in row.get("theory_object_ids", [])]
        source_ids = sorted({str(row["source_id"]) for row in impacts})
        limitations = sorted({str(row["source_limitation"]) for row in impacts})
        changed_question = (
            "Which explicit mediator and correction condition would make this branch answer: "
            + str(seed["maturation_question"])
            + (
                " under the exact source limitations " + " | ".join(limitations)
                if limitations
                else " when no literature-derived constraint is available"
            )
        )
        branch_rows.append(
            {
                "hypothesis_id": hypothesis_id,
                "branch_id": seed["branch_id"],
                "mechanism_key": f"matured-{seed['mechanism_key']}",
                "source_ids": source_ids,
                "changed_question": changed_question,
                "new_explanatory_dependency": {
                    "source": seed["mechanism_key"],
                    "relation": "must_be_mediated_by",
                    "target": seed["unique_primitives"][0],
                },
                "correction_condition": "The carrier must remain testable without assuming the Yang--Mills target conclusion.",
            }
        )
    programme = {
        "selected_hypothesis_ids": [row["hypothesis_id"] for row in branch_rows],
        "changed_questions": [row["changed_question"] for row in branch_rows],
        "dependencies": [row["new_explanatory_dependency"] for row in branch_rows],
        "correction_conditions": [row["correction_condition"] for row in branch_rows],
    }
    return {
        "branch_results": branch_rows,
        "branch_results_digest": canonical_digest(branch_rows),
        "programme_projection": programme,
        "programme_digest": canonical_digest(programme),
    }


def _full_literature_counterfactual_replays(
    *,
    snapshot: Mapping[str, Any],
    assimilation: Mapping[str, Any],
    portfolio: Mapping[str, Any],
    baseline_trace: Mapping[str, Any],
    theory_catalog: Mapping[str, Any],
    hypotheses: Sequence[Mapping[str, Any]],
) -> dict[str, Any]:
    """Extend exact generic derivation replay through target routing and branches."""

    worlds = _literature_counterfactual_worlds(snapshot)
    generic_replay = replay_literature_counterfactuals(
        snapshot,
        theory_catalog=theory_catalog,
        worlds=worlds,
        hypotheses=hypotheses,
        candidate_snapshot_ids=[snapshot["snapshot_id"]],
        freshness_max_age_seconds=DEFAULT_LITERATURE_FRESHNESS_SECONDS,
        freshness_evaluated_at=snapshot["search_completed_at"],
    )
    if generic_replay["baseline"]["assimilation"] != assimilation:
        raise YMCanonicalCycleError(
            "registered assimilation differs from the exact derived replay baseline"
        )
    baseline_selected = list(baseline_trace["selected_hypothesis_ids"])
    baseline_seed_by_id = {
        str(row["hypothesis_id"]): dict(row)
        for row in portfolio["parallel_branch_seeds"]
    }
    baseline_projection = _counterfactual_branch_projection(
        [baseline_seed_by_id[item] for item in baseline_selected], assimilation
    )
    replay_rows = []
    for generic_world in generic_replay["world_results"]:
        counterfactual_assimilation = generic_world["assimilation"]
        selected_seeds, route = _literature_routed_seeds(
            portfolio,
            counterfactual_assimilation,
            allow_empty_mappings=True,
            include_source_removals=False,
        )
        branch_projection = _counterfactual_branch_projection(
            selected_seeds, counterfactual_assimilation
        )
        selected_ids = [str(row["hypothesis_id"]) for row in selected_seeds]
        replay_rows.append(
            {
                "world_id": generic_world["world_id"],
                "operation": generic_world["transformation"]["operation"],
                "generic_world_digest": generic_world["content_digest"],
                "route": route,
                "selected_hypothesis_ids": selected_ids,
                "selection_changed": selected_ids != baseline_selected,
                "branch_projection": branch_projection,
                "questions_changed": (
                    branch_projection["branch_results_digest"]
                    != baseline_projection["branch_results_digest"]
                ),
                "programme_changed": (
                    branch_projection["programme_digest"]
                    != baseline_projection["programme_digest"]
                ),
            }
        )
    output = copy.deepcopy(dict(baseline_trace))
    output.pop("content_digest", None)
    output.update(
        {
            "counterfactual_replay_mode": "derived_claim_mapping_full_pipeline_local_only",
            "literature_counterfactual_replay": generic_replay,
            "baseline_branch_projection": baseline_projection,
            "full_pipeline_replays": replay_rows,
            "required_replay_operations": [
                "delete_source",
                "no_literature",
                "supersede_source",
                "contradict_source",
                "coverage_only_change",
            ],
            "all_scenarios_reexecuted": (
                len(replay_rows) == len(snapshot["sources"]) + 4
                and all(
                    row["evaluation"]["status"] == "passed"
                    for row in generic_replay["world_results"]
                )
            ),
            "null_effect_world_ids": list(generic_replay["null_effect_world_ids"]),
            "selection_change_scenarios": sorted(
                row["world_id"] for row in replay_rows if row["selection_changed"]
            ),
            "programme_change_scenarios": sorted(
                row["world_id"] for row in replay_rows if row["programme_changed"]
            ),
        }
    )
    output["content_digest"] = canonical_digest(output)
    return output


def _ym_conceptual_material(
    *,
    snapshot: Mapping[str, Any],
    assimilation: Mapping[str, Any],
    portfolio: Mapping[str, Any],
    parallel: Mapping[str, Any],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], dict[str, Any]]:
    """Forge domain systems from the executed literature and branch wave.

    The central mediator is not a generic regime-indexed bridge.  It is a
    spectral-descent transport groupoid whose objects and arrows keep three
    non-substitutable Yang--Mills burdens separate: producing a positive scale,
    proving that observables see the physical nonvacuum sector, and showing
    that both structures descend coherently across regulators/representations.
    """

    target_pressures = [
        "Produce a positive physical scale from finite-regulator control without assuming the desired continuum gap.",
        "Show that the gauge-invariant Euclidean observable sector detects every relevant nonvacuum Hamiltonian mode after OS reconstruction.",
        "Establish regulator-independent continuum identity and nontriviality while preserving the scale and observable semantics.",
    ]
    protected = [
        "Exact gauge invariance and reflection positivity where a constructive presentation supplies them.",
        "Rigorous finite-volume, strong-coupling, and lower-dimensional estimates inside their proven regimes.",
        "The distinction between Euclidean reconstruction, continuum universality, nontriviality, and a Hamiltonian spectral conclusion.",
    ]
    non_claim = (
        "This conceptual system is a conjectural organization of proof burdens. It proves no source claim, continuum construction, "
        "universality theorem, observable-completeness theorem, or Yang--Mills mass gap."
    )

    incumbent_id = "ym21-system-incumbent-regulator-chain"
    incumbent_primitives = [
        "regulated gauge field measure",
        "retained-boundary kernel",
        "finite-cutoff correlation estimate",
        "OS reconstruction endpoint",
    ]
    incumbent_relations = [
        "coarse_grains_to",
        "bounds_correlations_in",
        "reconstructs_after_limit",
    ]
    incumbent_mechanism = (
        "A sequential constructive chain obtains finite-regulator control, removes cutoffs, reconstructs a Hilbert space, "
        "and then attempts to identify exponential decay with a Hamiltonian gap."
    )
    incumbent_question = (
        "Which independently proved interfaces prevent a finite-regulator estimate from changing meaning as it crosses the continuum and OS steps?"
    )
    incumbent = {
        "system_id": incumbent_id,
        "relation": "incumbent",
        "lifecycle_state": "articulated",
        "structural_identity": _structural_identity(
            incumbent_id,
            primitives=incumbent_primitives,
            relations=incumbent_relations,
            mechanism=incumbent_mechanism,
            question=incumbent_question,
            genealogy=[],
        ),
        "conceptual_ancestors": [],
        "transformation_operations": ["genealogical reconstruction", "proof-interface decomposition"],
        "primitives": incumbent_primitives,
        "ontological_commitments": [
            "A concrete regulator and retained kernel are the primary carriers of constructive control.",
            "Continuum identity is expected to be established after finite-regulator estimates are secured.",
        ],
        "identities_and_differences": [
            "A finite-regulator transfer operator is not the reconstructed physical Hamiltonian.",
            "Volume uniformity and cutoff uniformity are independent quantifier demands.",
        ],
        "relations_operations_and_dynamics": incumbent_relations,
        "explanatory_ideal": "mechanism",
        "mechanism_or_principle": incumbent_mechanism,
        "protected_successes": protected,
        "target_pressures_addressed": target_pressures,
        "formerly_inexpressible_now_visible": [
            "The incumbent chain makes local estimate production explicit but leaves semantic transport between stages underdescribed."
        ],
        "unification_claims": {
            "unified_cases_or_routes": [
                "finite lattice coercivity",
                "block RG estimates",
                "OS reconstruction",
            ],
            "common_principle": "Sequential control through one constructive presentation.",
            "differences_preserved": [
                "Finite-regulator estimates remain distinct from continuum spectral conclusions."
            ],
            "erasure_risks": [
                "A sequential diagram can hide that an arrow changes the semantic object being controlled."
            ],
        },
        "implications_and_new_questions": [incumbent_question],
        "formalization_seeds": [
            "State every interface theorem and its quantifier order in the incumbent regulator-to-Hamiltonian chain."
        ],
        "correction_conditions": [
            "Revise the incumbent if one kernel cannot transport both observable meaning and spectral scale through regulator removal."
        ],
        "residual_contradictions": [
            "The object carrying the estimate can change before the physical spectral claim is formed."
        ],
        "non_claims": [non_claim],
    }

    scale_id = "ym21-system-coercive-scale-cocycle"
    scale_primitives = [
        "spectral-scale production witness",
        "spectral-scale cocycle",
        "arrow distortion seminorm",
    ]
    scale_relations = ["produces_scale_on", "transports_with_distortion", "composes_multiplicatively"]
    scale_mechanism = (
        "Assign each regulated presentation a dimensionful candidate scale produced by a noncircular coercive estimate, and assign each admissible comparison arrow a proved distortion bound whose composition law controls loss of scale."
    )
    scale_question = (
        "Can a positive, dimensionally normalized scale assignment obey a cutoff-uniform cocycle inequality on independently defined regulator-comparison arrows?"
    )
    scale = {
        "system_id": scale_id,
        "relation": "rival",
        "lifecycle_state": "reflectively_revised",
        "structural_identity": _structural_identity(
            scale_id,
            primitives=scale_primitives,
            relations=scale_relations,
            mechanism=scale_mechanism,
            question=scale_question,
            genealogy=["YM21-R05"],
        ),
        "conceptual_ancestors": ["YM21-R05"],
        "transformation_operations": [
            "split scale production from scale interpretation",
            "replace scalar gap estimate by a transport cocycle",
        ],
        "primitives": scale_primitives,
        "ontological_commitments": [
            "A candidate mass scale is a presentation-indexed quantity until its transport law is proved.",
            "The coercive witness must be definable without using the desired continuum spectral conclusion."
        ],
        "identities_and_differences": [
            "Positivity of a lattice Poincare constant is distinct from persistence of a dimensionful scale under cutoff removal.",
            "Volume-uniform control does not entail arrow-wise cutoff control."
        ],
        "relations_operations_and_dynamics": scale_relations,
        "explanatory_ideal": "process",
        "mechanism_or_principle": scale_mechanism,
        "protected_successes": protected,
        "target_pressures_addressed": [target_pressures[0], target_pressures[2]],
        "formerly_inexpressible_now_visible": [
            "Scale loss can be localized to a named comparison arrow rather than hidden inside an undifferentiated continuum limit."
        ],
        "unification_claims": {
            "unified_cases_or_routes": [
                "lattice Poincare/coercivity estimates",
                "transfer-matrix gaps",
                "multiscale RG comparison bounds",
            ],
            "common_principle": "Each route produces and transports a candidate scale with explicit distortion debt.",
            "differences_preserved": [
                "A functional-inequality constant, transfer-operator gap, and Hamiltonian spectral gap retain different semantics."
            ],
            "erasure_risks": [
                "Calling every positive constant a scale cocycle could relabel rather than solve the transfer problem."
            ],
        },
        "implications_and_new_questions": [
            scale_question,
            "Which comparison arrows preserve physical units rather than only dimensionless lattice separation?",
        ],
        "formalization_seeds": [
            "Define the scale-production domain and prove a noncircular arrow-distortion inequality."
        ],
        "correction_conditions": [
            "Demote if the cocycle is defined using a spectral gap of the target Hamiltonian.",
            "Split the system if scale composition depends on the regulator path."
        ],
        "residual_contradictions": [
            "A transported scale can remain positive while the observable sector fails to detect hidden nonvacuum states."
        ],
        "non_claims": [non_claim],
    }

    observable_id = "ym21-system-observable-completeness"
    observable_primitives = [
        "gauge-invariant observable detector family",
        "nonvacuum separating core",
        "OS spectral access relation",
    ]
    observable_relations = [
        "detects_nonvacuum_sector",
        "is_dense_after_OS_reconstruction",
        "separates_hidden_modes",
    ]
    observable_mechanism = (
        "Treat Euclidean clustering as a statement about a detector family and require an independent conservativity/density theorem showing that the reconstructed gauge-invariant core separates every relevant nonvacuum Hamiltonian mode."
    )
    observable_question = (
        "What exact density or recovery condition makes exponential Euclidean decay equivalent to control of the full physical nonvacuum spectrum?"
    )
    observable = {
        "system_id": observable_id,
        "relation": "rival",
        "lifecycle_state": "reflectively_revised",
        "structural_identity": _structural_identity(
            observable_id,
            primitives=observable_primitives,
            relations=observable_relations,
            mechanism=observable_mechanism,
            question=observable_question,
            genealogy=["YM21-R02"],
        ),
        "conceptual_ancestors": ["YM21-R02"],
        "transformation_operations": [
            "split existence of a mode from accessibility by an observable",
            "replace correlation decay by detector-relative spectral access",
        ],
        "primitives": observable_primitives,
        "ontological_commitments": [
            "A spectral mode may exist without being visible to a chosen Euclidean observable family.",
            "Physical completeness is a property of the reconstructed observable action, not of decay rates alone."
        ],
        "identities_and_differences": [
            "Reflection positivity enables reconstruction but does not prove detector conservativity.",
            "Exponential clustering of a subalgebra is not automatically a gap for the whole nonvacuum Hilbert space."
        ],
        "relations_operations_and_dynamics": observable_relations,
        "explanatory_ideal": "constraint",
        "mechanism_or_principle": observable_mechanism,
        "protected_successes": protected,
        "target_pressures_addressed": [target_pressures[1], target_pressures[2]],
        "formerly_inexpressible_now_visible": [
            "Hidden-mode failure is an explicit kernel of the observable detector rather than an informal worry about reconstruction."
        ],
        "unification_claims": {
            "unified_cases_or_routes": [
                "Schwinger-function clustering",
                "observable-net completeness",
                "OS Hamiltonian reconstruction",
            ],
            "common_principle": "Spectral inference is licensed only through a conservative reconstructed detector family.",
            "differences_preserved": [
                "Decay production and completeness of the detecting observables remain independent burdens."
            ],
            "erasure_risks": [
                "Defining completeness as whatever detects the desired gap would make the system circular."
            ],
        },
        "implications_and_new_questions": [
            observable_question,
            "Can a reflection-positive gauge-invariant subalgebra have exponential decay while missing a gapless superselection sector?",
        ],
        "formalization_seeds": [
            "Define detector conservativity on the reconstructed nonvacuum sector and construct boundary countermodels."
        ],
        "correction_conditions": [
            "Reject any completeness condition defined by assuming the target spectral gap.",
            "Revise if the physical target quantifies over sectors not generated by the proposed observable core."
        ],
        "residual_contradictions": [
            "A complete detector can reveal that a candidate scale vanishes; completeness does not create positivity."
        ],
        "non_claims": [non_claim],
    }

    transport_id = "ym21-system-regulator-transport-groupoid"
    transport_primitives = [
        "regulated Yang-Mills presentation",
        "admissible comparison arrow",
        "presentation descent class",
        "transport holonomy defect",
    ]
    transport_relations = [
        "transports_observable_semantics",
        "composes_as_comparison_arrow",
        "measures_holonomy_defect",
    ]
    transport_mechanism = (
        "Organize regulators, gauge-invariant presentations, and OS representations as objects connected by independently defined comparison arrows; theory identity is a coherent descent class, while nonzero loop holonomy records failed universality."
    )
    transport_question = (
        "Can admissible arrows and their coherence be defined before, and independently of, the continuum mass-gap conclusion?"
    )
    transport = {
        "system_id": transport_id,
        "relation": "challenger",
        "lifecycle_state": "reflectively_revised",
        "structural_identity": _structural_identity(
            transport_id,
            primitives=transport_primitives,
            relations=transport_relations,
            mechanism=transport_mechanism,
            question=transport_question,
            genealogy=["YM21-R06", "YM21-R08"],
        ),
        "conceptual_ancestors": ["YM21-R06", "YM21-R08"],
        "transformation_operations": [
            "replace privileged regulator identity by a transport groupoid",
            "turn universality failure into a holonomy obstruction",
        ],
        "primitives": transport_primitives,
        "ontological_commitments": [
            "The physical theory is represented by coherent equivalence data across admissible presentations, not by one privileged cutoff construction.",
            "Comparison arrows must be characterized by local constructive and semantic conditions that do not presuppose a positive gap."
        ],
        "identities_and_differences": [
            "Approximate comparison, unitary equivalence, and OS reconstruction are different arrow types.",
            "Path independence of theory identity is distinct from preservation of any particular positive scale."
        ],
        "relations_operations_and_dynamics": transport_relations,
        "explanatory_ideal": "structure",
        "mechanism_or_principle": transport_mechanism,
        "protected_successes": protected,
        "target_pressures_addressed": [target_pressures[1], target_pressures[2]],
        "formerly_inexpressible_now_visible": [
            "Universality failure becomes a path-dependent transport defect with a location and composition law."
        ],
        "unification_claims": {
            "unified_cases_or_routes": [
                "cutoff refinement",
                "block-spin comparison",
                "Euclidean-to-Hamiltonian reconstruction",
                "representation equivalence",
            ],
            "common_principle": "All identity claims are typed arrows whose composites expose coherence or holonomy debt.",
            "differences_preserved": [
                "Regulator refinement, representation change, and OS reconstruction remain typed, non-interchangeable arrows."
            ],
            "erasure_risks": [
                "A category can merely redescribe the missing comparison theorems if admissibility and coherence have no independent content."
            ],
        },
        "implications_and_new_questions": [
            transport_question,
            "Which loop defects distinguish universality failure from harmless choice of presentation?",
        ],
        "formalization_seeds": [
            "Define presentation objects, typed arrows, composition, and holonomy without invoking the desired gap."
        ],
        "correction_conditions": [
            "Demote if admissible arrows are defined as precisely those preserving the desired continuum gap.",
            "Retain plural presentations if comparison loops carry a nonvanishing target-relevant defect."
        ],
        "residual_contradictions": [
            "Coherent transport can identify a continuum theory whose physical spectrum is nevertheless gapless."
        ],
        "non_claims": [non_claim],
    }

    synthesis_id = SYNTHESIS_SYSTEM_ID
    synthesis_primitives = [
        "regulated Yang-Mills presentation",
        "admissible comparison arrow",
        "spectral-scale production witness",
        "spectral-scale cocycle",
        "observable-completeness witness",
        "gauge-invariant observable detector family",
        "descent-stability witness",
        "spectral-descent transport groupoid",
        "transport holonomy defect",
    ]
    synthesis_relations = [
        "produces_scale_on",
        "detects_nonvacuum_sector",
        "transports_observable_semantics",
        "satisfies_descent_cocycle",
        "measures_holonomy_defect",
        "factors_gap_transfer_into",
    ]
    synthesis_mechanism = (
        "A spectral-descent transport groupoid factors any proposed lattice-to-continuum mass-gap argument into three separately falsifiable witnesses: "
        "a noncircular coercive mechanism that produces a dimensionful candidate scale on each regulated presentation; a conservative gauge-invariant observable family that detects the reconstructed nonvacuum spectrum; and a descent-stability law showing that scale and observable semantics compose coherently across independently defined regulator, continuum, and representation arrows. "
        "Only their conjunction could license a presentation-independent spectral conclusion."
    )
    synthesis_question = (
        "Which minimal independent axioms on scale production, detector conservativity, and arrow coherence imply a positive regulator-independent Hamiltonian spectral lower bound without defining any axiom by that conclusion?"
    )
    formalization = [
        "YM21-F01: Define the spectral-descent transport groupoid: regulated reflection-positive Yang-Mills presentations as objects; refinement, comparison, continuum, and OS maps as typed arrows; identities, domains, and composition must be stated without a mass-gap premise.",
        "YM21-F02: Define a dimensionful scale-production witness kappa(P) from coercive, Poincare, transfer, or clustering data and state volume, lattice-spacing, coupling, and physical-unit quantifiers explicitly.",
        "YM21-F03: Define a gauge-invariant observable detector functor O(P) and an exact conservativity/density condition on the OS reconstructed nonvacuum Hilbert sector.",
        "YM21-F04: Prove or refute a recovery theorem connecting Euclidean detector correlations to the full Hamiltonian spectral measure, including superselection and hidden-mode boundary cases.",
        "YM21-F05: Define arrow distortion D(f) for the scale witness and prove kappa(Q) >= D(f) kappa(P), with a nonvacuous composition inequality for D(g composed with f).",
        "YM21-F06: Define transport of observable semantics along each arrow type and prove compatibility with reflection positivity, quotienting null states, and OS time evolution.",
        "YM21-F07: Define descent stability as path independence or a quantitatively vanishing holonomy defect on regulator-comparison loops, with cutoff-uniform rates and no post hoc admissibility.",
        "YM21-F08: Prove continuum identity and nontriviality for the descended object independently of the scale witness, distinguishing equivalence of selected observables from equivalence of theories.",
        "YM21-F09: Prove a conditional spectral-descent theorem and three independence countermodels: positive scale with incomplete detectors; complete detectors with vanishing scale; and both local witnesses with unstable/path-dependent descent.",
    ]
    corrections = [
        "YM21-C01: Reject the mediator if an admissible arrow is defined by preserving the mass gap or by assuming the target continuum theory.",
        "YM21-C02: Split or demote the scale component if volume-uniform coercivity fails to control lattice-spacing removal in physical units.",
        "YM21-C03: Reject the observable component if its detector family has a nontrivial kernel on any target-relevant nonvacuum sector.",
        "YM21-C04: Abandon regulator-independent synthesis if comparison-loop holonomy remains nonzero or path dependent at the continuum limit.",
        "YM21-C05: Revise the ontology if groupoid language adds no independently checkable law beyond listing the original missing lemmas.",
        "YM21-C06: Retire the programme if it cannot recover established reflection-positive finite-regulator results without changing the Clay target's dimension, gauge-group scope, nontriviality, or Hamiltonian meaning."
    ]
    synthesis = {
        "system_id": synthesis_id,
        "relation": "synthesis",
        "lifecycle_state": "synthesized",
        "structural_identity": _structural_identity(
            synthesis_id,
            primitives=synthesis_primitives,
            relations=synthesis_relations,
            mechanism=synthesis_mechanism,
            question=synthesis_question,
            genealogy=[scale_id, observable_id, transport_id],
        ),
        "conceptual_ancestors": [scale_id, observable_id, transport_id],
        "transformation_operations": [
            "three-factor proof-burden decomposition",
            "spectral-descent groupoid synthesis",
            "unification with non-substitutable witnesses",
            "adversarial noncircularity hardening",
        ],
        "primitives": synthesis_primitives,
        "ontological_commitments": [
            "The same physical Yang-Mills theory is a coherent descent class of presentations, not an unexamined identity of their local carriers.",
            "A physical mass scale is neither a bare finite-cutoff number nor a detector-relative correlation length; it is a produced, detected, and stably descended invariant.",
            "The three witnesses are jointly necessary within this programme and none may be defined by the desired Hamiltonian conclusion."
        ],
        "identities_and_differences": [
            "Scale production answers why a positive number appears; observable completeness answers whether it controls every relevant physical mode; descent stability answers whether that meaning survives presentation change.",
            "Regulator refinement, continuum passage, OS reconstruction, and unitary representation comparison remain distinct arrow types.",
            "Theory identity, nontriviality, and a positive spectral lower bound remain distinct conclusions."
        ],
        "relations_operations_and_dynamics": [*synthesis_relations, synthesis_mechanism],
        "explanatory_ideal": "unification",
        "mechanism_or_principle": synthesis_mechanism,
        "protected_successes": protected,
        "target_pressures_addressed": target_pressures,
        "formerly_inexpressible_now_visible": [
            "A mass-gap transfer failure can now be located in one of three non-substitutable interfaces—scale production, observable completeness, or descent stability—instead of being displaced inside an undifferentiated lattice-to-continuum bridge.",
            "Universality debt becomes a typed holonomy defect, while hidden spectral modes become a kernel of the reconstructed detector family."
        ],
        "unification_claims": {
            "unified_cases_or_routes": [
                "lattice coercivity and transfer-matrix routes",
                "Euclidean clustering and OS reconstruction routes",
                "observable-net and algebraic-QFT completeness routes",
                "RG universality and regulator-comparison routes",
            ],
            "common_principle": (
                "A regulator-independent mass-gap conclusion requires a produced scale, a complete physical detector, and coherent descent of both across typed presentation changes."
            ),
            "differences_preserved": [
                "Coercive scale production does not prove observable completeness.",
                "Observable completeness does not produce a positive scale.",
                "Descent coherence neither produces the scale nor proves detector conservativity.",
                "OS reconstruction is not regulator universality.",
                "Agreement of selected observables is not full theory identity or nontriviality.",
                "A vanishing holonomy defect is a transport condition, not a proof of a positive Hamiltonian lower bound."
            ],
            "erasure_risks": [
                "Calling every proof step an arrow could hide rather than solve missing estimates.",
                "Post hoc restriction to gap-preserving arrows would make descent circular.",
                "A single scalar invariant would erase the distinct semantics of scale, detection, and identity."
            ],
        },
        "implications_and_new_questions": [
            synthesis_question,
            "Can one construct a finite countermodel with a positive scale cocycle but a nonconservative observable detector?",
            "Which regulator-comparison loops expose nonuniversality through a nonvanishing transport holonomy defect?",
            "Does an AQFT recovery or nuclearity condition supply exactly the detector conservativity needed after OS reconstruction?",
            "Can the conditional F09 theorem be proved before any full Yang-Mills construction, thereby testing whether the mediator has real mathematical content?",
        ],
        "formalization_seeds": formalization,
        "correction_conditions": corrections,
        "residual_contradictions": [
            "It remains unknown whether a noncircular arrow class broad enough for four-dimensional Yang-Mills admits cutoff-uniform distortion and vanishing holonomy; the live dissent is that continuum identity may be local/algebraic without any globally coherent spectral-scale cocycle."
        ],
        "non_claims": [non_claim],
    }

    rounds = [
        {
            "round_id": "ym21-reflection-01-scale-cocycle",
            "system_ids": [incumbent_id, scale_id],
            "lenses_used": ["ontological", "representational", "modal"],
            "strongest_objections": [
                "A lattice gap or Poincare constant is not one object across changes of lattice spacing, coupling, volume, and units; treating it as such assumes the identity that must be earned.",
                "A cocycle can be empty notation unless arrow distortion is defined by independent estimates and composes nonvacuously."
            ],
            "blind_spots": [
                "The scale cocycle alone cannot show that the chosen observable family detects every physical nonvacuum mode."
            ],
            "mutation_or_synthesis": {
                "operation": "replace a regulator-local scalar gap surrogate by a dimensionful spectral-scale production witness plus an arrow-distortion cocycle",
                "changed_primitives_relations_or_explanation": [
                    "spectral-scale production witness",
                    "spectral-scale cocycle",
                    "transports_with_distortion",
                    "Scale survival is an arrow-wise composition burden rather than an automatic property of a positive finite-cutoff constant."
                ],
                "preserved_content": [protected[0], protected[1]],
                "lost_content": [
                    "The assumption that one positive regulator-local number has stable physical meaning before a transport law is proved."
                ],
            },
            "result": "mutated",
            "no_change_reason": None,
        },
        {
            "round_id": "ym21-reflection-02-observable-conservativity",
            "system_ids": [incumbent_id, observable_id],
            "lenses_used": ["epistemological", "explanatory", "representational"],
            "strongest_objections": [
                "Exponential decay only describes what the selected Euclidean observables can see; a hidden nonvacuum sector can invalidate the inference to a full Hamiltonian gap.",
                "Declaring the observable core complete because it yields the desired spectral conclusion would be circular."
            ],
            "blind_spots": [
                "Even a conservative detector can faithfully reveal a scale that collapses during regulator removal."
            ],
            "mutation_or_synthesis": {
                "operation": "split correlation decay from physical spectral access and introduce a conservative gauge-invariant observable detector",
                "changed_primitives_relations_or_explanation": [
                    "observable-completeness witness",
                    "nonvacuum separating core",
                    "detects_nonvacuum_sector",
                    "Hidden-mode risk becomes the kernel of a named detector map."
                ],
                "preserved_content": [protected[0], protected[2]],
                "lost_content": [
                    "The inference that reflection positivity plus clustering automatically controls the entire nonvacuum spectrum."
                ],
            },
            "result": "mutated",
            "no_change_reason": None,
        },
        {
            "round_id": "ym21-reflection-03-spectral-descent-synthesis",
            "system_ids": [scale_id, observable_id, transport_id, synthesis_id],
            "lenses_used": ["dialectical", "unificatory", "ontological", "explanatory"],
            "strongest_objections": [
                "Scale production, detector completeness, and theory identity protect different successes; collapsing them into one transfer principle would erase the very failures the synthesis is meant to explain.",
                "Groupoid language risks turning a list of unproved comparison lemmas into decorative categorical vocabulary."
            ],
            "blind_spots": [
                "The synthesis does not yet show that any nontrivial four-dimensional Yang-Mills presentation satisfies all three witness conditions."
            ],
            "mutation_or_synthesis": {
                "operation": "synthesize a spectral-descent transport groupoid with three non-substitutable witnesses and typed arrow classes",
                "changed_primitives_relations_or_explanation": [
                    "spectral-descent transport groupoid",
                    "descent-stability witness",
                    "factors_gap_transfer_into",
                    "A physical spectral invariant is produced, detected, and descended rather than merely carried through one sequential proof narrative."
                ],
                "preserved_content": protected,
                "lost_content": [
                    "The expectation that any one route—coercive, observable, or universality-based—can silently discharge the other two burdens."
                ],
            },
            "result": "synthesized",
            "no_change_reason": None,
        },
        {
            "round_id": "ym21-reflection-04-adversarial-holonomy",
            "system_ids": [incumbent_id, transport_id, synthesis_id],
            "lenses_used": ["reflexive", "genealogical", "modal", "dialectical"],
            "strongest_objections": [
                "The proposed mediator may manufacture depth by renaming universality as descent and missing comparison estimates as holonomy.",
                "Admissible arrows may be selected post hoc so that all inconvenient regulator paths disappear, making the theory self-sealing.",
                "The groupoid could preserve formal coherence while descending a trivial or gapless continuum object."
            ],
            "blind_spots": [
                "No current source establishes the required noncircular arrow class or cutoff-uniform holonomy estimate in four-dimensional pure Yang-Mills."
            ],
            "mutation_or_synthesis": {
                "operation": "harden the synthesis with independent arrow admissibility, explicit holonomy obstruction, nontriviality separation, and three independence countermodels",
                "changed_primitives_relations_or_explanation": [
                    "transport holonomy defect",
                    "measures_holonomy_defect",
                    "YM21-F07 cutoff-uniform path-independence obligation",
                    "YM21-F09 three-way independence countermodel obligation",
                    "Arrow admissibility must be testable before the mass-gap conclusion."
                ],
                "preserved_content": protected,
                "lost_content": [
                    "Category-theoretic coherence as sufficient evidence of physical universality.",
                    "Any post hoc freedom to define admissible arrows by success."
                ],
            },
            "result": "mutated",
            "no_change_reason": None,
        },
    ]
    branch_results = [dict(row) for row in parallel.get("branch_results", [])]
    generated_portfolio_ids = {
        str(row["hypothesis_id"]) for row in portfolio.get("hypotheses", [])
    }
    selected_hypothesis_ids = sorted(
        {
            str(row.get("genealogy", [""])[0])
            for row in branch_results
            if row.get("genealogy")
            and str(row.get("genealogy", [""])[0]) in generated_portfolio_ids
        }
    )
    changed_questions = sorted(
        {
            str(row.get("theory_delta", {}).get("changed_question"))
            for row in branch_results
            if str(row.get("theory_delta", {}).get("changed_question", "")).strip()
        }
    )
    if len(selected_hypothesis_ids) < 4 or len(changed_questions) < 4:
        raise YMCanonicalCycleError("concept forging requires four valid literature-rebased branch deltas")
    source_ids = sorted(
        {
            str(mapping["source_id"])
            for mapping in assimilation.get("theory_mappings", [])
            if set(mapping.get("theory_object_ids", [])) & set(selected_hypothesis_ids)
        }
    )
    if snapshot.get("snapshot_id") != assimilation.get("selected_snapshot", {}).get("snapshot_id"):
        raise YMCanonicalCycleError("concept forging crossed its current literature snapshot")

    synthesis["conceptual_ancestors"] = sorted(
        set(synthesis["conceptual_ancestors"]) | set(selected_hypothesis_ids)
    )
    synthesis["structural_identity"]["genealogy_ids"] = list(synthesis["conceptual_ancestors"])
    synthesis["implications_and_new_questions"] = list(
        dict.fromkeys([*synthesis["implications_and_new_questions"], *changed_questions])
    )
    rounds[2]["strongest_objections"].append(
        "Executed branch deltas disagree across "
        + ", ".join(selected_hypothesis_ids)
        + "; synthesis must preserve their source-conditioned distinctions rather than average them."
    )
    generation_trace = {
        "schema_version": "1.0.0",
        "snapshot_id": snapshot["snapshot_id"],
        "snapshot_digest": snapshot["content_digest"],
        "assimilation_packet_id": assimilation["packet_id"],
        "assimilation_digest": canonical_digest(assimilation),
        "portfolio_id": portfolio["portfolio_id"],
        "portfolio_digest": canonical_digest(portfolio),
        "parallel_portfolio_id": parallel["portfolio_id"],
        "parallel_digest": canonical_digest(parallel),
        "selected_hypothesis_ids": selected_hypothesis_ids,
        "causal_source_ids": source_ids,
        "branch_changed_questions": changed_questions,
        "generated_systems_digest": canonical_digest([incumbent, scale, observable, transport, synthesis]),
        "parent_rounds_digest": canonical_digest(rounds[:3]),
        "generation_rule": (
            "Domain templates are instantiated only after current-source assimilation and isolated branch maturation; "
            "selected branch genealogy and changed questions alter the synthesis and its third reflection round."
        ),
        "authority_boundary": "Generation is conjectural conceptual work and supplies no mathematical or source-claim authority.",
    }
    generation_trace["content_digest"] = canonical_digest(generation_trace)
    return [incumbent, scale, observable, transport, synthesis], rounds, generation_trace


def _assimilate_probe_round(
    systems: list[dict[str, Any]],
    rounds: list[dict[str, Any]],
    experiment_receipt: Mapping[str, Any],
    *,
    selected_system_id: str,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    """Apply the commissioned counterexample as an exact conceptual mutation.

    The receipt cannot merely add commentary.  It changes the selected
    system's F05/F07 obligations and C04 correction condition, while an
    objection/correction link names every changed JSON-pointer path.  The
    parent objects remain untouched so the adjudicator can verify the patch.
    """

    if len(rounds) != 4:
        raise YMCanonicalCycleError("probe assimilation requires the four-round conceptual template")
    output_systems = copy.deepcopy(systems)
    output_rounds = copy.deepcopy(rounds)
    final = output_rounds[-1]
    status = str(experiment_receipt.get("status"))
    outcome = str(experiment_receipt.get("epistemic_outcome"))
    result = experiment_receipt.get("result", {})
    if status != "counterexample" or outcome != "falsifies_claim":
        raise YMCanonicalCycleError("YM21 adversarial probe must expose the preregistered path-independence counterexample")
    witness = experiment_receipt.get("certificate", {})
    objection = (
        "The commissioned exact toy produced unequal path factors "
        f"({witness.get('left')} versus {witness.get('right')}); multiplicative composition alone therefore cannot imply path-independent descent."
    )
    correction_test = (
        "For every claimed path-independent transport law, compare at least two independently admissible paths with common endpoints and retain their exact holonomy defect as a separate obligation whenever the composites differ."
    )
    final["strongest_objections"].append(objection)
    final["correction_tests"] = [correction_test]
    final["mutation_or_synthesis"]["changed_primitives_relations_or_explanation"].append(
        "The exact counterexample forces path holonomy to remain a separate obstruction rather than a consequence of local factor multiplication."
    )
    final["mutation_or_synthesis"]["lost_content"].append(
        "The preregistered toy assumption that locally composable distortion factors automatically agree across regulator paths."
    )
    final["blind_spots"].append(
        "The finite rational counterexample diagnoses notation only and does not establish which comparison paths exist in Yang--Mills theory."
    )
    if (
        result.get("claim_holds") is not False
        or result.get("exact_values")
        != {"left": "1/2", "right": "5/8", "difference": "-1/8"}
    ):
        raise YMCanonicalCycleError("counterexample receipt does not contain the expected unequal exact result")

    selected = next(
        (
            system
            for system in output_systems
            if system.get("system_id") == selected_system_id
        ),
        None,
    )
    if selected is None:
        raise YMCanonicalCycleError("probe assimilation cannot resolve the selected conceptual system")
    if selected_system_id != SYNTHESIS_SYSTEM_ID:
        raise YMCanonicalCycleError("the exact descent probe may mutate only the selected spectral-descent synthesis")

    formalization = list(selected.get("formalization_seeds", []))
    corrections = list(selected.get("correction_conditions", []))
    if len(formalization) != 9 or len(corrections) != 6:
        raise YMCanonicalCycleError("selected synthesis lacks its complete pre-probe F01--F09/C01--C06 programme")
    formalization[4] = (
        "YM21-F05: Define arrow distortion D(f) for the scale witness, prove kappa(Q) >= D(f) kappa(P), and state composition only as a typed local inequality; no composite law may imply endpoint path equality without a separate comparison theorem."
    )
    formalization[6] = (
        "YM21-F07: Define descent stability by direct comparison of independently admissible common-endpoint path composites, record their transport holonomy defect exactly, and prove a cutoff-uniform vanishing bound rather than deriving path independence from local multiplicativity."
    )
    corrections[3] = (
        "YM21-C04: Abandon regulator-independent synthesis if any independently admissible common-endpoint comparison paths retain nonzero or path-dependent holonomy at the continuum limit; local composition laws alone do not discharge this test."
    )
    selected["formalization_seeds"] = formalization
    selected["correction_conditions"] = corrections
    final["semantic_patch_links"] = [
        {
            "candidate_ref": selected_system_id,
            "objection": objection,
            "correction_test": correction_test,
            "changed_paths": ["/correction_conditions", "/formalization_seeds"],
        }
    ]
    return output_systems, output_rounds


def _budget() -> dict[str, Any]:
    return {
        "budget_id": "ym21-exact-support-budget",
        "wall_time_seconds": 5.0,
        "grace_period_seconds": 0.1,
        "cpu_seconds": 2.0,
        "memory_bytes": 256 * 1024 * 1024,
        "disk_bytes": 16 * 1024 * 1024,
        "network_bytes": 0,
        "token_count": 0,
        "request_count": 0,
        "cost_usd": 0.0,
    }


class CycleExecution:
    def __init__(self, output_root: Path) -> None:
        self.output_root = output_root.resolve()
        self.workspace = self.output_root / "workspace"
        self.state_root = self.output_root / "state"
        self.workspace.mkdir(parents=True, exist_ok=True)
        self.namespace = Namespace(TARGET_ID, RUN_ID, "root", STATE_VERSION)
        self.prior_state = initial_state(TARGET_ID, RUN_ID)
        self.theory_digest = canonical_digest(self.prior_state)
        self.requests: list[dict[str, Any]] = []
        self.receipts: list[dict[str, Any]] = []
        self.roles: dict[str, Any] = {}
        self.counter = 0
        # Registry commands execute from the isolated workspace. Preserve the
        # exact registry argv while making this repository importable.
        prior_pythonpath = os.environ.get("PYTHONPATH", "")
        os.environ["PYTHONPATH"] = os.pathsep.join(
            value for value in (str(ROOT), prior_pythonpath) if value
        )
        self.dispatcher = DiscoveryOperatorDispatcher(
            registry_bindings(load_registry()),
            workspace=self.workspace,
            receipt_store=ReceiptStore(self.workspace / "operator-receipts"),
        )

    def dispatch(
        self,
        operator_id: str,
        kind: str,
        envelope: Mapping[str, Any],
        *,
        branch_id: str = "root",
        parameters: Mapping[str, Any] | None = None,
    ) -> tuple[dict[str, Any], dict[str, Any], str]:
        envelope = copy.deepcopy(dict(envelope))
        if hasattr(self, "source_routing_precommit") and operator_id in {
            "high-risk-hypothesis-forger",
            "parallel-hypothesis-portfolio",
            "reflective-conceptual-discovery",
            "reflective-theory-synthesizer",
            "dynamic-symbolic-simulation-experimenter",
            "blind-conceptual-preference-adjudicator",
        }:
            envelope["source_routing_precommit"] = copy.deepcopy(
                self.source_routing_precommit
            )
        self.counter += 1
        namespace = Namespace(TARGET_ID, RUN_ID, branch_id, STATE_VERSION)
        input_relative = f"operator-inputs/{self.counter:02d}-{operator_id}.json"
        output_relative = f"operator-outputs/{self.counter:02d}-{operator_id}.json"
        input_path = _write_immutable_json(self.workspace / input_relative, envelope)
        request = build_operator_request(
            operator_id=operator_id,
            operator_version="1.0.0",
            kind=kind,
            namespace=namespace,
            invocation_id=f"ym21-{self.counter:02d}-{operator_id}",
            input_artifacts=[artifact_descriptor(input_path, self.workspace, namespace)],
            declared_outputs=[output_relative],
            parameters=dict(parameters or {}),
            required=True,
            requested_at=REQUESTED_AT,
        )
        receipt = self.dispatcher.dispatch(request)
        if receipt["status"] != "succeeded":
            raise YMCanonicalCycleError(
                f"registered operator failed: {operator_id}: {receipt.get('error')}"
            )
        self.requests.append(request)
        self.receipts.append(receipt)
        return load_json(self.workspace / output_relative), receipt, output_relative

    def reflection_request(
        self,
        portfolio: Mapping[str, Any],
        parallel: Mapping[str, Any],
        snapshot: Mapping[str, Any],
        assimilation_path: str,
    ) -> dict[str, Any]:
        source_deltas = [
            (
                "The 2026 lattice-coercivity claim makes volume-uniform Poincare constants, continuum "
                "tightness, and OS/nontriviality separate priority audits."
            ),
            (
                "arXiv:2606.19362 changes R02/R04/R05/R06/R07/R08/R09/R10 priorities through six "
                "claim-specific mappings rather than a portfolio-wide endorsement."
            ),
            (
                "Current rigorous strong-coupling and 2D/3D stochastic results sharpen boundary conditions "
                "but do not transfer the Clay conclusion."
            ),
        ]
        return {
            "target_id": TARGET_ID,
            "run_id": RUN_ID,
            "branch_id": "root",
            "state_version": STATE_VERSION,
            "prior_conceptual_state_ref": "state:0",
            "discovery_charter": {
                "essential_question": (
                    "What explanatory structure can jointly preserve continuum construction, nontriviality, "
                    "representation identity, and a positive physical spectral scale without assuming any one of them?"
                ),
                "desired_understanding": (
                    "A unified but non-collapsing account of why local coercivity, global theory identity, "
                    "and physical spectral interpretation must cohere."
                ),
                "bottleneck_diagnosis": "conceptual",
                "bottleneck_evidence": (
                    "The newest claims repeatedly bundle distinct transfer steps, while incumbent failures recur "
                    "at the relation between representation, regulator, observable completeness, and spectrum."
                ),
                "target_commitments": list(_charter(snapshot)["target_commitments"]),
                "relevance_horizon": (
                    "A successful mediation would reorganize several constructive routes and expose distinct falsifiers even before a theorem is available."
                ),
                "incumbent_framework": (
                    "normalized retained-boundary kernels, weighted defects, block RG, and OS reconstruction"
                ),
                "conceptual_opacity": (
                    "It is unclear whether representation change is controlled by one privileged kernel or is itself the invariant phenomenon."
                ),
                "non_claim_boundary": (
                    "Reflection articulates and ranks conceptual systems only; it proves no source claim, continuum theory, universality theorem, or mass gap."
                ),
            },
            "conceptual_genealogy": {
                "inherited_concepts": [
                    "reflection positivity",
                    "lattice coercivity",
                    "Osterwalder-Schrader reconstruction",
                    "retained-boundary kernel",
                    "gauge-invariant observable core",
                    "representation and regulator change"
                ],
                "historical_or_logical_formation": [
                    "Constructive lattice programmes separate finite control from regulator removal.",
                    "OS reconstruction separates Euclidean consistency from physical spectral interpretation.",
                    "The YM21 incumbent programme made normalization and hidden-mode failures explicit.",
                    "The broad 2026 frontier search exposed multiple direct claims that compress these separations."
                ],
                "protected_successes": list(_charter(snapshot)["protected_successes"]),
                "rejected_or_retired_ancestors": [
                    "repository presence as theorem validation",
                    "finite lattice gap as automatic continuum Hamiltonian gap",
                    "one scalar truth score for high-risk concepts",
                    "experiments as parent discovery controller"
                ],
                "hidden_assumptions": [
                    "one representation must be ontologically privileged",
                    "mixing of an auxiliary stochastic generator transfers to the physical Hamiltonian",
                    "uniformity in volume automatically controls cutoff removal",
                    "observable decay sees every nonvacuum spectral mode"
                ],
            },
            "literature_basis": {
                "selected_snapshot_id": snapshot["snapshot_id"],
                "snapshot_target_id": TARGET_ID,
                "selected_snapshot_digest": snapshot["content_digest"],
                "search_completed_utc": snapshot["search_completed_at"],
                "freshness_status": "current",
                "search_receipt_ids": [row["lane_id"] for row in snapshot["lane_receipts"]],
                "assimilation_packet_ref": assimilation_path,
                "source_to_theory_delta_summary": source_deltas,
                "literature_generated_questions": [
                    "Can volume-uniform lattice coercivity remain physical under weak-coupling cutoff removal without assuming the desired phase?",
                    "Which exact observable-completeness condition turns Euclidean clustering into a Hamiltonian gap?",
                    "Can representation and regulator changes be treated as a groupoid whose invariant is spectral rather than one privileged RG trajectory?",
                    "What would distinguish a genuine weak/strong theory identity from agreement of selected observables?"
                ],
                "coverage_limitations": list(snapshot["coverage_limits"]),
                "superseded_snapshot_ids": [],
            },
            "root_tensions": [
                {
                    "tension_id": "ym21-local-coercivity-vs-continuum-identity",
                    "opposed_commitments": ["volume-uniform lattice control", "nontrivial regulator-independent continuum identity"],
                    "strongest_form_of_each_side": [
                        "A finite-cutoff functional inequality can control correlations uniformly in volume.",
                        "The target requires a nontrivial four-dimensional theory along cutoff removal, not only controlled finite systems."
                    ],
                    "minimal_incompatibility_or_missing_mediation": (
                        "No independently audited carrier currently transports coercivity constants, observables, and nontriviality through the continuum limit."
                    ),
                    "regime": "weak-coupling continuum trajectory",
                    "why_root_level": "Every constructive route must solve this before its spectral estimate has target meaning."
                },
                {
                    "tension_id": "ym21-euclidean-decay-vs-physical-completeness",
                    "opposed_commitments": ["Euclidean gauge-invariant clustering", "complete nonvacuum Hamiltonian spectral control"],
                    "strongest_form_of_each_side": [
                        "Reflection-positive Schwinger functions may exhibit exponential decay.",
                        "A positive Hamiltonian gap requires that the reconstructed observable core detects every relevant nonvacuum mode."
                    ],
                    "minimal_incompatibility_or_missing_mediation": (
                        "The density/recovery theorem connecting the measured Euclidean sector to the full physical spectrum is missing."
                    ),
                    "regime": "OS reconstruction and physical-time interpretation",
                    "why_root_level": "Without the mediation, decay can coexist with hidden spectral modes."
                },
                {
                    "tension_id": "ym21-representation-choice-vs-universality",
                    "opposed_commitments": ["one constructive regulator/representation", "representation-independent physical theory"],
                    "strongest_form_of_each_side": [
                        "Proofs need a concrete regulator and state representation.",
                        "The final spectral statement must not depend on arbitrary representational choices."
                    ],
                    "minimal_incompatibility_or_missing_mediation": (
                        "There is no controlled descent invariant proving that representation changes preserve theory identity and the physical scale."
                    ),
                    "regime": "regulator comparison and universality",
                    "why_root_level": "The tension determines what counts as the same Yang-Mills theory across the entire proof."
                }
            ],
            "high_risk_portfolio": dict(portfolio),
            "parallel_portfolio": dict(parallel),
            "operator_receipt_ids": [row["receipt_id"] for row in self.receipts],
            "explicit_unknowns": [
                "No direct 2026 solution claim has been independently theorem-audited.",
                "It is unknown whether any proposed external ontology admits a noncircular constructive realization.",
                "The broad search is bounded and cannot establish novelty or exhaustiveness."
            ],
        }

    def run(self) -> dict[str, Any]:
        preflight_snapshot, capture_binding, provider_source_catalog = build_current_literature_snapshot(
            theory_state_digest=self.theory_digest, output_root=self.output_root
        )
        counterbalance_seed = "ym21-proposal-field-free-upstream-v1"
        with tempfile.TemporaryDirectory(
            prefix="ym21-generated-id-preflight-", dir=self.output_root
        ) as preflight_directory:
            preflight_workspace = Path(preflight_directory)
            preflight_envelope = prepare_proposal_field_free_high_risk_envelope(
                charter=_charter(preflight_snapshot),
                literature_snapshot=preflight_snapshot,
                workspace=preflight_workspace,
                namespace=self.namespace,
                authored_incumbent_comparison_proposals=(
                    _authored_domain_template_incumbent_comparison_proposals(
                        preflight_snapshot
                    )
                ),
                repetitions=5,
                requested_count=10,
                counterbalance_seed=counterbalance_seed,
                hidden_prompt_texts=YM_PROPOSAL_FIELD_FREE_PROMPTS,
            )
            preflight_portfolio = preflight_envelope["selected_portfolio"]
            snapshot = bind_source_semantic_warrants(
                preflight_snapshot,
                _ym_semantic_source_warrants(
                    preflight_snapshot,
                    generated_portfolio=preflight_portfolio,
                ),
                authority_id="ym21-generated-candidate-source-claim-audit.v2",
            )
            high_risk_envelope = prepare_proposal_field_free_high_risk_envelope(
                charter=_charter(snapshot),
                literature_snapshot=snapshot,
                workspace=self.workspace,
                namespace=self.namespace,
                authored_incumbent_comparison_proposals=(
                    _authored_domain_template_incumbent_comparison_proposals(snapshot)
                ),
                repetitions=5,
                requested_count=10,
                counterbalance_seed=counterbalance_seed,
                hidden_prompt_texts=YM_PROPOSAL_FIELD_FREE_PROMPTS,
            )
            generated_candidate_binding = _assert_stable_generated_selection(
                preflight_envelope,
                high_risk_envelope,
                preflight_workspace=preflight_workspace,
                final_workspace=self.workspace,
                expected_namespace=self.namespace,
            )

        snapshot_path = "artifacts/00-frozen-live-literature-snapshot.json"
        _write_immutable_json(self.workspace / snapshot_path, snapshot)
        self.roles["literature_snapshot"] = snapshot_path

        theory_catalog = _ym_theory_catalog(snapshot)
        mapping_derivation = derive_claim_mappings(
            snapshot, theory_catalog=theory_catalog
        )
        mapping_routing_certificate = validate_source_routing_consumption(
            authority=capture_binding,
            sources=snapshot["sources"],
            stage="claim_mapping_derivation",
            theory_mappings=mapping_derivation["theory_mappings"],
            require_complete_mapping=True,
        )
        hypothesis_rebase = _derived_hypothesis_rebase(mapping_derivation)
        assimilation, assimilation_receipt, assimilation_path = self.dispatch(
            "frontier-literature-assimilator",
            "literature_assimilation",
            {
                "snapshot": snapshot,
                "frozen_provider_source_catalog": provider_source_catalog,
                "frozen_live_capture_binding": capture_binding,
                "theory_catalog": theory_catalog,
                "mapping_derivation": mapping_derivation,
                "hypotheses": hypothesis_rebase,
                "candidate_snapshot_ids": [snapshot["snapshot_id"]],
                "freshness_max_age_seconds": DEFAULT_LITERATURE_FRESHNESS_SECONDS,
                "freshness_evaluated_at": snapshot["search_completed_at"],
            },
        )
        self.roles["literature_assimilation"] = assimilation_path
        assimilation_routing_certificate = validate_source_routing_consumption(
            authority=capture_binding,
            sources=snapshot["sources"],
            stage="assimilation",
            theory_mappings=assimilation["theory_mappings"],
            require_complete_mapping=True,
        )

        self.source_routing_precommit = (
            build_source_routing_precommit_certificate(
                authority=capture_binding,
                snapshot=snapshot,
                assimilation=assimilation,
                target_id=TARGET_ID,
                run_id=RUN_ID,
                state_version=STATE_VERSION,
                assimilation_producer_receipt=assimilation_receipt,
            )
        )
        source_routing_path = "artifacts/01-source-routing-precommit.json"
        _write_immutable_json(
            self.workspace / source_routing_path,
            self.source_routing_precommit,
        )
        self.roles["source_routing_precommit"] = source_routing_path

        validate_source_routing_consumption(
            authority=capture_binding,
            sources=snapshot["sources"],
            stage="high_risk_investment_input",
            theory_mappings=assimilation["theory_mappings"],
            require_complete_mapping=True,
        )

        high_risk_envelope["assimilation_packet"] = copy.deepcopy(assimilation)
        portfolio, portfolio_receipt, portfolio_path = self.dispatch(
            "high-risk-hypothesis-forger",
            "hypothesis",
            high_risk_envelope,
            parameters={"requested_count": 10, "relevance_floor": 0.70},
        )
        self.roles["high_risk_portfolio"] = portfolio_path
        if portfolio != high_risk_envelope["selected_portfolio"]:
            raise YMCanonicalCycleError(
                "dispatched YM portfolio differs from the final recursively sealed selection"
            )
        _assert_generated_live_routing(
            portfolio=portfolio,
            theory_catalog=theory_catalog,
            mapping_derivation=mapping_derivation,
            hypothesis_rebase=hypothesis_rebase,
            assimilation=assimilation,
        )

        selected_seeds, literature_routing_trace = _literature_routed_seeds(
            portfolio,
            assimilation,
            routing_authority=capture_binding,
            routing_sources=snapshot["sources"],
        )
        literature_routing_trace = _full_literature_counterfactual_replays(
            snapshot=snapshot,
            assimilation=assimilation,
            portfolio=portfolio,
            baseline_trace=literature_routing_trace,
            theory_catalog=theory_catalog,
            hypotheses=hypothesis_rebase,
        )
        literature_routing_trace.pop("content_digest", None)
        literature_routing_trace["generated_candidate_binding"] = (
            generated_candidate_binding
        )
        literature_routing_trace["mapping_routing_certificate"] = (
            mapping_routing_certificate
        )
        literature_routing_trace["assimilation_routing_certificate"] = (
            assimilation_routing_certificate
        )
        literature_routing_trace["content_digest"] = canonical_digest(
            literature_routing_trace
        )
        _assert_generated_live_routing(
            portfolio=portfolio,
            theory_catalog=theory_catalog,
            mapping_derivation=mapping_derivation,
            hypothesis_rebase=hypothesis_rebase,
            assimilation=assimilation,
            routing_trace=literature_routing_trace,
        )
        dissent_seed = next(
            (row for row in reversed(selected_seeds) if row.get("is_wildcard")),
            selected_seeds[-1],
        )
        dissent_branch_id = dissent_seed["branch_id"]
        parallel, parallel_receipt, parallel_path = self.dispatch(
            "parallel-hypothesis-portfolio",
            "hypothesis",
            {
                "high_risk_portfolio": portfolio,
                "branch_seeds": selected_seeds,
                "dissent_branch_ids": [dissent_branch_id],
                "resource_budget": {
                    "wall_seconds": 20,
                    "max_workers": 4,
                    "cost_units": 20,
                    "storage_bytes": 500000,
                    "matched_budget_baseline_corner_coverage": 4,
                },
            },
        )
        self.roles["parallel_portfolio"] = parallel_path

        reflection_request = self.reflection_request(
            portfolio, parallel, snapshot, assimilation_path
        )
        conceptual_systems, reflection_round_template, conceptual_generation_trace = (
            _ym_conceptual_material(
                snapshot=snapshot,
                assimilation=assimilation,
                portfolio=portfolio,
                parallel=parallel,
            )
        )
        reflection_request["conceptual_generation_trace"] = conceptual_generation_trace
        reflection_request["literature_routing_trace"] = literature_routing_trace
        parent_reflection_rounds = reflection_round_template[:3]
        parent_conceptual_quality_evidence = build_conceptual_quality_evidence(
            systems=conceptual_systems,
            rounds=parent_reflection_rounds,
            snapshot=snapshot,
            proposal_receipt_ids=[
                portfolio_receipt["receipt_id"],
                parallel_receipt["receipt_id"],
            ],
            stage_id="parent",
        )
        preferred_id = parent_conceptual_quality_evidence["preferred_system_id"]
        parent_evaluation_receipt = parent_conceptual_quality_evidence[
            "evaluation_receipt"
        ]
        reflection_request.update(
            {
                "generation_mode": "operator_generated",
                "conceptual_systems": conceptual_systems,
                "reflection_rounds": parent_reflection_rounds,
                "preferred_system_id": preferred_id,
                "evaluation_receipt_ids": [
                    parent_evaluation_receipt["evaluation_id"]
                ],
                "independent_evaluation_evidence": [
                    parent_conceptual_quality_evidence
                ],
                "next_reflective_action": {
                    "kind": "formalize",
                    "question": (
                        "Can YM21-F01, F03, F05, and F07 be stated independently enough that the three F09 countermodels become constructible?"
                    ),
                    "expected_conceptual_change": (
                        "Replace the conjectural mediator with exact object, arrow, detector, distortion, and holonomy definitions or demote whichever component remains circular."
                    ),
                },
            }
        )
        programme_id = stable_identifier("programme", preferred_id, STATE_VERSION)
        reflection_request["support_probe"] = {
            "disposition": "commissioned",
            "theory_programme_id": programme_id,
            "theoretical_question_id": PROBE_QUESTION_ID,
            "conceptual_system_ids": [preferred_id],
            "theoretical_question": PROBE_QUESTION,
            "role": "symbolic_derivation",
            "why_theory_alone_is_currently_insufficient": (
                "The path-independence assumption must survive an exact counterexample search before it informs YM21-F05/F07; this cannot test whether Yang--Mills arrows or estimates exist."
            ),
            "possible_theory_updates": [
                "Retain path equality only if independently declared path products agree exactly.",
                "If they differ, preserve transport holonomy as a separate obstruction and revise any inference from local multiplicativity to global descent."
            ],
            "receipt_ids": ["ym21-commission-request-toy-descent"],
            "reflective_assimilation_event_ids": [],
        }
        parent_packet, parent_receipt, parent_path = self.dispatch(
            "reflective-conceptual-discovery",
            "theory",
            reflection_request,
            parameters={"stage": "full"},
        )

        experiment_branch = selected_seeds[0]["branch_id"]
        registered_claim = _registered_theory_claim_from_parent(
            parent_packet,
            expected_programme_id=programme_id,
            expected_conceptual_system_ids=[preferred_id],
        )
        triage_request = {
            "target_id": TARGET_ID,
            "theory_programme_id": registered_claim["theory_programme_id"],
            "source_theory_programme_digest": registered_claim[
                "source_theory_programme_digest"
            ],
            "source_reflection_packet_digest": registered_claim[
                "source_reflection_packet_digest"
            ],
            "conceptual_system_ids": list(registered_claim["conceptual_system_ids"]),
            "registered_theory_claims": [registered_claim],
            "theoretical_question_id": registered_claim["claim_id"],
            "question": registered_claim["statement"],
            "programme_maturity": "mature",
            "probe_role": "discriminator",
            "decision_effect": {
                "if_supported": "retain equality for this finite path pair as a notation-level maturation aid only",
                "if_not_supported": "retain a nonzero toy holonomy obstruction and revise F05/F07 so local composition never implies path independence",
            },
            "expected_conceptual_change": (
                "Decide whether local multiplicative factors suffice for path independence in this finite toy; do not update any Yang--Mills premise or truth status."
            ),
            "theory_generated_justification": (
                "Rounds 1 and 3 isolated local scale transport from global descent; the proposed adversarial round therefore commissions an exact unequal-path search."
            ),
            "candidate_methods": ["exact"],
            "state_version": STATE_VERSION,
        }
        experiment_request = {
            "run_id": RUN_ID,
            "branch_id": experiment_branch,
            "adapter": "exact",
            "model": {
                "operation": "equality",
                "left": "2/3 * 3/4",
                "right": "5/8",
            },
            "preregistration": {
                "hypothesis": "two locally composable toy regulator paths have equal total distortion, as path-independent descent would require",
                "decision_rule": {"comparator": "==", "threshold": 1},
                "stopping_rule": "stop after the declared exact rational evaluation",
                "analysis_plan": "normalize both path products as exact rationals, compare them, and preserve any nonzero difference as a toy holonomy counterexample",
                "registered_at": REQUESTED_AT,
            },
            "controls": [
                {
                    "control_id": "ym21-control-rational-domain",
                    "variable": "arithmetic_domain",
                    "value": "rational",
                    "role": "held_fixed",
                }
            ],
            "seed_policy": {"stochastic": False, "policy": "not_applicable"},
            "resource_budget": _budget(),
            "transfer_boundary": (
                "The certificate concerns one rational toy path comparison only. It is not evidence for lattice coercivity, "
                "continuum construction, regulator universality, OS reconstruction, or a Yang-Mills mass gap."
            ),
            "theory_effect_contract": {
                "tested_claim_id": registered_claim["claim_id"],
                "tested_claim_kind": registered_claim["claim_kind"],
                "target_relation": registered_claim["target_relation"],
                "if_supported": "record_scoped_consistency_only",
                "if_falsified": "record_scoped_counterexample_only",
                "theory_identity_locked": True,
                "automatic_theory_selection": False,
                "automatic_proof": False,
            },
            "created_at": REQUESTED_AT,
        }
        precommitted_triage = triage_probe(triage_request)
        if precommitted_triage["decision"] != "commission":
            raise YMCanonicalCycleError("sealed parent support question did not commission its exact probe")
        precommitted_spec = compile_experiment_spec(
            precommitted_triage, experiment_request
        )
        experiment_spec_path = "artifacts/05-precommitted-experiment-spec.json"
        _write_immutable_json(self.workspace / experiment_spec_path, precommitted_spec)
        self.roles["experiment_spec"] = experiment_spec_path
        experiment_envelope = {
            "triage_request": triage_request,
            "experiment_request": experiment_request,
            "experiment_spec": precommitted_spec,
        }
        experiment_receipt, experiment_operator_receipt, experiment_path = self.dispatch(
            "dynamic-symbolic-simulation-experimenter",
            "support_probe",
            experiment_envelope,
            branch_id=experiment_branch,
            parameters={"theory_commissioned": True},
        )
        self.roles["experiment_receipt"] = experiment_path

        synthesis_conceptual_systems, reflection_rounds = _assimilate_probe_round(
            conceptual_systems,
            reflection_round_template,
            experiment_receipt,
            selected_system_id=preferred_id,
        )
        synthesis_conceptual_quality_evidence = build_conceptual_quality_evidence(
            systems=synthesis_conceptual_systems,
            rounds=reflection_rounds,
            snapshot=snapshot,
            proposal_receipt_ids=[
                portfolio_receipt["receipt_id"],
                parallel_receipt["receipt_id"],
                experiment_operator_receipt["receipt_id"],
            ],
            stage_id="synthesis",
            previous_evidence=parent_conceptual_quality_evidence,
        )
        if synthesis_conceptual_quality_evidence["preferred_system_id"] != preferred_id:
            raise YMCanonicalCycleError("probe assimilation changed the blind selected system rather than maturing it")

        reflection_request["support_probe"] = {
            **reflection_request["support_probe"],
            "disposition": "assimilated",
            "receipt_ids": [experiment_receipt["receipt_id"]],
            "reflective_assimilation_event_ids": [
                "ym21-reflection-assimilation-toy-descent"
            ],
        }
        synthesis_envelope = {
            **reflection_request,
            "conceptual_systems": synthesis_conceptual_systems,
            "reflection_rounds": reflection_rounds,
            "evaluation_receipt_ids": [
                synthesis_conceptual_quality_evidence["evaluation_receipt"][
                    "evaluation_id"
                ]
            ],
            "independent_evaluation_evidence": [
                synthesis_conceptual_quality_evidence
            ],
            "prior_reflective_packet": parent_packet,
            "parallel_portfolio": parallel,
            "experiment_result": experiment_receipt,
        }
        synthesis_packet, synthesis_receipt, synthesis_path = self.dispatch(
            "reflective-theory-synthesizer",
            "theory",
            synthesis_envelope,
            parameters={"stage": "reflect"},
        )
        self.roles["reflective_packets"] = [parent_path, synthesis_path]

        operator_ids = {row["operator"]["operator_id"] for row in self.receipts}
        if operator_ids != SIX_OPERATORS or len(self.receipts) != 6:
            raise YMCanonicalCycleError(
                f"canonical wave did not execute the exact six registered operators: {sorted(operator_ids)}"
            )
        result = run_canonical_discovery_cycle(
            workspace=self.workspace,
            state_root=self.state_root,
            target_id=TARGET_ID,
            run_id=RUN_ID,
            state_version=STATE_VERSION,
            operator_requests=self.requests,
            operator_receipts=self.receipts,
            artifact_roles=self.roles,
            evaluator_identity="ym21-independent-canonical-evaluator",
            evaluator_version="ym21-canonical-evaluator/1.0.0",
            idempotency_key="ym21-canonical-parent-20260721",
        )
        _write_immutable_json(self.output_root / "canonical_cycle_result.json", result)
        _publish_committed_cycle(self.output_root)
        if self.output_root == DEFAULT_OUTPUT_ROOT.resolve():
            bind_registered_canonical_runtime()
        return result


def build_acceptance_report(
    *,
    result: Mapping[str, Any],
    requests: list[dict[str, Any]],
    receipts: list[dict[str, Any]],
    snapshot: Mapping[str, Any],
    assimilation: Mapping[str, Any],
    portfolio: Mapping[str, Any],
    parallel: Mapping[str, Any],
    experiment_receipt: Mapping[str, Any],
    capture_binding: Mapping[str, Any],
    literature_routing_trace: Mapping[str, Any],
    reflective_packets: list[dict[str, Any]],
    conceptual_quality_evidence: list[dict[str, Any]],
) -> dict[str, Any]:
    operator_ids = {row["operator"]["operator_id"] for row in receipts}
    feedback_ids = {row["producer_operator_id"] for row in result["feedback_edges"]}
    events = {row["event_id"]: row for row in result["events"]}
    reachability = all(
        edge["consumer_event_id"] in events
        and edge["producer_receipt_id"] in events[edge["consumer_event_id"]]["source_receipt_ids"]
        and edge["committed_state_generation"] == result["committed_state_version"]
        for edge in result["feedback_edges"]
    )
    direct_mappings = [
        row for row in assimilation["theory_mappings"] if row["source_id"] == DIRECT_CHALLENGER_ID
    ]
    acceptance_routing_certificate = validate_source_routing_consumption(
        authority=capture_binding,
        sources=snapshot["sources"],
        stage="acceptance",
        theory_mappings=assimilation["theory_mappings"],
        require_complete_mapping=True,
    )
    selected_hypothesis_ids = {
        row["hypothesis_id"] for row in parallel["branch_requests"]
    }
    evidence_receipts = [
        evidence["evaluation_receipt"] for evidence in conceptual_quality_evidence
    ]
    evidence_ids = [receipt["evaluation_id"] for receipt in evidence_receipts]
    selected_system_ids = {
        str(evidence["preferred_system_id"]) for evidence in conceptual_quality_evidence
    }
    preferred_id = next(iter(selected_system_ids)) if len(selected_system_ids) == 1 else ""
    preferred_systems = [
        next(
            item
            for item in packet["conceptual_systems"]
            if item["system_id"] == preferred_id
        )
        for packet in reflective_packets
    ]
    material_round_counts = [
        sum(
            row["result"] in {"mutated", "synthesized", "demoted"}
            and bool(
                row["mutation_or_synthesis"][
                    "changed_primitives_relations_or_explanation"
                ]
            )
            for row in packet["reflection_rounds"]
        )
        for packet in reflective_packets
    ]
    conceptual_fields = (
        "conceptual_systems",
        "reflection_rounds",
        "provisional_synthesis",
        "understanding_delta",
        "theoretical_programme",
        "stage_gates",
        "generation_mode",
        "evaluation_receipt_ids",
        "independent_evaluation_evidence",
    )
    conceptual_transition_digests = [
        canonical_digest({field: packet[field] for field in conceptual_fields})
        for packet in reflective_packets
    ]
    synthesizer_materially_extends_reflection = (
        len(conceptual_transition_digests) == 2
        and len(set(conceptual_transition_digests)) == 2
        and len(reflective_packets[0]["reflection_rounds"]) == 3
        and len(reflective_packets[1]["reflection_rounds"]) == 4
        and reflective_packets[1]["reflection_rounds"][:3]
        == reflective_packets[0]["reflection_rounds"]
        and reflective_packets[1]["reflection_rounds"][-1]["round_id"]
        == "ym21-reflection-04-adversarial-holonomy"
    )
    full_replays = list(literature_routing_trace.get("full_pipeline_replays", []))
    replay_operations = {str(row.get("operation")) for row in full_replays}
    generic_replay = literature_routing_trace.get(
        "literature_counterfactual_replay", {}
    )
    full_replay_acceptance = (
        literature_routing_trace.get("counterfactual_replay_mode")
        == "derived_claim_mapping_full_pipeline_local_only"
        and literature_routing_trace.get("all_scenarios_reexecuted") is True
        and len(full_replays) == len(snapshot["sources"]) + 4
        and replay_operations
        == {
            "delete_source",
            "no_literature",
            "supersede_source",
            "contradict_source",
            "coverage_only_change",
        }
        and bool(literature_routing_trace.get("programme_change_scenarios"))
        and generic_replay.get("baseline", {}).get("assimilation") == assimilation
        and generic_replay.get("null_effect_world_ids") == ["coverage-only-null"]
        and all(
            row.get("route", {}).get("assimilation_digest")
            == canonical_digest(
                next(
                    item["assimilation"]
                    for item in generic_replay.get("world_results", [])
                    if item["world_id"] == row["world_id"]
                )
            )
            and row.get("branch_projection", {}).get("programme_digest")
            == canonical_digest(
                row.get("branch_projection", {}).get("programme_projection", {})
            )
            for row in full_replays
        )
    )
    semantic_layer = generic_replay.get("baseline", {}).get(
        "mapping_derivation", {}
    ).get("semantic_claim_layer", {})
    semantic_replay_acceptance = (
        semantic_layer.get("epistemic_nulls", {}).get("source_truth_authorized")
        is False
        and semantic_layer.get("epistemic_nulls", {}).get(
            "semantic_entailment_authorized"
        )
        is False
        and semantic_layer.get("coverage_audit", {}).get(
            "snapshot_claim_enumeration_complete"
        )
        is True
        and semantic_layer.get("coverage_audit", {}).get(
            "explicit_warrant_claim_count", 0
        )
        > 0
        and all(
            row.get("mapping_derivation", {}).get("semantic_claim_layer_digest")
            == row.get("mapping_derivation", {}).get("semantic_claim_layer", {}).get(
                "content_digest"
            )
            for row in generic_replay.get("world_results", [])
        )
        and next(
            row
            for row in generic_replay.get("world_results", [])
            if row["world_id"] == "coverage-only-null"
        )["effects"]["semantic_coverage_audit_changed"]
        is True
        and next(
            row
            for row in generic_replay.get("world_results", [])
            if row["world_id"] == "coverage-only-null"
        )["effects"]["semantic_relation_decisions_changed"]
        is False
    )
    checks = {
        "six_registered_operator_receipts": len(receipts) == 6 and operator_ids == SIX_OPERATORS,
        "all_receipts_succeeded_with_independent_validators": all(
            row["status"] == "succeeded"
            and row["validator_receipts"]
            and all(item["status"] == "passed" for item in row["validator_receipts"])
            for row in receipts
        ),
        "frontier_assimilator_actually_executed": any(
            row["operator"]["operator_id"] == "frontier-literature-assimilator"
            for row in receipts
        ),
        "six_nonrenewing_lanes_from_bound_live_acquisition": (
            snapshot["provenance_mode"] == "frozen_response_replay"
            and len(snapshot["lane_receipts"]) == 6
            and all(
                row["execution_mode"] == "frozen_response_replay"
                and row["status"] == "completed"
                for row in snapshot["lane_receipts"]
            )
            and snapshot["original_acquisition_snapshot"]["provenance_mode"] == "live"
            and capture_binding["consumption_mode"] == "frozen_response_replay"
        ),
        "raw_capture_bound_without_exhaustiveness_claim": (
            capture_binding["raw_result_count"] >= 27
            and len(capture_binding["excluded_raw_result_ids"]) >= 6
        ),
        "claim_specific_2606_audit": (
            assimilation.get("mapping_provenance", {}).get("mode")
            == "deterministic_claim_derivation"
            and len(direct_mappings)
            == len(
                {
                    " ".join(str(claim).split()).casefold()
                    for source in snapshot["sources"]
                    if source["source_id"] == DIRECT_CHALLENGER_ID
                    for claim in source["claims"]
                }
            )
            and len(
                generic_replay.get("baseline", {})
                .get("mapping_derivation", {})
                .get("mapping_receipts", [])
            )
            == len(assimilation["theory_mappings"])
        ),
        "version_lineage_routing_is_enforced": (
            acceptance_routing_certificate["source_routing_eligibility"].get(
                "zenodo-18837540"
            )
            == "blocked_positive_support"
            and acceptance_routing_certificate["source_routing_eligibility"].get(
                "zenodo-19614728"
            )
            == "blocked_positive_support"
            and acceptance_routing_certificate["source_routing_eligibility"].get(
                "zenodo-21479499"
            )
            == "unverified_audit_only"
            and all(
                literature_routing_trace.get("source_routing_certificate", {}).get(
                    field
                )
                == acceptance_routing_certificate[field]
                for field in (
                    "source_routing_eligibility",
                    "source_ids",
                    "mapping_source_ids",
                    "require_complete_mapping",
                    "checked_rows",
                    "policy_digest",
                )
            )
            and literature_routing_trace.get("mapping_routing_certificate", {}).get(
                "stage"
            )
            == "claim_mapping_derivation"
            and literature_routing_trace.get(
                "assimilation_routing_certificate", {}
            ).get("stage")
            == "assimilation"
        ),
        "latest_literature_changed_parallel_priorities": (
            set(literature_routing_trace["selected_hypothesis_ids"])
            == selected_hypothesis_ids
            and literature_routing_trace["source_removal_changes_route"] is True
            and bool(literature_routing_trace.get("selection_change_scenarios"))
        ),
        "latest_literature_full_pipeline_counterfactual_replays": full_replay_acceptance,
        "source_semantic_claim_layer_causally_replayed": semantic_replay_acceptance,
        "parallel_branches_isolated_and_conflict_preserving": (
            len(parallel["branch_requests"]) == 4
            and len(parallel["branch_results"]) == 4
            and bool(parallel["merge_proposal"]["retained_dissent_ids"])
        ),
        "operator_generated_reflection_only": all(
            packet.get("generation_mode") == "operator_generated"
            for packet in reflective_packets
        )
        and result.get("conceptual_authority", {}).get("generation_modes")
        == ["operator_generated"]
        and result.get("conceptual_authority", {}).get("fallback_disposition")
        == "not_applicable",
        "spectral_descent_mediator_is_domain_specific": all(
            {
                "spectral-scale production witness",
                "observable-completeness witness",
                "descent-stability witness",
                "spectral-descent transport groupoid",
                "transport holonomy defect",
            }.issubset(set(system["primitives"]))
            and {
                "produces_scale_on",
                "detects_nonvacuum_sector",
                "transports_observable_semantics",
                "satisfies_descent_cocycle",
                "measures_holonomy_defect",
            }.issubset(set(system["relations_operations_and_dynamics"]))
            for system in preferred_systems
        ),
        "three_or_more_material_reflection_rounds": all(
            count >= 3 for count in material_round_counts
        )
        and all(
            all(row["strongest_objections"] for row in packet["reflection_rounds"])
            for packet in reflective_packets
        ),
        "G2_G4_pass_from_bound_internal_correlated_evidence": (
            all(
                evidence["gate_findings"]["G2_philosophical_depth"]["status"]
                == "pass"
                and evidence["gate_findings"]["G4_understanding_gain"]["status"]
                == "pass"
                and receipt["creative_worth_decision"] == "prefer"
                and receipt["promotion_decision"] == "not_requested"
                for evidence, receipt in zip(
                    conceptual_quality_evidence, evidence_receipts, strict=True
                )
            )
            and all(
                packet["stage_gates"]["G2_philosophical_depth"] == "pass"
                and packet["stage_gates"]["G4_understanding_gain"] == "pass"
                and packet["evaluation_receipt_ids"] == [evidence_id]
                and packet["independent_evaluation_evidence"]
                == [evidence]
                for packet, evidence, evidence_id in zip(
                    reflective_packets,
                    conceptual_quality_evidence,
                    evidence_ids,
                    strict=True,
                )
            )
        ),
        "blind_plural_content_adjudication_and_full_synthesis_gates": (
            len(selected_system_ids) == 1
            and all(len(evidence["judge_reports"]) == 3 for evidence in conceptual_quality_evidence)
            and conceptual_quality_evidence[0]["evaluation_role"] == "diagnostic"
            and conceptual_quality_evidence[1]["evaluation_role"] == "conceptual_gate"
            and all(
                finding["status"] == "pass"
                for finding in conceptual_quality_evidence[1]["gate_findings"].values()
            )
            and conceptual_quality_evidence[1]["stage_comparison"]["material"] is True
        ),
        "synthesizer_materially_extends_reflection": synthesizer_materially_extends_reflection,
        "experiment_remains_theory_subordinate": (
            experiment_receipt["transfer_boundary"].startswith("The certificate concerns one rational toy")
            and experiment_receipt["status"] == "counterexample"
            and experiment_receipt["epistemic_outcome"] == "falsifies_claim"
            and result["experiment_assimilation"]["theory_selected"] is False
            and result["experiment_assimilation"]["proof_authorized"] is False
        ),
        "single_atomic_commit": result["committed_state_version"] == 1
        and result["parallel_outcome"]["canonical_cas_commits"] == 1,
        "six_feedback_edges_reachable": len(result["feedback_edges"]) == 6
        and feedback_ids == SIX_OPERATORS
        and reachability,
        "operator_evidence_sealed": set(result["operator_evidence"]["successful_receipt_ids"])
        == {row["receipt_id"] for row in receipts},
        "active_current_literature_acceptance": result["literature_basis"]["mode"]
        == "active_current",
        "no_truth_promotion": all(
            row["promotion_decision"] == "not_requested"
            for row in result["evaluation_receipts"]
        ),
    }
    return {
        "schema_version": 1,
        "acceptance_id": "ym21-canonical-parent-cycle-acceptance-20260721",
        "target_id": TARGET_ID,
        "run_id": RUN_ID,
        "status": "passed" if all(checks.values()) else "failed",
        "checks": checks,
        "operator_ids": sorted(operator_ids),
        "receipt_ids": [row["receipt_id"] for row in receipts],
        "snapshot_id": snapshot["snapshot_id"],
        "assimilation_packet_id": assimilation["packet_id"],
        "portfolio_id": portfolio["portfolio_id"],
        "parallel_portfolio_id": parallel["portfolio_id"],
        "preferred_system_id": preferred_id,
        "conceptual_quality_evidence_ids": [
            evidence["evidence_id"] for evidence in conceptual_quality_evidence
        ],
        "conceptual_quality_evaluation_ids": evidence_ids,
        "conceptual_transition_digests": conceptual_transition_digests,
        "material_reflection_round_counts": material_round_counts,
        "commit_id": result["commit_id"],
        "manifest_digest": result["manifest_digest"],
        "state_digest": result["state_digest"],
        "authority_boundary": (
            "Acceptance proves registered execution, artifact reachability, and canonical commit integrity. "
            "It does not validate source claims, establish novelty, or prove Yang-Mills existence or a mass gap."
        ),
    }


def _acceptance_markdown(
    acceptance: Mapping[str, Any], result: Mapping[str, Any]
) -> bytes:
    return (
        "# YM21 canonical parent-cycle acceptance\n\n"
        f"- Status: `{acceptance['status']}`\n"
        f"- Six registered receipts: `{acceptance['checks']['six_registered_operator_receipts']}`\n"
        f"- Commit: `{result['commit_id']}` at state version `{result['committed_state_version']}`\n"
        f"- Reachable feedback edges: `{len(result['feedback_edges'])}`\n"
        f"- Literature mode: `{result['literature_basis']['mode']}`\n"
        f"- Source-semantic claim replay: `{acceptance['checks']['source_semantic_claim_layer_causally_replayed']}`\n"
        f"- Operator-generated reflection: `{acceptance['checks']['operator_generated_reflection_only']}`\n"
        f"- Internal-correlated G2/G4 evidence: `{acceptance['checks']['G2_G4_pass_from_bound_internal_correlated_evidence']}`\n"
        f"- Experiment authority: `{acceptance['checks']['experiment_remains_theory_subordinate']}`\n"
    ).encode("utf-8")


def _refinement_history_from_committed_material(
    evidence_rows: Sequence[Mapping[str, Any]], experiment_receipt: Mapping[str, Any]
) -> dict[str, Any]:
    if len(evidence_rows) != 2:
        raise YMCanonicalCycleError("publication requires exact parent/synthesis evidence")
    parent, synthesis = evidence_rows
    return {
        "schema_version": "2.0.0",
        "refinement_id": "ym21-blind-conceptual-refinement-20260721",
        "target_id": TARGET_ID,
        "run_id": RUN_ID,
        "parent_evidence_id": parent["evidence_id"],
        "synthesis_evidence_id": synthesis["evidence_id"],
        "probe_receipt_id": experiment_receipt["receipt_id"],
        "probe_outcome": experiment_receipt["epistemic_outcome"],
        "stage_comparison": synthesis["stage_comparison"],
        "retained_dissent": True,
        "change": (
            "The counterexample adds an objection-bearing round, rejects local-composition-to-path-independence, "
            "and raises minimum reflective resilience without changing any truth status."
        ),
        "authority_boundary": (
            "The refinement establishes internal conceptual maturation only; it has no theorem, "
            "source-validation, or external-efficacy authority."
        ),
    }


def _build_publication_payloads(material: Mapping[str, Any]) -> dict[str, bytes]:
    """Derive every successful publication byte from a replayed committed core."""

    evidence_rows = list(material["conceptual_quality_evidence"])
    result = material["result"]
    acceptance = build_acceptance_report(
        result=result,
        requests=list(material["requests"]),
        receipts=list(material["receipts"]),
        snapshot=material["snapshot"],
        assimilation=material["assimilation"],
        portfolio=material["portfolio"],
        parallel=material["parallel"],
        experiment_receipt=material["experiment_receipt"],
        capture_binding=material["capture_binding"],
        literature_routing_trace=material["literature_routing_trace"],
        reflective_packets=list(material["reflective_packets"]),
        conceptual_quality_evidence=evidence_rows,
    )
    if acceptance["status"] != "passed" or not all(acceptance["checks"].values()):
        raise YMCanonicalCycleError("committed material did not rebuild a passing acceptance report")
    refinement = _refinement_history_from_committed_material(
        evidence_rows, material["experiment_receipt"]
    )
    json_payloads: dict[str, Any] = {
        "canonical_cycle_result.json": result,
        "operator_requests.json": {"requests": list(material["requests"])},
        "operator_receipts.json": {"receipts": list(material["receipts"])},
        "artifact_roles.json": material["artifact_roles"],
        "frozen_provider_source_catalog.json": material["source_catalog"],
        "frozen_live_capture_binding.json": material["capture_binding"],
        "conceptual_generation_trace.json": material["conceptual_generation_trace"],
        "literature_routing_counterfactuals.json": material["literature_routing_trace"],
        PARENT_CONCEPTUAL_QUALITY_EVIDENCE_NAME: evidence_rows[0],
        SYNTHESIS_CONCEPTUAL_QUALITY_EVIDENCE_NAME: evidence_rows[1],
        CONCEPTUAL_QUALITY_REFINEMENT_HISTORY_NAME: refinement,
        "acceptance_report.json": acceptance,
    }
    payloads = {
        name: canonical_json(payload) + b"\n"
        for name, payload in json_payloads.items()
    }
    payloads["acceptance_report.md"] = _acceptance_markdown(acceptance, result)
    if set(payloads) != set(PUBLICATION_FILE_ROLES):
        raise YMCanonicalCycleError("publication payload set drifted from its closed role registry")
    return payloads


def _publication_descriptors(output_root: Path) -> list[dict[str, Any]]:
    descriptors: list[dict[str, Any]] = []
    for relative in sorted(PUBLICATION_FILE_ROLES):
        path = output_root / relative
        if path.is_symlink() or not path.is_file():
            raise YMCanonicalCycleError(f"publication file is absent or unsafe: {relative}")
        descriptors.append(
            {
                "path": relative,
                "sha256": file_digest(path),
                "size_bytes": path.stat().st_size,
                "role": PUBLICATION_FILE_ROLES[relative],
            }
        )
    return descriptors


def _write_publication_failure(
    output_root: Path, *, failed_stage: str, error: BaseException
) -> Path:
    result_path = output_root / "canonical_cycle_result.json"
    result = load_json(result_path)
    if not isinstance(result, Mapping):
        raise YMCanonicalCycleError("cannot bind post-commit failure to a result object")
    result_digest = file_digest(result_path)
    error_message = str(error).strip() or type(error).__name__
    error_message = error_message[:2000]
    failure_id = stable_identifier(
        "ympubfail",
        result["cycle_id"],
        result["commit_id"],
        failed_stage,
        type(error).__name__,
        error_message,
        result_digest,
    )
    payload: dict[str, Any] = {
        "schema_version": "1.0.0",
        "failure_id": failure_id,
        "status": "post_commit_publication_failed",
        "target_id": TARGET_ID,
        "run_id": RUN_ID,
        "cycle_id": result["cycle_id"],
        "commit_id": result["commit_id"],
        "failed_stage": failed_stage,
        "error_class": type(error).__name__,
        "error_message": error_message,
        "canonical_result_digest": result_digest,
        "publication_status_written": False,
        "retry_disposition": "resume_same_committed_core",
        "epistemic_effect": "none_operational_outcome_only",
    }
    payload["content_digest"] = canonical_digest(payload)
    validate_payload(payload, "ym_canonical_publication_failure.schema.json")
    return _write_immutable_json(
        output_root / PUBLICATION_FAILURE_DIR / f"{failure_id}.json", payload
    )


@contextmanager
def _publication_lock(output_root: Path):
    """Serialize incomplete-root recovery before rechecking the status marker."""

    output_root.mkdir(parents=True, exist_ok=True)
    lock_path = output_root / ".publication.lock"
    if lock_path.is_symlink():
        raise YMCanonicalCycleError("publication lock cannot be a symlink")
    with lock_path.open("a+b") as lock_stream:
        fcntl.flock(lock_stream.fileno(), fcntl.LOCK_EX)
        try:
            yield
        finally:
            fcntl.flock(lock_stream.fileno(), fcntl.LOCK_UN)


def _publish_committed_cycle(output_root: Path) -> dict[str, Any]:
    """Resume publication from one verified commit and write success status last."""

    output_root = output_root.resolve()
    status_path = output_root / PUBLICATION_STATUS_NAME
    with _publication_lock(output_root):
        stage = "core_validation"
        try:
            from validate_ym_canonical_parent_cycle_20260721 import (
                load_committed_publication_material,
                validate as validate_published_cycle,
            )

            if os.path.lexists(status_path):
                return validate_published_cycle(output_root, require_publication=True)
            material = load_committed_publication_material(output_root)
            stage = "report_build"
            payloads = _build_publication_payloads(material)
            stage = "report_write"
            for relative in sorted(payloads):
                _write_immutable_bytes(output_root / relative, payloads[relative])
            stage = "status_write"
            result = material["result"]
            core_validation = material["core_validation"]
            descriptors = _publication_descriptors(output_root)
            descriptor_digest = canonical_digest(descriptors)
            status: dict[str, Any] = {
                "schema_version": "1.0.0",
                "publication_id": stable_identifier(
                    "ympub",
                    TARGET_ID,
                    RUN_ID,
                    result["cycle_id"],
                    result["commit_id"],
                    result["manifest_digest"],
                    result["state_digest"],
                    core_validation["authorization_basis_digest"],
                    descriptor_digest,
                ),
                "status": "complete",
                "target_id": TARGET_ID,
                "run_id": RUN_ID,
                "cycle_id": result["cycle_id"],
                "commit_id": result["commit_id"],
                "manifest_digest": result["manifest_digest"],
                "state_digest": result["state_digest"],
                "core_validation_authorization_basis_digest": core_validation[
                    "authorization_basis_digest"
                ],
                "core_validation_present_decision_digest": core_validation[
                    "present_investment_decision_digest"
                ],
                "files": descriptors,
                "written_atomically_last": True,
                "authority_boundary": (
                    "Complete means the exact committed YM conceptual cycle was replayed and its derivative "
                    "reports were published atomically. It grants no theorem, source-validation, novelty, "
                    "external-efficacy, continuum-construction, or mass-gap authority."
                ),
            }
            status["content_digest"] = canonical_digest(status)
            validate_payload(status, "ym_canonical_publication_status.schema.json")
            _write_immutable_json(status_path, status)
            stage = "full_validation"
            return validate_published_cycle(output_root, require_publication=True)
        except Exception as exc:
            if not os.path.lexists(status_path) and (
                output_root / "canonical_cycle_result.json"
            ).is_file():
                _write_publication_failure(output_root, failed_stage=stage, error=exc)
            raise


def resume_or_validate_publication(output_root: Path) -> dict[str, Any]:
    """Validate a complete publication or resume reports from its existing commit."""

    output_root = output_root.resolve()
    had_status = os.path.lexists(output_root / PUBLICATION_STATUS_NAME)
    validation = _publish_committed_cycle(output_root)
    return {
        "status": "validated_existing" if had_status else "resumed_publication",
        "validation": validation,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-root", type=Path, default=DEFAULT_OUTPUT_ROOT)
    args = parser.parse_args()
    output_root = args.output_root.resolve()
    result_path = output_root / "canonical_cycle_result.json"
    if result_path.exists():
        try:
            outcome = resume_or_validate_publication(output_root)
            validation = outcome["validation"]
            result = load_json(result_path)
        except Exception as exc:
            print(
                "ERROR: existing YM canonical root could neither validate nor resume from its exact commit; "
                "preserve conflicting evidence and choose a new versioned --output-root only if repair is impossible: "
                f"{type(exc).__name__}: {exc}",
                file=sys.stderr,
            )
            return 1
        if output_root == DEFAULT_OUTPUT_ROOT.resolve():
            bind_registered_canonical_runtime()
        print(
            json.dumps(
                {
                    "status": outcome["status"],
                    "result": str(result_path),
                    "commit_id": result["commit_id"],
                    "committed_state_version": result["committed_state_version"],
                    "authorization_digest": validation["authorization_digest"],
                },
                indent=2,
                sort_keys=True,
            )
        )
        return 0
    state_pointer = (
        output_root
        / "state"
        / "targets"
        / TARGET_ID
        / "runs"
        / RUN_ID
        / "state-pointer.json"
    )
    if os.path.lexists(state_pointer):
        print(
            "ERROR: committed YM state exists without canonical_cycle_result.json; "
            "fail closed rather than dispatching a second scientific run",
            file=sys.stderr,
        )
        return 1
    try:
        result = CycleExecution(output_root).run()
    except Exception as exc:
        print(f"ERROR: {type(exc).__name__}: {exc}", file=sys.stderr)
        return 1
    print(
        json.dumps(
            {
                "status": "completed",
                "result": str(result_path),
                "commit_id": result["commit_id"],
                "committed_state_version": result["committed_state_version"],
                "operator_receipts": 6,
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
