# 에너지부문 이슈 브리프

HD현대 에너지부문 4개사(오일뱅크·H&L어드밴스드, 일렉트릭, 에너지솔루션, 하이드로젠) 관련 기사·증권사 리포트·정책 이슈를 모아 요약한 정적 웹페이지입니다.

- `index.html` — 페이지 (GitHub Pages로 게시)
- `data/issues.json` — 이슈 목록 (한 줄에 한 건, 최신순)
- `data/meta.json` — 최근 갱신 시각

평일 08:00·15:00(KST)에 Claude 예약 작업이 새 이슈를 `data/issues.json`에 추가하고 커밋합니다.

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
