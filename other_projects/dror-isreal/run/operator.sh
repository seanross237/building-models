#!/usr/bin/env bash

set -euo pipefail
shopt -s nullglob
export LC_ALL=C

DROR_ROOT="${1:?Usage: operator.sh <dror-root> <session-prefix>}"
PREFIX="${2:?Usage: operator.sh <dror-root> <session-prefix>}"

MAX_DEPTH=4
FANOUT_CAP=15
STAGGER_BATCH=3
STAGGER_GAP=60
POLL_INTERVAL=30
TREE_LOG="$DROR_ROOT/_index/tree.jsonl"
BRANCH_PROMPT="$DROR_ROOT/agents/branch/system-prompt.md"
LEAF_PROMPT="$DROR_ROOT/agents/leaf/system-prompt.md"
MODEL="gpt-5.4-mini"

mkdir -p "$DROR_ROOT/run/logs"
touch "$TREE_LOG"

timestamp_utc() {
  date -u +"%Y-%m-%dT%H:%M:%SZ"
}

log() {
  printf '[%s] %s\n' "$(timestamp_utc)" "$*"
}

json_escape() {
  local value="${1-}"
  value=${value//\\/\\\\}
  value=${value//\"/\\\"}
  value=${value//$'\n'/\\n}
  value=${value//$'\r'/\\r}
  value=${value//$'\t'/\\t}
  printf '%s' "$value"
}

log_event() {
  local event="$1"
  shift

  local json
  json="{\"ts\":\"$(timestamp_utc)\",\"event\":\"$(json_escape "$event")\""
  while (($# >= 2)); do
    local key="$1"
    local value="$2"
    shift 2
    json+=",\"$(json_escape "$key")\":\"$(json_escape "$value")\""
  done
  json+="}"
  printf '%s\n' "$json" >> "$TREE_LOG"
}

rel_path_from_root() {
  local absolute_path="$1"
  printf '%s\n' "${absolute_path#"$DROR_ROOT"/}"
}

depth_for_node() {
  local node_dir="$1"
  local rel_path
  rel_path="$(rel_path_from_root "$node_dir")"
  if [[ "$rel_path" == "tree" ]]; then
    printf '0\n'
    return 0
  fi

  local rel_under_tree="${rel_path#tree/}"
  local segments=()
  IFS='/' read -r -a segments <<< "$rel_under_tree"
  printf '%s\n' "${#segments[@]}"
}

slugify_rel_path() {
  local rel_path="$1"
  local slug="${rel_path#tree/}"
  if [[ "$slug" == "$rel_path" ]]; then
    slug="$rel_path"
  fi
  if [[ -z "$slug" || "$slug" == "tree" ]]; then
    slug="root"
  fi

  slug="$(printf '%s' "$slug" | tr '[:upper:]' '[:lower:]')"
  slug="${slug//\//-}"
  slug="${slug//_/-}"
  slug="$(printf '%s' "$slug" | tr -cd 'a-z0-9-')"
  while [[ "$slug" == *--* ]]; do
    slug="${slug//--/-}"
  done
  slug="${slug#-}"
  slug="${slug%-}"
  if [[ -z "$slug" ]]; then
    slug="root"
  fi
  printf '%.200s\n' "$slug"
}

session_name_for_node() {
  local node_dir="$1"
  local rel_path
  rel_path="$(rel_path_from_root "$node_dir")"
  printf '%s-%s\n' "$PREFIX" "$(slugify_rel_path "$rel_path")"
}

node_type() {
  local node_dir="$1"
  if [[ -f "$node_dir/TYPE" ]]; then
    local raw
    raw="$(tr -d '[:space:]' < "$node_dir/TYPE")"
    if [[ "$raw" == "leaf" ]]; then
      printf 'leaf\n'
      return 0
    fi
  fi
  printf 'branch\n'
}

find_child_scopes() {
  local node_dir="$1"
  local child_scope
  for child_scope in "$node_dir"/*/SCOPE.md; do
    printf '%s\n' "$child_scope"
  done
}

maybe_write_overflow_warning() {
  local parent_dir="$1"
  local child_scopes=()
  local child_scope
  while IFS= read -r child_scope; do
    [[ -n "$child_scope" ]] || continue
    child_scopes+=("$child_scope")
  done < <(find_child_scopes "$parent_dir")
  if ((${#child_scopes[@]} <= FANOUT_CAP)); then
    return 0
  fi

  local warning_file="$parent_dir/OVERFLOW_WARNING"
  if [[ -f "$warning_file" ]]; then
    return 0
  fi

  {
    printf 'timestamp: %s\n' "$(timestamp_utc)"
    printf 'reason: branch wrote %s children; operator cap is %s\n' "${#child_scopes[@]}" "$FANOUT_CAP"
    printf 'operator_policy: only the first %s children in lexical order will be spawned\n' "$FANOUT_CAP"
  } > "$warning_file"
}

node_within_parent_cap() {
  local node_dir="$1"
  if [[ "$node_dir" == "$DROR_ROOT/tree" ]]; then
    return 0
  fi

  local parent_dir
  parent_dir="$(dirname "$node_dir")"
  if [[ ! -f "$parent_dir/SCOPE.md" ]]; then
    return 0
  fi

  local child_scopes=()
  local child_scope
  while IFS= read -r child_scope; do
    [[ -n "$child_scope" ]] || continue
    child_scopes+=("$child_scope")
  done < <(find_child_scopes "$parent_dir")
  if ((${#child_scopes[@]} <= FANOUT_CAP)); then
    return 0
  fi

  maybe_write_overflow_warning "$parent_dir"

  local index=0
  for child_scope in "${child_scopes[@]}"; do
    index=$((index + 1))
    if [[ "$(dirname "$child_scope")" == "$node_dir" ]]; then
      if ((index <= FANOUT_CAP)); then
        return 0
      fi
      return 1
    fi
  done

  return 0
}

already_logged_event_for_path() {
  local event="$1"
  local rel_path="$2"
  grep -F "\"event\":\"$event\"" "$TREE_LOG" 2>/dev/null | grep -F "\"path\":\"$rel_path\"" >/dev/null 2>&1
}

spawn_agent() {
  local node_dir="$1"
  local mode="$2"

  local rel_path depth type session prompt_file kickoff combined_prompt
  rel_path="$(rel_path_from_root "$node_dir")"
  depth="$(depth_for_node "$node_dir")"
  type="$(node_type "$node_dir")"
  session="$(session_name_for_node "$node_dir")"

  if [[ "$type" == "leaf" ]]; then
    prompt_file="$LEAF_PROMPT"
  else
    prompt_file="$BRANCH_PROMPT"
  fi

  case "$mode:$type" in
    initial:branch)
      kickoff="You are being spawned for the FIRST time on this node. Your task is PARTITION. Read SCOPE.md, CHILDREN.md if it already exists, DECISIONS.md, MISSION.md, the parent README if any at ../README.md, and _index/trust-tiers.md. Research your scope shallowly, then (1) write README.md for this node with always-relevant knowledge; (2) partition into 1-${FANOUT_CAP} children unless SCOPE.md says the partition is pre-committed; (3) write or preserve CHILDREN.md as appropriate; (4) mkdir each child and write its SCOPE.md and TYPE if they do not already exist; (5) write WAITING-FOR-CHILDREN; (6) exit. Do NOT wait for children. Your depth is ${depth}. Max depth is ${MAX_DEPTH}. If depth+1 >= ${MAX_DEPTH}, all children MUST be type=leaf."
      ;;
    initial:leaf)
      kickoff="You are being spawned to do deep research on a leaf topic. Read SCOPE.md, parent ../README.md, DECISIONS.md, MISSION.md, and _index/trust-tiers.md. Research in English, Hebrew, and the destination-local language where applicable. Write facts.md, checklist.md, sources.md, and DONE in this directory. Append new source ledger entries to ${DROR_ROOT}/_index/sources.jsonl. Do your work, verify the files exist, write DONE, and exit."
      ;;
    synthesize:branch)
      kickoff="You are being RE-SPAWNED on a branch whose children are all complete. Your task is SYNTHESIZE. Read each child directory's SYNTHESIS.md for branch children or facts.md for leaf children. Write SYNTHESIS.md for this node that rolls up key findings, cross-child themes, and gaps. Then write DONE. Then exit. Do not re-research and do not re-partition."
      ;;
    *)
      log "Skipping unsupported spawn mode/type combination: mode=$mode type=$type path=$rel_path"
      return 1
      ;;
  esac

  if tmux has-session -t "$session" 2>/dev/null; then
    : > "$node_dir/LAUNCHED"
    log "Session already exists, treating as running: $session ($rel_path)"
    return 0
  fi

  combined_prompt="$(
    cat "$prompt_file"
    printf '\n---\n# Kickoff for this spawn\n%s\n' "$kickoff"
    printf 'Your node directory: %s\n' "$node_dir"
    printf 'Your depth: %s\n' "$depth"
    printf 'Project root: %s\n' "$DROR_ROOT"
  )"

  local quoted_node_dir quoted_root quoted_model quoted_run_log quoted_depth quoted_mode bash_script shell_command
  printf -v quoted_node_dir '%q' "$node_dir"
  printf -v quoted_root '%q' "$DROR_ROOT"
  printf -v quoted_model '%q' "$MODEL"
  printf -v quoted_run_log '%q' "$node_dir/run.log"
  printf -v quoted_depth '%q' "$depth"
  printf -v quoted_mode '%q' "$mode"

  bash_script="$(cat <<EOF
export DROR_DEPTH=$quoted_depth
export DROR_ROOT=$quoted_root
export DROR_MODE=$quoted_mode
set -o pipefail
cat <<'__DROR_PROMPT__' | codex --search exec --dangerously-bypass-approvals-and-sandbox --cd $quoted_node_dir --add-dir $quoted_root -m $quoted_model - 2>&1 | tee $quoted_run_log
$combined_prompt
__DROR_PROMPT__
status=\${PIPESTATUS[1]}
printf '=== codex exec exited with status =%s ===\n' "\$status" >> $quoted_run_log
sleep 120
EOF
)"
  printf -v shell_command 'arch -arm64 bash -lc %q' "$bash_script"

  if ! tmux new-session -d -s "$session" -c "$node_dir" "$shell_command"; then
    {
      printf 'timestamp: %s\n' "$(timestamp_utc)"
      printf 'reason: failed to create tmux session %s\n' "$session"
      printf 'mode: %s\n' "$mode"
      printf 'type: %s\n' "$type"
    } > "$node_dir/FAILED"
    log_event "spawn_failed" "path" "$rel_path" "session" "$session" "type" "$type" "mode" "$mode" "depth" "$depth"
    log "Failed to create tmux session for $rel_path ($session)"
    return 1
  fi

  : > "$node_dir/LAUNCHED"
  log_event "spawn" "path" "$rel_path" "session" "$session" "type" "$type" "mode" "$mode" "depth" "$depth"
  log "Spawned $mode $type agent: $session ($rel_path depth=$depth model=$MODEL)"
  return 0
}

log "Operator started"
log "DROR_ROOT=$DROR_ROOT"
log "PREFIX=$PREFIX"
log "MAX_DEPTH=$MAX_DEPTH FANOUT_CAP=$FANOUT_CAP STAGGER_BATCH=$STAGGER_BATCH STAGGER_GAP=$STAGGER_GAP POLL_INTERVAL=$POLL_INTERVAL"
log "Model=$MODEL"

while true; do
  if [[ -f "$DROR_ROOT/tree/DONE" ]]; then
    log "Root complete; exiting."
    log_event "root_complete" "path" "tree"
    exit 0
  fi

  spawned_count=0
  scope_files=()
  while IFS= read -r scope_file; do
    [[ -n "$scope_file" ]] || continue
    scope_files+=("$scope_file")
  done < <(find "$DROR_ROOT/tree" -type f -name SCOPE.md | sort)

  for scope_file in "${scope_files[@]}"; do
    node_dir="$(dirname "$scope_file")"
    rel_path="$(rel_path_from_root "$node_dir")"
    depth="$(depth_for_node "$node_dir")"

    if ! node_within_parent_cap "$node_dir"; then
      continue
    fi

    if [[ -f "$node_dir/DONE" ]]; then
      continue
    fi

    if [[ -f "$node_dir/FAILED" ]]; then
      if ! already_logged_event_for_path "failed_skip" "$rel_path"; then
        log_event "failed_skip" "path" "$rel_path"
        log "Skipping FAILED node: $rel_path"
      fi
      continue
    fi

    if [[ -f "$node_dir/BLOCKED" ]]; then
      if ! already_logged_event_for_path "blocked_skip" "$rel_path"; then
        log_event "blocked_skip" "path" "$rel_path"
        log "Skipping BLOCKED node: $rel_path"
      fi
      continue
    fi

    maybe_write_overflow_warning "$node_dir"

    if [[ -f "$node_dir/WAITING-FOR-CHILDREN" ]]; then
      all_done=true
      any_children=false
      child_scopes=()
      while IFS= read -r child_scope; do
        [[ -n "$child_scope" ]] || continue
        child_scopes+=("$child_scope")
      done < <(find_child_scopes "$node_dir")
      for child_scope in "${child_scopes[@]}"; do
        child_dir="$(dirname "$child_scope")"
        if ! node_within_parent_cap "$child_dir"; then
          continue
        fi
        any_children=true
        if [[ ! -f "$child_dir/DONE" ]]; then
          all_done=false
          break
        fi
      done

      if [[ "$any_children" == true && "$all_done" == true ]]; then
        rm -f "$node_dir/WAITING-FOR-CHILDREN" "$node_dir/LAUNCHED"
        if spawn_agent "$node_dir" synthesize; then
          spawned_count=$((spawned_count + 1))
          if ((spawned_count >= STAGGER_BATCH)); then
            log "Spawn batch limit reached; sleeping ${STAGGER_GAP}s"
            sleep "$STAGGER_GAP"
            spawned_count=0
          fi
        fi
      fi
      continue
    fi

    if [[ -f "$node_dir/LAUNCHED" ]]; then
      continue
    fi

    if ((depth > MAX_DEPTH)); then
      printf 'blocked: depth cap (%s > %s)\n' "$depth" "$MAX_DEPTH" > "$node_dir/BLOCKED"
      log_event "blocked" "path" "$rel_path" "reason" "depth_cap" "depth" "$depth"
      log "Blocked node beyond max depth: $rel_path"
      continue
    fi

    if spawn_agent "$node_dir" initial; then
      spawned_count=$((spawned_count + 1))
      if ((spawned_count >= STAGGER_BATCH)); then
        log "Spawn batch limit reached; sleeping ${STAGGER_GAP}s"
        sleep "$STAGGER_GAP"
        spawned_count=0
      fi
    fi
  done

  sleep "$POLL_INTERVAL"
done
