#!/usr/bin/env python3
from __future__ import annotations

import argparse
import html
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta, timezone
from pathlib import Path
from urllib.error import HTTPError, URLError

ROOT = Path(__file__).resolve().parents[2]
TOPICS_FILE = ROOT / "config/topics-we-care-about.yaml"
THRESHOLDS_FILE = ROOT / "config/thresholds.yaml"
TARGETED_TERMS_FILE = ROOT / "config/targeted-arxiv-terms.yaml"
ARXIV_API = "http://export.arxiv.org/api/query"

# Mapping from targeted-term research areas to topic directory slugs.
TARGETED_AREA_TO_TOPIC: dict[str, str] = {
    "navier_stokes": "millennium-prize-navier-stokes",
    "yang_mills": "millennium-prize-yang-mills",
    "riemann_hypothesis": "millennium-prize-riemann-hypothesis",
    "bsd_conjecture": "millennium-prize-bsd-conjecture",
    "hodge_conjecture": "millennium-prize-hodge-conjecture",
    "p_vs_np": "millennium-prize-p-vs-np",
    "quantum_gravity": "quantum-physics-breakthroughs",
}
ATOM_NS = {
    "atom": "http://www.w3.org/2005/Atom",
    "arxiv": "http://arxiv.org/schemas/atom",
}
ARXIV_DATETIME_FORMAT = "%Y-%m-%dT%H:%M:%SZ"

# arXiv's published rate limit is one request every 3 seconds. We use 3.5s
# to give a small safety margin. The previous unthrottled implementation
# slammed ~234 sequential requests per nightly run and ~half got 429'd
# (silently dropped 19/39 topics).
_ARXIV_MIN_REQUEST_INTERVAL = 3.5
# Sentinel: None means "no prior request from this process". We can't use
# 0.0 because time.monotonic() on macOS returns ~0 at process start, which
# would make the first call see "now - 0.0 ≈ 0" and sleep spuriously.
_arxiv_last_request_time: float | None = None


def _arxiv_throttle() -> None:
    """Block until at least _ARXIV_MIN_REQUEST_INTERVAL has elapsed since
    the last arXiv request from this process. Updates the last-request
    timestamp on return."""
    global _arxiv_last_request_time
    if _arxiv_last_request_time is not None:
        now = time.monotonic()
        wait = _ARXIV_MIN_REQUEST_INTERVAL - (now - _arxiv_last_request_time)
        if wait > 0:
            time.sleep(wait)
    _arxiv_last_request_time = time.monotonic()


class ArxivRateLimitError(RuntimeError):
    pass


class ArxivTransientError(RuntimeError):
    pass


def load_topics() -> list[dict[str, object]]:
    topics: list[dict[str, object]] = []
    current: dict[str, object] | None = None
    current_list: str | None = None

    for raw_line in TOPICS_FILE.read_text(encoding="utf-8").splitlines():
        line = raw_line.rstrip()
        if line.startswith("  - slug: "):
            if current:
                topics.append(current)
            current = {
                "slug": line.split(": ", 1)[1],
                "collect_from": [],
                "source_context": [],
                "paper_queries": [],
            }
            current_list = None
        elif current and line.startswith("    name: "):
            current["name"] = line.split(": ", 1)[1]
            current_list = None
        elif current and line.startswith("    priority: "):
            current["priority"] = line.split(": ", 1)[1]
            current_list = None
        elif current and line.startswith("    collect_from:"):
            current_list = "collect_from"
        elif current and line.startswith("    source_context:"):
            current_list = "source_context"
        elif current and line.startswith("    paper_queries:"):
            current_list = "paper_queries"
        elif current and line.startswith("      - ") and current_list:
            current.setdefault(current_list, []).append(line.split("- ", 1)[1].strip())

    if current:
        topics.append(current)

    return [topic for topic in topics if "papers" in topic.get("collect_from", [])]


def load_max_results(default: int = 5) -> int:
    for raw_line in THRESHOLDS_FILE.read_text(encoding="utf-8").splitlines():
        if raw_line.startswith("paper_max_results_per_topic:"):
            _, value = raw_line.split(":", 1)
            try:
                return int(value.strip())
            except ValueError:
                return default
    return default


def topic_paths(topic_slug: str) -> dict[str, Path]:
    base = ROOT / "data/topics" / topic_slug / "papers"
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


