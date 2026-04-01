---
topic: Special-case proof structure reveals what's needed for the general case
category: methodology
date: 2026-03-29
source: "yang-mills-conjecture strategy-002 meta-exploration-004"
---

## Lesson

When a proof succeeds for a special case, **analyze WHY it worked** — the specific structural property that made the proof easy. Then frame the general case as: restore that property + bound the deviation. This immediately identifies both the correct proof strategy and the key quantity to bound.

## Evidence

**yang-mills-conjecture strategy-002 exploration-004** — Proving sum_S ≥ 0 (a bilinear form in u, v) was intractable in general. But for T on rotation axes (the null eigenvector of the base case — the "most dangerous" direction), the proof was clean:

1. **Why it works on axes:** R_μ^T T_μ = c_μ n_μ (since R fixes its axis), so u_{μ,ν} = v_{μ,ν} = c_μ n_μ − c_ν n_ν. The bilinear form 2·u^T(I−D)v becomes the quadratic form 2·u^T(I−D)u = 2f(D,u) ≥ 0.
2. **What this reveals for the general case:** The deviation u − v = −(I − R^T)T measures how far T is from a rotation axis. The baseline term already contains f(R, T) terms that involve the same (I − R) structure. The natural approach is to show the baseline absorbs the bilinear correction.
3. **The key quantity:** ||u − v|| = ||(I − R^T)T||, which vanishes on axes and grows with how "off-axis" T is — but so does the baseline f(R, T).

Without the special-case proof, none of this structure would be visible. The 7 failed approaches for the general case (convexity, matrix domination, perturbation, Gershgorin, VCBL variants) all attempted to prove the bound without leveraging this structural insight.

## The Pattern

1. **Prove the special case.** Identify a subspace or parameter regime where the conjecture is provable.
2. **Identify the structural property** that made the proof work (e.g., u = v, symmetry, rank reduction, sign definiteness).
3. **Measure the deviation** from that property in the general case (e.g., ||u − v||).
4. **Check whether existing terms absorb the deviation** (e.g., the baseline contains f(R, T) terms of compatible structure).
5. **Design the next exploration** around this specific strategy, not a shotgun of approaches.

## Distinction from Related Entries

- **`work-backward-from-constraint.md`** — That entry is about framing tasks backward from a constraint. This entry is about extracting proof strategy from a special-case proof structure. Different trigger (successful special case vs. known constraint).
- **`characterize-maximizers-not-just-bounds.md`** — Related spirit (structural characterization reveals proof routes), but that entry is about characterizing WHERE the bound is tight, while this is about analyzing WHY a proof works in a subcase and generalizing the mechanism.
- **`decisive-negative-pivot.md`** — That entry is about pivoting after failure. This entry is about leveraging success in a special case to design the general approach.
