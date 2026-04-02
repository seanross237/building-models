#!/usr/bin/env python3
"""Demonstrate the algebraic time-locality of the localized band-energy balance.

This is not an exact Navier-Stokes counterexample. It only exhibits families of
piecewise-constant windowed balance terms with fixed late witness gain and
arbitrarily small earlier precursor mass.
"""

from __future__ import annotations


def family_late_burst_only(delta: float, total_window: float, gain: float, early_precursor: float) -> dict[str, float]:
    """Late gain is carried entirely by the late-window flux difference."""

    early_length = total_window - delta
    pi_ell_early = 0.0 if early_length == 0 else early_precursor / early_length
    pi_ell_late = gain / delta

    p_flux_minus = pi_ell_early * early_length
    witness_gain = pi_ell_late * delta

    return {
        "early_precursor": early_precursor,
        "pi_ell_early": pi_ell_early,
        "pi_ell_late": pi_ell_late,
        "late_transport": 0.0,
        "late_viscous": 0.0,
        "p_flux_minus": p_flux_minus,
        "late_witness_gain": witness_gain,
    }


def family_late_burst_plus_transport(
    delta: float, total_window: float, gain: float, early_precursor: float
) -> dict[str, float]:
    """Split the late gain between late-window flux and transport."""

    early_length = total_window - delta
    pi_ell_early = 0.0 if early_length == 0 else early_precursor / early_length
    pi_ell_late = 0.5 * gain / delta
    late_transport = 0.5 * gain / delta

    p_flux_minus = pi_ell_early * early_length
    witness_gain = (pi_ell_late + late_transport) * delta

    return {
        "early_precursor": early_precursor,
        "pi_ell_early": pi_ell_early,
        "pi_ell_late": pi_ell_late,
        "late_transport": late_transport,
        "late_viscous": 0.0,
        "p_flux_minus": p_flux_minus,
        "late_witness_gain": witness_gain,
    }


def format_row(label: str, values: dict[str, float]) -> str:
    return (
        f"{label:26s}  "
        f"{values['early_precursor']:12.6g}  "
        f"{values['pi_ell_early']:12.6g}  "
        f"{values['pi_ell_late']:12.6g}  "
        f"{values['late_transport']:12.6g}  "
        f"{values['late_witness_gain']:12.6g}"
    )


def main() -> None:
    delta = 0.2
    total_window = 1.0
    gain = 1.0
    precursor_levels = [1.0, 1e-2, 1e-6, 0.0]

    print("delta =", delta)
    print("total_window =", total_window)
    print("target late witness gain =", gain)
    print()
    print(
        "family                      "
        "early_P^-      pi_ell^-      pi_ell^+late  "
        "transport_late  gain_late"
    )
    print("-" * 94)

    for epsilon in precursor_levels:
        row = family_late_burst_only(delta, total_window, gain, epsilon)
        print(format_row("late_burst_only", row))

    print("-" * 94)

    for epsilon in precursor_levels:
        row = family_late_burst_plus_transport(delta, total_window, gain, epsilon)
        print(format_row("late_burst_plus_transport", row))

    print()
    print("Interpretation:")
    print("- In both families the late witness gain stays fixed at 1.")
    print("- The earlier precursor mass P_flux^- can be made arbitrarily small.")
    print("- This demonstrates only that the windowed balance form itself has no")
    print("  algebraic mechanism forcing late gain to depend on earlier P_flux^- .")


if __name__ == "__main__":
    main()
