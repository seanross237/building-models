"""FastAPI backend for ai_vids_virality.

Phase 1 added the kanban + sketch lifecycle endpoints. Phase 2 adds the
Signals page endpoints (`/api/signals`, `/api/signals/{id}/promote`,
`/api/signals/{id}/reject`) so the UI can browse real radar items
collected from Reddit / Hacker News / Google News / YouTube trending.

Review-gate endpoints still inline the downstream stub stages so a click
in the browser walks the sketch one full step forward.
"""
from __future__ import annotations

# Phase 8: load .env at the very top so adapters that read FAL_KEY etc.
# in their constructors see the values. override=False so existing
# process env (CI, tests, systemd EnvironmentFile) wins.
try:
    from dotenv import load_dotenv as _load_dotenv
    _load_dotenv(override=False)
except ImportError:
    pass

import hashlib
import json
import os
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from analyzers.score_signals import analyze as score_signals
from analyzers.score_signals.lens_rules import Lens, load_lens
from backend import events as backend_events
from backend import stats as backend_stats
from critic import pipeline as critic_pipeline
from critic.adapters.stub_critic import StubCritic
from idea_factory import stub_factory
from idea_factory.adapter import Premise
from publishing import pipeline as publishing_pipeline
from state.leaderboard import Leaderboard
from state.machine import InvalidTransition, Status
from state.store import Sketch, Store
from storyboard import pipeline as storyboard_pipeline
from video_gen import pipeline as video_pipeline


PROJECT_ROOT = Path(__file__).resolve().parent.parent
STATIC_DIR = Path(__file__).resolve().parent / "static"
LENS_PATH = PROJECT_ROOT / "config" / "comedy-lens.md"
SIGNAL_FRESHNESS_HOURS = 24


def _data_root() -> Path:
    """Allow tests to point at a temp directory via env var."""
    override = os.environ.get("AI_VIDS_DATA_ROOT")
    if override:
        return Path(override)
    return PROJECT_ROOT / "data"


def get_store() -> Store:
    return Store(root=_data_root())


def get_leaderboard() -> Leaderboard:
    return Leaderboard(_data_root() / "leaderboard.json")


def _now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _emit_transition_event(sketch_id: str, from_status: str, to_status: str) -> None:
    """Push an SSE `pipeline_update` event so connected UIs auto-refresh."""
    backend_events.publish_event(
        "pipeline_update",
        {
            "sketch_id": sketch_id,
            "from": from_status,
            "to": to_status,
        },
    )


def _load_lens() -> Lens:
    return load_lens(LENS_PATH)


def _rejected_signals_path(store: Store) -> Path:
    return store.root / "rejected-signals.json"


def _load_rejected_signals(store: Store) -> set:
    path = _rejected_signals_path(store)
    if not path.exists():
        return set()
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return set()
    if isinstance(data, list):
        return {str(x) for x in data}
    if isinstance(data, dict) and "ids" in data:
        return {str(x) for x in data["ids"]}
    return set()


def _save_rejected_signals(store: Store, ids: set) -> None:
    path = _rejected_signals_path(store)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps({"ids": sorted(ids)}, indent=2) + "\n", encoding="utf-8")


_FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---\n(.*)$", re.DOTALL)


def _parse_signal_file(path: Path) -> Optional[Dict[str, Any]]:
    if not path.exists():
        return None
    raw = path.read_text(encoding="utf-8")
    match = _FRONTMATTER_RE.match(raw)
    if not match:
        return None
    block, body = match.group(1), match.group(2)
    meta: Dict[str, Any] = {}
    for line in block.splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        meta[key.strip()] = value.strip()

    summary_match = re.search(r"^## Summary\n\n(.+?)(?=\n## |\Z)", body, flags=re.MULTILINE | re.DOTALL)
    summary = summary_match.group(1).strip() if summary_match else ""
    body_match = re.search(r"^## Source content\n\n(.+?)(?=\n## |\Z)", body, flags=re.MULTILINE | re.DOTALL)
    body_text = body_match.group(1).strip() if body_match else ""
    meta["_summary"] = summary
    meta["_body"] = body_text
    meta["_path"] = str(path)
    return meta


def _parse_iso(value: str) -> Optional[datetime]:
    if not value:
        return None
    try:
        if value.endswith("Z"):
            value = value[:-1] + "+00:00"
        dt = datetime.fromisoformat(value)
    except ValueError:
        return None
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)


def _hours_since(dt: Optional[datetime]) -> Optional[float]:
    if dt is None:
        return None
    return (datetime.now(timezone.utc) - dt).total_seconds() / 3600.0


def _is_promoted(store: Store, signal_id: str) -> bool:
    marker = store.queue_dir("idea-factory") / f"{signal_id}.json"
    if marker.exists():
        return True
    for sketch in store.list_sketches():
        if sketch.signal_id == signal_id:
            return True
    return False


def _iter_signal_files(store: Store) -> List[Path]:
    paths: List[Path] = []
    if not store.signals_dir.exists():
        return paths
    for source_dir in sorted(p for p in store.signals_dir.iterdir() if p.is_dir()):
        items_dir = source_dir / "items"
        if not items_dir.exists():
            continue
        for item in sorted(items_dir.glob("*.md")):
            paths.append(item)
    return paths


def _find_signal_file(store: Store, signal_id: str) -> Optional[Path]:
    for path in _iter_signal_files(store):
        if path.stem == signal_id:
            return path
    return None