def collapse_whitespace(value: str) -> str:
    return " ".join(value.split())


def normalize_phrase(value: str) -> str:
    return collapse_whitespace(re.sub(r"[/,+()]+", " ", value))


def topic_query_phrases(topic: dict[str, object]) -> list[str]:
    queries: list[str] = []
    seen: set[str] = set()

    def add(query: str) -> None:
        clean = collapse_whitespace(query)
        if not clean:
            return
        key = clean.lower()
        if key in seen:
            return
        seen.add(key)
        queries.append(clean)

    topic_name = str(topic.get("name", ""))
    source_context = [str(value).strip() for value in topic.get("source_context", []) if str(value).strip()]
    explicit_queries = [str(value).strip() for value in topic.get("paper_queries", []) if str(value).strip()]

    add(topic_name)
    normalized_name = normalize_phrase(topic_name)
    if normalized_name.lower() != topic_name.lower():
        add(normalized_name)
    for query in explicit_queries:
        add(query)

    lowered = f"{topic_name} {' '.join(source_context)}".lower()
    keyword_expansions = [
        (["self-evolving", "self-improving", "recursive improvement", "meta-optimization"], [
            "self-improving agents",
            "recursive self-improvement",
            "agent optimization",
        ]),
        (["eval", "experimentation", "regression", "a/b testing", "ab testing"], [
            "agent evaluation",
            "LLM evaluation",
            "automated experimentation",
        ]),
        (["orchestration", "planner", "worker", "multi-agent", "parallel agent"], [
            "multi-agent systems",
            "agent orchestration",
        ]),
        (["science", "research", "hypotheses", "literature", "validation"], [
            "AI for science",
            "research agents",
            "autonomous scientific discovery",
        ]),
        (["math", "theorem", "proof"], [
            "AI theorem proving",
            "machine learning for theorem proving",
        ]),
        (["physics"], [
            "AI for physics",
            "physics reasoning language models",
        ]),
        (["retrieval"], ["retrieval-augmented agents"]),
        (["observability", "logging", "tracing"], ["agent observability"]),
        (["safe tool"], ["tool-using agents"]),
        (["cost-aware", "token-aware"], ["efficient agent systems"]),
    ]

    for keywords, expansions in keyword_expansions:
        if any(keyword in lowered for keyword in keywords):
            for expansion in expansions:
                add(expansion)

    if "atlas" in source_context:
        for expansion in ["AI for science", "autonomous scientific discovery", "research agents"]:
            add(expansion)
    if "eywa" in source_context:
        for expansion in ["agent systems", "LLM agents"]:
            add(expansion)

    return queries[:6]


def build_search_expression(queries: list[str]) -> str:
    if not queries:
        raise ValueError("At least one search query is required")
    return " OR ".join(f'all:"{query}"' for query in queries)


def build_query_url(search_expression: str, max_results: int) -> str:
    params = {
        "search_query": search_expression,
        "start": "0",
        "max_results": str(max_results),
        "sortBy": "submittedDate",
        "sortOrder": "descending",
    }
    return f"{ARXIV_API}?{urllib.parse.urlencode(params)}"


