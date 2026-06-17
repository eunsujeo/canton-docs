#!/usr/bin/env python3
"""Canton LocalNet — Scan 상태 한눈에 보기.

Scan UI가 보기 불편해서, 학습에 필요한 것만 요약하는 CLI 도구.
  python3 scan-status.py    # 현재 상태 1회 출력
"""
import json, time, calendar, urllib.request

# macOS 기본 resolver는 *.localhost 서브도메인을 해석 못 하므로
# 127.0.0.1로 붙고 Host 헤더로 nginx 가상호스트 라우팅을 시킨다.
BASE = "http://127.0.0.1:4000/api/scan/v0"
HOST = "scan.localhost"

def get(path, method="GET", body=None):
    url = BASE + path
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(url, data=data, method=method,
                                 headers={"Content-Type": "application/json", "Host": HOST})
    try:
        with urllib.request.urlopen(req, timeout=5) as r:
            return r.status, json.load(r)
    except urllib.error.HTTPError as e:
        try: return e.code, json.load(e)
        except Exception: return e.code, None
    except Exception as e:
        return None, {"error": str(e)}

def short(pid, n=16):
    if not pid: return "?"
    # app_user_… / app_provider_… / sv:: / DSO:: 를 친근한 라벨로
    head = pid.split("::")[0]
    if head.startswith("app_user"): return "app-user"
    if head.startswith("app_provider"): return "app-provider"
    if head.startswith("sv"): return "SV"
    if head.startswith("DSO"): return "DSO"
    return pid[:n] + "…"

def num(p, payload="round"):
    try: return p["contract"]["payload"]["round"]["number"]
    except Exception: return "?"

def hhmmss(iso):
    """ISO UTC 문자열 → 로컬 시각 HH:MM:SS."""
    try:
        s = iso.replace("Z", "+0000").split(".")[0]
        t = time.strptime(s, "%Y-%m-%dT%H:%M:%S")
        epoch = calendar.timegm(t)  # UTC 기준 epoch
        return time.strftime("%H:%M:%S", time.localtime(epoch))
    except Exception:
        return (iso or "")[11:19]

def cc(v):
    try: return f"{float(v):,.0f}"
    except Exception: return str(v)

def render():
    lines = []
    ts = time.strftime("%Y-%m-%d %H:%M:%S")
    lines.append(f"\n  Canton LocalNet · Scan 상태   ({ts})")
    lines.append("  " + "─" * 52)

    code, dso = get("/dso")
    if code != 200 or not dso:
        lines.append(f"  ❌ Scan 연결 실패 — LocalNet이 떠 있나요? (make start)")
        lines.append(f"     {dso.get('error') if dso else ''}")
        return "\n".join(lines)

    sv = short(dso.get("sv_party_id"))
    latest = num(dso.get("latest_mining_round", {}))
    lines.append(f"  SV            : {dso.get('sv_party_id','?')[:30]}…")
    lines.append(f"  DSO           : {dso.get('dso_party_id','?')[:30]}…  (의결 임계치 {dso.get('voting_threshold')})")
    lines.append(f"  최신 라운드    : {latest}")

    code, cr = get("/closed-rounds")
    rounds = cr.get("rounds", cr) if isinstance(cr, dict) else cr
    n_closed = len(rounds) if isinstance(rounds, list) else 0
    lines.append(f"  닫힌 라운드    : {n_closed}" + ("" if n_closed else "  (아직 결산 전 — 잔액 통계 비어있음)"))

    # 총 잔액: 최신부터 0까지 내려가며 첫 성공값
    bal = None
    if isinstance(latest, int):
        for r in range(latest, -1, -1):
            code, b = get(f"/total-amulet-balance?asOfEndOfRound={r}")
            if code == 200 and b:
                bal = (r, b); break
    if bal:
        lines.append(f"  총 CC(Amulet) : round {bal[0]} 기준 {json.dumps(bal[1])[:60]}")
    else:
        lines.append(f"  총 CC(Amulet) : (집계 전 — 닫힌 라운드 생기면 표시)")

    lines.append("  " + "─" * 52)
    code, act = get("/activities", method="POST", body={"page_size": 10})
    acts = act.get("activities", []) if isinstance(act, dict) else []
    lines.append(f"  최근 활동 (최신 {len(acts)}):")
    for a in acts:
        t = a.get("activity_type", "?")
        rnd = a.get("round", "?")
        ts = hhmmss(a.get("date", ""))
        label = {"devnet_tap": "Tap(무료CC)", "transfer": "Transfer", "mint": "Mint(발행)"}.get(t, t)
        if a.get("tap"):
            tap = a["tap"]
            who = short(tap.get("amulet_owner"))
            head = f"    [{ts}] {label:<12} round {str(rnd):<3} {who}"
            lines.append(head)
            lines.append(f"             +{cc(tap.get('amulet_amount',0))} CC 무료 수령")
        elif a.get("transfer"):
            tr = a["transfer"]; s = tr.get("sender", {})
            who = short(s.get("party"))
            recvs = tr.get("receivers", []) or []
            head = f"    [{ts}] {label:<12} round {str(rnd):<3} {who}"
            lines.append(head)
            # 보상 수령(self) vs 실제 송금 구분
            reward = float(s.get("input_validator_reward_amount", 0) or 0)
            faucet = float(s.get("input_validator_faucet_amount", 0) or 0)
            change = s.get("sender_change_amount", 0)
            fee = float(s.get("sender_fee", 0) or 0) + float(s.get("holding_fees", 0) or 0)
            parts = []
            if reward: parts.append(f"밸리데이터보상 +{cc(reward)}")
            if faucet: parts.append(f"faucet +{cc(faucet)}")
            if recvs:
                tgt = ", ".join(f"{short(r.get('party'))} {cc(r.get('amount'))}CC" for r in recvs[:3])
                parts.append(f"→ {tgt}")
            parts.append(f"잔액 {cc(change)} CC")
            if fee: parts.append(f"수수료 {cc(fee)}")
            lines.append("             " + " · ".join(parts))
        else:
            lines.append(f"    [{ts}] {label:<12} round {str(rnd):<3}")
    if not acts:
        lines.append("    (활동 없음)")
    return "\n".join(lines)

if __name__ == "__main__":
    print(render())
