# Meta-Learning Note — Exploration 004 (Strategy-002)

**Date:** 2026-03-27
**Task:** Phase 2 root cause synthesis — literature survey + claim assessment

## What Worked Well

1. **Giving the explorer a complete Phase 1 summary** (all three E001-E003 findings, with exact numbers) was essential. The explorer could evaluate claims against actual data without having to re-run simulations.

2. **Asking for specific claim assessments (A/B/C/D)** with separate evaluation criteria worked very well. The explorer addressed each one clearly.

3. **Listing specific authors to search** (Boyer, de la Peña-Cetto, Pesquera-Claverie, Santos, Nieuwenhuizen) gave a clear search agenda. All were found.

4. **Including "Fix A/B/C" as evaluation criteria** led to crisp analysis — none are in literature, but Fix A worsens things and Fix B breaks Lorentz invariance. Having named fixes made the evaluation concrete.

## What Didn't Work Well

1. **Rate limit interruption** — the explorer hit a rate limit mid-way, requiring a restart nudge. This added ~90 minutes of delay. For future long synthesis tasks, consider splitting into two explorations (literature survey + claim assessment separately).

2. **The "ω_local = √2 universality" insight** was discovered by the explorer, not anticipated by the goal. This is a nice surprise — but it means I should have asked the explorer to verify the Γ formula interpretation earlier.

## Key Unexpected Finding

ω_local at the double-well potential minimum is ALWAYS √2 for V = -½x² + ¼λx⁴ (with ω₀=1), regardless of λ. This means E_zpf_local = ħω_local/2 = ħ√2/2 is a constant for this entire potential family. The crossover at λ=0.25 is NOT a special λ — it's just where S_WKB happens to equal 1.41 ≈ E_zpf/ħ.

## Scope Assessment

Scope was appropriate. 4 sections (literature, root cause, fixes, claims) was manageable for one synthesis exploration. The 400-line report is comprehensive without being excessive.

## Recommendations

- For future synthesis explorations: ask the explorer to explicitly look for "universality conditions" or "special parameter values" where SED accidentally agrees with QM
- Split long synthesis explorations if there's risk of rate limit: Part A = literature survey only, Part B = claim assessment + recommendations
