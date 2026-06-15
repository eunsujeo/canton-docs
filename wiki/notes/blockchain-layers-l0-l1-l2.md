---
title: 블록체인 계층 (L0 / L1 / L2)와 Canton의 위치
type: note
translated: 2026-06-15
status: done
tags: [개요, 정리, note]
---

> ⚠️ **내부 작성 정리 노트** — Canton 공식 문서의 충실 번역본이 아니라, 학습을 돕기 위해 직접 작성한 배경 설명입니다. 사실관계는 아래 참고 링크로 <abbr class="gloss" title="이해관계자 밸리데이터가 트랜잭션이 유효함을 미디에이터에 응답하는 것(confirmation)">확인</abbr>하세요.

# 블록체인 계층 (L0 / L1 / L2)와 Canton의 위치

"Canton은 퍼블릭 <abbr class="gloss" title="자체 합의로 트랜잭션을 직접 확정하는 기반 블록체인(L1). 다른 체인에 의존하지 않음">레이어 1</abbr> 블록체인이다"라는 문장을 이해하려면 블록체인 계층 개념을 알아야 한다.

## 한눈에 보기

| 계층 | 정의 | 보안의 출처 | 대표 예 |
|---|---|---|---|
| **L0 (<abbr class="gloss" title="여러 L1 블록체인을 구축·연결하도록 받쳐주는 기반 인프라 계층(예: Polkadot, Cosmos)">레이어 0</abbr>)** | 여러 L1을 구축·연결하는 기반 인프라 | 자체 프레임워크 | Polkadot(Relay Chain), Cosmos(IBC), Avalanche(Primary Network) |
| **L1 (레이어 1)** | 자체 <abbr class="gloss" title="여러 노드가 트랜잭션의 유효성·순서에 함께 동의하는 절차">합의</abbr>로 <abbr class="gloss" title="원장 상태를 바꾸는 원자적 작업 단위. 하나 이상의 컨트랙트를 생성·보관하며, 전부 적용되거나 전혀 적용되지 않음">트랜잭션</abbr>을 직접 확정하는 기반 블록체인 | **자체 합의** | Bitcoin, Ethereum, Solana, **Canton** |
| **L2 (<abbr class="gloss" title="L1 위에 얹혀 처리량을 늘리는 확장 계층(L2). 보안은 L1에 의존(예: Base, Arbitrum)">레이어 2</abbr>)** | L1 위에 얹혀 처리량을 늘리는 확장 계층 | **L1에 의존** | Base, Arbitrum, Optimism, zkSync |

핵심 구분: **자체 합의로 스스로 트랜잭션을 확정하면 L1, 다른 체인(주로 L1)에 보안을 의존하면 L2.** L0은 그런 L1들을 여러 개 만들고 이어 붙이는 토대다.

## Layer 1 (L1)
자체 합의로 트랜잭션을 직접 확정하는 기반 블록체인. 다른 체인에 의존하지 않는다.

- **범용 스마트<abbr class="gloss" title="원장에 기록되는 불변 데이터 단위. 상태 변경은 새 컨트랙트 생성으로 표현됨">컨트랙트</abbr>**: Ethereum(EVM), Solana, Avalanche, BNB Chain, Near, Aptos, Sui, Tron
- **결제/가치저장**: Bitcoin (스마트컨트랙트 제한적)
- **상호운용 지향**: Cosmos, Polkadot (L0 성격도 겸함)
- **1세대/연구지향**: Cardano, Algorand, Tezos
- **프라이버시·기관용**: **Canton**

## Layer 0 (L0)
여러 L1 블록체인을 구축·연결하도록 받쳐주는 기반 인프라 계층. 합의 프레임워크, 크로스체인 통신, 개발 SDK를 제공한다.

- **Polkadot** — Relay Chain이 여러 parachain(L1)을 연결
- **Cosmos** — Tendermint + IBC로 여러 앱체인을 연결
- **Avalanche** — Primary Network 위에 여러 Subnet
- **LayerZero / Quant** — 체인 간 메시징·상호운용 프로토콜 (넓은 의미의 L0)

## Layer 2 (L2)
L1 위에 얹혀 처리량·수수료를 개선하는 확장 계층. **자체 합의가 아니라 L1에 보안을 의존**한다.

- Ethereum 계열: Base, Arbitrum, Optimism(롤업), zkSync(ZK 롤업)

