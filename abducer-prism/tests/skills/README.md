<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->
# Skill forward-test cases

These cases exercise the ten judgment-oriented skills against the synthetic,
redistributable provider fixtures in `../fixtures`. They test observable routing
and safety gates rather than exact instructional wording.

| Case | Expected behavior |
| --- | --- |
| fresh Codex conversion | inspect and model through the provider-neutral launcher; stop for semantic review without executing source code |
| Claude baseline | discover candidates only; require a separate authorization before execution |
| diagnostic type derivation | require project-specific statement, observation, ranked-hypothesis, critic/defeater, judgment, decision, and action contracts backed by source evidence |
| parallel-test design | freeze typed workflow correspondence, independent oracles, negative controls, and bounded generative cases without execution |
| workflow documentation | add only source-grounded, behavior-neutral comments for reviewed typed workflow occurrences and stages |
| mixed workflow recovery | retain cross-provider ownership and proposed/unresolved judgments |
| OpenCode reasoning review | do not infer epistemic methods from names; leave the deterministic initial map operational/proposed for human review |
| preservation review | treat fake execution and offline integrity as smoke/integrity evidence; leave Trace and Behavioral unestablished without a native baseline |
| parallel-test execution | require an approved manifest and exact authority, isolate both legs, and preserve mismatches without adapting the oracle |
| upstream update | detect a semantic source change in dry-run mode without modifying the published conversion |

`test_skill_forward.py` runs these cases in temporary copies so fixture sources
and checked-in outputs cannot be mutated. `test_skill_package.py` validates
reference links, UI metadata, skill discovery boundaries, and a clean-copy
provider-neutral launcher contract.

The forward tests do not call a model and therefore do not grade prose. Their
scope is the invariant behavior that the skills must route to: no implicit
execution, explicit review gates, conservative reasoning defaults, evidence
caps, specific evidence-backed type contracts, dry-run update safety, and no
dependency on a repository-relative launcher path.
