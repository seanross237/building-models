#!/bin/bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
python3 "$ROOT/pipelines/aggregate-youtube.py" "$@"
python3 "$ROOT/pipelines/aggregate-arxiv.py" "$@"
