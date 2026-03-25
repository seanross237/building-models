# Atlas — Agent Loop Architecture

## Goal

Build a system that increases in capability and efficiency over time, empowering agents to take on increasingly difficult missions. The system should get better at research — not just accumulate knowledge about a domain, but learn how to investigate, what approaches work, how to frame problems, and when to change direction.

The first mission is quantum gravity. The architecture is domain-agnostic.

## How to Launch

### Fresh Run (no existing strategy)

1. **Start a missionary tmux session:**
   ```bash
   tmux new-session -d -s missionary -c /Users/seanross/kingdom_of_god/building_models/current_hunts/atlas/execution/instances/quantum-gravity
   ```

2. **Start Claude as the missionary:**
   ```bash
   tmux send-keys -t missionary "claude --system-prompt-file /Users/seanross/kingdom_of_god/building_models/current_hunts/atlas/execution/agents/missionary/system-prompt.md --permission-mode bypassPermissions" Enter
   ```

3. **Wait ~12 seconds for Claude to start, then send the launch prompt:**
   ```bash
   tmux send-keys -t missionary "This is a fresh run. No prior strategies exist. Read MISSION.md and MISSION-VALIDATION-GUIDE.md. Write STRATEGY.md in strategies/strategy-001/ (create the directory). Then read ../../SETUP-GUIDE.md and follow it to set up infrastructure. Then launch the strategizer in a tmux session called 'strategizer'. The strategizer system prompt is at ../../agents/strategizer/system-prompt.md. The strategizer should run 10 explorations total before writing its final report. Go." Enter
   ```

4. **Approve the settings permission prompt** — the missionary will need to edit `~/.claude/settings.json` to register the stop hook. Send "2" to the missionary tmux session when the prompt appears.

5. **The system then runs autonomously:**
   - Missionary writes strategy, sets up infrastructure, launches strategizer
   - Strategizer queries the librarian, designs explorations, launches explorers in tmux
   - Explorers research and write reports
   - Curator processes reports into the library after each exploration
   - After 10 explorations, strategizer writes final report and hands off to missionary
   - Missionary evaluates results and decides whether to create strategy-002

### What Happens During a Run

Each exploration cycle:
1. Strategizer decides what to explore next (reads history, reasoning)
2. Strategizer spawns a **librarian** (foreground sub-agent) to search the factual library and meta-inbox for relevant context
3. Strategizer writes GOAL.md with the exploration goal + librarian findings
4. Strategizer launches an **explorer** in a tmux session, monitors it via polling
5. Explorer researches, writes REPORT.md incrementally, writes REPORT-SUMMARY.md last (completion signal)
6. Strategizer detects completion, reads results, updates state and history
7. Strategizer launches **curator** in tmux (fire-and-forget) to process the report into the library
8. Strategizer writes meta-learning note, reflects, and repeats

### How to Monitor

- `tmux ls` — see all active sessions (missionary, strategizer, explorer-NNN, curator)
- `tmux capture-pane -t strategizer -p | tail -20` — see strategizer activity
- `tmux capture-pane -t explorer-NNN -p | tail -20` — see explorer activity
- `cat strategies/strategy-001/state.json` — check current state
- `cat strategies/strategy-001/HISTORY-OF-REPORT-SUMMARIES.md` — see exploration summaries
- `cat strategies/strategy-001/REASONING.md` — see strategizer's reasoning + librarian query logs
- `cat agents/library/curator-log.md` — see what curator added/skipped
- `cat agents/library/librarian-log.md` — see librarian search paths and results
- `cat /tmp/strategizer-hook.log` — check stop hook activity

### How to Stop

- **Emergency stop:** `touch strategies/strategy-001/PAUSE_HOOK`
- **Kill sessions:** `tmux kill-session -t strategizer; tmux kill-session -t missionary`
- **Kill everything:** `tmux kill-server`

### Cleaning Up for a Fresh Restart

