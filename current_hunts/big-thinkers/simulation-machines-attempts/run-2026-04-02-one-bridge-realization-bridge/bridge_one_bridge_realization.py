#!/usr/bin/env python3
"""Bridge the Step-7 one-bridge roles to one explicit helical realization candidate."""

from __future__ import annotations

import argparse
import importlib.util
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

ROLE_MAP = {
    "a1": "A_n",
    "a2": "B_n",
    "a3": "C_n",
    "a4": "D_n",
    "a5": "E_n",
}

# Step-7 desired core, expressed as target role -> exact role-pair witnesses.
STEP7_CORE = {
    "A_n": {("C_n", "D_n")},
    "B_n": {("A_n", "A_n")},
    "C_n": {("A_n", "A_n"), ("B_n", "C_n")},
    "D_n": {("A_n", "C_n")},
    "E_n": {("D_n", "D_n")},
}


def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


AUDIT = load_module(AUDIT_PATH, "one_bridge_realization_bridge_audit")


def mapped_name(name: str) -> str:
    if name.startswith("bar_"):
        return f"bar_{ROLE_MAP[name[4:]]}"
    return ROLE_MAP[name]


def mapped_plain(name: str) -> str:
    return mapped_name(name).replace("bar_", "")


def complex_str(z: complex) -> str:
    return f"{z.real:.12f}{z.imag:+.12f}j"


def desired_status(target_role: str, monomial: tuple[str, str]) -> str:
    mapped_target = ROLE_MAP[target_role]
    mapped_pair = tuple(mapped_name(item) for item in monomial)
    plain_pair = tuple(item.replace("bar_", "") for item in mapped_pair)
    if plain_pair in STEP7_CORE[mapped_target]:
        if any(item.startswith("bar_") for item in mapped_pair):
            return "conjugate-adjusted"
        return "exact"
    return "spectator"


def internal_summary():
    internal = AUDIT.aggregate_internal(AUDIT.CHOSEN_K, AUDIT.CHOSEN_SIGMA)
    rows = []
    exact_count = 0
    conjugate_count = 0
    for role in AUDIT.ROLES:
        target_rows = []
        for monomial, coeff in sorted(internal[role].items()):
            status = desired_status(role, monomial)
            if status == "exact":
                exact_count += 1
            elif status == "conjugate-adjusted":
                conjugate_count += 1
            target_rows.append(
                {
                    "monomial": [mapped_name(item) for item in monomial],
                    "plain_roles": [mapped_plain(item) for item in monomial],
                    "coeff": complex_str(coeff),
                    "abs_coeff": round(abs(coeff), 12),
                    "status": status,
                }
            )
        rows.append(
            {
                "target_role": ROLE_MAP[role],
                "wavevector": AUDIT.CHOSEN_K[role],
                "sigma": AUDIT.CHOSEN_SIGMA[role],
                "terms": target_rows,
            }
        )
    return rows, exact_count, conjugate_count


def desired_core_coverage(internal_rows):
    by_target = {row["target_role"]: row["terms"] for row in internal_rows}
    coverage = []
    for target_role, expected_pairs in STEP7_CORE.items():
        exact_matches = []
        conjugate_matches = []
        for term in by_target.get(target_role, []):
            pair = tuple(term["plain_roles"])
            if pair not in expected_pairs:
                continue
            if term["status"] == "exact":
                exact_matches.append(term)
            elif term["status"] == "conjugate-adjusted":
                conjugate_matches.append(term)
        coverage.append(
            {
                "target_role": target_role,
                "expected_pairs": [list(pair) for pair in sorted(expected_pairs)],
                "exact_matches": exact_matches,
                "conjugate_adjusted_matches": conjugate_matches,
                "missing_exact_pairs": [
                    list(pair)
                    for pair in sorted(expected_pairs)
                    if pair not in {tuple(term["plain_roles"]) for term in exact_matches}
                ],
            }
        )
    return coverage


