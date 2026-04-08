"""Publishing pipeline.

`run_publishers(sketch, store)` reads `config/publishing.yaml`, walks
every enabled destination, calls `publish()` on each, and returns the
list of `PublishResult` records. The caller decides what to do with
the results — the backend transitions the sketch to PUBLISHED if at
least one result succeeded.
"""
from __future__ import annotations

import importlib
import logging
from pathlib import Path
from typing import Any, Dict, List, Optional

from publishing.adapter import Publisher, PublishResult
from state.store import Sketch, Store


LOG = logging.getLogger("publishing.pipeline")

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PUBLISHING_CONFIG = PROJECT_ROOT / "config" / "publishing.yaml"


def load_publishing_config(path: Path = DEFAULT_PUBLISHING_CONFIG) -> Dict[str, Any]:
    if not path.exists():
        return {"destinations": []}
    try:
        import yaml  # type: ignore
        data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    except Exception as exc:
        LOG.warning("could not read publishing.yaml: %s", exc)
        return {"destinations": []}
    if not isinstance(data, dict):
        return {"destinations": []}
    data.setdefault("destinations", [])
    return data


def _instantiate(entry: Dict[str, Any]) -> Optional[Publisher]:
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
        LOG.warning("could not import publisher %s: %s", dotted, exc)
        return None
    cfg = dict(entry.get("config") or {})
    if "id" in entry and "id" not in cfg:
        cfg["id"] = entry["id"]
    try:
        return cls(config=cfg)
    except Exception as exc:
        LOG.warning("could not instantiate publisher %s: %s", dotted, exc)
        return None


def load_publishers(config: Optional[Dict[str, Any]] = None) -> List[Publisher]:
    cfg = config if config is not None else load_publishing_config()
    out: List[Publisher] = []
    for entry in cfg.get("destinations") or []:
        if not entry.get("enabled"):
            continue
        publisher = _instantiate(entry)
        if publisher is not None:
            out.append(publisher)
    return out


def run_publishers(
    sketch: Sketch,
    store: Store,
    *,
    publishers: Optional[List[Publisher]] = None,
    config: Optional[Dict[str, Any]] = None,
) -> List[PublishResult]:
    """Run every enabled publisher against a sketch and return the results.

    Adapters never raise, but we wrap the call in a safety net anyway.
    """
    if publishers is None:
        publishers = load_publishers(config)
    results: List[PublishResult] = []
    for publisher in publishers:
        try:
            result = publisher.publish(sketch, store)
        except Exception as exc:  # safety net
            LOG.warning(
                "publisher %s raised (treated as failure): %s",
                getattr(publisher, "destination_id", "?"),
                exc,
            )
            result = PublishResult(
                destination_id=getattr(publisher, "destination_id", "unknown"),
                success=False,
                error=f"publisher raised: {exc}",
            )
        results.append(result)
    return results


__all__ = [
    "load_publishers",
    "load_publishing_config",
    "run_publishers",
]
