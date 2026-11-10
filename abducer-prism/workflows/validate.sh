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

# Validate the immutable four-layer reasoning baseline and the additive, gap-aware
# materialization tranche. Prism imports resolve from the transferred toolkit root.
# Fake runs are typed integration smoke only; they do not execute source workflows,
# linked validators, or establish behavioral/epistemic equivalence.

set -euo pipefail

workflow_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
toolkit_root="$(cd "$workflow_dir/.." && pwd)"
repo_root="$(cd "$toolkit_root/.." && pwd)"
catalog="$repo_root/agentic/registries/reasoning_flow_catalog.yaml"
manifest="$workflow_dir/manifest.json"
prism="${PRISM_PATH:-$toolkit_root/.venv/bin/prism}"
taxonomy="$repo_root/.prism/import-abducer-prism-workflows/to-prism-state/conversion/project-semantic-taxonomy.json"
to_prism="$toolkit_root/bin/to-prism"

for command_name in jq rg diff find sort shasum python3; do
  command -v "$command_name" >/dev/null
done

test -x "$prism"
jq empty "$manifest"
"$to_prism" validate "$taxonomy" --schema project-semantic-taxonomy >/dev/null
python3 "$repo_root/.prism/refine-abducer-prism-semantic-names/validate_semantic_names.py"
python3 "$repo_root/.prism/refine-abducer-prism-reasoning-types/validate_reasoning_types.py" --self-test
python3 "$repo_root/.prism/add-abducer-prism-materialization-workflows/build_materializations.py" --mode self-test
python3 "$repo_root/.prism/add-abducer-prism-materialization-workflows/validate_materializations.py" --phase generated --self-test

diff -u \
  <(jq -r '.flows[].id' "$catalog" | sort) \
  <(jq -r '.workflows[].id' "$manifest" | sort)

test "$(find "$workflow_dir" -mindepth 2 -maxdepth 2 -type f -name '*.prism' ! -name 'sample_outputs.prism' | wc -l | tr -d ' ')" = 96
test "$(find "$workflow_dir" -mindepth 2 -maxdepth 2 -type f -name 'sample_outputs.prism' | wc -l | tr -d ' ')" = 19
test "$(find "$workflow_dir" -mindepth 3 -maxdepth 3 -type f -path '*/generated/*.prism' | wc -l | tr -d ' ')" = 47
test "$(find "$workflow_dir" -maxdepth 1 -type f -name '*.prism' | wc -l | tr -d ' ')" = 0

PYTHONDONTWRITEBYTECODE=1 python3 "$workflow_dir/validate_sample_outputs.py" --json >/dev/null

while IFS= read -r sample_path; do
  (
    cd "$toolkit_root"
    "$prism" check "workflows/$sample_path" >/dev/null
    "$prism" compile "workflows/$sample_path" >/dev/null
  )
done < <(find "$workflow_dir" -mindepth 2 -maxdepth 2 -type f -name 'sample_outputs.prism' -printf '%P\n' | sort)

while IFS=$'\t' read -r workflow_id module_id source_path; do
  test "$source_path" = "$module_id/reasoning.prism"
  module_root="$workflow_dir/$module_id"
  test -d "$module_root"

  for layer in types occurrences relations reasoning; do
    layer_path="$module_root/$layer.prism"
    test -f "$layer_path"
    (
      cd "$toolkit_root"
      "$prism" check "workflows/$module_id/$layer.prism" >/dev/null
      "$prism" compile "workflows/$module_id/$layer.prism" >/dev/null
    )
  done

  # Enforce the semantic ownership demonstrated by the layered toolkit example.
  ! rg -n '^(relation|reasoning|def|agent|workflow) ' "$module_root/types.prism"
  ! rg -n '^(relation|reasoning|def|agent|workflow) ' "$module_root/occurrences.prism"
  ! rg -n '^(reasoning|def|agent|workflow) ' "$module_root/relations.prism"
  ! rg -n '^(type|relation|def|agent|workflow) ' "$module_root/reasoning.prism"
  test "$(rg -c '^reasoning ' "$module_root/reasoning.prism")" = 1
  rg -q -- '-> Generated\[' "$module_root/occurrences.prism"
  rg -q '^relation ' "$module_root/relations.prism"
  rg -q '^# Layer: high-level epistemic topology only\.$' "$module_root/reasoning.prism"

  jq -r --arg id "$workflow_id" '
    .workflows[] | select(.id == $id) |
    [.source_workflow] + .contract_sources + .skill_bindings + .validator_bindings |
    .[] | select(.path != null) | [.path, .sha256] | @tsv
  ' "$manifest" | while IFS=$'\t' read -r linked_path linked_hash; do
    if test -f "$repo_root/$linked_path"; then
      linked_file="$repo_root/$linked_path"
    else
      linked_file="$repo_root/$linked_path/SKILL.md"
    fi
    test -f "$linked_file"
    test "sha256:$(shasum -a 256 "$linked_file" | awk '{print $1}')" = "$linked_hash"
  done
done < <(jq -r '.workflows[] | [.id, .module_id, .source] | @tsv' "$manifest")

while IFS= read -r module_id; do
  module_root="$workflow_dir/$module_id"
  for upper_layer in materialization main; do
    test -f "$module_root/$upper_layer.prism"
    (
      cd "$toolkit_root"
      "$prism" check "workflows/$module_id/$upper_layer.prism" >/dev/null
      "$prism" compile "workflows/$module_id/$upper_layer.prism" >/dev/null
    )
  done
done < <(jq -r '.workflows[] | select(.materialization.status == "linked_fake_handler_smoke") | .module_id' "$manifest")

python3 "$repo_root/.prism/add-abducer-prism-materialization-workflows/validate_smoke_runs.py" --write-evidence

while IFS= read -r generated_skill; do
  (
    cd "$toolkit_root"
    "$prism" check "workflows/$generated_skill" >/dev/null
    "$prism" compile "workflows/$generated_skill" >/dev/null
  )
done < <(jq -r '.workflows[].materialization.occurrence_bindings[]?.compiled_skill' "$manifest")

while IFS= read -r module_id; do
  test ! -e "$workflow_dir/$module_id/materialization.prism"
  test ! -e "$workflow_dir/$module_id/main.prism"
  test ! -e "$workflow_dir/$module_id/generated"
done < <(jq -r '.workflows[] | select(.materialization.status == "blocked_unresolved_projection_gap") | .module_id' "$manifest")

python3 "$workflow_dir/validate_fixture.py" --self-test

echo "validated 19 reasoning workflows: 76 semantic modules; 19 documentary samples; 10 materializations, 10 mains, 47 compiled skills; 9 explicit blockers"
