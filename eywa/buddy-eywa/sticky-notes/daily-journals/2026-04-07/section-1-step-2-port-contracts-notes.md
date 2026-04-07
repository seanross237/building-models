# Section 1, Step 2 — Port 4 Unchanged Contracts (notes)

## What I ported

- Faithful copies of `run-packet`, `node-packet`, `node-output`, and `node-record` from super-eywa into `buddy-eywa/eywa-system/contracts/`.
- Wrote `buddy-eywa/eywa-system/contracts/README.md` from scratch (44 lines), since the super-eywa README was a thin pre-existing stub that didn't cover the points the spec asked for.

## Judgment calls

- **Prose replacements were narrow.** I only swapped "Eywa" / "super-eywa" → "Buddy-Eywa" / "buddy-eywa" where the prose was clearly talking about *which system this contract belongs to*. The super-eywa source files almost never said "super-eywa" in body text — only one file (`run-packet-contract.md` purpose line) needed it. Everything else stayed identical.
- **Example values left as-is.** `run_2026_04_04_001`, `gpt-5.4`, the agent-orchestration prompt profile names, etc. — kept verbatim. They're illustrative and the spec said they could stay.
- **`node-output` notes line cleanup.** The super-eywa note pointed at `node-authored-response-contract.md` (the file we're explicitly NOT porting). I changed that single line to refer to "the worker-node or buddy-node authored response contracts" since those are what'll exist by end of Section 1. This felt necessary to avoid leaving a dangling pointer to a file that won't exist in buddy-eywa. Flagging it because it's the only place I touched a body sentence beyond the prose-replacement rule.
- **"Planned Buddy-Eywa Extensions" placement.** Put them at the very bottom of `node-packet` and `node-record`, after the existing `## Notes` section, as a top-level `##` heading. This keeps the original Notes section unchanged and makes the extensions section easy to find / strip when fields actually land.
- **"No additions planned" footer style.** Used a horizontal rule + blockquote for `run-packet` and `node-output`, so the footer is visually distinct from the original content but doesn't add a new heading that could be mistaken for a real contract section.
- **README structure.** Used the section ordering from the spec (what contracts are → what's in folder → relationship → versioning → DB sync → pointers). Used relative links for both pointers (`../../design-docs/`, `../../SYSTEM-OVERVIEW.md`) per the spec, even though both targets don't exist yet — Steps 5 and 6 create them.
- **README listing of upcoming contracts.** Used the *eventual* contract filenames (e.g. `subgraph-type-contract.md`, `buddy-node-authored-response-contract.md`) as my best guess at what Steps 3 and 4 will produce. If those steps pick different names, this list will need a tiny update.

## Uncertainties / things to revisit

- Are the contract filenames I assumed for Steps 3 and 4 (`subgraph-type-contract.md`, `subgraph-instance-contract.md`, `artifact-record-contract.md`, `buddy-node-authored-response-contract.md`, `worker-node-authored-response-contract.md`) the names Sean actually wants? They're not load-bearing but the README lists them.
- The "Planned Buddy-Eywa Extensions" wording — I described `inputs_from` and `subgraph_instance_id` as nested under `node_setup`. The spec literally said `node_setup.inputs_from` so I followed that, but `inputs_from` could plausibly live at the top level of `node_packet` instead. Worth confirming when Section 6 starts.
- The README's database sync section names tables `be_runs`, `be_nodes`, `be_buddy_turns` as examples. The spec gave those as examples too, but the actual table names will be locked down in Section 11.

## Things that seemed off in the super-eywa contracts (worth flagging)

- `node-output-contract.md` line 127 references `node-authored-response-contract.md`, which is being split / replaced. Buddy-eywa avoids that dangling pointer (see judgment call above), but the super-eywa file itself will go stale once super-eywa makes equivalent changes — minor cleanup item for super-eywa.
- `node-record-contract.md`'s `orchestration.initial_decision` / `final_decision` allowed values are `execute_locally` / `delegate` / `report_problem`, but `final_action_type` allows the wider set including `local_attempt`, `local_replan`, `recruit_help`, `report_success`. The two enums are subtly different and there's no explanation of how they map. Not buddy-eywa's problem to fix today, but it's a confusing inconsistency a future reader will trip on.
- `node-packet-contract.md`'s example shows `routing_policy: "return_to_creator"` inside `resolved_variables`, but `routing_policy` isn't listed anywhere in the field details. Same for `node-record-contract.md`. Tiny doc gap, not a structural problem.
- The super-eywa `contracts/README.md` is a 22-line stub — much thinner than what the spec asked buddy-eywa's README to be. I wrote buddy-eywa's from scratch rather than porting it, since porting wouldn't have hit any of the required content points.
