#!/usr/bin/env bash
# Full pipeline: data -> processed layers -> both poster variants.
set -euo pipefail
cd "$(dirname "$0")/.."
SIZE=${1:-A2}
scripts/fetch_data.sh
python3 scripts/build_gu.py
python3 scripts/extract_osm.py
python3 scripts/render.py --size "$SIZE" --subway
python3 scripts/render.py --size "$SIZE" --no-subway
