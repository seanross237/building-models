# Open-Eywa Dual Runtime Provider Plan

## Goal

Build Open-Eywa so one run can be launched with a runtime provider parameter such as:

- `openrouter`
- `claude`
- `codex`

The operator should be able to run the same Open-Eywa mission shape and choose which backend executes the node roles for that run.

Initial target:

- one provider for the whole run
- same orchestrator
- same node contract
- same role contract enforcement
- same mission/run artifacts

The runtime backend should be replaceable. The orchestrator should not care whether the work came from OpenRouter, Claude CLI, or Codex CLI.

## Operator UX I Would Build

I would make the canary entrypoint look like this:

```bash
python system/scripts/run_live_canary.py --runtime-provider openrouter --model google/gemini-2.5-flash-lite
python system/scripts/run_live_canary.py --runtime-provider claude --model claude-sonnet-4-6
python system/scripts/run_live_canary.py --runtime-provider codex --model gpt-5.4-mini
```

I would also support an optional per-role override later, but not in v1.

V1 parameter set:

- `--runtime-provider openrouter|claude|codex`
- `--model <model-name>`
- keep current canary flags like `--goal`, `--root-role`, `--max-iterations`

## First Spike Before Real Build

Before building anything substantial, I would verify one local fact:

- does `claude -p` use the desired monthly-plan path in your local setup?
- does `codex exec` use the desired monthly-plan path in your local setup?

This matters because Open-Eywa can choose the local CLI, but it cannot force the CLI's billing mode. If the installed CLI invocation path does not actually consume subscription credits the way you want, then the implementation needs an interactive or tmux-based path instead of a simple blocking non-interactive path.

I would treat this as a hard prerequisite spike, not an afterthought.

## Core Design Decision

I would keep the current runtime seam as the stable boundary:

- `RuntimeRequest`
- `RuntimeResult`
- `RuntimeAdapter.run(request) -> result`

That means:

- no orchestrator rewrite
- no return to the old `/eywa` bash state machine
- no provider logic in node progression or node lifecycle

The current system is already shaped correctly for a second and third backend.

## What Stays Stable

These parts should remain unchanged in meaning:

- `system/orchestrator/orchestrator_core.py`
- `system/orchestrator/orchestrator_progression.py`
- `system/orchestrator/role_contracts.py`
- node statuses and terminal outcomes
- required artifacts like `output/plan.md`, `output/final-output.md`, `output/escalation.md`

Code should still decide whether a run succeeded by checking artifacts and contract rules after the runtime returns.

## Runtime Architecture I Would Build

### 1. Replace the OpenRouter-only factory with a provider-selecting factory

Current shape is too narrow:

- `build_openrouter_runtime_for_live_canary(...)`

I would replace it with a provider-neutral builder, for example:

- `build_live_runtime(settings: LiveRuntimeSettings) -> RuntimeAdapter`

And use:

- `runtime_provider: Literal["openrouter", "claude", "codex"]`
- `model_name: str`
- provider-specific optional settings grouped cleanly

I would keep the OpenRouter builder as a thin internal helper, but stop making it the public top-level default path.

### 2. Add a shared CLI runtime base

I would add a shared module for the common CLI path, for example:

- `system/runtime/cli_runtime_base.py`

Its job:

- load the prompt bundle
- load prepared context packet(s)
- assemble one provider-neutral task file for the run
- launch the selected CLI in the node directory
- capture stdout/stderr into the run directory
- return a `RuntimeResult`

This avoids duplicating most of the runtime logic for Claude and Codex.

### 3. Add provider-specific adapters

I would add:

- `system/runtime/claude_cli_runtime.py`
- `system/runtime/codex_cli_runtime.py`

The shared base would handle task construction and result packaging.

The provider-specific adapters would only handle:

- exact command-line shape
- model flag wiring
- sandbox/approval flags
- how to pass the prompt or task file
- provider-specific metadata in `RuntimeResult.details`

### 4. Keep OpenRouter as its own adapter

I would leave:

- `system/runtime/openrouter_runtime.py`

mostly intact.

That backend already works through the same seam and should remain the API-backed option.

## Prompt and Task Packaging

I would not try to make the CLIs consume the OpenRouter message format directly.

Instead, I would build a shared run task file, probably under the run directory, for example:

- `system/runs/run-XXX/runtime-task.md`

That file would contain:

- role name
- selected provider
- prompt bundle content
- support docs content
- current runtime note
- prepared context packet path and embedded summary
- exact write requirements for artifacts
- trust-boundary reminders

Then the CLI backend would get a short invocation prompt like:

- "Read `system/runs/run-001/runtime-task.md` and execute it."

This keeps the prompt inspectable on disk and mirrors the working lesson from old `/eywa` without requiring tmux.

## Trust Boundary I Would Preserve

The main risk with CLI providers is tool sprawl.

OpenRouter currently exposes only a small node-bounded file tool layer. Claude CLI and Codex CLI can be much broader. To keep the rebuild disciplined, I would do this:

### V1 trust boundary

- run the CLI with cwd at the node root
- only grant extra readable/writable dirs deliberately
- keep success determined by artifact validation after the run
- forbid provider-specific protocol decisions from living in prompts

### V1 practical scope

I would aim for CLI parity with the current live seam first, not maximum tool power.

