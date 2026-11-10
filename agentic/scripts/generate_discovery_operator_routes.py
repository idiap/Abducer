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
"""Explicitly refresh operator-route documentation from the executable registry."""

from __future__ import annotations

from discovery_operator_registry import ROUTES_DOC_PATH, load_registry, render_routes


def main() -> int:
    ROUTES_DOC_PATH.parent.mkdir(parents=True, exist_ok=True)
    ROUTES_DOC_PATH.write_text(render_routes(load_registry()), encoding="utf-8")
    print(ROUTES_DOC_PATH)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
