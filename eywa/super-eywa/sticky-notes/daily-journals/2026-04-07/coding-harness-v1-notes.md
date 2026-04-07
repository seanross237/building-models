# Coding Harness V1 Notes

- Added packetized coding benchmark support under `data-system/grading/coding-packets/`.
- Coding runs now use a submission contract that asks execute turns to return a `main.py` artifact instead of only `FINAL_ANSWER` text.
- The engine now persists execute-time artifacts under run-history and threads them through `attachment_refs` into `final-output.json`.
- Added execution-backed grading for packetized coding tasks:
  - `binary_public_tests`
  - `binary_public_checker`
  - `continuous_public_simulator`
- Converted current runnable coding coverage for:
  - `coding-B1`
  - `coding-B2`
  - `coding-B3`
- Continuous-score coding tasks still need real packet bundles and public simulators before they stop grading as `ungraded`.
