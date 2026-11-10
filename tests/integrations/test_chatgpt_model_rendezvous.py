# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
# SPDX-License-Identifier: MIT
"""Native completion rendezvous tests using real leased SQLite jobs.

Responses are explicitly controlled fixtures. These tests verify transport,
schema checks, ownership and cancellation; they make no model/science claim.
"""

from concurrent.futures import ThreadPoolExecutor
import json
import time

import pytest

from integrations.chatgpt.chatgpt_model import ChatGPTServices, ModelRendezvous
from integrations.chatgpt.provider import ProviderError
from integrations.chatgpt.store import AccessDenied, Store

FORMAT = {
    "type": "json_schema",
    "json_schema": {
        "name": "hypothesis",
        "strict": True,
        "schema": {
            "type": "object",
            "properties": {"hypothesis": {"type": "string"}},
            "required": ["hypothesis"],
            "additionalProperties": False,
        },
    },
}
MESSAGES = [
    {"role": "system", "content": "Produce the declared research artifact."},
    {"role": "user", "content": "A bounded mathematical question."},
]


@pytest.fixture
def leased(tmp_path):
    store = Store(tmp_path / "research.sqlite3")
    store.provision_user("alice", "Alice")
    store.provision_user("bob", "Bob")
    project = store.create_project("alice", "Research")
    budget = {"timeout_seconds": 30, "max_model_calls": 2, "max_output_tokens": 32000}
    plan = store.prepare_plan(
        "alice",
        project["id"],
        workflow_id="native-test",
        inputs={},
        budget=budget,
        release="test-release",
        runtime_source_sha256="source",
    )
    job = store.start_job(
        "alice",
        plan["plan_id"],
        "start",
        release="test-release",
        runtime_source_sha256="source",
    )
    claimed = store.claim_job("worker-1", lease_seconds=60)
    assert claimed["id"] == job["id"]
    return store, claimed, budget


def services(leased, **kwargs):
    store, job, budget = leased
    return ChatGPTServices(
        budget,
        store=store,
        job_id=job["id"],
        worker_id="worker-1",
        poll_seconds=0.01,
        **kwargs,
    )


def completion(service, **kwargs):
    return service.completion(
        messages=MESSAGES, response_format=FORMAT, max_tokens=100, **kwargs
    )


def pending(queue, job):
    deadline = time.monotonic() + 3
    while time.monotonic() < deadline:
        page = queue.pending("alice", job["id"], limit=37)
        if page["pending"]:
            return page
        time.sleep(0.01)
    raise AssertionError("Native completion did not publish a pending request")


