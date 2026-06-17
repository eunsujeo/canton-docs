---
title: 모듈 5 — LocalNet 개발 (LocalNet Development)
source: https://docs.canton.network/appdev/modules/m5-localnet-development
translated: 2026-06-15
status: done
tags: [appdev, modules, localnet, 로컬개발]
---

> **출처(원문)**: [LocalNet Development](https://docs.canton.network/appdev/modules/m5-localnet-development) · 번역일 2026-06-15

## 📌 개발자 노트
- **한 줄 요약**: LocalNet은 Docker Compose 기반으로 **내 개발 머신에 Canton Network <abbr class="gloss" title="어떤 노드·파티·키가 네트워크에 참여하는지를 정의하는 구성 정보">토폴로지</abbr> 전체를 미러링**한 로컬 네트워크(참여자 3·<abbr class="gloss" title="파티를 호스팅하고 그 파티의 컨트랙트 데이터를 저장하는 참여자 노드">밸리데이터</abbr> 3·PostgreSQL·웹앱). 공유망 없이 다자간 앱을 개발·테스트한다. 개발 생애주기 5단계, 기동/중지, 포트, 디버깅까지.
- **핵심 용어**: LocalNet, Docker Compose, app-provider/app-user/sv 역할, 프로필(profile), 포트 패턴, lnav
- **선행 개념**: [데모 실행하기](../quickstart/running-the-demo.md), [사전 요구사항·설치](../quickstart/prerequisites.md)

---

# LocalNet 개발

> cn-quickstart의 LocalNet을 주된 개발·테스트 환경으로 사용하기

LocalNet은 **내 개발 머신에 Canton Network 토폴로지를 미러링**한 Docker Compose 기반 로컬 네트워크다. 여러 밸리데이터, 월렛 서비스, PQS, 전체 <abbr class="gloss" title="글로벌 Synchronizer를 구동하는 오픈소스 애플리케이션 모음(SV·밸리데이터·월렛 등)">Splice</abbr> 애플리케이션을 제공한다 — 공유 네트워크에 연결하지 않고도 다자간 애플리케이션을 빌드·테스트하는 데 필요한 모든 것이다.

## LocalNet이 제공하는 것

LocalNet은 참여자 3개, 밸리데이터 3개, PostgreSQL 데이터베이스, 그리고 NGINX 게이트웨이 뒤의 여러 웹 애플리케이션(월렛·SV·scan)으로 이루어진 토폴로지를 제공한다. 각 밸리데이터는 Splice 생태계에서 고유한 역할을 한다:

* **app-provider** — 자기 애플리케이션을 운영하는 사용자용
* **app-user** — 앱 제공자의 앱을 쓰려는 사용자용
* **sv** — <abbr class="gloss" title="글로벌 Synchronizer를 운영하고 네트워크 거버넌스에 참여하는 노드">슈퍼 밸리데이터</abbr>. <abbr class="gloss" title="슈퍼 밸리데이터들이 공동 운영하는 Canton의 퍼블릭 조율(합의) 계층">글로벌 Synchronizer</abbr> 제공과 자동 시장 거래(AMT) 처리

LocalNet은 개발·테스트용으로 설계되었다. 프로덕션 용도가 아니다.

## 개발 생애주기

대부분의 개발 팀은 cn-quickstart로 다섯 단계를 거친다:

### 학습 단계 (1~2일)

cn-quickstart와의 첫 상호작용은 환경을 띄우고, 샘플 애플리케이션을 둘러보고, 아키텍처를 이해하는 데 집중한다. main에서 pull 받아 로컬 사본을 최신으로 유지하라:

```bash
git clone https://github.com/digital-asset/cn-quickstart.git
cd cn-quickstart

# 학습 중 정기 업데이트
git pull origin main
```

### 실험 단계 (1~2주)

구성을 수정하고, API를 탐색하고, <abbr class="gloss" title="다자간 워크플로를 위해 설계된 Canton의 스마트 컨트랙트 언어">Daml</abbr> 코드를 바꿔 통합 패턴을 테스트하기 시작한다. 변경을 선택적으로 가져올 수 있도록 upstream 추적을 설정하라:

```bash
git remote add upstream https://github.com/digital-asset/cn-quickstart.git
git checkout -b experiments
git fetch upstream
git merge upstream/main
```

### 개발 단계 (2~3주)

샘플과 나란히 자신만의 애플리케이션을 만들기 시작한다. 많은 개발자가 병렬 디렉토리에 자기 코드를 만든다:

```text
cn-quickstart/
├── quickstart/    # 원본 샘플 코드
│   ├── daml/
│   ├── backend/
│   └── frontend/
└── myapp/         # 당신의 애플리케이션 코드
    ├── daml/
    ├── backend/
    └── frontend/
```

`settings.gradle.kts`를 갱신해 두 프로젝트 구조를 포함시킨다. 로컬 환경 오버라이드에는 `.envrc.private`를 쓴다. cn-quickstart 구성을 확장하는 커스텀 Docker Compose 파일을 만든다.

### 분리 단계

애플리케이션 복잡도가 cn-quickstart 샘플을 넘어서면, 원본 코드에 대한 의존성을 제거한다. 샘플 디렉토리를 삭제하고, 빌드 파일을 갱신하고, upstream git remote를 제거한다:

```bash
git remote remove upstream
rm -rf quickstart/
# settings.gradle.kts, build.gradle.kts 등 갱신
```

### 지속적 업데이트

분리 후, cn-quickstart의 체인지로그를 주기적으로 검토해 도입할 만한 도구 개선·툴 버전 갱신을 <abbr class="gloss" title="이해관계자 밸리데이터가 트랜잭션이 유효함을 미디에이터에 응답하는 것(confirmation)">확인</abbr>한다. cn-quickstart는 의존성이 아니라 참고 자료가 된다.

## LocalNet 기동·중지

cn-quickstart를 쓴다면 Makefile이 Docker Compose 명령을 감싼다:

```bash
cd quickstart
make setup    # 최초 설정
make build    # Daml·백엔드 빌드
make start    # LocalNet 시작
make stop     # LocalNet 중지
```

Docker Compose를 직접 제어하려면 환경 변수 `LOCALNET_DIR`(LocalNet 디렉토리 경로)와 `IMAGE_TAG`(Splice 버전)를 설정한 뒤 다음을 사용한다:

```bash
# 모든 노드 시작
docker compose --env-file $LOCALNET_DIR/compose.env \
               --env-file $LOCALNET_DIR/env/common.env \
               -f $LOCALNET_DIR/compose.yaml \
               -f $LOCALNET_DIR/resource-constraints.yaml \
               --profile sv \
               --profile app-provider \
               --profile app-user up -d

# 모든 노드 중지
docker compose --env-file $LOCALNET_DIR/compose.env \
               --env-file $LOCALNET_DIR/env/common.env \
               -f $LOCALNET_DIR/compose.yaml \
               -f $LOCALNET_DIR/resource-constraints.yaml \
               --profile sv \
               --profile app-provider \
               --profile app-user down -v
```

Docker Compose 프로필(`--profile app-provider` 등)을 환경 변수(`APP_PROVIDER_PROFILE=on/off`)와 함께 써서 특정 밸리데이터를 비활성화하고 자원 사용을 줄일 수 있다.

## 포트와 서비스

포트는 밸리데이터 역할에 기반한 패턴을 따른다:

* **SV**: `4${PORT_SUFFIX}` (예: Ledger API는 `4901`)
* **App Provider**: `3${PORT_SUFFIX}` (예: Ledger API는 `3901`)
* **App User**: `2${PORT_SUFFIX}` (예: Ledger API는 `2901`)

주요 포트 접미사:

* `901` — 참여자 Ledger API (gRPC)
* `902` — 참여자 Admin API
* `975` — JSON API (HTTP)
* `903` — 밸리데이터 Admin API
* `900` — Canton HTTP 헬스 체크
* `961` — Canton gRPC 헬스 체크

웹 UI:

* App User 월렛: `http://wallet.localhost:2000`
* App Provider 월렛: `http://wallet.localhost:3000`
* SV UI: `http://sv.localhost:4000`
* <abbr class="gloss" title="네트워크의 공개 통계·활동을 보여주는 익스플로러(블록 익스플로러의 Canton판)">Scan</abbr> UI: `http://scan.localhost:4000`

> **참고:** 머신에서 `*.localhost` 도메인이 해석되지 않으면 `/etc/hosts`에 항목을 추가하라:
>
> ```text
> 127.0.0.1   scan.localhost
> 127.0.0.1   wallet.localhost
> 127.0.0.1   sv.localhost
> ```

## LocalNet으로 디버깅

### 로그 수집·보기

디버깅을 시작하는 가장 빠른 방법은 모든 로그를 한 번에 수집하는 것이다:

```bash
make capture-logs
```

수집된 로그 파일은 [lnav](https://lnav.org/)로 분석하라 — 여러 로그 형식을 다루고, 서비스 전반의 이벤트를 필터·검색·상관 분석할 수 있다.

### 라이브 로그 보기

```bash
# 모든 컨테이너
docker compose -f $LOCALNET_DIR/compose.yaml logs -f

# 특정 서비스
docker compose -f $LOCALNET_DIR/compose.yaml logs -f app-provider-participant

# 오류만 필터
docker compose -f $LOCALNET_DIR/compose.yaml logs -f 2>&1 | grep -i error
```

### Canton Console 접근

Canton Console은 참여자·<abbr class="gloss" title="Synchronizer 구성요소. 암호화된 메시지에 전체 순서·타임스탬프를 부여하고 참여자에게 전달">시퀀서</abbr>·<abbr class="gloss" title="Synchronizer 구성요소. 이해관계자들의 확인을 모아 트랜잭션 승인/거부를 판정">미디에이터</abbr> 노드를 직접 검사·수정할 수 있게 해준다:

```bash
docker compose --env-file $LOCALNET_DIR/compose.env \
               --env-file $LOCALNET_DIR/env/common.env \
               -f $LOCALNET_DIR/compose.yaml \
               -f $LOCALNET_DIR/resource-constraints.yaml \
               run --rm console
```

또는 cn-quickstart에서는 `make canton-console`.

### 흔한 문제

* **컨테이너가 시작 실패** — 가용 메모리를 확인하라. 세 밸리데이터를 모두 띄운 LocalNet은 상당한 자원을 요구한다. 쓰지 않는 프로필을 비활성화해 부하를 줄여라.
* **Scan UI에 라운드가 안 보임** — 시작 후 Scan UI에 데이터가 나타나기까지 몇 분 걸릴 수 있다. 초기 네트워크 부트스트래핑 중 예상되는 동작이다.
* **데이터베이스 연결 오류** — 단일 PostgreSQL 인스턴스가 모든 구성 요소를 처리한다. 다른 서비스보다 먼저 성공적으로 시작됐는지 확인하라.

## 다음 단계

* [테스트 전략](https://docs.canton.network/appdev/modules/m5-testing-strategies) — Canton 애플리케이션을 위한 테스트 피라미드와 접근법
* [배포 진행](https://docs.canton.network/appdev/modules/m5-deployment-progression) — LocalNet에서 DevNet·TestNet·MainNet으로 이동

<!-- nav:start -->

---

⬅️ **이전**: [블록체인 개발자를 위한 Canton (모듈 2)](m2-canton-for-ethereum-devs.md) ・ ➡️ **다음**: [Canton Network QuickStart](../quickstart/index.md)

<!-- nav:end -->
