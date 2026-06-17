---
title: 데모 실행하기 (Running the Demo)
source: https://docs.canton.network/appdev/quickstart/running-the-demo
translated: 2026-06-15
status: done
tags: [appdev, quickstart, 데모, 로컬개발]
---

> **출처(원문)**: [Running the Demo](https://docs.canton.network/appdev/quickstart/running-the-demo) · 번역일 2026-06-15

## 📌 개발자 노트
- **한 줄 요약**: QuickStart 데모(소프트웨어 라이선스 앱)를 실제로 돌려보는 절차. 앱 설치 요청→수락→라이선스 생성→갱신 요청→Canton 월렛으로 결제(allocation)→갱신 완료까지. 더불어 Canton Console·<abbr class="gloss" title="다자간 워크플로를 위해 설계된 Canton의 스마트 컨트랙트 언어">Daml</abbr> Shell·CC <abbr class="gloss" title="네트워크의 공개 통계·활동을 보여주는 익스플로러(블록 익스플로러의 Canton판)">Scan</abbr>·SV UI로 내부를 들여다본다.
- **핵심 용어**: 앱 제공자/사용자, <abbr class="gloss" title="Canton Coin(CC)의 Daml/Scan상 기술적 이름. CC = Amulet">Amulet</abbr>·<abbr class="gloss" title="트랜잭션 수수료와 밸리데이터 보상에 쓰이는 네이티브 유틸리티 토큰(CC)">Canton Coin</abbr>(CC), <abbr class="gloss" title="탈중앙 Synchronizer 운영(Decentralized Synchronizer Operations) 파티. 슈퍼 밸리데이터들의 공동 거버넌스 주체">DSO</abbr> <abbr class="gloss" title="Canton에서 권한과 데이터 가시성의 주체가 되는 식별 가능한 참여 주체">파티</abbr>, allocation(할당), Canton Console, Daml Shell, PQS, CC Scan
- **선행 개념**: [사전 요구사항·설치](prerequisites.md). 관련 → [원장 모델](../../overview/learn/ledger-model.md)(제안-수락·조합 가능성)

---

# Canton Network 애플리케이션 Quickstart 데모 둘러보기

## 비즈니스 사례

Canton Network(CN) Quickstart는 CN 애플리케이션을 빌드·테스트·배포하는 개발 작업을 지원하는 스캐폴딩이다. 모든 CN 애플리케이션이 해결해야 하는 인프라 문제를 대신 풀어준다. CN Quickstart 애플리케이션을 사용하면 빌드 시스템·배포 구성·테스트 인프라 대신 **애플리케이션 자체를 만드는 데 집중**할 수 있다.

### 핵심 비즈니스 작업

Quickstart는 Canton 개발 패턴을 시연하기 위한 샘플 라이선스 앱을 제공한다. 이 앱에서 제공자는 자기 서비스에 대한 시간 기반 접근권을 판매한다. 사용자는 Canton Coin(CC)으로 결제하고 Canton 월렛으로 결제를 관리한다.

이 앱에는 네 당사자가 관여한다:

* 라이선스를 판매하는 **애플리케이션 제공자(Application Provider)**.
* 라이선스를 구매하는 **애플리케이션 사용자(Application User)**.
* [CC](https://www.canton.network/blog/canton-coin-a-canton-network-native-payment-application)를 사용해 결제를 처리하는 기반 **Amulet** 토큰 시스템.
* Amulet 결제 시스템을 운영하는 **DSO 파티**(Decentralized <abbr class="gloss" title="상태를 저장하지 않고 트랜잭션 합의·순서를 조율하는 Canton 구성요소">Synchronizer</abbr> Operations Party). CN에서는 이것이 <abbr class="gloss" title="글로벌 Synchronizer를 운영하고 네트워크 거버넌스에 참여하는 노드">슈퍼 밸리데이터</abbr>다.

애플리케이션은 다음 절차로 라이선스를 발급한다:

#### 라이선스 발급

제공자가 온보딩된 사용자를 위해 새 라이선스를 만든다. 라이선스는 만료된 상태로 시작하며, 사용 전 갱신이 필요하다.

#### 라이선스 갱신 요청

제공자가 갱신 요청을 만들어 사용자에게 결제 요청을 생성한다. 매칭되는 CC 결제 요청이 <abbr class="gloss" title="거래·컨트랙트가 기록되는 장부. Canton에선 활성 컨트랙트의 모음">원장</abbr>에 생성된다.

#### 라이선스 갱신 결제

사용자가 Canton 월렛으로 결제를 승인하면, 수락된 결제 <abbr class="gloss" title="원장에 기록되는 불변 데이터 단위. 상태 변경은 새 컨트랙트 생성으로 표현됨">컨트랙트</abbr>가 원장에 생성된다.

#### 라이선스 갱신

제공자가 수락된 결제를 처리하고 새 만료일로 라이선스를 갱신한다.

## 개요

이 절은 CN App Quickstart 안에서 Canton Network(CN) 비즈니스 작업에 친숙해지도록 돕는다. App Quickstart 애플리케이션은 당신의 팀이 비즈니스 요구에 맞게 확장하도록 의도되었다. App Quickstart에 익숙해지면 기술 선택과 애플리케이션 설계를 검토해 어떤 변경이 필요한지 판단하라. 기술·설계 결정은 궁극적으로 당신에게 달려 있다.

오류를 발견하면 Digital Asset 담당자에게 연락하라.

## 사전 요구사항

이 시연을 시작하기 전에 [CN App Quickstart](prerequisites.md)를 설치하라.

## 워크스루(Walkthrough)

CN App Quickstart는 비즈니스 요구에 따라 인가(authorization)를 켜거나 끄고 실행할 수 있다. `quickstart` 하위 디렉토리에서 `make setup` 명령으로 인가를 토글한다. `make setup`은 Observability·OAUTH2 활성화 여부와 파티 힌트를 묻는다. 이 데모에서는 `TEST MODE`를 끄고, 기본 파티 힌트를 쓰며, OAUTH2 활성/비활성 두 경우를 모두 보여준다. OAUTH2가 차이를 만드는 지점에서는 두 경로를 차례로 표시하니, 자기 경로를 따라가고 다른 쪽은 무시하면 된다. Observability는 켜도 되지만 이 데모에 필수는 아니다.

**경로 선택:**

OAUTH2 **없이** `make setup`:

![인증 없는 make setup](https://mintcdn.com/cantonfoundation/zmlOjLpKuDjnaObr/images/docs_website/make-setup-noauth.png?fit=max&auto=format&n=zmlOjLpKuDjnaObr&q=85&s=1408916657066dfd2af2a46b8d3eb678)

OAUTH2 **포함** `make setup`:

![인증 포함 make setup](https://mintcdn.com/cantonfoundation/zmlOjLpKuDjnaObr/images/docs_website/make-setup-with-oauth.png?fit=max&auto=format&n=zmlOjLpKuDjnaObr&q=85&s=d9e3d88dd7c5285588b698b1ce54a40e)

### Quickstart 빌드

<iframe width="560" height="315" src="https://www.youtube.com/embed/xsuMDLED6gI" title="Build Quickstart" frameBorder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowFullScreen></iframe>

App Quickstart 빌드·시작:

```bash
   make build; make start
```

시크릿 브라우저를 열고 다음으로 이동:

`app-provider.localhost:3000`

또는 터미널에서 quickstart/ 로부터 실행:

```bash
make open-app-ui
```

> **참고:** Safari 사용자는 `/etc/hosts`에서 `app-provider` 서브도메인을 수동으로 매핑해야 할 수 있다. 터미널 명령 `sudo nano /etc/hosts`로 다음을 추가하라:
>
> `127.0.0.1       app-provider.localhost`
>
> 이는 시스템이 `app-provider.localhost`를 로컬 머신으로 해석하게 한다. 저장하고 파일을 닫은 뒤 Safari를 재시작한다.

### 로그인

**OAUTH2 비활성화**

OAUTH2가 **비활성화**되면 홈페이지에 단순 로그인 필드가 나온다. User 필드에 "app-provider"를 입력해 `AppProvider`로 로그인하는 것부터 시작한다.

![인증 없는 CN App Quickstart 로그인 화면](https://mintcdn.com/cantonfoundation/QAGFSphBsRkeZIBi/images/docs_website/01-login-app-qs-noauth.png?fit=max&auto=format&n=QAGFSphBsRkeZIBi&q=85&s=d59ab8fc8fac6a24e0f7f9b080a865cd)

**OAUTH2 활성화**

OAUTH2가 **활성화**되면 홈페이지가 Keycloak의 OAuth 2.0 포털로 로그인하라고 안내한다:

![인증 포함 CN App Quickstart 로그인 화면](https://mintcdn.com/cantonfoundation/QAGFSphBsRkeZIBi/images/docs_website/01-login-app-qs-auth.png?fit=max&auto=format&n=QAGFSphBsRkeZIBi&q=85&s=3e86e1e6eceb3ab42a0c54f69b011a6e)

`AppProvider`의 사용자명은 "app-provider", 비밀번호는 "abc123"(모두 소문자)임을 기억해 두라.

Keycloak으로 `app-provider`로 로그인한다.

로그인 자격증명 입력: 사용자명 app-provider, 비밀번호 abc123

![AppProvider 로그인 화면](https://mintcdn.com/cantonfoundation/zmlOjLpKuDjnaObr/images/docs_website/login-app-provider-view.png?fit=max&auto=format&n=zmlOjLpKuDjnaObr&q=85&s=0ebbacbedf9bb9f6e86c27a3068b5d33)

### App Installs 메뉴

로그인하면 메뉴에서 **AppInstalls**를 선택한다.

![App Installs 화면](https://mintcdn.com/cantonfoundation/zmlOjLpKuDjnaObr/images/docs_website/qs-demo-app-installs-view.png?fit=max&auto=format&n=zmlOjLpKuDjnaObr&q=85&s=4ceb4f09666c5dc802ee454ba0ba9b47)

터미널을 열어 앱 설치 요청을 만든다.

`/quickstart/`에서 실행:

```bash
make create-app-install-request
```

이 명령은 참여자를 대신해 App Installation Request를 생성한다.

![App 설치 요청](https://mintcdn.com/cantonfoundation/QAGFSphBsRkeZIBi/images/docs_website/04-create-install-req.png?fit=max&auto=format&n=QAGFSphBsRkeZIBi&q=85&s=26967c3281af1c82122ec6ef2b9b6869)

> **참고:** 머신이 `LocalNet`을 <abbr class="gloss" title="참여자 노드가 파티를 대신해 원장에서 활동(컨트랙트 저장·트랜잭션 제출·확인)해 주는 것. 로컬 파티는 키까지 노드가 관리하고, 외부 파티는 제출 키를 파티 자신이 보유(노드는 중계)">호스팅</abbr>하기에 충분치 않거나 docker 컨테이너가 응답하지 않으면, 응답에 상태 코드 404 또는 000으로 실패가 표시될 수 있다(아래 이미지처럼). Docker 메모리 한도를 최소 8GB로 올리면 `LocalNet` 컨테이너가 제대로 동작할 것이다.

![App 설치 요청 오류](https://mintcdn.com/cantonfoundation/QAGFSphBsRkeZIBi/images/docs_website/05-error-app-install.png?fit=max&auto=format&n=QAGFSphBsRkeZIBi&q=85&s=f69a71143e15df482c1577bac0adf83e)

브라우저로 돌아간다.

### AppInstallRequest

설치 요청이 목록에 나타난다.

**Accept**를 클릭한다.

![요청 수락](https://mintcdn.com/cantonfoundation/QAGFSphBsRkeZIBi/images/docs_website/accept-awaiting-request.png?fit=max&auto=format&n=QAGFSphBsRkeZIBi&q=85&s=9343412c86851e6732bb53842df08640)

`AppInstallRequest`가 수락된다.

![수락된 요청](https://mintcdn.com/cantonfoundation/zmlOjLpKuDjnaObr/images/docs_website/success-accepted-appinstallrequest.png?fit=max&auto=format&n=zmlOjLpKuDjnaObr&q=85&s=b9e1db88000687ae2729bcb430ed70e6)

동작이 Cancel과 Create license로 갱신된다.

### 라이선스 생성

**Create License**를 클릭한다. 라이선스가 생성되고 "# Licenses" 필드가 갱신된다.

![라이선스 생성](https://mintcdn.com/cantonfoundation/QAGFSphBsRkeZIBi/images/docs_website/created-license.png?fit=max&auto=format&n=QAGFSphBsRkeZIBi&q=85&s=35f926610b07bc1fef45d0be2d4ee4dc)

다음으로 Licenses 메뉴로 가서 **Renewals**를 선택한다.

![Licenses 화면](https://mintcdn.com/cantonfoundation/zmlOjLpKuDjnaObr/images/docs_website/new-license-select-renewals.png?fit=max&auto=format&n=zmlOjLpKuDjnaObr&q=85&s=95ec9e7abab4f3b476744338bec788c2)

라이선스를 갱신하는 옵션이 있는 "License Renewal Request" 모달이 열린다.

![라이선스 갱신 요청 모달](https://mintcdn.com/cantonfoundation/zmlOjLpKuDjnaObr/images/docs_website/license-renewal-request-modal.png?fit=max&auto=format&n=zmlOjLpKuDjnaObr&q=85&s=d886889cfb347fbfa47f6d99ab0ff5a9)

**New**를 클릭해 "Renew License" 모달을 연다.

![라이선스 갱신 모달](https://mintcdn.com/cantonfoundation/zmlOjLpKuDjnaObr/images/docs_website/renew-license-modal.png?fit=max&auto=format&n=zmlOjLpKuDjnaObr&q=85&s=29534a7fc893b80cded1f139b76e48f3)

모달에서 라이선스 갱신 일수, 수수료, 라이선스 준비 시간, 정산 시간을 설정한다. 진행하려면 설명을 추가해야 한다.

"Prepare in"은 발신자(app-user)가 그 시각 전에 할당(allocation)을 수락해야 함을 알리는 표시다. "Settle in"은 제공자가 `completeRenewal`을 해야 하는 시간이다. 그 시간이 지나면 할당은 만료된다.

**Issue License Renewal Request**를 클릭한다.

![새 라이선스 갱신 요청](https://mintcdn.com/cantonfoundation/zmlOjLpKuDjnaObr/images/docs_website/new-license-renewal-request.png?fit=max&auto=format&n=zmlOjLpKuDjnaObr&q=85&s=265a21249aa5bf1a08da03a16d6a45a5)

Daml 컨트랙트에 따라, 라이선스는 만료 상태로 생성된다. 라이선스를 활성화하려면 갱신 결제 요청이 발급되어야 한다.

### 결제하기

결제하려면 Canton 월렛 [http://wallet.localhost:2000/allocations](http://wallet.localhost:2000/allocations)로 이동해, 프롬프트가 뜨면 `app-user`로 로그인한다.

월렛 위치는 다음으로 찾을 수 있다:

1. [LocalNet 애플리케이션 UI 레퍼런스](https://docs.canton.network/sdks-tools/development-tools/localnet#application-uis) 읽기.
2. App Provider의 "Tenants" 메뉴로 이동.

![AppProvider Tenants 메뉴](https://mintcdn.com/cantonfoundation/QAGFSphBsRkeZIBi/images/docs_website/app-provider-tenants.png?fit=max&auto=format&n=QAGFSphBsRkeZIBi&q=85&s=977310daf3ed1412cc3486604d2af9db)

3. 앱에 `app-user`로 로그인해 Licenses 메뉴로 이동한 뒤 **Renewals** 동작 클릭.

![AppUser Licenses 메뉴](https://mintcdn.com/cantonfoundation/QAGFSphBsRkeZIBi/images/docs_website/app-user-licenses-menu.png?fit=max&auto=format&n=QAGFSphBsRkeZIBi&q=85&s=169fcbca3a2c61ed799c28818cb1773d)

프롬프트가 뜨면 CC 월렛에 `app-user`로 로그인한다.

![Canton Coin 월렛 로그인](https://mintcdn.com/cantonfoundation/QAGFSphBsRkeZIBi/images/docs_website/canton-coin-wallet-app-user-log-in.png?fit=max&auto=format&n=QAGFSphBsRkeZIBi&q=85&s=590880b15dfa7537790f4057342d7cbd)

월렛에 CC가 없으면 금액을 입력하고 **TAP**을 클릭한다. 잠시 후 사용 가능 잔액이 자동 갱신된다.

![CC 받기(Tap)](https://mintcdn.com/cantonfoundation/zmlOjLpKuDjnaObr/images/docs_website/tap-canton-wallet.png?fit=max&auto=format&n=zmlOjLpKuDjnaObr&q=85&s=245af052dabbfd2e8cd7de3c58857cbb)

CC 월렛이 채워지면 "Allocations" 메뉴로 이동해, "Allocate before" 시간이 만료되기 전에 "Allocation Request"를 수락한다.

![CC 월렛 할당 수락](https://mintcdn.com/cantonfoundation/QAGFSphBsRkeZIBi/images/docs_website/canton-coin-wallet-allocations-menu.png?fit=max&auto=format&n=QAGFSphBsRkeZIBi&q=85&s=6d98ac7d9e67b87babc946dc0928f7b0)

할당 요청이 수락되면 새 "Allocations" 섹션이 나타난다. 이 섹션은 `licenseFeePayment` 정보를 보여준다.

![CC 월렛 수락된 할당](https://mintcdn.com/cantonfoundation/QAGFSphBsRkeZIBi/images/docs_website/canton-coin-wallet-accepted-allocation.png?fit=max&auto=format&n=QAGFSphBsRkeZIBi&q=85&s=0305dabc187ee90a1a7c7c6b09cda92a)

### 라이선스 갱신

`AppProvider`로 Quickstart에 돌아간다. Licenses 메뉴에서 **Renewals**를 선택한다. License Renewals Request 모달이 열린다. 초록색 **Complete Renewal** 버튼을 클릭한다.

![결제 후 갱신 완료](https://mintcdn.com/cantonfoundation/QAGFSphBsRkeZIBi/images/docs_website/app-provider-complete-renewal-after-payment.png?fit=max&auto=format&n=QAGFSphBsRkeZIBi&q=85&s=c324401b73bb9ee2cbd66c6a158d27c8)

라이선스 갱신이 성공적으로 완료되었다는 <abbr class="gloss" title="이해관계자 밸리데이터가 트랜잭션이 유효함을 미디에이터에 응답하는 것(confirmation)">확인</abbr>이 나타난다.

![결제 후 갱신 성공](https://mintcdn.com/cantonfoundation/zmlOjLpKuDjnaObr/images/docs_website/license-renewal-completed-successfully.png?fit=max&auto=format&n=zmlOjLpKuDjnaObr&q=85&s=f668dae8d5b6df522fed0a9f25777749)

`AppProvider`에서 로그아웃하고 `AppUser`로 로그인한다.

**OAUTH2 비활성화**

OAUTH2가 비활성화면 그냥 `app-user`로 로그인한다.

![인증 없는 AppUser 로그인 화면](https://mintcdn.com/cantonfoundation/zmlOjLpKuDjnaObr/images/docs_website/login-app-user-noauth.png?fit=max&auto=format&n=zmlOjLpKuDjnaObr&q=85&s=0066a63f9fea2644e82cf1c089f81434)

**OAUTH2 활성화**

OAUTH2가 활성화면 app-user 사용자명과 비밀번호로 로그인한다.

![로그인 화면](https://mintcdn.com/cantonfoundation/QAGFSphBsRkeZIBi/images/docs_website/01-login-app-qs-auth.png?fit=max&auto=format&n=QAGFSphBsRkeZIBi&q=85&s=3e86e1e6eceb3ab42a0c54f69b011a6e)

`AppUser`로 사용자명 "app-user", 비밀번호 "abc123"으로 로그인한다.

![AppUser 로그인 화면](https://mintcdn.com/cantonfoundation/QAGFSphBsRkeZIBi/images/docs_website/appuser-auth-login-view.png?fit=max&auto=format&n=QAGFSphBsRkeZIBi&q=85&s=b312b838303aa6e9ec67bde4630dff8b)

이제 AppInstall이 수락됨으로 표시된다.

![수락된 AppInstall](https://mintcdn.com/cantonfoundation/QAGFSphBsRkeZIBi/images/docs_website/accepted-app-install.png?fit=max&auto=format&n=QAGFSphBsRkeZIBi&q=85&s=c0f3be69a014c5946c9e0281ae6c02e4)

라이선스가 활성으로 표시된다.

![활성 라이선스](https://mintcdn.com/cantonfoundation/QAGFSphBsRkeZIBi/images/docs_website/app-user-license-active.png?fit=max&auto=format&n=QAGFSphBsRkeZIBi&q=85&s=2eba63df270f01f4f51adf922921d238)

축하한다. Canton 월렛의 결제 할당으로 라이선스를 성공적으로 생성·활성화했다!

## Canton Console

<iframe width="560" height="315" src="https://www.youtube.com/embed/zADHja_8TSg" title="Canton Console" frameBorder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowFullScreen></iframe>

Canton Console은 실행 중인 애플리케이션 원장에 연결한다. 콘솔을 통해 개발자는 UI를 우회해 CN과 더 직접적으로 상호작용할 수 있다. 예를 들어 Canton Console에서 참여자에 연결해 그 참여자의 위치와 Synchronizer 도메인을 볼 수 있다.

`quickstart/` 디렉토리에서 터미널로 Canton Console을 활성화한다. 실행:

```bash
make canton-console
```

콘솔이 시작되면 `participants`와 `participants.all` 명령을 차례로 실행한다.

```
participants
```

참여자의 상세 분류를 반환한다.

![원장 내 참여자 위치](https://mintcdn.com/cantonfoundation/QAGFSphBsRkeZIBi/images/docs_website/canton-console-participants.png?fit=max&auto=format&n=QAGFSphBsRkeZIBi&q=85&s=8c3d1cea96249b903b88c0da306ec93d)

```
participants.all
```

모든 참여자 참조 목록을 보여준다.

![참여자 Synchronizer](https://mintcdn.com/cantonfoundation/QAGFSphBsRkeZIBi/images/docs_website/canton-console-participants-all.png?fit=max&auto=format&n=QAGFSphBsRkeZIBi&q=85&s=df883230ed833027274e2ceea8f4fc64)

`LocalNet`에서는 나열된 참여자 중 아무에게나 연결할 수 있다. 앱 사용자의 <abbr class="gloss" title="파티를 호스팅하고 그 파티의 컨트랙트 데이터를 저장하는 참여자 노드">밸리데이터</abbr>에 연결:

`app-user`

![App User](https://mintcdn.com/cantonfoundation/QAGFSphBsRkeZIBi/images/docs_website/app-user.png?fit=max&auto=format&n=QAGFSphBsRkeZIBi&q=85&s=b01573fcbc32b72885075c33152069df)

오류가 나면 백틱(`)을 썼는지 다시 확인하라.

앱 제공자는 다음으로 연결할 수 있다:

`app-provider`

![App Provider](https://mintcdn.com/cantonfoundation/QAGFSphBsRkeZIBi/images/docs_website/app-provider.png?fit=max&auto=format&n=QAGFSphBsRkeZIBi&q=85&s=4a4bcd7454bf593f2f4c118b97552a87)

<abbr class="gloss" title="슈퍼 밸리데이터들이 공동 운영하는 Canton의 퍼블릭 조율(합의) 계층">글로벌 Synchronizer</abbr>를 시뮬레이션하는 슈퍼 밸리데이터에 연결:

`sv`

![슈퍼 밸리데이터](https://mintcdn.com/cantonfoundation/zmlOjLpKuDjnaObr/images/docs_website/sv.png?fit=max&auto=format&n=zmlOjLpKuDjnaObr&q=85&s=43495c2192db25d7959eb0f0eac8b951)

Canton Console은 Canton Network 밸리데이터의 상태(health)를 표시하는 진단 도구도 제공한다:

```
health.status
```

![자기 핑](https://mintcdn.com/cantonfoundation/zmlOjLpKuDjnaObr/images/docs_website/health-status.png?fit=max&auto=format&n=zmlOjLpKuDjnaObr&q=85&s=51203c8b4855d2105fb450166523df9f)

## Daml Shell

<iframe width="560" height="315" src="https://www.youtube.com/embed/bwUyYEFCo5w" title="Daml Shell" frameBorder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowFullScreen></iframe>

Daml Shell은 애플리케이션 제공자 참여자의 실행 중인 PQS 데이터베이스에 연결한다. 셸에서 자산과 그 상세를 실시간으로 볼 수 있다.

터미널에서 quickstart/ 로부터 셸을 실행:

```bash
make shell
```

데이터를 보려면 다음 명령을 실행한다:

```
active
```

고유 식별자와 자산 수를 보여준다:

![활성 식별자](https://mintcdn.com/cantonfoundation/QAGFSphBsRkeZIBi/images/docs_website/28-shell-ids.png?fit=max&auto=format&n=QAGFSphBsRkeZIBi&q=85&s=7e70568b90c6973178010c24d3d092bf)

```
active quickstart-licensing:Licensing.License:License
```

라이선스 상세를 나열한다.

![라이선스 상세](https://mintcdn.com/cantonfoundation/QAGFSphBsRkeZIBi/images/docs_website/29-license-details.png?fit=max&auto=format&n=QAGFSphBsRkeZIBi&q=85&s=96fcfbcf24fefeed145f2b0204786703)

```
active quickstart-licensing:Licensing.License:LicenseRenewalRequest
```

라이선스 갱신 요청 상세를 표시한다.

![라이선스 갱신 요청 상세](https://mintcdn.com/cantonfoundation/QAGFSphBsRkeZIBi/images/docs_website/active-quickstart-appinstallrequest.png?fit=max&auto=format&n=QAGFSphBsRkeZIBi&q=85&s=3b2865a66adc42d69afd314bac8df094)

```
archives quickstart-licensing:Licensing.AppInstall:AppInstallRequest
```

<abbr class="gloss" title="컨트랙트를 소비해 비활성으로 만드는 것(archive). 보관된 컨트랙트는 더 이상 쓸 수 없음">보관</abbr>된 라이선스를 보여준다.

![보관된 라이선스](https://mintcdn.com/cantonfoundation/QAGFSphBsRkeZIBi/images/docs_website/30-archive-licenses.png?fit=max&auto=format&n=QAGFSphBsRkeZIBi&q=85&s=150ef56808c53ccf89334ef49c426e3b)

## Canton Coin Scan

CC Scan 웹 UI를 [http://scan.localhost:4000/](http://scan.localhost:4000/)에서 둘러본다.

기본 활동 <abbr class="gloss" title="한 트랜잭션을 당사자별로 나눈 조각. 각 당사자는 자기 권한에 해당하는 뷰(자기 몫)만 받아 본다">뷰</abbr>는 총 CC 잔액과 밸리데이터 보상을 보여준다.

![CC 잔액](https://mintcdn.com/cantonfoundation/QAGFSphBsRkeZIBi/images/docs_website/36-cc-balance.png?fit=max&auto=format&n=QAGFSphBsRkeZIBi&q=85&s=93baef92a8fb40484bbd32259f47bee3)

**Network Info** 메뉴를 선택하면 SV 식별 정보를 볼 수 있다.

![활성 SV들](https://mintcdn.com/cantonfoundation/QAGFSphBsRkeZIBi/images/docs_website/34-active-svs.png?fit=max&auto=format&n=QAGFSphBsRkeZIBi&q=85&s=93baeac098a8ffb96118ad7bd82289dd)

Validators 메뉴는 로컬 밸리데이터가 SV에 등록되었음을 보여준다.

![등록된 밸리데이터](https://mintcdn.com/cantonfoundation/QAGFSphBsRkeZIBi/images/docs_website/37-registered-validator.png?fit=max&auto=format&n=QAGFSphBsRkeZIBi&q=85&s=18513ea59e63c153cdb7efc7d7ed9111)

## Observability 대시보드

> **참고:** App Quickstart가 개정 중인 동안 Observability가 동작하지 않을 수 있다.

웹 브라우저에서 [http://localhost:3030/dashboards](http://localhost:3030/dashboards)로 이동해 관측성 대시보드를 본다. **Quickstart - consolidated logs**를 선택한다.

![관측성 대시보드](https://mintcdn.com/cantonfoundation/QAGFSphBsRkeZIBi/images/docs_website/38-obs-dash.png?fit=max&auto=format&n=QAGFSphBsRkeZIBi&q=85&s=d2a79818718bd41e4efad50afdc757ea)

기본 뷰는 모든 서비스의 실시간 스트림을 보여준다.

![서비스 스트림](https://mintcdn.com/cantonfoundation/QAGFSphBsRkeZIBi/images/docs_website/39-service-stream.png?fit=max&auto=format&n=QAGFSphBsRkeZIBi&q=85&s=342cbdb1ea90bceed4b57c9c49941a0b)

서비스 필터를 "All"에서 "participant"로 바꾸면 참여자 로그를 볼 수 있다. 로그 항목을 선택하면 상세를 볼 수 있다.

![로그 항목 상세](https://mintcdn.com/cantonfoundation/QAGFSphBsRkeZIBi/images/docs_website/40-log-entry-details.png?fit=max&auto=format&n=QAGFSphBsRkeZIBi&q=85&s=b40da7d84eb5760da8d9b21866333f6a)

## SV UI

SV 웹 UI는 [http://sv.localhost:4000/](http://sv.localhost:4000/)로 이동한다. SV 뷰는 밸리데이터에서 직접 가져온 데이터를 탐색하기 쉬운 GUI로 보여준다.

'sv'로 로그인한다.

![SV UI 로그인](https://mintcdn.com/cantonfoundation/QAGFSphBsRkeZIBi/images/docs_website/33-sv-ui-login.png?fit=max&auto=format&n=QAGFSphBsRkeZIBi&q=85&s=56f28dbeeb635a41a95fafae9a745bc7)

UI는 SV에 관한 정보를 보여주고 활성 SV들을 나열한다.

![활성 SV들](https://mintcdn.com/cantonfoundation/QAGFSphBsRkeZIBi/images/docs_website/34-active-svs.png?fit=max&auto=format&n=QAGFSphBsRkeZIBi&q=85&s=93baeac098a8ffb96118ad7bd82289dd)

Validator Onboarding 메뉴에서 밸리데이터 온보딩 시크릿을 생성할 수 있다.

![밸리데이터 온보딩](https://mintcdn.com/cantonfoundation/QAGFSphBsRkeZIBi/images/docs_website/35-validator-onboarding.png?fit=max&auto=format&n=QAGFSphBsRkeZIBi&q=85&s=f1d1f3f9f901d215d3c33f1bb1a09d50)

## 다음 단계

CN App Quickstart에서 비즈니스 작업을 완료했고, Canton Console과 Daml Shell의 기초를 익혔다. CN App Quickstart 코드베이스를 둘러보고 비즈니스 요구에 맞게 수정해 보길 권한다. [App Quickstart 프로젝트 구조](https://docs.canton.network/appdev/quickstart/project-structure)나 [모듈 4: 애플리케이션 빌드](https://docs.canton.network/appdev/modules/m4-building-apps-intro)의 애플리케이션 개발 모듈을 더 살펴보면 좋다.

<!-- nav:start -->

---

⬅️ **이전**: [사전 요구사항·설치 (Prerequisites and Installation)](prerequisites.md) ・ ➡️ **다음**: [원자적 DvP는 Canton만 되나? — 원자성·잠금·조합성, "이더도 되잖아?"에 답하기](../../notes/atomic-dvp-real-differentiator.md)

<!-- nav:end -->
