"""Stats aggregation for the Phase 7 dashboard widgets.

Two endpoints call into here:

    GET /api/stats/cost      -> cost_stats(store)
    GET /api/stats/insights  -> insights_stats(store)

The data set is small enough (a few hundred sketches tops) that we
walk every sketch on every request rather than pre-aggregate. Both
functions are pure and take a `Store` so they're trivial to test
against a tmp_path.
"""
from __future__ import annotations

import logging
from collections import Counter, defaultdict
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

from state.store import Sketch, Store


LOG = logging.getLogger("backend.stats")


# ----------------------------------------------------------------- date helpers


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


def _today_start(now: Optional[datetime] = None) -> datetime:
    now = now or datetime.now(timezone.utc)
    return now.replace(hour=0, minute=0, second=0, microsecond=0)


# ----------------------------------------------------------------- cost stats


# Every sketch's cost is split across four stages. We walk the stored
# sketch JSON and pull per-stage numbers out of the fields each phase
# already persists:
#
#   premise     : sketch.history[].payload.variants (Phase 3 factory)
#   storyboard  : data/sketches/{id}/storyboard.json characters+frames (Phase 4)
#   video       : data/sketches/{id}/clips.json clips (Phase 5)
#   critic      : data/sketches/{id}/critic.json (Phase 6)
#
# Numbers the adapters report are already in integer cents.


STAGES = ("premise", "storyboard", "video", "critic")


def _sketch_cost_breakdown(store: Store, sketch: Sketch) -> Dict[str, Any]:
    """Return per-stage/provider cost breakdown for one sketch."""
    per_stage: Dict[str, int] = {stage: 0 for stage in STAGES}
    per_provider: Counter = Counter()

    # Premise stage — Phase 3 variants live as markers, but the
    # canonical record is the history entry the factory writes.
    for h in sketch.history or []:
        payload = h.get("payload") if isinstance(h, dict) else None
        if not isinstance(payload, dict):
            continue
        variants = payload.get("variants")
        if isinstance(variants, list):
            for variant in variants:
                if not isinstance(variant, dict):
                    continue
                cost = int(variant.get("cost_cents", 0) or 0)
                per_stage["premise"] += cost
                per_provider[f"premise:{variant.get('model_id', 'unknown')}"] += cost

    # Storyboard stage — read storyboard.json.
    storyboard_json = store.sketch_dir(sketch.id) / "storyboard.json"
    if storyboard_json.exists():
        try:
            import json
            meta = json.loads(storyboard_json.read_text(encoding="utf-8"))
        except Exception:
            meta = {}
        adapter_id = meta.get("adapter_id", "unknown")
        for ref in (meta.get("characters") or []):
            if not isinstance(ref, dict):
                continue
            cost = int(ref.get("cost_cents", 0) or 0)
            per_stage["storyboard"] += cost
            per_provider[f"storyboard:{adapter_id}"] += cost
        for frame in (meta.get("frames") or []):
            if not isinstance(frame, dict):
                continue
            cost = int(frame.get("cost_cents", 0) or 0)
            per_stage["storyboard"] += cost
            per_provider[f"storyboard:{adapter_id}"] += cost

    # Video stage — read clips.json.
    clips_json = store.sketch_dir(sketch.id) / "clips.json"
    if clips_json.exists():
        try:
            import json
            meta = json.loads(clips_json.read_text(encoding="utf-8"))
        except Exception:
            meta = {}
        adapter_id = meta.get("adapter_id", "unknown")
        for clip in (meta.get("clips") or []):
            if not isinstance(clip, dict):
                continue
            cost = int(clip.get("cost_cents", 0) or 0)
            per_stage["video"] += cost
            per_provider[f"video:{adapter_id}"] += cost

    # Critic stage — read critic.json.
    critic_json = store.sketch_dir(sketch.id) / "critic.json"
    if critic_json.exists():
        try:
            import json
            meta = json.loads(critic_json.read_text(encoding="utf-8"))
        except Exception:
            meta = {}
        cost = int(meta.get("cost_cents", 0) or 0)
        adapter_id = meta.get("adapter_id", "unknown")
        per_stage["critic"] += cost
        per_provider[f"critic:{adapter_id}"] += cost

    total = sum(per_stage.values())
    return {
        "sketch_id": sketch.id,
        "updated_at": sketch.updated_at,
        "total_cents": total,
        "per_stage": per_stage,
        "per_provider": dict(per_provider),
    }


