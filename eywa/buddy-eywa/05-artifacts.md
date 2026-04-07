# 05 — Artifacts

## The problem

Agents working on real tasks produce content that is:

- Too large to pass through Buddy's context window (a 500-line document, a code file, a research compilation)
- Structurally important enough that other agents need to read or modify it, not just summarize it
- Worth preserving after the host that produced it has moved on

Buddy is the strategic brain; he cannot and should not be the data carrier for every intermediate output. We need a first-class substrate for passing around content that is too big, too structural, or too persistent to live in conversation context.

## The core idea: two views of every artifact

Every artifact has two representations that are visible in different places:

- **Buddy's view** — a **summary card**: `{artifact_id, title, type, created_by, one-line summary, latest_version}`. Tiny, context-friendly, lets Buddy reason about what artifacts exist and what they're for without loading their actual content.
- **Worker's view** — the **actual content**, loaded into the worker's `rendered_prompt` only when the slot's `meta_prompt` references a buddy-bound variable that Buddy has resolved to that artifact via `context_bindings`.

This split is the artifact-world equivalent of the Buddy/Worker strategic/tactical split: Buddy reasons over a manifest of what exists, workers operate on the real bytes when they need them.

## Where artifacts live on disk

```
run_dir/
  artifacts/
    art_0001_plan_v1.md                      ← raw content
    art_0001_plan_v1.metadata.json           ← summary card
    art_0002_research_findings.json          ← raw content
    art_0002_research_findings.metadata.json ← summary card
    art_0003_code_draft_v1.py
    art_0003_code_draft_v1.metadata.json
    manifest.json                             ← full inventory for the run
```

Each artifact is a pair: the raw file plus a metadata sidecar. The `manifest.json` at the top of the folder is a denormalized index of everything, updated when artifacts are created or superseded.

## Metadata schema

```json
{
  "contract_name": "artifact_record",
  "contract_version": "v1",
  "artifact_id": "art_0001",
  "title": "Plan for task X",
  "type": "text_markdown",
  "created_by_node_id": "host_root__turn_1__slot_planner",
  "created_at_utc": "2026-04-07T15:30:00Z",
  "version": 1,
  "supersedes": null,
  "summary": "3-step plan: research A, implement B, test C",
  "content_ref": "art_0001_plan_v1.md",
  "content_size_bytes": 4821
}
```

The summary is the one-line hook Buddy sees. The content_ref is a relative path to the raw content file.

## Common artifact types

- `text_markdown` — plans, reports, briefs
- `text_plain` — logs, simple notes
- `code_python`, `code_js`, etc. — executable or editable source files
- `data_json` — structured findings, compiled research, parsed data
- `data_csv` — tabular data
- `image_png`, `image_jpg` — diagrams, screenshots (referenced by path only, not inlined into prompts)

The type field drives how the artifact is rendered into a worker's prompt when referenced.

## How workers create artifacts

A worker's authored response includes an `artifacts_created` list:

```json
{
  "output": "Plan drafted. Full plan is in artifact art_0001.",
  "output_summary": "Drafted the 3-step plan",
  "artifacts_created": [
    {
      "title": "Plan for task X",
      "type": "text_markdown",
      "content": "# Plan for task X\n\n## Step 1...\n## Step 2...",
      "summary": "3-step plan: research A, implement B, test C"
    }
  ],
  "fail_fast": { "triggered": false }
}
```

The engine:
1. Generates an `artifact_id`
2. Writes the content to `run_dir/artifacts/<id>_<slugified_title>.<ext>`
3. Writes the metadata sidecar
4. Appends the entry to `manifest.json`
5. Surfaces the new entry in the next-turn Buddy context

From the moment a worker authors an `artifacts_created` entry, the artifact exists in the run's artifact inventory and is visible to future Buddy turns.

## How workers read artifacts

Artifacts flow into workers via `context_bindings` on Buddy's authored response, never via per-slot instructions Buddy writes. The path is:

1. The Scientist authors a subgraph type whose slot `meta_prompt`s contain buddy-bound template variables like `{plan}` or `{review}`. Each one stands for an artifact (or other context value) that Buddy will resolve at pick time.
2. When Buddy picks the type, his `pick_subgraph` response includes a `context_bindings` map with one entry per buddy-bound variable. An artifact entry uses `binding_type: "artifact"` and an `artifact_id` from the run's manifest:

```json
{
  "turn_decision": "pick_subgraph",
  "chosen_subgraph_type": "revise_plan_given_review",
  "context_bindings": {
    "plan": {
      "binding_type": "artifact",
      "artifact_id": "art_0001"
    },
    "review": {
      "binding_type": "artifact",
      "artifact_id": "art_0003"
    }
  },
  "variable_overrides": {}
}
```

