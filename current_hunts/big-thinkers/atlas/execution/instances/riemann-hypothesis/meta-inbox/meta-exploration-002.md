# Meta-Learning: Exploration 002

## What worked well
- **Providing all formulas explicitly** again paid off — the explorer went straight to code.
- **Setting a 5-minute computation budget** worked — total was 5.5 minutes.
- **Asking for 2000 zeros** (not 10,000) was the right call based on exploration 001's lesson.
- **Generating a GUE simulation as control** was the explorer's initiative and was extremely valuable — it separated finite-size effects from genuine zeta-specific saturation.
- **Validation against Poisson** was also the explorer's initiative and confirmed the algorithm was correct.

## What didn't work well
- **The report was 21 lines for a long time** — the explorer wrote a skeleton then didn't update until all computations were done. Same pattern as exploration 001. Not a problem per se, but makes progress monitoring harder.
- **Three statistics in one exploration** was borderline — the explorer handled it well, but the report is very dense. Two statistics would have been more comfortable.

## Lessons for future explorations
1. **Including a "control computation" in the goal** (e.g., "also generate a GUE simulation as finite-size control") would be worth adding explicitly. The explorer did it on its own this time, but shouldn't rely on that.
2. **Saving zero data to disk** (the explorer used numpy .npz files) worked well for running multiple analysis scripts. Worth suggesting in future goals that involve reusing data.
3. **The saturation result is well-known** (Berry 1985), but having it computationally verified with our own code is valuable as a constraint for Phase 2 operator testing.
