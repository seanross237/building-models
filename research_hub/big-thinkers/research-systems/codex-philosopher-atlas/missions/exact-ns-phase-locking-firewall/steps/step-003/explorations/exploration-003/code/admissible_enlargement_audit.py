#!/usr/bin/env python3
"""Representative admissible-enlargement checks for Step-3 exploration 003."""

from __future__ import annotations

import itertools
import json
import math
from pathlib import Path


ROOT = Path(
    "/Users/seanross/kingdom_of_god/home-base/research_hub/big-thinkers/"
    "codex-philosopher-atlas/missions/exact-ns-phase-locking-firewall/steps/"
    "step-003/explorations/exploration-003/code/output"
)
TOL = 1e-10


def norm(v):
    return math.sqrt(sum(abs(x) ** 2 for x in v))


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


def scale(s, v):
    return tuple(s * x for x in v)


def negate(v):
    return tuple(-x for x in v)


def normalize(v):
    n = norm(v)
    if n == 0:
        raise ValueError("zero vector")
    return tuple(x / n for x in v)


def matvec(m, v):
    return tuple(sum(m[i][j] * v[j] for j in range(3)) for i in range(3))


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
    term = scale(dot(source_b, ha), projected_hb)
    return -1j * vdot(ht, term)


def sign_name(sig):
    return "+" if sig > 0 else "-"


def canonical_orbit(v):
    neg = negate(v)
    return tuple(v) if tuple(v) <= tuple(neg) else tuple(neg)


FAMILIES = {
    "generic_fan": {
        "base_modes": {
            "a": (1.0, 0.0, 0.0),
            "b": (0.0, 1.0, 0.0),
            "c": (0.0, 0.0, 1.0),
            "d": (1.0, 1.0, 0.0),
            "e": (1.0, 0.0, 1.0),
        },
        "seed_triads": [
            ("d", "a", "b"),
            ("e", "a", "c"),
        ],
    },
    "mirror_parallelogram": {
        "base_modes": {
            "a": (1.0, 0.0, 0.0),
            "b": (0.0, 1.0, 0.0),
            "d": (1.0, 1.0, 0.0),
            "e": (1.0, -1.0, 0.0),
        },
        "seed_triads": [
            ("d", "a", "b"),
            ("e", "a", "-b"),
        ],
    },
    "generic_fan_collinear": {
        "base_modes": {
            "a": (1.0, 0.0, 0.0),
            "b": (0.0, 1.0, 0.0),
            "c": (0.0, 2.0, 0.0),
            "d": (1.0, 1.0, 0.0),
            "e": (1.0, 2.0, 0.0),
        },
        "seed_triads": [
            ("d", "a", "b"),
            ("e", "a", "c"),
        ],
    },
    "edge_overlap_chain": {
        "base_modes": {
            "a": (1.0, 0.0, 0.0),
            "b": (0.0, 1.0, 0.0),
            "d": (1.0, 1.0, 0.0),
            "e": (2.0, 1.0, 0.0),
        },
        "seed_triads": [
            ("d", "a", "b"),
            ("e", "a", "d"),
        ],
    },
}


def expand_support(base_modes):
    modes = dict(base_modes)
    for label, vector in list(base_modes.items()):
        neg_label = f"-{label}"
        if neg_label not in modes:
            modes[neg_label] = negate(vector)
    return modes


def sign_for_label(label, signs):
    return signs[label[1:]] if label.startswith("-") else signs[label]


def triad_live(seed_triads, modes, signs):
    reports = []
    live = True
    for target, left, right in seed_triads:
        coeffs = {}
        for tau in (+1, -1):
            coeffs[sign_name(tau)] = projected_helical_coefficient(
                modes[target],
                modes[left],
                modes[right],
                tau,
                sign_for_label(left, signs),
                sign_for_label(right, signs),
            )
        reports.append(
            {
                "triad": [target, left, right],
                "coefficients": coeffs,
            }
        )
        if max(abs(x) for x in coeffs.values()) <= TOL:
            live = False
    return live, reports


def new_target_reports(active_modes, signs):
    support_orbits = {canonical_orbit(vector) for vector in active_modes.values()}
    reports = []
    seen = set()
    labels = sorted(active_modes)
    for left in labels:
        for right in labels:
            target = tuple(active_modes[left][i] + active_modes[right][i] for i in range(3))
            if norm(target) <= TOL:
                continue
            orbit = canonical_orbit(target)
            if orbit in support_orbits:
                continue
            key = (left, right, orbit)
            if key in seen:
                continue
            seen.add(key)
            coeffs = {}
            for tau in (+1, -1):
                coeffs[sign_name(tau)] = projected_helical_coefficient(
                    target,
                    active_modes[left],
                    active_modes[right],
                    tau,
                    sign_for_label(left, signs),
                    sign_for_label(right, signs),
                )
            if max(abs(x) for x in coeffs.values()) <= TOL:
                continue
            reports.append(
                {
                    "pair": [left, right],
                    "target": target,
                    "orbit": orbit,
                    "target_norm": norm(target),
                    "coefficients": coeffs,
                }
            )
    reports.sort(key=lambda item: (item["target_norm"], item["orbit"], tuple(item["pair"])))
    return reports


