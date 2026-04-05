# Adversarial Tests

This suite is the compact high-value "try to break it" layer.

Use it when you want a fast answer to:

- did this change make the system less sturdy?
- does the orchestrator still fail explicitly and safely?
- do ugly runtime outcomes stay contained?

This suite should stay:

- small
- high-signal
- mostly fixture-driven
- focused on important weird cases, not implementation trivia

Good additions here include:

- malformed control values
- missing required artifacts
- runtime failure modes
- tool boundary violations
- stale or contradictory node state
- mission-level failure handling

If a real bug is discovered and it is high-value, add a regression here when it belongs in the fast loop.
