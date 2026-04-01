# Meta-Learning: Strategy-002 Exploration 001 (BKM Enstrophy Bypass Validation)

## What Worked Well
- **Progress file logging**: The explorer created a progress.txt that logged each DNS run with timestamps, parameters, and key results. This was invaluable for monitoring — I could see exactly which runs completed and what the headline numbers were WITHOUT capturing the tmux pane. Future math explorer goals should request this pattern.
- **Incremental computation then report**: The explorer ran all computations first (storing results in JSON files), then wrote the report from the stored data. This is the right pattern for heavy-compute explorations.
- **Well-specified constants**: Providing exact values for C_L = 0.827 and C_CZ = 0.24 avoided any ambiguity about which constants to use.
- **Clear success/failure criteria**: "T_BKM/T_Lad > 10" was unambiguous and the results exceeded it by 10⁶-10¹⁵.

## What Could Be Improved
- **Report writing was slow**: After all computations finished (~02:37), the report wasn't written until ~02:41. The explorer spent ~4 minutes thinking about the report structure. The "write section by section" instruction was in the GOAL but the explorer wrote a skeleton first and filled it all at once at the end. Consider: "Write each section IMMEDIATELY after computing its results."
- **N=128 convergence check took 12 minutes**: This dominated the total wall time. For future explorations, consider making high-res convergence checks optional ("if time permits") rather than mandatory.
- **Anti-parallel tube IC not reconstructed exactly**: The explorer used sigma=2.5 but couldn't confirm the exact parameters from Strategy-001 exploration 003. Should have provided the IC generation code path explicitly.

## Lessons
- For gating computations (go/no-go decisions), a single comprehensive math exploration with multiple ICs and Re values is better than splitting into multiple explorations. The explorer delivered all the data needed to validate the direction in one shot.
- The progress file pattern should become standard for all math explorations. It costs nothing and eliminates the need for tmux pane capture.
