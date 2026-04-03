# Runtime Task

- **Role:** worker
- **Node root:** /Users/seanross/kingdom_of_god/home-base/.claude/worktrees/dual-runtime-provider/current_hunts/big-thinkers/open-eywa/missions/live-canaries/20260402-111039-tiny-live-canary/tree/root/children/step-01-research-and-write-tcp-udp-differences
- **Run ID:** run-001
- **Provider:** claude
- **Model:** (default)

## System Prompt

# Open-Eywa Worker

You are the `worker` role in Open-Eywa.

You are an execution-focused node. Your job is to do the task directly instead of decomposing it further.

Read your instructions and use the available local tools when they help. Open-Eywa gives you named tools for filesystem access, shell execution, Python, Sage, Lean, and background jobs.

If `input/context.md` exists, read it. It may contain parent task context and prior completed-step results that your current task depends on.

Write:

- `output/final-output.md`
- `output/state.md`

If the task is fundamentally impossible or based on a false premise, write:

- `output/escalation.md`

## How to Work

- favor machine-checkable results over unsupported prose
- use Python for general numerical and symbolic work
- use Sage for heavier algebra, number theory, and combinatorics
- use Lean for formalization and proof checking
- if a computation will take too long for one active tool call, start a background job
- write your final output so the parent can understand it without any other file

## Constraints

- do not create child directories
- do not touch orchestrator-controlled status files
- keep reproducible artifacts and scratch work under your node's `system/` area

## Runtime Note

You are running as an Open-Eywa node via CLI. Use the file tools available in your environment to read and write files. All work must stay within the current node directory. Do not assume any tools beyond file operations are available.

## Prepared Context

```json
[
  {
    "available_sections": {
      "context": {
        "path": "input/context.md",
        "text": "## Parent Task\nResearch and explain three key differences between TCP and UDP protocols. Write your findings to output/final-output.md.\n\n## Parent Plan\n## Plan\nStatus: draft\nReview: low\n\n### Step 1: research-and-write-tcp-udp-differences\nGoal: Research three key differences between TCP and UDP protocols and write the findings to output/final-output.md. Cover these three differences: (1) connection model \u2014 TCP is connection-oriented (three-way handshake) vs UDP is connectionless; (2) reliability and ordering \u2014 TCP guarantees delivery and in-order delivery, UDP does not; (3) speed and overhead tradeoffs \u2014 TCP has higher overhead due to its reliability mechanisms, UDP is faster and lower-overhead, making it suitable for real-time applications. Write clear, accurate prose with concrete examples where helpful. The file output/final-output.md must exist and contain all three differences when the step is complete.\nComplexity: 2\nImportance: 9\nDependencies: none\nIndependent: yes\nConfidence: high\nVerifiable: yes\n\n## Parent State\n# Planner State\n\n## Decision\n\nThis task could be executed directly by a single worker. The topic (TCP vs UDP) is well-understood, the three differences to cover are well-defined, and the output destination is explicit. No discovery or multi-branch exploration is needed.\n\nDespite this, the smallest honest plan that allows the orchestrator to route correctly is a single worker step. That is what the plan reflects.\n\n## Reasoning\n\nThe task is self-contained:\n- The domain knowledge (TCP/UDP protocol differences) is stable and not subject to discovery\n- The three areas to cover are implicit in the task but can be made explicit in the goal\n- One focused agent can research and write the output in a single session\n\nDecomposition into separate \"research\" and \"write\" steps would be artificial \u2014 the research is trivial and does not gate the writing in any meaningful way.\n\n## Scoring Rationale\n\n- Complexity: 2 \u2014 straightforward lookup of well-known protocol properties\n- Importance: 9 \u2014 this is the sole deliverable of the mission; if it fails, the mission fails\n\nAdjusted C \u00d7 I = 18, which routes to `worker` as expected.\n\n## Alternatives Considered\n\n- Two steps (research + write): rejected as artificial over-split; the research is trivial and inline with writing\n- Three steps (one per difference): rejected as extreme over-split with no benefit\n\n## Uncertainty\n\nNone meaningful. The topic is stable, the success criterion is concrete (file exists with three differences explained), and the routing is clear.\n"
      }
    },
    "children": [],
    "focus_sections": [
      "task_source",
      "context",
      "retrieved_knowledge",
      "plan",
      "state"
    ],
    "node": {
      "agent_mode": "worker",
      "path": "/Users/seanross/kingdom_of_god/home-base/.claude/worktrees/dual-runtime-provider/current_hunts/big-thinkers/open-eywa/missions/live-canaries/20260402-111039-tiny-live-canary/tree/root/children/step-01-research-and-write-tcp-udp-differences",
      "status": "active"
    },
    "progression": {
      "cancellation_reason": null,
      "failure_reason": null,
      "next_action_after_child_report": null,
      "terminal_outcome": null,
      "waiting_on_computation_note": null
    },
    "role": "worker",
    "task_source": {
      "path": "input/parent-instructions.md",
      "task_source_name": "parent-instructions",
      "text": "Research three key differences between TCP and UDP protocols and write the findings to output/final-output.md. Cover these three differences: (1) connection model \u2014 TCP is connection-oriented (three-way handshake) vs UDP is connectionless; (2) reliability and ordering \u2014 TCP guarantees delivery and in-order delivery, UDP does not; (3) speed and overhead tradeoffs \u2014 TCP has higher overhead due to its reliability mechanisms, UDP is faster and lower-overhead, making it suitable for real-time applications. Write clear, accurate prose with concrete examples where helpful. The file output/final-output.md must exist and contain all three differences when the step is complete.\n"
    }
  }
]
```

## Instructions

1. Read and understand the system prompt and prepared context above.
2. Execute the role's task using the available file tools.
3. Write all required output artifacts under `output/` in this directory.
4. If the task is impossible under the node's assumptions, write `output/escalation.md`.
5. Do not write files outside the node boundary.
