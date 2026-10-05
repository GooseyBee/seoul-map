"""Render the Seoul poster as a layered SVG (+ PNG preview, + PDF).

    python3 scripts/render.py --size A2 --subway      # with subway lines
    python3 scripts/render.py --size A2 --no-subway   # roads only

Every map layer is its own <g inkscape:groupmode="layer">, so colours and stroke
widths can be restyled per layer in Inkscape/Illustrator without touching the rest.
"""
import argparse
import json
from pathlib import Path

import shapely
from pyproj import Transformer
from shapely.geometry import shape
from shapely.ops import transform, unary_union, polylabel

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data/processed"
OUT = ROOT / "output"

PAGES = {"A2": (594, 420), "A1": (841, 594)}  # landscape, mm

# ---- palette: light purple + grays on a very light gray ground -------------
C = {
    "paper":    "#F3F2F5",
    "land":     "#FAF9FB",
    "green":    "#E2DEEA",
    "water":    "#BCAEDD",
    "waterway": "#BCAEDD",
    "minor":    "#DAD8DF",
    "mid":      "#AEABB6",
    "major":    "#5F5C68",
    "subway":   "#7458B5",
    "gu":       "#BDB6CB",
    "outline":  "#8E86A3",
    "ink":      "#46424F",
    "ink_soft": "#8A8594",
    "accent":   "#6E56AA",
}
# stroke widths in mm at A2; scaled up with the page
W = {"minor": 0.10, "mid": 0.26, "major": 0.50, "waterway": 0.30, "subway": 0.42,
     "gu": 0.22, "outline": 0.45}

FONT = "Pretendard, 'Noto Sans KR', sans-serif"

# Landmarks: (label on poster, OSM names to look for in order, label side, kind)
# kind "poi" = a building/park/attraction, "station" = railway station, "peak" = mountain
# top (drawn with a small triangle), "area" = label the named OSM area clipped to Seoul.
# Positions always come from OSM data; nothing here is a hand-typed coordinate.
LANDMARKS = [
    ("경복궁",          ["경복궁"], "r", "poi"),
    ("N서울타워",       ["N서울타워", "남산서울타워"], "r", "poi"),
    ("롯데월드타워",    ["롯데월드타워"], "r", "poi"),
    ("63스퀘어",        ["63스퀘어", "63빌딩"], "l", "poi"),
    ("동대문디자인플라자", ["동대문디자인플라자"], "r", "poi"),
    ("서울역",          ["서울역"], "l", "station"),
    ("서울숲",          ["서울숲"], "r", "poi"),
    ("올림픽공원",      ["올림픽공원"], "r", "poi"),
    ("여의도공원",      ["여의도공원"], "l", "poi"),
    ("하늘공원",        ["하늘공원"], "l", "poi"),
    ("코엑스",          ["코엑스"], "r", "poi"),
    ("김포국제공항",    ["김포국제공항"], "r", "poi"),
    ("북한산",          ["북한산국립공원"], "c", "area"),
    ("관악산",          ["관악산", "연주대"], "r", "peak"),
    ("도봉산",          ["도봉산자운봉"], "r", "peak"),
]
# OSM tags that mark a same-named feature as transport or a shop rather than the landmark
# itself (e.g. 경복궁 is also a subway station, many bus stops and a restaurant).
NOT_POI = ("railway=", "public_transport=", "highway=", "amenity=", "shop=")


def pick(places, names, kind, seoul):
    for n in names:
        cands = []
        for f in places:
            p = f["properties"]
            if p["name"] != n:
                continue
            pt = transform(to5179, shape(f["geometry"]))
            # summits often sit exactly on the city line (관악산 is shared with 과천), so allow 300 m
            if not seoul.buffer(300 if kind == "peak" else 0).contains(pt):
                continue
            ok = {"station": p["kind"] == "railway=station",
                  "peak": p["kind"] == "natural=peak",
                  "poi": bool(p["kind"]) and not p["kind"].startswith(NOT_POI)}[kind]
            if ok:
                cands.append((p.get("area_deg2", 0), pt))
        if cands:
            return max(cands, key=lambda c: c[0])[1]  # biggest area wins (the real park, not a namesake)
    return None


