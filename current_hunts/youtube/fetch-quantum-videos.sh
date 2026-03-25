#!/bin/bash
# fetch-quantum-videos.sh — Daily YouTube quantum physics video scraper
# Searches YouTube for recent quantum physics videos and appends to quantum-physics-videos.md
#
# Usage:
#   ./fetch-quantum-videos.sh              # Default: today's uploads
#   ./fetch-quantum-videos.sh --week       # This week's uploads (for backfill)
#   ./fetch-quantum-videos.sh --month      # This month's uploads (for backfill)

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
OUTPUT_FILE="$SCRIPT_DIR/quantum-physics-videos.md"
SEEN_FILE="$SCRIPT_DIR/.seen-ids"
RAW_FILE="$SCRIPT_DIR/.fetch-raw"
DATE_LABEL=$(TZ="America/Los_Angeles" date +"%Y-%m-%d")

# YouTube search filter codes (Upload date + Type: Video)
# EgQIAhAB = Today + Video
# EgQIAxAB = This week + Video
# EgQIBBAB = This month + Video
FILTER="EgQIAhAB"

if [[ "${1:-}" == "--week" ]]; then
    FILTER="EgQIAxAB"
    DATE_LABEL="$DATE_LABEL (week backfill)"
elif [[ "${1:-}" == "--month" ]]; then
    FILTER="EgQIBBAB"
    DATE_LABEL="$DATE_LABEL (month backfill)"
fi

# Search terms to cover the space
SEARCH_TERMS=(
    "quantum physics"
    "quantum mechanics"
    "quantum computing"
    "quantum theory"
)

MAX_PER_TERM=30

touch "$SEEN_FILE"
> "$RAW_FILE"

echo "[$(TZ='America/Los_Angeles' date)] Fetching quantum physics videos..."

for term in "${SEARCH_TERMS[@]}"; do
    echo "  Searching: $term"
    encoded_term=$(python3 -c "import urllib.parse; print(urllib.parse.quote('$term'))")
    yt-dlp "https://www.youtube.com/results?search_query=${encoded_term}&sp=$FILTER" \
        --flat-playlist \
        --playlist-end "$MAX_PER_TERM" \
        --print "%(id)s|||%(title)s|||%(channel)s|||%(duration_string)s|||%(view_count)s|||%(webpage_url)s" \
        --no-update \
        2>/dev/null >> "$RAW_FILE" || true
done

# Use Python for reliable parsing, deduplication, and formatting
export SCRIPT_DIR DATE_LABEL
python3 << 'PYEOF'
import os

script_dir = os.path.dirname(os.path.abspath("__file__"))
script_dir = os.environ.get("SCRIPT_DIR", ".")

raw_file = os.path.join(script_dir, ".fetch-raw")
seen_file = os.path.join(script_dir, ".seen-ids")
output_file = os.path.join(script_dir, "quantum-physics-videos.md")
date_label = os.environ.get("DATE_LABEL", "unknown")

# Load seen IDs
seen = set()
if os.path.exists(seen_file):
    with open(seen_file) as f:
        seen = set(line.strip() for line in f if line.strip())

# Parse raw results
videos = []
seen_this_run = set()

with open(raw_file) as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        parts = line.split("|||")
        if len(parts) != 6:
            continue

        vid_id, title, channel, duration, views, url = [p.strip() for p in parts]

        if not vid_id or vid_id in seen or vid_id in seen_this_run:
            continue

        seen_this_run.add(vid_id)

        # Format view count
        try:
            v = int(views)
            if v == 0:
                views_display = "new"
            elif v >= 1_000_000:
                views_display = f"{v/1_000_000:.1f}M views"
            elif v >= 1_000:
                views_display = f"{v/1_000:.1f}K views"
            else:
                views_display = f"{v} views"
        except (ValueError, TypeError):
            views_display = "new"

        videos.append({
            "id": vid_id,
            "title": title,
            "channel": channel,
            "duration": duration,
            "views": views_display,
            "url": url,
        })

if not videos:
    print("  No new videos found.")
    exit(0)

# Append to output file
with open(output_file, "a") as f:
    f.write(f"\n## {date_label} — {len(videos)} videos\n\n")
    for v in videos:
        f.write(f"- **{v['title']}** — {v['channel']} ({v['duration']}, {v['views']})\n")
        f.write(f"  {v['url']}\n")

# Update seen IDs
with open(seen_file, "a") as f:
    for v in videos:
        f.write(v["id"] + "\n")

print(f"  Done! Added {len(videos)} new videos to quantum-physics-videos.md")
PYEOF

rm -f "$RAW_FILE"
