# Atlas

Atlas is a hierarchical agent loop system for tackling complex research problems. Read `execution/atlas-overview.md` for the full architecture, how to launch, and known issues. Keep that doc up to date as things change.

## Quick Reference

- **Overview & launch guide:** `execution/atlas-overview.md`
- **Current mission:** `execution/instances/quantum-gravity/MISSION.md`
- **Agent system prompts:** `execution/agents/`
- **Test run notes:** `execution/test-run-notes.md`

## After a Mission Completes

When an Atlas mission completes (missionary declares MISSION-COMPLETE.md), review the Novel Claims from the final reports. Any claims that survived adversarial review and passed Tier 5 validation should be added to `../../promising-findings.md`, following the format already in that file.

## Briefing

When Sean asks to "open the briefing", "run the briefing", "briefing", or similar:

1. Start the dev server in the background: `cd organization/briefing && npm run dev`
2. Wait a couple seconds for it to start
3. Open the browser: `open http://localhost:5173`

If port 5173 is taken, check the dev server output for the actual port and open that instead.
