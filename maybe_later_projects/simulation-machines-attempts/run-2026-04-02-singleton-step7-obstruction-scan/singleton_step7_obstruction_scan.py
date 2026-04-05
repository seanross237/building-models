#!/usr/bin/env python3
"""Scan singleton realizations of the Step-7 core on the old five-vector support."""

from __future__ import annotations

import argparse
import importlib.util
import itertools
import json
import sys
from dataclasses import dataclass
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
STEP7_CORE = {
    "A_n": {("C_n", "D_n")},
    "B_n": {("A_n", "A_n")},
    "C_n": {("A_n", "A_n"), ("B_n", "C_n")},
    "D_n": {("A_n", "C_n")},
    "E_n": {("D_n", "D_n")},
}
EXPECTED_PAIRS = tuple(
    (target_role, pair)
    for target_role in STEP7_ROLES
    for pair in sorted(STEP7_CORE[target_role])
)


def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


AUDIT = load_module(AUDIT_PATH, "singleton_step7_obstruction_scan_audit")


@dataclass(frozen=True)
class Mode:
    vec: tuple[int, int, int]
    sigma: int
    role: str
    conjugated: bool

    @property
    def name(self) -> str:
        return ("bar_" if self.conjugated else "") + self.role


def support_modes(k_by_role: dict[str, tuple[int, int, int]], sigma_by_role: dict[str, int]) -> list[Mode]:
    modes: list[Mode] = []
    for role in STEP7_ROLES:
        k = k_by_role[role]
        sigma = sigma_by_role[role]
        modes.append(Mode(k, sigma, role, False))
        modes.append(Mode(AUDIT.v_scale(-1, k), -sigma, role, True))
    return modes


def aggregate_internal(
    k_by_role: dict[str, tuple[int, int, int]], sigma_by_role: dict[str, int]
) -> dict[str, dict[tuple[str, str], complex]]:
    modes = support_modes(k_by_role, sigma_by_role)
    out: dict[str, dict[tuple[str, str], complex]] = {role: {} for role in STEP7_ROLES}
    for target_role in STEP7_ROLES:
        target = k_by_role[target_role]
        sigma_target = sigma_by_role[target_role]
        for left in modes:
            for right in modes:
                if AUDIT.v_add(left.vec, right.vec) != target:
                    continue
                coeff = AUDIT.helical_coeff(
                    target,
                    left.vec,
                    right.vec,
                    sigma_target,
                    left.sigma,
                    right.sigma,
                )
                if abs(coeff) < 1e-12:
                    continue
                key = (left.name, right.name)
                out[target_role][key] = out[target_role].get(key, 0.0j) + coeff
    return out


def aggregate_external(
    k_by_role: dict[str, tuple[int, int, int]], sigma_by_role: dict[str, int]
) -> dict[tuple[tuple[int, int, int], int, str, str], complex]:
    modes = support_modes(k_by_role, sigma_by_role)
    active = {mode.vec for mode in modes}
    out: dict[tuple[tuple[int, int, int], int, str, str], complex] = {}
    for left in modes:
        for right in modes:
            target = AUDIT.v_add(left.vec, right.vec)
            if target == (0, 0, 0) or target in active:
                continue
            for sigma_target in (-1, 1):
                coeff = AUDIT.helical_coeff(
                    target,
                    left.vec,
                    right.vec,
                    sigma_target,
                    left.sigma,
                    right.sigma,
                )
                if abs(coeff) < 1e-12:
                    continue
                key = (target, sigma_target, left.name, right.name)
                out[key] = out.get(key, 0.0j) + coeff
    return out


def classify_term(target_role: str, monomial: tuple[str, str]) -> str:
    if monomial in STEP7_CORE[target_role]:
        return "exact"
    plain = tuple(name.replace("bar_", "") for name in monomial)
    if plain in STEP7_CORE[target_role]:
        return "conjugate-adjusted"
    return "spectator"


def format_pair(target_role: str, pair: tuple[str, str]) -> str:
    return f"{pair[0]} + {pair[1]} -> {target_role}"


