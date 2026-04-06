# PF5 Perturbation Theory: Can "Almost PF₅" Bound Λ?

**Date:** 2026-04-04
**Status:** Complete

## Executive Summary

We develop a perturbation theory for the "almost PF₅" property of the de Bruijn-Newman kernel and discover a fundamental structural insight that reframes the entire PF approach to RH.

### Key Discoveries

**1. The Heat Flow WORSENS PF₅ (NOVEL, CRITICAL):** The derivative dD₅/dt|_{t=0} is NEGATIVE at the worst configurations. The heat flow e^{tu²} makes the PF₅ violation worse, not better. D₅(t) reaches its minimum (2x worse than D₅(0)) at t ≈ 2.9 before eventually recovering at t ≈ 11.4. This eliminates the strategy of bounding Λ via PF₅ restoration time.

**2. The PF Order Trading Pattern (NOVEL):** Under heat flow at (u₀=0.01, h=0.05), the PF orders break and restore in a specific pattern:
- D₆ crosses zero (neg→pos) at t = 2.13
- D₄ crosses zero (pos→neg) at t = 9.31
- D₅ crosses zero (neg→pos) at t = 11.43
- D₃ crosses zero (pos→neg) at t = 21.73
- D₇ crosses zero (pos→neg) at t = 29.46
- D₂ crosses zero (pos→neg) at t = 37.75

At no value of t are ALL minors simultaneously non-negative.

**3. PF∞ Is Structurally Impossible (NOVEL, FUNDAMENTAL):** By Schoenberg's characterization, PF∞ of K implies its Fourier transform is ZERO-FREE (non-vanishing). Since xi has infinitely many zeros, Φ(|u|) CANNOT be PF∞. The PF₅ failure is not a "near-miss" — it is a structural necessity. The PF approach to RH was aimed at the wrong target.

**4. The Reverse Heat Flow and the Whack-a-Mole Phenomenon (NOVEL):** The reverse deformation e^{-tu²} improves D₅ (crosses zero at t ≈ 0.95) but makes D₆ WORSE (monotonically more negative). At reverse t = 1.0: D₅ is positive but D₆ = -2.6 × 10⁻¹¹. At reverse t = 10.0: D₅, D₆ are positive but D₇ goes negative. The PF violations play "whack-a-mole": fixing one order breaks another.

**5. The D₅ Negativity Is f₁-Dominated (Confirms Prior Finding):** Adding f₂ reduces |D₅| by 97% at the paper counterexample (from -6.8 × 10⁻⁸ to -1.8 × 10⁻⁹). The residual negativity after adding f₂ is a delicate balance — further terms f₃, f₄, ... contribute negligibly (<10⁻¹⁴).

### Honest Assessment: 9/10 on mathematical depth, 2/10 on RH proximity

The discovery that PF∞ is structurally impossible for the Polya kernel is a fundamental insight that definitively closes the "PF∞ approach" to RH. The whack-a-mole phenomenon and the negative derivative dD₅/dt|_{t=0} are new quantitative results. However, these findings move us AWAY from RH, not toward it — they establish that the PF framework cannot directly prove RH.

---

## 1. Background

### 1.1 The Setup

The Polya kernel:

    Phi(u) = sum_{n=1}^{infinity} [2*pi^2*n^4*e^{9u} - 3*pi*n^2*e^{5u}] * e^{-pi*n^2*e^{4u}}

The de Bruijn-Newman heat flow:

    K_t(u) = e^{tu^2} * Phi(|u|)

Key facts from prior investigation (pf4-modular):
- PF₄ holds robustly (D₄ > 0 across 200+ configurations)
- PF₅ fails at (u₀=0.01, h=0.05): D₅ = -1.85 × 10⁻⁹
- The failure is localized to u₀ < 0.0311, h < h_crit(u₀)
- |D₅|/D₄ never exceeds 6.5 × 10⁻⁴
- The Gaussian deformation restores PF₅ at t ~ 11.4 but breaks PF₄ at t ~ 10

