#!/usr/bin/env python3
"""Exact-ledger packet functionals on a conjugate-pair representative quotient.

The exact packet support is sign-closed, so a global sign-balance functional
must not count both members of every conjugate pair as independent "modes".
This module works on representative mode families with explicit conjugation
flags on triad legs.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Iterable, Optional


@dataclass(frozen=True)
class RepresentativeMode:
    """One representative of a conjugate-pair family."""

    mode_id: str
    packet_id: str
    sigma: int


@dataclass(frozen=True)
class TriadContribution:
    """One exact triad contribution in representative-mode coordinates."""

    left_mode_id: str
    left_conjugated: bool
    right_mode_id: str
    right_conjugated: bool
    target_mode_id: Optional[str]
    target_sigma: int
    value: complex
    status: str
    edge_label: Optional[str] = None
    external_target_key: Optional[str] = None


@dataclass
class PacketLedger:
    """Exact packet ledger with drive, leakage, and sign-sensitive functionals."""

    modes: Dict[str, RepresentativeMode]
    triads: list[TriadContribution]

    def _effective_sign(self, mode_id: str, conjugated: bool) -> int:
        sigma = self.modes[mode_id].sigma
        return -sigma if conjugated else sigma

    def drive_by_edge(self) -> Dict[str, float]:
        out: Dict[str, float] = {}
        for triad in self.triads:
            if triad.status != "desired" or triad.edge_label is None:
                continue
            out[triad.edge_label] = out.get(triad.edge_label, 0.0) + abs(triad.value)
        return out

    def drive_target(self) -> float:
        return sum(abs(triad.value) for triad in self.triads if triad.status == "desired")

    def leak_in(self) -> float:
        return sum(
            abs(triad.value)
            for triad in self.triads
            if triad.target_mode_id is not None and triad.status != "desired"
        )

    def leak_out(self) -> float:
        grouped: Dict[tuple[str, int], complex] = {}
        for triad in self.triads:
            if triad.target_mode_id is not None:
                continue
            key = (triad.external_target_key or "external", triad.target_sigma)
            grouped[key] = grouped.get(key, 0.0j) + triad.value
        return sum(abs(total) for total in grouped.values())

    def leak(self) -> float:
        drive = self.drive_target()
        if drive == 0:
            return float("inf")
        return (self.leak_in() + self.leak_out()) / drive

    def participation_by_representative(self, desired_only: bool = False) -> Dict[str, float]:
        weights = {mode_id: 0.0 for mode_id in self.modes}
        for triad in self.triads:
            if desired_only and triad.status != "desired":
                continue
            weight = abs(triad.value)
            weights[triad.left_mode_id] += weight
            weights[triad.right_mode_id] += weight
            if triad.target_mode_id is not None:
                weights[triad.target_mode_id] += weight
        return weights

    def sd_part(self) -> float:
        weights = self.participation_by_representative()
        total = sum(weights.values())
        if total == 0:
            return 1.0
        best_same_sign_weight = max(
            sum(weight for mode_id, weight in weights.items() if self.modes[mode_id].sigma == sign)
            for sign in (-1, 1)
        )
        return 1.0 - best_same_sign_weight / total

    def sd_target(self) -> float:
        drive = self.drive_target()
        if drive == 0:
            return 1.0
        heterochiral_weight = 0.0
        for triad in self.triads:
            if triad.status != "desired":
                continue
            sign_set = {
                self._effective_sign(triad.left_mode_id, triad.left_conjugated),
                self._effective_sign(triad.right_mode_id, triad.right_conjugated),
                triad.target_sigma,
            }
            if len(sign_set) > 1:
                heterochiral_weight += abs(triad.value)
        return heterochiral_weight / drive

    def summary(self) -> Dict[str, float | Dict[str, float]]:
        return {
            "drive_by_edge": self.drive_by_edge(),
            "drive_target": self.drive_target(),
            "leak_in": self.leak_in(),
            "leak_out": self.leak_out(),
            "leak": self.leak(),
            "sd_part": self.sd_part(),
            "sd_target": self.sd_target(),
        }


def summarize_ledgers(ledgers: Iterable[tuple[str, PacketLedger]]) -> Dict[str, Dict[str, float | Dict[str, float]]]:
    return {name: ledger.summary() for name, ledger in ledgers}
