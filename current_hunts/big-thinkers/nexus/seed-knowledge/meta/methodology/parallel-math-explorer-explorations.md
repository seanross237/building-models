---
topic: Run independent explorations in parallel to save wall-clock time
category: methodology
date: 2026-03-28
source: "amplituhedron strategy-001 meta-exploration-006, thermal-time strategy-002 meta-exploration-001"
---

## Lesson

When two or more math explorer computations are logically independent (different physical models, different mathematical structures, no shared intermediate results), run them as **simultaneous parallel explorations** rather than sequentially. Each math explorer task takes ~20 min; parallel execution gives ~2× improvement in wall-clock time with no quality penalty.

## Evidence

- **amplituhedron strategy-001 explorations 005 and 006** — Both were math explorer computation tasks (005: hidden zeros computation; 006: EFT-hedron positivity bounds). They were independent: neither needed the other's results. Each completed in ~20 min when run in parallel. The meta note estimates ~50 min if run serially. Actual saving: ~30 min, or ~60% of elapsed time.

- **thermal-time strategy-002 explorations 001, 002, and 003** — Three Phase 1 verification/survey probes launched simultaneously. All were standard (non-math) explorations: E001 (Rindler lattice verification), E002 (non-equilibrium post-quench test), E003 (excited-state modular flow). All three were independent and completed successfully. This confirms that the parallel launch pattern applies to **standard explorations**, not just math explorers. The ideal pattern for Phase 1: launch all independent probes simultaneously.

## When Parallelism Works

Parallel execution is appropriate when:
1. **Independent inputs** — neither exploration reads the other's output files.
2. **No shared code/state** — each explorer builds its own computation environment.
3. **Different physical objects** — computing EFT bounds and hidden zeros use different mathematical machinery.

## When NOT to Parallelize

Do NOT parallelize when:
- One exploration builds the baseline the other will compare against (use `sequence-computation-approaches.md` instead).
- Both explorations write to the same output file or directory.
- One exploration is a repair/adversarial check on the other's result.
- The second exploration's goal depends on what the first finds (e.g., "if X succeeds, do Y with the result").

## Practical Guidance

- **Typical math explorer computation task**: ~15–25 min wall-clock. Two independent tasks: ~20 min parallel vs. ~45 min serial.
- **Check independence explicitly** before assigning parallel goals — "do these goals share any intermediate results?" If yes, sequence them.
- **Same explorer type requirement**: parallelize within the same explorer type (math+math, standard+standard). Mixing types (math+standard) can also work if independent.

## Relationship to Other Patterns

This is a **scheduling** lesson (when to dispatch tasks), not a task-design lesson. It complements:
- `staged-computation-goals.md` — Sequential pipeline when stages depend on each other; parallel launch when they don't.
- `one-task-per-exploration.md` (goal-design) — Keeping each task focused enables independence checks.