def _build_signal_summary(
    meta: Dict[str, Any],
    lens: Lens,
    promoted: bool,
    rejected: bool,
) -> Dict[str, Any]:
    title = meta.get("title", "")
    body = meta.get("_body") or meta.get("_summary") or ""
    score = lens.score(title, body) if (title or body) else 5
    captured = meta.get("captured_at", "")
    published = meta.get("published_at", "")
    return {
        "id": meta.get("id", ""),
        "source": meta.get("source", ""),
        "title": title,
        "url": meta.get("source_url", ""),
        "summary": meta.get("_summary", ""),
        "score": score,
        "promoted": promoted,
        "rejected": rejected,
        "captured_at": captured,
        "published_at": published,
        "freshness_hours": meta.get("freshness_hours", ""),
    }


# ----------------------------------------------------------------- app

app = FastAPI(title="ai_vids_virality", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8000", "http://127.0.0.1:8000", "http://localhost:8765"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if STATIC_DIR.exists():
    app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")


# ----------------------------------------------------------------- helpers


def _sketch_summary(sketch: Sketch) -> Dict[str, Any]:
    premise = sketch.premise or {}
    return {
        "id": sketch.id,
        "status": sketch.status.value,
        "signal_id": sketch.signal_id,
        "logline": premise.get("logline", "(no premise)"),
        "tone": premise.get("tone", ""),
        "updated_at": sketch.updated_at,
    }


def _kanban_columns() -> List[str]:
    return [s.value for s in Status]


def _stub_beats_for(sketch: Sketch) -> List[Dict[str, Any]]:
    """Generate a deterministic 3-beat outline from the approved premise."""
    premise = sketch.premise or {}
    logline = premise.get("logline", "stub logline")
    return [
        {
            "n": 1,
            "duration_sec": 6,
            "location": "office",
            "characters": premise.get("characters", []),
            "action": f"establish: {logline}",
            "dialogue": None,
            "camera": "wide",
            "visual_note": "morning light, cluttered desk",
        },
        {
            "n": 2,
            "duration_sec": 12,
            "location": "office",
            "characters": premise.get("characters", []),
            "action": "the situation escalates absurdly",
            "dialogue": "you can't be serious",
            "camera": "two-shot",
            "visual_note": "fluorescent overhead",
        },
        {
            "n": 3,
            "duration_sec": 12,
            "location": "office",
            "characters": premise.get("characters", []),
            "action": "the twist lands",
            "dialogue": premise.get("twist", ""),
            "camera": "close-up",
            "visual_note": "punchline framing",
        },
    ]


# ----------------------------------------------------------------- models


class ManualIdeaIn(BaseModel):
    text: str


class ApprovePremiseIn(BaseModel):
    model_id: Optional[str] = None
    premise_index: Optional[int] = None


class PromoteSignalIn(BaseModel):
    """Phase 10: optional guidance the promoter types on the Signals page."""

    guidance: Optional[str] = None


class PremiseEditIn(BaseModel):
    """Phase 10: PATCH /api/sketch/{id}/premise body."""

    model_id: str
    premise_index: int
    premise: Dict[str, Any]


class PremiseAddIn(BaseModel):
    """Phase 10: POST /api/sketch/{id}/premise body."""

    premise: Dict[str, Any]


class BeatEditIn(BaseModel):
    """Phase 10: PATCH /api/sketch/{id}/beat/{n} body.

    All fields optional — only provided keys are updated on the beat.
    """

    action: Optional[str] = None
    dialogue: Optional[str] = None
    camera: Optional[str] = None
    visual_note: Optional[str] = None
    location: Optional[str] = None
    duration_sec: Optional[int] = None


def _list_variant_files(store: Store, sketch_id: str) -> List[Path]:
    queue_dir = store.queue_dir("premise-review")
    if not queue_dir.exists():
        return []
    return sorted(queue_dir.glob(f"{sketch_id}__*.json"))


def _load_variants(store: Store, sketch_id: str) -> List[Dict[str, Any]]:
    variants: List[Dict[str, Any]] = []
    for path in _list_variant_files(store, sketch_id):
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            continue
        variants.append(
            {
                "model_id": payload.get("model_id", ""),
                "generated_at": payload.get("generated_at", ""),
                "cost_cents": int(payload.get("cost_cents", 0) or 0),
                "duration_ms": int(payload.get("duration_ms", 0) or 0),
                "error": payload.get("error"),
                "premises": payload.get("premises") or [],
            }
        )
    return variants


def _contributing_model_ids(store: Store, sketch_id: str) -> List[str]:
    return [v["model_id"] for v in _load_variants(store, sketch_id) if v.get("model_id")]


# ----------------------------------------------------------------- routes


@app.get("/")
def index() -> FileResponse:
    index_path = STATIC_DIR / "index.html"
    if not index_path.exists():
        raise HTTPException(status_code=404, detail="index.html missing")
    return FileResponse(str(index_path))


@app.get("/api/kanban")
def kanban() -> JSONResponse:
    store = get_store()
    columns: Dict[str, List[Dict[str, Any]]] = {col: [] for col in _kanban_columns()}
    for sketch in store.list_sketches():
        columns.setdefault(sketch.status.value, []).append(_sketch_summary(sketch))
    return JSONResponse(content=columns)


@app.get("/api/sketch/{sketch_id}")
def get_sketch(sketch_id: str) -> JSONResponse:
    store = get_store()
    try:
        sketch = store.get_sketch(sketch_id)
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc))
    return JSONResponse(content=sketch.to_dict())


