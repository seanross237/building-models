---
topic: SED 3D ZPF two-point correlator — C_xx(d) = j₀(q) − (1/2)j₂(q)
confidence: verified
date: 2026-03-27
source: "stochastic-electrodynamics strategy-003 exploration-003"
---

## Key Result

The three-dimensional ZPF position-position correlator, averaged over all k-vector directions and polarizations (narrow-linewidth limit), is:

```
C_xx(d) = (3/2q³) [(q²−1)sin(q) + q cos(q)]    [q = ω₀d/c]
         = j₀(q) − (1/2) j₂(q)
```

where j₀(q) = sin(q)/q and j₂(q) = [(3−q²)sin(q) − 3q cos(q)]/q³ are spherical Bessel functions.

**[COMPUTED]** Verified to machine precision by three independent methods: direct analytic evaluation, numerical quadrature, and Bessel function form. Also confirmed by Monte Carlo (N=500,000 modes, ~0.05% agreement). See also `sed-coupled-oscillator-zpf-correlations.md` for the 1D result this generalizes.

## SED-QM Discrepancy Persists in 3D

**QM prediction** (uncoupled oscillators in product ground state): C_xx(d) = 0 for all d > 0.

**SED prediction** (3D ZPF): C_xx(d) ≠ 0 for any finite d.

**[CONJECTURED]** The 3D orientational average does NOT eliminate the SED-QM discrepancy. It modifies the shape relative to the 1D result:

| Regime | 1D model | 3D model |
|--------|----------|----------|
| d = 0 | 1 | 1 |
| Large d | cos(ω₀d/c) — constant amplitude | (3/2)sin(ω₀d/c)/(ω₀d/c) — decays as ~1/d |
| Never zero? | Never (full oscillation amplitude) | Never for finite d (damped but nonzero) |
| QM comparison | Large discrepancy at all d | Discrepancy shrinks with distance, never vanishes |

## Derivation

Two oscillators at r₁ = 0 and r₂ = dẑ driven by the x-component of the 3D ZPF. Each mode labeled by k-vector direction (θ,φ) and two polarizations perpendicular to k̂.

### Step 1: Polarization sum

For k̂ = (sin θ cos φ, sin θ sin φ, cos θ):
```
Σ_λ |ε̂^λ_x|² = 1 − k̂_x² = 1 − sin²θ cos²φ
```

### Step 2: Angular integral after φ integration

```
∫₀^{2π} (1 − sin²θ cos²φ) dφ = π(1 + cos²θ)
```

Setting u = cos θ, the key integral is:
```
I(q) ∝ π ∫₋₁^1 (1 + u²) e^{iqu} du
```

### Step 3: Analytic evaluation (integration by parts)

```
∫₋₁^1 e^{iqu} du = 2sin(q)/q

∫₋₁^1 u² e^{iqu} du = 2sin(q)/q + 4cos(q)/q² − 4sin(q)/q³
```

Final result:
```
I(q) = (4/q³)[(q²−1)sin(q) + q cos(q)]
```

**Verification at q=0:** Taylor expansion gives I(0) = 8/3; direct integration ∫₋₁^1(1+u²)du = 8/3. ✓

### Step 4: Normalize (narrow-linewidth limit)

|χ(ω)|² peaks sharply at ω ≈ ω₀, so:
```
C_xx(d) ≈ I(q) / I(0) = (3/2q³)[(q²−1)sin(q) + q cos(q)]
```

## Limiting Behaviors

### Near field (q → 0):

Taylor expanding I(q):
```
C_xx(d) = 1 − (ω₀d/c)²/5 + 3(ω₀d/c)⁴/280 + O(d⁶)
```
**[COMPUTED]** Verified: q=0.01 error 2.5×10⁻¹³, q=0.10 error 2.6×10⁻¹⁰, q=0.30 error 1.9×10⁻⁷. No near-field singularity; C_xx is analytic at d=0.

### Far field (q → ∞):

```
C_xx(q) = (3/2)[sin(q)/q + cos(q)/q² − sin(q)/q³]    [exact rewrite]
```
Leading term: C_xx ≈ (3/2)sin(q)/q ~ 1/d decay.

