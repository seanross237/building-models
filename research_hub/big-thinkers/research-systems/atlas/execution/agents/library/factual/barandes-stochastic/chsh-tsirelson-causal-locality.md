---
topic: barandes-stochastic
confidence: provisional
date: 2026-03-28
source: barandes-stochastic strategy-001 exploration-004, exploration-005 (adversarial review)
---

# CHSH/Tsirelson Bound from Causal Local ISP

## Core Result

Barandes, Hasan, & Kagan (arXiv:2512.18105, Dec 2025) derive the Tsirelson bound |<C>| <= 2sqrt(2) from causally local **unistochastic** processes, without assuming Hilbert space axioms.

**Key distinction:** No-signaling alone permits PR boxes (violations up to 4). Causal locality of the *underlying dynamics* (not just observable statistics) restricts to the quantum Tsirelson bound. This identifies which postulate does the work.

## Technical Structure

1. **Amplitude matrix Theta** (Eq. 17): Theta_{qt,q0} = e^{i*theta} * sqrt(p(qt|q0)). The phases theta are **arbitrary** — NOT derived from ISP axioms. Any stochastic matrix admits this representation.
2. **Unistochastic specialization:** The paper specializes to Theta = U (a unitary matrix). This yields p(qt|q0) = |<qt|U|q0>|^2 — **exactly the Born rule.**
3. **Causal locality** defined stochastically: system R does not causally influence system Q if p(q_t|q_0,r_0) = p(q_t|q_0). This is dynamical (constrains the stochastic kernel) rather than just marginal (constrains statistics).
4. Causal locality implies factorization of joint amplitude matrices: (AB)_{xy} = A_x tensor B_y
5. Factorization + Born rule → CHSH operator satisfies |<C>| <= 2sqrt(2) (standard quantum argument in stochastic language)

## Circularity Analysis (E005 Adversarial Review)

**Circularity is REAL and acknowledged by the authors.** The logical structure of the proof is:

```
ASSUME: (1) Dynamics are unistochastic [= Born rule QM]
        (2) Causal locality [= tensor product factorization]
DERIVE: Tsirelson's bound [= standard quantum bound]
```

This IS the standard Tsirelson (1980) proof in stochastic language. The stochastic causal locality condition translates directly into the tensor product factorization A_x ⊗ B_y used in Tsirelson's original argument.

**Paper's own acknowledgment (Section 5):** "We believe that the nontrivial structure of such matrices may provide a route toward a **novel proof** of Tsirelson's bound... **bypassing the need for explicit use of the quantum side of the stochastic-quantum correspondence.**" The authors themselves acknowledge the current proof DOES use the quantum side (= unistochastic = QM) and the truly novel proof is aspirational.

**Circularity is partial:** The *mathematical* content imports Born rule QM (full circularity for the result). The *physical interpretation* adds something — causal locality stated in stochastic terms without presupposing Hilbert spaces.

## Causal Locality vs. No-Signaling (CONFIRMED)

Causal locality is **strictly stronger** than no-signaling:

- **No-signaling** (observable level): P(q|x,y) = P(q|x) — constrains joint probability distributions over observables only. PR boxes satisfy this.
- **Causal locality** (dynamical level): p(qt|q0,r0) = p(qt|q0) — constrains the stochastic kernel itself. Requires that the dynamical law governing Q's evolution does not depend on R's initial configuration.

Any causally local system satisfies no-signaling (trivial from marginalization). The converse FAILS: PR boxes satisfy no-signaling but cannot be modeled by causally local stochastic dynamics. This is the paper's **genuine and correct** contribution.

**Philosophical addition:** Standard QM provides no language for causal locality at the microphysical level (Copenhagen refuses to assign dynamics to individual measurement events). The stochastic framework provides such a language.

## Prior Art Assessment

| Reference | What it does | Relation to Barandes |
|-----------|-------------|---------------------|
| Tsirelson (1980) | CHSH bound from tensor product structure | SAME result, QM language |
| Buhrman-Massar (2005) | Causality language within QM → CHSH bound | SAME result, causality framing |
| Popescu-Rohrlich (1994) | NS alone insufficient → PR boxes exist | Motivating negative result |
| Pawłowski et al. (2009) | Information causality → Tsirelson | Different non-QM derivation |
| NPA hierarchy (2007-2008) | Quantum correlations via SDP | Mathematical characterization |

**Verdict:** Mathematical result is full prior art (Tsirelson 1980). Conceptual framing (dynamical causal locality stated without Hilbert spaces) is genuinely new.

## Open Question (Not Yet Answered)

**Can a causally local but non-unistochastic ISP produce correlations beyond Tsirelson?** This is the critical open question, explicitly left unresolved by the paper. If NO, then ISP causal locality alone explains Tsirelson without assuming QM — this would be the genuinely novel proof the authors aspire to. If YES, then even the stochastic framework doesn't solve the problem.

## Assessment

**Strongest claim in the Feb 2026 cluster.** Survival classification: PARTIALLY SURVIVES.

- **Mathematical result:** Does NOT survive as novel (Tsirelson 1980 prior art)
- **Explanatory framing:** PARTIALLY SURVIVES (causal locality formulation is genuine, but translates immediately to tensor product factorization)
- **Future claim (bypassing quantum side):** NOT YET PROVEN

## No New Predictions

This is a foundational derivation, not a computational tool. Working physicists compute Bell correlations using the standard quantum formalism.
