# Exploration 002 — Normalization Resolution + Entangled-State Modular Hamiltonian

## Goal Summary
Two-part investigation for the Connes-Rovelli Thermal Time Hypothesis (TTH):
- **Part A:** Resolve normalization ambiguity — does physical time = modular time, or physical time = β × modular time?
- **Part B:** Compute K_A for the globally coupled thermal state (two coupled oscillators, single temperature β) and determine if ΔK_A = K_A - β H_A ≠ 0.

---

## 1. Part A — Normalization Resolution

### The Two Options
1. τ_physical = t_modular (no rescaling)
2. τ_physical = β × t_modular (time rate proportional to temperature)

### Evidence from Bisognano-Wichmann Theorem

The normalization is pinned down by the Bisognano-Wichmann (BW) theorem for the Rindler wedge, which provides an independently verifiable test.

**BW setup:**
- For a Rindler wedge with Rindler acceleration a, the Minkowski vacuum |0⟩ is a thermal KMS state with Unruh temperature T_U = a/(2π) (in units ℏ=c=k_B=1), i.e., inverse temperature β_U = 2π/a.
- BW theorem: K = 2π K_boost = (2π/a) H_R, where H_R is the Rindler Hamiltonian (the generator of Rindler time translations).

**Identifying physical time:**
- The modular flow σ_t = e^{iKt}...e^{-iKt} = e^{i(2π/a)H_R t}...
- This corresponds to Rindler time evolution for Rindler time η = (2π/a) t.
- Physical proper time for the Rindler observer at ρ₀ = 1/a (proper acceleration a): the Rindler metric is ds² = -(ρ₀ a)² dη², giving dτ/dη = ρ₀ a = 1. So τ = η.
- Therefore: τ = η = (2π/a) t = β_U × t.

**Conclusion:** Physical proper time τ = β × t_modular (option 2).

### Tolman-Ehrenfest Cross-check

This normalization is also consistent with the Tolman-Ehrenfest effect. If τ_physical = β × t_modular:
- A system at temperature T has modular flow parameter running at rate dt/dτ = 1/β = T.
- Hotter system (higher T, lower β) has FASTER modular flow per unit physical time.
- This is CONSISTENT with Tolman-Ehrenfest: hotter = faster clock (at higher gravitational potential, where β is smaller).

### Literature Status: RESOLVED

All three papers confirm the normalization via direct quotes (see next section).

### Explicit Confirmation from Literature

**Connes & Rovelli (1994), gr-qc/9406019:**

Non-relativistic limit (their eq. 43): "α_t A = e^{iβtH} A e^{-iβtH}" — the modular flow at t equals physical Hamiltonian evolution for time βt.

Rindler case (their eq. 55): "α_t = β_{2πa⁻¹t}" — modular flow at t = proper time flow at τ = (2π/a)t = β_U × t.

Their interpretation: "temperature is the ratio between thermal time and geometrical time."

**Martinetti & Rovelli (2003), gr-qc/0212074:**

Equation (18), Section 2.4: **"β = 1/T ≡ −τ/s"** — most explicit statement.

In words: "the proportionality factor is minus the inverse temperature" between modular parameter s and physical time τ. So |τ| = β|s|.

Rindler case (their eq. 31): τ = −(2π/a)s, so |τ| = β_U|s|. ✓

The minus sign is acknowledged as "historical reasons" — the substantive content is |τ| = β × |s|.

**Haggard & Rovelli (2013), arXiv:1302.0724:**

Equation (13): "φ = (kT/ℏ)t" — thermal time φ is T/ℏ × proper time. Equivalently, proper time = ℏ/(kT) × thermal time = βℏ × thermal time. In units ℏ=k=1: τ = β × (modular parameter). ✓

Used to derive Tolman-Ehrenfest: dφ = (kT/ℏ)ds ⇒ T·√g₁₁ = const (correct T-E law). ✓

**Conclusion:** All three papers confirm **τ_physical = β × t_modular**. The normalization is option (2).

### Cross-Check: Product State Recovery

With τ = β × t:
σ_{τ/β}(A) = e^{iK_A (τ/β)} A e^{-iK_A (τ/β)} = e^{iHτ} A e^{-iHτ}

