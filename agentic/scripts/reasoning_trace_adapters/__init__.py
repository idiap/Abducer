# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
"""Conservative adapters for public reasoning traces.

Adapters normalize observed records.  They intentionally do not synthesize
scientific claims from filenames, receipts, or successful control decisions.
"""

from .named_workflow import assemble_named_workflow_trace, load_events
from .legacy import adapt_legacy_projection
from .cohere_fast import assemble_cohere_fast_trace

__all__ = ["adapt_legacy_projection", "assemble_cohere_fast_trace", "assemble_named_workflow_trace", "load_events"]
