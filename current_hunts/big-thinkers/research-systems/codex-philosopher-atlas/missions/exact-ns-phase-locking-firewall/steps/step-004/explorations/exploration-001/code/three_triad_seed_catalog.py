#!/usr/bin/env python3
"""Classify third-budget seed graphs for the single-repeated-orbit rung."""

from __future__ import annotations

import itertools
import json
from pathlib import Path


ROOT = Path(
    "/Users/seanross/kingdom_of_god/home-base/current_hunts/big-thinkers/"
    "codex-philosopher-atlas/missions/exact-ns-phase-locking-firewall/steps/"
    "step-004/explorations/exploration-001/code/output"
)


def canonical_hypergraph(edges):
    support = sorted(set().union(*map(set, edges)))
    index = {vertex: i for i, vertex in enumerate(support)}
    remapped = [tuple(index[x] for x in edge) for edge in edges]
    best = None
    for perm in itertools.permutations(range(len(support))):
        candidate = tuple(
            sorted(tuple(sorted(perm[x] for x in edge)) for edge in remapped)
        )
        if best is None or candidate < best:
            best = candidate
    return best


def connected(edges):
    adjacency = {i: set() for i in range(len(edges))}
    for i, j in itertools.combinations(range(len(edges)), 2):
        if set(edges[i]) & set(edges[j]):
            adjacency[i].add(j)
            adjacency[j].add(i)
    seen = {0}
    stack = [0]
    while stack:
        node = stack.pop()
        for neighbor in adjacency[node]:
            if neighbor not in seen:
                seen.add(neighbor)
                stack.append(neighbor)
    return len(seen) == len(edges)


def enumerate_classes():
    classes = {}
    perm_cache = {m: list(itertools.permutations(range(m))) for m in range(3, 8)}
    del perm_cache  # kept to document the bounded support size

    for support_size in range(3, 8):
        vertices = range(support_size)
        all_edges = [tuple(edge) for edge in itertools.combinations(vertices, 3)]
        for edges in itertools.combinations(all_edges, 3):
            if len(set().union(*map(set, edges))) != support_size:
                continue
            if not connected(edges):
                continue
            key = canonical_hypergraph(edges)
            classes.setdefault(key, 0)
            classes[key] += 1

    report = []
    for key in sorted(classes):
        degree = {
            vertex: sum(vertex in edge for edge in key)
            for vertex in sorted(set().union(*map(set, key)))
        }
        pair_intersections = sorted(
            len(set(key[i]) & set(key[j]))
            for i, j in itertools.combinations(range(3), 2)
        )
        repeated_vertices = [v for v, deg in degree.items() if deg > 1]
        support_size = len(degree)

        if sorted(degree.values(), reverse=True) == [3, 1, 1, 1, 1, 1, 1]:
            status = "live_third_budget_family"
            family = "single_repeated_orbit_three_arm_star"
            note = (
                "Connectedness plus exactly one repeated orbit forces that orbit "
                "to lie in all three triads. This is the unique abstract seed "
                "graph for the declared third rung."
            )
            representative = {
                "triad_1": ["a", "b", "a+b"],
                "triad_2": ["a", "c", "a+c"],
                "triad_3": ["a", "d", "a+d"],
            }
        elif support_size <= 5:
            status = "reject_lower_budget_artifact"
            family = "contained_in_exhausted_lower_budget"
            note = (
                "A three-triad picture on five or fewer orbit classes does not "
                "add enough genuinely new support beyond the already exhausted "
                "first or second budgets."
            )
            representative = None
        elif any(size == 2 for size in pair_intersections):
            status = "reject_multiple_repeated_orbits"
            family = "shared_pair_or_parallelogram_core"
            note = (
                "Any pair-intersection of size two means the cluster repeats at "
                "least two orbit classes, so it is not the single-repeated-orbit "
                "third-rung budget."
            )
            representative = None
        else:
            status = "reject_multiple_repeated_orbits"
            family = "cycle_or_chain_with_more_than_one_reused_orbit"
            note = (
                "The support has six or seven orbit classes, but more than one "
                "orbit is reused across the cluster. That falls outside the "
                "declared single-repeated-orbit rung."
            )
            representative = None

        report.append(
            {
                "canonical_edge_triple": [list(edge) for edge in key],
                "support_size": support_size,
                "pair_intersections": pair_intersections,
                "degree_sequence_desc": sorted(degree.values(), reverse=True),
                "repeated_vertex_count": len(repeated_vertices),
                "status": status,
                "family": family,
                "note": note,
                "canonical_wavevector_representative": representative,
            }
        )
    return report


def main():
    ROOT.mkdir(parents=True, exist_ok=True)
    report = enumerate_classes()
    (ROOT / "three_triad_seed_catalog.json").write_text(
        json.dumps(report, indent=2) + "\n"
    )

    accepted = next(
        item for item in report if item["status"] == "live_third_budget_family"
    )

    lines = [
        "third_budget_seed_graphs=9 abstract connected 3-edge classes",
        "accepted_family=single_repeated_orbit_three_arm_star",
        "accepted_support_size=7",
        "accepted_degree_sequence=[3,1,1,1,1,1,1]",
        (
            "accepted_representative="
            "{(a,b,a+b), (a,c,a+c), (a,d,a+d)}"
        ),
        (
            "cross_scale_condition="
            "at least two distinct shell levels among the partner or output "
            "orbits; this is a parameter condition inside the same family"
        ),
        "",
        "rejected_classes:",
    ]
    for item in report:
        if item["status"] == "live_third_budget_family":
            continue
        lines.append(
            "  support="
            f"{item['support_size']}, "
            f"pair_intersections={item['pair_intersections']}, "
            f"degree_sequence={item['degree_sequence_desc']}, "
            f"reason={item['family']}"
        )
    (ROOT / "three_triad_seed_catalog_summary.txt").write_text(
        "\n".join(lines) + "\n"
    )


if __name__ == "__main__":
    main()
