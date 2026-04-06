# Grading

This is the Super-Eywa grading area.

It is the place for effectiveness-oriented question/task grading, separate from the correctness suite.

Structure:

- `test-questions/`
- `question-types/`
- `grading_methods/`
- `runs/`
- `reviews/`
- `tutoring/`
- `mx1-loops/`
- `mx1-tutoring/`
- `experiment-runs/`
- `benchmarks/`
- `prompt-experiments/`
- `supabase/`
- `all-test-questions.md`

Current runnable utilities:

- `run_test_question_v1.py`
- `run_live_batch_v1.py`
- `run_prompt_family_experiment_v1.py`
- `run_tutor_v1.py`
- `run_mx1_pilot_v1.py`
- `run_mx1_tutor_v1.py`
- `sync_to_supabase_v1.py`

Current notes:

- the question bank is only partly runnable right now
- the first grading pass uses a small explicit subset of simple graders
- the first prompt-family experiment freezes a 3-question benchmark and compares `baseline_execute` against `root transmute -> child execute`
- prompt-family experiment summaries are written under `experiment-runs/` and can be rendered with `data-system/derived-views/prompt-family-results/build_prompt_family_results_page.py`
- grading is automatic, but tutor output is manual and lives separately from the run path
- older reviewer sidecar JSON lives under `reviews/`; new manual tutor sidecars live under `tutoring/`
- MX1 pilot loops keep their manifest truth in `mx1-loops/` and their prompt-optimization tutor sidecars in `mx1-tutoring/`
- Supabase remains a derived layer; local disk artifacts stay canonical truth
