"""Unit tests for the lens-driven keyword scorer."""
from __future__ import annotations

from pathlib import Path

import pytest

from analyzers.score_signals.lens_rules import (
    HARD_PENALTY_KEYWORDS,
    Lens,
    load_lens,
    parse_lens_text,
    score_text,
)


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def test_parse_lens_extracts_both_sections() -> None:
    text = """\
# Comedy Lens

## Keywords that boost sketchability

- caught
- absurd
- senator

## Keywords that penalize

- killed
- shooting

## Some other section

- ignored
"""
    lens = parse_lens_text(text)
    assert lens.boost_keywords == ["caught", "absurd", "senator"]
    assert lens.penalty_keywords == ["killed", "shooting"]


def test_parse_lens_handles_missing_sections() -> None:
    lens = parse_lens_text("# nothing useful here\n")
    assert lens.boost_keywords == []
    assert lens.penalty_keywords == []


def test_score_baseline_is_five() -> None:
    lens = Lens()
    assert score_text("", "", lens) == 5


def test_score_boosts_with_matching_keywords() -> None:
    lens = Lens(boost_keywords=["senator", "caught"], penalty_keywords=[])
    title = "Senator caught using spoon as wifi antenna"
    base = score_text("", "", lens)
    boosted = score_text(title, "", lens)
    # Two boost matches + length bonus.
    assert boosted > base
    assert boosted >= base + 2


def test_score_penalty_keywords_subtract() -> None:
    lens = Lens(boost_keywords=[], penalty_keywords=["bomb"])
    title = "City announces new bomb-shelter regulations"
    score = score_text(title, "", lens)
    assert score < 5


def test_score_clamped_to_one_to_ten() -> None:
    lens = Lens(boost_keywords=["a"] * 100, penalty_keywords=[])
    title = "a a a a a a a a a a a a a a a a a a a a a"
    assert score_text(title, "", lens) == 10

    lens2 = Lens(boost_keywords=[], penalty_keywords=["a"] * 100)
    assert score_text(title, "", lens2) == 1


def test_hard_penalty_for_tragedy_words() -> None:
    lens = Lens(boost_keywords=["senator", "caught"], penalty_keywords=[])
    sketchy = score_text("Senator caught taking three lunches", "", lens)
    tragic = score_text("Senator caught after fatal incident", "", lens)
    assert tragic < sketchy
    for keyword in HARD_PENALTY_KEYWORDS[:3]:
        title = f"news headline mentioning {keyword} unfortunately"
        assert score_text(title, "", lens) < 5


def test_load_lens_from_real_file() -> None:
    lens = load_lens(PROJECT_ROOT / "config" / "comedy-lens.md")
    assert lens.boost_keywords, "real comedy-lens.md must define boost keywords"
    assert lens.penalty_keywords, "real comedy-lens.md must define penalty keywords"
    assert "senator" in lens.boost_keywords
    assert "killed" in lens.penalty_keywords


def test_score_uses_body_text_too() -> None:
    lens = Lens(boost_keywords=["spoon"], penalty_keywords=[])
    score_with_body = score_text("Local hearing", "He used a spoon as an antenna", lens)
    score_without_body = score_text("Local hearing", "", lens)
    assert score_with_body > score_without_body
