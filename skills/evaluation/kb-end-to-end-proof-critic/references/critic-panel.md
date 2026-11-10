<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->
# End-To-End Critic Panel

This panel determines whether the current artifact chain supports a plausible end-to-end proof of the main conjecture.

## Critics

Score each critic from `0` to `4`.

### 1. Main-Claim Closure

Ask:

1. Is the route target explicit?
2. Is the final implication to the main conjecture grounded?
3. Is there a terminal proved result that actually closes the remaining route?

### 2. Dependency Closure

Ask:

1. Are the macro-strategy completion items closed?
2. Are the route lemmas and payoff lemmas discharged rather than merely listed?
3. Does the proof still depend on open conditional steps?

### 3. Assumption Discipline

Ask:

1. Are assumptions explicit?
2. Do terminal proof attempts pass the assumption-discipline judge?
3. Are there unresolved representation shifts that change the assumptions mid-route?

### 4. Bridge Realism

Ask:

1. Is the bridge object typed?
2. Is the carrier mathematically inspectable?
3. Has the route stabilized around one object rather than multiple unresolved operationalizations?

### 5. Adversarial Pressure

Ask:

1. Has the route faced negative routes, barriers, or blocking results?
2. Has the system accumulated evidence beyond structural coherence?
3. Would a failure mode already be explicit if the route broke?

### 6. Proof Granularity

Ask:

1. Is there a real stepwise argument?
2. Are proof steps inspectable by experts?
3. Has at least one terminal proof attempt survived critique with substantive detail?

### 7. End-To-End Consistency

Ask:

1. Does the macro-proof chain remain coherent from the bridge result to the main conjecture?
2. Are route objects, invariants, and theorem statements aligned?
3. Is there any internal contradiction or unresolved representation shift?

### 8. Novelty Discipline

Ask:

1. Are prior-art findings explicitly tracked?
2. Are external references imported into InformalMathLib when used?
3. Would a proof claim survive a novelty audit?

## Mandatory Gates

Do not mark the main problem as plausibly solved unless all hold:

1. `grounded_main_conjecture`
2. `terminal_proved_attempt`
3. `completion_checklist_clear`
4. `no_failed_terminal_judges`

## Stop Rule

Mark `plausible_solution_detected = true` only if:

1. all mandatory gates pass;
2. the normalized average critic score is at least `0.80`;
3. no critic scores below `2`.

Otherwise continue the loop and identify the blocking defects explicitly.
