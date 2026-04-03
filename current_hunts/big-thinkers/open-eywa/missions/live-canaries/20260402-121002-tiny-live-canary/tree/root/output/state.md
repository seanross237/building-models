status: completed
role: worker
run_id: run-001
task: "Write a short operator note explaining what Open-Eywa is, why the node is the durable unit of work, and which mission files a human should inspect first."
input_context_present: false
inputs_read:
  - runtime-task.md
  - input/goal.md
  - system/runs/run-001/prepared-node-context.json
  - system/runs/run-001/request.json
  - system/events.jsonl
artifacts_written:
  - output/final-output.md
  - output/state.md
escalation_written: false
