---
topic: Rigorous Fourier proof of H_norm ≤ 1/12 at Q=I for SU(N) Wilson action (d=4)
confidence: verified
date: 2026-03-27
source: "yang-mills strategy-002 exploration-008; strategy-003 explorations 001, 004; SZZ arXiv:2204.12737; CNS arXiv:2509.04688"
---

## Overview

Rigorous proof via Fourier analysis that the normalized Hessian of the Wilson action achieves H_norm = 1/12 at the identity configuration Q=I for SU(2) in d=4, with a tight upper bound. This is a **12× improvement** over SZZ's Lemma 4.1 bound (H_norm ≤ 1) at Q=I, and 6× better than the CNS vertex bound (β < 1/24). Extension to all Q remains an open conjecture supported by strong numerical evidence (see `hnorm-conjecture-numerical-resolution.md`).

## Key Results

### Lemma A (Proved, Q=I)

On the d-dimensional hypercubic lattice (Z/LZ)^d with SU(N) Wilson action S = −(β/N) Σ_□ Re Tr(U_□), at Q=I:

```
HessS(v,v)|_{Q=I} ≤ (2dβ/N)|v|²
```

with equality in d=4, N=2 for the staggered mode v_{x,μ} = (−1)^{|x|+μ} v₀.

The tight normalized bound is:

```
H_norm_max(Q=I) = d / (4(d−1)N²)
```

**[CORRECTED by yang-mills-validation E006]** Prior formula ⌈d/2⌉⌊d/2⌋/(N²d(d−1)) was only correct for even d; see `d5-anomaly-eigenstructure.md`.

| d | N=2 H_norm | Decimal |
|---|-----------|---------|
| 3 | 3/(4×2×4) = **3/32** | **0.09375** |
| 4 | 4/(4×3×4) = **1/12** | **0.0833** |
| 5 | 5/(4×4×4) = **5/64** | **0.078125** |

**[VERIFIED]** at d=4 by eigenvalue computation (E009): λ_max = 4β, H_norm = 4β/48β = 1/12 exactly. **[PROVED ANALYTICALLY, S003-E004]**: Fourier block-diagonalization of K_curl at momentum k gives d×d block K(k)[μ,ν] = A(k)δ_{μν} − B(k); at k=(π,...,π): K = 4d·I_d − 4·J_d, eigenvalues 4d (mult. d−1) and 0 (mult. 1). This is the global maximum over all k → λ_max(K_curl) = 4d exactly, for ANY d and ANY lattice size L.

### GOAL.md Formula Correction

The formula "H_norm = 4/(3d)" in GOAL.md is **incorrect**. The correct formula is H_norm(I) = d/(4(d−1)N²). **[CORRECTED by yang-mills-validation E006]** The prior intermediate formula ⌈d/2⌉⌊d/2⌋/(N²d(d−1)) was only correct for even d. The universally correct formula d/(4(d−1)N²) gives 1/12 for d=4 N=2, 3/32 for d=3 N=2, and 5/64 for d=5 N=2. See `d5-anomaly-eigenstructure.md` for full derivation.

## Proof Method: Fourier Analysis of the Discrete Curl

### Step 1: Hessian as Squared Discrete Curl

At Q=I, the Hessian decomposes into a sum of per-plaquette terms:

```
HessS(v,v)|_{Q=I} = (β/(2N)) Σ_{x,μ<ν} |ω_{x,μν}(v)|²
```

where ω_{x,μν}(v) = v_{x,μ} + v_{x+ê_μ,ν} − v_{x+ê_ν,μ} − v_{x,ν} is the **discrete curl** of the tangent field.

### Step 2: Fourier Decomposition

In Fourier space with c_μ = 1 − e^{ik_μ}:

```
ω̂_{k,μν} = c_ν v̂_{k,μ} − c_μ v̂_{k,ν}
```

Using the exterior product identity |a∧b|² = |a|²|b|² − |a·b|²:

```
Σ_{μ<ν} |c_ν v̂_μ − c_μ v̂_ν|² = |c_k|²|v̂_k|² − |c̄_k · v̂_k|² ≤ |c_k|²|v̂_k|²
```

where |c_k|² = Σ_μ 4sin²(k_μ/2) ≤ 4d.

### Step 3: Upper Bound

Summing over k:
```
HessS(v,v)|_{Q=I} ≤ (β/(2N)) × 4d × |v|² = (2dβ/N)|v|²
```

Therefore H_norm ≤ d/(4N²(d−1)) = **1/12** for d=4, N=2.

