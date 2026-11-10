# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
# SPDX-License-Identifier: MIT
"""Bounded host services for the unchanged native research adapter.

Credentials and model selection are operator configuration, never research input.
The adapter keeps native prompts and schemas while translating the host's
completion-shaped interface to the Responses API. It does not retry paid calls.
"""

from __future__ import annotations

import base64
import io
import json
import os
import time
from types import SimpleNamespace
from urllib.error import HTTPError, URLError
from urllib.parse import urlsplit
from urllib.request import HTTPRedirectHandler, Request, build_opener
from uuid import uuid4


class ProviderError(RuntimeError):
    """A bounded provider operation failed without exposing credentials."""


class NoRedirect(HTTPRedirectHandler):
    """Never forward API credentials or literature requests through redirects."""

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        raise ProviderError("Provider redirects are disabled")


def provider_settings() -> tuple[str, str, str]:
    """Read trusted operator settings; do not inspect user checkout secrets."""
    model = os.environ.get("ABDUCER_MODEL", "").strip()
    key = os.environ.get("OPENAI_API_KEY", "").strip()
    base = os.environ.get("OPENAI_BASE_URL", "https://api.openai.com/v1").rstrip("/")
    parsed = urlsplit(base)
    if not model or not key:
        raise ProviderError("Configure ABDUCER_MODEL and OPENAI_API_KEY for the worker")
    if (
        parsed.scheme != "https"
        or not parsed.hostname
        or parsed.username
        or parsed.password
        or parsed.query
        or parsed.fragment
    ):
        raise ProviderError(
            "OPENAI_BASE_URL must be an HTTPS endpoint without credentials or query"
        )
    return model, key, base


class PublicLiteratureServices:
    """Shared bounded literature and timing services, independent of model keys."""

    def __init__(
        self, budget: dict, *, allow_public_network: bool, event=None, opener=None
    ):
        self.budget = budget
        self.deadline = time.monotonic() + budget["timeout_seconds"]
        self.calls = 0
        self.fetches = 0
        self.allow_public_network = allow_public_network
        self._event = event or (lambda *args: None)
        self._opener = opener or build_opener(NoRedirect())
        self._streams: dict[str, io.BytesIO] = {}

    def event(self, kind: str, payload: dict) -> None:
        """Forward bounded native progress without provider payloads or keys."""
        self._event(kind, payload)

    def _remaining(self, requested: float = 1200) -> float:
        remaining = self.deadline - time.monotonic()
        if remaining <= 0:
            raise ProviderError("Research deadline exceeded")
        return min(float(requested), remaining)

    def public_fetch(self, operation: str, **arguments) -> dict:
        """Serve the native bounded open/read/close literature protocol.

        Only the two canonical HTTPS API paths are reachable. Neither arbitrary
        URLs, redirects, arbitrary headers nor credential-bearing requests are
        accepted from research content.
        """
        if not self.allow_public_network:
            raise ProviderError("Public literature access is not authorized")
        if operation == "open":
            parsed = urlsplit(arguments.get("url", ""))
            allowed = {
                ("api.crossref.org", "/works"),
                ("export.arxiv.org", "/api/query"),
            }
            if (
                parsed.scheme != "https"
                or (parsed.hostname, parsed.path) not in allowed
                or parsed.port not in {None, 443}
                or parsed.username
                or parsed.password
                or parsed.fragment
                or arguments.get("method", "GET") != "GET"
                or arguments.get("resource_id") != "discovery-live-literature"
            ):
                raise ProviderError(
                    "Literature request is outside the declared API scope"
                )
            if self.fetches >= 6:
                raise ProviderError("Literature query budget exhausted")
            self.fetches += 1
            request = Request(
                arguments["url"],
                headers={"Accept": "*/*", "User-Agent": "AbducerResearch/0.1"},
            )
            try:
                with self._opener.open(
                    request, timeout=self._remaining(60)
                ) as response:
                    data = response.read(4 * 1024 * 1024 + 1)
            except (HTTPError, URLError, TimeoutError):
                raise ProviderError("Declared literature API unavailable") from None
            if len(data) > 4 * 1024 * 1024:
                raise ProviderError("Literature response exceeds byte budget")
            token = uuid4().hex
            self._streams[token] = io.BytesIO(data)
            return {"token": token}
        token = arguments.get("token")
        if token not in self._streams:
            raise ProviderError("Unknown literature response token")
        if operation == "read":
            size = arguments.get("size", 65536)
            if not isinstance(size, int) or not 1 <= size <= 65536:
                raise ProviderError("Invalid literature chunk size")
            return {"data": base64.b64encode(self._streams[token].read(size)).decode()}
        if operation == "close":
            self._streams.pop(token).close()
            return {}
        raise ProviderError("Unknown literature operation")


