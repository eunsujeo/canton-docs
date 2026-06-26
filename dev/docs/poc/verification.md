# 검증 항목 — 가치 · 방법 · 검증 가능성 · 합격 기준

> 1차 PoC의 핵심: 무스비/캔톤을 **왜 쓰는지(가치)** 를 항목별로 **검증**한다.
> 각 항목 = 가치(why) → 검증 방법(how, 어떤 인터페이스로 무엇을 보나) → **검증 가능성**(1차 환경에서 실제로 가능한가) → 합격 기준(pass).
> 시나리오: 국내은행 KRWK ↔ 해외은행 JPYC, 무스비 4-leg 원자 정산(고객 없음). 모델 [musubi-overview.md](musubi-overview.md), 구성 [architecture.md](architecture.md).

## 0. 국내은행이 가진 관측 수단 (검증 가능성의 전제)

1차 PoC에서 국내은행이 직접 볼 수 있는 것:

- **무스비 API / Console / Statements** — 주문·견적·정산 상태, 대시보드(`/api/v1/dashboard/stats`), 정산 확인서·트랜잭션 해시.
- **국내은행 Canton participant 원장(노드월렛)** — 국내은행 파티 뷰의 활성 컨트랙트(ACS)·FXOrder 상태·allocation·잔액·커밋 오프셋.
- **국내은행 KRWK 잔액** — 국내은행이 통제 → 실패 주입(잔액 부족 등) 가능.

직접 볼 수 **없는** 것(노드인프라/무스비 측):

- MM·수신 카운터파티·제3자(무관) 노드의 원장 뷰.
- 무스비 Core 내부 동작.

→ 따라서 **MM에 무엇이 보이나·제3자가 못 보나·DAML이 원장에서 강제하나**는 국내은행 뷰만으로는 부분적이며, 노드인프라 지원(제3자 노드 뷰·raw Ledger API·패키지)이 있어야 완전 검증된다. 아래 "검증 가능성"에 표시.

| # | 항목 | 검증 가능성 (1차) | 비고 |
|---|---|---|---|
| 1 | 원자적 DvP | **가능** | 정상+실패주입 모두 국내은행 뷰로 |
| 2 | 익명/프라이버시 | **제한적** | 국내은행 뷰는 가능, MM익명·제3자0건은 외부 뷰 필요 |
| 3 | 무스비 기능 정상동작 | **가능** | API/Console end-to-end |
| 4 | DAML 검증 | **제한적** | 상태·국내은행 권한 가능, 원장 강제 확인엔 raw Ledger API |
| 5 | 캔톤 이해 | **가능** | 국내은행 participant 원장·오프셋 |

---

## 1. 원자적 DvP — 검증 가능성: 가능

- **가치**: 국내은행이 KRWK를 먼저 보내고 해외은행이 JPYC를 안 보내는 카운터파티(Herstatt) 리스크를 구조적으로 제거.
- **검증 방법**:
  - 정상 정산 1건 실행 → 국내은행 원장(ACS·잔액)에서 **KRWK 차감과 JPYC 입금이 같은 트랜잭션(같은 오프셋)** 에 일어나는지 확인 + Console/Statements에서 **트랜잭션 해시 1개**(4 leg를 덮는 단일 캔톤 트랜잭션 해시) 확인.
  - 실패 주입: 국내은행 KRWK **잔액을 부족하게** 한 뒤 정산 시도 → 국내은행 leg 실패 → **전체 롤백**(잔액 무변동, FXOrder `FAILED`) 확인.
- **검증 가능성**: **가능** — 국내은행 leg(KRWK)는 국내은행이 통제하므로 정상·실패 모두 국내은행 뷰로 관측. (상대/MM leg 실패 주입은 노드인프라 협조 필요하나, 원자성 입증엔 국내은행 leg 실패로 충분.)
- **합격 기준**:
  - [ ] SETTLED 시 KRWK↓·JPYC↑가 단일 트랜잭션에 동시 반영.
  - [ ] 국내은행 leg 실패 시 전체 롤백(부분 정산 없음, FAILED).

## 2. 익명 / 프라이버시 — 검증 가능성: 제한적

