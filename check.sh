#!/usr/bin/env bash
# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
set -uo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")" || exit 1
# Keep subprocess commands on the same locked environment as the check tools.
export PATH="$PWD/.venv/bin:$PATH"

status=0
run() {
  printf '\n+ %s\n' "$*"
  "$@" || status=1
}

run pytest
run ruff check .
run black --check .
run pyright
run vulture . --min-confidence 80
run python3 .idiap-sd/idiap_sd.py frontend-test
run reuse lint
run python3 .idiap-sd/idiap_sd.py check
exit "$status"
