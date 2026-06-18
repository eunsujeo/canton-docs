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

## TODO (Phase 1)
- [ ] JSON Ledger API v2 엔드포인트 확인(Swagger `:9090`): ledger-end, active-contracts.
- [ ] `cli/ledger-view.py`: 토큰 민팅 + 참여자별 active-contracts 조회·요약.
- [ ] settlement DAR LocalNet 업로드 + 정산 1건 생성 후 → A/B엔 보이고 외부자엔 안 보임 확인.
