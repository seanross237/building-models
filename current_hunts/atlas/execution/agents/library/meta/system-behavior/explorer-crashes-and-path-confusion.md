---
topic: Explorer crashes and file path confusion
category: system-behavior
date: 2026-03-27
source: "strategy-004 meta-s4-002, strategy-004 meta-s4-005"
---

## Lesson

Explorers occasionally crash (likely from context exhaustion when spawned sub-agents pull too much data) and sometimes write files to wrong paths when similar-looking directories exist nearby. Both are recoverable but waste ~10 minutes each.

## Evidence

- **strategy-004 exploration s4-002** — Explorer crashed, likely from context exhaustion. Relaunch worked but wasted ~10 minutes. The report was also slightly over the line target (444 vs 400), suggesting the goal was at the limit of what one exploration can handle.
- **strategy-004 exploration s4-005** — Explorer wrote files to quantum-gravity/strategy-002 instead of quantum-gravity-2/strategy-004. Required manual file copying. Similar directory names caused confusion.

## When to apply

Always check report output after exploration completes -- verify the file exists at the expected path and has reasonable length. When designing goals with many deliverables (7+), consider whether the combined context might cause crashes. Use absolute paths in all goal file references (see also: goal-design/use-absolute-file-paths.md).
