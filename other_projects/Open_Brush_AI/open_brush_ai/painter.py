"""AI Painter — uses Claude (via OpenRouter or Anthropic) to decompose text prompts into Open Brush commands."""

from __future__ import annotations

import json
import re

import requests

from .client import OpenBrushClient
from .config import DEFAULT_MODEL, require_api_key
from .models import PaintingPlan
from .styles import StyleProfile, get_style

# ── System prompt ─────────────────────────────────────────────

SYSTEM_PROMPT = """\
You are an AI painter controlling Open Brush, a VR painting application.
Your job is to take a scene description and produce a detailed sequence of
painting commands that will create that scene in 3D space.

## Coordinate System

- **X axis**: left (−5) to right (+5)
- **Y axis**: ground (0) to sky (10)
- **Z axis**: near (+5, toward viewer) to far (−5, into distance)
- One unit ≈ 1 meter in VR space
- The canvas is roughly 10×10×10 units
- The viewer stands at approximately (0, 4, 6) looking toward Z=−5

## Available Commands

Each command is a JSON object with "action", "params", and optional "comment".

### Brush & Style
- `set_brush` — Change brush type
  params: {"type": "<BrushName>"}
- `set_color_rgb` — Set color (0.0-1.0 range)
  params: {"r": 0.5, "g": 0.2, "b": 0.8}
- `set_color_html` — Set color by name or hex
  params: {"color": "#FF6B00"} or {"color": "skyblue"}
- `set_size` — Set brush stroke width
  params: {"size": 0.5}  (range: 0.01 to 3.0)

### Movement (no drawing)
- `move_to` — Move brush to absolute position
  params: {"x": 0, "y": 5, "z": -2}
- `move_by` — Move brush by relative offset
  params: {"dx": 1, "dy": 0, "dz": -0.5}

### Drawing
- `draw_path` — Draw a path through a list of 3D points
  params: {"points": [[x1,y1,z1], [x2,y2,z2], ...]}
  This is your PRIMARY drawing command. Use 4-20 points per path.
  More points = smoother curves.
- `draw_stroke` — Full control: position + rotation + pressure per point
  params: {"strokes": [[x,y,z, rotX,rotY,rotZ, pressure], ...]}
  Use for advanced effects. Pressure 0.0-1.0 affects width.
- `draw_forward` — Draw a line forward from current position
  params: {"length": 2.0}

### Orientation
- `look_at` — Point brush toward a position
  params: {"x": 0, "y": 5, "z": -3}
- `turn_y` — Rotate left/right (degrees)
  params: {"degrees": 45}

### Timing
- `pause` — Wait between commands (for visual effect)
  params: {"seconds": 0.5}

## Available Brushes

### Standard (solid strokes)
- **Ink** — clean, smooth line (default for outlines)
- **Marker** — thick felt-tip marker look
- **Flat** — flat ribbon-like stroke
- **Pen** — thin ballpoint pen line
- **Highlighter** — semi-transparent wide marker

### Painterly (textured strokes)
- **OilPaint** — thick textured oil paint with visible brush marks
- **ThickPaint** — very thick impasto-style paint
- **WetPaint** — smooth wet-on-wet paint effect
- **Splatter** — paint splatter/spray texture

### Glowing / Neon
- **NeonPulse** — animated glowing neon tube
- **LightWire** — thin glowing wire
- **Light** — soft diffused glow
- **Electricity** — crackling electric arc

### Particles / Effects
- **Fire** — flickering flame particles trailing the stroke
- **Embers** — floating hot ember particles
- **Smoke** — wispy smoke trail
- **Stars** — twinkling star particles
- **Snow** — falling snowflake particles
- **Bubbles** — floating bubble particles
- **Rainbow** — multi-color flowing ribbon
- **Sparks** — bright flying spark particles
- **Leaves** — falling leaf particles
- **Lightning** — bright jagged lightning bolt

### Geometric
- **Dots** — evenly spaced dots along the path
- **Taffy** — stretchy taffy-like tube
- **Tube** — solid 3D tube
- **Comet** — glowing comet trail with tail

## Painting Principles

1. **Paint back-to-front**: Start with the sky/background (Z = −4 to −5),
   then middle ground (Z = −2 to −1), then foreground (Z = 0 to 2).
   This creates natural depth.

2. **Set state before drawing**: Brush type, color, and size persist between
   commands. Set them once, then draw multiple paths.

3. **Use move_to for disconnected shapes**: Before starting a new element,
   move_to its starting position. Otherwise the next draw_path continues
   from wherever the brush last was.

4. **Scale brush size by distance**: Background elements use larger sizes
   (1.0-2.5), foreground details use smaller (0.05-0.5).

5. **Build curves with points**: draw_path connects points with segments.
   Use 8-15 points for smooth curves. Fewer for sharp geometric shapes.

6. **Use 3D depth**: Offset elements on the Z axis to create parallax.
   Don't flatten everything to Z=0.

7. **Layer strokes**: Multiple overlapping strokes create richer textures.
   Draw a base layer, then add detail strokes on top.

8. **Match brush to subject**: Fire brush for flames, Snow for winter,
   OilPaint for landscapes, NeonPulse for sci-fi, etc.

9. **Aim for 30-80 commands** per painting. Under 20 looks sparse.
   Over 100 risks clutter.

10. **Comment everything**: Every command should have a comment explaining
    what part of the scene it creates.

## Output Format

Respond with ONLY a JSON object — no markdown, no explanation, no code fences:

{
  "title": "Short title for this painting",
  "description": "One sentence about the painting",
  "commands": [
    {"action": "set_brush", "params": {"type": "Ink"}, "comment": "Outline brush"},
    {"action": "set_color_html", "params": {"color": "#87CEEB"}, "comment": "Sky blue"},
    {"action": "draw_path", "params": {"points": [[-5,8,-4],[5,8,-4]]}, "comment": "Sky band"},
    ...
  ]
}
"""

