# 로컬 개발 환경 셋업 기록 (Phase 1)

> cn-quickstart / LocalNet 구동을 위한 사전 요구사항 설치 진행 기록.
> 위키 절차: [사전 요구사항·설치](../../wiki/appdev/quickstart/prerequisites.md)

## 머신
- macOS **arm64** (Apple Silicon), 메모리 **36GB** (LocalNet 8GB 권장 — 충분)
- shell: `zsh`, Homebrew 설치됨

## 사전 요구사항 체크리스트

| 항목 | 상태 | 왜 필요한가 | 비고 |
|---|---|---|---|
| Curl | ✅ | 설치 스크립트·아티팩트 다운로드 | 8.7.1 |
| Docker Desktop | ✅ | LocalNet이 Docker Compose 컨테이너로 동작(Canton 노드·SV·UI 전부) | 29.1.2, 데몬 실행중 |
| git | ✅ | cn-quickstart 저장소 클론 | 2.39.5 |
| Java | ✅ | Canton·Daml 툴이 JVM 위에서 실행 | OpenJDK 21 |
| **Direnv** | ✅ | cn-quickstart 폴더 진입 시 `.envrc`(환경변수·SDK 경로) 자동 로드 | 2.37.1 (`brew install direnv` + zsh 훅) — 2026-06-17 |
| **Nix** | ✅ | cn-quickstart가 빌드 도구·의존성을 Nix로 재현성 있게 고정 | 2.34.7 (사용자 직접 설치) — 2026-06-17 |
| Daml SDK | ⬜ | Daml 컨트랙트 컴파일·`daml` CLI(빌드/스크립트 실행) | 전역 설치 X — cn-quickstart에서 `make install-daml-sdk`로 설치 |

## 설치 절차 / 기록

### 1. Direnv (완료)
```bash
brew install direnv
# ~/.zshrc 에 훅 추가:
eval "$(direnv hook zsh)"
```
- cn-quickstart 클론 후 `direnv allow`로 `.envrc`가 자동 로드되게 하는 데 필요.
- 새 터미널부터 적용됨.

### 2. Nix (사용자 직접 실행)
macOS는 sudo 비밀번호 + 별도 APFS 볼륨/데몬 생성이 필요해 **본인 터미널에서** 실행:
```bash
sh <(curl -L https://nixos.org/nix/install)
```
- 설치 후 새 터미널에서 `nix --version` 확인.

### 2-1. Nix flakes 활성화 (함정 ⚠️)
공식 설치 스크립트(`nixos.org/nix/install`)는 **flakes가 기본 비활성**이다. cn-quickstart의 `.envrc`는 `use flake`라서 그대로면 `direnv allow`·`nix develop`이 다음 에러로 실패한다:
```
error: experimental Nix feature 'nix-command' is disabled; ...
```
해결 — 사용자 레벨 설정에 한 줄 추가(sudo 불필요):
```bash
mkdir -p ~/.config/nix
echo 'experimental-features = nix-command flakes' >> ~/.config/nix/nix.conf
```

### 3. Daml SDK — 별도 설치 단계 없음 (최신 cn-quickstart)
> ⚠️ 위키 원문엔 `make install-daml-sdk`가 있지만, **현재 받은 cn-quickstart엔 그 타깃이 없다.**
> Daml SDK(`sdk-version: 3.4.11`)는 **Nix flake / `make build`** 가 처리한다. 전역 설치·별도 명령 불필요.

## 실제 구동 절차 (최신 README 기준)
클론한 저장소 루트에서:
```bash
direnv allow            # ✅ 완료 — .envrc(use flake) 로드
cd quickstart
make setup              # 환경 구성 (대화형 어시스턴트)
make build              # frontend·backend·Daml 모델·docker 이미지 빌드 (오래 걸림)
make start              # 앱 + Canton 서비스 기동 (첫 실행 시 배포 어시스턴트)
```
선택(별도 터미널):
- `make capture-logs` — 로그 수집(블로킹, 디버깅용)
- `make canton-console` / `make shell` — Canton Console / Daml Shell

### make setup 권장 응답 (학습/첫 실행 기준)
- **LocalNet**: enable (로컬 샌드박스)
- **Observability**: disable (메모리 절약, 나중에 켜도 됨)
- **OAuth2**: disable (Keycloak 없이 단순하게 — 첫 실행 마찰 최소화)
- **TEST_MODE**: disable (standard)
- 파티 힌트: 기본값(비워둠)
> 언제든 `make setup` 다시 실행해 변경 가능.

### 편의 타깃 (UI 열기)
`make open-app-ui` · `open-sv-scan` · `open-sv-wallet` · `open-app-user-wallet` · `open-observe` · `open-swagger-ui`

### docker login — 불필요 ✅
위키 원문엔 `docker login`이 있으나 **최신 cn-quickstart는 불필요**.
이미지가 공개 GHCR에서 온다(`compose.env`):
```
IMAGE_REPO=${IMAGE_REPO:-ghcr.io/digital-asset/decentralized-canton-sync/docker/}  # Publicly released images
```
→ Docker Hub 계정·로그인 없이 바로 `make build` 가능. (Keycloak은 `quay.io`, 베이스 이미지는 Docker Hub 공개 이미지 — 전부 익명 pull)

### 그 외 추가로 필요한 것 — 없음
- DevNet VPN/스폰서 SV: LocalNet이라 불필요
- API 키·토큰·스테이블코인 발행 자격: 전부 로컬 시뮬레이션이라 불필요
- 디스크: 이미지·볼륨으로 수 GB 사용

## ✅ 구동 성공 (2026-06-17)
`make setup → build → start` 완료. 컨테이너 16개 전부 healthy, 모든 UI 200 OK.

### 접속 URL (LocalNet)
| UI | URL | 내용 |
|---|---|---|
| **App UI** (App Provider) | http://app-provider.localhost:3000 | 예제 앱(라이선싱/앱설치) 프론트 |
| **Scan** | http://scan.localhost:4000 | 네트워크·SV·CC 활동 익스플로러 |
| **SV Interface** | http://sv.localhost:4000 | 슈퍼밸리데이터 인터페이스 |
| **SV Wallet** | http://wallet.localhost:4000 | SV 지갑 |
| **App User Wallet** | http://wallet.localhost:2000 | 앱 사용자 지갑 |
| **Swagger UI** (JSON API v2) | http://localhost:9090 | Ledger JSON API 탐색 |
| Grafana(Observability) | http://localhost:3030 | (Observability 켰을 때만) |

> `make open-app-ui` / `open-sv-scan` / `open-sv-wallet` / `open-app-user-wallet` / `open-swagger-ui` 로도 열림.

### 종료/정리
- 멈춤: `make stop` · 데이터까지 정리: `make clean-all` (다음 빌드 충돌 예방차 세션 종료 시 권장)

### Scan 상태 빠르게 보기 (CLI)
Scan UI가 보기 불편할 때, 필요한 것만 요약하는 도구:
```bash
python3 ~/Workspace/canton/dev/scan-status.py    # 현재 상태 1회 출력
```
SV·DSO·최신 라운드·닫힌 라운드·총 CC·최근 활동(Tap/Transfer)을 한 화면에. (Scan 읽는 법은 위키 [notes/reading-scan-explorer.md](../../wiki/notes/reading-scan-explorer.md))
> 구현 메모: macOS resolver가 `*.localhost`를 못 풀어서 `127.0.0.1:4000` + `Host: scan.localhost` 헤더로 호출.

> 상세 로드맵: [roadmap.md](roadmap.md)
