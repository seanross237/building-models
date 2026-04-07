#!/usr/bin/env python3
"""Build a simple local HTML view for MX1 loop manifests."""

from __future__ import annotations

import argparse
import html
import json
from pathlib import Path
import sys
from typing import Any


THIS_DIR = Path(__file__).resolve().parent
REPO_ROOT = THIS_DIR.parents[2]
GRADING_DIR = REPO_ROOT / "data-system" / "grading"
if str(GRADING_DIR) not in sys.path:
    sys.path.insert(0, str(GRADING_DIR))

from mx1_loop_v1 import build_loop_id, build_loop_manifest_path  # noqa: E402


DEFAULT_BENCHMARK = GRADING_DIR / "benchmarks" / "mx1-three-question-v1.json"
DEFAULT_LOOPS_ROOT = GRADING_DIR / "mx1-loops"
DEFAULT_OUTPUT = THIS_DIR / "index.html"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Build the MX1 results page.")
    parser.add_argument("--benchmark-file", default=str(DEFAULT_BENCHMARK))
    parser.add_argument("--loops-root", default=str(DEFAULT_LOOPS_ROOT))
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT))
    parser.add_argument("--loop-label")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    build_results_page(
        benchmark_path=Path(args.benchmark_file).resolve(),
        loops_root=Path(args.loops_root).resolve(),
        output_path=Path(args.output).resolve(),
        loop_label=args.loop_label,
    )
    print(f"output={Path(args.output).resolve()}")
    return 0


def build_results_page(
    *,
    benchmark_path: Path,
    loops_root: Path,
    output_path: Path,
    loop_label: str | None = None,
) -> Path:
    benchmark = json.loads(benchmark_path.read_text(encoding="utf-8"))
    benchmark_id = str(benchmark.get("benchmark_id") or "mx1-benchmark")
    resolved_loop_label = str(loop_label or benchmark_id)
    families = [str(item) for item in list(benchmark.get("families") or [])]

    rows: list[dict[str, Any]] = []
    for question_entry in list(benchmark.get("questions") or []):
        question_id = str(question_entry.get("question_id") or "")
        for family in families:
            manifest_path = build_loop_manifest_path(
                question_id=question_id,
                family=family,
                loop_id=build_loop_id(question_id, family, resolved_loop_label),
                loops_root=loops_root,
            )
            if not manifest_path.exists():
                rows.append(
                    {
                        "question_id": question_id,
                        "family": family,
                        "status": "missing",
                    }
                )
                continue
            try:
                manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            except json.JSONDecodeError as exc:
                rows.append(
                    {
                        "question_id": question_id,
                        "family": family,
                        "status": "invalid_manifest",
                        "manifest_path": str(manifest_path),
                        "parse_error": str(exc),
                        "current_prompt_text": "",
                    }
                )
                continue
            best_attempt = manifest.get("best_attempt") or {}
            summary = manifest.get("history_summary") or {}
            rows.append(
                {
                    "question_id": question_id,
                    "question_title": manifest.get("question_title"),
                    "family": family,
                    "status": manifest.get("status"),
                    "manifest_path": str(manifest_path),
                    "iterations_completed": summary.get("iterations_completed"),
                    "best_score": summary.get("best_score"),
                    "best_iteration_index": summary.get("best_iteration_index"),
                    "best_run_id": summary.get("best_run_id"),
                    "best_grading_record_path": best_attempt.get("grading_record_path"),
                    "best_tutor_record_path": best_attempt.get("tutor_record_path"),
                    "best_total_tokens": best_attempt.get("total_tokens"),
                    "best_total_wall_time_ms": best_attempt.get("total_wall_time_ms"),
                    "best_total_cost_usd": best_attempt.get("total_cost_usd"),
                    "current_prompt_text": manifest.get("current_prompt_text"),
                    "starter_prompt_text": manifest.get("starter_prompt_text"),
                }
            )

    html_text = _render_page(benchmark_id=benchmark_id, rows=rows, benchmark=benchmark)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(html_text, encoding="utf-8")
    return output_path


