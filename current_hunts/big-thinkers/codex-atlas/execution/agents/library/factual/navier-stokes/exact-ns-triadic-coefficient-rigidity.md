---
topic: Exact Navier-Stokes triadic geometry fixes the coefficient hierarchy Tao's delayed-transfer circuit treats as free
confidence: checked
date: 2026-03-31
source: "anatomy-of-averaged-ns-blowup-firewall exploration-002; Tao 2016 JAMS"
---

## Finding

Tao's delayed-transfer circuit needs five effectively independent couplings with a deliberately engineered size/sign hierarchy,

```text
ε, ε^2 exp(-K^10), ε^(-1) K^10, ε^(-2), K,
```

but exact incompressible Navier-Stokes does not provide free gate constants. In Fourier variables it gives one quadratic law

```text
∂t û(k) + |k|^2 û(k)
  = -i ∑_{p+q=k} (q · û(p)) P_k û(q),
P_k = I - (k ⊗ k)/|k|^2,
```

so after shell rescaling the dimensionless interaction coefficients are rigid geometric functions of the triad `(k,p,q)` and polarization/helicity choices rather than independently assignable parameters.

## Exact Mismatch With Tao's Circuit

Tao's reduced shell dynamics require one engineered hierarchy to coexist in a single activation episode:

- weak pump `X1,n -> X2,n` of size `ε`,
- exponentially tiny seed `X1,n -> X3,n` of size `ε^2 exp(-K^10)`,
- strong amplifier `X2,n X3,n -> X3,n` of size `ε^(-1) K^10`,
- even stronger rotor `X3,n`-gated exchange `X1,n <-> X4,n` of size `ε^(-2)`,
- macroscopic next-shell pump `X4,n -> X1,n+1` of size `K`.

Exact NS certainly permits energy transfer, but the live firewall question is narrower: can one exact Fourier/helical configuration realize this whole separated hierarchy with the required sign pattern while staying inside one rigid quadratic law?

## Why This Survives As A Firewall Candidate

- A single exact triad has cyclic coefficient relations constrained by geometry, energy conservation, and helicity bookkeeping rather than five independent knobs.
- The exact target-mode projector `P_k` fixes how each interaction lands on the destination mode; it is not an optional correction that can be postponed to a later cleanup step.
- Therefore the issue is not "can NS cascade energy forward?" but "can NS reproduce Tao's deliberately mismatched time scales and signs without leaving order-one geometric coefficient rigidity?"

This is the strongest surviving Phase 1 candidate because it attacks the narrowest load-bearing requirement in Tao's proof.

## Relationship to Other Entries

- `tao-averaged-ns-delayed-transfer-circuit.md` states the engineered hierarchy that exact NS would need to realize.
- `exact-ns-unavoidable-spectator-couplings.md` covers the companion candidate: even if one desired triad exists, exact NS also turns on additional channels that threaten circuit isolation.
