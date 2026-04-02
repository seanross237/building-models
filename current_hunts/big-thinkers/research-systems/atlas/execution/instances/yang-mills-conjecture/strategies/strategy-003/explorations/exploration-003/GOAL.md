# Exploration 003: Prove the Hessian Eigenvalue Bound

## Mission Context

We are proving a mass gap bound for lattice SU(2) Yang-Mills on the d-dimensional hypercubic torus (d=4 is the target, but prove for general d if possible).

**The revised conjecture** (from Explorations 001-002):

> λ_max(HessS(Q)) ≤ 4d · (β/N)   for all Q ∈ SU(2)^E

where S(Q) = −(β/N) Σ_□ Re Tr(U_□) is the Wilson action and HessS is the 3|E|×3|E| Hessian matrix with respect to the Lie algebra parameterization Q_e → Q_e exp(Σ c_{e,a} iσ_a).

**If proved:** This gives λ_max(HessS) ≤ 4d·(β/N) = 8β for N=2, which via the Bakry-Émery condition (SZZ Theorem 1.3 with Ric = N/2 = 1 on each edge) gives a mass gap at β < 1/(16d) for generic d, or β < 1/64 for d=4 — wait, this doesn't match the claimed β < 1/4.

**IMPORTANT NORMALIZATION CHECK**: The SZZ Bakry-Émery condition is Ric(v,v) - HessS(v,v) ≥ K·|v|² where Ric = (N/2)|v|² per the Bochner formula on SU(N). For mass gap, need K > 0, i.e., HessS(v,v) < (N/2)|v|² for all unit v.

At Q flat: HessS(v,v; Q_flat) = (β/N) Σ_{□∋e} Re Tr(U_□) × |v_e|²/2 + cross terms.

Please VERIFY the exact SZZ threshold before proceeding. The mass gap requirement is H_norm := sup_Q λ_max(HessS(Q)) / (N/2) < 1, i.e., λ_max(HessS(Q)) < N/2. With our formula giving max eigenvalue scaling as d·β, this gives d·β < N/2, i.e., β < N/(2d) = 1/4 for N=2, d=4. But only if the normalization is correct.

## What's Already Known

### The Hessian Formula (from E002, verified to 1.4×10⁻⁶ against finite differences)

**Self-terms** (same edge, both derivatives):
H[(e,a),(e,b)] = (β/N) δ_{ab} Σ_{□∋e} Re Tr(U_□)

Key properties:
- Diagonal in color indices (proportional to I₃)
- Each edge participates in 2(d-1) plaquettes
- At flat connections (all U_□ = I): coefficient = (β/N) × 2(d-1) × 2 = 4(d-1)β/N per plaquette
- At generic Q: coefficient = (β/N) Σ_{□∋e} Re Tr(U_□) ≤ 4(d-1)β (since Re Tr ≤ 2 for SU(2))

**Cross-terms** (different edges sharing a plaquette):
H[(ep,a),(eq,b)] = −(β/N) sp sq Re Tr(Lp (iσa) mid_{pq} (iσb) Rq)

where sp = +1 for forward edges, −1 for backward; Lp, Rq, mid_{pq} are context matrices from the plaquette holonomy.

### Structural Facts
1. **Self-term correction C_self ≥ 0**: Since Re Tr(U_□) ≤ 2, the self-terms are MAXIMIZED at flat connections. [VERIFIED]
2. **At flat connections**: HessS = (β/2N)M exactly, where M is the "square-curl" operator. [VERIFIED]
3. **At flat connections**: λ_max(HessS) = 4d·(β/N) in the {iσ_a} basis. [VERIFIED for d=2,3,4]
4. **Gradient ascent on non-flat Q** reaches only 85% of the flat-connection bound. [COMPUTED]
5. **Cross-term kernel** has entries bounded by |(β/N)Re Tr(ABC)| ≤ 2β/N for 2×2 unitaries.

## Your Tasks

### Stage 1: Verify the SZZ Mass Gap Threshold

Before attempting the proof, establish the exact connection between λ_max(HessS) and the mass gap.

Search arXiv:2204.12737 (Shen-Zhu-Zhu 2023) for:
1. The Bakry-Émery condition (likely Theorem 1.3 or similar). What is the exact inequality?
2. The Ricci curvature of SU(2). What is Ric(v,v) / |v|²?
3. The relationship: if λ_max(HessS) ≤ C, what is the mass gap threshold on β?

Pin down the exact normalization. If the bound λ_max(HessS) ≤ 4d·(β/N) gives β < N/(2d), that's β < 1/4 for N=2, d=4. Verify this.

### Stage 2: The Proof Approach — Self-Term Dominance

The key structural observation: the self-terms dominate the diagonal and are maximized at flat connections.

**Attempt 1 — Gershgorin-type bound:**

For a symmetric matrix H, λ_max(H) ≤ max_i (H_{ii} + Σ_{j≠i} |H_{ij}|).

The self-terms give H_{(e,a),(e,a)} = (β/N) Σ_{□∋e} Re Tr(U_□).
The cross-terms give off-diagonal entries.

Can you show: self-terms + cross-term row sums ≤ 4d·(β/N)?

At flat connections, this should be tight (or near-tight). Away from flat, self-terms shrink. Do cross-term row sums also shrink? Compute numerically for 50 configs.

**Attempt 2 — Quadratic form bound:**

For any unit vector v, HessS(v,v) = Σ_□ h_□(v; Q) where h_□ is the per-plaquette Hessian contribution.

Can you bound h_□(v; Q) ≤ something × |v_edges_of_□|² and then sum over plaquettes?

The per-plaquette contribution has:
- Self-terms: (β/N) Re Tr(U_□) × Σ_{e∈□} |v_e|²
- Cross-terms: −(β/N) sp sq Re Tr(Lp iσa mid iσb Rq) × c_{ep,a} × c_{eq,b}

At flat connections, Re Tr(U_□) = 2 and the cross-terms have specific signs/structure.

Can you show: per-plaquette HessS_□(v,v) ≤ (4β/N) × (Σ_{e∈□} |c_e|²)?

If yes, summing over plaquettes gives λ_max ≤ (4β/N) × 2(d-1) × max_{e} (stuff) — but careful with the counting.

**Attempt 3 — Fourier analysis at flat connections + perturbation:**

At flat connections, HessS is translation-invariant and block-diagonalizes in Fourier space.

Compute the Fourier blocks. Show the maximum block eigenvalue is 4d·(β/N).

Then argue: perturbation away from flat REDUCES the max eigenvalue because it breaks the translation invariance that enables constructive interference of cross-terms.

### Stage 3: Numerical Support

For whichever approach seems most promising, test it numerically:
- Compute the relevant quantities (Gershgorin row sums, per-plaquette bounds, etc.) for 50+ random configs
- Find the worst case (max eigenvalue / bound ratio)
- If the bound is tight at flat connections and loose elsewhere, that supports the approach

### Stage 4: Proof or Obstruction Report

If you find a proof: write it as a complete argument with all steps.
If you hit an obstruction: characterize it precisely. What inequality fails? By how much? Is there a modified bound that works?

## Success Criteria

- Exact SZZ threshold verified (normalization pinned down)
- At least one of the three proof approaches produces a complete proof
- OR: clear identification of why each approach fails, with quantitative obstruction characterization

## Failure Criteria

- Cannot pin down the SZZ normalization (ambiguity in the literature)
- All approaches fail AND the failure modes are different (suggesting the bound is coincidental rather than structural)

## Output

Write your findings to REPORT.md (≤ 250 lines) and REPORT-SUMMARY.md (≤ 30 lines). Write incrementally after each stage.
