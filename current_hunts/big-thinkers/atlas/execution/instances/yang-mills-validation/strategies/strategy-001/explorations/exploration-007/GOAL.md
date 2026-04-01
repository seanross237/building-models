# Exploration 007: Adversarial Proof Review

## Mission Context

A prior research program proved mass gap for lattice SU(N) Yang-Mills at β < N²/(8(d-1)) — an 8× improvement over SZZ (arXiv:2204.12737) and 4× improvement over CNS (arXiv:2509.04688). The proof has been validated by 6 explorations: independent rederivation, novelty assessment, convention verification, large lattice tests, SU(3) extension, and dimensional analysis.

Your job is to find GAPS in the proof that haven't been caught yet. You are the adversarial reviewer.

## The Proof Chain

Here is the complete proof chain to scrutinize:

### Step 1: SZZ Framework (arXiv:2204.12737, Theorem 1.3)
The Bakry-Émery condition: if HessS(v,v) < (N/2)|v|² for all v, then the lattice Yang-Mills measure has a spectral gap (mass gap).

**Question to answer:** Is this theorem correctly applied? Specifically:
- Does the SZZ theorem assume anything about the lattice (finite? infinite? periodic?)
- Is the spectral gap directly equivalent to "mass gap" as the term is used in physics?
- Are there technical conditions (smoothness, compactness) that are satisfied?

### Step 2: Hessian Computation
HessS(v,v) = (β/(2N)) Σ_□ |B_□(Q,v)|² where B_□ is the plaquette linearization.

**Question to answer:** Is this formula correct?
- The LEFT perturbation formula: B_□ = v₁ + Ad_{Q₁}(v₂) − Ad_{Q₁Q₂Q₃⁻¹}(v₃) − Ad_{U_□}(v₄)
- Has this been verified? YES: by finite differences (both diagonal and off-diagonal), at Q=I and Q≠I. Agreement to 10⁻⁴.
- Does HessS = (β/(2N))|B|² capture the full covariant Hessian, or is there a connection term?

### Step 3: Cauchy-Schwarz Bound
|B_□(Q,v)|² = |v₁ + Ad_{P₂}v₂ − Ad_{P₃}v₃ − Ad_{P₄}v₄|²
≤ 4(|v₁|² + |v₂|² + |v₃|² + |v₄|²)  (by CS)

Since Ad_{P} is an isometry: |Ad_P(v)| = |v| for all P ∈ SU(N).

**Question to answer:** Is this the right Cauchy-Schwarz inequality?
- CS: |a₁+a₂+a₃+a₄|² ≤ 4(|a₁|²+|a₂|²+|a₃|²+|a₄|²)
- Here a₁=v₁, a₂=Ad_{P₂}v₂, a₃=−Ad_{P₃}v₃, a₄=−Ad_{P₄}v₄
- So |B_□|² ≤ 4(|v₁|²+|v₂|²+|v₃|²+|v₄|²) ← correct because |−x| = |x|
- Is there a tighter inequality available? (Not needed for the proof, but relevant for the conjecture.)

### Step 4: Link Counting
Each link e appears in exactly 2(d-1) plaquettes (as any of the 4 edges):
Σ_□ Σ_{e∈□} |v_e|² = 2(d-1) Σ_e |v_e|² = 2(d-1)|v|²

**Question to answer:** Is the count 2(d-1) correct?
- A link (x,μ) belongs to plaquettes in the (μ,ν) plane for each ν ≠ μ → (d-1) planes
- In each plane, the link belongs to 2 plaquettes (one on each side)
- Total: 2(d-1) plaquettes per link ← correct for periodic lattice

### Step 5: Mass Gap Threshold
Combining: HessS(v,v) ≤ (β/(2N)) × 4 × 2(d-1) × |v|² = 4(d-1)β|v|²/N

Bakry-Émery: need 4(d-1)β/N < N/2 → β < N²/(8(d-1))

For SU(2), d=4: β < 4/24 = 1/6.

**Question to answer:** Are all the steps reversible? Is it "HessS < X for all v" or "HessS ≤ X for all v"? Does the strict inequality matter?

### Step 6: What Does This Actually Prove?
The SZZ Bakry-Émery approach proves a SPECTRAL GAP for the lattice gauge field Gibbs measure. This means:

(a) Correlation functions decay exponentially
(b) There is a gap between the first and second eigenvalues of the transfer matrix

**Question to answer:**
- Is "spectral gap of the transfer matrix" the same as "mass gap" in the physics sense?
- Does this hold in finite volume only, or does it extend to infinite volume?
- Is there a lattice-to-continuum issue?

## What Has Already Been Verified

1. **Convention:** LEFT B_□ formula verified by FD at Q=I and Q≠I (E003)
2. **Q=I eigenvalue:** λ_max = 4β [VERIFIED exact, multiple explorations]
3. **Large lattice:** H_norm ≤ 1/12 for 71 configs across L=2,4,6 (E004)
4. **SU(3):** Same structure, N² scaling confirmed (E005)
5. **All dimensions:** Triangle inequality proof valid for all d (E006)
6. **Novelty:** Not in CNS papers (E002)

## Your Task

Read the proof chain above critically and answer:

1. **Is there a gap in the proof of β < N²/(8(d-1))?** Any step where the conclusion doesn't follow from the premises?
2. **Are there hidden assumptions?** E.g., does the Bakry-Émery theorem require the manifold to be simply connected? Does it work on a discrete lattice? Does it handle gauge invariance correctly?
3. **What is the weakest link?** Rank the steps by confidence.
4. **What would a referee object to?** If this were submitted as a paper, what would the main criticism be?
5. **Is the statement "mass gap" technically correct?** Or should it be "spectral gap of the lattice measure"?

## What to Look For

Search for:
- SZZ paper (arXiv:2204.12737) — read their actual theorem statement
- Bakry-Émery theory on manifolds — does it apply to product manifolds SU(N)^E?
- Spectral gap vs mass gap — is there a distinction in the lattice gauge theory literature?
- Whether the proof assumes anything about the gauge group being SU(2) specifically
- The Chatterjee paper (arXiv:2211.01540) for context on Wilson loop expectations

## Success Criteria
- [ ] Each step rated: VALID / VALID WITH CAVEAT / QUESTIONABLE / INVALID
- [ ] Any hidden assumptions identified
- [ ] Referee objections listed
- [ ] "Mass gap" vs "spectral gap" distinction clarified
- [ ] Weakest link identified

## What to Write
Write REPORT.md and REPORT-SUMMARY.md.
