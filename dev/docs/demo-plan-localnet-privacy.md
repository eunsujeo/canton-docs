# 데모 계획 — LocalNet 라이브 정산 + 원장 기록 + 프라이버시

> 목표: **LocalNet에서 DvP 정산이 실제로 진행되는 걸 웹/앱으로 보여주고, 원장에 어떻게 남는지, 그리고 "다른 Party는 못 본다(프라이버시)"를 시연.**
> 기반: [settlement 패키지](../daml/settlement/README.md)(테스트 통과), [remote-setup-plan](remote-setup-plan.md). (dev 문서 — 위키와는 분리)

## 목표 3가지
1. **라이브 진행**: 제안→수락→할당→실행이 실제 LocalNet 원장에서 도는 걸 화면으로.
2. **원장 기록**: 각 컨트랙트가 원장에 어떤 구조로 남는지(payload·create/archive 이력) 표시.
3. **프라이버시(하이라이트)**: 거래 당사자만 보고, **무관한 Party는 아무것도 못 본다**를 눈으로.

## 청중·목적·성공 기준 (먼저 정할 것)
- [ ] **청중**: 누구에게? (개발자 / 비즈니스 / 파트너 기관) → 깊이·언어(한/영) 결정.
- [ ] **목적**: 기술 검증(PoC 작동) vs 설득(왜 Canton/DvP) — 무게중심.
- **성공 기준 (이게 되면 데모 성공)**:
  1. 정산이 **라이브로 한 트랜잭션에** 끝나는 걸 보여줌.
  2. **외부자 패널이 비어** "남은 못 본다"가 명확.
  3. (강력) **한쪽 불이행 시 아무것도 안 움직임**(원자성) 시연.

## 🎯 데모의 심장 = 멀티 파티 뷰 (프라이버시)
**같은 원장**을 각 파티의 토큰으로 조회 → **보이는 게 다르다**.
```
┌ 기관A 패널 ┐ ┌ 기관B 패널 ┐ ┌ venue 패널 ┐ ┌ 외부자(outsider) 패널 ┐
│ Settlement │ │ Settlement │ │ Settlement │ │   (텅 빔)              │
│ +내 할당   │ │ +내 할당   │ │            │ │  "이 거래를 못 봄"     │
└────────────┘ └────────────┘ └────────────┘ └───────────────────────┘
```
- 정산을 돌리면 A·B·venue 패널엔 컨트랙트가 뜨고, **외부자 패널은 빈 채** → "C는 A·B의 거래를 못 본다" 가 즉시 증명.
- 부분 프라이버시: A는 B의 잔액/할당 내부를 못 봄(자기 leg만).

## 🎯 두 번째 하이라이트 = 원자성(실패·롤백 시연)
"전부 or 전무"를 보여주는 가장 강력한 장면 (프라이버시만큼 중요):
- **시나리오 A(실패)**: 기관A만 할당, 기관B 미할당 → venue가 Execute 시도 → **실패, 어떤 자산도 안 움직임**.
- **시나리오 B(취소)**: 정산 전 `Settlement_Cancel` → 잠긴 자산 **원위치**.
- 메시지: "갱신만 되고 결제 안 됨 / 한쪽만 빠짐"이 **구조적으로 불가능** = **카운터파티 리스크 0**.

## 데모 대본 (내러티브 — 클릭하며 할 이야기)
1. "기관A·B가 통화 맞교환(FX). 기존엔 한쪽이 먼저 보내면 떼일 위험(카운터파티 리스크)."
2. A가 제안 → B·venue 패널에 등장, **외부자 C 패널은 빈 채**("C는 거래 존재조차 모름").
3. B 수락 → 양측 자산 잠금(할당).
4. venue Execute → **양 통화가 한 번에** 이동. 원장 기록(payload) 펼쳐 보기.
5. (반전) **실패 시연**: 한쪽 미할당 → 실행 실패, 자산 그대로.
6. 마무리: "**당사자만 보고(프라이버시) + 동시·전부/전무로 정산(원자성) → 떼일 위험 없음.**"

