# Scripts

This directory will hold entry points for the rebuilt system.

Examples later:

- create node
- run mission
- run offline scenarios
- run validation suite
- inspect a node

Current scripts:

- `run_fast_sturdiness_suite.py`
  - runs contract tests, adversarial tests, and a compile check
- `run_live_canary.py`
  - runs a tiny real canary mission through a selectable runtime provider
  - `--runtime-provider openrouter|claude|codex` (default: `openrouter`)
  - `--model <model-name>` (default: `openai/gpt-4.1-mini`)
  - `--timeout-seconds <N>` for CLI provider subprocess timeout (default: 300)
  - OpenRouter-specific: `--referer-url`, `--title`, `--no-generation-stats`
