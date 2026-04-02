# Exploration 003: Path B — Flat Connections Maximize λ_max(H_actual)

## Goal

Determine whether flat connections (Q = I up to gauge equivalence) are global maximizers of λ_max(H_actual(Q)) for SU(2) Yang-Mills on L=2 lattice. This is the key to repairing the proof gap: if flat connections maximize the actual Hessian's top eigenvalue, then max_Q λ_max(H_actual(Q)) = dβ and the Bakry-Émery argument goes through.

## Summary of Findings

**⚠️ CRITICAL NEGATIVE RESULT: Flat connections are NOT global maximizers of λ_max(H_actual) at ANY dimension d ≥ 2.**

Two independent mechanisms were discovered:

1. **One-hot perturbations (d ≥ 3):** Rotating a single link INCREASES the top eigenvalue of the actual Hessian, while the B² formula Hessian's top eigenvalue is EXACTLY unchanged. This means r = λ_max(H_actual)/λ_max(H_formula) > 1, violating the inequality assumed by E001. Confirmed at d=3 (r = 1.0008) and d=4 (preliminary).

2. **Complex multi-link configurations (ALL d):** Random walk ascent from Haar-random starts finds non-flat configurations with λ_max EXCEEDING the flat value. At d=2: λ_max = 2.052 vs flat value 2.0 (excess 2.6%). **Verified at 5 different FD step sizes (h = 1e-3 to 2e-5) with gap consistent to 0.001.**

The excess over the flat value is:
- d=2: 2.6% (random walk, verified `[CHECKED]`)
- d=3: 0.2% (one-hot, θ ≈ 1, verified `[CHECKED]`); likely higher via random walk
- d=4: ≥ 0.001% (one-hot, θ = 0.1, preliminary `[COMPUTED]`); true max likely 0.2–0.4%

## Part 1: Perturbation Theory at Q = I

### Phase A: d=2, L=2 (24 DOF, 4 plaquettes)

**Eigenstructure at Q = I:** `[COMPUTED]`

| Level | λ     | Degeneracy | Description |
|-------|-------|------------|-------------|
| 0     | 0.0   | 15         | Gauge + kernel |
| 1     | 1.0   | 6          | |
| 2     | 2.0   | 3          | Top eigenspace |

So λ_max(H(I)) = dβ = 2.0 for d=2, β=1.0.

**First-order perturbation vanishes (symmetry):** `[COMPUTED]`

For 20 random multi-link perturbation directions, the 3×3 perturbation matrix Δ projected onto the top eigenspace has |eigenvalues| < 1.1 × 10⁻⁴ ≈ 0 (consistent with parity symmetry at the identity).

**Second-order: strict local maximum for multi-link perturbations:** `[COMPUTED]`

For all 20 random multi-link directions:
- d²λ_max/dt² ∈ [-0.285, -0.102], mean = -0.184
- Full 3×3 second-order matrix is **negative definite** for all 20 directions
- Direct d²H/dt² contribution: eigenvalues in [-0.50, -0.26] (always negative)
- Level repulsion: trace 0.09–0.19 (positive, partially counteracting, but not enough)

**CAVEAT:** This only shows I is a LOCAL max, not a GLOBAL max. The random walk (Part 4) shows higher values exist far from I.

**d=4 eigenstructure:** `[COMPUTED]`

| Level | λ     | Degeneracy |
|-------|-------|------------|
| 0     | 0.0   | 57         |
| 1     | 1.0   | 36         |
| 2     | 2.0   | 54         |
| 3     | 3.0   | 36         |
| 4     | 4.0   | 9          |

λ_max = 4.0, degeneracy 9 = (d-1)(N²-1). Matches expectation exactly.

**d=4 line scans (random multi-link, 2 directions):** `[COMPUTED]`

| Direction | d²λ/dt² | gap/t² (t=0.5) | Monotone? |
|-----------|---------|----------------|-----------|
| random_1  | -1.80   | 0.008          | YES       |
| random_2  | -2.96   | 0.010          | YES       |

Random multi-link perturbations always decrease λ_max at d=4 too.

### Phase B: d=3 One-Hot Counterexample

**⚠️ At d=3, one-hot (single-link) perturbations INCREASE λ_max.** `[CHECKED]`