def external_summary(limit: int):
    external = AUDIT.aggregate_external(AUDIT.CHOSEN_K, AUDIT.CHOSEN_SIGMA)
    items = sorted(external.items(), key=lambda item: abs(item[1]), reverse=True)
    rows = []
    for (target, sigma_target, left, right), coeff in items[:limit]:
        rows.append(
            {
                "target": target,
                "sigma": sigma_target,
                "monomial": [mapped_name(left), mapped_name(right)],
                "coeff": complex_str(coeff),
                "abs_coeff": round(abs(coeff), 12),
            }
        )
    return rows, len(external)


def checklist(coverage, total_external_count, exact_count, conjugate_count):
    has_exact_core = all(item["exact_matches"] for item in coverage)
    return {
        "explicit_wavevector_family": True,
        "fixed_helicity_assignment": True,
        "exact_coefficient_formula_present": True,
        "all_step7_core_edges_have_exact_internal_witness": has_exact_core,
        "some_step7_core_edges_only_survive_conjugate_adjustment": any(
            item["conjugate_adjusted_matches"] for item in coverage
        ),
        "finite_internal_closure_without_external_emission": total_external_count == 0,
        "exact_internal_desired_term_count": exact_count,
        "conjugate_adjusted_desired_term_count": conjugate_count,
    }


def payload(limit: int):
    internal_rows, exact_count, conjugate_count = internal_summary()
    coverage = desired_core_coverage(internal_rows)
    external_rows, total_external_count = external_summary(limit=limit)
    return {
        "candidate_source": str(AUDIT_PATH),
        "role_map": ROLE_MAP,
        "candidate_wavevectors": {ROLE_MAP[role]: AUDIT.CHOSEN_K[role] for role in AUDIT.ROLES},
        "candidate_sigmas": {ROLE_MAP[role]: AUDIT.CHOSEN_SIGMA[role] for role in AUDIT.ROLES},
        "desired_core": {target: [list(pair) for pair in sorted(pairs)] for target, pairs in STEP7_CORE.items()},
        "internal_ledger": internal_rows,
        "desired_core_coverage": coverage,
        "top_external_emissions": external_rows,
        "external_emission_count": total_external_count,
        "generic_checks": AUDIT.generic_checks(),
        "checklist": checklist(coverage, total_external_count, exact_count, conjugate_count),
    }


def print_text(data):
    print("Candidate explicit realization:")
    for role, vec in data["candidate_wavevectors"].items():
        sigma = data["candidate_sigmas"][role]
        print(f"  {role}: k = {tuple(vec)}, sigma = {sigma}")
    print()

    print("Desired-core coverage on this candidate:")
    for item in data["desired_core_coverage"]:
        print(f"  target {item['target_role']}:")
        print(f"    expected: {item['expected_pairs']}")
        if item["exact_matches"]:
            print("    exact matches:")
            for term in item["exact_matches"]:
                print(f"      {term['monomial']}  abs_coeff={term['abs_coeff']}")
        if item["conjugate_adjusted_matches"]:
            print("    conjugate-adjusted matches:")
            for term in item["conjugate_adjusted_matches"]:
                print(f"      {term['monomial']}  abs_coeff={term['abs_coeff']}")
        if item["missing_exact_pairs"]:
            print(f"    missing exact pairs: {item['missing_exact_pairs']}")
    print()

    print("Checklist against the Step-9 source-basis gap:")
    for key, value in data["checklist"].items():
        print(f"  {key}: {value}")
    print()

    print("Top external emissions:")
    for row in data["top_external_emissions"]:
        print(
            f"  target={tuple(row['target'])}, sigma={row['sigma']},"
            f" monomial={row['monomial']}, abs_coeff={row['abs_coeff']}"
        )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, default=12, help="number of external emissions to show")
    parser.add_argument("--json", action="store_true", help="print JSON")
    args = parser.parse_args()

    data = payload(limit=args.limit)
    if args.json:
        print(json.dumps(data, indent=2, sort_keys=True))
        return
    print_text(data)


if __name__ == "__main__":
    main()
