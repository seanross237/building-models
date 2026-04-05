#!/usr/bin/env python3
"""Scan one-step source-incidence packet lifts across the 32 core sign patterns."""

from __future__ import annotations

import importlib.util
import itertools
import json
import math
import statistics
import sys
from collections import defaultdict
from pathlib import Path


MODULE_PATH = Path(__file__).resolve().parent / "packet_ledger_functionals.py"


def load_module():
    spec = importlib.util.spec_from_file_location("packet_ledger_functionals_scan_module", MODULE_PATH)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


MOD = load_module()


def incidence_family_for_sigma(sigma_by_role, top_n=4):
    core = MOD.singleton_pair_family(sigma_by_role)
    active = {(mode.vec, mode.sigma) for mode in core}
    packet_order = ["A", "B", "C", "D", "A_next"]
    grouped_weight = {}
    incidence = {}

    for left in core:
        for right in core:
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
                incidence.setdefault(key, {packet: 0.0 for packet in packet_order})
                incidence[key][left.packet] += abs(coeff)
                incidence[key][right.packet] += abs(coeff)

    ranked = sorted(grouped_weight.items(), key=lambda item: (-item[1], item[0]))[:top_n]
    family = list(core)
    for idx, ((vec, sigma), _) in enumerate(ranked, start=1):
        packet = sorted(
            incidence[(vec, sigma)].items(),
            key=lambda item: (-item[1], packet_order.index(item[0])),
        )[0][0]
        family.append(MOD.NamedMode(f"x{idx}", vec, sigma, packet))
        family.append(MOD.NamedMode(f"bar_x{idx}", MOD.AUDIT.v_scale(-1, vec), -sigma, packet))
    return family


def main():
    rows = []
    for pattern in itertools.product((1, -1), repeat=len(MOD.AUDIT.ROLES)):
        sigma = dict(zip(MOD.AUDIT.ROLES, pattern))
        family = incidence_family_for_sigma(sigma)
        metrics = MOD.packet_metrics(family)
        plus = sum(1 for value in sigma.values() if value == 1)
        rows.append(
            {
                "sigma": sigma,
                "minority_count": min(plus, len(MOD.AUDIT.ROLES) - plus),
                "drive_target": metrics["drive_target"],
                "leak": metrics["leak"],
                "sd_part": metrics["sd_part"],
                "sd_target": metrics["sd_target"],
            }
        )

    rows = [row for row in rows if math.isfinite(row["leak"])]
    rows.sort(key=lambda row: row["leak"])

    print("Top 12 source-incidence packet families by leak:")
    for row in rows[:12]:
        print(json.dumps(row, sort_keys=True))

    print("\nGrouped by minority_count:")
    grouped = defaultdict(list)
    for row in rows:
        grouped[row["minority_count"]].append(row)
    for key in sorted(grouped):
        leaks = [row["leak"] for row in grouped[key]]
        sd_part = [row["sd_part"] for row in grouped[key]]
        sd_target = [row["sd_target"] for row in grouped[key]]
        print(
            json.dumps(
                {
                    "minority_count": key,
                    "count": len(grouped[key]),
                    "min_leak": min(leaks),
                    "mean_leak": statistics.mean(leaks),
                    "max_leak": max(leaks),
                    "mean_sd_part": statistics.mean(sd_part),
                    "mean_sd_target": statistics.mean(sd_target),
                },
                sort_keys=True,
            )
        )


if __name__ == "__main__":
    main()
