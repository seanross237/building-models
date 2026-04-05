# Exploration 002 Report

## Executive verdict

Decision target:

> Either there exists a smallest faithful exact support or exact triad cluster on
> which the preferred pair `(C_ℓ, E_ℓ^transfer)` is nontrivial and
> phase-sensitive, or the minimal setting already shows model-level failure
> because `C_ℓ` is either forced / tautological on one triad or can stay
> arbitrarily small once more than one exact transfer term is active while the
> delayed-transfer target remains live.

[COMPUTED] The smallest-support audit ends in:

```text
model-level failure
```

[CHECKED] The reason is sharp and two-stage:

1. on one exact active transfer term, `C_ℓ = ±1` identically, so the observable
   is too tautological to represent a genuine phase-locking burden;
2. on the smallest nontrivial exact cluster with two transfer inputs into the
   same receiver mode, exact phase tuning keeps the net receiver-band gain
   positive while driving `C_ℓ` arbitrarily close to `0`.

[CHECKED] So the preferred observable fails the minimal audit in the only two
honest ways available:

- too trivial on the single-triad setting,
- too weak on the first multi-term setting.

That is already enough to stop the strategy. A larger force-or-kill campaign is
not scientifically justified.

## Explicit transfer identity for `C_ℓ`

[VERIFIED] Exploration 001 fixed the exact phase variable

```text
Θ_τ = arg u_{s_p}(p) + arg u_{s_q}(q) - arg u_{s_k}(k) + arg C_τ
```

for each ordered helical triad term `τ`, with exact transfer contribution

```text
T_{τ,ℓ}(t)
  = Re( overline{u_{s_k}(k,t)} C_τ u_{s_p}(p,t) u_{s_q}(q,t) )
  = W_{τ,ℓ}(t) cos Θ_{τ,ℓ}(t).
```

[CHECKED] The preferred observable is

```text
C_ℓ(t) = (∑_{τ∈𝒯_ℓ} T_{τ,ℓ}(t)) / (∑_{τ∈𝒯_ℓ} |T_{τ,ℓ}(t)|).
```

[CHECKED] Therefore:

- if `𝒯_ℓ` contains exactly one nonzero transfer term, then

```text
C_ℓ(t) = T_{τ,ℓ}(t) / |T_{τ,ℓ}(t)| = ±1;
```

- if `𝒯_ℓ` contains at least two active terms, then cancellation is controlled
  only by the signed sum in the numerator, while the denominator keeps the full
  absolute mass of both terms.

This is the structural transfer identity the audit needs.

## Smallest faithful setting audit

[CHECKED] One exact triad is the smallest setting with a genuine helical phase
variable, but it is not scientifically adequate for the present observable:

- it forces `C_ℓ = ±1`,
- so it cannot test whether low coherence is compatible with delayed transfer,
- and it reduces the preferred observable to a sign bit rather than a
  population-level coherence burden.

[CHECKED] The first honest nontrivial setting is therefore the smallest
sign-closed exact cluster with **two distinct ordered transfer inputs feeding
the same receiver mode**.

[COMPUTED] An explicit exact-helical example is:

```text
target k  = (2,1,0)
pair 1    = (1,0,0) + (1,1,0)
pair 2    = (2,0,0) + (0,1,0)
signs     = (σ_k, σ_p1, σ_q1, σ_p2, σ_q2) = (1, -1, 1, 1, -1)
```

For this cluster, the exact helical coefficients are

```text
|c1| = 0.178839197367,
|c2| = 0.383750455201.
```

[COMPUTED] These were produced by
[minimal_cluster_cancellation_demo.py](./code/minimal_cluster_cancellation_demo.py),
which searched sign patterns and then built explicit phase/amplitude families.

[CHECKED] This is already the smallest setting where the question is
nontrivial:

- one transfer term is too small because `C_ℓ` is forced,
- two transfer terms are the first place where cancellation and phase
  competition can occur,
- and no packet bookkeeping is required.

## Low-coherence stress test

[COMPUTED] For the two-channel cluster above, choose phases so that

```text
Θ_1 = 0,   Θ_2 = π.
```

Then

```text
T_1 = +W_1,   T_2 = -W_2,
```

with exact mode phases given explicitly by the script.

[COMPUTED] Tuning the second source amplitude gives the family:

```text
eps = 1e-2:  net = 1.0e-2,   C_ℓ = 2.88e-2
eps = 1e-3:  net = 1.0e-3,   C_ℓ = 2.80e-3
eps = 1e-4:  net = 1.0e-4,   C_ℓ = 2.80e-4
```

while the receiver-mode gain stays positive because `net = T_1 + T_2 > 0`.

[CHECKED] This is the decisive structural point:

- the numerator of `C_ℓ` only sees the small residual positive gain,
- the denominator sees the full absolute transfer mass,
- so `C_ℓ` can be made arbitrarily small without killing short-time
  receiver-band activation.

[CHECKED] The delayed-transfer aspect does not rescue the observable. If the
smallest nontrivial cluster already admits positive receiver-band gain with
arbitrarily small `C_ℓ`, adding more modes or a longer quiet-to-burst mechanism
only creates **more** cancellation freedom, not less.

So the audit does not need a full delayed-threshold construction. The object is
already too weak at the minimal exact-support level.

## Larger-campaign go / no-go decision

[CHECKED] `No-go`.

[CHECKED] A larger campaign would only add complexity on top of an observable
that has already failed both minimal tests:

- it is tautological on one triad,
- and it loses quantitative force on the first multi-input cluster.

[CHECKED] That is exactly the kind of Phase 2 failure the strategy was designed
to catch early. There is no reason to spend more exploration budget proving a
firewall for a burden variable that the minimal setting already shows can be
arbitrarily weak during positive transfer.

## Audit verdict

```text
fail: model-level failure
```

[CHECKED] The preferred phase observable `C_ℓ` is definable but not strongly
coupled enough to delayed transfer in the smallest honest exact setting.

[CHECKED] The correct mission outcome is therefore:

```text
model-level failure
```

## Reproducible Artifact

[COMPUTED] The explicit minimal-cluster computation is in
[minimal_cluster_cancellation_demo.py](./code/minimal_cluster_cancellation_demo.py).

[CHECKED] I ran:

```text
python3 code/minimal_cluster_cancellation_demo.py
python3 -m py_compile code/minimal_cluster_cancellation_demo.py
```

successfully.