@app.post("/api/sketch/{sketch_id}/approve_premise")
def approve_premise(
    sketch_id: str,
    body: Optional[ApprovePremiseIn] = None,
) -> JSONResponse:
    """Approve a premise (Phase 3: optional `model_id` + `premise_index`).

    If `body.model_id` is set, the chosen variant becomes the canonical
    premise and the leaderboard increments approved for the chosen model
    and rejected for the losing models. If no body is supplied, the
    sketch's existing canonical premise is approved (Phase 1 path).
    """
    store = get_store()
    leaderboard = get_leaderboard()
    try:
        sketch = store.get_sketch(sketch_id)
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc))

    chosen_model: Optional[str] = body.model_id if body else None
    chosen_index: int = body.premise_index if (body and body.premise_index is not None) else 0

    variants = _load_variants(store, sketch_id)
    contributing_models = [v["model_id"] for v in variants if v.get("model_id")]

    if chosen_model and variants:
        chosen_variant = next((v for v in variants if v.get("model_id") == chosen_model), None)
        if chosen_variant is None:
            raise HTTPException(
                status_code=400,
                detail=f"unknown model_id {chosen_model} for sketch {sketch_id}",
            )
        premises = chosen_variant.get("premises") or []
        if chosen_index < 0 or chosen_index >= len(premises):
            raise HTTPException(
                status_code=400,
                detail=f"premise_index {chosen_index} out of range",
            )
        sketch.premise = premises[chosen_index]
        sketch.premises = premises
        store.save_sketch(sketch)

    # Leaderboard accounting: chosen model gets approved, losers get rejected.
    if chosen_model and contributing_models:
        for model_id in contributing_models:
            leaderboard.record_decision(model_id, approved=(model_id == chosen_model))

    try:
        store.transition(
            sketch_id,
            Status.SCRIPTED,
            {"action": "approve_premise", "model_id": chosen_model, "premise_index": chosen_index},
        )
    except InvalidTransition as exc:
        raise HTTPException(status_code=409, detail=str(exc))

    # Phase 4: run the real storyboard pipeline (beats + character refs +
    # per-beat frames) instead of the Phase 1 stub. Offline test runs set
    # `AI_VIDS_OFFLINE_STORYBOARD=1` so we use the null model adapter and
    # the stub storyboard adapter — no Claude CLI, no network.
    offline = os.environ.get("AI_VIDS_OFFLINE_STORYBOARD") == "1"
    model_adapter = None
    storyboard_adapter = None
    if offline:
        from idea_factory.adapter import ModelAdapter, PremiseResult
        from storyboard.adapters.stub_storyboard import StubStoryboardAdapter

        class _OfflineNullModel(ModelAdapter):
            model_id = "offline-null"

            def is_available(self) -> bool:
                return False

            def generate(self, signal, prompt, n_premises=3):  # type: ignore[override]
                return PremiseResult(
                    model_id=self.model_id,
                    signal_id=str(signal.get("signal_id", "")),
                    error="offline test run",
                )

        model_adapter = _OfflineNullModel()
        storyboard_adapter = StubStoryboardAdapter()

    try:
        storyboard_pipeline.run_storyboard(
            store,
            sketch_id,
            model_adapter=model_adapter,
            storyboard_adapter=storyboard_adapter,
            transition=True,
        )
    except Exception as exc:  # pragma: no cover - defensive
        raise HTTPException(status_code=500, detail=f"storyboard pipeline failed: {exc}")

    sketch = store.get_sketch(sketch_id)

    # Remove the per-variant markers and the legacy single-marker if present.
    for path in _list_variant_files(store, sketch_id):
        try:
            path.unlink()
        except FileNotFoundError:
            pass
    store.remove_queue_marker("premise-review", sketch_id)
    store.write_queue_marker(
        "storyboard-review",
        sketch_id,
        {"sketch_id": sketch_id, "queued_at": _now()},
    )
    _emit_transition_event(sketch_id, "premise_review", "storyboard_review")
    return JSONResponse(content=sketch.to_dict())


# ----------------------------------------------------------------- storyboard (Phase 4)


class RegenerateFrameIn(BaseModel):
    beat: int


def _frame_url(sketch_id: str, frame: Dict[str, Any]) -> str:
    beat_n = int(frame.get("beat_n", 1) or 1)
    return f"/data/sketches/{sketch_id}/storyboard/beat-{beat_n:02d}-start.png"


@app.get("/api/sketch/{sketch_id}/storyboard")
def get_storyboard(sketch_id: str) -> JSONResponse:
    store = get_store()
    try:
        sketch = store.get_sketch(sketch_id)
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc))

    storyboard_json_path = store.sketch_dir(sketch_id) / "storyboard.json"
    meta: Dict[str, Any] = {}
    if storyboard_json_path.exists():
        try:
            meta = json.loads(storyboard_json_path.read_text(encoding="utf-8"))
        except Exception:
            meta = {}

    frames = []
    for raw in sketch.storyboard_frames or []:
        beat_n = int(raw.get("beat_n", 1) or 1)
        # Cross-reference the beat action/location for UI captions.
        matching_beat: Dict[str, Any] = {}
        for beat in sketch.beats or []:
            try:
                if int(beat.get("n", -1)) == beat_n:
                    matching_beat = beat
                    break
            except (TypeError, ValueError):
                continue
        frames.append(
            {
                "beat_n": beat_n,
                "url": _frame_url(sketch_id, raw),
                "adapter_id": raw.get("adapter_id", ""),
                "error": raw.get("error"),
                "action": matching_beat.get("action", ""),
                "dialogue": matching_beat.get("dialogue", ""),
                "visual_note": matching_beat.get("visual_note", ""),
                "location": matching_beat.get("location", ""),
                "camera": matching_beat.get("camera", ""),
                "duration_sec": matching_beat.get("duration_sec", 0),
            }
        )

    characters = []
    for raw in meta.get("characters") or []:
        slug = raw.get("slug") or ""
        characters.append(
            {
                "name": raw.get("name", ""),
                "slug": slug,
                "url": f"/data/sketches/{sketch_id}/refs/{slug}.png" if slug else "",
                "error": raw.get("error"),
            }
        )

    premise = sketch.premise or {}
    return JSONResponse(
        content={
            "sketch_id": sketch_id,
            "status": sketch.status.value,
            "adapter_id": meta.get("adapter_id", ""),
            "style_guide": meta.get("style_guide", ""),
            "premise": {
                "logline": premise.get("logline", ""),
                "tone": premise.get("tone", ""),
            },
            "beats": sketch.beats or [],
            "characters": characters,
            "frames": frames,
        }
    )


