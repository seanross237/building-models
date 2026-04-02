# Exploration 003: Synthesis — Proof Strategy Assessment for λ_max(HessS) Global Maximum

## Goal Summary

Given findings from two prior literature surveys on (1) classical eigenvalue concavity/convexity theorems and (2) geodesic convexity and global optimality frameworks on compact Lie groups, produce a ranked assessment of proof strategies for establishing that λ_max(HessS(Q)) achieves its global maximum at Q = I (flat connection) on SU(N)^E.

This is a synthesis report. Its goal is to connect the two bodies of literature, rank approaches, and produce a concrete recommended proof strategy.

---

## Section 1: Cross-Reference — Where the Two Surveys Connect

### 1.1 Majorization (Survey 1) and Kostant's Theorem (Survey 1/2)

Survey 1 identified majorization as a direct proof path: if λ(H(Q)) ≺ λ(H(I)) for all Q (eigenvalues of H(Q) are majorized by those of H(I)), then λ_max(H(Q)) ≤ λ_max(H(I)) immediately, solving the problem.

**Connection to Kostant:** Kostant's convexity theorem says P(Ad(K)·X) = convex hull of Weyl orbit. In matrix terms (Schur-Horn theorem), this says: the diagonal entries of all unitary conjugates of a Hermitian matrix A form the convex hull of permutations of λ(A). This gives majorization — but only **within the unitary conjugacy orbit of A**.

The Schur-Horn theorem would give λ(H(Q)) ≺ λ(H(I)) **if and only if H(Q) were always a unitary conjugate of H(I)**. This is exactly true on the gauge orbit of the flat connection (gauge-equivalent configurations give unitarily conjugate Hessians). But for Q NOT gauge-equivalent to I, H(Q) has a fundamentally different form — it is not a conjugate of H(I), but a genuinely different matrix.

**Conclusion:** Kostant/Schur-Horn gives majorization on the gauge orbit of I, not globally. Majorization as a global statement would require proving H(Q) is "covered" by H(I) via some other mechanism — this is a separate, open question.

**Key distinction:** Majorization λ(H(Q)) ≺ λ(H(I)) is strictly stronger than Morse-theoretic uniqueness of maximum. If majorization holds, we get bounds on ALL eigenvalues, not just λ_max. This makes it harder to prove but more powerful. The Kostant-Schur-Horn machinery does not automatically deliver it.

### 1.2 Matrix Domination: A Stronger Form of Majorization