That means the task file should still say, in effect:

- work from prepared context
- write required node artifacts
- do not mutate orchestrator control files directly

If we later want "Claude/Codex with broader shell access," I would make that a separate tool profile decision, not something hidden inside the provider switch.

## Usage and Cost Recording

This is a meaningful design difference.

### OpenRouter

Keep the current behavior:

- token counts
- direct USD cost
- provider metadata

### Claude CLI / Codex CLI

I would not fake API-style costs.

For CLI-backed subscription runs, I would record:

- `provider_name`
- `provider_kind = "cli_subscription"`
- command metadata
- stdout/stderr artifact paths
- `total_cost_usd = 0.0`
- `provider_details.accounting_mode = "subscription_or_external"`
- `provider_details.usage_unavailable = true`

This keeps facts honest. If later either CLI provides reliable structured usage, we can add it without changing the orchestrator contract.

## Optional Tmux Mode

I would not make tmux the first implementation target.

I would build in two phases:

### Phase A

Blocking non-interactive CLI backend:

- Claude via `claude -p ...`
- Codex via `codex exec ...`

### Phase B

Optional tmux-backed execution mode for CLI providers:

- `execution_mode = "direct" | "tmux"`

Tmux mode would add:

- persistent session name recording
- pane capture logs
- zombie detection
- nudge and respawn logic

I would only build Phase B after Phase A works, because the monthly-credit goal may already be satisfied by direct CLI mode.

## Exact File Changes I Would Make

### New files

- `system/runtime/claude_cli_runtime.py`
- `system/runtime/codex_cli_runtime.py`
- `system/runtime/cli_runtime_base.py`
- `system/runtime/runtime_task_builder.py`
- `validation-suite/contract-tests/test_claude_cli_runtime.py`
- `validation-suite/contract-tests/test_codex_cli_runtime.py`
- `validation-suite/contract-tests/test_runtime_task_builder.py`

If tmux mode is added later:

- `system/runtime/tmux_session_manager.py`
- `validation-suite/contract-tests/test_tmux_session_manager.py`

### Existing files to change

- `system/runtime/runtime_factory.py`
  - replace OpenRouter-only entrypoint with provider-neutral live runtime builder
- `system/runtime/__init__.py`
  - export the new settings and builders
- `system/scripts/run_live_canary.py`
  - add `--runtime-provider`
  - route through the new provider-neutral runtime factory
- `system/scripts/README.md`
  - document the new launch options
- `OPEN-EYWA-IMPLEMENTATION-DETAILS.md`
  - update after implementation because the live runtime shape will have materially changed

## Implementation Order I Would Follow

### Step 1

Add provider-neutral runtime settings and builder.

Deliverable:

- one code path that chooses `openrouter`, `claude`, or `codex`

### Step 2

Extract shared run-task assembly out of `openrouter_runtime.py` into a reusable helper where it makes sense.

Deliverable:

- one canonical place that packages prompt bundle + prepared context into runtime instructions

### Step 3

Implement `ClaudeCliRuntime`.

Deliverable:

- `runtime.run(request)` launches Claude CLI, captures outputs, and returns a valid `RuntimeResult`

### Step 4

Implement `CodexCliRuntime`.

Deliverable:

- same contract as Claude runtime
- isolated command construction because Codex uses a different CLI shape

### Step 5

Wire the script entrypoint and test both providers on the tiny canary path.

Deliverable:

- the same `run_live_canary.py` script can run with all three providers

### Step 6

Add optional tmux mode only if the direct CLI mode does not meet the monthly-credit or inspectability need.

## Validation I Would Require

### Contract tests

- runtime factory selects the correct backend
- Claude runtime produces valid `RuntimeResult`
- Codex runtime produces valid `RuntimeResult`
- CLI task file is built correctly from prompt bundle + prepared context

### Scenario/integration tests

- worker canary with `claude`
- worker canary with `codex`
- multi-step tree canary with at least one CLI provider

### Manual checks

- confirm provider parameter works
- confirm artifacts are still the thing that determines success
- confirm run logs are written under `system/runs/run-XXX/`
- confirm failed CLI runs map cleanly to `failed`, `timed_out`, or `crashed`
- confirm billing/account mode is the desired monthly-plan path

## Main Risks

### 1. Billing mismatch

The CLI may be authenticated, but not through the account path you want.

Mitigation:

- verify this first with a manual spike

### 2. CLI tool access is broader than OpenRouter tool access

Mitigation:

- keep provider switch separate from tool-profile broadening
- keep success/failure enforced in code after the run

### 3. Codex and Claude CLI interfaces are not symmetrical

Mitigation:

- isolate command construction per provider
- do not over-abstract the provider adapters

### 4. Usage reporting will be inconsistent across providers

Mitigation:

- record honest provider metadata
- do not fake token or cost fields for CLI-backed subscription runs

## Recommendation

I would build this in two milestones.

### Milestone 1

Provider-selectable live runtime:

- `openrouter`
- `claude`
- `codex`

using direct non-interactive CLI mode for the two CLI providers.

### Milestone 2

Optional tmux-backed execution mode for `claude` and `codex` if needed for:

- subscription behavior
- human inspectability
- zombie recovery

That gets you the operator experience you asked for with the smallest clean change to current Open-Eywa.
