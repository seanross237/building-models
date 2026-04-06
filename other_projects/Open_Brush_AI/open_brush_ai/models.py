"""Pydantic models for Open Brush AI commands."""

from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel


class PaintCommand(BaseModel):
    """A single command to send to Open Brush."""

    action: Literal[
        "set_brush",
        "set_color_rgb",
        "set_color_html",
        "set_size",
        "move_to",
        "move_by",
        "draw_path",
        "draw_stroke",
        "draw_svg_path",
        "look_at",
        "turn_y",
        "turn_x",
        "turn_z",
        "draw_forward",
        "pause",
    ]
    params: dict[str, Any]
    comment: str = ""


class PaintingPlan(BaseModel):
    """Full painting plan returned by Claude."""

    title: str
    description: str
    commands: list[PaintCommand]


class Recording(BaseModel):
    """A saved recording with metadata."""

    version: str = "1.0"
    created_at: str
    prompt: str
    style: str | None = None
    plan: PaintingPlan
