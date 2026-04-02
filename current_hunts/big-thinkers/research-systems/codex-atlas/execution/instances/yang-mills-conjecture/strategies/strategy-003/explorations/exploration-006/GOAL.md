# Exploration 006: Direct Hessian Bound — Per-Plaquette and Anti-Correlation

## Mission Context

We need to prove |λ(HessS(Q))| ≤ 4d for all Q ∈ SU(2)^E on the d-dimensional hypercubic torus. This gives a mass gap at β < 1/(2d) = 1/8 for d=4.

**The D+C decomposition approach FAILED** (E005): the decoherence lemma ||C|| ≤ 2(d+1) is false for d≥3. But the full Hessian bound |λ(H)| ≤ 4d STILL holds in all tested configs. The mechanism is D/C anti-correlation: when ||C|| is large, |D| is small.

**This is the LAST proof attempt.** Everything else is done.

## What's Already Established

1. **Hessian formula** (E002, verified):
   - H = D(Q) + C(Q) where D = self-term (diagonal), C = cross-term
   - D_{(e,a)} = (β/N) Σ_{□∋e} Re Tr(U_□) — diagonal in color
   - C_{(ep,a),(eq,b)} = -(β/N) sp sq Re Tr(Lp iσa mid iσb Rq) — cross-terms

2. **Bounds on components:**
   - |D| ≤ 2(d-1) [PROVED]
   - Per-plaquette: ||C_□|| ≤ 3 [PROVED, E005]
   - Per-plaquette total: ||H_□|| ≤ 4 at flat [VERIFIED]
   - Color kernel F: SVs exactly (2, 2, 2|β₀|) where β₀ = Re Tr(MN)/2 [VERIFIED]

3. **Empirical bounds:**
   - λ_max(H) ≤ 16 = 4d (d=4) — zero violations in thousands of configs + gradient ascent
   - λ_min(H) ≥ -14.73 > -16 (d=4) — adversarial search
   - Flat connections are the unique global maximum of λ_max(H) [COMPUTED]

4. **D/C anti-correlation (E004-E005):**
   - Configs maximizing ||C|| (near saddle points, D ≈ 0) have ||C|| ≈ 11.68 but |λ(H)| ≈ 11.9
   - Configs maximizing |D| (anti-instantons, D = -6) have ||C|| ≈ 8.65, |λ(H)| ≈ 14.7
   - Pure flat (D = 6, ||C|| = 10): |λ(H)| = 16

## Your Tasks — Two Proof Approaches

### Approach A: Per-Plaquette Bound on the FULL Hessian H

Each plaquette □ contributes H_□ to the Hessian: H = Σ_□ H_□.

**Per-plaquette Hessian:** For plaquette □ with edges (e₁,...,e₄):
H_□ = D_□ + C_□

where D_□ is the self-term contribution and C_□ is the cross-term.

1. **Compute ||H_□||_op** numerically for 500+ random Q configs and gradient ascent.
   - At flat: ||H_□|| should be 4 (verify).
   - Is ||H_□|| ≤ 4 for ALL Q? If yes, this would be a per-plaquette version of our conjecture.

2. **If ||H_□|| ≤ 4 for all Q:** Can you prove it?
   H_□(v,v) = self-terms + cross-terms for edges of □.
   Each edge e has self-contribution (β/N) Re Tr(U_□) |c_e|² from this plaquette.
   Cross terms have 6 pairs, each bounded by |c_{ep}||c_{eq}| × 2 (from ||F|| = 2).

   Total: H_□(v,v) = (1/2) Re Tr(U_□) Σ|c_e|² + Σ_{p<q} s_p s_q c_p^T F^{pq} c_q

   At flat (Re Tr = 2): H_□ = Σ|c_e|² - Σ_{p<q} c_p^T (2I₃) c_q = (stuff involving signs s_p s_q)

3. **Aggregation:** If ||H_□|| ≤ f(Q_□) with Σ_□ f ≤ 4d, done.
   Each edge is in 2(d-1) plaquettes. The aggregation requires understanding the edge-overlap structure.

### Approach B: D/C Anti-Correlation Bound

**Goal:** Show that |D_min(Q)| + ||C(Q)||_op ≤ 4d for all Q.

This is WEAKER than decoherence (which bounds ||C|| alone) but accounts for the anti-correlation.

**Strategy:**
1. Express both |D| and ||C|| in terms of plaquette variables Re Tr(U_□).
2. D = (1/2) Σ_{□∋e} Re Tr(U_□) for each edge e, so |D_min| depends on the most negative sum of Re Tr.
3. ||C|| depends on the plaquette context matrices (not just Re Tr). But:
   - From E005: ||C_□|| ≤ 3 for each plaquette
   - The inter-plaquette aggregation of C depends on sign correlations
   - When Re Tr(U_□) ≈ -2 (maximizing |D|), the cross-terms have specific alignment patterns

4. **Numerical test:** For 1000+ configs, plot |D_min| + ||C||_op. Is it always ≤ 4d?
   From E005 data: max was 15.43 (anti-instanton GD). Is 4d = 16 always respected?

5. **If the combined bound holds:** Try to prove it by showing:
   - When Re Tr(U_□) = -2 for many □ (making |D| large): the cross-term color kernels have β₀ = Re Tr(MN)/2 ≈ -1, forcing the deficient SVD direction. This reduces ||C||.
   - Quantify: if Σ Re Tr(U_□) ≤ -c for edges of □, then ||C_□|| ≤ 3 - f(c) for some f.

### Approach C: Convexity / Local Maximum Argument

**Goal:** Show flat connections are the unique global maximum of λ_max(H(Q)).

E003 showed: d²λ_max/dε² < 0 for ALL perturbation directions from flat. So flat IS a strict local maximum.

1. **Is λ_max(H(Q)) a concave function of Q?** If yes, the local max is global.
   Test: for random Q₁, Q₂, is λ_max(H(tQ₁ + (1-t)Q₂)) ≤ t λ_max(H(Q₁)) + (1-t)λ_max(H(Q₂))?
   (Here "tQ₁ + (1-t)Q₂" means geodesic interpolation on SU(2).)

2. **Is there a Morse-theory argument?** λ_max(H(Q)) has flat connections as critical points with negative-definite Hessian. If the function has no other local maxima, flat is global.
   Test: run gradient ASCENT on λ_max(H(Q)) from 100 random starts. Do they all converge to flat?

3. **Does gauge invariance help?** H(Q) is gauge-invariant (H(gQg⁻¹) = H(Q) up to conjugation). Can we use the gauge orbit structure to reduce the problem?

## Numerical Verification

For EVERY bound or claim:
- Implement and test on L=2, d=4
- At least 100 configs (random + structured)
- Include anti-instanton starts (these are the hardest cases)
- Report exact values, not just pass/fail

## Priority Order

1. Approach B (anti-correlation) — most directly addresses the gap
2. Approach C (convexity) — if concavity holds, gives immediate proof
3. Approach A (per-plaquette H) — fallback if B and C fail

## Success Criteria

- ONE of the three approaches gives a proof of |λ(H)| ≤ 4d
- OR: proves a weaker bound (e.g., |λ| ≤ 5d or 6d) that still improves on SZZ
- OR: clear obstruction report for all three approaches

## Output

Write to REPORT.md (≤ 250 lines) and REPORT-SUMMARY.md (≤ 30 lines). Write incrementally.
