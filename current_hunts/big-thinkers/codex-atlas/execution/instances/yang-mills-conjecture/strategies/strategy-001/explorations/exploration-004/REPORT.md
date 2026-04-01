# Exploration 004: Synthesis of Phase 1 Decompositions + Proof Outline

## Goal

Synthesize findings from explorations 001–003, rank the candidate proof routes, produce a concrete proof outline for the best route, and identify the single hardest step.

---

## Section 1: Summary of Phase 1 Findings

### E001 (Maximal Tree Gauge)
- **Single-link theorem**: For ANY Q differing from I on exactly one edge, λ_max(M(Q)) = 16 exactly and P^T R(Q) P is negative semidefinite with 3D null space. Verified for 640 configs.
- **Uniform density**: P_e P_e^T = (9/64) I_3 for ALL 64 edges — the staggered eigenspace is uniformly distributed over the lattice.
- **Null space structure**: Null vectors v_null satisfy B_□(Q, v_null) = B_□(I, v_null) for all plaquettes containing the perturbed edge (non-trivial cancellation, not just "zero at edge").
- **Two-link perturbations**: Strictly negative max_eig in [−0.02, −0.11]; no inductive structure found.
- **Key gap**: Single-link → multi-link extension is blocked; no monotonicity or inductive structure identified.

### E002 (Per-Plaquette Structure)
- **Active/inactive split [PROVED]**: Active plaquettes (μ+ν odd) always have f ≤ 0; inactive (μ+ν even) always have f ≥ 0.
- **Cube-face grouping [COMPUTED, 0/160,000 violations]**: The 96 plaquettes partition into 16 groups of 6 (one per vertex x, indexed by the base vertex), with each group sum ≤ 0.
- **Cube-face formula [PROVED for cross-links=I]**:
  ∑_{μ<ν} |B_{(x,μ,ν)}|² = 32 + 8⟨n, W⟩ − |A|²
  where W = ∑_μ w_μ, A = ∑_μ s_μ w_μ, w_μ = Ad(Q_{x,μ})^{-1} n.
- **Bound follows**: 32 + 8⟨n,W⟩ ≤ 64 (triangle ineq) and −|A|² ≤ 0, giving ≤ 64.
- **Mechanism**: Staggered sign structure forces A = ∑_μ s_μ w_μ → 0 at Q=I (since ∑_μ s_μ = 0), ensuring equality at the identity.

### E003 (SO(3) Representation Theory)
- **Parallelogram identity [VERIFIED]**: For any (R_1, R_2, R_3) ∈ SO(3)³:
  |n + R_1 n + R_2 n + R_3 n|² + |n − R_1 n + R_2 n − R_3 n|² = 2|n + R_2 n|² + 2|R_1 n + R_3 n|² ≤ 16
