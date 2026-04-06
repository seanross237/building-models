# Prompt Profiles

This folder holds named prompt-profile fragments that Eywa nodes can run with through explicit variables.

Each profile should be:

- named
- versionable through file history
- human-readable
- injectable before the node task itself

The runtime currently expects:

- a prompt family and selected prompt text to define the main orchestration prompt
- zero or more extra prompt profiles through `additional_instruction_prompt_profiles`

Current implementation note:

- the runtime loads the actual profile text from `eywa-system/runtime/eywa_runtime/prompting.py`
- the markdown files in this folder are the readable mirrored definitions for the supplemental profile layer and should stay aligned with that source
