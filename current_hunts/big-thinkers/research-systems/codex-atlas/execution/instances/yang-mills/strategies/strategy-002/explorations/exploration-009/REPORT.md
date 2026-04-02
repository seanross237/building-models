# Exploration 009: Full Hessian Eigenvalue Computation at Q=I

## Goal
Verify that the staggered mode is the GLOBAL maximum eigenvector of the Wilson action Hessian at Q=I for SU(2) on a 2⁴ lattice. Find λ_max and check if it equals 4β.

## Setup
- L=2, d=4: 16 sites, 64 links, 3 generators/link → 192×192 Hessian
- SU(2) generators: τ_a = iσ_a/2 (antihermitian), Tr(τ_a τ_b) = −δ_{ab}/2
- Wilson action (SZZ convention): S = −(β/2) Σ_{plaquettes} Re Tr(U_□) [factor 1/N for SU(N), N=2]
- Code: `code/full_hessian.py`, `code/verify_hessian.py`, `code/eigenvalue_check.py`, `code/d5_test.py`

---

## Part 1: Hessian Structure at Q=I

### Formula Derivation

At Q=I, the Wilson action Hessian decouples into generator components. For links li, lj and generators a, b:

H[(li,a),(lj,b)] = δ_{ab} × K[li, lj]

where K[li, lj] = Σ_{plaquettes P containing both li and lj} (β/4) × sign_{li,P} × sign_{lj,P}

The sign convention: forward links (U) have sign +1, backward links (U†) have sign −1.

For each plaquette, four links appear: two forward (+1,+1) and two backward (−1,−1).

**Key structural properties:**
- Each link appears in 2(d−1) = 6 plaquettes (d=4)
- K diagonal = 6 × (β/4) = 3β/2
- H = K ⊗ I_3 (block diagonal, same structure for all 3 generators)

### Hessian Verification

Compared analytical Hessian vs. numerical finite differences (h=10⁻⁴):

| Metric | Value |
|--------|-------|
| Wilson action at Q=I | −192.0 (= −β × 96 plaquettes × Tr(I)=2) |
| Max |H_num − H_analytical| | 2.38×10⁻⁶ |
| Analytically ≈ numerically | True (tol=10⁻⁶) |

**[VERIFIED]** The analytical Hessian formula is correct.

---

## Part 2: Maximum Eigenvalue

### Convention Note

Two conventions appear in the literature:

| Convention | Action | Hessian scale | λ_max |
|-----------|--------|---------------|-------|
| S1 (raw) | S = −β Σ Re Tr(U_□) | K_entry = (β/2)s_is_j | 8β |
| S2 (SZZ) | S = −(β/2) Σ Re Tr(U_□) [SU(2), N=2] | K_entry = (β/4)s_is_j | 4β |

The SZZ convention uses S = −(β/N) Σ Re Tr, standard for SU(N) lattice gauge theories. For SU(2), N=2, introducing a factor of 1/2.

**[COMPUTED]** Under SZZ convention (S2):

| Quantity | Value |
|---------|-------|
| λ_max | **4β** |
| λ_max / β | 4.000000 |
| λ_max / (48β) = H_norm | **0.083333 = 1/12** ✓ |
| SZZ upper bound | 48β (H_norm_bound = 1) |
| Ratio tight/bound | 1/12 ✓ |

### Full Eigenvalue Spectrum (S2 convention, K matrix, 64×64)

| Eigenvalue | Multiplicity (K) | Multiplicity (H=K⊗I₃) |
|-----------|-----------------|----------------------|
| 0 | 19 | 57 |
| β/2 | - | - |
| β | - | - |
| 2β | 12 | 36 |
| 4β | 18 | 54 |
| 6β | 12 | 36 |
| **8β → 4β (S2)** | **3** | **9** |

Wait — correcting: under S2 convention (divide all by 2):

| K eigenvalue (S2) | Multiplicity | H eigenvalue |
|------------------|--------------|-------------|
| 0 | 19 | 57 |
| 1β | 12 | 36 |
| 2β | 18 | 54 |
| 3β | 12 | 36 |
| **4β** | **3** | **9** |

**[COMPUTED]** The maximum eigenvalue is 4β with multiplicity 9 (= 3 spatial modes × 3 generators). The eigenvalue spectrum is all non-negative: the Hessian is positive semi-definite at Q=I.

---

## Part 3: Staggered Mode Verification

### Definition
Staggered vector (64-dim, link space): w_{x,μ} = (−1)^{|x|+μ} / ‖w‖

where |x| = x₀+x₁+…+x_{d−1} (sum of coordinates, d=4).

Full 192-dim DOF vector: v^a_{x,μ} = δ_{a,0} × w_{x,μ} (one generator component).

### Results

**[COMPUTED]**

