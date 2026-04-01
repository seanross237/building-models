---
topic: Always check if the bottleneck tool can be bypassed, not just improved
confidence: verified
date: 2026-03-30
source: "vasseur-pressure s2-meta-exploration-005"
---

## Lesson

When a bottleneck tool (e.g., CZ theory for pressure bounds) limits progress, the default strategy is to improve the tool or find a better variant. But the higher-value question is: **can you bypass the tool entirely?** S2-E001 through S2-E005 all accepted CZ as the pressure tool and tried to improve other things around it (Chebyshev, commutator, compensated compactness, LP decomposition). Only E005's "unexpected findings" section identified "non-CZ pressure handling" as a direction. This should have been identified earlier.

## Protocol

When a bottleneck tool is identified:

1. **First question:** Can we avoid using this tool at all? What framework/approach does not require it?
2. **Second question:** If we must use it, is there a fundamentally different tool for the same job (not a variant of the same tool)?
3. **Third question (last resort):** Can we improve the tool's output within its existing framework?

S2-E001 through S2-E005 spent 5 explorations on question 3 (improving CZ or working around it). The strategizer should have asked question 1 after S2-E001 showed all CZ-based routes are tight.

## Example

- **Bottleneck:** CZ theory gives ||P^{21}||_{L^q} <= C ||u^below tensor u^above||_{L^{q/2}}
- **Question 3 attempts (5 explorations):** Chebyshev improvement (circular), commutator (blocked by three obstructions), LP decomposition (Bernstein kills it)
- **Question 1 (should have been asked earlier):** What if we use a non-CZ pressure estimate? E.g., nonlinear dissipation lower bounds that use the NS equation directly, or topological constraints that bypass pressure entirely.

## Distinct From

- **ask-what-replaces-the-bottleneck** — that asks what the new bottleneck is after reformulation; this asks whether you need the bottleneck tool at all
- **decomposition-audit-before-attacking-barrier** — that identifies which step is tight; this questions whether the whole proof structure is the right framework
- **decisive-negative-pivot** — that is about when to stop; this is about what direction to go (bypass vs. improve)
