#!/usr/bin/env python3
"""Minimal falsification model for harmonic far-field pressure on a local ball.

The model uses a uniform spherical shell on |y| = R with density 1/R against
the Newtonian kernel G(x) = 1 / (4*pi*|x|). By Newton's shell theorem the
resulting potential is exactly 1 on the interior ball |x| < R. We verify this
numerically at a few sample points and compute the local pairing exactly.
"""

from __future__ import annotations

import math


PI = math.pi
RADIUS_LOCAL = 1.0
RADIUS_SHELL = 2.0
TIME_LENGTH = 1.0


def cutoff_phi(radius: float) -> float:
    """Smooth radial cutoff supported on B_1."""
    if radius >= RADIUS_LOCAL:
        return 0.0
    return (1.0 - radius * radius) ** 2


def exact_shell_potential_inside() -> float:
    """Exact interior value from Newton's shell theorem."""
    return 1.0


def exact_pairing() -> float:
    """Integral over Q = B_1 x (-1, 0) of p_far * psi with psi=(1-|x|^2)^2."""
    radial_integral = (1.0 / 3.0) - (2.0 / 5.0) + (1.0 / 7.0)
    return TIME_LENGTH * 4.0 * PI * radial_integral


def local_energy_scale(amplitude: float) -> float:
    """Weighted local energy for the constant local field u_A = A e_1."""
    return amplitude * amplitude * exact_pairing()


def fibonacci_sphere_points(n: int, radius: float) -> list[tuple[float, float, float]]:
    """Nearly uniform points on a sphere for crude quadrature."""
    points = []
    golden_angle = PI * (3.0 - math.sqrt(5.0))
    for i in range(n):
        z = 1.0 - 2.0 * (i + 0.5) / n
        rho = math.sqrt(max(0.0, 1.0 - z * z))
        theta = golden_angle * i
        x = radius * rho * math.cos(theta)
        y = radius * rho * math.sin(theta)
        points.append((x, y, radius * z))
    return points


def approximate_shell_potential(
    x: tuple[float, float, float],
    n_points: int = 20000,
) -> float:
    """Approximate the shell potential at x by equal-area quadrature."""
    density = 1.0 / RADIUS_SHELL
    area = 4.0 * PI * RADIUS_SHELL * RADIUS_SHELL
    weight = area / n_points
    total = 0.0
    for y in fibonacci_sphere_points(n_points, RADIUS_SHELL):
        dx = x[0] - y[0]
        dy = x[1] - y[1]
        dz = x[2] - y[2]
        total += density * (1.0 / (4.0 * PI * math.sqrt(dx * dx + dy * dy + dz * dz))) * weight
    return total


def main() -> None:
    exact_potential = exact_shell_potential_inside()
    pairing = exact_pairing()

    print("Minimal harmonic far-field shell model")
    print(f"local cylinder Q = B_{RADIUS_LOCAL} x (-1, 0)")
    print(f"shell radius = {RADIUS_SHELL}")
    print(f"exact interior p_far value = {exact_potential:.12f}")
    print(f"exact pairing int_Q p_far * psi = {pairing:.12f}")
    print()

    print("Numerical shell-potential check at interior sample points")
    sample_points = [
        (0.0, 0.0, 0.0),
        (0.5, 0.0, 0.0),
        (0.25, 0.25, 0.25),
    ]
    for point in sample_points:
        approx = approximate_shell_potential(point)
        error = abs(approx - exact_potential)
        print(f"x={point}: approx={approx:.12f}, error={error:.3e}")
    print()

    print("Local energy-scale family u_A = A e_1")
    for amplitude in [1.0, 0.5, 0.25, 0.125]:
        energy = local_energy_scale(amplitude)
        ratio = pairing / math.sqrt(energy)
        print(
            f"A={amplitude:.3f}: U(A)={energy:.12f}, "
            f"pairing/U(A)^(1/2)={ratio:.12f}"
        )


if __name__ == "__main__":
    main()
