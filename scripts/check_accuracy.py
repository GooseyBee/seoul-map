"""Cross-check OSM layers against the independent official gu boundaries.

1. Han River: the gu boundaries between north- and south-bank districts follow the
   river, so they should run inside OSM's river polygon almost everywhere.
2. Bridges: count separate road/rail bridge crossings over the Han in OSM.
3. Peaks: print OSM elevations of the labelled summits for comparison with
   published figures.
"""
import json
from pathlib import Path

import shapely
from pyproj import Transformer
from shapely.geometry import shape
from shapely.ops import transform, unary_union

D = Path(__file__).resolve().parents[1] / "data/processed"
t = Transformer.from_crs("EPSG:4326", "EPSG:5179", always_xy=True).transform
load = lambda n: json.loads((D / n).read_text(encoding="utf-8"))["features"]

NORTH = {"강서구", "마포구", "용산구", "성동구", "광진구"}
SOUTH = {"영등포구", "동작구", "서초구", "강남구", "송파구", "강동구"}
gu = {f["properties"]["name"]: transform(t, shape(f["geometry"])) for f in load("gu.geojson")}
north = unary_union([gu[n] for n in NORTH])
south = unary_union([gu[n] for n in SOUTH])
river_line = north.boundary.intersection(south.boundary)
river_line = unary_union([g for g in getattr(river_line, "geoms", [river_line]) if g.length > 0])

water = unary_union([transform(t, shape(f["geometry"])).buffer(0) for f in load("osm_water.geojson")])
han = max(getattr(water, "geoms", [water]), key=lambda g: g.intersection(river_line.buffer(10)).area)
inside = river_line.intersection(han.buffer(30)).length / river_line.length
print(f"Han River: {river_line.length / 1000:.1f} km of official north/south gu boundary, "
      f"{inside:.1%} lies within 30 m of the OSM river polygon")

roads = [f for f in load("osm_roads.geojson") if f["properties"]["bridge"] and f["properties"]["cls"] != "minor"]
rail = load("osm_subway.geojson")
span = han.buffer(-20)
crossing = [transform(t, shape(f["geometry"])) for f in roads + rail]
crossing = [g for g in crossing if g.intersection(span).length > 300]
groups = unary_union([g.intersection(han).buffer(60) for g in crossing])
n = len(getattr(groups, "geoms", [groups]))
print(f"Han bridges: {n} separate crossings found in OSM (roads secondary+ and subway)")

peaks = [f for f in load("osm_places.geojson") if f["properties"]["kind"] == "natural=peak"]
for f in peaks:
    print("peak:", f["properties"]["name"], f["geometry"]["coordinates"])
