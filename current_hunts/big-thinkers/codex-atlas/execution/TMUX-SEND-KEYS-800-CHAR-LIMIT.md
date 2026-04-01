# tmux send-keys 800-Character Limit with Claude Code

**Date:** 2026-03-30
**Applies to:** Claude Code 2.1.87, tmux 3.6a, macOS

## The Problem

When sending a prompt longer than **799 characters** to a Claude Code session via `tmux send-keys`, the prompt is silently dropped. The Claude Code UI shows `[Pasted text #N +1 lines]` in the input box, but never starts processing. The session remains stuck at 0% with no thinking indicator.

Short prompts (under 800 chars) work perfectly.

## Root Cause

Claude Code's terminal input handler has an internal paste detection mechanism. When it receives a rapid burst of characters exceeding **800 characters** in a single `send-keys` call, it treats the entire input (including the trailing Enter/CR keypress) as pasted content rather than typed input. The Enter that should trigger submission gets absorbed into the paste buffer instead of being interpreted as a submit action.

This is NOT caused by tmux's bracketed paste mode (`\e[200~/\e[201~`) -- verified experimentally that tmux `send-keys` never inserts bracketed paste escape sequences regardless of input length. This is also NOT caused by tmux's `assume-paste-time` setting -- disabling it (setting to 0) does not change the behavior.

The threshold is a **fixed 800-character limit**, independent of terminal width. It was confirmed to be exactly 800: 799 chars always works, 800 chars always triggers paste detection.

## Symptoms

- Claude Code UI shows: `[Pasted text #N +1 lines]`
- The prompt text is in the input buffer but not submitted
- Session stays at 0%, no thinking indicator
- Sending a manual `Enter` afterward does unstick it (the text submits)

## Workarounds

### Option 1: Send Enter separately with a short delay (recommended)

```bash
tmux send-keys -t "$SESSION" -l "$LONG_PROMPT"
sleep 0.2
tmux send-keys -t "$SESSION" Enter
```

The `-l` flag sends the text literally (no key name lookup). The `sleep 0.2` ensures the Enter arrives in a separate input event, so Claude Code treats it as a submit action. Even `sleep 0.1` works. A `sleep 0` or no delay does NOT work -- the Enter arrives too quickly and is still treated as part of the paste.

### Option 2: Send without -l, Enter separate with delay

```bash
tmux send-keys -t "$SESSION" "$LONG_PROMPT"
sleep 0.2
tmux send-keys -t "$SESSION" Enter
```

Same principle, works the same way. The key is the delay before Enter.

### Option 3: Use tmux paste-buffer

```bash
echo "$LONG_PROMPT" > /tmp/prompt.txt
tmux load-buffer /tmp/prompt.txt
tmux paste-buffer -t "$SESSION" -p
sleep 0.2
tmux send-keys -t "$SESSION" Enter
rm /tmp/prompt.txt
```

The `-p` flag on `paste-buffer` inserts bracketed paste markers, which Claude Code handles correctly as pasted text. Enter must still be sent separately.

### Option 4: Keep prompts under 800 characters

If possible, shorten the prompt. Use file references instead of inline instructions:

```bash
# Instead of a long inline prompt:
tmux send-keys -t "$SESSION" "Read /tmp/instructions.txt and follow them" Enter
```

## Experimental Results Summary

| Chars | `send-keys "..." Enter` | `send-keys -l "..." + sleep + Enter` |
|-------|------------------------|--------------------------------------|
| 50    | Works                  | Works                                |
| 300   | Works                  | Works                                |
| 500   | Works                  | Works                                |
| 700   | Works                  | Works                                |
| 751   | Works                  | Works                                |
| 799   | Works                  | Works                                |
| 800   | **STUCK**              | Works                                |
| 901   | **STUCK**              | Works                                |
| 1200  | **STUCK**              | Works                                |
| 1500  | **STUCK**              | Works                                |

Additional findings:
- Special characters (slashes, dashes, quotes) do NOT affect the threshold
- Terminal width does NOT affect the threshold (tested at 60, 80, and 100 cols)
- tmux `assume-paste-time` setting does NOT affect the threshold
- The threshold is purely character-count based at exactly 800 chars

## Files to Update

Any script using `tmux send-keys` with potentially long prompts should be updated. Key files:

- `execution/operator/operator.sh` -- lines 98, 117, 132 (nudge messages can exceed 800 chars with long paths)
- `execution/agents/missionary/system-prompt.md` -- instructions for launching sub-agents
- Any agent system prompt that instructs launching tmux sessions
