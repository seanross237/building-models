#!/usr/bin/env python3
"""Representative closure audit for the third-budget three-arm seed."""

from __future__ import annotations

import itertools
import json
import math
from pathlib import Path


ROOT = Path(
    "/Users/seanross/kingdom_of_god/home-base/research_hub/big-thinkers/"
    "codex-philosopher-atlas/missions/exact-ns-phase-locking-firewall/steps/"
    "step-004/explorations/exploration-002/code/output"
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


FAMILIES = {
    "three_arm_generic": {
        "description": (
            "Single repeated orbit a, with three distinct partner shells and "
            "no low-dimensional coincidence among the partner orbits."
        ),
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
        "preferred_pairs": [
            ("p", "c"),
            ("q", "d"),
            ("r", "b"),
        ],
    },
    "three_arm_bridge_guard": {
        "description": (
            "Single repeated orbit a with the low-dimensional coincidence "
            "d = b + c, so p + c lands on the on-budget orbit r."
        ),
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
        "preferred_pairs": [
            ("p", "c"),
            ("r", "b"),
            ("q", "d"),
        ],
    },
}


def triad_live(seed_triads, modes, signs):
    reports = []
    live = True
    for target, left, right in seed_triads:
        coeff = projected_helical_coefficient(
            modes[target],
            modes[left],
            modes[right],
            signs[target],
            signs[left],
            signs[right],
        )
        reports.append({"triad": [target, left, right], "coefficient": coeff})
        if abs(coeff) <= TOL:
            live = False
    return live, reports


def new_target_reports(base_modes, signs):
    active_modes = expand_support(base_modes)
    support_orbits = {canonical_orbit(vector) for vector in base_modes.values()}
    current = {(canonical_orbit(vector), signs[label]) for label, vector in base_modes.items()}

    on_budget = []
    spill = []
    seen_on_budget = set()
    seen_spill = set()

    for left, right in itertools.product(sorted(active_modes), repeat=2):
        target = add(active_modes[left], active_modes[right])
        if norm(target) <= TOL:
            continue
        target_orbit = canonical_orbit(target)
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
            event = {
                "pair": [left, right],
                "target": target,
                "orbit": target_orbit,
                "target_sigma": sign_name(tau),
                "coefficient": coeff,
                "target_norm": norm(target),
            }
            key = (target_orbit, tau)
            if target_orbit in support_orbits:
                if key in current or key in seen_on_budget:
                    continue
                seen_on_budget.add(key)
                on_budget.append(event)
            else:
                if key in seen_spill:
                    continue
                seen_spill.add(key)
                spill.append(event)

    on_budget.sort(key=lambda item: (item["target_norm"], item["orbit"], tuple(item["pair"])))
    spill.sort(key=lambda item: (item["target_norm"], item["orbit"], tuple(item["pair"])))
    return {"on_budget": on_budget, "spill": spill}


def preferred_pair_checks(payload, signs):
    checks = []
    modes = expand_support(payload["base_modes"])
    for left, right in payload["preferred_pairs"]:
        target = add(modes[left], modes[right])
        coeffs = {}
        for tau in (+1, -1):
            coeffs[sign_name(tau)] = projected_helical_coefficient(
                target,
                modes[left],
                modes[right],
                tau,
                sign_for_label(left, signs),
                sign_for_label(right, signs),
            )
        checks.append(
            {
                "pair": [left, right],
                "target": target,
                "orbit": canonical_orbit(target),
                "coefficients": coeffs,
            }
        )
    return checks


def audit_family(name, payload):
    labels = sorted(payload["base_modes"])
    assignments = []
    live_assignments = 0
    spill_assignments = 0
    on_budget_assignments = 0

    for values in itertools.product((+1, -1), repeat=len(labels)):
        signs = dict(zip(labels, values))
        live, seed_report = triad_live(
            payload["seed_triads"], payload["base_modes"], signs
        )
        pass_one = new_target_reports(payload["base_modes"], signs)
        if live:
            live_assignments += 1
            if pass_one["spill"]:
                spill_assignments += 1
            if pass_one["on_budget"]:
                on_budget_assignments += 1
        assignments.append(
            {
                "signs": {label: sign_name(sign) for label, sign in signs.items()},
                "live_seed": live,
                "seed_triads": seed_report,
                "candidate_pair_checks": preferred_pair_checks(payload, signs),
                "new_on_budget_sectors": pass_one["on_budget"],
                "spill_sectors": pass_one["spill"],
            }
        )

    representative = next(item for item in assignments if item["live_seed"])
    return {
        "family": name,
        "description": payload["description"],
        "positive_mode_labels": labels,
        "total_assignments": len(assignments),
        "live_seed_assignments": live_assignments,
        "assignments_with_on_budget_new_sectors": on_budget_assignments,
        "assignments_with_spill": spill_assignments,
        "representative_live_assignment": representative,
        "assignments": assignments,
    }


def main():
    ROOT.mkdir(parents=True, exist_ok=True)
    reports = [audit_family(name, payload) for name, payload in FAMILIES.items()]
    (ROOT / "three_triad_closure_audit.json").write_text(
        json.dumps(to_serializable(reports), indent=2) + "\n"
    )

    lines = []
    for report in reports:
        lines.append(f"family={report['family']}")
        lines.append(f"  live_seed_assignments={report['live_seed_assignments']}/{report['total_assignments']}")
        lines.append(
            "  assignments_with_on_budget_new_sectors="
            f"{report['assignments_with_on_budget_new_sectors']}/{report['live_seed_assignments']}"
        )
        lines.append(
            "  assignments_with_spill="
            f"{report['assignments_with_spill']}/{report['live_seed_assignments']}"
        )
        rep = report["representative_live_assignment"]
        checks = rep["candidate_pair_checks"]
        for check in checks:
            plus_abs = abs(check["coefficients"]["+"])
            minus_abs = abs(check["coefficients"]["-"])
            lines.append(
                "  pair="
                f"{tuple(check['pair'])} -> orbit={tuple(check['orbit'])} "
                f"|C_+|={plus_abs:.6f} |C_-|={minus_abs:.6f}"
            )
        first_spill = rep["spill_sectors"][0]
        lines.append(
            "  representative_first_spill="
            f"{tuple(first_spill['pair'])} -> {tuple(first_spill['target'])}"
        )
    (ROOT / "three_triad_closure_audit_summary.txt").write_text(
        "\n".join(lines) + "\n"
    )


if __name__ == "__main__":
    main()