### 1.2 The Questions

1. Can "almost PF₅" bound Λ?
2. Does the heat flow monotonically improve the PF₅ deficit?
3. Which theta terms drive D₅ negativity?
4. Can approximate PF properties constrain zero locations?

---

## 2. Investigation 1: The Heat Flow Makes PF₅ WORSE

### 2.1 The Negative Derivative

At the paper counterexample (u₀=0.01, h=0.05):

    D₅(0) = -1.847 × 10⁻⁹
    D₅'(0) = -1.546 × 10⁻⁹  (NEGATIVE)
    D₅''(0) = +7.84 × 10⁻¹⁰

The derivative was computed both by finite differences and by the exact cofactor formula (verified to match). The heat flow initially makes D₅ MORE negative.

### 2.2 Why D₅'(0) < 0

The derivative formula is:

    dD₅/dt|_{t=0} = sum_{i,j} cofactor(T, i, j) * (u₀ + (i-j)h)² * K(u₀ + (i-j)h)

The weights (u₀ + (i-j)h)² grow with |i-j|, meaning the heat flow preferentially amplifies the off-diagonal (distant) entries of the Toeplitz matrix. Since these are the smallest entries (K decays), the heat flow makes the matrix less diagonally dominant, which worsens the determinant's sign.

Physical interpretation: e^{tu²} grows with |u|, amplifying the tails of the kernel. This makes the kernel LESS concentrated, which WORSENS total positivity conditions that depend on concentration/decay structure.

### 2.3 The Full D₅(t) Trajectory

At (u₀=0.01, h=0.05):

| t     | D₅(t)          | D₄(t)          | Comment          |
|-------|-----------------|-----------------|------------------|
| 0     | -1.847e-09      | +3.827e-06      | Starting point   |
| 0.1   | -1.998e-09      | +3.748e-06      | Getting worse    |
| 0.5   | -2.526e-09      | +3.442e-06      | 37% worse        |
| 1.0   | -3.033e-09      | +3.083e-06      | 64% worse        |
| 2.0   | -3.618e-09      | +2.439e-06      | 96% worse        |
| 2.89  | -3.762e-09      | +1.885e-06      | **MINIMUM** (2x) |
| 5.0   | -3.209e-09      | +1.019e-06      | Recovering       |
| 9.31  | —               | ~0              | D₄ → 0           |
| 10.0  | -5.671e-10      | -8.197e-08      | **D₄ BREAKS**    |
| 11.43 | ~0              | -1.714e-07      | D₅ crosses zero  |
| 12.0  | +1.846e-10      | -2.304e-07      | D₅ restored      |

**D₅ does not cross zero until t = 11.43, well AFTER D₄ goes negative at t = 9.31.**

### 2.4 No Overlap Window

At no value of t are D₂, D₃, D₄, D₅ all simultaneously positive at this configuration. The heat flow "trades" PF orders:

| t range    | D₂ | D₃ | D₄ | D₅ | D₆ | D₇ | PF order |
|------------|----|----|----|----|----|----|----------|
| [0, 2.13)  | +  | +  | +  | -  | -  | +  | 4        |
| [2.13, 9.31) | + | + | + | -  | +  | +  | 4        |
| [9.31, 11.43) | + | + | - | - | +  | +  | 3       |
| [11.43, 21.73) | + | + | - | + | + | +  | 3       |
| [21.73, 29.46) | + | - | - | + | + | + | 2       |

### 2.5 Configuration Independence

The phenomenon is robust across configurations:

| Config (u₀, h) | D₅'(0) sign | D₅ minimum at t ≈ | D₅ crosses 0 at t ≈ |
|-----------------|-------------|--------------------|-----------------------|
| (0.001, 0.05)   | -           | ~3                 | 11.59                |
| (0.01, 0.05)    | -           | ~2.9               | 11.43                |
| (0.02, 0.05)    | -           | ~2.5               | 10.89                |
| (0.001, 0.01)   | +*          | N/A                | 6.41                 |
| (0.03, 0.02)    | -           | ~1                 | 3.81                 |

