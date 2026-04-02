#!/usr/bin/env python3
"""Search helicity sheets and representative conventions on one explicit wavevector family."""

from __future__ import annotations

import argparse
import importlib.util
import itertools
import json
import sys
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

STEP7_ROLES = ("A_n", "B_n", "C_n", "D_n", "E_n")
AUDIT_ROLE_BY_STEP7 = {
    "A_n": "a1",
    "B_n": "a2",
    "C_n": "a3",
    "D_n": "a4",
    "E_n": "a5",
}
STEP7_CORE = {
    "A_n": (("C_n", "D_n"),),
    "B_n": (("A_n", "A_n"),),
    "C_n": (("A_n", "A_n"), ("B_n", "C_n")),
    "D_n": (("A_n", "C_n"),),
    "E_n": (("D_n", "D_n"),),
}


def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


AUDIT = load_module(AUDIT_PATH, "fixed_wavevector_sheet_search_audit")


def pair_key(pair: tuple[str, str]) -> tuple[str, str]:
    return tuple(sorted(pair))


def target_ledgers_for_sigma(sigma_by_role: dict[str, int]):
    modes = AUDIT.support_modes(AUDIT.CHOSEN_K, sigma_by_role)
    out: dict[str, dict[tuple[str, str], complex]] = {}
    for target in modes:
        terms: dict[tuple[str, str], complex] = {}
        for left in modes:
            for right in modes:
                if AUDIT.v_add(left.vec, right.vec) != target.vec:
                    continue
                coeff = AUDIT.helical_coeff(
                    target.vec,
                    left.vec,
                    right.vec,
                    target.sigma,
                    left.sigma,
                    right.sigma,
                )
                if abs(coeff) < 1e-12:
                    continue
                key = (left.name, right.name)
                terms[key] = terms.get(key, 0.0j) + coeff
        out[target.name] = terms
    external = AUDIT.aggregate_external(AUDIT.CHOSEN_K, sigma_by_role)
    return {
        "internal": out,
        "external_abs_sum": sum(abs(coeff) for coeff in external.values()),
        "external_count": len(external),
        "top_external": [
            {
                "target": list(target),
                "sigma": sigma_target,
                "monomial": [left, right],
                "abs_coeff": round(abs(coeff), 12),
            }
            for (target, sigma_target, left, right), coeff in sorted(
                external.items(), key=lambda item: abs(item[1]), reverse=True
            )[:8]
        ],
    }


def mode_name(step7_role: str, representative_bits: dict[str, int]) -> str:
    base = AUDIT_ROLE_BY_STEP7[step7_role]
    return f"bar_{base}" if representative_bits[step7_role] else base


def evaluate_configuration(
    sigma_by_role: dict[str, int],
    representative_bits: dict[str, int],
    precomputed: dict[str, object],
) -> dict[str, object]:
    internal = precomputed["internal"]
    exact_coverage = 0
    desired_abs_sum = 0.0
    internal_spectator_abs_sum = 0.0
    matched_pairs: list[dict[str, object]] = []
    missing_pairs: list[dict[str, object]] = []

    for target_role, expected_pairs in STEP7_CORE.items():
        target_name = mode_name(target_role, representative_bits)
        terms = internal[target_name]
        matched_unordered = set()
        for monomial, coeff in terms.items():
            monomial_key = pair_key(monomial)
            desired_here = False
            for sources in expected_pairs:
                expected_names = (
                    mode_name(sources[0], representative_bits),
                    mode_name(sources[1], representative_bits),
                )
                if monomial_key == pair_key(expected_names):
                    desired_here = True
                    matched_unordered.add(pair_key(expected_names))
                    desired_abs_sum += abs(coeff)
            if not desired_here:
                internal_spectator_abs_sum += abs(coeff)

        for sources in expected_pairs:
            expected_names = (
                mode_name(sources[0], representative_bits),
                mode_name(sources[1], representative_bits),
            )
            key = pair_key(expected_names)
            if key in matched_unordered:
                exact_coverage += 1
                matched_pairs.append(
                    {
                        "target_role": target_role,
                        "target_mode": target_name,
                        "sources": list(sources),
                        "mode_sources": list(expected_names),
                    }
                )
            else:
                missing_pairs.append(
                    {
                        "target_role": target_role,
                        "target_mode": target_name,
                        "sources": list(sources),
                        "mode_sources": list(expected_names),
                    }
                )

    total_expected = sum(len(pairs) for pairs in STEP7_CORE.values())
    total_leak = internal_spectator_abs_sum + float(precomputed["external_abs_sum"])
    return {
        "sigma_by_step7_role": {
            step7_role: sigma_by_role[AUDIT_ROLE_BY_STEP7[step7_role]]
            for step7_role in STEP7_ROLES
        },
        "representative_modes": {
            step7_role: mode_name(step7_role, representative_bits) for step7_role in STEP7_ROLES
        },
        "exact_coverage": exact_coverage,
        "total_expected_pairs": total_expected,
        "desired_abs_sum": desired_abs_sum,
        "internal_spectator_abs_sum": internal_spectator_abs_sum,
        "external_abs_sum": precomputed["external_abs_sum"],
        "external_count": precomputed["external_count"],
        "total_leak_abs_sum": total_leak,
        "matched_pairs": matched_pairs,
        "missing_pairs": missing_pairs,
        "top_external": precomputed["top_external"],
    }


