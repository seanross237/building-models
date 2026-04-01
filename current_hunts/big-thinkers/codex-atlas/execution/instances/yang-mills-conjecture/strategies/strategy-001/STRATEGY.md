# Strategy 001: Algebraic Decomposition and Proof Construction

## Objective

Prove (or precisely characterize the remaining obstruction to proving) Conjecture 1:

  For all Q in SU(2)^E on the d=4 hypercubic torus: lambda_max(M(Q)) <= 4d = 16

Equivalently: P^T R(Q) P <= 0 for all Q, where P is the 9-dimensional top eigenspace of M(I) and R(Q) = M(Q) - M(I).

This is the single inequality separating the proved beta < 1/6 from the conjectured beta < 1/4. A proof would yield a 12x improvement over SZZ (2023) and 6x over CNS (2025).

## Methodology: Decompose-Construct-Verify Pipeline

This is a proof problem. The prior mission (3 strategies, 30 explorations) comprehensively mapped the landscape, proved special cases, and eliminated 7 proof approaches. This strategy must go beyond mapping and attempt construction.

The methodology is a three-phase pipeline designed to find the proof's algebraic backbone first, then build the proof around it, then stress-test the result.

### Phase 1: Algebraic Decomposition (3 explorations, run in parallel)

**Goal:** Break the inequality P^T R(Q) P <= 0 into its algebraic constituents and find WHERE the hypercubic/SU(2) structure forces the bound. Each exploration attacks a different decomposition.

**Rules for Phase 1:**
- Every exploration MUST be a math explorer.
- Every exploration MUST start with numerical computation on L=2, d=4 before any algebraic manipulation. Compute first, derive second.
- Every exploration MUST produce: (a) a computational verification table, (b) an algebraic decomposition of the target quantity, (c) a clear statement of what sub-inequality would suffice for a proof.
- Write derivations incrementally — output each step to file as you complete it. If 10 minutes pass with no file write, output your current state immediately.

**Three decompositions to explore in parallel:**

1. **Maximal Tree Gauge Decomposition.** Fix a maximal spanning tree T of the lattice to identity (all links on T set to I via gauge transformation). This leaves only the "cocycle" links (one per fundamental cycle of the torus, plus the non-tree links) as free variables. In this gauge, most partial holonomies simplify. Compute P^T R(Q) P in maximal tree gauge. Count the effective degrees of freedom. Identify which cocycle links contribute most to the top eigenvalue. The question: does the reduced form reveal a tractable bound?

2. **Per-Plaquette Contribution Structure.** For v in P (staggered mode), write v^T R(Q) v = sum_plaquette f_plaq(Q). Each f_plaq depends on Q through partial holonomy rotations Ad(P_k) in SO(3). Compute f_plaq for every plaquette type (by orientation and position) for 50+ random Q. Map which plaquettes contribute positively and which negatively. Find the cancellation pattern. The question: is there a natural grouping of plaquettes (e.g., pairs sharing an edge, stars around a vertex) such that each GROUP's contribution is <= 0?

3. **SU(2)/SO(3) Representation Theory Bound.** Ad(SU(2)) = SO(3). Each partial holonomy rotation P_k acts via Ad(P_k) in SO(3). For v in P with fixed algebra direction n, v^T R(Q) v involves terms like |c_1 n + c_2 R_1 n + c_3 R_2 n + c_4 R_3 n|^2 - 4|n|^2 where c_k in {+/-1} and R_k in SO(3). Study the geometry: what is the maximum of |c_1 n + c_2 R_1 n + c_3 R_2 n + c_4 R_3 n|^2 over all R_k in SO(3), for fixed staggered signs c_k? Compute this maximum numerically (parametric sweep over SO(3)^3). If the per-plaquette maximum exceeds 4|n|^2 (which the prior mission says it does), characterize by how much. Find which SO(3) configurations of (R_1, R_2, R_3) are worst-case, and whether they can simultaneously occur across ALL plaquettes.

### Phase 2: Proof Construction + Adversarial (4 explorations, sequential with adaptation)

**Goal:** Use the Phase 1 decompositions to construct a proof attempt, then immediately stress-test it.

**Rules for Phase 2:**
- The first exploration in Phase 2 MUST synthesize ALL Phase 1 findings before choosing a proof direction. Don't launch a proof attempt without reading all three decompositions.
- Exploration 4 (the synthesis): read all three Phase 1 reports. Identify which decomposition gave the tightest sub-inequalities. Write a proof outline that chains them. Identify the single hardest step and state it precisely.
- Exploration 5: attempt the proof. This MUST be a math explorer. Every claimed inequality MUST be verified computationally on at least L=2 and L=4 lattices, for at least 50 configurations.
- Exploration 6: MANDATORY adversarial review. Goal: find a gap in the proof from E5, or find a configuration that comes closest to violating the bound. Use gradient ascent on P^T R(Q) P restricted to the "worst case" structure identified in Phase 1.
- Exploration 7: second proof attempt (or repair of first, depending on E6). If E5 failed completely, try a fundamentally different approach (not a patch).

