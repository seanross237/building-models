#!/usr/bin/env python3
"""Second-budget shared-mode closure audit for Step-3 exploration 002."""

from __future__ import annotations

import itertools
import json
import math
from pathlib import Path


ROOT = Path(
    "/Users/seanross/kingdom_of_god/home-base/research_hub/big-thinkers/"
    "codex-philosopher-atlas/missions/exact-ns-phase-locking-firewall/steps/"
    "step-003/explorations/exploration-002/code/output"
)
TOL = 1e-10


def add(a, b):
    return tuple(x + y for x, y in zip(a, b))


def neg(v):
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


def parallel(a, b):
    return cross(a, b) == (0, 0, 0)


def orbit(v):
    return min(tuple(v), neg(v))


def sign_name(sig):
    return "+" if sig > 0 else "-"


def label_vector(orbit_vectors, label):
    if label.startswith("-"):
        return neg(orbit_vectors[label[1:]])
    return orbit_vectors[label]


def label_sigma(signs, label):
    if label.startswith("-"):
        return signs[label[1:]]
    return signs[label]


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


FAMILY_DEFS = {
    "five_orbit_shared_vertex": {
        "description": "Two triad orbits share exactly one wavevector orbit.",
        "representatives": [
            {
                "name": "generic",
                "orbit_vectors": {
                    "a": (1, 0, 0),
                    "b": (0, 1, 0),
                    "c": (0, 0, 1),
                    "d": (1, 1, 0),
                    "e": (1, 0, 1),
                },
                "seed_orbits": ["a", "b", "c", "d", "e"],
                "seed_triads": [
                    {"name": "T1", "target": "d", "left": "a", "right": "b"},
                    {"name": "T2", "target": "e", "left": "a", "right": "c"},
                ],
                "decisive_pairs": [("d", "b"), ("e", "c")],
            },
            {
                "name": "forward_collision",
                "orbit_vectors": {
                    "a": (1, 0, 0),
                    "b": (0, 1, 0),
                    "c": (0, 2, 0),
                    "d": (1, 1, 0),
                    "e": (1, 2, 0),
                },
                "seed_orbits": ["a", "b", "c", "d", "e"],
                "seed_triads": [
                    {"name": "T1", "target": "d", "left": "a", "right": "b"},
                    {"name": "T2", "target": "e", "left": "a", "right": "c"},
                ],
                "decisive_pairs": [("d", "b"), ("e", "c")],
            },
        ],
    },
    "four_orbit_shared_edge": {
        "description": "Two triad orbits share two wavevector orbits on a four-orbit ledger.",
        "representatives": [
            {
                "name": "parallelogram",
                "orbit_vectors": {
                    "a": (1, 0, 0),
                    "b": (0, 1, 0),
                    "d": (1, 1, 0),
                    "e": (1, -1, 0),
                },
                "seed_orbits": ["a", "b", "d", "e"],
                "seed_triads": [
                    {"name": "T1", "target": "d", "left": "a", "right": "b"},
                    {"name": "T2", "target": "e", "left": "a", "right": "-b"},
                ],
                "decisive_pairs": [("d", "b")],
            }
        ],
    },
}


def catalog_sample(radius=2):
    vecs = [
        v
        for v in itertools.product(range(-radius, radius + 1), repeat=3)
        if v != (0, 0, 0) and orbit(v) == v
    ]
    pattern_counts = {}
    exemplars = {}
    for a in vecs:
        for b in vecs:
            if orbit(a) == orbit(b) or parallel(a, b):
                continue
            d = add(a, b)
            if d == (0, 0, 0):
                continue
            triad_1 = {orbit(a), orbit(b), orbit(d)}
            for c in vecs:
                if orbit(c) == orbit(a) or parallel(a, c):
                    continue
                e = add(a, c)
                if e == (0, 0, 0):
                    continue
                triad_2 = {orbit(a), orbit(c), orbit(e)}
                if triad_1 == triad_2:
                    continue
                support = {orbit(a), orbit(b), orbit(c), orbit(d), orbit(e)}
                if len(support) not in (4, 5):
                    continue
                key = {
                    "support_orbit_count": len(support),
                    "triad_orbit_overlap": len(triad_1 & triad_2),
                }
                encoded = (key["support_orbit_count"], key["triad_orbit_overlap"])
                pattern_counts[encoded] = pattern_counts.get(encoded, 0) + 1
                exemplars.setdefault(
                    encoded,
                    {
                        "a": a,
                        "b": b,
                        "c": c,
                        "d": d,
                        "e": e,
                        "support_orbits": sorted(support),
                    },
                )
    patterns = []
    for encoded in sorted(pattern_counts):
        patterns.append(
            {
                "support_orbit_count": encoded[0],
                "triad_orbit_overlap": encoded[1],
                "sample_count": pattern_counts[encoded],
                "exemplar": exemplars[encoded],
            }
        )
    return {"radius": radius, "patterns": patterns}


