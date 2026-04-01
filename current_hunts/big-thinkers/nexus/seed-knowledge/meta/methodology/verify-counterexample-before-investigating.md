---
topic: When finding a counterexample, verify it against the exact problem statement before investigating consequences
category: methodology
date: 2026-03-29
source: "yang-mills-conjecture strategy-002 meta-exploration-007"
---

## Lesson

When an exploration discovers what appears to be a counterexample to a conjecture, the **first priority** is verifying the counterexample against the exact problem statement — not investigating its consequences, implications, or structural meaning. Specifically: verify that the mathematical object being computed matches the definition in the conjecture. A false counterexample is worse than no result — it can derail strategy (pivoting away from a valid proof program) or contaminate the library with incorrect claims.

## Evidence

- **yang-mills-conjecture strategy-002 exploration-007** — Gradient ascent found λ_max(M(Q)) ≈ 16.08, apparently exceeding the bound of 16. The exploration then investigated consequences (multi-scale tests, failed proof approaches, structural insights) and concluded "λ_max(M(Q)) ≤ 16 is FALSE." However, the meta-note identified that the B_p formula used (B_p(a) = Q₁a₁ + Q₁Q₂a₂ − ...) may differ from the MISSION's adjoint representation formula (Ad(Q)(v) = QvQ⁻¹). The "counterexample" was never cross-checked against the exact problem statement's formula — a critical gap, since the existing library already documents that wrong B_□ formulas produce spurious violations (F = 16.76 on L=2 with the original wrong formula). The finding remains UNRESOLVED.

## Protocol

When a computation appears to violate a conjecture:

1. **Stop.** Do not investigate consequences or implications.
2. **Re-read the exact problem statement.** What mathematical object is the conjecture about? What is the precise formula?
3. **Verify your computation matches.** Does your code compute the same operator/quantity as the conjecture? Check representation (fundamental vs adjoint), convention (left vs right action), normalization, and sign conventions.
4. **If there is any formula ambiguity, resolve it first.** Compare your formula against the reference implementation or derive it independently from the problem statement.
5. **Only after verification: investigate consequences.**

The cost of this verification (30 minutes) is trivial compared to the cost of a false negative on a proved conjecture — which can redirect an entire strategy.

## Relationship to Other Patterns

- Complements **include-trivial-control-checks.md** (which validates code correctness within a computation; this validates alignment between the computation and the problem statement)
- Complements **verify-goal-claims-before-delegating.md** (which prevents wrong goals from the strategizer side; this prevents wrong counterexample claims from the explorer side)
- Distinct from **verify-unexpected-findings-immediately.md** (which is about designing a follow-up stress-test exploration; this is about within-exploration prioritization before any follow-up)
