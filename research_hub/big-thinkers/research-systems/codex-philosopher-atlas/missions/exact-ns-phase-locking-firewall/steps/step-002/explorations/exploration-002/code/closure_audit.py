#!/usr/bin/env python3
"""Numerical helical-coefficient checks for Step-2 exploration 002."""

from __future__ import annotations

import cmath
import itertools
import json
import math
from pathlib import Path

import numpy as np


ROOT = Path(
    "/Users/seanross/kingdom_of_god/home-base/research_hub/big-thinkers/"
    "codex-philosopher-atlas/missions/exact-ns-phase-locking-firewall/steps/"
    "step-002/explorations/exploration-002/code/output"
)


def arr(v):
    return np.array(v, dtype=float)


def norm(v):
    return float(np.linalg.norm(v))


def helical_basis(k, sigma):
    k = arr(k)
    khat = k / norm(k)
    ref = np.array([0.0, 0.0, 1.0])
    if abs(np.dot(khat, ref)) > 0.9:
        ref = np.array([1.0, 0.0, 0.0])
    e1 = np.cross(ref, khat)
    e1 = e1 / norm(e1)
    e2 = np.cross(khat, e1)
    return (e1 + 1j * sigma * e2) / math.sqrt(2.0)


def projected_helical_coefficient(target, source_a, source_b, sig_target, sig_a, sig_b):
    kt = arr(target)
    ka = arr(source_a)
    kb = arr(source_b)
    ht = helical_basis(kt, sig_target)
    ha = helical_basis(ka, sig_a)
    hb = helical_basis(kb, sig_b)
    # Directly evaluate the coefficient from the frozen exact interaction scalar:
    # -i * \bar{h_t} · [ (k_b · h_a) P_t h_b ].
    proj = np.eye(3) - np.outer(kt, kt) / (norm(kt) ** 2)
    return -1j * np.vdot(ht, (np.dot(kb, ha) * (proj @ hb)))


def sign_name(sig):
    return "+" if sig > 0 else "-"


def triad_report(name, p, q, sign_sheet):
    k = tuple((arr(p) + arr(q)).tolist())
    modes = {
        "k": tuple(k),
        "p": tuple(p),
        "q": tuple(q),
        "-k": tuple((-arr(k)).tolist()),
        "-p": tuple((-arr(p)).tolist()),
        "-q": tuple((-arr(q)).tolist()),
    }
    sig_k, sig_p, sig_q = sign_sheet

    representative = {}
    for tau in (+1, -1):
        representative[sign_name(tau)] = {
            "value": complex(
                projected_helical_coefficient(k, p, q, tau, sig_p, sig_q)
            ),
        }

    checks = []
    candidate_pairs = [
        ("p", "-q", tuple((arr(p) - arr(q)).tolist()), sig_p, sig_q),
        ("k", "p", tuple((arr(k) + arr(p)).tolist()), sig_k, sig_p),
        ("k", "q", tuple((arr(k) + arr(q)).tolist()), sig_k, sig_q),
    ]
    for left, right, target, sig_left, sig_right in candidate_pairs:
        values = {}
        for tau in (+1, -1):
            coeff = projected_helical_coefficient(
                target, modes[left], modes[right], tau, sig_left, sig_right
            )
            values[sign_name(tau)] = complex(coeff)
        checks.append(
            {
                "pair": [left, right],
                "target": target,
                "target_norm": norm(target),
                "coefficients": values,
            }
        )

    return {
        "name": name,
        "p": p,
        "q": q,
        "k": k,
        "sign_sheet": "".join(sign_name(s) for s in sign_sheet),
        "representative_coefficients": representative,
        "immediate_new_target_checks": checks,
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
    examples = [
        (
            "generic_scalene",
            (1.0, 0.0, 0.0),
            (1.0, 1.0, 0.0),
        ),
        (
            "equal_length_noncollinear",
            (1.0, 0.0, 0.0),
            (0.0, 1.0, 0.0),
        ),
    ]
    sign_sheets = {
        "+++": (+1, +1, +1),
        "++-": (+1, +1, -1),
        "+--": (+1, -1, -1),
    }

    reports = []
    for geom_name, p, q in examples:
        for sheet_name, sheet in sign_sheets.items():
            reports.append(triad_report(f"{geom_name}_{sheet_name}", p, q, sheet))

    out_path = ROOT / "closure_audit.json"
    out_path.write_text(json.dumps(to_serializable(reports), indent=2))

    summary_lines = []
    for item in reports:
        summary_lines.append(f"{item['name']}:")
        for tau, coeff in item["representative_coefficients"].items():
            summary_lines.append(
                f"  representative target sign {tau}: |C|="
                f"{abs(coeff['value']):.6f}"
            )
        for check in item["immediate_new_target_checks"]:
            mags = {
                tau: abs(info)
                for tau, info in check["coefficients"].items()
            }
            summary_lines.append(
                f"  pair {tuple(check['pair'])} -> {tuple(check['target'])}: "
                f"|C_+|={mags['+']:.6f}, |C_-|={mags['-']:.6f}"
            )
    (ROOT / "closure_audit_summary.txt").write_text("\n".join(summary_lines) + "\n")


if __name__ == "__main__":
    main()
