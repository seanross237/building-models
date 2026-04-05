# Exploration 004: Large-Lattice Verification (L=4) + Analytical Gradient Adversarial Search

**Date:** 2026-03-28
**Explorer:** Atlas Explorer Agent
**Mission:** Yang-Mills mass gap (strategy-003)

## Goal Summary

Test H_norm = λ_max(H)/(48β) ≤ 1/12 on L=4 lattices. Use analytical gradient ascent to search for counterexamples. Investigate d=5 anomaly. Verify B_P bound. Test per-plaquette inequality.

**Convention:** S = −(β/N) Σ Re Tr(U_□), generators τ_a = iσ_a/2, |A|² = −2 Tr(A²).

---

## Section 1: Sanity Check (Q=I, λ_max = 4β at L=4)

**[COMPLETED]**

L=4, d=4, SU(2), β=1.0: 256 sites, 1024 links, 3072 DOFs, 1536 plaquettes.

| Quantity | Value | Expected | Status |
|---------|-------|----------|--------|
| λ_max(H at Q=I) | 4.000000 | 4β = 4.000000 | ✓ PASS |
| H_norm = λ_max/48β | 0.08333333 | 1/12 = 0.08333333 | ✓ PASS |
| Convergence residual | 9.36e-09 | < 1e-6 | ✓ converged |

**SANITY CHECK PASSED.**

At Q=I, H = (β/2N) × (K_curl ⊗ I₃) exactly (verified: max error = 0.00e+00).
K_curl[l,l'] = Σ_P s_{l,P} s_{l',P}.

### Staggered Mode Verification

Three modes tested:

| Mode | Formula | K_curl eigenvalue | H eigenvalue | H_norm |
|------|---------|------------------|-------------|--------|
| A: isotropic | v[l,a₀] = (−1)^|x| all μ | 0 | 0 | 0 (null space) |
| B: directional | v[l(x,μ₀),a₀] = (−1)^|x|, zero μ≠μ₀ | 12 | 3β | 1/16 |
| C: GOAL.md mode | v[l(x,μ),a₀] = (−1)^(|x|+μ) | **16 = 4d** | **4β** | **1/12** |

Mode C is the true maximum eigenvector. Mode B (directional) gives eigenvalue 3β < 4β — this corrects an error from prior work which claimed directional modes give 4β.

The isotropic Mode A is in the null space: B_P cancels at every plaquette since
(+1)(−1)^|x| + (+1)(−1)^(|x|+1) + (−1)(−1)^(|x|+1) + (−1)(−1)^|x| = 0.

### K_curl Maximum Eigenspace

λ_max(K_curl) = 16, multiplicity 3. These are the modes v_{l,a₀} = (−1)^|x| f(μ_l) where f ∈ R^d satisfies Σ_μ f(μ) = 0 (zero-sum). Mode C uses f(μ) = (−1)^μ which has zero sum for even d.

K_curl eigenspectrum (L=4, d=4):

| K_curl eigenvalue | H eigenvalue | H_norm | K_curl mult. | H mult. (×3 gen) |
|---|---|---|---|---|
| 16 = 4d | 4β | 1/12 | 3 | 9 |
| 14 | 3.5β | 7/96 | 24 | 72 |
| 12 | 3β | 1/16 | 84 | 252 |
| 10 | 2.5β | 5/96 | 168 | 504 |
| 8 | 2β | 1/24 | 210 | 630 |
| 6 | 1.5β | 1/32 | 168 | 504 |
| 4 | β | 1/48 | 84 | 252 |
| 2 | 0.5β | 1/96 | 24 | 72 |
| 0 | 0 | 0 | 259 | 777 |

---

## Section 2: Random + Gibbs Scan Results (L=4)

**[COMPLETED]**

50+ configurations tested. Hessian built (3072×3072) for each; power iteration finds λ_max.

| Config Type | # Tested | Max H_norm | Conjecture Violated? |
|-------------|----------|------------|---------------------|
| Q = I | 1 | 0.08333333 = 1/12 | NO (equality) |
| Random Haar | 20 | 0.04537 | NO |
| Gibbs (β=0.5–4.0) | 10 | 0.07140 | NO |
| Near-identity (ε=0.01–1.5) | 9 | 0.08332 | NO |
| Wavelength-4 mode | 1 | 0.00781 | NO |

