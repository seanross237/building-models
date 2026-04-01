#!/usr/bin/env python3
"""Exact helical audit for exploration-002.

This script fixes one explicit five-role singleton support, computes the exact
helical coefficients using the Waleffe/Biferale helical basis formula, and
prints:

1. internal amplitude equations for the five distinguished amplitudes,
2. support-breaking external emissions forced by the active support,
3. a scan over all 32 helicity assignments on the same wavevector support.
"""

from __future__ import annotations

import itertools
import json
import math
from dataclasses import dataclass


Role = str
Vec = tuple[int, int, int]


ROLES: tuple[Role, ...] = ("a1", "a2", "a3", "a4", "a5")

CHOSEN_K: dict[Role, Vec] = {
    "a1": (1, 0, 0),
    "a2": (2, 0, 0),
    "a3": (0, 1, 0),
    "a4": (1, 1, 0),
    "a5": (2, 2, 0),
}

# Mixed helicity choice that keeps the only plausible activation triad
# a1 + a3 -> a4 nonzero on this support.
CHOSEN_SIGMA: dict[Role, int] = {
    "a1": 1,
    "a2": 1,
    "a3": -1,
    "a4": 1,
    "a5": 1,
}

# Adversarial sign choice that suppresses the desired activation channel.
ALT_SIGMA: dict[Role, int] = {
    "a1": 1,
    "a2": 1,
    "a3": 1,
    "a4": -1,
    "a5": 1,
}

DESIRED_EXACT: dict[Role, set[tuple[str, str]]] = {
    "a1": {("a3", "a4")},
    "a2": {("a1", "a1")},
    "a3": {("a1", "a1"), ("a2", "a3")},
    "a4": {("a1", "a3")},
    "a5": {("a4", "a4")},
}


def dot(a: tuple[complex, complex, complex], b: tuple[complex, complex, complex]) -> complex:
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]


def cross(a: tuple[complex, complex, complex], b: tuple[complex, complex, complex]) -> tuple[complex, complex, complex]:
    ax, ay, az = a
    bx, by, bz = b
    return (
        ay * bz - az * by,
        az * bx - ax * bz,
        ax * by - ay * bx,
    )


def v_add(a: Vec, b: Vec) -> Vec:
    return (a[0] + b[0], a[1] + b[1], a[2] + b[2])


def v_scale(c: int, a: Vec) -> Vec:
    return (c * a[0], c * a[1], c * a[2])


def norm(a: tuple[complex, complex, complex]) -> float:
    return math.sqrt(float((a[0] * a[0].conjugate() + a[1] * a[1].conjugate() + a[2] * a[2].conjugate()).real))


def normalize(a: tuple[complex, complex, complex]) -> tuple[complex, complex, complex]:
    n = norm(a)
    return (a[0] / n, a[1] / n, a[2] / n)


def cscale(c: complex, a: tuple[complex, complex, complex]) -> tuple[complex, complex, complex]:
    return (c * a[0], c * a[1], c * a[2])


def cadd(a: tuple[complex, complex, complex], b: tuple[complex, complex, complex]) -> tuple[complex, complex, complex]:
    return (a[0] + b[0], a[1] + b[1], a[2] + b[2])


def conj(a: tuple[complex, complex, complex]) -> tuple[complex, complex, complex]:
    return (a[0].conjugate(), a[1].conjugate(), a[2].conjugate())


def helical_basis(k: Vec, sigma: int) -> tuple[complex, complex, complex]:
    kh = normalize((complex(k[0]), complex(k[1]), complex(k[2])))
    ref = (0.0 + 0.0j, 0.0 + 0.0j, 1.0 + 0.0j)
    if norm(cross(kh, ref)) < 1e-12:
        ref = (0.0 + 0.0j, 1.0 + 0.0j, 0.0 + 0.0j)
    e1 = normalize(cross(ref, kh))
    e2 = cross(kh, e1)
    return cscale(1.0 / math.sqrt(2.0), cadd(e1, cscale(1j * sigma, e2)))


