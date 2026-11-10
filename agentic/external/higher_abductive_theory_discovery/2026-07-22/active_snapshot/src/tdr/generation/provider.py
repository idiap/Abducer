"""Provider-neutral generative interface.

Provider text is always treated as a proposal. It never mutates canonical
state and must be normalized by a skill before it can enter validation.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Protocol


class GeneratorProvider(Protocol):
    provider_id: str

    def generate(self, task: str, context: dict[str, Any], *, seed: int, n: int) -> list[dict[str, Any]]:
        """Return conjectural proposals; callers validate and label them."""


@dataclass(slots=True)
class DeterministicProvider:
    provider_id: str = "deterministic-local"

    def generate(self, task: str, context: dict[str, Any], *, seed: int = 0, n: int = 1) -> list[dict[str, Any]]:
        modes = context.get("modes") or ["local", "bridge", "mechanism", "mutation"]
        return [
            {
                "mode": modes[index % len(modes)],
                "proposal": f"{task}: apply {modes[index % len(modes)]} completion {index + 1}",
                "seed": seed,
                "provider_id": self.provider_id,
                "epistemic_status": "conjectural",
            }
            for index in range(n)
        ]


@dataclass(slots=True)
class CallableProvider:
    """Adapter for a local/hosted SDK callable without importing that SDK."""

    fn: Any
    provider_id: str = "callable-provider"

    def generate(self, task: str, context: dict[str, Any], *, seed: int = 0, n: int = 1) -> list[dict[str, Any]]:
        value = self.fn(task=task, context=context, seed=seed, n=n)
        if not isinstance(value, list) or not all(isinstance(item, dict) for item in value):
            raise TypeError("provider must return list[dict]")
        return value