def coverage_metrics(
    k_by_role: dict[str, tuple[int, int, int]], sigma_by_role: dict[str, int]
) -> dict[str, object]:
    internal = aggregate_internal(k_by_role, sigma_by_role)
    external = aggregate_external(k_by_role, sigma_by_role)

    exact_pairs: set[tuple[str, tuple[str, str]]] = set()
    conjugate_pairs: set[tuple[str, tuple[str, str]]] = set()
    exact_abs_sum = 0.0
    conjugate_abs_sum = 0.0
    spectator_abs_sum = 0.0

    for target_role, terms in internal.items():
        for monomial, coeff in terms.items():
            status = classify_term(target_role, monomial)
            plain = tuple(name.replace("bar_", "") for name in monomial)
            if status == "exact":
                exact_pairs.add((target_role, plain))
                exact_abs_sum += abs(coeff)
            elif status == "conjugate-adjusted":
                conjugate_pairs.add((target_role, plain))
                conjugate_abs_sum += abs(coeff)
            else:
                spectator_abs_sum += abs(coeff)

    external_abs_sum = sum(abs(coeff) for coeff in external.values())
    max_external_abs = max((abs(coeff) for coeff in external.values()), default=0.0)
    missing_exact_pairs = [item for item in EXPECTED_PAIRS if item not in exact_pairs]
    exact_or_conjugate_pairs = exact_pairs | conjugate_pairs
    missing_even_with_conjugates = [item for item in EXPECTED_PAIRS if item not in exact_or_conjugate_pairs]

    return {
        "exact_pair_count": len(exact_pairs),
        "conjugate_pair_count": len(conjugate_pairs),
        "exact_abs_sum": exact_abs_sum,
        "conjugate_abs_sum": conjugate_abs_sum,
        "spectator_abs_sum": spectator_abs_sum,
        "external_abs_sum": external_abs_sum,
        "external_term_count": len(external),
        "max_external_abs": max_external_abs,
        "exact_pairs": sorted(format_pair(role, pair) for role, pair in exact_pairs),
        "conjugate_pairs": sorted(format_pair(role, pair) for role, pair in conjugate_pairs),
        "missing_exact_pairs": [format_pair(role, pair) for role, pair in missing_exact_pairs],
        "missing_even_with_conjugates": [
            format_pair(role, pair) for role, pair in missing_even_with_conjugates
        ],
    }


def assignment_payload(source_perm: tuple[str, ...], sigma_pattern: tuple[int, ...]) -> dict[str, object]:
    role_to_source = dict(zip(STEP7_ROLES, source_perm))
    k_by_role = {role: AUDIT.CHOSEN_K[source] for role, source in role_to_source.items()}
    sigma_by_role = dict(zip(STEP7_ROLES, sigma_pattern))
    metrics = coverage_metrics(k_by_role, sigma_by_role)
    return {
        "role_to_source": role_to_source,
        "wavevectors": k_by_role,
        "sigma": sigma_by_role,
        **metrics,
    }


def sort_key(row: dict[str, object]) -> tuple[float, ...]:
    return (
        -float(row["exact_pair_count"]),
        -float(row["conjugate_pair_count"]),
        -float(row["exact_abs_sum"]),
        float(row["external_abs_sum"]) + float(row["spectator_abs_sum"]),
        float(row["external_abs_sum"]),
        float(row["max_external_abs"]),
    )


def structural_obstructions() -> list[dict[str, object]]:
    return [
        {
            "name": "double-target collision",
            "assumptions": ["A_n + A_n -> B_n", "A_n + A_n -> C_n"],
            "conclusion": "k_B = 2 k_A and k_C = 2 k_A, hence k_B = k_C",
            "effect": "full exact singleton realization forces B_n and C_n onto the same wavevector",
        },
        {
            "name": "amplifier zero-mode obstruction",
            "assumptions": ["B_n + C_n -> C_n"],
            "conclusion": "k_B = 0",
            "effect": "exact singleton amplifier edge is impossible on nonzero Fourier support",
        },
        {
            "name": "feedback conjugate obstruction",
            "assumptions": ["A_n + C_n -> D_n", "C_n + D_n -> A_n"],
            "conclusion": "k_D = k_A + k_C and k_A = k_C + k_D, hence 2 k_C = 0",
            "effect": "exact return leg cannot coexist with exact activation on nonzero singleton support; it needs a conjugate adjustment",
        },
    ]


