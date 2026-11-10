-- SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
--
-- SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
-- Neuro-symbolic AI Group
--
-- SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
-- Neuro-symbolic AI Group
--
-- SPDX-License-Identifier: MIT
namespace AbducerFormal.Discovery

inductive BridgeShape where
  | realization
  | transport
  | equivalence
  | factorization
  | obstruction
  deriving Repr, DecidableEq, Inhabited

def BridgeShape.render : BridgeShape -> String
  | .realization => "realization"
  | .transport => "transport"
  | .equivalence => "equivalence"
  | .factorization => "factorization"
  | .obstruction => "obstruction"

structure RouteSig where
  sourceStatementId : String
  targetStatementId : String
  sourceRegime : String
  targetRegime : String
  invariant : String
  candidateObject : String
  branchFamily : String := ""
  sourceExcerpt : String := ""
  targetExcerpt : String := ""
  multipleOperationalizations : Bool := false
  equivalencePressure : Bool := false
  factorizationPressure : Bool := false
  negativePressure : Bool := false
  underTypedCarrier : Bool := false
  barrierScope : String := ""
  deriving Repr, Inhabited

structure SearchReadiness where
  mode : String
  score : Nat
  blockers : List String
  reasons : List String
  deriving Repr, Inhabited

def hasText (text : String) : Bool :=
  !(text.trimAscii.isEmpty)

end AbducerFormal.Discovery
