# Exploration 001 Report

## Executive verdict

[VERIFIED] Decision target:

> Either there exists one preferred intrinsic exact-helical phase/coherence
> observable, with an explicit formula, exact triad population, phase variable,
> normalization, and harmless-change invariance ledger, that can be paired with a
> faithful delayed-transfer event; or all honest candidates still depend on
> non-canonical packet / role bookkeeping, unstable representative choices, or no
> longer contain genuine phase information, so the strategy should stop with the
> correct failure category.

[VERIFIED] Gate verdict: `fail: definition-level failure`.

[CHECKED] The exact single-triad phase variable itself survives. The obstruction
appears at the population level. Once the intrinsic exact triad population is
quotiented by harmless conjugation, an oriented circular phase statistic is no
longer intrinsic, and the only representative-invariant population statistic left
is a conjugation-even transfer-efficiency ratio. That backup object is
mathematically honest on the global all-triad population, but it is too globally
diluted to pair faithfully with the already-fixed delayed-transfer event
`E_flux`; every scientifically meaningful sharpening reintroduces shell/window,
witness-set, or packet-like bookkeeping.

[CHECKED] One key takeaway:

> the exact helical triad phase law is canonical, but no preferred
> population-level phase/coherence observable survives both harmless-change
> invariance and faithful pairing to `E_flux`.

## Exact helical phase law and candidate map

[VERIFIED] The exact helical NS interaction law already fixed in the earlier
singleton audit is the Waleffe helical form

```text
(partial_t + nu|k|^2) u_{s_k}(k)
  = -1/4 sum_{p+q=k} sum_{s_p,s_q}
      (s_p |p| - s_q |q|)
      conj((h_{s_p}(p) x h_{s_q}(q)) . h_{s_k}(k))
      u_{s_p}(p) u_{s_q}(q),
```

with `i k x h_s(k) = s|k| h_s(k)`.

[CHECKED] On a symmetric exact triad

```text
tau = (k,p,q; s_k,s_p,s_q),   k + p + q = 0,
```

the same law can be written in the equivalent conjugated form

```text
(partial_t + nu|k|^2) u_{s_k}(k)
  = sum_{tau : k+p+q=0} C_tau conj(u_{s_p}(p)) conj(u_{s_q}(q)).
```

Write

```text
u_{s_j}(j) = a_j exp(i phi_j),
C_tau = |C_tau| exp(-i psi_tau).
```

Then the exact triad phase variable is

```text
Phi_tau := phi_k + phi_p + phi_q + psi_tau
         = arg(C_tau u_{s_k}(k) u_{s_p}(p) u_{s_q}(q)).
```

[CHECKED] The corresponding exact contribution to the mode-energy equation of leg
`k` is

```text
T_{tau->k} = 2 |C_tau| a_k a_p a_q cos(Phi_tau).
```

So `Phi_tau` is the genuine helical triad phase, while `cos(Phi_tau)` is the
exact phase-to-transfer factor.

[CHECKED] Single-triad invariances:

- Translation invariance: under `u(x) -> u(x+x0)`, the phase shifts sum to
  `(k+p+q).x0 = 0`.
- Helical-basis gauge invariance: rotating the transverse frame changes modal
  phases and the coefficient phase `psi_tau`, but the combination
  `arg(C_tau u_k u_p u_q)` is unchanged.
- Reality / harmless conjugation: for
  `tau_bar = (-k,-p,-q; -s_k,-s_p,-s_q)`,
  `Phi_{tau_bar} = -Phi_tau` and
  `|C_{tau_bar}| a_{-k} a_{-p} a_{-q} = |C_tau| a_k a_p a_q`.

[CHECKED] Candidate map after this invariance screen:

1. `P_circ`: weighted circular concentration of `exp(i Phi_tau)` on an exact
   triad population.
2. `R_eff`: weighted average of `cos(Phi_tau)` on an exact triad population.

[CHECKED] Candidate family 1 keeps the full oriented phase information, but it
will fail harmless-conjugation invariance on the intrinsic exact population.
Candidate family 2 survives the conjugation quotient, but only as a
transfer-efficiency statistic on a chosen population.

## Preferred observable definition

[CHECKED] Preferred candidate attempt:

```text
P_circ,T(t)
  := | sum_[tau]inT w_tau(t) exp(i Phi_tau(t)) |
     / sum_[tau]inT w_tau(t),
```

with

```text
w_tau(t) := |C_tau| a_k(t) a_p(t) a_q(t).
```

[CHECKED] Explicit ledger for this preferred attempt:

- Exact triad population:
  `T = T_all`, the set of exact interacting conjugacy classes
  `[tau] = {tau, tau_bar}` with `C_tau != 0`.
- Exact phase variable:
  `Phi_tau = arg(C_tau u_k u_p u_q)`.
- Normalization:
  divide by total exact coefficient-amplitude weight `sum w_tau`.
