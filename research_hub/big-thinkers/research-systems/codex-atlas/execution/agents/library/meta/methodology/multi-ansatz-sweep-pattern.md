---
topic: Multi-ansatz sweep pattern — test all mathematical variants in one pass
category: methodology
date: 2026-03-27
source: "compton-unruh strategy-001 meta-exploration-004, riemann-hypothesis s002-meta-exploration-005"
---

## Lesson

When a problem has a small number (2–4) of mathematically similar candidate ansatze, testing all of them in a single exploration is efficient and productive. It rules out N-1 candidates in one pass, identifies the correct form (if any), and produces a direct comparison table. This is distinct from "one-task-per-exploration" — the cognitive task is unified (evaluate a class of ansatze for one phenomenon) even though multiple formulas are tested.

## Evidence

- **compton-unruh strategy-001 exploration-004** — Three candidate mechanisms for deriving MOND-like behavior from the de Sitter thermal crossover were tested in one exploration: (1) naive entropic F ~ T_dS, (2) excess temperature F ~ T_dS - T_GH, (3) ratio m_i ~ T_U/T_dS. Results: (1) wrong sign — excluded; (2) MOND-like but 11× wrong scale, ad hoc; (3) exact MOND but physically unjustified. Testing all three in one pass was highly efficient: ruled out 2, identified 1, and the comparison itself (same physics, three different treatments, three different results) was a key scientific finding demonstrating that the identity alone doesn't determine the physics.

- **stochastic-electrodynamics strategy-001 exploration-007** — Four noise spectra (S_n(ω) = C_n × ω^n for n=0,1,2,3) were tested in one script for their effect on the ALD-SED anharmonic oscillator residual error Δe(β). Total compute: ~10 minutes. The sign-reversal result (n=3 positive Δe, n<3 negative Δe) was immediately obvious from the raw data tables before any curve fitting — no disambiguation step required. Produced a clean diagnostic comparison table (sign, α exponent, magnitude by spectrum). Note: the explorer skipped power-law fits for negative-Δe variants because the sign was opposite; the goal should have explicitly requested |Δe| ~ β^α for all variants regardless of sign (see `goal-design/specify-computation-parameters.md`). Also produced a sign-flip threshold: n* ≈ 2.61 (see `methodology/sign-flip-diagnostic-for-critical-thresholds.md`).

- **riemann-hypothesis strategy-002 exploration-001** — Seven constructions (GUE control + C1–C4 with variants) were tested in one exploration, with a clear primary success criterion (β > 1.5). All variants were screened in the same run; the best (C1, random phases) immediately satisfied the criterion while others were ruled out or classified (C3b=GOE, C2=construction failure, C4=Poisson). The combination of a clear quantitative threshold (β > 1.5) with a multi-construction sweep made the result unambiguous — there was no post-hoc interpretation required. Note: 7 constructions is near the upper limit; the two C2/C4 construction failures would have been preventable with a sanity check step (see `goal-design/require-matrix-sanity-checks.md`), but they didn't prevent the main result.

## When to Apply

- When a quantity can be modified in 2–4 algebraically similar ways (e.g., different combinations of the same variables)
- When the distinguishing criterion between variants is which gives the correct observed behavior
- When each variant requires roughly the same computational effort

## When NOT to Apply

- When variants require fundamentally different physical assumptions or mathematical frameworks (split into separate explorations)
- When there are >4 variants (exploration may become too broad; consider splitting by category)
- When the task is primarily about understanding the mechanism behind one variant (not comparison)

## Key Design Elements

1. **List all variants explicitly** in the goal. Don't leave it to the explorer to discover which variants exist.
2. **Provide a comparison table template** — ask for a direct side-by-side result summary.
3. **Ask for the failure mode of each** — not just which succeeds, but why the others fail. This produces diagnostic value even from the excluded variants.

## Variant: Dense Fine Sweep for Non-Monotone Behavior

When a parameter sweep might be non-monotone (e.g., the metric first increases then decreases), include a **fine sweep around the suspected extremum** in addition to the coarse initial sweep. A sparse sweep can miss the true maximum or significantly underestimate it.

- **riemann-hypothesis s002-meta-exploration-005** — Part B of the exploration swept Gauss sum prime p across 6 coarse values (p=97 to 99991). The coarse sweep showed non-monotone behavior peaking around p=997 (β=1.092). The explorer added a 21-prime fine sweep around p=809–1999, which (1) found the true maximum (β=1.154 at p=809 vs. β=1.092 at p=997), (2) confirmed that neighboring primes fluctuate by ±0.4 (much larger than expected), and (3) established definitively that GUE (β=2) is never reached and the hypothesis is refuted — not just probably wrong. The fine sweep transformed an "ambiguous negative trend" into a "definitive refutation."

**Design rule:** If the metric vs. parameter relationship is expected to be non-monotone or has a suspected peak, include a fine grid (5–20 points) around the suspected peak in the goal. State: "Also include a fine sweep of [5-20 primes] around [the expected peak region] to characterize the extremum."

## Relationship to Other Patterns

Distinct from `comparison-exploration-pattern.md` (which compares two approaches/frameworks). The multi-ansatz sweep is for systematically testing a family of mathematical variants of the same underlying physical idea in a single exploration.
