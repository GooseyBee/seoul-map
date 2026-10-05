"""Dissolve KOSTAT-based 행정동 polygons (admdongkor) into Seoul's 25 gu.

Input : data/raw/HangJeongDong_ver20260701.geojson  (WGS84)
Output: data/processed/gu.geojson  (WGS84, one feature per gu, Korean name)
"""
import json
from pathlib import Path

from shapely.geometry import shape, mapping
from shapely.ops import unary_union

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "data/raw/HangJeongDong_ver20260701.geojson"
DST = ROOT / "data/processed/gu.geojson"


def main():
    feats = json.loads(SRC.read_text(encoding="utf-8"))["features"]
    by_gu = {}
    for f in feats:
        p = f["properties"]
        if p.get("sido") != "11":  # 11 = 서울특별시
            continue
        by_gu.setdefault((p["sgg"], p["sggnm"]), []).append(shape(f["geometry"]).buffer(0))
    out = []
    for (code, name), geoms in sorted(by_gu.items()):
        g = unary_union(geoms).buffer(0)
        out.append({"type": "Feature", "properties": {"code": code, "name": name},
                    "geometry": mapping(g)})
    assert len(out) == 25, f"expected 25 gu, got {len(out)}"
    DST.write_text(json.dumps({"type": "FeatureCollection", "features": out},
                              ensure_ascii=False), encoding="utf-8")
    print(f"wrote {DST} ({len(out)} gu)")


if __name__ == "__main__":
    main()
