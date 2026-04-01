# Computation Registry

Computations identified during explorations that would significantly advance the mission.
Maintained by the strategizer, read by the missionary and future strategizers.

## From Exploration 001 (Balaban RG Program)

### 1. Contraction analysis of 4D YM RG map
- **What:** Numerically study whether Balaban's RG transformation is contractive (in appropriate norms) for the marginally renormalizable 4D case
- **Why it matters:** Would inform Gap 2 (uniqueness of the continuum limit). If the RG map is contractive, uniqueness follows.
- **What it would resolve:** Whether the Tier 1 gap of proving uniqueness is within reach via Balaban's framework
- **Source:** Exploration 001
- **Difficulty:** Moderate — ~100-line numpy/scipy script once the map is formalized, but extracting the explicit RG map from Balaban's papers [11]-[12] is the hard part
- **Key references:** Balaban papers [11]-[12] on effective actions and β-functions in 4D

### 2. Wilson loop RG tracking
- **What:** Formalize how a Wilson loop observable transforms under one Balaban RG step, and estimate error bounds
- **Why it matters:** Would inform Gap 1 (extending UV stability to control gauge-invariant observables)
- **What it would resolve:** Whether Balaban's framework can be extended to track observables, not just the partition function
- **Source:** Exploration 001
- **Difficulty:** Conceptual — defining the right framework is the challenge; the computation itself would be moderate
- **Key references:** Balaban papers [6], [10], [11]

## From Exploration 002 (Constructive QFT 2D/3D vs 4D)

