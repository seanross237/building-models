#!/usr/bin/env python3
from __future__ import annotations

import argparse
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parents[2]
TOPICS_FILE = ROOT / "config/topics-we-care-about.yaml"
THRESHOLDS_FILE = ROOT / "config/thresholds.yaml"
YOUTUBE_FILTER = "EgQIAhAB"
PRINT_FORMAT = "%(id)s|||%(title)s|||%(channel)s|||%(duration_string)s|||%(view_count)s|||%(upload_date)s|||%(webpage_url)s"


def load_topics() -> list[dict[str, object]]:
    topics: list[dict[str, object]] = []
    current: dict[str, object] | None = None

    for raw_line in TOPICS_FILE.read_text(encoding="utf-8").splitlines():
        line = raw_line.rstrip()
        if line.startswith("  - slug: "):
            if current:
                topics.append(current)
            current = {"slug": line.split(": ", 1)[1], "source_context": []}
        elif current and line.startswith("    name: "):
            current["name"] = line.split(": ", 1)[1]
        elif current and line.startswith("    priority: "):
            current["priority"] = line.split(": ", 1)[1]
        elif current and line.startswith("      - "):
            value = line.split("- ", 1)[1]
            if value not in {"youtube", "papers"}:
                current.setdefault("source_context", []).append(value)

    if current:
        topics.append(current)

    return topics


def load_max_results(default: int = 30) -> int:
    for raw_line in THRESHOLDS_FILE.read_text(encoding="utf-8").splitlines():
        if raw_line.startswith("youtube_max_results_per_term:"):
            _, value = raw_line.split(":", 1)
            try:
                return int(value.strip())
            except ValueError:
                return default
    return default


def format_views(raw: str) -> str:
    try:
        value = int(raw)
    except (TypeError, ValueError):
        return "new"

    if value == 0:
        return "new"
    if value >= 1_000_000:
        return f"{value / 1_000_000:.1f}M views"
    if value >= 1_000:
        return f"{value / 1_000:.1f}K views"
    return f"{value} views"


def topic_paths(topic_slug: str) -> dict[str, Path]:
    base = ROOT / "data/topics" / topic_slug / "youtube"
    return {
        "base": base,
        "items": base / "items",
        "overview": base / "overview.md",
        "seen": base / "seen-ids.txt",
    }


def read_seen_ids(path: Path) -> set[str]:
    if not path.exists():
        return set()
    return {line.strip() for line in path.read_text(encoding="utf-8").splitlines() if line.strip()}


def fetch_lines(query: str, max_results: int) -> list[str]:
    url = f"https://www.youtube.com/results?search_query={quote(query)}&sp={YOUTUBE_FILTER}"
    command = [
        "yt-dlp",
        url,
        "--flat-playlist",
        "--playlist-end",
        str(max_results),
        "--print",
        PRINT_FORMAT,
        "--no-update",
    ]
    result = subprocess.run(command, capture_output=True, text=True, check=False)
    if result.returncode != 0:
        stderr = result.stderr.strip() or result.stdout.strip()
        raise RuntimeError(f"yt-dlp failed for query '{query}': {stderr}")
    return [line.strip() for line in result.stdout.splitlines() if line.strip()]


def parse_line(line: str) -> dict[str, str] | None:
    parts = line.split("|||")
    if len(parts) != 7:
        return None
    video_id, title, channel, duration, views, upload_date, url = [part.strip() for part in parts]
    if not video_id or not url:
        return None
    return {
        "id": video_id,
        "title": title,
        "channel": channel,
        "duration": duration or "unknown",
        "views": format_views(views),
        "upload_date": upload_date or "unknown",
        "url": url,
    }


def item_body(topic: dict[str, object], video: dict[str, str]) -> str:
    topic_name = str(topic["name"])
    priority = str(topic["priority"])
    source_context = ", ".join(topic.get("source_context", []))
    collected_at = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    return f"""# {video['title']}

- Topic: `{topic_name}`
- Priority: `{priority}`
- Source context: `{source_context}`
- Type: `youtube`
- Video ID: `{video['id']}`
- Channel: `{video['channel']}`
- Duration: `{video['duration']}`
- Views: `{video['views']}`
- Upload date: `{video['upload_date']}`
- URL: {video['url']}
- Collected at UTC: `{collected_at}`
- Transcript status: `pending`

## Summary

Not analyzed yet.

## Transcript

Transcript not collected yet.

## Notes

- Freshly collected by Research Radar.
"""


def append_overview(overview_path: Path, videos: list[dict[str, str]]) -> None:
    if not videos:
        return

    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    section = ["", f"## {stamp} — {len(videos)} new videos", ""]
    for video in videos:
        section.append(f"- **{video['title']}** — {video['channel']} ({video['duration']}, {video['views']})")
        section.append(f"  {video['url']}")
        section.append(f"  item: `items/{video['id']}.md`")
    overview_path.parent.mkdir(parents=True, exist_ok=True)
    with overview_path.open("a", encoding="utf-8") as handle:
        handle.write("\n".join(section) + "\n")


def ensure_overview_header(overview_path: Path, topic_name: str) -> None:
    if overview_path.exists():
        return
    overview_path.write_text(
        f"# {topic_name} — YouTube Overview\n\nKeep this file short. Roll up the main new videos here and use `items/` for the full details.\n",
        encoding="utf-8",
    )


def run_topic(topic: dict[str, object], max_results: int, dry_run: bool) -> int:
    slug = str(topic["slug"])
    name = str(topic["name"])
    paths = topic_paths(slug)
    paths["items"].mkdir(parents=True, exist_ok=True)
    ensure_overview_header(paths["overview"], name)
    seen = read_seen_ids(paths["seen"])

    if dry_run:
        print(f"[collect-youtube] dry-run topic: {slug} :: {name}")
        return 0

    lines = fetch_lines(name, max_results)
    new_videos: list[dict[str, str]] = []
    seen_this_run: set[str] = set()

    for line in lines:
        video = parse_line(line)
        if not video:
            continue
        video_id = video["id"]
        if video_id in seen or video_id in seen_this_run:
            continue
        seen_this_run.add(video_id)
        item_path = paths["items"] / f"{video_id}.md"
        item_path.write_text(item_body(topic, video), encoding="utf-8")
        new_videos.append(video)

    if new_videos:
        with paths["seen"].open("a", encoding="utf-8") as handle:
            for video in new_videos:
                handle.write(video["id"] + "\n")
        append_overview(paths["overview"], new_videos)

    print(f"[collect-youtube] topic={slug} new_videos={len(new_videos)}")
    return len(new_videos)


def main() -> int:
    parser = argparse.ArgumentParser(description="Collect topic-driven YouTube metadata for Research Radar.")
    parser.add_argument("--topic", dest="topic_slugs", action="append", default=[], help="Limit collection to one or more topic slugs.")
    parser.add_argument("--max-results", type=int, default=None, help="Override max results per topic.")
    parser.add_argument("--dry-run", action="store_true", help="Validate topic parsing without calling yt-dlp.")
    args = parser.parse_args()

    topics = load_topics()
    if args.topic_slugs:
        allowed = set(args.topic_slugs)
        topics = [topic for topic in topics if topic["slug"] in allowed]

    if not topics:
        print("[collect-youtube] no topics matched the current selection", file=sys.stderr)
        return 1

    max_results = args.max_results or load_max_results()
    total = 0
    for topic in topics:
        total += run_topic(topic, max_results=max_results, dry_run=args.dry_run)

    print(f"[collect-youtube] completed topics={len(topics)} total_new_videos={total}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
