# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
# 
# SPDX-License-Identifier: MIT

"""Shared utilities for evaluating proof hypotheses against KB artifacts.

This module centralizes the hypothesis triage logic used by:
- single-pass evaluation (`kb-hypothesis-evaluator`),
- iterative refutation/review loops (`kb-hypothesis-refutation-loop`).

Design principle:
- compute support/refute scores from explicit signals,
- adjust those scores with optional evidence + coherence signals,
- classify with threshold/margin policy into auditable verdicts.
"""

from __future__ import annotations

import datetime as dt
import logging
import re
from collections import Counter
from pathlib import Path
from typing import Any

_log = logging.getLogger(__name__)

import yaml

STATEMENT_BLOCK_PATTERN = re.compile(r"```yaml\n(.*?)\n```", re.DOTALL)
TOKEN_PATTERN = re.compile(r"[A-Za-z0-9_]+")
LATEX_COMMAND_PATTERN = re.compile(r"\\([A-Za-z]+)")
LATEX_SYMBOL_PATTERN = re.compile(r"(?<![A-Za-z])([A-Za-z](?:_[A-Za-z0-9]+)?)")

STOPWORDS = {
    "a",
    "an",
    "and",
    "are",
    "as",
    "at",
    "be",
    "by",
    "for",
    "from",
    "if",
    "in",
    "into",
    "is",
    "it",
    "of",
    "on",
    "or",
    "that",
    "the",
    "then",
    "there",
    "this",
    "to",
    "under",
    "will",
    "with",
}

NEGATION_MARKERS = {
    "neq",
    "not",
    "notsubseteq",
    "notin",
    "cannot",
    "impossible",
    "non",
    "no",
}

CONCEPTUAL_HYPOTHESIS_KINDS = {
    "definition-introduction",
    "representation-shift",
    "intermediate-invariant",
    "barrier-escape-principle",
    "analogy-transfer",
    "normal-form-reduction",
}


def _clamp01(value: float) -> float:
    """
    Relevance: Operates within the shared utilities layer.
    Concept: Internal helper implementing one deterministic step of this stage.
    Contribution: Contributes a deterministic transformation that supports end-to-end reasoning reproducibility.
    """

    return max(0.0, min(1.0, value))


def _safe_float(value: Any, default: float = 0.0) -> float:
    """
    Relevance: Operates within the shared utilities layer.
    Concept: Defensive conversion/parsing to keep scoring and reporting robust.
    Contribution: Reduces runtime ambiguity and prevents malformed artifacts from destabilizing the workflow.
    """

    try:
        return float(value)
    except (TypeError, ValueError):
        _log.warning("_safe_float: could not convert %r to float; using default %s", value, default)
        return default


def _as_list(value: Any) -> list[Any]:
    """
    Relevance: Operates within the shared utilities layer.
    Concept: Internal helper implementing one deterministic step of this stage.
    Contribution: Contributes a deterministic transformation that supports end-to-end reasoning reproducibility.
    """

    if isinstance(value, list):
        return value
    if value is None:
        return []
    return [value]


def _tokenize(text: str) -> set[str]:
    """
    Relevance: Operates within the shared utilities layer.
    Concept: Lightweight semantic feature computation for graph reasoning heuristics.
    Contribution: Contributes a deterministic transformation that supports end-to-end reasoning reproducibility.
    """

    tokens: set[str] = set()
    for match in TOKEN_PATTERN.findall(text.lower()):
        tok = match.strip("_")
        if len(tok) <= 1:
            continue
        if tok in STOPWORDS:
            continue
        tokens.add(tok)
    return tokens


def _jaccard(a: set[str], b: set[str]) -> float:
    """
    Relevance: Operates within the shared utilities layer.
    Concept: Lightweight semantic feature computation for graph reasoning heuristics.
    Contribution: Contributes a deterministic transformation that supports end-to-end reasoning reproducibility.
    """

    if not a and not b:
        return 0.0
    union = a | b
    if not union:
        return 0.0
    return len(a & b) / len(union)


def _statement_text(stmt: dict[str, Any]) -> str:
    """
    Relevance: Operates within the shared utilities layer.
    Concept: Internal helper implementing one deterministic step of this stage.
    Contribution: Contributes a deterministic transformation that supports end-to-end reasoning reproducibility.
    """

    parts = [
        str(stmt.get("latex", "")),
        str(stmt.get("informal", "")),
        str(stmt.get("proof_sketch", "")),
        str(stmt.get("notes", "")),
    ]
    return "\n".join([p for p in parts if p.strip()])


def _latex_symbol_tokens(latex: str) -> set[str]:
    """
    Relevance: Operates within the shared utilities layer.
    Concept: Extraction of structured signals from raw text or artifact payloads.
    Contribution: Adds symbol-level mathematical semantics beyond lexical overlap.
    """

    out: set[str] = set()
    for cmd in LATEX_COMMAND_PATTERN.findall(str(latex)):
        c = cmd.strip().lower()
        if c and c not in STOPWORDS:
            out.add(c)
    for sym in LATEX_SYMBOL_PATTERN.findall(str(latex)):
        s = sym.strip().lower()
        if s and s not in STOPWORDS:
            out.add(s)
    return out


def _symbol_role_tokens(stmt: dict[str, Any]) -> set[str]:
    """
    Relevance: Operates within the shared utilities layer.
    Concept: Extraction of structured signals from raw text or artifact payloads.
    Contribution: Captures coarse symbol-role alignment from statement metadata and LaTeX payload.
    """

    out: set[str] = set()
    for field in ("used_symbols", "concept_roles"):
        for item in _as_list(stmt.get(field)):
            text = str(item).strip().lower()
            if not text:
                continue
            for token in re.split(r"[^a-z0-9_]+", text):
                if token and token not in STOPWORDS and len(token) > 1:
                    out.add(token)
    out |= _latex_symbol_tokens(str(stmt.get("latex", "")))
    return out


def _family_signature(stmt: dict[str, Any]) -> set[str]:
    """
    Relevance: Operates within the shared utilities layer.
    Concept: Lightweight semantic feature computation for graph reasoning heuristics.
    Contribution: Approximates theorem-family signatures for cross-vocabulary similarity.
    """

    sig: set[str] = set()
    sid = str(stmt.get("id", "")).strip().lower().replace("st.", "")
    sig |= {t for t in TOKEN_PATTERN.findall(sid) if t and t not in STOPWORDS}
    kind = str(stmt.get("kind", "")).strip().lower()
    if kind:
        sig.add(kind)
    for tag in _as_list(stmt.get("method_tags")):
        tag_s = str(tag).strip().lower()
        if tag_s and tag_s not in STOPWORDS:
            sig.add(tag_s)
    notes = str(stmt.get("notes", "")).strip().lower()
    sig |= {t for t in TOKEN_PATTERN.findall(notes) if t and t not in STOPWORDS and len(t) > 2}
    return sig


def _chargram_counter(tokens: set[str], n: int = 3) -> Counter[str]:
    """
    Relevance: Operates within the shared utilities layer.
    Concept: Lightweight semantic feature computation for graph reasoning heuristics.
    Contribution: Provides deterministic pseudo-embedding vectors without external dependencies.
    """

    grams: Counter[str] = Counter()
    for token in tokens:
        t = f"^{token}$"
        if len(t) <= n:
            grams[t] += 1
            continue
        for i in range(len(t) - n + 1):
            grams[t[i : i + n]] += 1
    return grams