### 3. Numerical verification of Balaban's bounds on small lattices
- **What:** Implement block-spin RG for SU(2) lattice gauge theory on small lattices (e.g., 8⁴) and check whether Balaban's UV stability bounds are tight or have room for improvement
- **Why it matters:** Would reveal if there's unexploited room in the bounds that could simplify the Tier 1 gaps
- **What it would resolve:** Whether tighter bounds might make observable control (Gap 1) or uniqueness (Gap 2) more accessible
- **Source:** Exploration 002
- **Difficulty:** Moderate (100-200 lines of code for the RG step, but conceptual understanding of Balaban's setup needed)

### 4. Non-perturbative beta function comparison
- **What:** Compare perturbative beta function with Balaban-style block-spin beta function on the lattice
- **Why it matters:** Could illuminate how perturbative asymptotic freedom connects to non-perturbative UV stability
- **What it would resolve:** Whether the asymptotic freedom mechanism is fully captured by Balaban's framework
- **Source:** Exploration 002
- **Difficulty:** Moderate; would require lattice gauge theory simulation code

## From Exploration 004 (Lattice-Continuum Gap)

### 5. Transfer matrix spectral gap analysis for SU(2) on small lattices
- **What:** Numerically compute eigenvalues of the transfer matrix T for pure SU(2) lattice gauge theory on small spatial volumes (e.g., 4³) at various β. Track ratio of 2nd-largest to largest eigenvalue.
- **Why it matters:** If spectral gap persists as β → ∞, this provides numerical evidence for a rigorous spectral gap argument
- **What it would resolve:** Whether the mass gap is numerically robust under the continuum limit
- **Source:** Exploration 004
- **Difficulty:** Moderate (50-100 lines + existing lattice code)

### 6. Finite group approximation convergence to SU(2)
- **What:** Approximate SU(2) by finite subgroups (binary icosahedral group of order 120, etc.) and check whether Adhikari-Cao mass gap bounds converge to something meaningful as subgroup → SU(2)
- **Why it matters:** Tests whether the finite→continuous barrier is a technicality or fundamental
- **What it would resolve:** Whether Adhikari-Cao's techniques can be adapted for continuous groups
- **Source:** Exploration 004
- **Difficulty:** Moderate (100-150 lines)

## From Strategy-002 Exploration 001 (SZZ Technique Extraction)

### 7. Hessian sharpness check for SU(2) Bakry-Émery bound
- **What:** Numerically estimate max |HessS(v,v)|/|v|² for random Q ~ μ^{ym}_{N=2,β} at β = 0.02, 0.1, 0.5. Compare to Lemma 4.1 bound 8(d-1)Nβ = 48β for SU(2) in d=4.
- **Why it matters:** If the actual Hessian is significantly smaller than the bound (e.g., ≤ 24β instead of 48β), then the Bakry-Émery threshold might extend from 1/48 to 1/24 (or further) using SZZ's own edge formulation, without needing the vertex σ-model reformulation.
- **What it would resolve:** How much slack exists in Lemma 4.1 of SZZ. If tight, the edge formulation cannot be improved; if loose by 2×, we could recover the CNS bound 1/24 without changing the framework.
- **Source:** Strategy-002, Exploration 001
- **Difficulty:** Easy-Medium (50-70 lines of Monte Carlo code, adapt E003 SU(2) code)
- **Key references:** SZZ arXiv:2204.12737 Lemma 4.1; CNS arXiv:2509.04688

### 8. Effective coupling after one Balaban RG block-spin step
- **What:** Implement one Balaban-style block-spin transformation for SU(2) on an 8⁴ lattice → 4⁴ blocked lattice. Compute the effective action at the blocked scale. Measure the effective Hessian bound for the blocked action.
- **Why it matters:** The RG+Bakry-Émery idea: if after one RG step the effective coupling β_eff satisfies β_eff < 1/24, then the Bakry-Émery condition holds for the blocked system even when it fails for the original (β > 1/24). This could extend the mass gap result to larger β.
- **What it would resolve:** Whether one RG step actually reduces the Hessian enough to bring the system back into the Bakry-Émery regime. This is the core Phase 2 hypothesis of strategy-002.
- **Source:** Strategy-002, Exploration 001
- **Difficulty:** Hard (200-300 lines; requires implementing block-spin RG for SU(2), which needs non-trivial gauge-fixing)
- **Key references:** Balaban CMP 95 (1984), 99 (1985); SZZ arXiv:2204.12737; CNS arXiv:2509.04688

## From Strategy-002 Exploration 002 (Spectral Gap Scan)

### 9. Larger lattice spectral gap scan near deconfinement
- **What:** Repeat the τ_int vs. β scan on 6⁴ and 8⁴ lattices, focusing on β = 1.5–2.5. Check whether τ_int at β = 2.0 diverges with volume (true critical slowing down at the deconfinement transition) or stays finite (finite-size artifact on 4⁴).
- **Why it matters:** If τ_int(β=2.0) diverges with volume, the spectral gap genuinely vanishes at the deconfinement transition in infinite volume — meaning any proof of mass gap must handle this transition. If τ_int stays finite, the gap persists.
- **What it would resolve:** Whether the τ_int = 2.11 at β = 2.0 is a finite-size artifact or a genuine property of infinite-volume SU(2).
- **Source:** Strategy-002, Exploration 002
- **Difficulty:** Easy (modify E002 code, increase L; each β ≈ 30-60 min on 8⁴)
- **Key references:** SU(2) deconfinement transition literature (β_c ≈ 2.30 on finite lattices)

### 11. Master loop contraction estimate optimization
- **What:** Numerically optimize the parameters (λ, γ, ρ, C) in the master loop contraction estimate (Proposition 3.23 of arXiv:2505.16585, Cao-Nissim-Sheffield May 2025) to find the maximum β where the contraction holds. Current paper uses C = 10³ (conservative); with C optimized to C ~ 8de the threshold improves from 1/4000 to ~1/87 in d=4.
- **Why it matters:** Pin down the true maximum β₀(d) for the master loop approach, and determine how close it can get to 1/24 (the Bakry-Émery threshold). If there's a natural extension using curvature input, the master loop threshold might get closer to 1/24 with N-independent string tension.
- **What it would resolve:** Whether the gap between master loop (1/87) and Bakry-Émery (1/24) is fundamental or an artifact of conservative estimates.
- **Source:** Strategy-002, Exploration 003
- **Difficulty:** Easy (~20-line numpy optimization, inputs needed: Proposition 3.23 formula)
- **Key references:** CNS arXiv:2505.16585 Proposition 3.23, Remark 1.4

### 10. Poincaré constant lower bound estimate at β = 2.0
- **What:** Using the numerical spectral gap γ ≈ 0.24 at β = 2.0 as guidance, attempt to derive a rigorous lower bound for the Poincaré constant c_P ≥ ε > 0 at β ≤ 2.0, using whatever analytic tools are available (e.g., coupling/comparison arguments, or the Holley-Stroock comparison theorem).
- **Why it matters:** If a rigorous c_P ≥ 0.1 can be proved at β = 2.0, this would be a dramatic extension of SZZ into the physical regime.
- **What it would resolve:** Whether the numerical evidence (γ > 0 at β = 2.0) can be converted into a rigorous bound.
- **Source:** Strategy-002, Exploration 002
- **Difficulty:** Theoretical (no code needed); high difficulty; may require new analytic ideas
- **Key references:** SZZ arXiv:2204.12737; CNS arXiv:2509.04688; Holley-Stroock perturbation lemma

## From Exploration 008/009 (Hessian Proof + Eigenvalue Verification)

### 12. Prove ∑_□ |B_□(Q,v)|² ≤ 4d|v|² for all Q (closes the H_norm ≤ 1/12 gap)
- **What:** Prove the open conjecture that the sum of parallel-transported curl-squared over all plaquettes is bounded by 4d|v|². Combined with Lemma 5.1 from E008, this would give H_norm ≤ 1/12 for ALL Q (not just Q=I), completing the proof that β < 1/4 extends the mass gap.
- **Why it matters:** Closes the one remaining gap in the main novel claim. Proves β < 1/4 rigorously (vs. β < 1/8 currently proved).
- **What it would resolve:** Whether the threshold improvement is 12× (β < 1/4) vs. 8× (β < 1/6) over SZZ.
- **Source:** Exploration 008 (Section 5.3)
- **Difficulty:** Moderate-hard. E008 suggests Coulomb/temporal gauge fixing might work. Temporal gauge sets Q_{x,0}=I; then spatial plaquettes only involve spatial links. Might reduce to a lower-dimensional problem.
- **Key equation:** B_□(Q,v) = Ad_{P_□^{(1)}}v_1 + Ad_{P_□^{(2)}}v_2 - Ad_{P_□^{(3)}}v_3 - Ad_{P_□^{(4)}}v_4 where P_□^{(i)} are partial holonomies. Need ∑_□ |B_□|² ≤ 4d|v|².
- **Key papers:** SZZ arXiv:2204.12737 Section 4 (for comparison with their Lemma 4.1 approach)

### 13. Systematic H_norm scan for non-identity Q (100+ configs)
- **What:** Compute max eigenvalue of the full Hessian for 100+ diverse Q configurations: random SU(2)^64, Gibbs samples at β=0.5/1.0/2.0/3.0, perturbations of Q=I (ε=0.01/0.1/0.5), adversarial (gradient ascent from multiple starts). Check if any gives H_norm > 1/12.
- **Why it matters:** Would either (a) find a counterexample to the conjecture or (b) provide strong numerical evidence that Q=I is the global worst case.
- **What it would resolve:** Whether Conjecture A' (H_norm ≤ 1/12 for all Q) is plausible. If 100 diverse configs all give H_norm ≤ 1/12, the conjecture is strongly supported.
- **Source:** Exploration 009 (only tested 5 random Q — insufficient)
- **Difficulty:** Easy. ~50-line extension of E009's code (eigenvalue_check.py). Run time ~1 hour for 100 configs on L=2.
- **Key result to beat:** H_norm_max_observed = 1/12 = 0.0833 (at Q=I). All 5 random Q gave ≤ 0.042.

### 14. Verify SZZ action convention explicitly
- **What:** Read SZZ arXiv:2204.12737 Section 2 and extract the exact action S and inner product |·|² they use. Confirm whether their convention matches S = -(β/N)Re Tr(U_□) and |A|² = -2Tr(A²).
- **Why it matters:** All our H_norm calculations depend on this convention. E009 confirmed numerically that the 1/N normalization is essential for H_norm = 1/12, but we haven't directly verified this matches SZZ's setup.
- **What it would resolve:** Whether our claimed improvement (from SZZ's β<1/48 to β<1/4) is comparing apples-to-apples.
- **Source:** Exploration 008 (Gap 2, Section 8) and Exploration 009 (Convention Warning)
- **Difficulty:** Easy. Read 2 pages of SZZ, extract equations.
