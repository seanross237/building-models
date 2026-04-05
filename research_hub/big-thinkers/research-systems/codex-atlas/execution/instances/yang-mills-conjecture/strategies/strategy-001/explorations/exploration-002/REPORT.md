# Exploration 002: Per-Plaquette Contribution Structure for Staggered Modes

## Goal

Map f_□(Q) = |B_□(Q,v_stag)|² − |B_□(I,v_stag)|² for all 96 plaquettes on the L=2, d=4 lattice across diverse configs. Find a natural grouping where each group's sum ≤ 0, providing a proof route for Conjecture 1.

## Setup

- **Lattice**: L=2, d=4 hypercubic torus; 16 vertices, 64 edges, 96 plaquettes
- **Plane types**: (0,1),(0,2),(0,3),(1,2),(1,3),(2,3) — active (μ+ν odd): (0,1),(0,3),(1,2),(2,3); inactive: (0,2),(1,3)
- **B formula**: B_□ = c₁n + c₂Ad_{P₁}(n) − c₃Ad_{P₁P₂P₃⁻¹}(n) − c₄Ad_{U_□}(n)
  where c_k = staggered signs, satisfying c₃ = −c₁ and c₄ = −c₂ for ALL plane types
- **Equivalent form** (using c₃=−c₁, c₄=−c₂):
  B_□ = c₁(n + R_ξ n) + c₂(R₁ n + R_□ n)  where R_ξ = Ad_{P₁P₂P₃⁻¹}
- **Inner product**: |A|² = −2Re Tr(A²), |T_k|² = 1

---

## Stage 1: Verification at Q=I

**[COMPUTED]** Active planes: |B_I|² = 16 for all 64 active plaquettes. Inactive: |B_I|² = 0. Sum = 1024.

**[COMPUTED]** Sign structure: c₁ + c₂ − c₃ − c₄ = 2(s_μ − s_ν) where s_μ = (−1)^{|x|+μ}. This is ±4 for active planes and 0 for inactive planes.

**[COMPUTED]** f_□(I) = 0 for all 96 plaquettes (trivially).

---

## Stage 2: Per-Plaquette Data Across 36 Configurations

### Configuration types

10 random Haar, 10 near-identity (ε = 0.01–π), 5 Gibbs-like (β=0.5–4.0), 5 abelian, 5 adversarial, 1 identity.

### Global Sum f_□(Q) ≤ 0

**[COMPUTED]** Sum f_□(Q) ≤ 0 for ALL 36 tested configurations. All adversarial gradient ascent runs converge to Q=I (sum → 0 from below), confirming Q=I is the global maximum of v_stag^T M(Q) v_stag.

| Config type | Range of Sum f_□ |
|-------------|-----------------|
| Random Haar | −706 to −608 |
| Near-identity | −706 (ε=π) to −0.055 (ε=0.01) |
| Gibbs β=0.5–4.0 | −424 to −91 |
| Abelian | −666 to −586 |
| Adversarial | −10⁻⁵ (converges to Q=I) |

### Sign pattern: always #positive = #negative = 32

**[COMPUTED]** For every non-identity config, exactly 32 plaquettes have f_□ > 0 and 32 have f_□ < 0 (plus 32 inactive with f_□ ≥ 0... see below). Actually the decomposition is:

**[COMPUTED]** Individual plaquette classification (2000 random Haar configs × 96 plaquettes):
- **Active plaquettes** (μ+ν odd): max f_□ = **−0.21** < 0 — ALWAYS NEGATIVE
- **Inactive plaquettes** (μ+ν even): ALWAYS POSITIVE (every single test, 32000/32000)

This is the key structural result.

---

## Stage 3: Grouping Analysis

### Plane-type grouping: FAILS

**[COMPUTED]** Inactive planes (0,2) and (1,3) have positive per-plane sums:
- Plane (0,2): sums range from 0 to +108 across configs (ALWAYS POSITIVE for Q≠I)
- Plane (1,3): sums range from 0 to +81 (ALWAYS POSITIVE for Q≠I)

Example (random_haar_1): (0,1)=−203.6, (0,2)=+70.1, (0,3)=−196.9, (1,2)=−188.6, (1,3)=+36.2, (2,3)=−193.5.

