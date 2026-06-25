# PoC 아키텍처 메모 (단기)

> 단기 PoC의 구성요소·데이터 흐름·신뢰 지점. 우리는 **적격기관(국내은행)** 입장에서 무스비에 연결해 정산을 수행한다.
> 환경: **DevNet 또는 TestNet**(LocalNet 검증은 완료) · 인프라: **AWS Sandbox**.
> 관련: 무스비 제품/SDK는 [musubi-overview.md](musubi-overview.md), 노드인프라에 요청할 것은 [nodeinfra-asks.md](nodeinfra-asks.md), AWS/네트워크 진행은 [aws-sandbox-devnet-setup.md](aws-sandbox-devnet-setup.md).

## 0. 큰 그림 — 계층 분담

```
[B2C] 일반유저 ↔ 스테이블코인      → 퍼블릭 체인 (Base/Ethereum)   ← PoC 범위 밖
[B2B] 적격기관 ↔ 적격기관 정산(DvP)  → Canton (무스비)              ← 이 PoC
```

- **Canton(무스비)은 B2B 기관 간 정산 전용** — 통화↔통화 원자적 DvP, 거래 상대·금액 프라이버시.
- **단기 PoC는 B2B 정산만** 다룬다 — 고객·Fiat 온오프램프·브릿지 제외.

## 1. DvP (Delivery versus Payment)

정산 = 거래 약속을 실제 자산 이동으로 마무리하는 단계. 문제는 *누가 먼저 보내나* — 국내은행이 KRWK를 먼저 보냈는데 상대가 JPYC를 안 보내면 떼인다(**카운터파티/Herstatt 리스크**).

**DvP**: 양 통화를 한 트랜잭션에 동시에 교환 → **전부 성공 or 전부 무효**. 한쪽만 가는 일이 구조적으로 불가능. 이게 무스비를 B2B 정산에 쓰는 핵심 이유다.

## 2. 무스비 구성요소 (역할)

| 구성요소 | 무엇 | 단기 PoC에서 우리(국내은행) |
|---|---|---|
| **Core(무스비)** | 정산 코디네이터 — DAML 컨트랙트(`FXOrder`), 4-leg 원자 정산 개시·실행 | 무스비/노드인프라가 운영 |
| **Institution** | 송금 개시, 견적(RFQ) 비교·선택 | **우리 역할(송신측)** |
| **Custodian** | 자산 이동 승인·co-sign, 감사추적 | 우리가 Custodian 역할 · 지갑은 **노드월렛**(네이티브 파티 호스팅, 키 HSM/망분리) |
| **Market Maker** | 익명 RFQ에 호가, 유동성 공급. 4-leg 필수 참여자 | PoC용 테스트 MM은 무스비/노드인프라 준비 |
| **Gateway** | TradFi 통합(fiat·온오프램프·온보딩) | 단기 PoC 범위 밖 |

> 무스비 정산은 **4-leg / 4 confirming party**(송신 커스터디언·MM·Core·수신 커스터디언). 상세 [musubi-overview.md](musubi-overview.md) §3.

## 3. 단기 PoC 아키텍처 (AWS Sandbox + DevNet/TestNet)

```
┌─ AWS Sandbox (우리, 망분리 격리 환경) ──────────────────────────┐
│  Canton Participant Node          (우리 Party ID)              │
│  노드월렛 (네이티브 파티 호스팅 + 키 HSM/망분리)  ← 지갑/커스터디 │
│  Musubi Backend (REST+SSE)        (role: 송신측)               │
│  PostgreSQL                                                    │
└───────────────────────────┬─────────────── mTLS ───────────────┘
                            ▼
        ┌──────────── 무스비 정산 네트워크 (DevNet 또는 TestNet) ────────────┐
        │  Synchronizer(시퀀서) · 스폰서 SV · Core(코디네이터)               │
        │  카운터파티(일본은행 그룹) · Market Maker  ← 무스비/노드인프라 준비    │
        └──────────────────────────────────────────────────────────────────┘
```

- **AWS Sandbox = 망분리 때문에 쓴다** — 은행 내부망 밖 격리 환경에서 **우리 스택을 전부** 띄운다. 국내은행 내부 시스템 연동 최소화. 진행 방식 [aws-sandbox-devnet-setup.md](aws-sandbox-devnet-setup.md).
- **노드월렛 = 지갑/커스터디 컴포넌트** — 노드인프라 제공 SW. 캔톤 노드에 우리 파티를 **네이티브로 호스팅** + 키 HSM/망분리. Fireblocks(옴니버스)의 대안 — 최종 PoC의 Fireblocks 자리를 단기엔 노드월렛이 채운다.
- **footprint**: participant + 노드월렛 + Musubi backend + Postgres, 정산 네트워크로 mTLS.
- **프로비저닝**: 노드인프라/무스비가 **Party ID · JWT · 엔드포인트/TLS · 노드월렛 SW·배포물** 제공.
- **대부분 무스비/노드인프라 준비**: 카운터파티·MM·Core·네트워크는 무스비 측. 우리는 AWS Sandbox에 송신측 스택을 띄워 연결.

