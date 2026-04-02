#!/usr/bin/env python3

"""Print the elementary F_DT trigger bound used in the report."""


def main() -> None:
    print("F_DT trigger upper bound on the frozen normalized window I = [0, 1]")
    print(
        "Assumption: |C'(t)| <= K_seed * delta + K_amp * |C(t)| and |C(0)| = eta."
    )
    print()
    print("Then Gronwall gives")
    print("  |C(t)| <= exp(K_amp) * (eta + K_seed * delta)  for 0 <= t <= 1.")
    print()
    print("On the explicit subregime eta <= delta^2 and delta <= 1, this simplifies to")
    print("  |C(t)| <= exp(K_amp) * (delta^2 + K_seed * delta)")
    print("         <= exp(K_amp) * (K_seed + 1) * delta.")
    print()
    print("Therefore the sufficient condition")
    print("  delta <= 1 / (4 * exp(K_amp) * (K_seed + 1))")
    print("implies")
    print("  |C(t)| <= 1/4 = theta_C on I,")
    print("so no trigger event occurs on the frozen window:")
    print("  t_trig > 1.")


if __name__ == "__main__":
    main()
