---
topic: Explorer crashes and file path confusion
category: system-behavior
date: 2026-03-27
source: "strategy-004 meta-s4-002, strategy-004 meta-s4-005, compton-unruh strategy-001 meta-exploration-001"
---

## Lesson

Explorers occasionally crash (likely from context exhaustion when spawned sub-agents pull too much data) and sometimes write files to wrong paths when similar-looking directories exist nearby. Both are recoverable but waste ~10 minutes each.

## Evidence

- **strategy-004 exploration s4-002** — Explorer crashed, likely from context exhaustion. Relaunch worked but wasted ~10 minutes. The report was also slightly over the line target (444 vs 400), suggesting the goal was at the limit of what one exploration can handle.
- **strategy-004 exploration s4-005** — Explorer wrote files to quantum-gravity/strategy-002 instead of quantum-gravity-2/strategy-004. Required manual file copying. Similar directory names caused confusion.

## Variant: tmux Session Failures

tmux sessions can die silently, especially when large text is pasted without an explicit Enter keystroke afterward. Always send Enter after pasting text into tmux. This is a mechanical issue that has caused exploration relaunches.

- **yang-mills strategy-001 exploration 003** — First attempt crashed (tmux session died). Required relaunch. Root cause: missing Enter after paste.

## Variant: Context Contamination in Parallel Launches

When launching multiple explorers in parallel, the second explorer may pick up contextual signals from a different mission and work on the wrong problem entirely. This is not a file path issue — the explorer's cognitive context gets contaminated.

- **compton-unruh strategy-001 exploration 002** — A standard explorer launched in parallel with a math explorer got confused and worked on the classicality-budget mission instead of compton-unruh. Root cause: insufficient grounding context in the goal prompt.
- **Fix:** When running parallel explorers, repeat key context (mission name, directory, problem statement) explicitly in each goal prompt rather than just pointing to GOAL.md. The second explorer needs stronger grounding.

## Variant: Usage-Limit Death with Intermediate Files

When a math explorer hits Claude's usage limit mid-task (session terminates without writing the report), check for intermediate .npz/.pkl files before declaring data lost. If computation was completed and results were saved, manual report completion is feasible.

**Recovery workflow:**
1. Check for saved files: `ls code/*.npz code/*.pkl` (or wherever the goal specified output)
2. Load and inspect: `python3 -c "import numpy as np; d = np.load('results.npz'); print(list(d.keys()))"`
3. Write the report manually, matching the section structure of the GOAL.md
4. Add explicit save instructions to the goal for next time: "After each computation block, save to .npz before proceeding" (see goal-design/specify-computation-parameters.md)

- **riemann-hypothesis strategy-002 exploration-009** — Fourth consecutive session to die without writing the report (E006-E009). Report completed manually from `code/results_exact.npz`. All computation data intact; only the REPORT.md section was missing.

**Distinction from context-exhaustion crash:** Usage-limit death = session terminates cleanly but suddenly, mid-sentence if necessary. Context-exhaustion crash = session aborts, often without saving. Both can leave intermediate files; check in both cases.

## Variant: CWD Drift During Computation (Math Explorer)

A distinct path confusion variant: the explorer's current working directory **silently drifts** to a different exploration directory mid-session. The tmux session shows the correct starting directory, but the explorer navigates away (e.g., `cd ..` relative to a wrong assumption) and continues working coherently in the wrong directory. Because the directory structure is similar (another exploration-NNN/ under a different strategy), the explorer doesn't notice.

- **riemann-hypothesis strategy-003 exploration-005** — Explorer was launched in strategy-003/exploration-005 with a goal to compute K(τ) from prime orbit sums. Instead, it navigated to strategy-002/exploration-005 and ran C1 rescoring + Gauss Δ₃ computations — entirely wrong task, entirely wrong directory. Results were valid and scientifically valuable, but the original goal (prime orbit K(τ)) was never attempted. Required manual file copying to recover.

**Key difference from other path confusion variants:** The explorer didn't just write output to the wrong path — it read input from and worked in a different exploration's context entirely, executing a different exploration's work.

**Prevention: Add explicit directory confirmation as Task 0 in every GOAL.md:**

```
## CRITICAL: Confirm Working Directory
Your working directory should be explorations/exploration-NNN/.
Run: `pwd` and `ls` first. If you see files from a different exploration, STOP and cd to the correct directory.
Expected directory: /full/absolute/path/strategy-NNN/explorations/exploration-NNN/
```

This supplements the existing `use-absolute-file-paths.md` guidance (which covers output paths) with CWD verification (covering the explorer's operational context).

## When to apply

Always check report output after exploration completes -- verify the file exists at the expected path and has reasonable length. When designing goals with many deliverables (7+), consider whether the combined context might cause crashes. Use absolute paths in all goal file references (see also: goal-design/use-absolute-file-paths.md). For tmux-based launches, always explicitly send Enter after pasting the goal text. For parallel launches, repeat essential context in each explorer's goal prompt. When a session dies before completing the report, check for intermediate .npz/.pkl files immediately — computation may be fully recoverable. **For Math Explorer launches, add Task 0 "confirm working directory" (pwd + ls + expected path) to every GOAL.md.**