def helical_coeff(k: Vec, p: Vec, q: Vec, sigma_k: int, sigma_p: int, sigma_q: int) -> complex:
    hk = helical_basis(k, sigma_k)
    hp = helical_basis(p, sigma_p)
    hq = helical_basis(q, sigma_q)
    return -0.25 * (
        sigma_p * math.sqrt(p[0] * p[0] + p[1] * p[1] + p[2] * p[2])
        - sigma_q * math.sqrt(q[0] * q[0] + q[1] * q[1] + q[2] * q[2])
    ) * dot(cross(hp, hq), conj(hk))


@dataclass(frozen=True)
class Mode:
    vec: Vec
    sigma: int
    role: Role
    conjugated: bool

    @property
    def name(self) -> str:
        return ("bar_" if self.conjugated else "") + self.role


def support_modes(k_by_role: dict[Role, Vec], sigma_by_role: dict[Role, int]) -> list[Mode]:
    modes: list[Mode] = []
    for role in ROLES:
        k = k_by_role[role]
        sigma = sigma_by_role[role]
        modes.append(Mode(k, sigma, role, False))
        modes.append(Mode(v_scale(-1, k), -sigma, role, True))
    return modes


def aggregate_internal(k_by_role: dict[Role, Vec], sigma_by_role: dict[Role, int]) -> dict[Role, dict[tuple[str, str], complex]]:
    modes = support_modes(k_by_role, sigma_by_role)
    out: dict[Role, dict[tuple[str, str], complex]] = {role: {} for role in ROLES}
    for target_role in ROLES:
        target = k_by_role[target_role]
        sigma_target = sigma_by_role[target_role]
        for p in modes:
            for q in modes:
                if v_add(p.vec, q.vec) != target:
                    continue
                coeff = helical_coeff(target, p.vec, q.vec, sigma_target, p.sigma, q.sigma)
                if abs(coeff) < 1e-12:
                    continue
                key = (p.name, q.name)
                out[target_role][key] = out[target_role].get(key, 0.0j) + coeff
    return out


def aggregate_external(k_by_role: dict[Role, Vec], sigma_by_role: dict[Role, int]) -> dict[tuple[Vec, int, str, str], complex]:
    modes = support_modes(k_by_role, sigma_by_role)
    active = {mode.vec for mode in modes}
    out: dict[tuple[Vec, int, str, str], complex] = {}
    for p in modes:
        for q in modes:
            target = v_add(p.vec, q.vec)
            if target == (0, 0, 0) or target in active:
                continue
            for sigma_target in (-1, 1):
                coeff = helical_coeff(target, p.vec, q.vec, sigma_target, p.sigma, q.sigma)
                if abs(coeff) < 1e-12:
                    continue
                key = (target, sigma_target, p.name, q.name)
                out[key] = out.get(key, 0.0j) + coeff
    return out


def classify_term(target_role: Role, monomial: tuple[str, str]) -> str:
    if monomial in DESIRED_EXACT[target_role]:
        return "desired"
    plain = tuple(name.replace("bar_", "") for name in monomial)
    if plain in DESIRED_EXACT[target_role]:
        return "conjugate-mismatch"
    return "spectator"


def summary_for_sigma(k_by_role: dict[Role, Vec], sigma_by_role: dict[Role, int]) -> dict[str, float | int]:
    internal = aggregate_internal(k_by_role, sigma_by_role)
    external = aggregate_external(k_by_role, sigma_by_role)
    desired = 0.0
    internal_leak = 0.0
    for target_role, terms in internal.items():
        for monomial, coeff in terms.items():
            if classify_term(target_role, monomial) == "desired":
                desired += abs(coeff)
            else:
                internal_leak += abs(coeff)
    external_leak = sum(abs(coeff) for coeff in external.values())
    return {
        "desired_abs_sum": desired,
        "internal_leak_abs_sum": internal_leak,
        "external_leak_abs_sum": external_leak,
        "internal_term_count": sum(len(terms) for terms in internal.values()),
        "external_term_count": len(external),
    }


