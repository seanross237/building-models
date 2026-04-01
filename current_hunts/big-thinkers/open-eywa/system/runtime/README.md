# Runtime

This directory holds the rebuilt agent-run layer.

Current pieces:

- `runtime_interface.py`
  - stable runtime seam
- `simulated_runtime.py`
  - offline scripted runtime for confidence-building
- `prompt_loader.py`
  - loads prompt bundles from `stuff-for-agents/`
- `openrouter_client.py`
  - small OpenRouter chat-completions client
- `openrouter_runtime.py`
  - tiny real runtime path using prepared inputs and file tools
- `runtime_factory.py`
  - tiny runtime factory for live canary runs

Its job is to:

- prepare run context
- call the selected model runtime
- enforce artifact success rules
- record run-level usage and outcomes

This layer should remain replaceable. The node contract is the stable thing.
