---
topic: McCulloch Quantized Inertia — mechanism, negative mass problem, critiques
confidence: provisional
date: 2026-03-27
source: "compton-unruh strategy-001 exploration-003"
---

## Finding

McCulloch's Quantized Inertia (QI / MiHsC) proposes that inertia arises from a Casimir-like truncation of Unruh modes at the Hubble horizon, but the theory's core equation yields **negative inertial mass** at exactly the MOND-relevant accelerations it is meant to explain, and contains additional mathematical errors identified by Renda (2019).

## Mechanism

McCulloch proposes that when an object's acceleration decreases, the Unruh wavelengths it perceives lengthen. When these exceed the cosmic horizon diameter Θ ≈ 8.8 × 10²⁶ m, they are "disallowed" — a Hubble-scale Casimir effect that reduces available Unruh modes and hence inertial mass.

**Core equation:**

    m_i = m(1 - 2c²/(|a|Θ))

Critical acceleration where m_i → 0:

    a_min = 2c²/Θ ≈ 2.0 × 10⁻¹⁰ m/s²

In the deep-MOND regime, McCulloch derives:

    v⁴ = 2GMc²/Θ

giving v ∝ M^(1/4) — the baryonic Tully-Fisher relation. For the Milky Way (~6 × 10¹⁰ M☉), this predicts v ≈ 201 km/s (observed ~220 km/s). McCulloch (2017) fits 153 SPARC galaxies comparably to MOND.

## Critical Problem: Negative Inertial Mass

The formula becomes **negative** when a < a_min = 2c²/Θ ≈ 2.0 × 10⁻¹⁰ m/s². Since MOND operates at a₀ ≈ 1.2 × 10⁻¹⁰ m/s² < a_min:

    m_i/m ≈ 1 - (2.0 × 10⁻¹⁰)/(1.2 × 10⁻¹⁰) ≈ −0.70

The theory gives m_i/m ≈ −0.70 at the very scale it is supposed to explain galaxy rotation curves. This is unphysical. McCulloch's actual galaxy fits appear to use a modified version, but the published formula as written is internally inconsistent in its key regime.

## Published Critique: Renda (2019)

**Renda (2019)** MNRAS 489, 881 [arXiv:1908.01589] identified two additional derivation errors:
1. The function F(a) = B_s(a)/B(a) (ratio of discrete to continuous blackbody spectra) is NOT the monotonic linear function McCulloch claims — it has a peak at a_p ≈ 1.2 × 10⁻⁹ m/s² where F ≈ 2.17.
2. The peak wavelength contributes only a tiny fraction of total energy density; using it alone misrepresents the full spectrum.
Conclusion: flaws "require a major rethinking of the whole theory."

## Distinction from Compton-Unruh Resonance

McCulloch's QI is **NOT** based on a Compton-Unruh resonance. It does NOT invoke the proton Compton frequency. The critical acceleration a_min = 2c²/Θ is universal (mass-independent), while the Compton-Unruh matching acceleration a* = 2πmc³/ℏ is mass-dependent and 43 orders of magnitude too large. These are entirely different hypotheses.

**Conceptual insight that survives:** Mode truncation at the Hubble horizon is physically motivated (modes with λ > Hubble radius are unphysical) and is not subject to the thermal-detection objection. This is a distinct, potentially viable idea — but McCulloch's mathematical implementation of it is fatally flawed.

## Community Reception

DARPA funded McCulloch with $1.3M (2018) and $17.4M via the Otter program (2024). Published in EPL and Astrophys. Space Sci. but widely considered fringe. One physicist described it as "a concatenation of buzz words and bullshit."

## Key Papers

- McCulloch (2007) EPL 90, 29001
- McCulloch (2017) Astrophys. Space Sci. 362, 149 [arXiv:1709.04918]
- Renda (2019) MNRAS 489, 881 [arXiv:1908.01589]