- Symmetry / gauge / conjugation convention:
  `Phi_tau` includes the coefficient phase, so it is translation- and
  gauge-invariant; the population is quotiented by harmless conjugation.
- Exact sense in which it measures phase rather than amplitude only:
  if the amplitudes are frozen and only the modal phases are changed,
  `P_circ,T` changes through `exp(i Phi_tau)`.

[CHECKED] Why this looked like the right preferred object:

- it uses exact helical triads directly,
- it introduces no Tao role labels, desired edges, packet families, or witness
  triads,
- and it keeps the phase variable explicit instead of collapsing immediately to a
  signed-transfer scalar.

[VERIFIED] Why `P_circ,T_all` is inadmissible:

- The intrinsic exact population is the conjugacy-class population `[tau]`, not
  an arbitrarily oriented list of representatives.
- Replacing `tau` by `tau_bar` sends `Phi_tau -> -Phi_tau` while leaving `w_tau`
  unchanged.
- Therefore `exp(i Phi_tau)` is not an intrinsic class function on `[tau]`.
- Any rule that chooses one orientation inside each class is an extra convention,
  not exact NS data.
- Counting both orientations does not rescue the object:

```text
exp(i Phi_tau) + exp(-i Phi_tau) = 2 cos(Phi_tau),
```

  so the circular concentration collapses into a conjugation-even scalar and no
  longer measures an oriented phase concentration on `S^1`.

[CHECKED] One-sentence role-label ledger:

> `P_circ,T_all` does not secretly reintroduce packet roles or desired Tao edges,
> because it averages over the full exact interacting population with only exact
> coefficient-amplitude weights; it fails for conjugation-sign reasons instead.

## Backup observable or rejection of alternatives

[CHECKED] The only honest backup left after quotienting by conjugation is the
conjugation-even transfer-efficiency observable

```text
R_all(t)
  := sum_[tau]inT_all w_tau(t) cos(Phi_tau(t))
     / sum_[tau]inT_all w_tau(t),
```

again with `w_tau = |C_tau| a_k a_p a_q`.

[CHECKED] Explicit ledger for the backup:

- Exact triad population:
  `T_all`, all exact interacting conjugacy classes with `C_tau != 0`.
- Exact phase variable:
  the same gauge-corrected `Phi_tau`.
- Normalization:
  total exact coefficient-amplitude weight over `T_all`.
- Symmetry / gauge / conjugation convention:
  `cos(Phi_tau)` is invariant under `Phi_tau -> -Phi_tau`, so `R_all` is
  representative-invariant on conjugacy classes.
- Exact sense in which it measures phase rather than amplitude only:
  with amplitudes fixed, changing `Phi_tau` changes `cos(Phi_tau)` and therefore
  `R_all`.

[CHECKED] `R_all` is the cleanest remaining exact object, but it is not an
acceptable preferred observable for this mission.

[VERIFIED] Reason 1: it is scientifically too global. Primary 3D triad-phase
diagnostics on helical decompositions report that the forward transfer toward
small scales is carried by only a very small subset of helical triads, not by
the whole exact population. A global all-triad average therefore dilutes exactly
the rare triads that would matter for a delayed-transfer event.

[CHECKED] Reason 2: every meaningful sharpening reintroduces forbidden choices.
To make `R_eff` track the delayed-transfer event, one would have to replace
`T_all` by something like:

- triads crossing one shell or one chosen scale window,
- the top flux-carrying triads on a time window,
- triads inside a localized Fourier / Gabor packet,
- or a witness set tied to the later burst.

Each of those narrows the population by shell width, packet window, threshold, or
post hoc witness bookkeeping. Those are exactly the harmless-change instabilities
the gate forbids.

[CHECKED] Reason 3: if one instead ties the observable directly to the same local
filtered burst used in `E_flux`, the object stops being an independent helical
phase observable and becomes the same signed-transfer ledger in different words.
That is not the requested phase object.

[CHECKED] Rejected alternatives:

- shell-local phase concentration:
  non-canonical shell/window/interface bookkeeping;
- flux-carrying-triad concentration:
  post hoc target-set choice;
- localized Fourier packet / Gabor phase observable:
  packet/window dependence under a new name;
- packet-sign defect families:
  already closed non-canonical backups.

## Invariance ledger and event pairing

[CHECKED] Invariance ledger.

Intrinsic exact data:

- the exact helical triad law and coefficient `C_tau`,
- the gauge-corrected single-triad phase `Phi_tau = arg(C_tau u_k u_p u_q)`,
- the exact coefficient-amplitude weight `w_tau = |C_tau| a_k a_p a_q`,
- the conjugation-even factor `cos(Phi_tau)`,
- and the global exact population `T_all`.

Still choice-dependent or inadmissible:

- any oriented phase statistic using `exp(i Phi_tau)` on conjugacy classes,
- any shell-window or interface-width refinement used to localize the population,
- any packet / Gabor / localized Fourier window,
- any top-contributor threshold or witness-triad subset,
- and any desired-forward target set modeled on Tao edges.

