# Yang--Mills research workflow

For work on four-dimensional pure Yang--Mills existence or the mass gap, use
`$ym-run-clay-program` as the orchestrator and finish every research phase with
`$ym-audit-frontier`.

Maintain the following implication chain as separate proof obligations:

1. regulated gauge-invariant construction;
2. controlled, gauge-covariant RG trajectory;
3. entry into an independently defined infrared rigidity basin;
4. uniform physical correlation rigidity;
5. coherent continuum Schwinger data with the required positivity and locality;
6. Osterwalder--Schrader reconstruction;
7. a positive Hamiltonian spectral gap above a unique vacuum.

For every result, label its status as one of: exact theorem, conditional theorem,
finite-dimensional certificate, numerical calibration, falsification, conjecture,
or open frontier. Never promote a finite-volume lattice gap, standalone plaquette
tail, perturbative beta function, incomplete observable sector, or assumed
clustering estimate to a continuum mass gap.

Preserve gauge invariance, locality, reflection positivity, observable
completeness, physical scale normalization, and uniform cutoff/volume quantifiers
whenever a representation or limit changes. Record explicitly what each map
forgets and which certificates it transports.

Each phase should produce:

- a frozen theorem or obstruction statement with all quantifiers;
- a dependency graph and frontier ledger;
- adversarial calibration against restricted models or boundary conditions;
- executable finite certificates and tests where possible;
- a concise next-target decision based on the first unproved implication.

Do not base new work on an earlier regulator or Wilson-action calculation unless
it is necessary for a stated comparison, universality bridge, or calibration.

