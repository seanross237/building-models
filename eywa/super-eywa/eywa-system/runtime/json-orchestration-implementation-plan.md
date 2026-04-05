# JSON Orchestration Implementation Plan

## Purpose

This doc defines the first implementation plan for moving Super-Eywa from:

- runtime-decided heuristic delegation

to:

- node-decided orchestration through JSON-authored responses

The main design goal is:

- every node must return JSON
- every node response must include `orchestration_decision`
- variables must control the orchestration prompt stack
- runtime code must validate and realize legal graph consequences

## Core Design Direction

The node should decide what to do next.

The runtime should:

- prepare the structured request
- validate the structured response
- enforce budgets and legal transitions
- translate authored decisions into node outputs, packets, edges, and stored artifacts

This preserves the intended Eywa split:

- variables shape behavior
- bones enforce protocol and truth preservation

## First-Cut Scope

The first implementation pass should support three authored decisions:

- `execute_locally`
- `delegate`
- `report_problem`

This pass should not yet add a fully open-ended iterative replan loop.

The existing human-facing action layer should stay:

- `local_attempt`
- `local_replan`
- `recruit_help`
- `report_success`
- `report_problem`

The runtime will map JSON decisions into those existing action labels.

## Node Response Schema

Each model-authored node response should be valid JSON and should match a fixed protocol shape.

### Required Top-Level Fields

- `schema_name`
  - always `eywa_node_response`
- `schema_version`
  - starting at `v1`
- `orchestration_decision`
  - one of:
    - `execute_locally`
    - `delegate`
    - `report_problem`
- `decision_notes`
  - short explanation of why this decision was chosen

### `execute_locally` Shape

Required extra field:

- `response`
  - the node's real authored result text

Optional extra fields:

- `result_type`
  - default `summary`

### `delegate` Shape

Required extra fields:

- `helpers`
  - non-empty list of helper specs

Optional extra fields:

- `synthesis_brief`
  - how the parent intends to use helper results on the follow-up turn

Each helper spec should preserve:

- `label`
- `instructions`
- `variable_overrides`

### `report_problem` Shape

Required extra field:

- `response`
  - problem explanation text

## Variable Surface

The runtime should continue to preserve the full resolved variable set for every node.

### Existing Variables To Keep

- `runtime_provider`
- `model`
- `context_policy`
- `workflow_structure`
- `verification_policy`
- `tool_policy`
- `budget_policy`
- `routing_policy`
- `recovery_policy`

### Variables To Change

The default prompt profile should change from:

- `default-builder`

to:

- `agent_orchestration_basic_instruction_prompt`

### New Variables To Add

- `additional_instruction_prompt_profiles`
  - list of extra prompt injections layered on top of the base orchestration prompt
- `json_response_policy`
  - default `strict_required`
- `orchestration_policy`
  - default `agent_decides`

These new variables should be preserved even if the first implementation uses only a subset of them deeply.

The budget policy should also include:

- `max_turns_per_node`
  - caps how many authored decision turns one node may take before runtime stops it

## Prompt Stack

The prompt sent to the model should be assembled in this order.

### 1. Fixed Protocol Header

This is code-owned and not variable-driven.

It should state:

- return JSON only
- do not wrap JSON in markdown
- use the Eywa node response schema exactly
- only use allowed decisions for this turn

### 2. Base Prompt Profile

This should come from:

- `injected_prompt_profile`

For the first pass, the default should be:

- `agent_orchestration_basic_instruction_prompt`

This prompt should explain:

- you may execute locally
- you may delegate
- you may report a problem
- if you delegate, write helper instructions
- if you execute locally, put the real answer in `response`
- always include `orchestration_decision`

### 3. Additional Prompt Profiles

These should come from:

- `additional_instruction_prompt_profiles`

Examples:

- `double_check_reasoning_prompt`
- `numerical_self_verify_prompt`
- `be_conservative_about_delegation_prompt`

### 4. Runtime Facts

The prompt should include structured turn facts such as:

- current node id
- current depth
- max depth
- max helpers
- routing policy
- recovery policy
- whether child results are present
- allowed decisions for this turn

### 5. Node Assignment And Child Results

The actual task should come last.

If child results are present, they should be injected in a structured form before the model decides the next step.

## Execution Flow

### Turn 1: Initial Node Decision

1. runtime resolves variables
2. runtime builds prompt stack
3. runtime calls provider
4. runtime parses authored JSON
5. runtime validates schema and budget legality
6. runtime maps the authored decision into legal node output and outgoing packets

### If The Node Chooses `execute_locally`

The runtime should:

- map authored decision to `report_success`
- store the `response` text as the node result content
- emit a `success_report` packet if routing requires it

### If The Node Chooses `delegate`

The runtime should:

- validate helper count against `budget_policy.max_helpers_per_node`
- reject delegation if depth already reached `budget_policy.max_depth`
- reject additional delegation if the current turn would exceed `budget_policy.max_turns_per_node`
- create one helper node per helper spec
- record `helper_assignment` packets
- run helper nodes
- collect child results
- call the same parent node again for a follow-up turn

### If The Node Chooses `report_problem`

The runtime should:

- map authored decision to `report_problem`
- preserve the explanation text
- emit a `problem_report` packet if routing requires it

## Parent Follow-Up Turn After Delegation

After helpers finish, the parent node should receive a second turn with:

- original assignment
- child results
- any stored `synthesis_brief`
- updated turn facts

Under the initial `workflow_structure = sequential_parent_review`, the runtime should allow:

- `execute_locally`
- `report_problem`
- `delegate`

That preserves the desired behavior where a parent may:

- synthesize immediately
- decide another delegation round is needed
- conclude it cannot proceed

Budget limits should still constrain repeated delegation.

## Runtime Mapping Rules

The runtime should compile authored JSON into existing node-output vocabulary.

### Decision To Action Mapping

- `execute_locally` -> `report_success`
- `delegate` -> `recruit_help`
- `report_problem` -> `report_problem`

### Decision To Packet Mapping

- `execute_locally`
  - usually a `success_report` to creator when not root
- `delegate`
  - one `helper_assignment` per helper
- `report_problem`
  - a `problem_report` to creator when not root

### Root Node Behavior

The root node should still produce no upward packet when it finishes.

Its result should remain the canonical final result for grading and summary views.

## Storage And Replay Changes

The existing file-first run layout should remain.

The runtime should add preserved truth for:

- the exact prompt stack used
- the raw authored JSON response
- the parsed response object
- any validation fallback or retry notes
- the derived node output created from the authored response

### Replay Expectations

For each node replay directory, replay should clearly preserve:

- authored request
- raw provider response
- parsed authored JSON
- derived node output

### Node Record Expectations

The node record should remain clean and readable.

It should additionally preserve enough prompt metadata to reconstruct:

- which prompt profiles were active
- which decisions were allowed in that turn

The node record should still preserve only the derived final result in `results`, while heavier raw authored material stays in replay.

## Failure Handling

The runtime must not trust the model blindly.

### Invalid JSON

If the model returns invalid JSON:

- retry once using a repair prompt if recovery policy allows
- otherwise record a system-side problem result

### Illegal Decision

If the model returns:

- too many helpers
- delegation when depth is exhausted
- missing required fields
- unknown decision value

the runtime should:

- treat this as invalid authored output
- apply recovery policy
- if not recoverable, convert it into a `report_problem` style terminal outcome with explicit notes

## Deterministic Runtime Behavior

Deterministic mode should implement the same JSON protocol.

It should not bypass the new authored response shape.

This keeps:

- tests meaningful
- offline runtime behavior structurally aligned with live behavior

The deterministic executor can still author simple synthetic JSON decisions without using a live model.

## Grading Compatibility

The grading layer should continue to grade the final textual answer.

The actual answer should now live inside:

- the node-authored JSON `response`

but the runtime should still store the derived final text in:

- `node_record.results[0].content`

This means grading can continue to read the root node record without learning the full orchestration schema immediately.

## Docs To Update

- `eywa-system/runtime/README.md`
- `eywa-system/variables/README.md`
- `eywa-system/variables/variable-schema-v1.md`
- `eywa-system/variables/default-run-level-variables.json`
- contract docs where examples still imply heuristic or non-JSON-authored behavior

## Code Areas To Update

- `eywa-system/runtime/eywa_runtime/defaults.py`
- `eywa-system/runtime/eywa_runtime/prompting.py`
- `eywa-system/runtime/eywa_runtime/contracts.py`
- `eywa-system/runtime/eywa_runtime/executor.py`
- `eywa-system/runtime/eywa_runtime/engine.py`
- `eywa-system/runtime/tests/test_runtime.py`
- `eywa-system/runtime/tests/test_validation.py`
- grading compatibility helpers if needed

## Tests To Run

### Runtime Unit Tests

```bash
python3 -m unittest discover -s eywa-system/runtime/tests -p 'test_*.py'
```

### Grading Unit Tests

```bash
python3 -m unittest discover -s data-system/grading/tests -p 'test_*.py'
```

### Deterministic Manual Smoke

```bash
python3 eywa-system/runtime/run_v1.py \
  --task "Design the backend and build the frontend and validate the feature."
```

Confirm:

- root node replay preserves authored JSON
- helpers are created from `delegate` JSON, not heuristic splitting
- node records preserve derived result text cleanly

### Validation Smoke

```bash
python3 data-system/correctness-suite/validate_run_v1.py <run_dir>
```

Confirm:

- stored run still satisfies structural validation

### Optional Live Smoke

```bash
python3 eywa-system/runtime/run_v1.py \
  --task "For each n, let k(n) be the number of ones in the binary representation of 2023*n. Find the minimum k(n)." \
  --runtime-provider openrouter \
  --model openai/gpt-4.1-mini
```

Confirm:

- live model returns JSON
- runtime can parse and act on it
- replay preserves both raw response and parsed authored response

## Acceptance Criteria

This refactor is successful when:

- every node response is required to be JSON
- every node response includes `orchestration_decision`
- delegation is decided by the node, not by heuristic split code
- prompt profiles are variable-driven and recorded
- runtime still writes valid run-history artifacts
- deterministic tests pass
- validation tests pass
- grading still works against stored root result text