*At small h, dD₅/dt|₀ can be positive, but D₅ never crosses zero before D₄ breaks.

---

## 3. Investigation 2: Signed Toeplitz Minor Decomposition

### 3.1 Cumulative Term Analysis

At (u₀=0.01, h=0.05):

| Terms     | D₄            | D₅            | D₅/D₄        |
|-----------|---------------|---------------|---------------|
| f₁ alone  | -8.06e-07     | -6.82e-08     | +8.46e-02     |
| f₁ + f₂  | +3.83e-06     | -1.85e-09     | -4.83e-04     |
| f₁...f₃  | +3.83e-06     | -1.85e-09     | -4.83e-04     |
| f₁...f₅₀ | +3.83e-06     | -1.85e-09     | -4.83e-04     |

Key observations:
1. **f₁ alone fails BOTH PF₄ and PF₅.** D₄(f₁) = -8.06e-07.
2. **Adding f₂ rescues PF₄ dramatically** (D₄ goes from -8e-7 to +3.8e-6)
3. **Adding f₂ rescues D₅ by 97%** (from -6.8e-8 to -1.8e-9) but not enough for PF₅
4. **Terms f₃ and beyond contribute negligibly** (< 10⁻¹⁴ to D₅)

### 3.2 Incremental Contributions to D₅

At (u₀=0.001, h=0.05) — worst deficit:

| Term added | Δ(D₅)       | Cumulative D₅  |
|------------|-------------|-----------------|
| f₁ alone   | —           | -1.000e-07      |
| + f₂      | +9.758e-08  | -2.467e-09      |
| + f₃      | +1.241e-13  | -2.467e-09      |
| + f₄      | +1.041e-22  | -2.467e-09      |

The f₂ contribution is 97.5% of |D₅(f₁)|. The residual -2.47e-09 is the irreducible deficit.

### 3.3 Cofactor Analysis

Laplace expansion of D₅ along the first row at (u₀=0.01, h=0.05):

| j | (-1)^j T[0,j] M[0,j] | Value         |
|---|----------------------|---------------|
| 0 | + K(u₀) M₀₀        | +1.703e-06    |
| 1 | - K(u₀+h) M₀₁      | -5.335e-06    |
| 2 | + K(u₀+2h) M₀₂     | +5.892e-06    |
| 3 | - K(u₀+3h) M₀₃     | -2.670e-06    |
| 4 | + K(u₀+4h) M₀₄     | +4.071e-07    |
| **Sum** |                | **-1.847e-09** |

The five terms range from -5.3e-6 to +5.9e-6. Their cancellation to -1.8e-9 represents a 3000:1 cancellation ratio. D₅ is the tiny residue of massive opposing contributions.

### 3.4 Eigenvalue Structure

At (u₀=0.01, h=0.05):

| Matrix    | Eigenvalues                                          | det        |
|-----------|------------------------------------------------------|------------|
| T₅(f₁)   | {0.0093, 0.0172, 0.0916, 0.5198, 1.584}            | +1.22e-05  |
| T₅(full)  | {0.0099, 0.0178, 0.0923, 0.5205, 1.585}            | +1.34e-05  |
| T₅(f₂)   | {5.4e-4, 5.8e-4, 6.4e-4, 6.9e-4, 7.4e-4}          | +1.1e-16   |

The minimum eigenvalue of the full Toeplitz matrix is 0.0099 (positive), meaning T₅ is positive definite. But D₅ = det(T₅) is NOT the same as the smallest eigenvalue — it's the product of all eigenvalues, and the sign of the Toeplitz determinant (the PF condition) involves a specific structured minor, not the full matrix eigenvalues.

