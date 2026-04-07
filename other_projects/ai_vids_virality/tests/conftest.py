"""Phase 8 + 9: pytest conftest.

Three responsibilities:

1. Load `.env` so opt-in marker tests (`pytest -m fal`, `pytest -m llm`,
   `pytest -m openrouter`, etc.) can find their API keys without the
   user having to remember to `source .env` first. `override=False`
   keeps anything already set in the process environment in charge —
   that lets CI inject keys without `.env` getting in the way.

2. Stash the real `FAL_KEY` / `FAL_API_KEY` / `OPENROUTER_API_KEY`
   values aside (in module globals) and scrub them from the process
   environment at session start.

3. Provide autouse fixtures that re-scrub the keys before EVERY test,
   because `backend/main.py` and `pipelines/run_skeleton.py` call
   `load_dotenv()` at import time, which re-populates the env the
   first time any test imports the backend. The autouse fixtures
   guarantee offline tests never see the real keys, no matter what
   import-time side effects happen.

   Tests that genuinely want to call the real APIs use the
   `real_fal_key` / `real_openrouter_key` fixtures below, which
   re-inject the saved values via `monkeypatch.setenv` (auto-cleaned
   at test exit).
"""
from __future__ import annotations

import os

try:
    from dotenv import load_dotenv as _load_dotenv
    _load_dotenv(override=False)
except ImportError:
    pass

# Stash the real keys aside so the `real_*_key` fixtures can pull
# them back when an opt-in integration test asks for them.
_FAL_KEY_SAVED = os.environ.pop("FAL_KEY", None)
_FAL_API_KEY_SAVED = os.environ.pop("FAL_API_KEY", None)
_REAL_OPENROUTER_KEY = os.environ.pop("OPENROUTER_API_KEY", None)


import pytest


@pytest.fixture(autouse=True)
def _scrub_fal_keys_per_test():
    """Re-scrub FAL_KEY / FAL_API_KEY from os.environ before every test.

    Necessary because the backend's `import backend.main` triggers
    `dotenv.load_dotenv()` which re-injects the real key from `.env`
    even though conftest popped it at session start. Without this
    autouse fixture, any test that imports the backend AFTER the first
    one would see the real fal key and the routing would prefer
    fal-image / fal-video over the stub adapters tests expect.
    """
    os.environ.pop("FAL_KEY", None)
    os.environ.pop("FAL_API_KEY", None)
    yield


@pytest.fixture(autouse=True)
def _scrub_openrouter_key_per_test():
    """Re-scrub OPENROUTER_API_KEY from os.environ before every test.

    Same rationale as `_scrub_fal_keys_per_test`: any `import
    backend.main` or `import pipelines.run_skeleton` re-runs dotenv
    and re-populates the key, so we strip it before every test. Opt-in
    tests that genuinely want to hit OpenRouter use the
    `real_openrouter_key` fixture below.
    """
    os.environ.pop("OPENROUTER_API_KEY", None)
    yield


@pytest.fixture()
def real_fal_key(monkeypatch: pytest.MonkeyPatch) -> str:
    """Re-inject the real fal key for an opt-in integration test.

    Skips the calling test if `.env` didn't carry one. Use it like:

        @pytest.mark.fal
        def test_real_fal_call(real_fal_key, tmp_path):
            ...
    """
    key = _FAL_KEY_SAVED or _FAL_API_KEY_SAVED
    if not key:
        pytest.skip("FAL_KEY / FAL_API_KEY not set in .env or environment")
    monkeypatch.setenv("FAL_KEY", key)
    monkeypatch.setenv("FAL_API_KEY", key)
    return key


@pytest.fixture()
def real_openrouter_key(monkeypatch: pytest.MonkeyPatch) -> str:
    """Re-inject the real OpenRouter key for an opt-in integration test.

    Skips the calling test if `.env` didn't carry one. Use it like:

        @pytest.mark.openrouter
        def test_real_openrouter_call(real_openrouter_key):
            ...
    """
    if not _REAL_OPENROUTER_KEY:
        pytest.skip("OPENROUTER_API_KEY not set in .env or environment")
    monkeypatch.setenv("OPENROUTER_API_KEY", _REAL_OPENROUTER_KEY)
    return _REAL_OPENROUTER_KEY
