#!/usr/bin/env bash
set -euo pipefail

source "$(cd "$(dirname "$0")" && pwd)/common.sh"

MISSION="${1:-}"
[[ -n "$MISSION" ]] || fail "Usage: bin/start-planning-run.sh <mission>"

ensure_runtime_dirs
"$PATLAS_ROOT/bin/ensure-dispatcher.sh" >/dev/null

MISSION_DIR="$PATLAS_ROOT/missions/$MISSION"
[[ -d "$MISSION_DIR" ]] || fail "Missing mission: $MISSION_DIR"

LATEST_RUN_DIR="$(find "$MISSION_DIR/planning-runs" -maxdepth 1 -type d -name 'run-*' 2>/dev/null | sort | tail -1 || true)"
if [[ -n "$LATEST_RUN_DIR" && ! -f "$LATEST_RUN_DIR/winning-chain.md" ]]; then
  RUN_DIR="$LATEST_RUN_DIR"
  RUN_ID="$(basename "$RUN_DIR")"
else
  RUN_INDEX=1
  while [[ -d "$MISSION_DIR/planning-runs/run-$(printf '%03d' "$RUN_INDEX")" ]]; do
    ((RUN_INDEX+=1))
  done
  RUN_ID="run-$(printf '%03d' "$RUN_INDEX")"
  RUN_DIR="$MISSION_DIR/planning-runs/$RUN_ID"
fi

mkdir -p \
  "$RUN_DIR/planner-chains" \
  "$RUN_DIR/selected" \
  "$RUN_DIR/attacks" \
  "$RUN_DIR/judgments" \
  "$RUN_DIR/refined"

MISSION_CONTEXT="$RUN_DIR/mission-context.md"
PLANNER_TASK="$PATLAS_ROOT/runtime/tasks/${SESSION_PREFIX}-$(sanitize_token "$MISSION")-${RUN_ID}-planner.md"
SELECTOR_TASK="$PATLAS_ROOT/runtime/tasks/${SESSION_PREFIX}-$(sanitize_token "$MISSION")-${RUN_ID}-selector.md"
FINAL_TASK="$PATLAS_ROOT/runtime/tasks/${SESSION_PREFIX}-$(sanitize_token "$MISSION")-${RUN_ID}-final-decider.md"

if [[ ! -f "$MISSION_CONTEXT" ]]; then
  {
    echo "# Mission Context Snapshot"
    echo
    echo "Mission: $MISSION"
    echo "Planning run: $RUN_ID"
    echo "Timestamp: $(timestamp_utc)"
    echo
    for candidate in MISSION.md CHAIN.md CHAIN-HISTORY.md MISSION-COMPLETE.md; do
      if [[ -f "$MISSION_DIR/$candidate" ]]; then
        echo "## $candidate"
        echo
        cat "$MISSION_DIR/$candidate"
        echo
      fi
    done

    latest_step="$(find "$MISSION_DIR/steps" -maxdepth 1 -type d -name 'step-*' 2>/dev/null | sort | tail -1 || true)"
    if [[ -n "${latest_step:-}" && -f "$latest_step/RESULTS.md" ]]; then
      echo "## Latest Step Results"
      echo
      cat "$latest_step/RESULTS.md"
      echo
    fi
  } > "$MISSION_CONTEXT"
fi

cat > "$PLANNER_TASK" <<EOF
Plan a new wide-funnel run for mission "$MISSION".

Read $MISSION_CONTEXT first.

Write these outputs:
- $RUN_DIR/planner.md
- $RUN_DIR/planner-chains/chain-01.md
- $RUN_DIR/planner-chains/chain-02.md
- $RUN_DIR/planner-chains/chain-03.md
- Optional: $RUN_DIR/planner-chains/chain-04.md and chain-05.md if you generate more than three chains

Requirements:
- Produce 3-5 genuinely distinct chains.
- Each chain file must be a fully scoped candidate path with ordered steps, dependencies, expected outputs, and kill conditions.
- planner.md must summarize the portfolio and explain the major differences between chains.
- Preserve useful context from prior runs when relevant, but do not assume the current chain is still correct.
EOF

