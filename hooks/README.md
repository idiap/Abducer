<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->
# Native hooks and optional workflow policies

The native hook configuration and `scripts/` preserve the pre-normalization
behavior from Git revision `f90f0c6f`. Repository organization must not change
workflow composition or silently strengthen activation, step or stop rules.
The sole native helper adjustment maps relocated `docs/integrations/looper-*`
paths to their original `docs/looper-*` protection rule.

For example, the native pre-skill hook checks whether a controlled skill is
declared in a visible workflow. It does not require the activation receipt or
step-completion packet introduced by later workflow-local policies. Native stop
checks use the original required Looper artifacts. Native traces retain their
original latest-file behavior.

The later workflow-local extensions are retained in `workflow_local/` for
explicit callers and their separate tests. They are not registered in
`hooks.json` or `.codex/hooks.json`. An explicit caller may import
`hooks.workflow_local.pre_skill_use_policy`; this does not install or activate
that policy as a native hook. Its activation receipts and append-only traces
must not be attributed to the original native hook behavior.

Compatibility tests compare the baseline hook bytes and exercise original
accept, warn and block cases. Extension tests exercise only the explicitly
imported `hooks.workflow_local` package. A passing extension test is not evidence
that the native hook acquired that behavior.

The named-workflow task projection is stored under `registry/optional-tasks/`.
The native hook continues to read the original `registry/tasks/` namespace;
optional catalog generation therefore cannot enlarge its allowed skill set.
