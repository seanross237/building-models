#!/usr/bin/env python3
from __future__ import annotations

import argparse
import os
import re
import subprocess
import tempfile
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

# Cookie support for yt-dlp (helps avoid rate-limiting / bot detection).
# Override with env var YT_COOKIES_PATH; default is in research-radar dir.
_COOKIES_PATH_DEFAULT = os.path.expanduser("~/home-base/research_hub/research-radar/yt-cookies.txt")
COOKIES_PATH: str | None = os.environ.get("YT_COOKIES_PATH", _COOKIES_PATH_DEFAULT)
ITEM_GLOB = "data/topics/*/youtube/items/*.md"
SECTION_PATTERN = re.compile(r"(^## (?P<section>.+?)\n\n)(?P<body>.*?)(?=^## |\Z)", re.MULTILINE | re.DOTALL)
URL_PATTERN = re.compile(r"^- URL: (?P<url>.+)$", re.MULTILINE)
STATUS_PATTERN = re.compile(r"^- Transcript status: `(?P<status>[^`]+)`$", re.MULTILINE)


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def iter_item_files(topic_slugs: set[str] | None = None) -> list[Path]:
    files = sorted(ROOT.glob(ITEM_GLOB))
    if not topic_slugs:
        return files
    filtered: list[Path] = []
    for path in files:
        try:
            topic_slug = path.relative_to(ROOT / "data/topics").parts[0]
        except Exception:
            continue
        if topic_slug in topic_slugs:
            filtered.append(path)
    return filtered


def parse_url(text: str) -> str | None:
    match = URL_PATTERN.search(text)
    return match.group("url").strip() if match else None


def current_transcript_status(text: str) -> str | None:
    match = STATUS_PATTERN.search(text)
    return match.group("status") if match else None


def replace_section(text: str, section: str, new_body: str) -> str:
    def repl(match: re.Match[str]) -> str:
        if match.group("section") != section:
            return match.group(0)
        return f"## {section}\n\n{new_body.strip()}\n\n"

    if f"## {section}\n" not in text:
        return text.rstrip() + f"\n\n## {section}\n\n{new_body.strip()}\n"
    return SECTION_PATTERN.sub(repl, text)


def replace_transcript_status(text: str, new_status: str) -> str:
    line = f"- Transcript status: `{new_status}`"
    if STATUS_PATTERN.search(text):
        return STATUS_PATTERN.sub(line, text, count=1)
    marker = "- Collected at UTC:"
    if marker in text:
        return text.replace(marker, marker + "\n" + line, 1)
    return text


def choose_subtitle_file(temp_dir: Path) -> Path | None:
    candidates = sorted(temp_dir.glob("*.vtt")) + sorted(temp_dir.glob("*.srv3")) + sorted(temp_dir.glob("*.json3"))
    if not candidates:
        return None
    return max(candidates, key=lambda path: path.stat().st_size)


def clean_vtt_text(raw: str) -> str:
    lines: list[str] = []
    previous = ""
    for line in raw.splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        if stripped == "WEBVTT":
            continue
        if stripped.startswith("Kind:") or stripped.startswith("Language:"):
            continue
        if stripped.startswith("NOTE"):
            continue
        if "-->" in stripped:
            continue
        if re.fullmatch(r"[0-9]{2}:[0-9]{2}:[0-9]{2}\.\d{3}", stripped):
            continue
        if re.fullmatch(r"\d+", stripped):
            continue
        if stripped == previous:
            continue
        previous = stripped
        lines.append(stripped)
    return "\n".join(lines).strip()


def summarize_error(message: str) -> str:
    lines = [line.strip() for line in message.splitlines() if line.strip()]
    if not lines:
        return "Unknown transcript fetch error."
    if "429" in message or "Too Many Requests" in message:
        return "YouTube rate-limited the subtitle request (HTTP 429)."
    error_lines = [line for line in lines if line.startswith("ERROR:")]
    if error_lines:
        return error_lines[-1]
    return lines[-1]


