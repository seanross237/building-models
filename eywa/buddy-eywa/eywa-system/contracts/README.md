# Contracts

## What contracts are

Contracts are buddy-eywa's authoring schemas. They describe the shapes of the files-on-disk and JSON objects that the runtime produces, validates, and preserves. They are the shared vocabulary between the runtime, replay, grading, and the learning surfaces — every other layer in buddy-eywa builds against the shapes defined here.

## What's in this folder

Ported from super-eywa in Step 2 (the unchanged starting shapes):

- `run-packet-contract.md` — frozen starting package for a whole run
- `node-packet-contract.md` — frozen starting package for one node run
- `node-output-contract.md` — runtime-compiled output of a node execution
- `node-record-contract.md` — canonical preserved record of a node run

Coming in Step 3 (new structural contracts for subgraphs and artifacts):

- `subgraph-type-contract.md` — schema for library subgraph type specs
- `subgraph-instance-contract.md` — schema for materialized subgraph instances
- `artifact-record-contract.md` — schema for artifact metadata and the manifest

Coming in Step 4 (split of the old node-authored response into two roles):

- `buddy-node-authored-response-contract.md` — what a Buddy host node is allowed to author
- `worker-node-authored-response-contract.md` — what a worker (single-turn) node is allowed to author

## How contracts relate to the rest of the system

- The runtime validates authored JSON against the response contracts before acting on it.
- Node packets, node records, and node outputs are preserved to disk for replay and analysis.
- The learning surfaces (buddy-turns, slot-executions, artifact-usages) are derived from these records — the shapes here are what those derivations stand on.

## Versioning

Contracts are versioned via the `contract_version` field. Buddy-eywa starts every contract at `v1`. Breaking changes bump the version. Compatible extensions are documented in a "Planned Buddy-Eywa Extensions" section at the bottom of the relevant contract until they actually land in code.

## Database sync

When records conforming to these contracts get synced to Supabase, buddy-eywa writes to tables prefixed `be_*` (e.g., `be_runs`, `be_nodes`, `be_buddy_turns`). This keeps buddy-eywa's data fully separate from super-eywa's tables. The Supabase sync layer lives in `../../data-system/` and lands in Section 11.

## Pointers

- [`../../design-docs/`](../../design-docs/) — vision, subgraph types, buddy loop, workers, artifacts, learning surfaces, and the rest of the buddy-eywa design (moved here in Step 6)
- [`../../SYSTEM-OVERVIEW.md`](../../SYSTEM-OVERVIEW.md) — top-level orientation for the whole system (lands in Step 5)
