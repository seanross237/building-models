# Coding S1-S6 Packetization Notes

- Added real coding packets for `coding-S1` through `coding-S6`.
- Vendored the official AtCoder local tool bundles into each packet under `tools/`.
- Extended the coding packet schema with `official_tool.mode`, `official_tool.path`, and `official_tool.timeout_seconds`.
- Added a shared AtCoder tool runner in `data-system/grading/atcoder_official_tools_v1.py`.
- `S1`, `S2`, `S3`, `S5`, and `S6` use the official `vis` binary on bundled public instances.
- `S4` uses the official `tester` first, then runs `vis` on the captured transcript output.
- Public continuous scoring currently uses three bundled instances per task (`0000`, `0001`, `0002`) to keep MX1 runtime manageable.
- `S4` uses a tighter official-tool timeout (`10s`) because bad interactive submissions can otherwise stall the loop for too long.
- Regenerated `question-bank-v1.json`, and all `coding-S1..S6` now show `coding_packet_exists=true`.
- Deterministic smoke runs now return `grading_status=graded` for all six `S` tasks.
