"""Top-level radar pipeline.

Phase 2 reads `config/sources.yaml`, dynamically imports each enabled
collector module, calls its `fetch(store, config=...)`, then runs the
analyzer. Phase 3 swaps the stub idea factory for the multi-model factory
in `idea_factory/factory.py` (still falls back to the offline stub when
`use_stub_factory=True` is passed, which the Phase 1/2 tests use).
"""
from __future__ import annotations

# Phase 8: load .env so cron / one-shot CLI invocations of the radar
# pick up FAL_KEY and friends without the user having to source the
# file manually. override=False so anything in the environment wins.
try:
    from dotenv import load_dotenv as _load_dotenv
    _load_dotenv(override=False)
except ImportError:
    pass

import importlib
import logging
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional

from analyzers.score_signals import analyze as score_signals
from idea_factory import factory as multi_model_factory
from idea_factory import stub_factory
from state.store import Store


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SOURCES_PATH = PROJECT_ROOT / "config" / "sources.yaml"
LOG = logging.getLogger("pipelines.run_skeleton")


def _load_sources(path: Path) -> List[Dict[str, Any]]:
    if not path.exists():
        return []
    try:
        import yaml  # type: ignore
    except Exception as exc:
        LOG.warning("pyyaml unavailable, cannot read sources.yaml: %s", exc)
        return []
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    collectors = data.get("collectors") if isinstance(data, dict) else None
    if not isinstance(collectors, list):
        return []
    return [c for c in collectors if isinstance(c, dict)]


def _resolve_fetch(module_path: str) -> Optional[Callable[..., List[str]]]:
    try:
        module = importlib.import_module(module_path)
    except Exception as exc:
        LOG.warning("could not import collector %s: %s", module_path, exc)
        return None
    fn = getattr(module, "fetch", None)
    if not callable(fn):
        LOG.warning("collector %s has no callable fetch()", module_path)
        return None
    return fn


def _call_fetch(fn: Callable[..., List[str]], store: Store, config: Dict[str, Any]) -> List[str]:
    try:
        return fn(store, config=config)
    except TypeError:
        # Older collectors (e.g. the stub) don't accept a config kwarg.
        return fn(store)


def run(
    root: Optional[Path] = None,
    sources_path: Optional[Path] = None,
    analyzer_threshold: Optional[int] = None,
    use_stub_factory: bool = False,
    models_config_path: Optional[Path] = None,
) -> Dict[str, Any]:
    """Run the radar pipeline against the given data root.

    `analyzer_threshold` lets tests bypass the lens cutoff so deterministic
    fixture signals always promote. `use_stub_factory=True` keeps the
    Phase 1 hardcoded factory path active for offline tests; the production
    default uses the multi-model factory which calls real LLMs.
    """
    store = Store(root=root or PROJECT_ROOT / "data")
    sources = _load_sources(sources_path or DEFAULT_SOURCES_PATH)

    per_source: Dict[str, int] = {}
    new_signals: List[str] = []
    for entry in sources:
        if not entry.get("enabled"):
            continue
        collector_id = str(entry.get("id", "unknown"))
        module_path = entry.get("module") or f"collectors.{collector_id}.fetch"
        fetch_fn = _resolve_fetch(str(module_path))
        if fetch_fn is None:
            per_source[collector_id] = 0
            continue
        config = entry.get("config") or {}
        try:
            ids = _call_fetch(fetch_fn, store, config)
        except Exception as exc:
            LOG.warning("collector %s failed: %s", collector_id, exc)
            ids = []
        per_source[collector_id] = len(ids)
        new_signals.extend(ids)

    if analyzer_threshold is not None:
        analyzed = score_signals.analyze_pending(store, threshold=analyzer_threshold)
    else:
        analyzed = score_signals.analyze_pending(store)

    if use_stub_factory:
        new_sketches = stub_factory.run_factory(store)
    else:
        new_sketches = multi_model_factory.run_factory(
            store,
            models_config_path=models_config_path or multi_model_factory.DEFAULT_MODELS_PATH,
        )

    return {
        "per_source": per_source,
        "new_signals": new_signals,
        "analyzed": analyzed,
        "new_sketches": new_sketches,
    }


def main() -> int:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(name)s %(message)s")
    summary = run()
    print(
        "Phase 2 pipeline run: "
        f"{len(summary['new_signals'])} signals, "
        f"{len(summary['analyzed'])} analyzed, "
        f"{len(summary['new_sketches'])} sketches"
    )
    for source_id, count in summary["per_source"].items():
        print(f"  {source_id}: {count}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
