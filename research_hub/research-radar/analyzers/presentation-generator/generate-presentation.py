#!/usr/bin/env python3
"""Generate HTML presentations from high-scoring Research Radar items.

Reads queued presentation candidates, groups them by topic+date, calls Claude
to generate a complete single-file HTML presentation, and writes the output to
the presentations/ directory.
"""
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]  # research-radar/
REPO_ROOT = ROOT.parent  # home-base/
PRESENTATIONS_ROOT = REPO_ROOT / "presentations"
QUEUE_DIR = ROOT / "data/queues/presentation-candidates"
PUBLISHED_DIR = ROOT / "data/queues/published"
PROMPT_FILE = ROOT / "analyzers/presentation-generator/prompt.md"
GUIDE_FILE = REPO_ROOT / "presentations/guide_presentations.md"

SYSTEM_PROMPT = "\n".join([
    "You are generating a visual HTML slide deck for a research radar briefing.",
    "Output ONLY the raw HTML. No markdown fences, no commentary, no explanation.",
    "The entire response must be a valid HTML document starting with <!DOCTYPE html>.",
])

AUTH_ERROR_MARKERS = (
    "OAuth token has expired",
    "authentication_error",
    "Failed to authenticate",
)

LOG_PREFIX = "[build-presentations]"


def log(msg: str) -> None:
    print(f"{LOG_PREFIX} {msg}")


def log_err(msg: str) -> None:
    print(f"{LOG_PREFIX} ERROR: {msg}", file=sys.stderr)


def load_candidates() -> list[dict]:
    """Load all .json files from the presentation-candidates queue."""
    if not QUEUE_DIR.exists():
        return []
    candidates = []
    for path in sorted(QUEUE_DIR.glob("*.json")):
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
            data["_manifest_path"] = str(path)
            candidates.append(data)
        except (json.JSONDecodeError, OSError) as exc:
            log_err(f"skipping malformed manifest {path.name}: {exc}")
    return candidates


def group_candidates(candidates: list[dict], today: str) -> dict[str, list[dict]]:
    """Group candidates by topic_slug + date into presentation groups.

    Returns a dict mapping folder_name -> list of candidates.
    """
    groups: dict[str, list[dict]] = {}
    for candidate in candidates:
        slug = candidate.get("topic_slug", "unknown")
        folder = f"{slug}-radar-{today}"
        groups.setdefault(folder, []).append(candidate)
    return groups


def read_file_safe(path: Path) -> str:
    """Read a file, returning empty string on failure."""
    try:
        return path.read_text(encoding="utf-8")
    except OSError:
        return ""


def build_prompt(
    candidates: list[dict],
    folder_name: str,
    today: str,
    prompt_template: str,
) -> str:
    """Build the full prompt to send to Claude for presentation generation."""
    sections = [
        prompt_template,
        f"\n\n## Presentation folder name\n\n`{folder_name}`\n",
        f"\n\n## Date\n\n{today}\n",
    ]

    for i, candidate in enumerate(candidates):
        sections.append(f"\n\n---\n\n## Item {i + 1} of {len(candidates)}\n")

        # Include metadata
        sections.append(f"- Title: {candidate.get('title', 'Untitled')}")
        sections.append(f"- Topic: {candidate.get('topic_slug', 'unknown')}")
        sections.append(f"- Type: {candidate.get('item_type', 'unknown')}")
        sections.append(f"- Source URL: {candidate.get('source_url', '')}")
        sections.append(f"- Relevance score: {candidate.get('relevance_score', '?')}")

        # Read and include the summary markdown
        summary_rel = candidate.get("summary_path", "")
        if summary_rel:
            summary_path = ROOT / summary_rel
            summary_text = read_file_safe(summary_path)
            if summary_text:
                sections.append(f"\n### Summary file content\n\n{summary_text}")
            else:
                sections.append("\n### Summary file content\n\n(not available)")

        # Read and include the source item markdown
        source_rel = candidate.get("source_item_path", "")
        if source_rel:
            source_path = ROOT / source_rel
            source_text = read_file_safe(source_path)
            if source_text:
                # Truncate very long source items (transcripts can be huge)
                if len(source_text) > 30000:
                    source_text = source_text[:30000] + "\n\n[...truncated for length...]"
                sections.append(f"\n### Source item content\n\n{source_text}")
            else:
                sections.append("\n### Source item content\n\n(not available)")

    if len(candidates) > 1:
        sections.append(
            "\n\n## IMPORTANT: Multiple items\n\n"
            f"This presentation covers {len(candidates)} items for the same topic. "
            "Create a unified presentation that covers all items coherently. "
            "Each item should get at least one dedicated content slide, but share "
            "the title, TOC, TL;DR, and Eywa connection slides."
        )

    return "\n".join(sections)


def extract_html(raw: str) -> str:
    """Extract the HTML from Claude's response, handling JSON wrapper and fences."""
    text = raw.strip()

    # Claude --output-format json wraps in {"result": "..."}
    try:
        outer = json.loads(text)
        text = str(outer.get("result", "")).strip()
    except (json.JSONDecodeError, ValueError):
        pass

    # Strip markdown fences if present
    if text.startswith("```"):
        lines = text.splitlines()
        if lines[0].strip().startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]
        text = "\n".join(lines).strip()

    # Validate it looks like HTML
    if not text.startswith("<!DOCTYPE") and not text.startswith("<html"):
        # Try to find HTML within the output
        doctype_idx = text.find("<!DOCTYPE")
        html_idx = text.find("<html")
        start = -1
        if doctype_idx >= 0:
            start = doctype_idx
        elif html_idx >= 0:
            start = html_idx

        if start >= 0:
            end = text.rfind("</html>")
            if end > start:
                text = text[start : end + len("</html>")]
            else:
                text = text[start:]
        else:
            raise ValueError("Claude output does not contain valid HTML")

    return text


