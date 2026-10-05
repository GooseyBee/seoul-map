"""Small original landmark icons, drawn for this poster.

Each icon lives in a 10 x 10 unit box with its base centre at (5, 10), so it
"stands" on the landmark's OSM position. Shapes are simple geometric
silhouettes, not traced from photos or anyone's artwork.

Each entry is a list of (path d, style) where style is
  "body"  filled with the soft tint, outlined in the accent colour
  "solid" filled with the accent colour
  "line"  outline only
"""

PALACE = [  # 경복궁: stone base, hall, two-tier curved roof
    ("M1.2 10H8.8V9H1.2Z", "body"),
    ("M2.3 9V6.2H7.7V9", "body"),
    ("M3.8 9V7.2H6.2V9", "line"),
    ("M0.6 6.3Q5 4.6 9.4 6.3L8.2 4.9Q5 3.9 1.8 4.9Z", "solid"),
    ("M3 4.4V3.6H7V4.4", "body"),
    ("M1.9 3.7Q5 2.2 8.1 3.7L7.2 2.6Q5 1.9 2.8 2.6Z", "solid"),
]
NAMSAN_TOWER = [  # N서울타워 on 남산
    ("M0.6 10Q5 6.6 9.4 10Z", "body"),
    ("M4.5 8.4L4.7 3.8H5.3L5.5 8.4Z", "body"),
    ("M3.3 3.5Q5 2.3 6.7 3.5Q5 4.6 3.3 3.5Z", "solid"),
    ("M5 2.7V0.4", "line"),
]
LOTTE_TOWER = [  # 롯데월드타워: tall tapering spire
    ("M3.4 10L4.5 1.6Q5 0.2 5.5 1.6L6.6 10Z", "body"),
    ("M5 1.4V10", "line"),
]
SQUARE_63 = [  # 63스퀘어: slanted-top tower
    ("M3.6 10V2.8L6.4 1.4V10Z", "solid"),
    ("M4.3 4H5.7M4.3 5.6H5.7M4.3 7.2H5.7M4.3 8.8H5.7", "white"),
]
DDP = [  # 동대문디자인플라자: soft flowing blob
    ("M0.8 10Q0.2 6.6 3 6Q5 5.2 7.2 6Q9.9 6.8 9.2 10Z", "body"),
    ("M2 8.3Q5 6.8 8 8.3", "line"),
]
STATION = [  # 서울역: domed old station
    ("M1.4 10V6.4H8.6V10Z", "body"),
    ("M3.2 6.4Q5 3.4 6.8 6.4Z", "solid"),
    ("M5 4.4V3", "line"),
    ("M4.2 10V8.2Q5 7.2 5.8 8.2V10", "line"),
]
TREE = [  # parks: round tree
    ("M4.5 10V7.4H5.5V10Z", "solid"),
    ("M5 8Q1.6 8 1.8 5.2Q2 2 5 2Q8 2 8.2 5.2Q8.4 8 5 8Z", "body"),
]
TWIN_TREES = [  # 서울숲: two trees
    ("M3.2 10V7.6H4V10ZM6.6 10V8.2H7.4V10Z", "solid"),
    ("M3.6 8Q0.8 8 1 5.4Q1.2 2.4 3.6 2.4Q6 2.4 6.2 5.4Q6.4 8 3.6 8Z", "body"),
    ("M7 8.6Q5 8.6 5.2 6.6Q5.4 4.6 7 4.6Q8.8 4.6 8.9 6.6Q9 8.6 7 8.6Z", "body"),
]
GATE = [  # 올림픽공원: tall gate with a wing roof
    ("M2.6 10V5.2H3.6V10ZM6.4 10V5.2H7.4V10Z", "solid"),
    ("M0.8 5.2Q5 2.4 9.2 5.2Q5 4.2 0.8 5.2Z", "body"),
]
WINDMILL = [  # 하늘공원: wind turbine on a grassy mound
    ("M0.6 10Q5 7.4 9.4 10Z", "body"),
    ("M4.8 8.6L4.9 4.4H5.1L5.2 8.6Z", "solid"),
    ("M5 4.4L5.3 0.8M5 4.4L8 5.8M5 4.4L1.9 5.6", "line"),
]
MALL = [  # 코엑스: glass box
    ("M1.4 10V4.2H8.6V10Z", "body"),
    ("M3.8 4.2V10M6.2 4.2V10M1.4 6.2H8.6M1.4 8.1H8.6", "line"),
]
PLANE = [  # 김포국제공항
    ("M5 1Q5.6 1 5.6 2.2V4.6L9.4 6.8V7.8L5.6 6.6V8.6L6.8 9.4V10L5 9.5L3.2 10V9.4L4.4 8.6V6.6L0.6 7.8V6.8"
     "L4.4 4.6V2.2Q4.4 1 5 1Z", "solid"),
]
MOUNTAIN = [  # 북한산, 관악산, 도봉산: two peaks with snowy caps
    ("M0.4 10L3.6 4.6L5.2 6.8L6.8 3.2L9.6 10Z", "body"),
    ("M5.8 5.4L6.8 3.2L7.8 5.4L6.8 5Z", "solid"),
]

ICONS = {
    "경복궁": PALACE, "N서울타워": NAMSAN_TOWER, "롯데월드타워": LOTTE_TOWER, "63스퀘어": SQUARE_63,
    "동대문디자인플라자": DDP, "서울역": STATION, "서울숲": TWIN_TREES, "올림픽공원": GATE,
    "여의도공원": TREE, "하늘공원": WINDMILL, "코엑스": MALL, "김포국제공항": PLANE,
    "북한산": MOUNTAIN, "관악산": MOUNTAIN, "도봉산": MOUNTAIN,
}


def icon_svg(name, x, y, size, colors, stroke):
    """SVG for icon `name` with its base centre at (x, y), `size` mm tall."""
    parts = ICONS.get(name)
    if not parts:
        return ""
    s = size / 10
    fills = {"body": (colors["tint"], colors["accent"]), "solid": (colors["accent"], "none"),
             "line": ("none", colors["accent"]), "white": ("none", colors["land"])}
    out = [f'<g transform="translate({x - 5 * s:.2f} {y - 10 * s:.2f}) scale({s:.4f})" '
           f'stroke-width="{stroke / s:.3f}" stroke-linejoin="round" stroke-linecap="round">']
    for d, _ in parts:  # soft land-coloured halo so icons sit cleanly on top of roads
        out.append(f'<path d="{d}" fill="{colors["land"]}" stroke="{colors["land"]}" '
                   f'stroke-width="{stroke * 4 / s:.3f}"/>')
    for d, style in parts:
        fill, line = fills[style]
        out.append(f'<path d="{d}" fill="{fill}" stroke="{line}"/>')
    out.append("</g>")
    return "".join(out)
