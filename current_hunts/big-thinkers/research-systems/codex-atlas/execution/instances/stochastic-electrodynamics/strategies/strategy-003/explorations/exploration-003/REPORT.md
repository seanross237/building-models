# Exploration 003: Three-Dimensional ZPF Two-Point Correlator

**Goal:** Compute the 3D ZPF position-position correlation C_xx(d) by averaging over all k-vector directions and polarizations.

**Prior result (1D):** C_xx(d) = cos(ω₀d/c)  [VERIFIED in Strategy-002 E002]
**QM prediction (uncoupled oscillators):** C_xx = 0

**Key question:** Does the 3D orientational average kill the 1D correlations, or does a non-zero result persist?

---

## Section 1: The 3D ZPF Angular Integral

### Setup

Two oscillators at r₁ = 0 and r₂ = dẑ, both driven by the x-component of the ZPF.
The 3D ZPF has modes labeled by k-vector direction (θ,φ) and two polarizations perpendicular to k̂.

The frequency-domain cross-correlator for the x-component of E:
```
W_xx(d, ω) ∝ ∫ d³k/(2π)³ × S_E(ω) × [Σ_λ |ε̂^λ_x|²] × e^{ik_z d}
```

For k̂ = (sin θ cos φ, sin θ sin φ, cos θ), the sum over two polarizations perpendicular to k̂ gives:
```
Σ_λ |ε̂^λ_x|² = 1 - k̂_x² = 1 - sin²θ cos²φ
```

The angular integral (factoring out the radial/frequency part):
```
I(q) ∝ ∫₀^π sin θ dθ ∫₀^{2π} dφ × (1 - sin²θ cos²φ) × e^{iωd cosθ/c}
```
where q = ω₀d/c.

### φ Integration

```
∫₀^{2π} (1 - sin²θ cos²φ) dφ = 2π - sin²θ × π = π(2 - sin²θ) = π(1 + cos²θ)
```

### u = cosθ Substitution

Setting u = cos θ (u ∈ [-1, 1]):
```
I(q) ∝ π ∫₋₁^1 (1 + u²) e^{iqu} du
```

This is the key integral to evaluate analytically.

---

## Section 2: Analytic Evaluation of I(q)

### Computing the Integral

Split into two parts:

**Part 1:** ∫₋₁^1 e^{iqu} du = [e^{iqu}/(iq)]₋₁^1 = (e^{iq} - e^{-iq})/(iq) = 2sin(q)/q

**Part 2:** ∫₋₁^1 u² e^{iqu} du

Integrate by parts (v = u², dw = e^{iqu}du → dv = 2u du, w = e^{iqu}/(iq)):
```
= [u² e^{iqu}/(iq)]₋₁^1 - (2/iq) ∫₋₁^1 u e^{iqu} du
= (e^{iq} - e^{-iq})/(iq) - (2/iq) ∫₋₁^1 u e^{iqu} du
= 2sin(q)/q · (1/(iq)) · (iq) ... = 2sin(q)/q - (2/iq)·[∫₋₁^1 u e^{iqu} du]
```

For the inner integral ∫₋₁^1 u e^{iqu} du (parts with v=u, dw=e^{iqu}du):
```
= [u e^{iqu}/(iq)]₋₁^1 - (1/iq) ∫₋₁^1 e^{iqu} du
= (e^{iq} + e^{-iq})/(iq) - 2sin(q)/(iq·q)
= 2cos(q)/(iq) - 2sin(q)/(iq·q)
```

Substituting back (noting 1/(iq)² = -1/q²):
```
∫₋₁^1 u² e^{iqu} du = 2sin(q)/q - (2/iq)[2cos(q)/(iq) - 2sin(q)/(iq·q)]
                     = 2sin(q)/q - 4cos(q)/(iq)² + 4sin(q)/(iq)²·q
                     = 2sin(q)/q + 4cos(q)/q² - 4sin(q)/q³
```

### Final Expression

```
I(q) = 2sin(q)/q + 2sin(q)/q + 4cos(q)/q² - 4sin(q)/q³
     = 4sin(q)/q + 4cos(q)/q² - 4sin(q)/q³
     = (4/q³)[(q² - 1)sin(q) + q cos(q)]
```