## Canton의 위치
Canton은 **프라이버시 보존형 퍼블릭 L1**으로 소개된다. 다른 L1과의 차이:

- **프라이버시 우선**: 모든 노드에 전역 복제하지 않고, 데이터를 관련 <abbr class="gloss" title="Canton에서 권한과 데이터 가시성의 주체가 되는 식별 가능한 참여 주체">파티</abbr>에게만 분산 (<abbr class="gloss" title="한 트랜잭션을 &quot;뷰&quot;로 분해해, 각 파티가 자신과 관련된 부분만 보도록 하는 Canton의 핵심 프라이버시 방식">부분 트랜잭션 프라이버시</abbr>)
- **기관·규제 자산용 B2B 정산**에 초점 — 익명 퍼블릭 참여가 아니라 신원 기반 파티
- **EVM 네이티브 호환 없음** → Ethereum·Base 등 퍼블릭 EVM 체인과는 브릿지로 연결
- **L0적 성격도**: <abbr class="gloss" title="슈퍼 밸리데이터들이 공동 운영하는 Canton의 퍼블릭 조율(합의) 계층">글로벌 Synchronizer</abbr> + 다중 <abbr class="gloss" title="상태를 저장하지 않고 트랜잭션 합의·순서를 조율하는 Canton 구성요소">Synchronizer</abbr> 구조는 여러 <abbr class="gloss" title="거래·컨트랙트가 기록되는 장부. Canton에선 활성 컨트랙트의 모음">원장</abbr>을 조율·연결하는 면이 있다

> 실무 맥락: 스테이블코인 등 B2C 토큰은 퍼블릭 EVM 체인(예: Ethereum, Base)에서 발행하고, Canton은 기관 간 B2B 정산 계층으로 쓰는 멀티체인 분담 구조를 흔히 본다.

## 곁가지: 프라이버시를 "덧붙이는" 방식 (ZK-롤업·프라이빗 채널)
대부분의 퍼블릭 체인은 기본적으로 투명해서, 프라이버시를 별도 계층으로 덧붙인다(bolt-on). 대표적인 두 방식:

- **<abbr class="gloss" title="영지식 증명으로 다수 트랜잭션을 체인 밖에서 처리하고 유효성 증명만 L1에 올리는 L2 기술. 내용을 공개하지 않고 검증 가능해 프라이버시에도 활용">ZK-롤업</abbr>**: 영지식 증명으로 다수 트랜잭션을 체인 밖에서 처리하고 "유효하다"는 증명만 L1에 올린다. 내용을 공개하지 않고 검증할 수 있어 프라이버시에도 쓰인다. 예: zkSync, StarkNet, (프라이버시 특화) Aztec.
- **<abbr class="gloss" title="특정 참여자끼리만 거래 데이터를 공유하는 별도 통로. 채널 밖에서는 내용이 보이지 않음(예: 상태/결제 채널, Hyperledger Fabric channel)">프라이빗 채널</abbr>**: 특정 참여자끼리만 거래 데이터를 공유하는 별도 통로. 채널 밖에서는 보이지 않는다. 예: 상태/결제 채널(Lightning Network), Hyperledger Fabric의 channel.

| 방식 | 프라이버시 위치 |
|---|---|
| ZK-롤업·프라이빗 채널 | 기본 체인은 투명 → 위에 덧붙여(bolt-on) 가림 |
| **Canton** | 프로토콜 자체가 데이터를 관련 파티에게만 분산 (부분 트랜잭션 프라이버시) |

즉 Canton은 프라이버시를 별도 레이어로 붙이는 대신 **프로토콜에 내장**했다는 점이 핵심 차이다.

## 참고
- [Canton Network이란?](../overview/understand/what-is-canton.md) — Canton이 L1으로서 갖는 차별점
- [Ethereum: Layer 2 / scaling](https://ethereum.org/en/layer-2/)
- [Polkadot (Layer 0)](https://polkadot.network/) · [Cosmos (IBC)](https://cosmos.network/)

<!-- nav:start -->

---

⬅️ **이전**: [데모 실행하기 (Running the Demo)](../appdev/quickstart/running-the-demo.md) ・ ➡️ **다음**: [eUTXO와 이중지불 방지 — "존재하지 않는 것은 쓸 수 없다" 쉽게 이해하기](eutxo-double-spend.md)

<!-- nav:end -->
