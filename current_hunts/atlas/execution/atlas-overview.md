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
   tmux new-session -d -s missionary-<tag> -c /Users/seanross/kingdom_of_god/building_models/current_hunts/atlas/execution/instances/<mission-name>
   ```

4. **Start Claude as the missionary:**
   ```bash
   tmux send-keys -t missionary-<tag> "claude --system-prompt-file /Users/seanross/kingdom_of_god/building_models/current_hunts/atlas/execution/agents/missionary/system-prompt.md --permission-mode bypassPermissions" Enter
   ```

5. **Wait ~12 seconds for Claude to start, then send the launch prompt:**
   ```bash
   tmux send-keys -t missionary-<tag> "This is a fresh run. No prior strategies exist. Read MISSION.md and MISSION-VALIDATION-GUIDE.md. Read the missionary meta library at ../../agents/library/meta/missionary/INDEX.md for lessons from previous missions. Write STRATEGY.md in strategies/strategy-001/ (create the directory). Then read ../../SETUP-GUIDE.md and follow it to set up infrastructure. Then launch the strategizer in a tmux session called 'strategizer-<tag>'. The strategizer system prompt is at ../../agents/strategizer/system-prompt.md. Go." Enter
   ```

6. **Approve the settings permission prompt** — the missionary will need to edit `~/.claude/settings.json` to register the stop hook. Send "2" to the missionary tmux session when the prompt appears (this selects "Yes, and allow Claude to edit its own settings for this session").

7. **The system then runs autonomously:**
   - Missionary writes strategy, sets up infrastructure, launches strategizer
   - Strategizer queries the librarian, designs explorations, launches explorers in tmux
   - Explorers research, compute, and write reports
   - Curator processes reports into the library after each exploration
   - After 10 explorations (or fewer if the strategizer cuts short), strategizer writes final report and hands off to missionary
   - Missionary evaluates results, writes missionary meta-learning, and decides whether to create strategy-002

### What Happens During a Run

Each exploration cycle:
1. Strategizer decides what to explore next (reads history, reasoning, COMPUTATIONS-FOR-LATER.md)
2. Strategizer spawns a **librarian** (foreground sub-agent) to search the factual library, meta library, and meta-inbox for relevant context
3. Strategizer chooses explorer type (standard or math) and writes GOAL.md with the exploration goal + librarian findings
4. Strategizer launches an **explorer** in a tmux session, monitors it via polling (can run multiple in parallel)
5. Explorer researches/computes, writes REPORT.md incrementally, writes REPORT-SUMMARY.md last (completion signal)
6. Strategizer detects completion, reads results (including unexpected findings and identified computations)
7. Strategizer updates COMPUTATIONS-FOR-LATER.md with any flagged computations
8. Strategizer launches **curator** in tmux (fire-and-forget) to process the report into the library
9. Strategizer writes meta-learning note, reflects, and repeats

When the strategy completes:
1. Strategizer writes FINAL-REPORT.md with a **Novel Claims** section (claim, evidence, novelty search, counterargument, status)
2. Strategizer sets `done: true` in state.json (stop hook sees this and stops restarting)
3. Strategizer sends handoff message to the missionary via tmux
4. Missionary reads the final report, reasoning log, report summaries, and meta-inbox
5. Missionary evaluates both the science AND the methodology
6. Missionary writes a **missionary meta-learning note** to `../../agents/library/meta/missionary/`
7. Missionary decides: mission complete → write MISSION-COMPLETE.md, or more work needed → write next STRATEGY.md

### How to Monitor

- `tmux ls` — see all active sessions (\<prefix>-missionary, \<prefix>-strategizer, \<prefix>-explorer-NNN, \<prefix>-curator)
- `tmux capture-pane -t strategizer-<tag> -p | tail -20` — see strategizer activity
- `tmux capture-pane -t explorer-NNN -p | tail -20` — see explorer activity
- `cat instances/<mission>/strategies/strategy-NNN/state.json` — check current state
- `cat instances/<mission>/strategies/strategy-NNN/HISTORY-OF-REPORT-SUMMARIES.md` — see exploration summaries
- `cat instances/<mission>/strategies/strategy-NNN/REASONING.md` — see strategizer's reasoning + librarian query logs
- `cat agents/library/curator-log.md` — see what curator added/skipped
- `cat agents/library/librarian-log.md` — see librarian search paths and results
- `cat /tmp/strategizer-hook.log` — check stop hook activity

### How to Stop

- **Emergency stop:** `touch instances/<mission>/strategies/strategy-NNN/PAUSE_HOOK`
- **Kill sessions:** `tmux kill-session -t strategizer-<tag>; tmux kill-session -t missionary-<tag>`
- **Kill everything:** `tmux kill-server`

### Cleaning Up for a Fresh Restart

1. Kill tmux sessions: `tmux kill-session -t strategizer-<tag>; tmux kill-session -t missionary-<tag>; tmux kill-session -t curator 2>/dev/null`
2. Delete strategy directory: `rm -rf instances/<mission>/strategies/strategy-001`
3. Clear inboxes: `rm -f instances/<mission>/library-inbox/*` and `rm -f instances/<mission>/meta-inbox/*`
4. Remove stop hook from `~/.claude/settings.json` (the stale entry pointing to the deleted strategy)
5. MISSION.md and MISSION-VALIDATION-GUIDE.md are kept — they don't change between runs

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
5. It launches one or more **Explorers** in tmux sessions and monitors progress (can run parallel explorers for independent goals).
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
        strategizer-stop-hook.sh       ← template, copied into each strategy
        templates/                     ← state.json, LOOP-STATE.md, HISTORY-OF-REPORT-SUMMARIES.md, REASONING.md
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
            LOOP-STATE.md
            strategizer-stop-hook.sh
            explorations/
              exploration-NNN/
                GOAL.md
                REPORT.md
                REPORT-SUMMARY.md
                code/                  ← math explorer only: reproducible scripts and Lean files
    validation/
    SETUP-GUIDE.md
    LOOP-STOP-HOOK-GUIDE.md
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

Owns a single strategy. Runs autonomously in a stop hook loop. Has **pacing autonomy** — the missionary's phase budgets are suggestions, not fixed allocations. Can cut phases short or extend them based on evidence.

On first startup, reads **prior strategy FINAL-REPORTs** for unfiltered cross-strategy knowledge. For each exploration: queries the librarian for context, checks COMPUTATIONS-FOR-LATER.md, designs the goal, chooses explorer type (standard or math), launches an explorer in tmux (monitors progress, can nudge/timeout), processes results (including unexpected findings and identified computations), updates COMPUTATIONS-FOR-LATER.md, launches the curator, writes meta-learning notes.

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

The Strategizer loop is kept alive by a **stop hook** — a shell script registered in `~/.claude/settings.json`. When the strategizer's context runs out and Claude stops, the hook fires, checks if it's the right session (by matching the transcript path against the strategy directory name), and feeds a meta-prompt back in.

The hook checks, in order:
1. **PAUSE_HOOK file** — if present, let session die (emergency stop)
2. **state.json `done: true`** — if the strategy is complete, let session die (prevents crash-restart loop at end of strategy)
3. **LOOP-STATE.md exists** — if not, let session die (loop not active)
4. **Transcript path matching** — only catches the right session (prevents capturing explorers or curators running from the same directory)
5. **Max restarts safety cap** — prevents infinite loops
6. If all checks pass, increment iteration and output a JSON block that tells Claude to continue with a meta-prompt

See `LOOP-STOP-HOOK-GUIDE.md` for the full reference on how stop hooks work.

## Known Issues & Concerns

### Settings Permission Prompt
The missionary needs to edit `~/.claude/settings.json` to register the stop hook. Even with `--permission-mode bypassPermissions`, this triggers a manual approval prompt. **Workaround:** send "2" to the missionary tmux session when the prompt appears (this is a selection menu — send just the number, not Enter). **Future fix:** pre-register the hook before launching.

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

## Open Questions

1. **Parallel strategies** — The Missionary could run multiple strategies simultaneously. Not yet tested.

2. **Recursion** — The architecture could be made fractal. Not yet implemented.

3. **Validation agent** — A dedicated agent for systematic theory checking against the mission validation tiers. Currently validation is embedded ad-hoc in exploration goals.

4. **HISTORY-OF-REPORT-SUMMARIES.md compaction** — As explorations accumulate, this file grows. May need summarization when it gets too long, especially across context resets.

5. **Missionary oversight of strategizer** — Currently the missionary sits idle for hours until the strategizer finishes all explorations. Mid-strategy visibility would let the missionary abort a clearly failing strategy early (via an ABORT.md file) instead of waiting for all 10 explorations. The hard part: how to wake the missionary up. Options considered: strategizer sends periodic checkpoint messages (adds complexity), missionary polls state.json (Claude instances don't naturally poll), manual/babysitter trigger (defeats autonomy). The strategizer now has pacing autonomy (can cut phases short), which addresses the biggest waste. Missionary oversight is a "nice to have" if a clean wakeup mechanism emerges.

6. **Replication explorations** — Dedicated explorations that independently verify a previous exploration's key claims: re-read cited papers, check numbers, confirm reasoning. Especially important when the system claims novelty. One per strategy would catch errors before they propagate.

7. **Claim hardening workflow** — Separate "discovery" explorations (go wide, find candidates) from "hardening" explorations (take one claim, verify citations, search for prior art, compute numbers, run adversarial attack, produce a verification packet). Optimizes for producing defensible novel claims rather than broad theories.
