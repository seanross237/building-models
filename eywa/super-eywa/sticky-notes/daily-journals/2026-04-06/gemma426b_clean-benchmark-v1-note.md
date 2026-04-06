# Gemma Clean Benchmark V1

- Label: `gemma426b_clean_benchmark_v1_2026_04_06`
- Runtime provider: `openrouter`
- Model: `google/gemma-4-26b-a4b-it`
- Clean runner: `data-system/grading/run_clean_benchmark_v1.py`
- Clean prompt: `data-system/grading/prompt-experiments/benchmark-clean-v1/execute_prompt_v1.txt`
- Rebuilt summary: `data-system/grading/runs/gemma426b_clean_benchmark_v1_2026_04_06__summary_rebuilt.json`
- Manual review overlay: `data-system/grading/runs/gemma426b_clean_benchmark_v1_2026_04_06__manual-review.json`

Classification:

- Runnable as stored: `17`
- Benchmark-incomplete as stored: `5`
- Harness-missing / unscorable as stored: `9`

Trusted manual outcome on the runnable slice:

- Counted correct: `4`
- Counted wrong: `12`
- Partial but not counted correct: `1`
- Accuracy on runnable slice: `4 / 17` = `23.53%`

Aggregate run metrics on the runnable slice:

- Total tokens: `23,537`
- Total wall time: `194,489 ms`
- Total cost: `$0.007078`
- Average tokens per completed runnable question: `1,384.53`
- Average wall time per completed runnable question: `11,440.53 ms`
- Average cost per completed runnable question: `$0.000416`

Runtime / grading cleanup made during this pass:

- Added configurable OpenRouter generation settings via run-level variables in `eywa-system/runtime/eywa_runtime/executor.py`
- Added response-shape coercion for trivial `response` object mismatches in `eywa-system/runtime/eywa_runtime/authored_response.py`
- Added B4-specific `m=` extraction and B2 signed numeric grading in `data-system/grading/grading_methods/simple_grade_v1.py`
- Added `data-system/grading/build_clean_benchmark_summary_v1.py` so summaries can be rebuilt under current grading logic

Known remaining issues:

- `B6` and `B9` still hit malformed / truncated model outputs under the clean execute prompt
- Several architecture questions are benchmark-incomplete because the stored prompt omits answer choices or worked derivation material
- All coding questions remain harness-missing as stored; the repo still lacks executable benchmark instances / scorers for them