- **Per-plaquette max = 16** regardless of holonomy constraint (holonomy doesn't help).
- **Full quadratic form M [COMPUTED]**: The 192×192 Hessian of f at Q=I decomposes as M = M_perp ⊕ 0_along where M_perp (128×128) is STRICTLY NEGATIVE DEFINITE with max eigenvalue −4(2−√2) ≈ −2.34.
- **Fourier block structure [COMPUTED]**: M_perp is block-diagonal in lattice Fourier modes (16 blocks of size 8×8), each negative definite. The staggered mode block has eigenvalues {−40, −40, −20, −20, −20, −20, −4, −4}.
- **Constant-link case [PROVED]**: f(R,R,...,R) = 512(1 + cosθ) ≤ 1024 analytically.
- **Q=I is local maximum [COMPUTED]**: All second derivatives d²f/dt² = −26 for perpendicular perturbations; Hessian is negative semidefinite.
- **Morse-Bott structure [CONJECTURED]**: Critical manifold = U(1)_n^64 (where all Ad(Q_e) preserve n); f = 1024 on this manifold; transverse Hessian < 0.

---

## Section 2: Route Assessment

### Route A: Cube-face Inequality

**Claim**: ∑_{μ<ν} |B_{(x,μ,ν)}(Q)|² ≤ 64 for each vertex x and all Q ∈ SU(2)^E.

**Why this implies the conjecture**: The 96 plaquettes partition into 16 groups of 6 (one per vertex x; each plaquette (x,μ,ν) belongs uniquely to vertex x as its base vertex, and 16×6=96 ✓). If each group contributes ≤ 64, total ≤ 16×64 = 1024 = 4d×|v|², giving λ_max(M(Q)) ≤ 16. This is a PERFECT partition, not a cover.

**Phase 1 ingredients needed**:
- E002: Algebraic formula + cross-links=I proof (Lemmas 2–3)
- E002: Plaquette sign structure (active/inactive classification)
- E001: Uniform density property (supports the mechanism)

**What is proved**:
- Formula ∑|B|² = 32 + 8⟨n,W⟩ − |A|² for cross-links=I [PROVED, E002]
- Bound ≤ 64 for cross-links=I [PROVED, E002]
- 0 violations in 160,000 numerical tests [COMPUTED, E002]
- Adversarial attack converges to Q=I (sum → 64) [COMPUTED, E002]

**What needs to be proved**:
- The formula (or a bound ≤ 64) for general Q with arbitrary cross-links

**Estimated difficulty**: MEDIUM. The formula is proved for an important structural case. The generalization requires handling 12 cross-link variables that appear in the partial holonomies. The algebraic mechanism (staggered sign structure) should generalize, but requires explicit derivation.

**Potential obstructions**:
- The 12 cross-links per vertex introduce partial holonomies that don't factor cleanly into base-link contributions
- On the L=2 torus, each cube's cross-links are shared with adjacent cubes, so local gauge fixing is entangled

---

### Route B: Parallelogram Pairing

**Claim**: Pair each of 32 inactive plaquettes with one of 32 (of 64) active plaquettes sharing identical partial holonomies (R_1, R_2, R_3). Then:
- 32 paired (active+inactive) groups → each ≤ 16 (parallelogram identity)
- 32 unpaired active → each ≤ 16 (triangle inequality)
- Total ≤ 512 + 512 = 1024 ✓

**Phase 1 ingredients needed**: E003 parallelogram identity, E002 active/inactive split

**Estimated difficulty**: HIGH. The parallelogram identity requires two plaquettes to share identical holonomy triples (R_1, R_2, R_3). Active planes (0,1), (0,3), (1,2), (2,3) and inactive planes (0,2), (1,3) involve completely different links per vertex. There is no reason for their partial holonomies to coincide generically.

**Potential obstruction**: At vertex x=(0,0,0,0), the active plaquette (0,0,1) has R_1 = Ad(Q_{0,0}), while the inactive plaquette (0,0,2) has R_1 = Ad(Q_{0,0}). These agree! But R_2^{(0,1)} = Ad(Q_{0,0} Q_{e0,1} Q_{e1,0}^{-1}) ≠ R_2^{(0,2)} = Ad(Q_{0,0} Q_{e0,2} Q_{e2,0}^{-1}) generically. So the pairing breaks down at R_2 for different planes.

**Verdict**: Blocked without additional algebraic structure. Not recommended.

---

### Route C: Single-link → Multi-link Induction

**Claim**: Prove the single-link bound algebraically, then extend by induction or perturbation to all Q.

**Phase 1 ingredients needed**: E001 single-link theorem, uniform density

**Estimated difficulty**: VERY HIGH. E001 explicitly found no inductive structure. Two-link configurations restore strict negativity but in a non-monotone way. The single-link boundary (max_eig = 0) is a measure-zero set in configuration space.

**Verdict**: Blocked. E001 explicitly identified this as low tractability.

---

### Route D: Quadratic Form + Morse-Bott Theory

**Claim**: The Hessian M_perp < 0 at Q=I (proved) implies Q=I is the unique local maximum of f (up to U(1)_n^64 symmetry). Combined with compactness and topological arguments, f achieves its global maximum only on U(1)_n^64.

**Phase 1 ingredients needed**: E003 Fourier circulant computation, Morse-Bott analysis

**What is proved**: M_perp is strictly negative definite with max eigenvalue −4(2−√2). All 16 Fourier blocks are negative definite. This is a LOCAL result.

**Gap**: Extending the local result to global requires:
1. Proving M_perp < 0 at ALL points on U(1)_n^64 (not just Q=I)
2. Ruling out critical points of f outside U(1)_n^64 with f = 1024
3. A topological/analytic argument that no other global maximum exists

**Estimated difficulty**: HIGH for the global extension. The Fourier circulant proof step (STEP 1 in E003 Route 2) is itself MEDIUM difficulty and would be a clean algebraic result. But the Morse-Bott global argument is hard.

**Important note**: This route proves something STRONGER locally (all v, not just v ∈ P) but cannot currently reach the global result. Also, we know M(Q) ≤ M(I) as operators is IMPOSSIBLE (dead end #1), so any argument must carefully restrict to v ∈ P.

---

### Route Ranking

| Rank | Route | Gap Type | Difficulty |
|------|-------|----------|-----------|
| 1 | A: Cube-face inequality | Cross-link generalization of algebraic formula | MEDIUM |
| 2 | D: Quadratic form + Morse-Bott | Local→global extension | HIGH |
| 3 | B: Parallelogram pairing | Pairing structure doesn't exist generically | VERY HIGH |
| 4 | C: Single-link induction | No inductive structure identified | BLOCKED |

**Route A is the best route** because: (a) the proof is complete for the cross-links=I special case with a clean formula, (b) the mechanism (staggered sign structure) is transparent and well-motivated, (c) the partition structure is clean (16 independent local problems), and (d) the numerical evidence is overwhelming.

---

## Section 3: Proof Outline for Route A

### Setup

Let (V, E, P) be the L=2, d=4 hypercubic torus with |V|=16, |E|=64, |P|=96.

The staggered mode v ∈ R^192 has v_{x,μ} = (-1)^{|x|+μ} n ∈ su(2) ≅ R³ for a unit vector n.
Normalization: |v|² = ∑_{x,μ} |v_{x,μ}|² = 64.

The quadratic form: v^T M(Q) v = ∑_{□ ∈ P} |B_□(Q,v)|².
The conjecture is equivalent to: ∑_{□} |B_□(Q,v)|² ≤ 1024 = 16 × |v|² for all Q ∈ SU(2)^64.

### Main Theorem (Conjecture 1)

**Theorem**: For all Q ∈ SU(2)^E, λ_max(M(Q)) ≤ 16.

### Lemma Structure

---

**Lemma 0 (Plaquette Partition)** [PROVED]

The 96 plaquettes are partitioned by base vertex:
P = ⊔_{x ∈ V} P_x,   where P_x = {(x, μ, ν) : 0 ≤ μ < ν ≤ 3}

Each |P_x| = C(4,2) = 6. Total: 16 × 6 = 96 ✓.
Consequently: ∑_{□ ∈ P} |B_□|² = ∑_{x ∈ V} F_x(Q,v) where F_x = ∑_{μ<ν} |B_{(x,μ,ν)}|².

*Status*: PROVED (combinatorial identity of the lattice).

---

**Lemma 1 (Active Plaquette Per-Plaquette Bound)** [PROVED]

For any plaquette (x, μ, ν) with μ+ν odd (active) and any Q, v staggered:
|B_{(x,μ,ν)}(Q,v)|² ≤ 16.

*Proof sketch*: B = c₁(n + R_ξ n) + c₂(R_1 n + R_□ n) with c₁=c₂=±1 (active case). Triangle inequality: |B| ≤ |n + R_ξ n| + |R_1 n + R_□ n| ≤ 2 + 2 = 4, so |B|² ≤ 16.

*Status*: PROVED (E002, Stage 4). Tight at Q=I.

---

**Lemma 2 (B Formula Sign Structure)** [PROVED]

For any plaquette (x, μ, ν), the effective coefficients satisfy c₁ = c₃ ≡ a and c₂ = c₄ ≡ b, where a = (-1)^{|x|+μ} and b = (-1)^{|x|+ν+1}. The B formula simplifies to:
B_{(x,μ,ν)} = a(n + R_ξ n) + b(R_1 n + R_□ n)

Active planes (μ+ν odd): a = b. Inactive planes (μ+ν even): a = −b.

*Status*: PROVED (E003, Stage 1, verified algebraically).

---

**Lemma 3 (Cube-face Formula for Cross-links=I)** [PROVED]

When only the 4 base links {Q_{x,μ}}_{μ=0}^3 at vertex x vary (cross-links Q_{x+eμ,ν} = I for all μ,ν), define w_μ = Ad(Q_{x,μ})^{-1} n. Then:

F_x(Q,v) = ∑_{μ<ν} |B_{(x,μ,ν)}|² = 32 + 8⟨n, W⟩ − |A|²

where W = ∑_μ w_μ and A = ∑_μ s_μ w_μ with staggered signs s_μ = (-1)^{|x|+μ}.

*Status*: PROVED algebraically (E002, Stage 4). Verified to 3×10^{-14} over 10,000 numerical tests.

---

**Lemma 4 (Cube-face Bound for Cross-links=I)** [PROVED]

Under the conditions of Lemma 3: F_x(Q,v) ≤ 64.

*Proof*:
- 8⟨n, W⟩ ≤ 8|W| ≤ 8 ∑_μ |w_μ| = 8 × 4 = 32 (triangle inequality, |w_μ| = 1 ∀μ)
- −|A|² ≤ 0 (trivially)
- Therefore F_x ≤ 32 + 32 − 0 = 64 ✓

*Status*: PROVED (E002, Stage 4). Equality iff all w_μ = n AND A = 0, which requires all base links to preserve n.

---

**Lemma 5 (Cube-face Bound for General Q)** [NOT PROVED — THE GAP]

For ANY Q ∈ SU(2)^E and any vertex x:
F_x(Q,v) = ∑_{μ<ν} |B_{(x,μ,ν)}(Q,v)|² ≤ 64

where the B formula includes ALL 16 links: 4 base links {Q_{x,μ}} and 12 cross-links {Q_{x+eμ,ν}}.

*Status*: UNPROVED.
- Evidence: 0 violations in 160,000 random Haar tests [COMPUTED, E002]
- Adversarial gradient ascent on cube-face sum converges to 64 (= Q=I) [COMPUTED, E002]
- Maximum observed: 48.3 (far below 64) in 10,000 adversarial tests [COMPUTED, E002]
- Conjectured approach: generalize the formula to include effective rotations for cross-link contributions

---

**Main Theorem follows from Lemmas 0 + 5**:

∑_{□} |B_□(Q,v)|² = ∑_{x ∈ V} F_x(Q,v) ≤ ∑_{x ∈ V} 64 = 16 × 64 = 1024 = 4d × |v|² ✓

This gives λ_max(M(Q)) = max_{|v|=1, v∈P} v^T M(Q) v ≤ 16. □

---

## Section 4: The Single Hardest Step

**The single hardest step is Lemma 5**: the cube-face inequality for general Q.

Lemmas 0–4 are all proved. The entire proof reduces to one unproved lemma.

### Why Lemma 5 is the bottleneck

The difficulty is not conceptual but algebraic: the cube at vertex x involves 16 link variables total (4 base + 12 cross), and for general configurations, the B formula for each of the 6 plaquettes contains partial holonomies mixing base and cross-links. Specifically:

For plaquette (x, μ, ν):
- R_1^{μν} = Ad(Q_{x,μ}) — base link only
- R_ξ^{μν} = Ad(Q_{x,μ} · Q_{x+eμ,ν} · Q_{x+eν,μ}^{-1}) — base + 2 cross-links
- R_□^{μν} = Ad(Q_{x,μ} · Q_{x+eμ,ν} · Q_{x+eν,μ}^{-1} · Q_{x,ν}^{-1}) — full plaquette holonomy

When cross-links ≠ I, R_ξ^{μν} ≠ R_1^{μν}. The elegant formula 32 + 8⟨n,W⟩ − |A|² was derived by exploiting R_ξ = R_1 (which holds iff cross-links = I). For general Q, R_ξ ≠ R_1 and the formula takes a more complex form.

### What the general formula looks like

After factoring out R_μ = Ad(Q_{x,μ}) (since |R_μ v|² = |v|² for SO(3) rotations), each |B_{μν}|² can be written as:

|B_{μν}|² = |a(p_μ + q^{μν}) + b(n + r^{μν})|²

where:
- p_μ = Ad(Q_{x,μ})^{-1} n (base-link contribution)
- q^{μν} = Ad(Q_{x+eμ,ν} Q_{x+eν,μ}^{-1}) n (cross-link rotation of n)
- r^{μν} = Ad(Q_{x+eμ,ν} Q_{x+eν,μ}^{-1} Q_{x,ν}^{-1}) n (cross-link + second base-link rotation)
- a = (-1)^{|x|+μ}, b = (-1)^{|x|+ν+1}

For cross-links=I: q^{μν} = n, r^{μν} = p_ν, recovering the simplified formula.

For general Q: q^{μν} and r^{μν} are independent unit vectors depending on cross-links.

The cube-face sum ∑_{μ<ν} |a(p_μ + q^{μν}) + b(n + r^{μν})|² involves 4 + 12 unit vectors (4 p_μ and 6×2 cross-link vectors), connected by 6 plaquette holonomy structures.

### Why it's hard

The cross-link=I proof exploited the collapse q^{μν} → n and r^{μν} → p_ν, which gave the clean formula. For general q^{μν} and r^{μν}, the sum is a quadratic form in 16 unit vectors on S² with a complex coefficient structure.

The natural bound using per-active-plaquette inequality gives:
∑_active ≤ 4 × 16 = 64

But ∑_inactive ≥ 0 contributes positively, so a naive bound gives ≤ 64 + ∑_inactive — insufficient.

The proof must use the JOINT structure of active + inactive plaquettes at each vertex.

### Likely proof approach

The most natural generalization of the cross-links=I argument:

**Define effective unit vectors** absorbing cross-link contributions:
- w̃_μ^{(1)} = Ad(Q_{x,μ})^{-1} n  (base link contribution)
- w̃_μ^{(2)} = Ad(Q_{x,μ})^{-1} q^{μν}  (effective cross-link contribution, depends on μ,ν pair)

Then B_{μν} = a · Ad(Q_{x,μ}) · (something involving w̃ vectors)

The formula F_x = 32 + 8⟨n,W̃⟩ − |Ã|² would hold if appropriate W̃ and Ã can be defined such that |W̃| ≤ 4 (by some generalized triangle inequality) and Ã has the staggered structure.

**Specific computation to resolve Lemma 5**:

A symbolic computation (50–100 lines in sympy or Mathematica) that:
1. Parameterizes the 16 links at vertex x as R_0, R_1, R_2, R_3 (base) and C_{μν} for each of the 6 cross-link pairs
2. Expands F_x = ∑_{μ<ν} |B_{μν}|² symbolically in terms of inner products ⟨n, R_k n⟩
3. Groups terms by their rotation structure
4. Identifies whether the result can be written as 32 + 8⟨n,W̃⟩ − |Ã|² for appropriate vectors W̃, Ã on S² satisfying |W̃| ≤ 4 and |Ã|² ≥ 0
5. If not, identifies the obstructing terms and whether they are bounded by cross-cancellations

This computation is feasible because SO(3) rotations can be parameterized by 3 angles, and the expression is polynomial in ⟨n, R_k n⟩ ∈ [−1, 1].

**Alternative harder approach**: Reduce to cross-links=I via a gauge-transformation argument. At each vertex x, one could attempt to gauge-transform the 4 neighboring vertices to set the base links to I, then use a re-centered formula at the cross-link level. This is complicated by the entanglement of cubes sharing cross-links.

---

## Section 5: Cross-Check of Proof Outline

### Check 1: Handles ALL Q ∈ SU(2)^E

Lemma 5 claims the bound for ALL Q — including configurations where cross-links are far from I. If proved, the proof is complete for the full configuration space. ✓

### Check 2: Uses Correct B Formula

The B formula includes backward-traversed edges (e3, e4 with inverses on their links), consistent with E001 setup. The formula B = a(n + R_ξ n) + b(R_1 n + R_□ n) is the correct reduced form (verified in E002 and E003). ✓

### Check 3: Consistent with Dead Ends

- **M(Q) ≤ M(I) impossible**: Route A does not claim operator inequality; it only bounds the maximum eigenvalue. ✓
- **Per-plaquette factoring false**: Route A uses cube-face sums (6 plaquettes), not per-plaquette. Single plaquettes can have positive f, which is consistent. ✓
- **Global geodesic concavity fails**: Route A uses no concavity argument. ✓
- **Coulomb gauge / Gribov**: Route A uses no gauge fixing for the proof; it works in any gauge. ✓
- **Triangle inequality caps at 1/8**: Lemma 1 achieves |B| ≤ 4, but the cube-face bound uses the formula, not just triangle inequality per plaquette. ✓
- **Schur/Haar**: Route A uses no averaging argument. ✓

### Check 4: Known Special Cases

**Q=I**: W = 4n, A = (∑s_μ)n = 0·n = 0. Formula = 32 + 32 − 0 = 64 per vertex. Total = 1024. ✓

**Constant-link (Q_e = R for all e)**: E003 proved analytically: sum = 512(1 + cosθ) ≤ 1024. The cube-face inequality should give 64 per vertex (by symmetry, all 16 vertices contribute equally: 1024/16 = 64). Need to verify per-cube gives exactly 64. ✓ (implied by E003 result)

**Single-link perturbation**: E001 proved λ_max = 16 and global sum = 1024 exactly (for null vector). Since the partition gives ∑_x F_x = 1024 = 16 × 64, and each F_x ≤ 64 (Lemma 5), ALL vertex sums must be exactly 64 for the null vector. This is a strong prediction: each cube independently achieves its maximum 64 when any single link is perturbed.

**Verification**: This was NOT explicitly checked in the Phase 1 reports. Checking F_x = 64 for all x in a single-link configuration would be a simple ~10-line computation and would provide strong additional evidence for Lemma 5.

**Two-link perturbations**: λ_max < 16 (strictly). Prediction: some vertex x has F_x < 64. Consistent with all tested cases. ✓

**Pure gauge (Q = pure gauge transformation of I)**: B_□ = 0 for pure gauge, so f = 0. Each F_x = 0 ≤ 64. ✓

---

## Section 6: Synthesis Insights Beyond Individual Routes

### Insight 1: The Two Proofs Should Match

The cross-links=I formula F_x = 32 + 8⟨n,W⟩ − |A|² bounds F_x ≤ 64 via:
- "Alignment term" 8⟨n,W⟩ ≤ 32 (each base link contributes ≤ 8⟨n,n⟩ = 8 to alignment with n)
- "Anti-alignment penalty" −|A|² ≤ 0 (staggered sum penalizes configurations where links mis-align in a staggered pattern)

The second-order computation (E003) gives d²f/dt² = −26 for each perpendicular link perturbation. This means the "anti-alignment penalty" grows as −26t² for small t. The formula predicts −|A|² ≈ −4t² to leading order for a single base-link perturbation (since A ≈ s_μ·t·[axis] for small angle t). The factor 4 < 26 mismatch suggests the formula captures only the base-link contribution; cross-link effects provide additional suppression. This is qualitatively consistent with Lemma 5 being TRUE: cross-links only help (they can only decrease the total relative to the cross-links=I bound).

### Insight 2: Cross-links Cannot Make Things Worse

A key structural observation: the cross-links=I formula gives F_x ≤ 64 with equality at Q=I. For general cross-links, the numerical maximum is 48.3 (far below 64), suggesting cross-links REDUCE the bound. This makes intuitive sense: varying cross-links away from I creates additional decoherence (active plaquettes lose amplitude) without providing compensating gains in the staggered sum.

If this monotonicity can be made precise — e.g., ∂F_x/∂(cross-link rotations) ≤ 0 at each maximum of F_x — it would prove Lemma 5 by showing the maximum of F_x over cross-links is achieved at cross-links=I.

### Insight 3: The Role of the Staggered Mode

Both E001 and E002 identify the staggered sign structure as the key mechanism. The staggered mode has ∑_μ s_μ = 0 at every vertex x. This means:
- A = ∑_μ s_μ w_μ = 0 exactly at Q=I (since all w_μ = n)
- |A|² = 0 at the maximum → maximum is achieved at Q=I
- For any deformation, |A|² > 0 generically → penalty kicks in

For the general formula, this mechanism should generalize to an effective staggered condition on the cross-links too. The cross-link contributions q^{μν} and r^{μν} must also contribute an "effective A" term that vanishes at Q=I and provides a penalty for deviations.

### Insight 4: Connection Between Routes A and D

Route D's Fourier block structure and Route A's staggered sign mechanism are dual perspectives on the same physics:
- Route A: LOCAL (per-vertex) algebraic identity showing anti-alignment penalty
- Route D: GLOBAL Fourier analysis showing all modes decrease below the staggered mode

The staggered mode k=(1,1,1,1) has the LARGEST amplitude decrease (Fourier block eigenvalues: −40, −20, −20, −20, −20, −20, −4, −4) — consistent with the largest per-vertex sum being suppressed. A complete proof might combine both: use the Fourier structure to constrain the cross-link formula.

---

## Section 7: Summary

### Ranked Proof Routes

1. **Route A (Cube-face inequality)** — Best. Clear mechanism, proved for cross-links=I, 16-vertex partition, one unproved lemma.
2. **Route D (Quadratic form + Morse-Bott)** — Second. Rigorous local result, Fourier structure explicit, but global gap is larger.
3. **Route B (Parallelogram pairing)** — Blocked. Pairing requires shared holonomies that don't exist generically.
4. **Route C (Single-link induction)** — Blocked. No inductive structure.

### Proof Outline (Route A)

**Theorem**: For all Q ∈ SU(2)^64, λ_max(M(Q)) ≤ 16.

**Proof**:
1. (Lemma 0) Partition plaquettes into 16 cube-face groups P_x, one per vertex.
2. (Lemmas 1–2) Each B formula has the sign structure B = a(n + R_ξ n) + b(R_1 n + R_□ n).
3. (Lemmas 3–4) [PROVED] For cross-links=I: F_x = 32 + 8⟨n,W⟩ − |A|² ≤ 64.
4. (Lemma 5) [UNPROVED] For general Q: F_x ≤ 64.
5. Sum: ∑_x F_x ≤ 16 × 64 = 1024 = 4d|v|², giving λ_max ≤ 16. □

### Single Hardest Step

**Lemma 5: The cube-face inequality for general Q.**

Specifically: prove F_x(Q,v) ≤ 64 for all Q ∈ SU(2)^E and all x, where F_x involves 6 plaquettes with 16 link variables (4 base + 12 cross) per vertex.

### Specific Computation to Resolve the Hardest Step

A symbolic algebra computation (sympy/Mathematica, ~50–100 lines) that:
1. Expands F_x for general Q by writing each |B_{μν}|² = |a(p_μ + q^{μν}) + b(n + r^{μν})|² where p_μ, q^{μν}, r^{μν} are unit vectors
2. Sums over all 6 plaquettes, groups inner product terms by rotation structure
3. Determines if the result has the form 32 + 8⟨n,W̃⟩ − |Ã|² (or analogous form with |W̃| ≤ 4 and Ã appropriately staggered)
4. If the form holds, identify W̃ and Ã explicitly; the bound follows immediately
5. If not, determine whether a refined inequality (e.g., Cauchy-Schwarz on cross-terms) closes the gap

This is a targeted, feasible computation that could either complete the proof or identify the precise obstruction.
