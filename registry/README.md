<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->
# Abducer Workflow Registry

`registry/` makes Looper-controlled Abducer work visible as workflow
composition. The user-facing unit is the workflow. Skills, hooks, artifacts,
validators, and reports are the supporting parts.

Each task lives under `registry/tasks/<task-id>/task_registry.json` and must put
`visible_workflows` first in the operational interpretation of the task.

Validate with:

```bash
python agentic/scripts/validate_task_skill_registry.py
```
