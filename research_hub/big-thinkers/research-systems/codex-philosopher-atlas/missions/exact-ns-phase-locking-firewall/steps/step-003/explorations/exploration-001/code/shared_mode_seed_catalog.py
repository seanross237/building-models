#!/usr/bin/env python3
"""Classify abstract two-triad shared-mode seed families up to relabeling."""

from __future__ import annotations

import itertools
import json
from pathlib import Path


ROOT = Path(
    "/Users/seanross/kingdom_of_god/home-base/research_hub/big-thinkers/"
    "codex-philosopher-atlas/missions/exact-ns-phase-locking-firewall/steps/"
    "step-003/explorations/exploration-001/code/output"
)


def canonical_pair(edge_a, edge_b):
    union = sorted(edge_a | edge_b)
    best = None
    for perm in itertools.permutations(range(len(union))):
        mapping = {union[i]: perm[i] for i in range(len(union))}
        first = tuple(sorted(mapping[x] for x in edge_a))
        second = tuple(sorted(mapping[x] for x in edge_b))
        candidate = tuple(sorted((first, second)))
        if best is None or candidate < best:
            best = candidate
    return best


def family_name(intersection_size):
    if intersection_size == 3:
        return "same_triad_dead_seed"
    if intersection_size == 2:
        return "shared_parallelogram"
    if intersection_size == 1:
        return "generic_fan"
    raise ValueError(intersection_size)


def family_note(intersection_size):
    if intersection_size == 3:
        return (
            "The second triad orbit is not new. This is only a disguised "
            "rung-1 seed."
        )
    if intersection_size == 2:
        return (
            "Two distinct triad orbits share two independent wavevector "
            "orbits up to conjugation, so the seed has four orbit classes."
        )
    if intersection_size == 1:
        return (
            "Two distinct triad orbits share exactly one independent "
            "wavevector orbit up to conjugation, so the seed has five orbit "
            "classes."
        )
    raise ValueError(intersection_size)


def representative(intersection_size):
    if intersection_size == 3:
        return {
            "triad_1": ["p", "q", "p+q"],
            "triad_2": ["p", "q", "p+q"],
        }
    if intersection_size == 2:
        return {
            "triad_1": ["p", "q", "p+q"],
            "triad_2": ["p", "-q", "p-q"],
        }
    if intersection_size == 1:
        return {
            "triad_1": ["p", "q", "p+q"],
            "triad_2": ["p", "r", "p+r"],
        }
    raise ValueError(intersection_size)


def build_report():
    # Abstract triad orbits are 3-sets. Two-triad shared-mode seeds have
    # intersection size at least 1; disconnected pairs are outside the budget.
    universe = range(5)
    edges = [frozenset(edge) for edge in itertools.combinations(universe, 3)]
    classes = {}

    for edge_a in edges:
        for edge_b in edges:
            if len(edge_a & edge_b) == 0:
                continue
            key = canonical_pair(edge_a, edge_b)
            classes.setdefault(key, {"count": 0, "examples": set()})
            classes[key]["count"] += 1
            classes[key]["examples"].add((tuple(sorted(edge_a)), tuple(sorted(edge_b))))

    report = []
    for key in sorted(classes):
        intersection_size = len(set(key[0]) & set(key[1]))
        report.append(
            {
                "canonical_edge_pair": [list(key[0]), list(key[1])],
                "intersection_size": intersection_size,
                "independent_orbit_count": 6 - intersection_size,
                "family": family_name(intersection_size),
                "note": family_note(intersection_size),
                "canonical_wavevector_representative": representative(intersection_size),
                "raw_labeled_realizations_found": classes[key]["count"],
            }
        )
    return report


def main():
    ROOT.mkdir(parents=True, exist_ok=True)
    report = build_report()
    (ROOT / "shared_mode_seed_catalog.json").write_text(
        json.dumps(report, indent=2) + "\n"
    )

    lines = []
    for item in report:
        lines.append(f"family={item['family']}")
        lines.append(f"  edge-intersection size={item['intersection_size']}")
        lines.append(
            f"  independent orbit count={item['independent_orbit_count']}"
        )
        lines.append(f"  note={item['note']}")
        rep = item["canonical_wavevector_representative"]
        lines.append(f"  representative triad 1={tuple(rep['triad_1'])}")
        lines.append(f"  representative triad 2={tuple(rep['triad_2'])}")
    (ROOT / "shared_mode_seed_catalog_summary.txt").write_text(
        "\n".join(lines) + "\n"
    )


if __name__ == "__main__":
    main()