class HostedServices(PublicLiteratureServices):
    """Preserve the native completion protocol through a configured API model."""

    def __init__(
        self, budget: dict, *, allow_public_network: bool, event=None, opener=None
    ):
        model, self._key, self._base = provider_settings()
        self.model = SimpleNamespace(model_id=model)
        super().__init__(
            budget,
            allow_public_network=allow_public_network,
            event=event,
            opener=opener,
        )

    def completion(
        self,
        *,
        messages,
        response_format,
        max_tokens,
        reasoning_effort=None,
        timeout=1200,
    ):
        """Preserve the native requested schema; reject excess budgets outright."""
        if self.calls >= self.budget["max_model_calls"]:
            raise ProviderError("Model call budget exhausted")
        if (
            not isinstance(max_tokens, int)
            or not 1 <= max_tokens <= self.budget["max_output_tokens"]
        ):
            raise ProviderError(
                "Native request exceeds the approved output token budget"
            )
        fmt = dict(response_format)
        if fmt.get("type") == "json_schema":
            fmt = {"type": "json_schema", **fmt["json_schema"]}
        if fmt.get("type") not in {"json_schema", "json_object"}:
            raise ProviderError("Unsupported native response format")
        payload = {
            "model": self.model.model_id,
            "input": messages,
            "text": {"format": fmt},
            "max_output_tokens": max_tokens,
            "store": False,
        }
        if reasoning_effort:
            payload["reasoning"] = {"effort": reasoning_effort}
        raw = json.dumps(payload, allow_nan=False).encode()
        if len(raw) > 8 * 1024 * 1024:
            raise ProviderError("Native request exceeds the provider byte budget")
        self.calls += 1  # A network failure is still a consumed call; never auto-retry.
        request = Request(
            self._base + "/responses",
            data=raw,
            method="POST",
            headers={
                "Authorization": "Bearer " + self._key,
                "Content-Type": "application/json",
            },
        )
        try:
            with self._opener.open(
                request, timeout=self._remaining(timeout)
            ) as response:
                data = response.read(8 * 1024 * 1024 + 1)
        except HTTPError as exc:
            raise ProviderError(f"Model provider returned HTTP {exc.code}") from None
        except (URLError, TimeoutError):
            raise ProviderError("Model provider unavailable or timed out") from None
        if len(data) > 8 * 1024 * 1024:
            raise ProviderError("Model response exceeds byte budget")
        try:
            reply = json.loads(data)
            if reply.get("status") != "completed":
                raise ProviderError("Model response was incomplete or failed")
            parts = [
                part
                for item in reply.get("output", [])
                for part in item.get("content", [])
            ]
            if any(part.get("type") == "refusal" for part in parts):
                raise ProviderError("Model refused the native research request")
            content = "".join(
                part["text"] for part in parts if part.get("type") == "output_text"
            )
            if not content:
                raise ProviderError("Model response has no research artifact")
        except (ValueError, KeyError, TypeError):
            raise ProviderError("Malformed model provider response") from None
        return {
            "id": reply.get("id", ""),
            "model": reply.get("model", self.model.model_id),
            "choices": [
                {
                    "finish_reason": "stop",
                    "message": {"role": "assistant", "content": content},
                }
            ],
            "usage": reply.get("usage", {}),
        }
