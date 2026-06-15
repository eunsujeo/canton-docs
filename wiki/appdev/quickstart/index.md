---
title: Canton Network QuickStart
source: https://docs.canton.network/appdev/quickstart/index
translated: 2026-06-15
status: done
tags: [appdev, quickstart, 로컬개발]
---

> **출처(원문)**: [Canton Network QuickStart](https://docs.canton.network/appdev/quickstart/index) · 번역일 2026-06-15

## 📌 개발자 노트
- **한 줄 요약**: `cn-quickstart`로 내 로컬 PC에 **완전한 Canton Network 앱**(<abbr class="gloss" title="다자간 워크플로를 위해 설계된 Canton의 스마트 컨트랙트 언어">Daml</abbr> 모델 + Java 백엔드 + React 프론트 + 시뮬레이션 네트워크)을 띄워 보는 입문 프로젝트. 소프트웨어 라이선스 워크플로 데모로 다자간 <abbr class="gloss" title="여러 노드가 트랜잭션의 유효성·순서에 함께 동의하는 절차">합의</abbr>·제안-수락·토큰 이전 패턴을 익힌다.
- **핵심 용어**: LocalNet, cn-quickstart, 앱 제공자(App Provider)·앱 사용자(App User), Ledger API
- **선행 개념**: [모듈 1 — Canton 이해](../modules/m1-understanding-canton.md). 로컬 실행 준비는 다음 → [사전 요구사항·설치](prerequisites.md)

---

# Canton Network QuickStart

> cn-quickstart 프로젝트로 완전한 Canton Network 애플리케이션을 로컬에서 실행하기

[Canton Network QuickStart](https://github.com/digital-asset/cn-quickstart)(cn-quickstart)는 **내 로컬 머신에서 동작하는 Canton Network 셋업**을 제공하는 레퍼런스 애플리케이션이다. Daml 모델, Java 백엔드 서비스, React 프론트엔드, 시뮬레이션된 <abbr class="gloss" title="슈퍼 밸리데이터들이 공동 운영하는 Canton의 퍼블릭 조율(합의) 계층">글로벌 Synchronizer</abbr> 노드를 갖춘 로컬 Canton 샌드박스, 그리고 자신만의 애플리케이션을 빌드·테스트하기 위한 개발자 도구를 포함한다.

QuickStart는 **소프트웨어 라이선스 워크플로**를 시연한다 — 앱 제공자(App Provider)가 앱 사용자(App User)를 위한 라이선스를 만들고, 사용자는 갱신을 요청하고 <abbr class="gloss" title="트랜잭션 수수료와 밸리데이터 보상에 쓰이는 네이티브 유틸리티 토큰(CC)">Canton Coin</abbr>으로 결제할 수 있다. 이 워크플로는 프로덕션 Canton Network 애플리케이션에서 쓰게 될 핵심 패턴 — 다자간 합의, 제안-수락(propose-accept) 흐름, 토큰 이전 — 을 다룬다.

## 무엇을 얻나

QuickStart는 (LocalNet이라 부르는) 로컬 환경을 다음 구성으로 세팅한다:

* **시뮬레이션된 Canton Network** — <abbr class="gloss" title="글로벌 Synchronizer를 운영하고 네트워크 거버넌스에 참여하는 노드">슈퍼 밸리데이터</abbr> 노드, <abbr class="gloss" title="Synchronizer 구성요소. 암호화된 메시지에 전체 순서·타임스탬프를 부여하고 참여자에게 전달">시퀀서</abbr>, <abbr class="gloss" title="Synchronizer 구성요소. 이해관계자들의 확인을 모아 트랜잭션 승인/거부를 판정">미디에이터</abbr> 포함
* **앱 제공자(App Provider) 노드** — 라이선스 애플리케이션을 실행하는 <abbr class="gloss" title="파티를 호스팅하고 그 파티의 컨트랙트를 저장·실행하는 노드. 밸리데이터의 핵심 구성요소">참여자 노드</abbr>
* **앱 사용자(App User) 노드** — 월렛을 갖춘 별도의 참여자 노드
* **React 프론트엔드** — 제공자·사용자 두 역할 모두 지원
* **Java 백엔드** 서비스 — Ledger API 상호작용 처리
* **Canton Coin 월렛** — <abbr class="gloss" title="Synchronizer에 쓰기를 요청할 때 소비하는 자원. Canton Coin으로 비용을 지불">트래픽</abbr> 구매·결제 흐름용
* **로그 분석** — 디버깅·문제 해결을 위한 [lnav](https://docs.canton.network/appdev/quickstart/lnav)

## 이 섹션의 페이지

> - **[사전 요구사항·설치](prerequisites.md)**: 시스템 요건, 의존성, 단계별 설치
> - **[프로젝트 구조](https://docs.canton.network/appdev/quickstart/project-structure)**: QuickStart 프로젝트의 구성과 각 구성 요소의 역할
> - **[데모 실행하기](running-the-demo.md)**: 애플리케이션을 시작하고 라이선스 워크플로를 둘러보기

## 시작하기 전에

QuickStart는 모듈 1(Canton 이해)의 개념, 이상적으로는 모듈 3(Daml <abbr class="gloss" title="원장 위에서 규칙대로 자동 실행되는 코드화된 계약. Canton에선 Daml 템플릿으로 작성">스마트 컨트랙트</abbr>)에 대한 친숙함을 가정한다. 데모를 실행하는 데 Daml 전문가일 필요는 없지만, <abbr class="gloss" title="컨트랙트의 구조와 규칙(권한·초이스)을 정의하는 Daml 청사진">템플릿</abbr>·<abbr class="gloss" title="컨트랙트에서 수행 가능한 동작(권한이 부여된 당사자만 실행 가능)">초이스</abbr>·다자간 권한을 이해하면 애플리케이션이 무엇을 하는지 파악하는 데 도움이 된다.

> **참고:** QuickStart 저장소는 자신만의 Canton Network 애플리케이션을 빌드하기 위한 권장 출발점이다. 데모를 실행한 뒤, Daml 모델·백엔드·프론트엔드를 수정해 자신의 비즈니스 로직을 구현할 수 있다.

<!-- nav:start -->

---

⬅️ **이전**: [모듈 5 — LocalNet 개발 (LocalNet Development)](../modules/m5-localnet-development.md) ・ ➡️ **다음**: [사전 요구사항·설치 (Prerequisites and Installation)](prerequisites.md)

<!-- nav:end -->
