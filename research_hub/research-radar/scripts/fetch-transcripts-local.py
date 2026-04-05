#!/usr/bin/env python3
"""
Fetch YouTube transcripts from a residential IP using youtube_transcript_api.

Designed to run on a local Mac to bypass cloud-IP blocking.
Scans item .md files for pending/retry-needed transcripts and fills them in.

Usage:
    python3 fetch-transcripts-local.py --limit 100
    python3 fetch-transcripts-local.py --dry-run
"""
from __future__ import annotations

import argparse
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]  # research-radar/
ITEM_GLOB = "data/topics/*/youtube/items/*.md"

STATUS_PATTERN = re.compile(
    r"^- Transcript status: `(?P<status>[^`]+)`$", re.MULTILINE
)
VIDEO_ID_PATTERN = re.compile(
    r"^- Video ID: `(?P<vid>[^`]+)`$", re.MULTILINE
)
SECTION_PATTERN = re.compile(
    r"(^## (?P<section>.+?)\n\n)(?P<body>.*?)(?=^## |\Z)",
    re.MULTILINE | re.DOTALL,
)

PREFIX = "[fetch-transcripts]"


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def today_str() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d")


# ---------------------------------------------------------------------------
# File parsing helpers (mirrors collectors/youtube/fetch-transcripts.py)
# ---------------------------------------------------------------------------

def extract_video_id(text: str) -> str | None:
    m = VIDEO_ID_PATTERN.search(text)
    return m.group("vid") if m else None


def current_transcript_status(text: str) -> str | None:
    m = STATUS_PATTERN.search(text)
    return m.group("status") if m else None


def replace_transcript_status(text: str, new_status: str) -> str:
    line = f"- Transcript status: `{new_status}`"
    if STATUS_PATTERN.search(text):
        return STATUS_PATTERN.sub(line, text, count=1)
    return text


def replace_section(text: str, section: str, new_body: str) -> str:
    def repl(match: re.Match[str]) -> str:
        if match.group("section") != section:
            return match.group(0)
        return f"## {section}\n\n{new_body.strip()}\n\n"

    if f"## {section}\n" not in text:
        return text.rstrip() + f"\n\n## {section}\n\n{new_body.strip()}\n"
    return SECTION_PATTERN.sub(repl, text)


# ---------------------------------------------------------------------------
# Transcript fetching via youtube_transcript_api
# ---------------------------------------------------------------------------

def ensure_library_installed() -> bool:
    """Check that youtube_transcript_api is available; hint if not."""
    try:
        import youtube_transcript_api  # noqa: F401
        return True
    except ImportError:
        print(
            f"{PREFIX} ERROR: youtube_transcript_api not installed.\n"
            f"  Install it with:  pip3 install youtube-transcript-api"
        )
        return False


def fetch_transcript(video_id: str) -> tuple[str, str | None]:
    """
    Fetch a transcript for *video_id*.

    Returns (status, transcript_text | None).
    status is one of: "ready", "unavailable".
    """
    from youtube_transcript_api import YouTubeTranscriptApi
    from youtube_transcript_api._errors import (
        NoTranscriptFound,
        TranscriptsDisabled,
        RequestBlocked,
    )

    try:
        ytt = YouTubeTranscriptApi()
        transcript = ytt.fetch(video_id)
        full_text = " ".join(s.text for s in transcript.snippets)
        if not full_text.strip():
            return "unavailable", None
        return "ready", full_text.strip()
    except TranscriptsDisabled:
        return "unavailable", None
    except NoTranscriptFound:
        return "unavailable", None
    except RequestBlocked:
        print(f"{PREFIX} WARNING: request blocked for {video_id} (IP issue?)")
        return "unavailable", None
    except Exception as exc:
        print(f"{PREFIX} ERROR: unexpected exception for {video_id}: {exc}")
        return "unavailable", None


# ---------------------------------------------------------------------------
# Item file discovery and update
# ---------------------------------------------------------------------------

def iter_pending_items() -> list[Path]:
    """Return item files whose transcript status is pending or retry-needed."""
    results: list[Path] = []
    for path in sorted(ROOT.glob(ITEM_GLOB)):
        text = path.read_text(encoding="utf-8")
        status = current_transcript_status(text)
        if status in ("pending", "retry-needed"):
            results.append(path)
    return results


def update_item_file(path: Path, status: str, transcript_text: str | None) -> None:
    """Rewrite the item .md with the new transcript status and content."""
    original = path.read_text(encoding="utf-8")

    updated = replace_transcript_status(original, status)

    if status == "ready" and transcript_text:
        body = (
            f"Fetched via youtube_transcript_api (local) at `{utc_now()}`.\n\n"
            f"{transcript_text}"
        )
    else:
        body = (
            f"Transcript unavailable. Checked via youtube_transcript_api "
            f"(local) at `{utc_now()}`."
        )
    updated = replace_section(updated, "Transcript", body)
    path.write_text(updated, encoding="utf-8")


def copy_to_daily(video_id: str, transcript_text: str) -> None:
    """If today's daily dir exists, save a transcript copy there."""
    daily_dir = ROOT / "data" / "daily" / today_str() / "transcripts"
    if daily_dir.parent.exists():
        daily_dir.mkdir(parents=True, exist_ok=True)
        dest = daily_dir / f"{video_id}.txt"
        dest.write_text(transcript_text, encoding="utf-8")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> int:
    parser = argparse.ArgumentParser(
        description="Fetch YouTube transcripts locally using youtube_transcript_api."
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=100,
        help="Max number of transcripts to fetch (default: 100).",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="List items that would be processed without fetching.",
    )
    args = parser.parse_args()

    if not ensure_library_installed():
        return 1

    pending = iter_pending_items()
    total_pending = len(pending)
    to_process = pending[: args.limit]

    print(f"{PREFIX} found {total_pending} items needing transcripts")
    print(f"{PREFIX} will process up to {len(to_process)} this run")

    if args.dry_run:
        for p in to_process:
            text = p.read_text(encoding="utf-8")
            vid = extract_video_id(text) or p.stem
            status = current_transcript_status(text) or "?"
            print(f"{PREFIX} [dry-run] {vid} ({status}) -- {p}")
        remaining = total_pending - len(to_process)
        print(
            f"{PREFIX} dry-run complete. "
            f"Would process {len(to_process)}, "
            f"{remaining} would remain."
        )
        return 0

    fetched = 0
    failed = 0

    for i, path in enumerate(to_process, 1):
        text = path.read_text(encoding="utf-8")
        video_id = extract_video_id(text)
        if not video_id:
            print(f"{PREFIX} [{i}/{len(to_process)}] SKIP no video ID: {path.name}")
            failed += 1
            continue

        print(
            f"{PREFIX} [{i}/{len(to_process)}] fetching {video_id}...",
            end=" ",
            flush=True,
        )

        status, transcript_text = fetch_transcript(video_id)
        update_item_file(path, status, transcript_text)

        if status == "ready" and transcript_text:
            fetched += 1
            copy_to_daily(video_id, transcript_text)
            print("OK")
        else:
            failed += 1
            print("unavailable")

    remaining = total_pending - len(to_process)
    print(f"{PREFIX} done. Fetched {fetched}, failed {failed}, remaining {remaining}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
