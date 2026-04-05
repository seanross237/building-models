#!/usr/bin/env python3
"""Check completed codex-atlas missions and generate morning briefing presentations.

Scans atlas-mission manifests for missions with status "launched", checks whether
MISSION-COMPLETE.md exists in the mission directory, collects all available reports,
and calls Claude to generate an HTML slide-deck briefing.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]  # research-radar/
REPO_ROOT = ROOT.parent  # home-base/
PRESENTATIONS_ROOT = REPO_ROOT / "presentations"
QUEUE_DIR = ROOT / "data/queues/atlas-missions"
PROMPT_FILE = ROOT / "analyzers/morning-briefing/prompt.md"
GUIDE_FILE = REPO_ROOT / "presentations/guide_presentations.md"
INSTANCES_DIR = (
    REPO_ROOT
    / "research_hub/big-thinkers/research-systems/codex-atlas/execution/instances"
)

MAX_SINGLE_FILE_KB = 20
MAX_TOTAL_KB = 80

SYSTEM_PROMPT = "\n".join([
    "You are generating a visual HTML slide deck for an Atlas mission briefing.",
    "Output ONLY the raw HTML. No markdown fences, no commentary, no explanation.",
    "The entire response must be a valid HTML document starting with <!DOCTYPE html>.",
])

AUTH_ERROR_MARKERS = (
    "OAuth token has expired",
    "authentication_error",
    "Failed to authenticate",
)

LOG_PREFIX = "[morning-briefing]"


# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------

def log(msg: str) -> None:
    print(f"{LOG_PREFIX} {msg}")


def log_err(msg: str) -> None:
    print(f"{LOG_PREFIX} ERROR: {msg}", file=sys.stderr)


# ---------------------------------------------------------------------------
# File helpers
# ---------------------------------------------------------------------------

def read_file_safe(path: Path, max_bytes: int = MAX_SINGLE_FILE_KB * 1024) -> str:
    """Read a file, returning empty string on failure.  Truncates to *max_bytes*."""
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return ""
    if len(text) > max_bytes:
        text = text[:max_bytes] + "\n\n[...truncated to 20 KB...]"
    return text


# ---------------------------------------------------------------------------
# Manifest loading
# ---------------------------------------------------------------------------

def load_manifests() -> list[dict]:
    """Load all .json manifests from the atlas-missions queue."""
    if not QUEUE_DIR.exists():
        return []
    manifests: list[dict] = []
    for path in sorted(QUEUE_DIR.glob("*.json")):
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
            data["_manifest_path"] = str(path)
            manifests.append(data)
        except (json.JSONDecodeError, OSError) as exc:
            log_err(f"skipping malformed manifest {path.name}: {exc}")
    return manifests


def should_process(manifest: dict, force: bool) -> bool:
    """Return True if this manifest is eligible for briefing generation."""
    status = manifest.get("mission_status", "")
    if status == "briefed" and not force:
        return False
    if status != "launched" and not force:
        return False
    return True


# ---------------------------------------------------------------------------
# Report collection
# ---------------------------------------------------------------------------

def collect_mission_reports(mission_dir: Path) -> list[tuple[str, str]]:
    """Gather all available reports from a completed mission.

    Returns a list of (label, content) tuples.  Content is already truncated
    per-file to MAX_SINGLE_FILE_KB.
    """
    reports: list[tuple[str, str]] = []

    # 1. MISSION-COMPLETE.md
    complete_path = mission_dir / "MISSION-COMPLETE.md"
    text = read_file_safe(complete_path)
    if text:
        reports.append(("MISSION-COMPLETE.md", text))

    # 2. MISSION.md (original mission description)
    mission_path = mission_dir / "MISSION.md"
    text = read_file_safe(mission_path)
    if text:
        reports.append(("MISSION.md (original mission)", text))

    # 3. Strategy-level FINAL-REPORT.md files
    strategies_dir = mission_dir / "strategies"
    if strategies_dir.exists():
        for strategy_dir in sorted(strategies_dir.iterdir()):
            if not strategy_dir.is_dir():
                continue
            final_report = strategy_dir / "FINAL-REPORT.md"
            text = read_file_safe(final_report)
            if text:
                label = f"strategies/{strategy_dir.name}/FINAL-REPORT.md"
                reports.append((label, text))

            # 4. Exploration-level REPORT.md files
            explorations_dir = strategy_dir / "explorations"
            if explorations_dir.exists():
                for expl_dir in sorted(explorations_dir.iterdir()):
                    if not expl_dir.is_dir():
                        continue
                    report = expl_dir / "REPORT.md"
                    text = read_file_safe(report)
                    if text:
                        label = (
                            f"strategies/{strategy_dir.name}"
                            f"/explorations/{expl_dir.name}/REPORT.md"
                        )
                        reports.append((label, text))

    return reports


def enforce_total_limit(
    reports: list[tuple[str, str]],
    max_total: int = MAX_TOTAL_KB * 1024,
) -> list[tuple[str, str]]:
    """If total content exceeds *max_total* bytes, truncate the longest files first."""
    total = sum(len(c) for _, c in reports)
    if total <= max_total:
        return reports

    # Sort by length descending so we trim the biggest first
    indexed = sorted(enumerate(reports), key=lambda t: len(t[1][1]), reverse=True)
    excess = total - max_total

    result = list(reports)
    for idx, (label, content) in indexed:
        if excess <= 0:
            break
        available_trim = len(content) - 1024  # keep at least 1 KB
        if available_trim <= 0:
            continue
        trim_amount = min(available_trim, excess)
        new_len = len(content) - trim_amount
        result[idx] = (label, content[:new_len] + "\n\n[...truncated for size...]")
        excess -= trim_amount

    return result


# ---------------------------------------------------------------------------
# Prompt building
# ---------------------------------------------------------------------------

def build_prompt(
    manifest: dict,
    reports: list[tuple[str, str]],
    folder_name: str,
    today: str,
    prompt_template: str,
) -> str:
    """Build the full prompt for Claude."""
    sections = [
        prompt_template,
        f"\n\n## Presentation folder name\n\n`{folder_name}`\n",
        f"\n\n## Date\n\n{today}\n",
        f"\n\n## Mission metadata\n",
        f"- Mission name: {manifest.get('mission_name', 'unknown')}",
        f"- Title: {manifest.get('title', 'Untitled')}",
        f"- Topic: {manifest.get('topic_slug', 'unknown')}",
        f"- Source URL: {manifest.get('source_url', '')}",
        f"- Breakthrough score: {manifest.get('breakthrough_score', '?')}",
        f"- Breakthrough reasons: {', '.join(manifest.get('breakthrough_reasons', []))}",
    ]

    for label, content in reports:
        sections.append(f"\n\n---\n\n## Report: {label}\n\n{content}")

    return "\n".join(sections)


# ---------------------------------------------------------------------------
# Claude interaction
# ---------------------------------------------------------------------------

def extract_html(raw: str) -> str:
    """Extract HTML from Claude's response, handling JSON wrapper and fences."""
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

    # Find HTML content
    if not text.startswith("<!DOCTYPE") and not text.startswith("<html"):
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