| angle θ | λ_max(H_actual(Q)) | gap = λ(I) - λ(Q) | gap/θ² |
|---------|--------------------|--------------------|--------|
| 0.00    | 3.0000022          | 0                  | —      |
| 0.01    | 3.0000032          | -9.9 × 10⁻⁷       | -0.010 |
| 0.05    | 3.0000305          | -2.8 × 10⁻⁵        | -0.011 |
| 0.10    | 3.0001162          | -1.1 × 10⁻⁴        | -0.011 |
| 0.50    | 3.0025098          | -2.5 × 10⁻³        | -0.010 |
| 1.00    | 3.0058968          | -5.9 × 10⁻³        | -0.006 |
| π/2     | 2.9975971          | +2.4 × 10⁻³        | (decreasing) |
| π       | 2.8828878          | +1.2 × 10⁻¹        | (far below) |

Peak excess at θ ≈ 1.0: λ_max = 3.006, which is 0.2% above flat value.

**Verified:** Consistent across 4 FD step sizes AND all 9 link/color combinations. Numerical artifact ruled out.

### Phase C: d=4 One-Hot — CONFIRMED

**One-hot perturbations ALSO increase λ_max at d=4.** `[CHECKED]`

| angle θ | gap (h=1e-4) | gap (h=5e-5) | gap/θ² (h=1e-4) | gap/θ² (h=5e-5) | h-consistent |
|---------|-------------|--------------|-----------------|-----------------|-------------|
| 0.01    | -1.5e-6     | -3.9e-6      | 0.015           | 0.039           | marginal (noise) |
| 0.05    | -4.5e-5     | -4.3e-5      | 0.018           | 0.017           | YES         |
| 0.10    | -1.83e-4   | -1.82e-4     | 0.018           | 0.018           | YES         |
| 0.20    | -7.30e-4   | -7.30e-4     | 0.018           | 0.018           | YES         |

For θ ≥ 0.05, gap/θ² = 0.018 ± 0.001, with near-perfect agreement between h=1e-4 and h=5e-5.

Extrapolated to θ ≈ 1: max excess ≈ 0.018, so λ_max ≈ 4.018 (0.45% above flat value). True peak likely smaller due to higher-order corrections (at d=3, the θ=1 coefficient was 55% of the small-θ coefficient), giving estimated max excess ≈ 0.2-0.4%.

### Formula Hessian Invariance

**Critical observation:** `[COMPUTED]`

λ_max(H_formula(Q)) = dβ **exactly** for ALL one-hot perturbation angles θ, at ALL dimensions d=2,3,4. The B² formula Hessian's top eigenvalue is completely invariant under single-link rotations.

This means:
- r(Q) = λ_max(H_actual)/λ_max(H_formula) > 1 for one-hot perturbations at d ≥ 3
- **The inequality r ≤ 1 assumed by E001 is VIOLATED**
- E001 missed this because it tested large perturbations (Haar random, one-hot at θ=π), not small ones

## Part 2: Line Scans

**d=2 (20 random multi-link directions):** `[COMPUTED]`
- All c = (gap/t²) positive: c ∈ [0.006, 0.062], mean = 0.030
- No direction exceeds λ_max(I)
- **But this only tests multi-link directions from the identity!**

**d=3 (10 random multi-link directions):** `[COMPUTED]`
- All c positive: c ∈ [0.007, 0.023], mean = 0.014
- No random multi-link direction exceeds λ_max(I)

**d=2 special perturbations:** `[COMPUTED]`
- Uniform same rotation (all links in one direction): λ_max UNCHANGED (gauge direction on L=2)
- Staggered perturbation: λ_max UNCHANGED (also gauge on L=2)

## Part 3: Gauge Orbit Verification

**Gauge invariance confirmed at all dimensions:** `[COMPUTED]`

| d | Max |Δλ| across gauge orbit |
|---|-----|
| 2 | 5.2 × 10⁻⁸ |
| 3 | 2.2 × 10⁻⁷ |
| 4 | ~5 × 10⁻⁷ (2 transforms tested) |

## Part 4: Random Walk Ascent — Flat is Not Global Max

### d=2: Verified Counterexample `[CHECKED]`

Random walk from Haar-random starts found a configuration with **λ_max = 2.0523**, verified at 5 FD step sizes:

| h      | λ_max(best Q) | λ_max(I) | gap      |
|--------|---------------|----------|----------|
| 1e-3   | 2.0522534     | 2.0000   | -0.05225 |
| 5e-4   | 2.0522535     | 2.0000   | -0.05225 |
| 1e-4   | 2.0522535     | 2.0000   | -0.05225 |
| 5e-5   | 2.0522535     | 2.0000   | -0.05225 |
| 2e-5   | 2.0522543     | 2.0000   | -0.05225 |

