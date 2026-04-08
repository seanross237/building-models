"""Multi-model idea factory.

Reads `data/queues/idea-factory/`, for each unconsumed signal runs every
enabled `ModelAdapter` from `config/models.yaml`, and writes one
`PremiseResult` per model to
`data/queues/premise-review/{sketch_id}__{model_id}.json`. The signal also
becomes a `Sketch` in `PREMISE_REVIEW`, with a `variants` field on the
sketch listing every model that contributed.

Adapters run sequentially. One adapter failing does not block the others.
If every adapter fails for a signal, no sketch is created and the signal
is left in the idea-factory queue so the next run can retry.
"""
from __future__ import annotations

import hashlib
import importlib
import json
import logging
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from idea_factory.adapter import ModelAdapter, PremiseResult
from state.leaderboard import Leaderboard
from state.machine import Status
from state.store import Sketch, Store


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MODELS_PATH = PROJECT_ROOT / "config" / "models.yaml"
DEFAULT_PROMPT_PATH = PROJECT_ROOT / "idea_factory" / "prompts" / "premise_generation.md"
DEFAULT_LENS_PATH = PROJECT_ROOT / "config" / "comedy-lens.md"

LOG = logging.getLogger("idea_factory.factory")


# ----------------------------------------------------------------- config


def _load_models_config(path: Path) -> Dict[str, Any]:
    if not path.exists():
        return {"default_n_premises": 3, "models": []}
    try:
        import yaml  # type: ignore
        data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    except Exception as exc:
        LOG.warning("could not read models.yaml: %s", exc)
        return {"default_n_premises": 3, "models": []}
    if not isinstance(data, dict):
        return {"default_n_premises": 3, "models": []}
    data.setdefault("default_n_premises", 3)
    data.setdefault("models", [])
    return data


def _load_prompt_template(path: Path = DEFAULT_PROMPT_PATH) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8")


def _load_lens_excerpt(path: Path = DEFAULT_LENS_PATH, max_chars: int = 2000) -> str:
    if not path.exists():
        return ""
    text = path.read_text(encoding="utf-8")
    return text[:max_chars]


def _instantiate_adapter(entry: Dict[str, Any]) -> Optional[ModelAdapter]:
    dotted = entry.get("adapter")
    if not dotted:
        LOG.warning("models.yaml entry missing 'adapter': %s", entry)
        return None
    module_path, _, class_name = str(dotted).rpartition(".")
    if not module_path or not class_name:
        LOG.warning("invalid adapter path: %s", dotted)
        return None
    try:
        module = importlib.import_module(module_path)
        cls = getattr(module, class_name)
    except Exception as exc:
        LOG.warning("could not import adapter %s: %s", dotted, exc)
        return None
    config = dict(entry.get("config") or {})
    if "id" in entry:
        config["id"] = entry["id"]
    try:
        return cls(config=config)
    except Exception as exc:
        LOG.warning("could not instantiate adapter %s: %s", dotted, exc)
        return None


def load_adapters(models_config_path: Path = DEFAULT_MODELS_PATH) -> List[ModelAdapter]:
    cfg = _load_models_config(models_config_path)
    adapters: List[ModelAdapter] = []
    for entry in cfg.get("models", []) or []:
        if not entry.get("enabled"):
            continue
        adapter = _instantiate_adapter(entry)
        if adapter is not None:
            adapters.append(adapter)
    return adapters


# ----------------------------------------------------------------- prompt + signal


def _build_user_guidance_section(signal: Dict[str, Any]) -> str:
    """Phase 10: render the optional human guidance block.

    When the promoter typed something into the "what angle / spin are you
    thinking?" textarea on the Signals page, that text lives on the queue
    manifest as `user_guidance`. We splice it into the premise-generation
    prompt so every model adapter sees the producer's intuition.
    """
    guidance = signal.get("user_guidance")
    if not guidance or not str(guidance).strip():
        return ""
    return f"## Human guidance\n\n{str(guidance).strip()}\n"


def _format_prompt(template: str, signal: Dict[str, Any], n: int, lens: str) -> str:
    # `_build_user_guidance_section` returns either an empty string or a
    # fully-rendered markdown block. The template has a `{user_guidance_section}`
    # placeholder positioned between the Signal block and the Task block.
    return template.format(
        signal_title=str(signal.get("title", "")),
        signal_source=str(signal.get("source", "")),
        signal_url=str(signal.get("source_url", "")),
        signal_summary=str(signal.get("summary", "")),
        n_premises=n,
        comedy_lens=lens or "(comedy lens not available)",
        user_guidance_section=_build_user_guidance_section(signal),
    )


def _now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _make_sketch_id(signal_id: str) -> str:
    digest = hashlib.sha1(signal_id.encode("utf-8")).hexdigest()[:6]
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    return f"sk-{today}-{digest}"