def sigma_scan(k_by_role: dict[Role, Vec]) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for pattern in itertools.product((1, -1), repeat=len(ROLES)):
        sigma = dict(zip(ROLES, pattern))
        rows.append({"sigma": sigma, **summary_for_sigma(k_by_role, sigma)})
    rows.sort(
        key=lambda row: (
            0 if row["desired_abs_sum"] else 1,
            row["internal_leak_abs_sum"] + row["external_leak_abs_sum"],
        )
    )
    return rows


def fmt_complex(z: complex) -> str:
    return f"{z.real:.12f}{z.imag:+.12f}j"


def print_internal(name: str, k_by_role: dict[Role, Vec], sigma_by_role: dict[Role, int]) -> None:
    internal = aggregate_internal(k_by_role, sigma_by_role)
    print(f"## {name}: internal equations")
    print(json.dumps({"K": k_by_role, "sigma": sigma_by_role}, indent=2, sort_keys=True))
    for role in ROLES:
        print(f"- target {role} at {k_by_role[role]} with sigma={sigma_by_role[role]}")
        terms = internal[role]
        if not terms:
            print("  (no nonzero internal terms)")
            continue
        for monomial, coeff in sorted(terms.items()):
            print(
                "  "
                + json.dumps(
                    {
                        "monomial": monomial,
                        "coeff": fmt_complex(coeff),
                        "status": classify_term(role, monomial),
                    },
                    sort_keys=True,
                )
            )
    print()


def print_external(name: str, k_by_role: dict[Role, Vec], sigma_by_role: dict[Role, int], limit: int = 20) -> None:
    external = aggregate_external(k_by_role, sigma_by_role)
    items = sorted(external.items(), key=lambda item: abs(item[1]), reverse=True)
    print(f"## {name}: top external emissions")
    for (target, sigma_target, left, right), coeff in items[:limit]:
        print(
            json.dumps(
                {
                    "target": target,
                    "sigma": sigma_target,
                    "monomial": [left, right],
                    "coeff": fmt_complex(coeff),
                    "abs_coeff": round(abs(coeff), 12),
                },
                sort_keys=True,
            )
        )
    print()


def print_scan(k_by_role: dict[Role, Vec], limit: int = 10) -> None:
    print("## helicity scan")
    for row in sigma_scan(k_by_role)[:limit]:
        print(json.dumps(row, sort_keys=True))
    print()


def generic_checks() -> dict[str, object]:
    sample_k = (1, 0, 0)
    self_zero = {}
    for sigma_source in (-1, 1):
        for sigma_target in (-1, 1):
            coeff = helical_coeff(v_scale(2, sample_k), sample_k, sample_k, sigma_target, sigma_source, sigma_source)
            self_zero[f"source={sigma_source},target={sigma_target}"] = fmt_complex(coeff)
    return {
        "self_interaction_coefficients_for_k_plus_k_to_2k": self_zero,
        "amplifier_requires_zero_or_conjugate_leg": "For singleton roles, p+q=k3 with p in {±k2}, q in {±k3} has no exact a2*a3->a3 solution. The only nonzero-wavevector possibility is p=2k3, q=-k3, i.e. a2*bar_a3->a3.",
        "feedback_requires_conjugate_leg": "Combining k4=k1+k3 with target k1 forces k4+(-k3)=k1, so the exact monomial is bar_a3*a4->a1, not a3*a4->a1.",
    }


def main() -> None:
    print("## generic checks")
    print(json.dumps(generic_checks(), indent=2, sort_keys=True))
    print()
    print_internal("chosen", CHOSEN_K, CHOSEN_SIGMA)
    print_external("chosen", CHOSEN_K, CHOSEN_SIGMA)
    print_internal("alternative", CHOSEN_K, ALT_SIGMA)
    print_external("alternative", CHOSEN_K, ALT_SIGMA)
    print_scan(CHOSEN_K)


if __name__ == "__main__":
    main()
