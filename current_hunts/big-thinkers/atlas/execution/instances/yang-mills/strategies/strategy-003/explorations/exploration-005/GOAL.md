# Exploration 005: Weitzenböck R(Q) Sign — Extract from Jiang (2022) and Analyze

## Mission Context
This is a YANG-MILLS mission (strategy-003). Do not confuse with other missions.

## The One Inequality We Need to Prove

**Target:** ∑_□ |B_□(Q,v)|² ≤ 4d|v|² for all Q ∈ SU(N)^E.
Equivalently: M(Q) ≼ M(I) where M(Q) = ∑_□ B_□ B_□^T (operator on ⊕_e su(N)).

**Why:** Gives H_norm ≤ 1/12 → mass gap at β < 1/4 for SU(2), d=4 (12× SZZ arXiv:2204.12737).

## The Weitzenböck Decomposition (Phase 1 Finding)

From E001 (Phase 1): There is a discrete Weitzenböck identity:

  **M(Q) = M(I) + R(Q)**

where M(I) = K_curl (max eigenvalue = 4d, proved analytically by E004 via K_curl(k=(π,...,π)) = 4dI - 4J), and R(Q) is a curvature correction term.

The inequality M(Q) ≼ M(I) is EQUIVALENT to R(Q) ≼ 0 for all Q.

**Numerically confirmed (E004):** All 50+ tested L=4 configurations satisfy M(Q) ≼ M(I). Adversarial gradient search max = 0.063 << 1/12.

**Your task:** Find the explicit formula for R(Q) and determine whether R(Q) ≼ 0 is provable.

## Your Tasks

### Task 1 (Priority 1): Extract the Weitzenböck Formula

Search for and read the following papers to find the explicit discrete Weitzenböck formula:

1. **Jiang (2022)** — "Discrete Weitzenböck formula for lattice gauge theories." Find this paper (search arXiv, Google Scholar). Extract the exact formula for R(Q) in terms of the gauge field Q.

2. **SZZ (arXiv:2204.12737)** — Shen, Zhu, Zhu 2023. Section 4 (the Bakry-Émery curvature computation). They may use an identity similar to M(Q) = M(I) + correction. Extract:
   - Their exact formula for HessS(v,v)
   - Any decomposition of the form M(Q) = M(I) + R(Q)
   - Whether they bound R(Q) or just bound M(Q) directly

3. **Bakry-Émery literature**: Any paper using Γ₂ calculus for lattice gauge theory. The Weitzenböck identity is equivalent to the Γ₂ computation.

For each paper found, extract:
- The exact formula for the curvature correction R(Q)
- Whether the formula involves |F_□|² (plaquette curvature squared) terms
- Whether R(Q) ≼ 0 is proved or conjectured

### Task 2 (Priority 2): Sign Analysis of R(Q)

Once you have the formula for R(Q), analyze its sign.

**Key structure to look for:**

In differential geometry, the Weitzenböck identity for the connection Laplacian Δ on forms gives:
  Δ = ∇*∇ + Ric
where Ric is the Ricci curvature. For NEGATIVE Ricci curvature (Ric ≤ 0), the Laplacian is "easier to invert" — the curvature helps rather than hurts.

In our context: M(Q) = M(I) + R(Q) where M(I) = K_curl (the "flat Laplacian"). R(Q) is the "curvature contribution." For the bound M(Q) ≼ M(I) to hold, we need R(Q) ≼ 0, i.e., the curvature is NEGATIVE.

For SU(N) Yang-Mills, the curvature of the connection is the field strength F_□ = U_□ − I ∈ su(N) (or the plaquette holonomy). The Weitzenböck correction R(Q) should involve these field strengths.

**Specific structure to check:**
- Does R(Q) = −C × ∑_□ F_□ ⊗ F_□ for some positive constant C?
- Does R(Q) involve terms like −|F_□|² × (projection onto tangent direction)?
- Is R(Q) always negative semidefinite for SU(2) (using SU(2)-specific identities)?

### Task 3 (Priority 3): Worked Example

For the single-link excitation Q = exp(ε τ₁) on link (0,0) (all other links = I):

1. Compute M(Q) explicitly (using the corrected B_□ formula from E001/E002)
2. Compute R(Q) = M(Q) − M(I)
3. Find the eigenvalues of R(Q)
4. Verify R(Q) ≼ 0

E003 found: the 6 plaquettes containing link (0,0) get a cos(ε) suppression factor. This should translate into R(Q) having negative eigenvalues. Work out the algebra explicitly.

### Task 4 (Priority 4): Literature Novelty Check

After finding the Weitzenböck formula:
1. Has R(Q) ≼ 0 been proved before for lattice YM?
2. Is the formula M(Q) = M(I) + R(Q) used in SZZ/CNS?
3. If R(Q) ≼ 0 is not in the literature, is our claim (based on numerics + the Weitzenböck structure) genuinely novel?

## Success Criteria

**Full success:** Explicit formula for R(Q) found from literature + proof that R(Q) ≼ 0 (or identification of why it might be hard to prove).

**Partial success:** Formula found but sign proof incomplete. Clear statement of what additional algebra is needed.

**Key finding:** If R(Q) = −∑_□ (plaquette holonomy contribution)² or similar negative-definite structure, this closes the proof.

## Output Format

Write REPORT.md section by section:
1. Literature search results (Jiang 2022, SZZ, Bakry-Émery)
2. Explicit R(Q) formula
3. Sign analysis
4. Worked example (single-link excitation)
5. Novelty assessment
6. Summary: Is R(Q) ≼ 0 provable? What's the gap?

Write REPORT-SUMMARY.md (1 page): Formula found? Sign clear? Novel?

## Notes
- Write after EACH section, not all at once.
- This is a LITERATURE SEARCH + MATH PROOF task.
- The Jiang (2022) paper is the key reference — find it even if you have to search broadly.
- If you cannot find Jiang (2022), search for "discrete Weitzenböck" + "lattice gauge" + "SU(N)" more broadly.
