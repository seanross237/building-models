# Meta-Learning: Exploration S4-002 (BH Phase Transition)

## What worked
- Rich pre-loaded context (Bonanno-Reuter values, instability threshold, E001 ghost mass) let the explorer compute numbers directly
- Classification scheme (DISCRIMINATING/NOVEL/etc.) forced honest categorization — revealed that most predictions are inherited
- Including failure path instruction produced the critical finding: convention dependence (M_P vs M̄_P) is a genuine systematic uncertainty

## What didn't
- The explorer initially crashed (likely context exhaustion from spawned sub-agents pulling too much data), requiring relaunch
- 7 deliverables was at the limit — the report was 444 lines, slightly over the target 400

## Lesson
When exploring a domain's predictions, the classification scheme is ESSENTIAL — without it, you get a list of "predictions" that sounds impressive but is mostly inherited from standalone frameworks. The honest classification revealed that only 1 of 12 BH predictions is genuinely discriminating. This pattern (lots of consistency checks, few discriminators) may be a structural feature of the unified framework, not a failure of the exploration.

Also: explorer crashes happen. Always check the report length before declaring done. The relaunch strategy works but wastes ~10 minutes.
