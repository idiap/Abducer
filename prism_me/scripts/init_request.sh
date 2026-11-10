#!/usr/bin/env bash
# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT

set -euo pipefail

if [ "$#" -ne 1 ]; then
  echo "Usage: bash prism_me/scripts/init_request.sh <request-slug>" >&2
  exit 1
fi

slug="$1"

case "$slug" in
  "" | *[!A-Za-z0-9._-]*)
    echo "Request slug may contain only letters, digits, dot, underscore, and hyphen." >&2
    exit 1
    ;;
esac

pack_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
request_root="$PWD/.prism/$slug"
todo_path="$PWD/to-do.md"
mkdir -p "$request_root"

render_template() {
  local template_path="$1"
  local output_path="$2"

  if [ -e "$output_path" ]; then
    echo "skip  $output_path"
    return
  fi

  sed "s/<request-slug>/$slug/g" "$template_path" > "$output_path"
  echo "write $output_path"
}

render_template "$pack_root/shared/templates/01-spec.md" "$request_root/01-spec.md"
render_template "$pack_root/shared/templates/02-agent-contract.yaml" "$request_root/02-agent-contract.yaml"
render_template "$pack_root/shared/templates/02b-quality-criteria.md" "$request_root/02b-quality-criteria.md"
render_template "$pack_root/shared/templates/03-repo-map.md" "$request_root/03-repo-map.md"
render_template "$pack_root/shared/templates/03b-dependency-map.md" "$request_root/03b-dependency-map.md"
render_template "$pack_root/shared/templates/04-slice-plan.md" "$request_root/04-slice-plan.md"
render_template "$pack_root/shared/templates/04b-test-strategy.md" "$request_root/04b-test-strategy.md"
render_template "$pack_root/shared/templates/05-execution-log.md" "$request_root/05-execution-log.md"
render_template "$pack_root/shared/templates/05b-refinement-loop.md" "$request_root/05b-refinement-loop.md"
render_template "$pack_root/shared/templates/05c-test-evidence.md" "$request_root/05c-test-evidence.md"
render_template "$pack_root/shared/templates/05d-persona-review.md" "$request_root/05d-persona-review.md"
render_template "$pack_root/shared/templates/06-verification.md" "$request_root/06-verification.md"
render_template "$pack_root/shared/templates/07-handoff.md" "$request_root/07-handoff.md"
render_template "$pack_root/shared/templates/reasoning-log.md" "$request_root/reasoning-log.md"
render_template "$pack_root/shared/templates/00-skill-coverage-checklist.md" "$request_root/00-skill-coverage-checklist.md"

if [ ! -e "$todo_path" ]; then
  cp "$pack_root/shared/templates/to-do.md" "$todo_path"
  echo "write $todo_path"
else
  echo "skip  $todo_path"
fi