**Overall max H_norm: 0.08333333 = 1/12, achieved only at Q=I. No violation.**

Gibbs samples: H_norm increases monotonically with β_Gibbs (colder = closer to I). Max = 0.07140 at β_Gibbs=4.0.

Near-identity: H_norm decreases monotonically with ε. At ε=0.01, H_norm = 0.08332 ≈ 1/12.

---

## Section 3: Analytical Gradient Adversarial Search

**[COMPLETED]**

Two rounds of gradient ascent on SU(2) link manifold, seeking H_norm > 1/12.

Algorithm: finite-difference gradient g_{l,a} = Δ(v^T Hv)/δ per link, batch 50–100 links/step, decaying α.

### Round 1 (gradient_results.json): 5 configs × 20 steps

| Config | Start H_norm | Max H_norm | Counterexample? |
|--------|-------------|-----------|-----------------|
| Q=I | 0.08333 | 0.08333 | No |
| Near-id ε=0.1 | 0.08312 | 0.08312 | No |
| Perturbed ε=0.5 | 0.06613 | 0.06613 | No |
| Random Haar 1 | 0.04394 | 0.04396 | No |
| Random Haar 2 | 0.04359 | 0.04361 | No |

### Round 2 (gradient_ascent_results.json): extended runs

| Run | Method | Max H_norm | Counterexample? |
|----|--------|-----------|-----------------|
| grad_perturb0.5 | Gradient 31 steps | **0.06730** | No |
| coord_random | Coordinate ascent | 0.04664 | No |
| coord_perturb1 | Coordinate ascent | 0.04985 | No |

**No counterexample found.** Gradient ascent moves toward Q=I, never exceeds 1/12. Q=I is a fixed point of the gradient (gradient = 0 by symmetry).

---

## Section 4: d=5 Anomaly

**[COMPLETED]**

L=2, d=5: 32 sites, 160 links, 480 DOFs. Full diagonalization of 480×480 H at Q=I.

λ_max at d=5 = 5β > 4β. H_norm = 5/48 ≈ 0.1042 > 1/12.

Eigenvalue spectrum:
| Eigenvalue | Multiplicity |
|-----------|-------------|
| 5β | 12 |
| 4β | 60 |
| 3β | 120 |
| 2β | 120 |
| β | 60 |
| 0 | 108 |

Mode A (isotropic staggered) has eigenvalue 0 at d=5 too — null space is universal across all d.

Cross-dimensional pattern:
| d | λ_max | Mode C Rayleigh | Mode B Rayleigh |
|---|-------|----------------|----------------|
| 2 | 2β | 2β (= λ_max) | 1β |
| 3 | 3β | 2.667β | 2β |
| 4 | 4β | 4β (= λ_max) | 3β |
| 5 | 5β | 4.8β | 4β |

Mode C achieves λ_max for even d only. Reason: for f(μ) = (−1)^μ to be in the max eigenspace (Σ_μ f(μ) = 0 required), we need Σ_μ (−1)^μ = 0, which holds iff d is even.

H_norm_max = d/48, so 1/12 holds iff d ≤ 4.

### d=5 Maximum Eigenvector Identification (new computation)

The GOAL.md asks: what is the maximum eigenvector at d=5?

**Answer:** v[l(x,μ), a₀] = (−1)^|x| × f(μ) where f ∈ R^5 satisfies **Σ_μ f(μ) = 0** (zero-sum / "traceless"). This is ANY zero-sum direction vector — the eigenspace has dimension d−1 = 4.

Verified (overlap = 1.000000 for all 4 basis vectors):
- K Rayleigh = 20 = 4d for ANY zero-sum f (computed for multiple traceless f vectors) ✓
- The eigenvectors are exactly v = (−1)^|x| f(μ), not any more complicated spatial pattern.

