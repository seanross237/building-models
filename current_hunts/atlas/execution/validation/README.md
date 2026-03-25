# Physics Validation Suite

A toolkit for autonomous research agents working on quantum gravity, unified theories, and related physics. Use it to catch obvious failures early and confirm your theory matches known reality.

## Philosophy

- This is a **TOOLKIT**, not a gate. Use what's helpful, skip what's not.
- Tests are organized by category and difficulty.
- Each test has a **Prerequisites** field — if your theory isn't ready for that test yet, skip it.
- **Partial passes are fine.** Note what passed and what's still open.
- The goal is to catch obvious failures early, not to block progress.

## Files

| File | Purpose | When to Use |
|------|---------|-------------|
| [QUICK-CHECK.md](QUICK-CHECK.md) | 5 yes/no questions, 2 minutes | Every time you propose a new theory or major revision |
| [EXPERIMENTAL-DATA.md](EXPERIMENTAL-DATA.md) | Curated experimental values and bounds | When checking if your predictions violate known data |
| [VALIDATION-TESTS.md](VALIDATION-TESTS.md) | Structured test suite, Tier 1-5 | Progressive validation as your theory matures |
| [AGENT-INSTRUCTIONS.md](AGENT-INSTRUCTIONS.md) | How to run tests and report results | First time using this suite, or when unsure about process |
| [DATA-SOURCES.md](DATA-SOURCES.md) | Real datasets you can download and analyze | When you want to test predictions against actual data (LIGO, Planck, etc.) |

## Quick Start

1. Read **QUICK-CHECK.md** and answer the 5 questions about your theory.
2. If you pass, move to **VALIDATION-TESTS.md** Tier 1.
3. Work through tiers as your theory matures. Skip tests whose prerequisites aren't met.
4. Reference **EXPERIMENTAL-DATA.md** whenever you need a specific measurement or bound.
5. When ready for quantitative comparison, consult **DATA-SOURCES.md** for real datasets to analyze.
6. Follow **AGENT-INSTRUCTIONS.md** for reporting format.

## Important Reminders

- A "SKIP" is not a failure. It means "not applicable yet."
- A Tier 1 failure is a signal to rethink foundations.
- A Tier 3 failure might just mean a parameter needs tuning.
- If every Tier 4 test is "SKIP" after many iterations, push yourself to make predictions.
- **Never let this suite slow you down.** It exists to accelerate your work by catching dead ends early.