# ---------------------------------------------------------------------------
# Manifest updates
# ---------------------------------------------------------------------------

def update_manifest(manifest: dict, folder_name: str) -> None:
    """Update the manifest file to reflect briefed status."""
    path = Path(manifest["_manifest_path"])
    data = json.loads(path.read_text(encoding="utf-8"))
    data["mission_status"] = "briefed"
    data["briefed_at"] = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    data["presentation_folder"] = folder_name
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")


# ---------------------------------------------------------------------------
# Briefing generation
# ---------------------------------------------------------------------------

def generate_briefing(
    manifest: dict,
    today: str,
    model: str,
    max_turns: int,
    dry_run: bool = False,
    force: bool = False,
) -> bool:
    """Generate a morning briefing for a single completed mission.

    Returns True on success.
    """
    mission_name = manifest.get("mission_name", "")
    if not mission_name:
        log_err("manifest missing mission_name field")
        return False

    mission_dir = INSTANCES_DIR / mission_name
    complete_path = mission_dir / "MISSION-COMPLETE.md"

    if not complete_path.exists():
        log(f"skipping {mission_name} (MISSION-COMPLETE.md not found)")
        return False

    folder_name = f"{mission_name}-briefing-{today}"
    output_dir = PRESENTATIONS_ROOT / folder_name
    html_path = output_dir / "presentation.html"
    meta_path = output_dir / "meta.json"

    if html_path.exists() and not force:
        log(f"skipping {folder_name} (already exists, use --force to regenerate)")
        return True

    title = manifest.get("title", mission_name)

    if dry_run:
        log(f"dry-run: would generate briefing for mission {mission_name} ({title})")
        return True

    log(f"collecting reports for mission {mission_name}...")

    reports = collect_mission_reports(mission_dir)
    if not reports:
        log_err(f"no reports found for {mission_name}")
        return False

    reports = enforce_total_limit(reports)
    total_kb = sum(len(c) for _, c in reports) / 1024
    log(f"collected {len(reports)} report(s) ({total_kb:.1f} KB) for {mission_name}")

    prompt_template = read_file_safe(PROMPT_FILE, max_bytes=50 * 1024)
    if not prompt_template:
        log_err(f"prompt template not found at {PROMPT_FILE}")
        return False

    prompt = build_prompt(manifest, reports, folder_name, today, prompt_template)

    try:
        raw_output = run_claude(prompt, model=model, max_turns=max_turns)
    except RuntimeError as exc:
        log_err(f"Claude call failed for {mission_name}: {exc}")
        return False

    try:
        html = extract_html(raw_output)
    except ValueError as exc:
        log_err(f"failed to extract HTML for {mission_name}: {exc}")
        preview = " ".join(raw_output.split())[:300]
        log_err(f"raw output preview: {preview}")
        return False

    # Write output
    output_dir.mkdir(parents=True, exist_ok=True)
    html_path.write_text(html, encoding="utf-8")

    meta_title = f"\U0001f30d\U0001f4e1 {title} \u2014 Atlas Briefing"
    meta = {"title": meta_title}
    meta_path.write_text(json.dumps(meta, indent=2) + "\n", encoding="utf-8")

    log(f"wrote {html_path.relative_to(REPO_ROOT)}")
    log(f"wrote {meta_path.relative_to(REPO_ROOT)}")

    # Update manifest status
    update_manifest(manifest, folder_name)
    manifest_name = Path(manifest["_manifest_path"]).name
    log(f"updated {manifest_name} -> mission_status=briefed")

    return True


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> int:
    parser = argparse.ArgumentParser(
        description="Generate morning briefing presentations from completed codex-atlas missions."
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
        help="Maximum number of briefings to generate. 0 = no limit.",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Regenerate briefings even if output already exists or manifest is already briefed.",
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

    manifests = load_manifests()
    if not manifests:
        log("no atlas-mission manifests found")
        return 0

    eligible = [m for m in manifests if should_process(m, force=args.force)]
    if not eligible:
        log(f"found {len(manifests)} manifest(s), none eligible for briefing")
        return 0

    log(f"found {len(eligible)} eligible manifest(s) out of {len(manifests)} total")

    if args.limit > 0:
        eligible = eligible[: args.limit]
        log(f"limited to {len(eligible)} manifest(s)")

    successes = 0
    failures = 0
    skipped = 0

    for manifest in eligible:
        ok = generate_briefing(
            manifest=manifest,
            today=today,
            model=args.model,
            max_turns=args.max_turns,
            dry_run=args.dry_run,
            force=args.force,
        )
        if ok:
            successes += 1
        else:
            # Distinguish between "not ready" skips and real failures
            mission_name = manifest.get("mission_name", "")
            mission_dir = INSTANCES_DIR / mission_name
            if not (mission_dir / "MISSION-COMPLETE.md").exists():
                skipped += 1
            else:
                failures += 1

    log(
        f"completed "
        f"briefed={successes} skipped={skipped} failures={failures}"
    )
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
