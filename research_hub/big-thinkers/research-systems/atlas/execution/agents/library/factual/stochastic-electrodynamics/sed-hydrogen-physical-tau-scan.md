---
topic: SED hydrogen T_ion(L) with physical radiation-reaction time τ
confidence: verified
date: 2026-03-27
source: "stochastic-electrodynamics strategy-003 exploration-002"
---

## Overview

Physical-τ T_ion(L) scan for SED hydrogen: 7 L values (0.4–1.0), 20 trajectories each, using the **physical** radiation-reaction time τ = 2/(3α³) = 2.591×10⁻⁷ a.u. This corrects the 60.6× error in s002-E003 (which used τ = 1.57×10⁻⁵ a.u.). This is the first quantitative T_ion(L) scan with physically correct τ.

**Method:** Landau-Lifshitz ALD (no runaway), RK4 integrator with C-compiled inner loop, chunked FFT ZPF generation (2^17 points/chunk), 140 trajectories total completed in ~24 seconds. ZPF PSD: S_F(ω) = 2τω³ for 0 < ω ≤ ω_max = 100 a.u. Sanity checks all pass: pure Coulomb orbit → machine-precision energy conservation; ZPF RMS = theoretical σ = 1.4358 a.u. exactly.

---

## Complete T_ion(L) Results [COMPUTED]

| L/ħ | N_ion/20 | Frac  | Median T_ion (periods) | ⟨r⟩/a₀ | Notes                              |
|-----|----------|-------|------------------------|---------|-------------------------------------|
| 0.4 | 20/20    | 1.00  | 94                     | 1.823   | 5 nuclear collisions (< 50 periods) |
| 0.5 | 20/20    | 1.00  | 448                    | 1.514   |                                     |
| 0.6 | 19/20    | 0.95  | 1,633                  | 1.356   | 1 survived 10K-period cap           |
| 0.7 | 12/20    | 0.60  | 3,895                  | 1.122   | 8 survived 10K-period cap           |
| 0.8 | 15/20    | 0.75  | 7,886                  | 1.421   | 5 survived 10K-period cap           |
| 0.9 |  3/20    | 0.15  | 9,638                  | 1.115   | 17 survived 10K-period cap          |
| 1.0 | 18/20    | 0.90  | 19,223                 | 1.509   | Extended to 50K periods; 2 survived |

T_ion(L) is **monotonically increasing** with L. [COMPUTED]

---

## Power Law [COMPUTED]

Fitting T_ion ∝ L^n for L = 0.4–0.8 (best statistics, n_ion ≥ 12/20):

**T_ion(L) ≈ 37,527 × L^6.44 orbital periods** (R² = 0.9961)

| L   | Observed (periods) | Predicted (periods) | Error |
|-----|--------------------|--------------------|-------|
| 0.4 | 94                 | 103                | +10%  |
| 0.5 | 448                | 434                | −3%   |
| 0.6 | 1,633              | 1,402              | −14%  |
| 0.7 | 3,895              | 3,780              | −3%   |
| 0.8 | 7,886              | 8,927              | +13%  |

The L^6.44 exponent is much larger than expected from simple diffusion theory (diffusion → T_ion ∝ L^2). Theoretical explanation is an open question.

---

## Key Physical Results

### L=1.0 Circular Orbit: Not Permanently Stable [COMPUTED]

- 18/20 trajectories ionize within 50,000 orbital periods
- Median T_ion = **19,223 orbital periods ≈ 2.9 ps** (1 orbital period ≈ 152 attoseconds for ground-state hydrogen)
- Min: 10,184 periods (~1.5 ps); Max: 49,443 periods (~7.5 ps)
- 2/20 survived the 50,000 period cap

**Open question:** Is this finite lifetime physical (SED hydrogen not truly stable) or an artifact of the UV cutoff ω_max = 100 a.u. < physical ω_max = m_ec²/ħ ≈ 2980 a.u.? At higher ω_max, both ZPF energy input and radiation damping increase; the balance point may shift to longer or possibly infinite lifetime.

