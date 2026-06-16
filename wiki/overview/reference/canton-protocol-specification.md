---
title: Canton 프로토콜 명세
source: https://docs.canton.network/overview/reference/canton-protocol-specification
translated: 2026-06-15
status: done
tags: [overview, reference, 프로토콜, 아키텍처]
---

> **출처(원문)**: [Canton Protocol Specification](https://docs.canton.network/overview/reference/canton-protocol-specification) · 번역일 2026-06-15

## 📌 개발자 노트
- **한 줄 요약**: Canton 프로토콜의 기술 명세 진입점 — 2계층 <abbr class="gloss" title="여러 노드가 트랜잭션의 유효성·순서에 함께 동의하는 절차">합의</abbr> 아키텍처(<abbr class="gloss" title="원장 위에서 규칙대로 자동 실행되는 코드화된 계약. Canton에선 Daml 템플릿으로 작성">스마트 컨트랙트</abbr> 검증 + 순서화), 3개 노드 유형, 레퍼런스 페이지 목록, 핵심 보장(프라이버시·무결성·일관성·최종성·라이브니스), 계층 상호작용.
- **핵심 용어**: 2계층 합의, <abbr class="gloss" title="어떤 컨트랙트와 관계를 맺어 그것을 보거나 승인하는 파티 = 서명자 + 관찰자">이해관계자</abbr> 증명, <abbr class="gloss" title="비잔틴 장애 허용(Byzantine Fault Tolerance). 일부 노드가 악의적이거나 고장 나도 시스템이 올바르게 동작하는 성질">BFT</abbr> 순서화, 최종성(finality), 라이브니스(liveness)
- **선행 개념**: [아키텍처 개요](../learn/architecture.md), [2계층 합의](../learn/two-layer-consensus.md).

---

# Canton 프로토콜 명세

> 합의 계층, <abbr class="gloss" title="원장 상태를 바꾸는 원자적 작업 단위. 하나 이상의 컨트랙트를 생성·보관하며, 전부 적용되거나 전혀 적용되지 않음">트랜잭션</abbr> 처리, <abbr class="gloss" title="어떤 노드·파티·키가 네트워크에 참여하는지를 정의하는 구성 정보">토폴로지</abbr> 관리를 다루는 Canton 프로토콜 아키텍처의 기술 명세

이 절은 Canton 프로토콜의 전체 기술 명세를 제공한다. [Learn](../learn/architecture.md) 페이지가 개념을 상위 수준에서 소개한다면, 이 레퍼런스 페이지는 프로토콜 메커니즘을 상세히 기술한다 — Canton Network을 떠받치는 데이터 구조, 신뢰 가정, 메시지 흐름, 형식적 속성.

## 프로토콜 아키텍처

Canton의 프로토콜은 대부분의 블록체인이 뭉뚱그리는 두 관심사를 분리한다: **스마트 <abbr class="gloss" title="원장에 기록되는 불변 데이터 단위. 상태 변경은 새 컨트랙트 생성으로 표현됨">컨트랙트</abbr> 검증**과 **트랜잭션 순서화**. 그 결과는 각 계층을 독립적으로 최적화할 수 있는 2계층 합의 아키텍처다.

| 계층 | 책임 | 메커니즘 | 신뢰 경계 |
| --- | --- | --- | --- |
| **스마트 컨트랙트 합의** | 트랜잭션 정확성 검증 | 이해관계자 증명(P2P) | 영향받는 <abbr class="gloss" title="Canton에서 권한과 데이터 가시성의 주체가 되는 식별 가능한 참여 주체">파티</abbr>만 |
| **순서화 합의** | 일관된 <abbr class="gloss" title="상태를 저장하지 않고 트랜잭션 합의·순서를 조율하는 Canton 구성요소">Synchronizer</abbr> 순서 확립 | <abbr class="gloss" title="Synchronizer 구성요소. 암호화된 메시지에 전체 순서·타임스탬프를 부여하고 참여자에게 전달">시퀀서</abbr>를 통한 BFT 순서화 | Synchronizer 운영자 |

프로토콜은 세 가지 노드 유형에 걸쳐 작동한다:

* **<abbr class="gloss" title="파티를 호스팅하고 그 파티의 컨트랙트를 저장·실행하는 노드. 밸리데이터의 핵심 구성요소">참여자 노드</abbr>(Participant nodes)**는 파티를 <abbr class="gloss" title="참여자 노드가 파티를 대신해 원장에서 활동(컨트랙트 저장·트랜잭션 제출·확인)해 주는 것. 로컬 파티는 키까지 노드가 관리하고, 외부 파티는 제출 키를 파티 자신이 보유(노드는 중계)">호스팅</abbr>하고, 그들의 <abbr class="gloss" title="아직 보관(소비)되지 않아 현재 유효한 컨트랙트">활성 컨트랙트</abbr> 집합(ACS)을 유지하고, 그들을 대신해 스마트 컨트랙트 합의 프로토콜을 실행하며, LAPI(Ledger API)를 사용 가능하게 한다.
* **시퀀서 노드(Sequencer nodes)**는 발신자 프라이버시를 갖춘 인증된 이벤트 순서화 멀티캐스트를 제공한다.
* **<abbr class="gloss" title="Synchronizer 구성요소. 이해관계자들의 확인을 모아 트랜잭션 승인/거부를 판정">미디에이터</abbr> 노드(Mediator nodes)**는 검증 결과를 최종 트랜잭션 결정으로 묶는 2단계 <abbr class="gloss" title="트랜잭션이 최종 확정되어 원장에 반영되는 것">커밋</abbr> 프로토콜을 중재한다.

참여자와 미디에이터는 결코 직접 통신하지 않는다. 모든 메시지는 전역 순서를 부여하는 시퀀서를 통해 흐른다. 페이로드는 암호화되어, 시퀀서는 트랜잭션 내용이 아니라 메타데이터 — 수신자 목록과 메시지 크기 — 만 본다.

## 레퍼런스 페이지

* **[원장 모델(상세)](ledger-model-detailed.md)**: 확장 UTXO 모델 — <abbr class="gloss" title="컨트랙트의 구조와 규칙(권한·초이스)을 정의하는 Daml 청사진">템플릿</abbr>, 이해관계자, <abbr class="gloss" title="컨트랙트에서 수행 가능한 동작(권한이 부여된 당사자만 실행 가능)">초이스</abbr>, 트랜잭션 구조, <abbr class="gloss" title="한 트랜잭션을 당사자별로 나눈 조각. 각 당사자는 자기 권한에 해당하는 뷰(자기 몫)만 받아 본다">뷰</abbr>, 증인(witness).
* **[스마트 컨트랙트 합의](smart-contract-consensus.md)**: 이해관계자 증명 검증, 프라이버시 보존 합의, 신뢰 도메인 비교.
* **[순서화 합의](ordering-consensus.md)**: 시퀀서·미디에이터 아키텍처, BFT 순서화 서비스, <abbr class="gloss" title="Insanely Scalable State-machine replication. Canton 시퀀서가 메시지 전체 순서에 합의하는 데 쓰는 BFT 합의 알고리즘(1/3 미만 비잔틴 허용)">ISS</abbr> 기반 합의 프로토콜.
* **[트랜잭션 생애주기](transaction-lifecycle.md)**: 준비부터 커밋까지의 완전한 5단계 생애주기.
* **[토폴로지](topology.md)**: 네임스페이스 관리, 암호 키, 파티-참여자 매핑, 토폴로지 트랜잭션.

## 핵심 속성

Canton의 프로토콜은 다음 보장을 제공한다:

* **<abbr class="gloss" title="한 트랜잭션을 &quot;뷰&quot;로 분해해, 각 파티가 자신과 관련된 부분만 보도록 하는 Canton의 핵심 프라이버시 방식">부분 트랜잭션 프라이버시</abbr>**: 각 파티는 자신과 관련된 트랜잭션 부분만 본다. 시퀀서와 미디에이터는 트랜잭션 페이로드를 읽을 수 없다.
* **무결성(Integrity)**: 트랜잭션은 필요한 모든 이해관계자가 <abbr class="gloss" title="이해관계자 밸리데이터가 트랜잭션이 유효함을 미디에이터에 응답하는 것(confirmation)">확인</abbr>하고, 모든 <abbr class="gloss" title="컨트랙트의 주된 권한자. 생성·보관(소비)에 반드시 동의해야 하는 파티">서명자</abbr>에 대해 스마트 컨트랙트 로직이 검증을 통과할 때만 커밋된다.
* **일관성(Consistency)**: 순서화 계층은 주어진 Synchronizer의 모든 상태 변경에 단일 전역 순서를 보장해 <abbr class="gloss" title="같은 자산을 두 번 쓰는 부정행위">이중지불</abbr>을 막는 데 기여한다.
* **최종성(Finality)**: 미디에이터가 커밋 평결을 내리고 그것이 시퀀싱되면, 트랜잭션 결과는 최종이다. 포크나 재조직(reorg)이 없다.
* **라이브니스(Liveness)**: BFT 장애 허용 임계값(순서화 노드의 1/3 미만 결함) 하에서 프로토콜은 진전한다.

## 계층들이 상호작용하는 방식

<abbr class="gloss" title="다자간 워크플로를 위해 설계된 Canton의 스마트 컨트랙트 언어">Daml</abbr> 트랜잭션은 생애주기 동안 두 합의 계층을 거친다:

1. 제출 참여자가 트랜잭션을 로컬에서 준비한다 (스마트 컨트랙트 계층)
2. 참여자가 암호화된 뷰를 시퀀서에 보낸다 (순서화 계층)
3. 시퀀서가 영향받는 참여자에게 뷰를, 미디에이터에게 인포미 메시지를 분배한다
4. 각 확인 참여자가 자기 뷰를 검증하고 미디에이터에 확인 또는 거부를 보낸다 (순서화 계층을 통한 스마트 컨트랙트 계층)
5. 미디에이터가 확인을 집계하고 필요한 시간 창 내에 평결을 내리며, 시퀀서가 이를 모든 참여자에게 분배한다 (순서화 계층)

[트랜잭션 생애주기](transaction-lifecycle.md) 페이지가 각 단계를 상세히 다룬다.

<!-- nav:start -->

---

⬅️ **이전**: [Canton 네임 서비스 (CNS)](canton-name-service.md) ・ ➡️ **다음**: ["CIP-0056: Canton Network 토큰 표준"](cip-0056.md)

<!-- nav:end -->