**Adaptation rules:**
- If Phase 1 reveals that one decomposition is dramatically more tractable, allocate E5 and E7 to that decomposition (attacking from two angles).
- If Phase 1 reveals a structural reason the conjecture might be FALSE, pivot immediately: spend E5 on searching for counterexamples (large lattices, high-dimensional, SU(3)).
- If the synthesis (E4) concludes that no decomposition gives a tractable path, spend E5-E7 on the best partial result: tightening the proved bound from H_norm <= 1/8 toward 1/12 for restricted classes of Q.

### Phase 3: Consolidation (3 explorations)

**Goal:** Produce a defensible final report with either a proof or a precise characterization of what remains.

- Exploration 8: If a proof exists from Phase 2, formalize it cleanly with full details. If not, synthesize the best partial results and the tightest obstruction characterization.
- Exploration 9: Final adversarial review. Try to break whatever was produced. For a proof: find logical gaps and test numerically at L=4 and L=6. For a partial result: check whether the claimed bounds are optimal.
- Exploration 10: Write the final synthesis. This should be presentable to a mathematician working on lattice Yang-Mills.

## Cross-Phase Rules (MANDATORY for every exploration)

1. **Compute first, always.** No algebraic claim without numerical verification. Minimum: L=2, d=4, 50 configs. Better: L=2 AND L=4, 100+ configs.
2. **Use the corrected B_square formula.** Backward edges include their OWN link in the partial holonomy. See MISSION.md for the exact formula.
3. **Incremental writing.** Write each derivation step to file as you complete it. If more than 10 minutes pass with no file output, dump your current state. Long silent thinking periods waste the entire exploration.
4. **Tag every claim.** Use [PROVED], [COMPUTED], [CHECKED], or [CONJECTURED]. No untagged claims.
5. **Pre-load context.** Every exploration goal MUST include the relevant findings from the prior mission (the 7 dead ends, the Weitzenbock formula, the special cases proved, the decoherence mechanism).
6. **Do not revisit dead ends.** The following are PROVEN impossible or insufficient. Do not spend time on them:
   - Full operator ordering M(Q) <= M(I) (FALSE — trace invariant forces R(Q) to have positive eigenvalues)
   - Global geodesic concavity (FAILS at Q != I)
   - Per-plaquette factoring (FALSE for Q != I, ratio up to 8383x)
   - Coulomb gauge / perturbative Fourier (Gribov problem)
   - Jiang Weitzenbock F <= 0 (Jiang proves no sign for F in general)
   - Schur / Haar average (average != maximum)
   - Triangle inequality refinement (capped at H_norm <= 1/8, structurally cannot reach 1/12)

## Validation Criteria

**Success (strategy complete with proof):**
- A complete chain of inequalities from P^T R(Q) P <= 0 for all Q, with every step tagged [PROVED] and computationally verified
- Known special cases (pure gauge, flat, uniform, single-link) recovered as consequences
- Survives adversarial review (E6 and E9)

**Success (strategy complete with partial result):**
- H_norm bound tightened below 1/8 for all Q (improving beta < 1/6)
- OR: Conjecture 1 proved for a new family of configurations beyond the 4 known special cases
- OR: A precise reduction — "Conjecture 1 follows from inequality X, and X is equivalent to Y" — where Y is simpler/more tractable than the original

**Strategy exhausted:**
- All three Phase 1 decompositions produce intractable sub-problems AND the adversarial review (E6) finds no promising angles AND no partial improvement is achieved

## Context from Prior Mission

### What's Proved
- H_norm <= 1/8 for all Q -> beta < 1/6 (rigorous, via triangle inequality)
- H_norm = 1/12 at Q=I, achieved by staggered mode v = (-1)^{|x|+mu}
- Pure gauge isometry: M(Q_pure) = Ad_G^T M(I) Ad_G (isospectral)
- Trace invariant: Tr(M(Q)) = const for all Q
- Conjecture verified for 500+ configs including adversarial gradient ascent, zero violations
- Proved for: pure gauge, flat connections, uniform Q, single-link

### Key Structural Insight
R(Q)|_P <= 0 is the correct target (not R(Q) <= 0 as a full operator). The Weitzenbock exact formula gives max lambda[R(Q)|_P] = -W(Q)/12 for single-link (exact), and max lambda[R(Q)|_P] <= -W(Q)/12 for general Q (42/42 verified). Gradient ascent on P^T R(Q) P stays at -8 to -11, far from 0.

### The Decoherence Mechanism
At Q=I, staggered modes achieve maximum constructive interference in B_square(I,v) = 4d|v|^2. At Q != I, parallel transport Ad(G_k) rotations "misalign" contributions, causing destructive interference. The proof must formalize this decoherence.

### The Most Promising Untried Approach (from MISSION.md)
Staggered-mode Weitzenbock: for v = (-1)^{|x|+mu} n,
  v^T R(Q) v = sum_plaq [|sum_k c_k Ad(P_k)(n)|^2 - 4] |n|^2
where c_k in {+/-1} are staggered signs. Per-plaquette bound is FALSE, but the global sum may be bounded by exploiting the staggered sign structure on the hypercubic lattice.

### Key References
- SZZ: arXiv:2204.12737 (Bakry-Emery, beta < 1/48)
- CNS: arXiv:2509.04688 (beta < 1/24)
- Jiang: arXiv:2211.17195 (discrete Weitzenbock identity, no sign proved)

## Budget

10 explorations maximum. Do not request more. If progress is insufficient by exploration 7, shift to consolidation (partial results + obstruction characterization).