### Step 4: Tightness (d=4)

Equality holds when: (a) |c_k|² = 4d (requires k* = (π,π,...,π)), and (b) c_k ⊥ v̂_k (transversality). The staggered mode satisfies both in d=4 because N_active = d²/4 = 4. The bound is tight in d=4 but NOT tight in d=3 (N_active = 2 ≠ 9/4).

## Staggered Mode Analysis

The staggered mode v^{stag}_{x,μ} = (−1)^{|x|+μ} v₀ produces:
- **Active planes** (μ+ν odd): per-plaquette contribution = (8β/N)|v₀|²
- **Inactive planes** (μ+ν even): zero contribution

For d=4: 4 active plane types out of 6, explaining the factor N_active/total = 4/6 = 2/3 relative to the maximum possible.

## Extension to All Q: Gap and Partial Bounds

### Per-Plaquette Operator Inequality (Lemma 5.1)

For any B ∈ su(N) and U ∈ SU(N): −(1/N)Re Tr(B²U) ≤ (1/(2N))|B|², with equality iff U = I. **[PROVED]**

This shows for FIXED transported tangents, the plaquette phase U_□ = I is worst case. But as Q varies, the transported tangents B_□ also change — the bound is not directly applicable to general Q.

### Rigorous Global Triangle Inequality Bound

Using Lemma 5.1 + triangle inequality |B_□| ≤ Σ|Ã_k| ≤ 4 max|v_e|:

```
HessS(v,v; Q) ≤ (β/(2N)) × 4 × 2(d−1) × |v|² = 4(d−1)β|v|²/N
```

For N=2, d=4: ≤ 6β|v|², giving **H_norm ≤ 1/8** for ALL Q. **[CONJECTURED — proof incomplete]**

**[CORRECTED by yang-mills-validation E007]** The proof via Lemma 5.1 bounds only the B² term of the Hessian. The full Hessian at general Q also contains commutator cross terms not bounded by Lemma 5.1. The actual Hessian exceeds (β/2N)Σ|B_□|² by 1.5–2× at generic Q (see `adversarial-review-proof-chain.md` and `hessian-analytical-formula-c-decomposition.md`). The inequality H_norm ≤ 1/8 is strongly supported numerically (0 violations in 300+ configs) but NOT rigorously proved.

### Open Conjecture A'

The bound H_norm ≤ 1/12 holds for ALL Q ∈ SU(N)^E. This requires:

```
Σ_□ |B_□(Q,v)|² ≤ 4d|v|²  for all Q, v
```

where B_□ is the sum of parallel-transported tangent vectors. Strongly supported by numerical evidence (100 configs at L=2, 50+ at L=4, 0 violations — see `hnorm-conjecture-numerical-resolution.md`). **Proved for uniform Q, flat connections, and single-link configs; Q=I proved as strict local maximum** — see `b-square-inequality-proof-progress.md` for full status. **Per-plaquette proof route ruled out** — see `per-plaquette-inequality-false.md`.

## Improved Bakry-Émery Threshold (Corollary B, under Conjecture A')

| System | H_norm bound | β threshold | Improvement over SZZ |
|--------|-------------|-------------|---------------------|
| SZZ Lemma 4.1 (H_norm ≤ 1) | 1 | 1/48 | 1× |
| Cauchy-Schwarz (H_norm ≤ 1/4) | 1/4 | 1/12 | 4× |
| Global triangle (H_norm ≤ 1/8) | 1/8 | 1/6 [CONJECTURED] | 8× SZZ [CONJECTURED] |
| **Lemma A (H_norm ≤ 1/12)** | **1/12** | **β < N²/(4d) = 1/4** | **12× SZZ [CONJECTURED]** |
| CNS vertex (H_norm ≤ 1/2 rel.) | — | 1/24 | 2× |

In standard lattice units (β_lattice = N²β_SZZ): SZZ gives β < 1/12, CNS gives β < 1/6, Lemma A gives **β < 1.0**. The SU(2) deconfinement transition is at β ≈ 2.3 — all bounds are in the confined phase, but Lemma A extends furthest.

## Literature Check

**Not found in literature:**
- The exact formula H_norm_max = d/(4(d−1)N²)
- The staggered mode as the Hessian maximizer
- The Fourier analysis approach to tighten the plaquette Hessian bound
- The improved threshold β < N²/(4d)

**Verdict: The result appears to be NEW.** Nearest precedent is the CNS 2× improvement (vertex reformulation); the Fourier approach is geometrically different and yields a further 6× improvement over CNS.
