---
topic: Specify the level of rigor expected in output
category: goal-design
date: 2026-03-27
source: "yang-mills strategy-001 meta-exploration-001, meta-exploration-006, SED strategy-001 meta-exploration-002, classicality-budget strategy-002 meta-exploration-007, yang-mills strategy-002 meta-exploration-s002-001, yang-mills strategy-002 meta-exploration-s002-003, thermal-time strategy-002 meta-exploration-001"
---

## Lesson

When a goal involves technical mapping or analysis, explicitly specify the level of rigor expected (e.g., "theorem-level precision," "paper-by-paper inventory," "with precise citations"). Without this, explorers produce adequate summaries but miss the detailed technical tracking that makes results authoritative.

## Evidence

- **yang-mills strategy-001 exploration 001** — Asking for "precision at the theorem level" resulted in the explorer tracking down paper-by-paper content for all 14 Balaban papers, with specific theorem statements, dependency chains, and precise status classifications. Without this directive, the result would likely have been a competent but less granular overview.

- **yang-mills strategy-001 exploration 006** — Asking "what EXACTLY do they prove" (with emphasis on theorem statements) produced the most precise output of any exploration so far: full theorem statements with quantitative bounds, explicit coupling conditions, and mathematical formulations. The explorer independently discovered a "four layers of obstruction" structure — proving that **precise questions enable emergent structural discovery**. The goal asked a specific technical question; the explorer organized the answer into a structural framework not suggested by the goal.

- **yang-mills strategy-002 exploration-001** — Asking "what EXACTLY is the Bakry-Émery curvature inequality" produced the formula K_S = N/2 − 8N(d-1)β with complete factor derivation (diagonal 2 + off-diagonal 6 = 8). Asking "what EXACTLY fails at β ≥ 1/(16(d-1))" produced a specific sign-change analysis identifying exactly which step in Theorem 4.2 breaks. Sub-constant-level precision — individual numerical factors in the bound — was only achievable because the question was phrased at theorem precision. Compare: without this precision level, exploration-001 would have returned "Bakry-Émery fails at β = 1/48" without the mechanistic explanation.

## Specific Prompt Patterns

- **"What EXACTLY do they prove?"** — Forces theorem-level precision with quantitative statements.
- **"What EXACTLY is the [inequality / curvature formula / constant]?"** — Extracts individual factor-level derivations, not just the final bound. Produced K_S = N/2 − 8N(d-1)β derivation including the 2+6=8 combinatorial breakdown.
- **"What specifically fails for [extension/generalization]?"** — Forces mathematical precision about why techniques break down. Produced the four-layer finite→continuous obstruction analysis.
- **"Honest assessment of proximity to proof"** — Combined with rigor-level expectation, yielded an authentic 20-50+ year timeline rather than vague optimism.
- **"What is the exact coefficient?"** — When an exploration reports a qualitative disagreement (e.g., "SED and QM disagree at O(beta^2)"), ask for the *specific numerical value* where they diverge. The SED exploration reported the disagreement exists but didn't extract the specific SED coefficient, which would have been useful context for subsequent computations. (SED strategy-001 meta-exploration-002)
- **"Is X better than Y?"** — When the paper itself may directly answer a comparative question (e.g., "is β₀(4) > 1/24?"), ask it as a direct comparison rather than asking for descriptions of each in isolation. The paper's Remark or comparison section will often give the definitive answer. Produces a forced verdict that the strategizer can act on immediately.
  - **yang-mills strategy-002 exploration-003** — The goal asked "is β₀(4) > 1/24?" The explorer found the paper's own Remark 1.1 which directly answers: "No, the Sept 2025 paper achieves a larger β range." This was the key strategic fact, extracted by asking the comparative question rather than asking for parallel descriptions.

## Specific Prompt Pattern for Literature Searches

For literature search explorations, specify: **"For each paper, give one verdict line: what it computes and whether it contains the result."** This produces a scannable reference table rather than a narrative summary. The paper-by-paper format is the right rigor level for this task type — it's auditable and directly usable by the strategizer.

- **classicality-budget strategy-002 exploration 002** — The paper-by-paper verdict format (18 papers, one verdict per paper with "what it computes" + "contact with the three constants") produced a scannable reference that could be directly cited in a novelty claim. The goal explicitly requested this format, which is why it was delivered.

## Variant: Request Analytical Formulas Alongside Numerics

When a computation produces numerical results (correlators, spectra, discrepancies), **explicitly ask the explorer to derive exact analytical formulas when possible, then verify numerics against them.** Analytical formulas: (1) eliminate all doubt about numerical results; (2) provide physical insight (e.g., which terms dominate); (3) are publishable in a way that pure numerics are not.

- **thermal-time strategy-002 exploration-002** — The explorer derived exact closed-form expressions for both correlators: C_QM(t) = (2n_bar+1)/(4ω) × [cos(ω_+ t) + cos(ω_- t)] and C_global(t) = (2n_bar+1)/(2ω) × cos(ωt). The numerics were then verified against these formulas to 3e-13 relative error. This eliminates all doubt about the 102% discrepancy at λ=0.3 — it's analytically exact, not a numerical artifact. Future goals should explicitly request: "Derive the analytical formula if possible, then verify numerics against it."

**Specific sub-pattern: Request Analytic Derivation of Power-Law Coefficient**

When an exploration fits a power-law numerically (e.g., ‖ΔK_A‖ ~ λ^α or Δτ/τ ~ λ^α), **explicitly ask for the analytic derivation of the coefficient** — not just the numerical fit. The analytic coefficient (1) confirms the physical mechanism; (2) is more convincing to skeptical readers than a curve fit; (3) often reveals unexpected structure (e.g., which terms vanish and why).

- **thermal-time strategy-001 meta-exploration-002** — E002 fit ‖ΔK_A‖ ~ 42.1 × λ^{1.998} numerically. The explorer also gave the analytic argument for O(λ²): O(λ¹) vanishes because ⟨q_B⟩_thermal = 0 (odd-moment zero). This analytic proof is more convincing than the 1.998 fit — it explains WHY the exponent is exactly 2, not approximately 2. The strategizer note: "When you find O(λ²) correction, identify coefficient analytically — the numerical 0.68 is useful but the analytic formula (from second-order Duhamel) would be more convincing."

**Pattern:** "Fit the power law numerically. Then derive the leading coefficient analytically from the perturbative expansion. Identify which mechanism causes the O(λ¹) term to vanish (if relevant). Report: numerical fit α, analytic prediction, and the mechanism."

Apply when: any observable is fit to a power law in a coupling constant or small parameter, and the exponent is consistent with an integer (α ≈ 1.99 → probably exactly 2). Also apply when: any two-oscillator, lattice, or toy-model computation produces numerical correlators — the closed-form is often derivable and immensely more valuable than the numerics alone.

## When to apply

Any exploration that aims to produce a definitive technical map of a research program, proof structure, or theorem chain. Especially important when the goal is to identify the *precise* stopping point of existing work (as opposed to a general sense of "what's been done"). The "what specifically fails" pattern is particularly powerful for understanding structural vs. technical obstructions. Less important for broad landscape surveys where depth is less critical than coverage.
