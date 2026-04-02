# Exploration 002 Summary — Normalization + Entangled-State Modular Hamiltonian

## Goal
(A) Resolve the TTH normalization ambiguity — physical time = t or β×t?
(B) Compute ΔK_A = K_A - βH_A for the bilinearly coupled global thermal state.

## Outcome: FULL SUCCESS

Both goals achieved with precision.

---

## Part A: Normalization — RESOLVED

**Answer: τ_physical = β × t_modular (option 2).**

Confirmed by three independent sources:
1. **Bisognano-Wichmann theorem**: K = (2π/a)H_R for Rindler wedge. Modular flow at t corresponds to proper time τ = (2π/a)t = β_U × t. (Calculation: τ = η = (2π/a)t for Rindler observer at ρ₀=1/a.)
2. **Martinetti-Rovelli (2003), eq. 18** (clearest statement): "β ≡ -τ/s", i.e., τ = β × |s|. Their Rindler check gives τ = (2π/a)|s| = β_U|s|. ✓
3. **Connes-Rovelli (1994)**: modular group at t corresponds to physical time flow at βt. Temperature = ratio of thermal time to geometric time.
4. **Haggard-Rovelli (2013)**: φ = (kT/ℏ)τ, so τ = βℏ × φ (thermal time). Used to derive correct Tolman-Ehrenfest relation.

**Consequence for oscillator comparison:**
With τ = β×t: σ_{τ/β}(q_A) = e^{iK_A τ/β} q_A e^{-iK_A τ/β}. At λ=0: K_A = βH_A → σ_{τ/β}(q_A) = e^{iH_A τ} q_A e^{-iH_A τ} = standard QM. ✓

---

## Part B: ΔK_A — COMPUTED AND CHARACTERIZED

### Main Result: ΔK_A ≠ 0 for λ ≠ 0

For the global Gibbs state ρ_AB = exp(-β(H_A + H_B + λq_A⊗q_B))/Z:
- At λ=0: ΔK_A = K_A - βH_A - cI = 0 (exact, to 6×10⁻¹⁵) ✓
- At λ=0.3, β=2.0: ||ΔK_A||_F = 3.768 (numerically large correction)

### Perturbative Order: ΔK_A = O(λ²)

**Power law fit:** ||ΔK_A||_F ~ 42.1 × λ^{1.998}

**Analytic proof that O(λ¹) vanishes:** The first-order Duhamel expansion gives δρ_A ∝ Tr_B[ρ_B q_B] = ⟨q_B⟩ = 0 (thermal expectation of position operator vanishes). Therefore the first-order modular Hamiltonian correction is zero.

### Structure of ΔK_A at O(λ²)

1. **Diagonal (linear in n):** ΔK_A[n,n] ≈ Δβ × n, with Δβ = -1.36λ² (effective temperature renormalization — coupling makes A appear hotter).
2. **Band-2 off-diagonal:** ΔK_A[n, n+2] ≈ C × √((n+1)(n+2)) × λ² (proportional to the matrix element of a²+a†², i.e., squeezing).
3. **All other bands:** zero (bands 1, 3, 4, ... are <3×10⁻⁴).
4. **Shape universality:** ΔK_A/λ² has identical shape at λ=0.05 and λ=0.3 (cosine similarity = 1.000). Confirms pure O(λ²) behavior.

**Physical interpretation:** Bilinear coupling generates a squeezed thermal state for A. K_A is the modular Hamiltonian of a Gaussian state with modified covariance, which has both temperature renormalization and squeezing corrections.

---

## Observable Prediction (The Discriminating Experiment)

With normalization τ=β×t, TTH predicts the q_A autocorrelation C(τ) = Tr[ρ_A q_A σ_{τ/β}(q_A)] to have a different period than standard QM C_QM(τ) = Tr[ρ_A q_A e^{iH_A τ} q_A e^{-iH_A τ}]:

| λ    | Δτ/τ (measured)  |
|------|-----------------|
| 0.05 | 0.170% |
| 0.10 | 0.684% |
| 0.20 | 2.79%  |
| 0.30 | 6.48%  |
| 0.40 | 12.1%  |
| 0.50 | 20.3%  |

**Formula:** Δτ/τ ≈ 0.68 × λ² (to leading order; increases slightly at large λ).

**Direction:** TTH predicts LONGER period (slower oscillation). Physical cause: Δβ < 0 (A appears hotter), giving effective frequency (β/β_eff)ω_A < ω_A when normalized by β.

---

## Key Takeaway (Single Most Important Finding)

**For the bilinearly coupled thermal state at single temperature β, ΔK_A ≠ 0 and TTH (with correct τ=β×t normalization) gives a LONGER autocorrelation period than standard QM by Δτ/τ ≈ 0.68λ².** This is genuine, computable, and observable. TTH and QM are distinguishable for entangled states.

---

## Leads Worth Pursuing

1. **Phase 2 computation:** Vary β (at fixed λ=0.3) — what is the β-dependence of the coefficient 0.68? Does the period shift become larger at low temperature (large β)?
2. **Analytic formula for ΔK_A:** Second-order Duhamel expansion gives an analytic expression for ΔK_A. This could derive the exact coefficient 0.68 and show its dependence on ω_A, ω_B, β.
3. **Non-equilibrium states:** If ρ_AB is not a Gibbs state (e.g., locally thermal but not globally: ρ_A(β_A) ⊗ ρ_B(β_B)), ΔK_A will differ. This is the original "TTH vs QM" question from Exploration 001.
4. **Experimental proposal:** The 6.4% period shift at λ=0.3 is in principle observable with coupled quantum oscillators. What physical system would realize this? (Coupled trapped ions? Coupled bosonic modes in circuit QED?)

---

## Unexpected Findings

- **The sign and structure of ΔK_A**: Not just a temperature shift but also a SQUEEZING correction. This is unexpected and not obvious from the setup. The off-diagonal band-2 structure (proportional to a²+a†²) means the entangled modular Hamiltonian is that of a squeezed thermal state.
- **Normalization subtlety in Connes-Rovelli**: There is a genuine notational ambiguity in the original 1994 paper (they write "t = βτ" which superficially looks like option 1, but their own Bisognano-Wichmann calculation confirms option 2). Martinetti-Rovelli (2003) is the cleaner reference.

---

## Computations Identified

1. **Analytic ΔK_A via second-order Duhamel:** Compute the full O(λ²) formula analytically. Inputs: ρ_A^{(0)} = exp(-βH_A)/Z_A, C_B(s) = Tr[ρ_B q_B(s)q_B]. Output: closed-form ΔK_A. Difficulty: ~50-100 lines of symbolic manipulation (doable with SymPy). This would confirm and generalize the numerical result.
2. **β-dependence of period shift:** Run period_shift.py at multiple β values (β=1, 2, 4, 8) with λ=0.3 fixed. About 20 minutes of computation. Would reveal whether the O(λ²) coefficient scales as β², β, or something else — important for identifying the regime of maximum TTH-QM discrepancy.
