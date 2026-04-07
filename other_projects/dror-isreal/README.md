# dror-isreal

A hierarchical, agent-built knowledge base for Israelis leaving Israel to live
elsewhere. The end goal is a conversational product that walks a user through
the process — starting from broad questions and narrowing as the user's
situation clarifies ("you're going to Portugal — for Portugal you need these
three things — do you have your visa yet?").

This repo is **only the knowledge substrate** for that product. It is not the
product itself. The product reads this tree.

## What lives here

- `MISSION.md` — the product the knowledge base will back, who it's for, what
  non-negotiable constraints apply (verifiability, languages, trust tiers).
- `DECISIONS.md` — the architectural decisions taken up-front so the agents
  don't redecide them.
- `run/` — the bash scripts that orchestrate the pyramid of tmux-hosted
  Claude agents. Pure bash, zero-token orchestration, based on the atlas
  pattern.
- `agents/branch/system-prompt.md` — system prompt for a **branch agent**,
  which partitions its scope into children and waits for them.
- `agents/leaf/system-prompt.md` — system prompt for a **leaf agent**, which
  does deep research in a narrow scope and writes verifiable facts.
- `_index/` — shared indices: source ledger, topic dedupe, trust tiers,
  spawn log.
- `tree/` — the knowledge tree itself. Every folder has the same shape:
  `SCOPE.md` (input from parent), `TYPE` (branch or leaf), then eventually
  `README.md` + either children folders or `facts.md`/`checklist.md`/
  `sources.md`, and a `DONE` sentinel.

## Architecture in one paragraph

The operator (`run/operator.sh`) is a bash loop. It walks `tree/` looking for
`SCOPE.md` files that don't have a matching `LAUNCHED` sentinel. For each one,
it reads `TYPE`, spawns a tmux session running Claude Code with the right
system prompt, and writes `LAUNCHED`. Branch agents partition their scope,
create child folders with `SCOPE.md` + `TYPE`, write their own `README.md`,
then set up a background file-watch on children `DONE` files (so they cost
zero tokens while waiting). Leaf agents research, write `facts.md`/
`sources.md`/`checklist.md`, and drop `DONE`. The operator keeps walking.
The whole tree collapses upward as `DONE` sentinels propagate.

## Rules baked into the agents

- **Depth cap: 4 levels below `tree/`.** Operator refuses to spawn deeper.
- **Fanout cap: 15 children per branch.** Branch agents justify every child.
- **Every factual claim carries a source URL, fetch date, trust tier, and
  short verbatim quote.** No exceptions.
- **Trust tiers**: government > consulate/embassy > established law firm or
  bank > expat blog > forum. Each leaf must cite at least one tier-1 or
  tier-2 source per major claim.
- **Languages**: leaves must attempt English, Hebrew, and the destination's
  local language. Missing languages are recorded, not hidden.
- **No polling.** Parents wait via background file-watches. This rule has a
  horror story attached to it in the branch system prompt — atlas burned 255M
  tokens on a single polling strategizer.

## Launch / teardown

- `bash run/launch.sh` — clean start, spawns the operator in its own tmux
  session, which then spawns the 11 root domain branches.
- `bash run/teardown.sh` — kills every `dror-*` tmux session. Does NOT
  `killall claude` (unsafe if other Claude sessions exist on the box).
- `tmux attach -t dror-operator` — watch the orchestrator.
- `tmux ls | grep dror-` — see every running agent.
- `find tree -name DONE | wc -l` — progress check.

## Where this came from

This is a direct descendant of the atlas project
(`home-base_worktrees/experiment-report-c/current_hunts/big-thinkers/atlas`).
The agent architecture, the 800-character paste-limit workaround, the
pure-bash operator/babysitter pattern, the "no polling" rule, and the
file-based signaling are all reused verbatim from atlas. The innovations
here are the source ledger, the trust-tier discipline, the language
dimension, and the recursive branch/leaf contract that lets depth vary
across branches.
