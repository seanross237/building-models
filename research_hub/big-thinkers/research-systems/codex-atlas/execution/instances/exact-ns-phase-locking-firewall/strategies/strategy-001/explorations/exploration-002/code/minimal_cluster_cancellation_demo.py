#!/usr/bin/env python3
"""Minimal exact-support audit for exploration 002.

This script exhibits the smallest explicit exact-helical cluster I found with
two distinct ordered triad inputs feeding the same target mode. It then shows:

1. on a single active triad, the coherence ratio C_l is forced to +/-1;
2. on the two-input cluster, one can choose exact mode phases so that the two
   transfer contributions have opposite signs;
3. by tuning the source amplitudes, the net receiver-band gain stays positive
   while C_l becomes arbitrarily small.
"""

from __future__ import annotations

import itertools
import math


Vec = tuple[int, int, int]


def v_add(a: Vec, b: Vec) -> Vec:
    return (a[0] + b[0], a[1] + b[1], a[2] + b[2])


def dot(a, b) -> complex:
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]


def cross(a, b):
    ax, ay, az = a
    bx, by, bz = b
    return (
        ay * bz - az * by,
        az * bx - ax * bz,
        ax * by - ay * bx,
    )


def norm(a) -> float:
    return math.sqrt(float((a[0] * a[0].conjugate() + a[1] * a[1].conjugate() + a[2] * a[2].conjugate()).real))


def normalize(a):
    n = norm(a)
    return (a[0] / n, a[1] / n, a[2] / n)


def cscale(c: complex, a):
    return (c * a[0], c * a[1], c * a[2])


def cadd(a, b):
    return (a[0] + b[0], a[1] + b[1], a[2] + b[2])


def conj(a):
    return (a[0].conjugate(), a[1].conjugate(), a[2].conjugate())


def helical_basis(k: Vec, sigma: int):
    kh = normalize((complex(k[0]), complex(k[1]), complex(k[2])))
    ref = (0.0 + 0.0j, 0.0 + 0.0j, 1.0 + 0.0j)
    if norm(cross(kh, ref)) < 1e-12:
        ref = (0.0 + 0.0j, 1.0 + 0.0j, 0.0 + 0.0j)
    e1 = normalize(cross(ref, kh))
    e2 = cross(kh, e1)
    return cscale(1.0 / math.sqrt(2.0), cadd(e1, cscale(1j * sigma, e2)))


def k_norm(k: Vec) -> float:
    return math.sqrt(k[0] * k[0] + k[1] * k[1] + k[2] * k[2])


def helical_coeff(k: Vec, p: Vec, q: Vec, sigma_k: int, sigma_p: int, sigma_q: int) -> complex:
    hk = helical_basis(k, sigma_k)
    hp = helical_basis(p, sigma_p)
    hq = helical_basis(q, sigma_q)
    return -0.25 * (sigma_p * k_norm(p) - sigma_q * k_norm(q)) * dot(cross(hp, hq), conj(hk))


TARGET: Vec = (2, 1, 0)
PAIR1 = ((1, 0, 0), (1, 1, 0))
PAIR2 = ((2, 0, 0), (0, 1, 0))


def best_sign_pattern():
    best = None
    for sigma_k, sigma_p1, sigma_q1, sigma_p2, sigma_q2 in itertools.product((1, -1), repeat=5):
        c1 = helical_coeff(TARGET, PAIR1[0], PAIR1[1], sigma_k, sigma_p1, sigma_q1)
        c2 = helical_coeff(TARGET, PAIR2[0], PAIR2[1], sigma_k, sigma_p2, sigma_q2)
        if abs(c1) < 1e-12 or abs(c2) < 1e-12:
            continue
        score = abs(c1) + abs(c2)
        row = {
            "sigmas": (sigma_k, sigma_p1, sigma_q1, sigma_p2, sigma_q2),
            "c1": c1,
            "c2": c2,
            "score": score,
        }
        if best is None or row["score"] > best["score"]:
            best = row
    return best


def format_complex(z: complex) -> str:
    return f"{z.real:.12f}{z.imag:+.12f}j"


def main() -> None:
    best = best_sign_pattern()
    if best is None:
        raise SystemExit("No sign pattern found with two nonzero transfer inputs.")

    sigma_k, sigma_p1, sigma_q1, sigma_p2, sigma_q2 = best["sigmas"]
    c1 = best["c1"]
    c2 = best["c2"]

    print("# Minimal cluster")
    print(f"target k = {TARGET}")
    print(f"pair 1  = {PAIR1[0]} + {PAIR1[1]}")
    print(f"pair 2  = {PAIR2[0]} + {PAIR2[1]}")
    print(f"best sign pattern = {best['sigmas']}")
    print(f"coeff 1 = {format_complex(c1)}  |c1|={abs(c1):.12f}")
    print(f"coeff 2 = {format_complex(c2)}  |c2|={abs(c2):.12f}")
    print()

    print("# Single-triad observation")
    print("For one active transfer term T, C_l = T/|T| = +/-1 exactly.")
    print()

    target_amp = 1.0
    p1_amp = 1.0
    q1_amp = 1.0
    w1 = abs(c1) * target_amp * p1_amp * q1_amp

    # Tune the second channel to make the net transfer positive but arbitrarily small.
    eps_values = [1e-1, 1e-2, 1e-3, 1e-4]
    print("# Two-channel cancellation family")
    print("We choose phases so Theta_1 = 0 and Theta_2 = pi.")
    print("Then T1 = +W1 and T2 = -W2 with exact mode phases:")
    print(f"phi_target = 0")
    print(f"phi_p1 = 0, phi_q1 = {-math.atan2(c1.imag, c1.real):.12f}")
    print(f"phi_p2 = 0, phi_q2 = {math.pi - math.atan2(c2.imag, c2.real):.12f}")
    print()

    for eps in eps_values:
        desired_w2 = w1 - eps
        q2_amp = desired_w2 / abs(c2)
        t1 = w1
        t2 = -desired_w2
        net = t1 + t2
        coh = net / (abs(t1) + abs(t2))
        print(
            f"eps={eps:.1e}  "
            f"W1={w1:.12f}  W2={desired_w2:.12f}  "
            f"q2_amp={q2_amp:.12f}  net={net:.12f}  C_l={coh:.12e}"
        )

    print()
    print("# Conclusion")
    print(
        "Once two exact transfer terms feed the same receiver mode, exact phase tuning keeps "
        "the net receiver-band gain positive while driving C_l arbitrarily close to zero."
    )


if __name__ == "__main__":
    main()
