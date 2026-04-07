"""Fal.ai image adapter for the storyboard layer.

Routes character ref + per-beat frame generation through fal's
nano-banana-2 endpoint (Google's Nano Banana 2 image model). One key
(`FAL_KEY` / `FAL_API_KEY`) unlocks both the text-to-image variant for
character refs and the image-edit variant for per-beat frames
conditioned on the refs.

Verified slugs against the reference integration at
`serenade/serve_boldly/supabase/functions/generate-mockups/index.ts`:

    fal-ai/nano-banana-2          - text-to-image (character refs)
    fal-ai/nano-banana-2/edit     - text + image_urls -> image (per-beat frames)

Request body fields match the serve_boldly production integration:
`prompt`, `num_images`, `aspect_ratio`, `resolution: "1K"`,
`output_format: "png"`, `safety_tolerance: 4`. The edit endpoint
additionally takes `image_urls: [url1, url2, ...]`.

Both return `{"images": [{"url": "..."}]}`.

Auth + queue API match the pattern in `video_gen/adapters/fal_unified.py`:

    POST  https://queue.fal.run/{model_slug}        Authorization: Key
    GET   https://queue.fal.run/{slug}/requests/{id}/status
    GET   https://queue.fal.run/{slug}/requests/{id}

The CDN upload endpoint (used to host character ref PNGs as URLs the
edit endpoint can consume) uses `Bearer` auth, not `Key`:

    POST  https://fal.media/files/upload            Authorization: Bearer
"""
from __future__ import annotations

import logging
import os
import time
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional

from storyboard._common import copy_placeholder, slugify
from storyboard.adapter import CharacterRef, Frame, StoryboardAdapter


LOG = logging.getLogger("storyboard.adapters.fal_image")

QUEUE_BASE = "https://queue.fal.run"
CDN_UPLOAD_URL = "https://fal.media/files/upload"

ENV_KEY_PRIMARY = "FAL_KEY"
ENV_KEY_ALT = "FAL_API_KEY"

DEFAULT_TEXT_SLUG = "fal-ai/nano-banana-2"
DEFAULT_EDIT_SLUG = "fal-ai/nano-banana-2/edit"


def _build_character_prompt(character: Dict[str, Any], style_guide: str) -> str:
    name = character.get("name") or "unnamed character"
    description = character.get("description") or ""
    return "\n".join(
        [
            "Character reference sheet for a sketch-comedy short.",
            "Front view, centered, neutral expression, plain off-white background.",
            f"Character name: {name}",
            f"Description: {description}",
            "",
            "Style guide:",
            style_guide.strip() or "(no style guide)",
        ]
    )


def _build_frame_prompt(
    beat: Dict[str, Any],
    style_guide: str,
    char_names: List[str],
) -> str:
    location = beat.get("location") or "interior"
    action = beat.get("action") or ""
    visual_note = beat.get("visual_note") or ""
    camera = beat.get("camera") or "medium"
    dialogue = beat.get("dialogue") or ""
    chars_line = ", ".join(char_names) if char_names else "(no characters)"
    pieces = [
        f"Beat {beat.get('n', 1)} — start frame.",
        f"Location: {location}",
        f"Camera: {camera} shot",
        f"Characters on screen: {chars_line}",
        f"Action: {action}",
    ]
    if dialogue:
        pieces.append(f"Dialogue: {dialogue}")
    if visual_note:
        pieces.append(f"Visual note: {visual_note}")
    pieces.append("")
    pieces.append("Style guide:")
    pieces.append(style_guide.strip() or "(no style guide)")
    pieces.append("")
    pieces.append(
        "Use the provided reference images as authoritative anchors for "
        "character faces and outfits. Return only the generated image."
    )
    return "\n".join(pieces)


def _extract_image_url(payload: Any) -> Optional[str]:
    """Pull the first image URL out of a fal nano-banana response."""
    if not isinstance(payload, dict):
        return None
    images = payload.get("images")
    if isinstance(images, list) and images:
        first = images[0]
        if isinstance(first, dict):
            url = first.get("url")
            if isinstance(url, str) and url:
                return url
    # Some fal models return `{"image": {"url": "..."}}` shape.
    image = payload.get("image")
    if isinstance(image, dict):
        url = image.get("url")
        if isinstance(url, str) and url:
            return url
    return None


