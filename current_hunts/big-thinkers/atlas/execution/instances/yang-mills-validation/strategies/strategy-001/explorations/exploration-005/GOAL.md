# Exploration 005: SU(3) Extension

## Mission Context

The prior mission conjectured H_norm ≤ 1/12 for SU(2), d=4. The generalized conjecture for SU(N) predicts H_norm ≤ d/(4(d−1)N) = 1/18 for N=3, d=4. This exploration tests the SU(3) case.

## CRITICAL CONVENTION WARNING

**You MUST use the LEFT perturbation B_□ formula:**
```
P1 = I
P2 = Q1
P3 = Q1 @ Q2 @ Q3.conj().T           # INCLUDES Q3 inverse
P4 = Q1 @ Q2 @ Q3.conj().T @ Q4.conj().T  # = U_plaq
```

**SU(3) specifics:**
- N = 3, so N²−1 = 8 generators per link
- Action: S = −(β/3) Σ Re Tr(U_□) (β/N with N=3)
- Inner product: |A|² = −2Tr(A²) (same as SU(2))
- Gell-Mann matrices λ_a (a=1..8): τ_a = iλ_a/2, |τ_a|² = 1
- Adjoint representation is 8-dimensional

## Goal

Compute H_norm for SU(3), d=4 on L=2 and test whether H_norm ≤ 1/18.

## Tasks

### Task 1: SU(3) Setup and Q=I Sanity Check
On L=2, d=4 with SU(3):
- n_links = 64, n_gen = 8, n_dof = 512
- Full Hessian: 512×512 matrix

1. Implement the Gell-Mann matrices λ_1,...,λ_8
2. Implement adjoint_rep(g) for g ∈ SU(3): R[c,a] = −2 Re Tr(τ_c g τ_a g†)
3. Build the full Hessian at Q=I using the LEFT formula
4. Compute λ_max. Expected: 4d × (β/(2N)) per DOF → λ_max(H) = (β/(2×3)) × 4d = 4×4/6 β = 8β/3

Actually, let me derive the expected value more carefully:

At Q=I: HessS = (β/(2N)) Σ_□ |B_□|² where B_□ = v₁+v₂−v₃−v₄ (discrete curl).
The maximum of Σ_□ |B_□|²/|v|² is 4d = 16 (from the staggered mode, same Fourier argument).
So λ_max(H) = (β/(2N)) × 16 = 16β/6 = 8β/3 for N=3.

H_norm = λ_max(H) / (8(d−1)Nβ) = (8β/3) / (8×3×3×β) = 8/(3×72) = 1/27? Wait, let me recheck:
8(d−1)N = 8×3×3 = 72. H_norm = (8/3)/72 = 8/216 = 1/27.

Hmm, that doesn't match the predicted 1/18. Let me verify: the prior mission's formula is H_norm(I) = d/(4(d−1)N). For d=4, N=3: H_norm = 4/(4×3×3) = 4/36 = 1/9. That also doesn't match 1/18.

Wait, reading more carefully from MISSION-COMPLETE.md: "H_norm(I) = d/(4(d-1)N)" — but this uses a different H_norm normalization. Let me just compute numerically and let the code resolve the conventions.

**SANITY CHECK:** Whatever λ_max you get at Q=I, call it L₀. Then verify:
- L₀ = (β/(2N)) × 4d = 16β/(2×3) = 8β/3 ≈ 2.667β

### Task 2: SU(3) Random Configurations
Generate 20 random SU(3) Haar-distributed configurations:
```python
def random_su3():
    """Random Haar SU(3) via QR decomposition."""
    Z = np.random.randn(3,3) + 1j * np.random.randn(3,3)
    Q, R = np.linalg.qr(Z)
    D = np.diag(np.diag(R) / np.abs(np.diag(R)))
    Q = Q @ D
    if np.linalg.det(Q).real < 0:
        Q[:, 0] *= -1
    # Ensure det = 1
    Q /= np.linalg.det(Q)**(1/3)
    return Q
```

For each, compute λ_max(H) and H_norm. Report maximum.

### Task 3: Triangle Inequality Bound for SU(3)
The CS bound gives: |B_□|² ≤ 4 Σ|v_e|² (same as SU(2), since Ad is still an isometry).
Summing: Σ|B_□|² ≤ 4×2(d−1)×|v|² = 24|v|²
HessS ≤ (β/(2N))×24 = 4β for N=3.
K_S > 0 iff 4β < N/2 = 3/2, i.e., β < 3/8.

Check: does the triangle inequality proof generalize to SU(N)? The key is that Ad_{P}(v) is an isometry for any P ∈ SU(N). This is true (adjoint representation preserves Killing form). So H_norm ≤ 1/8 should still hold, giving β < N/(16(d−1)) for general N.

For N=3, d=4: β < 3/48 = 1/16. Wait, that's worse than 3/8. Let me recheck.

Actually K_S > 0 requires HessS(v,v) < (N/2)|v|². The CS bound gives HessS ≤ (β/(2N))×24×|v|² = 12β|v|²/N. So 12β/N < N/2 → β < N²/24.

For N=3: β < 9/24 = 3/8.
For N=2: β < 4/24 = 1/6. ✓

So the general threshold is β < N²/24 for d=4. ✓

### Task 4: Conjecture Check for SU(3)
The conjectured bound is λ_max(M(Q)) ≤ 4d = 16 for all Q ∈ SU(3)^E.
This would give HessS ≤ (β/(2N))×16 = 8β/(2N) = 8β/6 = 4β/3 for N=3.
K_S > 0 iff 4β/3 < 3/2 → β < 9/8. Hmm, that seems too large. Let me recheck.

Actually: K_S > 0 iff HessS < (N/2)|v|². HessS_max = (β/(2N)) λ_max(M).
So: (β/(2N)) × 16 < N/2 → 16β < N² → β < N²/16.
For N=3: β < 9/16 ≈ 0.5625.

Does H_norm ≤ 1/12 hold for SU(3)? Test on 20 configs. The H_norm formula is:
H_norm = λ_max(M(Q)) / (16(d−1)N²) = λ_max(M) / (16×3×9) = λ_max(M) / 432.

Wait this is getting confused. Let me just define:
- H_norm := max_v HessS(v,v) / (8(d-1)Nβ|v|²)
- At Q=I: H_norm = (β/(2N))×16 / (8×3×N×β) = 16 / (48N²) = 1/(3N²)
- For N=3: H_norm(I) = 1/27

So the question is: is H_norm ≤ 1/27 for ALL Q ∈ SU(3)^E?

JUST COMPUTE IT. Don't try to derive the answer analytically. Test 20 configs and report the max H_norm.

## Success Criteria
- [ ] λ_max at Q=I matches analytical prediction
- [ ] 20+ SU(3) configurations tested
- [ ] Clear table of H_norm by config type
- [ ] Triangle inequality threshold computed for SU(3)
- [ ] Any violation of H_norm(I) bound for general Q → report immediately

## What to Write
Write REPORT.md and REPORT-SUMMARY.md. Put all code in code/ subdirectory.