def seed_coefficients(rep, signs):
    reports = []
    live = True
    for triad in rep["seed_triads"]:
        coeff = projected_helical_coefficient(
            label_vector(rep["orbit_vectors"], triad["target"]),
            label_vector(rep["orbit_vectors"], triad["left"]),
            label_vector(rep["orbit_vectors"], triad["right"]),
            label_sigma(signs, triad["target"]),
            label_sigma(signs, triad["left"]),
            label_sigma(signs, triad["right"]),
        )
        reports.append(
            {
                "triad": [triad["target"], triad["left"], triad["right"]],
                "value": coeff,
            }
        )
        if abs(coeff) <= TOL:
            live = False
    return live, reports


def active_modes(rep, active_sectors):
    modes = []
    for orbit_name, sigma in sorted(active_sectors):
        vec = rep["orbit_vectors"][orbit_name]
        modes.append({"label": orbit_name, "vector": vec, "sigma": sigma})
        modes.append({"label": f"-{orbit_name}", "vector": neg(vec), "sigma": sigma})
    return modes


def scan_pass(rep, active_sectors):
    budget_orbits = {orbit(rep["orbit_vectors"][name]) for name in rep["seed_orbits"]}
    orbit_names = {orbit(rep["orbit_vectors"][name]): name for name in rep["seed_orbits"]}
    current = {(orbit(rep["orbit_vectors"][name]), sigma) for name, sigma in active_sectors}
    on_budget = {}
    spill = {}

    for left, right in itertools.product(active_modes(rep, active_sectors), repeat=2):
        target = add(left["vector"], right["vector"])
        if target == (0, 0, 0):
            continue
        target_orbit = orbit(target)
        for tau in (+1, -1):
            coeff = projected_helical_coefficient(
                target,
                left["vector"],
                right["vector"],
                tau,
                left["sigma"],
                right["sigma"],
            )
            if abs(coeff) <= TOL:
                continue
            key = (target_orbit, tau)
            event = {
                "pair": [left["label"], right["label"]],
                "target": target,
                "target_orbit": target_orbit,
                "target_orbit_name": orbit_names.get(target_orbit),
                "target_sigma": sign_name(tau),
                "coefficient": coeff,
            }
            if target_orbit in budget_orbits:
                if key not in current and key not in on_budget:
                    on_budget[key] = event
            elif key not in spill:
                spill[key] = event

    return {
        "new_on_budget_sectors": list(on_budget.values()),
        "spill_sectors": list(spill.values()),
    }


def closure_audit(rep):
    assignments = []
    seed_orbits = rep["seed_orbits"]
    sign_choices = list(itertools.product((+1, -1), repeat=len(seed_orbits)))

    exact_count = 0
    spill_count = 0
    fixed_count = 0

    for values in sign_choices:
        signs = dict(zip(seed_orbits, values))
        live, seed_report = seed_coefficients(rep, signs)
        assignment = {
            "signs": {name: sign_name(signs[name]) for name in seed_orbits},
            "seed_live": live,
            "seed_coefficients": seed_report,
            "passes": [],
        }
        if not live:
            assignment["status"] = "exactness_failure"
            assignments.append(assignment)
            continue

        exact_count += 1
        active_sectors = {(name, signs[name]) for name in seed_orbits}
        assignment["pass0"] = {
            "active_orbit_sectors": [
                {"orbit": name, "sigma": sign_name(sig)} for name, sig in sorted(active_sectors)
            ]
        }

        for pass_index in range(1, 6):
            pass_report = scan_pass(rep, active_sectors)
            pass_report["pass_index"] = pass_index
            assignment["passes"].append(pass_report)

            if pass_report["spill_sectors"]:
                assignment["status"] = "budget_spill"
                assignment["decisive_pass"] = pass_index
                spill_count += 1
                break

            additions = {
                (event["target_orbit_name"], +1 if event["target_sigma"] == "+" else -1)
                for event in pass_report["new_on_budget_sectors"]
            }
            if not additions:
                assignment["status"] = "fixed_point"
                assignment["decisive_pass"] = pass_index
                fixed_count += 1
                break

            active_sectors |= additions
        else:
            assignment["status"] = "pass_limit"

        assignments.append(assignment)

    exemplar = next(
        item for item in assignments if item["status"] == "budget_spill"
    )
    return {
        "representative": rep["name"],
        "raw_assignments": len(assignments),
        "exact_assignments": exact_count,
        "fixed_point_assignments": fixed_count,
        "spill_assignments": spill_count,
        "assignments": assignments,
        "exemplar": exemplar,
    }


