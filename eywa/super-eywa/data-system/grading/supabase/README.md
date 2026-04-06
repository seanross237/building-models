# Supabase Sync

This folder holds the first Supabase schema and sync notes for Super-Eywa grading data.

Principle:

- canonical truth stays on disk
- Supabase is a derived query layer on top

Current files:

- `schema_v1.sql`

The first sync script lives at:

- `../sync_to_supabase_v1.py`

Current v1 mirrored tables:

- `benchmark_questions`
- `graded_runs`
- `experiment_runs`
- `experiment_run_cases`
