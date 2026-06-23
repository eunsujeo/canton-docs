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

> ⚠️ **용어 주의**: L0/L1/L2는 **공식 규격이 아니라 업계 통용 분류**다. 경계가 흐릿하고(예: Cosmos·Polkadot은 L0이자 L1로 불림) 마케팅 맥락에 따라 다르게 쓰인다. 더 정밀한 현대적 관점은 아래 *<abbr class="gloss" title="실행·정산·합의·데이터가용성을 계층으로 분리해 각자 최적화하는 구조(예: 롤업+Celestia)">모듈러 블록체인</abbr>*.

## 왜 계층으로 나뉘나 — 확장성 트릴레마
계층이 생긴 근본 이유는 **<abbr class="gloss" title="탈중앙화·보안·확장성 셋을 동시에 만족하기 어렵다는 블록체인 설계 난제(보통 둘만 취함)">확장성 트릴레마</abbr>**: 한 체인이 **탈중앙화·보안·확장성**을 동시에 최고로 달성하기 어렵다(보통 둘을 취하면 하나가 희생된다).
- **L1은 보통 탈중앙화·보안을 우선** → 처리량(확장성)이 병목(예: Ethereum은 안전하지만 느리고 비쌈).
- 그래서 **L2**가 등장 — L1의 보안을 빌리면서 **처리량만** 끌어올린다(거래를 밖에서 묶어 L1에 요약 게시).
- **L0**은 다른 각도 — "한 체인을 빠르게"가 아니라 **여러 특화 L1을 만들고 잇는다**(체인마다 트릴레마 균형을 달리 잡게).

> 한 줄: **L2 = "L1을 빠르게", L0 = "L1을 여러 개로".** 둘 다 단일 체인의 한계를 푸는 서로 다른 방향이다.

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

### L2 "롤업"이란
거래를 **메인 체인 밖(off-chain)** 에서 처리해 **여러 건을 묶어(roll up)** 압축한 뒤, 그 결과·증명을 **L1에 다시 올려 보안을 빌리는** 방식. 빠르고 싸지만 최종 안전성은 L1에 의존. 검증 방식에 따라 두 종류:

| 종류 | 검증 방식 | 예 |
|---|---|---|
| **옵티미스틱 롤업** | **사기 증명(fraud proof)** — 일단 맞다고 보고, 이의제기 기간에 틀리면 증명해 되돌림 | Arbitrum, Optimism, **Base** |
| **ZK 롤업** | **유효성 증명(validity proof)** — 배치마다 영지식 증명을 올려 *미리* 정당성 보장 | zkSync, StarkNet |

- **순서화**: 롤업은 보통 **<abbr class="gloss" title="Synchronizer 구성요소. 암호화된 메시지에 전체 순서·타임스탬프를 부여하고 참여자에게 전달">시퀀서</abbr>**가 L2 거래 순서를 정함(현재 대개 단일·중앙화, 탈중앙 진행 중).
- **프라이버시**: 롤업 데이터는 보통 **L1에 공개**됨 → 거래가 다 보임(ZK로 일부 가릴 순 있음).

> 비유: **개별 거래 = 승객, 배치(묶음) = 버스 한 대, 본선 = L1.** 승객(거래)들을 한 명씩 본선에 보내는 대신 **버스 한 대에 모아 태워** 본선(L1)에 한 번에 올린다 → 빠르고 쌈. 단 승객 명단(거래 내역)은 공개.

### Canton과의 대비

| | L2 롤업 | Canton |
|---|---|---|
| 정체 | L1 보안을 빌린 **공개 확장 계층** | **프라이버시 내장 독립 L1** |
| 순서화 | 시퀀서(흔히 단일) | <abbr class="gloss" title="상태를 저장하지 않고 트랜잭션 합의·순서를 조율하는 Canton 구성요소">Synchronizer</abbr> **<abbr class="gloss" title="비잔틴 장애 허용(Byzantine Fault Tolerance). 일부 노드가 악의적이거나 고장 나도 시스템이 올바르게 동작하는 성질">BFT</abbr>**(탈중앙) |
| 검증 | 사기/유효성 **증명** | **<abbr class="gloss" title="어떤 컨트랙트와 관계를 맺어 그것을 보거나 승인하는 파티 = 서명자 + 관찰자">이해관계자</abbr>**가 직접 검증 |
| 프라이버시 | 제한적(대개 공개) | **완전한 <abbr class="gloss" title="한 트랜잭션을 &quot;뷰&quot;로 분해해, 각 파티가 자신과 관련된 부분만 보도록 하는 Canton의 핵심 프라이버시 방식">부분 트랜잭션 프라이버시</abbr>** |

> 멀티체인 맥락: 스테이블코인이 **Base(=옵티미스틱 롤업 L2)** 에서 발행되고, **Canton(독립 L1)으로 브릿지해 프라이빗 정산**하는 그림이 가능 — "롤업(공개·확장) ↔ Canton(프라이빗 정산)" 역할 분담. (실제 설계는 미확정)

