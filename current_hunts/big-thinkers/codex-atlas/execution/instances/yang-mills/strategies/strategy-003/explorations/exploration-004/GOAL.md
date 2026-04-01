# Exploration 004: Large-Lattice Verification (L=4) + Analytical Gradient Adversarial Search

## Mission Context
This is a YANG-MILLS mission (strategy-003). Do not confuse with other missions.

## Background

From Strategy 002 (E010): On an L=2, d=4, SU(2) lattice, H_norm ≤ 1/12 was confirmed for 100 diverse configurations. Max observed: 0.083331 ≈ 1/12 only near Q=I. Q=I is the unique worst case.

**Potential concern:** L=2 is very small (only 2 sites per dimension). Finite-size effects could hide a counterexample at larger L. We need to verify on L=4 (3072-dimensional Hessian, much more representative).

**Convention (required):** S = −(β/N) Σ_□ Re Tr(U_□), |A|² = −2Tr(A²). Always verify λ_max = 4β at Q=I before running the scan.

## Your Task

### Part 1 (Priority 1): L=4 Hessian Scan with Analytical Gradient Adversarial Search

Build the full Hessian at several L=4 configurations and test whether H_norm > 1/12.

**Technical setup:**
- L=4, d=4, SU(2): 4⁴=256 sites, 1024 links, 3 generators/link → 3072×3072 Hessian
- Full diagonalization of 3072×3072 is slow. Use **power iteration** for λ_max instead:
  - Start with a random vector w₀ of dimension 3072
  - Iterate: w_{n+1} = H w_n / |H w_n|  (apply Hessian, normalize)
  - Converges to the maximum eigenvector in ~100 iterations
  - Or use `scipy.sparse.linalg.eigsh(H, k=1, which='LM')` for a sparse Hessian

**Configurations to test (50+ total):**

A. **Q=I verification:** Confirm λ_max = 4β (or λ_max/(48β) = 1/12). This is the sanity check — if this fails, stop and debug.

B. **Staggered mode verification:** Confirm the staggered mode v_stag = {(-1)^(|x|+μ) * τ₁} is an eigenvector with eigenvalue 4β at L=4.

C. **Random Haar configs (20):** Draw Q_{x,μ} uniformly from SU(2) (random unit quaternions). Compute λ_max via power iteration. Report H_norm.

D. **Gibbs samples (10):** Sample from the SU(2) Gibbs measure at β=0.5, 1.0, 2.0, 3.0 (using heat bath). Report H_norm for each.