[VERIFIED] Preferred delayed-transfer companion event remains the already-fixed
exact physical-space event `E_flux`, defined by a localized positive forward-flux
burst plus witness gain on a fixed parabolic cylinder.

[CHECKED] Honest pairing verdict with `E_flux`: pairing fails.

[CHECKED] Why the pairing fails sharply:

- `E_flux` is localized in physical space and includes the positive-part burst
  condition plus witness activation on a fixed cylinder.
- The only canonically frozen triad observable left after the conjugation quotient
  is `R_all`, which lives on the global all-triad population.
- Primary 3D helical phase studies indicate that only a small subset carries the
  forward transfer, so `R_all` is too diluted to be a faithful companion to a
  localized burst event.
- Any attempt to isolate the relevant subset of triads requires shell, window, or
  witness conventions that are not intrinsic exact NS data.

[CHECKED] Therefore the existing `E_flux` event is usable in principle, but no
surviving canonically frozen helical phase observable pairs to it honestly.

## Theorem target / counterexample target

[CHECKED] If one nevertheless forced the backup object into a theorem target, the
cleanest remaining statement would be

```text
E_flux(x_*, t_*; ell, rho, r, Delta, delta)
  => sup_{t in [t_* - delta, t_*]} R_all(t) >= c(ell, rho, r, Delta, delta).
```

[CHECKED] The corresponding adversarial counterexample target would be

```text
find an exact NS solution segment with E_flux on the fixed cylinder
while sup_{t in [t_* - delta, t_*]} |R_all(t)| <= eps,
```

for arbitrarily small `eps`, by concentrating the local transfer on a tiny subset
of helical triads while the global all-triad average stays small.

[CHECKED] These are the right theorem/counterexample targets only for the rejected
backup. They are not authorized as the mission's live targets because the backup
does not pass the pairing gate.

## Gate verdict

[VERIFIED] Explicit gate verdict: `fail`.

[VERIFIED] Failure category: `definition-level failure`.

[CHECKED] This is not the right place to downgrade to `model-level failure`. The
line dies before the smallest-support or coupling audit of one frozen preferred
object, because the preferred phase-concentration candidate fails harmless-change
invariance and the only representative-invariant backup cannot be localized toward
`E_flux` without reintroducing non-canonical bookkeeping.

[CHECKED] Next-step implication: stop this strategy at Phase 0 rather than
proceeding to a smallest exact-support audit on a fake object.

## Sources used

[VERIFIED] Local sources:

- `execution/instances/exact-ns-phase-locking-firewall/strategies/strategy-001/STRATEGY.md`
- `execution/instances/exact-ns-phase-locking-firewall/MISSION.md`
- `execution/instances/exact-ns-phase-locking-firewall/MISSION-VALIDATION-GUIDE.md`
- `runtime/results/codex-atlas-exact-ns-phase-locking-firewall-strategy-001-receptionist-e001.md`
- `execution/agents/library/factual/navier-stokes/exact-helical-near-closed-tao-circuit-definition.md`
- `execution/agents/library/factual/navier-stokes/exact-singleton-tao-circuit-nonembeddability.md`
- `execution/agents/library/factual/navier-stokes/packetized-tao-circuit-noncanonical.md`
- `execution/agents/library/factual/navier-stokes/exact-ns-helical-sign-canonicity-failure.md`
- `execution/agents/library/factual/navier-stokes/exact-ns-physical-space-delayed-transfer-event.md`
- `execution/agents/library/meta/goal-design/require-harmless-change-invariance-for-observables.md`
- `execution/agents/library/meta/methodology/definition-extraction-gates-computation.md`
- `execution/instances/exact-ns-no-near-closed-tao-circuit/strategies/strategy-001/explorations/exploration-002/REPORT.md`

[VERIFIED] Primary-source external references consulted:

- Fabian Waleffe, "The nature of triad interactions in homogeneous turbulence,"
  Phys. Fluids A 4 (1992), DOI `10.1063/1.858309`, NASA NTRS record:
  <https://ntrs.nasa.gov/citations/19920038608>.
- Fabian Waleffe, "The helical decomposition and the instability assumption,"
  CTR Annual Research Briefs (1994), NASA PDF:
  <https://ntrs.nasa.gov/api/citations/19940007834/downloads/19940007834.pdf>.
- Di Kang, Bartosz Protas, Miguel D. Bustamante,
  "Alignments of Triad Phases in 1D Burgers and 3D Navier-Stokes Flows,"
  arXiv:2105.09425, abstract page:
  <https://arxiv.org/abs/2105.09425>.
- Brendan Murray, "Fourier Phase Dynamics in Turbulent Non-Linear Systems,"
  UCD PhD thesis repository page:
  <https://researchrepository.ucd.ie/entities/publication/14e94dc3-97a0-4564-9caa-9928b28ea083>.
