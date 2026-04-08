"""Shared helpers for Phase 2 collectors.

Every collector writes signal markdown files with the same YAML frontmatter
keys so the analyzer stays source-agnostic. The contract is:

    ---
    id: <source>-<source-specific-id>
    source: <source slug, matches data/signals/<slug>>
    source_url: <permalink to the original item>
    title: <one-line title>
    captured_at: <UTC ISO-8601 with Z>
    published_at: <UTC ISO-8601 with Z, or empty string if unknown>
    heat_score_raw: <float 0..1, source-native popularity proxy>
    freshness_hours: <int>
    tags: [tag1, tag2, ...]
    ---

    ## Summary

    <plain-text summary, 1-3 sentences>

    ## Source content

    <verbatim excerpt of the original post / headline / description>

The helpers here keep that format DRY across all four collectors.
"""
from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable, List, Optional, Set


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def utc_iso(dt: Optional[datetime] = None) -> str:
    moment = dt or utc_now()
    if moment.tzinfo is None:
        moment = moment.replace(tzinfo=timezone.utc)
    return moment.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def hours_since(dt: datetime) -> float:
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    delta = utc_now() - dt
    return delta.total_seconds() / 3600.0


def read_seen_ids(path: Path) -> Set[str]:
    if not path.exists():
        return set()
    return {line.strip() for line in path.read_text(encoding="utf-8").splitlines() if line.strip()}


def append_seen_id(path: Path, signal_id: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(signal_id + "\n")


def sanitize_one_line(text: Optional[str]) -> str:
    if not text:
        return ""
    return " ".join(str(text).split())


def render_signal_markdown(
    *,
    signal_id: str,
    source: str,
    source_url: str,
    title: str,
    summary: str,
    body: str,
    published_at: Optional[datetime],
    heat_score_raw: float,
    tags: Iterable[str],
) -> str:
    captured = utc_now()
    if published_at is None:
        freshness = 0
        published_str = ""
    else:
        freshness = max(0, int(hours_since(published_at)))
        published_str = utc_iso(published_at)
    tag_list = [t for t in (tags or []) if t]
    tag_str = ", ".join(tag_list)
    return (
        "---\n"
        f"id: {signal_id}\n"
        f"source: {source}\n"
        f"source_url: {source_url}\n"
        f"title: {sanitize_one_line(title)}\n"
        f"captured_at: {utc_iso(captured)}\n"
        f"published_at: {published_str}\n"
        f"heat_score_raw: {heat_score_raw:.3f}\n"
        f"freshness_hours: {freshness}\n"
        f"tags: [{tag_str}]\n"
        "---\n\n"
        "## Summary\n\n"
        f"{sanitize_one_line(summary) or '(no summary)'}\n\n"
        "## Source content\n\n"
        f"{(body or '').strip() or '(no body)'}\n"
    )


def write_signal_file(items_dir: Path, signal_id: str, markdown: str) -> Path:
    items_dir.mkdir(parents=True, exist_ok=True)
    out = items_dir / f"{signal_id}.md"
    out.write_text(markdown, encoding="utf-8")
    return out


__all__ = [
    "append_seen_id",
    "hours_since",
    "read_seen_ids",
    "render_signal_markdown",
    "sanitize_one_line",
    "utc_iso",
    "utc_now",
    "write_signal_file",
]
