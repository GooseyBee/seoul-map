"""Landmark icons for the poster, drawn originally for this project.

Style (see README "랜드마크 아이콘"): front elevation view, as on pictorial
tourist maps, so each landmark shows the silhouette people recognise it by
(the curved eaves of 근정전, the pod and mast of N서울타워, the tapering
spire of 롯데월드타워). Shapes are simplified from general knowledge of the
buildings, not traced from photos or anyone's illustration.

Every icon sits on a 24 x 24 unit grid with its base centre at (12, 24), so it
"stands" on the landmark's OSM position. Four tones only, all from the poster
palette: paper white, tint, mid purple (the water colour) and the dark accent,
with one shared outline weight so the set reads as a family.

Each part is (path d, style). Styles:
  tint / mid / white  filled with that tone and outlined in the accent
  dark                solid accent, no outline
  flat                solid mid purple, no outline (small trees)
  line                accent stroke only
  hl                  thin white highlight stroke
"""


def circle(cx, cy, r):
    return f"M{cx - r} {cy}a{r} {r} 0 1 0 {2 * r} 0a{r} {r} 0 1 0 {-2 * r} 0Z"


def pines(*spots):
    """Little pine-tree triangles, (x, base_y, height) each, for hills and mountains."""
    return "".join(f"M{x} {y - h}L{x + h * 0.45} {y}H{x - h * 0.45}Z" for x, y, h in spots)


