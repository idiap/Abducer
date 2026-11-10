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

"""Build parallel mathematical representations for theorem packets."""

from __future__ import annotations

import re
from typing import Any


def _clean_text(value: Any) -> str:
    return " ".join(str(value or "").strip().split())


def _strip_ticks(value: Any) -> str:
    return _clean_text(value).replace("`", "")


def _camel_case(value: Any, *, default: str) -> str:
    tokens = re.findall(r"[A-Za-z0-9]+", _strip_ticks(value))
    if not tokens:
        return default
    return "".join(token[:1].upper() + token[1:] for token in tokens)


def _snake_case(value: Any, *, default: str) -> str:
    tokens = re.findall(r"[A-Za-z0-9]+", _strip_ticks(value).lower())
    return "_".join(tokens) if tokens else default


def _symbol_ledger(
    *,
    bridge_name: str,
    invariant: str,
    witness_shape: str,
) -> list[dict[str, str]]:
    return [
        {
            "symbol": "W",
            "latex": "W",
            "lean": "W",
            "meaning": f"an admissible {bridge_name}",
        },
        {
            "symbol": "R(W)",
            "latex": r"\mathcal{R}(W)",
            "lean": "RouteObj W",
            "meaning": f"the route-side operationalization attached to {bridge_name}",
        },
        {
            "symbol": "T(W)",
            "latex": r"\mathcal{T}(W)",
            "lean": "TargetObj W",
            "meaning": "the target-side operationalization relevant to the queued theorem",
        },
        {
            "symbol": "BW(W)",
            "latex": r"\mathsf{BW}(W)",
            "lean": "BridgeWitness W",
            "meaning": witness_shape,
        },
        {
            "symbol": "Adm(W)",
            "latex": r"\mathrm{Adm}(W)",
            "lean": "Admissible W",
            "meaning": f"W satisfies the local admissibility conditions for {bridge_name}",
        },
        {
            "symbol": "PresInv(W, w)",
            "latex": r"\mathrm{PresInv}(W,w)",
            "lean": "PresInv W w",
            "meaning": invariant or "the witness preserves the named route invariant",
        },
        {
            "symbol": "RealizesTarget(W, w)",
            "latex": r"\mathrm{RealizesTarget}(W,w)",
            "lean": "RealizesTarget W w",
            "meaning": "the witness is strong enough to activate the local target claim",
        },
    ]


def _witness_shape(mode: str) -> str:
    normalized = _clean_text(mode).lower()
    if normalized == "equivalence-theorem":
        return "an equivalence witness between the route-side and target-side operationalizations"
    if normalized == "transport-lemma":
        return "a transport map from the route-side object into the target-side object"
    if normalized == "no-go-theorem":
        return "a would-be witness whose nonexistence would certify the barrier"
    if normalized == "threshold-version":
        return "a threshold-sensitive witness valid in the restricted regime"
    return "a mediating object together with the maps needed by the route"


def _latex_theorem(mode: str) -> str:
    normalized = _clean_text(mode).lower()
    if normalized == "no-go-theorem":
        return (
            r"\forall W,\ \mathrm{Adm}(W) \to "
            r"\neg \exists w : \mathsf{BW}(W),\ \mathrm{PresInv}(W,w) \wedge \mathrm{RealizesTarget}(W,w)."
        )
    if normalized == "threshold-version":
        return (
            r"\exists \theta,\ \forall W,\ \mathrm{Adm}_{\theta}(W) \to "
            r"\exists w : \mathsf{BW}(W),\ \mathrm{PresInv}(W,w) \wedge \mathrm{RealizesTarget}(W,w)."
        )
    return (
        r"\forall W,\ \mathrm{Adm}(W) \to "
        r"\exists w : \mathsf{BW}(W),\ \mathrm{PresInv}(W,w) \wedge \mathrm{RealizesTarget}(W,w)."
    )


def _lean_comment_lines(
    *,
    title: str,
    route_synopsis: str,
    invariant: str,
    source_id: str,
    target_id: str,
) -> list[str]:
    lines = [
        "-- Lean-style type-theory scaffold.",
        "-- This is a notation-oriented proof packet, not executable Lean.",
    ]
    if title:
        lines.append(f"-- theorem under test: {title}")
    if route_synopsis:
        lines.append(f"-- route synopsis: {route_synopsis}")
    if invariant:
        lines.append(f"-- preserved invariant: {invariant}")
    if source_id or target_id:
        lines.append(f"-- route: {source_id or '?'} -> {target_id or '?'}")
    return lines