def _cosine_counter(a: Counter[str], b: Counter[str]) -> float:
    """
    Relevance: Operates within the shared utilities layer.
    Concept: Lightweight semantic feature computation for graph reasoning heuristics.
    Contribution: Supplies normalized theorem-family embedding similarity.
    """

    if not a or not b:
        return 0.0
    dot = 0.0
    for key, val in a.items():
        dot += float(val) * float(b.get(key, 0))
    if dot <= 0:
        return 0.0
    na = sum(float(v) ** 2 for v in a.values()) ** 0.5
    nb = sum(float(v) ** 2 for v in b.values()) ** 0.5
    if na <= 0 or nb <= 0:
        return 0.0
    return _clamp01(dot / (na * nb))


def _theorem_family_similarity(source_stmt: dict[str, Any], target_stmt: dict[str, Any]) -> float:
    """
    Relevance: Operates within the shared utilities layer.
    Concept: Lightweight semantic feature computation for graph reasoning heuristics.
    Contribution: Adds theorem-family embedding similarity for deeper non-lexical matching.
    """

    s_sig = _family_signature(source_stmt)
    t_sig = _family_signature(target_stmt)
    j = _jaccard(s_sig, t_sig)
    emb = _cosine_counter(_chargram_counter(s_sig), _chargram_counter(t_sig))
    return _clamp01(0.45 * j + 0.55 * emb)


def _structural_signature_overlap(source_stmt: dict[str, Any], target_stmt: dict[str, Any]) -> float:
    """
    Relevance: Operates within the shared utilities layer.
    Concept: Lightweight semantic feature computation for graph reasoning heuristics.
    Contribution: Uses overlap over structured signatures (ids/kinds/method tags) instead of free-text lexical overlap.
    """

    return _jaccard(_family_signature(source_stmt), _family_signature(target_stmt))


def _evidence_coverage(evidence_terms: list[str], support_text: str, target_text: str) -> float:
    """
    Relevance: Operates within the shared utilities layer.
    Concept: Internal helper implementing one deterministic step of this stage.
    Contribution: Contributes a deterministic transformation that supports end-to-end reasoning reproducibility.
    """

    terms = [str(t).strip().lower() for t in evidence_terms if str(t).strip()]
    if not terms:
        return 0.0

    s = support_text.lower()
    t = target_text.lower()
    both = 0
    either = 0
    for term in terms:
        in_s = term in s
        in_t = term in t
        if in_s or in_t:
            either += 1
        if in_s and in_t:
            both += 1

    return _clamp01(0.7 * (both / len(terms)) + 0.3 * (either / len(terms)))


def _structured_statement_tokens(stmt: dict[str, Any]) -> set[str]:
    """
    Relevance: Operates within the shared utilities layer.
    Concept: Extraction of structured signals from already-processed statement payloads.
    Contribution: Lets hypothesis evaluation compare inferential schemas against typed statement structure rather than superficial free-text overlap.
    """

    out = _family_signature(stmt) | _symbol_role_tokens(stmt)
    out |= _tokenize(str(stmt.get("informal", "")))
    out |= _tokenize(str(stmt.get("proof_sketch", "")))
    return out


def _value_tokens(value: Any) -> set[str]:
    """
    Relevance: Operates within the shared utilities layer.
    Concept: Normalization of structured hypothesis fields into comparable token sets.
    Contribution: Makes antecedent, consequence, invariant, and barrier fields measurable without depending on raw lexical matching.
    """

    tokens: set[str] = set()
    for item in _as_list(value):
        tokens |= _tokenize(str(item))
    return tokens


def _field_alignment(value: Any, *statements: dict[str, Any]) -> float:
    """
    Relevance: Operates within the shared utilities layer.
    Concept: Structured alignment between a typed inferential field and statement signatures.
    Contribution: Quantifies whether a hypothesis commitment is actually grounded in the mathematical structure of the paired statements.
    """

    value_tokens = _value_tokens(value)
    if not value_tokens:
        return 0.0
    stmt_tokens: set[str] = set()
    for stmt in statements:
        if isinstance(stmt, dict):
            stmt_tokens |= _structured_statement_tokens(stmt)
    if not stmt_tokens:
        return 0.0
    covered = len(value_tokens & stmt_tokens) / max(1, len(value_tokens))
    return _clamp01(0.75 * covered + 0.25 * _jaccard(value_tokens, stmt_tokens))


def _field_gap_signal(value: Any, *statements: dict[str, Any], defaults: set[str] | None = None) -> float:
    """
    Relevance: Operates within the shared utilities layer.
    Concept: Detection of missing support for an explicit inferential commitment.
    Contribution: Penalizes hypotheses that declare precise mathematical commitments which are not reflected in the structured statement signatures.
    """

    normalized = " ".join(str(item).strip() for item in _as_list(value) if str(item).strip()).strip().lower()
    if not normalized:
        return 0.0
    if defaults and normalized in defaults:
        return 0.0
    return 1.0 if _field_alignment(value, *statements) < 0.12 else 0.0


def _negation_count(text: str) -> int:
    """
    Relevance: Operates within the shared utilities layer.
    Concept: Internal helper implementing one deterministic step of this stage.
    Contribution: Contributes a deterministic transformation that supports end-to-end reasoning reproducibility.
    """

    tokens = _tokenize(text)
    count = 0
    for token in tokens:
        if token in NEGATION_MARKERS or token.startswith("not"):
            count += 1
    return count


def _contradiction_signal(support_text: str, target_text: str, overlap_score: float) -> float:
    """
    Relevance: Operates within the shared utilities layer.
    Concept: Internal helper implementing one deterministic step of this stage.
    Contribution: Contributes a deterministic transformation that supports end-to-end reasoning reproducibility.
    """

    s_neg = _negation_count(support_text)
    t_neg = _negation_count(target_text)
    if (s_neg > 0) == (t_neg > 0):
        return 0.0
    if overlap_score < 0.08:
        return 0.0
    imbalance = abs(s_neg - t_neg)
    return _clamp01(0.18 + 0.55 * overlap_score + min(0.18, 0.04 * imbalance))


def _kind_compatibility(support_kind: str, target_kind: str) -> float:
    """
    Relevance: Operates within the shared utilities layer.
    Concept: Typed classification used to guide scoring and prioritization.
    Contribution: Contributes a deterministic transformation that supports end-to-end reasoning reproducibility.
    """

    s = support_kind.lower().strip()
    t = target_kind.lower().strip()

    if s == "definition" and t in {"theorem", "lemma", "corollary", "conjecture", "observation"}:
        return 0.90
    if s in {"axiom", "theorem", "lemma"} and t in {"theorem", "lemma", "corollary", "observation"}:
        return 0.86
    if s == "definition" and t == "definition":
        return 0.45
    if s == "conjecture":
        return 0.40
    if not s or not t:
        return 0.25
    return 0.60


