"""End-to-end video generation orchestration.

`run_video_pipeline(store, sketch_id)` is what the backend calls after a
user approves a storyboard. It loads the sketch's beats and storyboard
frames, picks an adapter from `config/video.yaml`, calls
`generate(start_frame, end_frame, prompt, duration_sec)` for each beat,
enforces the per-sketch cost cap, and finally stitches every successful
clip together with `stitch_clips()`. The sketch transitions to
`CRITIC_REVIEW` when stitching is done.

Adapter routing is dead simple in Phase 5: walk the list in
`routing.default` and pick the first adapter whose `is_available()`
returns True. Smarter routing (per-beat, dialogue-aware, budget-aware)
is a polish phase concern.
"""
from __future__ import annotations

import importlib
import json
import logging
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

from state.machine import Status
from state.store import Sketch, Store
from video_gen._common import copy_placeholder
from video_gen.adapter import VideoClip, VideoProviderAdapter
from video_gen.adapters.stub_video import StubVideoAdapter
from video_gen.stitch import StitchError, stitch_clips

# Lazy critic imports — see `_default_critic_adapter` below. We deliberately
# do NOT import the critic at module load time so older code paths that
# import video_gen.pipeline don't get a hard dependency on the critic
# package's adapter chain.


LOG = logging.getLogger("video_gen.pipeline")

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_VIDEO_CONFIG = PROJECT_ROOT / "config" / "video.yaml"
PROMPT_TEMPLATE_PATH = PROJECT_ROOT / "video_gen" / "prompts" / "clip_prompt.md"


# ----------------------------------------------------------------- config


def _load_video_config(path: Path = DEFAULT_VIDEO_CONFIG) -> Dict[str, Any]:
    if not path.exists():
        return {
            "routing": {"default": ["stub"]},
            "budget": {"max_cost_cents_per_sketch": 500},
            "adapters": [],
        }
    try:
        import yaml  # type: ignore
        data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    except Exception as exc:
        LOG.warning("could not read video.yaml: %s", exc)
        return {"routing": {"default": ["stub"]}, "budget": {"max_cost_cents_per_sketch": 500}, "adapters": []}
    if not isinstance(data, dict):
        return {"routing": {"default": ["stub"]}, "budget": {"max_cost_cents_per_sketch": 500}, "adapters": []}
    return data


def _instantiate_adapter(entry: Dict[str, Any]) -> Optional[VideoProviderAdapter]:
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
        LOG.warning("could not import video adapter %s: %s", dotted, exc)
        return None
    config = dict(entry.get("config") or {})
    if "id" in entry:
        config["id"] = entry["id"]
    try:
        return cls(config=config)
    except Exception as exc:
        LOG.warning("could not instantiate video adapter %s: %s", dotted, exc)
        return None


def load_adapters(
    config: Optional[Dict[str, Any]] = None,
) -> Dict[str, VideoProviderAdapter]:
    """Return {adapter_id: instance} for every enabled entry in `adapters`."""
    cfg = config if config is not None else _load_video_config()
    out: Dict[str, VideoProviderAdapter] = {}
    for entry in cfg.get("adapters") or []:
        if not entry.get("enabled"):
            continue
        adapter = _instantiate_adapter(entry)
        if adapter is None:
            continue
        out[adapter.provider_id] = adapter
    return out


def select_video_adapter(
    config: Optional[Dict[str, Any]] = None,
    adapters: Optional[Dict[str, VideoProviderAdapter]] = None,
) -> VideoProviderAdapter:
    """Walk routing.default and return the first available adapter.

    Falls back to the stub if nothing routable is found.
    """
    cfg = config if config is not None else _load_video_config()
    if adapters is None:
        adapters = load_adapters(cfg)
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
    # Last-resort stub.
    return StubVideoAdapter()


# ----------------------------------------------------------------- helpers


def _now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _load_prompt_template() -> str:
    if PROMPT_TEMPLATE_PATH.exists():
        return PROMPT_TEMPLATE_PATH.read_text(encoding="utf-8")
    return "{action}\nCamera: {camera}. Location: {location}. {visual_note}\n{dialogue_line}"


def _build_clip_prompt(beat: Dict[str, Any]) -> str:
    template = _load_prompt_template()
    dialogue = beat.get("dialogue") or ""
    dialogue_line = f'Dialogue: "{dialogue}"' if dialogue else ""
    characters = beat.get("characters") or []
    char_names = ", ".join(
        c.get("name", "") if isinstance(c, dict) else str(c) for c in characters
    ).strip(", ")
    return template.format(
        action=str(beat.get("action", "")).strip(),
        camera=str(beat.get("camera", "medium")).strip(),
        location=str(beat.get("location", "")).strip(),
        visual_note=str(beat.get("visual_note", "")).strip(),
        dialogue_line=dialogue_line,
        character_names=char_names or "(none)",
    )