def _resolve_cookies_path() -> str | None:
    """Return the cookies file path if it exists, or None (with a warning)."""
    if not COOKIES_PATH:
        return None
    expanded = os.path.expanduser(COOKIES_PATH)
    if os.path.isfile(expanded):
        return expanded
    print(f"[collect-transcripts] WARNING: cookies file not found at {expanded} — continuing without cookies")
    return None


def fetch_transcript_result(url: str) -> tuple[str, str | None, str]:
    cookies_file = _resolve_cookies_path()

    with tempfile.TemporaryDirectory(prefix="research-radar-transcript-") as tmp:
        temp_dir = Path(tmp)
        command = [
            "yt-dlp",
            url,
            "--skip-download",
            "--write-subs",
            "--write-auto-subs",
            "--sub-langs",
            "en.*,en",
            "--sub-format",
            "vtt",
            "-o",
            str(temp_dir / "%(id)s.%(ext)s"),
            "--no-update",
        ]
        if cookies_file:
            command.extend(["--cookies", cookies_file])
        result = subprocess.run(command, capture_output=True, text=True, check=False)
        if result.returncode != 0:
            stderr = result.stderr.strip() or result.stdout.strip()
            return "retry-needed", None, summarize_error(stderr)

        subtitle_file = choose_subtitle_file(temp_dir)
        if not subtitle_file:
            return "unavailable", None, "No English transcript or captions were available from YouTube."

        transcript_text = clean_vtt_text(subtitle_file.read_text(encoding="utf-8", errors="ignore"))
        if not transcript_text:
            return "unavailable", None, "Transcript file was present but empty after parsing."
        return "available", transcript_text, f"Transcript collected from `{subtitle_file.name}` at `{utc_now()}`."


def update_item_file(path: Path, status: str, transcript_text: str | None, note: str) -> str:
    original = path.read_text(encoding="utf-8")

    if status == "available" and transcript_text:
        body = f"Transcript source note: {note}\n\n{transcript_text}"
    elif status == "retry-needed":
        body = f"Transcript fetch needs retry. {note} Checked at `{utc_now()}`."
    else:
        body = f"Transcript unavailable. {note} Checked at `{utc_now()}`."

    updated = replace_section(original, "Transcript", body)
    updated = replace_transcript_status(updated, status)
    path.write_text(updated, encoding="utf-8")
    return "updated"


def should_skip(path: Path, force: bool) -> bool:
    if force:
        return False
    text = path.read_text(encoding="utf-8")
    status = current_transcript_status(text)
    return status in {"available", "unavailable"}


def main() -> int:
    parser = argparse.ArgumentParser(description="Collect YouTube transcripts into Research Radar item files.")
    parser.add_argument("--topic", dest="topic_slugs", action="append", default=[], help="Limit transcript collection to one or more topic slugs.")
    parser.add_argument("--force", action="store_true", help="Retry transcript collection even when a transcript status is already set.")
    parser.add_argument("--limit", type=int, default=None, help="Process at most this many item files.")
    parser.add_argument("--dry-run", action="store_true", help="Show which item files would be processed without calling yt-dlp.")
    args = parser.parse_args()

    topic_slugs = set(args.topic_slugs) if args.topic_slugs else None
    item_files = iter_item_files(topic_slugs)
    if args.limit is not None:
        item_files = item_files[: args.limit]

    if not item_files:
        print("[collect-transcripts] no item files matched the current selection")
        return 0

    processed = 0
    updated = 0
    for item_file in item_files:
        if should_skip(item_file, args.force):
            print(f"[collect-transcripts] skip existing status: {item_file}")
            continue

        if args.dry_run:
            print(f"[collect-transcripts] dry-run item: {item_file}")
            processed += 1
            continue

        text = item_file.read_text(encoding="utf-8")
        url = parse_url(text)
        if not url:
            print(f"[collect-transcripts] missing URL in {item_file}")
            continue

        status, transcript_text, note = fetch_transcript_result(url)
        result = update_item_file(item_file, status, transcript_text, note)
        processed += 1
        if result == "updated":
            updated += 1
        print(f"[collect-transcripts] {status}: {item_file.name}")

    print(f"[collect-transcripts] processed={processed} updated={updated}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
