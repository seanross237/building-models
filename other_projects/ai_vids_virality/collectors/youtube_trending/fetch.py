"""YouTube trending collector via yt-dlp.

Shells out to `yt-dlp --flat-playlist --dump-json
"https://www.youtube.com/feed/trending"` and parses each line of NDJSON
into a signal record. No API key needed.

If yt-dlp is not on `$PATH`, this collector logs a warning and returns
an empty list — the rest of the pipeline must keep running.
"""
from __future__ import annotations

import json
import logging
import shutil
import subprocess
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from collectors._common import (
    append_seen_id,
    read_seen_ids,
    render_signal_markdown,
    sanitize_one_line,
    write_signal_file,
)
from state.store import Store


SOURCE_NAME = "youtube_trending"
LOG = logging.getLogger("collectors.youtube_trending")

# YouTube has been quietly disabling /feed/trending; we try the canonical
# URL first and fall back to the official "Popular Right Now" auto-playlist
# which is what the YouTube site itself surfaces in its trending widget.
TRENDING_URLS: tuple = (
    "https://www.youtube.com/feed/trending",
    "https://www.youtube.com/playlist?list=PLrEnWoR732-BHrPp_Pm8_VleD68f9s14-",
)

DEFAULT_CONFIG: Dict[str, Any] = {
    "limit": 20,
    "urls": list(TRENDING_URLS),
}


def _yt_dlp_path() -> Optional[str]:
    return shutil.which("yt-dlp")


def _run_yt_dlp_url(url: str, limit: int, runner: Any) -> str:
    binary = _yt_dlp_path()
    if not binary:
        raise RuntimeError("yt-dlp not on PATH")
    cmd = [
        binary,
        "--flat-playlist",
        "--dump-json",
        "--playlist-end",
        str(limit),
        url,
    ]
    runner_fn = runner or subprocess.run
    result = runner_fn(cmd, capture_output=True, text=True, check=False, timeout=120)
    if getattr(result, "returncode", 1) != 0:
        raise RuntimeError(
            f"yt-dlp exited with {getattr(result, 'returncode', '?')}: "
            f"{getattr(result, 'stderr', '')[:300]}"
        )
    return getattr(result, "stdout", "") or ""


def _run_yt_dlp(limit: int, urls: List[str], runner: Any = None) -> str:
    """Try each URL in order, return the first stdout that produced data."""
    last_err: Optional[str] = None
    for url in urls:
        try:
            stdout = _run_yt_dlp_url(url, limit, runner)
        except Exception as exc:
            last_err = str(exc)
            LOG.warning("yt-dlp failed for %s: %s", url, exc)
            continue
        if stdout.strip():
            return stdout
    if last_err:
        raise RuntimeError(last_err)
    return ""


def _parse_lines(stdout: str) -> List[Dict[str, Any]]:
    items: List[Dict[str, Any]] = []
    for line in stdout.splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            items.append(json.loads(line))
        except json.JSONDecodeError:
            LOG.warning("yt-dlp emitted unparseable line: %.80s", line)
    return items


def _entry_to_signal(entry: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    video_id = entry.get("id")
    title = entry.get("title")
    if not video_id or not title:
        return None
    uploader = entry.get("uploader") or entry.get("channel") or ""
    view_count = entry.get("view_count")
    duration = entry.get("duration")
    url = entry.get("url") or f"https://www.youtube.com/watch?v={video_id}"

    if isinstance(view_count, (int, float)) and view_count > 0:
        heat = min(1.0, view_count / 5_000_000.0)
    else:
        heat = 0.5

    body_lines = [f"Uploader: {uploader}"]
    if isinstance(view_count, (int, float)):
        body_lines.append(f"Views: {int(view_count)}")
    if isinstance(duration, (int, float)):
        body_lines.append(f"Duration sec: {int(duration)}")
    body = "\n".join(body_lines)

    return {
        "id": f"yt-{video_id}",
        "source_url": url,
        "title": sanitize_one_line(title),
        "summary": sanitize_one_line(f"{title} — {uploader}"),
        "body": body,
        # yt-dlp's flat playlist doesn't reliably give us a publish date.
        "published_at": datetime.now(timezone.utc),
        "heat_score_raw": heat,
        "tags": ["youtube_trending", "video"],
    }


def fetch(
    store: Store,
    config: Optional[Dict[str, Any]] = None,
    runner: Any = None,
) -> List[str]:
    cfg: Dict[str, Any] = {**DEFAULT_CONFIG, **(config or {})}
    items_dir = store.signals_dir / SOURCE_NAME / "items"
    seen_path = store.seen_ids_path(SOURCE_NAME)
    seen_path.parent.mkdir(parents=True, exist_ok=True)
    seen_path.touch(exist_ok=True)
    seen = read_seen_ids(seen_path)

    urls = cfg.get("urls") or list(TRENDING_URLS)
    try:
        stdout = _run_yt_dlp(int(cfg.get("limit", 20)), urls, runner=runner)
    except Exception as exc:
        LOG.warning("youtube_trending collector skipped: %s", exc)
        return []

    new_ids: List[str] = []
    for entry in _parse_lines(stdout):
        signal = _entry_to_signal(entry)
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
