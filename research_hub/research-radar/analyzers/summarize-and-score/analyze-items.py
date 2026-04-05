#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
THRESHOLDS_FILE = ROOT / "config/thresholds.yaml"
LENS_FILE = ROOT / "config/what-we-care-about-right-now.md"
PROMPT_FILE = ROOT / "analyzers/summarize-and-score/prompt.md"
SCHEMA_FILE = ROOT / "analyzers/summarize-and-score/schema.json"
QUEUE_DIR = ROOT / "data/queues/presentation-candidates"
MAX_ANALYSIS_ATTEMPTS = 2
SYSTEM_PROMPT = "\n".join([
    "You are running an automated scheduled task.",
    "Work autonomously and output only the requested JSON object.",
    "Do not wrap the JSON in markdown fences.",
])
MODEL_REQUIRED_KEYS = {
    "summary",
    "relevance_score",
    "why_it_matters_now",
}
OPTIONAL_MODEL_KEYS = {"presentation_candidate", "key_takeaways"}
AUTH_ERROR_MARKERS = (
    "OAuth token has expired",
    "authentication_error",
    "Failed to authenticate",
)


class ClaudeUnavailableError(RuntimeError):
    pass


def load_threshold(default: int = 9) -> int:
    for raw_line in THRESHOLDS_FILE.read_text(encoding="utf-8").splitlines():
        if raw_line.startswith("relevance_for_presentation:"):
            _, value = raw_line.split(":", 1)
            try:
                return int(value.strip())
            except ValueError:
                return default
    return default


def summary_path_for(item_path: Path) -> Path:
    topic_slug = item_path.parents[2].name
    item_type = item_path.parents[1].name
    item_id = item_path.stem
    return ROOT / "data/topics" / topic_slug / "summaries/items" / f"{item_type}--{item_id}.md"


def summary_overview_path(topic_slug: str) -> Path:
    return ROOT / "data/topics" / topic_slug / "summaries/overview.md"


def queue_manifest_path(analysis: dict[str, object]) -> Path:
    return QUEUE_DIR / f"{analysis['topic_slug']}--{analysis['item_type']}--{analysis['item_id']}.json"


