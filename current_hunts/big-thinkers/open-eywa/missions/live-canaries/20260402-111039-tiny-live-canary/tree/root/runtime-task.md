# Runtime Task

- **Role:** synthesizer
- **Node root:** /Users/seanross/kingdom_of_god/home-base/.claude/worktrees/dual-runtime-provider/current_hunts/big-thinkers/open-eywa/missions/live-canaries/20260402-111039-tiny-live-canary/tree/root
- **Run ID:** run-003
- **Provider:** claude
- **Model:** (default)

## System Prompt

# Open-Eywa Synthesizer

You are the `synthesizer` role in Open-Eywa.

All child nodes of the current parent have completed. Your job is to read the plan, state, goal, and child outputs, then combine them into the parent's final result.

Write:

- `output/final-output.md`
- `output/state.md`

Your output must be self-contained and readable by the parent without any other file.

## Runtime Note

You are running as an Open-Eywa node via CLI. Use the file tools available in your environment to read and write files. All work must stay within the current node directory. Do not assume any tools beyond file operations are available.

## Prepared Context

```json
[
  {
    "available_sections": {
      "latest_child_report": {
        "json": {
          "child_node_id": "root.step-01-research-and-write-tcp-udp-differences",
          "child_node_path": "/Users/seanross/kingdom_of_god/home-base/.claude/worktrees/dual-runtime-provider/current_hunts/big-thinkers/open-eywa/missions/live-canaries/20260402-111039-tiny-live-canary/tree/root/children/step-01-research-and-write-tcp-udp-differences",
          "child_status": "finished",
          "failure_reason": null,
          "step_index": 0,
          "step_title": "research-and-write-tcp-udp-differences",
          "terminal_outcome": "completed"
        },
        "path": "system/latest-child-node-report.json"
      },
      "plan": {
        "path": "output/plan.md",
        "text": "## Plan\nStatus: draft\nReview: low\n\n### Step 1: research-and-write-tcp-udp-differences\nGoal: Research three key differences between TCP and UDP protocols and write the findings to output/final-output.md. Cover these three differences: (1) connection model \u2014 TCP is connection-oriented (three-way handshake) vs UDP is connectionless; (2) reliability and ordering \u2014 TCP guarantees delivery and in-order delivery, UDP does not; (3) speed and overhead tradeoffs \u2014 TCP has higher overhead due to its reliability mechanisms, UDP is faster and lower-overhead, making it suitable for real-time applications. Write clear, accurate prose with concrete examples where helpful. The file output/final-output.md must exist and contain all three differences when the step is complete.\nComplexity: 2\nImportance: 9\nDependencies: none\nIndependent: yes\nConfidence: high\nVerifiable: yes\n"
      },
      "progression_state": {
        "json": {
          "current_step_index": 1,
          "steps": [
            {
              "child_name": "step-01-research-and-write-tcp-udp-differences",
              "goal": "Research three key differences between TCP and UDP protocols and write the findings to output/final-output.md. Cover these three differences: (1) connection model \u2014 TCP is connection-oriented (three-way handshake) vs UDP is connectionless; (2) reliability and ordering \u2014 TCP guarantees delivery and in-order delivery, UDP does not; (3) speed and overhead tradeoffs \u2014 TCP has higher overhead due to its reliability mechanisms, UDP is faster and lower-overhead, making it suitable for real-time applications. Write clear, accurate prose with concrete examples where helpful. The file output/final-output.md must exist and contain all three differences when the step is complete.",
              "index": 0,
              "latest_child_status": "finished",
              "latest_failure_reason": null,
              "latest_terminal_outcome": "completed",
              "title": "research-and-write-tcp-udp-differences"
            }
          ]
        },
        "path": "system/progression-state.json"
      },
      "state": {
        "path": "output/state.md",
        "text": "# Mid-Plan Evaluator State\n\n## Decision\n\n**continue** \u2014 the single-step plan completed successfully. No remaining steps.\n\n## Evaluation\n\nStep 1 (`research-and-write-tcp-udp-differences`) finished with terminal outcome `completed`. The child produced `output/final-output.md` covering all three required differences:\n\n1. **Connection model** \u2014 TCP three-way handshake vs UDP connectionless datagrams \u2713\n2. **Reliability and ordering** \u2014 TCP sequence numbers, ACKs, retransmission vs UDP no guarantees \u2713\n3. **Speed and overhead tradeoffs** \u2014 TCP header/state/congestion overhead vs UDP 8-byte header, lower latency \u2713\n\nThe output is accurate, thorough, and meets the mission goal. No replanning needed. No escalation warranted.\n\n## Plan Status\n\nThe plan had one step. That step is done. The orchestrator should proceed to finalize this node.\n"
      }
    },
    "children": [
      {
        "child_name": "step-01-research-and-write-tcp-udp-differences",
        "failure_reason": null,
        "final_output_path": "children/step-01-research-and-write-tcp-udp-differences/output/final-output.md",
        "final_output_text": "# Three Key Differences Between TCP and UDP\n\n## 1. Connection Model\n\n**TCP (Transmission Control Protocol)** is connection-oriented. Before any data is exchanged, the two endpoints must complete a **three-way handshake**:\n\n1. Client sends `SYN`\n2. Server replies with `SYN-ACK`\n3. Client sends `ACK`\n\nOnly after this handshake is the connection established and data transfer begins. At the end of a session, a four-step teardown (`FIN` / `FIN-ACK` / `ACK`) closes the connection cleanly.\n\n**UDP (User Datagram Protocol)** is connectionless. A sender simply fires a datagram at the destination address with no prior coordination. There is no handshake, no session state, and no teardown. Each datagram is independent.\n\n**Concrete example:** Loading a web page uses TCP (HTTP/1.1 or HTTP/2). A DNS lookup uses UDP \u2014 the client fires a single query packet; the server fires a single response packet, with no connection setup required.\n\n---\n\n## 2. Reliability and Ordering\n\nTCP guarantees **reliable, in-order delivery**:\n\n- Every segment is assigned a sequence number.\n- The receiver sends cumulative acknowledgements (`ACK`).\n- If a segment is lost or arrives corrupted (fails checksum), the sender retransmits it.\n- Out-of-order segments are held in a reorder buffer until the gap is filled, so the application always reads data in the original order.\n\nUDP provides **no delivery guarantees and no ordering**:\n\n- Datagrams may be dropped silently (e.g., by a congested router).\n- Datagrams may arrive out of order or duplicated.\n- UDP has a checksum field, but on many platforms it is optional (IPv4) or the stack may still deliver a corrupted datagram to the application.\n- There is no acknowledgement or retransmission mechanism at the transport layer.\n\n**Concrete example:** A file download over TCP (FTP, HTTP) will always produce an exact byte-for-byte copy of the source. A video stream over UDP (many live-streaming and IPTV protocols) may drop frames under congestion \u2014 the video may stutter, but playback continues without waiting for retransmission.\n\n---\n\n## 3. Speed and Overhead Tradeoffs\n\nThe reliability mechanisms of TCP come at a cost:\n\n| Factor | TCP | UDP |\n|---|---|---|\n| Header size | 20\u201360 bytes | 8 bytes (fixed) |\n| Per-segment overhead | ACK round trip, sequence tracking, congestion window | None |\n| Latency | Higher \u2014 must wait for ACKs; head-of-line blocking on loss | Lower \u2014 no waiting |\n| Throughput on lossy links | Reduced by retransmissions and congestion control | Unaffected at transport layer |\n| CPU / state | Connection state, send/receive buffers, timers per connection | Stateless; minimal kernel overhead |\n\nTCP's congestion control algorithms (CUBIC, BBR, etc.) also throttle the sender when packet loss is detected, further reducing throughput on lossy or high-latency links.\n\nUDP sacrifices reliability for **lower latency and lower overhead**, making it well-suited for:\n\n- **Real-time audio/video** (VoIP, video conferencing, live streaming) \u2014 a slightly degraded frame is preferable to a frozen call waiting for retransmission.\n- **Online games** \u2014 position updates are time-sensitive; a stale retransmitted position is worse than no update.\n- **DNS, NTP, DHCP** \u2014 single-request/single-response protocols where the application can retransmit the whole query if no answer arrives.\n- **QUIC (HTTP/3)** \u2014 a modern protocol built on UDP that reimplements selective reliability and multiplexing in user space, avoiding TCP's head-of-line blocking.\n\n**Concrete example:** A VoIP call (e.g., using RTP over UDP) sends ~50 packets per second. If one is lost, the codec generates a brief audio glitch (often imperceptible) and continues. If the same call used TCP, losing a packet would stall all subsequent audio until the retransmission arrived \u2014 a far worse user experience.\n",
        "has_escalation": false,
        "has_final_output": true,
        "path": "children/step-01-research-and-write-tcp-udp-differences",
        "status": "finished",
        "terminal_outcome": "completed"
      }
    ],
    "focus_sections": [
      "task_source",
      "plan",
      "state",
      "children",
      "progression_state"
    ],
    "node": {
      "agent_mode": "synthesizer",
      "path": "/Users/seanross/kingdom_of_god/home-base/.claude/worktrees/dual-runtime-provider/current_hunts/big-thinkers/open-eywa/missions/live-canaries/20260402-111039-tiny-live-canary/tree/root",
      "status": "active"
    },
    "progression": {
      "cancellation_reason": null,
      "failure_reason": null,
      "next_action_after_child_report": null,
      "terminal_outcome": null,
      "waiting_on_computation_note": null
    },
    "role": "synthesizer",
    "task_source": {
      "path": "input/goal.md",
      "task_source_name": "goal",
      "text": "Research and explain three key differences between TCP and UDP protocols. Write your findings to output/final-output.md.\n"
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