def _status_from_verdict(verdict: str) -> str:
    """
    Relevance: Operates within the shared utilities layer.
    Concept: Internal helper implementing one deterministic step of this stage.
    Contribution: Contributes a deterministic transformation that supports end-to-end reasoning reproducibility.
    """

    if verdict == "supported":
        return "supported"
    if verdict == "refuted":
        return "refuted"
    if verdict == "provisionally-supported":
        return "provisionally-supported"
    if verdict == "provisionally-refuted":
        return "provisionally-refuted"
    return "needs-testing"


def _action_from_verdict(verdict: str) -> str:
    """
    Relevance: Operates within the shared utilities layer.
    Concept: Internal helper implementing one deterministic step of this stage.
    Contribution: Contributes a deterministic transformation that supports end-to-end reasoning reproducibility.
    """

    if verdict == "supported":
        return "promote-or-retest-with-deduction"
    if verdict == "refuted":
        return "archive-and-seek-alternative-hypothesis"
    if verdict in {"provisionally-supported", "provisionally-refuted"}:
        return "collect-stronger-deductive-evidence"
    return "run-another-abduce-deduce-round"


def _normalize_evidence_map(evidence_payload: Any) -> dict[str, dict[str, Any]]:
    """
    Relevance: Operates within the shared utilities layer.
    Concept: Normalization of input structures into stable internal forms.
    Contribution: Reduces runtime ambiguity and prevents malformed artifacts from destabilizing the workflow.
    """

    out: dict[str, dict[str, Any]] = {}
    if isinstance(evidence_payload, dict):
        if isinstance(evidence_payload.get("hypotheses"), list):
            items = evidence_payload.get("hypotheses", [])
        else:
            items = []
    elif isinstance(evidence_payload, list):
        items = evidence_payload
    else:
        return out

    for item in items:
        if not isinstance(item, dict):
            continue
        hid = str(item.get("hypothesis_id", "")).strip()
        if not hid:
            continue
        out[hid] = item
    return out


def _normalize_coherence_map(payload: Any) -> dict[str, dict[str, Any]]:
    """
    Relevance: Operates within the shared utilities layer.
    Concept: Normalization of input structures into stable internal forms.
    Contribution: Reduces runtime ambiguity and prevents malformed artifacts from destabilizing the workflow.
    """

    out: dict[str, dict[str, Any]] = {}
    if not isinstance(payload, dict):
        return out

    index_payload = payload.get("hypothesis_coherence_index")
    if isinstance(index_payload, dict):
        for hid, row in index_payload.items():
            hid_s = str(hid).strip()
            if not hid_s or not isinstance(row, dict):
                continue
            out[hid_s] = row

    rows = payload.get("hypothesis_coherence")
    if isinstance(rows, list):
        for row in rows:
            if not isinstance(row, dict):
                continue
            hid = str(row.get("hypothesis_id", "")).strip()
            if not hid:
                continue
            out[hid] = row
    return out


def load_hypothesis_evidence(path: Path | None) -> dict[str, dict[str, Any]]:
    """
    Relevance: Operates within the shared utilities layer.
    Concept: Primary callable implementing a stage-level behavior.
    Contribution: Contributes a deterministic transformation that supports end-to-end reasoning reproducibility.
    """

    if path is None:
        return {}
    if not path.exists():
        raise FileNotFoundError(f"Evidence file not found: {path}")
    try:
        payload = yaml.safe_load(path.read_text(encoding="utf-8"))
    except yaml.YAMLError as exc:
        raise ValueError(f"Evidence file is not valid YAML: {path}") from exc
    return _normalize_evidence_map(payload)


def load_coherence_signals(path: Path | None) -> tuple[dict[str, dict[str, Any]], dict[str, Any]]:
    """
    Relevance: Operates within the shared utilities layer.
    Concept: Primary callable implementing a stage-level behavior.
    Contribution: Contributes a deterministic transformation that supports end-to-end reasoning reproducibility.
    """

    if path is None:
        return {}, {}
    if not path.exists():
        raise FileNotFoundError(f"Coherence report not found: {path}")
    try:
        payload = yaml.safe_load(path.read_text(encoding="utf-8"))
    except yaml.YAMLError as exc:
        raise ValueError(f"Coherence report is not valid YAML: {path}") from exc
    if not isinstance(payload, dict):
        return {}, {}
    coherence_by_hypothesis = _normalize_coherence_map(payload)
    coherence_profile = payload.get("coherence_profile", {})
    if not isinstance(coherence_profile, dict):
        coherence_profile = {}
    return coherence_by_hypothesis, coherence_profile


def _coherence_adjustments(
    coherence_row: dict[str, Any] | None,
) -> tuple[float, float, list[str], dict[str, float]]:
    """
    Relevance: Operates within the shared utilities layer.
    Concept: Quantitative evaluation of hypotheses or theory-graph properties.
    Contribution: Produces the quantitative signals used for retention, revision, and route prioritization.
    """

    if not isinstance(coherence_row, dict):
        return 0.0, 0.0, [], {
            "explanatory_power_local": 0.0,
            "coherence_delta_global": 0.0,
            "global_coherence_if_accepted": 0.0,
        }

    explanatory_power = _clamp01(_safe_float(coherence_row.get("explanatory_power_local"), 0.0))
    coherence_delta = max(-1.0, min(1.0, _safe_float(coherence_row.get("coherence_delta_global"), 0.0)))
    global_if_accepted = _clamp01(_safe_float(coherence_row.get("global_coherence_if_accepted"), 0.0))

    support_delta = 0.20 * explanatory_power + 0.24 * max(0.0, coherence_delta)
    refute_delta = 0.24 * max(0.0, -coherence_delta) + 0.12 * max(0.0, 0.25 - explanatory_power)

    reasons: list[str] = []
    if explanatory_power >= 0.50:
        reasons.append(f"explanatory_power_local={explanatory_power:.4f}")
    if coherence_delta >= 0.03:
        reasons.append(f"coherence_delta_global=+{coherence_delta:.4f}")
    elif coherence_delta <= -0.03:
        reasons.append(f"coherence_delta_global={coherence_delta:.4f}")

    return (
        _clamp01(support_delta),
        _clamp01(refute_delta),
        reasons,
        {
            "explanatory_power_local": round(explanatory_power, 4),
            "coherence_delta_global": round(coherence_delta, 4),
            "global_coherence_if_accepted": round(global_if_accepted, 4),
        },
    )