PLANNER_SESSION="${SESSION_PREFIX}-$(sanitize_token "$MISSION")-${RUN_ID}-planner"
if [[ ! -f "$RUN_DIR/planner.md" ]]; then
  "$PATLAS_ROOT/bin/launch-role.sh" \
    --role planner \
    --workdir "$RUN_DIR" \
    --task-file "$PLANNER_TASK" \
    --session-name "$PLANNER_SESSION" \
    --sentinel-file "$RUN_DIR/planner.md"

  wait_for_status_terminal_state "$PATLAS_ROOT/runtime/status/${PLANNER_SESSION}.json"
fi

cat > "$SELECTOR_TASK" <<EOF
Select the best three chains from this planning run.

Inputs:
- Portfolio summary: $RUN_DIR/planner.md
- Candidate chains: $RUN_DIR/planner-chains/chain-*.md

Write these outputs:
- $RUN_DIR/selector.md
- $RUN_DIR/selected/chain-01.md
- $RUN_DIR/selected/chain-02.md
- $RUN_DIR/selected/chain-03.md

Requirements:
- Rank the full set of generated chains.
- selector.md must explain why the selected three make the strongest portfolio.
- Each selected chain file must contain the full text of the chosen chain, not just a pointer back to planner output.
EOF

SELECTOR_SESSION="${SESSION_PREFIX}-$(sanitize_token "$MISSION")-${RUN_ID}-selector"
if [[ ! -f "$RUN_DIR/selector.md" ]]; then
  "$PATLAS_ROOT/bin/launch-role.sh" \
    --role selector \
    --workdir "$RUN_DIR" \
    --task-file "$SELECTOR_TASK" \
    --session-name "$SELECTOR_SESSION" \
    --sentinel-file "$RUN_DIR/selector.md"

  wait_for_status_terminal_state "$PATLAS_ROOT/runtime/status/${SELECTOR_SESSION}.json"
fi

for idx in 01 02 03; do
  CHAIN_FILE="$RUN_DIR/selected/chain-$idx.md"
  ATTACK_TASK="$PATLAS_ROOT/runtime/tasks/${SESSION_PREFIX}-$(sanitize_token "$MISSION")-${RUN_ID}-attacker-$idx.md"
  ATTACK_SESSION="${SESSION_PREFIX}-$(sanitize_token "$MISSION")-${RUN_ID}-attacker-$idx"

  [[ -f "$CHAIN_FILE" ]] || fail "Selector did not produce $CHAIN_FILE"

  cat > "$ATTACK_TASK" <<EOF
Attack selected chain $idx for mission "$MISSION".

Read:
- $CHAIN_FILE

Write:
- $RUN_DIR/attacks/chain-$idx.md

Requirements:
- Critique every step concretely.
- Evaluate structural weaknesses of the whole chain.
- Be ruthless but fair.
EOF

  if [[ ! -f "$RUN_DIR/attacks/chain-$idx.md" ]]; then
    "$PATLAS_ROOT/bin/launch-role.sh" \
      --role attacker \
      --workdir "$RUN_DIR" \
      --task-file "$ATTACK_TASK" \
      --session-name "$ATTACK_SESSION" \
      --sentinel-file "$RUN_DIR/attacks/chain-$idx.md"
  fi
done

for idx in 01 02 03; do
  ATTACK_SESSION="${SESSION_PREFIX}-$(sanitize_token "$MISSION")-${RUN_ID}-attacker-$idx"
  if [[ ! -f "$RUN_DIR/attacks/chain-$idx.md" ]]; then
    wait_for_status_terminal_state "$PATLAS_ROOT/runtime/status/${ATTACK_SESSION}.json"
  fi
  [[ -f "$RUN_DIR/attacks/chain-$idx.md" ]] || fail "Attacker did not produce $RUN_DIR/attacks/chain-$idx.md"
done

for idx in 01 02 03; do
  CHAIN_FILE="$RUN_DIR/selected/chain-$idx.md"
  ATTACK_FILE="$RUN_DIR/attacks/chain-$idx.md"
  JUDGE_TASK="$PATLAS_ROOT/runtime/tasks/${SESSION_PREFIX}-$(sanitize_token "$MISSION")-${RUN_ID}-judge-$idx.md"
  JUDGE_SESSION="${SESSION_PREFIX}-$(sanitize_token "$MISSION")-${RUN_ID}-judge-$idx"

  cat > "$JUDGE_TASK" <<EOF
