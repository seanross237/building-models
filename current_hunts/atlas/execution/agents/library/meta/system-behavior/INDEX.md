# System Behavior — Meta Library

Lessons about how explorers actually behave: stalling patterns, reasoning limits, failure modes, and how to work with (not against) these behaviors.

## Entries

- **explorer-stalling-and-nudge-pattern.md** — Explorers consistently stall after initial output; nudges reliably break the stall. Monitor and nudge after 3-5 minutes of no progress.
- **computation-vs-reasoning-limits.md** — Explorers can evaluate formulas and reason about computation structure but cannot perform novel unpublished calculations.
- **explorer-crashes-and-path-confusion.md** — Explorers occasionally crash from context exhaustion and write to wrong paths; always verify output after completion.
- **synthesis-vs-research-mode.md** — Explicitly tell explorers "do NOT search, only synthesize" for construction tasks or they default to web searches.
