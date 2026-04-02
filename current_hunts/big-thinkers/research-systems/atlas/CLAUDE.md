# Atlas

Atlas is a hierarchical agent loop system for tackling complex research problems. Read `atlas-overview.md` for the full architecture, how to launch, and known issues. Keep that doc up to date as things change.

## Quick Reference

- **Overview & launch guide:** `atlas-overview.md`
- **Current missions:** `execution/instances/`
- **Agent system prompts:** `execution/agents/`
- **Test run notes:** `execution/test-run-notes.md`

## Briefing

When Sean asks to "open the briefing", "run the briefing", "briefing", or similar:

1. Start the dev server in the background: `cd organization/briefing && npm run dev`
2. Wait a couple seconds for it to start
3. Open the browser: `open http://localhost:5173`

If port 5173 is taken, check the dev server output for the actual port and open that instead.
