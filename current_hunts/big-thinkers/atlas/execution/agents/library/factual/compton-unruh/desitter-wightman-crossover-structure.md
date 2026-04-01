---
topic: De Sitter Wightman function — same thermal structure, Planckian in all regimes
confidence: verified
date: 2026-03-27
source: "compton-unruh strategy-001 exploration-004"
---

## Finding

The de Sitter Wightman function has the **same functional form** (sinh⁻²) as the flat Rindler Wightman function, with the acceleration a/c replaced by α_eff = √(a²/c² + H₀²). The spectral density is exactly thermal (Planckian) in ALL acceleration regimes — no new peaks, resonances, or spectral shape changes. The de Sitter modification changes only the temperature parameter.

## Wightman Functions

**Flat space (Rindler):**

    G⁺_R(Δτ) = -(1/(4π²)) · (a/(2c))² / sinh²(a·Δτ/(2c) - iε)

KMS periodicity β_U = 2πc/a. Temperature T_U = ℏa/(2πck_B).

**De Sitter (accelerating observer):**

    G⁺_dS(Δτ) = -(H²/(16π²)) / sinh²(α_eff·Δτ/2 - iε)

where α_eff = √(a²/c² + H₀²). KMS periodicity β_dS = 2π/α_eff. Temperature:

    T_dS(a) = (ℏ/(2πk_B)) · √(a²/c² + H₀²) = (ℏ/(2πck_B)) · √(a² + c²H₀²)

**Key structural result:** Both functions have the SAME sinh⁻² form. The crossover replaces a/c with α_eff — it changes the characteristic timescale, not the functional shape. (Checked against Birrell & Davies; Deser & Levin 1997.)

## Temperature Crossover Table

| Acceleration | T_U (K) | T_dS (K) | T_dS/T_U |
|-------------|---------|----------|----------|
| 100 cH₀ | 2.67×10⁻²⁸ | 2.67×10⁻²⁸ | 1.000 |
| 10 cH₀ | 2.67×10⁻²⁹ | 2.69×10⁻²⁹ | 1.005 |
| cH₀ | 2.67×10⁻³⁰ | 3.78×10⁻³⁰ | 1.414 |
| 0.1 cH₀ | 2.67×10⁻³¹ | 2.69×10⁻³⁰ | 10.05 |
| 0.01 cH₀ | 2.67×10⁻³² | 2.67×10⁻³⁰ | 100.0 |
| a₀ (MOND) | 4.87×10⁻³¹ | 2.72×10⁻³⁰ | 5.586 |

At a = a₀, T_dS ≈ 5.6 × T_U — the de Sitter background dominates the thermal environment by a factor of ~5.6.

## Spectral Density: Exactly Planckian

The spectral density (Fourier transform of G⁺) is guaranteed thermal by the KMS condition:

    ρ(ω; T) = (ω/(2π)) · 1/(exp(ℏω/(k_BT)) - 1)

This holds exactly in all regimes. The total power scales as T_dS⁴:

    P(a) ~ T_dS⁴ = [ℏ/(2πck_B)]⁴ · (a² + c²H₀²)²

Power enhancement at low acceleration: P_dS/P_Rindler = [1 + (cH₀/a)²]²:
- At cH₀: factor 4
- At 0.1 cH₀: factor ~10⁴
- At 0.01 cH₀: factor ~10⁸

## Implication for Mechanism Search

Since the spectral form is always Planckian and the only change is the temperature T_dS(a), any force modification from the de Sitter crossover must come entirely from the temperature-dependent behavior of the thermal bath — not from any resonance, spectral edge, or new mode structure. This constrains the mechanism to expressions involving T_U and/or T_dS as variables (see `tu-tds-mond-identity.md`).
