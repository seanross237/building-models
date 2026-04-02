from __future__ import annotations

from fractions import Fraction
from math import sqrt


LAMBDA_TMPL = Fraction(1, 3)
LAMBDA_SPEC = Fraction(1, 4)
LAMBDA_TOT = Fraction(3, 8)
LAMBDA_MIRROR = Fraction(1, 8)
LAMBDA_COMPANION = Fraction(1, 12)
LAMBDA_FEEDBACK = Fraction(1, 12)
LAMBDA_CROSS = Fraction(1, 12)
LAMBDA_ITIN = Fraction(1, 3)


def frac_str(x: Fraction) -> str:
    return f"{x.numerator}/{x.denominator}" if x.denominator != 1 else str(x.numerator)


def f_ss(mu: Fraction) -> dict[str, Fraction]:
    return {
        "Q_clk": Fraction(1, 6),
        "Q_seed": mu,
        "Q_amp": Fraction(1, 3) - mu,
        "Q_rot_D": Fraction(1, 4),
        "Q_rot_A": Fraction(1, 12),
        "Q_next": Fraction(1, 6),
        "D_mirror": mu,
        "D_companion": mu,
        "D_feedback": mu / 2,
        "D_cross": mu / 2,
        "Delta_tmpl": 2 * mu,
        "Delta_spec": 2 * mu,
    }


def f_sl(rho: Fraction) -> dict[str, Fraction]:
    return {
        "Q_clk": Fraction(1, 4),
        "Q_seed": rho,
        "Q_amp": Fraction(1, 4) - rho,
        "Q_rot_D": Fraction(1, 4),
        "Q_rot_A": Fraction(1, 8),
        "Q_next": Fraction(1, 8),
        "D_mirror": rho,
        "D_companion": rho,
        "D_feedback": rho,
        "D_cross": rho * rho,
        "Delta_tmpl": Fraction(1, 4),
        "Delta_spec": 3 * rho + rho * rho,
    }


def summarize(name: str, data: dict[str, Fraction]) -> None:
    d_on = (
        data["Q_clk"]
        + data["Q_seed"]
        + data["Q_amp"]
        + data["Q_rot_D"]
        + data["Q_rot_A"]
        + data["Q_next"]
    )
    d_off = (
        data["D_mirror"]
        + data["D_companion"]
        + data["D_feedback"]
        + data["D_cross"]
    )
    print(name)
    print("  int_I D_on   =", frac_str(d_on))
    print("  int_I D_off  =", frac_str(d_off))
    print("  Delta_tmpl   =", frac_str(data["Delta_tmpl"]), "<=", frac_str(LAMBDA_TMPL), data["Delta_tmpl"] <= LAMBDA_TMPL)
    print("  Delta_spec   =", frac_str(data["Delta_spec"]), "<=", frac_str(LAMBDA_SPEC), data["Delta_spec"] <= LAMBDA_SPEC)
    print("  L_tot        =", frac_str(d_off), "<=", frac_str(LAMBDA_TOT), d_off <= LAMBDA_TOT)
    print("  L_mirror     =", frac_str(data["D_mirror"]), "<=", frac_str(LAMBDA_MIRROR), data["D_mirror"] <= LAMBDA_MIRROR)
    print("  L_companion  =", frac_str(data["D_companion"]), "<=", frac_str(LAMBDA_COMPANION), data["D_companion"] <= LAMBDA_COMPANION)
    print("  L_feedback   =", frac_str(data["D_feedback"]), "<=", frac_str(LAMBDA_FEEDBACK), data["D_feedback"] <= LAMBDA_FEEDBACK)
    print("  L_cross      =", frac_str(data["D_cross"]), "<=", frac_str(LAMBDA_CROSS), data["D_cross"] <= LAMBDA_CROSS)
    print("  Itinerary spectator ratio <=", frac_str(LAMBDA_ITIN), d_off <= LAMBDA_ITIN)
    print()


def main() -> None:
    mu = Fraction(1, 12)
    rho = Fraction(1, 16)
    summarize("F_SS(mu=1/12)", f_ss(mu))
    summarize("F_SL(rho=1/16)", f_sl(rho))
    rho_root = (-3 + sqrt(10)) / 2
    print("rho_template_root ~= %.6f" % rho_root)
    print("1/12 ~= %.6f" % (1 / 12))
    print("1/16 = 0.062500")


if __name__ == "__main__":
    main()
