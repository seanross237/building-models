# Section 1, Step 3 — Structural Contracts (Builder C notes)

## What I wrote

Three new contract files in `eywa-system/contracts/`:

- `subgraph-type-contract.md` — schema for the reusable DAG recipes Buddy picks from
- `subgraph-instance-contract.md` — schema for the materialized form created when Buddy picks a type
- `artifact-record-contract.md` — schema for the artifact metadata sidecar plus the per-run manifest

## Judgment calls

- **Subgraph type seed examples include the `contract_name` / `contract_version` fields even though `02-subgraph-types.md` shows them without those fields.** The design doc was illustrating the inner shape, but the contracts folder convention (set by Builder B's ports) is that every authored contract starts with `contract_name` and `contract_version`. I added them to the seed examples to keep the convention consistent.
- **`buddy_policy` on `slots_resolved` excludes `"inherit"`.** The type-level `buddy` field allows `"never" | "always" | "inherit"`, but `inherit` is a resolution rule, not a stored state. Once an instance is materialized the policy must be concrete, so I documented `buddy_policy` as `"never" | "always"` only.
- **`artifact_refs` lives on `slots_resolved`, not at the instance top level.** Buddy may point different slots at different artifacts in the same instance, so the references need per-slot granularity. Putting them top-level would lose that.
- **`edges` is denormalized into the instance record** rather than recomputed from the type spec each time tooling needs the DAG. The duplication is small and the convenience is worth it for the learning surfaces and replay tools.
- **`subgraph_instance_id` format is `sg_inst_<shorthash>_<runid>_<counter>`** where `shorthash` is the first 8 hex chars of `type_content_hash`. The spec called this out as a recommendation; I locked it in. Counter is monotonic per run.
- **Files inside `run_dir/subgraphs/<id>/`** include `type_content_hash.txt` as a separate bare-text file even though the hash is also inside `instance.json`. Greppability across many runs was worth the tiny duplication.
- **Artifact `manifest.json` got its own `contract_name` of `artifact_manifest`** even though it was not strictly required. It made the shape match the rest of the contracts folder convention and gives the loader something to validate against.
- **Manifest entries are explicitly denormalized copies of artifact-record fields, not pointers.** This matches the design doc's intent that Buddy reads only from the manifest at turn time, without walking individual sidecars.
- **Manifest example artifact ordering.** I used `art_0001`, `art_0002`, `art_0004` (skipping `art_0003`) to make the supersedes example feel realistic — the worker that revised the plan ran after `art_0003` was already created. Consistent with the design doc's `art_0004` example.
- **Slugified title in filenames is left informal.** I used lowercase + underscores in the example (`art_0001_plan_for_task_x.md`). The exact slugifier is a runtime concern, not a contract concern, so I did not pin it down.
- **`text_plain` and the various `code_*` types** are listed explicitly in the contract per the spec. I kept the "etc." language for additional code types so the list does not feel like a hard closed set, while still naming the v1 starters.

## Cross-references to design docs

No deviations from `02-subgraph-types.md` or `05-artifacts.md`.

The seed examples (`just_execute`, `delegate_fanout_synthesize`) match the design doc exactly except for the added `contract_name` / `contract_version` envelope (judgment call above) and the addition of an empty `variables: {}` on the lone `worker` slot of `just_execute` for parity with the other type.

The artifact field set, allowed `type` values, and immutability rules are a faithful pull from `05-artifacts.md`.

## Uncertainties / things to revisit

- **Counter scope on `subgraph_instance_id`.** I scoped the counter to the run. If nested hosts ever spawn instances in parallel across hosts in the same run, the counter needs to be process-safe (atomic across hosts). That is a runtime concern not a contract concern, but flagging it.
- **`buddy: "inherit"` resolution rule** is not specified anywhere yet. The contract just says it gets resolved at materialization time. The actual rule (probably "look at parent host's policy") needs to land in Section 6 when the engine gets built.
- **`artifact_id` collisions between superseded versions and the slugified filename.** If two different artifacts have the same title, the filename slugs collide and only the `art_NNNN_` prefix disambiguates them. Worth confirming the writer always prefixes correctly when Section 5 builds the artifact engine.
- **`spec_resolved.json` versus `instance.json`.** I documented both because the spec called for both, but they overlap. Future builders may want to collapse them. Left as-is for now to honor the spec.

## Consistency with Builder B's ports

Voice intentionally matches `node-packet-contract.md` and `node-record-contract.md`:

- Same heading order: `Purpose` → `Required Fields` → `Field Details` → `Example Shape` → `Notes`
- Same terse, structural tone — no salesmanship, no marketing words
- Same JSON code-fence style for examples
- Same convention of listing required fields as a flat bullet list at the top, then expanding each in `Field Details`
- Same lowercase-bullet style in the `Notes` section (e.g., "the instance is the atomic unit...")

Intentional divergences from Builder B:

- The new contracts have a `Validation Rules` section where the ported contracts do not. The validation surface for these new shapes is genuinely richer (DAG validity, supersedes integrity, content-hash equivalence), and burying those rules in prose would be worse than naming a section for them. I did not retro-add `Validation Rules` to the ported contracts — that's outside my scope.
- `subgraph-type-contract.md` has a `Content Hashing` section and `subgraph-instance-contract.md` has a `Subgraph Instance ID Generation` section. These do not exist in the ported contracts because the ported shapes do not need them.
- I did not add a `Planned Buddy-Eywa Extensions` section to any of the three contracts. The ported contracts have one because they were super-eywa shapes being extended later. These three are buddy-eywa-native from day one and have nothing pending — adding an empty section would be filler.

## What the next reviewer should pay attention to

- The `contract_name` / `contract_version` envelope on the seed `subgraph_type` examples — design doc shows them without it. If Sean wants the seed files on disk to match the doc literally, drop the envelope from the example shapes.
- The `buddy_policy` exclusion of `"inherit"` on resolved slots. This is a structural call I made; if the runtime ends up wanting to preserve the original `inherit` value alongside the resolved one, the contract needs a second field.
- `Validation Rules` is a new section heading. If voice consistency with Builder B's ports is worth more than explicit validation surface, fold those rules into prose under `Notes` instead.
