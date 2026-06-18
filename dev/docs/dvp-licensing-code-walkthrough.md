# 예제 앱(라이선싱) Daml 코드 → DvP 골격 → Musubi 연결

> cn-quickstart의 라이선싱 예제를 직접 돌려보고 Daml 코드까지 읽으며 정리한 노트.
> **결론: 이 예제의 `License.daml`이 Musubi DvP의 거의 그대로의 골격이다.** (다리 1개 → 2개로 확장)
> 개념 배경은 위키 [DvP 정산 앱 2층 구조](../../wiki/notes/dvp-settlement-app-architecture.md) 참고.

## 코드 위치
```
quickstart/daml/licensing/daml/Licensing/
├─ AppInstall.daml   # AppInstallRequest, AppInstall
└─ License.daml      # License, LicenseRenewalRequest (+ DvP)
quickstart/daml/licensing-tests/daml/Licensing/Scripts/TestLicense.daml  # 시나리오 테스트
```

## 워크플로 ↔ 코드 매핑
| 단계 | 누가 | 코드(템플릿/초이스) |
|---|---|---|
| ① 가입 요청 | app-user | `AppInstallRequest` 생성 (`signatory user`) |
| ② 수락 | app-provider | `AppInstallRequest_Accept` (`controller provider`) → `AppInstall` 생성 |
| ③ 라이선스 발급 | app-provider | `AppInstall_CreateLicense` → `License` 생성(만료 상태) |
| ④ 갱신 요청 | app-provider | `License_Renew` (nonconsuming) → `LicenseRenewalRequest` 생성 |
| ⑤ 결제(할당) | app-user | 지갑에서 Allocation 수락 (transferLeg: user→provider) |
| ⑥ 완료(정산) | app-provider | `LicenseRenewalRequest_CompleteRenewal` → **원자적 DvP** |

## 핵심 1 — 제안-수락 패턴 = `signatory` + `choice ... controller`
- 누가 컨트랙트를 만드냐 = `signatory`, 각 행동을 누가 하냐 = `choice ... controller`.
- 일방적 강제 불가: 상대의 동의(서명·controller) 없이는 상태가 안 바뀐다. (Canton "동의 없이 못 바꾼다"의 코드 구현)

## 핵심 2 — 원자적 DvP는 "한 choice의 do 블록"
`LicenseRenewalRequest_CompleteRenewal` (License.daml:112~147)이 한 트랜잭션에서:
```haskell
do
  exercise allocationCid (Allocation_ExecuteTransfer ...)  -- (가) 결제: CC 이동
  archive licenseCid                                       -- (나) 옛 라이선스 폐기
  create oldLicense with expiresAt = ... + duration        -- (다) 새 라이선스(연장)
```
- 한 `do` = 한 Daml 트랜잭션 = **전부 성공 or 전부 롤백(원자성)**.
- → "CC만 빠지고 갱신 안 됨" 구조적으로 불가능. **이게 DvP의 본질.**
- 초이스 종류: `nonconsuming`(License_Renew, 원본 유지) / `postconsuming`(CompleteRenewal, 실행 후 요청 소비) / 기본 consuming.

## 핵심 3 — "지급 다리(transfer leg)" = 토큰 표준 Allocation
`LicenseRenewalRequest`가 `AllocationRequest` 인터페이스를 구현(License.daml:149~184):
```haskell
transferLegs = [ "licenseFeePayment" → TransferLeg
    { sender = user, receiver = provider, amount = licenseFeeAmount, instrumentId = ... } ]
```
- 이 leg 선언이 app-user 지갑에 뜬 **할당 요청**의 정체.
- 토큰 표준(`Splice.Api.Token.*`)이 이 leg를 받아 CC 이동을 처리 → 앱은 CC 전송 코드를 직접 안 짠다.

## 🔗 Musubi DvP = 다리 1개 → 2개
라이선싱은 **단방향 지급**(고객→회사 1 leg). Musubi는 **양방향 통화 교환 2 legs**:
```haskell
transferLegs = [
  "legKRW" → TransferLeg { sender=기관A, receiver=기관B, amount=..., instrumentId=KRW스테이블코인 },
  "legJPY" → TransferLeg { sender=기관B, receiver=기관A, amount=..., instrumentId=JPY스테이블코인 }
]
```
- `CompleteRenewal` 같은 초이스에서 **두 leg를 한 트랜잭션에 실행** → 양쪽 통화 동시 교환 = **원자적 FX DvP**.
- 스테이블코인 발행 체인은 미정(양쪽 시나리오 병기) — Canton 위 토큰 표준 인스트루먼트로 표현하느냐, 브릿지로 들여오느냐는 별도 설계.

## ⭐ Musubi에 더 맞는 참고 = OTCTrade 예제 (P2P 다중 leg)
> 라이선싱은 **판매자→고객(비대칭, B2C 느낌)** 이라 Musubi(**적격기관↔적격기관, 대칭**)와 모양이 다르다.
> 같은 원리(제안-수락·allocation·원자적 정산)지만, **토폴로지가 맞는 예제는 OTCTrade**다.

위치: `daml/external-test-sources/splice-token-test-trading-app/daml/Splice/Testing/Apps/TradingApp.daml`
(Splice 참고/테스트 예제 — 배포 앱 아님, 청사진으로 읽기用)

구조 ↔ Musubi 매핑:
| OTCTrade | Musubi |
|---|---|
| `venue` (운영자) | Musubi/정산 운영자(RFQ 베뉴) |
| `tradingParties` | 적격기관 A·B (P2P) |
| `transferLegs : TextMap TransferLeg` (**여러 개**) | legKRW(A→B) + legJPY(B→A) |
| `OTCTradeProposal` + `_Accept`(각 당사자) | RFQ 제안 + 양 기관 합의 |
| `OTCTradeProposal_InitiateSettlement` ("All trading parties approved" 검증) | 정산 개시 |
| `OTCTrade_Settle` (모든 leg 원자적 실행) | **양쪽 통화 동시 정산(FX DvP)** |

## Musubi 만들 때 출발점
- **1순위 참고: OTCTrade**(다중 leg·대칭·venue) — 라이선싱(단방향)보다 가까움.
- `licensing/` 자리에 새 패키지(예: `settlement/`)를 만들어 OTCTrade를 본떠 작성:
  - `SettlementProposal`(=OTCTradeProposal) + `transferLegs` 2개 + 양 기관 `_Accept`
  - `Settlement`(=OTCTrade) + `_Settle`(모든 leg 원자적 실행)
  - 라이선싱에서 배운 `AllocationRequest`/토큰표준 잠금 패턴은 그대로 재사용.

## 참고
- 실행 흐름·관찰: 위키 [Scan 읽는 법](../../wiki/notes/reading-scan-explorer.md) · [원장 모델](../../wiki/overview/learn/how-transactions-work.md)
- 로드맵 Phase 2(DvP 로직 구현)의 직접 근거: [roadmap.md](roadmap.md)
