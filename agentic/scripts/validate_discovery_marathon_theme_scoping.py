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
"""Validate that discovery marathon reports are isolated by target/theme."""

from __future__ import annotations

import re
import json
import html as html_lib
from pathlib import Path

from agentic_common import ROOT, clean_text, fail, load_optional_json, rel
from discovery_marathon_common import (
    LATEST_HTML,
    LATEST_JSON,
    LATEST_MD,
    LATEST_TIMELINE_HTML,
    TARGET_ACTIVE_DIR,
    read_report_target_id,
    target_report_paths,
)


MATHJAX_SCRIPT_RE = re.compile(r'<script data-embedded-dependency="mathjax-tex-svg">.*?</script>', re.DOTALL)
MARATHON_DATA_RE = re.compile(r'<script id="marathon-data" type="application/json">(.*?)</script>', re.DOTALL)
INLINE_TEX_RE = re.compile(r"\\\((.*?)\\\)", re.DOTALL)
DISPLAY_TEX_RE = re.compile(r"\\\[(.*?)\\\]", re.DOTALL)
UNBRACED_ACCENT_RE = re.compile(r"\\(?:widehat|overline)(?!\{)")
UNRENDERED_OS_FUNCTION_RE = re.compile(
    r"(?<![A-Za-z0-9_\\])S(?:_\{[^}]+\}|_[A-Za-z0-9]+)?\([^.;<>]*(?:\\Theta|Theta|W\(|T_\{?\\?delta\}?)[^.;<>]*\)"
)


def active_target_ids() -> list[str]:
    if not TARGET_ACTIVE_DIR.exists():
        return []
    target_ids: list[str] = []
    for path in sorted(TARGET_ACTIVE_DIR.glob("*.json")):
        pointer = load_optional_json(path)
        target_id = clean_text(pointer.get("target_id"))
        if target_id:
            target_ids.append(target_id)
    return target_ids


def validate_declared_target(path: Path, expected_target_id: str) -> None:
    if not path.exists():
        fail(f"missing target-scoped report artifact {rel(path)}")
    declared = read_report_target_id(path)
    if declared != expected_target_id:
        fail(f"{rel(path)} declares target `{declared or 'unknown'}`, expected `{expected_target_id}`")
    if path.suffix == ".html":
        document = MATHJAX_SCRIPT_RE.sub("", path.read_text(encoding="utf-8"))
        validate_rendered_accent_arguments(document, path)


def validate_rendered_accent_arguments(document: str, path: Path) -> None:
    def check_latex(latex: str, context: str) -> None:
        match = UNBRACED_ACCENT_RE.search(html_lib.unescape(latex))
        if match:
            fail(f"{rel(path)} {context} contains unbraced TeX accent `{match.group(0)}`; use a braced argument")

    def check_rendered_math_coverage(rendered_html: str, context: str) -> None:
        prose = html_lib.unescape(rendered_html)
        prose = INLINE_TEX_RE.sub("", prose)
        prose = DISPLAY_TEX_RE.sub("", prose)
        match = UNRENDERED_OS_FUNCTION_RE.search(prose)
        if match:
            fail(f"{rel(path)} {context} leaves OS function formula outside TeX delimiters: `{match.group(0)}`")

    static_document = MARATHON_DATA_RE.sub("", document)
    check_rendered_math_coverage(static_document, "static document")
    for index, match in enumerate(INLINE_TEX_RE.finditer(static_document), start=1):
        check_latex(match.group(1), f"static inline TeX fragment {index}")
    for index, match in enumerate(DISPLAY_TEX_RE.finditer(static_document), start=1):
        check_latex(match.group(1), f"static display TeX fragment {index}")
    payload_match = MARATHON_DATA_RE.search(document)
    if not payload_match:
        return
    try:
        payload = json.loads(html_lib.unescape(payload_match.group(1)))
    except json.JSONDecodeError as exc:
        fail(f"{rel(path)} has invalid embedded marathon-data JSON: {exc}")

    def walk(value: object, stack: list[str]) -> None:
        if isinstance(value, dict):
            for key, child in value.items():
                walk(child, [*stack, str(key)])
        elif isinstance(value, list):
            for index, child in enumerate(value):
                walk(child, [*stack, str(index)])
        elif isinstance(value, str) and stack:
            key = stack[-1]
            if key == "latex_render":
                check_latex(value, "/".join(stack))
            elif key.endswith("_html") or key == "html":
                check_rendered_math_coverage(value, "/".join(stack))
                for index, match in enumerate(INLINE_TEX_RE.finditer(html_lib.unescape(value)), start=1):
                    check_latex(match.group(1), f"{'/'.join(stack)} inline TeX fragment {index}")
                for index, match in enumerate(DISPLAY_TEX_RE.finditer(html_lib.unescape(value)), start=1):
                    check_latex(match.group(1), f"{'/'.join(stack)} display TeX fragment {index}")

    walk(payload, ["marathon-data"])


def validate_generic_compatibility_paths() -> None:
    existing = [path for path in [LATEST_JSON, LATEST_MD, LATEST_HTML, LATEST_TIMELINE_HTML] if path.exists()]
    if not existing:
        return
    declarations = {rel(path): read_report_target_id(path) for path in existing}
    declared_targets = {target for target in declarations.values() if target}
    if len(declared_targets) > 1:
        fail(f"generic discovery marathon report files disagree on target scope: {declarations}")


def main() -> int:
    targets = active_target_ids()
    if not targets:
        print("No target-specific discovery marathon pointers found; scoping validator is idle.")
        return 0
    for target_id in targets:
        paths = target_report_paths(target_id)
        for key in ["latest_json", "latest_md", "latest_html", "full_timeline_html"]:
            validate_declared_target(paths[key], target_id)
    validate_generic_compatibility_paths()
    print(f"validated target-scoped discovery marathon reports for {len(targets)} targets under {rel(ROOT / 'agentic/reports/discovery_marathon/targets')}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
