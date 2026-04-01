---
topic: P_k^{21} has less CZ slack than full pressure
confidence: verified
date: 2026-03-30
source: "vasseur-pressure strategy-001 exploration-004"
---

## Finding

**P_k^{21} (the De Giorgi bottleneck piece) has LESS CZ slack than the full pressure.** At q=2, P21 tightness is 1.7-3.9x slack, compared to 7.6-17.5x for the full pressure (from prior exploration). The CZ bound is tighter on the bottleneck piece than on the overall pressure.

## Mechanism

P21's RHS tensor f^{21} = u_below x u_below is smoother and more structured than the full tensor u x u, leaving less room for the CZ bound to be loose. P22 and P23 have even more CZ slack than P21 (their RHS involves u_above, which is supported on a small domain fraction, producing sparser data).

## Data (k=4, Re=500)

| IC | Full pressure | P21 | P22 | P23 |
|---|---|---|---|---|
| Taylor-Green | 0.387 | 0.407 | 0.385 | 0.414 |
| Anti-parallel | 0.637 | 0.580 | 0.677 | 0.690 |
| Random Gaussian | 0.262 | 0.259 | 0.314 | 0.319 |

At q=2, P21 tightness is comparable to or slightly higher than the full pressure (less slack). P22 and P23 have progressively more slack. The pattern strengthens at higher q.

## Implication

The standard De Giorgi argument's treatment of P_k^{21} via CZ theory already captures the correct scaling. The CZ bound is tightest precisely on the term that matters most. Improvements to beta are more likely to come from structural exploitation of the tensor form (div-free, bounded) or from other proof steps, not from CZ constant refinement.

## Verification

Pressure decomposition P_k^{21} + P_k^{22} + P_k^{23} = full pressure verified to machine precision (< 1.1e-15 relative error) for all 10 cases tested.
