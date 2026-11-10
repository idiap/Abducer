<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->
# Local Result-Elaboration Workflow Hooks

These hooks are checkpoints inside the result-elaboration workflow. They are not global Codex hooks and must not be registered in `hooks/hooks.json`.

## Hook Points

1. `pre_context_interpretation`
   - Input: source draft path.
   - Check: draft exists, extension markers can be searched, and the workflow is not running as a discovery-marathon job.

2. `post_context_interpretation`
   - Input: context packet.
   - Check: bounded contribution, non-claims, main mathematical objects, and section map are present.

3. `post_need_extraction`
   - Input: extracted needs.
   - Check: every slot/marker has a typed need, discharge criterion, and paper insertion target.

4. `pre_strategy_planning`
   - Input: needs list.
   - Check: dependencies are explicit, and no need has been silently converted into a discovery task.

5. `post_strategy_planning`
   - Input: ordered TODOs.
   - Check: each TODO has source marker, action, expected artifact, validation criterion, stop/quarantine condition, and skill handoff.

6. `post_narrative_integration`
   - Input: narrative integration plan.
   - Check: abstract/introduction/conclusion consequences are stated and claim boundaries are preserved.

7. `final_results_elaboration_validation`
   - Input: report JSON/Markdown.
   - Check: marker coverage, local-hook compliance, no discovery workflow coupling, and a coherent next manuscript action.

## Forbidden Couplings

Do not call or mutate:

- discovery marathon jobs or job logs;
- discovery branch schedulers;
- target active pointers;
- Looper discovery target hooks;
- long-horizon route portfolio managers;
- marathon report generation as part of this workflow.

This workflow may read prior reports as evidence if explicitly provided, but it must not drive or resume discovery.
