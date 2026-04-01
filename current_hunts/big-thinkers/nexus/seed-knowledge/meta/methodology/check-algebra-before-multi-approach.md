---
topic: Pre-screen for algebraic inevitability before committing to multiple exploration approaches
category: methodology
date: 2026-03-27
source: "compton-unruh strategy-001 meta-exploration-007"
---

## Lesson

When a formula involves a ratio of two expressions with the same structural factor (e.g., both have
2π in the denominator), that factor cancels identically in the ratio. **No internal mechanism can
restore it.** Before designing multiple exploration approaches to derive the "missing factor," spend
one minute checking whether the cancellation is algebraically inevitable. If it is, don't send four
approaches — spend the time on the one external lead that might actually work.

## Evidence

**compton-unruh strategy-001 exploration-007** — Four independent approaches were tested to derive
the factor 1/(2π) from the T_U/T_dS ratio:
- Approach A: Angular averaging → no extra factor
- Approach B: Horizon area ratios → 1/4, not 1/(2π)
- Approach C: Entropy rate ratio → no extra factor
- Approach D: Quantum information route → wrong direction

All four failed. This was **algebraically inevitable**: T_U = ℏa/(2πck_B) and T_dS = ℏH₀/(2πk_B)
both have the same 2π in the denominator, so T_U/T_dS = a/(cH₀) with no 2π. The meta-learning note
states: "In retrospect, this was predictable — the ratio T_U/T_dS trivially cancels 2π. The time
would have been better spent on understanding why Verlinde's factor works."

## Generalizations

- **Ratio of same-formula expressions**: If T_U and T_dS both derive from ℏ/(2πk_B)×f(param),
  the 2π is in both numerator and denominator and cancels.
- **Power-law combinations**: If both terms go as x^n, the ratio goes as 1 (constant), and no
  exploration will find an n-dependence.
- **Dimensional analysis first**: Check whether the desired factor even has the right dimensions to
  appear in the ratio before exploring mechanisms.

## The Pre-screening Question

Before designing approaches to "derive factor X from formula Y/Z":

> Can X appear in Y/Z at all, given the algebraic structure of Y and Z?

If Y and Z have the same structural factors, the answer is often NO. Answer this question analytically
before committing to exploration budget.

## Relationship to Other Entries

- `decisive-negative-pivot.md` — When a result is a hard kill (>10 OOM discrepancy or algebraic
  inevitability), pivot immediately; don't explore variants.
- `multi-ansatz-sweep-pattern.md` — When you genuinely don't know which of 2–4 similar candidates
  works, test them all. But first verify the ansatze are not all algebraically ruled out.
- `specify-failure-paths.md` — The formalism-applicability pre-screening variant: ask "can this
  formalism yield the modification in principle?" before committing. This entry is the algebraic
  version of that principle.
