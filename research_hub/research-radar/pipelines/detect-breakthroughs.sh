#!/bin/bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
python3 "$ROOT/analyzers/breakthrough-detector/detect-breakthroughs.py" "$@"
