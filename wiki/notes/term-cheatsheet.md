---
title: 용어 한 컷 카드 — 자주 막히는 용어 모음
type: note
translated: 2026-06-16
status: done
tags: [개요, 정리, note, 용어, 치트시트, 복습]
---

> ⚠️ **내부 작성 정리 노트** — 학습 중 자주 다시 묻게 되는 핵심 용어를 **한 줄 비유**로 모은 복습 카드. 정확한 정의는 [용어집](../glossary.md)과 각 페이지 참고.

# 용어 한 컷 카드

자주 헷갈리는 용어를 **한 줄 비유**로. 막히면 여기부터 보면 빠르다.

## 구성요소 (누가 무엇)

| 용어 | 한 컷 비유 |
|---|---|
| **<abbr class="gloss" title="Canton에서 권한과 데이터 가시성의 주체가 되는 식별 가능한 참여 주체">파티</abbr>(Party)** | <abbr class="gloss" title="거래·컨트랙트가 기록되는 장부. Canton에선 활성 컨트랙트의 모음">원장</abbr> 위 **거래 명의(이름표)**. 서버 아님. (≈ 이더리움 주소) |
| **<abbr class="gloss" title="파티를 호스팅하고 그 파티의 컨트랙트를 저장·실행하는 노드. 밸리데이터의 핵심 구성요소">참여자 노드</abbr>(Participant)** | Canton 프로토콜의 **코어 엔진**(파티 <abbr class="gloss" title="참여자 노드가 파티를 대신해 원장에서 활동(컨트랙트 저장·트랜잭션 제출·확인)해 주는 것. 로컬 파티는 키까지 노드가 관리하고, 외부 파티는 제출 키를 파티 자신이 보유(노드는 중계)">호스팅</abbr>·<abbr class="gloss" title="원장에 기록되는 불변 데이터 단위. 상태 변경은 새 컨트랙트 생성으로 표현됨">컨트랙트</abbr> 저장·실행) |
| **<abbr class="gloss" title="파티를 호스팅하고 그 파티의 컨트랙트 데이터를 저장하는 참여자 노드">밸리데이터</abbr>(Validator)** | 참여자 노드 + Canton Network 살림(온보딩·<abbr class="gloss" title="Synchronizer에 쓰기를 요청할 때 소비하는 자원. Canton Coin으로 비용을 지불">트래픽</abbr>·월렛). **참여자 노드를 감싼 완제품** |
| **<abbr class="gloss" title="상태를 저장하지 않고 트랜잭션 합의·순서를 조율하는 Canton 구성요소">Synchronizer</abbr>(동기화자)** | 내용은 못 보면서 **순서 잡고 <abbr class="gloss" title="이해관계자 밸리데이터가 트랜잭션이 유효함을 미디에이터에 응답하는 것(confirmation)">확인</abbr> 모으는 우체국+개표소** |
| **<abbr class="gloss" title="Synchronizer 구성요소. 암호화된 메시지에 전체 순서·타임스탬프를 부여하고 참여자에게 전달">시퀀서</abbr>(Sequencer)** | Synchronizer의 **우체국** — 순서·타임스탬프 부여 + 배달 |
| **<abbr class="gloss" title="Synchronizer 구성요소. 이해관계자들의 확인을 모아 트랜잭션 승인/거부를 판정">미디에이터</abbr>(Mediator)** | Synchronizer의 **개표소** — 확인 모아 가결/부결 판정 |
| **<abbr class="gloss" title="글로벌 Synchronizer를 운영하고 네트워크 거버넌스에 참여하는 노드">슈퍼 밸리데이터</abbr>(SV)** | <abbr class="gloss" title="슈퍼 밸리데이터들이 공동 운영하는 Canton의 퍼블릭 조율(합의) 계층">글로벌 Synchronizer</abbr>를 **공동 운영하는 노드**(<abbr class="gloss" title="탈중앙 Synchronizer 운영(Decentralized Synchronizer Operations) 파티. 슈퍼 밸리데이터들의 공동 거버넌스 주체">DSO</abbr>) |
| **호스팅(Hosting)** | 노드가 파티를 **대신 굴려줌**(데이터 저장·서명·제출). 은행이 계좌를 운영해주듯 |

