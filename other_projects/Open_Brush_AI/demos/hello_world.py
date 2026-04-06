"""Hello World demo — draws 'HI' with Neon Pulse brush. No AI needed."""

from open_brush_ai.client import OpenBrushClient
from open_brush_ai.models import PaintCommand, PaintingPlan


def make_plan() -> PaintingPlan:
    """Create a hardcoded plan that draws 'HI' in 3D space."""
    commands = [
        # Setup
        PaintCommand(
            action="set_brush", params={"type": "NeonPulse"},
            comment="Glowing neon letters"
        ),
        PaintCommand(
            action="set_color_html", params={"color": "#00FFFF"},
            comment="Cyan glow"
        ),
        PaintCommand(
            action="set_size", params={"size": 0.15},
            comment="Medium stroke width"
        ),

        # Letter H — left vertical
        PaintCommand(
            action="draw_path",
            params={"points": [[-2, 0, 0], [-2, 3, 0]]},
            comment="H left stroke"
        ),
        # Letter H — right vertical
        PaintCommand(
            action="draw_path",
            params={"points": [[-0.5, 0, 0], [-0.5, 3, 0]]},
            comment="H right stroke"
        ),
        # Letter H — crossbar
        PaintCommand(
            action="draw_path",
            params={"points": [[-2, 1.5, 0], [-0.5, 1.5, 0]]},
            comment="H crossbar"
        ),

        # Letter I — vertical
        PaintCommand(
            action="set_color_html", params={"color": "#FF00FF"},
            comment="Switch to magenta"
        ),
        PaintCommand(
            action="draw_path",
            params={"points": [[1, 0, 0], [1, 3, 0]]},
            comment="I vertical stroke"
        ),
        # Letter I — top serif
        PaintCommand(
            action="draw_path",
            params={"points": [[0.3, 3, 0], [1.7, 3, 0]]},
            comment="I top serif"
        ),
        # Letter I — bottom serif
        PaintCommand(
            action="draw_path",
            params={"points": [[0.3, 0, 0], [1.7, 0, 0]]},
            comment="I bottom serif"
        ),

        # Exclamation dot
        PaintCommand(
            action="set_brush", params={"type": "Stars"},
            comment="Sparkly dot"
        ),
        PaintCommand(
            action="set_size", params={"size": 0.3},
        ),
        PaintCommand(
            action="draw_path",
            params={"points": [[3, 0, 0], [3, 0.1, 0]]},
            comment="! dot (sparkle)"
        ),

        # Exclamation line
        PaintCommand(
            action="set_brush", params={"type": "NeonPulse"},
        ),
        PaintCommand(
            action="set_size", params={"size": 0.15},
        ),
        PaintCommand(
            action="set_color_html", params={"color": "#FFFF00"},
            comment="Yellow exclamation"
        ),
        PaintCommand(
            action="draw_path",
            params={"points": [[3, 0.8, 0], [3, 3, 0]]},
            comment="! line"
        ),
    ]

    return PaintingPlan(
        title="HI!",
        description="The letters HI! drawn in glowing neon — a hello from AI",
        commands=commands,
    )


def run(client: OpenBrushClient) -> None:
    plan = make_plan()
    client.execute_plan(plan)
