#!/usr/bin/env bash
# Download the inputs that are allowed from this environment.
# OSM (Geofabrik) is fetched only if the network allows it; otherwise place
# south-korea-latest.osm.pbf in data/raw/ by hand.
set -euo pipefail
cd "$(dirname "$0")/.."
mkdir -p data/raw
GU=data/raw/HangJeongDong_ver20260701.geojson
[ -f "$GU" ] || curl -fsSL -o "$GU" \
  https://raw.githubusercontent.com/vuski/admdongkor/master/ver20260701/HangJeongDong_ver20260701.geojson
PBF=data/raw/south-korea-latest.osm.pbf
[ -f "$PBF" ] || curl -fsSL -o "$PBF" https://download.geofabrik.de/asia/south-korea-latest.osm.pbf \
  || echo "!! Could not download OSM. Put south-korea-latest.osm.pbf in data/raw/ manually."
# Pretendard (SIL OFL) for Korean labels
if ! fc-list | grep -qi pretendard; then
  tmp=$(mktemp -d); (cd "$tmp" && npm pack -q pretendard@1.3.9 && tar xzf pretendard-1.3.9.tgz)
  mkdir -p ~/.local/share/fonts && cp "$tmp"/package/dist/public/static/Pretendard-*.otf ~/.local/share/fonts/
  fc-cache -f >/dev/null
fi
