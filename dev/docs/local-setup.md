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
| **Nix** | ⬜ | cn-quickstart가 빌드 도구·의존성을 Nix로 재현성 있게 고정 | 사용자 터미널에서 직접 설치 필요 (sudo) |
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

### 3. Daml SDK (Phase 1 진행 중 자동)
전역 설치하지 않는다. cn-quickstart 클론 → `quickstart/` 안에서:
```bash
make install-daml-sdk
```
- 용량이 커서 몇 분 소요.

## 다음 (Nix 설치 후)
1. `git clone https://github.com/digital-asset/cn-quickstart.git` → `cd cn-quickstart` → `direnv allow`
2. `docker login`
3. `cd quickstart` → `make install-daml-sdk`
4. `make setup` (Observability=n, OAuth2=y, 파티힌트=기본, TEST_MODE=n)
5. `make build` → 새 터미널 `make capture-logs` → `make start`
6. 대시보드 확인: Scan / SV / Wallet UI

> 상세 로드맵: [roadmap.md](roadmap.md)
