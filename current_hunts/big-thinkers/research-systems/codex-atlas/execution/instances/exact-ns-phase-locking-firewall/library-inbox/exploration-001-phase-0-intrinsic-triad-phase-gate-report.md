# Exploration 001 Report

## Executive verdict

Decision target:

> Either there exists one preferred intrinsic exact-helical phase/coherence
> observable, with an explicit formula, exact triad population, phase variable,
> normalization, and harmless-change invariance ledger, that can be paired with a
> faithful delayed-transfer event; or all honest candidates still depend on
> non-canonical packet / role bookkeeping, unstable representative choices, or no
> longer contain genuine phase information, so the strategy should stop with the
> correct failure category.

[VERIFIED] In the exact helical Fourier law,

```text
(∂t + ν|k|^2) u_{s_k}(k)
  = -1/4 ∑_{p+q=k} ∑_{s_p,s_q}
      (s_p |p| - s_q |q|)
      overline{(h_{s_p}(p) × h_{s_q}(q)) · h_{s_k}(k)}
      u_{s_p}(p) u_{s_q}(q),
```

each ordered triad contribution carries one intrinsic phase combination

```text
Θ_τ = arg u_{s_p}(p) + arg u_{s_q}(q) - arg u_{s_k}(k) + arg C_τ
```

modulo `2π`, where `C_τ` is the exact helical coefficient of the triad term.

[CHECKED] That phase variable is genuine exact-NS data, not packet bookkeeping,
and it is translation/gauge invariant because the Fourier translation factors
cancel on `k = p + q`.

[CHECKED] The Phase 0 gate therefore **passes narrowly**. The preferred
observable is not the old packet-sign family. It is a smooth-interface
**transfer-coherence defect** built from the exact signed helical triad
contributions to one forward scale-transfer ledger. The object is intrinsic
enough to justify a smallest-support audit.

[CHECKED] The pass is narrow because the already available localized
physical-space event `E_flux` is only an imperfect companion for this spectral
phase observable. The clean pair is obtained by dropping the spatial cutoff and
using the same smooth scale interface globally. That keeps the Tao-facing
delayed-transfer meaning while preserving an exact triad ledger.

## Exact helical phase law and candidate map

[VERIFIED] For each exact ordered helical triad term `τ = (k,p,q,s_k,s_p,s_q)`,
the contribution to the mode-energy equation is

```text
T_τ(t)
  = Re( overline{u_{s_k}(k,t)} C_τ u_{s_p}(p,t) u_{s_q}(q,t) )
  = W_τ(t) cos Θ_τ(t),
```

with positive weight

```text
W_τ(t) = |C_τ| |u_{s_k}(k,t)| |u_{s_p}(p,t)| |u_{s_q}(q,t)|.
```

[CHECKED] This is the exact place where phase enters transfer. The candidate
observables considered were:

1. packet-sign proxies inherited from `SD_part`, `SD_target`, and `Leak`,
2. pure phase-concentration averages on exact triad populations,
3. coherence-defect observables comparing signed transfer with absolute transfer
   on an intrinsic exact triad population.

[CHECKED] Candidate family 1 is rejected immediately as primary:

- `SD_part` still moves under conjugate-pair representative choice and harmless
  packet refinement,
- `SD_target` and `Leak` still depend on a non-canonical desired-triad witness
  set,
- and all three revive the packet/role bookkeeping that this mission forbids.

[CHECKED] Candidate family 2 is admissible only as backup. A raw concentration
statistic such as

```text
|∑_τ W_τ e^{iΘ_τ}| / ∑_τ W_τ
```

is too coarse to be the preferred object because exact conjugate pairing and
mixed forward/backward branches can suppress the average even when the transfer
ledger is phase-coherent in the only sense that matters here: constructive
forward transfer.

[CHECKED] Candidate family 3 survives the definition gate and is the preferred
family because it is:

- exact-helical and monomial-level,
- intrinsically tied to transfer rather than to packet roles,
- explicitly phase-sensitive through `T_τ = W_τ cos Θ_τ`,
- and naturally invariant once the interface/filter convention is fixed.

## Preferred observable definition

[CHECKED] Fix once and for all:

- a smooth coarse-graining kernel `G`,
- a scale ratio `ρ > 1`,
- one interface scale `ℓ`,
- and the associated exact forward-transfer ledger across that interface.

[CHECKED] Let `𝒯_ℓ` be the sign-closed population of all ordered helical triad
terms appearing in the exact transfer across the interface `ℓ -> ℓ/ρ`. Let
`T_{τ,ℓ}(t)` denote the exact signed contribution of triad term `τ` to that
ledger, so that

```text
T_{τ,ℓ}(t) = W_{τ,ℓ}(t) cos Θ_{τ,ℓ}(t).
```

[CHECKED] Preferred observable:

```text
C_ℓ(t) = (∑_{τ∈𝒯_ℓ} T_{τ,ℓ}(t)) / (∑_{τ∈𝒯_ℓ} |T_{τ,ℓ}(t)|),
D_ℓ(t) = 1 - C_ℓ(t).
```

[CHECKED] Interpretation:

- `C_ℓ(t) ≈ 1` means the exact triad population contributing to forward transfer
  across `ℓ` is phase-aligned in the constructive-forward direction;
- `C_ℓ(t) ≈ 0` means heavy cancellation across the exact triad population;
- `D_ℓ(t)` is the corresponding coherence defect.

[CHECKED] Exact sense in which this is phase rather than amplitude only:

```text
C_ℓ(t) = (∑_τ W_{τ,ℓ}(t) cos Θ_{τ,ℓ}(t)) / (∑_τ W_{τ,ℓ}(t) |cos Θ_{τ,ℓ}(t)|).
```

The amplitudes `W_{τ,ℓ}` only weight the population. The sign of each triad
contribution, hence the cancellation burden, is carried by the exact phase
variable `Θ_{τ,ℓ}`.

## Backup observable or rejection of alternatives

[CHECKED] Backup observable:

```text
A_ℓ(t) = |∑_{τ∈𝒯_ℓ} W_{τ,ℓ}(t) exp(i Θ_{τ,ℓ}(t))| / ∑_{τ∈𝒯_ℓ} W_{τ,ℓ}(t).
```

[CHECKED] `A_ℓ` measures phase concentration on the same intrinsic triad
population but is weaker as a firewall object:

- it does not distinguish concentration around forward-transfer-maximizing
  phases from concentration around phases that cancel forward transfer,
- it can be small because of exact conjugate pairing even when
  `C_ℓ` is the more informative object,
- and it is therefore a poorer theorem-facing burden variable.

[CHECKED] Rejected alternatives:

- packet-sign defect families: non-canonical for the reasons already closed in
  the helical-sign bottleneck mission,
- Tao-role hypergraph observables: not intrinsic for this mission because they
  need desired-channel labels,
- amplitude-only transfer magnitudes: fail the mission because they remove the
  exact phase variable entirely.

## Invariance ledger and event pairing

[VERIFIED] Intrinsic pieces:

- the helical triad law,
- the triad phase variable `Θ_τ` modulo `2π`,
- the exact coefficient phase `arg C_τ`,
- sign-closed summation over all triad terms in the chosen interface ledger,
- and the exact signed transfer contributions `T_{τ,ℓ}`.

[CHECKED] Choice-dependent but admissible observability conventions:

- the smooth filter `G`,
- the interface scale `ℓ`,
- the scale ratio `ρ`,
- and any later time-window parameters used in a delayed-transfer event.

[CHECKED] Harmless-change invariance:

- translation/gauge: survives because `k = p + q` cancels the translation phase;
- conjugation/representative choice: survives when the triad population is
  taken sign-closed and the observable is written in terms of the real transfer
  contributions `T_{τ,ℓ}`;
- packet refinement: irrelevant, because no packet decomposition is used;
- desired-channel relabeling: irrelevant, because the population is all triad
  terms in the interface ledger rather than a chosen witness subset.

