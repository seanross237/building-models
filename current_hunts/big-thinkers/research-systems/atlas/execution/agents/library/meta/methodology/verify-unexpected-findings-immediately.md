---
topic: Verify unexpected major findings immediately with a targeted stress-test exploration
category: methodology
date: 2026-03-27
source: "yang-mills strategy-002 meta-exploration-s002-005, meta-exploration-s002-006"
---

## Lesson

When a computation produces an unexpected major finding — one that changes the strategic picture — design an immediate stress-test exploration to verify and strengthen it. The verification should test the most plausible failure modes (different dimension, adversarial configurations, larger lattice). Don't add it to a queue; run it as the next exploration.

## Evidence

- **yang-mills strategy-002 exploration-005** — Found that SZZ Lemma 4.1 Hessian bound is 12-45× loose on a 3D lattice. This was unexpected (predicted tight, found ~45× slack at β=0.02). The natural failure mode: maybe only loose in 3D, not the physically relevant 4D case.

- **yang-mills strategy-002 exploration-006** — Immediate 4D follow-up (next exploration after E005). Result: slack is *even larger* in 4D (138× vs 45× at β=0.02). Also tested adversarial configurations (gradient ascent, aligned configs, eigenvalue search) — all gave slack ≥176×. The finding is robust across both dimensions and both Gibbs and non-Gibbs configurations.

## Protocol for Designing the Stress-Test

When an unexpected finding emerges from exploration N:

1. **Identify the most plausible failure mode.** "The result might be wrong because ___." For dimension-specific findings: "maybe it's only true in d≠4." For Gibbs-typical measurements: "maybe adversarial configurations saturate the bound."

2. **Design exploration N+1 to test that failure mode.** One key change (e.g., d=4 instead of d=3), plus adversarial search if the original only measured typical configurations.

3. **Include a direct comparison table.** Show the new result vs. the prior result at the same β. This makes the change immediately visible and prevents narrative drift.

4. **Treat the outcome as decisive.** If the finding survives the stress test, it's robust. If it fails, it reveals the scope limitation — equally valuable.

## What to Include in the Verification Goal

- Direct match to original setup (same lattice size, same β values) so comparison is clean
- The change being tested (e.g., "run this in 4D with d=4 in the Hessian formula")
- Adversarial search (at minimum: random configs, gradient ascent, one structured approach)
- A table format that directly shows Original vs. Verification at each β
- "The prior result was X — confirm or refute"

## What NOT to Do

- Don't defer the verification to "later in the strategy." Unexpected findings devalue if they remain unverified.
- Don't just run the same exploration again (same dimension, same β, same config type). The point is to test failure modes.
- Don't combine the verification with another goal — keep it focused (see one-task-per-exploration.md).

## Why This Matters

An unverified unexpected finding is fragile: the strategizer may build on it, only to discover later that it was a dimensional artifact or sampling bias. A verified finding — even if it changes the quantitative answer — is solid ground.

In the yang-mills case: E005's 3D result (45× slack) was already a major finding. E006's 4D result (138× slack, adversarial ≥176×) upgraded it to a **structural result** that holds across dimensions and configurations. That upgrade happened in one targeted exploration.

## Relationship to Other Patterns

- Complements **decisive-negative-pivot.md**: when verification confirms the finding, continue building on it. When it reveals a failure mode, pivot.
- Complements **adversarial-explorations-need-null-hypothesis.md**: the adversarial search in the verification plays the null-hypothesis role.
- Contrast with **dual-mechanism-robustness.md**: that pattern is for finding independent physical mechanisms for the same result. This pattern is for stress-testing a single computation against its most plausible failure modes.
