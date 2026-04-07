"""Stub critic adapter.

Always available, deterministic. The shot check passes everything (so the
retry loop never fires when the stub is in charge), and the full critique
returns a hardcoded scored report. This is what the pipeline routes to
when neither the Gemini nor the Claude adapter is available.
"""
from __future__ import annotations

import hashlib
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

from critic.adapter import CriticAdapter, ShotReport, SketchCritique


def _now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


class StubCritic(CriticAdapter):
    adapter_id = "stub-critic-v1"

    def is_available(self) -> bool:
        return True

    def check_shot(
        self,
        clip_path: Path,
        expected_frame: Path,
        character_refs: List[Path],
        beat_metadata: Dict[str, Any],
    ) -> ShotReport:
        return ShotReport(
            beat_n=int(beat_metadata.get("n", 1) or 1),
            passed=True,
            score=8,
            issues=[],
            suggestions=[],
            adapter_id=self.adapter_id,
            raw_response="(stub) deterministic pass",
        )

    def critique_sketch(
        self,
        final_cut_path: Path,
        sketch_metadata: Dict[str, Any],
    ) -> SketchCritique:
        return SketchCritique(
            sketch_id=str(sketch_metadata.get("sketch_id", "unknown")),
            overall_score=7,
            axes={
                "comedic_timing": 7,
                "pacing": 6,
                "punchline_landing": 7,
                "audio_clarity": 8,
                "character_consistency": 7,
            },
            issues=[
                "second beat lingers half a second too long",
                "background music is barely audible in the final beat",
            ],
            fix_suggestions=[
                "tighten the second beat by half a second",
                "raise the music bed in the final shot",
            ],
            is_funny=True,
            verdict="passes the stub bar — clean enough to publish",
            adapter_id=self.adapter_id,
            raw_response="(stub) deterministic critique",
        )


__all__ = ["StubCritic"]
