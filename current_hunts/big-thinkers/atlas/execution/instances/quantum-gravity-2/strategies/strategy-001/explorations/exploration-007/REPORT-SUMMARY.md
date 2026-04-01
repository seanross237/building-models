# Exploration 007 Summary: SCG v2.0 — Causal Order Rewrite

## Goal
Rewrite SCG's axioms replacing the symmetric cost function (Axiom 3) with a causal partial order, then assess what the revised theory achieves and what remains broken.

## What Was Done
Rewrote all five axioms. Only Axiom 3 required a major change: the symmetric metric c(x,y) was replaced with a triple — (a) a partial order on Omega encoding causal precedence, (b) a directed cost c(x,y) >= 0 defined only for causally ordered pairs, and (c) a volume measure v(x) providing the conformal factor. Axiom 4 was adjusted to optimize over causal chains rather than arbitrary paths. Axioms 1, 2, 5 are essentially unchanged.

## Outcome: SUCCEEDED — Genuine Improvement, But Not a Fix-All

**What's fixed:** The fatal Lorentzian signature problem is directly resolved. The Malament theorem guarantees that causal order + volume determines Lorentzian geometry (not Riemannian). The Jacobson bridge is strengthened. Hyperbolic (causal) propagation replaces elliptic propagation. CDT-like dimension selection becomes conceivable.

**What survives unchanged:** All four derivation chains survive the rewrite. The Barandes lifting already uses directed transitions. Pedraza gains signature compatibility. Jacobson is inherently Lorentzian and benefits. Diosi-Penrose is unaffected.

**What remains broken:** QM emergence is still reformulation not derivation (untouched). Continuum limit still unproven. Pedraza still 2D-only. No unique predictions. Self-consistency unproven. hbar = 2m*sigma^2 still renaming.

**New problems:** The volume measure v(x) is a new free function with no specified origin. The partial order on a "pre-geometric" configuration space arguably puts causal structure in by hand rather than deriving it.

## Key Takeaway
The repair moves SCG from "structurally broken" (dead on arrival due to signature incompatibility) to "ambitious but unproven" (on par with other QG research programs). That's real progress. The single largest remaining risk is the QM emergence chain — if the Barandes lifting is truly just a reformulation, SCG doesn't derive quantum mechanics, and no amount of axiom rewriting fixes that.