| Check | Result |
|-------|--------|
| Rayleigh quotient (S2 conv) | **4β** exactly |
| Eigenvector residual ‖Kw − λw‖ | **0.00e+00** (exact) |
| H_norm = λ/(48β) | **0.083333 = 1/12** ✓ |
| Is staggered in max eigenspace? | Yes (projection = 1.000000) |

The staggered mode for each of the 3 generators independently gives Rayleigh quotient 4β. The maximum eigenspace has dimension 9 (3 spatial modes × 3 generators). The staggered mode for generator a=0 lies entirely within this max eigenspace.

**Conclusion:** The staggered mode IS an eigenvector of the Hessian with eigenvalue 4β = λ_max. It is one element of the 9-dimensional maximum eigenspace. This confirms H_norm_max = 1/12 exactly for d=4, SU(2), L=2.

---

## Part 4: Random Q Eigenvalue Test

Tested 5 random configurations from the uniform SU(2)⁶⁴ product measure (seed=42). Hessian computed via finite differences.

| Trial | λ_max(Q) | λ_min(Q) | Exceeds λ_max(I)=4β? |
|-------|---------|---------|---------------------|
| 1 | 2.0265β | −2.0021β | No |
| 2 | 2.1391β | −1.9955β | No |
| 3 | 2.0021β | −1.9489β | No |
| 4 | 2.0304β | −2.2090β | No |
| 5 | 2.0434β | −1.9312β | No |

**[COMPUTED]** No random Q exceeds λ_max(I) = 4β. All 5 random configurations have λ_max ≈ 2β. Notably, for random Q the Hessian has negative eigenvalues (not positive semi-definite), unlike at Q=I.

**Observation:** Q=I appears to be the worst case for λ_max. Random configurations give roughly half the maximum eigenvalue. This supports the conjecture that Q=I maximizes the operator norm.

---

## Part 5: d=5 Test (Bonus)

**L=2, d=5:** 32 sites, 160 links, 3 generators → 480×480 matrix.

### Expected (from E007)
H_norm_max = 3/40 = 0.075 (staggered mode result).

### Actual Results

Under SZZ convention (S = −(β/2) Σ Re Tr):

| Quantity | Value |
|---------|-------|
| λ_max (full Hessian) | **5β** |
| H_norm = λ_max / (8×4×2×β) | **5/64 ≈ 0.07813** |
| E007 prediction (3/40) | 0.075 |
| Staggered mode Rayleigh quotient | 4.8β |
| Staggered mode H_norm | 4.8/64 = 3/40 = 0.075 ✓ |
| Staggered mode is eigenvector? | **No** (residual = 0.98) |

**[COMPUTED — IMPORTANT FINDING]** For d=5, the staggered mode is NOT an eigenvector and NOT the global maximum. The true λ_max = 5β > 4.8β (staggered). The E007 claim that H_norm = 3/40 described the staggered mode's Rayleigh quotient, but a larger eigenvector exists with H_norm = 5/64 ≈ 0.0781.

### d=5 Eigenvalue Spectrum (K matrix)

| Eigenvalue | Multiplicity (K) | Multiplicity (H) |
|-----------|-----------------|------------------|
| 0 | 36 | 108 |
| 1β | 20 | 60 |
| 2β | 40 | 120 |
| 3β | 40 | 120 |
| 4β | 20 | 60 |
| **5β** | **4** | **12** |

The maximum eigenvalue for d=5 is 5β, with multiplicity 12 in H (4 spatial × 3 generators).

---

## Summary of Results

| Claim | Status | Notes |
|-------|--------|-------|
| λ_max(Q=I, d=4, SU(2)) = 4β | **[VERIFIED]** | Under SZZ convention |
| H_norm = 1/12 for d=4 | **[VERIFIED]** | 4β/48β = 1/12 exactly |
| Staggered mode is eigenvector | **[VERIFIED]** | Zero residual |
| Staggered mode achieves λ_max | **[VERIFIED]** | Lies in max eigenspace |
| Random Q < 4β | **[COMPUTED]** | All 5 trials below 4β |
| d=5: H_norm = 3/40 (staggered) | **[VERIFIED]** | Matches E007 |
| d=5: Staggered is global max | **[COMPUTED FALSIFIED]** | True λ_max = 5β > 4.8β |
| Q=I is worst-case config | **[CONJECTURED]** | Only 5 random samples |

---

## Convention Note for Strategizer

The factor-of-2 between conventions:
- **S1** (no 1/N): S = −β Σ Re Tr → λ_max = 8β → H_norm = 1/6
- **S2** (SZZ standard): S = −(β/N) Σ Re Tr → λ_max = 4β → H_norm = 1/12

All claims about H_norm = 1/12 require the SZZ convention (S2). The Hessian formula must include the 1/N = 1/2 factor for SU(2). This should be flagged when comparing results from different papers.
