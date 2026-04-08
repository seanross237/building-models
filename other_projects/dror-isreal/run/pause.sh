#!/usr/bin/env bash

# Pause the dror-isreal pyramid at a clean stop point.
#
# Strategy:
#   1. Kill operator + babysitter immediately so no new agents spawn.
#   2. Let in-flight agents finish naturally (they will write DONE on their own).
#   3. Wait up to MAX_WAIT_SECS for the agent count to drop to zero, polling
#      every POLL_SECS.
#   4. If anything is still running at the timeout, do NOT auto-kill it.
#      Print the survivors and recommend the operator decide whether to wait
#      longer or run teardown.sh.
#
# This script never deletes content files. It only kills tmux sessions.
# Stranded LAUNCHED sentinels are handled by resume.sh, not here.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DROR_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
PREFIX="dror"
MAX_WAIT_SECS=1200
POLL_SECS=30

count_agent_sessions() {
  tmux list-sessions -F '#{session_name}' 2>/dev/null \
    | grep "^${PREFIX}-" \
    | grep -v "^${PREFIX}-operator$" \
    | grep -v "^${PREFIX}-babysitter$" \
    | wc -l \
    | tr -d ' '
}

kill_if_alive() {
  local session="$1"
  if tmux has-session -t "$session" 2>/dev/null; then
    tmux kill-session -t "$session"
    printf '  killed %s\n' "$session"
  fi
}

printf 'dror-isreal pause\n'
printf 'DROR root: %s\n\n' "$DROR_ROOT"

printf 'Step 1: stopping spawner sessions (operator + babysitter)\n'
kill_if_alive "${PREFIX}-operator"
kill_if_alive "${PREFIX}-babysitter"
printf '\n'

initial_agents="$(count_agent_sessions)"
printf 'Step 2: waiting for %s in-flight agents to finish naturally\n' "$initial_agents"
printf '(timeout: %ss, poll: %ss)\n\n' "$MAX_WAIT_SECS" "$POLL_SECS"

elapsed=0
while ((elapsed < MAX_WAIT_SECS)); do
  current="$(count_agent_sessions)"
  printf '  [%4ss] %s in-flight\n' "$elapsed" "$current"
  if ((current == 0)); then
    printf '\nAll in-flight agents finished cleanly.\n'
    break
  fi
  sleep "$POLL_SECS"
  elapsed=$((elapsed + POLL_SECS))
done

final="$(count_agent_sessions)"
printf '\n'
if ((final > 0)); then
  printf 'WARNING: %s agent(s) still running after %ss timeout.\n' "$final" "$MAX_WAIT_SECS"
  printf 'Survivors:\n'
  tmux list-sessions -F '#{session_name}' 2>/dev/null \
    | grep "^${PREFIX}-" \
    | grep -v "^${PREFIX}-operator$" \
    | grep -v "^${PREFIX}-babysitter$" \
    | sed 's/^/  - /'
  printf '\nThese are likely stuck on slow web fetches. Options:\n'
  printf '  - Wait longer:    bash run/pause.sh   (rerun, it picks up where it left off)\n'
  printf '  - Force kill all: bash run/teardown.sh\n'
  printf 'Stranded LAUNCHED sentinels (if any) will be cleaned up by resume.sh later.\n'
  exit 1
fi

printf 'Pause complete. Tree state preserved. To resume: bash run/resume.sh\n'
exit 0
