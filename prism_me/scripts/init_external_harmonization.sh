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
  echo "Usage: bash prism_me/scripts/init_external_harmonization.sh <request-slug>" >&2
  exit 1
fi

slug="$1"
pack_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
request_root="$PWD/.prism/$slug"

if [ ! -d "$request_root" ]; then
  echo "Missing request workspace: $request_root" >&2
  echo "Run: bash prism_me/scripts/init_request.sh $slug" >&2
  exit 1
fi

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

render_template "$pack_root/shared/templates/02c-external-surface.md" "$request_root/02c-external-surface.md"
render_template "$pack_root/shared/templates/02d-external-capabilities.md" "$request_root/02d-external-capabilities.md"
render_template "$pack_root/shared/templates/02e-agentic-shape.md" "$request_root/02e-agentic-shape.md"
