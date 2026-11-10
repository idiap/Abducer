---
name: project-onboarding-path-verifier
description: Derive and verify the shortest honest installation and first-run path for a repository. Use when prerequisites, dependency locks, CLI commands, configuration, example inputs, output paths, or optional provider integrations change, or when README setup instructions need proof against the executable project.
---

# Project Onboarding Path Verifier

Verify the path from a clean checkout to one inspectable result. Keep optional integrations outside the minimal path.

## Read First

1. Read package metadata and the dependency lock.
2. Read the actual CLI parser or supported entrypoint.
3. Read the smallest maintained example input.
4. Read the installation guide and current README commands.
5. Read [verification matrix](references/onboarding-verification-matrix.md) before reporting the path as verified.

## Verify The Path

1. Identify the minimum supported runtime and package manager.
2. Determine whether credentials or configuration are required for the default backend.
3. Verify dependency synchronization without changing dependency semantics.
4. Run CLI help for every command shown in the minimal path.
5. Execute the smallest safe example in an isolated temporary run directory.
6. Confirm the named outputs exist and open or parse as claimed.
7. Separate locally verified steps from credential-gated, network-dependent, or toolchain-optional steps.
8. Remove temporary outputs created by the verification run from the project tree.

## Handoff

Leave `$project-readme-orchestrator` a compact onboarding packet containing:

- prerequisites
- minimal install commands
- one first-run command
- first three to five outputs to inspect
- default backend and credential posture
- optional next steps
- verification evidence and explicit unverified boundaries

## Guardrails

- Never make provider setup mandatory when the default local path works without it.
- Do not put every backend, integration, or control mode into Quick Start.
- Do not claim a command was tested when only its documentation was inspected.
- Use the repository's supported locked environment.
- Do not write smoke-test results into tracked example projects; use temporary paths or clean them up safely.
