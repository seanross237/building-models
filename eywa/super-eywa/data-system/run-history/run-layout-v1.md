# Run Layout V1

## Purpose

This doc defines the intended v1 on-disk layout for preserved Super-Eywa run truth.

It connects the Eywa contracts to a concrete storage shape.

The goal is:

- preserve canonical truth on disk
- keep the layout easy for humans to browse
- keep the layout easy for later derived views and database ingestion

## Top-Level Run Layout

Each run should live in its own folder.

Example:

```text
run-history/
  run_2026_04_04_001/
    run_packet.json
    run_summary.json
    nodes/
    events/
    replay/
    derived/
```

## Required Run-Level Files

### `run_packet.json`

This is the canonical run setup packet.

It should follow:

- `eywa-system/contracts/run-packet-contract.md`

### `run_summary.json`

This is a small derived summary of the run as a whole.

For v1, it should preserve:

- `run_id`
- `root_node_id`
- `status`
- `node_count`
- `final_result_refs`
- `total_tokens`
- `total_cost_usd`
- `total_wall_time_ms`

This is not the source of truth.

It is a convenience layer.

## Node Layout

Each node run should live under `nodes/`.

Example:

```text
run_2026_04_04_001/
  nodes/
    node_root/
      events.jsonl
      edges.json
      node_packet.json
      node_record.json
    node_helper_backend/
      events.jsonl
      edges.json
      node_packet.json
      node_record.json
```

### `node_packet.json`

This should follow:

- `eywa-system/contracts/node-packet-contract.md`

### `node_record.json`

This should follow:

- `eywa-system/contracts/node-record-contract.md`

## Events Layout

Run-level events should live under:

```text
events/
  run-events.jsonl
```

For the current v1 implementation:

- a central run-level event log lives in `events/run-events.jsonl`
- node-local event and edge logs live beside each node record

The important thing is that the node record can point to them cleanly.

## Replay Layout

Heavier replay artifacts should live under:

```text
replay/
  node_root/
    raw-model.json
    tool-transcript.jsonl
    prompt-snapshot.json
  node_helper_backend/
    raw-model.json
```

This keeps replay material separate from the calm readable node record layer.

## Derived Layout

Convenience views generated from canonical truth should live under:

```text
derived/
  timeline.json
  simple-run-row.json
```

Examples:

- the timeline/story view for a run
- the simplified run-level row used for comparison

This is derived material, not the source of truth.

## Example Full Layout

```text
run-history/
  run_2026_04_04_001/
    run_packet.json
    run_summary.json
    nodes/
      node_root/
        events.jsonl
        edges.json
        node_packet.json
        node_record.json
      node_helper_backend/
        events.jsonl
        edges.json
        node_packet.json
        node_record.json
    events/
      run-events.jsonl
    replay/
      node_root/
        raw-model.json
        tool-transcript.jsonl
      node_helper_backend/
        raw-model.json
    derived/
      timeline.json
      simple-run-row.json
```

## Notes

- canonical truth lives in:
  - `run_packet.json`
  - `nodes/*/node_packet.json`
  - `nodes/*/node_record.json`
  - replay artifacts
- `run_summary.json` and `derived/` are convenience layers
- this layout is designed to be easy to ingest into later DB tables
