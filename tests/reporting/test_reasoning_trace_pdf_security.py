# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "agentic/scripts"))

from generate_public_reasoning_trace_latex import render_tex
from reasoning_trace_print_model import build_print_inventory
from reasoning_trace_tex_safety import tex_escape
from validate_public_reasoning_trace_pdf import EXPECTED_STEMS, companion_paths


def test_hostile_packet_text_is_inert_and_visible() -> None:
    packet = json.loads(companion_paths("theorem_proof_delivery")["packet"].read_text(encoding="utf-8"))
    attack = r"\input{/etc/passwd} \write18{touch OWNED} % } $ & # _ ^ ~"
    packet["inferences"][0]["conclusion"] = attack
    inventory = build_print_inventory(packet)
    tex = render_tex(packet, inventory)
    assert attack not in tex
    assert r"\textbackslash{}input" in tex
    assert "DACTED ABSOLUTE LOCAL PATH" in tex
    assert r"\textbackslash{}write18" in tex
    assert r"\input{/etc/passwd}" not in tex
    assert r"\write18{touch OWNED}" not in tex


def test_manifests_record_no_shell_escape_and_no_absolute_arguments() -> None:
    for stem in sorted(EXPECTED_STEMS):
        manifest = json.loads(companion_paths(stem)["manifest"].read_text(encoding="utf-8"))
        arguments = manifest["compiler"]["arguments"]
        assert "-no-shell-escape" in arguments
        assert not any(Path(argument).is_absolute() for argument in arguments)
