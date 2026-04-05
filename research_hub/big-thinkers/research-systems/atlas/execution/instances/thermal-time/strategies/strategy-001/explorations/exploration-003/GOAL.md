# Exploration 003 — Full QM vs Local TTH: The Critical Comparison

## Mission Context

You are working on the Connes-Rovelli thermal time hypothesis (TTH) mission. The mission asks: does TTH predict physical behavior that differs from standard quantum thermodynamics?

**This is the most important exploration so far.** Prior explorations established the mathematical toolkit and found that the local modular Hamiltonian K_A differs from βH_A for coupled oscillators (ΔK_A ≠ 0, O(λ²)). The question is now: does this ΔK_A cause the TTH autocorrelation to actually differ from the standard QM autocorrelation?

---

## The Core Issue (Read This First)

Exploration-002 computed ΔK_A ≠ 0 and found a period shift Δτ/τ ≈ 0.68λ². But it compared against the **wrong baseline**: the free oscillator under H_A alone.

The correct comparison is:

- **TTH prediction:** C_local(τ) = Tr[ρ_A · (e^{iK_A τ/β} x_A e^{-iK_A τ/β}) · x_A]
  Uses the LOCAL modular Hamiltonian K_A of subsystem A.

- **Standard QM prediction:** C_full(τ) = Tr[ρ_{AB} · (e^{iH_AB τ} x_A e^{-iH_AB τ}) · x_A]
  Uses the FULL coupled Hamiltonian H_AB acting on both A and B.

**Key identity:** For the global Gibbs state, K_{AB} = βH_{AB} exactly. So the global TTH prediction = standard QM prediction (they agree by construction for the global state). The question is whether the **local** TTH prediction (using K_A) agrees with QM.

**Why they might differ:** C_full evolves x_A under H_AB — this entangles A and B, creating normal-mode beating (two frequencies ω_±). C_local evolves x_A under K_A/β — this is a unitary flow on A's Hilbert space alone (no entanglement generation, one effective frequency). These are structurally different: one has beats, the other doesn't.

**If C_local ≠ C_full:** TTH's local interpretation gives a genuinely different prediction from standard QM. The period shift (or beat structure) is a novel TTH signature.

**If C_local = C_full:** TTH exactly reproduces standard QM for equilibrium coupled oscillators. The local modular flow somehow captures the full many-body dynamics — which would itself be a remarkable mathematical result.

---

## Your Goal: Three Computations, One Comparison

### Computation 1 — C_full_QM(τ) via Exact Diagonalization

**Setup:**
- Two harmonic oscillators: H_A = ω a†a, H_B = ω b†b (set ω = 1.0)
- Bilinear coupling: H_int = λ · q_A ⊗ q_B where q = (a + a†)/√2
- Full Hamiltonian: H_AB = H_A + H_B + H_int
- Global Gibbs state at β = 2.0: ρ_{AB} = e^{-β H_AB} / Z

**Compute:**
C_full(τ) = Tr[ρ_{AB} · x_A(τ) · x_A] where x_A(τ) = e^{iH_AB τ} x_A e^{-iH_AB τ}

In matrix form:
```python
C_full[i] = Tr[rho_AB @ (expm(1j * H_AB * tau[i]) @ x_A @ expm(-1j * H_AB * tau[i]))]
            * Tr[rho_AB @ x_A]  # but actually this is the 2-point function
```

More carefully: C_full(τ) = Tr[ρ_{AB} x_A(τ) x_A] = Tr[ρ_{AB} e^{iH_AB τ} x_A e^{-iH_AB τ} x_A]

Use the eigendecomposition of H_AB for efficiency:
- H_AB V = V Λ (eigenvalues Λ, eigenvectors V)
- x_A(τ) = V diag(e^{iΛτ}) V† x_A V diag(e^{-iΛτ}) V†
- C_full(τ) = Tr[ρ_{AB} x_A(τ) x_A]

**Parameters:** N_trunc = 20 per mode, β = 2.0, ω_A = ω_B = 1.0. Run for λ ∈ {0.1, 0.2, 0.3, 0.5}. Time range τ ∈ [0, 4π] with 500 points.

**Normal mode check:** For small λ, verify that C_full(τ) shows beating between ω_+ and ω_- (predicted by normal mode analysis). The beating frequency is ω_+ - ω_- ≈ λ/ω. This verifies the computation.

---

### Computation 2 — C_local_TTH(τ) via Local Modular Flow

**Load K_A from exploration-002.** The exploration-002 code directory has `compute_modular_v2.py` and `sweep_results_v2.json`. Use the same K_A computation as exploration-002 (or recompute for consistency):

For each λ, compute:
1. ρ_A = partial_trace(expm(-β H_AB)/Z, system=B)
2. K_A = -logm(ρ_A)
3. C_local(τ) = Tr[ρ_A · (expm(1j * K_A * τ / β) @ x_A @ expm(-1j * K_A * τ / β)) · x_A]

---

### Computation 3 — C_global_TTH(τ) as Control

**This should equal C_full_QM exactly.** Since K_{AB} = βH_{AB} for the Gibbs state:
C_global(τ) = Tr[ρ_{AB} · (expm(1j * K_AB * τ / β) @ x_A @ expm(-1j * K_AB * τ / β)) · x_A]
            = Tr[ρ_{AB} · (expm(1j * H_AB * τ) @ x_A @ expm(-1j * H_AB * τ)) · x_A]
            = C_full(τ)

Verify this numerically (should agree to machine precision). This is a consistency check.

---

### Analysis — What the Comparison Tells Us

For each λ value, produce:

