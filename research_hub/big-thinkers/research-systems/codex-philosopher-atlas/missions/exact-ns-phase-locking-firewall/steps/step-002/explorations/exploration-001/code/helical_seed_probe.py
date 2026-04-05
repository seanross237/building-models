#!/usr/bin/env python3
"""Probe one-triad helical coefficient zero patterns for Step-2 seed taxonomy."""

from __future__ import annotations

import itertools
import math
from dataclasses import dataclass
from typing import Iterable

Vec = tuple[float, float, float]


def add(a: Vec, b: Vec) -> Vec:
    return (a[0] + b[0], a[1] + b[1], a[2] + b[2])


def sub(a: Vec, b: Vec) -> Vec:
    return (a[0] - b[0], a[1] - b[1], a[2] - b[2])


def scale(s: complex, v: tuple[complex, complex, complex]) -> tuple[complex, complex, complex]:
    return (s * v[0], s * v[1], s * v[2])


def dot(a: tuple[complex, complex, complex], b: tuple[complex, complex, complex]) -> complex:
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]


def vdot(a: tuple[complex, complex, complex], b: tuple[complex, complex, complex]) -> complex:
    return a[0].conjugate() * b[0] + a[1].conjugate() * b[1] + a[2].conjugate() * b[2]


def cross(a: Vec, b: Vec) -> Vec:
    return (
        a[1] * b[2] - a[2] * b[1],
        a[2] * b[0] - a[0] * b[2],
        a[0] * b[1] - a[1] * b[0],
    )


def norm(v: tuple[complex, complex, complex]) -> float:
    return math.sqrt((abs(v[0]) ** 2) + (abs(v[1]) ** 2) + (abs(v[2]) ** 2))


def normalize(v: Vec) -> Vec:
    n = norm(v)
    if n == 0:
        raise ValueError("zero vector")
    return (v[0] / n, v[1] / n, v[2] / n)


def pick_reference(k: Vec) -> Vec:
    for cand in (
        (0.0, 0.0, 1.0),
        (0.0, 1.0, 0.0),
        (1.0, 0.0, 0.0),
    ):
        if norm(cross(cand, k)) > 1e-12:
            return cand
    raise ValueError(f"could not find reference for {k}")


def helical_mode(k: Vec, sigma: int, ref: Vec | None = None) -> tuple[complex, complex, complex]:
    ref = pick_reference(k) if ref is None else ref
    e1 = normalize(cross(ref, k))
    e2 = normalize(cross(k, e1))
    return (
        (e1[0] + 1j * sigma * e2[0]) / math.sqrt(2.0),
        (e1[1] + 1j * sigma * e2[1]) / math.sqrt(2.0),
        (e1[2] + 1j * sigma * e2[2]) / math.sqrt(2.0),
    )


def projector(k: Vec) -> tuple[tuple[float, float, float], tuple[float, float, float], tuple[float, float, float]]:
    khat = normalize(k)
    return (
        (1.0 - khat[0] * khat[0], -khat[0] * khat[1], -khat[0] * khat[2]),
        (-khat[1] * khat[0], 1.0 - khat[1] * khat[1], -khat[1] * khat[2]),
        (-khat[2] * khat[0], -khat[2] * khat[1], 1.0 - khat[2] * khat[2]),
    )


def matvec(
    m: tuple[tuple[float, float, float], tuple[float, float, float], tuple[float, float, float]],
    v: tuple[complex, complex, complex],
) -> tuple[complex, complex, complex]:
    return (
        m[0][0] * v[0] + m[0][1] * v[1] + m[0][2] * v[2],
        m[1][0] * v[0] + m[1][1] * v[1] + m[1][2] * v[2],
        m[2][0] * v[0] + m[2][1] * v[1] + m[2][2] * v[2],
    )


def ordered_coefficient(
    k: Vec,
    p: Vec,
    q: Vec,
    sig_k: int,
    sig_p: int,
    sig_q: int,
) -> complex:
    hk = helical_mode(k, sig_k)
    hp = helical_mode(p, sig_p)
    hq = helical_mode(q, sig_q)
    term = scale(dot(q, hp), matvec(projector(k), hq))
    return -1j * vdot(hk, term)


