#!/bin/bash
# Sync research project data files to public/data/ for the dashboard to fetch

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SCIENCE_DIR="$(dirname "$SCRIPT_DIR")"
DATA_DIR="$SCRIPT_DIR/public/data"

echo "Syncing research data to $DATA_DIR..."

# Clean and recreate
rm -rf "$DATA_DIR"
mkdir -p "$DATA_DIR/quantum-gravity"
mkdir -p "$DATA_DIR/dqcp"
mkdir -p "$DATA_DIR/grand-unified"
mkdir -p "$DATA_DIR/worldviews"

# Quantum Gravity Research Loop
echo "  -> quantum-gravity/"
cp "$SCIENCE_DIR/quantum-gravity-research/PROMPT.md" "$DATA_DIR/quantum-gravity/" 2>/dev/null
cp "$SCIENCE_DIR/quantum-gravity-research/FINAL-REPORT.md" "$DATA_DIR/quantum-gravity/" 2>/dev/null
cp "$SCIENCE_DIR/quantum-gravity-research/THEORIES.md" "$DATA_DIR/quantum-gravity/" 2>/dev/null
cp "$SCIENCE_DIR/quantum-gravity-research/HANDOFF.md" "$DATA_DIR/quantum-gravity/" 2>/dev/null
cp "$SCIENCE_DIR/quantum-gravity-research/state.json" "$DATA_DIR/quantum-gravity/" 2>/dev/null

# DQCP Formalization
echo "  -> dqcp/"
cp "$SCIENCE_DIR/dqcp-formalization/PROMPT.md" "$DATA_DIR/dqcp/" 2>/dev/null
cp "$SCIENCE_DIR/dqcp-formalization/RESULTS.md" "$DATA_DIR/dqcp/" 2>/dev/null
cp "$SCIENCE_DIR/dqcp-formalization/FINAL-VERDICT.md" "$DATA_DIR/dqcp/" 2>/dev/null
cp "$SCIENCE_DIR/dqcp-formalization/HANDOFF.md" "$DATA_DIR/dqcp/" 2>/dev/null
cp "$SCIENCE_DIR/dqcp-formalization/state.json" "$DATA_DIR/dqcp/" 2>/dev/null

# Grand Unified Theory
echo "  -> grand-unified/"
cp "$SCIENCE_DIR/grand-unified-theory/GRAND-THEORY.md" "$DATA_DIR/grand-unified/" 2>/dev/null
cp "$SCIENCE_DIR/grand-unified-theory/scripts/theory-builder/PROMPT.md" "$DATA_DIR/grand-unified/" 2>/dev/null
cp "$SCIENCE_DIR/grand-unified-theory/scripts/theory-builder/HANDOFF.md" "$DATA_DIR/grand-unified/" 2>/dev/null
cp "$SCIENCE_DIR/grand-unified-theory/scripts/theory-builder/CALCULATIONS.md" "$DATA_DIR/grand-unified/" 2>/dev/null
cp "$SCIENCE_DIR/grand-unified-theory/scripts/theory-builder/state.json" "$DATA_DIR/grand-unified/" 2>/dev/null

# Worldviews
echo "  -> worldviews/"
cp "$SCIENCE_DIR/worldviews/worldview_manifest.md" "$DATA_DIR/worldviews/" 2>/dev/null
cp "$SCIENCE_DIR/worldviews/core_tenets_of_physics.md" "$DATA_DIR/worldviews/" 2>/dev/null
cp "$SCIENCE_DIR/worldviews/tenet_stability_assessment.md" "$DATA_DIR/worldviews/" 2>/dev/null
cp "$SCIENCE_DIR/worldviews/theory-assessment-criteria.md" "$DATA_DIR/worldviews/" 2>/dev/null
cp "$SCIENCE_DIR/worldviews/worldviews/RANKINGS.md" "$DATA_DIR/worldviews/" 2>/dev/null

echo "Done! $(find "$DATA_DIR" -type f | wc -l | tr -d ' ') files synced."
