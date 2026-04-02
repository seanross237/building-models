# Exploration 004: Master Loop Contraction Estimate Optimization

## Mission Context
This is a YANG-MILLS mission. Do not confuse with other missions.

## Background

The Cao-Nissim-Sheffield (CNS) May 2025 paper (arXiv:2505.16585, "Expanded Regimes of Area Law for Lattice Yang-Mills Theories") proves the area law via master loop equations at β ≤ β₀(d). The explicit threshold stated in the proof is:

**β₀(4) = 10^{-40}/4** (from equation 2.2, with conservative constants)

However, when parameters are optimized:
- Structural threshold from Theorem 3.2: β < 1/(10³d) = 1/4000 in d=4
- With tighter contraction constant C ~ 8de: β ~ 1/(8de) ≈ 1/87 in d=4

The best Bakry-Émery threshold (CNS Sept 2025) is β < 1/24 ≈ 0.042.

The master loop optimized threshold (~1/87 ≈ 0.012) is 3.6× smaller than 1/24.

**The paper (Remark 1.4) explicitly asks:** Can the master loop approach be extended to cover β < 1/24 if the curvature of U(N) is used as input to the contraction estimate? This would combine the master loop's N-independent string tension with Bakry-Émery's better β range.

## Your Task

This is a COMPUTATIONAL task. Write code, run it, report numbers.

**IMPORTANT: Start coding immediately. Maximum 5 minutes of thinking before first line of code.**

### Task 1: Optimize the Contraction Estimate (Priority 1)

The master loop contraction condition (from Proposition 3.23 of arXiv:2505.16585) requires:
```
β · B(N,d) < C_d
```
where B(N,d) is a combinatorial factor related to the number of plaquettes and the group dimension, and C_d is a constant from the contraction estimate.

The paper sets C = 10³ for safety, giving threshold 1/(10³d). With the "deformation term" analysis, C ~ 8de, giving threshold 1/(8de) ≈ 1/87 in d=4.

**Your computation:**
1. Extract the explicit dependence of the threshold on the parameter C from the paper
2. Find the optimal value of C (minimize the threshold denominator)
3. In d=4, what is the maximum β where the contraction holds as a function of C?
4. Can any natural choice of C bring the threshold up to 1/24?

Write the threshold as a function: `β_max(C, d=4) = ?` and find `max_C β_max(C, d=4)`.

**Specifically:** The paper says the contraction requires:
`β < 1 / (C_1 · C_2(d))` where C_1 depends on the group combinatorics and C_2(d) = something × d.

Extract C_1 and C_2(d=4) from the proof (read Proposition 3.23, Lemma 3.24, Section 3.3 of arXiv:2505.16585). Then minimize the bound.

### Task 2: Curvature Input Estimate (Priority 2, if time allows)

The key question in Remark 1.4: "Can we use the Ricci curvature κ = N/2 of SU(N) as input to the master loop bound?"

The Bakry-Émery threshold is β < 1/24 because K_S = N/2 - 4(d-1)Nβ > 0 (vertex formulation). This uses the curvature κ = N/2 to offset the action's negative contribution.

If the master loop bound could be written as:
`β · B(N,d) < C_d + δ · κ`
where δ = some positive function of N and d, and κ = N/2, then at N → ∞ (large N limit), κ → ∞ and the threshold would approach 1/24 (or better).

**Your computation:** Write a simple script that:
1. Computes β_max as a function of κ for the conjectured modified bound: `β_max(κ) = (C_d + δκ) / B(N,d)` for δ = 0 (current paper) and δ = 1 (maximally curvature-enhanced)
2. Plots or prints β_max vs. κ for κ = 0, 0.5, 1.0, 2.0, 5.0, 10.0 (N ≈ 0, 1, 2, 4, 10, 20)
3. Reports: what value of δ would be needed to bring β_max up to 1/24 in d=4?

## Success Criteria

**Success:**
1. Extracted explicit formula for β_max(C, d=4)
2. Found the optimal C and corresponding maximum β₀(4)
3. Determined whether any δ > 0 (curvature input) could bring β₀(4) up to 1/24

**Failure:** If Proposition 3.23 is too implicit or the derivation requires more background than can be extracted. Report: what was found, what's missing.

## Source Material

- arXiv:2505.16585 — read Sections 3.3, 3.4, and Proposition 3.23, Lemma 3.24 carefully
- Key parameters: λ (surface weight), γ (loop weight), ρ (boundary factor), C (contraction constant)

## Output Format

1. **code/** directory with:
   - `contraction_optimize.py` — the optimization script
   - `results.txt` — all numerical outputs

2. **REPORT.md** covering:
   - Extracted β_max formula
   - Optimal C and corresponding β₀(4)
   - Curvature input analysis
   - Physical interpretation

3. **REPORT-SUMMARY.md** (1 page):
   - Bottom-line: what is the maximum achievable β₀(4) under master loop framework?
   - Can curvature input bring it to 1/24?
   - Implication for combining master loop + Bakry-Émery

## Important Notes
- Write code to files immediately, print results as you get them
- Do NOT spend more than 10 minutes on any single problem
- If you cannot extract Proposition 3.23 from the PDF, estimate the threshold using the structural analysis already done (β_max ~ 1/(Cd) for optimized C)
- Write report section by section, not all at once
