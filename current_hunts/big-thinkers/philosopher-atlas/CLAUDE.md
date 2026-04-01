# Philosopher Atlas

An alternative research architecture that replaces Atlas's Missionary with a **wide-funnel adversarial planning loop**. Fully independent from Atlas — own agents, own library, own babysitter.

## Quick Reference

- **Architecture guide:** `agents/philosopher/system-prompt.md`
- **Agent prompts:** `agents/` (explorer, math-explorer, strategizer, philosopher)
- **Library:** `library/` (independent — not shared with Atlas)
- **Babysitter:** `babysitter/system-prompt.md`
- **Active missions:** `missions/`
- **Idea pipeline:** `../idea-exploration/` (shared across all Big Thinkers)

## tmux Session Naming

All Philosopher Atlas sessions use the prefix `patlas-` to avoid collision with Atlas sessions:
- `patlas-strategizer-001`
- `patlas-explorer-001`
- `patlas-explorer-002`
- etc.

## How It Works (Wide Funnel)

```
Planner (generates 5 chains)
  → Selector (picks top 3)
  → 3× Attacker (parallel — one per chain)
  → 3× Judge (parallel — one per chain)
  → Final Decider (picks winner, incorporates elements from losers)
  → Strategizer executes Step 1
  → Results back to Planning Loop
  → Evaluate: replan / proceed / kill
  → Repeat until chain complete or killed
```

The wide funnel tests 3 chains adversarially instead of 1. This catches framing errors through cross-comparison, enables element transfer from losing chains, and produces better-designed negative findings. All planning loop agents run on Opus.

See `agents/philosopher/system-prompt.md` for full architecture documentation.
