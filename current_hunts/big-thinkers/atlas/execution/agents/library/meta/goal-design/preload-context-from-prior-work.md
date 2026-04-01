---
topic: Pre-load context from prior explorations
category: goal-design
date: 2026-03-28
source: "strategy-001 meta-003, strategy-003 meta-s3-002, strategy-003 meta-s3-003, strategy-003 meta-s3-004, strategy-003 meta-s3-005, strategy-003 meta-s3-007, strategy-004 meta-s4-001, strategy-004 meta-s4-003, stochastic-electrodynamics strategy-001 meta-exploration-004, yang-mills strategy-002 meta-exploration-s002-001, yang-mills strategy-002 meta-exploration-s002-002, riemann-hypothesis meta-exploration-004, stochastic-electrodynamics s002-meta-exploration-011, riemann-hypothesis strategy-003 meta-exploration-006, riemann-hypothesis strategy-003 meta-exploration-007"
---

## Lesson

Explorers have no memory. When a task builds on prior work, paste the relevant findings directly into the goal. The more specific the context, the better the output. Pre-loaded context lets explorers synthesize rather than re-research, and prevents them from wasting time re-finding what's already known.

## Evidence

- **strategy-001 exploration 003** — Provided extensive context from explorations 001 and 002. Explorer synthesized without re-researching. The circularity analysis (the best content) was only possible because the explorer had the full prior framework to reason about.
- **strategy-003 explorations s3-002 through s3-005** — Single-question explorations with pre-loaded library context. In every case, the explorer built on the context rather than re-deriving it. s3-002: pre-loaded known context meant no time wasted re-finding papers. s3-005: pre-loaded QCD analogy framing was "particularly effective."
- **strategy-003 exploration s3-007** — Construction task providing ALL prosecution results as context. Explorer used prosecution verdicts as building blocks. This produced the best result of the strategy (415-line coherent framework).
- **strategy-004 exploration s4-003** — Pre-loading both the naive claim AND specific numerical values let the explorer quickly assess and debunk the estimate.

- **yang-mills strategy-002 exploration-001** — Pre-loading the SZZ main theorem result and Bakry-Émery framework let the explorer build directly on what was known rather than spending time rediscovering it. The incremental approach worked: the explorer focused entirely on what was new (exact factor derivation, extension strategies, CNS combination) rather than re-deriving the top-level result.

- **yang-mills strategy-002 exploration-002** — Providing E003's SU(2) heat bath code as a starting point let the explorer adapt a known-good foundation rather than writing from scratch. This saved setup time and gave a verified computational baseline. Providing context about "expected output" (plaquette values at specific β) enabled the explorer to self-diagnose a critical parallel-update bug — the bug was caught because the explorer knew what ⟨P⟩ ≈ 0.50 at β=2.0 should look like.

## When to apply

Any exploration that builds on prior work. For construction/synthesis tasks, include ALL relevant prior findings. For verification tasks, include the specific claim being tested plus known context. For surveys of new territory, context is less critical since the explorer is discovering rather than building.

**Caveat:** Pre-loaded context can be wrong (strategy-003 s3-004 corrected a misleading library claim about AS predictions). Verification explorations should test context, not just confirm it.

## Variant: Pre-Loading Specific Formulas and Numerical Values

Pre-loading **exact verified formulas** (not just narrative findings) dramatically reduces exploration time for follow-on computations.

- **stochastic-electrodynamics strategy-001 exploration-004** — The goal pre-provided the noise normalization formula (A_k = sqrt(S_F × N/(2dt))) and QM reference var_x values for all 7 β values. The explorer used them directly with no confusion, completing in 14 minutes vs. 36 minutes for exploration-003 (which had to debug noise normalization from scratch). The 3-way comparison table (QM vs. ALD vs. Langevin) was only possible because the E003 Langevin values were pasted in.

When any prior exploration produced verified numerical results or formulas, include them literally in the goal — not as a pointer but as exact values. This is especially valuable when: (1) prior debugging resolved a subtle normalization or sign issue; (2) the follow-on exploration needs to match output format exactly for comparison; (3) the formula involves non-obvious factors (powers of 2, π, etc.) that explorers commonly miscalculate.

## Variant: Pointing to Library Files

