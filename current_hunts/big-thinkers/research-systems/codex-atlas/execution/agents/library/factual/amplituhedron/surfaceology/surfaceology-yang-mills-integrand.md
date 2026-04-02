---
topic: Surfaceology canonical Yang-Mills loop integrand via scalar scaffolding (PRL 2025)
confidence: verified
date: 2026-03-27
source: "amplituhedron strategy-001 exploration-007; arXiv:2408.11891 (PRL 2025)"
---

## Finding

The long-standing problem of defining a canonical loop integrand for **non-supersymmetric Yang-Mills theory** was solved in arXiv:2408.11891 (Arkani-Hamed, Cao, Dong, Figueiredo, He; published PRL 2025) using **surface kinematics**. This is a distinct resolution from the corolla polynomial approach (arXiv:2405.10601) and directly addresses what previously appeared to be a fundamental obstruction.

## The Problem Solved

Prior to this work, the "amplituhedron approach" to YM loop integrands failed due to: UV divergences, no Yangian symmetry, no dual conformal symmetry. These obstacles blocked amplituhedron-style encoding but not all geometric approaches. Surface kinematics circumvents them via a different geometric arena (kinematic space, not twistor space).

## Scalar Scaffolding

The key technique: embed n-point gluon amplitudes inside 2n-point scalar surface amplitudes. Adjacent scalar pairs "scaffold" each gluon:

```
ℐ_n^gluon = Res_{X_Scaff=0} ∫ ∏_P dy_P/y_P²  ∏_C u_C^{α'X_C}
```

Taking residues at scaffolding curve locations (where adjacent scalar pairs fuse into gluons) extracts the gluon integrand from the scalar surface formula.

## Surface Gauge Invariance

The gluon integrand satisfies a surface-generalized gauge invariance condition: shifts ε^μ → ε^μ + αp^μ leave the amplitude unchanged through combinations of surface kinematic X-variables. This is the loop-level analog of tree-level Ward identities, now manifest at the integrand level.

## Perfect Factorization (Resolving the 1/0 Problem)

A longstanding ambiguity in loop integrands: when cutting a propagator, "single cuts" could produce 0/0 = 1/0 ambiguities in standard kinematics. Surface kinematics assigns **distinct variables** X_{i,j} ≠ X_{j,i} even when curves are homologous, so all denominators remain non-zero. Single cuts give well-defined tree amplitudes without ambiguity.

## Recursion Structure

The loop integrand satisfies:
```
ℐ_n^S = ∑_i  Res_{X_{i,p}=0}[ℐ_n^S(X_{j,p} → X_{j,p} − X_{i,p})] / X_{i,p}
```
This recursively constructs all-multiplicity, multi-loop integrands from tree-level data.

## Explicit Results

| Level | Status |
|-------|--------|
| 1-loop all-multiplicity | ✅ Explicit formula |
| 2-loop 4-point | ✅ Explicit formula |
| Higher loop | Recursion exists; explicit all-multiplicity open |

1-loop and 2-loop results reproduce known YM integrands in D dimensions near D=4.

## Relation to Amplituhedron Yang-Mills Entry

The entry `yang-mills-scattering-forms.md` states "Loop-level general ❌ UV divergences prohibit." This is correct for the **amplituhedron approach** (twistor space, requires UV finiteness). The surface kinematics approach is a *different geometric framework* that works in kinematic space and is not subject to the same obstruction. These are complementary findings, not contradictory ones.
