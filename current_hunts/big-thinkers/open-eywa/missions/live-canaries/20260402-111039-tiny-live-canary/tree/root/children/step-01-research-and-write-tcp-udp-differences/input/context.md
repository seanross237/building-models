## Parent Task
Research and explain three key differences between TCP and UDP protocols. Write your findings to output/final-output.md.

## Parent Plan
## Plan
Status: draft
Review: low

### Step 1: research-and-write-tcp-udp-differences
Goal: Research three key differences between TCP and UDP protocols and write the findings to output/final-output.md. Cover these three differences: (1) connection model — TCP is connection-oriented (three-way handshake) vs UDP is connectionless; (2) reliability and ordering — TCP guarantees delivery and in-order delivery, UDP does not; (3) speed and overhead tradeoffs — TCP has higher overhead due to its reliability mechanisms, UDP is faster and lower-overhead, making it suitable for real-time applications. Write clear, accurate prose with concrete examples where helpful. The file output/final-output.md must exist and contain all three differences when the step is complete.
Complexity: 2
Importance: 9
Dependencies: none
Independent: yes
Confidence: high
Verifiable: yes

## Parent State
# Planner State

## Decision

This task could be executed directly by a single worker. The topic (TCP vs UDP) is well-understood, the three differences to cover are well-defined, and the output destination is explicit. No discovery or multi-branch exploration is needed.

Despite this, the smallest honest plan that allows the orchestrator to route correctly is a single worker step. That is what the plan reflects.

## Reasoning

The task is self-contained:
- The domain knowledge (TCP/UDP protocol differences) is stable and not subject to discovery
- The three areas to cover are implicit in the task but can be made explicit in the goal
- One focused agent can research and write the output in a single session

Decomposition into separate "research" and "write" steps would be artificial — the research is trivial and does not gate the writing in any meaningful way.

## Scoring Rationale

- Complexity: 2 — straightforward lookup of well-known protocol properties
- Importance: 9 — this is the sole deliverable of the mission; if it fails, the mission fails

Adjusted C × I = 18, which routes to `worker` as expected.

## Alternatives Considered

- Two steps (research + write): rejected as artificial over-split; the research is trivial and inline with writing
- Three steps (one per difference): rejected as extreme over-split with no benefit

## Uncertainty

None meaningful. The topic is stable, the success criterion is concrete (file exists with three differences explained), and the routing is clear.