This exactly reproduces standard QM time evolution at zero coupling. ✓

---

## 2. Part B — Entangled-State K_A Computation

### Setup
- Two harmonic oscillators: H_A = ω_A a†a, H_B = ω_B b†b, with ω_A = ω_B = 1.0
- Bilinear coupling: H_int = λ q_A ⊗ q_B (where q = (a+a†)/√2)
- Global thermal state: ρ_AB = exp(-β H_AB)/Z, with β = 2.0
- Partial trace: ρ_A = Tr_B[ρ_AB]
- Modular Hamiltonian: K_A = -log(ρ_A) [computed via eigendecomposition, N=20 Fock truncation]
- Correction: ΔK_A = K_A - β H_A_red - c·I (scalar offset c chosen to zero the trace)

### Key Result: ΔK_A ≠ 0 for λ ≠ 0

The modular Hamiltonian of the coupled subsystem A does NOT equal β H_A. The coupling generates a genuine, non-trivial correction.

**Parameter sweep results (β=2.0, ω_A=ω_B=1.0):**

| λ    | ‖ΔK_A‖_F | ΔK[0,0] | ΔK[1,1] | ΔK[2,2] |
|------|-----------|---------|---------|---------|
| 0.00 | 0.000000  | 0.0000  | 0.0000  | 0.0000  |
| 0.05 | 0.105904  | 0.0315  | 0.0281  | 0.0247  |
| 0.10 | 0.423121  | 0.1260  | 0.1124  | 0.0988  |
| 0.15 | 0.950246  | 0.2828  | 0.2524  | 0.2219  |
| 0.20 | 1.685187  | 0.5013  | 0.4473  | 0.3933  |
| 0.25 | 2.625426  | 0.7804  | 0.6964  | 0.6124  |
| 0.30 | 3.768246  | 1.1191  | 0.9987  | 0.8782  |
| 0.35 | 5.110890  | —       | —       | —       |
| 0.40 | 6.650684  | —       | —       | —       |
| 0.45 | 8.385148  | —       | —       | —       |
| 0.50 | 10.312152 | —       | —       | —       |

---

## 3. ΔK_A Parameter Sweep and Perturbative Order

### Scaling: ΔK_A = O(λ²)

**Numerical finding:** Power law fit gives ‖ΔK_A‖_F ~ 42.1 × λ^{1.998}. Ratio test: ‖ΔK(2λ)‖/‖ΔK(λ)‖ = 3.9998 ≈ 4.0 (consistent with O(λ²)).

**Analytic explanation (why O(λ) vanishes):**

At first order in λ, the Duhamel perturbation series gives:
```
δρ_A = Tr_B[δρ_AB]
     = -λβ ∫₀¹ ds Tr_B[ρ_A^s ⊗ ρ_B^s (q_A⊗q_B) ρ_A^{1-s} ⊗ ρ_B^{1-s}]
     = -λβ ∫₀¹ ds (ρ_A^s q_A ρ_A^{1-s}) · Tr[ρ_B q_B]
     = 0
```
because ⟨q_B⟩ = Tr[ρ_B q_B] = 0 (thermal expectation value of position vanishes). This is verified numerically: Tr[ρ_B q_B] = 0 to machine precision.

Therefore, **ΔK_A starts at O(λ²)**, confirming the numerical scaling.

---

## 4. Structure of ΔK_A

### Off-diagonal Structure

At λ=0.3, ΔK_A has a very specific band structure:
- **Band 0 (diagonal):** Non-zero, contributes 2.956/3.768 = 78% of ‖ΔK‖_F
- **Band 2 (off-diagonal, |i-j|=2):** Non-zero! Contributes 1.652/3.768 = 44% of ‖ΔK‖_F
- **Bands 1, 3, 4, ...:** Essentially zero (< 3×10⁻⁴)

This band-2 structure is physically natural: H_int = q_A⊗q_B contains q_A = (a+a†)/√2, which at second order gives (q_A)² = (a+a†)²/2 = n + 1/2 + (a²+a†²)/2. The a² and a†² operators connect Fock states that differ by 2, giving exactly band-2 structure.

### Band-2 Matrix Elements

