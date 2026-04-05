# Exploration 002 Report

## Decision target

Either there exists one preferred precursor observable `P` and one earlier region `R_-` for the exact-NS event `E_flux` such that `P` is dynamically tied to the delayed-transfer burst without merely restating the event earlier in time and without collapsing into a closed route, or no such precursor pair survives and the strategy should stop with the correct failure category.

## 1. Executive verdict

[CHECKED] The gate passes, but only with a narrow choice.

[CHECKED] The preferred precursor is not Lamb-vector geometry, not vortex stretching, and not a second event definition. It is the **earlier cumulative positive forward flux mass** through the same scale interface as `E_flux`, measured on a fixed predecessor cylinder:

```text
P_flux^-(R_-)
  = integral_{t_* - Delta}^{t_* - delta} integral_{B_r(x_*)} (Pi_ell(x,t))_+ dx dt.
```

[CHECKED] The preferred earlier region is the backward parabolic cylinder already implicit in the Phase 0 event data:

```text
R_- = B_r(x_*) x [t_* - Delta, t_* - delta].
```

[CHECKED] This pair survives because:

- it is measured on exact NS itself,
- it is dynamically tied to the later burst by the same filtered energy-transfer law,
- it is not a pressure / De Giorgi / epsilon-regularity rewrite,
- it is less tautological than using the event window itself, because it measures cumulative pre-burst transfer mass on a disjoint earlier interval and does not include the witness-gain clause.

[CHECKED] A backup survives, but only as backup: earlier Duchon-Robert activity on the same predecessor cylinder.

[CHECKED] The next exploration should directly test whether small `P_flux^-` on `R_-` rules out the later event `E_flux`, or whether an exact/fidelity-respecting counterexample remains possible.

## 2. Candidate precursor audit

[CHECKED] Candidate A: **earlier-region flux activity tied to the same scale interface**

This is the closest live candidate to the exact event:

- same exact transfer law `Pi_ell`,
- same physical-space localization,
- same scale interface that defines the delayed handoff.

[CHECKED] Tautology risk:

- If the candidate were simply "the same burst quantity on a slightly earlier slice," it would fail.
- The surviving version is **integrated pre-burst flux mass on the disjoint earlier slab** `R_-`, with no witness-gain clause.

[CHECKED] This is still close to the event, but that closeness is a strength rather than a bug: the hidden-precursor question is precisely whether the same transfer mechanism must already leave earlier measurable trace before the burst.

[CHECKED] Candidate B: **earlier Duchon-Robert activity**

This remains physically meaningful and exact-NS faithful. It measures short-scale transfer via local increments, not via the filtered stress tensor.

[CHECKED] Weaknesses:

- it is less directly a precursor to the preferred event than `P_flux^-`,
- it tends to slide toward a singularity-detection framing rather than a delayed-handoff framing,
- it gives up the clean witness-channel tie to `W`.

[CHECKED] Candidate C: **Lamb-vector / Beltrami-deficit geometry**

Rejected as preferred.

[VERIFIED] The local library already records the decisive weakness: near-Beltrami advantage collapses under tiny perturbations, so the mechanism is too fragile and too close to the already-closed pressure-side story to anchor the preferred precursor here.

[CHECKED] Candidate D: **vortex stretching / enstrophy production**

Rejected as preferred.

[CHECKED] These quantities measure amplification or activity in general. They are not naturally tied to the declared scale interface or witness channel of `E_flux`, and they risk turning the mission into a generic pre-blowup activity search.

## 3. Preferred precursor-and-region pair

[CHECKED] Preferred precursor observable:

```text
P_flux^-(R_-)
  = integral_{t_* - Delta}^{t_* - delta} integral_{B_r(x_*)} (Pi_ell(x,t))_+ dx dt.
```

[CHECKED] Preferred earlier region:

```text
R_- = B_r(x_*) x [t_* - Delta, t_* - delta].
```

[CHECKED] Smallness condition representing "no earlier warning":

