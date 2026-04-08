#!/usr/bin/env bash

# Resume the dror-isreal pyramid after pause.sh.
#
# Strategy:
#   1. Refuse to run if operator/babysitter are still alive (use teardown.sh).
#   2. Walk every LAUNCHED sentinel; classify each:
#        (a) DONE in same dir                       -> not stranded, skip
#        (b) WAITING-FOR-CHILDREN in same dir       -> not stranded, skip
#        (c) neither                                -> stranded, clear LAUNCHED
#      We do NOT touch WAITING-FOR-CHILDREN sentinels (unlike launch.sh, which
#      blindly removes them and would force re-partition of completed branches).
#   3. Restart operator + babysitter via the same tmux commands launch.sh uses.
#
# The operator's state machine handles everything else from here. Branches with
# WAITING-FOR-CHILDREN are checked for child completion and re-spawned in
# synthesize mode when ready. Stranded leaves get re-spawned for fresh research.
#
# Partial output files (facts.md, etc) inside stranded leaves are NOT deleted.
# Re-spawned agents will overwrite them. If you want a hard reset on a stranded
# node, delete its partial files manually before running this script.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DROR_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
PREFIX="dror"
LOG_DIR="$DROR_ROOT/run/logs"

is_alive() {
  tmux has-session -t "$1" 2>/dev/null
}

if is_alive "${PREFIX}-operator" || is_alive "${PREFIX}-babysitter"; then
  printf 'ERROR: operator or babysitter is still running.\n'
  printf 'Run bash run/pause.sh first (or bash run/teardown.sh to force-kill).\n'
  exit 1
fi

leftover_agents="$(tmux list-sessions -F '#{session_name}' 2>/dev/null \
  | grep "^${PREFIX}-" || true)"
if [[ -n "$leftover_agents" ]]; then
  printf 'ERROR: leftover %s-* tmux sessions detected:\n' "$PREFIX"
  printf '%s\n' "$leftover_agents" | sed 's/^/  - /'
  printf 'Run bash run/teardown.sh to clear them, then re-run resume.sh.\n'
  exit 1
fi

printf 'dror-isreal resume\n'
printf 'DROR root: %s\n\n' "$DROR_ROOT"

printf 'Step 1: scanning for stranded LAUNCHED sentinels\n'

stranded=0
preserved=0
launched_files=()
while IFS= read -r f; do
  [[ -n "$f" ]] || continue
  launched_files+=("$f")
done < <(find "$DROR_ROOT/tree" -type f -name LAUNCHED)

for launched in "${launched_files[@]}"; do
  node_dir="$(dirname "$launched")"
  if [[ -f "$node_dir/DONE" || -f "$node_dir/WAITING-FOR-CHILDREN" ]]; then
    preserved=$((preserved + 1))
    continue
  fi
  rm -f "$launched"
  stranded=$((stranded + 1))
done

printf '  cleared:   %s stranded LAUNCHED files (will be re-spawned)\n' "$stranded"
printf '  preserved: %s LAUNCHED files alongside DONE or WAITING-FOR-CHILDREN\n' "$preserved"
printf '\n'

printf 'Step 2: current tree state\n'
printf '  SCOPE.md:              %s\n' "$(find "$DROR_ROOT/tree" -name SCOPE.md | wc -l | tr -d ' ')"
printf '  DONE:                  %s\n' "$(find "$DROR_ROOT/tree" -name DONE | wc -l | tr -d ' ')"
printf '  WAITING-FOR-CHILDREN:  %s\n' "$(find "$DROR_ROOT/tree" -name WAITING-FOR-CHILDREN | wc -l | tr -d ' ')"
printf '  facts.md:              %s\n' "$(find "$DROR_ROOT/tree" -name facts.md | wc -l | tr -d ' ')"
printf '  README.md:             %s\n' "$(find "$DROR_ROOT/tree" -name README.md | wc -l | tr -d ' ')"
printf '  SYNTHESIS.md:          %s\n' "$(find "$DROR_ROOT/tree" -name SYNTHESIS.md | wc -l | tr -d ' ')"
printf '  FAILED:                %s\n' "$(find "$DROR_ROOT/tree" -name FAILED | wc -l | tr -d ' ')"
printf '  BLOCKED:               %s\n' "$(find "$DROR_ROOT/tree" -name BLOCKED | wc -l | tr -d ' ')"
printf '\n'

printf 'Step 3: starting operator + babysitter\n'
mkdir -p "$LOG_DIR"

tmux new-session -d -s "${PREFIX}-operator" -c "$DROR_ROOT" \
  "bash run/operator.sh '$DROR_ROOT' '$PREFIX' 2>&1 | tee -a run/logs/operator.log"

tmux new-session -d -s "${PREFIX}-babysitter" -c "$DROR_ROOT" \
  "bash run/babysitter.sh '$DROR_ROOT' '$PREFIX' 2>&1 | tee -a run/logs/babysitter.log"

printf '  - %s-operator\n' "$PREFIX"
printf '  - %s-babysitter\n' "$PREFIX"
printf '\nResume complete. Operator will start spawning on its next poll cycle.\n'
printf 'Watch:  tmux ls | grep dror-\n'
printf 'Pause:  bash run/pause.sh\n'
exit 0