### 프라이버시의 근거 (Canton 메커니즘)

각 참여자 노드는 **자기 파티가 이해관계자인 컨트랙트만 보유**한다 → 무관한 제3자는 거래를 데이터로 갖고 있지도 않다. RFQ도 MM에 **익명**으로 가 송수신자 신원이 노출되지 않는다.

## 4. 정산 데이터 흐름 (4-leg)

```mermaid
sequenceDiagram
    autonumber
    participant I as 국내은행 (송신 Institution)
    participant SC as 송신 Custodian
    participant V as 무스비 (Core)
    participant MM as Market Maker
    participant RC as 수신 Custodian
    participant R as 일본은행 그룹 (수신)
    I->>V: FX order 생성 (KRWK→JPYC, 금액, cost guard)
    V->>MM: 익명 견적요청 (통화쌍·금액·만료만)
    MM-->>V: 경쟁 견적 (환율·목표금액·유효기간)
    V-->>I: 견적 제시
    I->>V: best 견적 수락 (QUOTED, cost guard 검증)
    Note over SC,RC: 원자적 DvP (EXECUTING) — 단일 트랜잭션 4 leg
    SC->>V: KRWK (source)
    MM->>V: JPYC (target)
    V->>RC: JPYC (target) → 일본은행 그룹
    V->>MM: KRWK (source)
    Note over I,R: 한 leg라도 실패하면 전체 롤백 → SETTLED + 트랜잭션 해시 1개
```

상태(`FXOrder`): `PENDING` → `QUOTED` → `EXECUTING` → `SETTLED` (실패: `FAILED`/`EXPIRED`). 단계·합격 기준은 [short-term-scenario.md](short-term-scenario.md).

## 5. 단계별 진화 (단기 → 최종)

| 축 | 단기 PoC (올해) | 최종 PoC (내년) |
|---|---|---|
| 환경 | **DevNet/TestNet**, AWS Sandbox | 망분리 검토 + 국내은행 지갑 시스템 연동 |
| 통화 | KRWK ↔ JPYC (테스트 인스트루먼트) | 실제 발행 인스트루먼트 |
| 당사자 | 은행 자기계정 (고객 없음) | 국내은행 유저(고객) 온/오프램프 |
| 지갑/커스터디 | **노드월렛**(네이티브 파티 호스팅, HSM/망분리) | **Fireblocks**(국내은행 지갑 시스템) |
| Fiat | 없음 | (가능성) 온/오프램프 |
| MM/유동성 | 무스비 준비(테스트 MM) | MM 구조 확정(비즈니스 협의) |

> Fireblocks(Raw Signing) 등 최종 PoC 지갑/커스터디 논의는 `dev/docs/wallet-custody-fireblocks.md`에 별도 정리되어 있다(단기 범위 밖).

## 6. 신뢰 지점 (어디를 믿어야 하나)

- **정산 자체**: 원자성·프라이버시가 원장 메커니즘으로 보장. Core(무스비)는 코디네이션·실행만 하고, 4-leg co-sign으로 단일 주체가 자산을 일방 이동 못 함.
- **네트워크 연결**: mTLS + JWT(무스비 발급). 스폰서 SV·allowlist를 통해 DevNet/TestNet에 온보딩.
- **키 보관(단기)**: AWS Sandbox의 **노드월렛**(네이티브 파티 호스팅, HSM/망분리)이 파티 키를 보관·서명. 키 HSM 관리 주체는 확인 대상. 최종 단계에서 Fireblocks로 이동.

## 7. 결론 — 단기 PoC의 메시지

단기 PoC는 **무스비 정산 한 건을 DevNet/TestNet에서 적격기관으로서 직접 수행**해, (1) 원자적 DvP, (2) 프라이버시(익명 RFQ·부분 트랜잭션), (3) Synchronizer 활동을 확인하는 것이 목표다. 고객·Fiat·Fireblocks는 최종 PoC로 미루고, 단기엔 "캔톤/무스비가 기관 간 정산을 어떻게 안전하게 끝내는가"를 이해하는 데 집중한다.
</content>
