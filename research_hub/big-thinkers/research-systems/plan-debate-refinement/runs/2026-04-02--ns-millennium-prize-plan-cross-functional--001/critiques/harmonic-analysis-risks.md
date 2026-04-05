# Critique: Harmonic Analysis / Pressure / Nonlinear-Estimate Risks

## Strongest objections

### 1. The main route quietly reopens a route the status file already says is closed

The draft defaults to a minimal-blowup contradiction in `L^3`, but the status
file explicitly says standard compactness-rigidity host spaces such as `L^3`,
`\dot H^{1/2}`, and `BMO^{-1}` have already failed to supply a viable
Navier-Stokes-specific extraction package. So "`L^3` by default" is not a
neutral starting point. It is reopening a locally closed route without naming a
new ingredient that escapes the closure.

If the new ingredient is supposed to be "canonical one-bridge extraction," that
is still not enough. The status file also says the Tao-adjacent line is blocked
at `exact non-isolability / arbitrary-truncation requirement` and then again at
`source-basis / no-canonical-finite-reduction`. The draft currently behaves as
if canonicity is mainly a definitions problem. The status file says it is a
structural problem.

### 2. The plan mistakes exact local structure for theorem-bearing PDE leverage

An exact one-bridge object, even if canonically defined, is not yet a
contradiction mechanism. The nonlinear term in NS is not defeated by having a
clean local interaction picture. One still needs a one-sided, scale-appropriate
estimate that survives:

- the full quadratic interaction sum,
- pressure recovery `p = R_i R_j(u_i u_j)`,
- localization/commutator debt,
- symmetry actions,
- and compactness limits.

The draft jumps from "canonical extraction" to "obstruction theorem on that
object" without specifying what analytic quantity is controlled on the PDE side.
That is exactly where these routes usually die.

### 3. Pressure is almost absent from the main contradiction chain

From this lens, that is the largest gap in the draft.

The status file already closes:

- De Giorgi/Vasseur pressure improvement,
- the `H^1` pressure repair at the `W^{1,3}` wall,
- and the harmonic far-field loophole.

So any new plan that hopes to touch full regularity has to say very early how
its object interacts with the nonlocal pressure mechanism. Not in slogan form.
In theorem form. In particular:

- what pressure quantity is inherited under extraction,
- how low-frequency/far-field tails are controlled,
- why the object gives something stronger than a rephrasing of the same
  Calderon-Zygmund debt,
- and what one-sided gain is obtained after pressure is restored.

Without that, the route is not really an NS route. It is an exact-substructure
route with no demonstrated access to the obstruction.

### 4. Phase ordering is backwards

Phase 0 says "freeze the object layer" before the PDE bridge is really earned.
That is the wrong order for a problem with this failure history.

The first thing that should be frozen is not the object. It is the analytic
gain the object is supposed to produce. If the plan cannot state a scale-invariant
coercive quantity on the NS side that improves after extraction, then spending
time on canonicity, provenance, refinement stability, and reconstruction is
mostly bookkeeping around a non-mechanism.

### 5. Template-defect and leakage are being over-credited

The draft treats repaired template-defect and repaired leakage as the natural
subordinate tests once extraction succeeds. That is too optimistic.

The status file only supports these as frozen packet-screen objects on one
ledger, not as PDE-effective inequalities. There is still no proof that they
control any quantity that rules out a critical element once pressure,
localization, and recursive closure debt are reinstated. This is exactly where
"exact local structure" can be mathematically real and still useless for
regularity.

### 6. The fallback route is too close to the route already killed by the status file

The proposed fallback is "combined strain alignment plus vorticity-direction
coherence, aimed at a Constantin-Fefferman-type consequence." That is not yet a
genuinely different route.

The status file says the `e_2`-alignment line is structurally blocked because
`s_2 > 0` persists in high-vorticity regions and `e_2`-alignment suppresses the
feedback that could reverse it. It also says direct pressure-Hessian
self-damping is dead. So a fallback framed as "alignment plus coherence" is
dangerously close to repackaging the same obstruction unless it states a new
mechanism that controls the magnitude, not just the direction, of stretching in
a scale-critical way.

