# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
"""Explicitly invoked workflow-local policies, separate from native hooks.

These extensions were introduced after the f90f0c6f baseline. They remain
available to callers that deliberately import this package, but are never
registered in hooks/hooks.json or substituted for the original native hooks.
"""
