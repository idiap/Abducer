<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->
# prism_me

`prism_me` is a portable Prism-aligned skill pack for spec-driven agentic development in external repositories.

It now also carries a repo-local Codex control stack so the pack is not governed only by `AGENTS.md` prose and skill descriptions. The control stack combines:

- repo-local Codex config in `.codex/config.toml`
- repo-local lifecycle hooks in `.codex/hooks.json`
- repo-local escalation rules in `.codex/rules/prism-me.rules`
- a deterministic workflow CLI in `prism_me/scripts/prism_control.py`
- a multi-persona review lane that becomes due every 50 committed edit or write cycles, remains callable on demand, and is retained at the final release gate

It is intentionally separate from `skills/` and `skills/imported/`. The goal is not to pretend that an external project is already a native Prism registry family. The goal is to give an external repo a clean, copyable bundle that already thinks in Prism's terms:

- typed contracts before prompt prose
- staged lifecycle handoffs
- durable artifacts plus reasoning-log sidecars
- explicit provenance and runtime boundaries
- dependency mapping in Prism terms: `uv` bundles, reference KBs, backend profiles, and workspace mounts
- verification before release claims
- heavily annotated Python and Markdown surfaces that explain core concept, intent, and role

## Default Workspace

The pack assumes a request-scoped workspace at `.prism/<request-slug>/` with numbered artifacts:

1. `01-spec.md`
2. `02-agent-contract.yaml`
3. `02b-quality-criteria.md`
4. `03-repo-map.md`
5. `03b-dependency-map.md`
6. `04-slice-plan.md`
7. `04b-test-strategy.md`
8. `05-execution-log.md`
9. `05b-refinement-loop.md`
10. `05c-test-evidence.md`
11. `05d-persona-review.md`
12. `06-verification.md`
13. `07-handoff.md`
14. `reasoning-log.md`

Bootstrap that layout with:

```bash
bash prism_me/scripts/init_request.sh <request-slug>
```

## VSCode Quick Start

For immediate onboarding in a VSCode-based agentic workspace:

1. Open the repository root in VSCode.
2. Read [agents.md](./agents.md).
3. Run:

```bash
bash prism_me/scripts/init_vscode_onboarding.sh
```

5. Inspect the control stack:

```bash
python3 prism_me/scripts/prism_control.py status
python3 prism_me/scripts/prism_control.py validate
python3 prism_me/scripts/prism_control.py review-complete
```

6. Initialize a request workspace:

```bash
bash prism_me/scripts/init_request.sh <request-slug>
```

That gives the workspace a root-level `AGENTS.md` shim when needed, starter VSCode tasks when they do not already exist, and the full `.prism/<request-slug>/` artifact scaffold.
It also ensures a root `to-do.md` control file exists so the plan and active steps are visible from the repository root, and it installs the repo-local `.codex/` control surfaces used for hook and rule enforcement.

Optional Prism-core mirror templates are available when a request needs a more explicit contract or composition surface:

- `shared/templates/02f-skill-contract-profile.yaml`
- `shared/templates/02g-composition-model.yaml`

They are optional by design and do not change the default request bootstrap.

## External Harmonization Route

If the request starts from external code, external skills, or upstream references, initialize the extra harmonization artifacts with:

```bash
bash prism_me/scripts/init_external_harmonization.sh <request-slug>
```

Then use:

1. `prism-external-reference-scoper`
2. `prism-external-capability-extractor`
3. `prism-agentic-shape-forger`

before the deeper contract, planning, and implementation work.

## Skill Flow

Use the suite in this order unless a later artifact already exists and is still accurate:

1. `prism-spec-orchestrator`
2. `prism-spec-intake`
3. `prism-agent-contract-author`
4. `prism-quality-criteria-elicitor`
5. `prism-repo-cartographer`
6. `prism-dependency-cartographer`
7. `prism-slice-planner`
8. `prism-test-strategy-architect`
9. `prism-implementation-driver`
10. `prism-reflective-refinement-loop`
11. `prism-generative-validation-runner`
12. `prism-persona-review-orchestrator`
13. `prism-spec-verification-critic`
14. `prism-integration-handoff`

## Shared Assets

- `skill-pack.yaml` is the machine-readable pack index.
- `to-do.md` at the repo root is the live delivery-control surface for the active Prism ME request.
- `.codex/config.toml`, `.codex/hooks.json`, and `.codex/rules/prism-me.rules` are the repo-local Codex control surfaces.
- `prism_me/scripts/prism_control.py` is the deterministic control-plane CLI.
- `shared/references/` carries the Prism alignment rules and stage gates.
- `shared/templates/` carries the portable artifact templates.
- `shared/templates/02f-skill-contract-profile.yaml` and `shared/templates/02g-composition-model.yaml` are optional mirrors for Prism-core typing and composition.

The annotation policy lives in [shared/references/annotation-discipline.md](./shared/references/annotation-discipline.md). Use it whenever the work touches `.py` or `.md` files.
The dependency policy lives in [shared/references/dependency-discipline.md](./shared/references/dependency-discipline.md). Use it whenever the work needs a Prism-style picture of bundles, runtimes, backends, KBs, or workspace mounts.
The root-planning policy lives in [shared/references/todo-discipline.md](./shared/references/todo-discipline.md). Use it whenever the request needs a visible plan, active-step control, and handoff-ready checklist at the repository root.
The testing policy lives in [shared/references/testing-discipline.md](./shared/references/testing-discipline.md). Use it whenever the work needs systematic deterministic and generative validation.
The documentation policy lives in [shared/references/documentation-discipline.md](./shared/references/documentation-discipline.md). Use it whenever the work should result in concept-first, explanatory, example-rich documentation.
The skill-type and composition policy lives in [shared/references/skill-type-and-composition-discipline.md](./shared/references/skill-type-and-composition-discipline.md). Use it whenever the work needs explicit skill contracts, composition rules, or a path from external capabilities into Prism-shaped agent surfaces.
The Codex control policy lives in [shared/references/codex-control-stack.md](./shared/references/codex-control-stack.md). Use it whenever the work needs deterministic repo-local control over skill routing, shell behavior, or request-state validation.
The persona-review policy lives in [shared/references/persona-review-discipline.md](./shared/references/persona-review-discipline.md). Use it whenever the work needs the epistemologist, mathematician, AI researcher, and software engineer review loop.

This folder is meant to be copied as one unit into an external project root or used here as the source bundle for later Prism import work.
