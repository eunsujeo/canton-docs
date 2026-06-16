# 원격 공유 & 데모 대시보드 옵션 (나중에 진행)

> 학습·로컬 개발이 우선. 이 문서는 "개발 결과를 팀에 공유"하고 "Canton 시나리오·기능 테스트를 시연"할 단계가 오면 볼 계획 메모.

## 1) 원격 서버에 띄워 팀과 공유

LocalNet은 Docker Compose라 **클라우드 VM/리눅스 서버에 그대로** 올릴 수 있다.

- VM(8GB+ RAM)에 cn-quickstart 배포 → `make start` → 팀원이 **서버 URL로 웹 UI 접속**
- ⚠️ 손봐야 할 2가지:
  1. **도메인**: 기본 `*.localhost`(로컬 전용) → 원격 공유엔 **실제 도메인 + 리버스 프록시(nginx/caddy) + TLS** 필요. 빠른 공유면 **SSH 터널 / Tailscale** 로 소규모 팀만.
  2. **보안**: dev용이라 인증 약함 → **VPN·방화벽·접근제한 뒤**에 둘 것. 공개 노출 금지.
- 성격: 이건 여전히 **LocalNet(시뮬레이션)** 을 공용 dev 서버에 올린 것. 다른 기관과 진짜 연동은 **DevNet** 으로.

> 요약: **클라우드 VM + 리버스 프록시(또는 터널) + 접근제한.** dev 전용.

## 2) 데모 대시보드 (상당수 기본 제공)

cn-quickstart/Splice에 포함된 화면:

| 화면 | 보여주는 것 |
|---|---|
| **Scan UI** (`scan.localhost:4000`) | 네트워크·SV·밸리데이터·CC 활동(익스플로러) |
| **SV UI** (`sv.localhost:4000`) | SV 정보·밸리데이터 온보딩 |
| **Wallet** (`wallet.localhost`) | CC 잔액·결제·트래픽 |
| **Observability** (`localhost:3030`) | 서비스 로그·메트릭(기능 테스트·동작 확인) |
| **샘플 앱 프론트(React)** | 데모 시나리오 UI |

**"실행 가능한 시나리오·기능 테스트" 시연**:
- **Daml Script** — 거래 시퀀스를 스크립트로 자동 실행(데모·기능 테스트에 적합). "이 시나리오가 이렇게 흐른다"를 재현.
- **샘플 프론트 변형** — DvP 정산 등 우리 시나리오를 버튼으로 시연하는 커스텀 데모 대시보드.
- **Canton Console / Daml Shell** — 라이브 상태(participants, active 컨트랙트 등) 시연.

## 우선순위

1. **지금**: 로컬 LocalNet에서 학습·정산 로직 구현 ← 집중
2. **나중**: 공용 dev 서버(원격 VM) + 커스텀 데모 대시보드
3. **그 다음**: DevNet 온보딩(다른 기관 연동 필요 시)

## 참고 (위키)
- [환경 4단계 — LocalNet→DevNet→TestNet→MainNet](../../wiki/notes/canton-environments-localnet-to-mainnet.md) (하드웨어 스펙 포함)
- [DvP 정산 앱 2층 구조](../../wiki/notes/dvp-settlement-app-architecture.md)
- [LocalNet 개발](../../wiki/appdev/modules/m5-localnet-development.md) · [데모 실행](../../wiki/appdev/quickstart/running-the-demo.md)