E. **Analytical gradient adversarial search (20):** THIS IS THE KEY NEW ELEMENT vs E010.

   In E010, the adversarial search used stochastic hill climbing (random perturbations). Here, use the ANALYTICAL gradient of H_norm with respect to Q.

   The gradient of λ_max(Q) with respect to Q_{x,μ} is:
   ∂λ_max/∂Q_{x,μ} = v_max^T (∂H/∂Q_{x,μ}) v_max
   where v_max is the maximum eigenvector and ∂H/∂Q_{x,μ} is the derivative of the Hessian matrix.

   Compute this analytically using the formula H[i,j] = ∂²S/∂v_i∂v_j. The gradient ∂H[i,j]/∂Q_{x,μ} can be computed by differentiating the plaquette Hessian formula (E008/E009's code).

   Gradient ascent algorithm:
   1. Start from 5 different initial configs (random, near-identity, Gibbs samples)
   2. Compute λ_max and v_max via power iteration
   3. Compute gradient ∂λ_max/∂Q_{x,μ} = v_max^T (∂H/∂Q_{x,μ}) v_max for each link
   4. Project gradient to tangent space of SU(2) at Q_{x,μ} (Riemannian gradient)
   5. Take a step: Q_{x,μ} ← Q_{x,μ} * exp(α * grad_{x,μ}) for step size α
   6. Repeat 200 steps with decreasing α (line search or fixed schedule)
   7. Report: does gradient ascent find H_norm > 1/12? What does it converge to?

F. **Near-identity perturbations (L=4-specific):** At L=4, the staggered mode k*=(π,...,π) has wavelength 2, which fits into L=4 exactly. Check: are there larger-wavelength modes at L=4 that could give higher H_norm? Test with v = {(-1)^(|x|/2) * v₀} (wavelength-4 staggered).

### Part 2 (Priority 2): d=5 Anomaly Investigation

Strategy 002 E009 found: at d=5, the staggered mode is NOT the maximum eigenvector (true λ_max = 5β > 4.8β for staggered, where 4.8β = 3/40 × 64β).

**Task:** On a small d=5 lattice (L=2, so 2⁵=32 sites, 160 links):
1. Find the maximum eigenvector at Q=I. What is it?
2. How does it differ from the staggered mode?
3. Is there a formula for λ_max at general d? (E008 suggests d=4 is special because N_active = d²/4 only holds for d=4.)
4. What is H_norm_max(d=5)? (E009 found 5/64 ≈ 0.078, E008's formula gives 3/40 = 0.075.)

Understanding d=5 may illuminate why d=4 is the tight case.

### Part 3 (Priority 3): B_P Intermediate Bound at L=4

E010 found: ∑_□ |B_□(Q,v)|² = 4d × |v|² = 16|v|² exactly at Q=I, and < 16|v|² for all other tested Q (at L=2).

Verify this at L=4: is ∑_□ |B_□(Q,v)|² / |v|² always ≤ 16 = 4d for L=4 configs? Test for the maximum eigenvector v_max at each configuration.

This directly tests the open conjecture ∑_□ |B_□|² ≤ 4d|v|² at L=4.

## Technical Notes

**SU(2) parametrization:** Q = a₀ I + i(a₁σ₁ + a₂σ₂ + a₃σ₃) with a₀² + a₁² + a₂² + a₃² = 1. Random Haar = random unit quaternion. Exponential map: exp(tA) = cos(t|a|)I + sin(t|a|)|a|⁻¹ A for A = Σ aᵢτᵢ.

**Hessian building:** You can reuse/adapt the code from Strategy 002 E009 at:
../../strategy-002/explorations/exploration-009/code/full_hessian.py
Adapt for L=4 and use power iteration instead of full eigvalsh.

**Power iteration convergence check:** After 100 iterations, check |H w - λ w| / (λ|w|) < 1e-6.

**Analytical gradient of Hessian:** For each link (x,μ), the Hessian H depends on Q_{x,μ} through all plaquettes □ containing (x,μ). There are 2(d-1) such plaquettes. Differentiate the plaquette Hessian H_□(v;Q) with respect to Q_{x,μ} to get ∂H/∂Q_{x,μ}.

## Success Criteria

**Part 1 success:** 50+ L=4 configs tested with zero H_norm > 1/12. Analytical gradient ascent converges to Q≈I (not to some other maximum). Report: what is the max H_norm observed at L=4?

**Part 1 major finding:** If gradient ascent finds H_norm > 1/12 for some Q: REPORT IMMEDIATELY. This is a counterexample to the conjecture.

**Part 2 success:** Maximum eigenvector at Q=I for d=5 identified and explained.

**Part 3 success:** B_P bound ∑|B_□|² ≤ 16|v|² confirmed at L=4.

## Output Format

**code/** directory:
- `hessian_l4.py` — L=4 Hessian builder with power iteration
- `gradient_ascent.py` — analytical gradient adversarial search
- `d5_analysis.py` — d=5 maximum eigenvector investigation
- `results.json` — all numerical results

**REPORT.md** section by section:
1. Sanity check (Q=I, λ_max = 4β)
2. Random + Gibbs scan results
3. Analytical gradient adversarial search results and convergence
4. d=5 anomaly findings
5. B_P intermediate bound results
6. Conclusions

**REPORT-SUMMARY.md** (1 page):
- Is H_norm ≤ 1/12 confirmed at L=4 with zero counterexamples?
- What did gradient ascent converge to?
- What is the d=5 maximum eigenvector?
- Is ∑|B_□|² ≤ 16|v|² confirmed at L=4?

## Critical Requirement
Save code FIRST before running. Print results as computed. Write REPORT.md section by section — do NOT wait until the end. If 5 minutes pass without writing, write a progress update.
