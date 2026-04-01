# Philosopher Atlas (patlas) — Overview

## What It Is

An alternative research architecture to Atlas.
Instead of Atlas's Missionary (broad strategy,
sits idle during execution), patlas uses an
**adversarial planning loop** that produces
step-by-step chains, executes one step at a time,
 and re-evaluates between steps.

## How It Works

Wide Funnel Planning Loop:
  Planner (5 chains)
    → Selector (picks top 3)
    → 3× Attacker (parallel)
    → 3× Judge (parallel)
    → Final Decider (picks winner, merges elements)
    → Strategizer executes Step 1 (launches
  explorers)
    → Results back to Planning Loop
    → Evaluate: replan / proceed / kill
    → Repeat until chain complete or killed

### The Planning Loop (Wide Funnel)

Seven agents run in three phases in the
operator's context (not in tmux). All planning
loop agents run on Opus.

**Phase 1: Generate**

1. **Planner** — Given the mission, generates 3-5
 distinct research chains. Each chain is a
different path to a verifiable result, with
ordered steps, dependencies, expected outputs,
and kill conditions.

**Phase 2: Select and Test**

2. **Selector** — Picks the TOP 3 chains.
Justifies by explaining why each rejected
alternative is worse. Considers diversity,
novelty ceiling, partial-result value, and
risk profile.

3. **3× Attacker** (run in parallel) — Each
attacks one chain. Concrete failure modes,
premise checks, prior art, kill condition
calibration, bias detection. Also attacks the
structural premise of the entire chain.

4. **3× Judge** (run in parallel) — Each
evaluates one attacker's critique as VALID /
PARTIALLY VALID / INVALID. Produces the refined
chain with valid critiques incorporated. Gives a
probability assessment.

**Phase 3: Final Decision**

5. **Final Decider** — Sees all 3 refined chains
with probability assessments. Picks the ONE
winner. May incorporate elements from losing
chains (orientation steps, comparison analyses,
fallback diagnostics) into the winner.

### Why Wide Funnel

Tested against narrow funnel (select 1 → attack
→ judge). Key findings:
- Cross-chain comparison catches framing errors
  that single-chain review misses
- Elements transfer from losing chains enrich
  the winner
- Better negative-result design through
  portfolio comparison

### Execution

Once the planning loop produces a refined chain:

1. Extract Step 1 → write as GOAL.md for the
strategizer
2. Launch strategizer in tmux
(`patlas-strategizer-NNN`)
3. Strategizer decides how many explorations the
step needs, launches explorers
(`patlas-explorer-NNN`)
4. Strategizer writes RESULTS.md when done
5. Operator evaluates:
   - **Kill condition met** → Stop. Write up
negative result.
   - **On track** → Proceed to Step 2.
   - **Picture changed** → Replan (run planning
loop again with new evidence).

### The Strategizer

Receives a scoped step goal (not a broad
strategy). Has autonomy over:
- How many explorations to run
- Which explorer type (Standard Explorer for
literature, Math Explorer for computation)
- What approach to take

Key behaviors:
- **Parallelism principle**: When sub-tasks are
independent, launch separate parallel
explorations
- **No polling**: Uses `run_in_background=true`
to wait for explorers. Never polls status
manually.
- **Library queries**: Checks the library for
relevant prior findings before each exploration

### Explorers

Same as Atlas — run in their own tmux sessions,
produce REPORT.md (incrementally) and
REPORT-SUMMARY.md (last, signals completion).

- **Standard Explorer** (Sonnet) — literature
surveys, conceptual synthesis, theory analysis
- **Math Explorer** (Opus) — computation, formal
verification, counterexample search, proof
attempts

### Library

Independent from Atlas. Lives at `library/`.
Curator processes exploration reports into
factual findings. Receptionist/librarian searches
 the library for relevant context.

## How It Differs from Atlas