def search():
    sigma_patterns = []
    for pattern in itertools.product((1, -1), repeat=len(AUDIT.ROLES)):
        sigma_by_role = dict(zip(AUDIT.ROLES, pattern))
        sigma_patterns.append((sigma_by_role, target_ledgers_for_sigma(sigma_by_role)))

    rows = []
    for sigma_by_role, precomputed in sigma_patterns:
        for bits in itertools.product((0, 1), repeat=len(STEP7_ROLES)):
            representative_bits = dict(zip(STEP7_ROLES, bits))
            rows.append(evaluate_configuration(sigma_by_role, representative_bits, precomputed))

    rows.sort(
        key=lambda row: (
            -row["exact_coverage"],
            row["total_leak_abs_sum"],
            row["external_abs_sum"],
            -row["desired_abs_sum"],
            sum(1 for value in row["representative_modes"].values() if value.startswith("bar_")),
        )
    )
    return rows


def summarize(rows: list[dict[str, object]]) -> dict[str, object]:
    best = rows[0]
    max_coverage = best["exact_coverage"]
    best_with_max_coverage = [row for row in rows if row["exact_coverage"] == max_coverage]
    full_coverage = [row for row in rows if row["exact_coverage"] == row["total_expected_pairs"]]
    pair_catalog = [
        (target_role, sources)
        for target_role, expected_pairs in STEP7_CORE.items()
        for sources in expected_pairs
    ]
    pair_availability = {
        json.dumps({"target_role": target_role, "sources": list(sources)}, sort_keys=True): {
            "target_role": target_role,
            "sources": list(sources),
            "matched_in_some_configuration": False,
            "best_total_leak_abs_sum": None,
            "example_sigma_by_step7_role": None,
            "example_representative_modes": None,
        }
        for target_role, sources in pair_catalog
    }

    by_coverage = {}
    for row in rows:
        key = str(row["exact_coverage"])
        if key not in by_coverage:
            by_coverage[key] = {
                "best_total_leak_abs_sum": row["total_leak_abs_sum"],
                "best_external_abs_sum": row["external_abs_sum"],
                "best_desired_abs_sum": row["desired_abs_sum"],
                "representative_modes": row["representative_modes"],
                "sigma_by_step7_role": row["sigma_by_step7_role"],
                "missing_pair_count": len(row["missing_pairs"]),
            }
        matched_pairs = {
            (item["target_role"], tuple(item["sources"])) for item in row["matched_pairs"]
        }
        for pair in pair_catalog:
            if pair not in matched_pairs:
                continue
            bucket = pair_availability[
                json.dumps({"target_role": pair[0], "sources": list(pair[1])}, sort_keys=True)
            ]
            bucket["matched_in_some_configuration"] = True
            if (
                bucket["best_total_leak_abs_sum"] is None
                or row["total_leak_abs_sum"] < bucket["best_total_leak_abs_sum"]
            ):
                bucket["best_total_leak_abs_sum"] = row["total_leak_abs_sum"]
                bucket["example_sigma_by_step7_role"] = row["sigma_by_step7_role"]
                bucket["example_representative_modes"] = row["representative_modes"]

    return {
        "candidate_source": str(AUDIT_PATH),
        "fixed_wavevectors": {step7: AUDIT.CHOSEN_K[audit_role] for step7, audit_role in AUDIT_ROLE_BY_STEP7.items()},
        "searched_sigma_patterns": 2 ** len(AUDIT.ROLES),
        "searched_representative_conventions": 2 ** len(STEP7_ROLES),
        "searched_total_configurations": len(rows),
        "max_exact_coverage": max_coverage,
        "total_expected_pairs": best["total_expected_pairs"],
        "full_coverage_exists": bool(full_coverage),
        "best_configuration": best,
        "best_with_max_coverage_count": len(best_with_max_coverage),
        "by_coverage": by_coverage,
        "pair_availability": list(pair_availability.values()),
        "top_configurations": rows[:10],
    }


