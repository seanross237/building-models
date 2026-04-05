#!/usr/bin/env python3
"""Global adversarial packet-family scan across all 32 core sign patterns."""

from __future__ import annotations

import importlib.util
import itertools
import json
import multiprocessing as mp
import statistics
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent
SEARCH_PATH = ROOT / "search_adversarial_packet_families.py"


def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


SEARCH = load_module(SEARCH_PATH, "packet_adversarial_search_all_signs_module")
MOD = SEARCH.MOD
THRESHOLDS = (8, 10, 12, 15, 20, 30)


def sign_patterns():
    for pattern in itertools.product((1, -1), repeat=len(MOD.AUDIT.ROLES)):
        sigma = dict(zip(MOD.AUDIT.ROLES, pattern))
        plus = sum(1 for value in sigma.values() if value == 1)
        yield sigma, min(plus, len(MOD.AUDIT.ROLES) - plus)


def best_under_threshold(rows, threshold):
    eligible = [row for row in rows if row["leak"] <= threshold]
    if not eligible:
        return None
    return min(eligible, key=lambda row: (row["sd_target"], row["leak"], row["sd_part"]))


def serialize_sigma(sigma):
    return tuple(sigma[role] for role in MOD.AUDIT.ROLES)


def scan_one_pattern(pattern):
    sigma = dict(zip(MOD.AUDIT.ROLES, pattern))
    plus = sum(1 for value in sigma.values() if value == 1)
    minority_count = min(plus, len(MOD.AUDIT.ROLES) - plus)
    sigma_tuple = serialize_sigma(sigma)

    core_modes = MOD.singleton_pair_family(sigma)
    baseline_metrics = MOD.packet_metrics(core_modes)
    baseline_row = {
        "sigma": sigma,
        "sigma_tuple": sigma_tuple,
        "minority_count": minority_count,
        "drive_target": baseline_metrics["drive_target"],
        "leak": baseline_metrics["leak"],
        "sd_part": baseline_metrics["sd_part"],
        "sd_target": baseline_metrics["sd_target"],
    }

    candidates, rows = SEARCH.search_rows(core_modes)
    annotated = []
    for row in rows:
        annotated.append(
            {
                **row,
                "sigma": sigma,
                "sigma_tuple": sigma_tuple,
                "minority_count": minority_count,
            }
        )

    by_leak = min(annotated, key=lambda row: (row["leak"], row["sd_target"], row["sd_part"]))
    by_sd_target = min(annotated, key=lambda row: (row["sd_target"], row["leak"], row["sd_part"]))
    under_15 = best_under_threshold(annotated, 15)
    per_pattern = {
        "sigma": sigma,
        "sigma_tuple": sigma_tuple,
        "minority_count": minority_count,
        "best_leak": by_leak["leak"],
        "best_leak_sd_target": by_leak["sd_target"],
        "best_sd_target": by_sd_target["sd_target"],
        "best_sd_target_leak": by_sd_target["leak"],
        "best_sd_target_under_15": None if under_15 is None else under_15["sd_target"],
        "best_sd_target_under_15_leak": None if under_15 is None else under_15["leak"],
    }

    return {
        "baseline_row": baseline_row,
        "candidate_count": len(candidates),
        "rows": annotated,
        "per_pattern": per_pattern,
    }


def main():
    patterns = list(itertools.product((1, -1), repeat=len(MOD.AUDIT.ROLES)))
    worker_count = min(len(patterns), mp.cpu_count())

    with mp.Pool(processes=worker_count) as pool:
        results = pool.map(scan_one_pattern, patterns)

    all_rows = []
    baseline_rows = []
    per_pattern_best = []
    candidate_counts = []

    for result in results:
        baseline_rows.append(result["baseline_row"])
        candidate_counts.append(result["candidate_count"])
        all_rows.extend(result["rows"])
        per_pattern_best.append(result["per_pattern"])

    baseline_rows.sort(key=lambda row: (row["leak"], row["sd_target"], row["sd_part"]))
    all_rows.sort(key=lambda row: (row["leak"], row["sd_target"], row["sd_part"]))
    per_pattern_best.sort(key=lambda row: (row["best_leak"], row["best_leak_sd_target"]))

    print("Global search size:")
    print(
        json.dumps(
            {
                "patterns": len(per_pattern_best),
                "workers": worker_count,
                "candidate_count_min": min(candidate_counts),
                "candidate_count_max": max(candidate_counts),
                "tested_families": len(all_rows),
                "mean_families_per_pattern": round(len(all_rows) / len(per_pattern_best), 2),
            },
            sort_keys=True,
        )
    )

    print("\nBest 12 singleton baselines by leak:")
    for row in baseline_rows[:12]:
        print(json.dumps(row, sort_keys=True))

    print("\nBest 20 expanded families by leak globally:")
    for row in all_rows[:20]:
        print(json.dumps(row, sort_keys=True))

    print("\nBest 20 expanded families by sd_target subject to leak <= 15 globally:")
    filtered = [row for row in all_rows if row["leak"] <= 15]
    filtered.sort(key=lambda row: (row["sd_target"], row["leak"], row["sd_part"]))
    for row in filtered[:20]:
        print(json.dumps(row, sort_keys=True))

    print("\nBest expanded family by leak within each minority_count:")
    for minority_count in sorted({row["minority_count"] for row in per_pattern_best}):
        bucket = [row for row in per_pattern_best if row["minority_count"] == minority_count]
        best = min(bucket, key=lambda row: (row["best_leak"], row["best_leak_sd_target"]))
        print(json.dumps(best, sort_keys=True))

    print("\nBest achievable sd_target under leak thresholds globally:")
    for threshold in THRESHOLDS:
        best = best_under_threshold(all_rows, threshold)
        if best is None:
            continue
        print(json.dumps({"leak_threshold": threshold, **best}, sort_keys=True))

    print("\nBest achievable sd_target under leak thresholds by minority_count:")
    for threshold in THRESHOLDS:
        for minority_count in sorted({row["minority_count"] for row in all_rows}):
            bucket = [row for row in all_rows if row["minority_count"] == minority_count]
            best = best_under_threshold(bucket, threshold)
            if best is None:
                continue
            print(json.dumps({"leak_threshold": threshold, "minority_count": minority_count, **best}, sort_keys=True))

    front = SEARCH.pareto_front(all_rows)
    print("\nGlobal Pareto front in (leak, sd_target):")
    for row in front[:30]:
        print(json.dumps(row, sort_keys=True))

    print("\nPer-pattern summary stats:")
    print(
        json.dumps(
            {
                "best_leak_min": min(row["best_leak"] for row in per_pattern_best),
                "best_leak_median": statistics.median(row["best_leak"] for row in per_pattern_best),
                "best_sd_target_under_15_min": min(
                    row["best_sd_target_under_15"] for row in per_pattern_best if row["best_sd_target_under_15"] is not None
                ),
                "best_sd_target_under_15_median": statistics.median(
                    row["best_sd_target_under_15"] for row in per_pattern_best if row["best_sd_target_under_15"] is not None
                ),
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
