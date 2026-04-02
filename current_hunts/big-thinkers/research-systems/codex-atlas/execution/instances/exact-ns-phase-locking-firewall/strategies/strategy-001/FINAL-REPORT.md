# Final Report: Strategy 001

## Executive Verdict

```text
4. model-level failure
```

[CHECKED] Exploration 001 found a narrow Phase 0 survivor:

```text
C_ℓ(t) = (∑_{τ∈𝒯_ℓ} T_{τ,ℓ}(t)) / (∑_{τ∈𝒯_ℓ} |T_{τ,ℓ}(t)|),
D_ℓ(t) = 1 - C_ℓ(t),
```

the exact transfer-coherence ratio on a sign-closed helical triad population
across one smooth scale interface, with backup raw phase concentration
observable `A_ℓ`.

[CHECKED] Exploration 001 also fixed the clean delayed-transfer companion event
as the global spectral interface-burst event `E_ℓ^transfer`, rather than the
localized physical-space event `E_flux`.

[COMPUTED] Exploration 002 killed the route at the smallest honest exact-support
audit:

- on one active transfer term, `C_ℓ = ±1` identically, so the observable is too
  tautological to be a real phase-locking burden;
- on the first nontrivial exact-helical cluster with two transfer inputs feeding
  the same receiver mode, exact phase tuning keeps net receiver-band gain
  positive while driving `C_ℓ` arbitrarily close to `0`.

[CHECKED] So the chosen observable is definable but not strongly coupled enough
to delayed transfer. That is exactly a model-level failure.

## Directions Tried

### 1. Phase 0 intrinsic phase-object gate

[CHECKED] The old packet/sign family stayed dead. Packet representatives,
desired-triad witness sets, and refinement bookkeeping remained non-canonical.

[CHECKED] A new exact object did survive: the interface-based transfer-coherence
ratio `C_ℓ`, built directly from exact helical triad contributions
`T_{τ,ℓ} = W_{τ,ℓ} cos Θ_{τ,ℓ}`.

[CHECKED] This was a narrow success, not a theorem. It only justified the
smallest-support audit.

### 2. Phase 2 smallest honest exact-support audit

[COMPUTED] The decisive calculation is in
`explorations/exploration-002/code/minimal_cluster_cancellation_demo.py`.

[COMPUTED] An explicit exact-helical two-input cluster already defeats the hoped
for burden:

```text
target k  = (2,1,0)
pair 1    = (1,0,0) + (1,1,0)
pair 2    = (2,0,0) + (0,1,0)
signs     = (1, -1, 1, 1, -1)
|c1|      = 0.178839197367
|c2|      = 0.383750455201
```

[COMPUTED] With exact phase choices `Θ_1 = 0`, `Θ_2 = π` and tuned source
amplitudes, the family

```text
eps = 1e-2:  net gain = 1.0e-2,   C_ℓ = 2.88e-2
eps = 1e-3:  net gain = 1.0e-3,   C_ℓ = 2.80e-3
eps = 1e-4:  net gain = 1.0e-4,   C_ℓ = 2.80e-4
```

shows that positive receiver-band gain coexists with arbitrarily small
coherence ratio.

[CHECKED] That is the earliest honest point where the route should stop.

## Strongest Findings

1. [VERIFIED] Exact helical triad phases are genuine intrinsic data:
   `Θ_τ = arg u_p + arg u_q - arg u_k + arg C_τ` is translation/gauge invariant.
2. [CHECKED] A theorem-facing phase observable can be written without Tao-role
   labels, but the best surviving candidate is a cancellation ratio tied to one
   exact interface-transfer ledger.
3. [COMPUTED] The minimal-support audit shows the cancellation-ratio observable
   is too trivial on one triad and too weak on the first nontrivial cluster.

## Negative Results and Dead Ends

- [CHECKED] The localized physical-space event `E_flux` is not the clean
  companion event for the spectral phase observable because the spatial cutoff
  destroys the exact triad ledger.
- [CHECKED] Raw phase concentration `A_ℓ` is weaker than `C_ℓ` and therefore
  does not rescue the route.
- [CHECKED] No larger force-or-kill campaign is justified once the minimal audit
  already shows that positive transfer can occur with arbitrarily small `C_ℓ`.

## Recommended Next Move For The Missionary

[CHECKED] Kill this strategy as posed.

[CHECKED] Only reopen under a genuinely different intrinsic phase observable
family, not another net-transfer-versus-absolute-transfer ratio.

[CHECKED] Any replacement observable should be required, before mission launch,
to survive the same smallest-support adversarial screen:

- not forced to a trivial value on one exact triad,
- and not arbitrarily weakened by the first multi-input exact-helical cluster.

Without that, the mission will only rename the same cancellation defect.

## Claims Worth Carrying Forward

- [VERIFIED] There is a real exact helical triad-phase variable that can be
  written intrinsically without packet roles.
- [CHECKED] Not every intrinsic phase observable is scientifically useful; the
  minimal-support audit is what decides whether a definable object is actually a
  firewall candidate.
- [COMPUTED] Cancellation-ratio phase observables are a bad family for this
  mission: they die immediately between the single-triad and two-input-cluster
  tests.
