---
name: project-readme-orchestrator
description: Orchestrate a controlled concept-first repository README update. Use when creating, substantially rewriting, simplifying, or release-gating a project README so its promise, minimal installation path, first use, outputs, trust boundaries, and documentation links stay concise and synchronized with executable repository evidence.
---

# Project README Orchestrator

Build the README as the project's front door: clear enough to run quickly, accurate enough to trust, and shallow enough to lead readers into the documentation system.

Use this ordered stack:

1. `$project-readme-concept-builder`
2. `$project-onboarding-path-verifier`

The orchestrator assembles the two child packets after those hooks complete; it does not invoke itself.

## Workflow

1. Inspect the request and changed repository surfaces. Determine whether concept, onboarding, or both require refresh.
2. Build the concept packet with `$project-readme-concept-builder`.
3. Build the onboarding packet with `$project-onboarding-path-verifier`.
4. Assemble the README using [README quality contract](references/readme-quality-contract.md).
5. Keep exhaustive setup, integration, artifact, skill, and CI detail in the documents that own it.
6. Run the deterministic README gate:

   ```bash
   python proj_skills/project-readme-orchestrator/scripts/validate_project_readme.py --repo .
   ```

7. Run documentation, project-skill, and link tests affected by the change.
8. Inspect the final diff for conceptual order, duplicated guidance, stale paths, and claims stronger than their evidence.

## Output Contract

Leave:

- an updated [root project overview](../../README.md)
- a verified minimal install and first-run path
- links to canonical deeper documentation
- an updated [project-skill index](../INDEX.md) when the control stack changes
- deterministic validation evidence

## Ownership Boundaries

- Own README quality evidence and feed it into Prism verification and handoff gates.
- Do not duplicate the full install guide, skill catalog, workflow contract, integration manuals, artifact schema, or CI matrix.
- Do not rewrite executable workflow semantics to make prose true without explicit authorization.
- Route framework-architecture changes through the repository's meta-framework controls.

## Release Gate

Recommend that Prism block handoff when:

- the title and opening promise do not identify the project
- the conceptual model appears after installation detail
- the first local run requires undocumented credentials
- a displayed command fails parser or execution verification
- a local Markdown link is broken
- the README overstates validation, fidelity, or signoff

Minor wording preference is not a release blocker.
