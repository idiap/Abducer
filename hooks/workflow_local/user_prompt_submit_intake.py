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
from __future__ import annotations

from .hook_utils import emit, matching_named_workflows, read_payload, trace


CONTROL_TERMS = ("systematically navigate", "fully", "end to end", "recursive", "keep working", "controlled", "goal-oriented")


def main() -> int:
    payload = read_payload()
    prompt = str(payload.get("prompt", "")).lower()
    facts = payload.get("trigger_facts", {})
    recommendations = matching_named_workflows(facts) if isinstance(facts, dict) else []
    if recommendations:
        result = {
            "decision": "warn",
            "reason": "Structured trigger facts match named workflows; explicit activation is still required.",
            "workflow_recommendations": recommendations,
            "activation_authorized": False,
        }
    elif any(term in prompt for term in CONTROL_TERMS):
        result = {
            "decision": "warn",
            "reason": "Controlled target-navigation language detected; require target packet and workflow registry evidence.",
            "suggested_skill": "looper-target-goal-enricher",
            "activation_authorized": False,
        }
    else:
        result = {
            "decision": "accept",
            "reason": "No deterministic named-workflow trigger matched.",
            "activation_authorized": False,
        }
    trace("user_prompt_submit_intake", payload, result)
    emit(**result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
