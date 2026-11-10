<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->
# Specific epistemic contracts: incident diagnosis

Start from a realistic target-project request:

> Given operator statements and service measurements, return a ranked list of
> incident-cause hypotheses, critique the leading explanation, recommend a
> mitigation, and record the incident commander's decision.

A weak conversion emits `Input`, `List[String]`, `CritiqueResult`, and
`Output`. That loses the ontology and makes it impossible to tell generation
from evidence, ranking from truth, advice from authority, or decision from
execution.

The request instead induces these candidate contracts:

| Source concept | Specific candidate | Distinction retained |
| --- | --- | --- |
| operator message | `OperatorIncidentStatement` | token, speaker, channel, time |
| normalized assertion | `OperatorCauseClaim` | proposition and claimant |
| sampled metric | `DatabaseLatencyObservation` | value, unit, window, method, limitations |
| candidate explanation | `IncidentCauseHypothesis` | alternatives, predictions, falsifiers |
| criterion score | `HypothesisCriterionAssessment` | criterion, scale, grounds, uncertainty |
| ordered diagnosis | `RankedIncidentHypotheses` | rule, ties, exclusions, evidence snapshot |
| review | `IncidentAnalysisCritique` | critic types, standards, findings, disposition |
| warrant challenge | `IncidentHypothesisDefeater` | rebutting/undercutting kind and effect |
| advice | `MitigationRecommendation` | addressee, result, risks, preconditions |
| commitment | `MitigationDecision` | alternatives, authority, rule, rationale |
| intervention | `IncidentMitigationAction` | capability, status, effect/failure |

These shapes are candidates. A real target project must confirm every object
and field through its own instructions, schemas, examples, consumers, tests,
or reviewed decisions.

The workflow reasoning type composes several skill roles:

```text
NormalizeClaims:
  List[OperatorIncidentStatement] -> List[OperatorCauseClaim]
GenerateIncidentHypotheses:
  IncidentQuestion + observations + constraints
  -> Generated[List[IncidentCauseHypothesis]]
CritiqueIncidentAnalysis:
  hypotheses + observations + assumptions + critic standards
  -> Generated[IncidentAnalysisCritique]
RefuteIncidentHypotheses:
  hypotheses + critique findings + observations
  -> Generated[CandidateIncidentHypothesisDefeaters]
RankIncidentHypotheses:
  fixed hypotheses + criteria + evidence + defeaters
  -> Generated[RankedIncidentHypotheses]
RecommendMitigation:
  ranked hypotheses + constraints -> Generated[MitigationRecommendation]
RecordDecision (material boundary):
  recommendation + authority record -> MitigationDecision
ExecuteMitigation:
  decision + capability
  -> Result[IncidentMitigationAction, MitigationExecutionError]
```

`incident-input.json` contains statements, observations, constraints, and
ranking criteria. It does not call every input “evidence.”

`epistemic-output.json` is a differentiated result. Its leader is top-ranked
under one declared rule, not marked true or proved. A calibration gap and an
undercutting defeater remain visible. Recommendation, decision, and
not-yet-executed action are separate.

`project-semantic-taxonomy.json` shows the validated discovery artifact built
by `to-prism-derive-types`. Its example fingerprint and source anchors are
illustrative; a real run replaces them with the inspected project's digest and
actual evidence locations.

These occurrences are not counted from skills. The testimony corroborator can
contribute both to evidence assessment and later ranking, while source
independence and corroboration skills can jointly materialize one assessment.
Split only at an independently consumed/reviewed typed result; merge
complementary skill lenses that jointly produce one result.

The JSON illustrates data, not an executable `.prism` schema. Canonical Prism
would place nominal contracts in `types.prism`, operation composition in
`reasoning.prism`, and skill/effect bindings in `materialization.prism`.
