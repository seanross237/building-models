# Atlas Test Run Notes

---

## Run 2 — 2026-03-24

### Context
Second test run. Fixes from run 1 applied: foreground agents, simplified stop hook (transcript path matching), cleaned explorer/strategizer prompts, 20-exploration limit.

### Launch Process
- Missionary tmux session created, Claude started with bypassPermissions, launch prompt sent after 15s delay.
- Missionary read mission, validation guide, templates. Created strategy-001 directory and wrote STRATEGY.md.
- Missionary hit settings.json permission prompt (as expected). Approved with option 2 ("allow for session").

### Monitoring Log

- ~12:00 — Missionary complete. Created strategy-001, set up infrastructure, registered stop hook, launched strategizer.
- ~12:02 — Strategizer starts. Designed exploration-001 (spectral dimension convergence). Spawned explorer (foreground).
- ~12:16 — Exploration-001 complete (87,751 tokens). Strategizer processed results, designed exploration-002.
- ~12:18 — Exploration-002 running (BH entropy & holographic constraints).
- ~12:30 — Internet dropped. Explorer-002 had completed (100,703 tokens) right before outage. Strategizer hit ConnectionRefused trying to read results. Stuck ~33 min.
- ~13:05 — Internet back. Nudged strategizer with message. Resumed cleanly, processed exploration-002.
- ~13:10 — Exploration-003 launched (experimental bounds & failure modes).
- ~13:18 — Exploration-003 complete (87,309 tokens). Phase 1 complete. Strategizer built constraint_map_summary.
- ~13:28 — Exploration-004 complete (69,227 tokens). First theory construction attempt. Partially succeeded.
- ~13:39 — Exploration-005 complete. AS ↔ IDG bridge.
- ~13:49 — Exploration-006 complete. BMEG theory constructed with 4 novel predictions.
- ~14:00 — Exploration-007 complete (482 lines). eta_h > 0 robust; conditionally passed.
- Run stopped at 7/20 explorations to restart with new tmux setup. Strategizer was at 12% context.

### Exploration Progress

| # | Direction | Outcome | Tokens | Key Finding |
|---|-----------|---------|--------|-------------|
| 001 | Spectral dimension convergence | succeeded | 87,751 | Propagator must scale as p^4+ in UV; ghost-free options: entire functions, running couplings, or Lorentz violation |
| 002 | Thermodynamic/entanglement/holographic | succeeded | 100,703 | d_s=2 selected by holographic principle; UV theory is 2D CFT with c=6/pi per Planck cell |
| 003 | Experimental bounds & failure modes | succeeded | 87,309 | Ghost-unitarity-causality-locality trilemma; Horava-Lifshitz eliminated; IDG and fakeon gravity survive |
| 004 | Entanglement-driven dimensional flow | partially succeeded | 69,227 | Self-consistency loop identified; UV theory is c=2 two free bosons; 2D→4D emergence gap is critical |
| 005 | AS ↔ IDG bridge | succeeded | ~? | AS and IDG are partially overlapping; bi-metric distinction |
| 006 | BMEG theory construction | succeeded | ~? | BMEG constructed; 4 novel predictions; passes constraint map |
| 007 | BMEG self-consistency | succeeded | ~? | eta_h > 0 robust; conditionally passed |

### Key Learnings
- **Permission prompt** is the only manual intervention needed. Sending "2" (allow for session) works.
- **Incremental writing still broken.** Explorer-001 wrote 8 lines early, then nothing for ~10 min, then 521 lines at the end. Same pattern across all explorations. Less critical with foreground agents but risky if explorer hits context limit mid-research.
- **Internet outage recovery works.** Strategizer got stuck on API error but recovered cleanly when nudged. No data lost — explorer had already written files to disk.
- **Context efficiency is excellent.** Strategizer was at only 12% after 7 full explorations + processing. Should easily handle 20.
- **Foreground agents work but can't be monitored/timed out.** Strategizer is blind while explorer runs.
- **Exploration pace:** roughly 8-10 min per exploration.
- **Meta-learning notes are being written.** 7 files in meta-inbox with real lessons.
- **Curator test:** Manually launched curator on exploration-007 report. It created a new bmeg/ folder in the library with 3 entries. Worked but no log written before we stopped it.

### System Changes Made During Run 2
- Implemented tmux-based explorer pattern in strategizer prompt
- Strengthened incremental writing in explorer prompt
- Added curator-in-tmux step to strategizer exploration cycle
- Updated curator prompt: duplicate checking, detailed logging, cleanup
- Updated meta-learning prompt: general lessons not sub-agent-specific
- Fixed library-inbox path
- Updated atlas-overview.md throughout

---

## Run 3 — 2026-03-24

### Context
Third test run. New features: tmux-based explorers (strategizer monitors/can nudge/timeout), curator runs in tmux after each exploration, strengthened incremental writing instructions, meta-learning updated to general lessons.

### Launch Process
- Missionary launched, hit permission prompt, approved with "2".
- Missionary complete ~14:15. Strategizer launched. Notes "spawning Explorer in its own tmux session" — new tmux pattern is working.
- Explorer-001 launched in its own tmux session at ~14:17.

### Monitoring Log

- ~14:17 — Explorer-001 launched in tmux. Strategizer polling with sleep 60/90.
- ~14:25 — Explorer-001 complete (625 lines). Strategizer detected completion, processed results, killed explorer session.
- ~14:25 — Curator launched in tmux (fire-and-forget). Reading library for overlap.
- ~14:27 — Explorer-002 launched in tmux. 4 sessions running in parallel (missionary, strategizer, curator, explorer-002).
- Strategizer at 6% context.

### Curator Observations
- First curator run in progress. Checking overlap against existing library entries.
- No log written yet (still processing).

### Issues Found
- Strategizer said "state.json was already updated (possibly by a previous process)" — minor confusion but recovered fine.
- Incremental writing improved: REPORT.md at 33 lines early (vs 8 in run 2), finished at 625.
