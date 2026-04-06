"""Predefined artistic style profiles for AI painting."""

from __future__ import annotations

from pydantic import BaseModel


class StyleProfile(BaseModel):
    """Defines how a style affects AI painting behavior."""

    name: str
    description: str
    preferred_brushes: list[str]
    color_palette: list[str]
    brush_size_range: tuple[float, float]
    stroke_style: str


STYLES: dict[str, StyleProfile] = {
    "van_gogh": StyleProfile(
        name="Van Gogh",
        description="Thick, swirling brushstrokes with warm golden and deep blue tones. "
        "Impasto texture, visible brush marks, emotional intensity.",
        preferred_brushes=["OilPaint", "ThickPaint", "Marker"],
        color_palette=["#F4D03F", "#2E86C1", "#1A5276", "#D4AC0D", "#E67E22", "#1B4F72"],
        brush_size_range=(0.3, 1.5),
        stroke_style=(
            "Use swirling, curved paths — never straight lines. "
            "Create thick impasto strokes by using larger brush sizes. "
            "Layer strokes on top of each other for texture. "
            "Favor warm yellows and deep blues. Stars should be large swirling spirals."
        ),
    ),
    "anime": StyleProfile(
        name="Anime / Manga",
        description="Clean outlines, flat color fills, bold shadows. "
        "Cel-shaded look with strong contrast.",
        preferred_brushes=["Ink", "Marker", "Flat"],
        color_palette=["#FF6B9D", "#C7ECEE", "#FFC312", "#12CBC4", "#FDA7DF", "#ED4C67"],
        brush_size_range=(0.05, 0.8),
        stroke_style=(
            "Use clean, precise lines with the Ink brush for outlines. "
            "Fill areas with flat color using the Marker brush at larger sizes. "
            "Add bold shadow shapes — no gradients, just sharp shadow/light separation. "
            "Colors should be vibrant and saturated. Keep outlines thin (0.05-0.1)."
        ),
    ),
    "neon": StyleProfile(
        name="Neon Cyberpunk",
        description="Glowing neon lines on dark backgrounds. "
        "Electric colors, light trails, futuristic aesthetic.",
        preferred_brushes=["NeonPulse", "LightWire", "Electricity", "Light"],
        color_palette=["#FF00FF", "#00FFFF", "#FF006E", "#FFBE0B", "#8338EC", "#3A86FF"],
        brush_size_range=(0.05, 0.4),
        stroke_style=(
            "Use glowing brushes exclusively (NeonPulse, LightWire, Electricity). "
            "Create sharp geometric shapes — straight lines, angles, grids. "
            "Colors should be electric neon: hot pink, cyan, purple, electric blue. "
            "Add light trails and wire-like patterns. Think Tron / Blade Runner."
        ),
    ),
    "watercolor": StyleProfile(
        name="Watercolor",
        description="Soft, translucent washes with gentle color bleeding. "
        "Delicate and airy, with visible paper texture.",
        preferred_brushes=["WetPaint", "Light", "Splatter", "Smoke"],
        color_palette=["#AED6F1", "#F9E79F", "#FADBD8", "#D5F5E3", "#D2B4DE", "#F5CBA7"],
        brush_size_range=(0.5, 2.0),
        stroke_style=(
            "Use large, soft strokes that overlap and blend. "
            "Colors should be pastel and translucent-looking. "
            "Leave some areas 'unpainted' for the paper texture effect. "
            "Use Splatter brush for texture. Strokes should flow loosely — "
            "no hard edges or precise geometry. Let colors bleed into each other."
        ),
    ),
    "impressionist": StyleProfile(
        name="Impressionist",
        description="Dappled light, visible brushwork, emphasis on color and atmosphere "
        "over precise forms. Monet-like broken color technique.",
        preferred_brushes=["OilPaint", "Splatter", "Dots", "Marker"],
        color_palette=["#7FB3D8", "#F0B27A", "#82E0AA", "#F1948A", "#BB8FCE", "#F7DC6F"],
        brush_size_range=(0.1, 0.6),
        stroke_style=(
            "Use many small, distinct dabs of color rather than long strokes. "
            "Place complementary colors side by side — they mix optically. "
            "Don't outline anything. Build forms through accumulated color patches. "
            "Favor natural outdoor scenes. Light should feel dappled and shifting."
        ),
    ),
    "pixel": StyleProfile(
        name="Pixel Art / Retro",
        description="Blocky, grid-aligned shapes with limited color palettes. "
        "8-bit / 16-bit video game aesthetic.",
        preferred_brushes=["Flat", "Marker", "Ink"],
        color_palette=["#E74C3C", "#3498DB", "#2ECC71", "#F39C12", "#9B59B6", "#1ABC9C"],
        brush_size_range=(0.2, 0.5),
        stroke_style=(
            "Use only horizontal, vertical, and 45-degree diagonal lines. "
            "Build shapes as stacked rectangular blocks. "
            "Use a limited palette — max 6-8 colors per scene. "
            "Round numbers only for coordinates (snap to 0.5 grid). "
            "Think NES/SNES era: simple shapes, bold colors, no gradients."
        ),
    ),
    "fire": StyleProfile(
        name="Fire & Flame",
        description="Everything burns. Flickering flames, embers, molten flows. "
        "Warm palette from deep red to bright yellow.",
        preferred_brushes=["Fire", "Embers", "Smoke", "Light"],
        color_palette=["#FF0000", "#FF4500", "#FF8C00", "#FFD700", "#8B0000", "#FFA500"],
        brush_size_range=(0.1, 1.0),
        stroke_style=(
            "Use Fire and Embers brushes for primary elements. "
            "Strokes should flow upward like flames — start wide at bottom, taper up. "
            "Use Smoke brush for wisps at the edges. "
            "Colors transition from deep red/orange at the base to bright yellow at tips. "
            "Add floating ember particles with small Embers strokes."
        ),
    ),
}


def get_style(name: str) -> StyleProfile | None:
    """Look up a style by name (case-insensitive, underscores optional)."""
    key = name.lower().replace(" ", "_").replace("-", "_")
    return STYLES.get(key)


def list_styles() -> list[str]:
    """Return available style names."""
    return list(STYLES.keys())
