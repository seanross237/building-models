#!/usr/bin/env python3
"""Prototype sign-defect analysis on the existing singleton helical audit.

This is a small follow-up helper. It loads the existing exact helical support
audit and evaluates a few candidate sign-defect quantities on the 32-sign scan.
"""

from __future__ import annotations

import importlib.util
import json
import math
import statistics
import sys
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
AUDIT_PATH = (
    ROOT
    / "codex-atlas"
    / "execution"
    / "instances"
    / "exact-ns-no-near-closed-tao-circuit"
    / "strategies"
    / "strategy-001"
    / "explorations"
    / "exploration-002"
    / "code"
    / "helical_support_audit.py"
)


def load_audit_module():
    spec = importlib.util.spec_from_file_location("helical_support_audit_module", AUDIT_PATH)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


AUDIT = load_audit_module()
ROLES = AUDIT.ROLES


def contribution_rows(sigma):
    internal = AUDIT.aggregate_internal(AUDIT.CHOSEN_K, sigma)
    external = AUDIT.aggregate_external(AUDIT.CHOSEN_K, sigma)
    rows = []

    def source_info(name):
        conj = name.startswith("bar_")
        role = name.replace("bar_", "")
        sign = -sigma[role] if conj else sigma[role]
        return role, sign

    for target_role, terms in internal.items():
        target_sigma = sigma[target_role]
        for (left, right), coeff in terms.items():
            left_role, left_sigma = source_info(left)
            right_role, right_sigma = source_info(right)
            rows.append(
                {
                    "status": AUDIT.classify_term(target_role, (left, right)),
                    "abs_coeff": abs(coeff),
                    "target_role": target_role,
                    "target_sigma": target_sigma,
                    "left_role": left_role,
                    "left_sigma": left_sigma,
                    "right_role": right_role,
                    "right_sigma": right_sigma,
                }
            )

    for (_, target_sigma, left, right), coeff in external.items():
        left_role, left_sigma = source_info(left)
        right_role, right_sigma = source_info(right)
        rows.append(
            {
                "status": "external",
                "abs_coeff": abs(coeff),
                "target_role": None,
                "target_sigma": target_sigma,
                "left_role": left_role,
                "left_sigma": left_sigma,
                "right_role": right_role,
                "right_sigma": right_sigma,
            }
        )

    return rows


def sign_defect_count(sigma):
    plus = sum(1 for role in ROLES if sigma[role] == 1)
    minus = len(ROLES) - plus
    return min(plus, minus) / len(ROLES)


def sign_defect_mode(sigma, desired_only=False):
    rows = contribution_rows(sigma)
    if desired_only:
        rows = [row for row in rows if row["status"] == "desired"]
    weights = {role: 0.0 for role in ROLES}
    for row in rows:
        weight = row["abs_coeff"]
        for role in {row["left_role"], row["right_role"]}:
            weights[role] += weight
        if row["target_role"] in weights:
            weights[row["target_role"]] += weight
    total = sum(weights.values())
    if total == 0:
        return 1.0
    best_same_sign_weight = max(
        sum(weight for role, weight in weights.items() if sigma[role] == tau) for tau in (-1, 1)
    )
    return 1.0 - best_same_sign_weight / total


def sign_defect_triad(sigma, desired_only=False):
    rows = contribution_rows(sigma)
    if desired_only:
        rows = [row for row in rows if row["status"] == "desired"]
    total = sum(row["abs_coeff"] for row in rows)
    if total == 0:
        return 1.0
    heterochiral = sum(
        row["abs_coeff"]
        for row in rows
        if len({row["left_sigma"], row["right_sigma"], row["target_sigma"]}) > 1
    )
    return heterochiral / total


def leak_ratio(scan_row):
    if scan_row["desired_abs_sum"] == 0:
        return math.inf
    return (scan_row["internal_leak_abs_sum"] + scan_row["external_leak_abs_sum"]) / scan_row["desired_abs_sum"]


def main():
    finite_rows = []
    for row in AUDIT.sigma_scan(AUDIT.CHOSEN_K):
        sigma = row["sigma"]
        ratio = leak_ratio(row)
        payload = {
            "sigma": sigma,
            "desired_abs_sum": row["desired_abs_sum"],
            "leak_ratio": ratio,
            "sign_defect_count": sign_defect_count(sigma),
            "sign_defect_mode": sign_defect_mode(sigma),
            "sign_defect_mode_desired": sign_defect_mode(sigma, desired_only=True),
            "sign_defect_triad": sign_defect_triad(sigma),
            "sign_defect_triad_desired": sign_defect_triad(sigma, desired_only=True),
        }
        if math.isfinite(ratio):
            finite_rows.append(payload)

    print("Top finite rows by leak ratio:")
    for row in finite_rows[:12]:
        print(json.dumps(row, sort_keys=True))

    print("\nLeak ratio grouped by sign_defect_count:")
    groups = defaultdict(list)
    for row in finite_rows:
        groups[row["sign_defect_count"]].append(row["leak_ratio"])
    for defect in sorted(groups):
        vals = groups[defect]
        print(
            json.dumps(
                {
                    "sign_defect_count": defect,
                    "count": len(vals),
                    "min_leak_ratio": min(vals),
                    "mean_leak_ratio": statistics.mean(vals),
                    "max_leak_ratio": max(vals),
                },
                sort_keys=True,
            )
        )

    print("\nDesired activation coefficient table for a1,a3->a4:")
    for s1 in (-1, 1):
        for s3 in (-1, 1):
            for s4 in (-1, 1):
                coeff = AUDIT.helical_coeff(
                    AUDIT.CHOSEN_K["a4"],
                    AUDIT.CHOSEN_K["a1"],
                    AUDIT.CHOSEN_K["a3"],
                    s4,
                    s1,
                    s3,
                )
                print(
                    json.dumps(
                        {
                            "s1": s1,
                            "s3": s3,
                            "s4": s4,
                            "abs_coeff": abs(coeff),
                            "nonzero": abs(coeff) > 1e-12,
                        },
                        sort_keys=True,
                    )
                )


if __name__ == "__main__":
    main()
