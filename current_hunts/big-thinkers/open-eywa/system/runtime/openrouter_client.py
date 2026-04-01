from __future__ import annotations

from dataclasses import dataclass
import json
from typing import Any, Protocol
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen


class OpenRouterClientError(RuntimeError):
    """Raised when OpenRouter requests fail or return malformed data."""


class JsonHttpTransport(Protocol):
    def request_json(
        self,
        method: str,
        url: str,
        *,
        headers: dict[str, str],
        body: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Execute an HTTP request and return parsed JSON."""


class UrllibJsonTransport:
    def request_json(
        self,
        method: str,
        url: str,
        *,
        headers: dict[str, str],
        body: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        data = None if body is None else json.dumps(body).encode("utf-8")
        request = Request(url=url, method=method.upper(), headers=headers, data=data)
        try:
            with urlopen(request, timeout=60) as response:
                payload = response.read().decode("utf-8")
        except HTTPError as exc:
            error_body = exc.read().decode("utf-8", errors="replace")
            raise OpenRouterClientError(
                f"OpenRouter HTTP {exc.code}: {error_body}"
            ) from exc
        except URLError as exc:
            raise OpenRouterClientError(f"OpenRouter request failed: {exc.reason}") from exc

        try:
            return json.loads(payload)
        except json.JSONDecodeError as exc:
            raise OpenRouterClientError("OpenRouter returned non-JSON response.") from exc


@dataclass(frozen=True)
class OpenRouterClientConfig:
    api_key: str
    base_url: str = "https://openrouter.ai/api/v1"
    referer_url: str | None = None
    title: str | None = "Open-Eywa"


class OpenRouterChatClient:
    def __init__(
        self,
        config: OpenRouterClientConfig,
        *,
        transport: JsonHttpTransport | None = None,
    ) -> None:
        if not config.api_key.strip():
            raise OpenRouterClientError("OpenRouter API key must be non-empty.")
        self.config = config
        self.transport = transport or UrllibJsonTransport()

    def create_chat_completion(
        self,
        *,
        model: str,
        messages: list[dict[str, Any]],
        tools: list[dict[str, Any]] | None = None,
        tool_choice: str | dict[str, Any] | None = "auto",
        max_tokens: int | None = None,
        temperature: float | None = None,
    ) -> dict[str, Any]:
        body: dict[str, Any] = {
            "model": model,
            "messages": messages,
            "stream": False,
        }
        if tools:
            body["tools"] = tools
            body["tool_choice"] = tool_choice
        if max_tokens is not None:
            body["max_tokens"] = max_tokens
        if temperature is not None:
            body["temperature"] = temperature

        response = self.transport.request_json(
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
        response = self.transport.request_json(
            "GET",
            f"{self.config.base_url}/generation?{query}",
            headers=self._headers(),
        )
        if "data" not in response or not isinstance(response["data"], dict):
            raise OpenRouterClientError("OpenRouter generation response is missing data.")
        return response

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
