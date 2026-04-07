"""Gemini adapter — real call if `GEMINI_API_KEY` is set, deterministic stub otherwise.

The real path uses `httpx` to POST to the public Gemini generateContent
endpoint with the API key passed as a query param. The stub path returns
three deterministic premises with a slightly different flavor than the
OpenAI stub so the side-by-side UI shows visible differences.
"""
from __future__ import annotations

import logging
import os
import time
from typing import Any, Dict, List, Optional

from idea_factory.adapter import ModelAdapter, Premise, PremiseResult
from idea_factory.adapters._json_parsing import extract_first_json_object, find_premise_list


LOG = logging.getLogger("idea_factory.adapters.gemini_stub")
GEMINI_URL_TEMPLATE = "https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
ENV_KEY = "GEMINI_API_KEY"


def _stub_premises(signal: Dict[str, Any], n: int) -> List[Premise]:
    title = str(signal.get("title") or "an unnamed event").strip()
    base = title.lower().rstrip(".")
    seeds = [
        {
            "logline": f"A bored intern types up the official statement on {base}",
            "synopsis": (
                "A windowless office. The intern types one sentence, deletes it, "
                "types it again. The legal team watches over their shoulder."
            ),
            "tone": "deadpan",
            "twist": "the legal team's notes are also a draft of the same statement",
            "characters": [
                {"name": "Intern", "description": "wired on cold brew"},
                {"name": "Legal", "description": "two identically-suited lawyers"},
            ],
        },
        {
            "logline": f"A community center book club reviews the headline: {base}",
            "synopsis": (
                "Six retirees treat the news story as if it were a novel. They "
                "argue about the protagonist's motivation. Snacks are served."
            ),
            "tone": "absurdist book club",
            "twist": "they unanimously give it three stars",
            "characters": [
                {"name": "Marge", "description": "the harshest reviewer"},
                {"name": "Hank", "description": "wants more car chases"},
            ],
        },
        {
            "logline": f"A weather forecaster keeps trying to pivot back to {base}",
            "synopsis": (
                "A live morning-show meteorologist abandons the weather map and "
                "starts pitching the news story as a sketch. The anchors panic."
            ),
            "tone": "live-tv chaos",
            "twist": "the green-screen starts playing the wrong loop",
            "characters": [
                {"name": "Forecaster", "description": "off-script and free"},
                {"name": "Anchor", "description": "calculating how to cut to commercial"},
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


class GeminiAdapter(ModelAdapter):
    """Google Gemini adapter with a deterministic offline stub."""

    model_id = "gemini-2.5-pro"

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(config)
        if "id" in self.config:
            self.model_id = str(self.config["id"])
        self.api_model: str = str(self.config.get("api_model", "gemini-2.5-pro"))
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
            result.raw_response = "stub: GEMINI_API_KEY not set"
            return result

        started = time.time()
        try:
            import httpx
        except ImportError:
            result.error = "httpx not available"
            return result

        try:
            response = httpx.post(
                GEMINI_URL_TEMPLATE.format(model=self.api_model),
                params={"key": os.environ.get(ENV_KEY)},
                headers={"Content-Type": "application/json"},
                json={
                    "contents": [
                        {"role": "user", "parts": [{"text": prompt}]},
                    ],
                    "generationConfig": {
                        "temperature": 0.7,
                        "responseMimeType": "application/json",
                    },
                },
                timeout=self.timeout_sec,
            )
        except Exception as exc:
            result.error = f"gemini request failed: {exc}"
            result.duration_ms = int((time.time() - started) * 1000)
            return result

        result.duration_ms = int((time.time() - started) * 1000)
        if response.status_code != 200:
            result.error = f"gemini status {response.status_code}: {response.text[:300]}"
            return result

        try:
            payload = response.json()
        except Exception as exc:
            result.error = f"gemini json decode failed: {exc}"
            return result

        try:
            inner_text = payload["candidates"][0]["content"]["parts"][0]["text"]
        except (KeyError, IndexError, TypeError):
            result.error = "gemini response missing candidates[0].content.parts[0].text"
            return result

        result.raw_response = inner_text
        parsed = extract_first_json_object(inner_text)
        if parsed is None:
            result.error = "gemini response did not contain a JSON object"
            return result
        premise_dicts = find_premise_list(parsed)
        if not premise_dicts:
            result.error = "gemini response had no premises"
            return result
        result.premises = [Premise.from_dict(p) for p in premise_dicts[:n_premises]]
        return result


__all__ = ["GeminiAdapter"]