### 사이드체인·앱체인은 L2가 아니다
혼동하기 쉬운 이웃 개념:
- **<abbr class="gloss" title="자체 합의를 가진 독립 체인을 브릿지로 메인체인에 연결한 것(보안을 빌리는 L2와 다름)">사이드체인</abbr>**: **자체 합의를 가진 독립 체인**을 브릿지로 메인체인에 붙인 것. L2처럼 보이지만 **보안을 빌리지 않고 스스로 책임진다** → 분류상 L1에 가깝다(예: Polygon PoS).
- **앱체인(app-chain)**: 한 애플리케이션 전용 체인(Cosmos 앱체인, Polkadot parachain). L0 위에서 자체 상태·합의를 갖는다.

→ 가르는 기준은 한 가지: **보안을 어디서 얻나.** L1·사이드체인·앱체인=*자체*, L2=*L1에서 빌림*. 이 잣대로 보면 **Canton은 자체 합의를 가지므로 L1 쪽**이다.

## L1은 무엇으로 이루어지나 — 모놀리식 vs 모듈러
블록체인이 하는 일은 **네 가지 기능**으로 쪼갤 수 있다:

| 기능 | 하는 일 |
|---|---|
| 실행(execution) | 트랜잭션을 처리해 상태를 바꿈(스마트컨트랙트 구동) |
| 정산(settlement) | 결과를 최종 확정하고 분쟁을 정리 |
| 합의·순서화(consensus) | 트랜잭션의 단일 순서에 동의 |
| <abbr class="gloss" title="트랜잭션 데이터가 검증자들이 실제로 받아볼 수 있게 공개·보관되는 성질(없으면 검증 불가)">데이터 가용성</abbr>(DA) | 데이터를 검증 가능하게 공개·<abbr class="gloss" title="컨트랙트를 소비해 비활성으로 만드는 것(archive). 보관된 컨트랙트는 더 이상 쓸 수 없음">보관</abbr> |

- **모놀리식**: 한 체인이 넷을 다 함(Bitcoin, 초기 Ethereum). 단순하지만 트릴레마에 통째로 묶인다.
- **모듈러**: 기능을 계층으로 쪼갬(롤업=실행, L1=정산·DA, Celestia=DA 전담 등). 각 계층을 따로 최적화·교체할 수 있다.

→ 이 관점이 **Canton을 더 정확히 자리매김**한다. Canton은 **합의·순서화는 Synchronizer**(시퀀서+<abbr class="gloss" title="Synchronizer 구성요소. 이해관계자들의 확인을 모아 트랜잭션 승인/거부를 판정">미디에이터</abbr>)가, **실행·상태 보관은 <abbr class="gloss" title="파티를 호스팅하고 그 파티의 컨트랙트를 저장·실행하는 노드. 밸리데이터의 핵심 구성요소">참여자 노드</abbr>**가 맡아 **둘을 분리**한다. 즉 단일 모놀리식 L1이 아니라 *기능이 분리된 모듈러적 구조의 L1*이다. 게다가 실행 결과(상태)는 **모든 노드에 복제되지 않고 이해관계자에게만** 저장돼, "공개 DA"를 전제로 하는 일반 모듈러 스택과도 다르다(→ 프라이버시).

## Canton의 위치
Canton은 **프라이버시 보존형 퍼블릭 L1**으로 소개된다. 다른 L1과의 차이:

- **프라이버시 우선**: 모든 노드에 전역 복제하지 않고, 데이터를 관련 <abbr class="gloss" title="Canton에서 권한과 데이터 가시성의 주체가 되는 식별 가능한 참여 주체">파티</abbr>에게만 분산 (부분 트랜잭션 프라이버시)
- **기관·규제 자산용 B2B 정산**에 초점 — 익명 퍼블릭 참여가 아니라 신원 기반 파티
- **EVM 네이티브 호환 없음** → Ethereum·Base 등 퍼블릭 EVM 체인과는 브릿지로 연결
- **결정적 <abbr class="gloss" title="트랜잭션이 되돌려지지 않는다고 보장되는 상태. 확률적(점점 굳음) vs 결정적(즉시 최종)">확정성</abbr>**: 트랜잭션이 확정되면 **즉시 최종**(되감기 없음). Bitcoin은 확률적(여러 블록 기다려 점점 굳음), Ethereum PoS는 ~2 에폭 뒤 확정 — Canton은 BFT 순서화([ISS](iss-consensus.md))로 **블록 대기 없이 결정적**. 기관 정산에 핵심
- **L0적 성격도**: <abbr class="gloss" title="슈퍼 밸리데이터들이 공동 운영하는 Canton의 퍼블릭 조율(합의) 계층">글로벌 Synchronizer</abbr> + 다중 Synchronizer 구조는 여러 <abbr class="gloss" title="거래·컨트랙트가 기록되는 장부. Canton에선 활성 컨트랙트의 모음">원장</abbr>을 조율·연결하는 면이 있다

