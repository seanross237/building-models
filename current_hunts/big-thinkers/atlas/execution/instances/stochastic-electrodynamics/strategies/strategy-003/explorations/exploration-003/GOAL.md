# Exploration 003 — Three-Dimensional ZPF Correlations

## Mission Context

You are working on Stochastic Electrodynamics (SED), a classical field theory that uses a real electromagnetic zero-point field (ZPF) with spectral density S_F(ω) = 2τħω³/m to reproduce quantum mechanics.

**Prior work (Strategy-002 E002)** showed that in a **1D plane-wave ZPF model**, two harmonic oscillators at separation d have position-position correlations:
```
C_xx(d) = cos(ω₀d/c)
```
This was analytically derived and numerically confirmed to < 0.2% accuracy.

**QM prediction for uncoupled oscillators** (no interaction, product state): C_xx = 0 everywhere.

So SED predicts non-zero oscillating correlations where QM predicts zero — this is a genuine SED-QM discrepancy.

**BUT**: The 1D calculation was done with all ZPF modes traveling along the same axis (a plane-wave model). In the real 3D world, ZPF has contributions from all directions and polarizations.

**The open question:** When you average over all ZPF k-vector directions in 3D, does:
- (A) C_xx(d) → 0 (QM recovered — the 1D result was an artifact of the 1D model)
- (B) C_xx(d) → r⁻⁶ van der Waals term (SED predicts a non-QM observable correlation)
- (C) C_xx(d) → something else (e.g., r⁻³ near-field, r⁻¹ or oscillating far-field)

**Your job:** Compute the 3D ZPF correlation C_xx(d) analytically (or numerically if analytic is intractable).

## Setup

### Two Oscillators