@app.post("/api/sketch/{sketch_id}/storyboard/regenerate")
def regenerate_storyboard_frame(
    sketch_id: str,
    body: RegenerateFrameIn,
) -> JSONResponse:
    store = get_store()
    try:
        store.get_sketch(sketch_id)
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc))

    offline = os.environ.get("AI_VIDS_OFFLINE_STORYBOARD") == "1"
    storyboard_adapter = None
    if offline:
        from storyboard.adapters.stub_storyboard import StubStoryboardAdapter
        storyboard_adapter = StubStoryboardAdapter()

    try:
        new_frame = storyboard_pipeline.regenerate_frame(
            store,
            sketch_id,
            body.beat,
            storyboard_adapter=storyboard_adapter,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    except Exception as exc:  # pragma: no cover - defensive
        raise HTTPException(status_code=500, detail=f"regen failed: {exc}")

    return JSONResponse(
        content={
            "sketch_id": sketch_id,
            "beat_n": body.beat,
            "frame": new_frame,
            "url": _frame_url(sketch_id, new_frame),
        }
    )


@app.post("/api/sketch/{sketch_id}/approve_storyboard")
def approve_storyboard(sketch_id: str) -> JSONResponse:
    """Phase 5: trigger the real video pipeline + still-stub critic.

    The video pipeline transitions the sketch all the way to CRITIC_REVIEW
    (via VIDEO_PENDING) on its own, so we manually flip to VIDEO_PENDING
    first, then run the pipeline, then run the critic, then make sure the
    queue markers are clean.
    """
    store = get_store()
    try:
        store.get_sketch(sketch_id)
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc))

    try:
        store.transition(sketch_id, Status.VIDEO_PENDING, {"action": "approve_storyboard"})
    except InvalidTransition as exc:
        raise HTTPException(status_code=409, detail=str(exc))

    # Phase 5/6: route to the multi-provider video pipeline. Offline
    # test runs set AI_VIDS_OFFLINE_VIDEO=1 / AI_VIDS_OFFLINE_CRITIC=1
    # to force the stub adapters so the pipeline never shells out.
    offline_video = os.environ.get("AI_VIDS_OFFLINE_VIDEO") == "1"
    offline_critic = os.environ.get("AI_VIDS_OFFLINE_CRITIC") == "1"
    video_adapter = None
    critic_adapter = None
    if offline_video:
        from video_gen.adapters.stub_video import StubVideoAdapter
        video_adapter = StubVideoAdapter()
    if offline_critic:
        # Use the same id the routed yaml entry uses so test assertions
        # don't depend on whether the stub came from offline mode or
        # from the routing fallback.
        critic_adapter = StubCritic(config={"id": "stub"})

    try:
        video_pipeline.run_video_pipeline(
            store,
            sketch_id,
            adapter=video_adapter,
            critic_adapter=critic_adapter,
            transition=True,
        )
    except Exception as exc:  # pragma: no cover - defensive
        raise HTTPException(status_code=500, detail=f"video pipeline failed: {exc}")

    # Phase 6: real critic runs after the video pipeline. The pipeline
    # already moved the sketch to CRITIC_REVIEW, so the critic just
    # attaches its report onto the sketch + writes critic.json.
    try:
        critic_pipeline.run_full_critique(
            store,
            sketch_id,
            adapter=critic_adapter,
        )
    except Exception as exc:  # pragma: no cover - defensive
        raise HTTPException(status_code=500, detail=f"critic pipeline failed: {exc}")

    sketch = store.get_sketch(sketch_id)

    store.remove_queue_marker("storyboard-review", sketch_id)
    store.write_queue_marker(
        "final-review",
        sketch_id,
        {"sketch_id": sketch_id, "queued_at": _now()},
    )
    _emit_transition_event(sketch_id, "storyboard_review", "critic_review")
    return JSONResponse(content=sketch.to_dict())


@app.get("/api/sketch/{sketch_id}/clips")
def get_sketch_clips(sketch_id: str) -> JSONResponse:
    """Return the per-clip metadata + the URL of the final cut.

    The metadata mirrors `data/sketches/{id}/clips.json` (written by the
    video pipeline). The URLs all live under the dynamic `/data` route
    so the browser can fetch them.
    """
    store = get_store()
    try:
        sketch = store.get_sketch(sketch_id)
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc))

    clips_json_path = store.sketch_dir(sketch_id) / "clips.json"
    meta: Dict[str, Any] = {}
    if clips_json_path.exists():
        try:
            meta = json.loads(clips_json_path.read_text(encoding="utf-8"))
        except Exception:
            meta = {}

    clip_rows = []
    for raw in (meta.get("clips") or sketch.video_clips or []):
        beat_n = int(raw.get("beat_n", 0) or 0)
        clip_rows.append(
            {
                "beat_n": beat_n,
                "provider_id": raw.get("provider_id", ""),
                "duration_sec": raw.get("duration_sec", 0),
                "cost_cents": int(raw.get("cost_cents", 0) or 0),
                "duration_ms": int(raw.get("duration_ms", 0) or 0),
                "error": raw.get("error"),
                "url": f"/data/sketches/{sketch_id}/clips/beat-{beat_n:02d}.mp4",
            }
        )

    final_url = f"/data/sketches/{sketch_id}/final.mp4" if store.sketch_final_path(sketch_id).exists() else None

    return JSONResponse(
        content={
            "sketch_id": sketch_id,
            "status": sketch.status.value,
            "adapter_id": meta.get("adapter_id", ""),
            "total_cost_cents": int(meta.get("total_cost_cents", sketch.cost_cents_total or 0) or 0),
            "max_cost_cents_per_sketch": int(meta.get("max_cost_cents_per_sketch", 0) or 0),
            "cap_hit": bool(meta.get("cap_hit", False)),
            "cap_hit_at_beat": meta.get("cap_hit_at_beat"),
            "clip_count": len(clip_rows),
            "successful_clip_count": int(
                meta.get("successful_clip_count", len([c for c in clip_rows if not c.get("error")]))
                or 0
            ),
            "final_url": final_url,
            "clips": clip_rows,
        }
    )


