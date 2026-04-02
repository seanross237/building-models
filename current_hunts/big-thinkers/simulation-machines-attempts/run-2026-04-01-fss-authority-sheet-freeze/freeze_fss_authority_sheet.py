#!/usr/bin/env python3
"""Freeze `F_SS(1/12)` against the repaired Step-7 authority sheet."""

from __future__ import annotations

import argparse
import importlib.util
import json
import sys
from fractions import Fraction
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DOSSIER_PATH = (
    ROOT
    / "codex-philosopher-atlas"
    / "missions"
    / "exact-ns-no-near-closed-tao-circuit"
    / "steps"
    / "step-004"
    / "explorations"
    / "exploration-003"
    / "code"
    / "pro_circuit_dossier_check.py"
)
REPAIR_PATH = (
    ROOT
    / "codex-philosopher-atlas"
    / "missions"
    / "exact-ns-no-near-closed-tao-circuit"
    / "steps"
    / "step-005"
    / "explorations"
    / "exploration-001"
    / "code"
    / "repair_sheet_lock.py"
)
STEP7_RESULTS_PATH = (
    ROOT
    / "codex-philosopher-atlas"
    / "missions"
    / "exact-ns-no-near-closed-tao-circuit"
    / "steps"
    / "step-007"
    / "RESULTS.md"
)

MU = Fraction(1, 12)
RHO = Fraction(1, 16)


def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


DOSSIER = load_module(DOSSIER_PATH, "fss_authority_dossier_module")
REPAIR = load_module(REPAIR_PATH, "fss_authority_repair_module")


def frac_str(value: Fraction) -> str:
    return f"{value.numerator}/{value.denominator}" if value.denominator != 1 else str(value.numerator)


def sum_fields(data: dict[str, Fraction], fields: tuple[str, ...]) -> Fraction:
    total = Fraction(0)
    for field in fields:
        total += data[field]
    return total


def repaired_sheet():
    return {
        "Delta_tmpl": REPAIR.max_row("Delta_tmpl").value,
        "Delta_spec": REPAIR.max_row("Delta_spec").value,
        "L_tot": REPAIR.max_row("L_tot").value,
        "L_mirror": REPAIR.max_row("L_mirror").value,
        "L_companion": REPAIR.max_row("L_companion").value,
        "L_feedback": REPAIR.max_row("L_feedback").value,
        "L_cross": REPAIR.max_row("L_cross").value,
    }


def witness_metrics():
    data = DOSSIER.f_ss(MU)
    return {
        "int_I_D_on": sum_fields(
            data,
            ("Q_clk", "Q_seed", "Q_amp", "Q_rot_D", "Q_rot_A", "Q_next"),
        ),
        "int_I_D_off": sum_fields(
            data,
            ("D_mirror", "D_companion", "D_feedback", "D_cross"),
        ),
        "Delta_tmpl": data["Delta_tmpl"],
        "Delta_spec": data["Delta_spec"],
        "L_tot": sum_fields(
            data,
            ("D_mirror", "D_companion", "D_feedback", "D_cross"),
        ),
        "L_mirror": data["D_mirror"],
        "L_companion": data["D_companion"],
        "L_feedback": data["D_feedback"],
        "L_cross": data["D_cross"],
    }


def boundary_metrics():
    data = DOSSIER.f_sl(RHO)
    return {
        "Delta_tmpl": data["Delta_tmpl"],
        "Delta_spec": data["Delta_spec"],
        "L_tot": sum_fields(
            data,
            ("D_mirror", "D_companion", "D_feedback", "D_cross"),
        ),
        "L_mirror": data["D_mirror"],
        "L_companion": data["D_companion"],
        "L_feedback": data["D_feedback"],
        "L_cross": data["D_cross"],
    }