[CHECKED] Why the object does not secretly reintroduce packet roles or desired
triads: the only selection principle is "belongs to the exact transfer ledger
across the fixed scale interface `ℓ -> ℓ/ρ`." No Tao-role edge, packet family,
or witness-triad subset appears in the definition.

[CHECKED] Preferred delayed-transfer companion event:

```text
E_ℓ^transfer:
an earlier quiet interval for the exact forward-transfer ledger across `ℓ`,
followed by a short-window positive transfer burst and abrupt gain of the exact
receiver-band energy between `ℓ` and `ℓ/ρ`.
```

[CHECKED] This is the global spectral analogue of the existing physical-space
event `E_flux`. Direct reuse of localized `E_flux` is not preferred here because
the spatial cutoff `φ` destroys the clean helical triad population. But the
same scale-interface philosophy and the same delayed-transfer logic survive.

## Theorem target / counterexample target

[CONJECTURED] Preferred theorem target:

```text
If E_ℓ^transfer occurs on [t_* - Δ, t_*] with short activation window
[t_* - δ, t_*], then sup_{t∈[t_* - δ, t_*]} C_ℓ(t) ≥ c_0
```

for some quantitative threshold `c_0 > 0` determined by the event parameters.

[CONJECTURED] Preferred counterexample target:

```text
Construct or justify an exact-NS or tightly faithful reduced-model delayed
transfer episode E_ℓ^transfer for which sup_{t∈[t_* - δ, t_*]} C_ℓ(t) ≤ c_1
```

with `c_1` uniformly small.

[CHECKED] Smallest-support audit question forced by this pair:

```text
Can the delayed-transfer target remain live while the exact transfer-coherence
ratio C_ℓ stays small on the smallest exact support that still has a nontrivial
phase variable?
```

That is the next honest exploration.

## Gate verdict

```text
pass
```

[CHECKED] Exploration 001 succeeds, but only narrowly.

[CHECKED] What survived:

- one preferred intrinsic phase observable `C_ℓ` / `D_ℓ`,
- one backup observable `A_ℓ`,
- one clean invariance ledger,
- and one delayed-transfer companion event `E_ℓ^transfer` that stays faithful to
  the Tao-facing delayed-handoff mechanism without packet roles.

[CHECKED] What remains unresolved:

- whether `E_ℓ^transfer` is genuinely nontrivial on the smallest honest exact
  support,
- whether `C_ℓ` is more than a dressed-up cancellation ratio in that minimal
  setting,
- and whether the observable is coupled strongly enough to delayed transfer to
  support a firewall rather than a model-level negative.

[CHECKED] The strategy should proceed directly to the smallest honest
exact-support audit of the pair `(C_ℓ, E_ℓ^transfer)`.

## Sources

[VERIFIED] Exact helical interaction law and singleton-support obstructions:

- `/Users/seanross/kingdom_of_god/home-base/current_hunts/big-thinkers/research-systems/codex-atlas/execution/instances/exact-ns-no-near-closed-tao-circuit/strategies/strategy-001/explorations/exploration-002/REPORT.md`
- `/Users/seanross/kingdom_of_god/home-base/current_hunts/big-thinkers/research-systems/codex-atlas/execution/instances/exact-ns-no-near-closed-tao-circuit/library-inbox/exploration-001-definition-gate-near-closed-tao-circuit-report.md`

[CHECKED] Existing delayed-transfer event scaffold:

- `/Users/seanross/kingdom_of_god/home-base/current_hunts/big-thinkers/research-systems/codex-atlas/execution/instances/exact-ns-hidden-precursor-firewall/strategies/strategy-001/explorations/exploration-001/REPORT.md`
- `/Users/seanross/kingdom_of_god/home-base/current_hunts/big-thinkers/research-systems/codex-atlas/execution/agents/library/factual/navier-stokes/exact-ns-physical-space-delayed-transfer-event.md`