### ⟨r⟩(L=1.0) Matches QM to 0.6% [COMPUTED]

| Quantity | Value |
|----------|-------|
| ⟨r⟩ from simulation | 1.509 a₀ |
| QM ⟨r⟩ for 1s state | 1.500 a₀ |
| Deviation | 0.6% |

ZPF-driven SED orbit reproduces QM ground state mean radius to 0.6%. Consistent with Cole & Zou (2003) short-run result.

### Non-Monotonic Ionization Fraction [CONJECTURED]

The ionization *fraction* (not timescale) is non-monotonic:
- L=0.7: 60% ionized → L=0.8: 75% ionized (unexpected reversal)
- L=0.9: only 15% ionized (sharp drop)

The L=0.8 > L=0.7 reversal is statistically marginal (overlapping binomial confidence intervals at N=20). The L=0.9 drop to 15% is more significant. Possible interpretation: near-circular orbits (L ≥ 0.9) transition to a quasi-stable regime on the 10,000-period timescale.

### L=0.4 Nuclear Collision Channel [COMPUTED]

5/20 L=0.4 trajectories ionize within 50 periods via a distinct mechanism. At L=0.4, the orbit has:
- Semi-major axis a = 0.543 a₀, eccentricity e = 0.840
- Pericenter r_min = 0.087 a₀ — very close to nuclear collision threshold r_NUKE = 0.05 a₀

ZPF perturbations easily push pericenter below r_NUKE, causing nuclear collision ionization. This is qualitatively distinct from the slow stochastic escape that governs L ≥ 0.5.

---

## Comparison with s002-E003 (Wrong-τ Data)

| L/ħ | E003 Median T_ion | Physical-τ Median | Observed ratio | Expected |
|-----|-------------------|-------------------|----------------|----------|
| 0.5 | 17 periods        | 448 periods       | 26.3×          | 60.6×    |
| 0.7 | 83 periods        | 3,895 periods     | 46.9×          | 60.6×    |
| 0.9 | 108 periods       | 9,638 periods     | 89.2×          | 60.6×    |

Observed scaling ratios (26×–89×) are **below the expected 60.6×** and increase with L. The deviation from simple 1/τ scaling reflects:
1. Radiation damping also scales as τ — at large τ (E003), radiation re-captures near-escape electrons, shortening T_ion relative to pure ZPF prediction
2. Statistical bias in E003 (200-period cap with 19/20 ionized underestimates the true median)
3. L-dependent effect — more pronounced for nearly-circular orbits where radiation damping is effective per unit time

---

## Relation to s002-E003 Adversarial Critique

E006 adversarial review identified the wrong-τ issue as the primary weakness of E003 results. This exploration directly addresses that critique:

- **τ is 60× too large [FIXED]** — all results now use physical τ = 2.591×10⁻⁷ a.u.
- **Only 4 L values [IMPROVED]** — this scan covers 7 L values (0.4–1.0)
- **No fine scan near L_crit [STILL OPEN]** — T_ion divergence structure near Nieuwenhuizen's L_crit = 0.588ħ still unmeasured; would require ~5 L values in [0.55, 0.65] range and long runs

Remaining open question: Kramers critical-slowing exponent T_ion ∝ (L − L_crit)^{−α} near L_crit ≈ 0.588ħ.

---

## References

- SED strategy-003 exploration-002 (2026-03-27): source computation
- Nieuwenhuizen, T.M. (2020). Front. Phys. 8, 335: L_crit = 0.588ħ threshold
- Cole, D.C. & Zou, Y. (2003). Phys. Lett. A 317, 14-20: physical τ = 2e²/(3m_ec³)
- See also: `hydrogen-self-ionization.md` for three-phase history and mechanism analysis
