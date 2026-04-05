#!/usr/bin/env python3
"""Minimal exact-support audit for C_l and E_l^transfer.

This script fixes the smallest connected two-triad helical cluster needed for a
nontrivial coherence-defect ratio:

  k1 = (1,0,0), k2 = (0,1,0), k3 = (0,0,1),
  k4 = k1 + k2 = (1,1,0), k5 = k1 + k3 = (1,0,1).

It then computes:

1. the exact internal helical coefficients on the sign-closed support,
2. the receiver-band transfer identity for the two active interface triads,
3. the low-coherence cancellation family

      T4 = W,
      T5 = -W cos(eps),
      C_l = (T4 + T5) / (|T4| + |T5|) = tan^2(eps/2),

   with exact coefficient values for the chosen cluster,
4. the external emissions that show the support is not exact-NS isolated.

The point of the computation is structural: a single exact triad forces
|C_l| = 1 when active, while the first honest two-triad cluster already lets
the normalized coherence defect stay arbitrarily small at the same time that
the net receiver-band transfer stays positive.
"""

from __future__ import annotations

import cmath
import math
from collections import defaultdict
from dataclasses import dataclass


Role = str
Vec = tuple[int, int, int]


ROLES: tuple[Role, ...] = ("a1", "a2", "a3", "a4", "a5")

K_BY_ROLE: dict[Role, Vec] = {
    "a1": (1, 0, 0),
    "a2": (0, 1, 0),
    "a3": (0, 0, 1),
    "a4": (1, 1, 0),
    "a5": (1, 0, 1),
}

# One symmetric helicity assignment with both receiver equations active and
# equal-magnitude coefficients.
SIGMA_BY_ROLE: dict[Role, int] = {
    "a1": -1,
    "a2": 1,
    "a3": 1,
    "a4": 1,
    "a5": -1,
}


def dot(
    a: tuple[complex, complex, complex], b: tuple[complex, complex, complex]
) -> complex:
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]


def cross(
    a: tuple[complex, complex, complex], b: tuple[complex, complex, complex]
) -> tuple[complex, complex, complex]:
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
    return math.sqrt(
        float(
            (
                a[0] * a[0].conjugate()
                + a[1] * a[1].conjugate()
                + a[2] * a[2].conjugate()
            ).real
        )
    )


def normalize(
    a: tuple[complex, complex, complex]
) -> tuple[complex, complex, complex]:
    n = norm(a)
    return (a[0] / n, a[1] / n, a[2] / n)


def cscale(
    c: complex, a: tuple[complex, complex, complex]
) -> tuple[complex, complex, complex]:
    return (c * a[0], c * a[1], c * a[2])


def cadd(
    a: tuple[complex, complex, complex], b: tuple[complex, complex, complex]
) -> tuple[complex, complex, complex]:
    return (a[0] + b[0], a[1] + b[1], a[2] + b[2])


def conj(
    a: tuple[complex, complex, complex]
) -> tuple[complex, complex, complex]:
    return (a[0].conjugate(), a[1].conjugate(), a[2].conjugate())


def helical_basis(k: Vec, sigma: int) -> tuple[complex, complex, complex]:
    kh = normalize((complex(k[0]), complex(k[1]), complex(k[2])))
    ref = (0.0 + 0.0j, 0.0 + 0.0j, 1.0 + 0.0j)
    if norm(cross(kh, ref)) < 1e-12:
        ref = (0.0 + 0.0j, 1.0 + 0.0j, 0.0 + 0.0j)
    e1 = normalize(cross(ref, kh))
    e2 = cross(kh, e1)
    return cscale(1.0 / math.sqrt(2.0), cadd(e1, cscale(1j * sigma, e2)))


def helical_coeff(
    k: Vec, p: Vec, q: Vec, sigma_k: int, sigma_p: int, sigma_q: int
) -> complex:
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


def support_modes() -> list[Mode]:
    modes: list[Mode] = []
    for role in ROLES:
        k = K_BY_ROLE[role]
        sigma = SIGMA_BY_ROLE[role]
        modes.append(Mode(k, sigma, role, False))
        modes.append(Mode(v_scale(-1, k), -sigma, role, True))
    return modes


def aggregate_internal() -> dict[Role, dict[tuple[str, str], complex]]:
    modes = support_modes()
    out: dict[Role, dict[tuple[str, str], complex]] = {
        role: defaultdict(complex) for role in ROLES
    }
    for target_role in ROLES:
        target = K_BY_ROLE[target_role]
        sigma_target = SIGMA_BY_ROLE[target_role]
        for p in modes:
            for q in modes:
                if v_add(p.vec, q.vec) != target:
                    continue
                coeff = helical_coeff(
                    target, p.vec, q.vec, sigma_target, p.sigma, q.sigma
                )
                if abs(coeff) < 1e-12:
                    continue
                out[target_role][(p.name, q.name)] += coeff
    return out