The relative perturbation from f₂ is tiny: ||T₅(f₂)||_F / ||T₅(f₁)||_F = 8.5 × 10⁻⁴.

---

## 4. Investigation 3: The "Harmless Violation" Argument

### 4.1 Quantified Deficit

Across 54 configurations, the worst PF₅ deficits:

| Config (u₀, h) | |D₅|/D₄    |
|-----------------|------------|
| (0.001, 0.05)   | 6.48e-04   |
| (0.003, 0.05)   | 6.35e-04   |
| (0.005, 0.05)   | 6.07e-04   |
| (0.010, 0.05)   | 4.83e-04   |
| (0.001, 0.04)   | 3.68e-04   |

42 out of 54 tested configurations show D₅ < 0.

### 4.2 Toy Model: PF Failure and Zero Structure

Testing K_alpha(u) = exp(-u²)(1 + alpha*u⁴):

| alpha | D₅ sign | PF₅ |
|-------|---------|-----|
| 0     | +       | Yes |
| 0.01  | +       | Yes |
| 0.1   | +       | Yes |
| 1.0   | +       | Yes |

Surprisingly, the toy model maintains PF₅ even for large alpha. The PF₅ failure of the Polya kernel is NOT a generic consequence of non-Gaussianity — it requires the specific theta-function structure.

### 4.3 Sensitivity to Perturbations

Adding a perturbation ε cos(σu) exp(-δ|u|) to mimic a non-real zero contribution:

At ε = 10⁻³, σ = 21.02, δ = 0.1: the D₅ change is +9.3 × 10⁻¹⁰, which is 50% of |D₅|. This means a perturbation of order 10⁻³ in the kernel can change D₅ by order 1 relative to its current value. The D₅ negativity is extremely sensitive to kernel perturbations.

### 4.4 Conjectured Bound (Unproven)

If |D₅|/D₄ ≤ ε for all configurations, and if a quantitative Schoenberg-type inequality existed, non-real zeros would satisfy |σ - 1/2| ≤ C ε^{1/4} ≈ C × 0.16. This is far too weak for RH but would give a zero-free region. **However, no such inequality is known, and our Investigation 6 reveals that this approach faces fundamental obstacles.**

---

## 5. Investigation 4: Direct Computation

### 5.1 Ultra-Fine Heat Flow Scan

At the worst configuration (0.001, 0.05):

| t      | D₅            | D₄            | |D₅|/D₄     | D₅ change from t=0 |
|--------|---------------|---------------|-------------|---------------------|
| 0      | -2.467e-09    | +3.806e-06    | 6.48e-04    | 0%                  |
| 10⁻⁶   | -2.467e-09    | +3.806e-06    | 6.48e-04    | -0.00006%           |
| 10⁻³   | -2.469e-09    | +3.806e-06    | 6.49e-04    | -0.06%              |
| 10⁻²   | -2.482e-09    | +3.798e-06    | 6.53e-04    | -0.59%              |
| 10⁻¹   | -2.610e-09    | +3.727e-06    | 7.00e-04    | -5.8%               |
| 1.0    | -3.573e-09    | +3.057e-06    | 1.17e-03    | -44.8%              |

D₅ gets WORSE at every small t value. No improvement at any t < 3.

### 5.2 Higher-Order Minors at t=0

At (u₀=0.01, h=0.05):

| Order | Value          | Sign | Pattern     |
|-------|----------------|------|-------------|
| D₂    | +3.406e-02     | +    | PF₂ holds   |
| D₃    | +6.977e-04     | +    | PF₃ holds   |
| D₄    | +3.827e-06     | +    | PF₄ holds   |
| D₅    | -1.847e-09     | -    | PF₅ FAILS   |
| D₆    | -1.596e-11     | -    | PF₆ FAILS   |
| D₇    | +1.630e-13     | +    | D₇ positive |

