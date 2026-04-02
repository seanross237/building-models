# Exploration 003 Summary: Synthesis — Proof Strategy Assessment for λ_max(HessS) Global Maximum

## What Was the Goal

Synthesize findings from two prior literature surveys (classical eigenvalue concavity theorems; geodesic convexity on compact Lie groups) into a ranked assessment of proof strategies for establishing that λ_max(HessS(Q)) achieves its global maximum at Q = I (flat connection) on SU(N)^E.

---

## What Was Tried

This was a synthesis and analysis task — no new literature search. I cross-referenced the two survey bodies, identified connections between classical matrix analysis results (majorization, Schur-Horn/Kostant, 2024 unitary technique) and the topological/structural frameworks (perfect Morse theory, Rabitz trap-free, gauge symmetry), and ranked 8 candidate proof approaches.

---

## What Was the Outcome

**Succeeded.** Clear ranked list produced, connections between surveys identified, critical path specified, failure modes analyzed for top two approaches.

---

## Key Takeaway

**A new highest-priority approach emerged from the synthesis: direct matrix domination H(I) ≥ H(Q) as a positive semidefinite matrix.** Neither prior survey had explicitly named this as an approach. If H(I) - H(Q) ≥ 0 (PSD) for all Q, then λ_max(H(Q)) ≤ λ_max(H(I)) in two lines — no topology, no Morse theory, no gauge arguments needed. The "destructive interference" of plaquette contributions (SZZ bound 12-170x loose) is strong circumstantial evidence this might hold.

**Recommended critical path:**
1. **First:** Numerical matrix domination test for random Q ∈ SU(2)^E (1-2 days, ~20 lines of numpy). Either solves the problem or closes this path.
2. **In parallel:** Gradient ascent landscape survey — confirm Q=I is the unique attractor (1-2 days).
3. **If domination holds:** Analytical proof via D + C decomposition of Hessian.
4. **If domination fails, landscape clean:** Verify Rabitz transversality condition (rank of dH at non-flat critical points). If full rank: trap-free result applies.
5. **If all else:** Kirwan-type equivariant Morse theory with gauge symmetry. Hard (2-4 weeks), but has solid precedent from Atiyah-Bott on Riemann surfaces.

---

## Ranked Approaches

| Rank | Approach | Overall |
|------|----------|---------|
| 1 | Matrix domination H(I) ≥ H(Q) | ★★★★★ |
| 2 | Direct majorization λ(H(Q)) ≺ λ(H(I)) | ★★★★★ |
| 3 | Perfect Morse + gauge symmetry (Kirwan-type) | ★★★★ |
| 4 | Trap-free landscape (Rabitz transversality) | ★★★★ |
| 5 | Local second-variation at Q=I | ★★★ |
| 6–8 | Łojasiewicz, double bracket, SDP | ★★–★★★ |

---

## Connections Between Surveys (Key Finding)

1. **Majorization ≠ Morse theory — they are independent paths.** Majorization (if it holds) makes Morse theory unnecessary. If majorization fails, Morse is the fallback. Kostant/Schur-Horn only covers the gauge orbit of I, not global majorization.

2. **2024 unitary technique is a local bridge.** The second-variation formula from arXiv:2408.16906 establishes local concavity of λ_max(H(Q(t))) at Q=I within the convexity ball (~π√2/2 in each SU(2) factor). Combined with a landscape survey outside the ball, it can give global uniqueness.

3. **Matrix domination subsumes everything.** If H(I) - H(Q) ≥ 0 globally, it implies majorization, implies λ_max bound, implies Q=I is the unique global maximizer — without any topology. The plaquette interference structure makes this plausible.

---

## Failure Modes (Top Two)

**Matrix domination:** Fails if some Q has H(Q) with eigenvalues exceeding 1/12 (e.g., near an anti-flat plaquette configuration with holonomy ≈ -I). Check: compute H(Q) for Q with one plaquette holonomy = -I.

**Perfect Morse:** Fails if a second, non-flat local maximum exists. Check: gradient ascent from 1000 random starts. If any trajectory converges to Q* ≠ I (up to gauge), compute Hessian index there.

---

## Unexpected Findings

**The biggest gap in the literature:** No one has applied matrix domination (PSD ordering of Hessians) to lattice gauge theory. The SZZ bound is a SCALAR bound on λ_max, not a MATRIX bound. A matrix bound H(I) ≥ H(Q) would be far stronger and may be provable from the explicit Hessian formula. This appears to be a genuinely novel direction.

**Invexity confirmation:** The two surveys collectively show that "invexity" (every stationary point is a global max) is the correct abstract characterization of what we need to prove — but it's a tautological restatement. The real question is which of the four concrete mechanisms (domination, majorization, Morse, trap-free) delivers it.

---

## Computations Identified

1. **Numerical matrix domination test** — for ~1000 random Q ∈ SU(2)^E, check whether H(I) - H(Q) is PSD. Input: explicit H(Q) formula (D + C decomposition from Yang-Mills work). Difficulty: easy (20-line numpy). If positive: provides proof sketch. High priority.

2. **Gradient ascent landscape survey** — run gradient ascent on λ_max(H(Q)) from 1000 random starts on SU(2)^E (E = 4, 8). Record all attractors found. Input: explicit gradient of λ_max(H(Q)). Difficulty: moderate (100-line gradient ascent). If always converges to Q=I: supports perfect Morse.

3. **Rank of dH at critical points** — at any non-flat critical points found by (2), compute rank of the Jacobian of Q ↦ H(Q). Input: explicit dH formula. Difficulty: moderate. If full rank everywhere: Rabitz trap-free applies.
