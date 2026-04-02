#!/usr/bin/env python3
"""Packet-level exact-ledger functionals for concrete helical packet families."""

from __future__ import annotations

import importlib.util
import itertools
import json
import math
import sys
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
AUDIT_PATH = (
    ROOT
    / "codex-atlas"
    / "execution"
    / "instances"
    / "exact-ns-no-near-closed-tao-circuit"
    / "strategies"
    / "strategy-001"
    / "explorations"
    / "exploration-002"
    / "code"
    / "helical_support_audit.py"
)


def load_audit_module():
    spec = importlib.util.spec_from_file_location("helical_support_audit_packet_module", AUDIT_PATH)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


AUDIT = load_audit_module()
TARGET_EDGES = {
    ("A", "A", "B"),
    ("A", "A", "C"),
    ("B", "C", "C"),
    ("A", "C", "D"),
    ("C", "D", "A"),
    ("A", "B", "A"),
    ("A", "C", "A"),
    ("D", "A_next", "D"),
    ("D", "D", "A_next"),
}


@dataclass(frozen=True)
class NamedMode:
    name: str
    vec: tuple[int, int, int]
    sigma: int
    packet: str


@dataclass(frozen=True)
class LedgerRow:
    kind: str
    left_name: str
    right_name: str
    target_name: str | None
    left_packet: str
    right_packet: str
    target_packet: str | None
    left_sigma: int
    right_sigma: int
    target_sigma: int | None
    weight: float
    edge: tuple[str, str, str] | None
    desired: bool


ROLE_TO_PACKET = {
    "a1": "A",
    "a2": "B",
    "a3": "C",
    "a4": "D",
    "a5": "A_next",
}

CHOSEN_SIGMA = {
    "a1": 1,
    "a2": 1,
    "a3": -1,
    "a4": 1,
    "a5": 1,
}


def canonical_rep(name: str) -> str:
    return name.replace("bar_", "")


def amp(amplitudes: dict[str, float], name: str) -> float:
    return float(abs(amplitudes.get(name, 1.0)))


def enumerate_rows(named_modes: list[NamedMode], amplitudes=None):
    if amplitudes is None:
        amplitudes = {}
    active_by_key = {(mode.vec, mode.sigma): mode for mode in named_modes}
    rows: list[LedgerRow] = []

    for target in named_modes:
        for left in named_modes:
            for right in named_modes:
                if AUDIT.v_add(left.vec, right.vec) != target.vec:
                    continue
                coeff = AUDIT.helical_coeff(target.vec, left.vec, right.vec, target.sigma, left.sigma, right.sigma)
                if abs(coeff) < 1e-12:
                    continue
                edge = (left.packet, right.packet, target.packet)
                weight = abs(coeff) * amp(amplitudes, left.name) * amp(amplitudes, right.name)
                rows.append(
                    LedgerRow(
                        kind="internal",
                        left_name=left.name,
                        right_name=right.name,
                        target_name=target.name,
                        left_packet=left.packet,
                        right_packet=right.packet,
                        target_packet=target.packet,
                        left_sigma=left.sigma,
                        right_sigma=right.sigma,
                        target_sigma=target.sigma,
                        weight=weight,
                        edge=edge,
                        desired=edge in TARGET_EDGES,
                    )
                )

    for left in named_modes:
        for right in named_modes:
            target_vec = AUDIT.v_add(left.vec, right.vec)
            if target_vec == (0, 0, 0):
                continue
            for target_sigma in (-1, 1):
                if (target_vec, target_sigma) in active_by_key:
                    continue
                coeff = AUDIT.helical_coeff(target_vec, left.vec, right.vec, target_sigma, left.sigma, right.sigma)
                if abs(coeff) < 1e-12:
                    continue
                weight = abs(coeff) * amp(amplitudes, left.name) * amp(amplitudes, right.name)
                rows.append(
                    LedgerRow(
                        kind="external",
                        left_name=left.name,
                        right_name=right.name,
                        target_name=None,
                        left_packet=left.packet,
                        right_packet=right.packet,
                        target_packet=None,
                        left_sigma=left.sigma,
                        right_sigma=right.sigma,
                        target_sigma=target_sigma,
                        weight=weight,
                        edge=None,
                        desired=False,
                    )
                )

    return rows


