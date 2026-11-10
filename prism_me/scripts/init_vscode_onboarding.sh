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

workspace_root="$PWD"
pack_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
vscode_dir="$workspace_root/.vscode"
codex_dir="$workspace_root/.codex"
codex_rules_dir="$codex_dir/rules"
agents_path="$workspace_root/AGENTS.md"
tasks_path="$vscode_dir/tasks.json"
todo_path="$workspace_root/to-do.md"
codex_config_path="$codex_dir/config.toml"
codex_hooks_path="$codex_dir/hooks.json"
codex_rules_path="$codex_rules_dir/prism-me.rules"

mkdir -p "$vscode_dir"
mkdir -p "$codex_rules_dir"

if [ ! -e "$agents_path" ]; then
  cat > "$agents_path" <<'EOF'
# Workspace Agent Onboarding

This workspace uses `prism_me` for spec-driven agentic development.

Read these first:

1. `prism_me/agents.md`
2. `to-do.md`
3. `.prism/<request-slug>/00-skill-coverage-checklist.md`
4. `prism_me/shared/references/codex-control-stack.md`

Quick start:

```bash
bash prism_me/scripts/init_request.sh <request-slug>
```

External-source route:

```bash
bash prism_me/scripts/init_external_harmonization.sh <request-slug>
```

Default coordinator:

- `prism-spec-orchestrator`

Primary workspace:

- `.prism/<request-slug>/`

Root control files:

- `to-do.md`
- `.codex/config.toml`
- `.codex/hooks.json`
- `.codex/rules/prism-me.rules`

Control commands:

```bash
python3 prism_me/scripts/prism_control.py status
python3 prism_me/scripts/prism_control.py next
python3 prism_me/scripts/prism_control.py validate
python3 prism_me/scripts/prism_control.py review-complete
```

Hard rules:

1. Start with `prism-spec-orchestrator` before any deeper skill work.
2. Keep the root `to-do.md` and the skill coverage checklist synchronized with the current request state.
3. Do not leave any `prism_me` skill without an explicit disposition of `used`, `not-applicable`, `deferred`, or `blocked`.
4. Do not skip quality criteria, testing, reflective refinement, annotation, dependency mapping, or external harmonization without writing the reason in the request artifacts.
5. When the control stack marks persona review due after 50 committed edit or write cycles, route through the persona-review lane and record the resulting TODOs. Keep on-demand and final release-gate reviews available.
6. Do not mark a request ready for handoff until the coverage checklist, `to-do.md`, verification, and handoff all agree.

Optional Prism-core mirror templates:

- `prism_me/shared/templates/02f-skill-contract-profile.yaml`
- `prism_me/shared/templates/02g-composition-model.yaml`
EOF
  echo "write $agents_path"
else
  echo "skip  $agents_path"
fi

if [ ! -e "$todo_path" ]; then
  cp "$pack_root/shared/templates/to-do.md" "$todo_path"
  echo "write $todo_path"
else
  echo "skip  $todo_path"
fi

if [ ! -e "$codex_config_path" ]; then
  cp "$pack_root/shared/templates/codex-config.toml" "$codex_config_path"
  echo "write $codex_config_path"
else
  echo "skip  $codex_config_path"
fi

if [ ! -e "$codex_hooks_path" ]; then
  cp "$pack_root/shared/templates/codex-hooks.json" "$codex_hooks_path"
  echo "write $codex_hooks_path"
else
  echo "skip  $codex_hooks_path"
fi

if [ ! -e "$codex_rules_path" ]; then
  cp "$pack_root/shared/templates/prism-me.rules" "$codex_rules_path"
  echo "write $codex_rules_path"
else
  echo "skip  $codex_rules_path"
fi

if [ ! -e "$tasks_path" ]; then
  cat > "$tasks_path" <<'EOF'
{
  "version": "2.0.0",
  "inputs": [
    {
      "id": "prismRequestSlug",
      "type": "promptString",
      "description": "Prism ME request slug"
    }
  ],
  "tasks": [
    {
      "label": "Prism ME: Init Request Workspace",
      "type": "shell",
      "command": "bash",
      "args": [
        "prism_me/scripts/init_request.sh",
        "${input:prismRequestSlug}"
      ],
      "problemMatcher": []
    },
    {
      "label": "Prism ME: Init External Harmonization",
      "type": "shell",
      "command": "bash",
      "args": [
        "prism_me/scripts/init_external_harmonization.sh",
        "${input:prismRequestSlug}"
      ],
      "problemMatcher": []
    },
    {
      "label": "Prism ME: VSCode Onboarding",
      "type": "shell",
      "command": "bash",
      "args": [
        "prism_me/scripts/init_vscode_onboarding.sh"
      ],
      "problemMatcher": []
    },
    {
      "label": "Prism ME: Control Status",
      "type": "shell",
      "command": "python3",
      "args": [
        "prism_me/scripts/prism_control.py",
        "status"
      ],
      "problemMatcher": []
    },
    {
      "label": "Prism ME: Control Next Step",
      "type": "shell",
      "command": "python3",
      "args": [
        "prism_me/scripts/prism_control.py",
        "next"
      ],
      "problemMatcher": []
    },
    {
      "label": "Prism ME: Validate Control Stack",
      "type": "shell",
      "command": "python3",
      "args": [
        "prism_me/scripts/prism_control.py",
        "validate"
      ],
      "problemMatcher": []
    },
    {
      "label": "Prism ME: Mark Persona Review Complete",
      "type": "shell",
      "command": "python3",
      "args": [
        "prism_me/scripts/prism_control.py",
        "review-complete"
      ],
      "problemMatcher": []
    },
    {
      "label": "Prism ME: Open Root To-Do",
      "type": "shell",
      "command": "sed",
      "args": [
        "-n",
        "1,200p",
        "to-do.md"
      ],
      "problemMatcher": []
    }
  ]
}
EOF
  echo "write $tasks_path"
else
  echo "skip  $tasks_path"
fi