def _evidence_adjustments(evidence: dict[str, Any] | None) -> tuple[float, float, list[str]]:
    """
    Relevance: Operates within the shared utilities layer.
    Concept: Internal helper implementing one deterministic step of this stage.
    Contribution: Contributes a deterministic transformation that supports end-to-end reasoning reproducibility.
    """

    if not isinstance(evidence, dict):
        return 0.0, 0.0, []

    support_delta = 0.0
    refute_delta = 0.0
    reasons: list[str] = []

    deduce_class = str(evidence.get("deduce_class", "")).strip().lower()
    if deduce_class == "entailed":
        support_delta += 0.28
        reasons.append("deduce_class=entailed")
    elif deduce_class == "conditionally-entailed":
        support_delta += 0.14
        reasons.append("deduce_class=conditionally-entailed")
    elif deduce_class == "not-derived":
        refute_delta += 0.16
        reasons.append("deduce_class=not-derived")

    residual_delta = _safe_float(evidence.get("abduce_residual_delta"), 0.0)
    if residual_delta < 0:
        support_delta += min(0.16, 0.03 * abs(residual_delta))
        reasons.append(f"abduce_residual_delta={residual_delta}")
    elif residual_delta > 0:
        refute_delta += min(0.16, 0.03 * abs(residual_delta))
        reasons.append(f"abduce_residual_delta={residual_delta}")

    if bool(evidence.get("contradiction", False)):
        refute_delta += 0.24
        reasons.append("explicit_contradiction=true")

    if bool(evidence.get("experimental_success", False)):
        support_delta += 0.16
        reasons.append("experimental_success=true")
    if bool(evidence.get("falsified", False)):
        refute_delta += 0.34
        reasons.append("falsified=true")

    return _clamp01(support_delta), _clamp01(refute_delta), reasons


def classify_verdict(
    support_score: float,
    refute_score: float,
    support_threshold: float,
    refute_threshold: float,
    margin: float = 0.08,
    force_resolution: bool = False,
) -> str:
    """
    Relevance: Operates within the shared utilities layer.
    Concept: Primary callable implementing a stage-level behavior.
    Contribution: Contributes a deterministic transformation that supports end-to-end reasoning reproducibility.
    """

    if refute_score >= refute_threshold and (refute_score - support_score) >= margin:
        return "refuted"
    if support_score >= support_threshold and (support_score - refute_score) >= margin:
        return "supported"
    if force_resolution:
        if support_score >= refute_score:
            return "provisionally-supported"
        return "provisionally-refuted"
    return "inconclusive"


def load_kb_statements(kb_path: Path) -> dict[str, dict[str, Any]]:
    """
    Relevance: Operates within the shared utilities layer.
    Concept: Primary callable implementing a stage-level behavior.
    Contribution: Contributes a deterministic transformation that supports end-to-end reasoning reproducibility.
    """

    content = kb_path.read_text(encoding="utf-8")
    out: dict[str, dict[str, Any]] = {}
    for match in STATEMENT_BLOCK_PATTERN.finditer(content):
        try:
            payload = yaml.safe_load(match.group(1))
        except yaml.YAMLError:
            continue
        if not isinstance(payload, dict):
            continue
        sid = str(payload.get("id", "")).strip()
        if not sid:
            continue
        out[sid] = payload
    return out


def load_hypothesis_payload(phyp_path: Path) -> dict[str, Any]:
    """
    Relevance: Operates within the shared utilities layer.
    Concept: Primary callable implementing a stage-level behavior.
    Contribution: Contributes a deterministic transformation that supports end-to-end reasoning reproducibility.
    """

    try:
        payload = yaml.safe_load(phyp_path.read_text(encoding="utf-8"))
    except yaml.YAMLError as exc:
        raise ValueError(f"Hypothesis file is not valid YAML: {phyp_path}") from exc
    if not isinstance(payload, dict):
        raise ValueError("Hypothesis payload must be a YAML object.")
    if not isinstance(payload.get("hypotheses"), list):
        raise ValueError("Hypothesis payload must include list field `hypotheses`.")
    return payload


def load_analysis_scores(analysis_path: Path | None) -> dict[tuple[str, str], float]:
    """
    Relevance: Operates within the shared utilities layer.
    Concept: Primary callable implementing a stage-level behavior.
    Contribution: Contributes a deterministic transformation that supports end-to-end reasoning reproducibility.
    """

    if analysis_path is None:
        return {}
    if not analysis_path.exists():
        raise FileNotFoundError(f"Analysis file not found: {analysis_path}")
    try:
        payload = yaml.safe_load(analysis_path.read_text(encoding="utf-8"))
    except yaml.YAMLError as exc:
        raise ValueError(f"Analysis file is not valid YAML: {analysis_path}") from exc
    if not isinstance(payload, dict):
        return {}

    out: dict[tuple[str, str], float] = {}
    for item in payload.get("connection_candidates", []):
        if not isinstance(item, dict):
            continue
        src = str(item.get("from_id", "")).strip()
        dst = str(item.get("to_id", "")).strip()
        if not src or not dst:
            continue
        out[(src, dst)] = _clamp01(_safe_float(item.get("score"), 0.0))
    return out