## 아키텍처
```
LocalNet (참여자 노드 + JSON Ledger API v2)
        │  파티별 토큰으로 query/submit + 업데이트 스트림 구독
   백엔드(thin) — 파티별 토큰 보관, REST(제출) + SSE(실시간 푸시)
        │  SSE/WebSocket (새로고침 불필요)
   프론트(웹) — 파티 패널 4개, 변경 즉시 자동 갱신
```

### 실시간 갱신 (새로고침 불필요) — 요구사항
- 패널은 **새로고침 없이** 원장 변화에 따라 자동 갱신.
- 방식(추천): 백엔드가 **Ledger API 업데이트 스트림을 파티별 구독** → **SSE로 프론트 푸시**. (cn-quickstart 라이선스 UI가 같은 패턴 — "Action Needed" 새로고침 없이 등장)
- 폴백: 1~2초 **폴링**(스트림 까다로우면).
- 효과: A가 제안하면 B·venue 패널에 **즉시** 뜨고 외부자 패널은 계속 빈 채 → "실시간으로 남은 못 본다".

## 어디에 만드나 (위치)
**`canton/dev/demo/`** (새 폴더, 추적됨) — 우리 데모 앱. cn-quickstart(gitignore)와 분리, 네트워크로 LocalNet에 연결.
```
canton/dev/
├─ daml/settlement, settlement-tests   # Daml 소스(추적, 기존)
├─ demo/                                # ⭐ 데모 앱(추적, 신규)
│  ├─ backend/   # thin: Ledger API ↔ REST/SSE
│  └─ frontend/  # 파티 패널 4개, frontend-design
├─ docs/                                # 계획
├─ cn-quickstart/                       # gitignore — LocalNet 런타임
└─ *.html                               # 대시보드
```
- **demo/** = 추적되는 우리 코드. **cn-quickstart/** = LocalNet 띄우는 실행환경(클론). 데모는 LocalNet에 **HTTP(JSON Ledger API)로 붙음**.
- settlement **DAR**은 cn-quickstart 빌드에서 LocalNet에 업로드.
- Phase 1의 CLI(빠른 증명)는 `dev/demo/cli/` 또는 기존 `dev/scan-status.py` 옆에 둬도 됨.

## 단계별 계획 (빠른 성과 우선)

### Phase 0 — LocalNet 준비
- [ ] `make start`로 LocalNet 재기동.
- [ ] settlement DAR을 LocalNet 참여자에 업로드(또는 quickstart 빌드에 포함).
- [ ] 파티 준비: **instA=app-user, instB=app-provider**(이미 온보딩·CC 보유 재사용), **venue=별도 할당**, **outsider=별도 할당**(스테이크 없음).
- [ ] 각 기관 Amulet 자금 확인(tap).

### Phase 1 — 프라이버시 "빠른 증명" (CLI) ✅ 완료
- [ ] 파티별 토큰으로 Ledger API `active-contracts` 조회하는 스크립트.
- [ ] 정산 1건 만든 뒤 **A/B/venue/outsider 각각 조회** → "outsider엔 안 보임" 텍스트로 증명.
- [ ] (scan-status.py 확장 또는 새 cli) — **가장 빠른 가치 확인 지점.**

### Phase 2 — 정산을 LocalNet에서 구동
- [ ] propose→accept→allocate→execute를 LocalNet 원장에서 실행.
  - 처음엔 Canton Console / Daml Script(LocalNet 대상)로, 이후 백엔드 호출로.
- [ ] 각 단계 후 원장 상태(파티별)가 바뀌는 것 확인.

### Phase 3 — 웹 데모 (핵심 산출물)
- [ ] thin 백엔드: 파티별 토큰으로 `GET active-contracts` + `POST submit`(제안/수락/할당/실행).
- [ ] 프론트: **파티 패널 4개**(A/B/venue/outsider) 각자 자기 뷰 + **시나리오 버튼** + 컨트랙트 payload 표시.
- [ ] **실시간 갱신(새로고침 불필요)**: 백엔드 SSE 푸시(또는 폴링 폴백) → 변경 즉시 패널 자동 반영.
- [ ] 프라이버시 콜아웃: outsider 패널 강조("못 봄").
- [ ] **디자인: `frontend-design` 스킬 적용** — 발표·공유용이라 "안전한 다크 기본값"이 아니라 의도적·차별화된 룩으로(타이포·색·레이아웃). (UI 만들 때 이 스킬 먼저 호출)

### Phase 3.5 — 실패·롤백 시연 추가 (원자성)
- [ ] "한쪽만 할당" 상태에서 Execute 실패 보여주기(자산 불변 확인).
- [ ] `Settlement_Cancel` 버튼 → 잠긴 자산 원위치 확인.

### Phase 4 — 폴리시
- [ ] 단계 내러티브(설명 텍스트), 원장 레코드 JSON·이력 보기, 통화 2종(KRW/JPY) 분리(선택).

## 운영 준비 (시연 안정성)
- [ ] **반복 시연**: 리셋 스크립트(파티·자금·정산 초기화; `make clean-all`→`start` 또는 새 정산 id) — 여러 번 시연 가능하게.
- [ ] **트래픽 준비**: 각 파티가 submit하려면 트래픽 필요 → 데모 전 tap/충전 확인(없으면 거래 실패).
- [ ] **장소**: 대면(로컬 시연) vs 원격(공유 URL). 원격이면 [remote-setup-plan](remote-setup-plan.md) 옵션 A(VM) 필요.
- [ ] **백업**: 라이브 실패 대비 녹화/스크린샷 미리 확보.

## 핵심 결정사항
| 항목 | 방향(잠정) |
|---|---|
| Ledger API | **JSON API v2**(웹 친화, Swagger `:9090` 있음). gRPC 아님 |
| 인증/토큰 | LocalNet shared-secret 모드 **파티별 토큰** — 발급법 조사 필요(cn-quickstart 백엔드가 이미 함 → 참고) |
| 백엔드 | **새 thin 백엔드**(Node/FastAPI, 읽기 위주) 추천. 액션은 처음엔 Script/Console → 점진적으로 백엔드로 |
| 파티 | instA=app-user, instB=app-provider(재사용), venue·outsider=신규 할당 |
| 통화 | 현재 Amulet 1종으로 데모(충분), 추후 2종 |
| 프론트 | 정적 단일 HTML + fetch 또는 가벼운 프레임워크. **디자인은 `frontend-design` 스킬로**(제네릭 기본값 X) |

## 리스크 / 조사 필요
- [ ] **파티별 토큰 발급**(shared-secret) 구체 방법 — 데모 성패의 핵심.
- [ ] LocalNet에 **커스텀 DAR 업로드 + 파티 할당** 절차.
- [ ] **외부자가 정말 0개 보이는지** — 참여자 노드 호스팅 구조에 따라(외부자를 어느 노드가 호스팅하나). 별도 참여자/파티로 깔끔히 분리 필요.
- [ ] JSON Ledger API v2의 active-contracts/submit 사용법(Swagger로 확인).

## 관련
- [settlement 패키지·테스트](../daml/settlement/README.md) · [DvP 흐름 대시보드](../dvp-flow-dashboard.html)(정적 설명용)
- [roadmap](roadmap.md) Phase 3·4 · [remote-setup-plan](remote-setup-plan.md)
- 프라이버시 개념: 위키 [프라이버시 모델](../../wiki/overview/learn/privacy-model.md) · [원자적 DvP 차별점](../../wiki/notes/atomic-dvp-real-differentiator.md)
