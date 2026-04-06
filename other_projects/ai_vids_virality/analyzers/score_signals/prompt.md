# Score Signals Prompt (Phase 1 placeholder)

This prompt is unused in Phase 1. The Phase 1 analyzer is a deterministic
rule-based scorer (`analyze.py`) that does not call any LLM. The seam exists
so Phase 2 can drop a real Claude prompt here without changing the analyzer
caller.

When this becomes real, return a JSON object matching `schema.json` with:
- summary
- sketchability_score (1-10)
- comedy_angles
- character_archetypes
- topical_window_hours
- should_promote (bool)
