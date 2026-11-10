"""Construction and checking of staged theory-atlas objects."""

from __future__ import annotations

import re
from typing import Any

from tdr.domain.models import TheoryFragment, TheoryMorphism, stable_id


SECTION_PATTERNS = {
    "sort": re.compile(r"^\s*(?:sort|type)\s*[:=-]\s*(.+)$", re.I),
    "symbol": re.compile(r"^\s*(?:symbol|operation)\s*[:=-]\s*([^:]+):\s*(.+)$", re.I),
    "axiom": re.compile(r"^\s*(?:axiom|postulate)\s*[:=-]\s*(.+)$", re.I),
    "claim": re.compile(r"^\s*(?:claim|theorem|proposition)\s*[:=-]\s*(.+)$", re.I),
    "model": re.compile(r"^\s*(?:model|example)\s*[:=-]\s*(.+)$", re.I),
    "observable": re.compile(r"^\s*(?:observable|measurement)\s*[:=-]\s*(.+)$", re.I),
    "scope": re.compile(r"^\s*(?:scope|regime)\s*[:=-]\s*(.+)$", re.I),
}


def _source_content(source: Any) -> tuple[str, str, str]:
    if isinstance(source, str):
        return stable_id("source", source), "inline", source
    if not isinstance(source, dict):
        raise ValueError("each source must be text or an object")
    content = str(source.get("content", ""))
    source_id = str(source.get("artifact_id") or stable_id("source", content))
    locator = str(source.get("locator", "inline"))
    return source_id, locator, content


def map_fragment(payload: dict[str, Any]) -> TheoryFragment:
    """Extract a typed, source-addressable fragment without accepting it."""
    name = str(payload.get("name") or "Unnamed theory fragment")
    sources = payload.get("sources") or []
    if not sources:
        raise ValueError("at least one source is required")

    sorts: list[str] = list(payload.get("sorts", []))
    symbols: dict[str, str] = dict(payload.get("symbols", {}))
    axioms: list[str] = list(payload.get("axioms", []))
    claims: list[dict[str, Any]] = []
    models: list[str] = list(payload.get("models", []))
    observables: list[str] = list(payload.get("observables", []))
    regime: dict[str, Any] = dict(payload.get("regime", {}))
    source_refs: list[dict[str, Any]] = []

    for raw_source in sources:
        artifact_id, locator, content = _source_content(raw_source)
        source_refs.append({"artifact_id": artifact_id, "locator": locator})
        for line_number, line in enumerate(content.splitlines(), start=1):
            for kind, pattern in SECTION_PATTERNS.items():
                match = pattern.match(line)
                if not match:
                    continue
                ref = {"artifact_id": artifact_id, "locator": f"{locator}:L{line_number}"}
                if kind == "sort":
                    sorts.append(match.group(1).strip())
                elif kind == "symbol":
                    symbols[match.group(1).strip()] = match.group(2).strip()
                elif kind == "axiom":
                    axioms.append(match.group(1).strip())
                elif kind == "claim":
                    claims.append({"text": match.group(1).strip(), "source_ref": ref, "status": "sourced"})
                elif kind == "model":
                    models.append(match.group(1).strip())
                elif kind == "observable":
                    observables.append(match.group(1).strip())
                elif kind == "scope":
                    regime.setdefault("statements", []).append(match.group(1).strip())
                break

    for claim in payload.get("claims", []):
        if isinstance(claim, str):
            claims.append({"text": claim, "status": "conjecture", "source_ref": None})
        else:
            item = dict(claim)
            item.setdefault("status", "sourced" if item.get("source_ref") else "conjecture")
            claims.append(item)

    return TheoryFragment(
        fragment_id=str(payload.get("fragment_id") or stable_id("fragment", {"name": name, "sources": source_refs})),
        name=name,
        sorts=sorted(set(sorts)),
        symbols=dict(sorted(symbols.items())),
        axioms=list(dict.fromkeys(axioms)),
        claims=claims,
        models=list(dict.fromkeys(models)),
        observables=list(dict.fromkeys(observables)),
        regime=regime,
        source_refs=source_refs,
    )


def propose_morphism(payload: dict[str, Any]) -> TheoryMorphism:
    """Stage an interpretation map and emit every unproved satisfaction duty."""
    source = dict(payload.get("source_fragment") or {})
    target = dict(payload.get("target_fragment") or {})
    if not source or not target:
        raise ValueError("source_fragment and target_fragment are required")
    symbol_map = dict(payload.get("symbol_map") or {})
    declared = set((source.get("symbols") or {}).keys())
    missing = sorted(declared - symbol_map.keys())
    target_symbols = set((target.get("symbols") or {}).keys())
    unknown_targets = sorted({value for value in symbol_map.values() if value not in target_symbols})
    obligations = [f"map source symbol {name}" for name in missing]
    obligations.extend(f"establish target expression for {name}" for name in unknown_targets)
    obligations.extend(f"prove target satisfies image of axiom: {axiom}" for axiom in source.get("axioms", []))
    if source.get("regime") and not payload.get("scope_map"):
        obligations.append("supply a scope/regime preservation map")
    total = not missing and not unknown_targets
    return TheoryMorphism(
        morphism_id=str(payload.get("morphism_id") or stable_id("morphism", [source.get("fragment_id"), target.get("fragment_id"), symbol_map])),
        source_fragment_id=str(source.get("fragment_id", "unknown-source")),
        target_fragment_id=str(target.get("fragment_id", "unknown-target")),
        symbol_map=symbol_map,
        scope_map=dict(payload.get("scope_map") or {}),
        obligations=obligations,
        total_on_declared_domain=total,
    )

