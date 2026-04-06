#!/usr/bin/env python3
"""Build the prompt-family experiment results page from grading and run-history artifacts."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from statistics import mean
from typing import Any, Dict, Iterable, List, Optional


REPO_ROOT = Path(__file__).resolve().parents[3]
DEFAULT_SUMMARY = REPO_ROOT / "data-system" / "grading" / "runs" / "live-batch-v1-summary.json"
OUTPUT_DIR = Path(__file__).resolve().parent
OUTPUT_JSON = OUTPUT_DIR / "results.json"
OUTPUT_HTML = OUTPUT_DIR / "index.html"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build the prompt-family experiment results page.")
    parser.add_argument(
        "--summary",
        type=Path,
        default=DEFAULT_SUMMARY,
        help="Path to a grading batch summary JSON.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=OUTPUT_DIR,
        help="Directory where results.json and index.html should be written.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    summary = load_json(args.summary)
    source_rows, source_meta = extract_source_rows(summary)
    rows = [build_row(item) for item in source_rows]
    payload = build_payload(summary, args.summary, rows, source_meta)

    args.output_dir.mkdir(parents=True, exist_ok=True)
    (args.output_dir / "results.json").write_text(json.dumps(payload, indent=2), encoding="utf-8")
    (args.output_dir / "index.html").write_text(render_html(payload), encoding="utf-8")

    print(f"wrote {args.output_dir / 'results.json'}")
    print(f"wrote {args.output_dir / 'index.html'}")
    print(f"rows={len(rows)}")
    return 0


def load_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def maybe_load_json(path: Path) -> Dict[str, Any]:
    if not path.exists():
        return {}
    return load_json(path)


def extract_source_rows(summary: Dict[str, Any]) -> tuple[List[Dict[str, Any]], Dict[str, Any]]:
    if isinstance(summary.get("results"), list):
        return list(summary.get("results") or []), {
            "source_kind": "batch_summary",
            "experiment_run_id": "",
            "benchmark_id": "",
            "benchmark_title": "",
        }

    if isinstance(summary.get("question_results"), list) and isinstance(summary.get("variants"), dict):
        rows: List[Dict[str, Any]] = []
        variants = dict(summary.get("variants") or {})
        benchmark = dict(summary.get("benchmark") or {})
        for question_result in summary.get("question_results") or []:
            if not isinstance(question_result, dict):
                continue
            for variant_id, variant_config in variants.items():
                grading_record = question_result.get(variant_id)
                if not isinstance(grading_record, dict):
                    continue
                row = {
                    "grading_record": grading_record.get("grading_record_path"),
                    "variant_id": variant_id,
                    "variant_title": (variant_config or {}).get("title") or variant_id,
                    "prompt_family": (variant_config or {}).get("prompt_family"),
                    "selected_prompt_text": (variant_config or {}).get("selected_prompt_text"),
                    "base_header_prompt": (variant_config or {}).get("base_header_prompt"),
                    "child_prompt_family": (variant_config or {}).get("child_prompt_family"),
                    "child_selected_prompt_text": (variant_config or {}).get("child_selected_prompt_text"),
                    "child_base_header_prompt": (variant_config or {}).get("child_base_header_prompt"),
                    "question_id": question_result.get("question_id"),
                    "question_file": question_result.get("question_file"),
                    "domain": question_result.get("domain"),
                    "why_included": question_result.get("why_included"),
                    "experiment_run_id": summary.get("experiment_run_id"),
                    "benchmark_id": benchmark.get("benchmark_id"),
                    "benchmark_title": benchmark.get("title"),
                }
                rows.append(row)
        return rows, {
            "source_kind": "prompt_family_experiment",
            "experiment_run_id": str(summary.get("experiment_run_id") or ""),
            "benchmark_id": str(benchmark.get("benchmark_id") or ""),
            "benchmark_title": str(benchmark.get("title") or ""),
        }

    raise ValueError("Unsupported summary schema for prompt-family results page.")


def build_row(summary_row: Dict[str, Any]) -> Dict[str, Any]:
    grading_record_path = Path(str(summary_row["grading_record"]))
    grading_record = load_json(grading_record_path)
    run_dir = Path(str(grading_record["run_dir"]))
    review_record_path_value = grading_record.get("tutor_record_path") or grading_record.get("review_record_path")
    review_record = maybe_load_json(Path(str(review_record_path_value))) if review_record_path_value else {}

    run_summary = maybe_load_json(run_dir / "run_summary.json")
    run_packet = maybe_load_json(run_dir / "run_packet.json")
    node_record = maybe_load_json(run_dir / "nodes" / "node_root" / "node_record.json")
    prompt_snapshot = maybe_load_json(run_dir / "replay" / "node_root" / "prompt-snapshot.json")
    raw_model = maybe_load_json(run_dir / "replay" / "node_root" / "raw-model.json")

    run_level_variables = dict(run_packet.get("run_level_variables") or {})
    node_variables = dict(node_record.get("variables") or {})
    resolved_variables = merge_dicts(run_level_variables, node_variables)

    results = node_record.get("results") or []
    node_result_text = first_result_text(results)

    prompt_rendered_text = ""
    prompt_refs = []
    if isinstance(node_record.get("prompt"), dict):
        prompt_rendered_text = str(node_record["prompt"].get("rendered_prompt_text") or "")
        prompt_refs = list(node_record["prompt"].get("prompt_artifact_refs") or [])

    prompt_family = str(resolved_variables.get("prompt_family") or summary_row.get("prompt_family") or "legacy")
    selected_prompt_text = str(
        resolved_variables.get("selected_prompt_text")
        or summary_row.get("selected_prompt_text")
        or ""
    )
    base_header_prompt = str(
        resolved_variables.get("base_header_prompt")
        or summary_row.get("base_header_prompt")
        or ""
    )
    child_prompt_family = str(resolved_variables.get("child_prompt_family") or summary_row.get("child_prompt_family") or "")
    child_selected_prompt_text = str(
        resolved_variables.get("child_selected_prompt_text")
        or summary_row.get("child_selected_prompt_text")
        or ""
    )
    child_base_header_prompt = str(
        resolved_variables.get("child_base_header_prompt")
        or summary_row.get("child_base_header_prompt")
        or ""
    )

    row = {
        "question_id": grading_record.get("question_id"),
        "title": grading_record.get("title"),
        "question_file": grading_record.get("question_file"),
        "label": grading_record.get("label"),
        "variant_id": str(summary_row.get("variant_id") or ""),
        "variant_title": str(summary_row.get("variant_title") or ""),
        "domain": str(summary_row.get("domain") or ""),
        "why_included": str(summary_row.get("why_included") or ""),
        "experiment_run_id": str(summary_row.get("experiment_run_id") or ""),
        "benchmark_id": str(summary_row.get("benchmark_id") or ""),
        "benchmark_title": str(summary_row.get("benchmark_title") or ""),
        "run_id": grading_record.get("run_id"),
        "run_dir": str(run_dir),
        "runtime_provider": grading_record.get("runtime_provider"),
        "model": grading_record.get("model"),
        "node_count": coerce_int(grading_record.get("node_count") or run_summary.get("node_count")),
        "validation_status": grading_record.get("validation_status"),
        "validation_summary": grading_record.get("validation_summary") or {},
        "grading_status": grading_record.get("grading", {}).get("grading_status") or grading_record.get("grading_status"),
        "correct": coerce_bool(grading_record.get("grading", {}).get("correct") or grading_record.get("correct")),
        "score": coerce_float(grading_record.get("grading", {}).get("score") or grading_record.get("score")),
        "task_text": grading_record.get("task_text") or summary_row.get("task_text"),
        "root_result_excerpt": grading_record.get("root_result_excerpt") or node_result_text,
        "grading": grading_record.get("grading") or {},
        "review_record": review_record,
        "review": review_record.get("review") or grading_record.get("review") or {},
        "node_record": node_record,
        "run_summary": run_summary,
        "run_packet": run_packet,
        "prompt_snapshot": prompt_snapshot,
        "raw_model": raw_model,
        "resolved_variables": resolved_variables,
        "prompt_family": prompt_family,
        "selected_prompt_text": selected_prompt_text,
        "base_header_prompt": base_header_prompt,
        "child_prompt_family": child_prompt_family,
        "child_selected_prompt_text": child_selected_prompt_text,
        "child_base_header_prompt": child_base_header_prompt,
        "injected_prompt_profile": str(resolved_variables.get("injected_prompt_profile") or ""),
        "additional_instruction_prompt_profiles": list(resolved_variables.get("additional_instruction_prompt_profiles") or []),
        "workflow_structure": str(resolved_variables.get("workflow_structure") or ""),
        "verification_policy": str(resolved_variables.get("verification_policy") or ""),
        "routing_policy": str(resolved_variables.get("routing_policy") or ""),
        "recovery_policy": str(resolved_variables.get("recovery_policy") or ""),
        "context_policy": str(resolved_variables.get("context_policy") or ""),
        "tool_policy": str(resolved_variables.get("tool_policy") or ""),
        "budget_policy": resolved_variables.get("budget_policy") or {},
        "prompt_rendered_text": prompt_rendered_text,
        "prompt_artifact_refs": prompt_refs,
        "artifact_paths": build_artifact_paths(
            run_dir,
            grading_record_path,
            Path(str(review_record_path_value)) if review_record_path_value else None,
        ),
    }
    return row


def build_artifact_paths(
    run_dir: Path,
    grading_record_path: Path,
    review_record_path: Path | None,
) -> Dict[str, Optional[str]]:
    paths = {
        "grading_record": grading_record_path,
        "review_record": review_record_path,
        "run_dir": run_dir,
        "run_packet": run_dir / "run_packet.json",
        "run_summary": run_dir / "run_summary.json",
        "node_record": run_dir / "nodes" / "node_root" / "node_record.json",
        "prompt_snapshot": run_dir / "replay" / "node_root" / "prompt-snapshot.json",
        "raw_model": run_dir / "replay" / "node_root" / "raw-model.json",
        "timeline_json": run_dir / "derived" / "timeline.json",
        "timeline_md": run_dir / "derived" / "timeline.md",
        "simple_run_row": run_dir / "derived" / "simple-run-row.json",
        "events": run_dir / "nodes" / "node_root" / "events.jsonl",
        "edges": run_dir / "nodes" / "node_root" / "edges.json",
    }
    return {key: (str(path) if path and path.exists() else None) for key, path in paths.items()}


def build_payload(
    summary: Dict[str, Any],
    summary_path: Path,
    rows: List[Dict[str, Any]],
    source_meta: Dict[str, Any],
) -> Dict[str, Any]:
    by_question: Dict[str, List[Dict[str, Any]]] = {}
    for row in rows:
        by_question.setdefault(str(row.get("question_id") or ""), []).append(row)

    question_groups = []
    for question_id, question_rows in sorted(by_question.items(), key=lambda item: item[0]):
        ordered_rows = sorted(
            question_rows,
            key=lambda row: (
                str(row.get("variant_id") or ""),
                str(row.get("label") or ""),
                str(row.get("run_id") or ""),
            ),
        )
        variant_scores = {
            str(row.get("variant_title") or row.get("variant_id") or row.get("label") or ""): row.get("score", 0.0)
            for row in ordered_rows
        }
        baseline = next(
            (
                row
                for row in ordered_rows
                if str(row.get("variant_id") or "") == "baseline_execute" or str(row.get("label") or "") == "baseline"
            ),
            None,
        )
        comparison = next(
            (
                row
                for row in ordered_rows
                if str(row.get("variant_id") or "") == "transmute_candidate" or str(row.get("label") or "") == "main"
            ),
            None,
        )
        question_groups.append(
            {
                "question_id": question_id,
                "title": ordered_rows[0].get("title"),
                "question_file": ordered_rows[0].get("question_file"),
                "domain": ordered_rows[0].get("domain"),
                "why_included": ordered_rows[0].get("why_included"),
                "rows": ordered_rows,
                "variant_scores": variant_scores,
                "avg_score": round(mean(row.get("score", 0.0) for row in ordered_rows), 3),
                "best_score": max((row.get("score", 0.0) for row in ordered_rows), default=0.0),
                "correct_count": sum(1 for row in ordered_rows if row.get("correct")),
                "run_count": len(ordered_rows),
                "baseline_score": baseline.get("score") if baseline else None,
                "comparison_score": comparison.get("score") if comparison else None,
                "comparison_label": comparison.get("variant_title") or comparison.get("variant_id") or comparison.get("label"),
                "score_delta": round(
                    (comparison.get("score", 0.0) if comparison else 0.0)
                    - (baseline.get("score", 0.0) if baseline else 0.0),
                    3,
                )
                if baseline and comparison
                else None,
            }
        )

    aggregate_score = round(mean(row.get("score", 0.0) for row in rows), 3) if rows else 0.0
    prompt_families = sorted({str(row.get("prompt_family") or "legacy") for row in rows})
    injected_profiles = sorted({str(row.get("injected_prompt_profile") or "") for row in rows if row.get("injected_prompt_profile")})
    workflows = sorted({str(row.get("workflow_structure") or "") for row in rows if row.get("workflow_structure")})
    verification_policies = sorted({str(row.get("verification_policy") or "") for row in rows if row.get("verification_policy")})

    payload = {
        "source_summary": str(summary_path),
        "source_kind": source_meta.get("source_kind") or "unknown",
        "experiment_run_id": source_meta.get("experiment_run_id") or "",
        "benchmark_id": source_meta.get("benchmark_id") or "",
        "benchmark_title": source_meta.get("benchmark_title") or "",
        "runtime_provider": summary.get("runtime_provider"),
        "model": summary.get("model"),
        "rows": rows,
        "question_groups": question_groups,
        "totals": {
            "row_count": len(rows),
            "question_count": len(question_groups),
            "correct_rows": sum(1 for row in rows if row.get("correct")),
            "aggregate_score": aggregate_score,
            "legacy_rows": sum(1 for row in rows if row.get("prompt_family") == "legacy"),
            "prompt_family_rows": sum(1 for row in rows if row.get("prompt_family") != "legacy"),
            "prompt_families": prompt_families,
            "injected_prompt_profiles": injected_profiles,
            "workflow_structures": workflows,
            "verification_policies": verification_policies,
        },
    }
    return payload


def render_html(payload: Dict[str, Any]) -> str:
    embedded = json.dumps(payload, indent=2)
    safe_embedded = embedded.replace("</", "<\\/")
    template = """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Prompt Family Results</title>
  <style>
    :root {{
      --bg: #0a1020;
      --panel: rgba(15, 23, 42, 0.84);
      --panel-soft: rgba(17, 24, 39, 0.68);
      --line: rgba(148, 163, 184, 0.2);
      --text: #e7eefb;
      --muted: #9daec5;
      --accent: #f8b24d;
      --accent-soft: rgba(248, 178, 77, 0.12);
      --good: #52e0a6;
      --bad: #ff7b8e;
      --mono: "IBM Plex Mono", "SFMono-Regular", Consolas, monospace;
      --sans: "Avenir Next", "Segoe UI", "Trebuchet MS", system-ui, sans-serif;
    }}
    * {{ box-sizing: border-box; }}
    html {{ scroll-behavior: smooth; }}
    body {{
      margin: 0;
      color: var(--text);
      font-family: var(--sans);
      background:
        radial-gradient(circle at top left, rgba(248, 178, 77, 0.16), transparent 26%),
        radial-gradient(circle at top right, rgba(59, 130, 246, 0.12), transparent 24%),
        linear-gradient(180deg, #07111e 0%, #0b1322 55%, #07111e 100%);
      min-height: 100vh;
    }}
    .wrap {{
      max-width: 1520px;
      margin: 0 auto;
      padding: 28px 20px 60px;
    }}
    .hero {{
      position: relative;
      overflow: hidden;
      padding: 28px;
      border: 1px solid var(--line);
      border-radius: 26px;
      background: linear-gradient(180deg, rgba(15, 23, 42, 0.95), rgba(15, 23, 42, 0.72));
      box-shadow: 0 30px 90px rgba(0, 0, 0, 0.32);
    }}
    .hero::after {{
      content: "";
      position: absolute;
      right: -80px;
      top: -60px;
      width: 260px;
      height: 260px;
      border-radius: 50%;
      background: radial-gradient(circle, rgba(248, 178, 77, 0.2), transparent 68%);
      pointer-events: none;
    }}
    .kicker {{
      text-transform: uppercase;
      letter-spacing: 0.18em;
      font-size: 11px;
      color: var(--muted);
      margin-bottom: 8px;
    }}
    h1 {{
      margin: 0 0 10px;
      font-size: clamp(34px, 4vw, 56px);
      line-height: 1.02;
      letter-spacing: -0.05em;
      max-width: 980px;
    }}
    .subtitle {{
      color: var(--muted);
      line-height: 1.7;
      font-size: 15px;
      max-width: 1040px;
      margin: 0;
    }}
    .chips {{
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
      margin-top: 18px;
    }}
    .chip {{
      display: inline-flex;
      align-items: center;
      gap: 8px;
      padding: 8px 12px;
      border-radius: 999px;
      border: 1px solid var(--line);
      background: rgba(255, 255, 255, 0.04);
      color: var(--text);
      font-size: 12px;
    }}
    .chip b {{
      font-family: var(--mono);
      color: white;
      font-weight: 700;
    }}
    .grid {{
      display: grid;
      grid-template-columns: repeat(6, minmax(0, 1fr));
      gap: 14px;
      margin: 18px 0 26px;
    }}
    .stat {{
      border: 1px solid var(--line);
      border-radius: 20px;
      background: var(--panel);
      padding: 16px;
      min-height: 110px;
    }}
    .stat .label {{
      color: var(--muted);
      font-size: 11px;
      text-transform: uppercase;
      letter-spacing: 0.15em;
    }}
    .stat .value {{
      margin-top: 10px;
      font-size: 30px;
      font-weight: 700;
      letter-spacing: -0.05em;
    }}
    .stat .foot {{
      margin-top: 8px;
      color: var(--muted);
      font-size: 12px;
      line-height: 1.45;
    }}
    .section {{
      margin-top: 22px;
      border: 1px solid var(--line);
      border-radius: 24px;
      overflow: hidden;
      background: var(--panel);
    }}
    .section-head {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      gap: 12px;
      padding: 18px 20px;
      border-bottom: 1px solid var(--line);
      background: rgba(255, 255, 255, 0.02);
    }}
    .section-head h2 {{
      margin: 0;
      font-size: 18px;
      letter-spacing: -0.02em;
    }}
    .section-head .meta {{
      color: var(--muted);
      font-family: var(--mono);
      font-size: 12px;
    }}
    .table-wrap {{
      overflow: auto;
    }}
    table {{
      width: 100%;
      border-collapse: collapse;
      min-width: 1350px;
    }}
    th, td {{
      padding: 14px 16px;
      border-bottom: 1px solid rgba(148, 163, 184, 0.14);
      vertical-align: top;
      text-align: left;
    }}
    th {{
      position: sticky;
      top: 0;
      z-index: 1;
      background: rgba(8, 14, 28, 0.96);
      color: #c9d5e7;
      font-size: 11px;
      text-transform: uppercase;
      letter-spacing: 0.13em;
    }}
    tr:hover td {{
      background: rgba(255, 255, 255, 0.015);
    }}
    .title {{
      font-weight: 700;
      line-height: 1.3;
      margin-bottom: 4px;
    }}
    .tiny {{
      font-size: 12px;
      color: var(--muted);
      line-height: 1.45;
      word-break: break-word;
    }}
    .mono {{
      font-family: var(--mono);
      font-size: 12px;
      word-break: break-word;
    }}
    .score {{
      display: inline-flex;
      align-items: center;
      justify-content: center;
      min-width: 56px;
      padding: 6px 10px;
      border-radius: 999px;
      font-family: var(--mono);
      font-weight: 700;
      background: var(--accent-soft);
      color: #ffd58c;
    }}
    .score.good {{
      background: rgba(82, 224, 166, 0.12);
      color: #90f0c7;
    }}
    .score.bad {{
      background: rgba(255, 123, 142, 0.12);
      color: #ffafbb;
    }}
    .pill {{
      display: inline-flex;
      align-items: center;
      gap: 6px;
      padding: 6px 10px;
      border-radius: 999px;
      border: 1px solid var(--line);
      background: rgba(255, 255, 255, 0.03);
      font-size: 12px;
      margin: 0 6px 6px 0;
    }}
    .pill b {{
      color: white;
      font-family: var(--mono);
      font-weight: 700;
    }}
    .pill-row {{
      display: flex;
      flex-wrap: wrap;
      gap: 6px;
    }}
    .links {{
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
    }}
    a.link {{
      display: inline-flex;
      align-items: center;
      gap: 6px;
      padding: 7px 10px;
      border-radius: 999px;
      border: 1px solid var(--line);
      background: rgba(255, 255, 255, 0.03);
      color: #ffd58c;
      text-decoration: none;
      font-size: 12px;
      white-space: nowrap;
    }}
    a.link:hover {{ text-decoration: underline; }}
    details {{
      border-top: 1px solid rgba(148, 163, 184, 0.16);
      background: rgba(2, 6, 23, 0.22);
    }}
    summary {{
      cursor: pointer;
      list-style: none;
      padding: 14px 16px;
      font-weight: 700;
    }}
    summary::-webkit-details-marker {{ display: none; }}
    .detail-grid {{
      display: grid;
      grid-template-columns: repeat(3, minmax(0, 1fr));
      gap: 14px;
      padding: 0 16px 16px;
    }}
    .card {{
      border: 1px solid rgba(148, 163, 184, 0.14);
      border-radius: 18px;
      background: rgba(15, 23, 42, 0.62);
      padding: 14px;
    }}
    .card h3 {{
      margin: 0 0 10px;
      font-size: 14px;
    }}
    pre {{
      margin: 0;
      white-space: pre-wrap;
      word-break: break-word;
      font-family: var(--mono);
      font-size: 12px;
      line-height: 1.55;
      color: #d5dfef;
    }}
    .question-block {{
      display: grid;
      grid-template-columns: 1.05fr 0.95fr;
      gap: 14px;
      padding: 16px;
      border-top: 1px solid rgba(148, 163, 184, 0.12);
    }}
    .matrix {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
      gap: 10px;
    }}
    .matrix .cell {{
      border: 1px solid rgba(148, 163, 184, 0.14);
      border-radius: 14px;
      padding: 10px 12px;
      background: rgba(255, 255, 255, 0.03);
    }}
    .matrix .cell .name {{
      color: var(--muted);
      font-size: 11px;
      text-transform: uppercase;
      letter-spacing: 0.14em;
    }}
    .matrix .cell .val {{
      margin-top: 6px;
      font-family: var(--mono);
      font-size: 12px;
      line-height: 1.45;
      word-break: break-word;
    }}
    @media (max-width: 1200px) {{
      .grid {{ grid-template-columns: repeat(3, minmax(0, 1fr)); }}
      .detail-grid, .question-block {{ grid-template-columns: 1fr; }}
    }}
    @media (max-width: 760px) {{
      .wrap {{ padding: 14px; }}
      .hero {{ padding: 20px; border-radius: 20px; }}
      .grid {{ grid-template-columns: repeat(2, minmax(0, 1fr)); }}
    }}
  </style>
