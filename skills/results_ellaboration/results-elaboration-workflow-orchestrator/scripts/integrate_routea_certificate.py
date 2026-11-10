#!/usr/bin/env python3
# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
"""Integrate the Route A verification certificate into the paper narrative."""

from __future__ import annotations

import argparse
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
OUT_DIR = ROOT / "agentic/reports/results_ellaboration/a-finite-schur-feshbach-test-for-reflected-wilson-blocks-an-explicit-four-dimens"


OLD_PROTOCOL = (
    "The supplementary script \\texttt{verify\\_three\\_hairpin\\_block.py} symbolically verifies the formulas for $H$, $K$, $A$, $C$, the determinant, and the two reduced eigenvalues, and can print the eigenvalues for numerical choices of $(\\sigma,\\tau,\\eps)$."
)

NEW_PROTOCOL = (
    "The result-elaboration certificate \\texttt{routea\\_three\\_hairpin\\_certificate.json}, "
    "generated from the supplied verification script, symbolically verifies the formulas for "
    "$N_\\eps$, $q_\\eps$, $H$, $K$, $A$, $C$, the determinant, the uncorrected null value "
    "$z^TPKPz=\\sigma^2+4\\tau$, the removed Schur--Feshbach term $\\sigma^2$, and the corrected "
    "margins $u^TAu=2\\sigma$ and $v^TCv=2\\tau/3$.  This certificate supports the finite "
    "source-collision Route A block only; it is not evidence for the geometric collar modules "
    "G1--G4, endpoint modules E1--E2, or continuum/gap modules M1--M2."
)


OLD_CONCLUSION = (
    "What remains is now sharply separated.  The present source collision must be replaced or supplemented by a lattice-resolved geometric collar; renormalized coefficients and strict margins must be controlled along a continuum trajectory; endpoint cumulants need two-sided, regulator-specific error estimates; and reflection positivity must be joined to continuum reconstruction and a spectral estimate.  Those are open modules, not consequences of the finite block."
)

NEW_CONCLUSION = (
    "What remains is now sharply separated.  The verified calculation is the finite source-collision "
    "algebra: it certifies the displayed $3\\times3$ block, the cancellation of the spurious "
    "$\\sigma^2$ null-channel term, and the reduced margins.  The present source collision must still "
    "be replaced or supplemented by a lattice-resolved geometric collar; renormalized coefficients "
    "and strict margins must be controlled along a continuum trajectory; endpoint cumulants need "
    "two-sided, regulator-specific error estimates; and reflection positivity must be joined to "
    "continuum reconstruction and a spectral estimate.  Those are open modules, not consequences "
    "of the finite block or of the verification certificate."
)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("draft", type=Path)
    args = parser.parse_args()
    draft = args.draft.expanduser().resolve()
    text = draft.read_text(encoding="utf-8")
    if OLD_PROTOCOL not in text:
        raise SystemExit("could not find protocol sentence to replace")
    if OLD_CONCLUSION not in text:
        raise SystemExit("could not find conclusion sentence to replace")
    text = text.replace(OLD_PROTOCOL, NEW_PROTOCOL)
    text = text.replace(OLD_CONCLUSION, NEW_CONCLUSION)
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    out_path = OUT_DIR / "finite_wilson_os_routeA_SU2_certificate_integrated.tex"
    out_path.write_text(text, encoding="utf-8")
    print(f"Wrote {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
