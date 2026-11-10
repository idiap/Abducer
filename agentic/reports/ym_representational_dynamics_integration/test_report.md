<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->
# YM Restricted-Model Test Report

- Target: `yang-mills-existence-and-mass-gap-target`
- Status: `passed`
- Tests observed: 31 / expected 31
- Boundary: passing tests validate restricted models only, not continuum Yang-Mills or the Clay mass gap.

## relational_rigidity_finite_spectral_core

- Command: `/Users/afreitas/.local/bin/python3 -m unittest -v test_finite_spectral_core.py`
- CWD: `agentic/external/yang_mills_representational_dynamics/2026-07-20/research_package/02_relational_rigidity_program`
- Exit code: `0`
- Tests: 9

## heat_kernel_basin_entry

- Command: `/Users/afreitas/.local/bin/python3 -m unittest -v test_heat_kernel_influence.py test_advanced_regulator_calibration.py`
- CWD: `agentic/external/yang_mills_representational_dynamics/2026-07-20/research_package/03_heat_kernel_basin_entry`
- Exit code: `0`
- Tests: 14

## fibered_block_rg_two_plaquette_bridge

- Command: `/Users/afreitas/.local/bin/python3 -m unittest -v test_two_plaquette_bridge.py`
- CWD: `agentic/external/yang_mills_representational_dynamics/2026-07-20/research_package/04_fibered_block_rg`
- Exit code: `0`
- Tests: 8
