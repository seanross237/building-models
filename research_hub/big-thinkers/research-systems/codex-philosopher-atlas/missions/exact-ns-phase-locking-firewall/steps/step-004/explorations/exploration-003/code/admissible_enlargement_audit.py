#!/usr/bin/env python3
"""Admissible enlargement checks for the Step-4 third-budget pseudo-survivor."""

from __future__ import annotations

import itertools
import json
import math
from pathlib import Path


ROOT = Path(
    "/Users/seanross/kingdom_of_god/home-base/research_hub/big-thinkers/"
    "codex-philosopher-atlas/missions/exact-ns-phase-locking-firewall/steps/"
    "step-004/explorations/exploration-003/code/output"
)
TOL = 1e-10


def add(a, b):
    return tuple(x + y for x, y in zip(a, b))


def negate(v):
    return tuple(-x for x in v)


def dot(a, b):
    return sum(x * y for x, y in zip(a, b))


def vdot(a, b):
    return sum(x.conjugate() * y for x, y in zip(a, b))


def cross(a, b):
    return (
        a[1] * b[2] - a[2] * b[1],
        a[2] * b[0] - a[0] * b[2],
        a[0] * b[1] - a[1] * b[0],
    )


def norm(v):
    return math.sqrt(sum(abs(x) ** 2 for x in v))


def normalize(v):
    n = norm(v)
    if n == 0:
        raise ValueError("zero vector")
    return tuple(x / n for x in v)


def matvec(m, v):
    return tuple(sum(m[i][j] * v[j] for j in range(3)) for i in range(3))


def canonical_orbit(v):
    neg_v = negate(v)
    return tuple(v) if tuple(v) <= tuple(neg_v) else tuple(neg_v)


def sign_name(sig):
    return "+" if sig > 0 else "-"


def expand_support(base_modes):
    modes = dict(base_modes)
    for label, vector in list(base_modes.items()):
        modes[f"-{label}"] = negate(vector)
    return modes


def sign_for_label(label, signs):
    return signs[label[1:]] if label.startswith("-") else signs[label]


def helical_basis(k, sigma):
    khat = normalize(k)
    ref = (0.0, 0.0, 1.0)
    if abs(dot(khat, ref)) > 0.9:
        ref = (0.0, 1.0, 0.0)
    e1 = normalize(cross(ref, khat))
    e2 = normalize(cross(khat, e1))
    return tuple((e1[i] + 1j * sigma * e2[i]) / math.sqrt(2.0) for i in range(3))


def projected_helical_coefficient(target, source_a, source_b, sig_target, sig_a, sig_b):
    ha = helical_basis(source_a, sig_a)
    hb = helical_basis(source_b, sig_b)
    ht = helical_basis(target, sig_target)
    khat = normalize(target)
    proj = tuple(
        tuple((1.0 if i == j else 0.0) - khat[i] * khat[j] for j in range(3))
        for i in range(3)
    )
    projected_hb = matvec(proj, hb)
    term = tuple(dot(source_b, ha) * entry for entry in projected_hb)
    return -1j * vdot(ht, term)


def triad_live(seed_triads, modes, signs):
    for target, left, right in seed_triads:
        coeff = projected_helical_coefficient(
            modes[target],
            modes[left],
            modes[right],
            signs[target],
            signs[left],
            signs[right],
        )
        if abs(coeff) <= TOL:
            return False
    return True


def new_target_reports(base_modes, signs):
    active_modes = expand_support(base_modes)
    support_orbits = {canonical_orbit(vector) for vector in base_modes.values()}
    reports = []
    seen = set()

    for left, right in itertools.product(sorted(active_modes), repeat=2):
        target = add(active_modes[left], active_modes[right])
        if norm(target) <= TOL:
            continue
        target_orbit = canonical_orbit(target)
        if target_orbit in support_orbits:
            continue
        for tau in (+1, -1):
            coeff = projected_helical_coefficient(
                target,
                active_modes[left],
                active_modes[right],
                tau,
                sign_for_label(left, signs),
                sign_for_label(right, signs),
            )
            if abs(coeff) <= TOL:
                continue
            key = (target_orbit, tau)
            if key in seen:
                continue
            seen.add(key)
            reports.append(
                {
                    "pair": [left, right],
                    "target": target,
                    "orbit": target_orbit,
                    "target_sigma": sign_name(tau),
                    "coefficient": coeff,
                    "target_norm": norm(target),
                }
            )
    reports.sort(key=lambda item: (item["target_norm"], item["orbit"], tuple(item["pair"])))
    return reports


