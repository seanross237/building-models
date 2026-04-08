"""End-to-end critic orchestration.

`select_critic_adapter()` walks `config/critic.yaml` and returns the
first enabled adapter whose `is_available()` is True. The video pipeline
calls this for shot-level checks; the backend's `approve_storyboard`
chain calls `run_full_critique()` for the headline judgment after
stitching.
"""
from __future__ import annotations

import importlib
import json
import logging
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

from critic.adapter import CriticAdapter, ShotReport, SketchCritique
from critic.adapters.stub_critic import StubCritic
from state.store import Sketch, Store


LOG = logging.getLogger("critic.pipeline")

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CRITIC_CONFIG = PROJECT_ROOT / "config" / "critic.yaml"


# ----------------------------------------------------------------- config


def load_critic_config(path: Path = DEFAULT_CRITIC_CONFIG) -> Dict[str, Any]:
    if not path.exists():
        return {
            "shot_check": {"max_retries": 2, "enabled": True},
            "full_sketch": {"enabled": True},
            "routing": {"default": ["stub"]},
            "adapters": [],
        }
    try:
        import yaml  # type: ignore
        data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    except Exception as exc:
        LOG.warning("could not read critic.yaml: %s", exc)
        return {
            "shot_check": {"max_retries": 2, "enabled": True},
            "full_sketch": {"enabled": True},
            "routing": {"default": ["stub"]},
            "adapters": [],
        }
    if not isinstance(data, dict):
        return {
            "shot_check": {"max_retries": 2, "enabled": True},
            "full_sketch": {"enabled": True},
            "routing": {"default": ["stub"]},
            "adapters": [],
        }
    data.setdefault("shot_check", {"max_retries": 2, "enabled": True})
    data.setdefault("full_sketch", {"enabled": True})
    data.setdefault("routing", {"default": ["stub"]})
    data.setdefault("adapters", [])
    return data


def _instantiate(entry: Dict[str, Any]) -> Optional[CriticAdapter]:
    dotted = entry.get("adapter")
    if not dotted:
        return None
    module_path, _, class_name = str(dotted).rpartition(".")
    if not module_path or not class_name:
        return None
    try:
        module = importlib.import_module(module_path)
        cls = getattr(module, class_name)
    except Exception as exc:
        LOG.warning("could not import critic adapter %s: %s", dotted, exc)
        return None
    cfg = dict(entry.get("config") or {})
    if "id" in entry:
        cfg["id"] = entry["id"]
    try:
        return cls(config=cfg)
    except Exception as exc:
        LOG.warning("could not instantiate critic adapter %s: %s", dotted, exc)
        return None


def load_critic_adapters(
    config: Optional[Dict[str, Any]] = None,
) -> Dict[str, CriticAdapter]:
    cfg = config if config is not None else load_critic_config()
    out: Dict[str, CriticAdapter] = {}
    for entry in cfg.get("adapters") or []:
        if not entry.get("enabled"):
            continue
        adapter = _instantiate(entry)
        if adapter is None:
            continue
        out[adapter.adapter_id] = adapter
    return out


def select_critic_adapter(
    config: Optional[Dict[str, Any]] = None,
    adapters: Optional[Dict[str, CriticAdapter]] = None,
) -> CriticAdapter:
    cfg = config if config is not None else load_critic_config()
    if adapters is None:
        adapters = load_critic_adapters(cfg)
    routing = (cfg.get("routing") or {}).get("default") or []
    for adapter_id in routing:
        adapter = adapters.get(adapter_id)
        if adapter is None:
            continue
        try:
            available = adapter.is_available()
        except Exception as exc:
            LOG.warning("is_available() raised for %s: %s", adapter_id, exc)
            continue
        if available:
            return adapter
    return StubCritic()


def get_max_retries(config: Optional[Dict[str, Any]] = None) -> int:
    cfg = config if config is not None else load_critic_config()
    sc = cfg.get("shot_check") or {}
    if not sc.get("enabled", True):
        return 0
    try:
        return int(sc.get("max_retries", 2) or 0)
    except (TypeError, ValueError):
        return 2


# ----------------------------------------------------------------- helpers


def _now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _build_sketch_metadata(sketch: Sketch) -> Dict[str, Any]:
    premise = sketch.premise or {}
    return {
        "sketch_id": sketch.id,
        "logline": premise.get("logline", ""),
        "tone": premise.get("tone", ""),
        "twist": premise.get("twist", ""),
        "target_length_sec": int(premise.get("target_length_sec", 30) or 30),
        "beat_count": len(sketch.beats or []),
    }


# ----------------------------------------------------------------- public API


def run_full_critique(
    store: Store,
    sketch_id: str,
    *,
    adapter: Optional[CriticAdapter] = None,
    config: Optional[Dict[str, Any]] = None,
) -> SketchCritique:
    """Run the full-sketch critique on the assembled final.mp4.

    Persists the report to `data/sketches/{id}/critic.json` and writes
    a copy onto the sketch's `critic_report` field. Returns the
    critique dataclass.
    """
    sketch = store.get_sketch(sketch_id)
    cfg = config if config is not None else load_critic_config()
    if adapter is None:
        adapter = select_critic_adapter(cfg)

    final_path = store.sketch_final_path(sketch_id)
    metadata = _build_sketch_metadata(sketch)
    critique = adapter.critique_sketch(final_path, metadata)
    if critique.error:
        LOG.warning(
            "critic adapter %s returned error for %s: %s",
            critique.adapter_id,
            sketch_id,
            critique.error,
        )

    payload = critique.to_dict()
    payload["scored_at"] = _now()
    (store.sketch_dir(sketch_id) / "critic.json").write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    sketch.critic_report = payload
    store.save_sketch(sketch)
    return critique


def shot_check_clip(
    clip_path: Path,
    expected_frame: Optional[Path],
    character_refs: List[Path],
    beat_metadata: Dict[str, Any],
    *,
    adapter: Optional[CriticAdapter] = None,
    config: Optional[Dict[str, Any]] = None,
) -> ShotReport:
    """Run a single shot check via the routed critic adapter."""
    if adapter is None:
        adapter = select_critic_adapter(config)
    expected = expected_frame if expected_frame is not None else Path("/nonexistent")
    return adapter.check_shot(clip_path, expected, character_refs, beat_metadata)


__all__ = [
    "get_max_retries",
    "load_critic_adapters",
    "load_critic_config",
    "run_full_critique",
    "select_critic_adapter",
    "shot_check_clip",
]
