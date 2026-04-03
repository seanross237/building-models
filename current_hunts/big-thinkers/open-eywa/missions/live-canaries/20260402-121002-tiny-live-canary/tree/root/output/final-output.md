# Operator Note

Open-Eywa is a mission-oriented execution system that runs work as durable on-disk nodes. Each node carries its own task statement, prepared runtime context, event trail, and produced artifacts, so the work can be inspected and understood from the node directory itself instead of from a transient process.

The node is the durable unit of work because the directory persists the full handoff surface:

- the requested task in `input/goal.md`
- the role contract and constraints in `runtime-task.md`
- the prepared run context in `system/runs/run-001/prepared-node-context.json`
- the run metadata in `system/runs/run-001/request.json`
- the event history in `system/events.jsonl`
- the produced results under `output/`

That structure survives process exit, restart, or provider changes. A human or orchestrator can revisit the same node later and still recover what was asked, what context was provided, and what result was produced.

Inspect these mission files first:

1. `input/goal.md` - the operator-facing task to complete.
2. `runtime-task.md` - the worker contract, constraints, and required artifacts.
3. `system/runs/run-001/prepared-node-context.json` - the exact context prepared for this run.
4. `system/runs/run-001/request.json` - mission, node, and run identifiers.
5. `system/events.jsonl` - the durable event log for status and run lifecycle.