@app.get("/api/sketch/{sketch_id}/critic")
def get_sketch_critic(sketch_id: str) -> JSONResponse:
    """Return the SketchCritique JSON for a sketch.

    The pipeline writes this to `data/sketches/{id}/critic.json` after
    the full-sketch critique runs. We prefer the on-disk file (it has
    a `scored_at` timestamp the in-memory sketch doesn't carry) and fall
    back to the sketch's `critic_report` field if the file is missing.
    """
    store = get_store()
    try:
        sketch = store.get_sketch(sketch_id)
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc))

    critic_path = store.sketch_dir(sketch_id) / "critic.json"
    if critic_path.exists():
        try:
            payload = json.loads(critic_path.read_text(encoding="utf-8"))
        except Exception:
            payload = sketch.critic_report or {}
    else:
        payload = sketch.critic_report or {}

    return JSONResponse(
        content={
            "sketch_id": sketch_id,
            "status": sketch.status.value,
            "critic_report": payload,
        }
    )


@app.post("/api/sketch/{sketch_id}/send_back_for_regen")
def send_back_for_regen(sketch_id: str) -> JSONResponse:
    """Phase 6: send a critic-review sketch back to VIDEO_PENDING.

    Lets the human reviewer ask for another video pass without going
    all the way back to storyboard. The state machine gained a
    CRITIC_REVIEW -> VIDEO_PENDING edge in Phase 6 specifically for this.
    """
    store = get_store()
    try:
        store.get_sketch(sketch_id)
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc))
    try:
        sketch = store.transition(
            sketch_id,
            Status.VIDEO_PENDING,
            {"action": "send_back_for_regen"},
        )
    except InvalidTransition as exc:
        raise HTTPException(status_code=409, detail=str(exc))
    store.remove_queue_marker("final-review", sketch_id)
    store.write_queue_marker(
        "video-gen",
        sketch_id,
        {"sketch_id": sketch_id, "queued_at": _now()},
    )
    _emit_transition_event(sketch_id, "critic_review", "video_pending")
    return JSONResponse(content=sketch.to_dict())


@app.post("/api/sketch/{sketch_id}/publish")
def publish(sketch_id: str) -> JSONResponse:
    """Phase 7: run every enabled publisher and transition on success.

    The sketch transitions to PUBLISHED iff at least one publisher
    reported success. The full list of results (one per destination)
    is returned so the UI can show per-destination URLs / errors.
    """
    store = get_store()
    try:
        sketch = store.get_sketch(sketch_id)
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc))

    # Gate the transition before running any publishers so an invalid
    # state (e.g. publishing from premise_review) short-circuits with
    # 409 and we don't waste time on archive/upload work.
    from state.machine import can_transition
    if not can_transition(sketch.status, Status.PUBLISHED):
        raise HTTPException(
            status_code=409,
            detail=f"Invalid transition from {sketch.status.value} to published",
        )

    publishers = None
    if os.environ.get("AI_VIDS_OFFLINE_PUBLISH") == "1":
        # Offline test runs: force local_archive only so we never
        # touch YouTube / TikTok / X even if env vars happen to be set.
        from publishing.adapters.local_archive import LocalArchivePublisher
        publishers = [LocalArchivePublisher(config={"id": "local_archive"})]

    results = publishing_pipeline.run_publishers(
        sketch, store, publishers=publishers
    )
    success_count = sum(1 for r in results if r.success)

    if success_count == 0:
        # Every destination failed — keep the sketch in CRITIC_REVIEW so
        # the user can retry. Return 502 so the UI shows an error.
        raise HTTPException(
            status_code=502,
            detail={
                "error": "all publishers failed",
                "results": [r.to_dict() for r in results],
            },
        )

    try:
        sketch = store.transition(sketch_id, Status.PUBLISHED, {"action": "publish"})
    except InvalidTransition as exc:
        raise HTTPException(status_code=409, detail=str(exc))

    store.remove_queue_marker("final-review", sketch_id)
    _emit_transition_event(sketch_id, "critic_review", "published")
    return JSONResponse(
        content={
            "sketch": sketch.to_dict(),
            "results": [r.to_dict() for r in results],
            "success_count": success_count,
            "destination_count": len(results),
        }
    )