def search(limit: int) -> dict[str, object]:
    rows = []
    for source_perm in itertools.permutations(AUDIT.ROLES):
        for sigma_pattern in itertools.product((1, -1), repeat=len(STEP7_ROLES)):
            rows.append(assignment_payload(source_perm, sigma_pattern))
    rows.sort(key=sort_key)

    best_exact = rows[0]["exact_pair_count"]
    best_exact_rows = [row for row in rows if row["exact_pair_count"] == best_exact]
    best_exact_and_conjugate = max(
        row["exact_pair_count"] + row["conjugate_pair_count"] for row in rows
    )
    best_exact_conj_rows = [
        row
        for row in rows
        if row["exact_pair_count"] + row["conjugate_pair_count"] == best_exact_and_conjugate
    ]

    return {
        "candidate_source": str(AUDIT_PATH),
        "total_assignments_scanned": len(rows),
        "structural_obstructions": structural_obstructions(),
        "full_exact_realization_exists": any(
            row["exact_pair_count"] == len(EXPECTED_PAIRS) for row in rows
        ),
        "full_exact_or_conjugate_realization_exists": any(
            row["exact_pair_count"] + row["conjugate_pair_count"] == len(EXPECTED_PAIRS)
            for row in rows
        ),
        "best_exact_pair_count": best_exact,
        "best_exact_pair_fraction": f"{best_exact}/{len(EXPECTED_PAIRS)}",
        "best_exact_and_conjugate_pair_count": best_exact_and_conjugate,
        "best_exact_rows": best_exact_rows[:limit],
        "best_exact_and_conjugate_rows": best_exact_conj_rows[:limit],
        "top_rows_overall": rows[:limit],
    }


def print_row(prefix: str, row: dict[str, object]) -> None:
    print(prefix)
    print(f"  role_to_source: {row['role_to_source']}")
    print(f"  wavevectors: {row['wavevectors']}")
    print(f"  sigma: {row['sigma']}")
    print(
        "  coverage:"
        f" exact={row['exact_pair_count']}/{len(EXPECTED_PAIRS)},"
        f" conjugate={row['conjugate_pair_count']}/{len(EXPECTED_PAIRS)}"
    )
    print(
        "  weights:"
        f" exact_abs={row['exact_abs_sum']:.6f},"
        f" conjugate_abs={row['conjugate_abs_sum']:.6f},"
        f" spectator_abs={row['spectator_abs_sum']:.6f},"
        f" external_abs={row['external_abs_sum']:.6f},"
        f" max_external_abs={row['max_external_abs']:.6f}"
    )
    print(f"  exact_pairs: {row['exact_pairs']}")
    print(f"  conjugate_pairs: {row['conjugate_pairs']}")
    print(f"  missing_exact_pairs: {row['missing_exact_pairs']}")
    print(f"  missing_even_with_conjugates: {row['missing_even_with_conjugates']}")


def print_text(data: dict[str, object], limit: int) -> None:
    print("Structural singleton obstructions for the Step-7 exact core:")
    for item in data["structural_obstructions"]:
        print(f"- {item['name']}:")
        print(f"  assumptions: {item['assumptions']}")
        print(f"  conclusion: {item['conclusion']}")
        print(f"  effect: {item['effect']}")
    print()

    print("Exhaustive singleton scan on the old five-vector support:")
    print(f"- assignments scanned: {data['total_assignments_scanned']}")
    print(f"- full exact realization exists: {data['full_exact_realization_exists']}")
    print(
        "- full exact-or-conjugate realization exists:"
        f" {data['full_exact_or_conjugate_realization_exists']}"
    )
    print(f"- best exact coverage: {data['best_exact_pair_fraction']}")
    print(
        "- best exact+conjugate coverage:"
        f" {data['best_exact_and_conjugate_pair_count']}/{len(EXPECTED_PAIRS)}"
    )
    print()

    print(f"Top {limit} rows overall:")
    for index, row in enumerate(data["top_rows_overall"], start=1):
        print_row(f"{index}.", row)
        print()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, default=5, help="number of top rows to print")
    parser.add_argument("--json", action="store_true", help="print JSON")
    args = parser.parse_args()

    data = search(limit=args.limit)
    if args.json:
        print(json.dumps(data, indent=2, sort_keys=True))
        return
    print_text(data, limit=args.limit)


if __name__ == "__main__":
    main()
