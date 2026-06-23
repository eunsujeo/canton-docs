# 계획 — 실제 KRWK·JPY 스테이블코인으로 DvP 시연 (옵션 A)

> 목적: 현재 데모(legKRW·legJPY 모두 **Amulet 1종**)를 **별도의 두 토큰표준 인스트루먼트**(KRWK, JPY)로 바꿔
> "진짜 두 통화의 FX DvP"를 LocalNet에서 시연.
> ⚠️ 이 문서는 **계획만** — 실행/빌드 안 함. 관련: [데모 계획](demo-plan-localnet-privacy.md) · [demo/README](../demo/README.md)

## 0. 한 줄 요약 (왜 무거운가)
우리 **정산 컨트랙트(FxDvp)는 토큰 비종속**이라 Daml은 그대로 쓴다.
막는 건 **런타임 레지스트리** — 정산 실행이 토큰의 *오프레저 레지스트리 API*에 의존하는데
LocalNet엔 **Amulet용 레지스트리(Splice scan, `:4000`)만** 있다.
따라서 KRWK·JPY 각각에 **토큰표준 구현(Daml) + 레지스트리 앱(HTTP) + 발행자**를 새로 만들어야 한다.

---

## 1. 핵심 구조 — 우리 흐름이 레지스트리에 의존하는 지점
현재 백엔드(`dev/demo/backend/server.py`)에서 토큰에 묶인 곳:

| 단계 | 코드 | Amulet 종속성 |
|---|---|---|
| 제안 leg | `create_proposal()` `instrumentId={admin:DSO, id:"Amulet"}` | 인스트루먼트 ID 하드코딩 |
| 자산 잠금 | `allocate_for()` → 검증자 지갑 `POST /v0/allocations` | 지갑이 해당 토큰 allocation-instruction 지원 가정 |
| 잔액 | `balance_of()` → `/v0/wallet/balance` (Amulet 전용) | holding 집계가 Amulet 전용 |
| 실행 컨텍스트 | `registry_ctx()` → `POST :4000/registry/allocations/v1/{cid}/choice-contexts/execute-transfer` | **scan(Amulet 레지스트리) URL 하드코딩** |
| 실행 | `Settlement_Execute` + disclosedContracts | 레지스트리가 준 disclosed contracts 필요 |

토큰표준 5개 API (현재 Amulet이 광고하는 것, `/registry/metadata/v1/instruments`로 확인됨):
`metadata-v1`, `holding-v1`, `transfer-instruction-v1`, `allocation-v1`, `allocation-instruction-v1`.
새 토큰은 이 **5개 인터페이스를 Daml로 구현**하고, **오프레저 API**(`metadata/v1/*`, `allocations/v1/{cid}/choice-contexts/*`)를 HTTP로 제공해야 한다.

---

## 2. 먼저 정할 결정사항
1. **토큰 구현 방식**
   - (a) Splice **Amulet 코드를 포크/축약** → 가장 확실하나 코드량 많음.
   - (b) **최소 자체 구현** — Holding/Transfer/Allocation/AllocationInstruction 템플릿만 토큰표준 인터페이스 구현. 데모엔 충분, 권장.
   - (c) Splice가 제공하는 **레지스트리 레퍼런스/SDK**(있다면) 사용. → §9 확인 필요.
2. **발행 모델** (메모: KRWK·JPY는 Base/Ethereum 발행 → 브릿지)
   - (a) 데모 단순화: **Canton 네이티브 발행**(발행자 파티가 직접 민트). 가장 가벼움.
   - (b) 실제 아키 반영: **브릿지된 래핑 토큰**(외부 체인 락업 증명 → Canton 민트). 데모 범위 밖, 별도 트랙.
   - → 데모는 (a), 문구로 "실제는 브릿지" 명시.
