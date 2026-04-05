# Exploration 002: BKM Enstrophy Criterion — Formal Proof

## Mission Context

We are investigating the 3D Navier-Stokes regularity problem. Exploration 001 computationally validated that replacing the Ladyzhenskaya interpolation chain with BKM/CZ in the enstrophy equation gives effective blow-up times 10⁷ to 10¹⁶ times later — an overwhelming advantage. The structural reason: BKM puts ||∇ω|| inside a logarithm instead of raising it to power 3/2, so the dissipation term ν||∇ω||² always dominates.

## Goal

**State and prove a theorem** formalizing the BKM enstrophy bypass. Then computationally verify each proof step against DNS data.

## Target Theorem (to be refined)

**Theorem (BKM Enstrophy Bound):** Let u be a Leray-Hopf weak solution of the 3D Navier-Stokes equations on the periodic torus T³ = [0,2π]³ with viscosity ν > 0 and divergence-free initial data u₀ ∈ H¹(T³). Let ω = ∇×u be the vorticity. Then the enstrophy E(t) = ||ω(t)||²_{L²} satisfies:

  dE/dt ≤ 2C_{CZ} E(t) ||ω(t)||_{L^∞} [1 + log⁺(||∇ω(t)||_{L²}/||ω(t)||_{L²})] − 2ν||∇ω(t)||²_{L²}

where C_{CZ} is the Calderón-Zygmund constant for the Riesz transform on T³.

**Corollary 1 (No ν⁻³ factor):** After dropping the dissipation (which is non-positive for the bound), the enstrophy satisfies:

  dE/dt ≤ 2C_{CZ} E(t) ||ω(t)||_{L^∞} [1 + log⁺(||∇ω(t)||_{L²}/||ω(t)||_{L²})]

This is qualitatively different from the Ladyzhenskaya result:

  dE/dt ≤ (27C_L⁸)/(128ν³) E(t)³    (Ladyzhenskaya, after Young's inequality)

The BKM version has NO ν⁻³ factor and the enstrophy appears at power 1 (not 3).

**Corollary 2 (Conditional regularity):** If ||ω(t)||_{L^∞} and log(||∇ω(t)||_{L²}/||ω(t)||_{L²}) are both bounded on [0,T], then E(t) grows at most exponentially on [0,T] — no finite-time blow-up.

**Comparison with existing results:** The BKM criterion (1984) states that if ∫₀ᵀ ||ω(t)||_{L^∞} dt < ∞, then the solution is regular on [0,T]. Our theorem should be compared: does it give a STRICTLY weaker criterion than Prodi-Serrin L^p_t L^q_x criteria?

## Specific Tasks

### Task 1: Prove the main inequality
Start from the enstrophy equation:
  (1/2) d/dt ||ω||² = ∫ ω_i S_{ij} ω_j dx − ν||∇ω||²

Bound the vortex stretching:
  |∫ ω_i S_{ij} ω_j dx| ≤ ||ω||²_{L²} · ||S||_{L^∞}

Then bound ||S||_{L^∞} using CZ theory:
  ||S||_{L^∞} ≤ C_{CZ} ||ω||_{L^∞} [1 + log⁺(||∇ω||_{L²}/||ω||_{L²})]

Provide EXACT references for each step. Which theorem of CZ theory gives this bound? What is the precise statement?

**CRITICAL CHECK:** Is the CZ bound ||S||_{L^∞} ≤ C_{CZ} ||ω||_{L^∞} [1 + log⁺(||∇ω||/||ω||)] actually correct? This is the Brezis-Gallouet-Wainger type estimate. Verify the exact form. The BKM criterion itself uses ||ω||_{L^∞} ∈ L¹([0,T]) for regularity, but the ENSTROPHY bound needs S, not ω. The relationship is S_{ij} = (1/2)(∂_i u_j + ∂_j u_i) and ω = ∇×u. Via the Biot-Savart law, ||S||_{L^∞} can be bounded by ||ω||_{L^∞} plus a log correction.

**Verify computationally:** For each timestep in our DNS data (TGV Re=1000), check that the inequality chain holds with the claimed constants.

### Task 2: Compare with Prodi-Serrin
The Prodi-Serrin criterion requires u ∈ L^p([0,T]; L^q(T³)) with 2/p + 3/q ≤ 1, q > 3.

Our BKM enstrophy bound requires ω ∈ L¹([0,T]; L^∞(T³)) (plus the log correction).

Question: Is ω ∈ L¹_t L^∞_x implied by any Prodi-Serrin condition? If NOT, then our criterion is independent of Prodi-Serrin (neither strictly weaker nor stronger). If YES, then Prodi-Serrin is strictly stronger.

Use Sobolev embedding to compare: ω ∈ L^∞ ↪ H^s for s > 3/2, so ||ω||_{L^∞} ≤ C||ω||_{H^{3/2+ε}} for any ε > 0. But the Prodi-Serrin criteria are on u, not ω. Compare via ||∇u|| and ||ω||.

### Task 3: Quantify the advantage formally
Prove: The Ladyzhenskaya enstrophy ODE gives blow-up at time T_Lad = C/(ν³ E₀²) while the BKM enstrophy ODE gives blow-up at T_BKM = C'/( ||ω||_{L^∞,∞} ) where ||ω||_{L^∞,∞} is the sup of ||ω||_{L^∞} over [0,T].

Show that T_BKM/T_Lad grows as ν⁻³ × E₀² / ||ω||_{L^∞,∞} → ∞ as ν → 0 for flows where ||ω||_{L^∞}/E^{1/2} stays bounded.

**Verify computationally:** Compute T_BKM/T_Lad for our DNS data and check that it matches the theoretical scaling (should grow as ~Re³ per exploration 001 data).

### Task 4: Write the formal proof
Write a complete, self-contained proof of the main theorem and corollaries. Every step should be justified by either:
- A reference to a standard result (with exact citation)
- A computation that you verify numerically

The proof should be structured as a sequence of lemmas, each independently verifiable.

## Existing Code

The DNS solver and measurement infrastructure from exploration 001 are at:
  `../exploration-001/code/ns_solver.py`
  `../exploration-001/code/bkm_comparison.py`
  `../exploration-001/code/run_cases.py`

The results data is at:
  `../exploration-001/results/all_results.json`

You can load the results directly or rerun specific computations.

## Success Criteria

**Succeeds if:**
- A complete proof of the BKM enstrophy bound is given with all steps justified
- The comparison with Prodi-Serrin is resolved (strictly weaker, strictly stronger, or independent)
- The quantitative advantage T_BKM/T_Lad ~ ν⁻³ is proved analytically and verified computationally

**Partially succeeds if:**
- The proof has gaps but the gaps are precisely identified
- The comparison with Prodi-Serrin is clear even if the full proof isn't

**Fails if:**
- The BKM bound on ||S||_{L^∞} turns out to require a different form than assumed
- The proof reduces to something already in the literature with no new content

## Output

Write REPORT.md and REPORT-SUMMARY.md in the current directory. Put any code in code/. Structure the report as:
1. Statement of the theorem(s)
2. Proof (step by step, with verification tags)
3. Comparison with existing results
4. Computational verification
5. Assessment: what is genuinely novel vs. known?