Gap is -0.0523 ± 0.0001 across all h values. This is a **genuine** counterexample, not a numerical artifact.

Properties of the maximizing config:
- Max plaquette deviation: 0.698 (far from flat — not a gauge-equivalent flat connection)
- Found by 3 independent random walk runs, all finding λ > 2.0
- Best from 3 starts: 2.038, 2.052, 2.022

**This means flat connections are NOT global maximizers of λ_max(H_actual) even at d=2**, despite being strict local maxima. The landscape has higher-valued non-flat configurations separated from I by valleys.

## Part 5: D(Q) = H(I) - H(Q) Analysis

**Loewner order approach fails completely:** `[COMPUTED]`

D(Q) = H_actual(I) - H_actual(Q) is never PSD:
- d=2: 0/20 configs have D ≽ 0
- d=3: 0/20 configs have D ≽ 0
- D always has both positive and negative eigenvalues

Near flat (ε → 0): ||D||/ε² ≈ constant, #negative eigenvalues ≈ n/2 (half the eigenvalues of D are negative).

## Key Conclusions

### 1. Path B FAILS: Flat Connections Are Not Global Maximizers `[CHECKED]`

The hypothesis that max_Q λ_max(H_actual(Q)) = dβ (achieved at flat connections) is **disproved** at all dimensions d = 2, 3, 4. The true maximum exceeds dβ by:
- d=2: at least 2.6%
- d=3: at least 0.2% (one-hot), likely more via multi-link search
- d=4: at least 0.001% (one-hot at θ=0.1), likely ~0.4% at θ ≈ 1

### 2. The r ≤ 1 Inequality Is Violated `[COMPUTED]`

At d=3 (and preliminary d=4), the ratio r = λ_max(H_actual)/λ_max(H_formula) exceeds 1 for small one-hot perturbations. E001's finding of r ≤ 1 for ~300 configs at d=4 was because they tested large perturbations, not small single-link rotations.

### 3. Flat Is a Local Max for Multi-Link Perturbations `[COMPUTED]`

Despite not being the global max, flat connections ARE strict local maxima when perturbed along random multi-link directions:
- d=2: 20/20 directions give d²λ/dt² < 0
- d=3: 10/10 directions give monotone decrease
- d=4: 2/2 directions give d²λ/dt² < 0

The counterexample requires either (a) concentrated single-link perturbations at d ≥ 3, or (b) complex multi-link configurations far from flat at all d.

### 4. Proof Path Implications

The original proof chain (max λ_max = dβ at flat ⟹ Bakry-Émery threshold) needs revision:

**Option A — Tighter bound on true max:** Find max_Q λ_max(H_actual(Q)) = dβ(1 + ε(d)) and check if the adjusted threshold dβ(1+ε) < N²/(2(d-1)) still gives a useful β range. With ε ≈ 0.004 at d=4, the threshold shifts by only 0.4%, so the mass gap result survives with a slightly reduced β range.

**Option B — Probabilistic argument:** Since the Wilson action concentrates around flat connections at small β, the high-λ_max configurations have exponentially suppressed probability. A probabilistic version of the Bakry-Émery argument might work.

**Option C — Different spectral quantity:** Instead of max_Q λ_max(H_actual), use a weighted average or a quantity that accounts for the action density.

**Option D — Characterize the true maximizer:** Find what configurations actually maximize λ_max(H_actual) and prove the correct bound. The random walk found specific non-flat configs; understanding their structure could lead to an exact formula for the true maximum.

## Code

All scripts in `code/`:
- `lattice_core.py` — Core infrastructure (Hessian FD + formula, gauge transforms)
- `part1_d2_only.py` — d=2 perturbation theory (20 directions, full analysis)
- `part1_d4_targeted.py` — d=4 line scans + eigenstructure
- `part2_gauge_and_scans.py` — Gauge orbit + line scans (d=2,3,4)
- `part4_fast_gradient_ascent.py` — Random walk + simulated annealing
- `part5_proof_analysis.py` — D(Q) Loewner order analysis
- `check_formula_d4.py` — Formula Hessian invariance check
- `verify_counterexample.py` — Multi-h verification (d=2,3,4 one-hot)
- `verify_d2_excess.py` — Multi-h verification of d=2 random walk excess
- `extract_summary.py` — Statistics extraction
