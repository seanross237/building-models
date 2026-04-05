# Meta-Learning: Exploration 009 (Strategy 002, Exploration 004)

**What worked well:**
- "Work backward from data" framing produced the most actionable result so far — a specific calculation that needs to be done
- Asking for quantitative predictions (actual numbers for n_s) forced precision
- The explorer correctly identified the DESI-driven nature of the tension, which changes the strategic assessment

**What didn't work:**
- Explorer started editing wrong exploration files (got confused between exploration-003 and 004). Had to kill and restart. Clearer initial prompt needed.
- Explorer still batches writing despite "write after EVERY finding" instruction.

**Lessons:**
1. Working backward from observational tensions is extremely productive — it produces well-defined calculation targets
2. Always specify the exploration number explicitly in the initial prompt, not just the goal file path
3. The n_s tension being DESI-driven is important — it means a single dataset is driving the discrepancy, which could be a systematic
4. The physical beta functions paper (2024 PRL) is a game-changer — makes a previously ambiguous calculation unambiguous
5. Best next step: compute n_s from QG+F beta functions. This is a concrete, doable calculation.