3. **레지스트리 호스팅**: 인스트루먼트별 별도 HTTP 서비스 2개 vs 한 서비스가 2 인스트루먼트(KRWK·JPY) 제공. → **한 서비스 2 인스트루먼트** 권장(운영 간단).
4. **발행자(admin) 파티**: KRWK admin, JPY admin을 각각 새 파티로(예: `krwk-issuer`, `jpy-issuer`). venue(musubi)와 동일한 방식으로 할당+권한.

---

## 3. 단계별 작업

### Phase 0 — 스파이크(선조사, 0.5~1일) ★먼저
가장 큰 미지수 두 개를 코드 작성 전에 검증:
- [ ] **검증자 지갑이 제3 토큰을 다루나**: `/v0/wallet/token-standard/allocation-requests`·`/v0/allocations`가 Amulet 외 인스트루먼트도 처리하는지(토큰표준 제네릭인지). 안 되면 allocation 생성 경로를 자체 구현해야 함.
- [ ] **레지스트리 URL 디스커버리**: 검증자/지갑이 인스트루먼트 admin으로부터 그 토큰의 **레지스트리 HTTP 엔드포인트를 어떻게 찾는지**(메타데이터의 URL? validator 설정? DSO 등록?). 우리 `registry_ctx`는 `:4000`을 하드코딩 → 토큰별 라우팅 방법 확정 필요.
- [ ] Splice **토큰표준 인터페이스 패키지/예제** 위치 확인(`Splice.Api.Token.*`), 레퍼런스 레지스트리 존재 여부.

### Phase 1 — 토큰표준 인스트루먼트 (Daml)
- [ ] 새 Daml 패키지 `stablecoin`(예: `dev/daml/stablecoin/`).
- [ ] 템플릿: `Holding`(잔액), `TransferInstruction`, `Allocation`, `AllocationInstruction` — 각각 `Splice.Api.Token.*` 인터페이스 구현.
- [ ] 발행 템플릿: `IssuerRight`/`Mint` (admin이 특정 파티에 잔액 생성).
- [ ] KRWK·JPY는 **같은 코드 + 다른 instrumentId**(admin/symbol/decimals만 차이).
- [ ] DAR 빌드 → LocalNet 참여자(app-user·app-provider, 발행자 참여자)에 업로드(`POST /v2/packages`).

### Phase 2 — 레지스트리 백엔드 (오프레저 HTTP API) ★가장 무거움
Amulet의 scan이 하는 일을 우리 토큰용으로 구현:
- [ ] `GET /registry/metadata/v1/instruments` — KRWK·JPY 메타데이터.
- [ ] `GET /registry/metadata/v1/info` — adminId 등.
- [ ] `POST /registry/allocations/v1/{cid}/choice-contexts/execute-transfer` (그리고 `/withdraw`, `/cancel`) — **choiceContextData + disclosedContracts** 반환. ← 실행의 핵심.
- [ ] (필요시) transfer-instruction / allocation-instruction choice-context 엔드포인트.
- [ ] 이 서비스는 원장(JSON Ledger API)에서 토큰 룰/홀딩 컨트랙트를 읽어 disclosed contracts(createdEventBlob 포함)를 구성. Amulet의 `disclosedContracts` 형식과 동일하게.

### Phase 3 — 인스트루먼트 등록 + 디스커버리 배선
- [ ] Phase 0에서 확정한 방식으로 KRWK·JPY 레지스트리 URL을 검증자/지갑이 찾도록 설정.
- [ ] 발행자 파티(`krwk-issuer`, `jpy-issuer`) 할당 + `ledger-api-user` 권한(venue와 동일 패턴, `server.py:venue_party()` 참고).

### Phase 4 — 발행(민트)
- [ ] KRWK를 **국내은행(app-user)** 에 민트(예: 1,000,000 KRWK).
- [ ] JPY를 **해외은행(app-provider)** 에 민트(예: 100,000 JPY).
- [ ] 토큰표준 holding으로 잡히는지 확인(잔액 조회 경로 Phase 5와 연동).

