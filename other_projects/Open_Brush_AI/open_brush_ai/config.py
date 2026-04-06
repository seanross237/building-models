"""Configuration and settings for Open Brush AI."""

from __future__ import annotations

import os
from enum import Enum
from pathlib import Path

from dotenv import load_dotenv

# Load .env from project root
_project_root = Path(__file__).parent.parent
load_dotenv(_project_root / ".env")


class ExecutionMode(str, Enum):
    LIVE = "live"
    MOCK = "mock"
    RECORD = "record"


# API settings
OPEN_BRUSH_URL = os.environ.get("OPEN_BRUSH_URL", "http://localhost:40074/api/v1")
OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY", "")
ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"
DEFAULT_MODEL = os.environ.get("OPEN_BRUSH_AI_MODEL", "anthropic/claude-sonnet-4")
COMMAND_DELAY = float(os.environ.get("COMMAND_DELAY", "0.3"))

# Paths
RECORDINGS_DIR = _project_root / "recordings"
RECORDINGS_DIR.mkdir(exist_ok=True)


def require_api_key() -> tuple[str, str | None]:
    """Get API key and optional base URL. Prefers OpenRouter, falls back to Anthropic."""
    if OPENROUTER_API_KEY:
        return OPENROUTER_API_KEY, OPENROUTER_BASE_URL
    if ANTHROPIC_API_KEY:
        return ANTHROPIC_API_KEY, None
    raise RuntimeError(
        "No API key set. Add OPENROUTER_API_KEY or ANTHROPIC_API_KEY to .env"
    )