def write_queue_manifest(item: dict[str, object], summary_path: Path, analysis: dict[str, object]) -> None:
    QUEUE_DIR.mkdir(parents=True, exist_ok=True)
    manifest_path = queue_manifest_path(analysis)
    payload = {
        "topic_slug": analysis["topic_slug"],
        "item_type": analysis["item_type"],
        "item_id": analysis["item_id"],
        "title": analysis["title"],
        "relevance_score": analysis["relevance_score"],
        "source_url": analysis["source_url"],
        "summary_path": str(summary_path.relative_to(ROOT)),
        "source_item_path": str(Path(item["item_path"]).relative_to(ROOT)),
        "queued_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    }
    manifest_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def clear_queue_manifest(analysis: dict[str, object]) -> None:
    manifest_path = queue_manifest_path(analysis)
    if manifest_path.exists():
        manifest_path.unlink()


def ensure_summary_overview(path: Path, topic_slug: str) -> None:
    if path.exists():
        return
    path.write_text(
        (
            f"# {topic_slug} — Summaries Overview\n\n"
            "Keep this file short. Roll up the most relevant analyzed items here and use `items/` for the full details.\n"
        ),
        encoding="utf-8",
    )


def iter_item_paths(topic_filters: set[str] | None) -> list[Path]:
    paths: list[Path] = []
    topics_root = ROOT / "data/topics"
    for topic_dir in sorted(path for path in topics_root.iterdir() if path.is_dir()):
        if topic_filters and topic_dir.name not in topic_filters:
            continue
        for item_type in ("youtube", "papers"):
            items_dir = topic_dir / item_type / "items"
            if not items_dir.exists():
                continue
            for item_path in sorted(items_dir.glob("*.md")):
                if item_path.name == ".gitkeep":
                    continue
                paths.append(item_path)
    return paths


def parse_title(text: str) -> str:
    first_line = text.splitlines()[0].strip() if text.splitlines() else "Untitled"
    return first_line.removeprefix("# ").strip() or "Untitled"


def parse_metadata(text: str) -> dict[str, str]:
    metadata: dict[str, str] = {}
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped.startswith("- ") or ":" not in stripped:
            continue
        label, value = stripped[2:].split(":", 1)
        metadata[label.strip().lower()] = value.strip()
    return metadata


def strip_ticks(value: str) -> str:
    return value.strip().strip("`")


def load_item(item_path: Path) -> dict[str, object]:
    text = item_path.read_text(encoding="utf-8")
    metadata = parse_metadata(text)
    topic_slug = item_path.parents[2].name
    item_type = item_path.parents[1].name
    return {
        "item_path": item_path,
        "topic_slug": topic_slug,
        "item_type": "paper" if item_type == "papers" else "youtube",
        "item_id": item_path.stem,
        "title": parse_title(text),
        "source_url": metadata.get("url", "").strip(),
        "priority": strip_ticks(metadata.get("priority", "unknown")),
        "source_context": strip_ticks(metadata.get("source context", "unknown")),
        "metadata": metadata,
        "text": text,
    }


def extract_section(text: str, heading: str) -> str:
    pattern = rf"^{re.escape(heading)}\n\n(.*?)(?=^## |\Z)"
    match = re.search(pattern, text, flags=re.MULTILINE | re.DOTALL)
    if not match:
        return ""
    return match.group(1).strip()


def sentence_excerpt(text: str, max_sentences: int = 2, max_chars: int = 500) -> str:
    cleaned = " ".join(text.split())
    if not cleaned:
        return ""
    parts = [part.strip() for part in re.split(r"(?<=[.!?])\s+", cleaned) if part.strip()]
    excerpt = " ".join(parts[:max_sentences]) if parts else cleaned
    if len(excerpt) > max_chars:
        excerpt = excerpt[: max_chars - 3].rstrip() + "..."
    return excerpt


def heuristic_focus_matches(item: dict[str, object]) -> list[str]:
    haystack = f"{item['title']} {item['text']} {item['source_context']}".lower()
    groups = [
        ("self-evolving AI systems", ["self-evolving", "self-improving", "recursive self-improvement", "meta-optimization"]),
        ("eval and experimentation loops", ["eval", "evaluation", "experiment", "regression", "feedback loop", "a/b testing", "ab testing"]),
        ("durable agent orchestration", ["agent", "orchestration", "planner", "worker", "retrieval", "parallel agent"]),
        ("agent systems for hard science problems", ["physics", "theorem", "proof", "science", "scientific", "math"]),
    ]
    matches: list[str] = []
    for label, keywords in groups:
        if any(keyword in haystack for keyword in keywords):
            matches.append(label)
    return matches


def heuristic_relevance(item: dict[str, object]) -> int:
    haystack = f"{item['title']} {item['text']} {item['source_context']}".lower()
    score = 2
    priority = str(item.get("priority", "unknown"))
    if priority == "super_relevant":
        score += 3
    elif priority == "relevant":
        score += 2

    weighted_keywords = [
        ("self-evolving", 2),
        ("self-improving", 2),
        ("agent", 1),
        ("orchestration", 1),
        ("eval", 1),
        ("experiment", 1),
        ("feedback", 1),
        ("science", 1),
        ("physics", 1),
        ("math", 1),
        ("theorem", 1),
        ("retrieval", 1),
    ]
    for keyword, weight in weighted_keywords:
        if keyword in haystack:
            score += weight

    metadata = item.get("metadata", {})
    if isinstance(metadata, dict):
        transcript_status = strip_ticks(str(metadata.get("transcript status", "")))
        full_text_status = strip_ticks(str(metadata.get("full text status", "")))
        if transcript_status == "ready":
            score += 1
        elif transcript_status in {"retry-needed", "unavailable", "missing"}:
            score -= 1
        if full_text_status == "abstract-only":
            score -= 1

    return max(1, min(10, score))


def fallback_analysis(item: dict[str, object], threshold: int, reason: str) -> dict[str, object]:
    metadata = item.get("metadata", {})
    if not isinstance(metadata, dict):
        metadata = {}

    focus_matches = heuristic_focus_matches(item)
    relevance_score = heuristic_relevance(item)
    caveats: list[str] = []
    key_takeaways: list[str] = [f"Fallback analysis used because {reason}."]

    if item["item_type"] == "paper":
        abstract = extract_section(str(item["text"]), "## Abstract")
        summary = sentence_excerpt(abstract, max_sentences=3)
        if not summary:
            summary = f"A paper titled '{item['title']}' was collected for this topic, but only limited metadata was available during fallback analysis."
        full_text_status = strip_ticks(str(metadata.get("full text status", "unknown")))
        if full_text_status != "ready":
            caveats.append(f"full text status was `{full_text_status}`")
            key_takeaways.append(f"Full text was not available during analysis; current summary is based on the abstract and metadata.")
        authors = str(metadata.get("authors", "")).strip()
        if authors:
            key_takeaways.append(f"Collected paper metadata includes authors: {authors}.")
    else:
        transcript = extract_section(str(item["text"]), "## Transcript")
        channel = strip_ticks(str(metadata.get("channel", "unknown")))
        duration = strip_ticks(str(metadata.get("duration", "unknown")))
        transcript_status = strip_ticks(str(metadata.get("transcript status", "unknown")))
        if transcript_status == "ready" and transcript and "Transcript fetch" not in transcript:
            summary = sentence_excerpt(transcript, max_sentences=3)
        else:
            summary = (
                f"A YouTube video titled '{item['title']}' from {channel} ({duration}) was collected for this topic. "
                "Transcript content was not reliably available, so this fallback summary is based on metadata only."
            )
            caveats.append(f"transcript status was `{transcript_status}`")
            key_takeaways.append(f"Transcript content was unavailable during analysis, so deeper content validation is still needed.")
        key_takeaways.append(f"Source channel during collection: {channel}.")

    if focus_matches:
        why_it_matters_now = (
            f"This item maps to {', '.join(focus_matches)} within the current Eywa and Atlas lens. "
            "It is relevant because the system is prioritizing durable agent improvement, evaluation, and hard-problem-solving workflows."
        )
    else:
        why_it_matters_now = (
            "This item appears adjacent to the current Eywa and Atlas lens, but the connection is weaker based on the available metadata. "
            "It is worth storing, but it should stay low-confidence until richer source content is available."
        )

    if caveats:
        why_it_matters_now += " Current caveat: " + "; ".join(caveats) + "."

    if not any("focus" in takeaway.lower() for takeaway in key_takeaways):
        if focus_matches:
            key_takeaways.append(f"Strongest current match: {focus_matches[0]}.")
        else:
            key_takeaways.append("No strong focus-area keyword match was found beyond the topic assignment.")

    key_takeaways = key_takeaways[:5]

    return {
        "item_id": str(item["item_id"]),
        "topic_slug": str(item["topic_slug"]),
        "item_type": str(item["item_type"]),
        "title": str(item["title"]),
        "source_url": str(item["source_url"]),
        "summary": summary,
        "relevance_score": relevance_score,
        "why_it_matters_now": why_it_matters_now,
        "key_takeaways": key_takeaways,
        "presentation_candidate": relevance_score >= threshold,
        "model_presentation_candidate": False,
        "analysis_mode": "fallback",
        "analysis_error": reason,
    }


def build_prompt(item: dict[str, object], lens: str, prompt_template: str, schema_text: str) -> str:
    return "\n\n".join(
        [
            "Analyze this Research Radar item and return only one JSON object.",
            "The system will fill stable metadata fields from the source item.",
            "Your generated fields must include: summary, relevance_score, why_it_matters_now.",
            "If you include presentation_candidate, it must be a boolean.",
            "Required schema:",
            schema_text,
            "Scoring lens:",
            lens,
            "Prompt guidance:",
            prompt_template,
            "Item metadata:",
            json.dumps(
                {
                    "item_id": item["item_id"],
                    "topic_slug": item["topic_slug"],
                    "item_type": item["item_type"],
                    "title": item["title"],
                    "source_url": item["source_url"],
                    "priority": item["priority"],
                    "source_context": item["source_context"],
                },
                indent=2,
            ),
            "Item markdown:",
            str(item["text"]),
        ]
    )


def extract_json_block(raw: str) -> dict[str, object]:
    candidate = raw.strip()
    if candidate.startswith("```"):
        lines = candidate.splitlines()
        if len(lines) >= 3:
            candidate = "\n".join(lines[1:-1]).strip()
    start = candidate.find("{")
    end = candidate.rfind("}")
    if start == -1 or end == -1 or end <= start:
        raise ValueError("Claude output did not include a JSON object")
    parsed = json.loads(candidate[start : end + 1])
    return best_analysis_object(parsed)


def iter_objects(value: object) -> list[dict[str, object]]:
    objects: list[dict[str, object]] = []
    if isinstance(value, dict):
        objects.append(value)
        for nested in value.values():
            objects.extend(iter_objects(nested))
    elif isinstance(value, list):
        for nested in value:
            objects.extend(iter_objects(nested))
    return objects


def best_analysis_object(value: object) -> dict[str, object]:
    candidates = iter_objects(value)
    if not candidates:
        raise ValueError("Claude output did not contain a JSON object")

    best: dict[str, object] | None = None
    best_score = -1
    for candidate in candidates:
        score = len(MODEL_REQUIRED_KEYS & set(candidate))
        if OPTIONAL_MODEL_KEYS & set(candidate):
            score += 1
        if score > best_score:
            best = candidate
            best_score = score

    if best is None or best_score <= 0:
        raise ValueError("Claude output did not contain an analysis object")
    return best


def validate_analysis(data: dict[str, object], item: dict[str, object], threshold: int) -> dict[str, object]:
    missing = MODEL_REQUIRED_KEYS - set(data)
    if missing:
        raise ValueError(f"Missing required analysis keys: {sorted(missing)}")

    relevance_score = int(data["relevance_score"])
    if relevance_score < 1 or relevance_score > 10:
        raise ValueError("relevance_score must be between 1 and 10")

    data["item_id"] = str(item["item_id"])
    data["topic_slug"] = str(item["topic_slug"])
    data["item_type"] = str(item["item_type"])
    data["title"] = str(item["title"])
    data["source_url"] = str(item["source_url"])
    data["relevance_score"] = relevance_score
    data["summary"] = str(data["summary"]).strip()
    data["why_it_matters_now"] = str(data["why_it_matters_now"]).strip()
    data["key_takeaways"] = [str(entry).strip() for entry in data.get("key_takeaways", []) if str(entry).strip()]
    model_candidate = data.get("presentation_candidate")
    if isinstance(model_candidate, str):
        model_candidate = model_candidate.strip().lower() in {"true", "yes", "1"}
    data["model_presentation_candidate"] = bool(model_candidate)
    data["analysis_mode"] = str(data.get("analysis_mode", "claude")).strip() or "claude"
    if "analysis_error" in data:
        data["analysis_error"] = str(data["analysis_error"]).strip()
    data["presentation_candidate"] = relevance_score >= threshold
    data["presentation_threshold"] = threshold
    return data


def run_claude_raw(prompt: str, model: str, max_turns: int, cwd: Path) -> str:
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
    result = subprocess.run(command, cwd=cwd, capture_output=True, text=True, check=False)
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


def build_retry_prompt(base_prompt: str, raw_output: str, error: Exception) -> str:
    return "\n\n".join(
        [
            base_prompt,
            "Your previous response was invalid for the analysis pipeline.",
            f"Validation issue: {error}",
            "Return one corrected JSON object only.",
            "Generated fields required: summary, relevance_score, why_it_matters_now.",
            "presentation_candidate is optional, but if included it must be boolean.",
            "Previous invalid response:",
            raw_output,
        ]
    )


def run_claude_analysis(
    prompt: str,
    model: str,
    max_turns: int,
    cwd: Path,
    item: dict[str, object],
    threshold: int,
) -> dict[str, object]:
    attempt_prompt = prompt
    last_error: Exception | None = None
    last_output = ""

    for attempt in range(MAX_ANALYSIS_ATTEMPTS):
        try:
            raw_output = run_claude_raw(attempt_prompt, model=model, max_turns=max_turns, cwd=cwd)
        except ClaudeUnavailableError as exc:
            return validate_analysis(fallback_analysis(item, threshold=threshold, reason=str(exc)), item, threshold=threshold)
        last_output = raw_output
        try:
            parsed = extract_json_block(raw_output)
            return validate_analysis(parsed, item, threshold=threshold)
        except Exception as exc:
            last_error = exc
            if attempt + 1 < MAX_ANALYSIS_ATTEMPTS:
                attempt_prompt = build_retry_prompt(prompt, raw_output, exc)

    preview = " ".join(last_output.split())
    if len(preview) > 400:
        preview = preview[:400] + "..."
    return validate_analysis(
        fallback_analysis(item, threshold=threshold, reason=f"Claude response invalid: {last_error}. preview={preview}"),
        item,
        threshold=threshold,
    )


def summary_markdown(item: dict[str, object], analysis: dict[str, object]) -> str:
    generated_at = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    lines = [
        f"# {analysis['title']}\n\n",
        f"- Topic slug: `{analysis['topic_slug']}`\n",
        f"- Item type: `{analysis['item_type']}`\n",
        f"- Source item: `{item['item_path'].relative_to(ROOT)}`\n",
        f"- Source URL: {analysis['source_url']}\n",
        f"- Relevance score: `{analysis['relevance_score']}`\n",
        f"- Presentation candidate: `{str(analysis['presentation_candidate']).lower()}`\n",
        f"- Model presentation candidate: `{str(analysis['model_presentation_candidate']).lower()}`\n",
        f"- Analysis mode: `{analysis.get('analysis_mode', 'claude')}`\n",
        f"- Generated at UTC: `{generated_at}`\n\n",
        "## Summary\n\n",
        f"{analysis['summary']}\n\n",
        "## Why It Matters Now\n\n",
        f"{analysis['why_it_matters_now']}\n\n",
        "## Key Takeaways\n\n",
    ]
    for takeaway in analysis.get("key_takeaways", []):
        lines.append(f"- {takeaway}\n")
    if not analysis.get("key_takeaways"):
        lines.append("- No key takeaways provided.\n")
    if analysis.get("analysis_error"):
        lines.extend([
            "\n## Analysis Notes\n\n",
            f"{analysis['analysis_error']}\n\n",
        ])
    lines.extend([
        "\n## Structured Output\n\n",
        "```json\n",
        json.dumps(analysis, indent=2, sort_keys=True),
        "\n```\n",
    ])
    return "".join(lines)


def append_overview(overview_path: Path, summary_path: Path, analysis: dict[str, object]) -> None:
    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    section = [
        "",
        f"## {stamp} — {analysis['item_type']} score {analysis['relevance_score']}",
        "",
        f"- **{analysis['title']}**",
        f"  source: {analysis['source_url']}",
        f"  summary file: `items/{summary_path.name}`",
        f"  presentation candidate: `{str(analysis['presentation_candidate']).lower()}`",
    ]
    with overview_path.open("a", encoding="utf-8") as handle:
        handle.write("\n".join(section) + "\n")


def main() -> int:
    parser = argparse.ArgumentParser(description="Analyze Research Radar items with Claude and write per-item summaries.")
    parser.add_argument("--topic", dest="topic_slugs", action="append", default=[], help="Limit analysis to one or more topic slugs.")
    parser.add_argument("--limit", type=int, default=0, help="Stop after analyzing N items. Use 0 for no limit.")
    parser.add_argument("--force", action="store_true", help="Reanalyze items even if a summary file already exists.")
    parser.add_argument("--dry-run", action="store_true", help="Show which items would be analyzed without calling Claude or writing files.")
    parser.add_argument("--model", default="sonnet", help="Claude model alias.")
    parser.add_argument("--max-turns", type=int, default=8, help="Maximum Claude turns per item.")
    args = parser.parse_args()

    topic_filters = set(args.topic_slugs) if args.topic_slugs else None
    threshold = load_threshold()
    lens = LENS_FILE.read_text(encoding="utf-8")
    prompt_template = PROMPT_FILE.read_text(encoding="utf-8")
    schema_text = SCHEMA_FILE.read_text(encoding="utf-8")

    items = []
    for item_path in iter_item_paths(topic_filters):
        summary_path = summary_path_for(item_path)
        if summary_path.exists() and not args.force:
            continue
        items.append(item_path)

    if args.limit > 0:
        items = items[: args.limit]

    if not items:
        print("[analyze-items] no items matched the current selection")
        return 0

    if args.dry_run:
        for item_path in items:
            print(f"[analyze-items] dry-run: {item_path.relative_to(ROOT)}")
        print(f"[analyze-items] completed dry-run items={len(items)}")
        return 0

    total = 0
    failures = 0
    for item_path in items:
        item = load_item(item_path)
        summary_path = summary_path_for(item_path)
        summary_path.parent.mkdir(parents=True, exist_ok=True)
        overview_path = summary_overview_path(str(item["topic_slug"]))
        ensure_summary_overview(overview_path, str(item["topic_slug"]))
        prompt = build_prompt(item, lens, prompt_template, schema_text)

        try:
            analysis = run_claude_analysis(
                prompt,
                model=args.model,
                max_turns=args.max_turns,
                cwd=ROOT,
                item=item,
                threshold=threshold,
            )
            summary_path.write_text(summary_markdown(item, analysis), encoding="utf-8")
            append_overview(overview_path, summary_path, analysis)
            if analysis["presentation_candidate"]:
                write_queue_manifest(item, summary_path, analysis)
            else:
                clear_queue_manifest(analysis)
            print(
                f"[analyze-items] topic={item['topic_slug']} item={item['item_id']} score={analysis['relevance_score']} presentation_candidate={str(analysis['presentation_candidate']).lower()}"
            )
            total += 1
        except Exception as exc:  # pragma: no cover
            failures += 1
            print(f"[analyze-items] failed {item_path.relative_to(ROOT)}: {exc}", file=sys.stderr)

    print(f"[analyze-items] completed analyzed={total} failures={failures}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
