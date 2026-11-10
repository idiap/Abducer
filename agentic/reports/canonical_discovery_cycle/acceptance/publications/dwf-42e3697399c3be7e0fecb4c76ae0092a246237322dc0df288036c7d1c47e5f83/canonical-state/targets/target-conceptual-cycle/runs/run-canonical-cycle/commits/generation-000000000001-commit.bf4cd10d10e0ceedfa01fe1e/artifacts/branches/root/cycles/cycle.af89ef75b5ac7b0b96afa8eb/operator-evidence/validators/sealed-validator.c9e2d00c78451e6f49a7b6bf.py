"""Typed, replayable foundations for Abducer's conceptual-discovery runtime.

The package deliberately separates execution evidence, epistemic replay, semantic
learning, and persistence.  Discovery operators may propose changes, but only the
ledger reducer and transaction store can turn those proposals into durable state.
"""

from .contracts import ContractError, Namespace, canonical_digest, canonical_json
from .cycle import AUTHORITY_BOUNDARY, run_canonical_discovery_cycle
from .evaluation import evaluate_discovery_delta, validate_evaluation_receipt
from .hypotheses import (
    build_hidden_elicitation_prompt,
    replay_seed_free_high_risk_elicitation,
    run_seed_free_high_risk_elicitation,
    semantic_hypothesis_signature,
    validate_seed_free_high_risk_elicitation,
)
from .proof import build_proof_handoff, run_proof_continuation
from .scheduler import (
    consume_action,
    consume_action_transaction,
    schedule_discovery_actions,
)

__all__ = [
    "ContractError",
    "Namespace",
    "AUTHORITY_BOUNDARY",
    "build_proof_handoff",
    "build_hidden_elicitation_prompt",
    "canonical_digest",
    "canonical_json",
    "consume_action",
    "consume_action_transaction",
    "evaluate_discovery_delta",
    "run_proof_continuation",
    "run_canonical_discovery_cycle",
    "run_seed_free_high_risk_elicitation",
    "replay_seed_free_high_risk_elicitation",
    "schedule_discovery_actions",
    "semantic_hypothesis_signature",
    "validate_evaluation_receipt",
    "validate_seed_free_high_risk_elicitation",
]
