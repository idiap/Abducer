<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->

# Target Navigation Runbook

## P vs NP Vertical Slice

Run:

```bash
python agentic/scripts/run_target_navigation.py
```

Expected generated artifacts:

- `agentic/state/current_target.json`
- `agentic/state/dependency_graphs/p-vs-np.json`
- `agentic/state/dependency_frontier.json`
- `agentic/reports/dependency_closure/p-vs-np.md`
- `agentic/reports/dependency_frontier/latest.md`
- `agentic/reports/compliance/latest.md`
- `agentic/reports/drift/latest.md`
- `agentic/reports/frame_adequacy/latest.md`
- `agentic/reports/workflow_hub/latest.md`
- `agentic/reports/skill_reachability/latest.md`
- `agentic/reports/releases/ITER-0001.md`

## Validation

Run:

```bash
python agentic/scripts/agentic_check.py
python -m unittest discover -s tests -p 'test_looper_*.py'
```

The release report promotes the control-plane slice, not the mathematical
target. The dependency frontier intentionally remains open because the P vs NP
proof obligations are still proof debt.

## Yang-Mills representational dynamics overlay

The Yang-Mills target uses the target id
`yang-mills-existence-and-mass-gap-target`. Its representational dynamics
overlay is repo-visible and target-scoped:

- Source index: `agentic/reports/ym_representational_dynamics_integration/source_index.json`
- Restricted-model tests: `agentic/reports/ym_representational_dynamics_integration/test_report.json`
- Proof objects: `agentic/reports/discovery_marathon/targets/yang-mills-existence-and-mass-gap-target/proof_objects/ym_representational_dynamics_objects.json`
- Target overlay: `agentic/reports/discovery_marathon/targets/yang-mills-existence-and-mass-gap-target/ym_representational_dynamics_overlay.html`
- Validator: `python3 agentic/scripts/validate_ym_workflow_integration.py`

This layer does not prove the Clay problem. It imports a restricted theorem
suite and forces future cycles to preserve claim levels, non-claims, efficient
representation requirements, frontier blockers, and report-path separation from
P vs NP outputs.

## Next Mathematical Step

Use `agentic/state/dependency_frontier.json` to select the next route-lemma or
proof-debt node, then route that node into the existing Abducer `work` or
prove-cycle skills. The work loop records Looper frontier context when
`agentic/state/current_target.json` and `agentic/state/dependency_frontier.json`
exist.
