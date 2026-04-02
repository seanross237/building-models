#!/bin/bash
set -euo pipefail

ROOT="/Users/seanross/kingdom_of_god/home-base/research-radar"
python3 "$ROOT/collectors/youtube/fetch-topic-videos.py" "$@"
