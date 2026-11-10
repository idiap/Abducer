<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->
# Generated Views

Generated views are derived inspection artifacts. Regenerate them from their owning workflow; do not edit them as source-of-truth documents.

- Epistemic process map — [HTML](epistemic-process-map.html) / [JSON](epistemic-process-map.json)
- Project workflow graph — [HTML](project-workflow-graph.html) / [JSON](project-workflow-graph.json)
- Workflow and skill health audit — [HTML](workflow-health-audit.html) / [JSON](workflow-health-audit.json)

## Regeneration

From the repository root:

```bash
python3 proj_skills/project-workflow-graph-reporter/scripts/generate_workflow_graph_report.py \
  --repo . \
  --output docs/generated/project-workflow-graph.html \
  --json-output docs/generated/project-workflow-graph.json

python3 proj_skills/workflow-health-audit-orchestrator/scripts/generate_workflow_health_audit.py \
  --repo . \
  --output docs/generated/workflow-health-audit.html \
  --json-output docs/generated/workflow-health-audit.json
```