```text
P_flux^-(R_-) <= epsilon_prec.
```

[CHECKED] Why this pair is dynamically tied to `E_flux`:

- `E_flux` itself is a later burst in the same transfer rate `Pi_ell`,
- the witness channel `W` rises only because forward transfer through `ell` has accumulated,
- so earlier accumulated positive flux is the most faithful physically observable precursor candidate.

[CHECKED] Why this is not just the event restated:

- the event uses the later activation window `[t_* - delta, t_*]`,
- the precursor uses the earlier disjoint slab `[t_* - Delta, t_* - delta]`,
- the event requires both burst rate and witness gain,
- the precursor requires only cumulative earlier transfer mass and no witness clause.

[CHECKED] There is still an adversarial closeness issue, but it is now sharp enough to test rather than vague enough to reject immediately.

## 4. Backup pair or rejection of alternatives

[CHECKED] Backup precursor:

```text
P_DR^-(R_-)
  = integral_{t_* - Delta}^{t_* - delta} integral_{B_r(x_*)} (D_ell(u)(x,t))_+ dx dt.
```

[CHECKED] Why only backup:

- it is one step less directly tied to the preferred witness channel,
- it is easier to reinterpret as a singularity detector,
- it is therefore less clean for the delayed-transfer question than `P_flux^-`.

[CHECKED] Rejected region alternatives:

- **Backward cone / enlarged predecessor ball**: not chosen as preferred because the local library does not fix any canonical variant, and adding extra geometry would widen the observability conventions without yet buying clarity.
- **Window chosen after the fact**: rejected by design. The predecessor slab is the literal earlier portion of the same declared cylinder from exploration 001.

[CHECKED] Rejected precursor families:

- Lamb/Beltrami: too fragile and pressure-adjacent.
- Vortex stretching / enstrophy production: too generic and not naturally scale-interface-specific.
- "Same burst quantity, slightly earlier": rejected as the tautological version of the flux precursor.

## 5. Fidelity ledger and tautology/closed-route screen

[CHECKED] Fidelity ledger:

- measured on exact NS itself,
- uses the exact filtered transfer observable already fixed in exploration 001,
- introduces no reduced dynamical model,
- changes only the observation window from the later event slab to the earlier predecessor slab.

[CHECKED] Tautology screen:

- **Rejected tautology**: "precursor = `F_ell` on a nearby earlier time slice."
- **Accepted sharpened precursor**: integrated earlier transfer mass on a fixed disjoint earlier region, without the witness-gain clause.

[CHECKED] Closed-route screen:

- not a pressure-improvement quantity,
- not a De Giorgi recurrence statistic,
- not an epsilon-regularity criterion under new language,
- not a generic regularity norm.

[CHECKED] This is still the same physical transfer mechanism family as the event, but that is permissible. The mission asks for an earlier physical warning, not necessarily a different PDE quantity family.

## 6. Gate analysis and pass/fail verdict

[CHECKED] Lower-bound theorem target:

```text
If E_flux occurs later on Q, then P_flux^-(R_-) must exceed a quantitative lower bound
depending on the event thresholds and geometry.
```

[CHECKED] No-hidden-transfer target:

```text
If P_flux^-(R_-) <= epsilon_prec, then the later delayed-transfer event E_flux cannot occur.
```

[CHECKED] Counterexample target:

```text
Produce an exact-NS or faithful reduced-model scenario where P_flux^-(R_-) is small but E_flux
still occurs later.
```

[CHECKED] Failure of the precursor gate would have meant:

- every precursor is tautological,
- or every non-tautological candidate is generic / fragile / route-closed.

[CHECKED] That failure did not occur. One pair survives sharply enough to test.

## Pass/Fail Verdict

```text
pass
```

[CHECKED] Exploration 002 succeeds. The strategy should proceed to the first quantitative hidden-precursor test using the pair `(E_flux, P_flux^-)`, with Duchon-Robert retained only as backup.
