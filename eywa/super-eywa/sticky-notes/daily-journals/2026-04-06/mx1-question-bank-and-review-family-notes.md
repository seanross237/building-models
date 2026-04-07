Question-bank + MX1 build notes for 2026-04-06

What changed
- Normalized grading-bank access now goes through `question_bank_v1.py` and `question-bank-v1.json`.
- `load_question_case()` now falls back to parsing arbitrary markdown files directly when a temp file path is not present in the canonical catalog. This keeps catalog-backed official runs while allowing tests that create temporary copied question files.
- Added first-class `review` family support to the prompt-family path that is actually runnable in the engine: `review` is now a real authored orchestration decision, and the engine turns it into one review child plus a parent synthesis turn.
- Kept generic `agent_chooses` from selecting `review` by default. Review is available when the prompt family explicitly asks for it, rather than becoming a surprise default branch in generic orchestration.
- Added a review starter prompt file for MX1.
- Extended MX1 runner support so `execute` / `review` / `delegate` / `transmute` all resolve to family-appropriate starter prompts and budget configs.
- Patched the existing `run_mx1_sweep_v1.py` so it no longer hard-fails on a missing optional `build_mx1_results_page` import.
- Updated the default 3-question MX1 benchmark to use `B4` / `B5` / `B6` for cleaner exact-answer grading.

Tests
- `eywa-system/runtime/tests`: green
- `data-system/grading/tests`: green
- Added deterministic sweep coverage for `review` family.

Live verification
- A live 2-iteration `review`-family smoke on `B6` completed successfully.
- A live all-four-families one-iteration smoke on `B6` is being used as the matrix sanity check before attempting larger sweeps.
- The MX1 browser view now exists at `data-system/derived-views/mx1-results/index.html`.
- The current long-running full-sweep processes were launched one-question-per-session:
  - `B4` session `53939`
  - `B5` session `75807`
  - `B6` session `37515`
  - loop label: `mx1_v1_2026_04_06`

Judgment calls
- `review` is now a real family/decision instead of being faked as `delegate`-to-one. The repo already had half of that path in contracts/authored-response/executor, so finishing it was cleaner than fighting the existing shape.
- Full 3-question x 4-family x 20-iteration live MX1 is very expensive in wall-clock time and model calls. The infrastructure is ready for it, but it is not a quick within-turn operation.

Sweep check-in at 2026-04-06 17:27:44 +0545
- The original `B4` and `B6` sweep sessions had died while `B5` kept running.
- Root cause: `mx1_tutor_v1.py` only attempted strict `json.loads(...)` parsing on tutor output and would crash the whole loop when the tutor emitted raw backslashes like `\equiv`.
- Fix applied:
  - `_parse_json_or_repair(...)` now tries sanitized JSON candidates that escape invalid backslashes.
  - `_build_openrouter_tutor(...)` now falls back to the deterministic tutor if both the original tutor response and the repair response are still unparsable.
  - Added regression tests in `data-system/grading/tests/test_mx1_tutor_v1.py`.
- Focused grading tests passed after the fix:
  - `python3 -m unittest data-system/grading/tests/test_mx1_tutor_v1.py`
  - `python3 -m unittest data-system/grading/tests/test_mx1_pilot_v1.py data-system/grading/tests/test_run_and_tutor_v1.py`
- The live sweep was restarted cleanly from saved manifests after patching:
  - `B4` session `49784`
  - `B5` session `26662`
  - `B6` session `70635`
- Health check after restart:
  - all three processes alive
  - `B4 execute` advanced to 11 iterations
  - `B5 delegate` advanced to 9 iterations
  - `B6 execute` advanced to 12 iterations
- MX1 page rebuilt from current manifests:
  - `data-system/derived-views/mx1-results/index.html`

Agent grading switch at 2026-04-06 evening
- The old script-first grading path in `grading_methods/simple_grade_v1.py` is no longer the live default.
- Added `grading_methods/agent_grade_v1.py` and switched `run_test_question_v1.py` to use agent grading by default for live runs.
- Resolution logic:
  - `grading_provider=same` now resolves to `openrouter` for live runs and `deterministic` for offline tests.
  - deterministic grading still uses the old reference checker as an offline fallback so tests remain stable.
- New grading metadata now lands in each grading record:
  - `grader_provider`
  - `grader_model`
  - `grading_method`
  - `grading_trace_path`
- Grading traces are now written under `grading-traces/`.
- Supabase schema and sync were updated so `graded_runs` keeps the new grader metadata.
- Verified:
  - targeted grading tests green
  - runtime tests green
  - deterministic standalone grading smoke green
  - live MX1 smoke green on `B6 execute`
  - the live smoke grading row synced to Supabase successfully
- The old `mx1_v1_2026_04_06` sweep was stopped because it was started under the old script grader and should not be mixed with the new agent-graded runs.

Resilient parallel MX1 relaunch at 2026-04-06 evening
- Added `data-system/grading/run_mx1_resilient_v1.py` so each `(question, family)` loop can keep retrying from its manifest until `iterations_target` is reached.
- Relaunched the fresh agent-graded sweep as 12 parallel background processes, one per question-family pair, all under loop label `mx1_agent_grade_v1_2026_04_06`.
- This matches the intended parallelism boundary:
  - sequential only within one `(question, family)` loop
  - parallel across different questions and families
- Hardened manifest writes by keeping `mx1_loop_v1.write_json(...)` on atomic replace semantics.
- Hardened the MX1 results page builder so a single bad manifest read no longer crashes the whole page build.
- One transient manifest issue showed up on `B4 / delegate`; it was repaired and the loop is now advancing again.
- Confirmed live progress after relaunch:
  - all 12 question-family loops are active
  - the MX1 page rebuilds cleanly again
  - at least one fresh agent-graded correct hit has already landed:
    - `B6 / transmute / iteration 3`
    - grading row: `data-system/grading/runs/architecture-derived-B6-binary-representation-minimization/mx1_transmute_03__architecture-derived-B6-binary-representation-minimization__transmute__mx1_agent_grade_v1_2026_04_06__transmute__03__run_2026_04_06_140754.json`