def _frame_path_for_beat(store: Store, sketch_id: str, beat_n: int) -> Optional[Path]:
    candidate = store.sketch_storyboard_dir(sketch_id) / f"beat-{beat_n:02d}-start.png"
    if candidate.exists():
        return candidate
    # Phase 1 stub used a non-zero-padded name; check that as a fallback.
    legacy = store.sketch_storyboard_dir(sketch_id) / f"beat-{beat_n}-start.png"
    if legacy.exists():
        return legacy
    return None


# ----------------------------------------------------------------- public API


def _character_refs_for_sketch(store: Store, sketch_id: str) -> List[Path]:
    refs_dir = store.sketch_refs_dir(sketch_id)
    if not refs_dir.exists():
        return []
    return sorted(refs_dir.glob("*.png"))


def run_video_pipeline(
    store: Store,
    sketch_id: str,
    *,
    adapter: Optional[VideoProviderAdapter] = None,
    config: Optional[Dict[str, Any]] = None,
    transition: bool = True,
    critic_adapter: Any = None,
    max_retries: Optional[int] = None,
) -> Dict[str, Any]:
    """Generate per-beat clips for a sketch and stitch them into final.mp4.

    Returns a metadata dict (also persisted to `data/sketches/{id}/clips.json`).
    The `adapter` kwarg is for tests; production callers leave it None and
    the pipeline picks the routed adapter from `config/video.yaml`.

    Phase 6: after each clip is generated the routed `critic_adapter` runs
    a `check_shot()` against it. If the report's `passed` is False and we
    haven't hit `max_retries`, the clip is regenerated. Each retry counts
    against the same cost cap.
    """
    sketch = store.get_sketch(sketch_id)

    cfg = config if config is not None else _load_video_config()
    cap = int((cfg.get("budget") or {}).get("max_cost_cents_per_sketch", 500))

    # Track whether the caller injected the video adapter — if they did
    # we treat them as a unit test and avoid pulling in the routed critic
    # (which would otherwise shell out to Claude/Gemini). Tests that care
    # about the retry loop can still explicitly pass `critic_adapter`.
    adapter_was_injected = adapter is not None

    if adapter is None:
        adapter = select_video_adapter(cfg)

    if critic_adapter is None:
        if adapter_was_injected:
            from critic.adapters.stub_critic import StubCritic
            critic_adapter = StubCritic()
        else:
            critic_adapter = _default_critic_adapter()
    if max_retries is None:
        max_retries = _default_max_retries()

    clips_dir = store.sketch_clips_dir(sketch_id)
    clips_dir.mkdir(parents=True, exist_ok=True)

    beats = sketch.beats or []
    clips: List[VideoClip] = []
    shot_reports: List[Dict[str, Any]] = []
    cap_hit = False
    cap_hit_at_beat: Optional[int] = None
    cumulative_cost = 0
    character_refs = _character_refs_for_sketch(store, sketch_id)

    for beat in beats:
        try:
            beat_n = int(beat.get("n", len(clips) + 1) or len(clips) + 1)
        except (TypeError, ValueError):
            beat_n = len(clips) + 1
        duration_sec = float(beat.get("duration_sec", 5) or 5)

        # Cost cap pre-check: if running cost + this clip's estimate would
        # blow the cap, stop generating and proceed to stitch what we have.
        try:
            estimate = adapter.estimated_cost_cents(duration_sec)
        except Exception:
            estimate = 0
        if cap > 0 and (cumulative_cost + estimate) > cap:
            LOG.warning(
                "video pipeline cost cap reached at beat %s "
                "(cumulative=%s + estimate=%s > cap=%s); stopping",
                beat_n,
                cumulative_cost,
                estimate,
                cap,
            )
            cap_hit = True
            cap_hit_at_beat = beat_n
            break

        start_frame = _frame_path_for_beat(store, sketch_id, beat_n)
        out_path = clips_dir / f"beat-{beat_n:02d}.mp4"
        prompt = _build_clip_prompt(beat)

        if start_frame is None:
            # No storyboard frame on disk — fall back to placeholder copy.
            LOG.warning("no start frame for beat %s; using placeholder", beat_n)
            copy_placeholder(out_path)
            clips.append(
                VideoClip(
                    beat_n=beat_n,
                    path=out_path,
                    provider_id="stub-video-v1",
                    duration_sec=duration_sec,
                    error="no storyboard frame on disk",
                )
            )
            continue

        # Phase 6: shot-level retry loop. Total attempts = 1 + max_retries.
        clip: Optional[VideoClip] = None
        last_report: Optional[Any] = None
        total_attempts = max(1, 1 + max_retries)
        for attempt in range(total_attempts):
            clip = adapter.generate(
                start_frame=start_frame,
                end_frame=None,
                prompt=prompt,
                duration_sec=duration_sec,
                out_path=out_path,
                beat_n=beat_n,
            )
            cumulative_cost += int(getattr(clip, "cost_cents", 0) or 0)

            # Provider-side error: don't retry, log and move on.
            if clip.error:
                LOG.warning(
                    "beat %s adapter error on attempt %s/%s: %s",
                    beat_n,
                    attempt + 1,
                    total_attempts,
                    clip.error,
                )
                break

            # Run the shot check unless retries are disabled.
            if max_retries <= 0 or critic_adapter is None:
                break

            try:
                report = critic_adapter.check_shot(
                    out_path,
                    start_frame,
                    character_refs,
                    beat,
                )
            except Exception as exc:
                LOG.warning("critic check_shot raised on beat %s: %s", beat_n, exc)
                report = None

            if report is not None:
                last_report = report
                shot_reports.append(
                    {
                        "beat_n": beat_n,
                        "attempt": attempt + 1,
                        **report.to_dict(),
                    }
                )
                if report.passed:
                    LOG.info(
                        "beat %s shot check passed on attempt %s/%s",
                        beat_n,
                        attempt + 1,
                        total_attempts,
                    )
                    break
                LOG.warning(
                    "beat %s shot check FAILED on attempt %s/%s: issues=%s",
                    beat_n,
                    attempt + 1,
                    total_attempts,
                    report.issues,
                )
                if attempt + 1 >= total_attempts:
                    # Out of retries — keep the last clip and surface the
                    # failure on the clip's error field so the UI can show it.
                    clip.error = (
                        f"shot check failed after {total_attempts} attempts: "
                        f"{', '.join(report.issues) if report.issues else 'no details'}"
                    )
                    break
            else:
                # Critic itself failed — don't keep retrying on our problem.
                break

        assert clip is not None  # loop runs at least once
        clips.append(clip)

    # Stitch every clip whose file landed on disk (errors copy the
    # placeholder, so all `path`s are valid by the adapter contract).
    valid_paths = [c.path for c in clips if Path(c.path).exists() and Path(c.path).stat().st_size > 0]
    final_path = store.sketch_final_path(sketch_id)
    final_path.parent.mkdir(parents=True, exist_ok=True)
    stitched = False
    if valid_paths:
        try:
            stitch_clips(valid_paths, final_path)
            stitched = True
        except StitchError as exc:
            LOG.warning("stitch failed: %s; copying first clip as final.mp4", exc)
            try:
                final_path.write_bytes(Path(valid_paths[0]).read_bytes())
                stitched = True
            except Exception as inner:
                LOG.warning("could not even copy first clip: %s", inner)
    if not stitched:
        copy_placeholder(final_path)

    sketch.video_clips = [c.to_dict() for c in clips]
    sketch.final_cut_path = str(final_path)
    sketch.cost_cents_total = (sketch.cost_cents_total or 0) + cumulative_cost
    store.save_sketch(sketch)

    metadata = {
        "sketch_id": sketch_id,
        "adapter_id": getattr(adapter, "provider_id", "unknown"),
        "critic_adapter_id": getattr(critic_adapter, "adapter_id", None),
        "generated_at": _now(),
        "total_cost_cents": cumulative_cost,
        "max_cost_cents_per_sketch": cap,
        "max_retries": max_retries,
        "cap_hit": cap_hit,
        "cap_hit_at_beat": cap_hit_at_beat,
        "clip_count": len(clips),
        "successful_clip_count": len([c for c in clips if c.error is None]),
        "final_cut_path": str(final_path),
        "clips": [c.to_dict() for c in clips],
        "shot_reports": shot_reports,
    }
    (store.sketch_dir(sketch_id) / "clips.json").write_text(
        json.dumps(metadata, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    if transition:
        try:
            store.transition(
                sketch_id,
                Status.CRITIC_REVIEW,
                {
                    "action": "run_video_pipeline",
                    "adapter": metadata["adapter_id"],
                    "clip_count": metadata["clip_count"],
                    "total_cost_cents": cumulative_cost,
                    "cap_hit": cap_hit,
                },
            )
        except Exception as exc:
            LOG.warning("video pipeline transition failed: %s", exc)

    return metadata


def _default_critic_adapter() -> Any:
    """Return the routed critic adapter from `config/critic.yaml`.

    Imported lazily to avoid a hard import-time cycle between video_gen
    and the critic package. Returns the StubCritic if loading fails.
    """
    try:
        from critic.pipeline import select_critic_adapter
    except Exception as exc:
        LOG.warning("could not import critic.pipeline: %s", exc)
        from critic.adapters.stub_critic import StubCritic
        return StubCritic()
    try:
        return select_critic_adapter()
    except Exception as exc:
        LOG.warning("select_critic_adapter raised: %s", exc)
        from critic.adapters.stub_critic import StubCritic
        return StubCritic()


def _default_max_retries() -> int:
    try:
        from critic.pipeline import get_max_retries
        return get_max_retries()
    except Exception:
        return 2


__all__ = [
    "load_adapters",
    "run_video_pipeline",
    "select_video_adapter",
]
