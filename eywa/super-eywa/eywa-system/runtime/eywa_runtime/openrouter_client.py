"""Minimal OpenRouter client for the Super-Eywa live executor."""

from __future__ import annotations

from dataclasses import dataclass
import json
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen


class OpenRouterClientError(RuntimeError):
    """Raised when OpenRouter requests fail or return malformed data."""


@dataclass(frozen=True)
class OpenRouterClientConfig:
    api_key: str
    base_url: str = "https://openrouter.ai/api/v1"
    referer_url: str | None = None
    title: str | None = "Super-Eywa"


class OpenRouterChatClient:
    def __init__(self, config: OpenRouterClientConfig) -> None:
        if not config.api_key.strip():
            raise OpenRouterClientError("OpenRouter API key must be non-empty.")
        self.config = config

    def create_chat_completion(
        self,
        *,
        model: str,
        messages: list[dict[str, Any]],
        max_tokens: int = 600,
        temperature: float = 0.2,
    ) -> dict[str, Any]:
        body: dict[str, Any] = {
            "model": model,
            "messages": messages,
            "stream": False,
            "max_tokens": max_tokens,
            "temperature": temperature,
        }
        response = self._request_json(
            "POST",
            f"{self.config.base_url}/chat/completions",
            headers=self._headers(),
            body=body,
        )
        if "choices" not in response or not isinstance(response["choices"], list):
            raise OpenRouterClientError("OpenRouter completion response is missing choices.")
        return response

    def get_generation_stats(self, generation_id: str) -> dict[str, Any]:
        query = urlencode({"id": generation_id})
        response = self._request_json(
            "GET",
            f"{self.config.base_url}/generation?{query}",
            headers=self._headers(),
            body=None,
        )
        if "data" not in response or not isinstance(response["data"], dict):
            raise OpenRouterClientError("OpenRouter generation response is missing data.")
        return response

    def _request_json(
        self,
        method: str,
        url: str,
        *,
        headers: dict[str, str],
        body: dict[str, Any] | None,
    ) -> dict[str, Any]:
        data = None if body is None else json.dumps(body).encode("utf-8")
        request = Request(url=url, method=method.upper(), headers=headers, data=data)
        try:
            with urlopen(request, timeout=60) as response:
                payload = response.read().decode("utf-8")
        except HTTPError as exc:
            error_body = exc.read().decode("utf-8", errors="replace")
            raise OpenRouterClientError(f"OpenRouter HTTP {exc.code}: {error_body}") from exc
        except TimeoutError as exc:
            raise OpenRouterClientError("OpenRouter request timed out.") from exc
        except URLError as exc:
            raise OpenRouterClientError(f"OpenRouter request failed: {exc.reason}") from exc
        except OSError as exc:
            raise OpenRouterClientError(f"OpenRouter request failed: {exc}") from exc

        try:
            return json.loads(payload)
        except json.JSONDecodeError as exc:
            raise OpenRouterClientError("OpenRouter returned non-JSON response.") from exc

    def _headers(self) -> dict[str, str]:
        headers = {
            "Authorization": f"Bearer {self.config.api_key}",
            "Content-Type": "application/json",
        }
        if self.config.referer_url:
            headers["HTTP-Referer"] = self.config.referer_url
        if self.config.title:
            headers["X-Title"] = self.config.title
        return headers