def _render_page(*, benchmark_id: str, rows: list[dict[str, Any]], benchmark: dict[str, Any]) -> str:
    body_rows = []
    for row in rows:
        manifest_link = _link(row.get("manifest_path"), "manifest")
        grading_link = _link(row.get("best_grading_record_path"), "best grading")
        tutor_link = _link(row.get("best_tutor_record_path"), "best tutor")
        body_rows.append(
            "<tr>"
            f"<td>{html.escape(str(row.get('question_id') or ''))}</td>"
            f"<td>{html.escape(str(row.get('family') or ''))}</td>"
            f"<td>{html.escape(str(row.get('status') or ''))}</td>"
            f"<td>{html.escape(str(row.get('iterations_completed') or ''))}</td>"
            f"<td>{html.escape(str(row.get('best_score') or ''))}</td>"
            f"<td>{html.escape(str(row.get('best_iteration_index') or ''))}</td>"
            f"<td>{html.escape(str(row.get('best_total_tokens') or ''))}</td>"
            f"<td>{html.escape(str(row.get('best_total_wall_time_ms') or ''))}</td>"
            f"<td>{html.escape(str(row.get('best_total_cost_usd') or ''))}</td>"
            f"<td>{manifest_link} {grading_link} {tutor_link}</td>"
            f"<td><pre>{html.escape(str(row.get('current_prompt_text') or ''))}</pre></td>"
            "</tr>"
        )

    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>MX1 Results</title>
  <style>
    :root {{
      --bg: #0b1020;
      --panel: #121a30;
      --ink: #edf2ff;
      --muted: #9fb0d8;
      --line: #243252;
      --accent: #9dd8ff;
    }}
    body {{
      margin: 0;
      font-family: ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      background: radial-gradient(circle at top, #182446 0%, var(--bg) 50%);
      color: var(--ink);
    }}
    main {{
      max-width: 1440px;
      margin: 0 auto;
      padding: 32px 24px 60px;
    }}
    .card {{
      background: rgba(18, 26, 48, 0.88);
      border: 1px solid var(--line);
      border-radius: 18px;
      padding: 20px;
      margin-bottom: 20px;
      box-shadow: 0 10px 40px rgba(0, 0, 0, 0.25);
    }}
    h1 {{
      font-size: 42px;
      margin: 0 0 10px;
      line-height: 1.05;
    }}
    p, li {{
      color: var(--muted);
      line-height: 1.5;
    }}
    table {{
      width: 100%;
      border-collapse: collapse;
      font-size: 14px;
    }}
    th, td {{
      border-top: 1px solid var(--line);
      padding: 10px 8px;
      vertical-align: top;
      text-align: left;
    }}
    th {{
      color: var(--muted);
      font-size: 12px;
      text-transform: uppercase;
      letter-spacing: 0.08em;
    }}
    a {{
      color: var(--accent);
      text-decoration: none;
      margin-right: 10px;
    }}
    pre {{
      white-space: pre-wrap;
      word-break: break-word;
      margin: 0;
      font-family: ui-monospace, SFMono-Regular, Menlo, monospace;
      font-size: 12px;
      color: var(--ink);
    }}
  </style>
</head>
<body>
  <main>
    <section class="card">
      <p>Mission Exploration 1</p>
      <h1>MX1 Results for {html.escape(benchmark_id)}</h1>
      <p>{html.escape(str(benchmark.get("selection_notes") or ""))}</p>
      <p>Questions: {html.escape(", ".join(str(item.get("question_id")) for item in benchmark.get("questions") or []))}</p>
      <p>Families: {html.escape(", ".join(str(item) for item in benchmark.get("families") or []))}</p>
    </section>
    <section class="card">
      <table>
        <thead>
          <tr>
            <th>Question</th>
            <th>Family</th>
            <th>Status</th>
            <th>Iterations</th>
            <th>Best Score</th>
            <th>Best Iter</th>
            <th>Tokens</th>
            <th>Wall ms</th>
            <th>Cost</th>
            <th>Artifacts</th>
            <th>Current Prompt</th>
          </tr>
        </thead>
        <tbody>
          {''.join(body_rows)}
        </tbody>
      </table>
    </section>
  </main>
</body>
</html>
"""


def _link(path: object, label: str) -> str:
    value = str(path or "").strip()
    if not value:
        return ""
    resolved = Path(value).resolve()
    return f'<a href="file://{html.escape(str(resolved))}">{html.escape(label)}</a>'


if __name__ == "__main__":
    raise SystemExit(main())