def comparison_rows():
    sheet = repaired_sheet()
    witness = witness_metrics()
    rows = []
    for key in ("Delta_tmpl", "Delta_spec", "L_tot", "L_mirror", "L_companion", "L_feedback", "L_cross"):
        rows.append(
            {
                "metric": key,
                "f_ss": witness[key],
                "threshold": sheet[key],
                "passes": witness[key] <= sheet[key],
                "saturates": witness[key] == sheet[key],
                "friendly_saturator": REPAIR.max_row(key).witness,
            }
        )
    return rows


def payload():
    witness = witness_metrics()
    boundary = boundary_metrics()
    sheet = repaired_sheet()
    rows = comparison_rows()
    return {
        "witness_name": "F_SS(mu=1/12)",
        "boundary_template_witness": "F_SL(rho=1/16)",
        "canonical_packet_sheet": "canonical one-bridge role-labeled helical packet P_n = (A_n, B_n, C_n, D_n, E_n) with mandatory conjugate completion",
        "desired_channels": ["A->B", "A->C", "B,C->C", "C,A<->D", "D,D->E"],
        "spectator_classes": ["mirror", "companion", "feedback", "cross"],
        "fixed_window": "[0, 1]",
        "normalization": "|A_n(0)| = 1, arg A_n(0) = 0, and int_I D_on = 1 after the allowed whole-sheet exact scaling",
        "same_currency_rule": "Compare G_tmpl and G_leak only on the same frozen packet sheet, same window, and same D_on/D_off split; t_clk, t_trig, t_rot, and t_next remain diagnostics only.",
        "witness_metrics": witness,
        "boundary_metrics": boundary,
        "repaired_thresholds": sheet,
        "comparison_rows": rows,
        "historical_variance": {
            "L_cross": {
                "old_step4_threshold": REPAIR.OLD_THRESHOLDS["Lambda_cross"],
                "friendly_ceiling": REPAIR.max_row("L_cross").value,
                "controlling_authority": REPAIR.max_row("L_cross").value,
                "reason": "Some earlier helper/report artifacts still show L_cross = 1/12, but Step 7 treats those as historical variance only and freezes the later repaired branch authority at L_cross <= 1/24.",
            }
        },
        "sources": {
            "dossier_script": str(DOSSIER_PATH),
            "repair_script": str(REPAIR_PATH),
            "controlling_step7_result": str(STEP7_RESULTS_PATH),
        },
    }


def stringify(value):
    if isinstance(value, Fraction):
        return frac_str(value)
    if isinstance(value, dict):
        return {key: stringify(item) for key, item in value.items()}
    if isinstance(value, list):
        return [stringify(item) for item in value]
    return value


def print_text(data):
    print("Frozen witness:")
    print(f"  {data['witness_name']} on {data['fixed_window']}")
    print(f"  packet sheet: {data['canonical_packet_sheet']}")
    print(f"  same-currency rule: {data['same_currency_rule']}")
    print()

    print("Witness metrics versus repaired thresholds:")
    for row in data["comparison_rows"]:
        status = "pass" if row["passes"] else "fail"
        saturation = " (saturates)" if row["saturates"] else ""
        print(
            f"  {row['metric']}: {frac_str(row['f_ss'])} <= {frac_str(row['threshold'])}"
            f" [{status}{saturation}; repair witness: {row['friendly_saturator']}]"
        )
    print()

    print("Boundary-friendly witness kept in authority sheet:")
    print(f"  {data['boundary_template_witness']}")
    for key, value in data["boundary_metrics"].items():
        print(f"    {key}: {frac_str(value)}")
    print()

    print("Historical variance note:")
    cross = data["historical_variance"]["L_cross"]
    print(
        "  L_cross old threshold"
        f" {frac_str(cross['old_step4_threshold'])},"
        f" friendly ceiling {frac_str(cross['friendly_ceiling'])},"
        f" controlling authority {frac_str(cross['controlling_authority'])}"
    )
    print(f"  reason: {cross['reason']}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true", help="print a JSON snapshot")
    args = parser.parse_args()

    data = payload()
    if args.json:
        print(json.dumps(stringify(data), indent=2, sort_keys=True))
        return
    print_text(data)


if __name__ == "__main__":
    main()
