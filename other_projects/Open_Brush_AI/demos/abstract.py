"""Abstract art demo — algorithmic particle brush art. No AI needed."""

import math
import random

from open_brush_ai.client import OpenBrushClient
from open_brush_ai.models import PaintCommand, PaintingPlan

# Visually interesting particle/effect brushes
EFFECT_BRUSHES = [
    "Fire", "Embers", "Stars", "Snow", "Bubbles", "Smoke",
    "NeonPulse", "Lightning", "Rainbow", "Sparks",
]

# Rich color palette
COLORS = [
    "#FF006E", "#FB5607", "#FFBE0B", "#8338EC", "#3A86FF",
    "#06D6A0", "#EF476F", "#118AB2", "#FFD166", "#073B4C",
]


def _spiral_points(
    center_x: float, center_y: float, center_z: float,
    radius: float, turns: float, points_per_turn: int = 12,
    rise: float = 0.0,
) -> list[list[float]]:
    """Generate points along a 3D spiral."""
    points = []
    total_points = int(turns * points_per_turn)
    for i in range(total_points):
        t = i / points_per_turn * 2 * math.pi
        r = radius * (1 - i / total_points * 0.3)  # Slight taper
        x = center_x + r * math.cos(t)
        z = center_z + r * math.sin(t)
        y = center_y + rise * (i / total_points)
        points.append([round(x, 2), round(y, 2), round(z, 2)])
    return points


def _burst_points(
    center_x: float, center_y: float, center_z: float,
    radius: float, num_rays: int = 8, points_per_ray: int = 5,
) -> list[list[list[float]]]:
    """Generate points for a starburst pattern (returns list of paths)."""
    paths = []
    for i in range(num_rays):
        angle = (2 * math.pi * i) / num_rays
        elevation = random.uniform(-0.5, 0.5)
        ray = []
        for j in range(points_per_ray):
            t = j / (points_per_ray - 1)
            r = radius * t
            x = center_x + r * math.cos(angle)
            z = center_z + r * math.sin(angle)
            y = center_y + r * elevation
            ray.append([round(x, 2), round(y, 2), round(z, 2)])
        paths.append(ray)
    return paths


def make_plan() -> PaintingPlan:
    """Generate an abstract art piece with spirals, bursts, and particles."""
    random.seed()  # True random each time
    commands: list[PaintCommand] = []

    # ── Central spiral ──
    brush = random.choice(EFFECT_BRUSHES)
    color = random.choice(COLORS)
    commands.extend([
        PaintCommand(
            action="set_brush", params={"type": brush},
            comment=f"Central spiral with {brush}"
        ),
        PaintCommand(
            action="set_color_html", params={"color": color},
        ),
        PaintCommand(
            action="set_size", params={"size": 0.4},
        ),
        PaintCommand(
            action="draw_path",
            params={"points": _spiral_points(0, 3, 0, 2.5, 3, rise=4)},
            comment="Rising spiral"
        ),
    ])

    # ── Starburst clusters ──
    for _ in range(3):
        cx = random.uniform(-4, 4)
        cy = random.uniform(1, 7)
        cz = random.uniform(-3, 3)
        brush = random.choice(EFFECT_BRUSHES)
        color = random.choice(COLORS)

        commands.append(PaintCommand(
            action="set_brush", params={"type": brush},
            comment=f"Starburst with {brush}"
        ))
        commands.append(PaintCommand(
            action="set_color_html", params={"color": color},
        ))
        commands.append(PaintCommand(
            action="set_size", params={"size": random.uniform(0.1, 0.5)},
        ))

        burst = _burst_points(cx, cy, cz, random.uniform(1, 2.5))
        for ray in burst:
            commands.append(PaintCommand(
                action="draw_path", params={"points": ray},
                comment="Burst ray"
            ))

    # ── Floating rings ──
    for i in range(4):
        y = 2 + i * 1.5
        radius = random.uniform(0.5, 1.5)
        points = []
        for j in range(24):
            angle = 2 * math.pi * j / 24
            x = radius * math.cos(angle)
            z = radius * math.sin(angle)
            points.append([round(x, 2), round(y, 2), round(z, 2)])
        points.append(points[0])  # Close the ring

        commands.extend([
            PaintCommand(
                action="set_brush",
                params={"type": random.choice(EFFECT_BRUSHES)},
                comment=f"Floating ring {i+1}"
            ),
            PaintCommand(
                action="set_color_html",
                params={"color": random.choice(COLORS)},
            ),
            PaintCommand(
                action="set_size",
                params={"size": random.uniform(0.1, 0.3)},
            ),
            PaintCommand(
                action="draw_path", params={"points": points},
            ),
        ])

    # ── Random accent strokes ──
    for _ in range(6):
        start = [
            random.uniform(-4, 4),
            random.uniform(0, 8),
            random.uniform(-3, 3),
        ]
        # Flowing curve with 4-6 points
        points = [start]
        for _ in range(random.randint(3, 5)):
            last = points[-1]
            points.append([
                round(last[0] + random.uniform(-1.5, 1.5), 2),
                round(last[1] + random.uniform(-1, 1.5), 2),
                round(last[2] + random.uniform(-1, 1), 2),
            ])

        commands.extend([
            PaintCommand(
                action="set_brush",
                params={"type": random.choice(EFFECT_BRUSHES)},
            ),
            PaintCommand(
                action="set_color_html",
                params={"color": random.choice(COLORS)},
            ),
            PaintCommand(
                action="set_size",
                params={"size": random.uniform(0.05, 0.4)},
            ),
            PaintCommand(
                action="draw_path", params={"points": points},
                comment="Accent stroke"
            ),
        ])

    return PaintingPlan(
        title="Abstract Particle Dream",
        description="Spirals, starbursts, and floating rings made from particle brushes",
        commands=commands,
    )


def run(client: OpenBrushClient) -> None:
    plan = make_plan()
    client.execute_plan(plan)
