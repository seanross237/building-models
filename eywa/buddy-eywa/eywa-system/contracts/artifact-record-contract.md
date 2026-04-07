# Artifact Record Contract

## Purpose

An `artifact_record` is the metadata sidecar for one artifact in a run.

An artifact is a piece of content (file, document, code, data) too large or too structural to pass through Buddy's context window. Artifacts live in a per-run artifact store and are first-class objects that workers create and consume.

Every artifact has two views: Buddy sees a summary card in his per-turn inventory; workers see the actual content loaded into their prompts on demand. Buddy reasons strategically over a manifest of what exists, and workers operate on the real bytes only when they need them. This separation is load-bearing for keeping Buddy's context window sane as artifacts accumulate over a run.

## Required Fields

- `contract_name`
  - always `artifact_record`
- `contract_version`
  - starting at `v1`
- `artifact_id`
- `title`
- `type`
- `created_by_node_id`
- `created_at_utc`
- `version`
- `supersedes`
- `summary`
- `content_ref`
- `content_size_bytes`

## Field Details

### `artifact_id`

Unique within a run. Format `art_NNNN` (see ID generation section).

### `title`

Short human-readable name (e.g., "Plan for task X").

### `type`

One of the allowed artifact types. Drives how the artifact is rendered into a worker's prompt when referenced.

Allowed values for v1:

- `text_markdown` — plans, reports, briefs
- `text_plain` — logs, simple notes
- `code_python`, `code_js`, `code_typescript`, `code_rust`, etc. — source files
- `data_json` — structured findings, compiled research, parsed data
- `data_csv` — tabular data
- `image_png`, `image_jpg` — diagrams and screenshots (referenced by path only, never inlined into prompts)

### `created_by_node_id`

The node that authored this artifact.

### `version`

Integer, starts at `1`. Incremented when this artifact supersedes a prior version.

### `supersedes`

The `artifact_id` of the prior version this replaces, or `null` if this is the first version.

### `summary`

One-line hook Buddy sees in the artifact inventory view of his per-turn prompt.

### `content_ref`

Relative path (from `run_dir/artifacts/`) to the raw content file.

### `content_size_bytes`

Integer size of the content file.

## Immutability and Supersedes Chains

Artifacts are immutable. Modifying an artifact produces a new artifact with `supersedes` pointing to the prior version.

Both versions exist on disk forever. "Latest version" is a derived view computed by walking `supersedes` pointers.

Immutability avoids write conflicts (multiple workers never race on the same file), preserves debugging history, and makes replay deterministic.

## Artifact ID Generation

Format: `art_NNNN`, where `NNNN` is a 4-digit zero-padded monotonic counter scoped to the run.

The first artifact in a run is `art_0001`, the second is `art_0002`, and so on.

## On Disk

Layout of `run_dir/artifacts/`:

- `art_NNNN_<slugified_title>.<ext>` — raw content file (extension determined by `type`)
- `art_NNNN_<slugified_title>.metadata.json` — the `artifact_record` sidecar
- `manifest.json` — denormalized inventory for the whole run

## Manifest Shape

`manifest.json` lives at the top of `run_dir/artifacts/`. It is the denormalized index Buddy reads from when surfacing the inventory in his per-turn prompt.

Required fields:

- `contract_name`
  - always `artifact_manifest`
- `contract_version`
  - starting at `v1`
- `run_id`
- `artifacts`
  - list of summary entries, one per artifact, each containing:
    - `artifact_id`
    - `title`
    - `type`
    - `summary`
    - `version`
    - `supersedes`
    - `created_by_node_id`
    - `content_ref`
- `updated_at_utc`

The manifest is updated atomically whenever an artifact is created or superseded.

## Example Shape

### `artifact_record` (single artifact sidecar)

```json
{
  "contract_name": "artifact_record",
  "contract_version": "v1",
  "artifact_id": "art_0001",
  "title": "Plan for task X",
  "type": "text_markdown",
  "created_by_node_id": "node_root__t1__sg1__planner",
  "created_at_utc": "2026-04-07T15:30:00Z",
  "version": 1,
  "supersedes": null,
  "summary": "3-step plan: research A, implement B, test C",
  "content_ref": "art_0001_plan_for_task_x.md",
  "content_size_bytes": 4821
}
```

### `manifest.json`

```json
{
  "contract_name": "artifact_manifest",
  "contract_version": "v1",
  "run_id": "run_2026_04_07_001",
  "artifacts": [
    {
      "artifact_id": "art_0001",
      "title": "Plan for task X",
      "type": "text_markdown",
      "summary": "3-step plan: research A, implement B, test C",
      "version": 1,
      "supersedes": null,
      "created_by_node_id": "node_root__t1__sg1__planner",
      "content_ref": "art_0001_plan_for_task_x.md"
    },
    {
      "artifact_id": "art_0002",
      "title": "Research findings on quantum history",
      "type": "data_json",
      "summary": "12 papers on quantum computing history",
      "version": 1,
      "supersedes": null,
      "created_by_node_id": "node_root__t2__sg2__researcher",
      "content_ref": "art_0002_research_findings_on_quantum_history.json"
    },
    {
      "artifact_id": "art_0004",
      "title": "Plan for task X",
      "type": "text_markdown",
      "summary": "Revised 3-step plan after worker 2 failure",
      "version": 2,
      "supersedes": "art_0001",
      "created_by_node_id": "node_root__t3__sg3__planner",
      "content_ref": "art_0004_plan_for_task_x.md"
    }
  ],
  "updated_at_utc": "2026-04-07T16:05:00Z"
}
```

## Validation Rules

- `artifact_id` must be unique within a run
- if `supersedes` is non-null, that prior `artifact_id` must exist in the same run
- `content_ref` must resolve to a real file under `run_dir/artifacts/`
- `content_size_bytes` must match the actual file size
- `version` = 1 implies `supersedes: null`; `version` > 1 implies `supersedes` is non-null

## Notes

- v1 inlines artifact content into worker prompts at materialization time. v2 will introduce tool-based reads (workers read artifacts on demand), which will only change the worker-side read mechanism — Buddy's summary view stays identical.
- the artifact-usage learning surface (Section 11) records one row per artifact read event, so richly-used artifacts are visible in the learning data
- the manifest is denormalized on purpose: Buddy's per-turn prompt loads from it directly, without walking individual sidecars
