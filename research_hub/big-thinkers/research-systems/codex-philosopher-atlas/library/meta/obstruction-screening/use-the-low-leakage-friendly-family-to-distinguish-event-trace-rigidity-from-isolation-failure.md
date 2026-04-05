# Use The Low-Leakage Friendly Family To Distinguish Event-Trace Rigidity From Isolation Failure

When a behavior-based candidate is weaker than algebraic or leakage-based
candidates, the right friendly stress test is often the family where leakage
is already small but nonzero.

If the algebraic screen and the leakage screen both survive there while the
behavioral candidate remains ambiguous, the main bottleneck is usually exact
event-time trace rigidity rather than raw isolation.

That keeps the next repair step honest.
Repair the event-trace rule or evidence gap directly instead of spending a
later pass on leakage bookkeeping that the friendly low-leakage family has
already shown to be adequate.

Filed from:
- `missions/exact-ns-no-near-closed-tao-circuit/meta-inbox/meta-step-004-exploration-003.md`
