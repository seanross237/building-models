"""Reddit collector.

Hits the public `https://www.reddit.com/r/{sub}.json` endpoints with a
custom User-Agent. No auth, no API key, no money. Each post becomes a
markdown signal file under `data/signals/reddit/items/`.

Idempotent via `.seen-ids` and skips posts older than `max_age_hours`.
"""
from __future__ import annotations

import logging
import os
import time
from datetime import datetime, timezone
from typing import Any, Dict, Iterable, List, Optional

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


SOURCE_NAME = "reddit"
USER_AGENT = "ai-vids-virality/0.2 (+https://example.com)"
OAUTH_TOKEN_URL = "https://www.reddit.com/api/v1/access_token"
OAUTH_API_BASE = "https://oauth.reddit.com"
REDDIT_CLIENT_ID = "REDDIT_CLIENT_ID"
REDDIT_CLIENT_SECRET = "REDDIT_CLIENT_SECRET"
REDDIT_USER_AGENT = "REDDIT_USER_AGENT"
_TOKEN_CACHE: Dict[str, Any] = {"token": None, "expires_at": 0.0}
LOG = logging.getLogger("collectors.reddit")

DEFAULT_CONFIG: Dict[str, Any] = {
    "subreddits": ["popular", "news", "nottheonion", "politics", "funny"],
    "limit_per_sub": 25,
    "max_age_hours": 24,
}


def _user_agent() -> str:
    return os.environ.get(REDDIT_USER_AGENT, USER_AGENT)


def _get_oauth_token(http: Any) -> Optional[str]:
    client_id = (os.environ.get(REDDIT_CLIENT_ID) or "").strip()
    client_secret = (os.environ.get(REDDIT_CLIENT_SECRET) or "").strip()
    if not client_id or not client_secret:
        return None

    if time.monotonic() < float(_TOKEN_CACHE.get("expires_at", 0.0) or 0.0):
        token = _TOKEN_CACHE.get("token")
        return str(token) if token else None

    try:
        resp = http.post(
            OAUTH_TOKEN_URL,
            auth=(client_id, client_secret),
            data={"grant_type": "client_credentials"},
            headers={"User-Agent": _user_agent()},
            timeout=15,
        )
        if getattr(resp, "status_code", 0) != 200:
            LOG.warning("reddit oauth token fetch returned status %s", getattr(resp, "status_code", "?"))
            return None
        payload = resp.json()
        if not isinstance(payload, dict):
            LOG.warning("reddit oauth token payload was not a JSON object")
            return None
        token = payload.get("access_token")
        expires_in = int(payload.get("expires_in", 0) or 0)
        if not token:
            LOG.warning("reddit oauth token payload missing access_token")
            return None
        cache_lifetime = max(0, min(expires_in - 600, 3000))
        _TOKEN_CACHE["token"] = token
        _TOKEN_CACHE["expires_at"] = time.monotonic() + cache_lifetime
        return str(token)
    except Exception as exc:  # pragma: no cover
        LOG.warning("reddit oauth token fetch failed: %s", exc)
        return None


def _fetch_subreddit(sub: str, limit: int, http: Any) -> List[Dict[str, Any]]:
    token = _get_oauth_token(http)
    if token:
        url = f"{OAUTH_API_BASE}/r/{sub}.json?limit={limit}"
        headers = {"Authorization": f"Bearer {token}", "User-Agent": _user_agent()}
    else:
        url = f"https://www.reddit.com/r/{sub}.json?limit={limit}"
        headers = {"User-Agent": _user_agent()}
    try:
        resp = http.get(url, headers=headers, timeout=15)
    except Exception as exc:  # pragma: no cover
        LOG.warning("reddit fetch failed for %s: %s", sub, exc)
        return []
    if getattr(resp, "status_code", 0) != 200:
        LOG.warning("reddit /r/%s returned status %s", sub, getattr(resp, "status_code", "?"))
        return []
    try:
        payload = resp.json()
    except Exception as exc:  # pragma: no cover
        LOG.warning("reddit /r/%s json parse failed: %s", sub, exc)
        return []
    children = payload.get("data", {}).get("children", []) if isinstance(payload, dict) else []
    return [child.get("data", {}) for child in children if isinstance(child, dict)]


def _post_to_signal(
    post: Dict[str, Any],
    sub: str,
    max_age_hours: float,
) -> Optional[Dict[str, Any]]:
    post_id = post.get("id")
    title = post.get("title")
    if not post_id or not title:
        return None
    if post.get("stickied") or post.get("over_18"):
        return None
    created_utc = post.get("created_utc")
    if created_utc is None:
        return None
    try:
        published_at = datetime.fromtimestamp(float(created_utc), tz=timezone.utc)
    except (TypeError, ValueError):
        return None
    if hours_since(published_at) > max_age_hours:
        return None

    permalink = post.get("permalink", "")
    source_url = f"https://www.reddit.com{permalink}" if permalink else post.get("url", "")
    selftext = post.get("selftext") or ""
    if len(selftext) > 1500:
        selftext = selftext[:1500] + "..."

    ups = int(post.get("ups", 0) or 0)
    num_comments = int(post.get("num_comments", 0) or 0)
    heat = min(1.0, (ups / 10000.0) + (num_comments / 5000.0))

    return {
        "id": f"reddit-{post_id}",
        "source_url": source_url,
        "title": sanitize_one_line(title),
        "summary": sanitize_one_line(selftext)[:400] or sanitize_one_line(title),
        "body": selftext or title,
        "published_at": published_at,
        "heat_score_raw": heat,
        "tags": [sub, "reddit"],
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
    for sub in cfg.get("subreddits", []) or []:
        posts = _fetch_subreddit(sub, int(cfg.get("limit_per_sub", 25)), http_client)
        for post in posts:
            signal = _post_to_signal(post, sub, float(cfg.get("max_age_hours", 24)))
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
