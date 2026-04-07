"""Hacker News collector.

Hits the public Firebase API at `https://hacker-news.firebaseio.com/v0/`.
No auth, no API key. We pull the top-stories list and then fetch each
item, write a signal markdown file, and dedupe via `.seen-ids`.
"""
from __future__ import annotations

import logging
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

import requests

from collectors._common import (
    append_seen_id,
    hours_since,
    read_seen_ids,
    render_signal_markdown,
    sanitize_one_line,
    write_signal_file,
)
from state.store import Store


SOURCE_NAME = "hacker_news"
TOPSTORIES_URL = "https://hacker-news.firebaseio.com/v0/topstories.json"
ITEM_URL = "https://hacker-news.firebaseio.com/v0/item/{id}.json"
LOG = logging.getLogger("collectors.hacker_news")

DEFAULT_CONFIG: Dict[str, Any] = {
    "limit": 30,
    "max_age_hours": 24,
}


def _fetch_top_ids(http: Any, limit: int) -> List[int]:
    try:
        resp = http.get(TOPSTORIES_URL, timeout=15)
    except Exception as exc:  # pragma: no cover
        LOG.warning("hn topstories fetch failed: %s", exc)
        return []
    if getattr(resp, "status_code", 0) != 200:
        return []
    try:
        ids = resp.json() or []
    except Exception as exc:  # pragma: no cover
        LOG.warning("hn topstories json parse failed: %s", exc)
        return []
    return [int(x) for x in ids[:limit] if isinstance(x, (int, str))]


def _fetch_item(http: Any, item_id: int) -> Optional[Dict[str, Any]]:
    try:
        resp = http.get(ITEM_URL.format(id=item_id), timeout=15)
    except Exception as exc:  # pragma: no cover
        LOG.warning("hn item %s fetch failed: %s", item_id, exc)
        return None
    if getattr(resp, "status_code", 0) != 200:
        return None
    try:
        return resp.json()
    except Exception:  # pragma: no cover
        return None


def _item_to_signal(
    item: Dict[str, Any],
    max_age_hours: float,
) -> Optional[Dict[str, Any]]:
    if not isinstance(item, dict):
        return None
    if item.get("type") not in ("story", None):
        return None
    if item.get("dead") or item.get("deleted"):
        return None
    item_id = item.get("id")
    title = item.get("title")
    if not item_id or not title:
        return None
    timestamp = item.get("time")
    if timestamp is None:
        return None
    try:
        published_at = datetime.fromtimestamp(float(timestamp), tz=timezone.utc)
    except (TypeError, ValueError):
        return None
    if hours_since(published_at) > max_age_hours:
        return None

    score = int(item.get("score", 0) or 0)
    descendants = int(item.get("descendants", 0) or 0)
    heat = min(1.0, (score / 1000.0) + (descendants / 500.0))

    body = item.get("text") or ""
    if len(body) > 1500:
        body = body[:1500] + "..."

    source_url = item.get("url") or f"https://news.ycombinator.com/item?id={item_id}"

    return {
        "id": f"hn-{item_id}",
        "source_url": source_url,
        "title": sanitize_one_line(title),
        "summary": sanitize_one_line(body)[:400] or sanitize_one_line(title),
        "body": body or title,
        "published_at": published_at,
        "heat_score_raw": heat,
        "tags": ["hacker_news", "tech"],
    }


def fetch(
    store: Store,
    config: Optional[Dict[str, Any]] = None,
    http: Any = None,
) -> List[str]:
    cfg: Dict[str, Any] = {**DEFAULT_CONFIG, **(config or {})}
    http_client = http or requests
    items_dir = store.signals_dir / SOURCE_NAME / "items"
    seen_path = store.seen_ids_path(SOURCE_NAME)
    seen_path.parent.mkdir(parents=True, exist_ok=True)
    seen_path.touch(exist_ok=True)
    seen = read_seen_ids(seen_path)

    new_ids: List[str] = []
    top_ids = _fetch_top_ids(http_client, int(cfg.get("limit", 30)))
    for item_id in top_ids:
        item = _fetch_item(http_client, item_id)
        signal = _item_to_signal(item or {}, float(cfg.get("max_age_hours", 24)))
        if not signal:
            continue
        sid = signal["id"]
        if sid in seen:
            continue
        markdown = render_signal_markdown(
            signal_id=sid,
            source=SOURCE_NAME,
            source_url=signal["source_url"],
            title=signal["title"],
            summary=signal["summary"],
            body=signal["body"],
            published_at=signal["published_at"],
            heat_score_raw=signal["heat_score_raw"],
            tags=signal["tags"],
        )
        write_signal_file(items_dir, sid, markdown)
        append_seen_id(seen_path, sid)
        seen.add(sid)
        new_ids.append(sid)
    return new_ids