@dataclass(frozen=True)
class Triad:
    name: str
    p: tuple[int, int, int]
    q: tuple[int, int, int]

    @property
    def k(self) -> tuple[int, int, int]:
        return (
            self.p[0] + self.q[0],
            self.p[1] + self.q[1],
            self.p[2] + self.q[2],
        )


TRIADS = [
    Triad("right_isosceles", (1, 0, 0), (0, 1, 0)),
    Triad("unequal_noncollinear", (2, 0, 0), (0, 1, 0)),
    Triad("generic_3d", (1, 1, 0), (0, 1, 1)),
    Triad("collinear", (1, 0, 0), (2, 0, 0)),
]


def fmt_sign(s: int) -> str:
    return "+" if s > 0 else "-"


def sign_word(sig: tuple[int, int, int]) -> str:
    return "".join(fmt_sign(s) for s in sig)


def flip_all(sig: tuple[int, int, int]) -> tuple[int, int, int]:
    return (-sig[0], -sig[1], -sig[2])


def swap_inputs(sig: tuple[int, int, int]) -> tuple[int, int, int]:
    return (sig[0], sig[2], sig[1])


def permute(sig: tuple[int, int, int], perm: tuple[int, int, int]) -> tuple[int, int, int]:
    return (sig[perm[0]], sig[perm[1]], sig[perm[2]])


def orbit_partition(
    actions: Iterable,
) -> list[list[tuple[int, int, int]]]:
    universe = {(a, b, c) for a, b, c in itertools.product((1, -1), repeat=3)}
    parts: list[list[tuple[int, int, int]]] = []
    while universe:
        seed = next(iter(universe))
        stack = [seed]
        seen: set[tuple[int, int, int]] = set()
        while stack:
            cur = stack.pop()
            if cur in seen:
                continue
            seen.add(cur)
            for action in actions:
                nxt = action(cur)
                if nxt not in seen:
                    stack.append(nxt)
        parts.append(sorted(seen, reverse=True))
        universe -= seen
    return sorted(parts, key=lambda part: (len(part), [sign_word(x) for x in part]))


def run_probe() -> str:
    lines: list[str] = []
    ordered_parts = orbit_partition((flip_all, swap_inputs))
    orbit_parts = orbit_partition(
        tuple(
            [flip_all]
            + [
                (lambda perm: (lambda sig: permute(sig, perm)))((0, 1, 2)),
                (lambda perm: (lambda sig: permute(sig, perm)))((0, 2, 1)),
                (lambda perm: (lambda sig: permute(sig, perm)))((1, 0, 2)),
                (lambda perm: (lambda sig: permute(sig, perm)))((1, 2, 0)),
                (lambda perm: (lambda sig: permute(sig, perm)))((2, 0, 1)),
                (lambda perm: (lambda sig: permute(sig, perm)))((2, 1, 0)),
            ]
        )
    )
    lines.append("ordered-sign classes (global sign flip + input swap):")
    for part in ordered_parts:
        lines.append("  " + ", ".join(sign_word(sig) for sig in part))
    lines.append("")
    lines.append("orbit-sign classes (global sign flip + full mode permutation):")
    for part in orbit_parts:
        lines.append("  " + ", ".join(sign_word(sig) for sig in part))
    lines.append("")
    for triad in TRIADS:
        p = tuple(float(x) for x in triad.p)
        q = tuple(float(x) for x in triad.q)
        k = tuple(float(x) for x in triad.k)
        area = norm(cross(p, q))
        lines.append(
            f"triad={triad.name} p={triad.p} q={triad.q} k={triad.k} area={area:.6f}"
        )
        mags: dict[tuple[int, int, int], float] = {}
        for sig_k, sig_p, sig_q in itertools.product((1, -1), repeat=3):
            coeff = ordered_coefficient(k, p, q, sig_k, sig_p, sig_q)
            mag = abs(coeff)
            mags[(sig_k, sig_p, sig_q)] = mag
            lines.append(
                "  signs="
                f"{fmt_sign(sig_k)}{fmt_sign(sig_p)}{fmt_sign(sig_q)} "
                f"coeff={coeff.real:+.12f}{coeff.imag:+.12f}j "
                f"|coeff|={mag:.12f}"
            )
        nonzero = sum(m > 1e-10 for m in mags.values())
        lines.append(f"  nonzero_sign_triples={nonzero}/8")
        lines.append("")
    return "\n".join(lines)


if __name__ == "__main__":
    print(run_probe())