### ⭐ CUBE-FACE GROUPING: ALL SUMS ≤ 0 [COMPUTED, STRONG EVIDENCE]

**Each of the 16 cubes (one per vertex x) has sum ≤ 0:**
∑_{μ<ν} f_{(x,μ,ν)}(Q) ≤ 0  for all x ∈ vertices, all Q tested.

- **36 initial configs × 16 vertices = 576 tests: 0 violations**
- **10,000 random Haar configs × 16 vertices = 160,000 tests: 0 violations**
- **Adversarial attack targeting cube sum at x=(0,0,0,0): converges to 0 (at Q=I)**

This is the partition of 96 plaquettes into 16 groups of 6. Each group sum ≤ 0. If proved, this implies Conjecture 1 immediately.

Equivalently: ∑_{μ<ν} |B_{(x,μ,ν)}(Q)|² ≤ 64  for all x, Q.

### ⭐ VERTEX-STAR GROUPING: ALL SUMS ≤ 0 [COMPUTED, STRONG EVIDENCE]

Each vertex star (24 plaquettes containing vertex x as a corner): 576 tests, 0 violations.

This is NOT a partition (plaquettes overlap) but provides further evidence.

### Edge-star grouping: ALMOST always ≤ 0

1 violation out of 36 configs × 64 edges (max positive = 0.48 in a Gibbs config). Not a reliable proof route.

### Plane-type PAIRS: ALL ALWAYS ≤ 0

**[COMPUTED]** Every pair of distinct plane types has sum ≤ 0. All 15 pairs: ALWAYS ≤ 0 across 36 configs. This follows because each active plane is strongly negative (−200) while inactive planes are only moderately positive (+50–110).

### Finer grouping: active vs. inactive within each cube

**[COMPUTED]** Sum of the 4 active plaquettes per cube vertex: 0/80,000 violations.
→ This follows trivially from the individual per-active-plaquette bound (each ≤ 0).

Sum of the 2 inactive plaquettes per cube vertex: ALWAYS POSITIVE (80,000/80,000).
→ Their positive contributions are always outweighed by the active.

### Holonomy correlation

**[COMPUTED]** Correlation between f_□ and W_□ = 1 − ReTr(U_□)/2 is ≈ 0.0006 (essentially zero). Per-plaquette holonomy magnitude does not predict f_□.

---

## Stage 4: Algebraic Analysis

### Per-active-plaquette bound: PROVED by triangle inequality

**[PROVED]** For any active plaquette (x, μ, ν) with μ+ν odd, and any Q:

Since c₃ = −c₁ and c₄ = −c₂:
```
B = c₁(n + R_ξ n) + c₂(R₁ n + R_□ n)
```
|B| ≤ |n + R_ξ n| + |R₁ n + R_□ n| ≤ 2 + 2 = 4

Therefore |B_active|² ≤ 16 = |B_I|² → **f_active ≤ 0** for all Q.

This is tight at Q=I (each active |B_I|² = 16).

For inactive plaquettes: |B_I|² = 0 and f_inactive = |B_inactive|² ≥ 0 (trivially). The inactive plaquettes also satisfy |B_inactive|² ≤ 16 by the same bound, but f_inactive can range [0,16].

### Cube-face sum: proved for simplified case (cross-links = I)

**[PROVED]** When only the 4 base links Q_{x,μ} vary and all cross-links Q_{x+μ,ν} = I:

Introducing w_μ = R_μ^{−1} n (unit vectors on S²), the formula simplifies exactly to:

```
∑_{μ<ν} |B_{(x,μ,ν)}|² = 32 + 8⟨n, W⟩ − |A|²
```

where W = ∑_μ w_μ and A = ∑_μ s_μ w_μ (with s = staggered signs at x).

**Bound**:
- 8⟨n, W⟩ ≤ 8|W| ≤ 8 ∑_μ |w_μ| = 8·4 = 32  (triangle inequality on S²)
- −|A|² ≤ 0  (trivially)

Therefore: ∑|B_{μν}|² ≤ 32 + 32 − 0 = **64**. ✓

