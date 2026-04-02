---
topic: Test cancellation-ratio observables on the first two-channel exact cluster
category: methodology
date: 2026-04-01
source: "exact-ns-phase-locking-firewall strategy-001 meta-exploration-002"
---

## Lesson

Observables of the form

```text
burden = (signed net transfer) / (absolute transfer mass)
```

are structurally vulnerable to the first exact support with two active inputs into the same receiver. The numerator sees only the residual after cancellation, while the denominator keeps the full mass of both channels. Opposite-phase tuning can therefore keep the target transfer positive while driving the ratio arbitrarily close to zero.

So before studying delayed thresholds, long quiet-to-burst mechanisms, or larger supports, test the first two-channel exact cluster.

## Evidence

- **exact-ns-phase-locking-firewall exploration-002** — After the one-triad tautology screen, the smallest exact cluster with two transfer inputs into one receiver mode already killed the preferred burden `C_ell = (sum T)/(sum |T|)`.
- With phases `Theta_1 = 0` and `Theta_2 = pi`, the exploration produced `T_1 > 0`, `T_2 < 0`, positive net receiver gain, and `C_ell -> 0` by tuning one source amplitude.
- The decisive feature was structural, not delayed or multiscale: numerator = residual signed gain, denominator = full absolute transfer mass.

## Protocol

1. Identify the first exact support with two distinct inputs feeding the same target channel or receiver mode.
2. Write the exact signed contributions and the absolute-mass denominator term by term.
3. Test an adversarial opposite-sign phase arrangement.
4. Tune amplitudes to see whether positive net transfer can survive while the ratio tends to zero.
5. If it can, stop the campaign unless a new invariant ties the residual to the absolute mass.

## When to Apply

- phase-locking or coherence-burden missions
- transfer-alignment observables
- exact-support audits where the denominator is unsigned mass and the numerator is signed net effect
- any delayed-threshold program whose only burden variable is a cancellation ratio

## Relationship to Other Entries

- `coefficient-weighted-amplitude-level-leakage.md` says to define exact-support observables at the coefficient-amplitude level. This entry adds the next diagnostic: once the observable is defined, test whether a two-channel cancellation already kills it.
- `toy-subsystem-isolation-inside-exact-network.md` asks whether a reduced subsystem survives inside exact dynamics. This entry is narrower: even before full-network issues, a two-channel exact cluster may already defeat a cancellation-ratio burden.