### Phase 5 — 데모 백엔드 연동 (`server.py`)
- [ ] `create_proposal()`: `legKRW.instrumentId = {admin: KRWK_ADMIN, id:"KRWK"}`, `legJPY.instrumentId = {admin: JPY_ADMIN, id:"JPY"}`, 금액을 FX 비율로(예: KRWK 1,000,000 ↔ JPY 100,000).
- [ ] `registry_ctx()`: 단일 `:4000` 하드코딩 → **인스트루먼트별 레지스트리 라우팅**(leg의 admin/instrument로 엔드포인트 선택). 두 leg가 서로 다른 레지스트리에서 disclosed contracts를 받음.
- [ ] `allocate_for()`: 토큰표준 지갑이 KRWK/JPY allocation을 만들도록(Phase 0 결과에 따라 경로 조정).
- [ ] 실행: `legmap` 수집 시 Amulet 전용 `:Splice.AmuletAllocation:AmuletAllocation` 대신 **각 토큰의 Allocation 템플릿**으로 매칭.
- [ ] `balance_of()`: KRWK·JPY를 각각 holding API로 조회(은행별 두 통화 잔액).
- [ ] `reset`: 두 토큰 allocation withdraw + 정산 취소(현행 로직 일반화).

### Phase 6 — 프론트(`frontend/index.html`)
- [ ] leg 표시: instrument를 "KRWK"/"JPY"로(이미 `l.inst` 사용 — 백엔드가 실제 ID 주면 자동).
- [ ] 잔액 바: 은행별 **두 통화 잔액**(국내은행 KRWK 보유·JPY 0, 해외은행 반대) 표기.
- [ ] 용어 legend의 "Amulet 대역" 주석 제거, 실제 KRWK/JPY 설명으로 교체.

### Phase 7 — 검증
- [ ] 전체 흐름(제안→수락→개시→양측 잠금→실행)에서 **KRWK·JPY가 한 트랜잭션에 원자적 교환**.
- [ ] 프라이버시 유지(제3자 정산 0건) — 토큰만 바뀌어도 동일해야.
- [ ] 실패 시연(한쪽 미할당 → 실행 실패, 자산 불변)도 두 토큰에서 성립.

---

## 4. 리스크 / 확인 필요
- **(高) 레지스트리 disclosed-contracts 구현**: execute가 받는 disclosedContracts를 토큰 룰/홀딩에서 정확히 구성해야 함. 형식·서명·synchronizerId 한 곳만 틀려도 실행 400. (Amulet은 scan이 대신 해줌.)
- **(高) 디스커버리**: 검증자가 우리 레지스트리를 못 찾으면 지갑 경로 전체를 우회 구현해야 함(Phase 0에서 판정).
- **(中) 지갑 호환**: `/v0/allocations`가 제3 토큰 미지원이면 allocation 생성/withdraw를 JSON Ledger API로 직접 구현.
- **(中) 발행 모델 정합**: 데모는 네이티브 민트지만 실제는 브릿지 → 문구로 명확히 구분(메모: 발행 체인 미확정, 양 시나리오 병기).
- **(低) DAR/패키지 업로드, 파티/권한**: venue 분리에서 이미 검증된 패턴 재사용.

## 5. 노력 추정 (대략)
- Phase 0 스파이크: 0.5~1일 (이게 전체 가능성을 가른다)
- Phase 1 Daml: 1~2일
- Phase 2 레지스트리: **2~4일** (가장 큼)
- Phase 3~7 통합·프론트·검증: 2~3일
- 합계 ≈ **1~2주** (스파이크 결과에 크게 좌우)

## 6. 대안 메모
- **옵션 B(라벨 stand-in)**: 내부 Amulet 유지, UI만 KRWK/JPY 표기 + "대역" 주석. 수 분. 로컬 시연엔 충분.
- **권장 경로**: 먼저 B로 내러티브 확보 → 진짜 토큰이 필요한 시점(파트너 검증/실거래 PoC)에 A를 Phase 0 스파이크부터 착수.