to5179 = Transformer.from_crs("EPSG:4326", "EPSG:5179", always_xy=True).transform


def load(name):
    p = DATA / name
    if not p.exists():
        return []
    return json.loads(p.read_text(encoding="utf-8"))["features"]


class Page:
    def __init__(self, size, seoul):
        self.w, self.h = PAGES[size]
        self.k = self.w / PAGES["A2"][0]          # stroke/text scale vs. A2
        margin = 34 * self.k
        footer = 46 * self.k
        box_w, box_h = self.w - 2 * margin, self.h - margin - footer - 8 * self.k
        minx, miny, maxx, maxy = seoul.bounds
        self.s = min(box_w / (maxx - minx), box_h / (maxy - miny))   # mm per metre
        self.ox = margin + (box_w - (maxx - minx) * self.s) / 2 - minx * self.s
        self.oy = margin + (box_h - (maxy - miny) * self.s) / 2 + maxy * self.s
        self.footer_y = self.h - footer

    def xy(self, x, y):
        return self.ox + x * self.s, self.oy - y * self.s

    def path(self, geom):
        parts = []
        for g in getattr(geom, "geoms", [geom]):
            if g.is_empty:
                continue
            if g.geom_type == "Polygon":
                for ring in [g.exterior, *g.interiors]:
                    parts.append(self._ring(ring.coords, close=True))
            elif g.geom_type in ("LineString", "LinearRing"):
                parts.append(self._ring(g.coords))
            elif hasattr(g, "geoms"):
                parts.append(self.path(g))
        return "".join(parts)

    def _ring(self, coords, close=False):
        pts = [self.xy(x, y) for x, y in coords]
        d = "M" + " ".join(f"{x:.2f} {y:.2f}" for x, y in pts)
        return d + ("Z" if close else "")


def project(feats):
    return [transform(to5179, shape(f["geometry"])) for f in feats]


def clip(geoms, seoul, tol):
    if not geoms:
        return shapely.GeometryCollection()
    arr = shapely.intersection(shapely.simplify(geoms, tol), seoul)
    arr = arr[~shapely.is_empty(arr)]
    return shapely.GeometryCollection(list(arr))


def clip_areas(geoms, seoul, tol, min_area):
    """Union overlapping polygons first (a forest inside a national park must not cancel
    out under even-odd filling), then clip and drop specks too small to see on paper."""
    if not geoms:
        return shapely.GeometryCollection()
    g = unary_union(shapely.make_valid(geoms)).intersection(seoul)
    g = shapely.simplify(g, tol)
    polys = [p for p in getattr(g, "geoms", [g]) if p.geom_type == "Polygon" and p.area >= min_area]
    polys += [q for p in getattr(g, "geoms", [g]) if p.geom_type == "MultiPolygon"
              for q in p.geoms if q.area >= min_area]
    return shapely.MultiPolygon(polys)


def layer(lid, label, body, **style):
    attrs = " ".join(f'{k.replace("_", "-")}="{v}"' for k, v in style.items())
    return (f'<g id="{lid}" inkscape:groupmode="layer" inkscape:label="{label}" {attrs}>\n'
            f"{body}\n</g>")