- **가치**: 거래 상대·금액·환율이 무관한 제3자에 비공개, MM도 송수신자 신원을 모름.
- **검증 방법**:
  - (국내은행 뷰) 국내은행 participant ACS에 **국내은행이 이해관계자인 컨트랙트만** 있는지 확인.
  - (FXOrder observer) 국내은행 FXOrder 컨트랙트의 **관찰자 집합**이 당사자+MM(견적 수락 후)로 한정되는지 확인.
  - (MM 익명) MM에 전달되는 RFQ 페이로드에 **신원 미포함**(통화쌍·금액·만료만)인지 — MM 측 뷰 또는 데이터 모델로 확인.
  - (제3자 0건) **무관한 제3자 노드** 뷰에서 이 거래 컨트랙트가 0건인지 확인.
- **검증 가능성**: **제한적** —
  - *가능*: 국내은행 뷰가 국내은행 컨트랙트만 보유함은 국내은행 participant로 직접 확인.
  - *외부 필요*: **MM 익명**은 MM 측 뷰/스키마, **제3자 0건**은 거래에 무관한 노드 뷰가 있어야 입증 → 노드인프라가 제3자(비당사자) 노드 뷰 또는 RFQ 스키마를 제공해야 완전 검증([nodeinfra-asks.md](nodeinfra-asks.md) G).
- **합격 기준**:
  - [ ] 국내은행 participant ACS = 국내은행 거래만(무관 컨트랙트 없음).
  - [ ] (외부 뷰 확보 시) 제3자 노드에 이 거래 0건.
  - [ ] (확보 시) MM RFQ에 송수신 신원 미포함.

## 3. 무스비 기능 정상 동작 — 검증 가능성: 가능

- **가치**: 무스비 정산 레일(주문·RFQ·4-leg 정산)이 실제 네트워크에서 작동.
- **검증 방법**:
  - API/Console로 FX order 생성 → MM 경쟁 견적 → best 견적 수락 → 4-leg 정산 → SETTLED, end-to-end 1회. SSE로 상태 전이 실시간 관측.
  - cost guard(최악 환율 한도) 설정 후 한도 벗어난 견적 거부 확인.
  - 소요 시간 측정(~15초), Statements에서 정산 확인서·해시 조회.
- **검증 가능성**: **가능** — 전부 국내은행이 호출/관측하는 무스비 API·Console로 확인.
- **합격 기준**:
  - [ ] 주문→견적→정산 전 과정 완료(~15초 목표).
  - [ ] SETTLED + 트랜잭션 해시 1개.
  - [ ] cost guard 위반 견적 거부.

## 4. DAML 검증 — 검증 가능성: 제한적

- **가치**: 정산 컨트랙트(`FXOrder`) 로직·권한이 **앱이 아니라 원장에서** 강제됨.
- **검증 방법**:
  - (상태) FXOrder 상태가 `PENDING→QUOTED→EXECUTING→SETTLED`(실패 `FAILED`/`EXPIRED`) 경로로만 진행하는지 국내은행 원장·API로 관측.
  - (권한·거부) 잘못된 호출 거부 확인: 견적 수락 전 정산 시도, 만료 후 실행, 기대 allocation 불일치 등.
  - (원장 강제) 위 거부가 **무스비 백엔드 검증이 아니라 DAML 컨트랙트(원장)** 에서 막히는지 확인하려면 국내은행 participant의 **raw Ledger API로 직접 명령 제출**(백엔드 우회)해 보아야 함.
- **검증 가능성**: **제한적** —
  - *가능*: 상태 전이·정상 권한 흐름은 API/국내은행 원장으로 확인.
  - *외부/추가 필요*: "원장이 강제" 입증은 raw Ledger API 접근 + 패키지/DAR(`FXOrder` package id) 지식이 있어야 함([nodeinfra-asks.md](nodeinfra-asks.md) C·G). 없으면 "API 단 검증"까지만.
- **합격 기준**:
  - [ ] 상태 전이가 정의된 경로로만 진행.
  - [ ] 순서 위반/권한 없는 호출 거부.
  - [ ] (raw Ledger 접근 시) 거부가 원장 단에서 강제됨을 확인.

## 5. 캔톤 이해 — 검증 가능성: 가능