## Missing assumptions or prerequisites

### 1. A new ingredient escaping the existing host-space closure

If `L^3` remains the default host space, the plan must explicitly state what
new structure is available now that was not present in the already audited
`L^3`/`\dot H^{1/2}`/`BMO^{-1}` attempts. Without that, the route is just
reopening a failed compactness-rigidity template.

### 2. An exact pressure-stability statement under extraction

The plan needs a theorem-shaped prerequisite of the form:

"the extracted object controls or reflects a scale-invariant quantity that
survives reconstruction of the full pressure term."

Right now there is no such statement.

### 3. A precise nonlinear quantity with one-sided sign or coercivity

What is the contradiction supposed to come from?

- a flux lower bound?
- a bilinear interaction defect?
- a depletion of vortex stretching?
- a coercive lower bound on leakage after normalization?

Until that is named precisely, "obstruction theorem" is a placeholder.

### 4. Symmetry and profile-decomposition compatibility

The extraction lemma must survive:

- scaling,
- translation,
- rotation if relevant,
- Galilean drift,
- weak convergence/nonlinear profile decomposition,
- and harmless refinement without changing the claimed bad quantity.

The draft says some of these words, but it does not recognize that this is
where the current object family has already broken.

### 5. For the fallback: a hypothesis that is not merely `e_2` alignment in disguise

If the fallback is serious, it must specify:

- the exact criterion it is strengthening or verifying,
- the scale-critical norm/topology in which coherence is measured,
- and why the hypothesis is not implied by, or equivalent to, the already
  blocked `e_2`-alignment picture plus known positive-`s_2` dynamics.

## Concrete revisions

### 1. Replace the `L^3` default with a hard prerequisite gate

Do not say "defaulting to `L^3`." Say instead:

"No critical-element route is active until a Navier-Stokes-specific extraction
mechanism is identified that is not already ruled out by the status-file
closure for `L^3`, `\dot H^{1/2}`, and `BMO^{-1}`."

If no such mechanism can be written in one page, stop the main route
immediately.

### 2. Move the pressure/nonlinearity gate ahead of object freezing

Before Phase 0, insert a new gate:

- write the exact scale-invariant quantity to be improved,
- write how pressure is reconstructed and estimated after extraction,
- write why this is not another exact rewrite with restored localization debt.

If that gate fails, do not spend time refining the object layer.

### 3. Demote template-defect and leakage from "theorem horizon" to "kill tests"

Use them only to answer the narrower question:

"Do these screens produce any PDE-stable one-sided inequality once pressure and
symmetry debt are restored?"

If not, they should terminate the route, not extend it.

### 4. Rewrite the fallback so it cannot collapse back to the blocked alignment route

Forbid vague "alignment/coherence" language. Require instead:

- one theorem statement in standard PDE form,
- one explicit scale-critical control quantity,
- one argument for why it changes the sign or size of the stretching term,
  rather than merely its direction,
- one explanation of why the status-file `s_2 > 0` obstruction does not simply
  reappear.

If this cannot be stated precisely, the fallback is not live.

### 5. Add an explicit no-go option as a success condition

Given the status file, a credible positive outcome is not only "advance the
Millennium route." Another credible outcome is:

- prove that no canonical extraction of the current one-bridge/packet family can
  be compatible with critical-element compactness and pressure stability.

That would be theorem-bearing negative progress and is more honest than letting
the plan drift into another object-definition campaign.

## Salvageability

The plan is salvageable without a full rewrite only in a narrower sense than the
draft currently suggests.

It is salvageable if it is rewritten into a short, brutal prerequisite program:

1. prove there is a genuinely new extraction mechanism not already killed by the
   status file;
2. prove that it survives pressure reconstruction and nonlinear profile debt;
3. only then ask whether template-defect or leakage produce a contradiction.

Without those revisions, the main route is not a serious prize-facing NS plan.
It is a refined restatement of the same packet/extraction hope after the
repository has already recorded why that hope keeps failing.

The fallback is also salvageable, but only if it abandons generic
alignment-language and states a quantitatively new, scale-critical depletion
mechanism that does not reduce to the blocked `e_2` picture.
