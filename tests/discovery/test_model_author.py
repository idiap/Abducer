# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
"""Regression checks for real-call provenance, bounded repairs and frozen replay."""
import json

import pytest

from agentic.discovery.contracts import ContractError
from agentic.discovery.model_author import ModelAuthor


SCHEMA = {"type": "object", "additionalProperties": False, "required": ["conjecture"],
          "properties": {"conjecture": {"type": "string", "minLength": 8}}}


def response(value, reason="stop"):
    return {"model": "test-provider", "choices": [{"finish_reason": reason,
            "message": {"content": json.dumps(value)}}], "usage": {"total_tokens": 20}}


def author(tmp_path, completion, **identity):
    return ModelAuthor(root=tmp_path, completion=completion,
        **{"target_id": "target-a", "run_id": "run-a", "model_id": "selected-model", **identity})


def run(operator, **overrides):
    args = {"instruction": "Articulate a conjecture, preserving uncertainty.",
            "inputs": {"question": "A bounded theory question"}, "schema": SCHEMA}
    args.update(overrides)
    return operator.author("hypotheses", **args)


def test_repairs_retain_actual_attempts_and_replay_without_calls(tmp_path):
    calls = []
    def completion(**args):
        calls.append(args)
        return response({"wrong": "field"} if len(calls) == 1 else {"conjecture": "An unproved possibility"})
    operator = author(tmp_path, completion)
    result = run(operator)
    assert len(calls) == 2
    assert "additional properties" in calls[1]["messages"][-1]["content"].lower()
    assert json.loads((tmp_path / "hypotheses/attempt-1/validation.json").read_text())["status"] == "rejected"
    assert run(operator) == result
    assert len(calls) == 2
    assert result["scientific_truth_verified"] is False
    assert result["authority"] == "internally_correlated_model_authorship"
    with pytest.raises(ContractError, match="crossed"):
        run(author(tmp_path, completion, run_id="other-run"))
    with pytest.raises(ContractError, match="crossed"):
        run(operator, inputs={"question": "A different task"})


def test_domain_rejection_and_truncation_never_release_result(tmp_path):
    calls = []
    def completion(**args):
        calls.append(args)
        return response({"conjecture": "Unsupported certainty"}, "length" if len(calls) == 1 else "stop")
    def reject(value):
        raise ContractError("missing a falsifier")
    with pytest.raises(ContractError, match="after 3 attempts.*falsifier"):
        run(author(tmp_path, completion), validator=reject)
    assert len(calls) == 3
    assert not (tmp_path / "hypotheses/result.json").exists()
    assert "truncated" in (tmp_path / "hypotheses/attempt-1/validation.json").read_text()


def test_provider_failure_retains_request_and_never_retries_automatically(tmp_path):
    calls = []
    def completion(**args):
        calls.append(args)
        raise RuntimeError("provider unavailable")
    with pytest.raises(RuntimeError, match="unavailable"):
        run(author(tmp_path, completion))
    assert len(calls) == 1
    failure = json.loads((tmp_path / "hypotheses/attempt-1/failure.json").read_text())
    assert failure["status"] == "provider_failed"
    with pytest.raises(FileExistsError):
        run(author(tmp_path, completion))
    assert len(calls) == 1


def test_replay_checks_response_and_reruns_domain_validator(tmp_path):
    operator = author(tmp_path, lambda **_: response({"conjecture": "A bounded possibility"}))
    run(operator)
    def changed_validator(value):
        raise ContractError("newly detected target drift")
    with pytest.raises(ContractError, match="target drift"):
        run(operator, validator=changed_validator)
    path = tmp_path / "hypotheses/attempt-1/response.json"
    path.write_text(path.read_text().replace("bounded possibility", "proven conclusion"))
    with pytest.raises(ContractError, match="digest changed"):
        run(operator)


def test_transport_normalizes_tuple_inputs_before_frozen_replay(tmp_path):
    calls = []
    def completion(**arguments):
        calls.append(arguments)
        return response({"conjecture": "An explicitly bounded possibility"})
    operator = author(tmp_path, completion)
    result = run(operator, inputs={"allowed_paths": ("/mechanism", "/primitives")})
    assert run(operator, inputs={"allowed_paths": ["/mechanism", "/primitives"]}) == result
    assert len(calls) == 1