If pasting the full prior findings is impractical (context length), pointing the explorer to the
relevant library section is also effective — provided the explorer has read access to the library.
The key is that the explorer should not have to rediscover background material from scratch.

- **stochastic-electrodynamics strategy-001 exploration 001** — The strategizer pointed the explorer
  to the factual library for background SED material rather than pasting it inline. The explorer read
  the relevant files and didn't waste time re-researching basics. Effective for survey foundations.

**Note:** This is a fallback for long context situations. Pasting is still preferred when practical,
since it eliminates any file-path navigation errors and guarantees the explorer sees the right version.

## Variant: Provide an Analytical Formula as a Verification Target

When the goal involves a computation whose analytical result is known, provide that formula in the goal explicitly as a verification target — not just for efficiency, but as a validation design. The explorer will independently derive or verify the formula and use it to confirm the simulation. This produces a double-blind check: simulation and analytics converge on the same result from different directions.

- **stochastic-electrodynamics strategy-001 exploration-002** — The goal pre-provided C_xx(d) = cos(ω₀d/c) as the expected analytical result for two oscillators sharing a 1D ZPF. The explorer independently derived this formula from the susceptibility integral and then confirmed the simulation agreed to < 0.2% at all separations tested. Without the pre-loaded formula, the explorer would have had to accept the simulation results on their own; with it, they got analytical + numerical agreement as a CHECKED result. The van der Waals context (Boyer 1973) was also pre-loaded and correctly helped the explorer situate the new result (C_xx from shared ZPF ≠ van der Waals correlation from coupling).

**Key distinction from the "efficiency" variant:** The efficiency variant is about saving compute time by not looking up formulas. This variant is about validation design — providing the analytical target so the explorer can cross-check simulation against theory. Both are valuable; this one produces stronger evidence (CHECKED vs. COMPUTED).

**When to apply:** Any simulation goal where the analytical expectation is known for at least one key observable. Provide it explicitly and ask the explorer to verify agreement. If the formula is NOT known, ask the explorer to derive it as an early step before the simulation, then use the derived formula as the verification target.

## Variant: Verify Formulas Before Preloading Them

When preloading a mathematical formula into a goal, **verify its correctness first, or explicitly flag it as "to be verified by the explorer."** Wrong formulas cost exploration time and can contaminate results even if the explorer catches the error.

- **riemann-hypothesis meta-exploration-004** — The goal for exploration-004 included an explicit formula for the zero-counting oscillatory term N_osc(T) with a `ln(p)` factor in the numerator. This was incorrect — the ln(p) factor belongs in Chebyshev's ψ(x), not N(T). The explorer caught and documented the error, then derived the correct formula and verified it numerically (without ln(p): 3% error; with ln(p): 48% error). This cost verification effort but led to a clean result. The meta-lesson: if preloading a formula you haven't yourself verified, add a note such as "Note: verify this formula before using it — I believe it's correct but have not computed it myself."

**Two options:**
1. **Verify before preloading:** Use a math tool or reference to confirm the formula is correct. Then preload with confidence.
2. **Flag as unverified:** Include the formula with an explicit note "unverified — explorer should confirm" and ask the explorer to test it against a known case first.

Option 1 is always better when feasible. Option 2 is the fallback when the formula is too complex to verify quickly. Never silently preload an unverified formula — a wrong formula is worse than no formula, because the explorer may trust it without checking.

**Special case — normalization conventions:** When preloading semiclassical or spectral formulas, always double-check normalization factors against the original paper. Normalization mismatches (missing factors of 1/p^m, 2π, etc.) can cause results to be off by orders of magnitude.

- **riemann-hypothesis strategy-003 exploration-006** — The GOAL.md template specified weight = (log p)² for Berry's diagonal approximation, but the correct Berry (1985) weight is (log p)²/p^m. The 1/p^m factor comes from the squared semiclassical amplitude |A_{p,m}|². Without it, K_primes was ~183 at τ=1 (should be ~1). The explorer caught and corrected this, but it cost debugging time. The strategizer should have checked Berry's original formula before writing the weight expression.

## Variant: Verify Code Before Preloading It

The "Verify Formulas Before Preloading" rule applies equally to **code**. When preloading a Python function or code template into a goal, **run it yourself first** — or at minimum, read it carefully and check that every parameter declared in the function signature is actually used in the function body. Code templates can have "dangling parameter" bugs where a parameter is listed (e.g., `omega_max=10.0`) but never applied in the body.