def dms(v, pos, neg):
    d = abs(v)
    deg, mins = int(d), (d - int(d)) * 60
    return f"{deg}°{mins:05.2f}′{pos if v >= 0 else neg}"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--size", default="A2", choices=PAGES)
    ap.add_argument("--subway", action=argparse.BooleanOptionalAction, default=True)
    ap.add_argument("--draft", action=argparse.BooleanOptionalAction, default=True)
    a = ap.parse_args()

    gu_feats = load("gu.geojson")
    gus = project(gu_feats)
    seoul = unary_union(gus).buffer(0)
    pg = Page(a.size, seoul)
    k = pg.k
    tol = 0.08 / pg.s            # simplify to ~0.08 mm on paper: invisible, keeps files small

    meta = json.loads((DATA / "osm_meta.json").read_text()) if (DATA / "osm_meta.json").exists() else {}
    osm_date = (meta.get("timestamp") or "")[:10] or "????-??-??"

    roads = load("osm_roads.geojson")
    road_geoms = {c: project([f for f in roads if f["properties"]["cls"] == c and not f["properties"]["tunnel"]])
                  for c in ("minor", "mid", "major")}

    out = []
    out.append(f'<rect width="{pg.w}" height="{pg.h}" fill="{C["paper"]}"/>')
    out.append(layer("land", "land", f'<path d="{pg.path(seoul)}"/>', fill=C["land"]))

    speck = (0.6 / pg.s) ** 2      # anything under ~0.6 x 0.6 mm on paper is noise
    green = clip_areas(project(load("osm_green.geojson")), seoul, tol, speck)
    out.append(layer("green", "green (parks, mountains)", f'<path d="{pg.path(green)}"/>',
                     fill=C["green"], fill_rule="evenodd"))  # safe now: polygons are unioned

    water = clip_areas(project(load("osm_water.geojson")), seoul, tol, speck)
    waterway = clip(project([f for f in load("osm_waterway.geojson")
                             if f["properties"]["waterway"] in ("river", "canal", "stream")]), seoul, tol)
    out.append(layer("water", "water",
                     f'<path d="{pg.path(water)}" fill="{C["water"]}" fill-rule="nonzero"/>\n'
                     f'<path d="{pg.path(waterway)}" fill="none" stroke="{C["waterway"]}" '
                     f'stroke-width="{W["waterway"] * k:.3f}" stroke-linecap="round" stroke-linejoin="round"/>'))

    for c, lbl in (("minor", "roads – minor"), ("mid", "roads – secondary"), ("major", "roads – major")):
        g = clip(road_geoms[c], seoul, tol)
        out.append(layer(f"roads-{c}", lbl, f'<path d="{pg.path(g)}"/>', fill="none", stroke=C[c],
                         stroke_width=f"{W[c] * k:.3f}", stroke_linecap="round", stroke_linejoin="round"))

    if a.subway:
        sub = clip(project(load("osm_subway.geojson")), seoul.buffer(50), tol)
        out.append(layer("subway", "subway", f'<path d="{pg.path(sub)}"/>', fill="none", stroke=C["subway"],
                         stroke_width=f"{W['subway'] * k:.3f}", stroke_linecap="round",
                         stroke_linejoin="round", stroke_opacity="0.85"))

    gu_lines = unary_union([g.boundary for g in gus]).difference(seoul.exterior.buffer(1))
    out.append(layer("gu-boundaries", "gu boundaries",
                     f'<path d="{pg.path(shapely.simplify(gu_lines, tol))}" fill="none" stroke="{C["gu"]}" '
                     f'stroke-width="{W["gu"] * k:.3f}" stroke-dasharray="{1.2 * k:.2f} {0.9 * k:.2f}"/>\n'
                     f'<path d="{pg.path(seoul.exterior)}" fill="none" stroke="{C["outline"]}" '
                     f'stroke-width="{W["outline"] * k:.3f}" stroke-linejoin="round"/>'))

    # ---- labels ---------------------------------------------------------------
    # Labels avoid each other with a simple greedy check on paper-space boxes:
    # district names go down first, then each landmark tries right / left / above / below.
    gu_fs, lm_fs = 3.6 * k, 2.5 * k
    taken = []

    def tbox(x, y, text, fs, anchor):
        w = len(text) * fs * 0.98 + 0.4 * k          # Hangul glyphs are ~1 em wide
        x0 = {"start": x, "end": x - w, "middle": x - w / 2}[anchor]
        return shapely.box(x0, y - fs * 0.6, x0 + w, y + fs * 0.6)

    places = load("osm_places.geojson")
    greens = load("osm_green.geojson")
    found, missing = [], []
    for label, names, side, kind in LANDMARKS:
        if kind == "area":
            polys = [transform(to5179, shape(f["geometry"])) for f in greens
                     if f["properties"]["name"] in names]
            g = unary_union(polys).intersection(seoul) if polys else None
            pt = polylabel(max(getattr(g, "geoms", [g]), key=lambda x: x.area), tolerance=20) \
                if g is not None and not g.is_empty else None
        else:
            pt = pick(places, names, kind, seoul)
        if pt is None:
            missing.append(label)
        else:
            found.append((label, side, kind, *pg.xy(pt.x, pt.y)))
    for label, side, kind, x, y in found:          # marks are obstacles for every label
        if kind != "area":
            taken.append(shapely.box(x - k, y - k, x + k, y + k))

    gl = []
    for f, g in zip(gu_feats, gus):
        p = polylabel(max(getattr(g, "geoms", [g]), key=lambda x: x.area), tolerance=20)
        x, y = pg.xy(p.x, p.y)
        name = f["properties"]["name"]
        # nudge a district name up or down if a landmark mark sits under it
        for dy in (0, gu_fs * 1.3, -gu_fs * 1.3, gu_fs * 2.6, -gu_fs * 2.6):
            bx = tbox(x, y + dy, name, gu_fs, "middle")
            if not any(bx.intersects(t) for t in taken):
                break
        y += dy
        taken.append(bx)
        gl.append(haloed(f'x="{x:.2f}" y="{y:.2f}"', name, k))
    out.append(layer("labels-gu", "labels – districts", "\n".join(gl), font_family=FONT, font_weight="600",
                     font_size=f"{gu_fs:.2f}", fill=C["ink_soft"], text_anchor="middle",
                     letter_spacing=f"{0.25 * k:.2f}", dominant_baseline="middle"))

    ll = []
    gap = 1.6 * k
    for label, side, kind, x, y in found:
        if kind == "area":
            text = f"▲ {label}"
            taken.append(tbox(x, y, text, 3.0 * k, "middle"))
            ll.append(haloed(f'x="{x:.2f}" y="{y:.2f}" text-anchor="middle" font-size="{3.0 * k:.2f}"', text, k))
            continue
        opts = {"r": (x + gap, y, "start"), "l": (x - gap, y, "end"),
                "t": (x, y - lm_fs * 1.2, "middle"), "b": (x, y + lm_fs * 1.2, "middle")}
        order = [side] + [o for o in "rltb" if o != side]
        best = min(order, key=lambda o: (sum(tbox(*opts[o][:2], label, lm_fs, opts[o][2]).intersection(t).area
                                             for t in taken), order.index(o)))
        tx, ty, anchor = opts[best]
        taken.append(tbox(tx, ty, label, lm_fs, anchor))
        if kind == "peak":
            r = 1.0 * k
            mark = (f'<path d="M{x:.2f} {y - r:.2f}L{x + r:.2f} {y + r * 0.7:.2f}L{x - r:.2f} {y + r * 0.7:.2f}Z" '
                    f'fill="{C["accent"]}" stroke="{C["land"]}" stroke-width="{0.3 * k:.2f}"/>')
        else:
            mark = (f'<circle cx="{x:.2f}" cy="{y:.2f}" r="{0.75 * k:.2f}" fill="{C["accent"]}" '
                    f'stroke="{C["land"]}" stroke-width="{0.35 * k:.2f}"/>')
        ll.append(mark + haloed(f'x="{tx:.2f}" y="{ty:.2f}" text-anchor="{anchor}"', label, k))
    out.append(layer("labels-landmarks", "labels – landmarks", "\n".join(ll), font_family=FONT,
                     font_weight="500", font_size=f"{lm_fs:.2f}", fill=C["accent"],
                     dominant_baseline="middle"))

    # ---- footer ---------------------------------------------------------------
    c = transform(lambda x, y: Transformer.from_crs("EPSG:5179", "EPSG:4326", always_xy=True).transform(x, y),
                  seoul.centroid)
    fy = pg.footer_y + 14 * k
    mx = 34 * k
    data_line = (f"© OpenStreetMap contributors · OSM data {osm_date} · "
                 f"행정구역 경계: 통계청 SGIS (admdongkor ver20260701)")
    tag = " · DRAFT" if a.draft else ""
    foot = (f'<line x1="{mx:.2f}" y1="{pg.footer_y:.2f}" x2="{pg.w - mx:.2f}" y2="{pg.footer_y:.2f}" '
            f'stroke="{C["gu"]}" stroke-width="{0.25 * k:.2f}"/>'
            f'<text x="{mx:.2f}" y="{fy + 6 * k:.2f}" font-size="{15 * k:.2f}" font-weight="700" '
            f'fill="{C["ink"]}" letter-spacing="{1.5 * k:.2f}">서울</text>'
            f'<text x="{mx + 32 * k:.2f}" y="{fy + 6 * k:.2f}" font-size="{6 * k:.2f}" font-weight="300" '
            f'fill="{C["ink_soft"]}" letter-spacing="{2.4 * k:.2f}">SEOUL</text>'
            f'<text x="{pg.w - mx:.2f}" y="{fy:.2f}" text-anchor="end" font-size="{3.2 * k:.2f}" '
            f'font-weight="500" fill="{C["ink"]}" letter-spacing="{0.4 * k:.2f}">'
            f'{dms(c.y, "N", "S")}  {dms(c.x, "E", "W")}</text>'
            f'<text x="{pg.w - mx:.2f}" y="{fy + 6 * k:.2f}" text-anchor="end" font-size="{2.2 * k:.2f}" '
            f'fill="{C["ink_soft"]}">{data_line}{tag}</text>')
    out.append(layer("footer", "footer", foot, font_family=FONT))

    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" '
           f'xmlns:inkscape="http://www.inkscape.org/namespaces/inkscape" '
           f'width="{pg.w}mm" height="{pg.h}mm" viewBox="0 0 {pg.w} {pg.h}">\n'
           f'<title>서울 Seoul poster ({a.size}, {"subway" if a.subway else "no subway"})</title>\n'
           + "\n".join(out) + "\n</svg>\n")

    OUT.mkdir(exist_ok=True)
    stem = f"seoul_{a.size}_{'subway' if a.subway else 'nosubway'}{'_draft' if a.draft else ''}"
    (OUT / f"{stem}.svg").write_text(svg, encoding="utf-8")
    import cairosvg
    cairosvg.svg2png(bytestring=svg.encode(), write_to=str(OUT / f"{stem}.png"),
                     output_width=2400 if a.draft else 4000)  # preview only; print from the PDF/SVG
    cairosvg.svg2pdf(bytestring=svg.encode(), write_to=str(OUT / f"{stem}.pdf"))
    print(f"wrote output/{stem}.svg/.png/.pdf  (OSM {osm_date})")
    if missing:
        print("landmarks not found in OSM data:", ", ".join(missing))


def haloed(pos, text, k):
    """A label drawn twice: a soft land-coloured outline underneath, then the fill.
    (Two elements instead of paint-order, which not every renderer supports.)"""
    return (f'<text {pos} fill="{C["land"]}" stroke="{C["land"]}" stroke-width="{0.9 * k:.2f}" '
            f'stroke-linejoin="round">{text}</text><text {pos}>{text}</text>')


if __name__ == "__main__":
    main()
