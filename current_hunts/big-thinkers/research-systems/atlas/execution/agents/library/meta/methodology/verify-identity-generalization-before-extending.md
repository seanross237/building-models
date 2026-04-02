---
topic: Verify that key identities generalize before extending a proof to a larger space
category: methodology
date: 2026-03-29
source: "yang-mills-conjecture meta-exploration-008, yang-mills-conjecture strategy-002 meta-explorations 003, 004"
---

## Lesson

When extending a proof from a subspace to a larger space, **FIRST check whether the key identities the proof relies on still hold in the larger space.** An identity that is exact on the subspace may fail completely on the full space — and this failure immediately rules out the original proof technique, saving an entire exploration from a dead end.

## Evidence

**yang-mills-conjecture exploration-008** — Attempted to extend the E006 staggered-mode proof (which used a trace identity: c + Tr(P) = 64 independently of Q) to the full 9D eigenspace. The trace identity **fails** for general spatial patterns s: Tr(M_total(s)) varies by factor ~3 over Q. This was discovered mid-exploration after substantial computation. Had the trace identity been tested at the outset (a quick 2-line computation), the approach could have been ruled out immediately and the exploration could have focused on alternative proof structures (gap decomposition, SDP/SOS) from the start.

## The Check

Before designing an exploration to extend Proof A (which works on subspace S) to the full space V:

1. **List the key identities** that Proof A depends on (trace identities, budget identities, norm conservation, etc.)
2. **Test each identity on V** with 3–5 random examples from V \ S
3. **If any identity fails**, the proof technique cannot generalize — pivot to a different approach immediately

Cost: near-zero (a few numerical evaluations). Payoff: avoids wasting an entire exploration on a provably dead approach.

## Variant: Verify Conjectures Adversarially Before Proving Them

Before investing an exploration in proving an intermediate conjecture (e.g., LEMMA_D ≥ 0), first verify it adversarially — not just with random tests. In high-dimensional spaces (30D+), random sampling has poor coverage and can miss counterexamples entirely.

**yang-mills-conjecture strategy-002 exploration-003** — LEMMA_D appeared to hold under 200K random tests. Adversarial optimization found min eigenvalue = -2.13. An entire exploration was designed to prove LEMMA_D, which is false. Had adversarial testing been run first (in the prior exploration E002), the proof attempt could have been redirected to the correct target (sum_S = LEMMA_D + LEMMA_RDR ≥ 0) immediately.

**Principle:** Before designing an exploration to prove X, include an adversarial test of X in the preceding exploration. See also `budget-adversarial-for-high-dim.md`.

## Variant: Verify Predecessor Exploration Claims Before Building On Them

When an exploration builds on results from a previous exploration in the same chain, **independently re-derive or verify the predecessor's key claims** rather than assuming them. Previous explorations can contain errors that propagate into the current work.

**yang-mills-conjecture strategy-002 exploration-004** — E003 claimed "sum_S(D=I) = 0 for all R, T." E004 discovered this is **FALSE** — the correct statement is sum_S(D=I) ≥ 0 with min eigenvalue = 0. The corrected identity (sum_S = 6Σf + |ΣR^T T|²) is strictly stronger and enabled both the master identity decomposition and the Critical T theorem. Had the error not been caught, the proof strategy would have been built on wrong foundations.

**Principle:** When the current exploration's starting point is a result from the previous exploration, verify it numerically with fresh code (not copied) before using it as a foundation. This is especially important for equality claims (= 0) vs. inequality claims (≥ 0) — the gap between them often contains the key insight.

## Distinction from Related Entries

- **`check-algebra-before-multi-approach.md`** — That entry is about pre-screening whether a factor can appear in a ratio formula (algebraic inevitability). This entry is about testing whether proof-specific identities survive generalization to a larger space. Different triggers, different checks.
- **`verify-goal-claims-before-delegating.md`** — That entry is about verifying factual claims before citing them in GOAL.md. This entry is about testing mathematical identity generalization before committing to a proof strategy.
- **`include-trivial-control-checks.md`** — Related spirit (cheap check prevents wasted work), but that entry is about code validation controls; this is about mathematical identity generalization.
