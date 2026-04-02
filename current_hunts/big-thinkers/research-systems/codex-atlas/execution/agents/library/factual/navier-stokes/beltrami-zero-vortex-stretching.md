---
topic: ABC (Beltrami) flows and z-invariant vortex tubes have zero vortex stretching identically
confidence: verified
date: 2026-03-30
source: "navier-stokes strategy-001 exploration-003"
---

## ABC Flow (Beltrami)

For ABC flow with omega = u, the vortex stretching integral:

integral(S*omega*omega) = integral((u*grad)u * u) = 0

by incompressibility (integration by parts with div(u) = 0 on periodic domain). This gives VS = 0 at all times for inviscid evolution. With viscosity, the flow decays exponentially while remaining near-Beltrami, with VS staying negligible. [COMPUTED]

## Z-Invariant Vortex Tubes

With vorticity purely in the z-direction and no z-variation, the strain tensor S acts only in the x-y plane while omega is in z, giving:

integral(S*omega*omega) = 0

identically. **Fix:** Adding sinusoidal z-modulation (e.g., omega_z = profile(r) * [1 + A*cos(z)]) breaks the z-symmetry and restores nonzero vortex stretching. For anti-parallel tubes, oscillating the tube x-centers as pi +/- delta*sin(z) mimics vortex reconnection geometry. [COMPUTED]

## Significance

These are exact symmetry degeneracies, not numerical artifacts. They represent edge cases where the vortex stretching inequality is trivially satisfied (both sides = 0). When designing initial conditions for vortex stretching studies, z-symmetry breaking must be explicitly included.
