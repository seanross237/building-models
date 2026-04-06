## MX1 + Final Output Notes

- Added explicit `final_output` routing to the runtime.
- `transmute` now hands final-answer ownership to its child by default.
- `delegate` still keeps synthesis/final-answer ownership with the parent.
- Grading now reads canonical `final-output.json` first instead of assuming the root node is always final.
- MX1 pilot was updated so the transmute path is `root transmute -> child execute`, with no parent review turn.
- Tightened prompt/repair handling after Gemma returned near-correct but invalid wrapper JSON.
- Adjusted MX1 manifest logic so the loop’s “best prompt” is family-scoped rather than being hijacked by the execute baseline.
- Added compact run context and result excerpts into MX1 attempt history so the tutor can recommend the next prompt using actual run behavior, not just score/token/time.
- Current live pilot target: `architecture-derived-B6-binary-representation-minimization`, family `transmute`, loop label `live_b6_transmute_v2`.

## B6 MX1 v3 Outcome

- Fresh loop label: `live_b6_transmute_v3`.
- Tightened the fixed execute prompt first so Gemma would stop truncating invalid JSON and instead produce short valid answers.
- Baseline became valid and cheap: wrong answer `1`, `451` tokens, `3007` ms.
- Ran the full 10-iteration `transmute` loop with Gemma-as-tutor between attempts.
- All 10 transmute attempts stayed wrong on score.
- Best transmute efficiency landed at iteration `09`: wrong answer `1`, `709` tokens, `6939` ms.
- The loop did move around the efficiency surface, but it did not improve correctness over baseline.

## Tutor Bug Found

- Late in the loop, the tutor generated a prompt whose JSON scaffold had drifted from the `transmute` family toward `execute_locally`.
- Fixed by normalizing any applied tutor prompt back onto the family’s canonical scaffold before it becomes the loop’s next prompt.
- Added a test so future loops cannot silently drift prompt families this way.
