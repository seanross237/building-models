# Running Atlas with Alternative Models via OpenRouter

**Status:** Future expansion — not yet integrated into Atlas

## What This Does

Uses OpenRouter as an API proxy so Claude Code's interface can drive non-Anthropic models (Kimi K2.5, Grok 4.1, DeepSeek, etc.). Atlas stays completely unchanged. You just swap which binary launches explorer sessions.

## How It Works

```
Normal:   claude  -->  Anthropic API  -->  Claude (Opus/Sonnet)
                                              |
                                     decides what to do
                                              |
                                     Claude Code executes tools locally

OpenRouter:  clauo  -->  OpenRouter API  -->  Kimi K2.5 / Grok / etc.
                                                  |
                                          decides what to do
                                                  |
                                          Claude Code executes tools locally
```

Claude Code (the local app) stays the same. It still runs bash, reads files, writes files — all on your machine. The only thing that changes is which remote model is making the decisions.

## Data Privacy

When any model runs through Claude Code, it receives:
- System prompts (agent instructions)
- Every file the agent reads (goals, reports, library entries)
- Every bash command output
- Full conversation history for that session

**With Anthropic:** data goes to Anthropic's servers. They don't train on API data.

**With OpenRouter + Kimi K2.5:** data goes to OpenRouter → Moonshot (China-based). Their data retention policy may differ. The model can't access your filesystem directly — it only sees what Claude Code sends it as conversation context. But that includes the full content of any file it reads.

**With OpenRouter + Grok 4.1:** data goes to OpenRouter → xAI.

**Practical guidance:**
- For research math missions: probably fine, the data is academic
- For anything proprietary or personal: stick with Anthropic
- OpenRouter lets you filter providers by data policy — look for "no logging" providers
- The video transcript noted that some models (e.g., Mimo) conflict with OpenRouter's privacy guardrails entirely

## Setup

### 1. Get an OpenRouter API Key

Go to https://openrouter.ai/keys, create account, generate key.

### 2. Add API Key to Environment

In `~/.zshrc`, add:

```bash
export OPENROUTER_API_KEY="sk-or-v1-your-key-here"
```

Then `source ~/.zshrc` or open a new terminal.

### 3. Create the Wrapper Script

Create `~/.local/bin/clauo`:

```bash
#!/bin/bash
# Claude Code via OpenRouter
# Usage: clauo [any claude args]
# Override model: OPENROUTER_MODEL=x-ai/grok-4-0414 clauo ...

MODEL="${OPENROUTER_MODEL:-moonshot/kimi-k2.5}"

exec env \
  ANTHROPIC_BASE_URL="https://openrouter.ai/api/v1" \
  ANTHROPIC_API_KEY="$OPENROUTER_API_KEY" \
  ANTHROPIC_MODEL="$MODEL" \
  claude "$@"
```

Make it executable:

```bash
chmod +x ~/.local/bin/clauo
```

### 4. Test Standalone

```bash
clauo                    # Opens Claude Code with Kimi K2.5
```

Try a simple task to verify tool use works (file reads, bash commands). If the model can't execute tools, it won't work as an Atlas explorer.

### 5. Test with a Different Model

```bash
OPENROUTER_MODEL=x-ai/grok-4-0414 clauo    # Grok 4.1
OPENROUTER_MODEL=deepseek/deepseek-r1 clauo  # DeepSeek R1
```

## Integrating with Atlas (When Ready)

Atlas itself doesn't need to change. The integration point is `operator.sh`, which launches explorers. Two options:

### Option A: Environment Variable in Operator

Add one line near the top of `operator.sh`:

```bash
EXPLORER_CMD="${EXPLORER_CMD:-claude}"
```

Then change the explorer launch line from:

```bash
tmux send-keys -t "$session_name" "claude --system-prompt-file ..." Enter
```

To:

```bash
tmux send-keys -t "$session_name" "$EXPLORER_CMD --system-prompt-file ..." Enter
```

Launch with:

```bash
# Opus strategizer + missionary (unchanged), cheap explorers
EXPLORER_CMD=clauo bash operator.sh /path/to/strategy prefix missionary-session

# Or with a specific model
OPENROUTER_MODEL=x-ai/grok-4-0414 EXPLORER_CMD=clauo bash operator.sh ...
```

### Option B: Per-Explorer Model Selection

For more control, the strategizer could write a `<!-- model: openrouter/kimi-k2.5 -->` comment in GOAL.md, and operator.sh could read it to decide which binary to use. This lets the strategizer assign cheap models to literature surveys and keep Opus for math explorations.

## Model Recommendations for Atlas Explorers

| Model | Cost (per 1M in/out) | Context | Tool Use | Notes |
|---|---|---|---|---|
| Kimi K2.5 | ~$1/$3 | 1M | Good | Clean responses, large context matches Opus |
| Grok 4.1 | $0.20/$0.50 | 128K | Good | Cheapest viable option |
| DeepSeek R1 | $0.55/$2.19 | 128K | Decent | Strong reasoning, verbose |
| Free models | $0/$0 | Varies | Weak | Likely won't handle Atlas explorer prompts |

## Risks and Limitations

- **Tool use compatibility:** Not all models handle Claude Code's tool protocol correctly. Test before running a real mission.
- **Context window:** Strategizer needs 1M context. Most non-Anthropic models max at 128K-200K. Only use alternative models for explorers (bounded tasks), not strategizer or missionary.
- **Quality floor:** For math explorations (proofs, computations), weaker models produce reports that waste strategizer time evaluating wrong results. Literature survey explorations are more forgiving.
- **No mid-session model swap:** You can't change the model during a session. Must relaunch.
- **Can't switch models within Claude Code:** `/model` command will try to use Anthropic models regardless.
