"""Rule-based scoring engine driven by `config/comedy-lens.md`.

The lens markdown contains two bullet-list sections, "Keywords that boost
sketchability" and "Keywords that penalize". This module parses those
lists and exposes a tiny scoring function that the analyzer calls for
every signal. Phase 3 will replace this with an LLM call but the
contract (`Lens.score(title, body) -> int`) will stay the same.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional

# Tragedy keywords that always knock the score down hard regardless of
# whether they appear in the lens file. These are sketch-killers.
HARD_PENALTY_KEYWORDS = ("died", "killed", "shooting", "shot", "murder", "fatal")
HARD_PENALTY_WEIGHT = 3

BOOST_HEADING_RE = re.compile(r"^##\s+keywords?\s+that\s+boost", re.IGNORECASE)
PENALTY_HEADING_RE = re.compile(r"^##\s+keywords?\s+that\s+penalize", re.IGNORECASE)
HEADING_RE = re.compile(r"^##\s+", re.IGNORECASE)


@dataclass
class Lens:
    boost_keywords: List[str] = field(default_factory=list)
    penalty_keywords: List[str] = field(default_factory=list)

    def score(self, title: str, body: str = "") -> int:
        return score_text(title, body, self)


def _extract_bullet_section(lines: List[str], heading_re: re.Pattern) -> List[str]:
    out: List[str] = []
    in_section = False
    for raw in lines:
        line = raw.rstrip()
        if heading_re.match(line):
            in_section = True
            continue
        if in_section and HEADING_RE.match(line):
            break
        if in_section and line.startswith("- "):
            keyword = line[2:].strip().lower()
            if keyword:
                out.append(keyword)
    return out


def parse_lens_text(text: str) -> Lens:
    lines = text.splitlines()
    boost = _extract_bullet_section(lines, BOOST_HEADING_RE)
    penalty = _extract_bullet_section(lines, PENALTY_HEADING_RE)
    return Lens(boost_keywords=boost, penalty_keywords=penalty)


def load_lens(path: Path) -> Lens:
    if not path.exists():
        return Lens()
    return parse_lens_text(path.read_text(encoding="utf-8"))


def score_text(title: str, body: str, lens: Lens) -> int:
    text = f"{title or ''} {body or ''}".lower()
    score = 5  # baseline

    for kw in lens.boost_keywords:
        if kw and kw in text:
            score += 1
    for kw in lens.penalty_keywords:
        if kw and kw in text:
            score -= 2

    title_len = len(title or "")
    if 20 <= title_len <= 120:
        score += 1

    for kw in HARD_PENALTY_KEYWORDS:
        if kw in text:
            score -= HARD_PENALTY_WEIGHT
            break

    return max(1, min(10, score))


__all__ = ["HARD_PENALTY_KEYWORDS", "Lens", "load_lens", "parse_lens_text", "score_text"]