def _evaluate_bridge_hypothesis(
    hypothesis: dict[str, Any],
    statements: dict[str, dict[str, Any]],
    analysis_scores: dict[tuple[str, str], float],
    evidence_by_hypothesis: dict[str, dict[str, Any]],
    coherence_by_hypothesis: dict[str, dict[str, Any]],
    support_threshold: float,
    refute_threshold: float,
    margin: float,
    force_resolution: bool,
) -> dict[str, Any]:
    """
    Relevance: Operates within the shared utilities layer.
    Concept: Quantitative evaluation of hypotheses or theory-graph properties.
    Contribution: Produces the quantitative signals used for retention, revision, and route prioritization.
    """

    hyp_id = str(hypothesis.get("id", "")).strip()
    source_id = str(hypothesis.get("support_statement_id", "")).strip()
    target_id = str(hypothesis.get("target_statement_id", "")).strip()
    priority = _safe_float(hypothesis.get("priority"), 0.0)
    current_status = str(hypothesis.get("status", "tentative")).strip() or "tentative"

    source_stmt = statements.get(source_id)
    target_stmt = statements.get(target_id)
    missing_source = source_stmt is None
    missing_target = target_stmt is None
    missing_any = missing_source or missing_target

    source_text = _statement_text(source_stmt or {})
    target_text = _statement_text(target_stmt or {})
    lexical_overlap = _structural_signature_overlap(source_stmt or {}, target_stmt or {})
    symbol_role_alignment = _jaccard(_symbol_role_tokens(source_stmt or {}), _symbol_role_tokens(target_stmt or {}))
    theorem_family_similarity = _theorem_family_similarity(source_stmt or {}, target_stmt or {})

    evidence_terms = [str(x) for x in _as_list(hypothesis.get("evidence_terms")) if str(x).strip()]
    evidence_coverage = _evidence_coverage(evidence_terms, source_text, target_text)

    source_kind = str((source_stmt or {}).get("kind", ""))
    target_kind = str((target_stmt or {}).get("kind", ""))
    kind_compat = _kind_compatibility(source_kind, target_kind)

    target_deps = {str(x).strip() for x in _as_list((target_stmt or {}).get("depends_on")) if str(x).strip()}
    source_deps = {str(x).strip() for x in _as_list((source_stmt or {}).get("depends_on")) if str(x).strip()}

    direct_dependency = 1.0 if source_id and source_id in target_deps else 0.0
    reverse_dependency = 1.0 if target_id and target_id in source_deps else 0.0
    self_loop = 1.0 if source_id and source_id == target_id else 0.0
    semantic_overlap = _clamp01(
        0.10 * lexical_overlap + 0.40 * symbol_role_alignment + 0.35 * theorem_family_similarity + 0.15 * kind_compat
    )

    provenance = hypothesis.get("provenance", {}) if isinstance(hypothesis.get("provenance"), dict) else {}
    provenance_score = _safe_float(provenance.get("analysis_score"), -1.0)
    analysis_score = provenance_score if provenance_score >= 0.0 else analysis_scores.get((source_id, target_id), 0.0)
    analysis_score = _clamp01(analysis_score)
    evidence = evidence_by_hypothesis.get(hyp_id, {})
    coherence_row = coherence_by_hypothesis.get(hyp_id, {})

    contradiction = _contradiction_signal(source_text, target_text, semantic_overlap)
    weak_signal = 1.0 if (direct_dependency == 0.0 and semantic_overlap < 0.08 and analysis_score < 0.20) else 0.0
    antecedent_alignment = _field_alignment(hypothesis.get("support_antecedent_schema"), source_stmt or {})
    consequence_alignment = _field_alignment(hypothesis.get("target_consequence_schema"), target_stmt or {})
    invariant_alignment = _field_alignment(hypothesis.get("preserved_invariant"), source_stmt or {}, target_stmt or {})
    barrier_alignment = _field_alignment(hypothesis.get("barrier_scope"), source_stmt or {}, target_stmt or {})
    commitment_support = _clamp01(
        0.28 * antecedent_alignment
        + 0.28 * consequence_alignment
        + 0.28 * invariant_alignment
        + 0.16 * barrier_alignment
    )
    commitment_refute = _clamp01(
        0.30 * _field_gap_signal(hypothesis.get("support_antecedent_schema"), source_stmt or {}, defaults={"unconditional"})
        + 0.30 * _field_gap_signal(
            hypothesis.get("target_consequence_schema"), target_stmt or {}, defaults={"statement-conclusion"}
        )
        + 0.25 * _field_gap_signal(hypothesis.get("preserved_invariant"), source_stmt or {}, target_stmt or {})
        + 0.15 * _field_gap_signal(hypothesis.get("barrier_scope"), source_stmt or {}, target_stmt or {}, defaults={"none"})
    )
    novel_bridge_support = 1.0 if (
        direct_dependency == 0.0
        and contradiction < 0.18
        and analysis_score >= 0.38
        and commitment_support >= 0.28
        and (symbol_role_alignment >= 0.18 or theorem_family_similarity >= 0.24)
    ) else 0.0

    base_support = _clamp01(
        0.10 * direct_dependency
        + 0.24 * analysis_score
        + 0.05 * lexical_overlap
        + 0.18 * symbol_role_alignment
        + 0.14 * theorem_family_similarity
        + 0.09 * evidence_coverage
        + 0.08 * kind_compat
        + 0.12 * semantic_overlap
        + 0.10 * novel_bridge_support
    )

    base_refute = _clamp01(
        0.48 * self_loop + 0.16 * float(missing_any) + 0.12 * reverse_dependency + 0.18 * contradiction + 0.06 * weak_signal
    )
    support_delta, refute_delta, evidence_reasons = _evidence_adjustments(evidence)
    coherence_support_delta, coherence_refute_delta, coherence_reasons, coherence_signals = _coherence_adjustments(coherence_row)
    support_score = _clamp01(base_support + 0.14 * commitment_support + support_delta + coherence_support_delta)
    refute_score = _clamp01(base_refute + 0.12 * commitment_refute + refute_delta + coherence_refute_delta)

    verdict = classify_verdict(
        support_score=support_score,
        refute_score=refute_score,
        support_threshold=support_threshold,
        refute_threshold=refute_threshold,
        margin=margin,
        force_resolution=force_resolution,
    )
    confidence = _clamp01(max(support_score, refute_score) * (0.55 + 0.45 * abs(support_score - refute_score)))

    reasons = []
    if missing_source:
        reasons.append(f"support statement missing from KB: {source_id}")
    if missing_target:
        reasons.append(f"target statement missing from KB: {target_id}")
    if self_loop > 0:
        reasons.append("self-loop support->target relation is invalid")
    if direct_dependency > 0:
        reasons.append("target already depends on support in KB")
    if reverse_dependency > 0:
        reasons.append("reverse dependency detected (potential direction conflict)")
    if lexical_overlap >= 0.18:
        reasons.append("structural signature overlap between support and target")
    if symbol_role_alignment >= 0.18:
        reasons.append("symbol-role alignment indicates semantic compatibility")
    if theorem_family_similarity >= 0.25:
        reasons.append("theorem-family embedding similarity indicates structural proximity")
    if analysis_score >= 0.45:
        reasons.append("high connector analysis score for support->target pair")
    if novel_bridge_support > 0:
        reasons.append("novel bridge is structurally well-supported despite absent explicit dependency")
    if antecedent_alignment >= 0.18:
        reasons.append(
            f"support antecedent schema grounded in support statement structure: {str(hypothesis.get('support_antecedent_schema', '')).strip()}"
        )
    if consequence_alignment >= 0.18:
        reasons.append(
            f"target consequence schema grounded in target statement structure: {str(hypothesis.get('target_consequence_schema', '')).strip()}"
        )
    if invariant_alignment >= 0.18:
        reasons.append(
            f"preserved invariant matches shared mathematical structure: {str(hypothesis.get('preserved_invariant', '')).strip()}"
        )
    if barrier_alignment >= 0.18 and str(hypothesis.get("barrier_scope", "")).strip().lower() not in {"", "none"}:
        reasons.append(f"barrier scope is structurally visible: {str(hypothesis.get('barrier_scope', '')).strip()}")
    if contradiction >= 0.28:
        reasons.append("negation mismatch suggests potential contradiction")
    for reason in evidence_reasons:
        reasons.append(reason)
    for reason in coherence_reasons:
        reasons.append(reason)

    return {
        "hypothesis_id": hyp_id,
        "kind": str(hypothesis.get("kind", "bridge-link")),
        "priority": round(priority, 4),
        "current_status": current_status,
        "target_statement_id": target_id,
        "support_statement_id": source_id,
        "verdict": verdict,
        "next_status": _status_from_verdict(verdict),
        "recommended_action": _action_from_verdict(verdict),
        "support_score": round(support_score, 4),
        "refute_score": round(refute_score, 4),
        "confidence": round(confidence, 4),
        "inferential_commitment": {
            "support_antecedent_schema": str(hypothesis.get("support_antecedent_schema", "")).strip(),
            "target_consequence_schema": str(hypothesis.get("target_consequence_schema", "")).strip(),
            "preserved_invariant": str(hypothesis.get("preserved_invariant", "")).strip(),
            "barrier_scope": str(hypothesis.get("barrier_scope", "")).strip(),
        },
        "signals": {
            "direct_dependency": round(direct_dependency, 4),
            "reverse_dependency": round(reverse_dependency, 4),
            "self_loop": round(self_loop, 4),
            "analysis_score": round(analysis_score, 4),
            "lexical_overlap": round(lexical_overlap, 4),
            "structural_signature_overlap": round(lexical_overlap, 4),
            "semantic_overlap": round(semantic_overlap, 4),
            "novel_bridge_support": round(novel_bridge_support, 4),
            "symbol_role_alignment": round(symbol_role_alignment, 4),
            "theorem_family_similarity": round(theorem_family_similarity, 4),
            "evidence_coverage": round(evidence_coverage, 4),
            "kind_compatibility": round(kind_compat, 4),
            "contradiction_signal": round(contradiction, 4),
            "antecedent_alignment": round(antecedent_alignment, 4),
            "consequence_alignment": round(consequence_alignment, 4),
            "invariant_alignment": round(invariant_alignment, 4),
            "barrier_alignment": round(barrier_alignment, 4),
            "commitment_support": round(commitment_support, 4),
            "commitment_refute": round(commitment_refute, 4),
            "evidence_support_adjustment": round(support_delta, 4),
            "evidence_refute_adjustment": round(refute_delta, 4),
            "coherence_support_adjustment": round(coherence_support_delta, 4),
            "coherence_refute_adjustment": round(coherence_refute_delta, 4),
            "explanatory_power_local": coherence_signals["explanatory_power_local"],
            "coherence_delta_global": coherence_signals["coherence_delta_global"],
            "global_coherence_if_accepted": coherence_signals["global_coherence_if_accepted"],
        },
        "reasons": reasons,
    }