The off-diagonal elements at |i-j|=2 are:
```
ΔK_A[n, n+2] ≈ -0.0347 × √((n+1)(n+2))  [at λ=0.3]
```

This is precisely the matrix element of (a†² + a²) (the squeezing operator). Specifically:
- a†²[n+2, n] = √((n+1)(n+2)) — verified for n=1 to 17
- Coefficient: -0.0347 = -C × λ² / λ² for some constant C at λ=0.3

### Diagonal Structure

The diagonal of ΔK_A is approximately **linear in n** (i.e., proportional to H_A_red = ω_A n):
```
ΔK_A[n,n] ≈ Δβ × n + const  (the trace-zero normalization removes the const)
```
with Δβ ≈ -0.0136/λ² × λ² = -1.36 λ² (effective inverse temperature shift).

**At λ=0.3:** Δβ ≈ -0.120, giving effective inverse temperature β_eff ≈ 1.88 (hotter than actual β=2).

**Δβ scaling:** Δβ ~ λ^{1.98} (power law fit), confirming O(λ²).

### Physical Interpretation

To leading order in λ²:
```
K_A ≈ β_eff H_A + λ²·C(β,ω)·(a† + a)² + const·I
     ≈ β_eff H_A + λ²·C(β,ω)·(squeezing) + const·I
```

The coupling to B:
1. **Renormalizes temperature**: β_eff = β + Δβ = β - 1.36λ² (subsystem A appears hotter)
2. **Generates squeezing**: off-diagonal band-2 correction, meaning K_A is the Hamiltonian of a squeezed thermal state

This makes physical sense: bilinear coupling generates correlations that appear as effective squeezing in the marginal state of A. A Gaussian thermal state coupled bilinearly becomes a Gaussian state with modified covariance matrix, and its modular Hamiltonian is a general quadratic (= squeezing + displacement + temperature).

### Shape Universality

The shape of ΔK_A/λ² is identical at λ=0.05 and λ=0.3 (cosine similarity = 1.0000). This confirms ΔK_A = λ² × f(β,ω) + O(λ⁴) with no λ³ correction.

---

## 5. Modular Flow Comparison

### Setup
For λ=0.3, β=2.0: computed three autocorrelation functions C(τ) = Tr[ρ_A q_A q_A(τ)]:

1. **TTH (bare modular)**: q_A(t) = e^{iK_A t} q_A e^{-iK_A t}, t = modular parameter
2. **Standard QM**: q_A(τ) = e^{iH_A τ} q_A e^{-iH_A τ}, τ = physical time
3. **TTH (normalized)**: same as TTH but with normalization τ = β·t, so q_A(τ) = σ_{τ/β}(q_A)

### Results

**First zero crossing (quarter-period) at λ=0.3:**
- TTH bare modular: t₀ = 0.836 (modular time)
- QM Heisenberg: τ₀ = π/2 = 1.571 (physical time)
- TTH normalized (τ=β·t): τ₀ = 1.672 (physical time)

**Ratio TTH normalized / QM: 1.672 / 1.571 = 1.064** (6.4% longer period for TTH)

### Interpretation

With normalization τ = β·t:
- At λ=0 (product state): TTH normalized = QM exactly (verified: both give τ₀ = π/2)
- At λ=0.3: TTH normalized gives a 6.4% LONGER period than QM
  - Due to Δβ = -0.120: effective frequency ω_eff = 1/(β_eff) × ω = 1/1.88 × 1 ≈ 0.532 (vs QM ω=1/β×β = 1... hmm)

More precisely: the period is determined by the full K_A (including squeezing), not just the diagonal part. The 6.4% shift incorporates both the diagonal renormalization AND the squeezing correction.

**This is the genuine TTH prediction**: for a bilinearly coupled quantum system at temperature β, the TTH-predicted position autocorrelation has a period LONGER than the standard Hamiltonian evolution of the isolated subsystem A. The correction is O(λ²):

**Period shift formula (computed):** Δτ/τ ≈ 0.68 × λ² (leading order) with higher-order corrections.

**Detailed period shift results (β=2.0, ω_A=ω_B=1.0):**

