"""File-backed leaderboard tracking per-model approval rates.

State lives at `data/leaderboard.json`:

    {
      "claude-opus":     {"total": 12, "approved": 5, "rejected": 7},
      "gpt-5":           {"total": 12, "approved": 3, "rejected": 9},
      "gemini-2.5-pro":  {"total": 12, "approved": 4, "rejected": 8}
    }

`record_generation` increments `total` once per generated PremiseResult.
`record_decision` increments `approved` or `rejected` when the human acts.
`get_leaderboard` returns the full payload for the API.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, Optional


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PATH = PROJECT_ROOT / "data" / "leaderboard.json"


class Leaderboard:
    def __init__(self, path: Optional[Path] = None) -> None:
        self.path = Path(path or DEFAULT_PATH)

    # ----------------------------------------------------------------- IO

    def _read(self) -> Dict[str, Dict[str, int]]:
        if not self.path.exists():
            return {}
        try:
            data = json.loads(self.path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            return {}
        if not isinstance(data, dict):
            return {}
        cleaned: Dict[str, Dict[str, int]] = {}
        for model_id, stats in data.items():
            if not isinstance(stats, dict):
                continue
            cleaned[str(model_id)] = {
                "total": int(stats.get("total", 0) or 0),
                "approved": int(stats.get("approved", 0) or 0),
                "rejected": int(stats.get("rejected", 0) or 0),
            }
        return cleaned

    def _write(self, data: Dict[str, Dict[str, int]]) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(
            json.dumps(data, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )

    @staticmethod
    def _row(stats: Dict[str, int]) -> Dict[str, int]:
        return {
            "total": int(stats.get("total", 0) or 0),
            "approved": int(stats.get("approved", 0) or 0),
            "rejected": int(stats.get("rejected", 0) or 0),
        }

    # ----------------------------------------------------------------- mutators

    def record_generation(self, model_id: str) -> None:
        data = self._read()
        row = data.get(model_id, {"total": 0, "approved": 0, "rejected": 0})
        row["total"] = int(row.get("total", 0)) + 1
        data[model_id] = self._row(row)
        self._write(data)

    def record_decision(self, model_id: str, approved: bool) -> None:
        data = self._read()
        row = data.get(model_id, {"total": 0, "approved": 0, "rejected": 0})
        if approved:
            row["approved"] = int(row.get("approved", 0)) + 1
        else:
            row["rejected"] = int(row.get("rejected", 0)) + 1
        data[model_id] = self._row(row)
        self._write(data)

    # ----------------------------------------------------------------- read

    def get_leaderboard(self) -> Dict[str, Any]:
        data = self._read()
        rows = []
        for model_id, stats in sorted(data.items()):
            total = int(stats.get("total", 0) or 0)
            approved = int(stats.get("approved", 0) or 0)
            rejected = int(stats.get("rejected", 0) or 0)
            decided = approved + rejected
            rate = (approved / decided) if decided > 0 else 0.0
            rows.append(
                {
                    "model_id": model_id,
                    "total": total,
                    "approved": approved,
                    "rejected": rejected,
                    "approval_rate": round(rate, 3),
                }
            )
        return {"models": rows}


__all__ = ["Leaderboard"]