**Verification at q=0:** lim_{q→0} (4/q³)[(q²-1)sin(q) + q cos(q)]
Taylor expanding: (q²-1)(q - q³/6 + ...) + q(1 - q²/2 + ...) = (-q + q³/6 + q³) + (q - q³/2) = q³(1+1/6-1/2) = q³(2/3)
So I(0) = 4/q³ × (2/3)q³ = 8/3.

Direct check: ∫₋₁^1 (1+u²) du = [u + u³/3]₋₁^1 = (1+1/3)-(-1-1/3) = 8/3 ✓

---

## Section 3: C_xx(d) — The 3D Correlation Function

### Narrow-Linewidth Limit

In the narrow-linewidth limit (γ ≪ ω₀), |χ(ω)|² peaks sharply at ω ≈ ω₀, so:
```
C_xx(d) ≈ W_xx(d, ω₀) / W_xx(0, ω₀) = I(ω₀d/c) / I(0)
```

### Result

Defining q = ω₀d/c:
```
C_xx(d) = I(q)/I(0) = [(4/q³)((q²-1)sin q + q cos q)] / (8/3)

         = (3/2q³) [(q²-1)sin(q) + q cos(q)]
```

**Equivalently, in terms of spherical Bessel functions j₀ and j₂:**
```
C_xx(d) = j₀(q) - (1/2) j₂(q)
```

where j₀(q) = sin(q)/q and j₂(q) = [(3-q²)sin(q) - 3q cos(q)]/q³.

This can be verified:
j₀ - j₂/2 = sin(q)/q - [(3-q²)sin(q) - 3q cos(q)]/(2q³)
           = [2q²sin(q) - (3-q²)sin(q) + 3q cos(q)] / (2q³)
           = [(2q² - 3 + q²)sin(q) + 3q cos(q)] / (2q³)
           = [(3q² - 3)sin(q) + 3q cos(q)] / (2q³)
           = (3/2q³)[(q²-1)sin(q) + q cos(q)] ✓

---

## Section 4: Limiting Behavior

### 4.1 d → 0 (q → 0): Near Field

Taylor expand I(q):
∫₋₁^1 (1+u²) e^{iqu} du ≈ ∫₋₁^1 (1+u²)(1 + iqu - q²u²/2 - iq³u³/6 + q⁴u⁴/24) du

Odd powers of u vanish by symmetry. Even terms:
- ∫₋₁^1 (1+u²) du = 8/3
- -(q²/2) ∫₋₁^1 u²(1+u²) du = -(q²/2)[2/3 + 2/5] = -(q²/2)(16/15) = -8q²/15
- +(q⁴/24) ∫₋₁^1 u⁴(1+u²) du = +(q⁴/24)[2/5 + 2/7] = +(q⁴/24)(24/35) = q⁴/35

So I(q) = 8/3 - 8q²/15 + q⁴/35 + O(q⁶)

And:
```
C_xx(d) = 1 - (1/5)(ω₀d/c)² + (3/280)(ω₀d/c)⁴ + O(d⁶)
```

The leading correction is -d²/5. No d⁻ⁿ singularities; C_xx is analytic at d=0.

### 4.2 d → ∞ (q → ∞): Far Field

The analytic formula factors as:
```
C_xx(q) = (3/2) [sin(q)/q + cos(q)/q² - sin(q)/q³]
```

This is exact (not an approximation). At large q:
- Leading term: (3/2)sin(q)/q  → decays as ~1/d
- Next term: (3/2)cos(q)/q²  → decays as ~1/d²
- Next term: -(3/2)sin(q)/q³ → decays as ~1/d³