1. Kill tmux sessions: `tmux kill-session -t strategizer; tmux kill-session -t missionary; tmux kill-session -t curator 2>/dev/null`
2. Delete strategy directory: `rm -rf execution/instances/quantum-gravity/strategies/strategy-001`
3. Clear inboxes: `rm -f execution/instances/quantum-gravity/library-inbox/*` and `rm -f execution/instances/quantum-gravity/meta-inbox/*`
4. Remove stop hook from `~/.claude/settings.json` (the stale entry pointing to the deleted strategy)
5. MISSION.md and MISSION-VALIDATION-GUIDE.md are kept — they don't change between runs

## How It Works

A hierarchical agent system for tackling complex, open-ended research problems. Three levels — Missionary, Strategizer, and Explorer — plus support agents (Curator, Librarian).

### The Outer Loop (Missionary)

1. The **Missionary** reads the mission and writes a STRATEGY.md — a methodology for the Strategizer to follow.
2. The **Strategizer** runs 10 explorations within that strategy.
3. When complete, the Strategizer writes a FINAL-REPORT.md and hands off to the Missionary via tmux.
4. The Missionary evaluates results against the mission validation guide, decides whether to create strategy-002.
5. If more work is needed, the cycle repeats with a new strategy informed by what was learned.

### The Inner Loop (Strategizer)

1. The Strategizer queries the **Librarian** for relevant context from the factual library and meta-inbox.
2. It designs an exploration goal (GOAL.md) using librarian findings + its own history.
3. It launches an **Explorer** in a tmux session and monitors progress.
4. The Explorer researches, writes REPORT.md and REPORT-SUMMARY.md.
5. The Strategizer processes results, launches the **Curator** to update the library, writes meta-learning notes.
6. Repeat for 10 explorations.

### Knowledge Accumulation

Knowledge flows four ways:
- **Downward**: goals, success criteria, strategy, librarian-curated context
- **Upward**: reports with findings, outcomes, and leads
- **Lateral (via library)**: accumulated domain knowledge accessible to any agent via the librarian
- **Meta (via meta-inbox)**: lessons about the exploration process itself, accessible to the librarian and missionary

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
      explorer/system-prompt.md
      library/
        factual/                       ← 95+ research entries with INDEX.md hierarchy
        curator/system-prompt.md
        curator-log.md                 ← curator's record of what it added/skipped/updated
        receptionist/system-prompt.md  ← librarian agent, queried by strategizer before each exploration
        librarian-log.md               ← librarian's record of searches and results
      scribe/system-prompt.md          ← on standby
    instances/
      quantum-gravity/
        MISSION.md
        MISSION-VALIDATION-GUIDE.md
        library-inbox/                 ← reports waiting for curator processing
        meta-inbox/                    ← meta-learning notes from strategizer
        strategies/
          strategy-001/
            STRATEGY.md
            FINAL-REPORT.md            ← written when strategy completes
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

Sets the overall mission direction. Writes STRATEGY.md — a methodology and protocol — and spawns a setup agent to create infrastructure. When a strategy completes, receives the final report, evaluates against the mission, and decides whether to create the next strategy. Stays alive in its tmux session throughout.

### Strategizer (Middle Level)

Owns a single strategy. Runs autonomously in a stop hook loop. For each exploration: queries the librarian for context, designs the goal, launches an explorer in tmux (monitors progress, can nudge/timeout), processes results, launches the curator, writes meta-learning notes. Runs 10 explorations then writes FINAL-REPORT.md and hands off to the missionary.

**Directions vs. Strategy:** The strategy is the methodology (how to explore). Directions are specific lines of investigation (what to explore). The strategizer tries multiple directions within one strategy. A direction failing is a pivot, not completion.

### Explorer (Bottom Level)

Executes a single investigation in its own tmux session. Receives a goal with everything it needs (including librarian-curated context). Produces REPORT.md (detailed) and REPORT-SUMMARY.md (concise). Writes incrementally to disk — the Strategizer monitors REPORT.md line count for progress. REPORT-SUMMARY.md being written signals completion.

### Librarian / Receptionist (Support)