def decisive_pair_report(rep):
    seed_orbits = rep["seed_orbits"]
    signs = {name: +1 for name in seed_orbits}
    reports = []
    for left, right in rep["decisive_pairs"]:
        coeffs = {}
        target = add(
            label_vector(rep["orbit_vectors"], left),
            label_vector(rep["orbit_vectors"], right),
        )
        for tau in (+1, -1):
            coeffs[sign_name(tau)] = projected_helical_coefficient(
                target,
                label_vector(rep["orbit_vectors"], left),
                label_vector(rep["orbit_vectors"], right),
                tau,
                label_sigma(signs, left),
                label_sigma(signs, right),
            )
        reports.append(
            {
                "pair": [left, right],
                "target": target,
                "coefficients": coeffs,
            }
        )
    return reports


def audit_family(name, payload):
    representative_reports = []
    for rep in payload["representatives"]:
        representative_reports.append(
            {
                "representative": rep["name"],
                "description": payload["description"],
                "seed_orbits": rep["seed_orbits"],
                "orbit_vectors": rep["orbit_vectors"],
                "decisive_pairs": decisive_pair_report(rep),
                "closure": closure_audit(rep),
            }
        )
    return {"family": name, "description": payload["description"], "representatives": representative_reports}


def write_summary(catalog, family_reports):
    lines = []
    lines.append("Catalog sample:")
    for pattern in catalog["patterns"]:
        lines.append(
            "  support size="
            f"{pattern['support_orbit_count']}, "
            f"triad overlap={pattern['triad_orbit_overlap']}, "
            f"sample count={pattern['sample_count']}"
        )
    for family in family_reports:
        lines.append(f"{family['family']}:")
        for rep in family["representatives"]:
            closure = rep["closure"]
            lines.append(
                f"  {rep['representative']}: "
                f"exact={closure['exact_assignments']}/{closure['raw_assignments']}, "
                f"fixed={closure['fixed_point_assignments']}, "
                f"spill={closure['spill_assignments']}"
            )
            for pair in rep["decisive_pairs"]:
                mags = {tau: abs(value) for tau, value in pair["coefficients"].items()}
                lines.append(
                    "    decisive pair "
                    f"{tuple(pair['pair'])} -> {tuple(pair['target'])}: "
                    f"|C_+|={mags['+']:.6f}, |C_-|={mags['-']:.6f}"
                )
            exemplar = closure["exemplar"]
            spill_events = exemplar["passes"][0]["spill_sectors"]
            first = spill_events[0]
            lines.append(
                "    exemplar spill assignment="
                + ", ".join(f"{k}={v}" for k, v in exemplar["signs"].items())
            )
            lines.append(
                "    first spill witness="
                f"{tuple(first['pair'])} -> {tuple(first['target'])}, "
                f"sigma={first['target_sigma']}, "
                f"|C|={abs(first['coefficient']):.6f}"
            )
    return "\n".join(lines) + "\n"


def main():
    ROOT.mkdir(parents=True, exist_ok=True)

    catalog = catalog_sample()
    family_reports = [audit_family(name, payload) for name, payload in FAMILY_DEFS.items()]

    out_json = {
        "catalog_sample": catalog,
        "family_reports": family_reports,
    }
    (ROOT / "shared_mode_closure_audit.json").write_text(
        json.dumps(to_serializable(out_json), indent=2) + "\n"
    )
    (ROOT / "shared_mode_closure_audit_summary.txt").write_text(
        write_summary(catalog, family_reports)
    )


if __name__ == "__main__":
    main()
