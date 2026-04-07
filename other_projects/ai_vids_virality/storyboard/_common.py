"""Shared helpers for the storyboard layer."""
from __future__ import annotations

import re
import shutil
from pathlib import Path
from typing import Optional


PLACEHOLDER_PATH = Path(__file__).resolve().parent / "placeholder.png"


def ensure_placeholder() -> Path:
    """Ensure the Phase 1 placeholder PNG exists. Generate via PIL if missing."""
    if PLACEHOLDER_PATH.exists() and PLACEHOLDER_PATH.stat().st_size > 0:
        return PLACEHOLDER_PATH
    PLACEHOLDER_PATH.parent.mkdir(parents=True, exist_ok=True)
    try:
        from PIL import Image  # type: ignore
    except ImportError as exc:  # pragma: no cover
        raise RuntimeError(
            "Pillow is required to generate the storyboard placeholder. "
            "Install it via requirements.txt."
        ) from exc
    Image.new("RGB", (512, 512), "#444").save(PLACEHOLDER_PATH)
    return PLACEHOLDER_PATH


def copy_placeholder(out_path: Path) -> None:
    """Copy the placeholder PNG into `out_path` (creating parent dirs)."""
    out_path.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(ensure_placeholder(), out_path)


_SLUG_RE = re.compile(r"[^a-z0-9]+")


def slugify(name: str, fallback: str = "character") -> str:
    cleaned = _SLUG_RE.sub("-", (name or "").strip().lower()).strip("-")
    return cleaned or fallback


__all__ = ["PLACEHOLDER_PATH", "copy_placeholder", "ensure_placeholder", "slugify"]