Queried by the strategizer as a foreground sub-agent before each exploration. Searches both the factual library (via INDEX.md hierarchy) and the meta-inbox (lessons learned). Returns relevant findings and context. Logs all searches to `librarian-log.md`.

### Library Curator (Support)

Launched in tmux (fire-and-forget) after each exploration. Processes the explorer's report from library-inbox into the factual library. Checks for duplicates, conflicts, and existing coverage before adding. Updates all INDEX.md files including the root. Logs everything to `curator-log.md`. Deletes processed reports from inbox.

## Orchestration

The Strategizer loop is kept alive by a **stop hook** — a shell script registered in `~/.claude/settings.json`. When the strategizer's context runs out and Claude stops, the hook fires, checks if it's the right session (by matching the transcript path against the strategy directory name), and feeds a meta-prompt back in.

The hook is simple by design:
- **Transcript path matching** — only catches sessions started from the strategy directory
- **PAUSE_HOOK file** — emergency stop
- **Max restarts safety cap** — prevents infinite loops
- **No session claiming, no CWD filtering** — those were sources of bugs and have been removed

See `LOOP-STOP-HOOK-GUIDE.md` for the full reference on how stop hooks work.

## Known Issues & Concerns

### Settings Permission Prompt
The missionary needs to edit `~/.claude/settings.json` to register the stop hook. Even with `--permission-mode bypassPermissions`, this triggers a manual approval prompt. **Workaround:** manually approve when it appears (send "2" to the tmux session). **Future fix:** pre-register the hook before launching.

### Explorer Getting Stuck
If an explorer gets stuck or hangs, the strategizer can detect it via tmux monitoring (REPORT.md line count stalls). The strategizer will nudge after 5 minutes of no progress, then kill and move on after 10 more minutes. Partial results on disk survive.

### Stop Hook Not Yet Battle-Tested
The simplified stop hook (transcript path matching) has been tested in isolation but hasn't been through a real context reset yet. It should work — the logic is simple — but watch the first context reset carefully. Check `/tmp/strategizer-hook.log`.

## Things to Evaluate

### Librarian Query Quality
The strategizer queries the librarian before each exploration with a description of what it's about to explore. **Key concern:** Does the strategizer give the librarian enough context — both what it's trying to do next AND what types of data it would need? A vague query produces irrelevant results; a narrow query misses important related findings. Monitor this by reading:
- `REASONING.md` — the strategizer logs what it queried and what came back
- `librarian-log.md` — the librarian logs its full search path, what it found, and what it skipped
If the librarian is returning poor results, the fix could be in the strategizer (better queries), the librarian (better search), or the library structure (better organization/indexes).

### Curator Index Consistency
The curator is supposed to update ALL INDEX.md files from root to leaf when adding new entries. In run 2, it missed the root INDEX.md — new folders existed but weren't listed at the top level. The prompt has been strengthened but this needs monitoring via `curator-log.md`.

### Meta-Learning Loop
Meta-learning notes are written by the strategizer after each exploration and read by the librarian. **Evaluate:** Are the lessons actually useful? Are they being surfaced when relevant? Or are they too generic ("no issues this time") to add value?

### Missionary Handoff
The strategizer hands off to the missionary via tmux message when the strategy completes. **Evaluate:** Does the missionary make good use of the final report? Does it create meaningfully different strategy-002s, or does it repeat similar approaches?

## Open Questions

1. **Parallel strategies** — The Missionary could run multiple strategies simultaneously. Not yet tested.

2. **Parallel explorers** — Explorers run in tmux sessions, so the strategizer could run multiple in parallel. Not yet implemented but the infrastructure supports it.

3. **Recursion** — The architecture could be made fractal. Not yet implemented.

4. **Validation agent** — A dedicated agent for systematic theory checking against the mission validation tiers. Currently validation is embedded ad-hoc in exploration goals.

5. **HISTORY-OF-REPORT-SUMMARIES.md compaction** — As explorations accumulate, this file grows. May need summarization when it gets too long, especially across context resets.
