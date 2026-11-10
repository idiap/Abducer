-- SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
--
-- SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
-- Neuro-symbolic AI Group
--
-- SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
-- Neuro-symbolic AI Group
--
-- SPDX-License-Identifier: MIT
import AbducerFormal.Discovery.Basic

namespace AbducerFormal.Discovery

def readinessScore (route : RouteSig) : Nat :=
  let base :=
    (if hasText route.sourceStatementId then 1 else 0) +
    (if hasText route.targetStatementId then 1 else 0) +
    (if hasText route.sourceRegime then 1 else 0) +
    (if hasText route.targetRegime then 1 else 0) +
    (if hasText route.invariant then 1 else 0) +
    (if hasText route.candidateObject && !route.underTypedCarrier then 1 else 0) +
    (if hasText route.sourceExcerpt then 1 else 0) +
    (if hasText route.targetExcerpt then 1 else 0) +
    (if hasText route.branchFamily then 1 else 0)
  base +
    (if route.multipleOperationalizations || route.equivalencePressure then 1 else 0) +
    (if route.factorizationPressure then 1 else 0) +
    (if route.negativePressure then 1 else 0)

def assessReadiness (route : RouteSig) : SearchReadiness :=
  let blockers :=
    (if hasText route.sourceStatementId then [] else ["missing source statement id"]) ++
    (if hasText route.targetStatementId then [] else ["missing target statement id"]) ++
    (if hasText route.sourceRegime then [] else ["missing source regime"]) ++
    (if hasText route.targetRegime then [] else ["missing target regime"]) ++
    (if hasText route.invariant then [] else ["missing preserved invariant"]) ++
    (if hasText route.candidateObject && !route.underTypedCarrier then [] else ["candidate object is missing or still under-typed"])
  let reasons :=
    (if hasText route.invariant then ["the preserved invariant is named"] else []) ++
    (if hasText route.candidateObject && !route.underTypedCarrier then ["the bridge carrier is named and not marked under-typed"] else []) ++
    (if route.multipleOperationalizations || route.equivalencePressure then ["the route is explicitly equivalence- or coherence-facing"] else []) ++
    (if route.factorizationPressure then ["the route is diagrammatic enough for factorization search"] else []) ++
    (if route.negativePressure then ["negative pressure is explicit, so bounded obstruction search is meaningful"] else [])
  let score := readinessScore route
  if !blockers.isEmpty then
    if score >= 6 then
      {
        mode := "hybrid-llm-plus-symbolic"
        score := score
        blockers := blockers
        reasons := reasons ++ ["the route is partially typed but still needs LLM mediation on missing fields"]
      }
    else
      {
        mode := "llm-first"
        score := score
        blockers := blockers
        reasons := reasons ++ ["the route is still too schematic for bounded symbolic search"]
      }
  else
    {
      mode := "symbolic-search-ready"
      score := score
      blockers := []
      reasons := reasons ++ ["the route is typed enough for bounded search over bridge shapes"]
    }

def appendUnique (items : List BridgeShape) (shape : BridgeShape) : List BridgeShape :=
  if shape ∈ items then items else items ++ [shape]

def searchShapes (route : RouteSig) : List BridgeShape :=
  let shapes0 := [BridgeShape.realization]
  let shapes1 := if route.sourceRegime != route.targetRegime then appendUnique shapes0 BridgeShape.transport else shapes0
  let shapes2 := if route.multipleOperationalizations || route.equivalencePressure then appendUnique shapes1 BridgeShape.equivalence else shapes1
  let shapes3 := if route.factorizationPressure then appendUnique shapes2 BridgeShape.factorization else shapes2
  let shapes4 := if route.negativePressure || route.underTypedCarrier || hasText route.barrierScope then appendUnique shapes3 BridgeShape.obstruction else shapes3
  shapes4

def renderShapes (shapes : List BridgeShape) : String :=
  String.intercalate "," (shapes.map BridgeShape.render)

end AbducerFormal.Discovery