FAMILIES = {
    "three_arm_generic": {
        "base_modes": {
            "a": (1.0, 0.0, 0.0),
            "b": (0.0, 1.0, 0.0),
            "c": (0.0, 0.0, 2.0),
            "d": (0.0, 2.0, 1.0),
            "p": (1.0, 1.0, 0.0),
            "q": (1.0, 0.0, 2.0),
            "r": (1.0, 2.0, 1.0),
        },
        "seed_triads": [
            ("p", "a", "b"),
            ("q", "a", "c"),
            ("r", "a", "d"),
        ],
        "preferred_enlargement_pair": ("p", "c"),
    },
    "three_arm_bridge_guard": {
        "base_modes": {
            "a": (1.0, 0.0, 0.0),
            "b": (0.0, 1.0, 0.0),
            "c": (0.0, 0.0, 1.0),
            "d": (0.0, 1.0, 1.0),
            "p": (1.0, 1.0, 0.0),
            "q": (1.0, 0.0, 1.0),
            "r": (1.0, 1.0, 1.0),
        },
        "seed_triads": [
            ("p", "a", "b"),
            ("q", "a", "c"),
            ("r", "a", "d"),
        ],
        "preferred_enlargement_pair": ("r", "b"),
    },
}


def choose_enlargement(payload, reports):
    modes = expand_support(payload["base_modes"])
    preferred = tuple(payload["preferred_enlargement_pair"])
    preferred_target = canonical_orbit(add(modes[preferred[0]], modes[preferred[1]]))
    for report in reports:
        if tuple(report["orbit"]) == tuple(preferred_target):
            return report
    for report in reports:
        if tuple(report["pair"]) == preferred:
            return report
    return reports[0] if reports else None


def choose_target_sign(report):
    return +1 if report["target_sigma"] == "+" else -1


def distinct_label(base_modes):
    index = 1
    while True:
        label = f"g{index}"
        if label not in base_modes:
            return label
        index += 1


def to_serializable(value):
    if isinstance(value, dict):
        return {k: to_serializable(v) for k, v in value.items()}
    if isinstance(value, list):
        return [to_serializable(v) for v in value]
    if isinstance(value, tuple):
        return [to_serializable(v) for v in value]
    if isinstance(value, complex):
        return {"re": value.real, "im": value.imag, "abs": abs(value)}
    return value


def audit_family(name, payload):
    labels = sorted(payload["base_modes"])
    assignments = []
    live_assignments = 0
    force_assignments = 0
    enlargement_failure_assignments = 0

    for values in itertools.product((+1, -1), repeat=len(labels)):
        signs = dict(zip(labels, values))
        live = triad_live(payload["seed_triads"], payload["base_modes"], signs)
        first_pass = new_target_reports(payload["base_modes"], signs)
        chosen = choose_enlargement(payload, first_pass)
        residual = []
        if chosen is not None:
            enlarged_base = dict(payload["base_modes"])
            new_label = distinct_label(enlarged_base)
            enlarged_base[new_label] = chosen["orbit"]
            enlarged_signs = dict(signs)
            enlarged_signs[new_label] = choose_target_sign(chosen)
            residual = new_target_reports(enlarged_base, enlarged_signs)

        if live:
            live_assignments += 1
            if first_pass:
                force_assignments += 1
            if residual:
                enlargement_failure_assignments += 1

        assignments.append(
            {
                "signs": {label: sign_name(sign) for label, sign in signs.items()},
                "live_seed": live,
                "first_pass_new_targets": first_pass,
                "chosen_enlargement": chosen,
                "residual_new_targets_after_enlargement": residual,
                "enlargement_failure": bool(residual),
            }
        )

    representative = next(item for item in assignments if item["live_seed"])
    return {
        "family": name,
        "positive_mode_labels": labels,
        "total_assignments": len(assignments),
        "live_seed_assignments": live_assignments,
        "first_pass_force_assignments": force_assignments,
        "enlargement_failure_assignments": enlargement_failure_assignments,
        "representative_live_assignment": representative,
        "assignments": assignments,
    }


def main():
    ROOT.mkdir(parents=True, exist_ok=True)
    reports = [audit_family(name, payload) for name, payload in FAMILIES.items()]
    (ROOT / "admissible_enlargement_audit.json").write_text(
        json.dumps(to_serializable(reports), indent=2) + "\n"
    )

    lines = []
    for report in reports:
        lines.append(f"family={report['family']}")
        lines.append(f"  live_seed_assignments={report['live_seed_assignments']}/{report['total_assignments']}")
        lines.append(
            "  first_pass_force_assignments="
            f"{report['first_pass_force_assignments']}/{report['live_seed_assignments']}"
        )
        lines.append(
            "  enlargement_failure_assignments="
            f"{report['enlargement_failure_assignments']}/{report['live_seed_assignments']}"
        )
        rep = report["representative_live_assignment"]
        chosen = rep["chosen_enlargement"]
        residual = rep["residual_new_targets_after_enlargement"][0]
        lines.append(
            "  chosen_enlargement="
            f"{tuple(chosen['pair'])} -> {tuple(chosen['target'])}"
        )
        lines.append(
            "  residual_target_after_enlargement="
            f"{tuple(residual['pair'])} -> {tuple(residual['target'])}"
        )
    (ROOT / "admissible_enlargement_audit_summary.txt").write_text(
        "\n".join(lines) + "\n"
    )


if __name__ == "__main__":
    main()
