---
topic: TTH normalization resolved (τ = β·t_modular) and discriminating observable identified
confidence: verified
date: 2026-03-27
source: thermal-time/strategies/strategy-001/explorations/exploration-001/REPORT.md; exploration-002/REPORT.md; Connes & Rovelli (1994), Martinetti & Rovelli (2003), Haggard & Rovelli (2013)
---

## Summary

Two foundational results for the Connes-Rovelli Thermal Time Hypothesis (TTH): (1) the normalization ambiguity is resolved — physical proper time equals β times the modular time parameter (τ = β · t_modular), confirmed by the Bisognano-Wichmann theorem and three papers with explicit citations; (2) the discriminating observable between TTH and standard QM is the position autocorrelation function, which disagrees between theories when the subsystem is entangled with another (see `tth-deltaK-and-period-shift.md`).

## Part 1: Normalization Resolution

**The ambiguity (identified in exploration-001):** Two candidate identifications:
1. τ_physical = t_modular (no rescaling)
2. τ_physical = β × t_modular (physical time proportional to temperature)

**Resolution via Bisognano-Wichmann:**

For Rindler wedge with acceleration a, β_U = 2π/a:
- BW theorem: K = (2π/a) H_R = β_U H_R
- Modular flow acts as Rindler time evolution: η = (2π/a)·t = β_U · t
- Rindler proper time for observer at ρ₀=1/a: τ = η = β_U · t ✓

Therefore τ_physical = β × t_modular (option 2).

**Literature confirmation — three explicit quotes:**

- **Connes & Rovelli (1994), gr-qc/9406019, eq. 43:** α_t A = e^{iβtH} A e^{−iβtH} — modular flow at modular parameter t corresponds to physical evolution for time βt. Their summary: "temperature is the ratio between thermal time and geometrical time."
- **Martinetti & Rovelli (2003), gr-qc/0212074, eq. 18:** β = 1/T ≡ −τ/s (most explicit statement). In words: |τ| = β × |modular parameter|. Rindler case (eq. 31): τ = −(2π/a)s, so |τ| = β_U|s| ✓.
- **Haggard & Rovelli (2013), arXiv:1302.0724, eq. 13:** φ = (kT/ℏ)t — thermal time φ is (T/ℏ) times proper time. In units k=ℏ=1: τ = β × φ. Used to derive Tolman-Ehrenfest effect correctly.

**Cross-checks:**
- Product state recovery: σ_{τ/β}(A) = e^{iK_A(τ/β)} A e^{−iK_A(τ/β)} = e^{iH_A τ} A e^{−iH_A τ} — reproduces standard QM at λ=0 ✓
- Tolman-Ehrenfest direction: hotter system (higher T, lower β) → faster modular flow per unit physical time ✓

## Part 2: When TTH = QM

**Theorem:** TTH normalized (with τ=β·t) equals standard QM for subsystem A if and only if K_A = βH_A + const·I, which holds if and only if ρ_A is a Gibbs state for H_A.

**Implication:**
- Uncoupled (λ=0): ρ_A = e^{−βH_A}/Z_A → K_A = βH_A + const → TTH normalized = QM (verified numerically)
- Any non-trivial entangling coupling (λ≠0): ΔK_A = K_A − βH_A ≠ 0 → TTH deviates from QM

The regime where TTH makes new predictions is exactly the entangled case (see `tth-deltaK-and-period-shift.md`).

## Part 3: The Discriminating Observable

**Observable:** C(τ) = ⟨q_A(τ) q_A(0)⟩_ρ — position autocorrelation for oscillator A.

**In the product state (λ=0):**
- TTH (normalized): σ_{τ/β}(q_A) oscillates at ω_A (exact QM agreement)
- Standard QM: q_A(τ) oscillates at ω_A
- No discrimination possible

**In the entangled state (λ≠0):**
- TTH (normalized): period is τ₀^{TTH} = π/(2ω_eff) where ω_eff < ω_A (shifted by ΔK_A)
- Standard QM: period is τ₀^{QM} = π/(2ω_A)
- At λ=0.3: Δτ/τ = 6.4% (TTH period longer by 6.4%)

**Comparison (λ=0.3, β=2.0, ω_A=ω_B=1.0):**

| Observable | TTH normalized | Standard QM |
|-----------|----------------|-------------|
| Period τ₀ (first zero) | 1.672 | 1.571 (= π/2) |
| Period ratio TTH/QM | 1.064 | 1.000 |
| Amplitude (2n̄+1)/(2mω) | 0.6565 | 0.6565 |
| Depends on β_A? | YES (through K_A) | Only through initial state |

**Quantitative formula (leading order):** Δτ/τ ≈ 0.71 × λ² (confirmed numerically to λ^{2.07}).

The position autocorrelation period is the best discriminating observable because:
1. It differs between theories even with correct normalization (unlike frequency confusion before E002)
2. The difference is O(λ²) and grows monotonically with coupling
3. The amplitude factor cancels (same in TTH and QM), leaving a clean period shift
