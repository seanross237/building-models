# Mission: Exact NS No-Near-Closed Tao Circuit

## Why This Mission Exists

The latest Codex Atlas mission on Tao's averaged-NS blowup mechanism reached a
sharp mechanism-level negative result:

- Tao's blowup depends on a near-isolated five-mode delayed-threshold circuit.
- The strongest surviving exact-NS contrast is that real Navier-Stokes may be
  too interaction-entangled to realize that circuit cleanly.
- That contrast did **not** yet sharpen into a usable theorem object.

The Atlas result explicitly recommended a narrower follow-up:

```text
formalize and test an exact Fourier/helical no-near-closed-Tao-circuit theorem
```

This mission is that follow-up, but in `patlas` form.

## The Question

Can one formulate and test a quantitative "no near-closed Tao circuit"
statement for exact Navier-Stokes?

The target is not a regularity proof directly. The target is one concrete
mathematical object:

- an impossibility theorem
- a lower bound on unavoidable spectator leakage
- a rigidity statement for exact triadic or helical couplings
- or a counterexample showing the whole idea is false

Either a positive obstruction or a negative kill is a valid success state.

## Atlas Source Basis

This mission should treat the following copied Atlas artifacts as established
local context:

- `atlas-source/atlas-anatomy-of-averaged-ns-blowup-firewall-MISSION-COMPLETE.md`
- `atlas-source/atlas-anatomy-of-averaged-ns-blowup-firewall-FINAL-REPORT.md`
- `atlas-source/atlas-anatomy-exploration-001-REPORT.md`
- `atlas-source/atlas-anatomy-exploration-002-REPORT.md`
- `atlas-source/atlas-exact-ns-no-near-closed-tao-circuit-MISSION.md`

Key inherited result:

```text
exact-NS circuit non-isolability
```

is the strongest surviving candidate discrepancy, but it is still only a
mechanism-level insight until made quantitative.

## What Success Looks Like

One of the following:

1. **Positive obstruction**

   A precise statement of the form:

   - any exact-NS mode packet approximating Tao's five-stage circuit must
     generate unavoidable extra couplings of size at least `...`
   - or no almost-closed subsystem with Tao's pump/amplifier/rotor hierarchy
     can exist under exact NS triadic geometry and exact Leray projection

2. **Negative kill**

   A concrete exact-NS or helical/Fourier model shows that a near-closed
   Tao-like circuit is in fact possible, so this firewall idea should be
   dropped.

3. **Definition-level obstruction**

   The notion can be made only in ways that are too vague, too unstable, or
   too unconstrained to support a real theorem test.

## Moonshot Bias

This mission should prefer one genuinely high-upside chain over a portfolio of
only tidy obstruction audits.

Specifically:

- include at least one chain whose primary success mode is a theorem-shaped
  impossibility statement or an explicit near-circuit construction, not merely
  a better audit memo;
- accept a lower "useful failure" floor for that chain if its ceiling is much
  higher;
- prefer direct exact-mode or helical-model testing over branches that spend
  most of their budget refining definitions without ever touching a concrete
  subsystem;
- if forced to choose between a careful medium-upside audit branch and a
  credible high-upside explicit-construction or no-circuit theorem branch, lean
  toward keeping the moonshot in the top portfolio.

The point of this mission is to test whether the Atlas mechanism insight can be
turned into a real mathematical object. Planning should not optimize only for
safe negative results.

## What Failure Looks Like

- "Near-closed Tao circuit" cannot be defined concretely.
- The definition can be written but cannot be tested even in a simplified
  Fourier/helical setting.
- The candidate collapses back into vague language about "entanglement" with no
  quantitative content.

These are still valid bounded negative outcomes if written sharply.

## Established Results (Do Not Re-Derive)

- De Giorgi / epsilon-regularity / pressure / host-space routes are already
  heavily screened or closed at estimate level.
