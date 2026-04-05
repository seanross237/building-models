# Prompt Profiles

This folder holds named prompt-profile fragments that Eywa nodes can run with through explicit variables.

Each profile should be:

- named
- versionable through file history
- human-readable
- injectable before the node task itself

The runtime currently expects:

- one base orchestration prompt profile through `injected_prompt_profile`
- zero or more extra prompt profiles through `additional_instruction_prompt_profiles`

Current implementation note:

- the runtime loads the actual profile text from `eywa-system/runtime/eywa_runtime/prompting.py`
- the markdown files in this folder are the readable mirrored definitions and should stay aligned with that source
