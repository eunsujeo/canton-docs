# 데모 계획 — LocalNet 라이브 정산 + 원장 기록 + 프라이버시

> 목표: **LocalNet에서 DvP 정산이 실제로 진행되는 걸 웹/앱으로 보여주고, 원장에 어떻게 남는지, 그리고 "다른 Party는 못 본다(프라이버시)"를 시연.**
> ⚠️ 대외비 — 위키엔 넣지 않음. 기반: [settlement 패키지](../daml/settlement/README.md)(테스트 통과), [remote-setup-plan](remote-setup-plan.md).

## 목표 3가지
1. **라이브 진행**: 제안→수락→할당→실행이 실제 LocalNet 원장에서 도는 걸 화면으로.
2. **원장 기록**: 각 컨트랙트가 원장에 어떤 구조로 남는지(payload) 표시.
3. **프라이버시(하이라이트)**: 거래 당사자만 보고, **무관한 Party는 아무것도 못 본다**를 눈으로.

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

## 아키텍처
```
LocalNet (참여자 노드 + JSON Ledger API v2)
        │  파티별 토큰으로 query/submit
   백엔드(thin) — 파티별 인증 토큰 보관, REST/SSE 노출
        │
   프론트(웹) — 파티 패널 4개 + 시나리오 버튼 + 라이브 폴링
```

## 단계별 계획 (빠른 성과 우선)

### Phase 0 — LocalNet 준비
- [ ] `make start`로 LocalNet 재기동.
- [ ] settlement DAR을 LocalNet 참여자에 업로드(또는 quickstart 빌드에 포함).
- [ ] 파티 준비: **instA=app-user, instB=app-provider**(이미 온보딩·CC 보유 재사용), **venue=별도 할당**, **outsider=별도 할당**(스테이크 없음).
- [ ] 각 기관 Amulet 자금 확인(tap).

### Phase 1 — 프라이버시 "빠른 증명" (CLI, UI 전)
- [ ] 파티별 토큰으로 Ledger API `active-contracts` 조회하는 스크립트.
- [ ] 정산 1건 만든 뒤 **A/B/venue/outsider 각각 조회** → "outsider엔 안 보임" 텍스트로 증명.
- [ ] (scan-status.py 확장 또는 새 cli) — **가장 빠른 가치 확인 지점.**

### Phase 2 — 정산을 LocalNet에서 구동
- [ ] propose→accept→allocate→execute를 LocalNet 원장에서 실행.
  - 처음엔 Canton Console / Daml Script(LocalNet 대상)로, 이후 백엔드 호출로.
- [ ] 각 단계 후 원장 상태(파티별)가 바뀌는 것 확인.

### Phase 3 — 웹 데모 (핵심 산출물)
- [ ] thin 백엔드: 파티별 토큰으로 `GET active-contracts` + `POST submit`(제안/수락/할당/실행).
- [ ] 프론트: **파티 패널 4개**(A/B/venue/outsider) 각자 자기 뷰 폴링 + **시나리오 버튼** + 컨트랙트 payload 표시.
- [ ] 프라이버시 콜아웃: outsider 패널 강조("못 봄").

### Phase 4 — 폴리시
- [ ] 단계 내러티브(설명 텍스트), 원장 레코드 JSON 보기, 통화 2종(KRW/JPY) 분리(선택).

## 핵심 결정사항
| 항목 | 방향(잠정) |
|---|---|
| Ledger API | **JSON API v2**(웹 친화, Swagger `:9090` 있음). gRPC 아님 |
| 인증/토큰 | LocalNet shared-secret 모드 **파티별 토큰** — 발급법 조사 필요(cn-quickstart 백엔드가 이미 함 → 참고) |
| 백엔드 | **새 thin 백엔드**(Node/FastAPI, 읽기 위주) 추천. 액션은 처음엔 Script/Console → 점진적으로 백엔드로 |
| 파티 | instA=app-user, instB=app-provider(재사용), venue·outsider=신규 할당 |
| 통화 | 현재 Amulet 1종으로 데모(충분), 추후 2종 |
| 프론트 | 정적 단일 HTML(현 대시보드 스타일) + fetch, 또는 가벼운 프레임워크 |

## 리스크 / 조사 필요
- [ ] **파티별 토큰 발급**(shared-secret) 구체 방법 — 데모 성패의 핵심.
- [ ] LocalNet에 **커스텀 DAR 업로드 + 파티 할당** 절차.
- [ ] **외부자가 정말 0개 보이는지** — 참여자 노드 호스팅 구조에 따라(외부자를 어느 노드가 호스팅하나). 별도 참여자/파티로 깔끔히 분리 필요.
- [ ] JSON Ledger API v2의 active-contracts/submit 사용법(Swagger로 확인).

## 관련
- [settlement 패키지·테스트](../daml/settlement/README.md) · [DvP 흐름 대시보드](../dvp-flow-dashboard.html)(정적 설명용)
- [roadmap](roadmap.md) Phase 3·4 · [remote-setup-plan](remote-setup-plan.md)
- 프라이버시 개념: 위키 [프라이버시 모델](../../wiki/overview/learn/privacy-model.md) · [원자적 DvP 차별점](../../wiki/notes/atomic-dvp-real-differentiator.md)