class FalImageAdapter(StoryboardAdapter):
    """fal.ai nano-banana storyboard adapter."""

    adapter_id = "fal-image"

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(config)
        self.text_slug: str = str(self.config.get("text_slug", DEFAULT_TEXT_SLUG))
        self.edit_slug: str = str(self.config.get("edit_slug", DEFAULT_EDIT_SLUG))
        self.poll_interval_sec: float = float(self.config.get("poll_interval_sec", 3))
        self.timeout_sec: float = float(self.config.get("timeout_sec", 240))
        self.queue_base: str = str(self.config.get("queue_base", QUEUE_BASE))
        self.cdn_upload_url: str = str(self.config.get("cdn_upload_url", CDN_UPLOAD_URL))
        self.cost_cents_per_image: int = int(self.config.get("cost_cents_per_image", 4))

    def _api_key(self) -> str:
        return os.environ.get(ENV_KEY_PRIMARY) or os.environ.get(ENV_KEY_ALT) or ""

    def is_available(self) -> bool:
        return bool(self._api_key())

    # ----------------------------------------------------------------- HTTP helpers

    def _queue_headers(self) -> Dict[str, str]:
        return {
            "Authorization": f"Key {self._api_key()}",
            "Content-Type": "application/json",
        }

    def _cdn_headers(self, file_name: Optional[str] = None) -> Dict[str, str]:
        # CDN endpoint uses Bearer scheme (verified against fal_client source).
        headers = {
            "Authorization": f"Bearer {self._api_key()}",
            "Content-Type": "image/png",
        }
        if file_name:
            headers["X-Fal-File-Name"] = file_name
        return headers

    def _upload_to_cdn(self, path: Path, httpx_mod: Any) -> str:
        raw = path.read_bytes()
        resp = httpx_mod.post(
            self.cdn_upload_url,
            content=raw,
            headers=self._cdn_headers(file_name=path.name),
            timeout=120,
        )
        if resp.status_code not in (200, 201):
            raise RuntimeError(
                f"fal cdn upload status {resp.status_code}: {resp.text[:300]}"
            )
        payload = resp.json()
        url = payload.get("access_url") or payload.get("url")
        if not url:
            raise RuntimeError(f"fal cdn missing access_url: {payload}")
        return url

    def _submit(self, slug: str, body: Dict[str, Any], httpx_mod: Any) -> Dict[str, Any]:
        url = f"{self.queue_base}/{slug}"
        resp = httpx_mod.post(
            url, headers=self._queue_headers(), json=body, timeout=60
        )
        if resp.status_code not in (200, 201):
            raise RuntimeError(
                f"fal submit status {resp.status_code}: {resp.text[:300]}"
            )
        payload = resp.json()
        if not isinstance(payload, dict) or "request_id" not in payload:
            raise RuntimeError(f"fal submit missing request_id: {payload}")
        return payload

    def _urls_from_submit(
        self, slug: str, submit_payload: Dict[str, Any], request_id: str
    ) -> tuple[str, str]:
        """Extract (status_url, response_url) from a fal submit payload.

        fal's queue API returns these explicitly so the client doesn't have
        to know about model-slug sub-path stripping rules — for slugs like
        `nano-banana-2/edit`, fal strips the `/edit` and the poll/result
        endpoints live under just `nano-banana-2`. Reconstructing from
        the full slug yields a 405 against the real API.

        Falls back to reconstruction so existing mocked tests keep working.
        """
        status_url = submit_payload.get("status_url") if isinstance(submit_payload, dict) else None
        response_url = submit_payload.get("response_url") if isinstance(submit_payload, dict) else None
        if status_url and not response_url:
            response_url = status_url.removesuffix("/status")
        if not status_url:
            status_url = f"{self.queue_base}/{slug}/requests/{request_id}/status"
        if not response_url:
            response_url = f"{self.queue_base}/{slug}/requests/{request_id}"
        return status_url, response_url

    def _poll(
        self,
        slug: str,
        submit_payload: Dict[str, Any],
        httpx_mod: Any,
        sleep_fn: Callable[[float], None] = time.sleep,
    ) -> None:
        request_id = submit_payload.get("request_id", "") if isinstance(submit_payload, dict) else ""
        status_url, _ = self._urls_from_submit(slug, submit_payload, request_id)
        deadline = time.time() + self.timeout_sec
        while time.time() < deadline:
            resp = httpx_mod.get(status_url, headers=self._queue_headers(), timeout=30)
            # fal returns 200 when the job is COMPLETED and 202 (Accepted)
            # while it's still IN_QUEUE / IN_PROGRESS. Both are normal —
            # the body's "status" field is the source of truth.
            if resp.status_code not in (200, 202):
                raise RuntimeError(
                    f"fal poll status {resp.status_code}: {resp.text[:300]}"
                )
            payload = resp.json()
            status = (payload.get("status") or "").upper() if isinstance(payload, dict) else ""
            if status == "COMPLETED":
                return
            if status in {"FAILED", "ERROR", "CANCELLED"}:
                raise RuntimeError(f"fal request {status.lower()}: {payload}")
            sleep_fn(self.poll_interval_sec)
        raise RuntimeError(f"fal poll timed out after {self.timeout_sec}s")

    def _fetch_result(
        self, slug: str, submit_payload: Dict[str, Any], httpx_mod: Any
    ) -> Dict[str, Any]:
        request_id = submit_payload.get("request_id", "") if isinstance(submit_payload, dict) else ""
        _, response_url = self._urls_from_submit(slug, submit_payload, request_id)
        resp = httpx_mod.get(response_url, headers=self._queue_headers(), timeout=60)
        if resp.status_code != 200:
            raise RuntimeError(
                f"fal result status {resp.status_code}: {resp.text[:300]}"
            )
        return resp.json()

    def _download_image(self, url: str, out_path: Path, httpx_mod: Any) -> None:
        resp = httpx_mod.get(url, timeout=120)
        if resp.status_code != 200:
            raise RuntimeError(f"fal image download status {resp.status_code}")
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_bytes(resp.content)

    def _run_one(
        self,
        slug: str,
        body: Dict[str, Any],
        out_path: Path,
        httpx_mod: Any,
    ) -> Optional[str]:
        """Submit, poll, fetch, download. Returns the source URL on success."""
        submit = self._submit(slug, body, httpx_mod)
        self._poll(slug, submit, httpx_mod)
        result = self._fetch_result(slug, submit, httpx_mod)
        url = _extract_image_url(result)
        if not url:
            raise RuntimeError(f"fal nano-banana-2 result missing image url: {result}")
        self._download_image(url, out_path, httpx_mod)
        return url

    # ----------------------------------------------------------------- public API

    def generate_character_ref(
        self,
        character: Dict[str, Any],
        style_guide: str,
        out_path: Path,
    ) -> CharacterRef:
        name = str(character.get("name") or "unnamed")
        ref = CharacterRef(
            name=name,
            slug=slugify(name),
            path=out_path,
            prompt="",
            adapter_id=self.adapter_id,
        )

        if not self.is_available():
            ref.error = f"{ENV_KEY_PRIMARY} (or {ENV_KEY_ALT}) not set"
            copy_placeholder(out_path)
            return ref

        try:
            import httpx
        except ImportError as exc:
            ref.error = f"httpx unavailable: {exc}"
            copy_placeholder(out_path)
            return ref

        prompt = _build_character_prompt(character, style_guide)
        ref.prompt = prompt
        # Body shape mirrors the serve_boldly production integration.
        body = {
            "prompt": prompt,
            "num_images": 1,
            "aspect_ratio": "1:1",
            "resolution": "1K",
            "output_format": "png",
            "safety_tolerance": 4,
        }

        started = time.time()
        try:
            self._run_one(self.text_slug, body, out_path, httpx)
            ref.cost_cents = self.cost_cents_per_image
        except Exception as exc:
            ref.error = f"fal nano-banana-2 character ref failed: {exc}"
            copy_placeholder(out_path)
        finally:
            ref.duration_ms = int((time.time() - started) * 1000)
        return ref

    def generate_frame(
        self,
        beat: Dict[str, Any],
        character_refs: List[CharacterRef],
        style_guide: str,
        out_path: Path,
    ) -> Frame:
        beat_n = int(beat.get("n", 1) or 1)
        frame = Frame(
            beat_n=beat_n,
            path=out_path,
            prompt="",
            adapter_id=self.adapter_id,
        )

        if not self.is_available():
            frame.error = f"{ENV_KEY_PRIMARY} (or {ENV_KEY_ALT}) not set"
            copy_placeholder(out_path)
            return frame

        try:
            import httpx
        except ImportError as exc:
            frame.error = f"httpx unavailable: {exc}"
            copy_placeholder(out_path)
            return frame

        # Pick the character refs that appear in this beat.
        beat_characters = beat.get("characters") or []
        beat_names = [
            c.get("name") if isinstance(c, dict) else str(c) for c in beat_characters
        ]
        beat_names = [n for n in beat_names if n]

        prompt = _build_frame_prompt(beat, style_guide, beat_names)
        frame.prompt = prompt

        # Upload every relevant character ref PNG to fal CDN so we can
        # pass them as image_urls to nano-banana edit.
        ref_urls: List[str] = []
        relevant = [
            r for r in character_refs
            if not beat_names or r.name in beat_names
        ]
        started = time.time()
        for ref in relevant:
            try:
                ref_url = self._upload_to_cdn(Path(ref.path), httpx)
                ref_urls.append(ref_url)
            except Exception as exc:
                LOG.warning("fal cdn upload for %s failed: %s", ref.path, exc)

        if not ref_urls:
            # No anchors — fall back to the text-only model so we still
            # get a frame, just without character continuity.
            try:
                body = {
                    "prompt": prompt,
                    "num_images": 1,
                    "aspect_ratio": "16:9",
                    "resolution": "1K",
                    "output_format": "png",
                    "safety_tolerance": 4,
                }
                self._run_one(self.text_slug, body, out_path, httpx)
                frame.cost_cents = self.cost_cents_per_image
            except Exception as exc:
                frame.error = f"fal nano-banana-2 frame (text-only) failed: {exc}"
                copy_placeholder(out_path)
            finally:
                frame.duration_ms = int((time.time() - started) * 1000)
            return frame

        body = {
            "prompt": prompt,
            "image_urls": ref_urls,
            "num_images": 1,
            "aspect_ratio": "16:9",
            "resolution": "1K",
            "output_format": "png",
            "safety_tolerance": 4,
        }
        try:
            self._run_one(self.edit_slug, body, out_path, httpx)
            frame.cost_cents = self.cost_cents_per_image
        except Exception as exc:
            frame.error = f"fal nano-banana-2 frame (edit) failed: {exc}"
            copy_placeholder(out_path)
        finally:
            frame.duration_ms = int((time.time() - started) * 1000)
        return frame


__all__ = ["FalImageAdapter", "_extract_image_url"]
