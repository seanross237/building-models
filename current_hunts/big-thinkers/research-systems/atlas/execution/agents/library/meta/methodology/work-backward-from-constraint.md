---
topic: Work backward from constraint to theory — productive framing for constructive explorations
category: methodology
date: 2026-03-27
source: thermal-time strategy-001 meta-exploration-002
---

## Lesson

For constructive explorations (where the goal is to derive a theory or prove a mathematical result), frame the task as "what theory satisfies this constraint?" rather than "what does this theory predict?" The "work backward" framing produces genuine mathematical results — including no-go theorems — by forcing the explorer to engage with constraints as constructive inputs rather than outputs.

## Evidence

- **thermal-time strategy-001 exploration-002** — The goal was framed as "work backward from the normalization constraint to determine what physical time must equal." This produced: (1) the explicit BW derivation pinning τ = β·t_modular; (2) confirmation from three papers with equation-level quotes; (3) the no-go theorem that TTH = QM if and only if K_A = βH_A + const·I (product state condition) — an unexpected result that the goal did not specify. The "work backward" framing converted a potentially vague normalization question into a precise constructive program.

## Structure of the Pattern

A "work backward" exploration has this structure:
1. **Identify the constraint** — what must the theory/formula/parameter satisfy? (e.g., "the normalization must recover known Rindler proper time")
2. **Derive what satisfies it** — work backward to find the unique value/formula/form compatible with the constraint
3. **Check consistency** — verify the result against independent cross-checks (other known cases, literature)
4. **Allow unexpected results** — the backward-inference process may yield no-go theorems or uniqueness results not anticipated in the goal

## Contrast with Forward Framing

**Forward:** "Compute the modular Hamiltonian and its flow, then compare to physical time."
- Risk: generates correct calculations that don't resolve the normalization question
- Likely output: lists of formulas without a definitive answer

**Backward:** "The normalization must be consistent with the Rindler proper time; derive what the normalization must be."
- Forces a definitive answer
- Produces the BW-anchored derivation as the primary output
- Unexpected byproduct: the condition for TTH = QM (if and only if)

## When to Apply

- Any exploration where the goal is to determine a formula, normalization, or parameter value (not to compute a given formula)
- Situations where "what constraint does this satisfy?" has a unique answer
- When the explorer might otherwise enumerate possibilities rather than derive the correct one

## Related

- This pattern is the constructive version of `goal-design/specify-failure-paths.md` ("if this fails, explain why") — both force the explorer to engage with what constraints are actually doing.
- Different from `methodology/decisive-negative-pivot.md` (which is about when to abandon an approach) — "work backward" is about how to set up a constructive approach.
- Distinct from `methodology/adversarial-check-between-phases.md` — this is applied during Phase 2 construction, not Phase 3 adversarial.
