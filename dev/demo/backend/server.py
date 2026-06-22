#!/usr/bin/env python3
"""데모 백엔드 (thin) — 파티별 원장 뷰를 JSON으로 제공 + 프론트 HTML 서빙.

의존성 없음(Python stdlib). LocalNet JSON Ledger API를 참여자별 토큰으로 호출.
  python3 server.py            # http://localhost:8888
프론트는 /api/state 를 폴링해 각 파티 패널을 실시간 갱신.
"""
import hmac, hashlib, base64, json, os, urllib.request
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

AUD = "https://canton.network.global"
USER = "ledger-api-user"
SECRET = "unsafe"
# 패널 = (참여자 포트, key, 표시이름, 역할)
PARTIES = [
    (2975, "A",        "기관 A", "app-user (제안자)"),
    (3975, "B",        "기관 B", "app-provider (+venue)"),
    (4975, "outsider", "외부자", "sv (무관 제3자)"),
]
HERE = os.path.dirname(os.path.abspath(__file__))
FRONTEND = os.path.join(HERE, "..", "frontend", "index.html")

def _b64(b): return base64.urlsafe_b64encode(b).rstrip(b"=")
def _token():
    h = _b64(b'{"alg":"HS256","typ":"JWT"}')
    p = _b64(json.dumps({"sub": USER, "aud": AUD}).encode())
    s = _b64(hmac.new(SECRET.encode(), h + b"." + p, hashlib.sha256).digest())
    return (h + b"." + p + b"." + s).decode()
TOK = _token()

def _call(port, path, method="GET", body=None):
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(f"http://127.0.0.1:{port}{path}", data=data, method=method,
        headers={"Authorization": "Bearer " + TOK, "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=15) as r:
        return json.loads(r.read().decode())

def _short(p): return p.split("::")[0] if p else p
def _tmpl(tid):
    parts = tid.split(":"); return ":".join(parts[1:]) if len(parts) >= 3 else tid

def party_view(port):
    """그 참여자가 보는 활성 컨트랙트 요약 (Settlement는 상세 포함)."""
    off = _call(port, "/v2/state/ledger-end")["offset"]
    pd = _call(port, "/v2/parties")["partyDetails"]
    locals_ = [p["party"] for p in pd if p.get("isLocal") and not p["party"].startswith("participant::")]
    counts, settlements = {}, []
    for party in locals_:
        req = {"filter": {"filtersByParty": {party: {"cumulative":
                [{"identifierFilter": {"WildcardFilter": {"value": {"includeCreatedEventBlob": False}}}}]}}},
               "verbose": False, "activeAtOffset": off}
        for e in _call(port, "/v2/state/active-contracts", "POST", req):
            ev = e.get("contractEntry", {}).get("JsActiveContract", {}).get("createdEvent", {})
            tid = ev.get("templateId")
            if not tid: continue
            name = _tmpl(tid)
            counts[name] = counts.get(name, 0) + 1
            if "Settlement.FxDvp" in name:
                arg = ev.get("createArgument", {})
                legs = arg.get("transferLegs", {})
                settlements.append({
                    "template": name.split(":")[-1],
                    "contractId": ev.get("contractId", "")[:16] + "…",
                    "approvers": [_short(a) for a in arg.get("approvers", [])],
                    "legs": {k: {"from": _short(v.get("sender")), "to": _short(v.get("receiver")),
                                 "amount": v.get("amount"), "inst": (v.get("instrumentId") or {}).get("id")}
                             for k, v in legs.items()},
                })
    return {"parties": [_short(p) for p in locals_], "counts": counts, "settlements": settlements}

def state():
    out = []
    for port, key, name, role in PARTIES:
        try:
            v = party_view(port)
            out.append({"key": key, "name": name, "role": role, "ok": True, **v})
        except Exception as e:
            out.append({"key": key, "name": name, "role": role, "ok": False, "error": str(e)})
    return {"panels": out}

class H(BaseHTTPRequestHandler):
    def log_message(self, *a): pass
    def _send(self, code, body, ctype="application/json"):
        b = body.encode() if isinstance(body, str) else body
        self.send_response(code); self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(b))); self.end_headers(); self.wfile.write(b)
    def do_GET(self):
        if self.path.startswith("/api/state"):
            try: self._send(200, json.dumps(state(), ensure_ascii=False))
            except Exception as e: self._send(500, json.dumps({"error": str(e)}))
        elif self.path in ("/", "/index.html"):
            try: self._send(200, open(FRONTEND, "rb").read(), "text/html; charset=utf-8")
            except FileNotFoundError: self._send(404, "frontend/index.html 없음")
        else:
            self._send(404, "not found", "text/plain")

if __name__ == "__main__":
    print("데모 백엔드: http://localhost:8888  (Ctrl+C로 종료)")
    ThreadingHTTPServer(("127.0.0.1", 8888), H).serve_forever()