PALACE = [  # 경복궁 근정전: two-tier stone terrace, columned hall, double roof with upturned eaves
    ("M1.6 24H22.4V22.2H1.6Z", "tint"),
    ("M3.8 22.2V20.8H20.2V22.2", "tint"),
    ("M10.4 24V20.8H13.6V24", "white"),
    ("M10.4 22.4H13.6", "line"),
    ("M5 20.8V16.4H19V20.8Z", "white"),
    ("M7.6 16.4V20.8M9.8 16.4V20.8M14.2 16.4V20.8M16.4 16.4V20.8", "line"),
    ("M10.6 20.8V17.4H13.4V20.8Z", "mid"),
    ("M5.4 12.8H18.6Q20.2 15 23.4 15Q12 17.9 0.6 15Q3.8 15 5.4 12.8Z", "dark"),
    ("M7.6 12.8V10.4H16.4V12.8", "white"),
    ("M8.6 10.4V12.8M10.8 10.4V12.8M13.2 10.4V12.8M15.4 10.4V12.8", "line"),
    ("M8.4 7H15.6Q16.9 9.2 19.8 9.4Q12 11.6 4.2 9.4Q7.1 9.2 8.4 7Z", "dark"),
    ("M7.4 6.4Q8 7 8.8 7H15.2Q16 7 16.6 6.4", "line"),
    ("M3.4 15.4Q12 17 20.6 15.4", "hl"),
]
NAMSAN_TOWER = [  # N서울타워 on 남산: wooded hill, slim shaft, observation pod, mast
    ("M0 24Q3.6 18.2 12 17.8Q20.4 18.2 24 24Z", "tint"),
    (pines((4.4, 22.8, 2.6), (6.6, 21.6, 2.2), (19.4, 22.6, 2.6), (17.2, 21.2, 2)), "flat"),
    ("M10.2 18.4V17H13.8V18.4", "white"),
    ("M11 17L11.4 9.2H12.6L13 17Z", "white"),
    ("M8.4 9.4Q12 11 15.6 9.4L14.8 7.4Q12 6.6 9.2 7.4Z", "mid"),
    ("M9.2 7.4Q12 5.4 14.8 7.4Q12 8 9.2 7.4Z", "dark"),
    ("M9.4 8.6Q12 9.4 14.6 8.6", "hl"),
    ("M11.5 6.2L11.8 1.4H12.2L12.5 6.2Z", "dark"),
    ("M12 1.4V0.2", "line"),
]
LOTTE_TOWER = [  # 롯데월드타워: tapering curved spire with a centre seam and an open crown, mall podium
    ("M4.4 24V21.8Q12 20.6 19.6 21.8V24Z", "tint"),
    ("M8.8 24Q9.4 12 11.3 3.8L12 0.8L12.7 3.8Q14.6 12 15.2 24Z", "white"),
    ("M12 0.8V24", "line"),
    ("M10.4 24Q10.9 13 11.7 4.6M13.6 24Q13.1 13 12.3 4.6", "hl"),
    ("M10.4 24Q10.9 13 11.7 4.6M13.6 24Q13.1 13 12.3 4.6", "line"),
    ("M11.3 3.8L12 0.8L12.7 3.8L12.9 6.2H11.1Z", "mid"),
    ("M11.1 5H12.9", "line"),
]
SQUARE_63 = [  # 63스퀘어: tapering glass tower with a slanted top
    ("M5.2 24V22.4H18.8V24Z", "tint"),
    ("M7.8 22.4L8.8 6.2L15.2 3L16.2 22.4Z", "mid"),
    ("M8.6 9.4H15.4M8.4 12.6H15.6M8.2 15.8H15.8M8 19H16", "hl"),
    ("M12 4.6V22.4", "hl"),
    ("M7.8 22.4L8.8 6.2L15.2 3L16.2 22.4Z", "line"),
]
DDP = [  # 동대문디자인플라자: low, flowing metal shell with panel seams
    ("M0.8 24Q0.2 18.6 4.2 17.4Q8.4 16.2 12.6 15.6Q19.8 14.8 22.6 18.4Q24 20.6 23.2 24Z", "white"),
    ("M2.4 21.6Q11 17.2 21.6 19.2M1.4 23.2Q12 19.6 22.8 21.4", "line"),
    ("M5.4 18.6Q11 16.4 18 16.6", "hl"),
    ("M14.4 24Q15.6 21.6 18.2 22L18.8 24Z", "mid"),
]
STATION = [  # 문화역서울284 (old 서울역): central dome, corner turrets, clock, arched door
    ("M1.4 24V16.8H22.6V24Z", "tint"),
    ("M8 24V13.8H16V24Z", "white"),
    ("M8.6 13.8Q8.6 8.4 12 8.2Q15.4 8.4 15.4 13.8Z", "mid"),
    ("M9.8 12.6Q10 9.8 12 9.4", "hl"),
    ("M11.2 8.4V6.8H12.8V8.4", "white"),
    ("M12 6.8V5.2", "line"),
    ("M2 16.8Q2 14.4 3.6 14.4Q5.2 14.4 5.2 16.8Z M18.8 16.8Q18.8 14.4 20.4 14.4Q22 14.4 22 16.8Z", "mid"),
    (circle(12, 15.9, 1.15), "white"),
    ("M12 15.2V15.9H12.6", "line"),
    ("M10.6 24V20.6Q12 19 13.4 20.6V24Z", "mid"),
    ("M3.2 22.6V20.4Q4 19.4 4.8 20.4V22.6M5.8 22.6V20.4Q6.6 19.4 7.4 20.4V22.6"
     "M16.6 22.6V20.4Q17.4 19.4 18.2 20.4V22.6M19.2 22.6V20.4Q20 19.4 20.8 20.4V22.6", "line"),
]
GROVE = [  # 서울숲: a grove, one big tree between two smaller ones
    ("M5.4 24V20.2H6.4V24ZM17.6 24V20.2H18.6V24Z", "dark"),
    (circle(5.9, 17.4, 3.4) + circle(18.1, 17.4, 3.4), "mid"),
    ("M11.3 24V17.6H12.7V24Z", "dark"),
    (circle(12, 12.4, 5.8), "tint"),
    ("M8.4 11Q9.2 8.2 12 7.6", "hl"),
    ("M1.2 24H22.8", "line"),
]
PARK_TREE = [  # 여의도공원: broad shade tree with a small bench
    ("M11.2 24V16.4H12.8V24Z", "dark"),
    ("M12 17.6Q3.4 17.8 3.6 11.6Q3.8 5 12 4.8Q20.2 5 20.4 11.6Q20.6 17.8 12 17.6Z", "tint"),
    ("M7 10.6Q8 7.4 11.6 6.8", "hl"),
    ("M15 22.4H21M15.6 22.4V24M20.4 22.4V24M15 21H21", "line"),
    ("M1.2 24H22.8", "line"),
]
PEACE_GATE = [  # 올림픽공원 세계평화의문: swept wing roof on paired pillars
    ("M1 24H23", "line"),
    ("M4.4 24V13.2H6.8V24ZM17.2 24V13.2H19.6V24Z", "white"),
    ("M6.8 16.4H17.2M6.8 18H17.2", "line"),
    ("M0.6 9.2Q6 12.2 12 11.4Q18 12.2 23.4 9.2L22.4 12.6Q12 15.4 1.6 12.6Z", "dark"),
    ("M3.6 12.2Q12 14.2 20.4 12.2", "hl"),
]
SKY_PARK = [  # 하늘공원: grassy mound with 억새 tufts and two wind turbines
    ("M0 24Q12 14.2 24 24Z", "tint"),
    ("M4 22.6Q3.6 21 2.8 20.4M4.6 22.4Q4.8 20.8 5.2 19.8M5.2 22.6Q6 21.4 6.8 21"
     "M18.6 22Q18.2 20.4 17.4 19.8M19.2 21.8Q19.4 20.2 19.8 19.2M19.8 22Q20.6 20.8 21.4 20.4", "line"),
    ("M11.5 16.4L11.8 6.2H12.2L12.5 16.4Z", "white"),
    ("M12 6.2L12.5 0.8L12.9 1.2ZM12 6.2L16.8 8.6L16.4 9.1ZM12 6.2L7.1 8.4L7.3 8.9Z", "dark"),
    (circle(12, 6.2, 0.75), "dark"),
    ("M17.8 18.4L18 11.6H18.2L18.4 18.4Z", "white"),
    ("M18.1 11.6L18.4 8L18.7 8.3ZM18.1 11.6L21.3 13.2L21 13.6ZM18.1 11.6L14.9 13L15.1 13.4Z", "dark"),
]
COEX = [  # 코엑스 and 트레이드타워: tall tower with a pointed crown beside the low glass hall
    ("M13.4 24V5.2L15.9 2.8L18.4 5.2V24Z", "mid"),
    ("M15.9 4.2V24", "hl"),
    ("M13.4 24V5.2L15.9 2.8L18.4 5.2V24Z", "line"),
    ("M1.6 24V16.2Q7.6 14.2 13.4 16.2V24Z", "white"),
    ("M4.6 15.4V24M7.5 15V24M10.4 15.4V24M1.6 19.4Q7.6 17.6 13.4 19.4", "line"),
]
AIRPORT = [  # 김포국제공항: climbing jet over a runway
    ("M1.6 24H6.6M9.6 24H14.4M17.4 24H22.4", "line"),
    ("G rotate(-14 12 15)", None),
    ("M2.4 15.6Q2.4 14 4.8 14H17.8Q21.6 14 22.8 15.8Q21.6 17.4 17.8 17.4H4.8Q2.4 17.4 2.4 15.6Z", "white"),
    ("M3.4 14.2L2.2 9.6H4.6L7.6 14Z", "dark"),
    ("M10.2 16.6L7.6 21.4H9.8L14.8 16.6Z", "dark"),
    ("M18.6 14.6Q20.4 14.8 21.4 15.6H18.6Z", "mid"),
    ("M7.6 15.7H8.2M9.6 15.7H10.2M11.6 15.7H12.2M13.6 15.7H14.2M15.6 15.7H16.2", "line"),
    ("G end", None),
]
MOUNT_BUKHAN = [  # 북한산: rounded granite domes (인수봉·백운대)
    ("M0.4 24L5.2 14.8Q6.6 12.6 7.8 14.6L9.4 17L12.4 8.4Q14.4 5.2 16.4 8.4L19.2 13.4L23.6 24Z", "tint"),
    ("M12.4 8.4Q14.4 5.2 16.4 8.4Q15 10 14.4 12.6Q13.6 10 12.4 8.4Z", "mid"),
    ("M5.2 14.8Q6.6 12.6 7.8 14.6Q6.8 15.4 6.4 16.8Q6 15.6 5.2 14.8Z", "mid"),
    (pines((4.4, 23.2, 2.6), (6.6, 23.4, 2.0), (19.6, 23.2, 2.6)), "flat"),
]
MOUNT_GWANAK = [  # 관악산: jagged ridge with the 연주대 pavilion perched on the top crag
    ("M0.4 24L5.8 15.2L8.2 17.2L12 10.2L13.2 11.4L15 9L18.2 14.8L23.6 24Z", "tint"),
    ("M15 9L18.2 14.8L16.4 14L15.4 15.8L14.6 12.4L13.2 11.4Z", "mid"),
    ("M14.2 9V7.9H15.8V9", "white"),
    ("M13.4 8Q15 6.6 16.6 8L15.8 6.8H14.2Z", "dark"),
    (pines((4.4, 23.2, 2.6), (19.8, 23.2, 2.6), (17.8, 23.4, 2)), "flat"),
]
MOUNT_DOBONG = [  # 도봉산: a cluster of sharp rock spires (선인봉·만장봉·자운봉)
    ("M0.4 24L4.6 16L7 17.6L9.4 10.8L10.6 11.6L12.2 6.8L13.8 10.4L14.8 9.2L16.6 12.8L19.4 14.6L23.6 24Z", "tint"),
    ("M12.2 6.8L13.8 10.4L13 12.2L11.6 10.4L10.6 11.6Z M14.8 9.2L16.6 12.8L15.6 12.6Z", "mid"),
    (pines((4.2, 23.2, 2.6), (6.4, 23.4, 2), (19.8, 23.2, 2.6)), "flat"),
]

