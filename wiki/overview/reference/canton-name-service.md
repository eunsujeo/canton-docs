---
title: Canton 네임 서비스 (CNS)
source: https://docs.canton.network/overview/reference/canton-name-service
translated: 2026-06-15
status: done
tags: [overview, reference, CNS, 네이밍]
---

> **출처(원문)**: [Canton Name Service](https://docs.canton.network/overview/reference/canton-name-service) · 번역일 2026-06-15

## 📌 개발자 노트
- **한 줄 요약**: CNS는 사람이 읽을 수 있는 이름을 <abbr class="gloss" title="Canton에서 권한과 데이터 가시성의 주체가 되는 식별 가능한 참여 주체">파티</abbr> 식별자에 매핑한다(인터넷의 DNS와 유사). 이름 형식, 등록(구독 결제 모델)·갱신·이름 해석(정방향/역방향), <abbr class="gloss" title="슈퍼 밸리데이터들이 공동 운영하는 Canton의 퍼블릭 조율(합의) 계층">글로벌 Synchronizer</abbr> 저장(<abbr class="gloss" title="다자간 워크플로를 위해 설계된 Canton의 스마트 컨트랙트 언어">Daml</abbr> <abbr class="gloss" title="원장에 기록되는 불변 데이터 단위. 상태 변경은 새 컨트랙트 생성으로 표현됨">컨트랙트</abbr>), API 레퍼런스.
- **핵심 용어**: CNS·ANS(Amulet Name Service), `.unverified.cns`, <abbr class="gloss" title="탈중앙 Synchronizer 운영(Decentralized Synchronizer Operations) 파티. 슈퍼 밸리데이터들의 공동 거버넌스 주체">DSO</abbr> 파티, AnsRules/AnsEntry/AnsEntryContext, Scan API
- **선행 개념**: [핵심 개념](../understand/core-concepts.md), [Canton Coin](../understand/canton-coin.md).

---

# Canton 네임 서비스 (CNS)

> Canton Network에서 파티 식별자에 매핑되는 사람이 읽을 수 있는 이름

Canton 네임 서비스(Canton Name Service, CNS)는 사람이 읽을 수 있는 이름을 Canton Network의 파티 식별자에 매핑한다. 인터넷의 DNS와 유사한 기능을 한다: `auth0_007c675a429eaf831f0991308d85::12201abe669f...` 같은 길고 불투명한 파티 ID 대신, `alice.unverified.cns` 같은 이름을 공유할 수 있다.

CNS는 글로벌 <abbr class="gloss" title="상태를 저장하지 않고 트랜잭션 합의·순서를 조율하는 Canton 구성요소">Synchronizer</abbr> 위의 Daml 컨트랙트 집합으로 구현되며 DSO 파티가 거버넌스한다. 기반 코드는 [Splice](https://github.com/canton-network/splice) 코드베이스에서 Amulet Name Service(ANS)라 불린다.

## 이름 형식

CNS 엔트리 이름은 `<선택한-이름>.unverified.cns` 패턴을 따른다. 접미사 `.unverified.cns`는 모든 사용자 등록 이름에 붙는다. `unverified` 레이블은 등록자에 대한 신원 검증이 수행되지 않았음을 나타낸다 — 월렛과 충분한 <abbr class="gloss" title="트랜잭션 수수료와 밸리데이터 보상에 쓰이는 네이티브 유틸리티 토큰(CC)">Canton Coin</abbr>이 있는 누구나 이름을 등록할 수 있다.

DSO 자신은 특수 엔트리 `dso.cns`를 보유하며, 이는 만료가 없고 컨트랙트 ID도 없다(표준 등록 흐름이 아니라 DSO가 직접 제공).

## 등록 작동 방식

CNS 엔트리 등록은 Daml 구독 결제 모델 위에 구축된 다단계 과정이다:

1. 사용자가 Validator App의 ANS API의 **POST** `/v0/entry/create` 엔드포인트를 호출하며 `name`, `url`, `description`을 제공한다.
2. Validator App이 `AnsRules_RequestEntry` <abbr class="gloss" title="컨트랙트에서 수행 가능한 동작(권한이 부여된 당사자만 실행 가능)">초이스</abbr>를 실행해 `AnsEntryContext` 컨트랙트와 `SubscriptionRequest` 컨트랙트를 생성한다.
3. 사용자가 월렛을 통해 구독 요청을 수락하면, Canton Coin으로 초기 결제가 트리거된다.
4. DSO 자동화가 초기 결제를 수집(`AnsEntryContext_CollectInitialEntryPayment`)하고, DSO로 이전된 Canton Coin을 소각(burn)하며, `AnsEntry` 컨트랙트를 생성한다.

엔트리 수수료와 수명은 `AnsRules` 컨트랙트의 `AnsRulesConfig`에 구성된다. 결제는 DSO 파티로 가서 소각된다 — 재분배되지 않는다.

## 갱신

CNS 엔트리는 만료된다. 각 엔트리는 `expiresAt` 타임스탬프를 가지며, 소유자는 이름을 유지하려면 그 전에 갱신해야 한다.

갱신은 같은 구독 결제 메커니즘을 쓴다. 갱신 결제가 도래하면, 사용자가 충분한 Canton Coin을 갖고 자동 갱신을 활성화했다면 월렛 자동화가 이를 자동 처리할 수 있다. 그러면 DSO 자동화가 `AnsEntryContext_CollectEntryRenewalPayment`를 실행해 결제를 소각하고 `expiresAt`를 구성된 `entryLifetime` 간격만큼 연장한다.

엔트리가 만료 전에 갱신되지 않으면, 어떤 <abbr class="gloss" title="컨트랙트의 주된 권한자. 생성·보관(소비)에 반드시 동의해야 하는 파티">서명자</abbr>든 `AnsEntry_Expire`를 실행해 <abbr class="gloss" title="컨트랙트를 소비해 비활성으로 만드는 것(archive). 보관된 컨트랙트는 더 이상 쓸 수 없음">보관</abbr>할 수 있다.

## 이름 해석 (Name Resolution)

CNS는 양방향 해석을 지원한다 — 이름→파티, 파티→이름(정방향·역방향 DNS와 유사).

Scan API는 조회를 위한 세 가지 공개 엔드포인트를 제공한다:

* **GET** `/v0/ans-entries/by-name/{name}` — 정확한 이름을 소유 파티 ID를 포함한 엔트리로 해석
* **GET** `/v0/ans-entries/by-party/{party}` — 파티 ID를 그 CNS 엔트리로 해석
* **GET** `/v0/ans-entries?name_prefix=<prefix>&page_size=<n>` — 이름 접두사로 엔트리 검색

월렛 같은 애플리케이션은 이 엔드포인트를 써서 원시 파티 식별자 대신 사람이 읽을 수 있는 이름을 표시한다. 예컨대 다른 사용자에게 Canton Coin을 보낼 때 전체 파티 ID 대신 `alice.unverified.cns`를 입력할 수 있다.

이 동일한 엔드포인트는 Validator App의 Scan Proxy API(`/v0/scan-proxy/ans-entries/*` 아래)를 통해서도 제공되며, 여러 <abbr class="gloss" title="글로벌 Synchronizer를 운영하고 네트워크 거버넌스에 참여하는 노드">슈퍼 밸리데이터</abbr> 노드를 조회해 <abbr class="gloss" title="여러 노드가 트랜잭션의 유효성·순서에 함께 동의하는 절차">합의</abbr> 결과를 반환함으로써 <abbr class="gloss" title="비잔틴 장애 허용(Byzantine Fault Tolerance). 일부 노드가 악의적이거나 고장 나도 시스템이 올바르게 동작하는 성질">BFT</abbr> 검증을 제공한다.

## 글로벌 Synchronizer에서의 저장

CNS 상태는 전적으로 글로벌 Synchronizer에 `splice-amulet-name-service` 패키지의 Daml 컨트랙트로 존재한다. 핵심 컨트랙트 유형은:

* **`AnsRules`** — 구성(엔트리 수수료, 수명, 갱신 기간)을 보유하는 싱글톤 컨트랙트. DSO 파티가 서명.
* **`AnsEntryContext`** — CNS 엔트리와 그 구독 사이의 관계를 추적. DSO와 엔트리 소유자가 함께 서명.
* **`AnsEntry`** — 이름, 소유 파티, URL, 설명, 만료 시간을 담는 실제 이름 레코드. DSO와 엔트리 소유자가 함께 서명.

이 컨트랙트들은 표준 Daml 권한 규칙을 따르므로, 생성·갱신·만료에 엔트리 소유자와 DSO 양측의 동의가 필요하다.

## API 레퍼런스

CNS 기능은 Validator App이 노출하는 두 API에 나뉘어 있다:

**ANS API** (엔트리 관리) — [ans-external.yaml](https://raw.githubusercontent.com/canton-network/splice/refs/heads/main/apps/validator/src/main/openapi/ans-external.yaml) OpenAPI 스펙 참고:

* **POST** `/v0/entry/create` — 새 엔트리 생성 요청
* **GET** `/v0/entry/all` — 인증된 사용자가 소유한 모든 엔트리 나열

**Scan API** (이름 해석) — [scan.yaml](https://raw.githubusercontent.com/canton-network/splice/refs/heads/main/apps/scan/src/main/openapi/scan.yaml) OpenAPI 스펙 참고:

* **GET** `/v0/ans-entries` — 이름 접두사로 엔트리 나열
* **GET** `/v0/ans-entries/by-name/{name}` — 정확한 이름으로 엔트리 조회
* **GET** `/v0/ans-entries/by-party/{party}` — 파티 ID로 엔트리 조회
* **POST** `/v0/ans-rules` — 현재 ANS 규칙 구성 조회

ANS API는 토큰 주체(subject)가 엔트리를 요청·나열하는 사용자와 일치하는 JWT 인증을 요구한다. Scan API 엔드포인트는 공개다.

<!-- nav:start -->

---

⬅️ **이전**: [Canton Coin 토크노믹스](canton-coin-tokenomics.md) ・ ➡️ **다음**: [Canton 프로토콜 명세](canton-protocol-specification.md)

<!-- nav:end -->