def _intervention_maxima(hypotheses: list[dict[str, Any]]) -> tuple[float, float]:
    """
    Relevance: Operates within the shared utilities layer.
    Concept: Internal helper implementing one deterministic step of this stage.
    Contribution: Contributes a deterministic transformation that supports end-to-end reasoning reproducibility.
    """

    max_downstream = 0.0
    max_unresolved = 0.0
    for h in hypotheses:
        metrics = h.get("metrics", {}) if isinstance(h.get("metrics"), dict) else {}
        max_downstream = max(max_downstream, _safe_float(metrics.get("downstream_impact"), 0.0))
        max_unresolved = max(max_unresolved, _safe_float(metrics.get("unresolved_dependencies"), 0.0))
    return max(max_downstream, 1.0), max(max_unresolved, 1.0)


def _evaluate_intervention_hypothesis(
    hypothesis: dict[str, Any],
    statements: dict[str, dict[str, Any]],
    evidence_by_hypothesis: dict[str, dict[str, Any]],
    coherence_by_hypothesis: dict[str, dict[str, Any]],
    support_threshold: float,
    refute_threshold: float,
    margin: float,
    force_resolution: bool,
    max_downstream: float,
    max_unresolved: float,
) -> dict[str, Any]:
    """
    Relevance: Operates within the shared utilities layer.
    Concept: Quantitative evaluation of hypotheses or theory-graph properties.
    Contribution: Produces the quantitative signals used for retention, revision, and route prioritization.
    """

    hyp_id = str(hypothesis.get("id", "")).strip()
    target_id = str(hypothesis.get("target_statement_id", "")).strip()
    priority = _safe_float(hypothesis.get("priority"), 0.0)
    current_status = str(hypothesis.get("status", "tentative")).strip() or "tentative"

    target_stmt = statements.get(target_id)
    missing_target = target_stmt is None

    metrics = hypothesis.get("metrics", {}) if isinstance(hypothesis.get("metrics"), dict) else {}
    downstream = _safe_float(metrics.get("downstream_impact"), 0.0)
    unresolved = _safe_float(metrics.get("unresolved_dependencies"), 0.0)
    cross_component = _clamp01(_safe_float(metrics.get("cross_component_potential"), 0.0))
    betweenness = _clamp01(_safe_float(metrics.get("betweenness"), 0.0))
    evidence = evidence_by_hypothesis.get(hyp_id, {})
    coherence_row = coherence_by_hypothesis.get(hyp_id, {})

    downstream_norm = _clamp01(downstream / max_downstream)
    unresolved_norm = _clamp01(unresolved / max_unresolved)

    base_support = _clamp01(
        0.44 * priority + 0.22 * cross_component + 0.18 * downstream_norm + 0.10 * unresolved_norm + 0.06 * betweenness
    )

    low_priority = 1.0 if priority < 0.28 else 0.0
    stagnation = 1.0 if (downstream_norm < 0.08 and cross_component < 0.20) else 0.0
    base_refute = _clamp01(0.55 * float(missing_target) + 0.30 * low_priority + 0.15 * stagnation)
    support_delta, refute_delta, evidence_reasons = _evidence_adjustments(evidence)
    coherence_support_delta, coherence_refute_delta, coherence_reasons, coherence_signals = _coherence_adjustments(coherence_row)
    support_score = _clamp01(base_support + support_delta + coherence_support_delta)
    refute_score = _clamp01(base_refute + refute_delta + coherence_refute_delta)

    verdict = classify_verdict(
        support_score=support_score,
        refute_score=refute_score,
        support_threshold=support_threshold,
        refute_threshold=refute_threshold,
        margin=margin,
        force_resolution=force_resolution,
    )
    confidence = _clamp01(max(support_score, refute_score) * (0.55 + 0.45 * abs(support_score - refute_score)))

    reasons = []
    if missing_target:
        reasons.append(f"target statement missing from KB: {target_id}")
    if priority >= 0.60:
        reasons.append("high priority inherited from connector hypotheses")
    if cross_component >= 0.45:
        reasons.append("strong cross-component potential")
    if downstream_norm >= 0.45:
        reasons.append("high downstream impact relative to intervention set")
    if low_priority > 0:
        reasons.append("low priority weakens intervention focus")
    if stagnation > 0:
        reasons.append("low downstream/cross-component signals indicate low-yield target")
    for reason in evidence_reasons:
        reasons.append(reason)
    for reason in coherence_reasons:
        reasons.append(reason)

    return {
        "hypothesis_id": hyp_id,
        "kind": str(hypothesis.get("kind", "intervention-focus")),
        "priority": round(priority, 4),
        "current_status": current_status,
        "target_statement_id": target_id,
        "support_statement_id": "",
        "verdict": verdict,
        "next_status": _status_from_verdict(verdict),
        "recommended_action": _action_from_verdict(verdict),
        "support_score": round(support_score, 4),
        "refute_score": round(refute_score, 4),
        "confidence": round(confidence, 4),
        "signals": {
            "priority": round(priority, 4),
            "cross_component": round(cross_component, 4),
            "downstream_norm": round(downstream_norm, 4),
            "unresolved_norm": round(unresolved_norm, 4),
            "betweenness": round(betweenness, 4),
            "missing_target": int(missing_target),
            "evidence_support_adjustment": round(support_delta, 4),
            "evidence_refute_adjustment": round(refute_delta, 4),
            "coherence_support_adjustment": round(coherence_support_delta, 4),
            "coherence_refute_adjustment": round(coherence_refute_delta, 4),
            "explanatory_power_local": coherence_signals["explanatory_power_local"],
            "coherence_delta_global": coherence_signals["coherence_delta_global"],
            "global_coherence_if_accepted": coherence_signals["global_coherence_if_accepted"],
        },
        "reasons": reasons,
    }


