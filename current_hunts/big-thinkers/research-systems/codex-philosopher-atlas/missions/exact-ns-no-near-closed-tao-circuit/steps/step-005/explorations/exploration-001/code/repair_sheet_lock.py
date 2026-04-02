from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction


def frac_str(x: Fraction) -> str:
    return f"{x.numerator}/{x.denominator}" if x.denominator != 1 else str(x.numerator)


@dataclass(frozen=True)
class WitnessRow:
    value: Fraction
    witness: str


F_SS = {
    "Delta_tmpl": WitnessRow(Fraction(1, 6), "F_SS(mu=1/12)"),
    "Delta_spec": WitnessRow(Fraction(1, 6), "F_SS(mu=1/12)"),
    "L_tot": WitnessRow(Fraction(1, 4), "F_SS(mu=1/12)"),
    "L_mirror": WitnessRow(Fraction(1, 12), "F_SS(mu=1/12)"),
    "L_companion": WitnessRow(Fraction(1, 12), "F_SS(mu=1/12)"),
    "L_feedback": WitnessRow(Fraction(1, 24), "F_SS(mu=1/12)"),
    "L_cross": WitnessRow(Fraction(1, 24), "F_SS(mu=1/12)"),
}

F_SL = {
    "Delta_tmpl": WitnessRow(Fraction(1, 4), "F_SL(rho=1/16)"),
    "Delta_spec": WitnessRow(Fraction(49, 256), "F_SL(rho=1/16)"),
    "L_tot": WitnessRow(Fraction(49, 256), "F_SL(rho=1/16)"),
    "L_mirror": WitnessRow(Fraction(1, 16), "F_SL(rho=1/16)"),
    "L_companion": WitnessRow(Fraction(1, 16), "F_SL(rho=1/16)"),
    "L_feedback": WitnessRow(Fraction(1, 16), "F_SL(rho=1/16)"),
    "L_cross": WitnessRow(Fraction(1, 256), "F_SL(rho=1/16)"),
}

OLD_THRESHOLDS = {
    "lambda_tmpl": Fraction(1, 3),
    "lambda_spec": Fraction(1, 4),
    "Lambda_tot": Fraction(3, 8),
    "Lambda_mirror": Fraction(1, 8),
    "Lambda_companion": Fraction(1, 12),
    "Lambda_feedback": Fraction(1, 12),
    "Lambda_cross": Fraction(1, 12),
}


def max_row(metric: str) -> WitnessRow:
    rows = [F_SS[metric], F_SL[metric]]
    return max(rows, key=lambda row: row.value)


def main() -> None:
    friendly_ceiling = {
        "lambda_tmpl": max_row("Delta_tmpl"),
        "lambda_spec": max_row("Delta_spec"),
        "Lambda_tot": max_row("L_tot"),
        "Lambda_mirror": max_row("L_mirror"),
        "Lambda_companion": max_row("L_companion"),
        "Lambda_feedback": max_row("L_feedback"),
        "Lambda_cross": max_row("L_cross"),
    }
    repaired = dict(friendly_ceiling)
    repaired["Lambda_cross"] = WitnessRow(
        OLD_THRESHOLDS["Lambda_cross"],
        "unchanged; Step 4 records no uniform hostile cross-gap above 1/24",
    )

    print("# Friendly Maxima")
    for key in (
        "Delta_tmpl",
        "Delta_spec",
        "L_tot",
        "L_mirror",
        "L_companion",
        "L_feedback",
        "L_cross",
    ):
        row = max_row(key)
        print(f"{key}: {frac_str(row.value)}  [{row.witness}]")

    print()
    print("# Repair Sheet")
    for key in (
        "lambda_tmpl",
        "lambda_spec",
        "Lambda_tot",
        "Lambda_mirror",
        "Lambda_companion",
        "Lambda_feedback",
        "Lambda_cross",
    ):
        old = OLD_THRESHOLDS[key]
        new = repaired[key].value
        slack_removed = old - new
        print(
            f"{key}: {frac_str(old)} -> {frac_str(new)}"
            f"  [slack removed = {frac_str(slack_removed)}; saturated by {repaired[key].witness}]"
        )

    print()
    print("# Friendly Ceilings Not All Promoted To Repairs")
    print(
        "Lambda_cross friendly ceiling:"
        f" {frac_str(friendly_ceiling['Lambda_cross'].value)}"
        f"  [{friendly_ceiling['Lambda_cross'].witness}]"
    )
    print(
        "Lambda_cross authorized repair: unchanged at"
        f" {frac_str(repaired['Lambda_cross'].value)}"
        " because the hostile Step-4 cross entry is only delta."
    )

    print()
    print("# Exact Gap Notes From Recorded Anti Data")
    print("lambda_tmpl: anti value recorded only symbolically as 1/2 - O(delta); exact numeric gap is not pinned by Step 4.")
    print(
        "lambda_spec: (11/24 + delta) - 49/256"
        f" = {frac_str(Fraction(11, 24) - Fraction(49, 256))} + delta"
    )
    print(
        "Lambda_tot: (11/24 + delta) - 1/4"
        f" = {frac_str(Fraction(11, 24) - Fraction(1, 4))} + delta"
    )
    print(
        "Lambda_mirror: 1/8 - 1/12"
        f" = {frac_str(Fraction(1, 8) - Fraction(1, 12))}"
    )
    print(
        "Lambda_companion: 1/6 - 1/12"
        f" = {frac_str(Fraction(1, 6) - Fraction(1, 12))}"
    )
    print(
        "Lambda_feedback: 1/6 - 1/16"
        f" = {frac_str(Fraction(1, 6) - Fraction(1, 16))}"
    )
    print("Lambda_cross: delta - 1/24; not uniformly positive on the recorded delta-range, so cross is not the live hostile overload entry.")


if __name__ == "__main__":
    main()