def run_claude(prompt: str, model: str, max_turns: int) -> str:
    """Call Claude CLI and return the raw output."""
    command = [
        "claude",
        "-p",
        prompt,
        "--output-format",
        "json",
        "--model",
        model,
        "--dangerously-skip-permissions",
        "--append-system-prompt",
        SYSTEM_PROMPT,
        "--max-turns",
        str(max_turns),
    ]
    result = subprocess.run(
        command,
        cwd=str(ROOT),
        capture_output=True,
        text=True,
        check=False,
    )
    stdout = result.stdout.strip() or result.stderr.strip()

    if any(marker in stdout for marker in AUTH_ERROR_MARKERS):
        raise RuntimeError(f"Claude authentication error: {stdout[:200]}")

    if result.returncode != 0 and not result.stdout.strip():
        raise RuntimeError(
            result.stderr.strip() or f"claude exited with code {result.returncode}"
        )

    return stdout


def move_to_published(candidate: dict) -> None:
    """Move a processed manifest from the queue to published/."""
    PUBLISHED_DIR.mkdir(parents=True, exist_ok=True)
    src = Path(candidate["_manifest_path"])
    if src.exists():
        dst = PUBLISHED_DIR / src.name
        shutil.move(str(src), str(dst))


def generate_presentation(
    folder_name: str,
    candidates: list[dict],
    today: str,
    model: str,
    max_turns: int,
    dry_run: bool = False,
    force: bool = False,
) -> bool:
    """Generate a presentation for a group of candidates. Returns True on success."""
    output_dir = PRESENTATIONS_ROOT / folder_name
    html_path = output_dir / "presentation.html"
    meta_path = output_dir / "meta.json"

    if html_path.exists() and not force:
        log(f"skipping {folder_name} (already exists, use --force to regenerate)")
        # Still move manifests so they don't get re-queued
        for candidate in candidates:
            move_to_published(candidate)
        return True

    titles = [c.get("title", "Untitled") for c in candidates]
    title_display = titles[0] if len(titles) == 1 else f"{candidates[0].get('topic_slug', 'unknown')} ({len(titles)} items)"

    if dry_run:
        log(f"dry-run: would generate {folder_name} for: {', '.join(titles)}")
        return True

    log(f"generating presentation for {title_display}...")

    prompt_template = read_file_safe(PROMPT_FILE)
    if not prompt_template:
        log_err(f"prompt template not found at {PROMPT_FILE}")
        return False

    prompt = build_prompt(candidates, folder_name, today, prompt_template)

    try:
        raw_output = run_claude(prompt, model=model, max_turns=max_turns)
    except RuntimeError as exc:
        log_err(f"Claude call failed for {folder_name}: {exc}")
        return False

    try:
        html = extract_html(raw_output)
    except ValueError as exc:
        log_err(f"failed to extract HTML for {folder_name}: {exc}")
        # Log a preview of what we got
        preview = " ".join(raw_output.split())[:300]
        log_err(f"raw output preview: {preview}")
        return False

    # Write output
    output_dir.mkdir(parents=True, exist_ok=True)
    html_path.write_text(html, encoding="utf-8")

    meta_title = f"\U0001f4e1 {title_display} \u2014 Research Radar"
    meta = {"title": meta_title}
    meta_path.write_text(json.dumps(meta, indent=2) + "\n", encoding="utf-8")

    log(f"wrote {html_path.relative_to(REPO_ROOT)}")
    log(f"wrote {meta_path.relative_to(REPO_ROOT)}")

    # Move processed manifests to published
    for candidate in candidates:
        move_to_published(candidate)
        manifest_name = Path(candidate["_manifest_path"]).name
        log(f"moved {manifest_name} to published/")

    return True


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Generate HTML presentations from Research Radar candidates."
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be generated without calling Claude or writing files.",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=0,
        help="Maximum number of presentation groups to generate. 0 = no limit.",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Regenerate presentations even if output already exists.",
    )
    parser.add_argument(
        "--model",
        default="sonnet",
        help="Claude model alias (default: sonnet).",
    )
    parser.add_argument(
        "--max-turns",
        type=int,
        default=4,
        help="Maximum Claude turns (default: 4).",
    )
    args = parser.parse_args()

    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    candidates = load_candidates()
    if not candidates:
        log("no presentation candidates queued")
        return 0

    log(f"found {len(candidates)} queued candidate(s)")

    groups = group_candidates(candidates, today)
    log(f"grouped into {len(groups)} presentation(s)")

    if args.limit > 0:
        limited_keys = list(groups.keys())[: args.limit]
        groups = {k: groups[k] for k in limited_keys}
        log(f"limited to {len(groups)} presentation(s)")

    successes = 0
    failures = 0

    for folder_name, group_candidates_list in groups.items():
        ok = generate_presentation(
            folder_name=folder_name,
            candidates=group_candidates_list,
            today=today,
            model=args.model,
            max_turns=args.max_turns,
            dry_run=args.dry_run,
            force=args.force,
        )
        if ok:
            successes += 1
        else:
            failures += 1

    log(f"completed generated={successes} failures={failures}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