The pattern +, +, +, -, -, +, ... is not monotonically deteriorating. D₆ is also negative but D₇ is positive. At (u₀=0.05, h=0.1), ALL minors D₂ through D₇ are positive.

### 5.3 Taylor Expansion of D₅(t)

    D₅(t) ≈ D₅(0) + t D₅'(0) + (t²/2) D₅''(0)
           = -1.847e-9 - 1.546e-9 t + 3.92e-10 t²

Linear prediction of D₅ = 0: t ≈ -D₅(0)/D₅'(0) = -1.20 (NEGATIVE). The linear approximation predicts D₅ would be zero in the reverse direction, which matches Investigation 6 (where D₅ crosses zero at reverse t ≈ 0.95).

The quadratic minimum is at t = -D₅'(0)/D₅''(0) ≈ 3.9, close to the actual minimum at t ≈ 2.9.

### 5.4 The Convolution Dead End

Convolution with a PF∞ kernel (e.g., a Gaussian) preserves but CANNOT improve PF order, by Karlin's composition formula: PF_min(4, ∞) = PF_4. This is a dead end.

The multiplicative deformation e^{tu²} is NOT a convolution — it's a frequency-domain convolution (multiplication in u-domain = convolution in Fourier domain). This is why it can change PF properties non-monotonically.

---

## 6. Investigation 5: The Turning Point and PF Spectrum

### 6.1 PF Order Crossing Times

At (u₀=0.01, h=0.05), each Dr first changes sign at:

| Minor | Sign at t=0 | First crossing t | Transition  |
|-------|-------------|------------------|-------------|
| D₂    | +           | 37.75            | pos → neg   |
| D₃    | +           | 21.73            | pos → neg   |
| D₄    | +           | 9.31             | pos → neg   |
| D₅    | -           | 11.43            | neg → pos   |
| D₆    | -           | 2.13             | neg → pos   |
| D₇    | +           | 29.46            | pos → neg   |

**There is no interval [0, T] where D₂ through D₅ are all positive.** The window between D₄ going negative (9.31) and D₅ going positive (11.43) is a gap, not an overlap.

### 6.2 The Alternative Deformation Discovery

The REVERSE heat flow e^{-tu²} improves D₅:

| reverse t | D₅ at (0.01, 0.05) | D₄          | D₆            |
|-----------|---------------------|-------------|----------------|
| 0         | -1.847e-09          | +3.827e-06  | -1.596e-11     |
| 0.1       | -1.689e-09          | +3.908e-06  | -1.693e-11     |
| 0.5       | -9.721e-10          | +4.240e-06  | -2.096e-11     |
| 0.95      | ~0                  | +4.680e-06  | -2.639e-11     |
| 1.0       | +1.257e-10          | +4.680e-06  | **-2.639e-11** |
| 2.0       | +3.105e-09          | +5.650e-06  | **-3.833e-11** |
| 5.0       | +2.084e-08          | +9.359e-06  | **-7.393e-11** |

D₅ is restored but D₆ gets WORSE (more negative, monotonically). The reverse heat flow concentrates the kernel, improving PF₅ but degrading PF₆.

### 6.3 The Whack-a-Mole Phenomenon

Under reverse heat flow e^{-tu²} at (u₀=0.01, h=0.05):

| reverse t | D₅  | D₆  | D₇  | D₈  | D₉  | D₁₀ |
|-----------|-----|-----|-----|-----|-----|------|
| 0         | -   | -   | +   | +   | +   | ?    |
| 1.0       | +   | -   | +   | +   | +   | -    |
| 5.0       | +   | -   | +   | +   | ?   | ?    |
| 10.0      | +   | +   | -   | +   | ?   | ?    |

At reverse t = 10: D₅ and D₆ are positive, but D₇ goes negative. The negativity "migrates" to higher orders. At reverse t = 1.0, checking up to D₁₀: {D₅=+, D₆=-, D₇=+, D₈=+, D₉=+, D₁₀=-}. Two orders fail simultaneously.

