<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->
# Codex Control Stack

This reference explains how `prism_me` hardens skill execution inside a Codex IDE or CLI workspace.

The goal is simple: keep `AGENTS.md` and the skills as the semantic layer, then add deterministic local controls around them so stage order, artifact discipline, and risky shell behavior do not depend only on prose.

## Layers

Use the stack in this order:

1. `AGENTS.md` for repository intent, norms, and human-readable workflow semantics.
2. `prism_me` skills for staged procedures and artifact-specific playbooks.
3. `prism_me/scripts/prism_control.py` as the deterministic local control plane.
4. `.codex/hooks.json` for lifecycle checks and extra developer context.
5. `.codex/rules/prism-me.rules` for shell-prefix decisions when Codex requests work outside the sandbox.
6. `.codex/config.toml` for repo-local feature flags and approval hardening.

## What The Control Plane Does

`prism_me/scripts/prism_control.py` is the local workflow CLI. It is the place to encode repeatable control logic instead of scattering that logic across free-form skill prose.

It currently provides:

- `status`: inspect the active request slug, current stage, next artifact, and next skill.
- `next`: print the next recommended Prism step in a short operator-friendly form.
- `validate`: verify that the repo-local Codex control files exist and parse cleanly.
- `review-complete`: mark the current persona review complete and advance the next automatic review threshold.
- hook entrypoints for session start, prompt submission, shell preflight checks, and shell post-check reminders.

## Hook Behavior

The repo-local `hooks.json` wires Codex lifecycle events into `prism_control.py`.

- `SessionStart`: injects concise Prism control context at startup and resume time.
- `UserPromptSubmit`: reinforces explicit orchestrator-first routing and blocks obvious requests to bypass the control surfaces.
- `PreToolUse`: blocks a small set of destructive shell patterns and rejects ad hoc shell mutation of `.prism/` and `to-do.md` when the control scripts should be used instead.
- `PostToolUse` on `Bash`: reminds Codex to capture request initialization and test evidence after shell steps that matter to Prism accounting.
- `PostToolUse` on `Edit|Write`: counts committed code-generation cycles and marks persona review due every 50 cycles. On-demand and final release-gate reviews remain independent of the counter.

This is a guardrail, not a perfect enforcement boundary. The current Codex hook runtime can intercept `Bash` and edit or write tools, but interception is still incomplete for some shell paths and tool variants.

## Rules Scope

The repo-local `.rules` file is for sandbox-escape decisions, not routine in-workspace shell work.

Use rules to:

- forbid obviously destructive escalations,
- require prompts for history-rewriting Git operations,
- allow clearly safe read-only escalations when the user chooses to grant them.

Keep the rules file narrow. The repo-local hook layer is a better place for Prism-specific workflow checks.

## Operating Expectations

When using `prism_me` in this controlled mode:

1. Start request work with `prism-spec-orchestrator`.
2. Bootstrap workspaces with `bash prism_me/scripts/init_request.sh <request-slug>` instead of hand-making `.prism/` trees.
3. Check state with `python3 prism_me/scripts/prism_control.py status`.
4. Treat persona review as due work every time the edit or write counter hits 50 new committed cycles; retain on-demand and final release-gate review independently.
5. Keep `to-do.md` and `.prism/<request-slug>/00-skill-coverage-checklist.md` synchronized with the actual stage.
6. Record shell-driven checks in the request artifacts instead of leaving them implicit in chat history.

## Recommended Commands

Use these from the repository root:

```bash
python3 prism_me/scripts/prism_control.py status
python3 prism_me/scripts/prism_control.py next
python3 prism_me/scripts/prism_control.py validate
python3 prism_me/scripts/prism_control.py review-complete
```

When the workspace is clean but the request has not started yet:

```bash
bash prism_me/scripts/init_request.sh <request-slug>
```

If the source starts outside Prism:

```bash
bash prism_me/scripts/init_external_harmonization.sh <request-slug>
```
