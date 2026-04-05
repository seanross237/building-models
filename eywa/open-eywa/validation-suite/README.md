# Validation Suite

This suite is being rebuilt before live model testing resumes.

The intended layers are:

- `contract-tests/`
  Small deterministic tests for node invariants and protocol rules.
- `adversarial-tests/`
  Small high-value weird-case tests for fast sturdiness checks.
- `scenario-tests/`
  Offline end-to-end tests using simulated agent behavior.
- `canaries/`
  Very small live integration tests for later, after the offline suite is solid.
- `notes/`
  Test taxonomy, priorities, and reliability thinking.

The core principle is:

- prove orchestration correctness offline first
- use live models only as a thin integration check

Fast check:

```bash
python3 system/scripts/run_fast_sturdiness_suite.py
```