def _evaluate_conceptual_hypothesis(
    hypothesis: dict[str, Any],
    statements: dict[str, dict[str, Any]],
    analysis_scores: dict[tuple[str, str], float],
    evidence_by_hypothesis: dict[str, dict[str, Any]],
    coherence_by_hypothesis: dict[str, dict[str, Any]],
    support_threshold: float,
    refute_threshold: float,
    margin: float,
    force_resolution: bool,
) -> dict[str, Any]:
    """
    Relevance: Operates within the shared utilities layer.
    Concept: Quantitative evaluation of hypotheses or theory-graph properties.
    Contribution: Produces the quantitative signals used for retention, revision, and route prioritization.
    """

    hyp_id = str(hypothesis.get("id", "")).strip()
    kind = str(hypothesis.get("kind", "")).strip().lower()
    target_id = str(hypothesis.get("target_statement_id", "")).strip()
    source_id = str(hypothesis.get("support_statement_id", "")).strip()
    priority = _safe_float(hypothesis.get("priority"), 0.0)
    current_status = str(hypothesis.get("status", "tentative")).strip() or "tentative"

    source_stmt = statements.get(source_id, {})
    target_stmt = statements.get(target_id, {})
    source_text = _statement_text(source_stmt)
    target_text = _statement_text(target_stmt)
    lexical_overlap = _structural_signature_overlap(source_stmt, target_stmt)
    symbol_role_alignment = _jaccard(_symbol_role_tokens(source_stmt), _symbol_role_tokens(target_stmt))
    theorem_family_similarity = _theorem_family_similarity(source_stmt, target_stmt)

    provenance = hypothesis.get("provenance", {}) if isinstance(hypothesis.get("provenance"), dict) else {}
    analysis_score = _safe_float(provenance.get("analysis_score"), analysis_scores.get((source_id, target_id), 0.0))
    analysis_score = _clamp01(analysis_score)
    evidence = evidence_by_hypothesis.get(hyp_id, {})
    coherence_row = coherence_by_hypothesis.get(hyp_id, {})

    novelty_bonus = 0.06
    if kind in {"representation-shift", "normal-form-reduction"}:
        novelty_bonus = 0.12
    elif kind in {"barrier-escape-principle", "intermediate-invariant"}:
        novelty_bonus = 0.10

    direct_dependency = 0.0
    target_deps = {str(x).strip() for x in _as_list(target_stmt.get("depends_on")) if str(x).strip()}
    if source_id and source_id in target_deps:
        direct_dependency = 1.0

    antecedent_alignment = _field_alignment(hypothesis.get("support_antecedent_schema"), source_stmt)
    consequence_alignment = _field_alignment(hypothesis.get("target_consequence_schema"), target_stmt)
    invariant_alignment = _field_alignment(hypothesis.get("preserved_invariant"), source_stmt, target_stmt)
    barrier_alignment = _field_alignment(hypothesis.get("barrier_scope"), source_stmt, target_stmt)
    commitment_support = _clamp01(
        0.24 * antecedent_alignment
        + 0.20 * consequence_alignment
        + 0.36 * invariant_alignment
        + 0.20 * barrier_alignment
    )
    commitment_refute = _clamp01(
        0.22 * _field_gap_signal(hypothesis.get("support_antecedent_schema"), source_stmt, defaults={"unconditional"})
        + 0.18 * _field_gap_signal(
            hypothesis.get("target_consequence_schema"), target_stmt, defaults={"statement-conclusion"}
        )
        + 0.34 * _field_gap_signal(hypothesis.get("preserved_invariant"), source_stmt, target_stmt)
        + 0.26 * _field_gap_signal(hypothesis.get("barrier_scope"), source_stmt, target_stmt, defaults={"none"})
    )

    semantic_overlap = _clamp01(
        0.10 * lexical_overlap + 0.45 * symbol_role_alignment + 0.35 * theorem_family_similarity + 0.10 * direct_dependency
    )
    contradiction = _contradiction_signal(source_text, target_text, semantic_overlap)
    base_support = _clamp01(
        0.32 * _clamp01(priority)
        + 0.20 * analysis_score
        + 0.06 * lexical_overlap
        + 0.16 * symbol_role_alignment
        + 0.12 * theorem_family_similarity
        + 0.08 * direct_dependency
        + 0.08 * semantic_overlap
        + novelty_bonus
    )
    missing_target = 1.0 if (target_id and target_id not in statements) else 0.0
    missing_source = 1.0 if (source_id and source_id not in statements) else 0.0
    base_refute = _clamp01(0.28 * missing_target + 0.16 * missing_source + 0.34 * contradiction)

    support_delta, refute_delta, evidence_reasons = _evidence_adjustments(evidence)
    coherence_support_delta, coherence_refute_delta, coherence_reasons, coherence_signals = _coherence_adjustments(coherence_row)
    support_score = _clamp01(base_support + 0.18 * commitment_support + support_delta + coherence_support_delta)
    refute_score = _clamp01(base_refute + 0.12 * commitment_refute + refute_delta + coherence_refute_delta)

    verdict = classify_verdict(
        support_score=support_score,
        refute_score=refute_score,
        support_threshold=support_threshold,
        refute_threshold=refute_threshold,
        margin=margin,
        force_resolution=force_resolution,
    )
    confidence = _clamp01(max(support_score, refute_score) * (0.55 + 0.45 * abs(support_score - refute_score)))

    reasons = [
        f"conceptual_kind={kind}",
    ]
    if analysis_score >= 0.35:
        reasons.append("connector support for conceptual bridge present")
    if semantic_overlap >= 0.14:
        reasons.append("nontrivial structured semantic overlap between support and target contexts")
    if invariant_alignment >= 0.18:
        reasons.append(
            f"conceptual move preserves explicit invariant: {str(hypothesis.get('preserved_invariant', '')).strip()}"
        )
    if barrier_alignment >= 0.18 and str(hypothesis.get("barrier_scope", "")).strip().lower() not in {"", "none"}:
        reasons.append(f"conceptual move is barrier-scoped: {str(hypothesis.get('barrier_scope', '')).strip()}")
    if consequence_alignment >= 0.18:
        reasons.append(
            f"conceptual move targets explicit consequence schema: {str(hypothesis.get('target_consequence_schema', '')).strip()}"
        )
    for reason in evidence_reasons:
        reasons.append(reason)
    for reason in coherence_reasons:
        reasons.append(reason)

    return {
        "hypothesis_id": hyp_id,
        "kind": kind,
        "priority": round(priority, 4),
        "current_status": current_status,
        "target_statement_id": target_id,
        "support_statement_id": source_id,
        "verdict": verdict,
        "next_status": _status_from_verdict(verdict),
        "recommended_action": _action_from_verdict(verdict),
        "support_score": round(support_score, 4),
        "refute_score": round(refute_score, 4),
        "confidence": round(confidence, 4),
        "inferential_commitment": {
            "support_antecedent_schema": str(hypothesis.get("support_antecedent_schema", "")).strip(),
            "target_consequence_schema": str(hypothesis.get("target_consequence_schema", "")).strip(),
            "preserved_invariant": str(hypothesis.get("preserved_invariant", "")).strip(),
            "barrier_scope": str(hypothesis.get("barrier_scope", "")).strip(),
        },
        "signals": {
            "analysis_score": round(analysis_score, 4),
            "lexical_overlap": round(lexical_overlap, 4),
            "structural_signature_overlap": round(lexical_overlap, 4),
            "semantic_overlap": round(semantic_overlap, 4),
            "symbol_role_alignment": round(symbol_role_alignment, 4),
            "theorem_family_similarity": round(theorem_family_similarity, 4),
            "direct_dependency": round(direct_dependency, 4),
            "contradiction_signal": round(contradiction, 4),
            "novelty_bonus": round(novelty_bonus, 4),
            "antecedent_alignment": round(antecedent_alignment, 4),
            "consequence_alignment": round(consequence_alignment, 4),
            "invariant_alignment": round(invariant_alignment, 4),
            "barrier_alignment": round(barrier_alignment, 4),
            "commitment_support": round(commitment_support, 4),
            "commitment_refute": round(commitment_refute, 4),
            "evidence_support_adjustment": round(support_delta, 4),
            "evidence_refute_adjustment": round(refute_delta, 4),
            "coherence_support_adjustment": round(coherence_support_delta, 4),
            "coherence_refute_adjustment": round(coherence_refute_delta, 4),
            "explanatory_power_local": coherence_signals["explanatory_power_local"],
            "coherence_delta_global": coherence_signals["coherence_delta_global"],
            "global_coherence_if_accepted": coherence_signals["global_coherence_if_accepted"],
        },
        "reasons": reasons,
    }


