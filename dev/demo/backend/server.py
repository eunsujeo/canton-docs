#!/usr/bin/env python3
"""데모 백엔드 (thin) — 파티별 원장 뷰(JSON) + 시나리오 액션 + 프론트 서빙.

의존성 없음(Python stdlib). LocalNet JSON Ledger API를 참여자별 토큰으로 호출.
  python3 server.py            # http://localhost:8888
액션: POST /api/action {"step":"create|accept|initiate|execute|reset"}
"""
import hmac, hashlib, base64, json, os, time, urllib.request
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

AUD = "https://canton.network.global"; USER = "ledger-api-user"; SECRET = "unsafe"
PKG = "5959344bd3212e47ebf70a2cde52b8125f79939ca6583f18a8873d574cf9095b"  # quickstart-settlement
T_PROP = f"{PKG}:Settlement.FxDvp:SettlementProposal"
T_SETTLE = f"{PKG}:Settlement.FxDvp:Settlement"
# 패널 = (참여자 포트, key, 표시이름, 역할)
PARTIES = [
    (2975, "A",        "국내은행", "제안 기관 · app-user"),
    (3975, "B",        "해외은행", "상대 기관 · app-provider·venue"),
    (4975, "outsider", "제3자",   "무관 기관 · sv"),
]
# 파티 ID → 친근한 표시 이름
def label(p):
    if not p: return p
    if p.startswith("app_user_"): return "국내은행"
    if p.startswith("app_provider_"): return "해외은행"
    if p.startswith("DSO::"): return "DSO"
    if p.startswith("sv::"): return "SV"
    return p.split("::")[0]
HERE = os.path.dirname(os.path.abspath(__file__))
FRONTEND = os.path.join(HERE, "..", "frontend", "index.html")

def _b64(b): return base64.urlsafe_b64encode(b).rstrip(b"=")
def _token():
    h = _b64(b'{"alg":"HS256","typ":"JWT"}'); p = _b64(json.dumps({"sub": USER, "aud": AUD}).encode())
    s = _b64(hmac.new(SECRET.encode(), h + b"." + p, hashlib.sha256).digest())
    return (h + b"." + p + b"." + s).decode()
TOK = _token()

