#!/usr/bin/env python3
"""LocalNet에 SettlementProposal 1건 생성 (데모/프라이버시 증명용).

전제: settlement DAR이 app-user·app-provider 참여자에 업로드돼 있어야 함.
  python3 upload-dar.py   # (또는 JSON API /v2/packages 로 업로드)
실행 후: python3 ledger-view.py Settlement  → A·B엔 보이고 sv(외부자)엔 안 보임.

토큰: shared-secret HS256(secret="unsafe").
"""
import hmac, hashlib, base64, json, time, urllib.request

PKG = "5959344bd3212e47ebf70a2cde52b8125f79939ca6583f18a8873d574cf9095b"  # quickstart-settlement 0.0.1
TMPL = f"{PKG}:Settlement.FxDvp:SettlementProposal"

def b64(b): return base64.urlsafe_b64encode(b).rstrip(b"=")
def token():
    h = b64(b'{"alg":"HS256","typ":"JWT"}')
    p = b64(json.dumps({"sub": "ledger-api-user", "aud": "https://canton.network.global"}).encode())
    s = b64(hmac.new(b"unsafe", h + b"." + p, hashlib.sha256).digest())
    return (h + b"." + p + b"." + s).decode()
TOK = token()

def call(port, path, method="GET", body=None):
    data = json.dumps(body).encode() if body is not None else None
    r = urllib.request.Request(f"http://127.0.0.1:{port}{path}", data=data, method=method,
        headers={"Authorization": "Bearer " + TOK, "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(r, timeout=30) as x: return x.status, x.read().decode()
    except urllib.error.HTTPError as e: return e.code, e.read().decode()[:600]

# 파티 ID 동적 확보 (app-user 참여자 기준)
_, body = call(2975, "/v2/parties")
ps = [d["party"] for d in json.loads(body)["partyDetails"]]
A = next(p for p in ps if p.startswith("app_user_"))       # 기관A
B = next(p for p in ps if p.startswith("app_provider_"))   # 기관B (+venue 겸용, 데모 단순화)
DSO = next(p for p in ps if p.startswith("DSO::"))          # Amulet 발행자(instrumentId.admin)

def leg(s, r, amt):
    return {"sender": s, "receiver": r, "amount": amt,
            "instrumentId": {"admin": DSO, "id": "Amulet"}, "meta": {"values": {}}}

args = {"venue": B, "settlementCid": None,
        "transferLegs": {"legKRW": leg(A, B, "100.0"), "legJPY": leg(B, A, "20.0")},
        "approvers": [A]}
cmd = {"commands": [{"CreateCommand": {"templateId": TMPL, "createArguments": args}}],
       "commandId": f"demo-settle-{int(time.time())}", "actAs": [A], "userId": "ledger-api-user"}

st, resp = call(2975, "/v2/commands/submit-and-wait", "POST", cmd)
print("SettlementProposal 생성:", st)
print(resp[:300])
print("\n→ 확인: python3 ledger-view.py Settlement  (A·B엔 보이고 sv엔 없음)")
