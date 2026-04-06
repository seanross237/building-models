# Open Brush AI

AI-powered painting controller for [Open Brush](https://openbrush.app/) VR. Describe a scene in natural language, and AI generates painting commands that execute in Open Brush via its HTTP API.

**Nobody has built this before.** Open Brush has the API, Claude has the brains — this project connects them.

## Quick Start

```bash
# Install dependencies
uv sync

# Run a demo (no API key needed)
uv run python -m open_brush_ai --demo hello
uv run python -m open_brush_ai --demo landscape
uv run python -m open_brush_ai --demo abstract

# Set up your Anthropic API key
cp .env.example .env
# Edit .env and add your ANTHROPIC_API_KEY

# Paint with AI (mock mode — prints commands, doesn't need Open Brush running)
uv run python -m open_brush_ai "paint a sunset over mountains" --mode mock

# Paint with a style
uv run python -m open_brush_ai "a dragon breathing fire" --style fire --mode mock
uv run python -m open_brush_ai "a serene lake" --style van_gogh --mode mock

# Interactive REPL
uv run python -m open_brush_ai --interactive

# List available styles
uv run python -m open_brush_ai --list-styles
```

## With Open Brush Running

When Open Brush is running with the API enabled (port 40074):

```bash
# Paint live — watch it draw in VR!
uv run python -m open_brush_ai "a city skyline at night" --style neon --mode live

# Record commands for later playback
uv run python -m open_brush_ai "a forest clearing" --mode record

# Replay a recording
uv run python -m open_brush_ai --playback recordings/20260404_forest_clearing.json --mode live
```

## Execution Modes

| Mode | What it does |
|------|-------------|
| `mock` (default) | Prints commands to console. No HTTP calls. |
| `live` | Sends commands to Open Brush in real-time. |
| `record` | Generates commands and saves to a JSON file. |

## Painting Styles

7 built-in styles that modify how the AI composes paintings:

- **van_gogh** — Thick swirling strokes, golden/blue palette, Oil Paint brush
- **anime** — Clean outlines, flat colors, bold shadows
- **neon** — Glowing neon lines, cyberpunk aesthetic
- **watercolor** — Soft translucent washes, pastel colors
- **impressionist** — Dappled color dabs, broken color technique
- **pixel** — Blocky grid-aligned shapes, retro 8-bit look
- **fire** — Flames, embers, and molten flows

Or pass any freeform style: `--style "dark gothic cathedral"`

## Project Structure

```
open_brush_ai/
  config.py     — Settings, env loading, execution modes
  models.py     — Pydantic models for commands and plans
  client.py     — Open Brush HTTP API wrapper
  painter.py    — Claude AI integration (the brain)
  styles.py     — Artistic style profiles
  __main__.py   — CLI entry point

demos/
  hello_world.py  — Draws "HI!" in neon (no AI needed)
  landscape.py    — Mountain scene (no AI needed)
  abstract.py     — Algorithmic particle art (no AI needed)

recordings/       — Saved painting sessions (JSON)
```

## How It Works

1. You describe a scene: *"paint a campfire in a dark forest"*
2. The AI (Claude) receives your prompt + a system prompt that teaches it:
   - The Open Brush coordinate system (10x10x10 canvas)
   - Available brushes and what they look like (Fire, NeonPulse, OilPaint, etc.)
   - Composition principles (back-to-front, layer strokes, use 3D depth)
3. Claude generates a structured JSON plan: 30-80 commands with brush changes, colors, and 3D paths
4. The client executes each command against Open Brush's HTTP API at `localhost:40074`
5. You watch it paint in VR

## Open Brush API

Open Brush exposes an HTTP API at `http://localhost:40074/api/v1`. Key commands:

- `draw.path=[x,y,z],[x,y,z],...` — draw a path through 3D points
- `brush.type=Fire` — change brush
- `color.set.html=#FF0000` — set color
- `brush.size.set=0.5` — set stroke width
- `brush.move.to=[x,y,z]` — move brush position

Full docs: https://docs.openbrush.app/user-guide/open-brush-api
