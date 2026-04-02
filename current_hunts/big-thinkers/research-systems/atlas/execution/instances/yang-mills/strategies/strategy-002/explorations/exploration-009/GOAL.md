# Exploration 009: Full Hessian Eigenvalue Computation at Identity + General Q Bound

## Mission Context
This is a YANG-MILLS mission. Do not confuse with other missions.

## Background

From the adversarial review (Exploration 007), we found:
- The staggered mode v_{x,μ} = (-1)^{|x|+μ} v₀ at Q=I gives H_norm = 1/12 in d=4
- This formula was verified numerically for specific (L, β) values
- The claim is that H_norm = 1/12 is the MAXIMUM over ALL tangent vectors at Q=I

**Open question:** Is the staggered mode the GLOBAL maximum eigenvalue of the Hessian matrix at Q=I? Or could there be a different tangent vector that gives H_norm > 1/12?

**Secondary open question:** For configurations Q ≠ I, is max H_norm ≤ 1/12? We observed this numerically in E006, but need verification.

## Your Task

### Part 1: Full Hessian Eigenvalue Computation at Q=I (Priority 1)

Compute the FULL Hessian matrix of the Wilson action S at Q=I for SU(2) on a small lattice (L=2, d=4: 2⁴=16 sites, 64 links, 3 generators per link → matrix size 192×192).

1. **Build the Hessian matrix H[i,j] = ∂²S/∂v_i ∂v_j at Q=I** using the formula:
   For two link-tangent pairs (e, a) and (f, b) where a, b ∈ {1,2,3} (su(2) generators):
   H[(e,a),(f,b)] = ∂²S / (∂v_e^a ∂v_f^b) at Q=I

2. **Find the maximum eigenvalue** using numpy.linalg.eigvalsh (or power iteration)

3. **Compare to the SZZ bound**: max eigenvalue should ≤ 48β × |v|²... wait, that's for the normalized version. Actually:
   - The Hessian as a bilinear form: H(v,v) ≤ λ_max × |v|²
   - The SZZ claim: H(v,v) ≤ 8(d-1)Nβ × |v|² → λ_max ≤ 48β
   - The tight claim: H(v,v) ≤ (1/12) × 48β × |v|² → λ_max ≤ 4β

4. **Report**: λ_max / (48β) = H_norm_true_max. Is this exactly 1/12?

### Part 2: Verify Staggered Mode is Maximum Eigenmode

The staggered vector v_stag should correspond to an eigenvector of the Hessian matrix with eigenvalue 4β. Verify:
1. Construct the staggered vector as a 192-dimensional vector (64 links × 3 generators)
2. Apply the Hessian matrix: H @ v_stag
3. Check: H @ v_stag = 4β × v_stag (i.e., v_stag is an eigenvector with eigenvalue 4β)

If yes: the staggered mode IS the maximum eigenvector, confirming H_norm_max = 1/12.
If no: report the actual maximum eigenvalue and the corresponding eigenvector.

### Part 3: Test Q ≠ I

For 5 random configurations Q drawn from the SU(2)⁶⁴ product measure (uniformly random, not Gibbs), check whether the maximum eigenvalue of the Hessian at Q exceeds λ_max(I) = 4β.

Report: max eigenvalue at random Q vs at Q=I. Is Q=I always the worst case?

### Part 4: Test d=5 (if time allows)

Build the Hessian at Q=I for d=5 on a 2⁵ lattice. Verify H_norm_max = 3/40 ≈ 0.075 (the formula from E007).

## Technical Setup

For SU(2), the generators are {τ₁, τ₂, τ₃} = {iσ₁, iσ₂, iσ₃}/2 with:
- [τ_a, τ_b] = ε_{abc} τ_c (structure constants)
- Tr(τ_a τ_b) = -δ_{ab}/2

The Wilson action: S = -β Σ_{(x,μ,ν): μ<ν} Re Tr(U_{x,μ} U_{x+μ̂,ν} U_{x+ν̂,μ}⁻¹ U_{x,ν}⁻¹)

At Q=I, for tangent perturbation U_{x,μ}(t) = exp(t v_{x,μ}^a τ_a):
∂²S/∂v_{x,μ}^a ∂v_{y,ν}^b at Q=I = -β Σ_{□∋(x,μ),(y,ν)} ∂²/∂t∂s Re Tr(exp(tv_{x,μ}^aτ_a) [other links] exp(sv_{y,ν}^bτ_b) [other links])|_{t=s=0}

Save code to code/ directory, use deterministic seeds, print eigenvalue results immediately.

## Success Criteria

**Success:**
1. λ_max of Hessian at Q=I found: should be ≤ 4β
2. Staggered mode verified as eigenvector with eigenvalue 4β
3. Random Q gives max eigenvalue ≤ 4β

**Failure:** Hessian computation is too complex or noisy for the small lattice. Report: what was computed and what failed.

## Output Format

1. **code/** directory:
   - `full_hessian.py` — complete Hessian matrix computation at Q=I
   - `eigenvalue_check.py` — staggered mode verification + random Q test
   - `results.json` — all numerical results

2. **REPORT.md** covering:
   - Hessian structure at Q=I
   - Maximum eigenvalue (λ_max vs 4β vs 48β)
   - Staggered mode verification
   - Random Q test results

3. **REPORT-SUMMARY.md** (1 page):
   - Is λ_max = 4β confirmed for Q=I?
   - Is staggered mode the eigenvector?
   - Does Q=I give the worst-case eigenvalue?

## Notes
- Use L=2 (small enough for 192×192 matrix, fast)
- Save code immediately before running
- Print results as computed
- The matrix is real symmetric — use numpy.linalg.eigvalsh for efficiency
- Write section by section, not all at once
