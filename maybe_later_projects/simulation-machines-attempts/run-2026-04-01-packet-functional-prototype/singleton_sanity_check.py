#!/usr/bin/env python3
"""Sanity-check the packet functionals on the old singleton exact support audit."""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

from packet_ledger import PacketLedger, RepresentativeMode, TriadContribution


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
    spec = importlib.util.spec_from_file_location("singleton_audit_module", AUDIT_PATH)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


AUDIT = load_audit_module()


def parse_source_name(name: str, sigma_by_role: dict[str, int]):
    conjugated = name.startswith("bar_")
    role = name.replace("bar_", "")
    sigma = -sigma_by_role[role] if conjugated else sigma_by_role[role]
    return role, conjugated, sigma


def build_singleton_ledger(sigma_by_role: dict[str, int]) -> PacketLedger:
    modes = {
        role: RepresentativeMode(mode_id=role, packet_id=role, sigma=sigma_by_role[role])
        for role in AUDIT.ROLES
    }
    triads: list[TriadContribution] = []

    edge_map = {
        ("a1", "a1", "a2"): "A,A->B",
        ("a1", "a1", "a3"): "A,A->C",
        ("a2", "a3", "a3"): "B,C->C",
        ("a1", "a3", "a4"): "A,C->D",
        ("a3", "a4", "a1"): "C,D->A",
        ("a1", "a2", "a1"): "A,B->A",
        ("a1", "a3", "a1"): "A,C->A",
        ("a4", "a5", "a4"): "D,A_next->D",
        ("a4", "a4", "a5"): "D,D->A_next",
    }

    internal = AUDIT.aggregate_internal(AUDIT.CHOSEN_K, sigma_by_role)
    for target_role, terms in internal.items():
        for (left_name, right_name), coeff in terms.items():
            left_role, left_conjugated, _ = parse_source_name(left_name, sigma_by_role)
            right_role, right_conjugated, _ = parse_source_name(right_name, sigma_by_role)
            status = AUDIT.classify_term(target_role, (left_name, right_name))
            edge_label = None
            if status == "desired":
                edge_label = edge_map.get((left_role, right_role, target_role))
            triads.append(
                TriadContribution(
                    left_mode_id=left_role,
                    left_conjugated=left_conjugated,
                    right_mode_id=right_role,
                    right_conjugated=right_conjugated,
                    target_mode_id=target_role,
                    target_sigma=sigma_by_role[target_role],
                    value=coeff,
                    status=status,
                    edge_label=edge_label,
                )
            )

    external = AUDIT.aggregate_external(AUDIT.CHOSEN_K, sigma_by_role)
    for (target_vec, target_sigma, left_name, right_name), coeff in external.items():
        left_role, left_conjugated, _ = parse_source_name(left_name, sigma_by_role)
        right_role, right_conjugated, _ = parse_source_name(right_name, sigma_by_role)
        target_key = f"{target_vec}:{target_sigma}"
        triads.append(
            TriadContribution(
                left_mode_id=left_role,
                left_conjugated=left_conjugated,
                right_mode_id=right_role,
                right_conjugated=right_conjugated,
                target_mode_id=None,
                target_sigma=target_sigma,
                value=coeff,
                status="external",
                external_target_key=target_key,
            )
        )

    return PacketLedger(modes=modes, triads=triads)


def main():
    ledgers = {
        "chosen": build_singleton_ledger(AUDIT.CHOSEN_SIGMA),
        "alternative": build_singleton_ledger(AUDIT.ALT_SIGMA),
    }
    for name, ledger in ledgers.items():
        print(f"## {name}")
        print(json.dumps(ledger.summary(), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