**[COMPUTED]** 1/q² corrections are significant even at q=10 (~13% error); approaches leading-term behavior for q ≥ 20. The (3/2)sin(q)/q approximation confirmed as asymptotically correct but not numerically dominant until large q.

### Special value at q = 1 (d = c/ω₀):

At q=1, the factor (q²−1) = 0, so the sin term vanishes:
```
C_xx(q=1) = (3/2) cos(1) ≈ 0.81045    [exact, machine-precision confirmed]
```

## Numerical Verification

All methods agree to machine precision (errors ≤ 7×10⁻¹⁷):

| q | Analytic | Numerical quadrature | Bessel form |
|---|----------|---------------------|-------------|
| 0.000 | 1.00000000 | 1.00000000 | 1.00000000 |
| 0.500 | 0.95066552 | 0.95066552 | 0.95066552 |
| 1.000 | 0.81045346 | 0.81045346 | 0.81045346 |
| 2.000 | 0.35542474 | 0.35542474 | 0.35542474 |
| π | −0.15198178 | −0.15198178 | −0.15198178 |
| 5.000 | −0.25915046 | −0.25915046 | −0.25915046 |
| 10.000 | −0.09337321 | −0.09337321 | −0.09337321 |

Monte Carlo (N=500,000 random k-vector directions, two polarizations each):
agreement at q=0.5 to q=5 within ~0.05% (consistent with 1/√N statistical error).

## Connection to Electrodynamics Green's Functions

The formula C_xx(d) = j₀(q) − (1/2)j₂(q) is the **xx-component of the transverse projection tensor** averaged over the sphere — the exact equal-time two-point ZPF electric field correlator in classical electrodynamics:
```
⟨E_i(r₁) E_j(r₂)⟩_{ZPF,T=0} ∝ [δᵢⱼ × f(r) + r̂ᵢr̂ⱼ × g(r)]
```
For oscillators separated along ẑ: r̂_x = 0, so the second term drops out and W_xx = C × f(r) = C × [j₀(q) − (1/2)j₂(q)].

This is the known result from classical electrodynamics, confirming internal consistency.

## Physical Interpretation of 1/d Decay

In 1D, all modes share the same propagation direction → perfectly constructive interference at resonance. In 3D, off-axis k-vectors contribute phase factors e^{i(ω/c)d cos θ}, which partially cancel under spherical integration. This introduces destructive interference that reduces amplitude by ~1/d for large d.

Note: the van der Waals/Casimir-Polder r⁻⁶ energy interaction is NOT present here — that arises from second-order Coulomb coupling between induced dipoles, a distinct mechanism.

## Observability

At d = c/ω₀ (one reduced wavelength, q=1): C_xx ≈ 0.81. The discrepancy between SED (~0.81) and QM (0) is large in principle but requires:
1. Narrow linewidth oscillators (γ/ω₀ ≪ 1)
2. Measuring position correlations between two spatially separated oscillators at the quantum level
3. No coupling between the oscillators (to maintain the product-state QM comparison)

## Adversarial Status (s003-E004)

**Verdict: VERIFIED (standard result) — Novelty: 2/5**

The formula C_xx = j₀(q) − (1/2)j₂(q) is the xx-component of the transverse photon propagator at equal times — a result that appears in classical and quantum field theory textbooks (Mandel & Wolf; Cohen-Tannoudji). Boyer (1975) contains the ZPF spectral and correlator functions from which this follows. Claiming the formula itself as novel would be embarrassing to a domain expert.

The genuine contribution is the **discrepancy framing**: explicitly identifying C_xx^{SED}(d) ≠ 0 vs. C_xx^{QM}(d) = 0 as a directly observable SED-QM discriminant that has not been highlighted in the literature as a testable prediction. The four-way numerical verification (quadrature + Bessel + Monte Carlo × 2) is solid but demonstrates well-known physics.

Strongest surviving objection: In full QED, vacuum fluctuations mediate Casimir-like correlations at finite separation — the QM "zero" cited is for truly uncoupled oscillators with no photon exchange, which is the correct comparison but must be stated carefully.