def request_feed(url: str) -> bytes:
    request = urllib.request.Request(url, headers={"User-Agent": "research-radar/0.1"})
    last_error: Exception | None = None

    # 5 attempts with exponential backoff on 429 / transient errors. The
    # global throttle (_arxiv_throttle) handles steady-state pacing; this
    # backoff handles bursts where arXiv tells us to slow down anyway.
    backoff_schedule = [5, 15, 45, 90]  # seconds to wait BEFORE retries 2..5

    for attempt in range(5):
        _arxiv_throttle()
        buffer = bytearray()
        try:
            with urllib.request.urlopen(request, timeout=15) as response:
                while True:
                    chunk = response.read(8192)
                    if not chunk:
                        break
                    buffer.extend(chunk)
                    if b"</feed>" in buffer:
                        break

            payload = bytes(buffer)
            if b"</feed>" not in payload:
                raise RuntimeError("arXiv feed did not finish cleanly")
            return payload.split(b"</feed>", 1)[0] + b"</feed>"
        except HTTPError as exc:
            last_error = exc
            if exc.code == 429 and attempt < len(backoff_schedule):
                # Honor Retry-After header if arXiv sends one, otherwise
                # use our exponential schedule.
                retry_after_header = exc.headers.get("Retry-After") if exc.headers else None
                try:
                    wait = int(retry_after_header) if retry_after_header else backoff_schedule[attempt]
                except (TypeError, ValueError):
                    wait = backoff_schedule[attempt]
                print(
                    f"[collect-papers] arXiv 429 on attempt {attempt + 1}, "
                    f"backing off {wait}s",
                    file=sys.stderr,
                )
                time.sleep(wait)
                continue
            if exc.code == 429:
                raise ArxivRateLimitError("arXiv HTTP error 429 after retries") from exc
            raise RuntimeError(f"arXiv HTTP error {exc.code}") from exc
        except (URLError, TimeoutError, RuntimeError) as exc:
            last_error = exc
            if attempt < len(backoff_schedule):
                wait = backoff_schedule[attempt]
                print(
                    f"[collect-papers] arXiv transient error on attempt {attempt + 1}, "
                    f"backing off {wait}s: {exc}",
                    file=sys.stderr,
                )
                time.sleep(wait)
                continue
            raise ArxivTransientError(f"arXiv request failed: {exc}") from exc

    raise RuntimeError(f"arXiv request failed: {last_error}")


def safe_item_id(raw_identifier: str) -> str:
    return re.sub(r"[^A-Za-z0-9._-]+", "-", raw_identifier.replace("/", "--")).strip("-")


def parse_arxiv_datetime(value: str) -> datetime | None:
    if not value:
        return None
    try:
        return datetime.strptime(value, ARXIV_DATETIME_FORMAT).replace(tzinfo=timezone.utc)
    except ValueError:
        return None


def download_full_text(paper_id: str, pdf_url: str) -> tuple[str, str]:
    """Attempt to download the PDF and extract text via pdftotext.

    Returns (full_text_status, full_text_content).
    full_text_status is 'ready' on success, 'abstract-only' on any failure.
    """
    if not pdf_url:
        # Construct from paper ID if missing.
        pdf_url = f"https://arxiv.org/pdf/{paper_id}.pdf"

    # Check pdftotext availability first to avoid a pointless download.
    if not shutil.which("pdftotext"):
        print(f"[collect-papers] pdftotext not found on PATH — falling back to abstract for {paper_id}")
        return "abstract-only", ""

    try:
        import requests  # noqa: F811 — available on the box per task spec
    except ImportError:
        # Fall back to urllib if requests is somehow missing.
        return _download_full_text_urllib(paper_id, pdf_url)

    try:
        response = requests.get(pdf_url, timeout=30, headers={"User-Agent": "research-radar/0.1"})
        response.raise_for_status()
    except Exception as exc:
        print(f"[collect-papers] PDF download failed for {paper_id}: {exc}")
        return "abstract-only", ""

    return _extract_text_from_pdf_bytes(paper_id, response.content)


def _download_full_text_urllib(paper_id: str, pdf_url: str) -> tuple[str, str]:
    """Fallback downloader using only stdlib."""
    req = urllib.request.Request(pdf_url, headers={"User-Agent": "research-radar/0.1"})
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            pdf_bytes = resp.read()
    except Exception as exc:
        print(f"[collect-papers] PDF download (urllib) failed for {paper_id}: {exc}")
        return "abstract-only", ""
    return _extract_text_from_pdf_bytes(paper_id, pdf_bytes)


def _extract_text_from_pdf_bytes(paper_id: str, pdf_bytes: bytes) -> tuple[str, str]:
    """Write PDF bytes to a temp file, run pdftotext, return extracted text."""
    with tempfile.TemporaryDirectory(prefix="research-radar-pdf-") as tmp:
        pdf_path = os.path.join(tmp, "paper.pdf")
        txt_path = os.path.join(tmp, "paper.txt")
        with open(pdf_path, "wb") as fh:
            fh.write(pdf_bytes)

        result = subprocess.run(
            ["pdftotext", "-layout", pdf_path, txt_path],
            capture_output=True, text=True, check=False,
        )
        if result.returncode != 0:
            print(f"[collect-papers] pdftotext failed for {paper_id}: {result.stderr.strip()}")
            return "abstract-only", ""

        try:
            text = Path(txt_path).read_text(encoding="utf-8", errors="replace").strip()
        except Exception as exc:
            print(f"[collect-papers] could not read pdftotext output for {paper_id}: {exc}")
            return "abstract-only", ""

        if not text:
            print(f"[collect-papers] pdftotext produced empty output for {paper_id}")
            return "abstract-only", ""

        return "ready", text


