"""OpenRouter adapter — OpenAI-compatible chat-completions for any OpenRouter model.

One adapter, N model slugs. Configure per-model via `config/models.yaml`:

  - id: gpt-5
    enabled: true
    adapter: idea_factory.adapters.openrouter.OpenRouterAdapter
    config:
      api_model: openai/gpt-5
      timeout_sec: 120

  - id: gemini-2.5-pro
    enabled: true
    adapter: idea_factory.adapters.openrouter.OpenRouterAdapter
    config:
      api_model: google/gemini-2.5-pro
      timeout_sec: 120

`is_available()` checks `OPENROUTER_API_KEY`. The endpoint is
`https://openrouter.ai/api/v1/chat/completions`. Auth header is
`Authorization: Bearer <key>`. The body shape is identical to OpenAI's
chat-completions, with one OpenRouter-specific addition: `HTTP-Referer`
and `X-Title` headers (recommended by OpenRouter for free-tier rate
limit grace; not required).

Unlike the Phase 3 `OpenAIAdapter` / `GeminiAdapter`, there is NO
deterministic stub fallback here. If `OPENROUTER_API_KEY` is missing we
return a `PremiseResult` with `error` set and let the factory move on.
The legacy stubs are still on disk (and listed as `*-stub` entries with
`enabled: false` in `config/models.yaml`) if anyone needs the fallback.
"""
from __future__ import annotations

import logging
import os
import time
from typing import Any, Dict, Optional

from idea_factory.adapter import ModelAdapter, Premise, PremiseResult
from idea_factory.adapters._json_parsing import extract_first_json_object, find_premise_list


LOG = logging.getLogger("idea_factory.adapters.openrouter")
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
ENV_KEY = "OPENROUTER_API_KEY"

# Recommended-but-optional headers so OpenRouter's free-tier grace kicks
# in (they identify the caller in their dashboard). Harmless on paid
# accounts.
DEFAULT_REFERER = "https://github.com/seanross237/ai_vids_virality"
DEFAULT_TITLE = "ai_vids_virality"


class OpenRouterAdapter(ModelAdapter):
    """Unified OpenRouter adapter — one class, many model slugs."""

    model_id = "openrouter"

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(config)
        # The factory passes `id` through from `config/models.yaml` so
        # the leaderboard rows stay stable across phases. Override the
        # default `model_id` with whatever the registry entry is called.
        if "id" in self.config:
            self.model_id = str(self.config["id"])
        self.api_model: str = str(self.config.get("api_model", "openai/gpt-5"))
        self.timeout_sec: int = int(self.config.get("timeout_sec", 120))
        self.referer: str = str(self.config.get("referer", DEFAULT_REFERER))
        self.title: str = str(self.config.get("title", DEFAULT_TITLE))

    def is_available(self) -> bool:
        return bool(os.environ.get(ENV_KEY))

    # ----------------------------------------------------------------- generate

    def generate(
        self,
        signal: Dict[str, Any],
        prompt: str,
        n_premises: int = 3,
    ) -> PremiseResult:
        signal_id = str(signal.get("signal_id") or signal.get("id") or "unknown")
        result = PremiseResult(model_id=self.model_id, signal_id=signal_id)

        key = os.environ.get(ENV_KEY)
        if not key:
            result.error = "OPENROUTER_API_KEY not set"
            return result

        started = time.time()
        try:
            import httpx  # local import so tests that never touch this adapter don't pay the cost
        except ImportError:
            result.error = "httpx not available"
            return result

        try:
            response = httpx.post(
                OPENROUTER_URL,
                headers={
                    "Authorization": f"Bearer {key}",
                    "Content-Type": "application/json",
                    "HTTP-Referer": self.referer,
                    "X-Title": self.title,
                },
                json={
                    "model": self.api_model,
                    "messages": [
                        {"role": "system", "content": "You output only strict JSON."},
                        {"role": "user", "content": prompt},
                    ],
                    "temperature": 0.7,
                    "response_format": {"type": "json_object"},
                },
                timeout=self.timeout_sec,
            )
        except Exception as exc:
            result.error = f"openrouter request failed: {exc}"
            result.duration_ms = int((time.time() - started) * 1000)
            return result

        result.duration_ms = int((time.time() - started) * 1000)
        if response.status_code != 200:
            result.error = f"openrouter status {response.status_code}: {response.text[:300]}"
            return result
        try:
            payload = response.json()
        except Exception as exc:
            result.error = f"openrouter json decode failed: {exc}"
            return result

        try:
            inner_text = payload["choices"][0]["message"]["content"]
        except (KeyError, IndexError, TypeError):
            result.error = "openrouter response missing choices[0].message.content"
            return result

        result.raw_response = inner_text
        parsed = extract_first_json_object(inner_text)
        if parsed is None:
            result.error = "openrouter response did not contain a JSON object"
            return result
        premise_dicts = find_premise_list(parsed)
        if not premise_dicts:
            result.error = "openrouter response had no premises"
            return result
        result.premises = [Premise.from_dict(p) for p in premise_dicts[:n_premises]]
        return result


__all__ = ["OpenRouterAdapter"]