## 원장·거래 모델

| 용어 | 한 컷 비유 |
|---|---|
| **컨트랙트(Contract)** | 원장 위 **불변 객체**(지폐·계약서 한 장). 수정 불가, 생성·<abbr class="gloss" title="컨트랙트를 소비해 비활성으로 만드는 것(archive). 보관된 컨트랙트는 더 이상 쓸 수 없음">보관</abbr>만 |
| **<abbr class="gloss" title="확장 UTXO. 금액만이 아니라 임의의 상태·규칙을 담는 컨트랙트로 원장을 구성하는 모델">eUTXO</abbr>** | 돈 = 잔액 숫자가 아니라 **지폐 한 장 한 장**(상태+규칙 담은 컨트랙트) |
| **<abbr class="gloss" title="원장 상태를 바꾸는 원자적 작업 단위. 하나 이상의 컨트랙트를 생성·보관하며, 전부 적용되거나 전혀 적용되지 않음">트랜잭션</abbr>(Transaction)** | 원장을 바꾸는 **원자적 작업**(전부 아니면 전무) |
| **트랜잭션 트리** | 한 거래가 일으킨 **연쇄 동작을 펼친 나무**(도미노 한 판, 통째로 <abbr class="gloss" title="트랜잭션이 최종 확정되어 원장에 반영되는 것">커밋</abbr>) |
| **<abbr class="gloss" title="한 트랜잭션을 당사자별로 나눈 조각. 각 당사자는 자기 권한에 해당하는 뷰(자기 몫)만 받아 본다">뷰</abbr>(View)** | view=본다 → **나한테 보이는 내 몫**(거래를 당사자별로 쪼갠 조각) |
| **<abbr class="gloss" title="전체 원장 중 그 참여자 노드가 보관하는 자기 조각. 자기 파티가 이해관계자인 컨트랙트만 담김(전체 사본은 어디에도 없음)">원장 샤드</abbr>(Shard)** | 한 **노드가 보관하는 장부 조각**(자기 파티 관련만). 전체 사본은 없음 |
| **<abbr class="gloss" title="같은 자산을 두 번 쓰는 부정행위">이중지불</abbr>** | 같은 지폐를 **두 번 쓰기**(eUTXO라 구조적으로 불가) |
| **조합 가능성(Composability)** | 독립 컨트랙트를 한 거래로 **레고처럼 묶기**(예: <abbr class="gloss" title="인도-대-지급(Delivery vs Payment). 자산 인도와 대금 지급을 동시·원자적으로 처리">DvP</abbr>=자산↔대금 동시) |

## 초이스·권한

| 용어 | 한 컷 비유 |
|---|---|
| **<abbr class="gloss" title="컨트랙트에서 수행 가능한 동작(권한이 부여된 당사자만 실행 가능)">초이스</abbr>(Choice)** | 컨트랙트의 **메서드/버튼**(불변 객체를 바꾸는 유일한 길) |
| **<abbr class="gloss" title="실행하면 그 컨트랙트를 보관(소비)하는 초이스. 상태 변경·이전에 쓴다(기본값)">소비형 초이스</abbr>** | 누르면 컨트랙트 **소비(사라짐)** — 상태 변경·이전용 (기본값) |
| **<abbr class="gloss" title="실행해도 컨트랙트를 활성으로 남겨두는 초이스. 조회·알림·읽기에 쓴다">비소비형 초이스</abbr>** | 눌러도 **그대로** — 조회·읽기용 |
| **<abbr class="gloss" title="어떤 컨트랙트와 관계를 맺어 그것을 보거나 승인하는 파티 = 서명자 + 관찰자">이해관계자</abbr>(Stakeholder)** | 그 컨트랙트의 **<abbr class="gloss" title="컨트랙트의 주된 권한자. 생성·보관(소비)에 반드시 동의해야 하는 파티">서명자</abbr> + <abbr class="gloss" title="컨트랙트를 볼 수 있으나 단독으로 행위할 수는 없는 파티">관찰자</abbr>**(관계자) |
| **서명자(Signatory)** | "내 동의 없인 이 컨트랙트 성립 불가" — 생성·보관에 **반드시 동의** |
| **관찰자(Observer)** | **보기만** 함(예: 규제기관) |
| **<abbr class="gloss" title="컨트랙트의 특정 초이스(동작)를 실행할 권한을 가진 파티">컨트롤러</abbr>(Controller)** | 특정 **초이스(버튼)를 누를 권한**자 |