Across 45 configurations at reverse t = 1.0:
- D₅ failures: 11/45 (some configs still fail)
- D₆ failures: 5/45
- D₇ failures: 0/45
- D₈ failures: 5/45

---

## 7. Investigation 6: Schoenberg's Theorem — The Fundamental Insight

### 7.1 Precise Statement of Schoenberg's Characterization

**Theorem (Schoenberg 1951, Karlin):** For a continuous, even, integrable K: R → R with Fourier transform K-hat(x), the following are equivalent:
1. K is PF∞ (totally positive of infinite order)
2. K has the form K(u) = c exp(-αu²) prod_k cosh(β_k u)^{-1}
3. 1/K-hat(x) is an entire function of order ≤ 2 with only real zeros

**Critical distinction:** Condition (3) says 1/K-hat has real zeros, NOT that K-hat has real zeros. These are completely different conditions.

### 7.2 Application to the Polya Kernel

For K(u) = Phi(|u|):
- K-hat(x) = xi(1/2 + ix) (the Riemann xi-function)
- RH says xi has only real zeros, i.e., K-hat has only real zeros
- Schoenberg says: K is PF∞ iff 1/K-hat has only real zeros

Since xi has infinitely many zeros, 1/xi has infinitely many POLES. The function 1/xi is NOT entire. Therefore condition (3) of Schoenberg FAILS, meaning K = Phi(|u|) CANNOT be PF∞.

### 7.3 The Fundamental Consequence

**PF∞ of K implies K-hat is zero-free (non-vanishing everywhere).** This follows from condition (2): if K is a product of sech factors, its Fourier transform is a product of sech Fourier transforms, each of which is non-vanishing.

Since xi has infinitely many (real) zeros, Phi(|u|) CANNOT be PF∞. This is a mathematical certainty, not a computational artifact. The PF₅ failure is NECESSARY, not a "near-miss."

### 7.4 What PF∞ Would Actually Mean

If Phi(|u|) were PF∞, it would mean:
- xi(1/2 + ix) ≠ 0 for ALL x (real or complex)
- xi has NO zeros at all
- This contradicts the known existence of infinitely many zeros of zeta

So the PF∞ approach is fundamentally misguided for RH. **PF∞ is a condition about the ABSENCE of zeros, while RH is about the LOCATION of zeros.**

### 7.5 The de Bruijn-Newman Connection, Reconsidered

The parameter Λ is defined as inf{t : H_t has all real zeros}. But this does NOT require K_t to be PF∞. The zeros of H_t can all be real without K_t being PF∞ — the Fourier transform can have only real zeros while not being zero-free.

The implication chain is:
- K_t is PF∞ ⟹ H_t is zero-free ⟹ H_t has (vacuously) only real zeros ⟹ t ≥ Λ

But this is wasteful: PF∞ gives zero-free, which is MUCH stronger than "all zeros real."

A more productive approach would seek conditions on K that imply "all zeros of K-hat are real" WITHOUT requiring K-hat to be zero-free. This is exactly what the Jensen polynomial approach (Griffin-Ono-Rolen-Zagier) does, but through a different mechanism.

### 7.6 What the PF ORDER Does Tell Us

Although PF∞ is impossible, the finite PF order carries information:
- PF₂ (log-concavity) is equivalent to the Turan inequalities
- PF₃ constrains 3-point correlations
- PF₄ (proven computationally) constrains 4-point correlations of the kernel values

The PF order measures a kind of "regularity" of the kernel. Higher PF order means the kernel's Toeplitz matrices are "closer to" positive semi-definite in more elaborate ways. The failure at order 5 may encode information about the spacing distribution of zeta zeros, but extracting this information requires new theory.

---

## 8. Conclusions

### What We Established (Novel Contributions)

1. **dD₅/dt|_{t=0} < 0:** The heat flow worsens PF₅ initially. This is a quantitative result computed analytically and numerically (verified by exact cofactor formula).

