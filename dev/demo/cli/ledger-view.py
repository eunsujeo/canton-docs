#!/usr/bin/env python3
"""LocalNet 파티별 원장 뷰 — "각 파티가 무엇을 보는가" 요약 (프라이버시 증명용).

각 참여자 노드의 JSON Ledger API를 그 노드의 토큰으로 조회해, 로컬 파티가
이해관계자인 활성 컨트랙트를 템플릿별로 집계한다.
→ 참여자마다 보이는 게 다르고, 무관한 파티(외부자)는 그 거래를 못 본다.

토큰: shared-secret 모드라 HS256(secret="unsafe")로 직접 생성.
사용: python3 ledger-view.py [필터문자열]   (예: Settlement → 정산 관련만)
"""
import hmac, hashlib, base64, json, sys, urllib.request
from collections import Counter

SECRET = "unsafe"
AUD = "https://canton.network.global"
USER = "ledger-api-user"
# (포트, 라벨) — canton이 호스트에 직접 노출
PARTICIPANTS = [
    (2975, "app-user      (기관A)"),
    (3975, "app-provider  (기관B)"),
    (4975, "sv            (외부자 후보)"),
]
FILTER = sys.argv[1] if len(sys.argv) > 1 else None  # 템플릿 부분일치 필터

def b64(b): return base64.urlsafe_b64encode(b).rstrip(b"=")
def token():
    h = b64(b'{"alg":"HS256","typ":"JWT"}')
    p = b64(json.dumps({"sub": USER, "aud": AUD}).encode())
    s = b64(hmac.new(SECRET.encode(), h + b"." + p, hashlib.sha256).digest())
    return (h + b"." + p + b"." + s).decode()
TOK = token()

def call(port, path, method="GET", body=None):
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(f"http://127.0.0.1:{port}{path}", data=data, method=method,
        headers={"Authorization": "Bearer " + TOK, "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=20) as r:
        return json.loads(r.read().decode())

def tmpl_name(tid):  # "hash:Module:Entity" → "Module:Entity"
    parts = tid.split(":")
    return ":".join(parts[1:]) if len(parts) >= 3 else tid

def local_parties(port):
    d = call(port, "/v2/parties")
    return [p["party"] for p in d["partyDetails"]
            if p.get("isLocal") and not p["party"].startswith("participant::")]

def active(port, party, offset):
    req = {"filter": {"filtersByParty": {party: {"cumulative":
            [{"identifierFilter": {"WildcardFilter": {"value": {"includeCreatedEventBlob": False}}}}]}}},
           "verbose": False, "activeAtOffset": offset}
    return call(port, "/v2/state/active-contracts", "POST", req)

def short(p): return p.split("::")[0]

print(f"\n  LocalNet 파티별 원장 뷰" + (f"  (필터: '{FILTER}')" if FILTER else ""))
print("  " + "=" * 60)
for port, label in PARTICIPANTS:
    try:
        off = call(port, "/v2/state/ledger-end")["offset"]
        parties = local_parties(port)
    except Exception as e:
        print(f"\n  ● {label} [:{port}]  — 연결 실패: {e}")
        continue
    print(f"\n  ● {label} [:{port}]  로컬파티: {', '.join(short(p) for p in parties)}")
    counter = Counter()
    for party in parties:
        for entry in active(port, party, off):
            ev = entry.get("contractEntry", {}).get("JsActiveContract", {}).get("createdEvent", {})
            tid = ev.get("templateId")
            if not tid: continue
            name = tmpl_name(tid)
            if FILTER and FILTER.lower() not in name.lower(): continue
            counter[name] += 1
    if not counter:
        print(f"      (보이는 컨트랙트 {'(필터 일치)' if FILTER else ''} 없음)")
    else:
        for name, n in counter.most_common():
            print(f"      {n:>3}  {name}")
print()
