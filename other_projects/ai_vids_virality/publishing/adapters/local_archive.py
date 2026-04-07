"""LocalArchivePublisher — always works, no API.

Copies the sketch's final cut, sketch.json, and critic.json into
`data/published/{sketch_id}/`, and writes a `published_at.txt` stamp.
This is the only publisher that's always available, so the backend
can transition a sketch to PUBLISHED even when no external destinations
are configured.
"""
from __future__ import annotations

import logging
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Optional

from publishing.adapter import Publisher, PublishResult
from state.store import Sketch, Store


LOG = logging.getLogger("publishing.adapters.local_archive")


def _now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


class LocalArchivePublisher(Publisher):
    destination_id = "local_archive"

    def is_available(self) -> bool:
        return True

    def publish(self, sketch: Sketch, store: Store) -> PublishResult:
        result = PublishResult(
            destination_id=self.destination_id,
            success=False,
        )
        archive_dir = store.published_dir / sketch.id
        try:
            archive_dir.mkdir(parents=True, exist_ok=True)
        except Exception as exc:
            result.error = f"could not create archive dir: {exc}"
            return result

        # Copy final.mp4 (if it exists on disk).
        final_src = store.sketch_final_path(sketch.id)
        final_dst = archive_dir / "final.mp4"
        if final_src.exists():
            try:
                shutil.copyfile(final_src, final_dst)
            except Exception as exc:
                result.error = f"final.mp4 copy failed: {exc}"
                return result
        else:
            # Without a final cut there's nothing to publish, but we
            # still write sketch/critic metadata so the archive is
            # at least inspectable.
            LOG.warning("sketch %s has no final.mp4 on disk at publish time", sketch.id)

        # Copy sketch.json (canonical state at publish time).
        sketch_src = store.sketch_json_path(sketch.id)
        sketch_dst = archive_dir / "sketch.json"
        if sketch_src.exists():
            try:
                shutil.copyfile(sketch_src, sketch_dst)
            except Exception as exc:
                result.error = f"sketch.json copy failed: {exc}"
                return result

        # Copy critic.json (Phase 6 output) if present.
        critic_src = store.sketch_dir(sketch.id) / "critic.json"
        critic_dst = archive_dir / "critic.json"
        if critic_src.exists():
            try:
                shutil.copyfile(critic_src, critic_dst)
            except Exception as exc:
                LOG.warning("critic.json copy failed: %s", exc)
                # Critic is optional — don't fail the publish.

        # Copy clips.json (Phase 5 output) if present.
        clips_src = store.sketch_dir(sketch.id) / "clips.json"
        clips_dst = archive_dir / "clips.json"
        if clips_src.exists():
            try:
                shutil.copyfile(clips_src, clips_dst)
            except Exception as exc:
                LOG.warning("clips.json copy failed: %s", exc)

        # Published_at stamp.
        stamp = _now_iso()
        try:
            (archive_dir / "published_at.txt").write_text(stamp + "\n", encoding="utf-8")
        except Exception as exc:
            LOG.warning("published_at.txt write failed: %s", exc)

        result.success = True
        result.url = f"file://{archive_dir.resolve()}"
        result.extra = {
            "archive_dir": str(archive_dir),
            "published_at": stamp,
            "final_mp4_present": final_src.exists(),
        }
        return result


__all__ = ["LocalArchivePublisher"]
