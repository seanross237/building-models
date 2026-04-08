"""StubPublisher — no-op placeholder used for destinations that aren't wired yet.

Matches the `Publisher` ABC and always returns success with a
descriptive URL so the UI can see the destination was attempted.
Used for `tiktok` and `x` entries in `config/publishing.yaml` until
real adapters ship.
"""
from __future__ import annotations

import logging

from publishing.adapter import Publisher, PublishResult
from state.store import Sketch, Store


LOG = logging.getLogger("publishing.adapters.stub_publisher")


class StubPublisher(Publisher):
    destination_id = "stub"

    def is_available(self) -> bool:
        # Stubs are always "available" so the routing layer can decide
        # whether to run them based on the enabled flag alone.
        return True

    def publish(self, sketch: Sketch, store: Store) -> PublishResult:
        LOG.info(
            "stub publish: destination=%s sketch=%s (no external call made)",
            self.destination_id,
            sketch.id,
        )
        return PublishResult(
            destination_id=self.destination_id,
            success=True,
            url=f"stub://{self.destination_id}/{sketch.id}",
            extra={"stub": True},
        )


__all__ = ["StubPublisher"]
