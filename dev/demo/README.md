# demo — LocalNet 라이브 정산 + 프라이버시 데모

계획: [../docs/demo-plan-localnet-privacy.md](../docs/demo-plan-localnet-privacy.md)

## 구조 (예정)
```
demo/
├─ cli/        # Phase 1: 파티별 Ledger API 조회로 프라이버시 텍스트 증명
├─ backend/    # Phase 3: thin (Ledger API ↔ REST/SSE)
└─ frontend/   # Phase 3: 파티 패널 4개 (frontend-design)
```

## 🔑 Phase 1 발견 — 파티별 토큰 발급 (최대 리스크 해소)
LocalNet은 **shared-secret 모드** → JWT를 **HS256, 시크릿 문자열 `"unsafe"`** 로 직접 만들 수 있다.
출처: `cn-quickstart .../docker/modules/.../utils.sh`의 `generate_jwt()`:
```bash
jwt-cli encode hs256 --s unsafe --p '{"sub":"<user>", "aud":"<audience>"}'
```
- **claims**: `sub` = ledger-api 유저, `aud` = audience
- **유저**: `ledger-api-user` (참여자마다 동일 이름이지만 각자 자기 참여자 범위)
- **audience**: `https://canton.network.global`
- Python으로 직접 생성 가능(jwt-cli 불필요): HS256(`hmac`), base64url.

## 참여자별 JSON Ledger API (포트)
| 파티(참여자) | JSON API | gRPC Ledger API |
|---|---|---|
| app-user | `:2975` | `:2901` |
| app-provider | `:3975` | `:3901` |
| sv | `:4975`(추정, 확인 필요) | `:4901` |
- nginx 호스트: `json-ledger-api.localhost` (Host 헤더) 또는 포트 직접.

## 🔒 프라이버시가 구조적으로 보장되는 이유
각 **참여자 노드는 자기 파티가 이해관계자인 컨트랙트만 저장**한다.
→ app-user 참여자 API를 조회하면 **app-user 것만**, app-provider API는 **app-provider 것만** 보임.
→ **외부자(무관 파티/참여자)는 그 정산을 *데이터로 갖고 있지도 않음*** = 못 봄. (토큰 권한 문제 이전에 데이터 자체가 없음)

## 데모 파티 매핑
| 역할 | 파티 | 비고 |
|---|---|---|
| 기관A | app-user | 이미 온보딩·CC 보유 |
| 기관B | app-provider | 이미 온보딩·CC 보유 |
| venue | (신규 할당 또는 app-provider 겸용) | 운영자 |
| 외부자 | sv 참여자 또는 신규 파티 | 정산에 스테이크 없음 → 못 봄 |

## Phase 1 ✅ 완료 — 프라이버시 텍스트 증명
- [x] JSON Ledger API v2 확정: canton이 **호스트에 직접 노출**(`127.0.0.1:2975` app-user / `3975` app-provider / `4975` sv). nginx 불필요. 엔드포인트: `/v2/version`, `/v2/state/ledger-end`, `/v2/parties`, `POST /v2/state/active-contracts`.
- [x] **`cli/ledger-view.py`**: 토큰(HS256 unsafe) 민팅 + 참여자별 활성 컨트랙트 템플릿 집계.
  ```bash
  python3 dev/demo/cli/ledger-view.py            # 전체
  python3 dev/demo/cli/ledger-view.py Licensing  # 특정 템플릿만
  ```
- [x] **프라이버시 증명(실측)**: `Licensing.License` → app-user 2개·app-provider 2개·**sv(외부자) 0개**. 두 당사자 계약을 외부자는 못 봄.

### active-contracts 요청 형식 (확정)
```json
POST /v2/state/active-contracts
{"filter":{"filtersByParty":{"<party>":{"cumulative":[{"identifierFilter":{"WildcardFilter":{"value":{"includeCreatedEventBlob":false}}}}]}}},
 "verbose":false,"activeAtOffset":<ledger-end offset>}
```

## Phase 2 ✅ (일부) — 우리 DvP를 LocalNet에서, 프라이버시 증명
- [x] settlement DAR을 app-user·app-provider 참여자에 업로드 (`POST /v2/packages`, DAR bytes).
  - 패키지 ID: `5959344bd3212e47ebf70a2cde52b8125f79939ca6583f18a8873d574cf9095b`
- [x] **SettlementProposal 생성** (`POST /v2/commands/submit-and-wait`, CreateCommand) → `cli/create-settlement.py`.
- [x] **프라이버시 증명(우리 DvP)**: `Settlement.FxDvp:SettlementProposal` → app-user 1·app-provider 1·**sv(외부자) 0**.
  ```bash
  python3 dev/demo/cli/create-settlement.py    # 제안 1건 생성
  python3 dev/demo/cli/ledger-view.py Settlement
  ```
- 데모 단순화: venue=app-provider 겸용, 통화=Amulet 1종, leg KRW(A→B 100)·JPY(B→A 20).

## TODO (Phase 2 나머지 ~ 3)
- [ ] 전체 흐름(accept→**실제 CC 할당**→execute)을 LocalNet에서 — 실제 Amulet allocation 필요(테스트 하네스 아님).
- [ ] (선택) venue·outsider 별도 파티 할당으로 역할 분리.
- [ ] 백엔드(SSE 실시간) + 프론트 파티 패널 4개 (Phase 3, frontend-design).

## Phase 3 ✅ (1차) — 웹 데모 (프라이버시 뷰)
- `backend/server.py` (Python stdlib, 무의존성): 참여자별 토큰으로 JSON Ledger API 조회 → `/api/state` JSON + 프론트 서빙. `python3 backend/server.py` → http://localhost:8888
- `frontend/index.html` (frontend-design 적용): **삼면 비교** — 기관A·B 감사시트 카드(교차 화살표 leg) vs 외부자 다크 보이드("데이터 없음"). 2.5s 폴링 실시간.
- 실측: A 정산1건(활성11) · B 정산1건(활성12) · **외부자 정산0건(활성46)** → "바쁜 노드인데 이 거래만 없다" = 프라이버시 증명.
- TODO: 시나리오 버튼(제안/수락/할당/실행) + SSE 전환 + 통화 2종.
