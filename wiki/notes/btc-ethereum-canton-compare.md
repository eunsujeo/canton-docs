---
title: BTC vs Ethereum vs Canton — 한눈 비교
type: note
translated: 2026-06-16
status: done
tags: [개요, 정리, note, 비교, 합의, 프라이버시]
---

> ⚠️ **내부 작성 정리 노트** — Canton 공식 문서의 충실 번역본이 아니라, 학습을 돕기 위해 직접 작성한 비교 정리입니다. 정확한 정의는 [용어집](../glossary.md)·각 페이지 참고.

# BTC vs Ethereum vs Canton — 한눈 비교

세 네트워크를 <abbr class="gloss" title="여러 노드가 트랜잭션의 유효성·순서에 함께 동의하는 절차">합의</abbr>·프라이버시·데이터 모델 관점에서 비교.

## 한눈에 비교표

| 항목 | **Bitcoin (BTC)** | **Ethereum** | **Canton** |
|---|---|---|---|
| **데이터 모델** | UTXO (동전) | 계정(Account, 잔액) | **<abbr class="gloss" title="확장 UTXO. 금액만이 아니라 임의의 상태·규칙을 담는 컨트랙트로 원장을 구성하는 모델">eUTXO</abbr>** (<abbr class="gloss" title="원장에 기록되는 불변 데이터 단위. 상태 변경은 새 컨트랙트 생성으로 표현됨">컨트랙트</abbr>=상태+규칙) |
| **<abbr class="gloss" title="원장 위에서 규칙대로 자동 실행되는 코드화된 계약. Canton에선 Daml 템플릿으로 작성">스마트 컨트랙트</abbr>** | 거의 없음(Script 제한적) | 풍부(EVM/Solidity) | 풍부(**<abbr class="gloss" title="다자간 워크플로를 위해 설계된 Canton의 스마트 컨트랙트 언어">Daml</abbr>**) |
| **합의 방식** | PoW(작업증명) | PoS(지분증명) | **2계층**: <abbr class="gloss" title="어떤 컨트랙트와 관계를 맺어 그것을 보거나 승인하는 파티 = 서명자 + 관찰자">이해관계자</abbr> <abbr class="gloss" title="이해관계자 밸리데이터가 트랜잭션이 유효함을 미디에이터에 응답하는 것(confirmation)">확인</abbr> + 순서화 **<abbr class="gloss" title="비잔틴 장애 허용(Byzantine Fault Tolerance). 일부 노드가 악의적이거나 고장 나도 시스템이 올바르게 동작하는 성질">BFT</abbr>**(SV) |
| **누가 검증?** | 모든 노드가 전부 | 모든 노드가 전부 | **그 거래 이해관계자만** |
| **검증자가 보는 것** | 전부 공개 | 전부 공개 | **당사자만**(SV는 암호봉투만) |
| **확정(finality)** | 확률적(되감기 가능) | BFT형(약 2/3 지분) | **결정적**(되감기 없음) |
| **<abbr class="gloss" title="같은 자산을 두 번 쓰는 부정행위">이중지불</abbr> 방지** | UTXO 1회 소비 + 최장체인 | **논스(순번)** + 전역상태 | **구조적**(컨트랙트 1회 <abbr class="gloss" title="컨트랙트를 소비해 비활성으로 만드는 것(archive). 보관된 컨트랙트는 더 이상 쓸 수 없음">보관</abbr>) |
| **병렬성** | 중간 | 낮음(계정 잠금) | **높음**(독립 컨트랙트) |
| **프라이버시** | 없음(가명) | 없음(가명) | **있음**(<abbr class="gloss" title="한 트랜잭션을 &quot;뷰&quot;로 분해해, 각 파티가 자신과 관련된 부분만 보도록 하는 Canton의 핵심 프라이버시 방식">부분 트랜잭션 프라이버시</abbr>) |
| **신뢰 모델** | 해시파워 과반 정직 | 지분 2/3 정직 | 내 <abbr class="gloss" title="파티를 호스팅하고 그 파티의 컨트랙트 데이터를 저장하는 참여자 노드">밸리데이터</abbr> + 순서엔 **SV 2/3** |
| **주 용도** | P2P 디지털 현금·가치저장 | 퍼블릭 dApp·DeFi·NFT | **규제·기관 정산, 다자간 프라이빗 워크플로** |
| **블록 익스플로러** | [mempool.space](https://mempool.space) · [blockstream.info](https://blockstream.info) | [etherscan.io](https://etherscan.io) | [cantonscan.com](https://www.cantonscan.com) · CC Scan(망별) |

> 💡 익스플로러도 차이가 드러난다: BTC/ETH 스캔은 **누구나 모든 거래·잔액**을 본다(전부 공개). **Canton(CantonScan·CC Scan)** 은 네트워크 통계·SV·밸리데이터·<abbr class="gloss" title="트랜잭션 수수료와 밸리데이터 보상에 쓰이는 네이티브 유틸리티 토큰(CC)">Canton Coin</abbr> 활동 같은 **공개 가능한 메타데이터**는 보여주지만, **개별 거래 내용은 당사자만** 본다(부분 <abbr class="gloss" title="원장 상태를 바꾸는 원자적 작업 단위. 하나 이상의 컨트랙트를 생성·보관하며, 전부 적용되거나 전혀 적용되지 않음">트랜잭션</abbr> 프라이버시 때문).

## 한 줄씩 직관

- **BTC** = 공개 장부 위 **동전(UTXO)** 주고받기. 단순·견고하지만 프로그래밍·프라이버시 약함.
- **Ethereum** = 공개 **세계 컴퓨터**(계정 + 스마트 컨트랙트). 강력하지만 **다 공개**, 계정 잠금으로 병렬성↓.
- **Canton** = **프라이빗 다자간 <abbr class="gloss" title="거래·컨트랙트가 기록되는 장부. Canton에선 활성 컨트랙트의 모음">원장</abbr>**. eUTXO 컨트랙트 + 당사자만 검증·열람 + 결정적 확정 → **무결성·프라이버시·<abbr class="gloss" title="트랜잭션이 전부 적용되거나 전혀 적용되지 않는 성질. 일부만 반영되는 일이 없음">원자성</abbr> 동시**.

## 핵심 구분 3가지

1. **누가 보나**: BTC·ETH = 전 세계 / **Canton = 당사자만** ← 가장 큰 차이
2. **BFT를 어디에**: ETH는 전체 상태에 / **Canton은 "순서"에만**(내용은 당사자가 검증) — [2계층 합의](../overview/learn/two-layer-consensus.md)
3. **확정**: BTC 확률적 ↔ **Canton 결정적**(되감기 없음 → 정산에 유리)

## B2B 정산 관점

- BTC/ETH 정산 → 거래·금액 **전부 공개** + (BTC는) 확정 불확실
- **Canton 정산** → **당사자만** 보고 + **즉시 확정** + 원자적 <abbr class="gloss" title="인도-대-지급(Delivery vs Payment). 자산 인도와 대금 지급을 동시·원자적으로 처리">DvP</abbr> → 기관 정산에 적합

## 블록 익스플로러 (스캔)
- **Bitcoin**: [mempool.space](https://mempool.space) · [blockstream.info](https://blockstream.info)
- **Ethereum**: [etherscan.io](https://etherscan.io)
- **Canton**: [cantonscan.com](https://www.cantonscan.com) (네트워크·SV·밸리데이터 통계) · CC Scan(<abbr class="gloss" title="슈퍼 밸리데이터들이 공동 운영하는 Canton의 퍼블릭 조율(합의) 계층">글로벌 Synchronizer</abbr> Canton Coin 활동, 망별 URL — 예: MainNet `https://scan.global`)

## 참고 링크
- [eUTXO vs 계정 모델](eutxo-double-spend.md) · [블록체인 계층 L0/L1/L2](blockchain-layers-l0-l1-l2.md)
- [2계층 합의](../overview/learn/two-layer-consensus.md) · [프라이버시 모델](../overview/learn/privacy-model.md) · [신뢰 모델](../overview/learn/trust-model.md)
- [용어 한 컷 카드](term-cheatsheet.md)

<!-- nav:start -->

---

⬅️ **이전**: [블록체인 계층 (L0 / L1 / L2)와 Canton의 위치](blockchain-layers-l0-l1-l2.md) ・ ➡️ **다음**: [Canton 환경 4단계 — LocalNet → DevNet → TestNet → MainNet](canton-environments-localnet-to-mainnet.md)

<!-- nav:end -->
