#!/bin/bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
python3 "$ROOT/analyzers/daily-analysis/analyze-youtube.py" "$@"
python3 "$ROOT/analyzers/daily-analysis/analyze-arxiv.py" "$@"