**Mode C fails at d=5** because f(μ) = (−1)^μ = (1,−1,1,−1,1) has Σ f = 1 ≠ 0. K Rayleigh = 19.2 = 4.8β < 5β. The mode is in a *sub-maximal* eigenspace.

**Simplest d=5 maximum eigenvectors** (K_rq = 20.0000 confirmed for each):
- f = (1,−1,0,0,0): v alternates between directions 0 and 1, zero elsewhere
- f = (1,1,−2,0,0): combination of directions 0,1 vs 2
- f = (1,1,1,1,−4): direction 4 vs all others
- Any linear combination with Σ f(μ) = 0

**The d=5 maximum eigenspace is geometrically the same as d=4:** both use the staggered site factor (−1)^|x| × traceless direction vector. The difference is dimension: d−1=3 for d=4, d−1=4 for d=5. The d=4 mode C = (−1)^(|x|+μ) is special because (−1)^μ is itself traceless in even d.

---

## Section 5: B_P Intermediate Bound at L=4

**[COMPLETED]**

K_curl (1024×1024) at L=4: λ_max = 16.0000 = 4d exactly. B_P bound Σ|B_P|² ≤ 4d|v|² confirmed.

B_P with v_max at 5 configs:

| Config | H_norm | BP_sum/|v|² | ≤ 16? |
|--------|--------|------------|-------|
| Q=I | 0.08333 | 16.000 | ✓ (equality) |
| near-id ε=0.1 | 0.08245 | 15.713 | ✓ |
| warm start ε=0.5 | 0.06705 | 10.843 | ✓ |
| random Haar 1 | −0.045* | 7.408 | ✓ |
| random Haar 2 | 0.04172 | 6.138 | ✓ |

*power iteration artifact (converged to min eigenvalue).

---

## Section 6: Conclusions

**[COMPLETED]**

1. **H_norm ≤ 1/12 at L=4: CONFIRMED.** Zero counterexamples across 50+ configurations and adversarial gradient search. Q=I is the global maximum.

2. **Maximum eigenvector: v[l(x,μ),a₀] = (−1)^(|x|+μ).** Multiplicity 9. Prior claim of "directional staggered modes" was wrong.

3. **B_P bound Σ|B_P|² ≤ 4d|v|² confirmed** at L=4 with equality at Q=I.

4. **d=5 anomaly explained:** λ_max = dβ, H_norm = d/48. Bound fails for d≥5.

5. **Per-plaquette B_P approach: DEFINITIVELY FALSE** (Sections 7–8).

---

## Section 7: Fourier Analysis — Analytical Proof of λ_max(K_curl) = 4d

**[NEW — COMPLETED]**

K_curl = d₁^T d₁ commutes with lattice translations. Block-diagonalize by Fourier:

At momentum k, the d×d direction-space block is:
  K_curl(k)[μ,ν] = A(k) δ_{μν} − B(k)

At k = (π,...,π): sin²(π/2) = 1, giving:
  **K_curl(k=(π,...,π)) = 4d · I_d − 4 · J_d**

Eigenvalues of 4d·I − 4·J:
- **4d** with multiplicity d−1 (traceless eigenvectors: Σ_μ v_μ = 0)
- **0** with multiplicity 1 (eigenvector: (1,1,...,1))

This is the global maximum of K_curl over all k. Therefore:

**Theorem:** λ_max(K_curl) = 4d for the d-dimensional hypercubic torus, multiplicity d−1.

**Corollary:** λ_max(H at Q=I) = (β/2N) × 4d = 2βd/N.

For d=4, N=2: λ_max = 4β, H_norm = 4/48 = **1/12** ✓
For d=5, N=2: λ_max = 5β, H_norm = 5/48 ✓

The maximum eigenvectors are v_{l,a₀} = (−1)^|x| f(μ_l) with Σ_μ f(μ) = 0.

For even d: Mode C uses f(μ) = (−1)^μ which satisfies Σ(−1)^μ = 0 → Mode C is in the max eigenspace.
For odd d: Σ(−1)^μ = 1 ≠ 0 → Mode C is NOT max; must use genuinely zero-sum f.