</head>
<body>
  <div class="wrap">
    <section class="hero">
      <div class="kicker">Prompt-family experiment loop</div>
      <h1>Results page for prompt-family experiments</h1>
      <p class="subtitle">
        This dashboard is built from preserved grading rows and run-history truth. It shows the selected variables for each run,
        the prompt render that reached the node, the score, the validation state, and direct file links back to the source
        grading and runtime artifacts.
      </p>
      <div class="chips" id="hero-chips"></div>
    </section>

    <section class="grid" id="stats"></section>

    <section class="section">
      <div class="section-head">
        <h2>Experiment Rows</h2>
        <div class="meta" id="row-meta"></div>
      </div>
      <div class="table-wrap">
        <table>
          <thead>
            <tr>
              <th>Question</th>
              <th>Label</th>
              <th>Score</th>
              <th>Prompt Family</th>
              <th>Resolved Variables</th>
              <th>Artifacts</th>
            </tr>
          </thead>
          <tbody id="rows"></tbody>
        </table>
      </div>
    </section>

    <section class="section">
      <div class="section-head">
        <h2>Per-Question Summary</h2>
        <div class="meta" id="question-meta"></div>
      </div>
      <div id="question-groups"></div>
    </section>
  </div>

  <script id="results-data" type="application/json">__RESULTS_DATA__</script>
  <script>
    const data = JSON.parse(document.getElementById('results-data').textContent);
    const rows = data.rows || [];
    const groups = data.question_groups || [];

    const chipItems = [
      ['Source summary', data.source_summary],
      ['Source kind', data.source_kind || 'unknown'],
      ['Runtime', `${data.runtime_provider} / ${data.model}`],
      ['Rows', String(data.totals.row_count)],
      ['Questions', String(data.totals.question_count)],
      ['Aggregate score', String(data.totals.aggregate_score)],
      ['Prompt-family rows', String(data.totals.prompt_family_rows)]
    ];
    document.getElementById('hero-chips').innerHTML = chipItems.map(([label, value]) => `
      <span class="chip"><b>${escapeHtml(label)}</b> ${escapeHtml(value)}</span>
    `).join('');

    const stats = [
      {label: 'Rows', value: data.totals.row_count, foot: 'all experiment rows included in the dashboard'},
      {label: 'Questions', value: data.totals.question_count, foot: 'unique question ids represented here'},
      {label: 'Aggregate Score', value: data.totals.aggregate_score, foot: 'mean score across all rows'},
      {label: 'Correct Rows', value: data.totals.correct_rows, foot: 'rows marked correct by grading'},
      {label: 'Legacy Rows', value: data.totals.legacy_rows, foot: 'rows without prompt-family metadata yet'},
      {label: 'Prompt Families', value: (data.totals.prompt_families || []).join(', ') || 'none', foot: 'families observed in the source rows'},
    ];
    document.getElementById('stats').innerHTML = stats.map(item => `
      <div class="stat">
        <div class="label">${escapeHtml(item.label)}</div>
        <div class="value">${escapeHtml(String(item.value))}</div>
        <div class="foot">${escapeHtml(item.foot)}</div>
      </div>
    `).join('');

    document.getElementById('row-meta').textContent = `${rows.length} rows from ${data.source_summary}`;
    document.getElementById('question-meta').textContent = `${groups.length} question groups`;

    document.getElementById('rows').innerHTML = rows.map(row => `
      <tr>
        <td>
          <div class="title">${escapeHtml(row.title || row.question_id || '')}</div>
          <div class="tiny">${escapeHtml(row.question_id || '')}</div>
          <div class="tiny">${escapeHtml(row.domain || '')}</div>
          <div class="tiny">${escapeHtml(row.task_text || '')}</div>
          <div class="tiny" style="margin-top:8px;">${escapeHtml(row.root_result_excerpt || '')}</div>
        </td>
        <td>
          ${row.variant_title ? `<span class="pill"><b>variant</b> ${escapeHtml(row.variant_title)}</span>` : ''}
          <span class="pill">${escapeHtml(row.label || '')}</span>
          <div class="tiny">${escapeHtml(row.validation_status || '')}</div>
          <div class="tiny">${escapeHtml(row.grading_status || '')}</div>
        </td>
        <td>
          <span class="score ${row.correct ? 'good' : 'bad'}">${escapeHtml(String(row.score))}</span>
          <div class="tiny" style="margin-top:8px;">${row.correct ? 'correct' : 'incorrect'}</div>
          <div class="tiny">nodes: ${escapeHtml(String(row.node_count || ''))}</div>
        </td>
        <td>
          <div class="pill-row">
            <span class="pill"><b>family</b> ${escapeHtml(row.prompt_family || 'legacy')}</span>
            <span class="pill"><b>injected</b> ${escapeHtml(row.injected_prompt_profile || 'n/a')}</span>
            <span class="pill"><b>workflow</b> ${escapeHtml(row.workflow_structure || 'n/a')}</span>
            <span class="pill"><b>verify</b> ${escapeHtml(row.verification_policy || 'n/a')}</span>
          </div>
          <div class="tiny" style="margin-top:8px;">child: ${escapeHtml(row.child_prompt_family || 'n/a')}</div>
        </td>
        <td>
          <details>
            <summary>view selected variables</summary>
            <div class="detail-grid">
              <div class="card">
                <h3>Resolved variables</h3>
                <pre>${escapeHtml(JSON.stringify(row.resolved_variables || {}, null, 2))}</pre>
              </div>
              <div class="card">
                <h3>Prompt selection</h3>
                <pre>${escapeHtml(JSON.stringify({
                  prompt_family: row.prompt_family,
                  selected_prompt_text: row.selected_prompt_text,
                  base_header_prompt: row.base_header_prompt,
                  review_prompt_family: row.resolved_variables?.review_prompt_family,
                  review_selected_prompt_text: row.resolved_variables?.review_selected_prompt_text,
                  review_base_header_prompt: row.resolved_variables?.review_base_header_prompt,
                  child_prompt_family: row.child_prompt_family,
                  child_selected_prompt_text: row.child_selected_prompt_text,
                  child_base_header_prompt: row.child_base_header_prompt,
                  injected_prompt_profile: row.injected_prompt_profile,
                  additional_instruction_prompt_profiles: row.additional_instruction_prompt_profiles,
                  workflow_structure: row.workflow_structure,
                  verification_policy: row.verification_policy,
                  routing_policy: row.routing_policy,
                  recovery_policy: row.recovery_policy,
                  budget_policy: row.budget_policy
                }, null, 2))}</pre>
              </div>
              <div class="card">
                <h3>Prompt render excerpt</h3>
                <pre>${escapeHtml(JSON.stringify({
                  initial_prompt: row.prompt_snapshot?.initial_prompt,
                  final_prompt: row.prompt_snapshot?.final_prompt,
                  rendered_prompt_text: row.prompt_rendered_text,
                  prompt_artifact_refs: row.prompt_artifact_refs,
                  node_state: row.node_record?.state,
                  final_action_type: row.node_record?.final_action_type
                }, null, 2))}</pre>
              </div>
            </div>
          </details>
        </td>
        <td>
          <div class="links">
            ${artifactLink('run dir', row.artifact_paths?.run_dir)}
            ${artifactLink('grading', row.artifact_paths?.grading_record)}
            ${artifactLink('run packet', row.artifact_paths?.run_packet)}
            ${artifactLink('run summary', row.artifact_paths?.run_summary)}
            ${artifactLink('node record', row.artifact_paths?.node_record)}
            ${artifactLink('prompt snapshot', row.artifact_paths?.prompt_snapshot)}
            ${artifactLink('raw model', row.artifact_paths?.raw_model)}
            ${artifactLink('timeline.md', row.artifact_paths?.timeline_md)}
          </div>
        </td>
      </tr>
    `).join('');

    document.getElementById('question-groups').innerHTML = groups.map(group => {
      const variants = Object.entries(group.variant_scores || {});
      return `
        <details open>
          <summary>
            ${escapeHtml(group.title || group.question_id || '')}
            <span class="tiny"> - ${escapeHtml(String(group.run_count))} rows, avg ${escapeHtml(String(group.avg_score))}</span>
          </summary>
          <div class="question-block">
            <div class="card">
              <h3>Question</h3>
              <pre>${escapeHtml(group.rows?.[0]?.task_text || '')}</pre>
            </div>
            <div class="card">
              <h3>Group summary</h3>
              <div class="matrix">
                <div class="cell"><div class="name">question id</div><div class="val">${escapeHtml(group.question_id || '')}</div></div>
                <div class="cell"><div class="name">domain</div><div class="val">${escapeHtml(group.domain || 'n/a')}</div></div>
                <div class="cell"><div class="name">average score</div><div class="val">${escapeHtml(String(group.avg_score))}</div></div>
                <div class="cell"><div class="name">best score</div><div class="val">${escapeHtml(String(group.best_score))}</div></div>
                <div class="cell"><div class="name">correct rows</div><div class="val">${escapeHtml(String(group.correct_count))}</div></div>
                <div class="cell"><div class="name">baseline</div><div class="val">${escapeHtml(group.baseline_score == null ? 'n/a' : String(group.baseline_score))}</div></div>
                <div class="cell"><div class="name">${escapeHtml(group.comparison_label || 'comparison')}</div><div class="val">${escapeHtml(group.comparison_score == null ? 'n/a' : String(group.comparison_score))}</div></div>
                <div class="cell"><div class="name">delta (comparison - baseline)</div><div class="val">${escapeHtml(group.score_delta == null ? 'n/a' : String(group.score_delta))}</div></div>
                <div class="cell"><div class="name">why included</div><div class="val">${escapeHtml(group.why_included || 'n/a')}</div></div>
                <div class="cell"><div class="name">variants</div><div class="val">${escapeHtml(variants.map(([label, score]) => `${label}: ${score}`).join(' | ') || 'n/a')}</div></div>
              </div>
            </div>
          </div>
        </details>
      `;
    }).join('');

    function artifactLink(label, path) {{
      if (!path) return '';
      const href = fileUrl(path);
      return `<a class="link" href="${href}">${escapeHtml(label)}</a>`;
    }}

    function fileUrl(path) {{
      const normalized = String(path).replace(/#/g, '%23');
      return `file://${encodeURI(normalized)}`;
    }}

    function escapeHtml(text) {{
      return String(text)
        .replaceAll('&', '&amp;')
        .replaceAll('<', '&lt;')
        .replaceAll('>', '&gt;')
        .replaceAll('"', '&quot;')
        .replaceAll("'", '&#39;');
    }}
  </script>
</body>
</html>
"""
    return template.replace("__RESULTS_DATA__", safe_embedded).replace("{{", "{").replace("}}", "}")


def merge_dicts(*dicts: Dict[str, Any]) -> Dict[str, Any]:
    merged: Dict[str, Any] = {}
    for source in dicts:
        for key, value in source.items():
            if isinstance(value, dict) and isinstance(merged.get(key), dict):
                merged[key] = merge_dicts(merged[key], value)
            else:
                merged[key] = value
    return merged


def first_result_text(results: Any) -> str:
    if isinstance(results, list):
        for result in results:
            if isinstance(result, dict):
                content = result.get("content")
                if content:
                    return str(content)
    return ""


def coerce_bool(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value.lower() == "true"
    return bool(value)


def coerce_float(value: Any) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return 0.0


def coerce_int(value: Any) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return 0


def escape_html(text: str) -> str:
    return (
        str(text)
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
        .replace("'", "&#39;")
    )


if __name__ == "__main__":
    raise SystemExit(main())