A stronger condition than majorization: if **H(I) - H(Q) ≥ 0** as a matrix (positive semidefinite for all Q), then λ_max(H(Q)) ≤ λ_max(H(I)) follows immediately (from Weyl's interlacing inequalities). This is "matrix domination" and it is the cleanest possible path.

Matrix domination would follow from the D + C decomposition of H(Q) if one could show that H(I) - H(Q) = (D(I) - D(Q)) + (C(I) - C(Q)) is always PSD. The plaquette "destructive interference" (SZZ bound is 12-170x loose) suggests that at Q=I the plaquette contributions constructively reinforce, while away from I they compete. Whether this produces a global PSD domination requires direct verification.

**Connection to Survey 2 (Morse theory):** If matrix domination holds, the critical point structure of λ_max(H(Q)) is trivially resolved — Q=I achieves the maximum and all other Q have strictly lower λ_max (assuming the inequality is strict). Morse theory becomes unnecessary. Matrix domination is a "shortcut" that makes Morse theory redundant.

### 1.3 The 2024 Unitary Result and Local Second-Variation Analysis

Survey 1 identified arXiv:2408.16906: along geodesic paths u(t) = e^{itx}e^{iy} with ‖u(t)-I‖ < √2, the sum of top m eigenvalue phases is **convex** in t. The proof technique is a second-variation formula:

  d²/dt² ∑_{k≤m} θ_k(t) = 2 ∑_{k≤m, j>m} [sin(θ_k - θ_j) / |e^{iθ_k} - e^{iθ_j}|²] |⟨xv_k, v_j⟩|²

Survey 2 independently confirmed that local second-variation analysis at Q=I is one of the most tractable approaches for establishing local concavity.

**Connection:** The 2024 paper's technique is the **same class of argument** as what's needed for local concavity of λ_max(H(Q(t))) at Q=I. The difference is:
- 2024 paper: second variation of θ_k(u(t)) → POSITIVE → eigenvalue phase CONVEXITY of group element near identity
- Our problem: second variation of λ_max(H(Q(t))) → NEGATIVE at Q=I (numerically confirmed) → CONCAVITY of H's eigenvalue near flat connection

The proof structure is parallel. The 2024 formula is for the group element's own eigenvalues; our problem concerns a derived matrix H(Q). But the analytic technique (write the second variation as a sum of explicitly-signed terms) is directly adaptable.

**Important:** This is a **local** argument only — it establishes local concavity at Q=I within a geodesic ball. To go from local to global, one still needs one of the topological frameworks from Survey 2.

### 1.4 Perfect Morse Theory ↔ Gauge Symmetry ↔ Atiyah-Bott

Survey 2 identified perfect Morse theory (5 stars) as the highest-promise framework. The connection to Survey 1 comes through the gauge symmetry argument:

**Survey 2 finding:** Atiyah-Bott (1983) and Kirwan (1984) showed the Yang-Mills functional on Riemann surfaces is equivariantly perfect — the equivariant Morse polynomial equals the equivariant Poincaré polynomial. The flat connection is the unique equivariant top critical point.

**Connection to Survey 1 (Kostant/AGS):** The AGS theorem (moment map convexity) is a CONSEQUENCE of equivariant Morse theory in the Hamiltonian setting. Both are "equivariant" results. The lattice analog of Atiyah-Bott would use equivariant localization/Morse theory with the gauge group G_gauge ≅ SU(N)^V acting on SU(N)^E.

**The specific mechanism:** For SU(2)^E ≅ (S³)^E, the Poincaré polynomial is (1+t³)^E with b_{3E} = 1. A perfect Morse function has c_{3E} = 1 (unique top critical point). Q=I has Morse index 3E (negative-definite Hessian in all directions, confirmed numerically). If perfectness can be proved, uniqueness of the global max follows directly.

**Why Kostant helps:** The gauge symmetry acts on the critical set. If critical points NOT at Q=I always have some gauge-orbit symmetry (i.e., they come in continuous families), they cannot be Morse-non-degenerate — they would be Morse-Bott critical manifolds, not isolated points. This constrains the structure of non-flat critical points and makes the perfect Morse condition more tractable.

### 1.5 Trap-Free Landscape (Survey 2) and Differential dH (Cross-Survey)

Survey 2 identified the Rabitz-Russell trap-free result as the second-highest-promise approach. The key condition is transversality: the differential dH: T_Q(SU(N)^E) → T(Herm(N)) must be "generically surjective" (full rank at non-maximal critical points).

**Connection to Survey 1 plaquette structure:** The differential dH[ξ] = Σ_P dH_P[ξ_P] is a sum over plaquettes. Each H_P depends on the four edges of plaquette P. The question of whether dH is surjective is directly computable from the plaquette geometry.

For a d-dimensional lattice with N×N link variables:
- Tangent space at Q: dimension = dim(SU(N)) × E = (N²-1) × E
- Target space: dim(Herm(N,ℂ)) = N² (or the relevant N×N block space for the Hessian)
- For N=2, d=4: dim(su(2)) = 3, so for E ≥ N²/(N²-1) edges, the count allows surjectivity

The trap-free result is GENERIC (holds for almost all problems satisfying the transversality condition). Whether lattice Yang-Mills specifically satisfies it requires an explicit rank computation — but the lattice structure (multiple plaquettes, each contributing to dH) makes surjectivity plausible.

---

## Section 2: Ranked Assessment of Proof Strategies

### Approach 1: Direct Matrix Domination H(I) ≥ H(Q)
**Question:** Is H(I) - H(Q) ≥ 0 (PSD) for all Q ∈ SU(N)^E?

| Dimension | Assessment |
|-----------|------------|
| **Feasibility** | Easy (numerical verification in ~20 lines) / Hard (analytical proof) |
| **Decisiveness** | YES — if H(I) ≥ H(Q) everywhere, λ_max(H(Q)) ≤ λ_max(H(I)) directly |
| **Verifiability** | YES — numerical check of H(I) - H(Q) for random Q is immediate |
| **Novelty** | Novel — no prior application of matrix domination to lattice Hessians found |

**Overall: ★★★★★** (conditional — check numerically first)

**Strongest approach if true.** The "destructive interference" of plaquette contributions (SZZ bound is 12-170x loose) is circumstantial evidence that H(I) may dominate H(Q). If the diagonal term D satisfies D(I) ≥ D(Q) and the cross term C doesn't compensate, matrix domination holds.

**Failure mode:** H(Q) - H(I) has positive eigenvalues for some Q. This would be detected immediately by a numerical check. Most likely to fail for Q near the "antipodal" configuration (plaquette holonomies near -I).

---

### Approach 2: Direct Majorization λ(H(Q)) ≺ λ(H(I))
**Question:** Are the eigenvalues of H(Q) always majorized by those of H(I)?

| Dimension | Assessment |
|-----------|------------|
| **Feasibility** | Easy (numerical) / Hard (analytical) |
| **Decisiveness** | YES — majorization gives λ_max(H(Q)) ≤ λ_max(H(I)) directly |
| **Verifiability** | YES — compute eigenvalues of H(Q) for random Q and check |
| **Novelty** | Novel — no prior application found |

**Overall: ★★★★★** (conditional — check numerically first)

Strictly weaker than matrix domination (H(I) ≥ H(Q) implies majorization, but not vice versa), so if matrix domination fails, majorization might still hold. The Kostant/Schur-Horn connection shows majorization IS the "right" framework if any classical result applies.

**Failure mode:** For some Q, the sorted eigenvalue vector (λ₁(H(Q)), ..., λₙ(H(Q))) violates majorization against (λ₁(H(I)), ..., λₙ(H(I))). Need to check all partial sums Σ_{k=1}^m λ_k(H(Q)) ≤ Σ_{k=1}^m λ_k(H(I)).

---

### Approach 3: Perfect Morse Theory + Gauge Symmetry (Kirwan-type)
**Question:** Is λ_max(H(Q)) a perfect Morse function on SU(N)^E? Does gauge symmetry force c_{top} = 1?

| Dimension | Assessment |
|-----------|------------|
| **Feasibility** | Hard — requires adapting Atiyah-Bott/Kirwan to finite-dimensional lattice setting |
| **Decisiveness** | YES — unique top-index critical point = global max |
| **Verifiability** | YES — numerical gradient ascent survey gives strong evidence; rank of Hessian at all critical points confirms non-degeneracy |
| **Novelty** | Novel — no lattice Yang-Mills analog of Atiyah-Bott found in literature |

**Overall: ★★★★** (high theoretical value)

**The argument structure:**
- On SU(2)^E ≅ (S³)^E, b_{3E} = 1 (unique top Betti number)
- A perfect Morse function has c_{3E} = b_{3E} = 1 → unique local max = global max
- Q=I has Morse index 3E (numerically confirmed: Hessian is negative-definite)
- The gauge group G_gauge = SU(2)^V acts on SU(2)^E. Any critical point comes with its entire gauge orbit.
- If a non-flat critical point has a continuous gauge orbit (i.e., non-isolated), it's Morse-Bott degenerate, not Morse — which supports the Morse condition for non-flat critical points being saddles, not local maxima.
- If the gauge orbit of every non-flat critical point is trivial (discrete), we need to count them separately — but the equivariant argument would classify them.

**Failure mode:** A non-flat Q is a non-degenerate critical point with Morse index 3E (top index). This would mean the function has two local maxima, each isolated, which is consistent with the Morse inequalities (requires compensating saddle points). The early indicator is gradient ascent from 1000 random starts: if it ALWAYS converges to Q=I, this rules out competing local maxima.

---

### Approach 4: Trap-Free Landscape via Transversality (Rabitz-type)
**Question:** Is the differential d(λ_max ∘ H) generically surjective at non-maximal critical points?

| Dimension | Assessment |
|-----------|------------|
| **Feasibility** | Moderate — requires implementing dH and checking rank at critical points |
| **Decisiveness** | YES for generic problems; in particular case requires rank verification |
| **Verifiability** | YES — rank of dH at any non-flat critical points is directly computable |
| **Novelty** | Novel — no application of Rabitz trap-free results to lattice Yang-Mills |

**Overall: ★★★★**

**The mechanism:** Russell-Rabitz (2016) proved that for almost all quantum control problems, the landscape has no local traps (every non-global stationary point is a saddle). The key condition is parametric transversality: the map Q ↦ λ_max(H(Q)) should be transverse to critical values generically.

For lattice Yang-Mills, the plaquette structure means dH involves contributions from multiple edges per plaquette. If the combined dH at a non-flat critical point is full-rank, that critical point cannot be a local maximum (it would have directions of ascent).

**Failure mode:** A non-flat critical point Q* has rank(dH at Q*) < dim(Herm(N)) — the differential degenerates. This might happen at configurations with special symmetry (e.g., configurations where all plaquettes are identical or have special angles). Early indicator: check rank of dH numerically at any critical points found by gradient ascent.

---

### Approach 5: Local Concavity via Second-Variation Analysis at Q=I
**Question:** Can we rigorously prove d²λ_max(H(Q(t)))/dt²|_{t=0} < 0 for all geodesics Q(t) through I?

| Dimension | Assessment |
|-----------|------------|
| **Feasibility** | Moderate — requires computing the full second variation formula explicitly |
| **Decisiveness** | PARTIAL — local proof only; need a separate local-to-global argument |
| **Verifiability** | YES — computable from the Hessian decomposition H = D + C |
| **Novelty** | Standard technique (second-variation), Novel application |

**Overall: ★★★** (necessary supporting result, not sufficient alone)

This is the technique borrowed from arXiv:2408.16906. The second variation formula for a non-degenerate eigenvalue λ_max with eigenvector v along a geodesic Q(t) = exp(tξ)·I is:

  d²λ_max/dt²|_{t=0} = v†(d²H/dt²)v + 2 Σ_{k≠max} |v†(dH/dt)w_k|² / (λ_max - λ_k)

At Q=I, the Hessian has been computed analytically: H_norm(I) = 1/12 for d=4, N=2. The formula for d²H/dt² involves second derivatives of plaquette traces. The second term (sum over k) is always negative (λ_max > λ_k for other eigenvalues, and the sum has negative signs). The sign of d²λ_max/dt²|_{t=0} depends on whether v†(d²H/dt²)v is negative enough to dominate.

**Failure mode:** v†(d²H/dt²)v is positive and large enough to make the total second variation positive — meaning Q=I is locally a minimum of λ_max along some geodesic. Numerics confirm Q=I is a local max, so this would be a contradiction — failure here would indicate a computational error.

---

### Approach 6: Łojasiewicz + Uniqueness (Flow Convergence)
**Question:** Can Łojasiewicz + uniqueness of critical structure give global convergence?

| Dimension | Assessment |
|-----------|------------|
| **Feasibility** | Hard — Łojasiewicz is automatic; uniqueness requires one of the above approaches |
| **Decisiveness** | PARTIAL — gives convergence rate, not global max alone |
| **Verifiability** | NO independent test |
| **Novelty** | Standard |

**Overall: ★★★** (supporting result; depends on the main approaches above)

Łojasiewicz holds automatically on compact analytic manifolds like SU(N)^E. Combined with uniqueness of local maxima (from Morse or trap-free arguments), it gives: every gradient ascent trajectory converges to Q=I at a rate |f(Q(t)) - f(I)|^{1-θ} ≤ C/t. This is a complementary convergence result, not an independent proof of global optimality.

---

### Approach 7: Double Bracket Reformulation
**Question:** Can λ_max(H(Q)) be reformulated as a trace optimization, enabling Brockett-type double bracket flow?

| Dimension | Assessment |
|-----------|------------|
| **Feasibility** | Hard — reformulation requires novel extension of double bracket theory to λ_max |
| **Decisiveness** | PARTIAL — works cleanly only for trace functions |
| **Verifiability** | NO |
| **Novelty** | Moderate |

**Overall: ★★** (theoretically interesting but low priority)

The variational characterization λ_max(H(Q)) = max_{‖v‖=1} v†H(Q)v = max_P Tr(P·H(Q)) (where P ranges over rank-1 projectors) converts the problem to a joint optimization over (Q, P) ∈ SU(N)^E × ℂP^{N-1}. On the joint space, one could attempt a double bracket flow. However, this reformulation adds a new variable P and the joint optimization landscape is more complex. This approach is lowest priority.

---

### Approach 8: SDP Certificate (Numerical)
**Question:** Does a numerical SDP dual certificate confirm global optimality of Q=I?

| Dimension | Assessment |
|-----------|------------|
| **Feasibility** | Easy — standard SDP solver |
| **Decisiveness** | NO — numerical, not analytic |
| **Verifiability** | YES |
| **Novelty** | Standard |

**Overall: ★★** (useful for numerical confidence only)

---

## Section 3: Full Ranking Summary Table

| Rank | Approach | Feasibility | Decisiveness | Verifiability | Novelty | Overall |
|------|----------|-------------|--------------|---------------|---------|---------|
| 1 | **Matrix domination H(I) ≥ H(Q)** | Easy (num) / Hard (anal) | Yes | Yes | Novel | ★★★★★ |
| 2 | **Direct majorization λ(H(Q)) ≺ λ(H(I))** | Easy (num) / Hard (anal) | Yes | Yes | Novel | ★★★★★ |
| 3 | **Perfect Morse + gauge symmetry (Kirwan-type)** | Hard | Yes | Yes (num) | Novel | ★★★★ |
| 4 | **Trap-free (Rabitz transversality)** | Moderate | Yes (generic) | Yes | Novel | ★★★★ |
| 5 | **Local second-variation at Q=I** | Moderate | Partial | Yes | Standard | ★★★ |
| 6 | **Łojasiewicz + uniqueness** | Hard | Partial | No | Standard | ★★★ |
| 7 | **Double bracket reformulation** | Hard | Partial | No | Moderate | ★★ |
| 8 | **SDP certificate** | Easy | No | Yes | Standard | ★★ |

---

## Section 4: The Critical Path

**Recommended sequence: two parallel tracks, converging at Step 3.**

### Track A: Direct Computational Attack (Fastest to Decision)

**Step A1 (1-2 days): Numerical matrix domination test**

For ~1000 random Q ∈ SU(2)^E (E = 4 for a 2×2 lattice with periodic BC), compute H(Q) and H(I). Check:
1. Is H(I) - H(Q) ≥ 0 (all eigenvalues of the difference ≥ 0)?
2. If not, is λ(H(Q)) ≺ λ(H(I)) (majorization: Σ_{k=1}^m λ_k(H(Q)) ≤ Σ_{k=1}^m λ_k(H(I)) for all m)?

Inputs needed: The explicit formula for H(Q) from the Yang-Mills Hessian work (D+C decomposition). The flat connection value H(I) = (1/12) × I_{relevant block} for d=4, N=2.

**Expected value:** HIGH. If matrix domination holds, this is essentially a proof sketch — the analytical proof would follow by showing H(I) - H(Q) = (sum of PSD contributions) for all Q. If majorization holds without full PSD domination, we have a weaker but still direct proof path.

**If Track A1 succeeds:** Move directly to analytical proof of matrix domination or majorization using the Hessian formula. The D + C decomposition of H should make this tractable.

**If Track A1 fails:** Matrix domination and majorization are dead. Move to Track B.

---

### Track B: Topological/Structural Attack (Higher Effort, Guaranteed Path If Correct)

**Step B1 (parallel with A1): Gradient ascent landscape survey**

Run 1000 gradient ascent trajectories from random initializations on SU(2)^E (small E = 2, 4, 8). Record:
1. All critical points found (by watching for ‖∇f‖ → 0)
2. The value of λ_max at each critical point
3. Whether all trajectories converge to Q=I

If ALL trajectories converge to Q=I: strong evidence for perfect Morse (unique top critical point). Proceed to Step B2.

If some trajectories converge elsewhere: record those critical points. Check whether they are saddle points (by computing Hessian index). If they have index < 3E, they are saddles and not competing maxima — still consistent with Q=I being the unique global max.

**Step B2 (if B1 finds no competing maxima): Trap-free rank verification**

At any critical points found by B1, compute rank(dH). If full rank everywhere, the Rabitz transversality condition is numerically satisfied — the landscape is trap-free. This gives: every stationary point that is not a global maximum must be a saddle. Combined with the confirmed global max at Q=I, this closes the argument.

**Step B3 (analytical): Equivariant Morse theory**

If numerical evidence strongly supports uniqueness of maximum (Tracks A and B both indicate no competing maxima), proceed to analytical proof via one of:
- Kirwan-type equivariant Morse theory: prove f = λ_max(H(Q)) is G_gauge-equivariantly perfect on SU(N)^E
- Analytical Rabitz transversality: show rank(dH) = dim(Herm(N)) at all non-flat critical points, using the plaquette structure

---

### Recommended Sequence

```
Step 1: Numerical matrix domination + majorization test (1-2 days)
        ↓
   [If HOLDS]: Sketch analytical proof via H = D + C decomposition (DONE)
   [If FAILS]: Move to Step 2
        ↓
Step 2: Gradient ascent landscape survey — find all local maxima (1-2 days)
        ↓
   [If Q=I is the only maximum found]: Move to Step 3
   [If other maxima found]: Check Morse index — are they saddles? If yes, still OK.
        ↓
Step 3: Rank verification of dH at non-flat critical points (1 day)
        ↓
   [If full rank]: Rabitz trap-free applies → Q=I is unique global max (DONE numerically)
   [If rank deficient]: Move to equivariant Morse theory (Week-level effort)
        ↓
Step 4: Kirwan-type equivariant Morse argument (1-2 weeks)
```

Expected outcome: The problem is resolved at Step 1 or Step 3. Steps 2 and 4 are fallbacks.

---

## Section 5: Failure Mode Analysis — Top Two Approaches

### Top Approach: Matrix Domination H(I) ≥ H(Q)

**Most likely failure mode:** The Hessian at non-flat Q has eigenvalues that EXCEED λ_max(H(I)) = 1/12 for some direction.

**Mechanism:** Away from flat connection, some plaquettes may have holonomy near -I (anti-aligned). In this case, the diagonal self-term D(Q) could generate large positive contributions that are not cancelled by the cross-term C(Q). Physically, this corresponds to a configuration with a highly curved plaquette where the quantum fluctuation energy is concentrated.

**How to detect early:** Check H(Q) for Q where one plaquette holonomy is exactly -I (the "most anti-flat" configuration). This is the extremal case. If H(I) ≥ H(Q) fails anywhere, it fails here.

**What to do if it fails:** Matrix domination is dead. Move to majorization: even if the maximum eigenvalue of H(Q) exceeds λ_max(H(I)) for some Q, it might still be the case that the GLOBAL maximum of λ_max(H(Q)) is achieved at Q=I by the overall landscape structure. But this would require a different proof.

**Secondary failure mode:** H(I) ≥ H(Q) holds for all Q but the margin is extremely small, making the analytical proof via D + C decomposition difficult. This is a proof-difficulty failure, not a mathematical failure of the approach.

---

### Second Approach: Perfect Morse + Gauge Symmetry

**Most likely failure mode:** A non-flat critical point Q* of λ_max(H(Q)) exists with Morse index 3E (top index), meaning it is a competing local maximum.

**Mechanism:** On SU(N)^E, there can be "gauge-inequivalent" configurations with special symmetry that also give locally maximal λ_max. For example, configurations where all plaquettes have holonomy e^{iπ} = -I might create a "second flat connection" in a twisted gauge sense.

**How to detect early:**
1. Run gradient ascent from 100-1000 random initializations. If a trajectory converges to a point Q* ≠ I (or its gauge orbit), record Q*.
2. At Q*, compute the full Hessian and its eigenvalues. If the Hessian is negative-definite, Q* is a second local max — and the Morse approach needs more care.
3. Check the value λ_max(H(Q*)). If it equals λ_max(H(I)), the function has two equal global maxima (consistent with a symmetry). If it's less than λ_max(H(I)), Q* is a local-but-not-global max.

**What to do if a second local max exists:**
- If λ_max(H(Q*)) = λ_max(H(I)): The two maxima are related by a gauge symmetry (they should be gauge-equivalent). The statement "global max is at flat connections" is still true; it's just that Q* is also flat (gauge-equivalent to I). The statement needs to be rephrased as: "global max is achieved at and only at flat connections."
- If λ_max(H(Q*)) < λ_max(H(I)): Q* is a local-but-not-global max, and the Morse approach must account for it. The Kirwan equivariant argument would need to exclude this case, which is harder but not impossible.

**Secondary failure mode:** The function λ_max(H(Q)) is NOT a Morse function (some critical points are degenerate). This would happen if H(Q) has a repeated maximum eigenvalue at a non-flat Q, making the eigenvalue function non-smooth and the Morse condition fail. How to detect: check whether the Hessian of f at any critical point Q* has zero eigenvalues (degenerate critical point).

---

## Section 6: Connections Summary

### Does Majorization Connect to Morse Theory?

**Honest assessment:** Majorization and Morse theory are **alternative, independent proof paths**, not connected ones.

- Majorization gives λ_max directly (no critical point theory needed). If it holds, Morse theory is not necessary.
- Morse theory gives global uniqueness via topology. If majorization fails, Morse theory is the fallback.
- The Kostant-Schur-Horn theorem provides the LANGUAGE of majorization (eigenvalue ordering via orbit projections) but does NOT deliver global majorization for our specific H(Q) — it only covers the gauge orbit of I.

**Where they do connect:** If matrix domination holds (H(I) ≥ H(Q) as matrices), then automatically every local max of λ_max(H(Q)) must be at a point where λ_max(H(Q)) = λ_max(H(I)) — which requires H(Q) to achieve equality in the PSD domination. This means the Hessian of the matrix difference is zero at the max, providing constraints that can be used to identify all maxima. So matrix domination effectively replaces both majorization AND Morse theory by directly characterizing the maximizers.

### Does the 2024 Unitary Proof Technique Connect to the Topological Frameworks?

**Yes, as a "bridge" argument.** The 2024 technique (second-variation formula for eigenvalue sums along geodesics) can prove LOCAL concavity of λ_max(H(Q)) within a geodesic ball around Q=I. Within the convexity radius of SU(2)^E (approximately π√2/2 per factor), the function would be geodesically concave. Any local max within this ball is the unique local max in the ball — and since the ball is geodesically convex, it's also the local-to-global statement for that region.

**The bridge:** Local concavity (from 2024 technique) + absence of any maxima OUTSIDE the ball (from Morse/trap-free survey of the full landscape) would give global uniqueness. This is a "two-piece" argument that uses both survey's findings.

Practically: the convexity radius (~π√2/2 ≈ 2.22 in SU(2)) covers roughly half the diameter of each SU(2) factor. Gradient ascent from a random initialization often starts within this ball. So the "local concavity ball" is large enough to be practically useful.

---

## Section 7: Ranking Justification and Expected Value

**Why Approach 1 (matrix domination) is first:**

1. If H(I) ≥ H(Q) everywhere, the proof is two lines: "by PSD domination, λ_max(H(Q)) ≤ λ_max(H(I)) = 1/12." No topology, no critical point theory, no Morse conditions needed.
2. The plaquette "destructive interference" phenomenon (SZZ bound is 12-170x loose) suggests that at Q=I, contributions from different plaquettes constructively interfere to produce the maximum eigenvalue, while away from I they destructively interfere. Matrix domination is the algebraic statement of this physical intuition.
3. The numerical check is trivial: compute H(I) - H(Q) for 1000 random Q. If all eigenvalues are ≥ 0: verified. If any are < 0: falsified.
4. The analytical proof, if matrix domination holds numerically, would use the explicit D + C decomposition plus properties of SU(2) representations. This is a tractable algebraic computation, not a new theory.

**Why Approach 3 (perfect Morse) is ranked highly despite difficulty:**

1. Even if matrix domination fails, perfect Morse theory provides a clean topological proof that requires NO special structure of H — only the topology of SU(2)^E and the fact that Q=I is a non-degenerate top-index critical point.
2. The Atiyah-Bott precedent makes it mathematically plausible — the lattice is a finite-dimensional version of the gauge theory they studied.
3. Numerical evidence (gradient ascent always converging to Q=I) can be collected in parallel with Track A, at low additional cost.

**Why Approach 4 (trap-free) is close to Approach 3:**

The trap-free approach has the advantage of being directly checkable: compute rank(dH) at critical points. If it's full rank, the result is essentially proven (modulo the generic condition). Approach 3 requires an analytic proof of perfectness, which is harder. Approach 4 may be easier to execute even if it requires more computation.

---

## Section 8: What This Synthesis Adds (Beyond Listing Approaches)

### New Insight 1: Matrix Domination as a Previously Unnamed Priority

Neither prior survey explicitly identified "direct matrix domination H(I) ≥ H(Q)" as a distinct approach. Survey 1 mentioned majorization; Survey 2 focused on topology. The connection between the plaquette destructive interference and PSD domination is a new synthesis insight.

**Why this matters:** Matrix domination is STRONGER than all topological arguments combined. It directly gives the bound on λ_max without any critical point theory, Morse conditions, or gauge group arguments. If it holds, it is by far the simplest proof.

### New Insight 2: Kostant/Schur-Horn is a Dead End for Global Majorization

The apparent connection "Kostant theorem → majorization → global bound" breaks down because H(Q) is NOT a unitary conjugate of H(I) for non-gauge-equivalent Q. Kostant/Schur-Horn only applies within the gauge orbit of I. This clarifies a potential confusion in the prior surveys.

### New Insight 3: The 2024 Unitary Technique is a Local Bridge, Not a Global Solution

The 2024 paper's second-variation technique can establish local concavity at Q=I (within the geodesic convexity ball), but not global. This makes it a supporting result that, combined with a landscape survey, could give the full argument.

### New Insight 4: Two Independent Proof Tracks Converge

The direct approach (matrix domination/majorization) and the topological approach (Morse/trap-free) are independent. If either succeeds, the problem is solved. Running both in parallel maximizes the probability of finding a proof quickly.

---

## Section 9: Summary Recommendations

### What to Try First

1. **Immediately:** Numerical matrix domination test. This takes 1-2 days and either solves the problem or closes this path decisively.

2. **In parallel:** Gradient ascent landscape survey on SU(2)^E. This takes 1-2 days and either confirms perfect Morse structure or finds competing maxima that need analysis.

3. **If Step 1 succeeds:** Work out the analytical proof using D + C decomposition. Expected effort: 1-2 weeks.

4. **If Step 1 fails, Step 2 gives clean result:** Verify Rabitz transversality (rank of dH) at all critical points found. Expected effort: 1-3 days.

5. **If all numerical checks support uniqueness but Step 1 fails:** Attempt Kirwan-type equivariant Morse theory with gauge symmetry. Expected effort: 2-4 weeks. This is the hardest path but remains a valid proof strategy with solid precedent.

### What to NOT Try First

- SDP certificate: numerical only, not a proof.
- Double bracket reformulation: too indirect.
- Łojasiewicz alone: gives convergence but not global max certification.
- Global geodesic concavity: impossible by theorem (compact manifold, harmonic functions must be constant).

---

## References

**From Survey 1 (Classical Matrix Analysis):**
- C. Davis (1957): Convex invariant functions on Hermitian matrices
- A.S. Lewis (1996): Spectral functions on H_n
- T. Ando (1979): Concavity on positive definite matrices
- B. Kostant (1973): Orbit projection convexity (Schur-Horn generalization)
- Atiyah-Guillemin-Sternberg (1982): Moment map convexity
- arXiv:2408.16906 (2024): Convexity of eigenvalue sums of unitary segments near identity

**From Survey 2 (Riemannian/Topological Frameworks):**
- Russell, Rabitz (2016): arXiv:1608.06198 — trap-free quantum control landscapes
- arXiv:2409.15139 (2024): Path-connectedness of globally optimal set
- M.F. Atiyah, R. Bott (1983): Yang-Mills equivariant Morse theory on surfaces
- F. Kirwan (1984): Cohomology of quotients and equivariant perfectness
- Bloch, Brockett, Ratiu (1992): Double bracket flows (CMP 147:57)
- Milnor, Bott: Standard Morse theory references

**Problem-Specific:**
- SZZ (Shen-Zhu-Zhu) Lemma 4.1: Hessian eigenvalue bound (12-170x loose)
- Weitzenbock formula: H = D + C decomposition of Yang-Mills Hessian
- H_norm(I) = 1/12 for d=4, N=2 (proved via Fourier block-diagonalization)
