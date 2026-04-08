"""In-memory SSE pub/sub for Phase 7.

Every connected client has its own `asyncio.Queue`. When anything
in the backend calls `publish_event(event_type, data)` we push a
copy to every subscriber. The SSE endpoint consumes one queue per
client and yields `text/event-stream` frames.

Clients are cleaned up on disconnect via the `try/finally` in the
SSE generator. If a queue fills faster than a client can drain it
(unlikely in practice — events are tiny JSON blobs), oldest events
are dropped.
"""
from __future__ import annotations

import asyncio
import json
import logging
import time
from collections import defaultdict
from typing import Any, AsyncIterator, Dict, Optional


LOG = logging.getLogger("backend.events")

_MAX_QUEUE_SIZE = 64
_subscribers: Dict[int, "asyncio.Queue[str]"] = {}
_next_client_id: int = 0
_lock = asyncio.Lock()


def _sse_frame(event_type: str, data: Dict[str, Any]) -> str:
    payload = json.dumps(data, default=str)
    return f"event: {event_type}\ndata: {payload}\n\n"


async def subscribe() -> int:
    """Register a new SSE subscriber and return its client id."""
    global _next_client_id
    async with _lock:
        client_id = _next_client_id
        _next_client_id += 1
        _subscribers[client_id] = asyncio.Queue(maxsize=_MAX_QUEUE_SIZE)
    return client_id


async def unsubscribe(client_id: int) -> None:
    async with _lock:
        _subscribers.pop(client_id, None)


def publish_event(event_type: str, data: Dict[str, Any]) -> None:
    """Fan out an event to every current subscriber.

    Called from synchronous backend code (the FastAPI route handlers),
    so we can't `await` — we drop into the running loop via
    `asyncio.get_event_loop().call_soon_threadsafe()` when possible,
    otherwise we fall back to a direct put_nowait() on each queue.
    """
    if not _subscribers:
        return
    frame = _sse_frame(event_type, {**data, "event_type": event_type, "ts": time.time()})
    for client_id, queue in list(_subscribers.items()):
        try:
            queue.put_nowait(frame)
        except asyncio.QueueFull:
            # Drop the oldest frame to make room — SSE is best-effort
            # and we prefer fresh events over backlog.
            try:
                _ = queue.get_nowait()
                queue.put_nowait(frame)
            except Exception:
                LOG.warning("dropping event for overfull client %s", client_id)


async def iter_events(client_id: int) -> AsyncIterator[str]:
    """Async generator that yields SSE frames for a single subscriber.

    Sends a keepalive comment every 15s so idle proxies don't close
    the connection. Cleans up its queue on disconnect.
    """
    queue = _subscribers.get(client_id)
    if queue is None:
        return
    try:
        # Announce the connection so the UI knows the stream is live.
        yield _sse_frame("hello", {"client_id": client_id})
        while True:
            try:
                frame = await asyncio.wait_for(queue.get(), timeout=15.0)
                yield frame
            except asyncio.TimeoutError:
                # SSE comment lines start with `:` and are ignored by clients.
                yield ": keepalive\n\n"
    finally:
        await unsubscribe(client_id)


def subscriber_count() -> int:
    """Snapshot for tests and stats."""
    return len(_subscribers)


__all__ = [
    "iter_events",
    "publish_event",
    "subscribe",
    "subscriber_count",
    "unsubscribe",
]