def _signal_already_consumed(store: Store, signal_id: str) -> bool:
    for sketch in store.list_sketches():
        if sketch.signal_id == signal_id:
            return True
    return False


# ----------------------------------------------------------------- main entry


def run_factory(
    store: Store,
    models_config_path: Path = DEFAULT_MODELS_PATH,
    prompt_template: Optional[str] = None,
    lens_text: Optional[str] = None,
    leaderboard: Optional[Leaderboard] = None,
    adapters: Optional[List[ModelAdapter]] = None,
) -> List[str]:
    """Run the multi-model factory across the idea-factory queue.

    Returns the list of sketch IDs created during this invocation. The
    `adapters` and `leaderboard` kwargs are exposed primarily for tests so
    they can wire in fakes without touching `models.yaml` or the real
    leaderboard file.
    """
    if adapters is None:
        adapters = load_adapters(models_config_path)
    if not adapters:
        LOG.info("no adapters enabled, factory is a no-op")
        return []

    cfg = _load_models_config(models_config_path)
    default_n = int(cfg.get("default_n_premises", 3) or 3)

    template = prompt_template if prompt_template is not None else _load_prompt_template()
    lens = lens_text if lens_text is not None else _load_lens_excerpt()
    if leaderboard is None:
        leaderboard = Leaderboard(store.root / "leaderboard.json")

    new_sketch_ids: List[str] = []
    for marker_path in store.list_queue("idea-factory"):
        signal_payload = store.read_queue_marker(marker_path)
        signal_id = str(signal_payload.get("signal_id") or marker_path.stem)
        if _signal_already_consumed(store, signal_id):
            continue

        prompt = _format_prompt(template, signal_payload, default_n, lens)

        results: List[PremiseResult] = []
        for adapter in adapters:
            try:
                result = adapter.generate(signal_payload, prompt, n_premises=default_n)
            except Exception as exc:  # adapters MUST not raise; this is the safety net
                LOG.warning("adapter %s raised: %s", getattr(adapter, "model_id", "?"), exc)
                result = PremiseResult(
                    model_id=getattr(adapter, "model_id", "unknown"),
                    signal_id=signal_id,
                    error=f"adapter raised: {exc}",
                )
            results.append(result)
            if result.premises and not result.error:
                leaderboard.record_generation(result.model_id)
            elif result.error:
                LOG.warning(
                    "adapter %s failed for %s: %s",
                    result.model_id,
                    signal_id,
                    result.error,
                )

        successful = [r for r in results if r.premises and not r.error]
        if not successful:
            LOG.warning("all adapters failed for %s, skipping sketch creation", signal_id)
            continue

        sketch_id = _make_sketch_id(signal_id)
        if store.sketch_json_path(sketch_id).exists():
            continue

        # Persist each variant as its own marker file under premise-review.
        variants_meta: List[Dict[str, Any]] = []
        for result in results:
            marker_id = f"{sketch_id}__{result.model_id}"
            payload = {
                "sketch_id": sketch_id,
                "signal_id": signal_id,
                "model_id": result.model_id,
                "generated_at": _now(),
                "premise_count": len(result.premises),
                "cost_cents": result.cost_cents,
                "duration_ms": result.duration_ms,
                "error": result.error,
                "premises": [p.to_dict() for p in result.premises],
            }
            store.write_queue_marker("premise-review", marker_id, payload)
            variants_meta.append(
                {
                    "model_id": result.model_id,
                    "premise_count": len(result.premises),
                    "cost_cents": result.cost_cents,
                    "duration_ms": result.duration_ms,
                    "error": result.error,
                }
            )

        # The sketch's canonical premise defaults to the first premise from
        # the first successful model — the human can override at review time.
        first = successful[0]
        canonical_premise = first.premises[0].to_dict()
        sketch = Sketch(
            id=sketch_id,
            status=Status.PREMISE_REVIEW,
            signal_id=signal_id,
            premise=canonical_premise,
            premises=[p.to_dict() for p in first.premises],
        )
        sketch.history.append(
            {
                "from": Status.IDEA_PENDING.value,
                "to": Status.PREMISE_REVIEW.value,
                "at": _now(),
                "payload": {
                    "factory": "multi_model",
                    "variants": variants_meta,
                    "signal_title": signal_payload.get("title", ""),
                },
            }
        )
        # Phase 10: if the human typed guidance text at promote time, stamp
        # a `human_promote_with_guidance` event onto the sketch history so
        # the UI / stats layer can see that this sketch was producer-steered.
        guidance = signal_payload.get("user_guidance")
        if guidance and str(guidance).strip():
            sketch.history.append(
                {
                    "from": None,
                    "to": None,
                    "at": _now(),
                    "event": "human_promote_with_guidance",
                    "payload": {"guidance": str(guidance).strip()},
                }
            )
        store.save_sketch(sketch)
        new_sketch_ids.append(sketch_id)

    return new_sketch_ids


__all__ = ["load_adapters", "run_factory"]
