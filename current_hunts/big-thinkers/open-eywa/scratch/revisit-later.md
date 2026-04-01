# Revisit Later

- Planner prompt guidance now discourages child steps that perform parent-level synthesis or review, but real planners may still propose them. The current child `input/context.md` handoff makes those runs viable; revisit later if this still causes avoidable cost or churn.
- `system/orchestrator/orchestrator_progression.py` is still the main complexity pressure point. Keep watching for chances to split more decision logic into smaller modules if new behaviors start to pile up there.
