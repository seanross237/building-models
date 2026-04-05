# April 2 NS Pursuit Plan

This document defines the operating plan for the next Navier-Stokes regularity push.

The target is not another broad survey. The target is to identify a genuinely new proof path for the 3D Navier-Stokes regularity problem and pursue it hard enough to learn whether it can survive contact with real mathematics.

## Canonical Starting Point

Before doing anything else, every lead agent must read:

- `current-status-of-navier-stokes.md`

Treat that file as the authoritative frontier map. If an older mission document, planning memo, or library note conflicts with it, the status file wins.

The first job is to understand:

- which routes are already closed
- which structural obstructions are durable
- which partial mechanisms still look alive
- which surviving gaps are real rather than just rhetorical

## Phase 1: Review the Current NS Status

The initial agent should produce a short orientation memo after reviewing `current-status-of-navier-stokes.md`.

That memo should answer:

- What classes of approaches have already failed?
- Why did they fail?
- Which failures look fundamental versus implementation-specific?
- What fragments or mechanisms still seem load-bearing?
- What kinds of new approaches would actually count as novel now?

Novel here means:

- not just rewording an already-closed route
- not just shifting notation around an old obstruction
- not just retrying a failed program with weaker evidence
- explicitly different in object class, mechanism, scale-bridging strategy, or proof architecture

## Phase 2: Generate 10 Novel Angles

After the review, generate 10 new angles of attack that could plausibly matter for the Millennium Prize problem.

Each angle must include:

- a short name
- the core idea in 3-6 sentences
- what makes it genuinely different from prior closed routes
- which obstruction from `current-status-of-navier-stokes.md` it is trying to bypass
- what the first concrete theorem-object, invariant, or mechanism would need to be
- what evidence would make the angle more plausible
- what evidence would kill it quickly

The standard is novelty plus theorem-facing structure. Do not accept vague programs like "use better harmonic analysis" or "combine geometry and PDE more deeply" unless they come with a concrete new object and a specific reason prior obstructions may not apply.

## Phase 3: One Agent Per Angle

Assign one agent to each of the 10 angles.

Each agent should explore the plausibility of its angle, not just advocate for it. The job is adversarially honest exploration.

Each angle agent should produce:

- a concise statement of the proposed route
- a check against the known obstructions in `current-status-of-navier-stokes.md`
- the strongest argument for why the route might work
- the strongest argument for why it probably fails
- the first 2-5 concrete subproblems that would need to be solved
- whether the route appears theorem-facing, mechanism-facing, or mostly speculative
- a final verdict: `promising`, `weakly promising`, `unclear`, or `dead`

Agents should prefer early falsification over inflated optimism. If an angle collapses under the existing status memo, say so directly.

## Phase 4: Choose the Top Path

After the 10 explorations finish, compare them and select the single strongest path.

Selection should prioritize:

- genuine novelty relative to prior closed branches
- a concrete theorem-object or mechanism to pursue
- ability to survive the known obstructions
- plausibility of producing a real intermediate result
- depth of runway if the first step works

Do not choose the most elegant idea if another one has a better chance of producing a real foothold.

## Phase 5: Pursue the Best Path Aggressively

Once the top path is chosen, pursue it continuously for as long as it remains the most promising route.

That pursuit should be iterative:

1. define the next sharp subproblem
2. assign an agent or small set of agents to attack it
3. evaluate the result honestly
4. refine the path, narrow it, or kill it if the evidence turns against it
5. continue only while it remains the best available frontier

This is not a one-shot brainstorming exercise. The chosen angle should be pushed into concrete lemmas, explicit model problems, proof skeletons, obstruction checks, and failure analysis.

## Status Update Requirement

Any meaningful finding from this process must be folded back into:

- `current-status-of-navier-stokes.md`

This includes:

- newly closed routes
- newly identified structural obstructions
- newly promoted mechanisms that survived scrutiny
- any theorem-facing object that appears durable enough to carry forward
- any change in what now looks faintly worth trying

The status file should remain the canonical memory of the NS effort. Agents should not let new learnings remain trapped inside isolated mission artifacts if those learnings materially change the frontier picture.

## Working Standard

The bar for success is not "generate interesting thoughts."

The bar is:

- produce genuinely new angles
- eliminate weak ones quickly
- identify one path worth concentrated pursuit
- keep pushing that path until it is no longer the best option
- update the canonical NS status document whenever the frontier meaningfully changes