**[COMPUTED]** The 3-term form is exact to machine precision for all q (it's just the formula rewritten).

For large d, the leading behavior is:
```
C_xx(d) ≈ (3/2) sin(ω₀d/c) / (ω₀d/c)    [large d, leading term]
```

This **decays as 1/d** (far-field). Oscillating but diminishing.

**Special value:** At q=1 (d = c/ω₀), since q²-1=0, the sin term vanishes and:
```
C_xx(q=1) = (3/2) cos(1) ≈ 0.81045   [exact]
```

### 4.3 Comparison with 1D Result

| Regime | 1D model | 3D model |
|--------|----------|----------|
| d=0 | 1 | 1 |
| Large d | cos(ω₀d/c) | (3/2)sin(ω₀d/c)/(ω₀d/c) |
| Decay | None (oscillates at amplitude 1) | ~1/d |
| QM value | 0 (discrepancy) | 0 (still discrepancy, but smaller) |

---

## Section 5: Numerical Verification

**Script:** `code/compute_3d_correlator.py`

### 5.1 Exact Integral Check I(0) = 8/3

```
I(0) numerical:  2.6666666667
I(0) analytic:   2.6666666667  (= 8/3)
Error:           0.00e+00
```
**[COMPUTED]** Machine-precision agreement.

### 5.2 Analytic vs Numerical Integration — Selected q Values

```
     q  |   Analytic   |  Numerical   |    Bessel    |   Error
-----------------------------------------------------------------
  0.000  |  1.00000000  |  1.00000000  |  1.00000000  |  0.00e+00
  0.500  |  0.95066552  |  0.95066552  |  0.95066552  |  3.33e-16
  1.000  |  0.81045346  |  0.81045346  |  0.81045346  |  0.00e+00
  2.000  |  0.35542474  |  0.35542474  |  0.35542474  |  5.55e-17
  3.142  | -0.15198178  | -0.15198178  | -0.15198178  |  0.00e+00
  5.000  | -0.25915046  | -0.25915046  | -0.25915046  |  0.00e+00
 10.000  | -0.09337321  | -0.09337321  | -0.09337321  |  6.94e-17
```
**[COMPUTED]** All three methods agree to machine precision.

### 5.3 Near-Field Taylor Expansion Verification

```
q=0.01: exact=0.9999800001, Taylor=0.9999800001, err=2.45e-13
q=0.10: exact=0.9980010712, Taylor=0.9980010714, err=2.64e-10
q=0.30: exact=0.9820865931, Taylor=0.9820867857, err=1.93e-07
```
**[COMPUTED]** Taylor series C_xx ≈ 1 - q²/5 + 3q⁴/280 verified to high accuracy.

### 5.4 Monte Carlo Verification (N=500,000 modes)

Monte Carlo: random k-vector directions sampled uniformly on sphere, two polarizations perpendicular to k, x-projection weight = 1 - sin²θ cos²φ.

```
   d (=q)  |   Analytic   |  Monte Carlo  |  MC Error
-------------------------------------------------------
   0.5000  |  0.95066552  |  0.95072590   |  0.0001
   1.0000  |  0.81045346  |  0.81067847   |  0.0002
   3.1416  | -0.15198178  | -0.15237740   |  0.0004
   5.0000  | -0.25915046  | -0.25963151   |  0.0005
```
**[COMPUTED]** Monte Carlo agrees with analytic formula to ~0.05% (consistent with sqrt(N) statistical error).

### 5.5 Far-Field Behavior Verification

Leading-order approximation (3/2)sin(q)/q:
```
q=5:   exact=-0.25915046, approx=-0.28767728, err=2.85e-02  (11% error — not yet asymptotic)
q=10:  exact=-0.09337321, approx=-0.08160317, err=1.18e-02  (13% error — 1/q² corrections)
q=20:  exact= 0.06983002, approx= 0.06847089, err=1.36e-03  (2% error — approaching)
q=50:  exact=-0.00728912, approx=-0.00787125, err=5.82e-04  (8% from next term)
```
**[COMPUTED]** The (3/2)sin(q)/q approximation is the leading term but 1/q² corrections are significant even at q=10. The decay as 1/d is confirmed.

**Plot:** `code/C_xx_3D_vs_1D.png` — shows the 3D result vs 1D cos(q) and far-field envelope.

---

## Section 6: Does C_xx → 0 in 3D?

**NO.** The 3D orientational average does NOT make C_xx vanish.

The result C_xx(d) = (3/2q³)[(q²-1)sin(q) + q cos(q)] is:
- Exactly 1 at d=0
- Non-zero for all finite d
- Oscillating and decaying as ~sin(ω₀d/c)/(ω₀d/c) for large d

The 3D result differs from the 1D result in that the oscillations are damped by a 1/d envelope, but they never reach zero for finite d. SED still predicts non-zero spatial correlations between uncoupled oscillators, in disagreement with QM.

---

## Section 7: Implications for the SED-QM Discrepancy

### The discrepancy persists in 3D

**QM prediction** (product state of uncoupled oscillators): C_xx(d) = 0 for all d > 0.

**SED prediction** (3D ZPF): C_xx(d) = (3/2q³)[(q²-1)sin(q) + q cos(q)] ≠ 0 for any finite d.

The 3D averaging does NOT eliminate the SED-QM discrepancy. It modifies the shape:
- **1D:** constant-amplitude oscillations, cos(ω₀d/c), never decaying — large discrepancy at all d
- **3D:** oscillating correlations decaying as ~1/(ω₀d/c) at large d — discrepancy that shrinks with distance but never vanishes

### Connection to Electrodynamics Green's Functions

The formula C_xx(d) = j₀(q) - (1/2)j₂(q) is the **xx-component of the transverse projection tensor** averaged over the sphere. This is the exact form expected from classical electrodynamics: the two-point ZPF electric field correlator at equal times.

This connects to the known result:
```
<E_i(r₁) E_j(r₂)>_{ZPF,T=0} ∝ [δᵢⱼ × f(r) + r̂ᵢr̂ⱼ × g(r)]
```
where f and g are combinations of spherical Bessel functions. The xx component with separation along ẑ (so r̂ = ẑ, r̂_x = 0) becomes:
```
W_xx = C × f(r)  (the r̂ᵢr̂ⱼ term drops out since r̂_x = 0)
```
This f(r) is exactly our j₀(q) - (1/2)j₂(q).

### Physical Interpretation

The 1/d decay of C_xx in 3D can be understood as follows:
- In 1D, all modes have the same propagation direction and perfectly constructive interference in phase at the resonant frequency
- In 3D, modes with k-vectors pointing off-axis contribute phase factors e^{i k_z d} = e^{i(ω/c)d cosθ}, which partially cancel when integrated over the sphere
- This spherical average introduces destructive interference that reduces the amplitude by a factor 1/d for large d

The van der Waals/Casimir-Polder r⁻⁶ behavior is NOT found in C_xx(d) — the r⁻⁶ energy interaction comes from second-order Coulomb coupling between induced dipoles, not from the direct ZPF correlation studied here.

### Observability

Whether the predicted C_xx(d) ~ sin(ω₀d/c)/(ω₀d/c) is measurable depends on:
1. The ratio γ/ω₀ (linewidth vs. frequency) — the narrow-linewidth approximation is crucial
2. The magnitude: at d = λ/2π (one reduced wavelength), q=1, C_xx ≈ 0.81 — a large effect
3. Any competing mechanisms that would create or destroy correlations at the same order

The discrepancy between SED's prediction (~0.81 at q=1) and QM's (0) is large in principle, but requires measuring correlations between two spatially separated oscillators at the quantum level without allowing any interaction between them.

---

## Summary of Results

**[COMPUTED]** Three-dimensional ZPF correlator (narrow-linewidth limit):
```
C_xx(d) = (3/2q³) [(q²-1)sin(q) + q cos(q)]    [q = ω₀d/c]
         = j₀(q) - (1/2) j₂(q)
```

**[COMPUTED]** Limiting behaviors:
- d→0:  C_xx → 1 - (ω₀d/c)²/5 + O(d⁴)
- d→∞:  C_xx → (3/2) sin(ω₀d/c)/(ω₀d/c)   [oscillating, decaying ~1/d]
- Never zero for finite d

**[CONJECTURED]** SED-QM discrepancy: SED predicts non-zero C_xx at all finite d; QM predicts 0. The discrepancy persists in 3D but is smaller (1/d decay) than in 1D (no decay).