def print_text(summary: dict[str, object]) -> None:
    print("Fixed explicit wavevector family:")
    for role, vec in summary["fixed_wavevectors"].items():
        print(f"  {role}: k = {tuple(vec)}")
    print()

    print(
        "Search size:"
        f" sigma={summary['searched_sigma_patterns']},"
        f" representative_conventions={summary['searched_representative_conventions']},"
        f" total={summary['searched_total_configurations']}"
    )
    print(
        "Best exact coverage:"
        f" {summary['max_exact_coverage']} / {summary['total_expected_pairs']}"
        f"  full_coverage_exists={summary['full_coverage_exists']}"
    )
    print()

    best = summary["best_configuration"]
    print("Best configuration:")
    print(f"  sigma_by_role = {best['sigma_by_step7_role']}")
    print(f"  representatives = {best['representative_modes']}")
    print(
        "  leak ledger:"
        f" desired_abs_sum={best['desired_abs_sum']:.12f},"
        f" internal_spectator_abs_sum={best['internal_spectator_abs_sum']:.12f},"
        f" external_abs_sum={best['external_abs_sum']:.12f},"
        f" total_leak_abs_sum={best['total_leak_abs_sum']:.12f}"
    )
    print("  matched pairs:")
    for item in best["matched_pairs"]:
        print(
            f"    target={item['target_role']},"
            f" sources={tuple(item['sources'])},"
            f" modes={tuple(item['mode_sources'])}"
        )
    print("  missing pairs:")
    for item in best["missing_pairs"]:
        print(
            f"    target={item['target_role']},"
            f" sources={tuple(item['sources'])},"
            f" modes={tuple(item['mode_sources'])}"
        )
    print("  top external emissions:")
    for item in best["top_external"]:
        print(
            f"    target={tuple(item['target'])}, sigma={item['sigma']},"
            f" monomial={tuple(item['monomial'])}, abs_coeff={item['abs_coeff']}"
        )
    print()

    print("Best row at each coverage level:")
    for coverage, row in sorted(summary["by_coverage"].items(), key=lambda item: int(item[0]), reverse=True):
        print(
            f"  coverage={coverage}:"
            f" total_leak_abs_sum={row['best_total_leak_abs_sum']:.12f},"
            f" external_abs_sum={row['best_external_abs_sum']:.12f},"
            f" desired_abs_sum={row['best_desired_abs_sum']:.12f},"
            f" missing_pair_count={row['missing_pair_count']}"
        )
    print()

    print("Desired-pair availability anywhere in the search:")
    for item in summary["pair_availability"]:
        print(
            f"  target={item['target_role']}, sources={tuple(item['sources'])},"
            f" matched={item['matched_in_some_configuration']},"
            f" best_total_leak_abs_sum={item['best_total_leak_abs_sum']}"
        )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true", help="print full JSON summary")
    args = parser.parse_args()

    rows = search()
    summary = summarize(rows)
    if args.json:
        print(json.dumps(summary, indent=2, sort_keys=True))
        return
    print_text(summary)


if __name__ == "__main__":
    main()
