<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->
# Onboarding Verification Matrix

Record the strongest evidence available for each public onboarding statement.

| Surface | Minimum evidence | Failure response |
| --- | --- | --- |
| Runtime version | Package metadata and CI/runtime configuration agree | State the supported range; resolve disagreement before publishing |
| Dependency install | Locked resolver succeeds | Do not publish an unlocked substitute as canonical |
| CLI syntax | Actual parser help accepts the shown subcommand and flags | Fix the command or the CLI before handoff |
| Default credentials | Backend selection and configuration code agree | Say whether a key is required; do not infer |
| Example input | Example exists and is accepted by the current loader | Select another maintained example |
| First run | Isolated execution exits successfully | Report the blocker; do not label the path verified |
| Named outputs | Files exist and match the claimed role | Correct the list using the workflow response |
| Optional integration | Dependency extra and command surface exist | Mark it optional and state whether live execution was tested |

Use these evidence labels:

- `executed`: command completed in the current environment
- `parser_verified`: accepted by the live CLI help or parser
- `source_verified`: supported by authoritative code or configuration
- `credential_gated`: requires unavailable credentials
- `environment_gated`: requires an unavailable external tool or service
- `not_verified`: retained only with an explicit caveat

The root README should contain the executed local path. Put the fuller evidence and platform notes in the installation guide.