| λ    | τ_TTH (norm) | τ_QM   | Δτ/τ     |
|------|-------------|--------|----------|
| 0.00 | 1.5708      | 1.5708 | 0.000000 |
| 0.05 | 1.5735      | 1.5708 | 0.001702 |
| 0.10 | 1.5815      | 1.5708 | 0.006841 |
| 0.20 | 1.6146      | 1.5708 | 0.027877 |
| 0.30 | 1.6726      | 1.5708 | 0.064804 |
| 0.40 | 1.7609      | 1.5708 | 0.121036 |
| 0.50 | 1.8896      | 1.5708 | 0.202971 |

Power law fit: Δτ/τ ~ λ^{2.07} (consistent with O(λ²) + higher-order terms).

---

## 6. Interpretation — Are TTH and QM Different?

### Direct Answer: YES (with the correct normalization)

For the globally coupled thermal state ρ_AB = e^{-βH_AB}/Z with bilinear coupling H_int = λq_A⊗q_B:

1. ΔK_A = K_A - βH_A - c·I ≠ 0 for λ ≠ 0 (**confirmed**)
2. ΔK_A is O(λ²) (**confirmed analytically and numerically**)
3. With normalization τ=β·t (from Bisognano-Wichmann), TTH gives a 6.4% longer period than QM for λ=0.3 (**computed**)
4. At λ=0, TTH with normalization τ=β·t exactly reproduces standard QM (**verified**)

### Physical Meaning

TTH identifies physical time with modular flow. For an isolated system (λ=0), the modular Hamiltonian is K_A = βH_A, and TTH with normalization τ=β·t reduces to standard QM. This is the "trivial" case.

For an entangled system (λ≠0), the modular Hamiltonian K_A is NOT simply βH_A. It includes:
- A temperature renormalization (effective β decreases, system appears hotter)
- A squeezing correction (off-diagonal q_A²-type term)

The TTH-predicted time evolution σ_{τ/β}(q_A) is NOT the same as Heisenberg evolution e^{iH_A τ} q_A e^{-iH_A τ}. This constitutes a genuine discriminating prediction.

### When Does TTH = QM?

TTH (normalized) = QM for subsystem A if and only if K_A = βH_A + const·I, which happens if and only if:
- ρ_A is a Gibbs state for H_A: ρ_A = e^{-βH_A}/Z_A
- This is exactly the product state case λ=0 (or more generally: any coupling that doesn't change the marginal of A)

For all non-trivial couplings that entangle A with B, ΔK_A ≠ 0 and TTH deviates from QM.

---

## 7. Part C — Perturbative Order: COMPLETED

**Result:** ΔK_A = O(λ²).

**Analytic proof:** The O(λ¹) contribution to δρ_A vanishes because ⟨q_B⟩_{thermal} = 0 (odd-moment zero-point of the thermal state). Therefore the first-order correction to the modular Hamiltonian also vanishes.

**Implication for observability:** The TTH-QM difference scales as λ² for weak coupling. For λ=0.3, the 6.4% period shift corresponds to Δτ_period/τ_period ≈ 0.71 × λ². This is in principle observable for sufficiently large λ.

---

## 8. Literature Status (Part A — Normalization)

The Bisognano-Wichmann analysis strongly indicates normalization (2): τ = β × t_modular. This is consistent with:
- Rindler proper time correctly recovered from modular flow
- Unruh temperature correctly reproduced
- Standard QM recovered at λ=0 for product states
- Tolman-Ehrenfest effect direction (hotter = faster clock)

Literature agent fetching Connes-Rovelli (1994), Martinetti-Rovelli (2003), and Haggard-Rovelli (2013) to confirm with explicit citations. See below for updates.

---

## Appendix: Numerical Details

- Fock space truncation: N=20 per mode (total Hilbert space: 400×400)
- Modular Hamiltonian computed via eigendecomposition (NOT scipy.logm) to avoid issues with small eigenvalues
- At λ=0, ‖ΔK_A‖_F = 6×10⁻¹⁵ (machine precision) ✓
- Verification at each λ: Tr[ρ_A] = 1.000000, all eigenvalues positive
- Scripts: `code/compute_modular_v2.py`, `code/analyze_deltaK.py`, `code/off_diagonal_analysis.py`
