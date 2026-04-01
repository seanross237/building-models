# Runtime

This directory will hold the rebuilt agent-run layer.

Its job will be to:

- prepare run context
- call the selected model runtime
- enforce artifact success rules
- record run-level usage and outcomes

This layer should remain replaceable. The node contract is the stable thing.