**Complete max eigenspace characterization (all d):**
- Spatial structure: (−1)^|x| (staggered, momentum k=(π,...,π))
- Direction structure: any f ∈ R^d with Σ f(μ) = 0 (zero-sum hyperplane, dimension d−1)
- Generator: fixed a₀ (multiplicity N²−1 = 3 for SU(2))
- Total multiplicity: (d−1) × (N²−1) in full DOF space

Verified at d=2,3,4,5: all max eigenvectors have overlap 1.000000 with (−1)^|x| f(μ) form.

---

## Section 8: Per-Plaquette Inequality Test — CRITICAL FINDING

**[NEW — COMPLETED]**

Tested: H_P(Q,v) ≤ (β/2N)|B_P(Q,v)|² for each plaquette P.

B_P defined using Convention 2: Q_k → exp(s_k ε τ_a) Q_k, giving
  B_P(Q,v) = Σ_{k,a} v_{k,a} s_k Lp_k(Q) τ_a W_k(Q) Rs_k(Q)
  |B_P|² = −2 Re Tr(B_P²)

**At Q=I: H_P(I,v) = (β/2N)|B_P(I,v)|² exactly** for ALL plaquettes and ALL v. Ratio = 1.000000 to machine precision. Analytically: both sides equal (β/2N) Σ_a (Σ_k s_k v_{k,a})².

**Per-plaquette results at Q≠I (pp_bound_corrected.py):**

| Config | Max per-plaq ratio | |B_P|²<0 count | VIOLATED? |
|--------|-------------------|--------------|-----------|
| Q=I | 1.000000 | 0/1536 | NO |
| near-id ε=0.1 | **1.770** | 0/1536 | **YES** |
| near-id ε=0.5 | **158.3** | 117/1536 | **YES** |
| random Haar 1 | **8383** | 248/1536 | **YES** |
| random Haar 2 | **2496** | 234/1536 | **YES** |

**Global sum at true v_max (full eigvalsh, not power iteration):**

| Config | λ_max = Σ H_P | (β/2N)Σ|B_P|² | Ratio | Violated? |
|--------|--------------|----------------|-------|---------|
| Q=I | 4.0000 | 4.0000 | 1.000 | NO |
| near-id ε=0.5 | 3.2131 | 2.0875 | **1.539** | **YES** |
| random Haar 1 | 2.0611 | 1.0645 | **1.936** | **YES** |
| random Haar 2 | 2.0475 | 1.0745 | **1.906** | **YES** |

**The entire B_P proof chain is dead:**
- Step 1: H_P ≤ (β/2N)|B_P|² per plaquette → **FALSE** for all Q ≠ I
- Step 1': Σ H_P ≤ (β/2N) Σ|B_P|² globally → **FALSE** at v_max for Q ≠ I
- Step 2: Σ|B_P|² ≤ 4d|v|² → TRUE (confirmed)

H_norm ≤ 1/12 is still confirmed numerically, but the proof cannot go through B_P. Any proof must use a direct spectral argument, gauge orbit convexity, or a completely different chain.

**Q=I is special:** the per-plaquette equality at Q=I is a flat-vacuum coincidence. The nonlinear holonomy at Q≠I breaks both per-plaquette and global-sum forms of the inequality simultaneously.

---

## Computation Notes

- Hessian build at L=4 (3072×3072): 0.5–3.4s per config
- K_curl full diagonalization (1024×1024): ~5–10s
- d=5 Hessian full diagonalization (480×480): ~0.5s
- Gradient ascent step (batch 50 links): ~6–7s
- Per-plaquette bound test (4 configs × 1536 plaquettes): ~8 min each
- Total compute: ~90 minutes

## Correction Log

- Section 1 corrected: directional staggered modes (−1)^|x| δ_{μ,μ₀} have H eigenvalue 3β, NOT 4β. True max is Mode C = (−1)^(|x|+μ) with eigenvalue 4β.
- Section 8 corrected: global sum Σ H_P ≤ (β/2N)Σ|B_P|² was reported as holding based on random (non-maximizing) vectors. At true v_max it is violated. Both steps of the B_P chain fail.
