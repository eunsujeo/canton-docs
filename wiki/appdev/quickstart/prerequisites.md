---
title: 사전 요구사항·설치 (Prerequisites and Installation)
source: https://docs.canton.network/appdev/quickstart/prerequisites
translated: 2026-06-15
status: done
tags: [appdev, quickstart, 설치, 로컬개발]
---

> **출처(원문)**: [Prerequisites and Installation](https://docs.canton.network/appdev/quickstart/prerequisites) · 번역일 2026-06-15

## 📌 개발자 노트
- **한 줄 요약**: CN Quickstart를 로컬에 설치·실행하는 절차. **Docker Desktop(메모리 8GB 권장)·Nix·Direnv** 준비 → 저장소 클론 → <abbr class="gloss" title="다자간 워크플로를 위해 설계된 Canton의 스마트 컨트랙트 언어">Daml</abbr> SDK 설치(`make install-daml-sdk`) → `make setup`/`build`/`start`로 LocalNet 기동. Windows는 WSL 2 필수.
- **핵심 용어**: Docker Desktop, Nix, Direnv, Daml SDK, `make` 명령, LocalNet, DevNet/TestNet/MainNet, OAuth2·Observability
- **선행 개념**: [Canton Network QuickStart](index.md). 다음 → [데모 실행하기](running-the-demo.md)

---

# 사전 요구사항·설치

> 개발 환경을 세팅하고 Canton Network QuickStart를 설치하기

# Canton Network quickstart 설치

## 소개

Quickstart 애플리케이션은 **필수적인** 스캐폴딩을 제공해, 당신과 팀이 CN 애플리케이션 개발에 친숙해지도록 돕는다. Quickstart 애플리케이션은 출발대(launchpad)이며, 당신의 비즈니스 요구에 맞게 확장하도록 의도되었다. Quickstart에 익숙해지면, 기술 선택과 애플리케이션 설계를 검토해 어떤 변경이 필요한지 판단하라. 기술·설계 결정은 궁극적으로 당신에게 달려 있다.

## 개요

이 가이드는 CN Quickstart의 설치와 `LocalNet` 배포를 안내한다. 편의를 위해 경험 수준에 따라 [빠른 경로 설치](#빠른-경로-설치)와 [단계별 지침](#단계별-지침)을 제공한다. 오류를 발견하면 Digital Asset의 담당자에게 연락하라.

### 로드맵

* 설치 후, [데모 둘러보기](running-the-demo.md)로 예제 애플리케이션에서 비즈니스 작업을 완료해 본다.
* Quickstart 프로젝트가 어떻게 구조화돼 있는지 개요는 [프로젝트 구조 가이드](https://docs.canton.network/appdev/quickstart/project-structure)를 읽는다.
* lnav를 이용한 디버깅은 [lnav로 디버깅·문제 해결](https://docs.canton.network/appdev/quickstart/lnav)에서 배운다.
* 추가 디버깅 정보는 [cn-quickstart 저장소](https://github.com/digital-asset/cn-quickstart)의 관측성·문제 해결 섹션에 있다.

## 사전 요구사항

[CN-Quickstart GitHub 저장소](https://github.com/digital-asset/cn-quickstart) 접근은 공개되어 있다. 다만 Digital Asset이 제공하는 일부 아티팩트를 가져온다.

CN Quickstart는 도커화된(Dockerized) 애플리케이션으로 [Docker Desktop](https://www.docker.com/products/docker-desktop/)이 필요하다. Docker Desktop에 **메모리 8GB 할당**을 권장한다. 컨테이너가 비정상(unhealthy)이면 가능한 한 자원을 추가 할당하라. 머신 메모리가 충분치 않으면 Observability를 끈다(decline).

기타 요구사항:

* [Curl](https://curl.se/download.html)
* [Direnv](https://direnv.net/docs/installation.html)
* [Nix](https://nixos.org/download/)
* Windows 사용자는 관리자 권한으로 [WSL 2](https://learn.microsoft.com/en-us/windows/wsl/install)를 설치·사용해야 한다.

### Nix 다운로드 지원

머신에 Nix가 있는지 <abbr class="gloss" title="이해관계자 밸리데이터가 트랜잭션이 유효함을 미디에이터에 응답하는 것(confirmation)">확인</abbr>:

```bash
nix --version
```

`Nix (Nix) 2.25.2` 같은 결과가 나오면 완료된 것이다.

MacOS 권장 설치:

```bash
sh <(curl -L https://nixos.org/nix/install)
```

Linux 권장 설치(Windows 사용자는 이 명령과 이후 모든 명령을 WSL 2에서 실행):

```bash
sh <(curl -L https://nixos.org/nix/install) --daemon
```

## 빠른 경로 설치

사전 요구사항에 익숙하다면 아래 축약 설치 지침을 사용하라. 더 자세한 지침은 아래에 제공된다.

1. [GitHub에서 클론](#github에서-클론)하고 `cn-quickstart` 저장소로 cd: `git clone https://github.com/digital-asset/cn-quickstart.git`
2. [Docker Desktop](#docker) 앱이 실행 중인지 확인: `docker info`
3. 터미널로 Docker 저장소에 로그인: `docker login`
4. `quickstart` 하위 디렉토리로 **cd**: `cd quickstart`
5. quickstart 하위 디렉토리에서 [Daml SDK 설치](#daml-sdk-설치): `make install-daml-sdk`
6. [로컬 개발 환경 구성](#localnet에-밸리데이터-배포): `make setup`
7. 프롬프트가 뜨면, OAuth2 활성화, Observability 비활성화, TEST MODE 비활성화, <abbr class="gloss" title="Canton에서 권한과 데이터 가시성의 주체가 되는 식별 가능한 참여 주체">파티</abbr> 힌트는 기본값을 쓰도록 비워 둔다.
8. `quickstart` 하위 디렉토리에서 애플리케이션 빌드: `make build`
9. 새 터미널 창에서 `quickstart` 하위 디렉토리로부터 로그 수집 시작: `make capture-logs`
10. 이전 터미널 창으로 돌아와 애플리케이션과 Canton 서비스 시작: `make start`
11. 선택 — 별도 셸에서 `quickstart` 하위 디렉토리로부터 [Canton Console](#로컬-canton-노드에-연결) 실행: `make canton-console`
12. 선택 — 네 번째 셸에서 `quickstart` 하위 디렉토리로부터 Daml Shell 시작: `make shell`
13. 완료되면 다음으로 [애플리케이션 종료](#애플리케이션-종료) 및 기타 서비스 종료: `make stop && make clean-all`
14. 해당하면 Canton Console은 `exit`로, Daml Shell은 `quit`로 종료한다.

## 단계별 지침

### GitHub에서 클론

`cn-quickstart` 저장소를 로컬 머신에 클론하고 **cd** 한다.

```bash
git clone https://github.com/digital-asset/cn-quickstart.git
cd cn-quickstart
direnv allow
```

![direnv 허용](https://mintcdn.com/cantonfoundation/QAGFSphBsRkeZIBi/images/docs_website/01-allow-direnv.png?fit=max&auto=format&n=QAGFSphBsRkeZIBi&q=85&s=add8265c0387084840d113832461ca2e)

### Docker

Docker Desktop 애플리케이션이 컴퓨터에서 실행 중인지 확인한다.

터미널로 Docker 저장소에 로그인한다.

```bash
docker login
```

마지막 명령은 [Docker Hub](https://app.docker.com/) 사용자명과 비밀번호 또는 *개인 액세스 토큰(Personal Access Token, PAT)* 을 요구한다.

명령은 'Login Succeeded'를 반환해야 한다.

### Daml SDK 설치

`quickstart` 하위 디렉토리로 **cd** 하고, 거기서 Daml SDK를 설치한다.

```bash
cd quickstart
make install-daml-sdk
```

> **참고:** 프로젝트 작업 흐름(choreography)을 제공하는 `Makefile`은 `quickstart/` 디렉토리에 있다. `make`는 `quickstart/` 안에서만 동작한다.
>
> `make` 관련 오류가 보이면 현재 작업 디렉토리를 다시 확인하라.

Daml SDK는 크기가 커서 완료까지 몇 분 걸릴 수 있다.

![Daml SDK 압축 해제](https://mintcdn.com/cantonfoundation/QAGFSphBsRkeZIBi/images/docs_website/06-unpack-sdk.png?fit=max&auto=format&n=QAGFSphBsRkeZIBi&q=85&s=bbfffb42c7250a27209501a2eb47adcf)

### LocalNet에 밸리데이터 배포

`make setup`을 실행해 로컬 개발 환경을 구성한다.

`Observability`를 비활성화한다. OAuth2를 활성화한다. 파티 힌트는 기본값을 쓰도록 비워 두고 `TEST MODE`를 비활성화한다.

> **참고:** 파티 힌트는 파티 노드의 식별 해시에 대한 별칭(alias)으로 쓰인다. 파티 힌트는 사용자 신원의 일부가 아니라 편의 기능이다. 같은 힌트를 가진 파티 노드가 여럿 존재할 수도 있다.

```text
% make setup
Starting local environment setup tool...
./gradlew configureProfiles --no-daemon --console=plain --quiet
Enable Observability? (Y/n): n
OBSERVABILITY_ENABLED set to 'false'.

Enable OAUTH2? (Y/n): y
AUTH_MODE set to 'oauth2'.

Specify a party hint (this will identify the participant in the
  network) [quickstart-USERNAME-1]:
PARTY_HINT set to 'quickstart-USERNAME-1'.

Enable TEST_MODE? (Y/n): n
TEST_MODE set to 'off'.

.env.local updated successfully.
```

`make setup`을 다시 실행하면 이 선택들을 언제든 바꿀 수 있다.

> **참고:** Docker Desktop에 할당된 메모리가 8GB 미만이면 OAuth2와 Observability가 불안정할 수 있다.

애플리케이션을 빌드한다.

```bash
make build
```

![빌드 성공](https://mintcdn.com/cantonfoundation/QAGFSphBsRkeZIBi/images/docs_website/07-build-success-1.png?fit=max&auto=format&n=QAGFSphBsRkeZIBi&q=85&s=932899ab2d860f43ca157a6904434228)

새 터미널 창에서 `quickstart` 하위 디렉토리로부터 로그 수집을 시작한다.

```bash
make capture-logs
```

완료되면 이전 터미널로 돌아와 애플리케이션과 Canton 서비스를 시작한다.

```bash
make start
```

### 로컬 Canton 노드에 연결

별도 셸에서 `quickstart` 하위 디렉토리로부터 Canton Console을 실행한다.

```bash
make canton-console
```

![Canton 콘솔](https://mintcdn.com/cantonfoundation/QAGFSphBsRkeZIBi/images/docs_website/11-canton-console.png?fit=max&auto=format&n=QAGFSphBsRkeZIBi&q=85&s=a43a087a3b359953280e29e0568e3acf)

네 번째 셸에서 quickstart 하위 디렉토리로부터 Daml Shell을 시작한다.

```bash
make shell
```

![Daml 셸](https://mintcdn.com/cantonfoundation/QAGFSphBsRkeZIBi/images/docs_website/12-daml-shell.png?fit=max&auto=format&n=QAGFSphBsRkeZIBi&q=85&s=7389585ba51905f5af1dabde12f65319)

### 애플리케이션 종료

*⚠️ (CN Quickstart를 곧바로 이어서 쓸 계획이면 이 절의 실행을 미뤄라)*

#### Canton 콘솔 종료

완료되면 Canton 콘솔 터미널을 연다. `exit`를 실행해 콘솔 컨테이너를 멈추고 제거한다.

#### Daml 셸 종료

Daml 셸 터미널에서 `quit`를 실행해 셸 컨테이너를 멈춘다.

#### CN Quickstart 종료

마지막으로, 애플리케이션과 관측성 서비스를 다음으로 종료한다:

```bash
make stop && make clean-all
```

개발 중과 매 세션 종료 시 `make clean-all`을 실행해 두면 이후 애플리케이션 빌드에서 충돌 오류를 피할 수 있어 현명하다.

## 다음 단계

CN Quickstart를 성공적으로 설치했다.

다음 절 "데모 둘러보기"는 예제 애플리케이션의 시연을 제공한다.

### 애플리케이션을 Canton Network에 연결하기

`LocalNet` 배포는 로컬 <abbr class="gloss" title="파티를 호스팅하고 그 파티의 컨트랙트 데이터를 저장하는 참여자 노드">밸리데이터</abbr>에 연결되고, 그 밸리데이터는 다시 로컬 <abbr class="gloss" title="글로벌 Synchronizer를 운영하고 네트워크 거버넌스에 참여하는 노드">슈퍼 밸리데이터</abbr>(<abbr class="gloss" title="상태를 저장하지 않고 트랜잭션 합의·순서를 조율하는 Canton 구성요소">Synchronizer</abbr>)에 연결된다. 스테이징·최종 프로덕션 배포에서는 다시 퍼블릭 Canton Network에 연결된 밸리데이터에 연결해야 한다.

Canton Network는 세 개의 Synchronizer 풀을 제공한다. 프로덕션 네트워크는 `MainNet`, 프로덕션 스테이징 네트워크는 `TestNet`이다. 개발자로서 당신은 대부분 개발 스테이징 네트워크인 `DevNet`에 연결하게 된다.

DevNet에 연결하려면 CN에서 허용목록(whitelist)에 오른 [SV 노드](https://docs.canton.network/global-synchronizer/deployment/onboarding-process)에 대한 접근이 필요하다. CF는 밸리데이터 노드를 후원할 수 있는 [SV 노드 목록](https://sync.global/sv-network/)을 게시한다. `DevNet`에 접근하려면 후원 SV 담당자에게 VPN 연결 정보를 문의하라.

## 자원

* [Curl](https://curl.se/download.html)
* [Direnv](https://direnv.net/docs/installation.html)
* [Docker Desktop](https://www.docker.com/products/docker-desktop/)
* [Docker Hub](https://app.docker.com/)
* [CF의 SV 노드 목록](https://sync.global/sv-network/)
* [Digital Asset Docker](https://console.cloud.google.com/artifacts/docker/da-images/europe/public)
* [Nix](https://nixos.org/download/)
* [Quickstart GitHub 저장소](https://github.com/digital-asset/cn-quickstart)
* [밸리데이터 온보딩 문서](https://docs.canton.network/global-synchronizer/deployment/onboarding-process)
* [WSL 2](https://learn.microsoft.com/en-us/windows/wsl/install)

<!-- nav:start -->

---

⬅️ **이전**: [Canton Network QuickStart](index.md) ・ ➡️ **다음**: [데모 실행하기 (Running the Demo)](running-the-demo.md)

<!-- nav:end -->
