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
"""Reject the historical raw-JSON proof launcher.

Current proof execution requires a live one-shot coordination capability that
cannot be reconstructed from a file or command line.  The dedicated launcher
will be exposed only at that in-process authority boundary.
"""

from __future__ import annotations

import argparse
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("handoff", type=Path)
    parser.add_argument("--run-directory", type=Path, required=True)
    parser.add_argument("--attempt-number", type=int, default=1)
    args = parser.parse_args()
    parser.error(
        "raw request/handoff JSON cannot carry current proof authority; "
        "use the in-process post-commit action-ledger capability route"
    )
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
