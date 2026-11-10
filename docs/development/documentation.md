<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->

# Documentation maintenance

Use this guide when changing human-facing documentation. The audience is a new user,
a researcher inspecting evidence, or a maintainer looking for exact commands.

## Shared structure

Keep the root README sections in this order: Overview, Key concepts, Getting started,
Examples, Architecture, Documentation, Development and validation, Limitations and
status, Dependencies and license. Keep the nine area indexes linked from `docs/README.md`.
Specialist collections may keep their existing paths and names.

## Content and preservation rules

- Explain the project's own purpose, workflow, artifacts, and evidence boundaries.
- Give setup requirements, a first example, expected outputs, and interpretation.
- Verify commands and paths against current source; distinguish implemented behavior
  from proposals, fixtures, generated reports, and retired integrations.
- Preserve useful detail and attribution. When shortening the README, retain substantive
  examples and reference content in the linked detailed project guide.
- Keep specialist paths stable. If a move is necessary, update inbound links and keep
  a compatibility pointer. Never overwrite generated scientific evidence to repair a link.
- Mark optional outputs as generated paths with a producing workflow, rather than
  presenting absent files as available evidence. Link stable source fixtures where possible.
- Refresh generated catalogs through their generators; identify retained historical pages
  explicitly. Never describe an archived skill as currently installed solely because its page exists.

## Review and validation

Check local Markdown destinations, section anchors, code-block commands, and consistency
between the README, getting-started guide, architecture, and source contracts.
Run the project's documentation checks and `git diff --check`; use focused runtime
checks if a documented command or behavior changes. Documentation checks do not establish
scientific validity. Keep live providers, canonical state mutation, and expensive research
runs out of a documentation-only smoke check.
