---
topic: Use absolute file paths in goals
category: goal-design
date: 2026-03-27
source: "strategy-004 meta-s4-005"
---

## Lesson

Always include the FULL absolute path for any files the explorer should read or write. Relative paths cause explorers to write to the wrong directory, especially when similar-looking directories exist nearby in the filesystem.

## Evidence

- **strategy-004 exploration s4-005** — Explorer wrote files to quantum-gravity/strategy-002 instead of quantum-gravity-2/strategy-004. Required manual file copying. The directories had similar names, and the explorer resolved the relative path incorrectly.

## When to apply

Every exploration goal that references file paths. No exceptions.
