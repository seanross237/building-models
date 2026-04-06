"""Landscape demo — a simple mountain scene. No AI needed."""

from open_brush_ai.client import OpenBrushClient
from open_brush_ai.models import PaintCommand, PaintingPlan


def make_plan() -> PaintingPlan:
    """Create a hardcoded mountain landscape."""
    commands = [
        # ── Sky ──
        PaintCommand(
            action="set_brush", params={"type": "Light"},
            comment="Soft sky fill"
        ),
        PaintCommand(
            action="set_color_html", params={"color": "#87CEEB"},
            comment="Sky blue"
        ),
        PaintCommand(
            action="set_size", params={"size": 2.0},
        ),
        # Wide sky bands
        PaintCommand(
            action="draw_path",
            params={"points": [[-5, 8, -3], [5, 8, -3]]},
            comment="Upper sky"
        ),
        PaintCommand(
            action="set_color_html", params={"color": "#B0D4E8"},
        ),
        PaintCommand(
            action="draw_path",
            params={"points": [[-5, 6.5, -3], [5, 6.5, -3]]},
            comment="Lower sky"
        ),

        # ── Sun ──
        PaintCommand(
            action="set_brush", params={"type": "Embers"},
            comment="Glowing sun"
        ),
        PaintCommand(
            action="set_color_html", params={"color": "#FFD700"},
            comment="Golden"
        ),
        PaintCommand(
            action="set_size", params={"size": 1.0},
        ),
        PaintCommand(
            action="draw_path",
            params={"points": [
                [3, 7.5, -4], [3.3, 7.8, -4], [3.6, 7.5, -4],
                [3.3, 7.2, -4], [3, 7.5, -4],
            ]},
            comment="Sun circle"
        ),

        # ── Far mountain ──
        PaintCommand(
            action="set_brush", params={"type": "Ink"},
            comment="Distant mountain"
        ),
        PaintCommand(
            action="set_color_html", params={"color": "#6B7B8D"},
            comment="Misty blue-gray"
        ),
        PaintCommand(
            action="set_size", params={"size": 0.8},
        ),
        PaintCommand(
            action="draw_path",
            params={"points": [
                [-5, 2, -4], [-3, 5.5, -4], [-1, 3, -4],
                [1, 6, -4], [3, 3.5, -4], [5, 4, -4], [5, 2, -4],
            ]},
            comment="Mountain ridge silhouette"
        ),

        # ── Near mountain ──
        PaintCommand(
            action="set_color_html", params={"color": "#4A5568"},
            comment="Darker near mountain"
        ),
        PaintCommand(
            action="set_size", params={"size": 1.0},
        ),
        PaintCommand(
            action="draw_path",
            params={"points": [
                [-5, 1, -2], [-2, 4.5, -2], [0, 2, -2],
                [2, 5, -2], [4, 2.5, -2], [5, 1, -2],
            ]},
            comment="Foreground mountain"
        ),

        # ── Snow caps ──
        PaintCommand(
            action="set_brush", params={"type": "Snow"},
            comment="Mountain snow"
        ),
        PaintCommand(
            action="set_color_html", params={"color": "white"},
        ),
        PaintCommand(
            action="set_size", params={"size": 0.3},
        ),
        PaintCommand(
            action="draw_path",
            params={"points": [
                [-2.5, 4.2, -2], [-2, 4.5, -2], [-1.5, 4.2, -2],
            ]},
            comment="Left peak snow"
        ),
        PaintCommand(
            action="draw_path",
            params={"points": [
                [1.5, 4.7, -2], [2, 5, -2], [2.5, 4.7, -2],
            ]},
            comment="Right peak snow"
        ),

        # ── Ground ──
        PaintCommand(
            action="set_brush", params={"type": "OilPaint"},
            comment="Grassy ground"
        ),
        PaintCommand(
            action="set_color_html", params={"color": "#2D5016"},
            comment="Dark green"
        ),
        PaintCommand(
            action="set_size", params={"size": 1.5},
        ),
        PaintCommand(
            action="draw_path",
            params={"points": [[-5, 0.5, 0], [0, 0.8, 0], [5, 0.5, 0]]},
            comment="Ground plane"
        ),
        PaintCommand(
            action="set_color_html", params={"color": "#3A6B1E"},
            comment="Lighter green layer"
        ),
        PaintCommand(
            action="draw_path",
            params={"points": [[-5, 0.3, 0.5], [0, 0.5, 0.5], [5, 0.3, 0.5]]},
            comment="Foreground grass"
        ),

        # ── Trees ──
        PaintCommand(
            action="set_brush", params={"type": "Ink"},
            comment="Tree trunks"
        ),
        PaintCommand(
            action="set_color_html", params={"color": "#5C4033"},
            comment="Brown trunk"
        ),
        PaintCommand(
            action="set_size", params={"size": 0.1},
        ),
        PaintCommand(
            action="draw_path",
            params={"points": [[-3, 0.5, 0], [-3, 2, 0]]},
            comment="Left tree trunk"
        ),
        PaintCommand(
            action="draw_path",
            params={"points": [[3.5, 0.5, 1], [3.5, 1.8, 1]]},
            comment="Right tree trunk"
        ),
        # Tree foliage
        PaintCommand(
            action="set_brush", params={"type": "Splatter"},
            comment="Leafy canopy"
        ),
        PaintCommand(
            action="set_color_html", params={"color": "#228B22"},
            comment="Forest green"
        ),
        PaintCommand(
            action="set_size", params={"size": 0.6},
        ),
        PaintCommand(
            action="draw_path",
            params={"points": [
                [-3.5, 2, 0], [-3, 2.8, 0], [-2.5, 2, 0],
            ]},
            comment="Left tree canopy"
        ),
        PaintCommand(
            action="draw_path",
            params={"points": [
                [3, 1.8, 1], [3.5, 2.5, 1], [4, 1.8, 1],
            ]},
            comment="Right tree canopy"
        ),
    ]

    return PaintingPlan(
        title="Mountain Landscape",
        description="A serene mountain scene with snow-capped peaks, golden sun, and evergreen trees",
        commands=commands,
    )


def run(client: OpenBrushClient) -> None:
    plan = make_plan()
    client.execute_plan(plan)
