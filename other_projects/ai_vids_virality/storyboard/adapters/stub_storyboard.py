"""Stub storyboard adapter.

Always copies `storyboard/placeholder.png` to `out_path`. This is both
the Phase 1 behavior and the Phase 4 fallback when no real adapter is
available (e.g. `GEMINI_API_KEY` not set).
"""
from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List, Optional

from storyboard._common import copy_placeholder, slugify
from storyboard.adapter import CharacterRef, Frame, StoryboardAdapter


class StubStoryboardAdapter(StoryboardAdapter):
    """Always-available adapter that writes the Phase 1 placeholder PNG."""

    adapter_id = "stub-storyboard-v1"

    def is_available(self) -> bool:
        return True

    def generate_character_ref(
        self,
        character: Dict[str, Any],
        style_guide: str,
        out_path: Path,
    ) -> CharacterRef:
        name = str(character.get("name") or "unnamed")
        copy_placeholder(out_path)
        return CharacterRef(
            name=name,
            slug=slugify(name),
            path=out_path,
            prompt="(stub) no prompt sent",
            adapter_id=self.adapter_id,
        )

    def generate_frame(
        self,
        beat: Dict[str, Any],
        character_refs: List[CharacterRef],
        style_guide: str,
        out_path: Path,
    ) -> Frame:
        copy_placeholder(out_path)
        return Frame(
            beat_n=int(beat.get("n", 1) or 1),
            path=out_path,
            prompt="(stub) no prompt sent",
            adapter_id=self.adapter_id,
        )


__all__ = ["StubStoryboardAdapter"]