## 파티 종류 (키를 누가 쥐냐)

| 용어 | 한 컷 비유 |
|---|---|
| **<abbr class="gloss" title="키를 노드(밸리데이터)가 보관·서명하는 파티(=수탁형). '로컬'은 노드 시점 작명 — 키·신원이 노드 안에 있음">로컬 파티</abbr>** | **키를 노드가 보관**(수탁). "로컬"=노드 시점=키가 노드 *안* |
| **<abbr class="gloss" title="키를 파티 주인이 직접 보관하고 거래마다 외부 서명하는 파티(=자기수탁). '외부'는 노드 시점 — 키가 노드 밖에 있음">외부 파티</abbr>** | **키를 본인이 보관**(자기수탁). "외부"=노드 *바깥*(파티 주인 바깥 아님!) |

## 네트워크·운영

| 용어 | 한 컷 비유 |
|---|---|
| **Canton** | 기반 **프로토콜(엔진)** |
| **<abbr class="gloss" title="글로벌 Synchronizer를 구동하는 오픈소스 애플리케이션 모음(SV·밸리데이터·월렛 등)">Splice</abbr>** | 그 엔진으로 공개망을 **운영하는 소프트웨어 묶음**(토큰·월렛·<abbr class="gloss" title="네트워크의 공개 통계·활동을 보여주는 익스플로러(블록 익스플로러의 Canton판)">Scan</abbr>·거버넌스) |
| **글로벌 Synchronizer** | SV들이 공동 운영하는 **공개 백본** |
| **<abbr class="gloss" title="트랜잭션 수수료와 밸리데이터 보상에 쓰이는 네이티브 유틸리티 토큰(CC)">Canton Coin</abbr>(CC)** | 수수료·보상용 토큰(=Splice의 <abbr class="gloss" title="Canton Coin(CC)의 Daml/Scan상 기술적 이름. CC = Amulet">Amulet</abbr>) |
| **트래픽(Traffic)** | 네트워크 **쓰기 사용료**(CC로 지불) |
| **<abbr class="gloss" title="비잔틴 장애 허용(Byzantine Fault Tolerance). 일부 노드가 악의적이거나 고장 나도 시스템이 올바르게 동작하는 성질">BFT</abbr>** | 일부가 **거짓말·고장 나도 견딤**(SV 2/3 정직하면 OK) |
| **<abbr class="gloss" title="원장(Daml 컨트랙트) 위에서 실행·기록되는 것. 모든 이해관계자가 공유·검증·강제">온-원장</abbr> / <abbr class="gloss" title="원장 밖, 내 백엔드 인프라에서 실행되는 것. 외부 API·UI·복잡 계산 등 나만 처리">오프-원장</abbr>** | 원장(<abbr class="gloss" title="다자간 워크플로를 위해 설계된 Canton의 스마트 컨트랙트 언어">Daml</abbr>)에서 실행 / 내 백엔드에서 실행 |
| **LocalNet→DevNet→TestNet→MainNet** | 로컬 → 공유 개발 → 스테이징 → 실제. 공유망은 온보딩 필요 |

## 더 깊은 정리 노트
- [eUTXO와 이중지불 방지](eutxo-double-spend.md) · [로컬 파티 vs 외부 파티](local-vs-external-party.md) · [파티 per-user vs 옴니버스](party-design-per-user-vs-omnibus.md)
- [환경 4단계](canton-environments-localnet-to-mainnet.md) · [Canton vs Splice](canton-vs-splice.md) · [블록체인 계층 L0/L1/L2](blockchain-layers-l0-l1-l2.md)
- 정확한 정의 전체: [용어집](../glossary.md)

<!-- nav:start -->

---

⬅️ **이전**: [Synchronizer 종류 — 사설 vs 컨소시엄 vs 글로벌](synchronizer-types-private-consortium-global.md)

<!-- nav:end -->