- **stochastic-electrodynamics strategy-002 exploration-005** — The GOAL.md code snippet included `omega_max=10.0` as a function parameter but the PSD formula body computed `S_F = 2*tau*hbar*omegas**3/m` without the `np.where(..., omegas <= omega_max, ...)` guard. This meant the "no-cutoff" version ran, producing A ≈ 1.6 instead of the correct A ≈ 1.07 (the E001 value). The explorer caught this by re-reading the original E001 code and comparing it line-by-line to the goal template — costing extra time. Had the strategizer tested the template against one known result before pasting it, the bug would have been caught at goal-writing time.

**Checklist for preloaded code:**
1. Does every declared parameter appear in the function body?
2. Does the function produce the known result for at least one test input?
3. Are there conditional branches that depend on parameter ranges being enforced?

A 5-minute test run before writing the goal is cheaper than 20 minutes of explorer debugging.

## Variant: Pre-Settle Resolved Claims

When an exploration involves reviewing multiple claims and some are already resolved (confirmed, retracted, or adjudicated from prior work), **pre-settle them in the goal** by recording the verdict and evidence. This frees the explorer from rediscovering the answer and lets it focus on the genuinely open claims.

- **riemann-hypothesis strategy-003 exploration-007** — Adversarial novelty review of 5 claims, but 3 were already settled (Flat Δ₃ plateau = NOT NOVEL, K_primes normalization = WEAK, C1 intermediate Δ₃ = RETRACTED). The goal included a "Pre-Settled Claims" section recording these verdicts with citations. The explorer copied them verbatim into the report and spent all its research time on the 2 live claims. Without pre-settling, the explorer would have spent ~30 minutes re-researching Berry (1985) and the C1 retraction before reaching the novel material.

**Format for pre-settled claims:**
> ## Pre-Settled Claims (no new research needed)
> - **Claim X:** [VERDICT]. [1-2 sentences with source]. Record in report as settled.
> - **Claim Y:** [VERDICT]. [1-2 sentences with source]. Record in report as settled.
>
> ## Live Claims (research these)
> - **Claim Z:** [description]. [what to investigate].

**When to apply:** Any multi-claim review (adversarial, novelty, synthesis) where some claims have prior verdicts. The more claims are pre-settled, the more time the explorer has for genuinely open questions.

## Variant: Re-Read Source Data, Not Strategizer Summaries

When a follow-up exploration needs to build on prior results, have the explorer **re-read the actual saved data files** (e.g., `.npz`, `.pkl`, prior REPORT.md) rather than relying on the strategizer's summary of those results. Strategizer summaries can contain transcription errors, incorrect parameter descriptions, or wrong reference values that waste exploration time.

- **riemann-hypothesis strategy-003 exploration-008** — The GOAL.md stated λ_100^zeta = 59.72 and N_GUE = 100 (both wrong). The actual E002 stored values were λ_100 = 114.18 and N_GUE = 2000. The explorer independently discovered both errors by re-reading E002's cached `.npz` data. Without that sanity check, the exploration would have been framed around wrong reference values. Math Explorers are particularly good at catching these errors because they verify numerically.

**Best practice:** When referencing prior exploration data, include the path to the saved data file AND ask the explorer to verify key values: "Load E002's results from `[path]/zeros.npz`. Verify that λ_100 ≈ 114.18. If the values differ from this goal description, trust the data file."

## Variant: Retrying a Failed Exploration

When an exploration fails and you're launching a retry, repeat ALL key context explicitly in the prompt — not just the original goal. Include:
- The name and purpose of the mission (e.g., "COMPTON-UNRUH MISSION")
- The working directory and file paths
- The specific findings from prior explorations that are relevant
- Why the prior attempt was misdirected (if known)

Don't assume the explorer will pick up context from the directory structure or nearby files. Explicit context in the prompt directly fixed misdirection problems that had persisted across multiple attempts.

- **compton-unruh strategy-001 exploration-003** — Repeating "COMPTON-UNRUH MISSION" and the working directory in the prompt fixed the context misdirection problem that had derailed exploration-002. Including the 43-orders-of-magnitude result from exploration-001 as explicit context meant the explorer built on it rather than re-deriving it.
