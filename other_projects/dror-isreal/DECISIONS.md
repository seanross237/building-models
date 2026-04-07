# Decisions (locked)

These are the architectural decisions made up-front so the agents don't
re-decide them. Each is locked unless explicitly revisited.

## Taxonomy

- **Root partition style**: domain-first (not country-first, not
  journey-stage). Domains at level 0, with countries appearing as
  cross-cutting specializations under `tree/_countries/` referenced from
  leaf nodes that need them.
- **Root domains (11 + 1 cross-cut)**: pre-committed, written by hand in
  `tree/CHILDREN.md`. Branch agents do NOT get to re-partition the root.
  Every other level is decided by the agent at that level.

## Shape

- **Depth cap**: 4 levels below `tree/`. Operator refuses to spawn deeper.
- **Fanout cap**: 15 children per branch node. Branch agents must justify
  any child and may choose 1–15.
- **Variable depth**: a branch may decide its children are leaves (ending a
  path early) if the topic is narrow enough. A 2-deep branch is as valid
  as a 4-deep one.
- **Branch vs leaf is the terminating condition**, not a fixed depth.

## Sources

- **Trust tiers** (`_index/trust-tiers.md`):
  1. Government official (.gov.il, .pt/.de/.etc official ministries)
  2. Consulate / embassy official page
  3. Established law firm, major bank, or recognized relocation service
  4. Expat blog or established community site
  5. Forum post / anecdote
- **Rule**: each leaf must cite at least one tier-1 or tier-2 source per
  major claim. Tier-4 and tier-5 are used for texture and to surface lived
  experience, never as the sole support for a factual claim.
- **Source ledger**: `_index/sources.jsonl`, append-only. Before citing a
  URL, a leaf checks the ledger; if present, reuse the entry (same fetch
  date, same quote). Otherwise append a new entry.

## Languages

- **Mandatory surfaces per leaf**: English, Hebrew, destination local.
- **Missing is recorded, not hidden.** If no Hebrew source exists for a
  given topic, `sources.md` records "hebrew: not found" with the search
  queries attempted.
- **Hebrew is not optional.** The exit-from-Israel branches (especially
  `01_exiting-israel`) will have more Hebrew sources than English.

## Orchestration

- **Model**: Sonnet for all agents (branch and leaf).
- **Claude invocation**: `claude --system-prompt-file <path>
  --permission-mode bypassPermissions` (borrowed from atlas).
- **Session naming**: `dror-<slugified-tree-path>` — e.g.
  `dror-01-exiting-israel-bituach-leumi`. Operator enforces slugging.
- **800-character paste bug**: every prompt to a child session goes through
  `run/safe_send_prompt.sh` (literal send + 0.3s sleep + Enter). Not
  optional.
- **Polling is banned.** Parents use background file-watches
  (`run_in_background=true` on a `while [ ! -f DONE ]; do sleep 30; done`).
  See the horror story in `agents/branch/system-prompt.md`.
- **Stagger factor**: the operator spawns at most 3 new children per
  branch at a time, with a 60-second gap, to avoid slamming rate limits.
  As children finish, new ones come in.
- **Verification cadence**: TBD. Not implemented in this build.

## What the root-level agent does NOT decide

- The 11 domains at level 0 (already committed).
- The trust-tier policy.
- The language policy.
- The depth/fanout caps.

## What every agent DOES decide

- The shape of its own subtree below its SCOPE.md.
- Whether its children are branches or leaves.
- Which sources to cite and in what language.
- How narrowly to scope each child.