Consider two identical harmonic oscillators:
- Oscillator 1 at position **r₁ = 0** (origin)
- Oscillator 2 at position **r₂ = d ẑ** (along z-axis, separation d)
- Both oscillators respond to the x-component of the ZPF electric field (x-polarized)
- Natural frequency ω₀, damping rate γ = τω₀² ≪ ω₀
- No direct coupling between oscillators (this is NOT van der Waals — there's no interaction Hamiltonian)

### ZPF in 3D

The 3D ZPF is a superposition of all plane-wave modes labeled by wavevector **k** and polarization λ:
```
E(r, t) = Σ_{k,λ} A_k × ε̂_{k,λ} × Re[e^{i(k·r - ωt + φ_{k,λ})}]
```
where:
- ω = c|k| (dispersion relation)
- ε̂_{k,λ} are the two polarization unit vectors perpendicular to k
- φ_{k,λ} are independent random phases (uniform on [0, 2π])
- A_k² ∝ ω³ (ZPF spectral density, S_E(ω) ∝ ω³)

### Key Reference: Ibison & Haisch (1996)

Ibison, M. & Haisch, B. (1996). Phys. Rev. A 54, 2737.

This paper explicitly writes the 3D ZPF two-point electric field correlator. Find this paper (use web search). Their formula should look like:
```
⟨E_i(r₁,t) E_j(r₂,t)⟩ = C × δᵢⱼ × f(ω₀|r₁-r₂|/c)
                         + C' × (r̂ᵢr̂ⱼ − δᵢⱼ/3) × g(ω₀|r₁-r₂|/c)
```
for some functions f, g, where r̂ = (r₁-r₂)/|r₁-r₂|.

Also check:
- Boyer, T.H. (1975). "Random electrodynamics." Phys. Rev. D 11, 790.
- Boyer, T.H. (1980). "Thermal effects of acceleration through random classical radiation." Phys. Rev. D 21, 2137.
- de la Peña & Cetto (2014) textbook (if accessible)

## Analytic Approach

### Step 1: Write the ZPF Two-Point Correlator

The ZPF electric field correlator in 3D (frequency domain) is:
```
W_ij(r, ω) = ⟨Ê*_i(0,ω) Ê_j(r,ω)⟩
```

For x-polarized components (i=j=x), and separation d along ẑ:
```
W_xx(d, ω) = ∫ d³k/(2π)³ × S_E(ω) × |ε̂_x·ε̂_{k,λ}|² × e^{ik_z d}
```

The sum over polarizations: for a k-vector in direction k̂ = (sin θ cos φ, sin θ sin φ, cos θ), the two polarization vectors are perpendicular to k̂. The x-component of the polarization vectors averages over angles.

**Angular integration** for the x-component:
```
⟨|ε̂_x·ε̂_{k}|²⟩_{angle average} = (1 - k̂_x²/2) averaged over sphere...
```

Actually the correct formula for the sum of squared x-projections of polarization vectors for mode k is:
```
Σ_λ |ε̂^λ_x|² = 1 - k̂_x² = 1 - sin²θ cos²φ
```
(sum over 2 polarizations perpendicular to k)

Then the angular integral:
```
W_xx(d, ω) ∝ ∫₀^π sin θ dθ ∫₀^{2π} dφ × (1 - sin²θ cos²φ) × e^{iωd cos θ/c}
```

Integrate over φ first: ∫₀^{2π} (1 - sin²θ cos²φ) dφ = 2π(1 - sin²θ/2) = 2π(1 - (1-cos²θ)/2) = π(1 + cos²θ)

Then:
```
W_xx(d, ω) ∝ π ∫₀^π sin θ × (1 + cos²θ) × e^{iωd cos θ/c} dθ
```

Substitute u = cos θ, du = -sin θ dθ:
```
W_xx(d, ω) ∝ π ∫₋₁^1 (1 + u²) e^{iωdu/c} du
```

**This integral is analytic.** Compute it:
```
∫₋₁^1 e^{iωdu/c} du = 2 sin(ωd/c) / (ωd/c) = 2 sinc(ωd/c)

∫₋₁^1 u² e^{iωdu/c} du = ? (integrate by parts twice)
```

The result should be expressible in terms of sinc and its derivatives (or equivalently, spherical Bessel functions j₀ and j₂).

### Step 2: Compute C_xx(d) Using the Oscillator Response

Each oscillator responds as a driven harmonic oscillator:
```
x̃(ω) = χ(ω) × E_x(r, ω)
```
where χ(ω) = 1/(ω₀² - ω² + iγω) is the susceptibility.

The position-position correlation:
```
C_xx(d) = ⟨x₁(t)x₂(t)⟩ / ⟨x₁²⟩^{1/2} ⟨x₂²⟩^{1/2}
         = ∫ |χ(ω)|² W_xx(d,ω) S_F(ω) dω / ∫ |χ(ω)|² S_F(ω) dω
```

In the narrow-linewidth limit (γ ≪ ω₀), |χ(ω)|² peaks sharply at ω ≈ ω₀, so:
```
C_xx(d) ≈ W_xx(d, ω₀) / W_xx(0, ω₀)
```

where W_xx(d, ω₀) is the value of the 3D correlator at frequency ω₀.

### Step 3: Evaluate the Result

Compute W_xx(d, ω₀) / W_xx(0, ω₀) analytically. The integral from Step 1 gives:
```
I(q) = ∫₋₁^1 (1 + u²) e^{iqu} du   where q = ω₀d/c
```

At d=0 (q=0): I(0) = ∫₋₁^1 (1+u²) du = [u + u³/3]₋₁^1 = (1 + 1/3) - (-1 - 1/3) = 8/3

At d>0:
```
∫₋₁^1 e^{iqu} du = (2/q) sin(q)
∫₋₁^1 u² e^{iqu} du = -d²/dq² ∫₋₁^1 e^{iqu} du = -d²/dq² [(2/q) sin(q)]
```

Compute -d²/dq² [(2/q) sin(q)] explicitly.

The final result will be C_xx(d) = I(ω₀d/c) / I(0) — some function of ω₀d/c.

**Key question:** Is this function:
- Zero everywhere (C_xx → 0 in 3D)?
- ~(c/ω₀d)^n for large d (power-law, possibly r⁻⁶ van der Waals type)?
- Oscillating but decaying?
- Something else?

## Alternative Numerical Verification

If the analytic approach gets stuck, set up a numerical computation:
1. Generate N_modes random k-vectors uniformly distributed over a sphere
2. For each k-vector, assign 2 polarization vectors perpendicular to k
3. For each mode, compute the contribution to ⟨E_x(0,t) E_x(d_z,t)⟩
4. Sum contributions vs. d_z
5. Plot C_xx(d) / C_xx(0)

This will show the d-dependence even if the analytic form isn't derivable.

## Limiting Cases to Check

1. **d → 0**: C_xx(0) = 1 (autocorrelation = 1, trivially)
2. **1D limit** (only modes along ẑ): Should recover C_xx(d) = cos(ω₀d/c) ✓
3. **d → ∞**: Should decay to 0 (decorrelation at large separation) — what's the decay rate?
4. **Near field (ω₀d/c ≪ 1)**: Taylor expand in ω₀d/c. What's the leading correction?

## Near-Field Expansion (Important!)

For ω₀d/c ≪ 1 (near field, d ≪ λ = c/ω₀):

The van der Waals correlation in QM (via Casimir-Polder) goes as d⁻⁶ for the interaction energy. If C_xx(d) ≈ 1 - (ω₀d/c)² × (constant) for small d, then the correlation itself doesn't have the r⁻⁶ term. The van der Waals force in SED comes from a different mechanism (second-order Coulomb coupling), not from C_xx.

Check: is C_xx(d) analytic in d at d=0, or is there a non-analytic piece?

## What Faria-França May Have on This

Also check: does Faria & Franca have any computation of the 3D ZPF correlator? Or does de la Peña & Cetto?

## Success Criteria

**Minimum success (pass):**
- Found Ibison-Haisch (1996) or Boyer (1975) formula for the 3D ZPF correlator
- Set up the integral ∫₋₁^1 (1+u²) e^{iqu} du and evaluated it
- Stated C_xx(d) as a function of q = ω₀d/c (even if approximate)

**Good success (Tier 4):**
- Analytic expression for C_xx(d) in the narrow-linewidth limit
- Limiting behavior at d→0, d→∞, and ω₀d/c ~ 1
- Answer to: "Does C_xx → 0 in 3D or does it stay non-zero?"

**Excellent success:**
- Closed-form C_xx(d) with asymptotic expansions
- Clear comparison to the 1D result cos(ω₀d/c)
- Physical interpretation: does the 3D orientational average kill the oscillations?

## Key Prior Result (Verified Baseline)

**1D result (analytically derived + numerically confirmed):**
```
C_xx(d) = cos(ω₀d/c)     (1D plane-wave ZPF model)
```

Your 3D computation should recover this in the limit where all k-vectors are colinear (1D limit). Use this as a sanity check.

## Output Format

Write REPORT.md as you work (incremental writing encouraged — write each section as you complete it).

REPORT.md structure:
1. Formula from literature (Ibison-Haisch or Boyer) for the 3D ZPF correlator
2. Angular integration — derive W_xx(d, ω₀) analytically
3. C_xx(d) result — as a function of ω₀d/c
4. Limiting behavior — d→0, d→∞, near-field, far-field
5. Numerical verification (if needed)
6. Answer: does 3D orientational average give C_xx → 0 or non-zero?
7. Implications for the SED-QM discrepancy

Then write REPORT-SUMMARY.md (1 page max) with the key result.

## Your Exploration Directory

`/Users/seanross/kingdom_of_god/building_models/current_hunts/atlas/execution/instances/stochastic-electrodynamics/strategies/strategy-003/explorations/exploration-003/`

Save code to a `code/` subdirectory.
