<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->
# Source Provenance And Adaptation Boundary

The project-support pack was adapted on 2026-08-05 from
`/Users/afreitas/Downloads/proj_skills.zip`, SHA-256
`f7f7c0bb68afad73d6c69170eacd527bece49665b1c6b474836f736a88de7f3d`.
The archive passed `unzip -t` and contained 21 skills from a Rover/SVA-oriented donor project.

Twenty skills were adapted to Abducer/Prism. `animate-workflow-runtime` was deferred because
its `.rover` event protocol has no truthful native mapping and would duplicate current reasoning
monitoring. macOS metadata, AppleDouble files, bytecode caches, and compiled Python files were
excluded. Donor terminology, repository paths, test globs, report taxonomies, and authority
claims were rewritten for this repository; source scripts are not treated as trusted until the
local validator and regression tests pass.

The source agent metadata carried mixed licensing headers, including unresolved `TBD` values.
This import does not invent or upgrade a license. Repository maintainers should resolve licensing
before distributing the inherited material outside the permissions of the source project.
