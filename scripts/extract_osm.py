"""Cut the layers the poster needs out of an OSM extract.

Input : data/raw/*.osm.pbf  (Geofabrik south-korea-latest.osm.pbf, or any extract covering Seoul)
Output: data/processed/osm_<layer>.geojson (WGS84) + data/processed/osm_meta.json

Layers
  water     natural=water / waterway=riverbank / landuse=reservoir polygons
  waterway  waterway=river|stream|canal lines (streams with no polygon, e.g. 청계천)
  green     parks, forests, woods, scrub, nature reserves (mountains read as green)
  roads     highway=* lines, tagged with a simplified class (major / mid / minor)
  subway    railway=subway|light_rail lines in service
  places    named features whose name is on LANDMARK_NAMES (for label positions)

Only features touching Seoul's bounding box (+ a small buffer) are kept.
"""
import json
import sys
from pathlib import Path

import osmium
from shapely import wkb
from shapely.geometry import box, mapping

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/processed"

# Seoul bbox from the gu boundaries, padded ~1 km so clipping later is clean.
BBOX = box(126.75, 37.41, 127.20, 37.72)

ROAD_CLASS = {
    "motorway": "major", "motorway_link": "major", "trunk": "major", "trunk_link": "major",
    "primary": "major", "primary_link": "major",
    "secondary": "mid", "secondary_link": "mid", "tertiary": "mid", "tertiary_link": "mid",
    "residential": "minor", "unclassified": "minor", "living_street": "minor",
}
GREEN = {
    ("leisure", "park"), ("leisure", "garden"), ("landuse", "forest"), ("natural", "wood"),
    ("natural", "scrub"), ("natural", "heath"), ("leisure", "nature_reserve"),
    ("boundary", "national_park"), ("landuse", "recreation_ground"),
}
LANDMARK_NAMES = {
    "경복궁", "창덕궁", "덕수궁", "광화문", "N서울타워", "남산서울타워", "롯데월드타워",
    "63빌딩", "63스퀘어", "동대문디자인플라자", "서울역", "서울숲", "올림픽공원",
    "여의도공원", "여의도한강공원", "하늘공원", "월드컵공원", "서울월드컵경기장",
    "서울올림픽주경기장", "잠실종합운동장", "코엑스", "김포국제공항", "청와대",
    "북한산", "백운대", "관악산", "연주대", "도봉산", "자운봉", "인왕산", "남산", "목멱산",
    "북한산국립공원", "아차산", "수락산", "불암산", "청계산", "남산공원", "어린이대공원",
    "서울대공원", "보라매공원", "노들섬", "선유도공원", "밤섬", "북촌한옥마을", "숭례문", "흥인지문",
}

wkbf = osmium.geom.WKBFactory()


def in_service(tags):
    return not any(k in tags for k in ("disused", "abandoned", "construction", "proposed"))


def main(pbf):
    layers = {k: [] for k in ("water", "waterway", "green", "roads", "subway", "places")}

    def add(layer, geom, props):
        if geom.is_empty or not geom.intersects(BBOX):
            return
        layers[layer].append({"type": "Feature", "properties": props, "geometry": mapping(geom)})

    fp = (osmium.FileProcessor(pbf)
          .with_areas()
          .with_filter(osmium.filter.KeyFilter(
              "highway", "waterway", "natural", "landuse", "leisure", "railway",
              "boundary", "name", "water")))

    for obj in fp:
        t = obj.tags
        name = t.get("name")
        try:
            if obj.is_node():
                if name in LANDMARK_NAMES:
                    loc = obj.location
                    add("places", wkb.loads(wkbf.create_point(loc), hex=True),
                        {"name": name, "kind": _kind(t), "osm": f"n{obj.id}"})
            elif obj.is_way():
                hw = t.get("highway")
                if hw in ROAD_CLASS and t.get("area") != "yes":
                    add("roads", _line(obj), {"cls": ROAD_CLASS[hw], "hw": hw,
                                              "bridge": t.get("bridge") == "yes",
                                              "tunnel": t.get("tunnel") in ("yes", "building_passage")})
                elif t.get("railway") in ("subway", "light_rail") and in_service(t):
                    add("subway", _line(obj), {"railway": t["railway"], "name": name,
                                               "tunnel": t.get("tunnel") == "yes"})
                elif t.get("waterway") in ("river", "stream", "canal") and t.get("tunnel") != "culvert":
                    add("waterway", _line(obj), {"waterway": t["waterway"], "name": name})
            elif obj.is_area():
                geom = wkb.loads(wkbf.create_multipolygon(obj), hex=True)
                if (t.get("natural") == "water" or t.get("waterway") == "riverbank"
                        or t.get("landuse") in ("reservoir", "basin")):
                    add("water", geom, {"name": name, "water": t.get("water")})
                elif any((k, t.get(k)) in GREEN for k in ("leisure", "landuse", "natural", "boundary")):
                    add("green", geom, {"name": name, "kind": _kind(t)})
                if name in LANDMARK_NAMES:
                    add("places", geom.representative_point(),
                        {"name": name, "kind": _kind(t), "osm": f"a{obj.id}"})
        except (RuntimeError, ValueError):
            # broken geometry in the source (e.g. an unclosed multipolygon): skip it
            continue

    OUT.mkdir(parents=True, exist_ok=True)
    for k, feats in layers.items():
        (OUT / f"osm_{k}.geojson").write_text(
            json.dumps({"type": "FeatureCollection", "features": feats}, ensure_ascii=False),
            encoding="utf-8")
        print(f"{k:9s} {len(feats):7d} features")

    header = osmium.io.Reader(pbf, osmium.osm.osm_entity_bits.NOTHING).header()
    meta = {"source": Path(pbf).name,
            "timestamp": header.get("osmosis_replication_timestamp") or header.get("timestamp")}
    (OUT / "osm_meta.json").write_text(json.dumps(meta, ensure_ascii=False, indent=2))
    print(meta)


def _line(way):
    return wkb.loads(wkbf.create_linestring(way), hex=True)


def _kind(t):
    for k in ("tourism", "historic", "natural", "leisure", "building", "railway", "aeroway", "boundary"):
        if k in t:
            return f"{k}={t[k]}"
    return ""


if __name__ == "__main__":
    pbfs = sys.argv[1:] or [str(p) for p in sorted((ROOT / "data/raw").glob("*.osm.pbf"))]
    if not pbfs:
        sys.exit("No .osm.pbf found in data/raw/. Download south-korea-latest.osm.pbf from Geofabrik.")
    main(pbfs[0])
