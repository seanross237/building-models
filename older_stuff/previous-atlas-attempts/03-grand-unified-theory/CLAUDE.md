# Grand Unified Theory Research Project

This is an autonomous research system pursuing a grand unified theory of physics.

## Quick Start

The research loop runs in a tmux session. To check on it:
```bash
tmux attach -t theory-builder
```

## Key Files

- `GRAND-THEORY.md` — The living knowledge document (source of truth)
- `scripts/theory-builder/PROMPT.md` — Research protocol
- `scripts/theory-builder/HANDOFF.md` — Context between iterations
- `scripts/theory-builder/state.json` — Structured state
- `scripts/theory-builder/CALCULATIONS.md` — Detailed calculation records
- `scripts/theory-builder/LOOP-STATE.md` — Loop control (active/iteration/max)

## How It Works

Three-phase cycle:
- **Phase A: Theorize** — Survey knowledge, generate candidate theories, pick the most promising
- **Phase B: Investigate** — Do the math with adversarial agents (Calculator, Checker, Skeptic)
- **Phase C: Verdict** — Did it work? Update GRAND-THEORY.md, choose next direction

The stop hook auto-continues between iterations.

## To Stop

Create a pause file:
```bash
touch scripts/theory-builder/PAUSE_HOOK
```

## To Resume

Remove the pause file:
```bash
rm scripts/theory-builder/PAUSE_HOOK
```
