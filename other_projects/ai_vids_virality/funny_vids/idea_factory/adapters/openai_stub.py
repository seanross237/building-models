"""OpenAI adapter — real call if `OPENAI_API_KEY` is set, deterministic stub otherwise.

The real path uses `httpx` to POST to `/v1/chat/completions`. The stub
path returns three deterministic premises derived from the signal title
so tests can assert exact output.
"""
from __future__ import annotations

import logging
import os
import time
from typing import Any, Dict, List, Optional

from idea_factory.adapter import ModelAdapter, Premise, PremiseResult
from idea_factory.adapters._json_parsing import extract_first_json_object, find_premise_list


LOG = logging.getLogger("idea_factory.adapters.openai_stub")
OPENAI_URL = "https://api.openai.com/v1/chat/completions"
ENV_KEY = "OPENAI_API_KEY"


def _stub_premises(signal: Dict[str, Any], n: int) -> List[Premise]:
    title = str(signal.get("title") or "an unnamed event").strip()
    base = title.lower().rstrip(".")
    seeds = [
        {
            "logline": f"Two coworkers nervously discuss the day {base}",
            "synopsis": (
                "An open-plan office tries to act normal. One employee keeps "
                "glancing at the news. The other refuses to acknowledge it."
            ),
            "tone": "dry workplace",
            "twist": "the boss has been the news source the whole time",
            "characters": [
                {"name": "Riley", "description": "the one who can't stop bringing it up"},
                {"name": "Dana", "description": "the one performing normalcy"},
            ],
        },
        {
            "logline": f"A local news crew tries to get a calm quote about {base}",
            "synopsis": (
                "A reporter pushes a microphone into the face of every passerby. "
                "Each answer is more unhinged than the last. The cameraman gives up."
            ),
            "tone": "mockumentary",
            "twist": "the third passerby is the original subject in disguise",
            "characters": [
                {"name": "Reporter", "description": "earnest, exhausted"},
                {"name": "Passerby", "description": "wildly opinionated"},
            ],
        },
        {
            "logline": f"Two AI assistants on a desk argue whether {base} is real",
            "synopsis": (
                "Two voice assistants on the same desk debate the merits of the "
                "story until their owner walks in and unplugs them both."
            ),
            "tone": "absurdist",
            "twist": "the owner is also an AI, but doesn't know it",
            "characters": [
                {"name": "Assistant A", "description": "credulous"},
                {"name": "Assistant B", "description": "skeptical"},
                {"name": "Owner", "description": "blissfully unaware"},
            ],
        },
    ]
    chosen = seeds[: max(1, n)]
    return [
        Premise(
            logline=c["logline"],
            synopsis=c["synopsis"],
            tone=c["tone"],
            target_length_sec=30,
            characters=c["characters"],
            twist=c["twist"],
        )
        for c in chosen
    ]


class OpenAIAdapter(ModelAdapter):
    """OpenAI chat-completions adapter with a deterministic offline stub."""

    model_id = "gpt-5"

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(config)
        if "id" in self.config:
            self.model_id = str(self.config["id"])
        self.api_model: str = str(self.config.get("api_model", "gpt-5"))
        self.timeout_sec: int = int(self.config.get("timeout_sec", 120))

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

        if not self.is_available():
            result.premises = _stub_premises(signal, n_premises)
            result.raw_response = "stub: OPENAI_API_KEY not set"
            return result

        started = time.time()
        try:
            import httpx  # local import so the test path works without httpx in stub mode
        except ImportError:
            result.error = "httpx not available"
            return result

        try:
            response = httpx.post(
                OPENAI_URL,
                headers={
                    "Authorization": f"Bearer {os.environ.get(ENV_KEY)}",
                    "Content-Type": "application/json",
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
            result.error = f"openai request failed: {exc}"
            result.duration_ms = int((time.time() - started) * 1000)
            return result

        result.duration_ms = int((time.time() - started) * 1000)
        if response.status_code != 200:
            result.error = f"openai status {response.status_code}: {response.text[:300]}"
            return result
        try:
            payload = response.json()
        except Exception as exc:
            result.error = f"openai json decode failed: {exc}"
            return result

        try:
            inner_text = payload["choices"][0]["message"]["content"]
        except (KeyError, IndexError, TypeError):
            result.error = "openai response missing choices[0].message.content"
            return result

        result.raw_response = inner_text
        parsed = extract_first_json_object(inner_text)
        if parsed is None:
            result.error = "openai response did not contain a JSON object"
            return result
        premise_dicts = find_premise_list(parsed)
        if not premise_dicts:
            result.error = "openai response had no premises"
            return result
        result.premises = [Premise.from_dict(p) for p in premise_dicts[:n_premises]]
        return result


__all__ = ["OpenAIAdapter"]