def test_original_messages_schema_owned_response_and_idempotency(leased, monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    monkeypatch.delenv("ABDUCER_MODEL", raising=False)
    store, job, _ = leased
    service = services(leased)
    queue = ModelRendezvous(store)
    with ThreadPoolExecutor(max_workers=1) as executor:
        future = executor.submit(completion, service)
        first = pending(queue, job)
        assert queue.metadata("alice", job["id"])["model_handoff_waiting"] is True
        pieces, page = [], first
        while True:
            pieces.append(page["content"])
            if page["next_offset"] is None:
                break
            page = queue.pending(
                "alice", job["id"], offset=page["next_offset"], limit=37
            )
            assert page["request_id"] == first["request_id"]
            assert page["request_sha256"] == first["request_sha256"]
        request = json.loads("".join(pieces))
        assert request["messages"] == MESSAGES
        assert request["response_format"] == FORMAT
        assert request["token_limit_enforcement"] == "requested_guidance_only"
        with pytest.raises(AccessDenied):
            queue.pending("bob", job["id"])
        with pytest.raises(AccessDenied):
            queue.submit("bob", job["id"], first["request_id"], '{"hypothesis":"x"}')
        for invalid in (
            "not JSON",
            '{"hypothesis":1}',
            '{"hypothesis":"x","other":true}',
            '{"hypothesis":"x","hypothesis":"y"}',
            '{"hypothesis":NaN}',
            '{"hypothesis":1e999}',
        ):
            with pytest.raises(ValueError):
                queue.submit("alice", job["id"], first["request_id"], invalid)
        response = '{"hypothesis": "A controlled test candidate."}'
        receipt = queue.submit("alice", job["id"], first["request_id"], response)
        assert receipt["accepted"] is True and receipt["duplicate"] is False
        assert receipt["scientific_truth_verified"] is False
        duplicate = queue.submit("alice", job["id"], first["request_id"], response)
        assert duplicate["duplicate"] is True
        result = future.result(timeout=3)
    assert result["choices"][0]["message"]["content"] == response
    assert result["usage"] == {} and result["token_usage_observed"] is False
    assert result["model"] == "chatgpt-conversation"
    assert service.calls == 1
    assert queue.metadata("alice", job["id"])["model_handoff_waiting"] is False
    with pytest.raises(ValueError, match="different response"):
        queue.submit(
            "alice", job["id"], first["request_id"], '{"hypothesis":"changed"}'
        )


@pytest.mark.parametrize("failure", ["cancel", "lease", "disabled", "wrong-worker"])
def test_waiting_call_stops_when_job_authority_changes(leased, failure):
    store, job, _ = leased
    service = services(leased)
    queue = ModelRendezvous(store)
    with ThreadPoolExecutor(max_workers=1) as executor:
        future = executor.submit(completion, service)
        request = pending(queue, job)
        if failure == "cancel":
            store.cancel_job("alice", job["id"])
        elif failure == "disabled":
            store.provision_user("alice", "Alice", active=False)
        else:
            with store.connection(write=True) as db:
                if failure == "lease":
                    db.execute("UPDATE jobs SET lease_until=0 WHERE id=?", (job["id"],))
                else:
                    db.execute(
                        "UPDATE jobs SET worker_id='other' WHERE id=?", (job["id"],)
                    )
        with pytest.raises((ProviderError, AccessDenied)):
            future.result(timeout=3)
        with pytest.raises((ProviderError, AccessDenied, ValueError)):
            queue.submit(
                "alice", job["id"], request["request_id"], '{"hypothesis":"too late"}'
            )


def test_deadline_does_not_synthesize_completion(leased):
    store, job, _ = leased
    with pytest.raises(ProviderError, match="timed out|expired"):
        completion(services(leased), timeout=0.05)
    with store.connection() as db:
        row = db.execute(
            "SELECT status,response FROM chatgpt_model_requests WHERE job_id=?",
            (job["id"],),
        ).fetchone()
    assert row["status"] in {"expired", "cancelled"} and row["response"] is None


def test_canonical_call_budget_and_schema_references_are_enforced(leased):
    store, job, budget = leased
    queue = ModelRendezvous(store)
    payload = {"messages": MESSAGES, "response_format": FORMAT, "max_tokens": 100}
    for _ in range(budget["max_model_calls"]):
        request_id, _ = queue.enqueue(
            job["id"], "worker-1", payload, time.time() + 30, budget
        )
        queue.submit("alice", job["id"], request_id, '{"hypothesis":"fixture"}')
        assert queue.consume(job["id"], "worker-1", request_id)
    with pytest.raises(ProviderError, match="budget exhausted"):
        queue.enqueue(
            job["id"],
            "worker-1",
            payload,
            time.time() + 30,
            {**budget, "max_model_calls": 100},
        )
    with pytest.raises(ProviderError, match="within the request"):
        services(leased).completion(
            messages=MESSAGES,
            response_format={
                "type": "json_schema",
                "json_schema": {"schema": {"$ref": "https://outside.example/schema"}},
            },
            max_tokens=100,
        )


def test_response_bytes_and_authorization_do_not_depend_on_api_key(leased):
    store, job, _ = leased
    queue = ModelRendezvous(store)
    with pytest.raises(ValueError, match="384 KiB"):
        queue.submit("alice", job["id"], "unknown", '"' + "x" * (384 * 1024) + '"')
    with pytest.raises(ProviderError, match="not authorized"):
        services(leased).public_fetch(
            "open",
            url="https://api.crossref.org/works",
            resource_id="discovery-live-literature",
        )


def test_response_expiring_during_validation_never_gets_receipt(leased, monkeypatch):
    store, job, budget = leased
    queue = ModelRendezvous(store)
    request_id, _ = queue.enqueue(
        job["id"],
        "worker-1",
        {"messages": MESSAGES, "response_format": FORMAT, "max_tokens": 100},
        time.time() + 0.05,
        budget,
    )

    class SlowValidator:
        FORMAT_CHECKER = None

        def __init__(self, *args, **kwargs):
            pass

        def iter_errors(self, value):
            time.sleep(0.08)
            return iter(())

    monkeypatch.setattr(
        "integrations.chatgpt.chatgpt_model.validators.validator_for",
        lambda schema: SlowValidator,
    )
    with pytest.raises(ValueError, match="expired during validation"):
        queue.submit("alice", job["id"], request_id, '{"hypothesis":"late"}')
    with store.connection() as db:
        row = db.execute(
            "SELECT response,status FROM chatgpt_model_requests WHERE id=?",
            (request_id,),
        ).fetchone()
    assert row["response"] is None and row["status"] == "awaiting"