def packet_metrics(named_modes: list[NamedMode], amplitudes=None):
    rows = enumerate_rows(named_modes, amplitudes=amplitudes)

    drive_by_edge: dict[tuple[str, str, str], float] = {edge: 0.0 for edge in TARGET_EDGES}
    leak_in = 0.0
    leak_out = 0.0

    for row in rows:
        if row.kind == "internal" and row.desired and row.edge is not None:
            drive_by_edge[row.edge] += row.weight
        elif row.kind == "internal":
            leak_in += row.weight
        else:
            leak_out += row.weight

    drive_target = sum(drive_by_edge.values())
    leak = math.inf if drive_target == 0 else (leak_in + leak_out) / drive_target

    # Conjugate-pair quotient for global sign defect: aggregate participation by
    # canonical representative and use the representative sign only once.
    representative_sign = {}
    representative_weight = {}
    mode_lookup = {mode.name: mode for mode in named_modes}
    for mode in named_modes:
        rep = canonical_rep(mode.name)
        if rep not in representative_sign and not mode.name.startswith("bar_"):
            representative_sign[rep] = mode.sigma
        representative_weight.setdefault(rep, 0.0)

    target_total = 0.0
    target_heterochiral = 0.0

    for row in rows:
        touched = {canonical_rep(row.left_name), canonical_rep(row.right_name)}
        if row.target_name is not None:
            touched.add(canonical_rep(row.target_name))
        for rep in touched:
            representative_weight[rep] = representative_weight.get(rep, 0.0) + row.weight

        if row.kind == "internal" and row.desired and row.target_sigma is not None:
            target_total += row.weight
            if len({row.left_sigma, row.right_sigma, row.target_sigma}) > 1:
                target_heterochiral += row.weight

    plus = sum(weight for rep, weight in representative_weight.items() if representative_sign.get(rep) == 1)
    minus = sum(weight for rep, weight in representative_weight.items() if representative_sign.get(rep) == -1)
    total = plus + minus
    sd_part = 1.0 if total == 0 else min(plus, minus) / total
    sd_target = 1.0 if target_total == 0 else target_heterochiral / target_total

    return {
        "drive_by_edge": drive_by_edge,
        "drive_target": drive_target,
        "leak_in": leak_in,
        "leak_out": leak_out,
        "leak": leak,
        "sd_part": sd_part,
        "sd_target": sd_target,
        "row_count": len(rows),
    }


def singleton_pair_family(sigma_by_role):
    modes = []
    for role in AUDIT.ROLES:
        vec = AUDIT.CHOSEN_K[role]
        sigma = sigma_by_role[role]
        packet = ROLE_TO_PACKET[role]
        modes.append(NamedMode(role, vec, sigma, packet))
        modes.append(NamedMode(f"bar_{role}", AUDIT.v_scale(-1, vec), -sigma, packet))
    return modes


def shell_index(vec):
    norm = math.sqrt(sum(x * x for x in vec))
    j = 0
    while 2 ** (j + 1) <= norm:
        j += 1
    return j


def nearest_anchor_packet(vec, sigma, anchors):
    candidates = []
    for name, anchor_vec, anchor_sigma, packet in anchors:
        if anchor_sigma != sigma:
            continue
        if shell_index(anchor_vec) != shell_index(vec):
            continue
        dist2 = sum((a - b) ** 2 for a, b in zip(anchor_vec, vec))
        candidates.append((dist2, name, packet))
    if not candidates:
        return None
    candidates.sort()
    return candidates[0][2]


def expanded_shell_sign_family():
    # Start from the lowest-leak singleton sign pattern.
    sigma_by_role = dict(CHOSEN_SIGMA)
    modes = singleton_pair_family(sigma_by_role)

    # One-step external closure representatives from the chosen singleton audit.
    # These are the strongest unique positive-helicity targets appearing in the
    # audit summary; each is then assigned by shell+sign nearest-anchor rule.
    additions = [
        ("b1", (2, 1, 0), 1),
        ("b2", (1, 2, 0), 1),
        ("b3", (0, 2, 0), 1),
        ("b4", (2, 3, 0), 1),
    ]
    anchors = [
        ("a1", AUDIT.CHOSEN_K["a1"], sigma_by_role["a1"], "A"),
        ("a2", AUDIT.CHOSEN_K["a2"], sigma_by_role["a2"], "B"),
        ("a3", AUDIT.CHOSEN_K["a3"], sigma_by_role["a3"], "C"),
        ("a4", AUDIT.CHOSEN_K["a4"], sigma_by_role["a4"], "D"),
        ("a5", AUDIT.CHOSEN_K["a5"], sigma_by_role["a5"], "A_next"),
    ]

    for name, vec, sigma in additions:
        packet = nearest_anchor_packet(vec, sigma, anchors)
        if packet is None:
            continue
        modes.append(NamedMode(name, vec, sigma, packet))
        modes.append(NamedMode(f"bar_{name}", AUDIT.v_scale(-1, vec), -sigma, packet))

    return modes


