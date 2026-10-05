# seoul-map

서울 전체를 담은 A1/A2 벽걸이 포스터. OpenStreetMap 데이터로 그린 벡터(SVG·PDF) 지도이고, 연보라와 회색만 씁니다.

## 현재 상태

- [x] 저장소 생성, 작업 브랜치 `claude/seoul-poster-draft-gurkv4`
- [x] 구 경계 데이터 확보 (통계청 SGIS 기반, 2026-07-01 기준, 25개 구 확인)
- [x] 레이어별 SVG 렌더링 파이프라인 (가로 A2, 지하철 있음/없음 두 버전)
- [ ] **OSM 데이터 대기 중**: 이 클라우드 환경에서 OpenStreetMap 서버가 모두 차단되어 있어서 `south-korea-latest.osm.pbf` 업로드를 기다리는 중
- [ ] 작은 초안 2종 (지하철 있음/없음) 렌더링 후 검토
- [ ] 한강 곡선·다리·산 위치와 한글 표기 검수
- [ ] 초안 승인 후 A1/A2 최종본 (SVG + PDF)

## 실행 방법

```bash
python3 -m pip install -r requirements.txt
# OSM 다운로드가 막혀 있으면 south-korea-latest.osm.pbf 를 data/raw/ 에 직접 넣기
scripts/build.sh A2        # 또는 A1
```

결과물은 `output/seoul_<크기>_<subway|nosubway>[_draft].{svg,png,pdf}` 로 나옵니다.

```mermaid
flowchart LR
  A[admdongkor 행정동 GeoJSON<br/>통계청 SGIS 2026-07-01] --> B[build_gu.py<br/>25개 구로 합치기]
  C[Geofabrik<br/>south-korea-latest.osm.pbf] --> D[extract_osm.py<br/>물·녹지·도로·지하철·랜드마크]
  B --> E[render.py<br/>EPSG:5179 투영, 서울 경계로 자르기]
  D --> E
  E --> F[SVG 레이어별]
  E --> G[PNG 미리보기]
  E --> H[PDF]
```

## 프로젝트 구조

```
seoul-map/
├── README.md
├── requirements.txt
├── scripts/
│   ├── fetch_data.sh     # 구 경계·OSM·폰트(Pretendard) 받기
│   ├── build_gu.py       # 행정동 → 구 경계 합치기
│   ├── extract_osm.py    # pbf에서 포스터용 레이어만 추출
│   ├── render.py         # 레이어별 SVG + PNG + PDF
│   └── build.sh          # 전체 파이프라인
├── data/
│   ├── raw/              # 원본 (git 제외, 용량이 큼)
│   └── processed/
│       └── gu.geojson    # 서울 25개 구 경계 (커밋됨)
└── output/               # 포스터 결과물
```

## 설계 결정과 그 이유

### 데이터

| 항목 | 선택 | 이유 |
|---|---|---|
| 도로·물·녹지·지하철 | OpenStreetMap (Geofabrik 일일 추출본) | 프로젝트 요구사항. 공개 라이선스(ODbL)라 포스터에 써도 되고, 출처 표기만 하면 됨 |
| 구 경계 | 통계청 SGIS 행정동 경계 (admdongkor ver20260701) → 구 단위로 합침 | 공식 출처 기반이면서 2026-07-01까지 반영된 최신본. 국가공간정보포털·vworld는 이 환경에서 접속 불가 |
| 지하철 노선 | OSM `railway=subway`, `light_rail` 선로 | 공식 노선도 이미지는 저작권이 있어 따라 그리지 않음. 실제 선로 위치를 데이터로 그림 |
| 랜드마크 위치 | OSM에서 이름으로 찾은 좌표만 사용 | 손으로 좌표를 입력하지 않음. 데이터에 없으면 빼고 경고를 출력 |

### 디자인

| 항목 | 선택 | 이유 |
|---|---|---|
| 방향 | 가로 (A2 594×420mm 기준, A1은 같은 비율로 확대) | 서울은 동서(약 37km)가 남북(약 30km)보다 길어서 가로가 꽉 차 보임 |
| 투영 | EPSG:5179 (UTM-K) | 한국 공식 좌표계라 서울 모양이 왜곡 없이 나옴. 위경도 그대로 그리면 동서로 약 25% 늘어남 |
| 범위 | 서울 경계 안쪽만 그리고 바깥은 비움 | 도시 모양이 하나의 실루엣으로 보여서 깔끔하고 귀여운 인상 |
| 위계 | 주요도로 0.50mm 진회색 / 보조 0.26mm / 골목 0.10mm 연회색 | 한강과 큰 길이 먼저 보이고 골목은 질감으로만 남게 |
| 지하철 색 | 공식 노선색 대신 진한 보라 한 가지 | "연보라+회색만" 팔레트를 지키기 위해. 노선색 버전이 필요하면 공식색을 채도만 낮춰 추가 가능 |
| 글꼴 | Pretendard (SIL OFL) | 한글이 깔끔하고 무료로 인쇄물에 쓸 수 있음 |
| 라벨 | 25개 구 이름 + 랜드마크 15곳 | 요구사항(구 이름 + 10~20곳). 글자 뒤에 바탕색 테두리를 둘러 도로 위에서도 읽히게 |
| 터널 도로 | 그리지 않음 | 지하라 지상 풍경과 맞지 않고, 남산 등 녹지 위에 선이 생겨 지저분해짐 |

### 팔레트

| 레이어 | 색 |
|---|---|
| 배경 | `#F3F2F5` |
| 서울 땅 | `#FAF9FB` |
| 공원·산 | `#E2DEEA` |
| 물 | `#BCAEDD` |
| 주요도로 | `#5F5C68` |
| 보조도로 | `#AEABB6` |
| 골목 | `#DAD8DF` |
| 지하철 | `#7458B5` |
| 랜드마크 | `#6E56AA` |
