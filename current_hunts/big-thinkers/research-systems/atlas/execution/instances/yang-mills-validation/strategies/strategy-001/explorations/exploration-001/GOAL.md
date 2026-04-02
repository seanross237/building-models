# Exploration 001: Independent Proof Rederivation — β < 1/6 from SZZ

## Mission Context

A prior research program claimed to prove a mass gap for lattice SU(2) Yang-Mills in d=4 at coupling β < 1/6 — an 8× improvement over SZZ (arXiv:2204.12737) and 4× improvement over CNS (arXiv:2509.04688). Your job is to **independently rederive this result from scratch**, starting from the SZZ paper, and then compare with the claimed proof.

This is an adversarial verification — you are trying to find errors, not confirm claims.

## Goal

Starting from the SZZ Bakry-Émery framework (arXiv:2204.12737, Theorem 1.3), independently derive the tightest mass gap threshold achievable by improving their Hessian bound (Lemma 4.1). Do NOT read the prior mission's proof first — derive it yourself.

## Staged Tasks

### Stage 0: Convention Setup and Sanity Check
State precisely the SZZ convention:
- Wilson action: S(Q) = −(β/N) Σ_{□} Re Tr(U_□), where N=2 for SU(2)
- Inner product on su(N): ⟨A,B⟩ = −2 Re Tr(AB), so |A|² = −2 Tr(A²)
- For SU(2) generators τ_a = iσ_a/2: |τ_a|² = 1

**Convention table (critical — get this right):**

| Convention | Action formula | λ_max at Q=I | H_norm at Q=I |
|-----------|---------------|-------------|--------------|
| S1 (raw) | S = −β Σ Re Tr(U_□) | 8β | 1/6 |
| S2 (SZZ) | S = −(β/N) Σ Re Tr(U_□) | 4β | 1/12 |

You MUST use S2 (SZZ convention) throughout. If you ever get λ_max = 8β at Q=I, you have a convention error.

**Sanity check:** On a small lattice (L=2, d=4), compute the Hessian of S at Q=I numerically. Verify that:
1. The Hessian is a 192×192 matrix (64 links × 3 generators)
2. λ_max = 4β exactly
3. The Hessian is positive semi-definite

If this sanity check fails, STOP and diagnose the convention issue before proceeding.

### Stage 1: State the SZZ Bakry-Émery Condition
From arXiv:2204.12737 Theorem 1.3, the mass gap condition is:
- The Bakry-Émery curvature K_S = Ric − HessS > 0 implies a spectral gap
- Ric(v,v) = (N/2)|v|² for SU(N) (Ricci curvature of the product manifold)
- So K_S > 0 iff HessS(v,v) < (N/2)|v|² for all v

SZZ Lemma 4.1 bounds: HessS(v,v) ≤ 8(d−1)Nβ|v|²

This gives K_S > 0 iff 8(d−1)Nβ < N/2, i.e., β < 1/(16(d−1)) = 1/48 for d=4.

**Verify this derivation step by step.** Write out each inequality. Check that 16(d−1) = 48 for d=4.

### Stage 2: Analyze Where SZZ's Lemma 4.1 is Loose
The SZZ bound HessS(v,v) ≤ 8(d−1)Nβ|v|² comes from bounding each plaquette's Hessian contribution individually.

For each plaquette □ with edges e₁, e₂, e₃, e₄ (where e₃, e₄ are backward):
- The Hessian contribution involves B_□(Q,v) = v₁ + Ad_{P₁}(v₂) − Ad_{P₃}(v₃) − Ad_{P₄}(v₄)
  where P_k are partial holonomies around the plaquette
- At Q=I: B_□(I,v) = v₁ + v₂ − v₃ − v₄ (no parallel transport)

SZZ bounds |B_□|² ≤ (sum of |v_e|)² per plaquette, then sums over plaquettes. This is the triangle inequality.

**Your task:** Try to do better. Specifically:

1. At Q=I, can you compute HessS(v,v) exactly using Fourier analysis? The lattice has translation symmetry, so the Hessian decomposes in Fourier space.

2. What is the maximum of HessS(v,v)/|v|² over all tangent vectors v at Q=I? This gives the exact H_norm at Q=I.

3. For general Q, the triangle inequality gives |B_□(Q,v)|² ≤ (|v₁| + |v₂| + |v₃| + |v₄|)² since Ad acts as an isometry. Can you get a tighter bound by using Cauchy-Schwarz more carefully? Specifically, try bounding Σ_□ |B_□|² using the fact that each link appears in exactly 2(d−1) plaquettes.

### Stage 3: Derive Your Best Threshold
Whatever bound you get for max_v HessS(v,v)/|v|², call it C·β. Then:
- K_S > 0 iff Cβ < N/2
- Mass gap at β < N/(2C)

What value of C do you get? What threshold for β?

### Stage 4: Numerical Verification
On L=2, d=4, SU(2):
1. Compute the exact Hessian at Q=I (192×192 matrix)
2. Compute λ_max — does it agree with your analytical formula?
3. Compute HessS(v_stag, v_stag)/|v_stag|² for the staggered mode v_{x,μ} = (−1)^{|x|+μ} τ₁ — is this the maximum?
4. For 5 random Q (Haar-distributed), compute H_norm numerically. Is it less than your analytical bound?

### Stage 5: Compare with the Claimed Proof
After completing your independent derivation, read the prior mission's claimed proof chain:
- λ_max(M(Q)) ≤ 8(d−1) = 24 for all Q via triangle inequality
- H_norm = λ_max/(48) ≤ 24/48 = 1/2... wait, that gives 1/2 not 1/8.
- The claimed H_norm ≤ 1/8 needs a tighter triangle inequality argument. What is it?

Does your derivation agree with theirs? If not, where exactly does the discrepancy arise?

## Success Criteria
- [ ] Convention sanity check passes (λ_max = 4β at Q=I under SZZ)
- [ ] Independent derivation of the best achievable β threshold from the SZZ framework
- [ ] Numerical verification on L=2 lattice
- [ ] Clear comparison with the claimed β < 1/6 result
- [ ] Every step written with explicit formulas, not just "it follows that..."

## Failure Criteria
- Convention error detected → STOP, diagnose, report the error
- Your threshold differs from 1/6 → report BOTH numbers and explain the discrepancy
- The sanity check fails → this is actually the most important finding

## What to Write
Write REPORT.md and REPORT-SUMMARY.md in your exploration directory. Include all computations with runnable code. The report should be self-contained — a reader should be able to verify every step.