- **가치**: 팀이 캔톤 핵심 개념을 실물로 체득.
- **검증 방법**:
  - 국내은행 participant 원장 뷰(ACS)로 부분 트랜잭션 프라이버시 체감(자기 view만).
  - 커밋 오프셋(`ledger-end`) 변화·Synchronizer 활동 관찰 → 순서 확정·전달 이해.
  - 정산 1건의 트랜잭션 트리로 2계층 합의 흐름 확인.
- **검증 가능성**: **가능** — 국내은행 participant만으로 관측.
- **합격 기준**:
  - [ ] 파티/뷰·2계층 합의·Synchronizer를 데모로 설명 가능.

---

## 6. 정산 시나리오 (검증을 돌리는 흐름)

```mermaid
sequenceDiagram
    autonumber
    participant I as 국내은행 (송신 Institution)
    participant SC as 송신 Custodian (국내은행, 노드월렛)
    participant V as 무스비 Core
    participant MM as Market Maker
    participant RC as 수신 Custodian (해외은행)
    Note over I,RC: 모든 메시지는 Canton Synchronizer(시퀀서) 경유 — 아래는 논리 흐름
    I->>V: 1. FX order 생성 (KRWK→JPYC, 금액, cost guard)
    V-->>I: intentId 발급 (이 주문의 식별자)
    Note over I,V: 이후 상태는 SSE(intent_id 필터)로 실시간 수신
    V->>MM: 2. 익명 견적요청 (통화쌍·금액·만료만)
    MM-->>V: 3. 경쟁 견적 (각 quoteId)
    V-->>I: 견적 제시 (intentId · quoteId 목록)
    I->>V: 4. best 견적 수락 (intentId + quoteId, QUOTED, cost guard 검증)
    Note over SC,RC: 5. 원자적 DvP (EXECUTING) — 단일 트랜잭션 4 leg
    SC->>V: KRWK (source)
    MM->>V: JPYC (target)
    V->>RC: JPYC (target) → 해외은행
    V->>MM: KRWK (source)
    Note over I,RC: 6. SETTLED (intentId) → txHash (4 leg 단일 트랜잭션 해시 = 정산 증빙)
```

> 트랜잭션 해시 1개 = 4 leg를 덮는 단일 캔톤 트랜잭션 해시(규제 보고용 증빙). 각 단계가 검증 항목과 연결: 5=원자성(1), RFQ 2=익명(2), 전 과정=기능(3), 상태·권한=DAML(4).

## 7. 검증 전제 — 노드인프라에 요청할 것

"제한적" 항목을 완전 검증하려면 다음이 필요(→ [nodeinfra-asks.md](nodeinfra-asks.md) G):

- **제3자(비당사자) 노드 뷰** — 프라이버시 "제3자 0건" 시연용.
- **MM 측 RFQ 페이로드/스키마** — MM 익명 확인용.
- **raw Ledger API 접근 + `FXOrder` 패키지/DAR id** — DAML 원장 강제 확인용.
- **실패 주입 협조** — 상대/MM leg 실패 케이스까지 보려면(국내은행 leg 실패만으론 국내은행 측 롤백까지).

## 8. 추가 검증 후보 (필요 시)

- **결정적 확정(Finality)** — 캔톤은 즉시 확정(reorg 없음). SETTLED 후 되돌릴 수 없음을 확인(기존 결제 방식 대비 강점).
- **감사추적/증빙** — Statements의 정산 확인서·단일 해시로 거래를 단일 증빙으로 재구성 가능한지.
- **재시도/멱등성** — 동일 주문 재제출·중복 방지(`intentId`) 동작.

## 9. 범위 밖 (1차 제외)

- Fireblocks(외부 지갑) 실연동 — 최종 PoC. 비교만 [wallet-comparison.md](wallet-comparison.md).
- 고객·Fiat 온/오프램프·브릿지, MM 구조 확정(비즈니스 협의), 통화 USD 경유.

## 참고 (출처)

- 정산 흐름·상태: https://musubinetwork.com/how-it-works
- FXOrder 상태·서명자: https://musubinetwork.com/technical/fxorder
- API 인증(`/whoami` 등): https://musubinetwork.com/authentication
- API 규약(SSE·`dashboard/stats`): https://musubinetwork.com/api-conventions
- 프라이버시 모델: https://musubinetwork.com/compliance/privacy
- Canton Network 문서(프라이버시·확정성): https://docs.canton.network