def load_targeted_terms() -> list[dict[str, object]]:
    """Load targeted arXiv search terms from config/targeted-arxiv-terms.yaml.

    Expected YAML structure (parsed with a lightweight line parser):
        areas:
          - area: navier_stokes
            terms:
              - "Navier-Stokes existence and smoothness"
              - "Navier-Stokes regularity"
          - area: yang_mills
            terms:
              - "Yang-Mills mass gap"

    Returns a list of dicts with keys: area (str), terms (list[str]).
    Returns an empty list if the file does not exist.
    """
    if not TARGETED_TERMS_FILE.exists():
        return []

    areas: list[dict[str, object]] = []
    current: dict[str, object] | None = None
    in_terms = False

    for raw_line in TARGETED_TERMS_FILE.read_text(encoding="utf-8").splitlines():
        line = raw_line.rstrip()

        if line.startswith("  - area:"):
            if current:
                areas.append(current)
            area_name = line.split(":", 1)[1].strip().strip('"').strip("'")
            current = {"area": area_name, "terms": []}
            in_terms = False
        elif current is not None and line.strip() == "terms:":
            in_terms = True
        elif current is not None and in_terms and line.strip().startswith("- "):
            term = line.strip().lstrip("- ").strip().strip('"').strip("'")
            if term:
                current.setdefault("terms", []).append(term)
        elif line and not line.startswith(" ") and not line.startswith("#"):
            in_terms = False

    if current:
        areas.append(current)

    return areas


def parse_entry(entry: ET.Element) -> dict[str, object]:
    entry_id = collapse_whitespace(entry.findtext("atom:id", default="", namespaces=ATOM_NS))
    title = html.unescape(collapse_whitespace(entry.findtext("atom:title", default="", namespaces=ATOM_NS)))
    summary = html.unescape(collapse_whitespace(entry.findtext("atom:summary", default="", namespaces=ATOM_NS)))
    published = collapse_whitespace(entry.findtext("atom:published", default="", namespaces=ATOM_NS))
    updated = collapse_whitespace(entry.findtext("atom:updated", default="", namespaces=ATOM_NS))
    authors = [
        collapse_whitespace(author.findtext("atom:name", default="", namespaces=ATOM_NS))
        for author in entry.findall("atom:author", ATOM_NS)
    ]

    pdf_url = ""
    primary_url = entry_id
    for link in entry.findall("atom:link", ATOM_NS):
        rel = link.attrib.get("rel", "")
        title_attr = link.attrib.get("title", "")
        href = link.attrib.get("href", "")
        if rel == "alternate" and href:
            primary_url = href
        if title_attr == "pdf" and href:
            pdf_url = href

    raw_identifier = entry_id.rsplit("/", 1)[-1]
    primary_category = ""
    primary_node = entry.find("arxiv:primary_category", ATOM_NS)
    if primary_node is not None:
        primary_category = primary_node.attrib.get("term", "").strip()

    categories: list[str] = []
    for category in entry.findall("atom:category", ATOM_NS):
        term = category.attrib.get("term", "").strip()
        if term and term not in categories:
            categories.append(term)

    doi = collapse_whitespace(entry.findtext("arxiv:doi", default="", namespaces=ATOM_NS))
    journal_ref = collapse_whitespace(entry.findtext("arxiv:journal_ref", default="", namespaces=ATOM_NS))
    comment = collapse_whitespace(entry.findtext("arxiv:comment", default="", namespaces=ATOM_NS))

    return {
        "id": raw_identifier,
        "item_id": safe_item_id(raw_identifier),
        "entry_id": entry_id,
        "title": title,
        "summary": summary,
        "published": published,
        "updated": updated,
        "published_at": parse_arxiv_datetime(published),
        "updated_at": parse_arxiv_datetime(updated),
        "authors": [author for author in authors if author],
        "url": primary_url,
        "pdf_url": pdf_url,
        "primary_category": primary_category,
        "categories": categories,
        "doi": doi,
        "journal_ref": journal_ref,
        "comment": comment,
    }


