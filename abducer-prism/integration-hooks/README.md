<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->
# Provider guard frontends

These files adapt native lifecycle events to the installed logical
`to-prism guard` command. They do not contain conversion policy and do not use
paths relative to this checkout.

- Codex: register `codex/hooks.json` as a trusted hook source. It uses only
  currently executable `command` handlers.
- Claude: merge the `hooks` object from `claude/settings.json` into the target
  settings layer. Do not replace unrelated project settings.
- OpenCode: install `opencode/to-prism-guards.ts` in the active project or
  global plugins directory. OpenCode hooks are executable plugin callbacks;
  there is no native declarative hook file to merge.

Installation is intentionally separate from conversion. The converter must
never write these files into an inspected source tree implicitly. A missing,
malformed, timed-out, or nonzero guard invocation fails closed.

Provider hooks are defense in depth. Source/output path separation, read-only
inspection, before/after fingerprints, staged generation, and publication
gates remain authoritative.
