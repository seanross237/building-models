#!/usr/bin/env python3
"""Run Opus analysis on each arXiv paper in the daily aggregate.

Reads data/daily/YYYY-MM-DD/arxiv_aggregated.md, runs Opus on each paper
using full content from data/daily/YYYY-MM-DD/papers/<paper-id>.md,
and updates the table with relevance, novelty, and summary.
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DAILY_ROOT = ROOT / "data" / "daily"
LENS_FILE = ROOT / "config" / "what-we-care-about-right-now.md"
PROMPT_FILE = Path(__file__).resolve().parent / "prompt-arxiv.md"

PREFIX = "[analyze-arxiv]"
MODEL = "opus"
MAX_TURNS = 2

SYSTEM_PROMPT = "\n".join([
    "You are running an automated scheduled task.",
    "Work autonomously and output only the requested JSON object.",
    "Do not wrap the JSON in markdown fences.",
])

AUTH_ERROR_MARKERS = (
    "OAuth token has expired",
    "authentication_error",
    "Failed to authenticate",
)


class ClaudeUnavailableError(RuntimeError):
    pass


def parse_aggregated_table(text: str) -> list[dict[str, str]]:
    """Parse the markdown table rows from arxiv_aggregated.md.

    Returns a list of dicts with keys matching the table headers (lowercased).
    """
    lines = text.splitlines()
    header_line = None
    header_idx = -1
    for i, line in enumerate(lines):
        if line.startswith("|") and "Title" in line:
            header_line = line
            header_idx = i
            break

    if header_line is None:
        return []

    headers = [h.strip().lower() for h in header_line.split("|")[1:-1]]

    rows: list[dict[str, str]] = []
    for line in lines[header_idx + 2:]:  # skip header + separator
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.split("|")[1:-1]]
        if len(cells) != len(headers):
            continue
        row = dict(zip(headers, cells))
        rows.append(row)

    return rows


def rebuild_aggregated_md(original_text: str, rows: list[dict[str, str]]) -> str:
    """Rebuild the full aggregated markdown with updated row values."""
    lines = original_text.splitlines()

    # Find the header line
    header_idx = -1
    for i, line in enumerate(lines):
        if line.startswith("|") and "Title" in line:
            header_idx = i
            break

    if header_idx == -1:
        return original_text

    # Preserve everything before and including the separator
    result_lines = lines[: header_idx + 2]

    # Rebuild data rows
    for row in rows:
        title = row.get("title", "")
        authors = row.get("authors", "")
        topic = row.get("topic", "")
        category = row.get("category", "")
        relevance = row.get("relevance", "-")
        novelty = row.get("novelty", "-")
        summary = row.get("summary", "-")
        num = row.get("#", "")
        result_lines.append(
            f"| {num} "
            f"| {title} "
            f"| {authors} "
            f"| {topic} "
            f"| {category} "
            f"| {relevance} "
            f"| {novelty} "
            f"| {summary} |"
        )

    result_lines.append("")
    return "\n".join(result_lines)


def load_paper_id_index(topics_root: Path, target_date: str) -> dict[str, str]:
    """Build title -> paper_id mapping from source items collected on target_date."""
    title_to_pid: dict[str, str] = {}

    if not topics_root.exists():
        return title_to_pid

    for topic_dir in sorted(p for p in topics_root.iterdir() if p.is_dir()):
        items_dir = topic_dir / "papers" / "items"
        if not items_dir.exists():
            continue
        for item_path in sorted(items_dir.glob("*.md")):
            if item_path.name == ".gitkeep":
                continue
            text = item_path.read_text(encoding="utf-8")
            first_line = text.splitlines()[0].strip() if text.splitlines() else ""
            title = first_line.removeprefix("# ").strip()
            metadata: dict[str, str] = {}
            for line in text.splitlines():
                stripped = line.strip()
                if stripped.startswith("- ") and ": " in stripped:
                    label, value = stripped[2:].split(": ", 1)
                    metadata[label.strip().lower()] = value.strip()
            pid = metadata.get("paper id", "").strip().strip("`")
            if pid and title:
                title_to_pid[title] = pid

    return title_to_pid


def run_claude(prompt: str) -> str:
    """Call Claude CLI with opus model and return raw output."""
    command = [
        "claude",
        "-p",
        prompt,
        "--output-format", "json",
        "--model", MODEL,
        "--dangerously-skip-permissions",
        "--append-system-prompt", SYSTEM_PROMPT,
        "--max-turns", str(MAX_TURNS),
    ]
    result = subprocess.run(command, cwd=ROOT, capture_output=True, text=True, check=False)
    stdout = result.stdout.strip() or result.stderr.strip()
    if any(marker in stdout for marker in AUTH_ERROR_MARKERS):
        raise ClaudeUnavailableError("Claude authentication is unavailable in the current runtime")
    if result.returncode != 0 and not result.stdout.strip():
        raise RuntimeError(result.stderr.strip() or f"claude exited with code {result.returncode}")

    try:
        outer = json.loads(stdout)
        raw_result = str(outer.get("result", "")).strip()
    except json.JSONDecodeError:
        raw_result = stdout
    if not raw_result:
        raise RuntimeError("claude produced no analysis payload")
    if any(marker in raw_result for marker in AUTH_ERROR_MARKERS):
        raise ClaudeUnavailableError("Claude authentication is unavailable in the current runtime")
    return raw_result


def extract_json(raw: str) -> dict:
    """Extract a JSON object from Claude's raw output."""
    candidate = raw.strip()
    if candidate.startswith("```"):
        lines = candidate.splitlines()
        if len(lines) >= 3:
            candidate = "\n".join(lines[1:-1]).strip()
    start = candidate.find("{")
    end = candidate.rfind("}")
    if start == -1 or end == -1 or end <= start:
        raise ValueError("Claude output did not include a JSON object")
    return json.loads(candidate[start: end + 1])