def fetch_entries(queries: list[str], max_results: int) -> list[dict[str, object]]:
    search_expression = build_search_expression(queries)
    payload = request_feed(build_query_url(search_expression, max_results=max_results))
    root = ET.fromstring(payload)
    entries = []
    for entry in root.findall("atom:entry", ATOM_NS):
        parsed = parse_entry(entry)
        if parsed["id"] and parsed["url"]:
            entries.append(parsed)
    return entries


def filter_recent(entries: list[dict[str, object]], lookback_hours: int) -> list[dict[str, object]]:
    if lookback_hours <= 0:
        return entries

    cutoff = datetime.now(timezone.utc) - timedelta(hours=lookback_hours)
    recent_entries = []
    for entry in entries:
        published_at = entry.get("published_at")
        if isinstance(published_at, datetime) and published_at >= cutoff:
            recent_entries.append(entry)
    return recent_entries


def ensure_overview_header(overview_path: Path, topic_name: str) -> None:
    if overview_path.exists():
        return
    overview_path.write_text(
        (
            f"# {topic_name} — Papers Overview\n\n"
            "Keep this file short. Roll up the main new papers, notable authors, and useful "
            "research directions for this topic here.\n\n"
            "Full item files belong in `items/`.\n"
        ),
        encoding="utf-8",
    )


def metadata_line(label: str, value: str) -> str:
    if not value:
        return ""
    return f"- {label}: {value}\n"


def item_body(
    topic: dict[str, object],
    paper: dict[str, object],
    queries: list[str],
    *,
    full_text_status: str = "abstract-only",
    full_text_content: str = "",
    targeted_area: str | None = None,
) -> str:
    topic_name = str(topic["name"])
    priority = str(topic["priority"])
    source_context = ", ".join(topic.get("source_context", [])) or "unknown"
    search_queries = " | ".join(queries)
    authors = ", ".join(paper["authors"]) if paper["authors"] else "Unknown"
    categories = ", ".join(paper["categories"]) if paper["categories"] else "unknown"
    collected_at = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    full_text_section = full_text_content if full_text_content else "Full paper text not extracted yet. Use the paper URL or PDF link above."

    lines = [
        f"# {paper['title']}\n\n",
        f"- Topic: `{topic_name}`\n",
        f"- Priority: `{priority}`\n",
        f"- Source context: `{source_context}`\n",
        "- Type: `paper`\n",
        "- Collector: `arXiv`\n",
        f"- Paper ID: `{paper['id']}`\n",
        f"- Item ID: `{paper['item_id']}`\n",
        f"- Authors: {authors}\n",
        f"- Published: `{paper['published']}`\n",
        f"- Updated: `{paper['updated']}`\n",
        metadata_line("Primary category", f"`{paper['primary_category']}`" if paper["primary_category"] else ""),
        f"- Categories: `{categories}`\n",
        metadata_line("DOI", f"`{paper['doi']}`" if paper["doi"] else ""),
        metadata_line("Journal ref", str(paper["journal_ref"])),
        metadata_line("Comment", str(paper["comment"])),
        f"- URL: {paper['url']}\n",
        metadata_line("PDF", str(paper["pdf_url"])),
        f"- Search queries: {search_queries}\n",
        f"- Collected at UTC: `{collected_at}`\n",
        f"- Full text status: `{full_text_status}`\n",
    ]
    if targeted_area:
        lines.append(f"- Targeted research area: `{targeted_area}`\n")
    lines.extend([
        "- Analysis status: `pending`\n\n",
        "## Abstract\n\n",
        f"{paper['summary']}\n\n",
        "## Summary\n\n",
        "Not analyzed yet.\n\n",
        "## Full Text\n\n",
        f"{full_text_section}\n\n",
        "## Notes\n\n",
        "- Freshly collected from arXiv by Research Radar.\n",
    ])
    return "".join(line for line in lines if line)