def choose_enlargement(reports):
    if not reports:
        return None
    return reports[0]


def distinct_base_labels(base_modes):
    label = f"g{len(base_modes) + 1}"
    while label in base_modes:
        label = f"g{len(base_modes) + 2}"
    return label


def choose_target_sign(coefficients):
    if abs(coefficients["+"]) > TOL:
        return +1
    if abs(coefficients["-"]) > TOL:
        return -1
    raise ValueError("attempted to enlarge on a zero coefficient")


def audit_family(name, payload):
    base_modes = payload["base_modes"]
    modes = expand_support(base_modes)
    positive_labels = sorted(base_modes)
    assignments = []
    live_assignments = 0
    first_pass_force_count = 0
    enlargement_failure_count = 0

    for values in itertools.product((1, -1), repeat=len(positive_labels)):
        signs = dict(zip(positive_labels, values))
        live, seed_report = triad_live(payload["seed_triads"], modes, signs)
        first_pass_reports = new_target_reports(modes, signs)
        first_pass_force = bool(first_pass_reports)
        enlargement = choose_enlargement(first_pass_reports)
        residual_reports = []
        if enlargement is not None:
            enlarged_base_modes = dict(base_modes)
            new_label = distinct_base_labels(enlarged_base_modes)
            enlarged_base_modes[new_label] = enlargement["orbit"]
            enlarged_modes = expand_support(enlarged_base_modes)
            enlarged_signs = dict(signs)
            enlarged_signs[new_label] = choose_target_sign(enlargement["coefficients"])
            residual_reports = new_target_reports(enlarged_modes, enlarged_signs)
        enlargement_failure = bool(residual_reports)

        if live:
            live_assignments += 1
            if first_pass_force:
                first_pass_force_count += 1
            if enlargement_failure:
                enlargement_failure_count += 1

        assignments.append(
            {
                "signs": {label: sign_name(value) for label, value in signs.items()},
                "live_seed": live,
                "seed_triads": seed_report,
                "first_pass_new_targets": first_pass_reports,
                "chosen_enlargement": enlargement,
                "residual_new_targets_after_enlargement": residual_reports,
                "enlargement_failure": enlargement_failure,
            }
        )

    return {
        "family": name,
        "positive_mode_labels": positive_labels,
        "live_seed_assignments": live_assignments,
        "first_pass_force_assignments": first_pass_force_count,
        "enlargement_failure_assignments": enlargement_failure_count,
        "total_assignments": len(assignments),
        "assignments": assignments,
    }


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


def main():
    ROOT.mkdir(parents=True, exist_ok=True)
    reports = [audit_family(name, payload) for name, payload in FAMILIES.items()]
    (ROOT / "admissible_enlargement_audit.json").write_text(
        json.dumps(to_serializable(reports), indent=2) + "\n"
    )

    lines = []
    for report in reports:
        lines.append(f"{report['family']}:")
        lines.append(
            "  live seed assignments="
            f"{report['live_seed_assignments']}/{report['total_assignments']}"
        )
        lines.append(
            "  assignments with first-pass new targets="
            f"{report['first_pass_force_assignments']}/{report['live_seed_assignments']}"
        )
        lines.append(
            "  assignments still forcing new targets after one admissible enlargement="
            f"{report['enlargement_failure_assignments']}/{report['live_seed_assignments']}"
        )
        exemplar = next(
            (
                item
                for item in report["assignments"]
                if item["live_seed"] and item["enlargement_failure"]
            ),
            None,
        )
        if exemplar is None:
            continue
        lines.append(
            "  exemplar signs="
            + ", ".join(f"{k}={v}" for k, v in exemplar["signs"].items())
        )
        enlargement = exemplar["chosen_enlargement"]
        lines.append(
            "  chosen enlargement via pair "
            f"{tuple(enlargement['pair'])} -> {tuple(enlargement['target'])}"
        )
        residual = exemplar["residual_new_targets_after_enlargement"][0]
        mags = {tau: abs(value) for tau, value in residual["coefficients"].items()}
        lines.append(
            "  residual forced pair "
            f"{tuple(residual['pair'])} -> {tuple(residual['target'])}: "
            f"|C_+|={mags['+']:.6f}, |C_-|={mags['-']:.6f}"
        )
    (ROOT / "admissible_enlargement_audit_summary.txt").write_text(
        "\n".join(lines) + "\n"
    )


if __name__ == "__main__":
    main()
