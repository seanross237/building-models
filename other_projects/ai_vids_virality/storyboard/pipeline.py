"""End-to-end storyboard generation orchestration.

`run_storyboard(store, sketch_id)` is the function the backend calls
after a user approves a premise. It:

    1. Loads the sketch (asserting SCRIPTED status).
    2. Generates a beat sheet with the Phase 3 model adapter (Claude CLI).
    3. Generates one character reference image per unique character.
    4. Generates a start frame per beat, conditioned on the character refs.
    5. Writes `data/sketches/{id}/storyboard.json` summarising everything.
    6. Transitions the sketch to STORYBOARD_REVIEW.

Adapter selection is driven by `config/storyboard.yaml`: the first
enabled adapter whose `is_available()` returns True wins. In practice
that's `GeminiImageAdapter` when `GEMINI_API_KEY` is set, falling back
to `StubStoryboardAdapter` otherwise.
"""
from __future__ import annotations

import hashlib
import importlib
import json
import logging
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

from idea_factory.adapter import ModelAdapter
from state.machine import Status
from state.store import Sketch, Store
from storyboard._common import slugify
from storyboard.adapter import CharacterRef, Frame, StoryboardAdapter
from storyboard.beats import generate_beats


LOG = logging.getLogger("storyboard.pipeline")

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_STORYBOARD_CONFIG = PROJECT_ROOT / "config" / "storyboard.yaml"


# ----------------------------------------------------------------- config


def _load_storyboard_config(path: Path = DEFAULT_STORYBOARD_CONFIG) -> Dict[str, Any]:
    if not path.exists():
        return {
            "adapters": [],
            "default_style_guide": "",
            "frame_size": "1024x1024",
            "character_ref_size": "512x512",
        }
    try:
        import yaml  # type: ignore
        data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    except Exception as exc:
        LOG.warning("could not read storyboard.yaml: %s", exc)
        return {"adapters": [], "default_style_guide": "", "frame_size": "1024x1024"}
    if not isinstance(data, dict):
        return {"adapters": [], "default_style_guide": "", "frame_size": "1024x1024"}
    return data


def _instantiate_adapter(entry: Dict[str, Any]) -> Optional[StoryboardAdapter]:
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
        LOG.warning("could not import storyboard adapter %s: %s", dotted, exc)
        return None
    try:
        return cls(config=dict(entry.get("config") or {}))
    except Exception as exc:
        LOG.warning("could not instantiate storyboard adapter %s: %s", dotted, exc)
        return None


def select_storyboard_adapter(
    config: Optional[Dict[str, Any]] = None,
) -> StoryboardAdapter:
    """Return the first enabled adapter whose `is_available()` is True.

    Never raises. Falls back to the stub adapter if no config entry is
    usable — that keeps the pipeline running in any environment.
    """
    cfg = config if config is not None else _load_storyboard_config()
    for entry in cfg.get("adapters") or []:
        if not entry.get("enabled"):
            continue
        adapter = _instantiate_adapter(entry)
        if adapter is None:
            continue
        try:
            available = adapter.is_available()
        except Exception as exc:
            LOG.warning("is_available() raised for %s: %s", adapter.adapter_id, exc)
            continue
        if available:
            return adapter
    # Absolute last resort: import the stub directly.
    from storyboard.adapters.stub_storyboard import StubStoryboardAdapter
    return StubStoryboardAdapter()


# ----------------------------------------------------------------- helpers