def append_overview(overview_path: Path, papers: list[dict[str, object]]) -> None:
    if not papers:
        return

    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    section = ["", f"## {stamp} — {len(papers)} new papers", ""]
    for paper in papers:
        authors = ", ".join(paper["authors"][:3]) if paper["authors"] else "Unknown"
        if len(paper["authors"]) > 3:
            authors += ", et al."
        published = str(paper["published"])[:10] if paper["published"] else "unknown"
        section.append(f"- **{paper['title']}** — {authors}")
        section.append(f"  published: `{published}`")
        section.append(f"  {paper['url']}")
        section.append(f"  item: `items/{paper['item_id']}.md`")
    overview_path.parent.mkdir(parents=True, exist_ok=True)
    with overview_path.open("a", encoding="utf-8") as handle:
        handle.write("\n".join(section) + "\n")


def run_topic(topic: dict[str, object], max_results: int, lookback_hours: int, dry_run: bool) -> int:
    slug = str(topic["slug"])
    name = str(topic["name"])
    paths = topic_paths(slug)
    paths["items"].mkdir(parents=True, exist_ok=True)
    ensure_overview_header(paths["overview"], name)
    seen = read_seen_ids(paths["seen"])
    queries = topic_query_phrases(topic)
    effective_max_results = max(max_results, min(15, max(5, len(queries) * 3)))

    if dry_run:
        print(f"[collect-papers] dry-run topic: {slug} :: {name}")
        print(f"[collect-papers] queries: {' | '.join(queries)}")
        return 0

    papers = fetch_entries(queries, max_results=effective_max_results)
    recent_papers = filter_recent(papers, lookback_hours=lookback_hours)
    new_papers: list[dict[str, object]] = []
    seen_this_run: set[str] = set()

    for paper in recent_papers:
        paper_id = str(paper["id"])
        if paper_id in seen or paper_id in seen_this_run:
            continue
        seen_this_run.add(paper_id)

        # Attempt full-text extraction from the PDF.
        full_text_status, full_text_content = download_full_text(
            paper_id, str(paper.get("pdf_url", ""))
        )

        item_path = paths["items"] / f"{paper['item_id']}.md"
        item_path.write_text(
            item_body(topic, paper, queries, full_text_status=full_text_status, full_text_content=full_text_content),
            encoding="utf-8",
        )
        new_papers.append(paper)

    if new_papers:
        with paths["seen"].open("a", encoding="utf-8") as handle:
            for paper in new_papers:
                handle.write(str(paper["id"]) + "\n")
        append_overview(paths["overview"], new_papers)

    print(
        f"[collect-papers] topic={slug} queries={len(queries)} candidates={len(papers)} recent_papers={len(recent_papers)} new_papers={len(new_papers)}"
    )
    return len(new_papers)


def run_targeted_area(
    area: str, terms: list[str], max_results: int, lookback_hours: int, dry_run: bool
) -> int:
    """Run arXiv searches for a single targeted research area and write items to the mapped topic dir."""
    topic_slug = TARGETED_AREA_TO_TOPIC.get(area)
    if not topic_slug:
        print(f"[collect-papers] WARNING: no topic mapping for targeted area '{area}' — skipping")
        return 0

    paths = topic_paths(topic_slug)
    paths["items"].mkdir(parents=True, exist_ok=True)
    ensure_overview_header(paths["overview"], f"Targeted: {area}")
    seen = read_seen_ids(paths["seen"])

    # Build a synthetic topic dict for item_body.
    synthetic_topic: dict[str, object] = {
        "slug": topic_slug,
        "name": area.replace("_", " ").title(),
        "priority": "high",
        "source_context": ["targeted-arxiv-terms"],
    }

    if dry_run:
        print(f"[collect-papers] dry-run targeted area: {area} -> {topic_slug}")
        print(f"[collect-papers] targeted terms: {' | '.join(terms)}")
        return 0

    papers = fetch_entries(terms, max_results=max_results)
    recent_papers = filter_recent(papers, lookback_hours=lookback_hours)
    new_papers: list[dict[str, object]] = []
    seen_this_run: set[str] = set()

    for paper in recent_papers:
        paper_id = str(paper["id"])
        if paper_id in seen or paper_id in seen_this_run:
            continue
        seen_this_run.add(paper_id)

        full_text_status, full_text_content = download_full_text(
            paper_id, str(paper.get("pdf_url", ""))
        )

        item_path = paths["items"] / f"{paper['item_id']}.md"
        item_path.write_text(
            item_body(
                synthetic_topic,
                paper,
                terms,
                full_text_status=full_text_status,
                full_text_content=full_text_content,
                targeted_area=area,
            ),
            encoding="utf-8",
        )
        new_papers.append(paper)

    if new_papers:
        with paths["seen"].open("a", encoding="utf-8") as handle:
            for paper in new_papers:
                handle.write(str(paper["id"]) + "\n")
        append_overview(paths["overview"], new_papers)

    print(
        f"[collect-papers] targeted area={area} topic={topic_slug} terms={len(terms)} "
        f"candidates={len(papers)} recent={len(recent_papers)} new={len(new_papers)}"
    )
    return len(new_papers)


