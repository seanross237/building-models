"""Optional integration test that hits the real public network.

Marked with `@pytest.mark.network` so it's excluded from default runs.
Use `pytest -m network` to opt in.
"""
from __future__ import annotations

from pathlib import Path

import pytest

from collectors.hacker_news import fetch as hn
from state.store import Store


@pytest.mark.network
def test_hacker_news_real_topstories(tmp_path: Path) -> None:
    """Hit the real public Hacker News Firebase API. Requires internet."""
    store = Store(root=tmp_path)
    new_ids = hn.fetch(store, config={"limit": 5, "max_age_hours": 24 * 365})
    assert len(new_ids) >= 1, "expected at least one HN top story from the real API"
    items_dir = tmp_path / "signals" / "hacker_news" / "items"
    assert any(items_dir.glob("*.md"))
