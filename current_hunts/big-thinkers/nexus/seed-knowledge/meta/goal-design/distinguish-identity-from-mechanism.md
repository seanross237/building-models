---
topic: Require explicit distinction between algebraic identities and physical mechanisms
category: goal-design
date: 2026-03-27
source: "compton-unruh strategy-001 meta-exploration-004"
---

## Lesson

When an exploration finds a mathematical identity connecting two quantities (e.g., "A = B algebraically"), require the explorer to explicitly state whether this is (a) an algebraic identity (trivially and certainly true) or (b) a physical derivation (requires mechanism and assumptions). These are completely different levels of claim, and explorers will conflate them if not asked to distinguish.

## Evidence

- **compton-unruh strategy-001 exploration-004** — The explorer discovered that T_U(a)/T_dS(a) = μ_MOND(a/cH₀) exactly — the de Sitter temperature ratio IS the standard MOND interpolation function. This is algebraically trivial (divide the two expressions). But whether this identity *means* anything physically requires a derivation of why m_i ∝ T_U/T_dS — which does not exist. The explorer correctly flagged this: "The claim that this is novel is CONJECTURED — it's simple enough that it may have been noted before. Verlinde (2016) arrives at a similar conclusion through a different path." Without the distinction, this could have been reported as a physics result instead of a mathematical observation.

## How to Apply

When designing goals for explorations involving derivations or connections between quantities, add:

> "For any mathematical relationship you find: explicitly state whether it is (a) an algebraic identity (true by definition/algebra regardless of physics), (b) a result that follows from standard physics assumptions, or (c) a novel physical claim requiring new assumptions. Label each conclusion clearly."

The **COMPUTED / CONJECTURED** tagging system partially achieves this, but a specific identity-vs-mechanism flag is more direct.

## Why It Matters

- An algebraic identity is always true regardless of any physical interpretation. It cannot be falsified and does not make a physical prediction.
- A physical mechanism must specify what assumptions connect the identity to dynamics. Different assumptions can give different (even opposite) results from the same identity.
- In compton-unruh exploration-004: three physically motivated ansatze using the same temperatures (T_dS, T_dS - T_GH, T_U²/T_dS) gave three different physical predictions — one with wrong sign, one wrong magnitude, one correct. The identity alone does not select among them.

## Related Lessons

See also `specify-failure-paths.md` for requiring honest weakness assessments of all assumptions.