1. **Time series plot:** C_full(τ), C_local(τ), C_global(τ) on the same axes. Can you see a visual difference?

2. **Frequency analysis:** FFT of each signal. Report the dominant frequency (or frequencies) in each. Does C_full show two peaks at ω_+ and ω_-? Does C_local show one peak at an effective ω_eff?

3. **Period shift:** For C_local vs C_full, define the period shift as the time of first zero-crossing shift. Compare to exploration-002's formula Δτ/τ ≈ 0.68λ² (now with the correct baseline).

4. **Norm of difference:** Compute ||C_full - C_local||_2 / ||C_full||_2 over the time window. How large is the relative discrepancy?

5. **Physical prediction table:** Fill in:
   | λ    | ω_eff (local TTH) | ω_+, ω_- (QM normal modes) | Beat frequency | ||C_full - C_local||/||C_full|| |
   |------|--------------------|----------------------------|----------------|-------------------------------|
   | 0.1  | ...                | ...                        | ...            | ...                            |
   | 0.3  | ...                | ...                        | ...            | ...                            |
   | 0.5  | ...                | ...                        | ...            | ...                            |

---

## Additional Analysis: Local vs Global Modular Flow

This is the conceptual heart of the exploration. The local modular flow σ_t^{K_A} and the restriction of the global modular flow σ_t^{K_AB}|_A are related by the **Takesaki theorem**: for a Gibbs state, the restriction of the global modular flow to A is NOT the same as the local modular flow of ρ_A, except in special cases (e.g., when A and B are uncoupled).

**Literature question (brief):** Does Connes-Rovelli explicitly say whether TTH should use the local or global modular flow? Look at their Section 3 (or wherever they discuss subsystems) in the 1994 paper. The answer will determine whether:
- TTH = QM (if TTH uses global modular flow, which = H_AB dynamics)
- TTH ≠ QM (if TTH uses local modular flow, which ≠ H_AB dynamics when λ≠0)

Report what you find, but do not spend more than 30 minutes on this literature search — the computation is more important.

---

## Rigor Requirements

- **Verify C_global = C_full:** Report the maximum absolute difference. It should be < 10^{-10}.
- **Beat structure in C_full:** Confirm the FFT peak positions match ω_± = √(ω² ± λ) to within 1%.
- **Stability check:** Run at N=15 and N=25. Report whether C_local changes by more than 1% (tests Fock truncation sensitivity).

---

## Prior Results (Pre-Loaded Context)

**From exploration-001:**
- K_A = βH_A + (constant) for uncoupled thermal oscillator (K_{λ=0} = βH_A exactly)
- Modular flow σ_t(x_A) = cos(β ω t) x_A + sin(β ω t) p_A/ω (product state)
- KMS condition verified numerically

**From exploration-002:**
- ΔK_A = K_A - βH_A has: diagonal part Δβ = -1.36λ² (temperature renormalization) + band-2 off-diagonal (squeezing ∝ a²+a†²)
- ||ΔK_A||_F ~ 42.1 × λ^{1.998} (power law, O(λ²) confirmed)
- Normalization: τ_physical = β × t_modular (confirmed by Connes-Rovelli 1994, Martinetti-Rovelli 2003, Haggard-Rovelli 2013)
- With correct normalization: C_local(τ) oscillates at ω_eff = ω(β/β_eff) where β_eff = β + Δβ ≈ β(1 - 1.36λ²/β)

**Exploration-002 code:** `/Users/seanross/kingdom_of_god/home-base/research_hub/big-thinkers/research-systems/atlas/execution/instances/thermal-time/strategies/strategy-001/explorations/exploration-002/code/`
- `compute_modular_v2.py` — computes ρ_A, K_A via partial trace + matrix log
- `sweep_results_v2.json` — sweep results for λ ∈ [0, 0.5]

You can import or copy-paste the partial trace and K_A computation functions from `compute_modular_v2.py`.

---

## Failure Paths

1. **If C_global ≠ C_full at more than 10^{-6}:** The Fock space truncation is causing significant error. Increase N or reduce the λ range to where the coupling is small enough. Report the error and what parameter regime is reliable.

2. **If C_local = C_full to within numerical precision:** This would mean the local modular flow exactly reproduces the global dynamics. Report this as a significant result — there may be a theorem that explains it (perhaps for Gaussian states the local modular flow IS the restriction of the global flow). Search for this theorem.

3. **If the FFT shows more than 2 peaks in C_full:** The Fock truncation N=20 may be aliasing. Check by increasing to N=25.

4. **If the literature is ambiguous on local vs. global:** Report both interpretations and proceed computationally with both. The numbers will distinguish them.

---

## Output

**Write to:** `/Users/seanross/kingdom_of_god/home-base/research_hub/big-thinkers/research-systems/atlas/execution/instances/thermal-time/strategies/strategy-001/explorations/exploration-003/`

1. `REPORT.md` — sections: (1) Setup, (2) C_full_QM results + normal mode analysis, (3) C_local_TTH results, (4) C_global_TTH control check, (5) Comparison table, (6) Frequency analysis, (7) Interpretation — is TTH distinguishable from QM?
2. `REPORT-SUMMARY.md` — written LAST as completion signal
3. `code/` — all Python scripts

**Write REPORT.md incrementally.** Write the skeleton first, then fill sections.

---

## The Single Most Important Number

At the end of the exploration, report: **||C_full - C_local||_2 / ||C_full||_2** for λ = 0.3, β = 2.0, τ ∈ [0, 4π]. This is the fractional discrepancy between TTH and standard QM for the autocorrelation function. If this number is ≫ numerical noise, TTH makes a genuinely novel prediction.