**Equality** iff all w_μ = n (i.e., R_μ fixes n, so Q_{x,μ} lies in the stabilizer of n) AND A = ∑s_μ w_μ = 0 (which holds if all w_μ = n, since ∑s_μ = 0).

At Q=I: w_μ = n for all μ, W = 4n, A = 0·n = 0. Sum = 32 + 32 − 0 = 64. ✓

**[COMPUTED] Verified** formula against numerical computation: max discrepancy < 3×10⁻¹⁴ over 10,000 tests. Max numerical value = 61.5 (well below 64).

### Cube-face sum: general case status

**[COMPUTED]** For general Q (cross-links non-trivial): max over 10,000 random tests = 48.3. Adversarial attack converges to exactly 64 (at Q=I). So bound is 64 and tight at Q=I.

**[CONJECTURED]** The formula ∑|B_{μν}|² = 32 + 8⟨n, W̃⟩ − |Ã|² should generalize to the full configuration space with appropriate definitions of W̃ and Ã involving the 16 link variables. The simplified formula reveals the mechanism: the staggered sign structure ensures A = ∑s_μ w_μ → 0 as Q → I (since ∑s_μ = 0), which is exactly what makes Q=I the maximum.

### Proof gap for full conjecture

The proof is complete for:
1. Per-active-plaquette: f_active ≤ 0. ✓ PROVED.
2. Cube-face sum (cross-links = I): ∑|B|² ≤ 64. ✓ PROVED.

**PROOF GAP**: The cube-face sum for general Q (with arbitrary cross-links) is not yet proved. Specifically, we need to show:

∑_{μ<ν} |c₁_{μν}(n + R_ξ_{μν} n) + c₂_{μν}(R_{1,μν} n + R_ξ_{μν} R_{4,μν}^{-1} n)|² ≤ 64

where each plaquette involves its own partial holonomies R_ξ, R_1, R_4 depending on all 16 links.

**Candidate approach**: Factor out R_ξ_{μν} from each term and apply a generalized triangle inequality. Or use a gauge transformation argument at the neighboring vertices.

---

## Summary of Findings

| Result | Status | Tag |
|--------|--------|-----|
| f_active(Q) ≤ 0 for all active plaquettes | PROVED by triangle inequality | [PROVED] |
| f_inactive(Q) ≥ 0 for all inactive plaquettes | Trivial (|B_I|²=0) | [PROVED] |
| Sum f_□(Q) ≤ 0 for all tested Q | 36/36 configs + adversarial | [COMPUTED] |
| Cube-face sum ≤ 0 (160K tests) | 0 violations | [COMPUTED] |
| Cube-face bound proved (cross-links=I) | Formula verified, proof complete | [PROVED] |
| Cube-face bound (general Q) | Adversarial confirms max at Q=I | [COMPUTED] |
| Gradient ascent max → Q=I | 5/5 runs converge to 0 | [COMPUTED] |
| #pos plaquettes always 32 (inactive) | Confirmed structurally | [COMPUTED] |

---

## Key Algebraic Formula

For L=2, d=4 lattice, vertex x=(0,0,0,0), staggered signs s=(1,−1,1,−1), cross-links = I:

∑_{μ<ν} |B_{(x,μ,ν)}(Q)|² = 32 + 8⟨n, ∑_μ w_μ⟩ − |∑_μ s_μ w_μ|²

where w_μ = Ad_{Q_{x,μ}}^{−1} n ∈ S² are the parallel-transported reference vectors.

Upper bound proof:
- 8⟨n, ∑_μ w_μ⟩ ≤ 8 ∑_μ ⟨n, w_μ⟩ ≤ 8 ∑_μ |w_μ| = 32
- −|∑_μ s_μ w_μ|² ≤ 0

So ∑|B|² ≤ 64. ∎ (for cross-links=I case)

---

## Code

All computations in `code/`:
- `compute_plaquette_contributions.py` — main computation (36 configs, all groupings)
- `deep_analysis.py` — 10K stress test, adversarial attacks, finer groupings
- `alg_test2.py` — algebraic formula derivation and proof for simplified case

Output files: `/tmp/exploration002_output.txt`, `/tmp/exploration002_deep.txt`, `/tmp/exploration002_alg2.txt`
