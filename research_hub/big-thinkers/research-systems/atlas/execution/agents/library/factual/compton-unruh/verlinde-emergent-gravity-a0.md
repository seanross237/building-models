---
topic: Verlinde emergent gravity — derives a₀ = cH₀/6 from de Sitter entropy
confidence: provisional
date: 2026-03-27
source: "compton-unruh strategy-001 exploration-003"
---

## Finding

Verlinde's emergent gravity program derives the MOND acceleration scale a₀ = cH₀/6 ≈ 1.1 × 10⁻¹⁰ m/s² from first principles via the competition between area-law and volume-law entropy in de Sitter space. This is within 9% of Milgrom's empirical a₀ ≈ 1.2 × 10⁻¹⁰ m/s².

## Mechanism

Gravity is not fundamental but emerges from the entanglement structure of an underlying microscopic theory. In de Sitter space (our universe with positive Λ), two entropy contributions compete:

1. **Area-law entropy** — standard holographic bound, scaling as surface area (Bekenstein-Hawking)
2. **Volume-law entropy** — from the thermal character of the cosmological horizon, scaling as volume

The volume-law contribution overtakes the area law at the cosmological horizon scale. At sub-Hubble scales, de Sitter microstates don't fully thermalize, creating "memory effects" — an entropy displacement caused by matter. The response to this displacement produces an additional "dark" gravitational force.

**Derived acceleration scale:**

    a₀ = cH₀/6 ≈ 1.1 × 10⁻¹⁰ m/s²

The factor of 6 arises from the specific geometry of entropy displacement in de Sitter space. Ratio to observed: a₀(Verlinde)/a₀(obs) ≈ 0.92 — within 8%.

## Connection to the Unruh Effect and de Sitter Crossover

Verlinde (2011) explicitly uses the Unruh temperature T = ℏa/(2πck_B) as a key ingredient in deriving Newton's law from thermodynamics. The 2017 paper extends this to de Sitter space where competition between Unruh and Gibbons-Hawking thermal effects creates the transition at a ~ cH₀. This is closely related to the de Sitter crossover already established (see `gibbons-hawking-crossover.md`) and the T_U/T_dS = μ_MOND identity (see `tu-tds-mond-identity.md`).

## Key Equation and Deep-MOND-Only Limitation

Verlinde (2016) derives the apparent dark matter mass for a spherically symmetric point mass (his eq. 7.40):

    M_D²(r) = (cH₀/6G) × r² × d/dr[r × M_B(r)]

For a POINT MASS M_B = M (constant), d/dr(rM) = M, giving:

    g_D = G × M_D / r² = √((cH₀/6) × G × M_B / r²) = √(a₀_eff × g_B)

where a₀_eff = cH₀/6. This is the deep-MOND formula (g ≈ √(a₀ × g_B)).

**Critical limitation:** Verlinde does NOT derive a full interpolation function connecting the
Newtonian and deep-MOND regimes. He derives only the DEEP-MOND limit for point-mass exterior regions.
For extended mass distributions (inside galaxies), the d/dr(rM_B) term depends on the local mass
distribution gradient, making predictions depend on the distribution shape, not just the local
acceleration. This is why the theory fails inside dwarf spheroidals.

The factor of 6 arises from the specific geometry of entropy displacement: spatial volume of de Sitter,
area-to-volume ratio in the holographic calculation, and geometric factors in the 3D treatment
(4π factor from spherical averaging → factor of ~6).

## Observational Status (Updated)

- **Brouwer et al. (2017)** MNRAS 466, 2547: Weak lensing around 33,613 isolated galaxies — "good
  agreement" with Verlinde's predictions in the exterior regime (where the point-mass approximation
  holds). Encouraging but covers only the deep-MOND exterior region.
- **Lelli et al. (2017)** MNRAS Lett. 468, L68 (arXiv:1702.04355): Testing Verlinde against the
  Radial Acceleration Relation (RAR) — the tight empirical correlation between total and baryonic
  acceleration across thousands of galaxies. **Result: Verlinde's theory is INCONSISTENT with the
  RAR.** The RAR is naturally explained by standard MOND (which has a well-defined interpolation
  function); Verlinde gives different predictions in the interior of galaxies (where the mass
  distribution gradient matters).
- **Pardo (2017)** arXiv:1706.00785: Dwarf galaxy rotation curves "inconsistent" with Verlinde's
  predictions — interior failure as expected from the deep-MOND-only limitation.
- **Bullet Cluster**: Challenging, as with MOND.

**Rotation curve fits (compton-unruh E006):** NGC 3198 and NGC 2403 with a₀ = cH₀/6 give
χ²/dof ~ 1.21 and 0.52 respectively — fitting as well as or better than MOND. This is expected since
Verlinde (in the exterior point-mass regime) uses the same μ(x) = x/√(1+x²) functional form.

## Criticisms

| Critique | Author | Status |
|----------|--------|--------|
| Unphysical entropy required for arbitrary Newtonian potentials | Visser (2011) arXiv:1108.5240 | Moderate |
| Ultracold neutron experiments show quantum coherence, contradicting entropic thermodynamics | Kobakhidze (2011) Phys. Rev. D 83, 021502 | Moderate |
| Ordinary surfaces don't obey assumed thermodynamic laws | Several 2018 studies | Moderate |
| Dwarf galaxy failures | Pardo (2017) arXiv:1706.00785 | Moderate |

## Key Papers

- Verlinde (2011) JHEP 04, 029 [arXiv:1001.0785] — Newton from entropy + Unruh temperature
- Verlinde (2017) SciPost Phys. 2, 016 [arXiv:1611.02269] — de Sitter extension, derives a₀
- Jacobson (1995) gr-qc/9504004 — Einstein equations as equation of state; foundational for all entropic gravity

## Assessment

Most theoretically sophisticated of the surviving Unruh-based approaches. Derives a₀ from first principles (within 8%), avoids thermal-detection objection (uses entropy as structural quantity), connects to well-established holographic physics. But remains incomplete: Visser objection unresolved, cluster failures inherited from MOND, no fully rigorous derivation.