- The far-field harmonic pressure loophole is closed.
- Tao's averaged-NS cascade has already been reconstructed at mechanism level.
- The prior Atlas mission already identified the strongest qualitative live
  candidate:

  ```text
  exact-NS circuit non-isolability
  ```

Do not repeat those earlier analyses from scratch. Start from the inherited
Atlas source packet and move immediately toward formalization and test.

## What Must Be Avoided

- Do **not** drift back into generic estimate improvement.
- Do **not** re-survey Tao's paper broadly.
- Do **not** accept a slogan like "NS has too much coupling" as a result.
- Do **not** attempt a full regularity proof.
- Do **not** count a narrative contrast as success unless it becomes a
  definition, lower bound, rigidity statement, or counterexample.

## Core Mission Structure

### Step 1: Define a Tao-like circuit quantitatively

Using the inherited Atlas mechanism reconstruction, define the smallest exact
notion of a Tao-like circuit in terms of:

- a finite set of active modes or helical mode packets
- a target coupling graph
- desired hierarchy of dominant couplings
- admissible spectator couplings or leakage
- threshold or timescale separation conditions

The definition can be simplified, but it must be concrete enough to test.

**Deliverable:** a definition or small family of definitions for
`near-closed Tao circuit`.

**Kill condition:** if no precise definition can be made, stop and report that
the idea is too vague to pursue.

### Step 2: Translate exact NS into the right language

Work in the most appropriate exact framework, likely:

- Fourier triads
- helical decomposition
- exact Leray-projected bilinear interactions

Recover the exact interaction law relevant to the candidate circuit and
identify:

- which couplings are desired
- which extra couplings are forced automatically
- which are forbidden by geometry or helicity selection
- which can be tuned by mode choice and which cannot

**Deliverable:** a concrete interaction table for the exact-NS candidate
subsystem.

### Step 3: Test the obstruction

Choose the smallest meaningful configuration and ask:

- can the Tao-like desired couplings dominate?
- do unavoidable spectator couplings exceed any reasonable leakage threshold?
- is there a lower bound on leakage coming from exact triadic geometry or Leray
  projection?
- or can a clever helical or geometric choice suppress enough unwanted
  couplings to realize a near-circuit?

This may be analytical, computational, or mixed, but the mission should prefer
small explicit test objects over diffuse symbolic rhetoric.

**Deliverable:** either

- a quantitative no-circuit / leakage lower bound

or

- a concrete near-circuit construction showing the obstruction fails

### Step 4: Final report

One of three outcomes:

1. **Concrete no-circuit statement found**
2. **Counterexample / near-circuit found**
3. **Definition-level failure: idea too vague or too unconstrained**

## Budget

3-5 explorations total.

Expected shape:

- 1 exploration to define the object
- 1 exploration to compute exact NS couplings
- 1 exploration to prove or disprove near-closure
- optional adversarial stress test

## Why `patlas` Is A Good Fit

This mission is narrow enough for adversarial planning to help:

- the planner can generate genuinely different formalization strategies
- attackers can punish vague definitions and fake theorem objects early
- judges can force the winning plan to lock one exact target and one exact test
  configuration before any momentum builds

The mission should favor early kill conditions over broad speculative
exploration.

## Planner Steering Note

During planning and selection, explicitly consider at least these two very
different high-value directions:

1. **No-circuit theorem route**
   Fix a minimal exact Fourier/helical subsystem and try to prove a lower bound
   on unavoidable spectator leakage or a rigidity obstruction to Tao-style gate
   isolation.

2. **Near-circuit construction route**
   Treat the firewall idea adversarially and search for the smallest exact-NS
   or helical configuration that approximately realizes Tao-like pump /
   amplifier / rotor logic. If such a configuration survives honest exact
   coupling accounting, that kills the firewall idea cleanly and quickly.

A planning run that omits both of these and drifts toward only definitional
cleanup is under-ambitious for this mission.