def aggregate_external() -> dict[tuple[Vec, int], complex]:
    modes = support_modes()
    active = {mode.vec for mode in modes}
    out: dict[tuple[Vec, int], complex] = defaultdict(complex)
    for p in modes:
        for q in modes:
            target = v_add(p.vec, q.vec)
            if target == (0, 0, 0) or target in active:
                continue
            for sigma_target in (-1, 1):
                coeff = helical_coeff(
                    target, p.vec, q.vec, sigma_target, p.sigma, q.sigma
                )
                if abs(coeff) < 1e-12:
                    continue
                out[(target, sigma_target)] += coeff
    return out


def receiver_coefficients(
    internal: dict[Role, dict[tuple[str, str], complex]]
) -> tuple[complex, complex]:
    c4 = internal["a4"][("a1", "a2")] + internal["a4"][("a2", "a1")]
    c5 = internal["a5"][("a1", "a3")] + internal["a5"][("a3", "a1")]
    return c4, c5


def single_triad_ratio(sign: int) -> float:
    return float(sign)


def cancellation_family(radius: float, eps: float, coeff_abs: float) -> dict[str, float]:
    weight = 2.0 * coeff_abs * radius**3
    t4 = weight
    t5 = -weight * math.cos(eps)
    numerator = t4 + t5
    denominator = abs(t4) + abs(t5)
    return {
        "radius": radius,
        "eps": eps,
        "weight": weight,
        "T4": t4,
        "T5": t5,
        "net_transfer": numerator,
        "abs_transfer_sum": denominator,
        "C_l": numerator / denominator,
        "tan_sq_half_eps": math.tan(0.5 * eps) ** 2,
    }


def phase_assignment(eps: float) -> dict[str, float]:
    # With coefficient phase -pi/2 in both receiver equations, these modal
    # phases realize Theta_4 = 0 and Theta_5 = pi - eps in the cos-form
    # T = W cos(Theta).
    return {
        "phi1": 0.0,
        "phi2": 0.0,
        "phi3": 0.0,
        "phi4": -0.5 * math.pi,
        "phi5": 0.5 * math.pi - eps,
    }


def main() -> None:
    internal = aggregate_internal()
    external = aggregate_external()
    c4, c5 = receiver_coefficients(internal)

    print("# Minimal exact cluster")
    print("K =", K_BY_ROLE)
    print("sigma =", SIGMA_BY_ROLE)
    print()

    print("# Internal helical ledger")
    for role in ROLES:
        terms = internal[role]
        if not terms:
            continue
        print(f"{role}:")
        for monomial, coeff in sorted(terms.items()):
            print(f"  {monomial}: {coeff.real:+.12f}{coeff.imag:+.12f}j")
    print()

    print("# Receiver equations")
    print(f"c4 = {c4.real:+.12f}{c4.imag:+.12f}j")
    print(f"c5 = {c5.real:+.12f}{c5.imag:+.12f}j")
    print(
        "d/dt a4 = c4 * a1 * a2, d/dt a5 = c5 * a1 * a3, "
        "with |c4| = |c5| =",
        f"{abs(c4):.12f}",
    )
    print(
        "Single active triad ratio:",
        "C_l = sign(T_tau,l) in {+1, -1} whenever T_tau,l != 0",
    )
    print()

    print("# Low-coherence cancellation family")
    print(
        "Take |a1| = |a2| = |a3| = |a4| = |a5| = R and set phases",
        phase_assignment(0.1),
        "for the sample eps = 0.1 case.",
    )
    for eps in (0.1, 0.05, 0.02, 0.01):
        row = cancellation_family(radius=10.0, eps=eps, coeff_abs=abs(c4))
        print(
            "eps = {eps:.3f}: T4 = {T4:.12f}, T5 = {T5:.12f}, "
            "net = {net_transfer:.12f}, C_l = {C_l:.12e}, "
            "tan^2(eps/2) = {tan_sq_half_eps:.12e}".format(**row)
        )
    print()

    print("# External emissions")
    print("external target count =", len(external))
    for (target, sigma_target), coeff in sorted(
        external.items(), key=lambda item: abs(item[1]), reverse=True
    )[:10]:
        print(
            f"  target={target}, sigma={sigma_target}: "
            f"{coeff.real:+.12f}{coeff.imag:+.12f}j"
        )


if __name__ == "__main__":
    main()