def _call(port, path, method="GET", body=None):
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(f"http://127.0.0.1:{port}{path}", data=data, method=method,
        headers={"Authorization": "Bearer " + TOK, "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=20) as r:
        return json.loads(r.read().decode())

def _short(p): return p.split("::")[0] if p else p
def _tmpl(tid):
    parts = tid.split(":"); return ":".join(parts[1:]) if len(parts) >= 3 else tid

# ---- 파티 해석 ----
def parties():
    pd = _call(2975, "/v2/parties")["partyDetails"]
    A = next(p["party"] for p in pd if p["party"].startswith("app_user_") and p.get("isLocal"))
    B = next(p["party"] for p in pd if p["party"].startswith("app_provider_"))
    DSO = next(p["party"] for p in pd if p["party"].startswith("DSO::"))
    return A, B, DSO

# ---- ACS 조회 ----
def active(port, party):
    off = _call(port, "/v2/state/ledger-end")["offset"]
    req = {"filter": {"filtersByParty": {party: {"cumulative":
            [{"identifierFilter": {"WildcardFilter": {"value": {"includeCreatedEventBlob": False}}}}]}}},
           "verbose": False, "activeAtOffset": off}
    out = []
    for e in _call(port, "/v2/state/active-contracts", "POST", req):
        ev = e.get("contractEntry", {}).get("JsActiveContract", {}).get("createdEvent", {})
        if ev.get("templateId"): out.append(ev)
    return out

def find(port, party, suffix):
    return [(ev["contractId"], ev.get("createArgument", {}))
            for ev in active(port, party) if ev.get("templateId", "").endswith(suffix)]

# ---- 커맨드 ----
def submit(port, actAs, command):
    cmd = {"commands": [command], "commandId": f"demo-{int(time.time()*1000)}",
           "actAs": [actAs], "userId": USER}
    return _call(port, "/v2/commands/submit-and-wait", "POST", cmd)

def create_proposal():
    A, B, DSO = parties()
    def leg(s, r, amt): return {"sender": s, "receiver": r, "amount": amt,
        "instrumentId": {"admin": DSO, "id": "Amulet"}, "meta": {"values": {}}}
    args = {"venue": B, "settlementCid": None,
            "transferLegs": {"legKRW": leg(A, B, "100.0"), "legJPY": leg(B, A, "20.0")},
            "approvers": [A]}
    return submit(2975, A, {"CreateCommand": {"templateId": T_PROP, "createArguments": args}})

def ex(port, actAs, cid, choice, arg, tmpl):
    return submit(port, actAs, {"ExerciseCommand":
        {"templateId": tmpl, "contractId": cid, "choice": choice, "choiceArgument": arg}})

# ---- 지갑(Validator) API: 토큰표준 할당 생성 ----
import re as _re, calendar as _cal, time as _time
def _wtoken(sub):
    h = _b64(b'{"alg":"HS256","typ":"JWT"}'); p = _b64(json.dumps({"sub": sub, "aud": AUD}).encode())
    s = _b64(hmac.new(SECRET.encode(), h + b"." + p, hashlib.sha256).digest()); return (h + b"." + p + b"." + s).decode()
def _wcall(wport, sub, path, method="GET", body=None):
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(f"http://127.0.0.1:{wport}/api/validator{path}", data=data, method=method,
        headers={"Authorization": "Bearer " + _wtoken(sub), "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read().decode())
def _snake(k): return _re.sub(r'(?<!^)(?=[A-Z])', '_', k).lower()
def _conv(o):
    if isinstance(o, dict): return {_snake(k): _conv(v) for k, v in o.items()}
    if isinstance(o, list): return [_conv(x) for x in o]
    return o
def _flatmeta(o):
    if isinstance(o, dict):
        if set(o.keys()) == {"values"} and isinstance(o["values"], dict): return _flatmeta(o["values"])
        return {k: _flatmeta(v) for k, v in o.items()}
    if isinstance(o, list): return [_flatmeta(x) for x in o]
    return o
def _micros(iso):
    m = _re.match(r'(.*?)(\.\d+)?(Z|\+0000)$', iso)
    t = _cal.timegm(_time.strptime(m.group(1), "%Y-%m-%dT%H:%M:%S"))
    return int(t * 1_000_000 + round(float(m.group(2) or 0) * 1_000_000))
def _alloc_legs(wport, sub, ref_cid):
    """그 지갑에서 ref_cid 정산에 대해 이미 잠근 leg 집합."""
    out = set()
    for a in _wcall(wport, sub, "/v0/allocations").get("allocations", []):
        al = a["contract"]["payload"]["allocation"]
        if al["settlement"].get("settlementRef", {}).get("cid") == ref_cid:
            out.add(al.get("transferLegId"))
    return out

def allocate_for(wport, sub, sender_prefix, ref_cid):
    """그 은행 지갑에서 현재 정산(ref_cid)의 자기 leg를 잠근다. 이미 잠긴 leg는 skip(중복 방지)."""
    have = _alloc_legs(wport, sub, ref_cid)
    reqs = _wcall(wport, sub, "/v0/wallet/token-standard/allocation-requests").get("allocation_requests", [])
    done = 0
    for r in reqs:
        pl = r["contract"]["payload"]
        if pl["settlement"].get("settlementRef", {}).get("cid") != ref_cid: continue
        s = _flatmeta(_conv(pl["settlement"]))
        for f in ("requested_at", "allocate_before", "settle_before"):
            if isinstance(s.get(f), str): s[f] = _micros(s[f])
        for legId, leg in pl.get("transferLegs", {}).items():
            if leg["sender"].startswith(sender_prefix) and legId not in have:
                _wcall(wport, sub, "/v0/allocations", "POST",
                       {"settlement": s, "transfer_leg_id": legId, "transfer_leg": _flatmeta(_conv(leg))})
                done += 1
    return done

def current_ref():
    """현재 살아있는 Settlement의 ref cid (= 원 제안 cid). 없으면 None."""
    _, B, _ = parties()
    for cid, arg in find(3975, B, "Settlement"):
        return arg.get("settlementCid")
    return None

def allocated_legs(ref_cid):
    if not ref_cid: return set()
    legs = set()
    for wport, sub in [(2000, "app-user"), (3000, "app-provider")]:
        try: legs |= _alloc_legs(wport, sub, ref_cid)
        except Exception: pass
    return legs

def do_action(step):
    A, B, DSO = parties()
    if step == "create":
        create_proposal(); return {"ok": True, "msg": "기관 A가 정산을 제안했습니다."}
    if step == "accept":
        props = find(3975, B, "SettlementProposal")
        for cid, arg in props:
            if B not in arg.get("approvers", []):
                ex(3975, B, cid, "SettlementProposal_Accept", {"approver": B}, T_PROP)
                return {"ok": True, "msg": "기관 B가 제안을 수락했습니다."}
        return {"ok": False, "msg": "수락할 제안이 없습니다(이미 수락됨?)."}
    if step == "initiate":
        props = find(3975, B, "SettlementProposal")
        for cid, arg in props:
            if A in arg.get("approvers", []) and B in arg.get("approvers", []):
                now = time.time()
                fmt = lambda t: time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(t))
                ex(3975, B, cid, "SettlementProposal_InitiateSettlement",
                   {"prepareUntil": fmt(now+3600), "settleBefore": fmt(now+7200)}, T_PROP)
                return {"ok": True, "msg": "venue가 정산을 개시했습니다(Settlement 생성)."}
        return {"ok": False, "msg": "양측 수락된 제안이 없습니다."}
    if step == "allocate":
        ref = current_ref()
        if not ref: return {"ok": False, "msg": "개시된 정산이 없습니다. 먼저 정산을 개시하세요."}
        n = allocate_for(2000, "app-user", "app_user_", ref) + allocate_for(3000, "app-provider", "app_provider_", ref)
        return {"ok": True, "msg": f"양측이 자기 통화를 잠갔습니다(신규 할당 {n}건). 자산이 묶였습니다." if n
                else "이미 양측 자산이 잠겨 있습니다."}
    if step == "execute":
        return {"ok": False, "msg": "실행(원자적 정산)은 준비 중입니다. (할당 실행 컨텍스트 구현 중)"}
    if step == "reset":
        n = 0
        for cid, arg in find(2975, A, "SettlementProposal"):
            try: ex(2975, A, cid, "SettlementProposal_Reject", {"trader": A}, T_PROP); n += 1
            except Exception: pass
        for cid, arg in find(3975, B, "Settlement"):
            try: ex(3975, B, cid, "Settlement_Cancel", {"allocationsWithContext": {}}, T_SETTLE); n += 1
            except Exception: pass
        return {"ok": True, "msg": f"초기화 완료(정리 {n}건)."}
    return {"ok": False, "msg": f"알 수 없는 단계: {step}"}

# ---- 패널 뷰 ----
def party_view(port):
    pd = _call(port, "/v2/parties")["partyDetails"]
    locals_ = [p["party"] for p in pd if p.get("isLocal") and not p["party"].startswith("participant::")]
    counts, settlements = {}, []
    for party in locals_:
        for ev in active(port, party):
            name = _tmpl(ev["templateId"]); counts[name] = counts.get(name, 0) + 1
            if "Settlement.FxDvp" in name:
                arg = ev.get("createArgument", {}); legs = arg.get("transferLegs", {})
                settlements.append({
                    "template": name.split(":")[-1], "contractId": ev.get("contractId", "")[:12] + "…",
                    "approvers": [label(a) for a in arg.get("approvers", [])],
                    "legs": {k: {"from": label(v.get("sender")), "to": label(v.get("receiver")),
                                 "amount": v.get("amount"), "inst": (v.get("instrumentId") or {}).get("id")}
                             for k, v in legs.items()}})
    return {"parties": [label(p) for p in locals_], "counts": counts, "settlements": settlements}

def state():
    out = []
    for port, key, name, role in PARTIES:
        try: out.append({"key": key, "name": name, "role": role, "ok": True, **party_view(port)})
        except Exception as e: out.append({"key": key, "name": name, "role": role, "ok": False, "error": str(e)})
    # 현재 정산 기준 할당 여부(양 leg)
    allocated = False
    try:
        ref = current_ref(); legs = allocated_legs(ref)
        allocated = bool(ref) and ("legKRW" in legs) and ("legJPY" in legs)
    except Exception: pass
    return {"panels": out, "allocated": allocated}

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
        else: self._send(404, "not found", "text/plain")
    def do_POST(self):
        if self.path.startswith("/api/action"):
            ln = int(self.headers.get("Content-Length", 0))
            step = json.loads(self.rfile.read(ln) or b"{}").get("step", "")
            try: self._send(200, json.dumps(do_action(step), ensure_ascii=False))
            except Exception as e: self._send(200, json.dumps({"ok": False, "msg": str(e)[:200]}, ensure_ascii=False))
        else: self._send(404, "not found", "text/plain")

if __name__ == "__main__":
    print("데모 백엔드: http://localhost:8888  (Ctrl+C 종료)")
    ThreadingHTTPServer(("127.0.0.1", 8888), H).serve_forever()