def _lean_scaffold(
    *,
    mode: str,
    title: str,
    bridge_name: str,
    invariant: str,
    route_synopsis: str,
    source_id: str,
    target_id: str,
    admissibility_conditions: list[str],
    first_lemma_title: str,
    negative_barrier_version: str,
) -> str:
    bridge_type = _camel_case(bridge_name, default="BridgeCarrier")
    theorem_name = _snake_case(title or "route theorem", default="route_theorem")
    lemma_name = _snake_case(first_lemma_title or "first lemma", default="first_lemma")
    normalized_mode = _clean_text(mode).lower()
    witness_hint = _witness_shape(normalized_mode)
    lines = _lean_comment_lines(
        title=title,
        route_synopsis=route_synopsis,
        invariant=invariant,
        source_id=source_id,
        target_id=target_id,
    )
    if admissibility_conditions:
        lines.append("-- admissibility conditions:")
        lines.extend(f"--   - {item}" for item in admissibility_conditions[:4])
    lines.extend(
        [
            f"constant {bridge_type} : Type",
            f"constant Admissible : {bridge_type} -> Prop",
            f"constant RouteObj : {bridge_type} -> Type",
            f"constant TargetObj : {bridge_type} -> Type",
            f"-- BridgeWitness W should be read as {witness_hint}.",
            f"constant BridgeWitness : {bridge_type} -> Type",
            f"constant PresInv : (W : {bridge_type}) -> BridgeWitness W -> Prop",
            f"constant RealizesTarget : (W : {bridge_type}) -> BridgeWitness W -> Prop",
        ]
    )
    if normalized_mode == "threshold-version":
        lines.extend(
            [
                f"constant Threshold : {bridge_type} -> Prop",
                "",
                f"theorem {theorem_name}",
                f"    (W : {bridge_type})",
                f"    (hW : Admissible W)",
                f"    (hth : Threshold W) :",
                "    exists w : BridgeWitness W, PresInv W w /\\ RealizesTarget W w",
            ]
        )
    elif normalized_mode == "no-go-theorem":
        lines.extend(
            [
                "",
                f"theorem {theorem_name}",
                f"    (W : {bridge_type})",
                f"    (hW : Admissible W) :",
                "    not (exists w : BridgeWitness W, PresInv W w /\\ RealizesTarget W w)",
            ]
        )
    else:
        lines.extend(
            [
                "",
                f"theorem {theorem_name}",
                f"    (W : {bridge_type})",
                f"    (hW : Admissible W) :",
                "    exists w : BridgeWitness W, PresInv W w /\\ RealizesTarget W w",
            ]
        )
    lines.extend(
        [
            "",
            f"theorem {lemma_name}",
            f"    (W : {bridge_type})",
            f"    (hW : Admissible W) :",
            "    exists w : BridgeWitness W, PresInv W w",
        ]
    )
    if negative_barrier_version:
        barrier_name = _snake_case(f"{title} barrier", default="route_barrier")
        lines.extend(
            [
                "",
                f"-- barrier variant: {negative_barrier_version}",
                f"theorem {barrier_name}",
                f"    (W : {bridge_type})",
                f"    (hW : Admissible W) :",
                "    not (exists w : BridgeWitness W, PresInv W w /\\ RealizesTarget W w)",
            ]
        )
    return "\n".join(line.rstrip() for line in lines if line is not None).strip()


def build_mathematical_layers(
    *,
    title: Any,
    exact_statement: Any,
    route_synopsis: Any,
    bridge_name: Any,
    invariant: Any,
    mode: Any,
    source_statement_id: Any = "",
    target_statement_id: Any = "",
    source_excerpt: Any = "",
    target_excerpt: Any = "",
    admissibility_conditions: list[Any] | None = None,
    first_nontrivial_lemma_title: Any = "",
    first_nontrivial_lemma_statement: Any = "",
    negative_barrier_version: Any = "",
) -> dict[str, Any]:
    title_text = _clean_text(title)
    exact_statement_text = _clean_text(exact_statement)
    route_synopsis_text = _clean_text(route_synopsis)
    bridge_name_text = _strip_ticks(bridge_name) or "bridge object"
    invariant_text = _strip_ticks(invariant) or "named route invariant"
    mode_text = _clean_text(mode)
    source_id = _clean_text(source_statement_id)
    target_id = _clean_text(target_statement_id)
    source_excerpt_text = _clean_text(source_excerpt)
    target_excerpt_text = _clean_text(target_excerpt)
    admissibility = [_clean_text(item) for item in (admissibility_conditions or []) if _clean_text(item)]
    first_lemma_title = _clean_text(first_nontrivial_lemma_title)
    first_lemma_statement = _clean_text(first_nontrivial_lemma_statement)
    negative_text = _clean_text(negative_barrier_version)
    witness_shape = _witness_shape(mode_text)
    return {
        "status": "generated",
        "representation_kind": "informal-latex-lean-style",
        "quantifier_signature": (
            f"For every admissible `{bridge_name_text}` on the route from `{source_id}` to `{target_id}`."
            if source_id or target_id
            else f"For every admissible `{bridge_name_text}`."
        ),
        "object_signature": {
            "bridge_object": bridge_name_text,
            "route_object": "R(W)",
            "target_object": "T(W)",
            "bridge_witness": "BW(W)",
            "invariant": invariant_text,
        },
        "symbol_ledger": _symbol_ledger(
            bridge_name=bridge_name_text,
            invariant=invariant_text,
            witness_shape=witness_shape,
        ),
        "informal": {
            "exact_statement": exact_statement_text,
            "route_synopsis": route_synopsis_text,
            "source_excerpt": source_excerpt_text,
            "target_excerpt": target_excerpt_text,
            "first_nontrivial_lemma": first_lemma_statement,
            "negative_barrier_version": negative_text,
        },
        "latex": {
            "theorem_statement": _latex_theorem(mode_text),
            "first_nontrivial_lemma": first_lemma_statement,
            "negative_barrier_version": negative_text,
            "gloss": (
                f"`BridgeWitness` should be read as {witness_shape}; "
                f"`PresInv` stands for preserving `{invariant_text}`."
            ),
        },
        "lean_style": {
            "status": "non-executable-scaffold",
            "theorem_name": _snake_case(title_text or "route theorem", default="route_theorem"),
            "scaffold": _lean_scaffold(
                mode=mode_text,
                title=title_text,
                bridge_name=bridge_name_text,
                invariant=invariant_text,
                route_synopsis=route_synopsis_text,
                source_id=source_id,
                target_id=target_id,
                admissibility_conditions=admissibility,
                first_lemma_title=first_lemma_title,
                negative_barrier_version=negative_text,
            ),
        },
    }
