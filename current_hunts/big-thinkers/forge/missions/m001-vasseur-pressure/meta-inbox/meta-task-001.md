---
topic: Code worker simulation timeout management
category: goal-design
date: 2026-03-30
source: m001-vasseur-pressure, strategy-001, task-001
---

Code workers running long simulations (>2 min) hit Bash timeout limits and stall. The worker tried running N=128 simulations inline and kept timing out. Eventually it used tmux sub-agents (good), but then got stuck polling them with sleep+tail (also timing out).

Lessons:
1. SPECs for simulation tasks should explicitly warn about the 10-minute Bash timeout and recommend saving scripts to files and running via `python3 script.py > output.txt 2>&1 &` or tmux sub-agents
2. For polling, suggest `tmux has-session` + `tail -5 output.txt` without sleep (just run the check commands directly and accept the output)
3. Splitting simulation runs into separate invocations (one per Re×N combo) works better than one monolithic script
4. scipy.fft with workers=-1 gave 5× speedup — should be standard in all NS simulation SPECs
