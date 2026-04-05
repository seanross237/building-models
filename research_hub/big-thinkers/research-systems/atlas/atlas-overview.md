# Atlas — Agent Loop Architecture

## Goal

Build a system that increases in capability and efficiency over time, empowering agents to take on increasingly difficult missions. The system should get better at research — not just accumulate knowledge about a domain, but learn how to investigate, what approaches work, how to frame problems, and when to change direction.

The architecture is domain-agnostic. Missions have included quantum gravity, nature of time, Yang-Mills, and the Riemann Hypothesis.

## How to Launch

### Fresh Run (no existing strategy)

1. **Create the instance directory** (if it doesn't exist):
   ```bash
   INSTANCE="instances/<mission-name>"
   mkdir -p "$INSTANCE/strategies" "$INSTANCE/library-inbox" "$INSTANCE/meta-inbox"
   ```

2. **Write MISSION.md and MISSION-VALIDATION-GUIDE.md** in the instance directory.

3. **Start a missionary tmux session:**
   ```bash
   tmux new-session -d -s missionary-<tag> -c /Users/seanross/kingdom_of_god/home-base/research_hub/big-thinkers/research-systems/atlas/execution/instances/<mission-name>
   ```

4. **Start Claude as the missionary:**
   ```bash
   tmux send-keys -t missionary-<tag> "claude --system-prompt-file /Users/seanross/kingdom_of_god/home-base/research_hub/big-thinkers/research-systems/atlas/execution/agents/missionary/system-prompt.md --permission-mode bypassPermissions" Enter
   ```

5. **Wait ~12 seconds for Claude to start, then send the launch prompt:**
   ```bash
   tmux send-keys -t missionary-<tag> "This is a fresh run. No prior strategies exist. Read MISSION.md and MISSION-VALIDATION-GUIDE.md. Read the missionary meta library at ../../agents/library/meta/missionary/INDEX.md for lessons from previous missions. Write STRATEGY.md in strategies/strategy-001/ (create the directory). Then read ../../SETUP-GUIDE.md and follow it to set up infrastructure. Then launch the strategizer in a tmux session called 'strategizer-<tag>'. The strategizer system prompt is at ../../agents/strategizer/system-prompt.md. Go." Enter
   ```

6. **(Optional) Start the babysitter cron** in the parent Claude session if you want monitoring. See the Babysitter section below.

7. **The system then runs autonomously:**
   - Missionary writes strategy, sets up infrastructure, launches strategizer + operator
   - Strategizer queries the librarian, designs explorations, writes GOAL.md files
   - Operator detects GOAL.md → launches explorer in tmux
   - Explorers research, compute, and write reports
   - Operator detects REPORT-SUMMARY.md → kills explorer, nudges strategizer
   - Strategizer processes results, writes next GOAL.md
   - Curator processes reports into the library after each exploration
   - After up to 20 explorations (or fewer if the strategizer cuts short), strategizer writes final report
   - Operator detects FINAL-REPORT.md → notifies missionary
   - Missionary evaluates results, writes missionary meta-learning, and decides whether to create strategy-002

### What Happens During a Run

The **Operator** (`execution/operator/operator.sh`) is a pure bash script that handles all tmux operations — launching explorers, detecting completion, nudging the strategizer, and notifying the missionary. This separation exists because the strategizer's token cost grows with every bash command (full context re-sent each time). The operator does the plumbing for zero tokens.

Each exploration cycle:
1. Strategizer decides what to explore next (reads history, reasoning, COMPUTATIONS-FOR-LATER.md)
2. Strategizer spawns a **librarian** (foreground sub-agent) to search the factual library, meta library, and meta-inbox for relevant context
3. Strategizer chooses explorer type (standard or math) and writes GOAL.md with the exploration goal + librarian findings
4. Strategizer stops and waits — the **Operator** detects the new GOAL.md and launches the explorer in a tmux session
5. Explorer researches/computes, writes REPORT.md incrementally, writes REPORT-SUMMARY.md last (completion signal)
6. **Operator** detects REPORT-SUMMARY.md, kills the explorer session, nudges the strategizer
7. Strategizer processes results
8. Strategizer updates COMPUTATIONS-FOR-LATER.md with any flagged computations
9. Strategizer launches **curator** (fire-and-forget sub-agent) to process the report into the library
10. Strategizer writes meta-learning note, reflects, writes next GOAL.md, and the cycle repeats

When the strategy completes:
1. Strategizer writes FINAL-REPORT.md with a **Novel Claims** section (claim, evidence, novelty search, counterargument, status)
2. Strategizer sets `done: true` in state.json
3. **Operator** detects FINAL-REPORT.md and sends handoff message to the missionary
4. Missionary reads the final report, reasoning log, report summaries, and meta-inbox
5. Missionary evaluates both the science AND the methodology
6. Missionary writes a **missionary meta-learning note** to `../../agents/library/meta/missionary/`
7. Missionary decides: mission complete → write MISSION-COMPLETE.md, or more work needed → write next STRATEGY.md

When a mission completes:
1. Kill all tmux sessions for the mission: `tmux kill-session -t <prefix>-missionary; tmux kill-session -t <prefix>-strategizer; tmux kill-session -t <prefix>-curator`

### How to Monitor

- `tmux ls` — see all active sessions (\<prefix>-missionary, \<prefix>-strategizer, \<prefix>-explorer-NNN, \<prefix>-curator)
- `tmux capture-pane -t strategizer-<tag> -p | tail -20` — see strategizer activity
- `tmux capture-pane -t explorer-NNN -p | tail -20` — see explorer activity
- `cat instances/<mission>/strategies/strategy-NNN/state.json` — check current state
- `cat instances/<mission>/strategies/strategy-NNN/HISTORY-OF-REPORT-SUMMARIES.md` — see exploration summaries
- `cat instances/<mission>/strategies/strategy-NNN/REASONING.md` — see strategizer's reasoning + librarian query logs
- `cat agents/library/curator-log.md` — see what curator added/skipped
- `cat agents/library/librarian-log.md` — see librarian search paths and results
- `cat execution/babysitter/status.json` — current session statuses (babysitter)
- `tail execution/babysitter/logs/summary.md` — recent babysitter actions

### How to Stop

- **Kill sessions:** `tmux kill-session -t strategizer-<tag>; tmux kill-session -t missionary-<tag>`
- **Kill everything:** `tmux kill-server`

### Cleaning Up for a Fresh Restart

1. Kill tmux sessions: `tmux kill-session -t strategizer-<tag>; tmux kill-session -t missionary-<tag>; tmux kill-session -t curator 2>/dev/null`
2. Delete strategy directory: `rm -rf instances/<mission>/strategies/strategy-001`
3. Clear inboxes: `rm -f instances/<mission>/library-inbox/*` and `rm -f instances/<mission>/meta-inbox/*`
4. MISSION.md and MISSION-VALIDATION-GUIDE.md are kept — they don't change between runs

## How It Works

A hierarchical agent system for tackling complex, open-ended research problems. Three levels — Missionary, Strategizer, and Explorer — plus support agents (Curator, Librarian).

### The Outer Loop (Missionary)

1. The **Missionary** reads the mission, the meta library (lessons from past missionaries), and writes a STRATEGY.md — a methodology for the Strategizer to follow.
2. The **Strategizer** runs up to 10 explorations within that strategy (can cut short or extend phases at its discretion).
3. When complete, the Strategizer writes a FINAL-REPORT.md (including Novel Claims) and hands off to the Missionary via tmux.
4. The Missionary evaluates results against the mission validation guide — both the science and the methodology.
5. The Missionary writes a **missionary meta-learning note** for future missionaries.
6. If more work is needed, the cycle repeats with a new strategy informed by what was learned.

### The Inner Loop (Strategizer)

1. The Strategizer queries the **Librarian** for relevant context from the factual library, meta library, and meta-inbox.
2. It checks **COMPUTATIONS-FOR-LATER.md** for high-value computations flagged by previous explorers.
3. It designs an exploration goal (GOAL.md) using librarian findings + its own history.
4. It chooses an explorer type: **standard** (literature/synthesis) or **math** (computation/formalization).
5. It launches one or more **Explorers** in tmux sessions and waits via file-watch (can run parallel explorers for independent goals).
6. The Explorer researches/computes, writes REPORT.md and REPORT-SUMMARY.md (including unexpected findings and identified computations).
7. The Strategizer processes results, updates COMPUTATIONS-FOR-LATER.md, launches the **Curator** to update the library, writes meta-learning notes.
8. Repeat for up to 10 explorations.

### Knowledge Accumulation

Knowledge flows five ways:
- **Downward**: goals, success criteria, strategy, librarian-curated context
- **Upward**: reports with findings, outcomes, leads, unexpected discoveries, and novel claims
- **Lateral (via factual library)**: accumulated domain knowledge accessible to any agent via the librarian
- **Meta (via meta library)**: curated operational lessons organized by topic (goal-design, methodology, system-behavior, missionary). Written by strategizers and missionaries, surfaced by the librarian.
- **Computations (via COMPUTATIONS-FOR-LATER.md)**: identified computations that would advance the mission but couldn't be completed in a single exploration. Persists across strategies at the instance level.

## File Structure

```
atlas/
  CLAUDE.md                            ← points new agents to this overview
  execution/
    agents/
      missionary/system-prompt.md
      strategizer/
        system-prompt.md
        templates/                     ← state.json, HISTORY-OF-REPORT-SUMMARIES.md, REASONING.md
      explorer/system-prompt.md        ← standard explorer (literature, synthesis, analysis)
      math-explorer/system-prompt.md   ← math explorer (computation, Lean 4, counterexamples)
      library/
        factual/                       ← domain knowledge entries with INDEX.md hierarchy
        meta/                          ← operational lessons, organized by topic
          INDEX.md
          goal-design/                 ← how to write good exploration goals
          methodology/                 ← what strategy structures and approaches work
          system-behavior/             ← how explorers actually behave (stalling, limits, modes)
          missionary/                  ← strategy-design lessons from past missionaries
        curator/system-prompt.md
        curator-log.md                 ← curator's record of what it added/skipped/updated
        receptionist/system-prompt.md  ← librarian agent, queried by strategizer before each exploration
        librarian-log.md               ← librarian's record of searches and results
      scribe/system-prompt.md          ← on standby
    babysitter/
      system-prompt.md
      status.json
      logs/
        checks.jsonl
        summary.md
    instances/
      <mission-name>/
        MISSION.md
        MISSION-VALIDATION-GUIDE.md
        MISSION-COMPLETE.md            ← written by missionary when mission is done
        COMPUTATIONS-FOR-LATER.md      ← computations flagged by explorers, maintained by strategizer
        library-inbox/                 ← reports waiting for curator processing
        meta-inbox/                    ← meta-learning notes from strategizer
        strategies/
          strategy-NNN/
            STRATEGY.md
            FINAL-REPORT.md            ← written when strategy completes (includes Novel Claims)
            state.json
            HISTORY-OF-REPORT-SUMMARIES.md
            REASONING.md               ← includes librarian query/response logs
            explorations/
              exploration-NNN/
                GOAL.md
                REPORT.md
                REPORT-SUMMARY.md
                code/                  ← math explorer only: reproducible scripts and Lean files
    validation/
    SETUP-GUIDE.md
    atlas-overview.md                  ← this file
    test-run-notes.md
  organization/
    visuals/
    briefing/
```

## Agents

### Missionary (Top Level)

Sets the overall mission direction. On startup, reads the mission, validation guide, and the **missionary meta library** (`meta/missionary/INDEX.md`) for lessons from past missionaries. Writes STRATEGY.md — a methodology and protocol — and spawns a setup agent to create infrastructure.

When a strategy completes: reads the final report, reasoning log, report summaries, and meta-inbox. Evaluates both the science and the methodology. Writes a **missionary meta-learning note** to the meta library. Reviews **Novel Claims** across all strategies. Decides whether to create the next strategy or declare the mission complete (writing MISSION-COMPLETE.md with consolidated novel claims).

### Strategizer (Middle Level)

Owns a single strategy. Runs autonomously via event-driven file-watch. Has **pacing autonomy** — the missionary's phase budgets are suggestions, not fixed allocations. Can cut phases short or extend them based on evidence.

On first startup, reads **prior strategy FINAL-REPORTs** for unfiltered cross-strategy knowledge. For each exploration: queries the librarian for context, checks COMPUTATIONS-FOR-LATER.md, designs the goal, chooses explorer type (standard or math), launches an explorer in tmux (waits via file-watch at zero token cost, babysitter handles error cases), processes results (including unexpected findings and identified computations), updates COMPUTATIONS-FOR-LATER.md, launches the curator, writes meta-learning notes.

Can run **parallel explorers** for independent goals — concept sprints (competing approaches), independent domains, or construction + research pairs. Processes results one at a time to avoid curator conflicts.

Runs up to 10 explorations then writes FINAL-REPORT.md with a **Novel Claims** section and hands off to the missionary.

**Directions vs. Strategy:** The strategy is the methodology (how to explore). Directions are specific lines of investigation (what to explore). The strategizer tries multiple directions within one strategy. A direction failing is a pivot, not completion. Must try at least 3 substantially different directions.

### Explorer (Bottom Level)

Executes a single investigation in its own tmux session. Receives a goal with everything it needs (including librarian-curated context). Produces REPORT.md (detailed) and REPORT-SUMMARY.md (concise). Writes incrementally to disk — the Strategizer monitors REPORT.md line count for progress. REPORT-SUMMARY.md being written signals completion.

**Computation capability:** Explorers have full shell access and are instructed to write and execute code (Python, scipy, numpy, sympy, mpmath) rather than reasoning about what results "should" be. Individual bash commands time out at 10 minutes — heavy computations must be broken into stages with intermediate results saved to disk.

**Report extras:** REPORT-SUMMARY.md includes two additional sections:
- **Unexpected findings** — discoveries outside the goal's scope (cross-domain connections, contradicted assumptions, etc.)
- **Computations identified** — calculations that would advance the investigation but couldn't be completed in one exploration (tracked in COMPUTATIONS-FOR-LATER.md)

Two explorer variants exist — the Strategizer chooses which to use based on the goal:

| Standard Explorer | Math Explorer |
|---|---|
| Literature surveys, conceptual synthesis, theory analysis | Computation, formal verification, counterexample search |
| Primary output is prose | Primary output is code and verified claims |
| `agents/explorer/system-prompt.md` | `agents/math-explorer/system-prompt.md` |

The **Math Explorer** produces a `code/` directory alongside REPORT.md with reproducible scripts and Lean files. Tags every claim with verification status: `[VERIFIED]` (Lean proof compiles), `[COMPUTED]` (code ran), `[CHECKED]` (cross-verified), or `[CONJECTURED]` (reasoning only). Uses Python/SageMath/SymPy for computation and Lean 4 + Mathlib for formalization.

### Librarian / Receptionist (Support)

Queried by the strategizer as a foreground sub-agent before each exploration. Searches the factual library (via INDEX.md hierarchy), the meta library (operational lessons), and the meta-inbox (uncurated recent notes). Returns relevant findings and context. Logs all searches to `librarian-log.md`.

### Library Curator (Support)

Launched in tmux (fire-and-forget) after each exploration. Processes the explorer's report from library-inbox into the factual library AND the meta-learning note from meta-inbox into the meta library. Checks for duplicates, conflicts, and existing coverage before adding. Updates all INDEX.md files including the root. Logs everything to `curator-log.md`. Deletes processed reports from inbox.

## Orchestration

### Event-Driven File-Watch

The strategizer waits for explorer completion via a background file-watch:
```bash
while [ ! -f REPORT-SUMMARY.md ]; do sleep 30; done
```
Run with `run_in_background=true`, this costs zero tokens while waiting. When the explorer writes REPORT-SUMMARY.md, the strategizer wakes up automatically and processes results. The babysitter handles error cases (stuck explorers, zombie sessions).

## Babysitter

A lightweight monitoring system that watches over running Atlas sessions.

### How It Works

- A **cron heartbeat** fires every 5 minutes.
- The heartbeat runs a quick bash check (file timestamps, tmux pane errors, zombie detection) — costs **0 tokens if everything is healthy**.
- If something's wrong, spawns a **haiku sub-agent** that classifies sessions, nudges stuck agents, and escalates if needed.

### Escalation Ladder

1. **IDLE** — session exists but no recent activity
2. **SUSPICIOUS** — no progress for multiple checks
3. **NUDGE** — send-keys to the tmux session to prompt the agent
4. **CTRL-C + NUDGE** — kill the current command and re-prompt
5. **ALERT** — notify the operator (log + status file)

### Scope

- Monitors explorers and strategizers.
- **Skips** curators and missionaries (curators are fire-and-forget; missionaries wait legitimately).
- **Zombie detection:** sessions at 0% with no thinking indicator for >3 minutes are flagged.
- All missions discovered dynamically via glob — no hardcoded paths.

### Setup

The babysitter cron is **session-only** — it dies when the parent Claude session exits. Must be set up each session if you want monitoring. To start it, ask Claude in the parent session to:

> Create a cron that fires every 5 minutes. It should run the babysitter heartbeat bash check from `execution/babysitter/system-prompt.md` — the heartbeat script checks all active missions dynamically (file timestamps, tmux pane errors, zombie detection). If healthy (STALE=0 NEW_DONE=0), do nothing. If something needs attention, spawn a haiku babysitter subagent with the full system prompt. The heartbeat script and escalation logic are in `execution/babysitter/system-prompt.md`.

Or simply: "Start the babysitter cron for Atlas monitoring."

### Config

- `execution/babysitter/system-prompt.md` — babysitter agent prompt
- `execution/babysitter/status.json` — current session statuses
- `execution/babysitter/logs/checks.jsonl` — raw check results
- `execution/babysitter/logs/summary.md` — human-readable recent actions

## Known Issues & Concerns

### Zombie Sessions
Explorers can accept a prompt but never start processing — stuck at 0% with no thinking indicator. The babysitter's zombie detection catches this (sessions at 0% for >3 minutes), but manual intervention (Ctrl-C + re-send) may be needed if the babysitter isn't running.

### Explorer Getting Stuck
If an explorer gets stuck or hangs, the strategizer can detect it via tmux monitoring (REPORT.md line count stalls). The strategizer will nudge after 5 minutes of no progress, then kill and move on after 10 more minutes. Partial results on disk survive.

### Bash Timeout Constraint
Individual bash commands in Claude Code time out at 10 minutes (600,000ms). Explorers doing heavy computation (large parameter sweeps, high-precision calculations, many iterations) must break work into stages. The explorer system prompt warns about this, but explorers that attempt a single monolithic computation will hit the wall and have to retry.

### Curator is Fire-and-Forget
The curator runs in tmux and the strategizer doesn't wait for it. If the curator fails silently, reports may not make it into the library. No verification step exists. Monitor via `curator-log.md`.

## Things to Evaluate

### Librarian Query Quality
The strategizer queries the librarian before each exploration with a description of what it's about to explore. **Key concern:** Does the strategizer give the librarian enough context — both what it's trying to do next AND what types of data it would need? A vague query produces irrelevant results; a narrow query misses important related findings. Monitor this by reading:
- `REASONING.md` — the strategizer logs what it queried and what came back
- `librarian-log.md` — the librarian logs its full search path, what it found, and what it skipped
If the librarian is returning poor results, the fix could be in the strategizer (better queries), the librarian (better search), or the library structure (better organization/indexes).

### Curator Index Consistency
The curator is supposed to update ALL INDEX.md files from root to leaf when adding new entries. In early runs, it missed the root INDEX.md — new folders existed but weren't listed at the top level. The prompt has been strengthened but this needs monitoring via `curator-log.md`.

### Meta-Learning Loop
Meta-learning flows through two channels: strategizer notes (about goal design, explorer behavior) and missionary notes (about strategy design, methodology choices). **Evaluate:** Are the lessons actually useful? Are they being surfaced when relevant? Is the meta library growing with genuinely new insights or filling with generic observations?

### Missionary Handoff
The strategizer hands off to the missionary via tmux message when the strategy completes. **Evaluate:** Does the missionary make good use of the final report? Does it create meaningfully different strategies, or does it repeat similar approaches? Does reading prior FINAL-REPORTs help the strategizer avoid repeating failed directions?

### Novel Claims Quality
FINAL-REPORTs now include a Novel Claims section. **Evaluate:** Are claims actually novel (not just restated known results)? Are novelty searches thorough? Are counterarguments addressed rather than hand-waved? Does the missionary's consolidated claims section in MISSION-COMPLETE.md accurately represent the strongest findings?

### COMPUTATIONS-FOR-LATER Utilization
Explorers flag computations, strategizers collect them. **Evaluate:** Does the strategizer actually consult this file when planning? Do flagged computations ever become exploration goals? Or is it write-only?

### Idea Creation
Strategizers and missionaries are instructed to spawn background sub-agents to score and log promising ideas to `../idea-exploration/ATLAS-IDEAS.md`. **Track:** How many ideas are being generated per mission? Are they high quality or noise? Are the validator scores calibrated (do "Run" ideas actually make good missions)? If missions are producing zero ideas, the instruction may need reinforcing or the agents may not be encountering cross-domain leads.

### Idea Validator Token Cost
Each idea validation spawns a background sub-agent that does 10-15 minutes of research. **Track:** How many tokens does each validation consume? If strategizers are spawning many validators per mission, the overhead could add up. Monitor whether the token cost is justified by the quality of ideas surfaced.

## Open Questions

1. **Missionary oversight of strategizer** — Currently the missionary sits idle for hours until the strategizer finishes all explorations. Mid-strategy visibility would let the missionary abort a clearly failing strategy early (via an ABORT.md file) instead of waiting for all 10 explorations. The hard part: how to wake the missionary up. Options considered: strategizer sends periodic checkpoint messages (adds complexity), missionary polls state.json (Claude instances don't naturally poll), manual/babysitter trigger (defeats autonomy). The strategizer now has pacing autonomy (can cut phases short), which addresses the biggest waste. Missionary oversight is a "nice to have" if a clean wakeup mechanism emerges.

2. **HISTORY-OF-REPORT-SUMMARIES.md compaction** — As explorations accumulate, this file grows. May need summarization when it gets too long, especially across context resets. What's the right compaction strategy — drop old summaries, merge them, or create a two-level summary?

3. **Should the strategizer compact between explorations?** — The previous design mandated `/compact` before processing each result, to prevent context (and token cost) from growing with every exploration. This was removed because it's unclear whether the cost savings outweigh the loss of in-context reasoning history. Arguments for compacting: context stays ~30-50K, each exploration costs roughly the same, a strategizer that doesn't compact may burn through its budget by exploration 5. Arguments against: the strategizer loses nuance from earlier explorations that files don't fully capture, compaction may discard reasoning threads that would inform later pivots, and the 1M context window may be large enough to make this unnecessary. Needs data from a run without mandatory compaction to compare token usage and decision quality.

## Things to Review

1. **Agent token consumption** — Profile the token counts for each agent type (missionary, strategizer, explorer, curator, librarian) across a full mission. Which agents consume the most tokens? Are any agents burning context on boilerplate rather than research? This data should inform prompt compression and context management.

2. **Strategizer explorer count freedom** — Currently strategizers run up to 10 explorations per strategy. Review whether this cap is right, and whether strategizers should have full freedom to decide how many explorations to run based on the problem. Some strategies may only need 3; others may need 15. The current fixed cap may force premature wrap-up or unnecessary padding.

## Future Expansions

1. **Parallel strategies** — The Missionary could run multiple strategies simultaneously. Not yet tested.

2. **Recursion** — The architecture could be made fractal — an explorer could itself spawn sub-explorers for complex sub-problems. Not yet implemented.

3. **Validation agent** — A dedicated agent for systematic theory checking against the mission validation tiers. Currently validation is embedded ad-hoc in exploration goals.

4. **Replication explorations** — Dedicated explorations that independently verify a previous exploration's key claims: re-read cited papers, check numbers, confirm reasoning. Especially important when the system claims novelty. One per strategy would catch errors before they propagate.

5. **Claim hardening workflow** — Separate "discovery" explorations (go wide, find candidates) from "hardening" explorations (take one claim, verify citations, search for prior art, compute numbers, run adversarial attack, produce a verification packet). Optimizes for producing defensible novel claims rather than broad theories.

6. **Philosopher chain** — Instead of open-ended exploration, start by creating the logical chain needed to establish a claim. Then adversarially attack and refine that chain. Then detail out the requirements to solidify each step. Catches dead ends early (Compton-Unruh ran 8 explorations when dimensional analysis killed it in exploration-001). Best for hardening claims that already exist — compose with standard Atlas (discover first, then chain-harden). See `instances/classicality-budget/PROOF-CHAINS.md` for an example applied to a completed mission. Implementation: a new philosopher agent that reads a claim (from MISSION-COMPLETE.md or promising-findings.md), maps the full dependency chain, identifies the weakest link, and designs the follow-up explorations needed to close each gap.

7. **Idea creator + idea validator** — Two complementary systems. The **idea creator** generates candidate missions it thinks are well-suited to Atlas — problems where the agent loop's strengths (literature synthesis, computational verification, adversarial self-review, multi-strategy iteration) give a real advantage. Draws from Atlas outputs, the research radar, cross-mission connections, and open problems in the field. The **idea validator** takes those candidates and scores their likelihood of producing breakthrough results — not just "is this tractable" but "if Atlas runs this, what are the odds it finds something genuinely new?" Considers the state of the field, whether the key gaps are computational vs. conceptual, how crowded the area is, and whether Atlas has relevant prior work to build on. The philosopher chain (#6) is the next step — once an idea passes validation, the philosopher builds the attack plan.

8. **Automated idea pipeline** — Currently the idea creator and validator are guide docs used in interactive sessions with a human in the loop. Automate them as standalone agents that can run end-to-end: idea creator generates candidates, validator scores them, high-ranked ideas feed into the philosopher chain, and top philosopher outputs become Atlas missions. The full pipeline — research radar → idea creator → validator → philosopher → Atlas mission — could run autonomously, with the human reviewing a ranked queue of ready-to-launch missions rather than driving each step.

9. **Research radar** — An agent that scans for new findings in science (arXiv, journals, preprints) that Atlas could build off of. Monitors fields relevant to completed and planned missions for developments that change the landscape — new theorems that close gaps in our proof chains, new experimental results that confirm or kill our predictions, new frameworks that open mission opportunities. Feeds discoveries into the library and flags high-priority items for follow-up missions. Turns Atlas from reactive (we pick topics) to proactive (the field's movement tells us where to look next).

10. **Explorer plan detection** — We need to be able to identify when an explorer would work better when given a plan first, and what kind of plan. We should bake into Atlas a way to learn this over time. Perhaps a verifier agent or some form of validation can run when applicable.

11. **Plan-then-execute explorer split** — Every explorer writes a plan first (what to compute, what checks to run, what would falsify the hypothesis), then a fresh agent executes the plan without seeing the goal directly. Separates "what to do" from "doing it" — the planner can't skip checks by getting excited about results, and the executor can't drift from the plan. Test this against the current single-agent explorer using the clean-room cases. Key question: does the plan transfer cleanly across agents, or does the executor lose context? See also condition D in `organization/ideas-for-explorer-prompt-changes.md`.

12. **Explorer prompt/architecture clean-room testing** — We have specific exploration instances where we now know the right answer (both correct and incorrect results). Use these as test cases to evaluate different explorer configurations: open-ended vs. prescriptive goals, library guard-rails injected into prompts, self-review vs. fresh adversarial review, plan-then-execute splits, etc. Detailed test plan and candidate cases documented in `organization/ideas-for-explorer-prompt-changes.md`. Results should feed back into the explorer system prompt and strategizer goal-writing guidance.

13. **Ephemeral strategizer with STRATEGIZER-STATE.md** — Instead of keeping the strategizer alive across all explorations (accumulating context and cost), spin up a fresh agent for each exploration cycle. The strategizer writes a `STRATEGIZER-STATE.md` brain dump at the end of each cycle: current thinking, hunches, rejected options, why it made each decision, what it would explore next and why. The next invocation reads this file along with HISTORY, REASONING, and state.json to reconstruct the full picture. Benefits: fixed predictable cost per cycle, no context growth, trivial crash recovery (indistinguishable from normal startup), no accumulated framing bias from early explorations coloring later decisions. Risk: dark knowledge loss — reasoning nuance that the strategizer doesn't articulate in the brain dump. Testable: replay a completed strategy with ephemeral agents and compare decision quality against the persistent run.

14. **Remote compute for heavy workloads** — Math explorers run DNS, parameter sweeps, and other compute-heavy jobs on the local machine, which ties up the laptop for hours (N=128 DNS took 110+ minutes on an M-series MacBook). Give explorers a "remote compute" tool that ships code to a cloud instance (Modal, EC2, GCP) with more cores or GPU acceleration, runs it, and pulls results back. GPU-accelerated FFTs (cupy) on an A100 would cut DNS from hours to minutes. The tool should be transparent — the explorer writes normal Python, the tool handles packaging, uploading, executing, and retrieving results. Key design question: does the explorer decide when to use remote compute, or does the operator/strategizer make that call based on estimated runtime?

## Future Missions

See `../idea-exploration/ATLAS-IDEAS.md` for candidate missions and their validator scores.