Judge selected chain $idx for mission "$MISSION".

Read:
- Original selected chain: $CHAIN_FILE
- Attack critique: $ATTACK_FILE

Write:
- $RUN_DIR/judgments/chain-$idx.md
- $RUN_DIR/refined/chain-$idx.md

Requirements:
- Label each major critique valid, partially valid, or invalid.
- Produce a refined chain that incorporates the valid critiques.
- Include a probability assessment for whether this chain can yield a presentable result.
EOF

  if [[ ! -f "$RUN_DIR/judgments/chain-$idx.md" || ! -f "$RUN_DIR/refined/chain-$idx.md" ]]; then
    "$PATLAS_ROOT/bin/launch-role.sh" \
      --role judge \
      --workdir "$RUN_DIR" \
      --task-file "$JUDGE_TASK" \
      --session-name "$JUDGE_SESSION" \
      --sentinel-file "$RUN_DIR/judgments/chain-$idx.md"
  fi
done

for idx in 01 02 03; do
  JUDGE_SESSION="${SESSION_PREFIX}-$(sanitize_token "$MISSION")-${RUN_ID}-judge-$idx"
  if [[ ! -f "$RUN_DIR/judgments/chain-$idx.md" || ! -f "$RUN_DIR/refined/chain-$idx.md" ]]; then
    wait_for_status_terminal_state "$PATLAS_ROOT/runtime/status/${JUDGE_SESSION}.json"
  fi
  [[ -f "$RUN_DIR/judgments/chain-$idx.md" ]] || fail "Judge did not produce $RUN_DIR/judgments/chain-$idx.md"
  [[ -f "$RUN_DIR/refined/chain-$idx.md" ]] || fail "Judge did not produce $RUN_DIR/refined/chain-$idx.md"
done

cat > "$FINAL_TASK" <<EOF
Make the final wide-funnel decision for mission "$MISSION".

Read:
- $RUN_DIR/selector.md
- $RUN_DIR/judgments/chain-01.md
- $RUN_DIR/judgments/chain-02.md
- $RUN_DIR/judgments/chain-03.md
- $RUN_DIR/refined/chain-01.md
- $RUN_DIR/refined/chain-02.md
- $RUN_DIR/refined/chain-03.md

Write:
- $RUN_DIR/final-decider.md
- $RUN_DIR/winning-chain.md

Requirements:
- Choose one winning refined chain.
- You may incorporate elements from losing chains if they improve the winner.
- final-decider.md must explain the choice.
- winning-chain.md must be the canonical chain text ready to copy into CHAIN.md.
EOF

FINAL_SESSION="${SESSION_PREFIX}-$(sanitize_token "$MISSION")-${RUN_ID}-final-decider"
if [[ ! -f "$RUN_DIR/final-decider.md" || ! -f "$RUN_DIR/winning-chain.md" ]]; then
  "$PATLAS_ROOT/bin/launch-role.sh" \
    --role final-decider \
    --workdir "$RUN_DIR" \
    --task-file "$FINAL_TASK" \
    --session-name "$FINAL_SESSION" \
    --sentinel-file "$RUN_DIR/final-decider.md"

  wait_for_status_terminal_state "$PATLAS_ROOT/runtime/status/${FINAL_SESSION}.json"
fi
[[ -f "$RUN_DIR/final-decider.md" ]] || fail "Final decider did not produce final-decider.md"
[[ -f "$RUN_DIR/winning-chain.md" ]] || fail "Final decider did not produce winning-chain.md"

cp "$RUN_DIR/winning-chain.md" "$MISSION_DIR/CHAIN.md"
touch "$MISSION_DIR/CHAIN-HISTORY.md"
if ! rg -q "^## $RUN_ID — " "$MISSION_DIR/CHAIN-HISTORY.md"; then
  {
    echo
    echo "## $RUN_ID — $(timestamp_utc)"
    echo
    cat "$RUN_DIR/final-decider.md"
    echo
    echo "### Winning Chain"
    echo
    cat "$RUN_DIR/winning-chain.md"
    echo
  } >> "$MISSION_DIR/CHAIN-HISTORY.md"
fi

echo "planning_run=$RUN_DIR"
echo "chain_file=$MISSION_DIR/CHAIN.md"
echo "chain_history=$MISSION_DIR/CHAIN-HISTORY.md"
