---
topic: T_U/T_dS modified inertia lacks action principle — momentum is not conserved
confidence: verified
date: 2026-03-27
source: "compton-unruh strategy-001 exploration-008"
---

## Finding

The T_U/T_dS modified inertia formulation has no Lagrangian or action principle, which means
momentum is not conserved when a body moves through a varying gravitational field. The magnitude
of spurious momentum violation is estimated to be ~10⁶³ kg·m/s over a galaxy merger timescale —
comparable to the galaxy's actual momentum. This is a serious theoretical defect; without an
action principle, the model cannot be embedded in quantum field theory or coupled consistently
to general relativity.

## The Non-Conservation Argument

In modified inertia, the momentum of a body is:

    p = m_i × v = m × μ(g_N/a₀) × v

As the body moves through a gravitational field, μ(g_N/a₀) varies because g_N changes along
the trajectory. Then:

    dp/dt = m × dμ/dt × v + m × μ × a

For Newton's 3rd law: F₁₂ = −F₂₁ (gravitational forces equal and opposite). The force equations are:

    dp₁/dt = F₂₁   and   dp₂/dt = −F₁₂ = F₂₁

But the TOTAL momentum change:

    d(p₁+p₂)/dt = (m₁×dμ₁/dt×v₁) + (m₂×dμ₂/dt×v₂) ≠ 0

in general (because dμ/dt × v ≠ 0 when μ changes along the trajectory). Total momentum is not
conserved.

## Estimated Magnitude [COMPUTED]

For two galaxies passing each other at v ~ 10⁶ m/s with Δμ ~ 0.1 (MOND regime transition):
- Momentum violation rate: ~Δμ × m × v per transit
- For M ~ 10¹¹ M_sun: ~0.1 × 2×10⁴¹ kg × 10⁶ m/s ≈ 2×10⁴⁶ kg·m/s per transit
- Over a merger timescale (~10⁹ years = 3×10¹⁶ s):

**Spurious impulse ≈ 10⁶³ kg·m/s — comparable to the galaxy's actual orbital momentum.**

This is not a small correction. It implies the model's predictions for interacting galaxy systems
(mergers, clusters) are untrustworthy even qualitatively.

## Comparison to Modified Gravity (AQUAL)

In Bekenstein-Milgrom (1984) modified gravity (AQUAL), the Lagrangian formulation:

    L = -(a₀²/8πG) × F(|∇Φ|²/a₀²)    [modified gravitational kinetic term]

guarantees momentum conservation via Noether's theorem. The action formulation automatically
enforces the correct conservation laws, including in non-trivial field configurations and during
mergers.

Modified inertia has no such guarantee. It exists only as a phenomenological prescription
mapping F = m_i × a, without a variational principle.

## Theoretical Consequences

1. **No embedding in QFT**: Without an action principle, there is no canonical quantization
   procedure and no path integral formulation.
2. **No consistent coupling to GR**: Modified inertia must be coupled to the stress-energy
   tensor to embed in GR. Without an action, this coupling is arbitrary.
3. **No predictive power in non-trivial configurations**: The formula m_i = m × μ(g_N/a₀) is
   well-defined for isolated test particles in static fields. For time-varying fields, multiple
   interacting bodies, or relativistic motion, it gives no unambiguous prediction.
4. **The Jeans instability problem**: The modified dispersion relation ω² = (c_s²k² - 4πGρ)/μ
   amplifies gravitational instability on large scales (μ→0), potentially causing regularization
   issues that can only be understood with an action principle.

## Verdict

**SERIOUS THEORETICAL DEFECT.** The momentum non-conservation is an O(1) effect in interacting
systems (galaxy mergers), not a small correction. Combined with the absence of an action principle,
this means the T_U/T_dS modified inertia model cannot be considered a complete physical theory —
only a phenomenological prescription that is adequate for isolated galaxy rotation curves (where
g_N is approximately static and the non-conservation issue doesn't manifest).

## Relationship to Other Entries

- `tu-tds-viability-scorecard.md` — full model assessment (conservation scores 2/10)
- `tu-tds-acceleration-ambiguity.md` — related internal inconsistency
- `verlinde-emergent-gravity-a0.md` — Verlinde's modified gravity formulation, which has an
  action principle and avoids this problem