@app.post("/api/sketch/{sketch_id}/reject")
def reject(sketch_id: str) -> JSONResponse:
    store = get_store()
    leaderboard = get_leaderboard()
    try:
        sketch = store.get_sketch(sketch_id)
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc))

    contributing = _contributing_model_ids(store, sketch_id)
    for model_id in contributing:
        leaderboard.record_decision(model_id, approved=False)

    previous_status = sketch.status.value
    try:
        sketch = store.transition(sketch_id, Status.REJECTED, {"action": "reject"})
    except InvalidTransition as exc:
        raise HTTPException(status_code=409, detail=str(exc))

    for path in _list_variant_files(store, sketch_id):
        try:
            path.unlink()
        except FileNotFoundError:
            pass
    for queue in ("premise-review", "storyboard-review", "video-gen", "final-review"):
        store.remove_queue_marker(queue, sketch_id)
    _emit_transition_event(sketch_id, previous_status, "rejected")
    return JSONResponse(content=sketch.to_dict())


# ----------------------------------------------------------------- premises (Phase 3)


@app.get("/api/sketch/{sketch_id}/premises")
def get_sketch_premises(sketch_id: str) -> JSONResponse:
    store = get_store()
    try:
        sketch = store.get_sketch(sketch_id)
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc))

    variants = _load_variants(store, sketch_id)
    signal_summary: Dict[str, Any] = {"id": sketch.signal_id}
    if sketch.history:
        first = sketch.history[0]
        payload = first.get("payload") if isinstance(first, dict) else None
        if isinstance(payload, dict) and payload.get("signal_title"):
            signal_summary["title"] = payload["signal_title"]
    return JSONResponse(
        content={
            "sketch_id": sketch_id,
            "signal": signal_summary,
            "variants": variants,
            "status": sketch.status.value,
        }
    )


# ----------------------------------------------------------------- Phase 10: manual editing affordances


def _variant_marker_path(store: Store, sketch_id: str, model_id: str) -> Path:
    return store.queue_dir("premise-review") / f"{sketch_id}__{model_id}.json"


def _read_variant_marker(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _write_variant_marker(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _normalize_premise_payload(raw: Dict[str, Any]) -> Dict[str, Any]:
    """Coerce an inbound premise dict to the canonical shape on disk.

    Matches the fields used by `idea_factory.adapter.Premise`:
    logline, synopsis, tone, target_length_sec, characters, twist.
    Unknown keys are dropped so the UI can't stuff arbitrary junk in.
    """
    return {
        "logline": str(raw.get("logline", "")).strip(),
        "synopsis": str(raw.get("synopsis", "")).strip(),
        "tone": str(raw.get("tone", "")).strip(),
        "target_length_sec": int(raw.get("target_length_sec", 30) or 30),
        "characters": list(raw.get("characters") or []),
        "twist": str(raw.get("twist", "")).strip(),
    }


@app.patch("/api/sketch/{sketch_id}/premise")
def edit_sketch_premise(sketch_id: str, body: PremiseEditIn) -> JSONResponse:
    """Phase 10: update a single premise on a per-model variant in place.

    The variant file on disk (`queues/premise-review/{sketch_id}__{model}.json`)
    has its `premises[premise_index]` replaced with the user-edited payload.
    The sketch gains a `human_edit_premise` event in its history. If the
    edited premise is currently the sketch's canonical premise, that gets
    rewritten too so the UI reflects the change immediately.
    """
    store = get_store()
    try:
        sketch = store.get_sketch(sketch_id)
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc))

    marker_path = _variant_marker_path(store, sketch_id, body.model_id)
    if not marker_path.exists():
        raise HTTPException(
            status_code=404,
            detail=f"variant {body.model_id} not found for {sketch_id}",
        )
    try:
        payload = _read_variant_marker(marker_path)
    except json.JSONDecodeError as exc:
        raise HTTPException(status_code=500, detail=f"variant file corrupt: {exc}")

    premises = list(payload.get("premises") or [])
    if body.premise_index < 0 or body.premise_index >= len(premises):
        raise HTTPException(
            status_code=400,
            detail=f"premise_index {body.premise_index} out of range (have {len(premises)})",
        )

    new_premise = _normalize_premise_payload(body.premise)
    premises[body.premise_index] = new_premise
    payload["premises"] = premises
    payload["premise_count"] = len(premises)
    _write_variant_marker(marker_path, payload)

    sketch.history.append(
        {
            "from": None,
            "to": None,
            "at": _now(),
            "event": "human_edit_premise",
            "payload": {
                "model_id": body.model_id,
                "premise_index": body.premise_index,
                "logline": new_premise.get("logline", ""),
            },
        }
    )
    store.save_sketch(sketch)

    return JSONResponse(
        content={
            "sketch_id": sketch_id,
            "model_id": body.model_id,
            "premise_index": body.premise_index,
            "premise": new_premise,
            "status": sketch.status.value,
        }
    )


