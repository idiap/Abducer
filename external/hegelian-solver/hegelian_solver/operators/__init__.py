# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT

"""Transformation operator library."""

from hegelian_solver.operators.library import (
    ALL_OPERATOR_NAMES,
    operator_for_trigger,
    propose_candidates,
)

__all__ = ["ALL_OPERATOR_NAMES", "operator_for_trigger", "propose_candidates"]