def cost_stats(store: Store, *, now: Optional[datetime] = None) -> Dict[str, Any]:
    """Today / yesterday / this-week cost rollups broken down by stage + provider."""
    now = now or datetime.now(timezone.utc)
    today = _today_start(now)
    yesterday = today - timedelta(days=1)
    week_start = today - timedelta(days=now.weekday())  # monday this week

    buckets = {
        "today": {"total": 0, "per_stage": {s: 0 for s in STAGES}, "per_provider": Counter()},
        "yesterday": {"total": 0, "per_stage": {s: 0 for s in STAGES}, "per_provider": Counter()},
        "this_week": {"total": 0, "per_stage": {s: 0 for s in STAGES}, "per_provider": Counter()},
        "all_time": {"total": 0, "per_stage": {s: 0 for s in STAGES}, "per_provider": Counter()},
    }

    per_sketch: List[Dict[str, Any]] = []
    for sketch in store.list_sketches():
        breakdown = _sketch_cost_breakdown(store, sketch)
        per_sketch.append(breakdown)
        updated_at = _parse_iso(sketch.updated_at or "") or now
        slots: List[str] = ["all_time"]
        if updated_at >= today:
            slots.append("today")
        if yesterday <= updated_at < today:
            slots.append("yesterday")
        if updated_at >= week_start:
            slots.append("this_week")
        for slot in slots:
            buckets[slot]["total"] += breakdown["total_cents"]
            for stage, cents in breakdown["per_stage"].items():
                buckets[slot]["per_stage"][stage] += cents
            for provider, cents in breakdown["per_provider"].items():
                buckets[slot]["per_provider"][provider] += cents

    # Convert Counters to plain dicts for JSON serialization.
    for slot in buckets.values():
        slot["per_provider"] = dict(slot["per_provider"])

    return {
        "generated_at": now.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "sketch_count": len(per_sketch),
        "buckets": buckets,
        "per_sketch": per_sketch,
    }


# ----------------------------------------------------------------- insights


def insights_stats(store: Store, *, top_n: int = 10, days: int = 30) -> Dict[str, Any]:
    """Top approved loglines + approval rate by signal source (last N days)."""
    now = datetime.now(timezone.utc)
    window_start = now - timedelta(days=days)

    approved: List[Dict[str, Any]] = []
    per_source: Dict[str, Dict[str, int]] = defaultdict(
        lambda: {"total": 0, "published": 0, "rejected": 0}
    )

    for sketch in store.list_sketches():
        updated = _parse_iso(sketch.updated_at or "") or now
        if updated < window_start:
            continue
        source = "unknown"
        signal_id = sketch.signal_id or ""
        if signal_id.startswith("reddit-"):
            source = "reddit"
        elif signal_id.startswith("hn-"):
            source = "hacker_news"
        elif signal_id.startswith("gn-"):
            source = "google_news"
        elif signal_id.startswith("yt-"):
            source = "youtube_trending"
        elif signal_id.startswith("manual-"):
            source = "manual"
        elif signal_id.startswith("reddit-stub-"):
            source = "reddit_stub"

        per_source[source]["total"] += 1
        status = sketch.status.value if sketch.status else "unknown"
        if status == "published":
            per_source[source]["published"] += 1
            premise = sketch.premise or {}
            approved.append(
                {
                    "sketch_id": sketch.id,
                    "source": source,
                    "logline": premise.get("logline", ""),
                    "tone": premise.get("tone", ""),
                    "updated_at": sketch.updated_at,
                }
            )
        elif status == "rejected":
            per_source[source]["rejected"] += 1

    # Sort approved loglines newest-first, then clip to top_n.
    approved.sort(key=lambda row: row.get("updated_at") or "", reverse=True)
    top_approved = approved[:top_n]

    # Attach approval rate per source.
    source_rows = []
    for source, counts in sorted(per_source.items()):
        decided = counts["published"] + counts["rejected"]
        rate = (counts["published"] / decided) if decided > 0 else 0.0
        source_rows.append(
            {
                "source": source,
                "total": counts["total"],
                "published": counts["published"],
                "rejected": counts["rejected"],
                "approval_rate": round(rate, 3),
            }
        )

    return {
        "generated_at": now.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "window_days": days,
        "top_approved": top_approved,
        "per_source": source_rows,
    }


__all__ = ["STAGES", "cost_stats", "insights_stats"]
