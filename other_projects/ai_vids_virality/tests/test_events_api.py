"""Tests for the Phase 7 SSE events endpoint."""
from __future__ import annotations

import asyncio
import json
from pathlib import Path
from typing import Iterator

import pytest
from fastapi.testclient import TestClient

import backend.main as backend_main
from backend import events as backend_events


@pytest.fixture()
def client(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Iterator[TestClient]:
    monkeypatch.setenv("AI_VIDS_DATA_ROOT", str(tmp_path))
    with TestClient(backend_main.app) as test_client:
        yield test_client


def _run(coro) -> None:
    """Helper: run a coroutine in a fresh event loop so tests don't
    pollute each other via `get_event_loop()`."""
    loop = asyncio.new_event_loop()
    try:
        loop.run_until_complete(coro)
    finally:
        loop.close()


def test_events_endpoint_advertises_sse_content_type(client: TestClient) -> None:
    """Inspect the StreamingResponse directly without reading the body.

    FastAPI's TestClient can block on streaming generators that have
    no immediate data to yield, so we call the endpoint function
    directly and inspect its `media_type`.
    """
    loop = asyncio.new_event_loop()
    try:
        response = loop.run_until_complete(backend_main.events_stream())
        assert response.media_type == "text/event-stream"
        assert response.headers.get("cache-control") == "no-cache"
        # The endpoint registered one subscriber — clean it up.
        loop.run_until_complete(
            backend_events.unsubscribe(backend_events._next_client_id - 1)
        )
    finally:
        loop.close()


def test_publish_event_fans_out_to_subscribers() -> None:
    """publish_event should deliver a frame to every connected subscriber."""

    async def scenario() -> None:
        # Initial sanity: no subscribers.
        assert backend_events.subscriber_count() == 0

        client_a = await backend_events.subscribe()
        client_b = await backend_events.subscribe()
        assert backend_events.subscriber_count() == 2
        try:
            backend_events.publish_event(
                "pipeline_update",
                {"sketch_id": "sk-x", "from": "critic_review", "to": "published"},
            )
            for cid in (client_a, client_b):
                queue = backend_events._subscribers[cid]  # type: ignore[attr-defined]
                frame = await asyncio.wait_for(queue.get(), timeout=1)
                assert "event: pipeline_update" in frame
                parsed = json.loads(
                    frame.split("data:", 1)[1].split("\n\n", 1)[0].strip()
                )
                assert parsed["sketch_id"] == "sk-x"
                assert parsed["to"] == "published"
                assert "ts" in parsed
                assert parsed["event_type"] == "pipeline_update"
        finally:
            await backend_events.unsubscribe(client_a)
            await backend_events.unsubscribe(client_b)

    _run(scenario())
    assert backend_events.subscriber_count() == 0


def test_publish_event_noop_with_no_subscribers() -> None:
    """Publishing an event with zero subscribers must be a no-op, not a crash."""
    assert backend_events.subscriber_count() == 0
    backend_events.publish_event("pipeline_update", {"sketch_id": "sk-y"})
    assert backend_events.subscriber_count() == 0


def test_publish_event_full_queue_drops_oldest() -> None:
    """When a subscriber's queue fills up, publish_event should still
    deliver the newest frame by dropping the oldest one."""

    async def scenario() -> None:
        client_id = await backend_events.subscribe()
        queue = backend_events._subscribers[client_id]  # type: ignore[attr-defined]
        try:
            # Fill the queue to its max.
            while True:
                try:
                    queue.put_nowait("filler\n\n")
                except asyncio.QueueFull:
                    break
            # Publishing a new event should evict oldest + land at tail.
            backend_events.publish_event("pipeline_update", {"sketch_id": "sk-latest"})
            saw_update = False
            while not queue.empty():
                frame = queue.get_nowait()
                if "pipeline_update" in frame:
                    saw_update = True
            assert saw_update
        finally:
            await backend_events.unsubscribe(client_id)

    _run(scenario())


def test_publish_event_called_from_transition_endpoint(client: TestClient) -> None:
    """When a state transition fires, the events stream should see
    a `pipeline_update` frame. We subscribe manually, fire a manual idea
    (which transitions a new sketch into premise_review and emits the
    event), and drain the subscriber queue.
    """

    async def scenario() -> None:
        client_id = await backend_events.subscribe()
        queue = backend_events._subscribers[client_id]  # type: ignore[attr-defined]
        try:
            # Manual idea creation fires a pipeline_update event.
            res = client.post(
                "/api/manual_idea",
                json={"text": "a quick test idea for the events pipe"},
            )
            assert res.status_code == 200
            frame = await asyncio.wait_for(queue.get(), timeout=1)
            assert "event: pipeline_update" in frame
            parsed = json.loads(
                frame.split("data:", 1)[1].split("\n\n", 1)[0].strip()
            )
            assert parsed["to"] == "premise_review"
            assert parsed["source"] == "manual"
        finally:
            await backend_events.unsubscribe(client_id)

    _run(scenario())