| | Atlas | patlas |
|---|---|---|
| **Top-level control** | Missionary (writes broad strategy) | Wide-funnel planning loop (3 chains tested adversarially) |
| **Feedback loop** | ~10 explorations before missionary evaluates | Re-evaluates between every step |
| **Plan testing** | None — missionary commits to a direction | 3 chains attacked and judged in parallel before any budget spent |
| **Strategizer scope** | Full strategy (~10 explorations) | Single step (1-5 explorations) |
| **Replanning** | Missionary writes strategy-002 | Planning loop revises entire remaining chain with new evidence |
| **Kill conditions** | Informal | Explicit checkpoints between every step |
| **Shared resources** | Own library, own agents, own tmux prefix | Fully independent — can run simultaneously |
| **Planning agents** | 1 (missionary) | 7 (planner, selector, 3× attacker, 3× judge, final decider) |

## tmux Naming

All sessions use prefix `patlas-`:
- `patlas-strategizer-001`
- `patlas-explorer-001`, `patlas-explorer-002`,
etc.
- `patlas-curator`

## File Structure

philosopher-atlas/
  patlas-overview.md          ← this file
  CLAUDE.md                   ← quick reference
  agents/
    philosopher/system-prompt.md   ← architecture
 guide (detailed)
    strategizer/system-prompt.md
    explorer/system-prompt.md
    math-explorer/system-prompt.md
  library/
    factual/                  ← knowledge base
    meta/                     ← methodology
learnings
    curator/system-prompt.md
    receptionist/system-prompt.md
  babysitter/
    system-prompt.md
  missions/
    /
      CHAIN.md                ← current refined
chain
      CHAIN-HISTORY.md        ← all planning loop
 runs
      steps/
        step-001/
          GOAL.md             ← scoped goal for
strategizer
          RESULTS.md          ← strategizer
output
          state.json
          REASONING.md
          HISTORY-OF-REPORT-SUMMARIES.md
          explorations/
            exploration-001/
              GOAL.md
              REPORT.md
              REPORT-SUMMARY.md

## Known Issues / Learnings

1. **The attacker can over-correct.** In the
first mission (NS regularity, narrow funnel), the
attacker correctly identified that measuring
individual inequality constants was wrong, but
steered the mission away from ALL computation.
Atlas (without an attacker) just computed things
and got better results. The attacker enforces
consensus with the model's priors, which is
harmful when the correct approach is
counterintuitive. (Same pattern as "critics
reintroduce default priors" from the architecture
exploration benchmarks.)

2. **Wide funnel catches framing errors that
narrow funnel misses.** In the second mission
(Vasseur pressure), the narrow funnel's single
attacker missed a fundamental H^1 vs L^p
confusion. The wide funnel's parallel attackers
comparing across 3 chains caught it through
cross-comparison. This reframing was load-bearing
— it determined whether explorers asked the right
question.

3. **Wide funnel enables element transfer.** The
Final Decider incorporated an orientation step
from Chain 1 and a Caffarelli-Vasseur comparison
from Chain 4 into the Chain 2 winner. These
elements would have been lost in a narrow funnel.

4. **Polling kills token budgets.** A previous
Atlas mission wasted 255M tokens on status-check
polling. The strategizer prompt now explicitly
prohibits polling and requires
`run_in_background=true`.

5. **Parallel explorations are better for
independent sub-tasks.** The strategizer prompt
now includes a "parallelism principle" — split
independent work across focused explorers rather
than overloading one.

## How to Launch a Mission

1. Create `missions/<name>/` directory
2. Run the wide-funnel planning loop in operator
   context:
   a. Planner generates 5 chains
   b. Selector picks top 3
   c. 3× Attacker (launch in parallel)
   d. 3× Judge (launch in parallel)
   e. Final Decider picks winner, merges elements
3. Write CHAIN.md and CHAIN-HISTORY.md
4. Create `steps/step-001/` with GOAL.md,
state.json, REASONING.md, HISTORY
5. Launch strategizer in tmux with its system
prompt
6. Monitor with background wait (not polling)
7. When RESULTS.md appears, evaluate: proceed /
replan / kill