def analyze_paper(title: str, paper_text: str, lens: str, prompt_template: str) -> dict:
    """Run Opus on a paper with full content."""
    prompt = "\n\n".join([
        prompt_template,
        "What we care about right now:",
        lens,
        f"Paper title: {title}",
        "Full paper content:",
        paper_text[:100000],  # cap to avoid token limits
    ])
    raw = run_claude(prompt)
    return extract_json(raw)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Run Opus analysis on daily arXiv aggregate."
    )
    parser.add_argument(
        "--date",
        default=datetime.now(timezone.utc).strftime("%Y-%m-%d"),
        help="Date to analyze (YYYY-MM-DD). Default: today UTC.",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=0,
        help="Stop after analyzing N items. Use 0 for no limit.",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Re-analyze items even if they already have scores.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show which items would be analyzed without calling Claude.",
    )
    args = parser.parse_args()
    target_date: str = args.date

    aggregated_path = DAILY_ROOT / target_date / "arxiv_aggregated.md"
    if not aggregated_path.exists():
        print(f"{PREFIX} no aggregated file found at {aggregated_path.relative_to(ROOT)}")
        return 0

    papers_dir = DAILY_ROOT / target_date / "papers"
    topics_root = ROOT / "data" / "topics"

    original_text = aggregated_path.read_text(encoding="utf-8")
    rows = parse_aggregated_table(original_text)

    if not rows:
        print(f"{PREFIX} no rows found in {aggregated_path.relative_to(ROOT)}")
        return 0

    # Build title -> paper_id mapping
    title_to_pid = load_paper_id_index(topics_root, target_date)

    # Build set of available paper files
    available_papers: set[str] = set()
    if papers_dir.exists():
        for f in papers_dir.iterdir():
            if f.suffix == ".md":
                available_papers.add(f.stem)

    # Load lens and prompt
    lens = LENS_FILE.read_text(encoding="utf-8") if LENS_FILE.exists() else ""
    prompt_template = PROMPT_FILE.read_text(encoding="utf-8") if PROMPT_FILE.exists() else ""

    # Determine which rows need analysis
    to_analyze: list[int] = []
    for i, row in enumerate(rows):
        if not args.force and row.get("relevance", "-") != "-":
            continue
        to_analyze.append(i)

    if args.limit > 0:
        to_analyze = to_analyze[: args.limit]

    if not to_analyze:
        print(f"{PREFIX} all items already analyzed for {target_date}")
        return 0

    if args.dry_run:
        for idx in to_analyze:
            row = rows[idx]
            title = row.get("title", "Untitled")
            pid = title_to_pid.get(title, "unknown")
            has_paper = pid in available_papers
            print(f"{PREFIX} dry-run: #{row.get('#', '?')} {title[:80]} (paper={'yes' if has_paper else 'no'})")
        print(f"{PREFIX} dry-run complete: {len(to_analyze)} items would be analyzed")
        return 0

    analyzed = 0
    failures = 0

    for idx in to_analyze:
        row = rows[idx]
        title = row.get("title", "Untitled")
        pid = title_to_pid.get(title, "")

        try:
            paper_text = ""
            if pid and pid in available_papers:
                paper_path = papers_dir / f"{pid}.md"
                paper_text = paper_path.read_text(encoding="utf-8")

            if not paper_text:
                # Try to find paper by scanning available papers for title match
                for paper_file in papers_dir.iterdir() if papers_dir.exists() else []:
                    if paper_file.suffix != ".md":
                        continue
                    content = paper_file.read_text(encoding="utf-8")
                    first_line = content.splitlines()[0].strip() if content.splitlines() else ""
                    if first_line.removeprefix("# ").strip() == title:
                        paper_text = content
                        break

            if not paper_text:
                print(f"{PREFIX} no paper content found for #{row.get('#', '?')} {title[:60]}, skipping")
                failures += 1
                continue

            result = analyze_paper(title, paper_text, lens, prompt_template)

            relevance = result.get("relevance", "-")
            novelty = result.get("novelty", "-")
            summary = str(result.get("summary", "-")).replace("|", "\\|").replace("\n", " ")

            rows[idx]["relevance"] = str(relevance)
            rows[idx]["novelty"] = str(novelty)
            rows[idx]["summary"] = summary

            print(
                f"{PREFIX} #{row.get('#', '?')} relevance={relevance} novelty={novelty} "
                f"title={title[:60]}"
            )
            analyzed += 1

        except ClaudeUnavailableError as exc:
            print(f"{PREFIX} auth error, skipping remaining items: {exc}", file=sys.stderr)
            failures += 1
            break
        except Exception as exc:
            print(f"{PREFIX} failed #{row.get('#', '?')} {title[:60]}: {exc}", file=sys.stderr)
            failures += 1
            continue

    # Rewrite the aggregated file with updated rows
    updated_text = rebuild_aggregated_md(original_text, rows)
    aggregated_path.write_text(updated_text, encoding="utf-8")
    print(f"{PREFIX} updated {aggregated_path.relative_to(ROOT)}")
    print(f"{PREFIX} completed analyzed={analyzed} failures={failures}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
