"""Google News RSS collector.

Pulls one or more Google News RSS feeds and turns each entry into a
signal markdown file. Uses `feedparser` to parse, no auth, no API key.

Idempotent via `.seen-ids`. Skips entries older than `max_age_hours`.
"""
from __future__ import annotations

import hashlib
import logging
import re
from datetime import datetime, timezone
from typing import Any, Dict, Iterable, List, Optional

import feedparser

from collectors._common import (
    append_seen_id,
    hours_since,
    read_seen_ids,
    render_signal_markdown,
    sanitize_one_line,
    write_signal_file,
)
from state.store import Store


SOURCE_NAME = "google_news"
LOG = logging.getLogger("collectors.google_news")
TAG_RE = re.compile(r"<[^>]+>")

DEFAULT_CONFIG: Dict[str, Any] = {
    "feeds": [
        "https://news.google.com/rss?hl=en-US&gl=US&ceid=US:en",
    ],
    "limit_per_feed": 20,
    "max_age_hours": 24,
}


def _strip_tags(text: str) -> str:
    return TAG_RE.sub("", text or "")


def _entry_id(entry: Dict[str, Any]) -> str:
    raw = entry.get("id") or entry.get("link") or entry.get("title") or ""
    digest = hashlib.sha1(str(raw).encode("utf-8")).hexdigest()[:12]
    return f"gn-{digest}"


def _entry_published(entry: Dict[str, Any]) -> Optional[datetime]:
    parsed = entry.get("published_parsed") or entry.get("updated_parsed")
    if not parsed:
        return None
    try:
        return datetime(*parsed[:6], tzinfo=timezone.utc)
    except (TypeError, ValueError):
        return None


def _parse_feed(url: str, parser: Any) -> Any:
    try:
        return parser.parse(url)
    except Exception as exc:  # pragma: no cover
        LOG.warning("google news feed %s parse failed: %s", url, exc)
        return None


def _entry_to_signal(
    entry: Dict[str, Any],
    max_age_hours: float,
) -> Optional[Dict[str, Any]]:
    title = entry.get("title")
    if not title:
        return None
    published_at = _entry_published(entry)
    if published_at is None:
        # Some Google News entries skip the date — fall back to "now-ish".
        published_at = datetime.now(timezone.utc)
    if hours_since(published_at) > max_age_hours:
        return None

    summary_raw = entry.get("summary", "") or ""
    summary = _strip_tags(summary_raw)

    return {
        "id": _entry_id(entry),
        "source_url": entry.get("link", ""),
        "title": sanitize_one_line(title),
        "summary": sanitize_one_line(summary)[:400] or sanitize_one_line(title),
        "body": summary or title,
        "published_at": published_at,
        "heat_score_raw": 0.5,
        "tags": ["google_news"],
    }


def fetch(
    store: Store,
    config: Optional[Dict[str, Any]] = None,
    parser: Any = None,
) -> List[str]:
    cfg: Dict[str, Any] = {**DEFAULT_CONFIG, **(config or {})}
    rss = parser or feedparser
    source_name = str(cfg.get("source_name", SOURCE_NAME))
    items_dir = store.signals_dir / source_name / "items"
    seen_path = store.seen_ids_path(source_name)
    seen_path.parent.mkdir(parents=True, exist_ok=True)
    seen_path.touch(exist_ok=True)
    seen = read_seen_ids(seen_path)

    new_ids: List[str] = []
    feeds: Iterable[str] = cfg.get("feeds", []) or []
    limit = int(cfg.get("limit_per_feed", 20))
    for feed_url in feeds:
        parsed = _parse_feed(feed_url, rss)
        if parsed is None:
            continue
        entries = list(getattr(parsed, "entries", []) or [])[:limit]
        for entry in entries:
            entry_dict = dict(entry) if not isinstance(entry, dict) else entry
            signal = _entry_to_signal(entry_dict, float(cfg.get("max_age_hours", 24)))
            if not signal:
                continue
            sid = signal["id"]
            if sid in seen:
                continue
            markdown = render_signal_markdown(
                signal_id=sid,
                source=source_name,
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