ICONS = {
    "경복궁": PALACE, "N서울타워": NAMSAN_TOWER, "롯데월드타워": LOTTE_TOWER, "63스퀘어": SQUARE_63,
    "동대문디자인플라자": DDP, "서울역": STATION, "서울숲": GROVE, "올림픽공원": PEACE_GATE,
    "여의도공원": PARK_TREE, "하늘공원": SKY_PARK, "코엑스": COEX, "김포국제공항": AIRPORT,
    "북한산": MOUNT_BUKHAN, "관악산": MOUNT_GWANAK, "도봉산": MOUNT_DOBONG,
}


def icon_svg(name, x, y, size, colors, stroke):
    """SVG for icon `name` with its base centre at (x, y), `size` mm tall."""
    parts = ICONS.get(name)
    if not parts:
        return ""
    s = size / 24
    sw = stroke / s
    fills = {
        "tint":  (colors["tint"], colors["accent"], sw),
        "mid":   (colors["water"], colors["accent"], sw),
        "white": (colors["land"], colors["accent"], sw),
        "dark":  (colors["accent"], "none", 0),
        "flat":  (colors["water"], "none", 0),
        "line":  ("none", colors["accent"], sw),
        "hl":    ("none", colors["land"], sw * 0.8),
    }
    head = (f'<g transform="translate({x - 12 * s:.2f} {y - 24 * s:.2f}) scale({s:.4f})" '
            f'stroke-linejoin="round" stroke-linecap="round">')
    halo, body = [], []
    # soft ground shadow so the icon sits on the map rather than floating
    body.append(f'<ellipse cx="12" cy="24" rx="8" ry="1.1" fill="{colors["water"]}" opacity="0.55"/>')
    for d, style in parts:
        if style is None:  # group markers
            tag = "</g>" if d == "G end" else f'<g transform="{d[2:]}">'
            halo.append(tag)
            body.append(tag)
            continue
        fill, line, w = fills[style]
        if style != "hl":  # land-coloured halo lifts the icon off the roads underneath
            halo.append(f'<path d="{d}" fill="{colors["land"]}" stroke="{colors["land"]}" '
                        f'stroke-width="{sw * 5:.3f}"/>')
        body.append(f'<path d="{d}" fill="{fill}" stroke="{line}" stroke-width="{w:.3f}"/>')
    return head + "".join(halo) + "".join(body) + "</g>"
