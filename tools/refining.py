#!/usr/bin/env python3
"""싱가포르 정제마진(추정)·크랙 스프레드 계산 도구

데이터: 한국석유공사 페트로넷 '일일국제제품가격'(싱가포르 현물, $/bbl)과
        오피넷 '국제유가'의 Dubai(현물). 둘 다 화~토 갱신(T일 가격을 T+1일 공개).
계산:
  - 정제마진(추정) = 제품 가중평균 가격 − Dubai
    가중치(단순화한 수율 가정): 나프타 15%, 휘발유(92RON) 20%, 등유 15%,
    경유(0.001%) 35%, 고유황중유(380cst) 10%, 연료·손실 5%(가치 0)
    ※ 증권사 '싱가포르 복합정제마진'과 수율·운영비 가정이 달라 절대값은 다를 수 있음. 흐름 확인용.
  - 경유 크랙 = 경유(0.001%) − Dubai, 휘발유 크랙 = 휘발유(92RON) − Dubai,
    나프타 크랙 = 나프타 − Dubai
사용법: python3 tools/refining.py   → 최근 2일 값과 전일비를 JSON으로 출력
"""
import html, json, re, subprocess

UA = "Mozilla/5.0"
W = {"나프타": 0.15, "휘발유92": 0.20, "등유": 0.15, "경유0001": 0.35, "중유380": 0.10}

def get(url, data=None):
    cmd = ["curl", "-sS", "-A", UA, "--max-time", "30", url]
    if data:
        cmd[1:1] = ["-X", "POST", "--data", data]
    b = subprocess.run(cmd, capture_output=True).stdout
    h = b.decode("utf-8", errors="replace")
    if h.count("�") > 30:
        h = b.decode("cp949", errors="ignore")
    t = html.unescape(re.sub(r"<script.*?</script>|<style.*?</style>|<[^>]+>", " ", h, flags=re.S | re.I))
    return re.sub(r"\s+", " ", t)

def products():
    t = get("https://www.petronet.co.kr/v4/sub.jsp",
            "fmuId=KDFQSTAT&smuId=KDFQ01&tmuId=KDFQ0200&fmuOrd=03&smuOrd=03_01&tmuOrd=03_01_02")
    i = t.find("일일국제제품가격 목록")
    seg = t[i:i + 4000]
    rows = {}
    year = None
    for m in re.finditer(r"(?:(\d{2})년 )?(\d{1,2})월 (\d{1,2})일 ((?:-?[\d.]+ ){8})", seg):
        if m.group(1):
            year = "20" + m.group(1)
        v = [float(x) for x in m.group(4).split()]
        d = f"{year}-{int(m.group(2)):02d}-{int(m.group(3)):02d}"
        # 열 순서: 휘발유95, 휘발유92, 등유, 경유0.05, 경유0.001, 중유180, 중유380, 나프타
        rows[d] = {"휘발유95": v[0], "휘발유92": v[1], "등유": v[2], "경유005": v[3], "경유0001": v[4],
                   "중유180": v[5], "중유380": v[6], "나프타": v[7]}
    return rows

def dubai():
    t = get("https://www.opinet.co.kr/glopcoilSelect.do")
    out = {}
    # 원/리터 표 다음에 $/bbl 표가 같은 날짜로 반복됨 → 날짜별 마지막 값이 $/bbl
    for m in re.finditer(r"(\d{2})년(\d{1,2})월(\d{1,2})일 ([\d.]+) ([\d.]+) ([\d.]+)", t):
        d = f"20{m.group(1)}-{int(m.group(2)):02d}-{int(m.group(3)):02d}"
        out[d] = {"dubai": float(m.group(4)), "brent": float(m.group(5)), "wti": float(m.group(6))}
    return out

def main():
    p, c = products(), dubai()
    days = sorted(set(p) & set(c))
    res = []
    for d in days:
        pr, du = p[d], c[d]["dubai"]
        basket = sum(pr[k] * w for k, w in W.items())
        res.append({"date": d, "dubai": du, "margin": round(basket - du, 2),
                    "gasoil_crack": round(pr["경유0001"] - du, 2), "gasoline_crack": round(pr["휘발유92"] - du, 2),
                    "naphtha_crack": round(pr["나프타"] - du, 2), "products": pr})
    out = {"latest": res[-1] if res else None, "previous": res[-2] if len(res) > 1 else None,
           "source": "한국석유공사 페트로넷(싱가포르 제품 현물)·오피넷(Dubai)"}
    if out["latest"] and out["previous"]:
        out["change"] = {k: round(out["latest"][k] - out["previous"][k], 2) for k in ["margin", "gasoil_crack", "gasoline_crack", "naphtha_crack"]}
    print(json.dumps(out, ensure_ascii=False, indent=1))

if __name__ == "__main__":
    main()