3. At materialization time the runtime walks every slot's `meta_prompt`, finds each buddy-bound variable token, looks the referenced artifact up in `manifest.json`, loads its content, and substitutes a rendered view of that content into the prompt body in place of the `{plan}` / `{review}` token.
4. The substituted text lands in `slots_resolved[<slot_label>].rendered_prompt`. That field is exactly what the worker sees — meta prompt skeleton + inlined artifact content, already assembled.

For a `text_markdown` artifact the rendered view is the raw markdown body; for `data_json` it is the JSON serialized into the prompt; for `image_*` types only the path is referenced. The type field on the artifact record drives the per-type rendering rule.

Bindings are flat across the whole instance — every slot in the same instance shares the same `context_bindings`, so two slots that both reference `{plan}` resolve to the same artifact. The worker gets the real content inlined; Buddy never does.

## Modifying artifacts — immutability and versioning

Artifacts are **immutable**. A worker that wants to "modify" `art_0001` produces a new artifact with `supersedes: "art_0001"`:

```json
{
  "artifacts_created": [
    {
      "title": "Plan for task X",
      "type": "text_markdown",
      "content": "# Plan for task X (revised)...",
      "summary": "Revised 3-step plan after worker 2 failure",
      "supersedes": "art_0001"
    }
  ]
}
```

This gets written as `art_0004` (or whatever the next ID is) with metadata pointing back to `art_0001`. Both versions exist on disk forever. The manifest's summary view surfaces the latest version by default but can show history on request.

Immutability wins here because:
- It avoids write conflicts entirely (multiple workers never race on the same file)
- It preserves complete history for the Scientist to study
- "Latest version" is a derived view, trivially computable from `supersedes` pointers
- Debugging and replay are deterministic

## Scoping — simple in v1

All artifacts created anywhere in a run live in the same `run_dir/artifacts/` store and are **globally visible within that run**. No per-host scopes, no sibling isolation. A nested host at depth 3 can reference an artifact created at depth 0, and vice versa.

This is the simple choice and it's almost certainly correct for v1. If later you notice a specific need for tighter scoping ("this subgraph's intermediate artifacts shouldn't be visible to its siblings"), you add it as a variable on the subgraph type, not as a structural rule. Don't pre-build scoping machinery before a real need shows up.

## What Buddy sees in each turn

Every Buddy turn's prompt includes an artifact inventory block:

```
ARTIFACT INVENTORY:
- art_0001  (text_markdown)  "3-step plan: research A, implement B, test C"
- art_0002  (data_json)      "12 papers on quantum computing history"
- art_0003  (code_python)    "Initial implementation of step 1"
- art_0004  (text_markdown)  "Revised 3-step plan after worker 2 failure"  [supersedes art_0001]
```

Buddy reasons over this catalog when deciding which subgraph type to pick next and which artifacts to bind to that type's buddy-bound variables. Any of these IDs can land in `context_bindings` as an `artifact` binding, and the engine handles loading the actual content into each affected slot's `rendered_prompt`.

## Tool-based reads (v2)

For v1, artifact content is inlined into worker prompts at materialization time. This is simple but can bloat prompts when workers reference many large artifacts.

For v2, workers get an explicit `read_artifact(artifact_id)` tool and load content on demand. This requires tool-use support in the worker execution path and is a clean migration because the Buddy-side summary view stays identical — only the worker's read mechanism changes.

## Artifacts as a third learning surface

Artifact data becomes a third table the Scientist can study:

```
(artifact_id, created_by_slot_role, created_by_subgraph_type, used_by_slot_role,
 used_by_subgraph_type, downstream_run_score)
```

Questions this surface can answer:

- "Artifacts created by `researcher` slots score highest when consumed by `planner` slots, not `executor` slots. Does that suggest a better default type?"
- "Plans written as markdown score higher than plans written as JSON. Is that a formatting insight for the `planner` slot prompt profile?"
- "Code artifacts tend to get superseded once, then reach a stable version. Is there a way to shortcut the first attempt?"

The Scientist can use this surface independently of the buddy-turn and slot-execution tables, and the three together give a much richer picture of why runs succeed or fail than any one of them alone.

## What this adds to the bones

- One new contract: `artifact_record` (fields described above)
- One new worker output field: `artifacts_created`
- A new `artifact` binding kind on Buddy's `context_bindings` (so subgraph-type meta prompts can reference artifacts via buddy-bound variables)
- One new directory per run: `artifacts/`
- Engine logic for: writing artifacts on worker completion, resolving `artifact` bindings into the per-slot `rendered_prompt` at materialization time, maintaining the manifest, surfacing inventory in Buddy's prompt

That's the entire addition. It does not touch the Buddy/Worker/subgraph primitives — it's purely additive, a shared substrate they all use.