def main() -> int:
    parser = argparse.ArgumentParser(description="Collect topic-driven paper metadata for Research Radar.")
    parser.add_argument("--topic", dest="topic_slugs", action="append", default=[], help="Limit collection to one or more topic slugs.")
    parser.add_argument("--max-results", type=int, default=None, help="Override max results per topic.")
    parser.add_argument("--lookback-hours", type=int, default=24, help="Only keep papers published within the last N hours. Use 0 to disable.")
    parser.add_argument("--dry-run", action="store_true", help="Validate topic parsing without network access.")
    args = parser.parse_args()

    topics = load_topics()
    if args.topic_slugs:
        allowed = set(args.topic_slugs)
        topics = [topic for topic in topics if topic["slug"] in allowed]

    if not topics:
        print("[collect-papers] no topics matched the current selection", file=sys.stderr)
        return 1

    max_results = args.max_results or load_max_results()
    total = 0
    failures = 0
    soft_failures = 0
    for topic in topics:
        try:
            total += run_topic(topic, max_results=max_results, lookback_hours=args.lookback_hours, dry_run=args.dry_run)
        except (ArxivRateLimitError, ArxivTransientError) as exc:  # pragma: no cover
            soft_failures += 1
            print(f"[collect-papers] topic={topic['slug']} transient-skip: {exc}", file=sys.stderr)
        except Exception as exc:  # pragma: no cover
            failures += 1
            print(f"[collect-papers] topic={topic['slug']} failed: {exc}", file=sys.stderr)

    # --- Targeted search terms (in addition to topic-based searches) ---
    targeted_areas = load_targeted_terms()
    targeted_total = 0
    targeted_failures = 0
    targeted_soft_failures = 0

    if targeted_areas:
        print(f"[collect-papers] running {len(targeted_areas)} targeted research area(s)")
        for area_entry in targeted_areas:
            area = str(area_entry.get("area", ""))
            terms = [str(t) for t in area_entry.get("terms", []) if str(t).strip()]
            if not area or not terms:
                continue
            try:
                targeted_total += run_targeted_area(
                    area, terms, max_results=max_results, lookback_hours=args.lookback_hours, dry_run=args.dry_run
                )
            except (ArxivRateLimitError, ArxivTransientError) as exc:
                targeted_soft_failures += 1
                print(f"[collect-papers] targeted area={area} transient-skip: {exc}", file=sys.stderr)
            except Exception as exc:
                targeted_failures += 1
                print(f"[collect-papers] targeted area={area} failed: {exc}", file=sys.stderr)

    all_failures = failures + targeted_failures
    all_soft_failures = soft_failures + targeted_soft_failures
    total_units = len(topics) + len(targeted_areas)
    print(
        f"[collect-papers] completed topics={len(topics)} total_new_papers={total} failures={failures} transient_skips={soft_failures}"
    )
    if targeted_areas:
        print(
            f"[collect-papers] targeted areas={len(targeted_areas)} targeted_new_papers={targeted_total} "
            f"targeted_failures={targeted_failures} targeted_transient_skips={targeted_soft_failures}"
        )

    # Promote chronic transient-skip rates to a real failure so the
    # nightly wrapper actually notices when arXiv throttles us into the
    # ground. Threshold: more than a quarter of all topics+areas dropped.
    soft_failure_threshold = max(1, total_units // 4)
    if all_soft_failures > soft_failure_threshold:
        print(
            f"[collect-papers] FAIL: {all_soft_failures} transient skips exceeds "
            f"threshold {soft_failure_threshold} ({total_units // 4} = total/4); "
            f"escalating to hard failure",
            file=sys.stderr,
        )
        return 1
    return 1 if all_failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