STYLE_TEMPLATE = """
## Style Override: {name}

{description}

**Use these brushes**: {brushes}
**Color palette**: {palette}
**Brush size range**: {size_min} to {size_max}

**Stroke instructions**: {stroke_style}

You MUST follow this style. It overrides your default choices for brush type,
color palette, and stroke technique.
"""


class AIPainter:
    """Generates and executes paintings using Claude + Open Brush."""

    def __init__(
        self,
        client: OpenBrushClient,
        model: str = DEFAULT_MODEL,
    ):
        self.client = client
        self.model = model
        self._api_key, self._base_url = require_api_key()

    def paint(
        self,
        prompt: str,
        style: str | None = None,
    ) -> PaintingPlan:
        """Generate a painting plan from a text prompt and execute it."""
        print(f"\n  🎨 Generating painting plan...")
        print(f"     Prompt: {prompt}")
        if style:
            print(f"     Style: {style}")
        print(f"     Model: {self.model}")
        via = "OpenRouter" if self._base_url else "Anthropic"
        print(f"     Via: {via}")
        print()

        plan = self._generate_plan(prompt, style)
        print(f"  ✓ Plan generated: \"{plan.title}\" ({len(plan.commands)} commands)\n")

        self.client.execute_plan(plan)
        return plan

    def _generate_plan(self, prompt: str, style: str | None) -> PaintingPlan:
        """Ask Claude to decompose the scene into painting commands."""
        system = self._build_system_prompt(style)

        if self._base_url:
            # OpenRouter (OpenAI-compatible API)
            text = self._call_openrouter(system, prompt)
        else:
            # Direct Anthropic SDK
            text = self._call_anthropic(system, prompt)

        # Strip markdown code fences if Claude wraps the JSON
        text = re.sub(r"^```(?:json)?\s*", "", text.strip())
        text = re.sub(r"\s*```$", "", text.strip())

        try:
            data = json.loads(text)
        except json.JSONDecodeError as e:
            print(f"  ✗ Failed to parse Claude's response as JSON:")
            print(f"    {e}")
            print(f"    Raw response (first 500 chars):")
            print(f"    {text[:500]}")
            raise

        return PaintingPlan.model_validate(data)

    def _call_openrouter(self, system: str, prompt: str) -> str:
        """Call Claude via OpenRouter's OpenAI-compatible API."""
        resp = requests.post(
            f"{self._base_url}/chat/completions",
            headers={
                "Authorization": f"Bearer {self._api_key}",
                "Content-Type": "application/json",
                "HTTP-Referer": "https://serenade.gifts",
                "X-Title": "Open Brush AI",
            },
            json={
                "model": self.model,
                "max_tokens": 8192,
                "messages": [
                    {"role": "system", "content": system},
                    {"role": "user", "content": prompt},
                ],
            },
            timeout=60,
        )
        resp.raise_for_status()
        return resp.json()["choices"][0]["message"]["content"]

    def _call_anthropic(self, system: str, prompt: str) -> str:
        """Call Claude via the Anthropic SDK directly."""
        import anthropic
        client = anthropic.Anthropic(api_key=self._api_key)
        response = client.messages.create(
            model=self.model,
            max_tokens=8192,
            system=system,
            messages=[{"role": "user", "content": prompt}],
        )
        return response.content[0].text

    def _build_system_prompt(self, style: str | None) -> str:
        """Assemble the full system prompt with optional style override."""
        prompt = SYSTEM_PROMPT

        if style:
            profile = get_style(style)
            if profile:
                prompt += STYLE_TEMPLATE.format(
                    name=profile.name,
                    description=profile.description,
                    brushes=", ".join(profile.preferred_brushes),
                    palette=", ".join(profile.color_palette),
                    size_min=profile.brush_size_range[0],
                    size_max=profile.brush_size_range[1],
                    stroke_style=profile.stroke_style,
                )
            else:
                # Treat as a freeform style instruction
                prompt += f"\n\n## Style Override\n\nPaint in this style: {style}\n"

        return prompt
