# 에너지부문 이슈 브리프

HD현대 에너지부문 4개사(오일뱅크·H&L어드밴스드, 일렉트릭, 에너지솔루션, 하이드로젠) 관련 기사·증권사 리포트·정책 이슈를 모아 요약한 정적 웹페이지입니다.

- `index.html` — 페이지 (GitHub Pages로 게시)
- `data/issues.json` — 이슈 목록 (한 줄에 한 건, 최신순)
- `data/meta.json` — 최근 갱신 시각

평일 08:00·11:00·15:00·18:00(KST)에 Claude 예약 작업이 새 이슈를 `data/issues.json`에 추가하고 커밋합니다.

## 이슈 항목 형식
| 필드 | 설명 |
|---|---|
| id | `YYYYMMDD-영문-슬러그` |
| date | 기사·발표일 `YYYY-MM-DD` (KST) |
| category | `common` · `oilbank` · `electric` · `solar` · `hydrogen` |
| type | `domestic`(국내기사) · `foreign`(외신) · `report`(리포트) · `policy`(정책) |
| region | `KR` `US` `EU` `GL` `CN` `JP` `ME` `IN` |
| importance | 3 핵심 · 2 주요 · 1 참고 |
| title / originalTitle | 한국어 제목 / 외신 원제 |
| summary | 2~4개 문장 배열 |
| impact | 영향 포인트 (객관적·중립적 서술) |
| source / url / extraLinks | 출처, 원문 https 링크, 추가 링크 `[{label,url}]` |
| addedAt | 추가 시각 ISO8601 |
| detail | (핵심 이슈만) '자세히 보기' 상세 요약, 4~6개 문장 배열 |
| verified | 원문을 직접 열어 읽고 썼으면 true, 검색 결과 발췌 기반이면 false |

## 주요 지표 (`data/indicators.json`)
`{"asOf": "수집 시각", "items": [{group, label, value, unit, change, dir, asOf, source}]}`
- `dir`: `up` · `down` · `flat` (오르면 빨강 ▲, 내리면 파랑 ▼)
- `asOf`: 그 수치의 기준일(예: `11/25`, `11월 3주 평균`). 값을 못 찾으면 직전 값과 기준일을 그대로 둡니다.