@app.post("/api/sketch/{sketch_id}/premise")
def add_sketch_premise(sketch_id: str, body: PremiseAddIn) -> JSONResponse:
    """Phase 10: add a new human-authored premise to a sketch.

    Creates / appends to a `{sketch_id}__human.json` variant marker under
    `queues/premise-review/`. If the human variant already exists, the new
    premise is appended; otherwise a fresh marker is created.
    """
    store = get_store()
    try:
        sketch = store.get_sketch(sketch_id)
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc))

    new_premise = _normalize_premise_payload(body.premise)

    marker_path = _variant_marker_path(store, sketch_id, "human")
    if marker_path.exists():
        try:
            payload = _read_variant_marker(marker_path)
        except json.JSONDecodeError:
            payload = {}
        premises = list(payload.get("premises") or [])
        premises.append(new_premise)
        payload["sketch_id"] = sketch_id
        payload["signal_id"] = sketch.signal_id or ""
        payload["model_id"] = "human"
        payload["premises"] = premises
        payload["premise_count"] = len(premises)
        payload.setdefault("generated_at", _now())
        payload.setdefault("cost_cents", 0)
        payload.setdefault("duration_ms", 0)
        payload.setdefault("error", None)
    else:
        payload = {
            "sketch_id": sketch_id,
            "signal_id": sketch.signal_id or "",
            "model_id": "human",
            "generated_at": _now(),
            "premise_count": 1,
            "cost_cents": 0,
            "duration_ms": 0,
            "error": None,
            "premises": [new_premise],
        }
    _write_variant_marker(marker_path, payload)

    sketch.history.append(
        {
            "from": None,
            "to": None,
            "at": _now(),
            "event": "human_add_premise",
            "payload": {
                "model_id": "human",
                "premise_index": len(payload.get("premises") or []) - 1,
                "logline": new_premise.get("logline", ""),
            },
        }
    )
    store.save_sketch(sketch)

    return JSONResponse(
        content={
            "sketch_id": sketch_id,
            "model_id": "human",
            "premise_index": len(payload.get("premises") or []) - 1,
            "premise": new_premise,
            "variant_premise_count": len(payload.get("premises") or []),
            "status": sketch.status.value,
        }
    )


def _write_beats_sidecar(store: Store, sketch_id: str, beats: List[Dict[str, Any]]) -> Path:
    """Phase 10: mirror `sketch.beats` into a sidecar `beats.json` file.

    Downstream pipelines still read `sketch.beats` from `sketch.json` so the
    sidecar is informational — it's what the plan's acceptance criteria says
    to `cat` after a beat edit. Writing both keeps the source of truth on
    the sketch and also satisfies the plan's file shape.
    """
    path = store.sketch_dir(sketch_id) / "beats.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps({"sketch_id": sketch_id, "beats": beats}, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return path


@app.patch("/api/sketch/{sketch_id}/beat/{beat_n}")
def edit_sketch_beat(sketch_id: str, beat_n: int, body: BeatEditIn) -> JSONResponse:
    """Phase 10: update a single beat on a sketch.

    Finds the beat by its `n` field (1-indexed, matching how the pipeline
    writes them), applies only the provided fields, writes a
    `beats.json` sidecar in the sketch directory, and appends a
    `human_edit_beat` event to the sketch history. The canonical beat list
    on `sketch.beats` is also updated so downstream code sees the edit.
    """
    store = get_store()
    try:
        sketch = store.get_sketch(sketch_id)
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc))

    beats = list(sketch.beats or [])
    target_index: Optional[int] = None
    for i, beat in enumerate(beats):
        try:
            if int(beat.get("n", -1)) == int(beat_n):
                target_index = i
                break
        except (TypeError, ValueError):
            continue
    if target_index is None:
        raise HTTPException(status_code=404, detail=f"beat {beat_n} not found on {sketch_id}")

    updates = body.model_dump(exclude_none=True)
    beat = dict(beats[target_index])
    beat.update(updates)
    beats[target_index] = beat
    sketch.beats = beats

    sketch.history.append(
        {
            "from": None,
            "to": None,
            "at": _now(),
            "event": "human_edit_beat",
            "payload": {
                "beat_n": int(beat_n),
                "fields_updated": sorted(updates.keys()),
            },
        }
    )
    store.save_sketch(sketch)
    sidecar_path = _write_beats_sidecar(store, sketch_id, beats)

    return JSONResponse(
        content={
            "sketch_id": sketch_id,
            "beat_n": int(beat_n),
            "beat": beat,
            "beats_sidecar_path": str(sidecar_path),
            "status": sketch.status.value,
        }
    )


# ----------------------------------------------------------------- leaderboard


@app.get("/api/leaderboard")
def get_leaderboard_endpoint() -> JSONResponse:
    return JSONResponse(content=get_leaderboard().get_leaderboard())


# ----------------------------------------------------------------- signals


@app.get("/api/signals")
def list_signals() -> JSONResponse:
    store = get_store()
    lens = _load_lens()
    rejected = _load_rejected_signals(store)

    rows: List[Dict[str, Any]] = []
    for path in _iter_signal_files(store):
        meta = _parse_signal_file(path)
        if not meta:
            continue
        signal_id = meta.get("id") or path.stem
        captured = _parse_iso(str(meta.get("captured_at", "")))
        age_hours = _hours_since(captured)
        if age_hours is not None and age_hours > SIGNAL_FRESHNESS_HOURS:
            continue
        promoted = _is_promoted(store, signal_id)
        is_rejected = signal_id in rejected
        rows.append(_build_signal_summary(meta, lens, promoted, is_rejected))

    rows.sort(key=lambda r: (-int(r.get("score") or 0), r.get("captured_at", "")))
    return JSONResponse(content={"signals": rows})