def canonical_target_pair(vec, sigma):
    neg_vec = AUDIT.v_scale(-1, vec)
    options = [
        (tuple(vec) + (sigma,), tuple(vec), sigma),
        (tuple(neg_vec) + (-sigma,), tuple(neg_vec), -sigma),
    ]
    options.sort(key=lambda item: item[0])
    return options[0][1], options[0][2]


def expanded_incidence_family():
    sigma_by_role = dict(CHOSEN_SIGMA)
    modes = singleton_pair_family(sigma_by_role)
    active = {(mode.vec, mode.sigma) for mode in modes}
    packet_order = ["A", "B", "C", "D", "A_next"]
    grouped_weight = {}
    incidence = {}

    for left in modes:
        for right in modes:
            target_vec = AUDIT.v_add(left.vec, right.vec)
            if target_vec == (0, 0, 0):
                continue
            for target_sigma in (-1, 1):
                if (target_vec, target_sigma) in active:
                    continue
                coeff = AUDIT.helical_coeff(target_vec, left.vec, right.vec, target_sigma, left.sigma, right.sigma)
                if abs(coeff) < 1e-12:
                    continue
                rep_vec, rep_sigma = canonical_target_pair(target_vec, target_sigma)
                key = (rep_vec, rep_sigma)
                grouped_weight[key] = grouped_weight.get(key, 0.0) + abs(coeff)
                incidence.setdefault(key, {packet: 0.0 for packet in packet_order})
                incidence[key][left.packet] += abs(coeff)
                incidence[key][right.packet] += abs(coeff)

    ranked = sorted(grouped_weight.items(), key=lambda item: (-item[1], item[0]))[:4]
    for idx, ((vec, sigma), _) in enumerate(ranked, start=1):
        packet = sorted(
            incidence[(vec, sigma)].items(),
            key=lambda item: (-item[1], packet_order.index(item[0])),
        )[0][0]
        modes.append(NamedMode(f"x{idx}", vec, sigma, packet))
        modes.append(NamedMode(f"bar_x{idx}", AUDIT.v_scale(-1, vec), -sigma, packet))

    return modes


def summarized_metrics(named_modes):
    metrics = packet_metrics(named_modes)
    return {
        "drive_target": metrics["drive_target"],
        "leak": metrics["leak"],
        "sd_part": metrics["sd_part"],
        "sd_target": metrics["sd_target"],
        "row_count": metrics["row_count"],
        "drive_by_edge": {
            f"{a},{b}->{c}": value for (a, b, c), value in sorted(metrics["drive_by_edge"].items()) if value > 0
        },
        "packet_sizes": {
            packet: sum(1 for mode in named_modes if mode.packet == packet)
            for packet in sorted({mode.packet for mode in named_modes})
        },
    }


def singleton_scan():
    rows = []
    for pattern in itertools.product((1, -1), repeat=len(AUDIT.ROLES)):
        sigma = dict(zip(AUDIT.ROLES, pattern))
        modes = singleton_pair_family(sigma)
        metrics = packet_metrics(modes)
        plus = sum(1 for value in sigma.values() if value == 1)
        rows.append(
            {
                "sigma": sigma,
                "minority_count": min(plus, len(AUDIT.ROLES) - plus),
                "drive_target": metrics["drive_target"],
                "leak": metrics["leak"],
                "sd_part": metrics["sd_part"],
                "sd_target": metrics["sd_target"],
            }
        )
    rows.sort(key=lambda row: (0 if math.isfinite(row["leak"]) else 1, row["leak"]))
    return rows


def main():
    print("Singleton-pair packet scan:")
    for row in singleton_scan()[:10]:
        print(json.dumps(row, sort_keys=True))

    print("\nExpanded non-singleton shell-sign-nearest-anchor family:")
    family = expanded_shell_sign_family()
    print(json.dumps(summarized_metrics(family), sort_keys=True))

    print("\nExpanded non-singleton source-incidence family:")
    family = expanded_incidence_family()
    print(json.dumps(summarized_metrics(family), sort_keys=True))


if __name__ == "__main__":
    main()
