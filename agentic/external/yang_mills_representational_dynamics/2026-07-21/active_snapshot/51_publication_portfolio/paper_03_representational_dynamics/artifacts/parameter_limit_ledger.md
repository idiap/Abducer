# Parameter and limit ledger

| Symbol/index | Meaning | Quantifier requirement | Failure if omitted |
|---|---|---|---|
| \(i\in I\) | generic directed regulator/recovery index | eventual bounds on one directed tail | pointwise arrows do not define a stable family |
| \(t\ge0\) | Euclidean semigroup time | estimate holds for every \(t\), convergence at each fixed \(t\) | finitely many time samples do not locate spectral support |
| \(m>0\) | physical exponential rate | one value independent of \(i\) and the recovered vector | finite gaps can collapse |
| \(M_x<\infty\) | vector-dependent amplitude | may depend on \(x\), not on late indices or \(t\) | no uniform recovered bound |
| \(x\in\mathcal D\) | dense centered observable core | \(\mathcal D\) dense in \(\Omega^\perp\) | hidden low-energy sector remains invisible |
| \(n\) | cutoff/truncation index in countermodels | must be controlled before target limit | pointwise positive gaps are inconclusive |
| \(L\) | volume index in limit defect | supremum in \(L\) must decay before \(L\to\infty\) | iterated limits disagree |
| \(a\downarrow0\) | lattice spacing in Yang--Mills chain | constants stable in physical units | regulator-scale gap need not be physical |
| \(L\to\infty\) | thermodynamic limit | volume-uniform normalized observables | boundary and entropy costs may dominate |

No numerical Yang--Mills parameter is frozen by the theorem. The exact Python
supplement uses finite diagonal spectra and integer arrays only to verify
countermodels and certificate composition.
