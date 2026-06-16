---
title: ISS — Canton 시퀀서의 BFT 순서화 알고리즘
type: note
translated: 2026-06-16
status: done
tags: [정리, note, 합의, BFT, 시퀀서, ordering]
---

> ⚠️ **내부 작성 정리 노트** — Canton 공식 문서의 충실 번역본이 아니라, 학습을 돕기 위해 직접 작성한 배경 설명입니다. 알고리즘 세부는 원논문/구현으로 <abbr class="gloss" title="이해관계자 밸리데이터가 트랜잭션이 유효함을 미디에이터에 응답하는 것(confirmation)">확인</abbr>하세요(아래 참고).

# ISS — Canton 시퀀서의 BFT 순서화 알고리즘

**<abbr class="gloss" title="Insanely Scalable State-machine replication. Canton 시퀀서가 메시지 전체 순서에 합의하는 데 쓰는 BFT 합의 알고리즘(1/3 미만 비잔틴 허용)">ISS</abbr> = Insanely Scalable State-machine replication.** Canton의 **탈중앙화 <abbr class="gloss" title="Synchronizer 구성요소. 암호화된 메시지에 전체 순서·타임스탬프를 부여하고 참여자에게 전달">시퀀서</abbr>**가 메시지의 **전체 순서(total order)** 에 <abbr class="gloss" title="여러 노드가 트랜잭션의 유효성·순서에 함께 동의하는 절차">합의</abbr>할 때 쓰는 **<abbr class="gloss" title="비잔틴 장애 허용(Byzantine Fault Tolerance). 일부 노드가 악의적이거나 고장 나도 시스템이 올바르게 동작하는 성질">BFT</abbr> 합의 알고리즘**이다.

## 한 줄 정의

> **ISS = "여러 리더가 병렬로 순서를 정해 처리량을 끌어올린 BFT 합의."** Canton 시퀀서가 암호화된 메시지들에 **단일 전체 순서**를 매기는 데 사용.

## 어디에 쓰이나 (위치)

- Canton **2계층 합의** 중 **계층 2(순서화 합의)** ([2계층 합의](../overview/learn/two-layer-consensus.md)).
- 글로벌 같은 **탈중앙 <abbr class="gloss" title="상태를 저장하지 않고 트랜잭션 합의·순서를 조율하는 Canton 구성요소">Synchronizer</abbr>**의 **시퀀서 클러스터**가 여러 노드로 BFT를 돌릴 때 ISS를 씀.
- **내용은 안 봄**: 암호화된 봉투에 *순서만* 매김 → 프라이버시 유지(순서는 도착 기준, 내용 불필요).

## ISS가 푸는 문제 — "단일 리더 병목"

전통적 BFT(예: PBFT)는 보통 **리더 1명**이 순서를 제안한다 → 리더가 병목·단일 장애점이 되어 **처리량이 안 늘어남**.

**ISS의 핵심 아이디어**: 요청 공간을 여러 **버킷(bucket)** 으로 나눠 **여러 노드가 동시에 리더** 역할을 한다(멀티 리더). 각 리더가 자기 몫의 순서를 병렬로 정하고, 그 결과를 **하나의 전체 순서로 합친다**.

> 비유: 창구 1개(단일 리더)에 줄 서는 대신, **여러 창구(멀티 리더)** 가 동시에 번호표를 나눠 처리하되, 최종 번호표는 **하나의 통합 순번**으로 합쳐진다 → 빠르면서도 순서는 일관.

## 보장과 한계

| 항목 | 내용 |
|---|---|
| **장애 허용** | 노드의 **1/3 미만**이 비잔틴(악의·고장)이어도 견딤 (그 이상이면 깨짐) |
| **안전성(safety)** | 정직 노드는 **모순된 순서를 확정하지 않음** (서로 다른 결론 X) |
| **라이브니스(liveness)** | 일부 노드가 죽어도 **계속 진행**(멈추지 않음) |
| **확정** | 결정적 — 한 번 순서가 정해지면 **되감기 없음**(BTC식 reorg 없음) |
| **확장성** | 멀티 리더 병렬화로 **높은 처리량** |

## 왜 Canton에 중요한가

- **순서는 BFT(ISS)로, 내용 검증은 <abbr class="gloss" title="어떤 컨트랙트와 관계를 맺어 그것을 보거나 승인하는 파티 = 서명자 + 관찰자">이해관계자</abbr>가** → 프라이버시(내용 비공개) + 무결성(일관된 순서) 동시.
- **결정적 확정** → 기관 정산(<abbr class="gloss" title="인도-대-지급(Delivery vs Payment). 자산 인도와 대금 지급을 동시·원자적으로 처리">DvP</abbr>)에 필수 ("끝나면 끝", 되감기 없음).
- **멀티 리더 확장성** → 많은 기관·거래를 감당.

## 한 줄 정리

> **ISS = Canton 시퀀서가 암호화 메시지에 단일 전체 순서를 매기는 멀티 리더 BFT 합의.** 1/3 미만 비잔틴을 견디고, 결정적 확정·높은 처리량을 제공하며, 내용은 보지 않아 프라이버시를 지킨다.

## 참고 링크
- [2계층 합의](../overview/learn/two-layer-consensus.md) — 순서화 계층에서 ISS 사용
- [순서화 합의](../overview/reference/ordering-consensus.md) — 순서화 상세 레퍼런스
- [글로벌 Synchronizer 아키텍처](../overview/learn/global-synchronizer-architecture.md) — 분산 시퀀서·BFT
- [BTC vs Ethereum vs Canton](btc-ethereum-canton-compare.md) — 합의 비교

<!-- nav:start -->

---

⬅️ **이전**: [eUTXO와 이중지불 방지 — "존재하지 않는 것은 쓸 수 없다" 쉽게 이해하기](eutxo-double-spend.md) ・ ➡️ **다음**: [로컬 파티 vs 외부 파티 — 쉽게 이해하기](local-vs-external-party.md)

<!-- nav:end -->
