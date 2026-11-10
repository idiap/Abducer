<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->
# Cohere-fast release gate

Disposition: **blocked**

The workflow is isolated and default-off. A valid artifact or event digest establishes integrity only, not scientific correctness.

| Check | Status | Detail |
|---|---|---|
| source_manifest | pass | agentic/imports/cohere_fast/source_manifest.json |
| source_dispositions | pass | agentic/imports/cohere_fast/dispositions.json |
| collision_report | pass | agentic/imports/cohere_fast/collision_report.json |
| isolation_contract | pass | agentic/spec/cohere_fast_isolation_contract.yaml |
| invocation_schema | pass | agentic/spec/cohere_fast_invocation.schema.json |
| domain_registry | pass | agentic/registries/domain_skill_bundles.yaml |
| parent_contract | pass | agentic/registries/cohere_fast_workflow_contracts.yaml |
| subworkflows | pass | agentic/registries/cohere_fast_subworkflows.yaml |
| ym_workflow | pass | agentic/registries/cohere_fast_ym_workflow.yaml |
| artifact_schema | pass | agentic/spec/cohere_fast_artifacts.schema.json |
| status_crosswalk | pass | agentic/registries/cohere_fast_status_crosswalk.yaml |
| runner | pass | agentic/orchestration/cohere_fast_runner.py |
| trace_adapter | pass | agentic/scripts/reasoning_trace_adapters/cohere_fast.py |
| task_projection | pass | registry/tasks/cohere-fast/task_registry.json |
| live_trace_test | pass | tests/integration/test_cohere_fast_ym_lifecycle.py |
| noninterference_test | pass | tests/integration/test_cohere_fast_noninterference.py |
| documentation | pass | docs/workflows/cohere-fast.md |
| default_off | pass | The domain route remains disabled until source redistribution authority is resolved. |
| isolated_root | pass |  |
| domain_skill_count | pass | 30 |
| source_license | blocked | No license file was detected in the supplied archive; redistribution stays disabled. |