> 실무 맥락: 스테이블코인 등 B2C 토큰은 퍼블릭 EVM 체인(예: Ethereum, Base)에서 발행하고, Canton은 기관 간 B2B 정산 계층으로 쓰는 멀티체인 분담 구조를 흔히 본다.

## 곁가지: 프라이버시를 "덧붙이는" 방식 (ZK-롤업·프라이빗 채널)
대부분의 퍼블릭 체인은 기본적으로 투명해서, 프라이버시를 별도 계층으로 덧붙인다(bolt-on). 대표적인 두 방식:

- **<abbr class="gloss" title="영지식 증명으로 다수 트랜잭션을 체인 밖에서 처리하고 유효성 증명만 L1에 올리는 L2 기술. 내용을 공개하지 않고 검증 가능해 프라이버시에도 활용">ZK-롤업</abbr>**: 영지식 증명으로 다수 트랜잭션을 체인 밖에서 처리하고 "유효하다"는 증명만 L1에 올린다. 내용을 공개하지 않고 검증할 수 있어 프라이버시에도 쓰인다. 예: zkSync, StarkNet, (프라이버시 특화) Aztec.
- **<abbr class="gloss" title="특정 참여자끼리만 거래 데이터를 공유하는 별도 통로. 채널 밖에서는 내용이 보이지 않음(예: 상태/결제 채널, Hyperledger Fabric channel)">프라이빗 채널</abbr>**: 특정 참여자끼리만 거래 데이터를 공유하는 별도 통로. 채널 밖에서는 보이지 않는다. 예: 상태/결제 채널(Lightning Network), Hyperledger Fabric의 channel.

| 방식 | 프라이버시 위치 | 장점 | 단점 |
|---|---|---|---|
| **ZK-롤업·프라이빗 채널** (덧붙이기/bolt-on) | 기본 체인은 투명 → 위에 덧붙여 가림 | • 기존 퍼블릭 체인(Ethereum 등) **생태계·유동성 위에서** 사용<br>• 필요한 부분만 **선택적으로** 프라이버시 추가<br>• 성숙한 인프라·도구 | • 별도 계층이라 **복잡·추가 도구/신뢰** 필요<br>• 프라이버시가 **부분적·선택적**(기본은 투명, 메타데이터 누출 가능)<br>• 채널은 참여자 고정·확장 제약 |
| **Canton** (내장) | 프로토콜 자체가 데이터를 관련 파티에게만 분산 (부분 트랜잭션 프라이버시) | • **기본이 프라이빗** — 메타데이터까지 가림<br>• 별도 도구 없이 **무결성과 동시** 달성<br>• 기관·규제 자산에 적합 | • **별도 생태계**(EVM 비호환 → 브릿지 필요)<br>• 퍼블릭 DeFi 유동성·익명 참여와는 거리<br>• 상대적으로 새 기술·생태계 작음 (신원 기반, 익명 아님) |

즉 Canton은 프라이버시를 별도 레이어로 붙이는 대신 **프로토콜에 내장**했다는 점이 핵심 차이다. → 덧붙이기 방식은 *기존 생태계를 그대로 쓰되 프라이버시가 부분적*, Canton은 *프라이버시가 완전·기본이되 별도 생태계*라는 트레이드오프.

> 💡 **"프로토콜에 내장"이란?** 프라이버시가 추가 기능이 아니라, **거래를 처리하는 기본 방식 자체에 처음부터 들어가 있다**는 뜻. (나중에 블라인드를 단 집 vs 처음부터 불투명 유리로 지은 집)

## 참고
- [Canton Network이란?](../overview/understand/what-is-canton.md) — Canton이 L1으로서 갖는 차별점
- 관련 노트: [BTC vs Ethereum vs Canton 비교](btc-ethereum-canton-compare.md) · [ISS — 시퀀서 BFT 순서화](iss-consensus.md) · [Synchronizer 종류](synchronizer-types-private-consortium-global.md) · [Canton B2B vs B2C](canton-b2b-vs-b2c.md)
- 외부: [Ethereum: Layer 2 / scaling](https://ethereum.org/en/layer-2/) · [Polkadot (Layer 0)](https://polkadot.network/) · [Cosmos (IBC)](https://cosmos.network/) · [확장성 트릴레마(Vitalik)](https://vitalik.eth.limo/general/2021/04/07/sharding.html)

<!-- nav:start -->

---

⬅️ **이전**: [원자적 DvP는 Canton만 되나? — 원자성·잠금·조합성, "이더도 되잖아?"에 답하기](atomic-dvp-real-differentiator.md) ・ ➡️ **다음**: [BTC vs Ethereum vs Canton — 한눈 비교](btc-ethereum-canton-compare.md)

<!-- nav:end -->