def evaluate_hypotheses(
    hypotheses: list[dict[str, Any]],
    statements: dict[str, dict[str, Any]],
    analysis_scores: dict[tuple[str, str], float] | None = None,
    evidence_by_hypothesis: dict[str, dict[str, Any]] | None = None,
    coherence_by_hypothesis: dict[str, dict[str, Any]] | None = None,
    coherence_profile: dict[str, Any] | None = None,
    support_threshold: float = 0.62,
    refute_threshold: float = 0.62,
    margin: float = 0.08,
    force_resolution: bool = False,
) -> dict[str, Any]:
    """Evaluate a heterogeneous hypothesis set with kind-specific scorers.

    Hypothesis kinds are dispatched to dedicated evaluators because
    intervention-focused and conceptual hypotheses expose different signals than
    bridge-link hypotheses.
    """
    analysis_scores = analysis_scores or {}
    evidence_by_hypothesis = evidence_by_hypothesis or {}
    coherence_by_hypothesis = coherence_by_hypothesis or {}
    coherence_profile = coherence_profile or {}
    max_downstream, max_unresolved = _intervention_maxima(hypotheses)

    results: list[dict[str, Any]] = []
    verdict_counts: dict[str, int] = {}
    status_counts: dict[str, int] = {}

    for hypothesis in hypotheses:
        if not isinstance(hypothesis, dict):
            continue
        kind = str(hypothesis.get("kind", "bridge-link")).strip().lower()
        # Dispatch by hypothesis semantics: each family has a different notion
        # of supporting/refuting evidence and risk.
        if kind == "intervention-focus":
            result = _evaluate_intervention_hypothesis(
                hypothesis=hypothesis,
                statements=statements,
                evidence_by_hypothesis=evidence_by_hypothesis,
                coherence_by_hypothesis=coherence_by_hypothesis,
                support_threshold=support_threshold,
                refute_threshold=refute_threshold,
                margin=margin,
                force_resolution=force_resolution,
                max_downstream=max_downstream,
                max_unresolved=max_unresolved,
            )
        elif kind in CONCEPTUAL_HYPOTHESIS_KINDS:
            result = _evaluate_conceptual_hypothesis(
                hypothesis=hypothesis,
                statements=statements,
                analysis_scores=analysis_scores,
                evidence_by_hypothesis=evidence_by_hypothesis,
                coherence_by_hypothesis=coherence_by_hypothesis,
                support_threshold=support_threshold,
                refute_threshold=refute_threshold,
                margin=margin,
                force_resolution=force_resolution,
            )
        else:
            result = _evaluate_bridge_hypothesis(
                hypothesis=hypothesis,
                statements=statements,
                analysis_scores=analysis_scores,
                evidence_by_hypothesis=evidence_by_hypothesis,
                coherence_by_hypothesis=coherence_by_hypothesis,
                support_threshold=support_threshold,
                refute_threshold=refute_threshold,
                margin=margin,
                force_resolution=force_resolution,
            )

        results.append(result)
        verdict = str(result.get("verdict", "inconclusive"))
        status = str(result.get("next_status", "needs-testing"))
        verdict_counts[verdict] = verdict_counts.get(verdict, 0) + 1
        status_counts[status] = status_counts.get(status, 0) + 1

    results.sort(
        key=lambda r: (
            _safe_float(r.get("priority"), 0.0),
            _safe_float(r.get("confidence"), 0.0),
            _safe_float(r.get("support_score"), 0.0),
        ),
        reverse=True,
    )

    return {
        "metadata": {
            "evaluated_utc": dt.datetime.now(dt.UTC).isoformat(),
            "hypothesis_count": len(results),
            "support_threshold": support_threshold,
            "refute_threshold": refute_threshold,
            "margin": margin,
            "force_resolution": force_resolution,
            "evidence_count": len(evidence_by_hypothesis),
            "coherence_signal_count": len(coherence_by_hypothesis),
            "global_coherence": _safe_float(coherence_profile.get("global_coherence"), 0.0),
        },
        "summary": {
            "verdict_counts": verdict_counts,
            "next_status_counts": status_counts,
        },
        "results": results,
    }


def apply_results_to_payload(
    payload: dict[str, Any],
    results: list[dict[str, Any]],
    round_index: int | None = None,
) -> dict[str, Any]:
    """Write evaluation results back into hypothesis payload state.

    The payload keeps a full evaluation history per hypothesis so later rounds
    can audit status transitions and supporting reasons.
    """
    by_id = {
        str(item.get("hypothesis_id", "")).strip(): item
        for item in results
        if isinstance(item, dict) and str(item.get("hypothesis_id", "")).strip()
    }

    hypotheses = payload.get("hypotheses", [])
    if not isinstance(hypotheses, list):
        return payload

    stamp = dt.datetime.now(dt.UTC).isoformat()

    for h in hypotheses:
        if not isinstance(h, dict):
            continue
        hid = str(h.get("id", "")).strip()
        if not hid or hid not in by_id:
            continue

        r = by_id[hid]
        h["status"] = str(r.get("next_status", h.get("status", "needs-testing")))
        evaluation_record = {
            "evaluated_utc": stamp,
            "round": round_index,
            "verdict": r.get("verdict"),
            "support_score": r.get("support_score"),
            "refute_score": r.get("refute_score"),
            "confidence": r.get("confidence"),
            "recommended_action": r.get("recommended_action"),
            "reasons": r.get("reasons", []),
        }
        hist = h.get("evaluation_history")
        if not isinstance(hist, list):
            hist = []
            h["evaluation_history"] = hist
        hist.append(evaluation_record)
        h["latest_evaluation"] = evaluation_record

    meta = payload.get("metadata")
    if not isinstance(meta, dict):
        meta = {}
        payload["metadata"] = meta
    meta["last_evaluated_utc"] = stamp
    if round_index is not None:
        meta["last_evaluation_round"] = round_index
    return payload


def is_resolved_status(status: str) -> bool:
    """
    Relevance: Operates within the shared utilities layer.
    Concept: Primary callable implementing a stage-level behavior.
    Contribution: Contributes a deterministic transformation that supports end-to-end reasoning reproducibility.
    """

    return status.strip().lower() in {"supported", "refuted"}