def _now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _unique_characters(beats: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Collect unique characters across every beat, keyed by name."""
    seen: Dict[str, Dict[str, Any]] = {}
    for beat in beats:
        for char in beat.get("characters") or []:
            if isinstance(char, dict):
                name = str(char.get("name") or "").strip()
                if not name:
                    continue
                if name not in seen:
                    seen[name] = {
                        "name": name,
                        "description": str(char.get("description") or "").strip(),
                    }
            elif isinstance(char, str) and char.strip():
                name = char.strip()
                if name not in seen:
                    seen[name] = {"name": name, "description": ""}
    return list(seen.values())


def _frame_filename(beat_n: int) -> str:
    return f"beat-{beat_n:02d}-start.png"


def _ref_filename(slug: str) -> str:
    return f"{slug}.png"


# ----------------------------------------------------------------- public API


def run_storyboard(
    store: Store,
    sketch_id: str,
    *,
    model_adapter: Optional[ModelAdapter] = None,
    storyboard_adapter: Optional[StoryboardAdapter] = None,
    storyboard_config: Optional[Dict[str, Any]] = None,
    transition: bool = True,
) -> Dict[str, Any]:
    """Generate beats, character refs, and per-beat frames for a sketch.

    `model_adapter` is optional — tests inject a fake. In production the
    pipeline picks the Phase 3 default (Claude CLI) via `_default_model_adapter`.
    `storyboard_adapter` is also optional — tests inject the stub.
    """
    sketch = store.get_sketch(sketch_id)

    cfg = storyboard_config if storyboard_config is not None else _load_storyboard_config()
    style_guide = str(cfg.get("default_style_guide") or "").strip()

    if storyboard_adapter is None:
        storyboard_adapter = select_storyboard_adapter(cfg)
    if model_adapter is None:
        model_adapter = _default_model_adapter()

    # Step 1: beats.
    beats = generate_beats(sketch, model_adapter)
    sketch.beats = beats
    store.save_sketch(sketch)

    # Step 2: character refs (one per unique character).
    refs_dir = store.sketch_refs_dir(sketch_id)
    refs_dir.mkdir(parents=True, exist_ok=True)
    characters = _unique_characters(beats)
    character_refs: List[CharacterRef] = []
    seen_slugs: Dict[str, int] = {}
    for char in characters:
        base_slug = slugify(char["name"])
        count = seen_slugs.get(base_slug, 0)
        slug = base_slug if count == 0 else f"{base_slug}-{count + 1}"
        seen_slugs[base_slug] = count + 1
        out_path = refs_dir / _ref_filename(slug)
        ref = storyboard_adapter.generate_character_ref(char, style_guide, out_path)
        ref.slug = slug
        ref.path = out_path
        character_refs.append(ref)

    # Step 3: per-beat frames.
    storyboard_dir = store.sketch_storyboard_dir(sketch_id)
    storyboard_dir.mkdir(parents=True, exist_ok=True)
    frames: List[Frame] = []
    for beat in beats:
        beat_n = int(beat.get("n", 1) or 1)
        out_path = storyboard_dir / _frame_filename(beat_n)
        frame = storyboard_adapter.generate_frame(beat, character_refs, style_guide, out_path)
        frame.beat_n = beat_n
        frame.path = out_path
        frames.append(frame)

    # Step 4: persist metadata onto the sketch.
    sketch.storyboard_frames = [f.to_dict() for f in frames]
    storyboard_meta = {
        "adapter_id": getattr(storyboard_adapter, "adapter_id", "unknown"),
        "generated_at": _now(),
        "style_guide": style_guide,
        "characters": [r.to_dict() for r in character_refs],
        "frames": [f.to_dict() for f in frames],
        "frame_size": cfg.get("frame_size", "1024x1024"),
    }
    (store.sketch_dir(sketch_id) / "storyboard.json").write_text(
        json.dumps(storyboard_meta, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    store.save_sketch(sketch)

    # Step 5: transition SCRIPTED -> STORYBOARD_REVIEW (optional so callers
    # that handle transitions themselves don't double-fire).
    if transition:
        try:
            store.transition(
                sketch_id,
                Status.STORYBOARD_REVIEW,
                {
                    "action": "run_storyboard",
                    "adapter": storyboard_meta["adapter_id"],
                    "beat_count": len(beats),
                },
            )
        except Exception as exc:
            LOG.warning("storyboard transition failed: %s", exc)

    return storyboard_meta


def regenerate_frame(
    store: Store,
    sketch_id: str,
    beat_n: int,
    *,
    storyboard_adapter: Optional[StoryboardAdapter] = None,
    storyboard_config: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """Re-run frame generation for a single beat. Returns the new frame dict."""
    sketch = store.get_sketch(sketch_id)
    cfg = storyboard_config if storyboard_config is not None else _load_storyboard_config()
    style_guide = str(cfg.get("default_style_guide") or "").strip()

    if storyboard_adapter is None:
        storyboard_adapter = select_storyboard_adapter(cfg)

    # Find the beat.
    beat: Optional[Dict[str, Any]] = None
    for b in sketch.beats or []:
        try:
            if int(b.get("n", -1)) == int(beat_n):
                beat = b
                break
        except (TypeError, ValueError):
            continue
    if beat is None:
        raise ValueError(f"beat {beat_n} not found on sketch {sketch_id}")

    # Load existing character refs from the storyboard.json so regen uses
    # the same anchors as the original run.
    storyboard_json_path = store.sketch_dir(sketch_id) / "storyboard.json"
    existing_refs: List[CharacterRef] = []
    if storyboard_json_path.exists():
        try:
            meta = json.loads(storyboard_json_path.read_text(encoding="utf-8"))
        except Exception:
            meta = {}
        for char in meta.get("characters") or []:
            if not isinstance(char, dict):
                continue
            path_str = char.get("path")
            if not path_str:
                continue
            existing_refs.append(
                CharacterRef(
                    name=str(char.get("name", "")),
                    slug=str(char.get("slug", "")),
                    path=Path(path_str),
                    prompt=str(char.get("prompt", "")),
                    adapter_id=str(char.get("adapter_id", "")),
                )
            )

    out_path = store.sketch_storyboard_dir(sketch_id) / _frame_filename(int(beat_n))
    frame = storyboard_adapter.generate_frame(beat, existing_refs, style_guide, out_path)
    frame.beat_n = int(beat_n)
    frame.path = out_path

    # Update the sketch + storyboard.json in place.
    new_frame_dict = frame.to_dict()
    updated_frames: List[Dict[str, Any]] = []
    replaced = False
    for f in sketch.storyboard_frames or []:
        if int(f.get("beat_n", -1)) == int(beat_n):
            updated_frames.append(new_frame_dict)
            replaced = True
        else:
            updated_frames.append(f)
    if not replaced:
        updated_frames.append(new_frame_dict)
    sketch.storyboard_frames = updated_frames
    store.save_sketch(sketch)

    if storyboard_json_path.exists():
        try:
            meta = json.loads(storyboard_json_path.read_text(encoding="utf-8"))
        except Exception:
            meta = {"frames": []}
        meta_frames = meta.get("frames") or []
        new_meta_frames: List[Dict[str, Any]] = []
        seen = False
        for f in meta_frames:
            if int(f.get("beat_n", -1)) == int(beat_n):
                new_meta_frames.append(new_frame_dict)
                seen = True
            else:
                new_meta_frames.append(f)
        if not seen:
            new_meta_frames.append(new_frame_dict)
        meta["frames"] = new_meta_frames
        meta["regenerated_beat"] = int(beat_n)
        meta["regenerated_at"] = _now()
        storyboard_json_path.write_text(
            json.dumps(meta, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )

    return new_frame_dict


# ----------------------------------------------------------------- default model


def _default_model_adapter() -> ModelAdapter:
    """Pick the production model adapter for beat sheet generation.

    Phase 3 installed ClaudeCLIAdapter as the default. If the CLI isn't
    available we fall back to a dummy adapter that returns an empty
    response — the beats.py module will then emit a fallback single beat.
    """
    try:
        from idea_factory.adapters.claude_cli import ClaudeCLIAdapter
    except ImportError as exc:
        LOG.warning("claude cli adapter unavailable: %s", exc)
        return _NullModelAdapter()
    adapter = ClaudeCLIAdapter(
        config={"id": "claude-opus", "cli_model": "claude-opus-4-6", "timeout_sec": 180, "max_turns": 1}
    )
    if not adapter.is_available():
        LOG.warning("claude cli not on PATH; beats will use fallback")
        return _NullModelAdapter()
    return adapter


class _NullModelAdapter(ModelAdapter):
    """No-op adapter used when no real LLM is available."""

    model_id = "null"

    def is_available(self) -> bool:
        return False

    def generate(self, signal, prompt, n_premises=3):  # type: ignore[override]
        from idea_factory.adapter import PremiseResult
        return PremiseResult(
            model_id=self.model_id,
            signal_id=str(signal.get("signal_id", "")),
            error="no model adapter available",
        )


__all__ = [
    "regenerate_frame",
    "run_storyboard",
    "select_storyboard_adapter",
]
