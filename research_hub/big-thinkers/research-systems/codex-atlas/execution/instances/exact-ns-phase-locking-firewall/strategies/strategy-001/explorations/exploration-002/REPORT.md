# Exploration 002 Report

## 1. Executive verdict

[VERIFIED] Decision target:

> Either there exists a smallest faithful exact support or exact triad cluster
> on which the frozen pair `(C_ℓ, E_ℓ^transfer)` is nontrivial and
> phase-sensitive, or the minimal setting already shows model-level failure
> because `C_ℓ` is either forced on one active triad or can stay arbitrarily
> small once more than one exact interface transfer term is active while the
> delayed-transfer target remains live.

[CHECKED] Verdict on the frozen pair: `fail: model-level failure`.

[VERIFIED] On one exact active triad,

```text
C_ℓ(t) = T_{τ,ℓ}(t) / |T_{τ,ℓ}(t)| ∈ {+1,-1}
```

whenever `T_{τ,ℓ}(t) != 0`, so the observable is already tautological there.

[CHECKED] The first honest nontrivial setting is therefore not one triad but the
smallest connected two-triad exact cluster. Distinct exact triads cannot share
two wavevectors, because then the third leg is fixed by `k + p + q = 0`, so a
connected cluster with two distinct active interface terms needs at least five
wavevectors before sign closure.

[COMPUTED] In that smallest two-triad cluster, `C_ℓ` can be made arbitrarily
small while the net receiver-band transfer stays strictly positive. The exact
family is

```text
T_4 = W,
T_5 = -W cos ε,
C_ℓ = (T_4 + T_5) / (|T_4| + |T_5|) = tan^2(ε/2) -> 0
```

as `ε -> 0+`, with `T_4 + T_5 = W (1 - cos ε) > 0`.

[CHECKED] Because `E_ℓ^transfer` uses absolute thresholds on positive transfer
and receiver-band gain, while `C_ℓ` is a normalized cancellation ratio, the
event thresholds can still be met by amplitude scaling even when `C_ℓ` is
arbitrarily small.

[CHECKED] Direct answer to the exploration question:

> `E_ℓ^transfer` can remain live in the first honest nontrivial setting while
> `C_ℓ` stays arbitrarily small. One exact triad makes `C_ℓ` tautological; the
> first honest two-triad cluster already exposes a low-coherence counterexample.

## 2. Explicit transfer identity for `C_ℓ`

[VERIFIED] The frozen Phase 1 identity is

```text
sum_{τ in T_ℓ} T_{τ,ℓ}(t)
  = net signed interface transfer across ℓ -> ℓ/ρ,

T_{τ,ℓ}(t) = W_{τ,ℓ}(t) cos Θ_τ(t),
W_{τ,ℓ}(t) > 0,

C_ℓ(t)
  = (sum_{τ in T_ℓ} T_{τ,ℓ}(t))
    / (sum_{τ in T_ℓ} |T_{τ,ℓ}(t)|).
```

[CHECKED] Here `Θ_τ` is the exact helical triad phase corrected by the helical
coefficient phase, exactly as in exploration 001, so `C_ℓ` is a normalized
signed-transfer / absolute-transfer ratio rather than an amplitude-only scalar.

[COMPUTED] For the smallest two-triad cluster

```text
k1 = (1,0,0),  k2 = (0,1,0),  k3 = (0,0,1),
k4 = (1,1,0) = k1 + k2,
k5 = (1,0,1) = k1 + k3,
σ = (-,+,+,+,-),
```

the exact helical computation in `code/minimal_c_support_audit.py` gives

```text
(d/dt) a4 = c4 a1 a2,   c4 = - i / (2 sqrt(2)),
(d/dt) a5 = c5 a1 a3,   c5 = - i / (2 sqrt(2)).
```

[COMPUTED] Writing `a_j = r_j exp(i φ_j)`, the receiver-band energy derivative is

```text
(d/dt) (|a4|^2 + |a5|^2)/2 = T_4 + T_5,

T_4 = 2 |c4| r1 r2 r4 cos Θ_4,
T_5 = 2 |c5| r1 r3 r5 cos Θ_5,

Θ_4 = φ1 + φ2 - φ4 - π/2,
Θ_5 = φ1 + φ3 - φ5 - π/2.
```

[CHECKED] This is the required explicit identity: `Θ_τ` enters only through the
`cos Θ_τ` factors, while `C_ℓ` measures cancellation across the two active
exact-transfer terms.

## 3. Smallest faithful setting audit

[VERIFIED] One exact triad is too small for the pair. It does keep the exact
triad phase variable and one transfer term, but then

```text
C_ℓ = ±1
```

whenever the transfer is nonzero. So one triad does not give a nontrivial
coherence burden; it only says whether that single term is forward or backward.

[CHECKED] The first honest nontrivial setting is therefore the smallest
connected two-triad cluster. The explicit cluster above uses the minimum five
wavevectors compatible with two distinct exact triads and nontrivial phase
competition.

[COMPUTED] Its internal exact ledger has only the two desired receiver terms and
their mirror return legs:

```text
(d/dt) a1 = +(i / (4 sqrt(2))) (2 a4 \bar a2 + 2 a5 \bar a3),
(d/dt) a2 = +(i / (4 sqrt(2))) (2 a4 \bar a1),
(d/dt) a3 = -(i / (4 sqrt(2))) (2 a5 \bar a1),
(d/dt) a4 = -(i / (2 sqrt(2))) a1 a2,
(d/dt) a5 = -(i / (2 sqrt(2))) a1 a3.
```

[COMPUTED] The same sign-closed support is not dynamically isolated inside exact
NS: the audit script finds `36` nonzero external target channels. So the
honest object is the exact local two-triad ledger itself, or its Galerkin
truncation if one insists on a closed reduced model.

[CHECKED] Fidelity ledger for this reduced setting:

- Preserved: exact Waleffe coefficients on the active triads, true triad-phase
  variables `Θ_4, Θ_5`, conjugate mirror closure on the active support, and the
  exact coefficient-weighted amplitude-level transfer identity entering `C_ℓ`.
- Discarded: the `36` external spectator emissions and any longer-range delayed
  memory mechanism beyond the short receiver-band transfer ledger.

[CHECKED] That is enough for the present audit because the only Phase 2 question
is whether the frozen ratio `C_ℓ` is already forced or already too weak on the
smallest honest phase-sensitive transfer ledger.

## 4. Low-coherence stress test

[COMPUTED] Impose the symmetric amplitude choice

```text
r1 = r2 = r3 = r4 = r5 = R
```

and the phase choice

```text
Θ_4 = 0,
Θ_5 = π - ε,
0 < ε << 1.
```

Then, because `|c4| = |c5| = 1 / (2 sqrt(2))`,

```text
T_4 = (R^3 / sqrt(2)),
T_5 = - (R^3 / sqrt(2)) cos ε,
T_4 + T_5 = (R^3 / sqrt(2)) (1 - cos ε) > 0,

C_ℓ
  = (T_4 + T_5) / (|T_4| + |T_5|)
  = (1 - cos ε) / (1 + cos ε)
  = tan^2(ε/2).
```

[COMPUTED] So `C_ℓ -> 0` as `ε -> 0+` even though the net receiver-band
transfer remains positive.

[COMPUTED] The script gives the explicit numerical sample `R = 10`:

```text
ε = 0.100: T4 = 707.106781186547,
           T5 = -703.574192576952,
           net = 3.532588609595,
           C_ℓ = 2.504172577142e-03

ε = 0.050: T4 = 707.106781186547,
           T5 = -706.223081837111,
           net = 0.883699349437,
           C_ℓ = 6.252605089276e-04
```

[CHECKED] This is the honest low-coherence counterexample mechanism:

- the signed sum stays positive,
- the normalized coherence ratio is arbitrarily small,
- and the positive receiver-band transfer can still exceed any fixed short-window
  threshold after rescaling `R`, because the transfer magnitude scales like
  `R^3` while `C_ℓ` is scale-invariant.

[CHECKED] The earlier-quiet clause in `E_ℓ^transfer` does not rescue `C_ℓ`.
At `Θ_4 = Θ_5 = π/2`, both active transfer terms vanish exactly, so the same
cluster has an exact quiet state. The transfer terms depend continuously on the
phases, so a short move from exact cancellation or exact quiet to the
near-cancelling burst above changes the absolute burst size but does not impose
any positive lower bound on `C_ℓ`.

[CHECKED] Therefore the direct answer to the minimal-setting question is:

> one exact triad forces `C_ℓ` and is too tautological for the mission; once the
> first honest two-triad cluster is activated, `C_ℓ` can stay arbitrarily small
> while the delayed-transfer target remains live at the level of positive
> short-window receiver-band transfer and gain.

## 5. Larger-campaign go / no-go decision

[CHECKED] Decision: `no-go`.

[CHECKED] A larger force-or-kill campaign is scientifically unjustified after
this audit. The minimal honest setting already shows that the frozen `C_ℓ`
observable does not encode a coercive phase-locking burden. It is only a
normalized cancellation ratio.

[CHECKED] Enlarging the support cannot repair this defect:

- adding more active interface terms only adds more cancellation freedom in the
  numerator of `C_ℓ`,
- the exact support is already spectator-contaminated in the smallest cluster,
  so larger supports will not restore one-triad rigidity,
- and the event side `E_ℓ^transfer` is thresholded in absolute transfer / gain,
  not in normalized coherence.

[CHECKED] So a larger campaign would not be testing a plausible firewall claim.
It would be trying to rescue an observable that has already failed at the first
exact phase-sensitive adversarial screen.

## 6. Audit verdict

[VERIFIED] Terminal audit verdict: `fail`.

[CHECKED] Failure category: `model-level failure`.

[CHECKED] Sharp reason:

```text
one exact triad makes C_ℓ tautological;
the smallest nontrivial exact two-triad cluster already allows
positive receiver-band transfer with C_ℓ arbitrarily small.
```

[CHECKED] Next-step implication: stop this strategy rather than escalate to a
larger force-or-kill campaign. If any continuation is attempted, it must use a
sharply reformulated observable, not the frozen pair `(C_ℓ, E_ℓ^transfer)`.

[COMPUTED] Reproducible artifacts:

- `code/minimal_c_support_audit.py`
- `code/minimal_c_support_audit_output.txt`