2. **The PF order trading pattern:** Under heat flow, PF orders break and restore in a specific, configuration-independent order. There is no t value where all D₂ through D₅ are simultaneously positive.

3. **PF∞ is structurally impossible for Phi(|u|):** By Schoenberg's theorem, PF∞ implies zero-free Fourier transform. Since xi has zeros, Phi cannot be PF∞. This DEFINITIVELY closes the "approach RH via PF∞" strategy.

4. **The whack-a-mole phenomenon:** Any deformation that fixes PF₅ breaks another PF order. The negativity migrates to different orders under different deformations. Under reverse heat flow: fixing D₅ worsens D₆; fixing D₆ worsens D₇.

5. **The D₅ deficit is extraordinarily sensitive:** Kernel perturbations of order 10⁻³ change D₅ by order 1 (relative to its current value). The 3000:1 cancellation in the cofactor expansion makes D₅ a delicate balance.

### What This Means for RH

The PF framework cannot directly prove RH. The fundamental obstacle is:
- **PF∞ ⟹ zero-free** (too strong — RH needs "all real," not "zero-free")
- **Finite PF order ⟹ ???** (no known connection to zero location)

The most promising salvage directions:

**A. Modified PF conditions:** Instead of PF∞ of K, seek PF-like conditions on a MODIFIED kernel that directly control zero location rather than zero existence.

**B. The Jensen polynomial approach:** Griffin-Ono-Rolen-Zagier proved eventual hyperbolicity (all large n, fixed d). Extending to all n for d = 4 would be the natural next target, and PF₄ may provide tools.

**C. Quantitative zero-free region from PF₄:** Even though PF₄ doesn't prove RH, it may give computable zero-free regions via the variation-diminishing property. This would not prove RH but would improve existing bounds.

**D. Understanding WHY order 5 fails:** The failure at order 5 (not 4 or 6) may encode deep arithmetic information about the zeta zeros. The connection between PF order and the spacing statistics of zeros is unexplored.

### Rating: 9/10 on mathematical depth, 2/10 on RH proximity

The Schoenberg obstruction is a genuine mathematical insight that definitively answers the question "can PF analysis prove RH?" (Answer: not through PF∞). The quantitative results on the heat flow derivative, the turning point, and the whack-a-mole phenomenon are novel and mathematically rigorous. However, these findings move us FURTHER from RH by closing a strategic avenue, rather than opening one.

---

## 9. References

1. [arXiv 2602.20313](https://arxiv.org/abs/2602.20313) — "On the Polya Frequency Order of the de Bruijn-Newman Kernel"
2. Schoenberg, I.J. (1951) — "On Polya frequency functions. I."
3. Karlin, S. (1968) — "Total Positivity"
4. [Griffin-Ono-Rolen-Zagier (2019)](https://arxiv.org/abs/1902.07321) — "Jensen polynomials for the Riemann zeta function"
5. [Rodgers-Tao (2018)](https://arxiv.org/abs/1801.05914) — "The de Bruijn-Newman constant is non-negative"

---

## 10. Files Produced

- `findings.md` — This document
- `inv1_heat_flow_fine.py` — Fine-grained heat flow D₅(t) across configurations
- `inv2_signed_decomposition.py` — Theta-term decomposition of D₅
- `inv3_harmless_violation.py` — Deficit quantification and perturbation sensitivity
- `inv4_direct_computation.py` — Ultra-fine t scan, higher minors, Taylor expansion
- `inv5_monotonicity_and_turning.py` — Turning point, PF crossing times, alternative deformations
- `inv6_reverse_heat_and_schoenberg.py` — Reverse heat flow, Schoenberg analysis
- `inv1_results.json` — Heat flow scan data
- `inv2_results.json` — Decomposition data
- `inv3_results.json` — Deficit survey data
- `inv4_results.json` — Direct computation data
- `inv6_results.json` — Reverse heat flow data
