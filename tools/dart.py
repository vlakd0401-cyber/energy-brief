#!/usr/bin/env python3
"""DART 공시 조회 도우미 (API 키 불필요, dart.fss.or.kr 공개 화면 사용)

사용법:
  python3 tools/dart.py list "HD현대일렉트릭" [보고서명 키워드] [시작일 YYYYMMDD]
      → 최근 공시 목록(접수번호, 보고서명, 접수일)
  python3 tools/dart.py sections 20261116001028
      → 보고서 목차(섹션 이름)
  python3 tools/dart.py read 20261116001028 ["3. 원재료 및 생산설비"]
      → 공시 본문(또는 해당 섹션) 텍스트
원문 링크: https://dart.fss.or.kr/dsaf001/main.do?rcpNo=<접수번호>
"""
import html, re, subprocess, sys, urllib.parse
from datetime import date

UA = "Mozilla/5.0"

def curl(url, data=None):
    cmd = ["curl", "-sS", "-A", UA, "--max-time", "30", url]
    if data is not None:
        cmd[1:1] = ["-X", "POST", "-H", "X-Requested-With: XMLHttpRequest",
                    "-H", "Referer: https://dart.fss.or.kr/dsab007/main.do", "--data", urllib.parse.urlencode(data)]
    return subprocess.run(cmd, capture_output=True).stdout

def text(b):
    head = b[:4000].lower()
    if b"euc-kr" in head or b"ks_c_5601" in head:
        h = b.decode("cp949", errors="ignore")
    else:
        try:
            h = b.decode("utf-8")
        except UnicodeDecodeError:
            h = b.decode("cp949", errors="ignore")
    t = html.unescape(re.sub(r"<style.*?</style>|<script.*?</script>|<[^>]+>", " ", h, flags=re.S | re.I))
    t = re.sub(r"\.xforms[^{]*\{[^}]*\}", " ", t)
    t = re.sub(r"[ \t\xa0]+", " ", t)
    return re.sub(r"\n\s*\n+", "\n", t).strip()

def list_reports(corp, name="", start="20250101"):
    data = {"currentPage": 1, "maxResults": 100, "maxLinks": 10, "sort": "date", "series": "desc",
            "option": "corp", "textCrpNm": corp, "textCrpCik": "", "reportName": "",
            "startDate": start, "endDate": date.today().strftime("%Y%m%d"),
            "finalReport": "recent", "businessCode": "all", "autoSearch": "N"}
    h = curl("https://dart.fss.or.kr/dsab007/detailSearch.ax", data).decode("utf-8", errors="ignore")
    for tr in re.findall(r"<tr>(.*?)</tr>", h, re.S):
        rc = re.search(r"rcpNo=(\d{14})", tr)
        if rc:
            cells = [html.unescape(re.sub(r"<[^>]+>|\s+", " ", c)).strip() for c in re.findall(r"<td[^>]*>(.*?)</td>", tr, re.S)]
            line = " | ".join(c for c in cells[1:5] if c)
            if not name or name in line:
                print(rc.group(1), line)

def nodes(rcp):
    h = curl(f"https://dart.fss.or.kr/dsaf001/main.do?rcpNo={rcp}").decode("utf-8", errors="ignore")
    pat = (r"node\d+\['text'\]\s*=\s*\"([^\"]+)\";\s*node\d+\['id'\]\s*=\s*\"\d+\";\s*node\d+\['rcpNo'\]\s*=\s*\"(\d+)\";"
           r"\s*node\d+\['dcmNo'\]\s*=\s*\"(\d+)\";\s*node\d+\['eleId'\]\s*=\s*\"(\d+)\";\s*node\d+\['offset'\]\s*=\s*\"(\d+)\";"
           r"\s*node\d+\['length'\]\s*=\s*\"(\d+)\";\s*node\d+\['dtd'\]\s*=\s*\"([^\"]+)\"")
    ns = re.findall(pat, h)
    if not ns:  # 단일 문서 공시
        m = re.search(r'viewDoc\("(\d+)",\s*"(\d+)",\s*"(\d+)",\s*"(\d+)",\s*"(\d+)",\s*"(\w+)"', h)
        if m:
            ns = [("본문",) + m.groups()]
    return ns

def read(rcp, section=None):
    for n in nodes(rcp):
        if section and not n[0].startswith(section):
            continue
        url = f"https://dart.fss.or.kr/report/viewer.do?rcpNo={n[1]}&dcmNo={n[2]}&eleId={n[3]}&offset={n[4]}&length={n[5]}&dtd={n[6]}"
        print(f"## {n[0]}\n{text(curl(url))}\n")
        if not section:
            break

if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    if cmd == "list":
        list_reports(sys.argv[2], *(sys.argv[3:5]))
    elif cmd == "sections":
        for n in nodes(sys.argv[2]):
            print(n[0])
    elif cmd == "read":
        read(sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else None)
    else:
        print(__doc__)
