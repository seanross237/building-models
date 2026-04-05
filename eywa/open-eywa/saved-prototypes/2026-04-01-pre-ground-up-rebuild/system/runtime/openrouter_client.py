from __future__ import annotations

import json
import socket
import time
import urllib.error
import urllib.request
from typing import Any


class OpenRouterError(RuntimeError):
    pass


class OpenRouterClient:
    def __init__(
        self,
        *,
        api_key: str,
        api_base_url: str,
        chat_endpoint: str,
        timeout_seconds: int,
        max_retries: int,
        retry_backoff_seconds: float,
        app_name: str,
        app_url: str,
    ) -> None:
        self.api_key = api_key
        self.url = api_base_url.rstrip("/") + chat_endpoint
        self.timeout_seconds = timeout_seconds
        self.max_retries = max(1, max_retries)
        self.retry_backoff_seconds = max(0.0, retry_backoff_seconds)
        self.app_name = app_name
        self.app_url = app_url

    def chat_completion(
        self,
        *,
        model: str,
        messages: list[dict[str, Any]],
        tools: list[dict[str, Any]],
        temperature: float,
        max_completion_tokens: int,
    ) -> dict[str, Any]:
        payload = {
            "model": model,
            "messages": messages,
            "tools": tools,
            "tool_choice": "auto",
            "temperature": temperature,
            "max_tokens": max_completion_tokens,
        }
        body = json.dumps(payload).encode("utf-8")
        request = urllib.request.Request(
            self.url,
            data=body,
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
                "HTTP-Referer": self.app_url,
                "X-Title": self.app_name,
            },
            method="POST",
        )
        last_error: Exception | None = None
        for attempt in range(1, self.max_retries + 1):
            try:
                with urllib.request.urlopen(request, timeout=self.timeout_seconds) as response:
                    payload = json.loads(response.read().decode("utf-8"))
                    if payload.get("error"):
                        message = json.dumps(payload["error"], ensure_ascii=True)
                        last_error = OpenRouterError(f"OpenRouter response error: {message}")
                    elif not payload.get("choices"):
                        preview = json.dumps(payload, ensure_ascii=True)[:1200]
                        last_error = OpenRouterError(
                            f"OpenRouter returned a malformed response without choices: {preview}"
                        )
                    else:
                        return payload
            except urllib.error.HTTPError as exc:
                details = exc.read().decode("utf-8", errors="replace")
                if exc.code in {429, 500, 502, 503, 504}:
                    last_error = OpenRouterError(f"OpenRouter HTTP {exc.code}: {details}")
                else:
                    raise OpenRouterError(f"OpenRouter HTTP {exc.code}: {details}") from exc
            except (TimeoutError, socket.timeout) as exc:
                last_error = exc
            except urllib.error.URLError as exc:
                last_error = exc

            if attempt < self.max_retries:
                time.sleep(self.retry_backoff_seconds * attempt)

        if isinstance(last_error, OpenRouterError):
            raise last_error
        if isinstance(last_error, urllib.error.URLError):
            raise OpenRouterError(f"OpenRouter request failed: {last_error}") from last_error
        raise OpenRouterError("OpenRouter request timed out while reading the response.") from last_error