@app.post("/api/signals/{signal_id}/promote")
def promote_signal(
    signal_id: str,
    body: Optional[PromoteSignalIn] = None,
) -> JSONResponse:
    """Promote a signal into the idea-factory queue.

    Phase 10: the body now accepts an optional `{"guidance": "..."}` field.
    When the promoter typed guidance text in the Signals page dialog, it
    gets stored on the queue manifest as `user_guidance` and the idea
    factory passes it into every model adapter's prompt. Missing / empty
    guidance omits the field entirely so the behavior is identical to
    Phase 2 for unannotated promotes.
    """
    store = get_store()
    lens = _load_lens()
    path = _find_signal_file(store, signal_id)
    if path is None:
        raise HTTPException(status_code=404, detail=f"signal {signal_id} not found")
    meta = _parse_signal_file(path)
    if not meta:
        raise HTTPException(status_code=500, detail="signal file unparseable")

    if _is_promoted(store, signal_id):
        return JSONResponse(content={"signal_id": signal_id, "promoted": True, "already": True})

    title = meta.get("title", "")
    body_text = meta.get("_body") or meta.get("_summary") or ""
    score = lens.score(title, body_text)
    payload: Dict[str, Any] = {
        "signal_id": signal_id,
        "source": meta.get("source", "unknown"),
        "source_url": meta.get("source_url", ""),
        "title": title,
        "summary": meta.get("_summary", ""),
        "sketchability_score": score,
        "comedy_angles": [
            {"angle": "manual", "note": "force-promoted from signals page"},
        ],
        "character_archetypes": ["everyman", "authority figure"],
        "topical_window_hours": 48,
        "should_promote": True,
        "analyzed_at": _now(),
        "source_item_path": str(path),
        "force_promoted": True,
    }
    guidance_text = (body.guidance or "").strip() if body is not None else ""
    if guidance_text:
        payload["user_guidance"] = guidance_text
    store.write_queue_marker("idea-factory", signal_id, payload)
    new_sketches = stub_factory.run_factory(store)
    return JSONResponse(
        content={
            "signal_id": signal_id,
            "promoted": True,
            "score": score,
            "new_sketches": new_sketches,
            "user_guidance": guidance_text or None,
        }
    )


@app.post("/api/signals/{signal_id}/reject")
def reject_signal(signal_id: str) -> JSONResponse:
    store = get_store()
    rejected = _load_rejected_signals(store)
    rejected.add(signal_id)
    _save_rejected_signals(store, rejected)
    return JSONResponse(content={"signal_id": signal_id, "rejected": True})


# ----------------------------------------------------------------- manual idea


@app.post("/api/manual_idea")
def manual_idea(body: ManualIdeaIn) -> JSONResponse:
    store = get_store()
    text = body.text.strip()
    if not text:
        raise HTTPException(status_code=400, detail="text required")

    digest = hashlib.sha1(f"manual::{text}::{_now()}".encode("utf-8")).hexdigest()[:6]
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    sketch_id = f"sk-{today}-m{digest}"

    premise: Dict[str, Any] = {
        "logline": text,
        "synopsis": text,
        "tone": "manual",
        "target_length_sec": 30,
        "characters": [],
        "twist": "",
    }
    sketch = Sketch(
        id=sketch_id,
        status=Status.PREMISE_REVIEW,
        signal_id=f"manual-{digest}",
        premise=premise,
        premises=[premise],
    )
    sketch.history.append(
        {
            "from": Status.IDEA_PENDING.value,
            "to": Status.PREMISE_REVIEW.value,
            "at": _now(),
            "payload": {"source": "manual"},
        }
    )
    store.save_sketch(sketch)
    store.write_queue_marker(
        "premise-review",
        sketch_id,
        {"sketch_id": sketch_id, "source": "manual", "queued_at": _now()},
    )
    backend_events.publish_event(
        "pipeline_update",
        {"sketch_id": sketch_id, "from": None, "to": "premise_review", "source": "manual"},
    )
    return JSONResponse(content=sketch.to_dict())


# ----------------------------------------------------------------- Phase 7: events + stats + bulk reject


@app.get("/api/events")
async def events_stream() -> StreamingResponse:
    """Server-sent events stream.

    The UI listens at this URL at boot and re-fetches the current page
    whenever a `pipeline_update` event arrives. Keepalive comments are
    sent every 15s so idle proxies don't close the connection.
    """
    client_id = await backend_events.subscribe()
    return StreamingResponse(
        backend_events.iter_events(client_id),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",  # disable nginx buffering if fronted
        },
    )


@app.get("/api/stats/cost")
def stats_cost() -> JSONResponse:
    """Daily / weekly / all-time cost rollups broken down by stage + provider."""
    store = get_store()
    return JSONResponse(content=backend_stats.cost_stats(store))


@app.get("/api/stats/insights")
def stats_insights() -> JSONResponse:
    """Top approved loglines + approval rate per signal source (last 30 days)."""
    store = get_store()
    return JSONResponse(content=backend_stats.insights_stats(store))


class BulkRejectIn(BaseModel):
    signal_ids: List[str]


@app.post("/api/signals/bulk_reject")
def bulk_reject_signals(body: BulkRejectIn) -> JSONResponse:
    """Mark a batch of signals as user-rejected.

    Persists into `data/rejected-signals.json` so the Signals page can
    hide them in the listing. Does not touch sketches — that's a
    different endpoint.
    """
    store = get_store()
    rejected = _load_rejected_signals(store)
    ids = [str(x).strip() for x in (body.signal_ids or []) if str(x).strip()]
    for signal_id in ids:
        rejected.add(signal_id)
    _save_rejected_signals(store, rejected)
    return JSONResponse(
        content={
            "rejected_count": len(ids),
            "total_rejected_now": len(rejected),
        }
    )


# ----------------------------------------------------------------- /data route (registered LAST so it never shadows /api)
#
# We don't use `app.mount("/data", StaticFiles(...))` because the tests
# change the data root per-test via the AI_VIDS_DATA_ROOT env var, and
# a static mount is bound at app import time. Instead we register a
# dynamic route that resolves the data root on every request and
# returns the requested file if it lives inside it.


@app.get("/data/{file_path:path}")
def serve_data_file(file_path: str) -> FileResponse:
    data_root = _data_root().resolve()
    target = (data_root / file_path).resolve()
    try:
        target.relative_to(data_root)
    except ValueError:
        raise HTTPException(status_code=403, detail="path escapes data root")
    if not target.exists() or not target.is_file():
        raise HTTPException(status_code=404, detail="not found")
    return FileResponse(str(target))
