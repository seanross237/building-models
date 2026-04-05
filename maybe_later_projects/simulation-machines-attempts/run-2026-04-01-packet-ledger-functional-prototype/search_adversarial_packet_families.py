#!/usr/bin/env python3
"""Adversarial search for low-Leak, low-SD_target packet families.

Searches around the current best exploratory core sign pattern by:

- taking the strongest one-step external representative mode pairs,
- choosing subsets of them,
- assigning each chosen pair to one of its top incidence-weight role packets,
- evaluating exact-ledger packet metrics.
"""

from __future__ import annotations

import importlib.util
import itertools
import json
import math
import sys
from pathlib import Path


MODULE_PATH = Path(__file__).resolve().parent / "packet_ledger_functionals.py"


def load_module():
    spec = importlib.util.spec_from_file_location("packet_ledger_functionals_search_module", MODULE_PATH)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


MOD = load_module()
PACKET_ORDER = ["A", "B", "C", "D", "A_next"]
DEFAULT_CANDIDATE_COUNT = 6
DEFAULT_SUBSET_SIZES = (1, 2, 3, 4)
DEFAULT_PACKET_OPTION_COUNT = 3


def external_rep_candidates(core_modes):
    active = {(mode.vec, mode.sigma) for mode in core_modes}
    grouped_weight = {}
    incidence = {}

    for left in core_modes:
        for right in core_modes:
            target_vec = MOD.AUDIT.v_add(left.vec, right.vec)
            if target_vec == (0, 0, 0):
                continue
            for target_sigma in (-1, 1):
                if (target_vec, target_sigma) in active:
                    continue
                coeff = MOD.AUDIT.helical_coeff(target_vec, left.vec, right.vec, target_sigma, left.sigma, right.sigma)
                if abs(coeff) < 1e-12:
                    continue
                rep_vec, rep_sigma = MOD.canonical_target_pair(target_vec, target_sigma)
                key = (rep_vec, rep_sigma)
                grouped_weight[key] = grouped_weight.get(key, 0.0) + abs(coeff)
                incidence.setdefault(key, {packet: 0.0 for packet in PACKET_ORDER})
                incidence[key][left.packet] += abs(coeff)
                incidence[key][right.packet] += abs(coeff)

    ranked = sorted(grouped_weight.items(), key=lambda item: (-item[1], item[0]))
    candidates = []
    for key, weight in ranked:
        packet_scores = sorted(
            [(packet, score) for packet, score in incidence[key].items() if score > 0],
            key=lambda item: (-item[1], PACKET_ORDER.index(item[0])),
        )
        candidates.append(
            {
                "key": key,
                "weight": weight,
                "packet_scores": packet_scores,
            }
        )
    return candidates


def build_family(core_modes, chosen):
    family = list(core_modes)
    for idx, (candidate, packet) in enumerate(chosen, start=1):
        vec, sigma = candidate["key"]
        family.append(MOD.NamedMode(f"x{idx}", vec, sigma, packet))
        family.append(MOD.NamedMode(f"bar_x{idx}", MOD.AUDIT.v_scale(-1, vec), -sigma, packet))
    return family


def pareto_front(rows):
    front = []
    for row in sorted(rows, key=lambda row: (row["leak"], row["sd_target"], row["sd_part"])):
        dominated = False
        for other in front:
            if (
                other["leak"] <= row["leak"]
                and other["sd_target"] <= row["sd_target"]
                and (other["leak"] < row["leak"] or other["sd_target"] < row["sd_target"])
            ):
                dominated = True
                break
        if not dominated:
            front.append(row)
    return front


def search_rows(core_modes, candidate_count=DEFAULT_CANDIDATE_COUNT, subset_sizes=DEFAULT_SUBSET_SIZES, packet_option_count=DEFAULT_PACKET_OPTION_COUNT):
    candidates = external_rep_candidates(core_modes)[:candidate_count]
    rows = []
    for subset_size in subset_sizes:
        for subset in itertools.combinations(candidates, subset_size):
            packet_options = []
            for candidate in subset:
                packet_options.append([packet for packet, _ in candidate["packet_scores"][:packet_option_count]])
            for assignment in itertools.product(*packet_options):
                chosen = list(zip(subset, assignment))
                family = build_family(core_modes, chosen)
                metrics = MOD.packet_metrics(family)
                rows.append(
                    {
                        "subset_size": subset_size,
                        "added_keys": [candidate["key"] for candidate, _ in chosen],
                        "assigned_packets": list(assignment),
                        "drive_target": metrics["drive_target"],
                        "leak": metrics["leak"],
                        "sd_part": metrics["sd_part"],
                        "sd_target": metrics["sd_target"],
                    }
                )

    rows = [row for row in rows if math.isfinite(row["leak"]) and row["drive_target"] > 0]
    rows.sort(key=lambda row: (row["leak"], row["sd_target"], row["sd_part"]))
    return candidates, rows


def search_rows_for_sigma(sigma_by_role, candidate_count=DEFAULT_CANDIDATE_COUNT, subset_sizes=DEFAULT_SUBSET_SIZES, packet_option_count=DEFAULT_PACKET_OPTION_COUNT):
    core_modes = MOD.singleton_pair_family(sigma_by_role)
    return search_rows(
        core_modes,
        candidate_count=candidate_count,
        subset_sizes=subset_sizes,
        packet_option_count=packet_option_count,
    )


def main():
    candidates, rows = search_rows_for_sigma(MOD.CHOSEN_SIGMA)

    print("Search size:")
    print(json.dumps({"candidate_count": len(candidates), "tested_families": len(rows)}, sort_keys=True))

    print("\nTop 15 by leak:")
    for row in rows[:15]:
        print(json.dumps(row, sort_keys=True))

    print("\nTop 15 by sd_target subject to leak <= 15:")
    filtered = [row for row in rows if row["leak"] <= 15]
    filtered.sort(key=lambda row: (row["sd_target"], row["leak"], row["sd_part"]))
    for row in filtered[:15]:
        print(json.dumps(row, sort_keys=True))

    print("\nPareto front in (leak, sd_target):")
    for row in pareto_front(rows)[:20]:
        print(json.dumps(row, sort_keys=True))

    print("\nBest achievable sd_target under leak thresholds:")
    for threshold in (10, 12, 15, 20, 30):
        eligible = [row for row in rows if row["leak"] <= threshold]
        if not eligible:
            continue
        best = min(eligible, key=lambda row: (row["sd_target"], row["leak"], row["sd_part"]))
        print(json.dumps({"leak_threshold": threshold, **best}, sort_keys=True))


if __name__ == "__main__":
    main()
