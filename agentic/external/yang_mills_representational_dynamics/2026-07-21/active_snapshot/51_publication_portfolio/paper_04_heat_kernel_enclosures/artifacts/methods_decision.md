# Certification methods decision

Selected backend: exact Python `Fraction` arithmetic with a short explicit
trust base.

Reasons:

- theorem pass decisions reduce to integer comparisons;
- no external interval library or platform rounding mode is trusted;
- Machin, Taylor, dyadic exponential, and integer-square-root bounds are
  inspectable in one source file;
- coarse constants are acceptable because the local image margin is large.

Decimal values are upward-rounded displays only. A faster floating evaluator
is used solely for the cross-representation diagnostic.
