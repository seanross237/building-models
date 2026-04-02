# Exploration 002 Summary

## Goal

Decide whether the frozen pair

```text
C_ℓ(t) = (sum_{τ in T_ℓ} T_{τ,ℓ}(t)) / (sum_{τ in T_ℓ} |T_{τ,ℓ}(t)|),
E_ℓ^transfer = quiet earlier interface transfer, then a short-window positive
transfer burst and receiver-band gain across ℓ -> ℓ/ρ,
```

survives the smallest honest exact-support audit.

## What I tried

- [VERIFIED] Checked the one-triad case directly from the definition of `C_ℓ`.
- [CHECKED] Identified the first honest nontrivial setting as a connected
  two-triad exact cluster, since two distinct exact triads need at least five
  wavevectors before sign closure.
- [COMPUTED] Built the explicit cluster

```text
k1 = (1,0,0), k2 = (0,1,0), k3 = (0,0,1),
k4 = (1,1,0), k5 = (1,0,1), σ = (-,+,+,+,-),
```

  and computed its exact helical coefficients in
  `code/minimal_c_support_audit.py`.
- [COMPUTED] Derived the exact two-term cancellation family

```text
T_4 = W,  T_5 = -W cos ε,  C_ℓ = tan^2(ε/2),
```

  and evaluated numerical samples in
  `code/minimal_c_support_audit_output.txt`.

## Outcome

- [CHECKED] Outcome: the pair fails the minimal audit.
- [VERIFIED] On one active triad, `C_ℓ = ±1` whenever the transfer is nonzero,
  so the observable is tautological there.
- [COMPUTED] On the smallest honest two-triad cluster, `C_ℓ` can be made
  arbitrarily small while the net receiver-band transfer stays positive.
- [CHECKED] Terminal audit verdict: `fail`, with failure category
  `model-level failure`.

## Verification scorecard

- [VERIFIED] Single-triad forcing: `C_ℓ = T/|T| = ±1`.
- [CHECKED] Minimal cluster size: five wavevectors for the first connected
  two-triad exact cluster.
- [COMPUTED] Exact receiver coefficients:

```text
(d/dt) a4 = -(i / (2 sqrt(2))) a1 a2,
(d/dt) a5 = -(i / (2 sqrt(2))) a1 a3.
```

- [COMPUTED] Exact low-coherence family:

```text
C_ℓ = (1 - cos ε)/(1 + cos ε) = tan^2(ε/2) -> 0.
```

- [COMPUTED] Exact-support honesty check: the sign-closed support already emits
  to `36` external target channels.

## Key takeaway

[CHECKED] `C_ℓ` is not a phase-locking firewall observable. It is forced on one
triad and becomes only a cancellation ratio once two exact interface terms are
active. That means `E_ℓ^transfer` can stay live while `C_ℓ` is arbitrarily
small in the first honest nontrivial setting.

## Proof gaps or computation gaps identified

- [CHECKED] I did not construct a fully isolated exact-NS finite-support
  solution, because the smallest sign-closed support already has `36` external
  emissions.
- [CHECKED] That gap does not affect the verdict: spectator terms only add more
  cancellation freedom and cannot restore a positive lower bound for `C_ℓ`.
- [CHECKED] The audit therefore already kills the frozen observable pair without
  needing a larger forcing campaign.

## Unexpected findings

- [CHECKED] The decisive negative appears at the first exact two-triad cluster;
  no large search or long simulation is needed.
- [COMPUTED] The symmetric cluster has equal receiver coefficients
  `|c4| = |c5| = 1 / (2 sqrt(2))`, which makes the cancellation formula exact
  and especially sharp.
- [CHECKED] The delayed-transfer event is not the bottleneck here. The route
  dies earlier because the coherence observable itself is already too
  tautological or too weak.

## Decision

[CHECKED] Do not proceed to a larger force-or-kill campaign on the frozen pair
`(C_ℓ, E_ℓ^transfer)`. Any continuation would need a genuinely different phase
observable, not another normalization of the same signed-transfer ledger.
