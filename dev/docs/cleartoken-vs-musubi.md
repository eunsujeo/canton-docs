---
title: ClearToken vs Musubi — 같은 Canton DvP, 정반대 포지셔닝
type: note
translated: 2026-06-24
status: done
tags: [정리, note, dvp, 결제, 스테이블코인, 경쟁분석]
---

> ⚠️ **내부 작성 정리 노트** — Canton 공식 문서의 충실 번역본이 아니라, 경쟁/참고 사례를 이해하기 위해 직접 작성한 배경 설명입니다. ClearToken 사실관계는 아래 출처 링크로 <abbr class="gloss" title="이해관계자 밸리데이터가 트랜잭션이 유효함을 미디에이터에 응답하는 것(confirmation)">확인</abbr>하세요.

> **출처**: [ClearToken launches regulated stablecoin FX and tokenised settlement on Canton Network](https://cleartoken.io/news/press-releases/cleartoken-launches-regulated-stablecoin-fx-and-tokenised-settlement-on-canton-network/) (보도자료) · 정리일 2026-06-24

# ClearToken vs Musubi

노무라(Nomura)가 투자한 영국 ClearToken이 Canton Network 위에 결제·청산 인프라를 올렸다. 우리(Musubi)와 **같은 Canton·같은 원자적 <abbr class="gloss" title="인도-대-지급(Delivery vs Payment). 자산 인도와 대금 지급을 동시·원자적으로 처리">DvP</abbr>**라는 기술 토대를 쓰지만, **신뢰 모델과 자산 범위가 정반대**다. 한 번 정리.

## 한 줄 차이

> **ClearToken = 규제 인가받은 중앙 청산소가 fiat까지 <abbr class="gloss" title="실물·금융 자산을 원장 위의 토큰(컨트랙트)으로 표현하는 것">토큰화</abbr>** · **Musubi = 무인가 분산형으로 스테이블코인 B2B 정산.**

| | ClearToken | Musubi |
|---|---|---|
| 신뢰 모델 | **FCA 인가 중앙 엔티티**(수탁기관·청산소)가 결제·청산의 신뢰 앵커 | **분산형** — 별도 청산 주체 없음, 참여사가 각자 노드/지갑 운영 |
| 자산 범위 | fiat·증권·암호자산·스테이블코인 **전부** (fiat 자체를 토큰화) | KRW·JPY **스테이블코인 한정** (fiat 미취급) |
| 대상 | 전통 금융기관(은행 간 결제·청산) | 한·일 B2B 스테이블코인 정산 |
| 토큰 발행 | (해당 없음 — fiat·자산 토큰화 레지스터) | Base/Ethereum 발행 스테이블코인, Canton은 B2B 정산 레일 |
| Canton 역할 | 인가 청산소 위의 정산 레일 | 분산 DvP 정산 레일 |

## ClearToken이 올린 것 — Daml 기반 플랫폼 3종

| 플랫폼 | 역할 | 결제 방식 |
|---|---|---|
| **CT Register** | fiat·스테이블코인·증권을 토큰화/역토큰화 (감사가능한 결제용 데이터 토큰으로 변환) | — |
| **CT Pay** | 여러 은행 간 <abbr class="gloss" title="지급-대-지급(Payment vs Payment). 두 통화의 지급을 동시·원자적으로 처리해 한쪽만 가는 일을 막음">PvP</abbr>(Payment vs Payment) | 통화 대 통화, **<abbr class="gloss" title="시차 탓에 한쪽만 먼저 지급하고 상대는 갚지 않는 외환 결제 리스크(1974년 Herstatt 은행 파산에서 유래)">Herstatt 리스크</abbr> 제거** |
| **CT Settle** | fiat·암호자산·스테이블코인 간 DvP 넷팅 결제 | 원자적 DvP + 차액결제 |

추가로 **CT Clear**(중앙청산, `ClearToken CCP Limited`)를 위해 영란은행(BoE) 인가를 추진 중.

## 규제 지위

- `ClearToken Depository Limited` — **FCA 인가**(2025-12 기준) 수탁기관(Depository) 겸 인가 결제기관(Authorised Payment Institution).
- `ClearToken CCP Limited` — 청산 서비스(CT Clear)용, BoE 인가 추진.
- 즉 ClearToken의 차별점은 기술이 아니라 **"규제 인가받은 중앙 결제소를 토큰 레일 위에 구현"** 했다는 점.

## "무슨 말일까"에 대한 답

- **같은 것**: Canton Network, <abbr class="gloss" title="다자간 워크플로를 위해 설계된 Canton의 스마트 컨트랙트 언어">Daml</abbr>, 원자적 DvP/PvP, Herstatt(결제 시점차) 리스크 제거라는 토대.
- **다른 것**: ClearToken은 **규제·중앙화로 fiat까지** 먹는 노선이고, Musubi는 **분산·스테이블코인 특화** 노선이다.
- **시사점**: Canton DvP 인프라를 정반대 포지셔닝으로 푸는 경쟁/참고 사례. ClearToken이 "인가 + fiat 포함"으로 기관 시장을 노리는 만큼, Musubi는 **분산성·스테이블코인 특화·한일 회랑(corridor)** 이라는 차별점을 어떻게 방어·강조할지 점검할 신호.

## 참고 링크
- [원자적 DvP가 진짜 차별점](atomic-dvp-real-differentiator.md) — DvP/<abbr class="gloss" title="트랜잭션이 전부 적용되거나 전혀 적용되지 않는 성질. 일부만 반영되는 일이 없음">원자성</abbr>이 왜 핵심인가
- [DvP 정산 앱 아키텍처](dvp-settlement-app-architecture.md) — Musubi 정산 앱 구조
- [Canton B2B vs B2C](canton-b2b-vs-b2c.md) — Canton이 B2B 정산에 쓰이는 이유
- [토큰 발행·브릿지 패턴](token-issuance-bridge-patterns.md) — 멀티체인 스테이블코인 발행 구조

> 참고 링크의 상대경로는 위키(`wiki/notes/`) 기준 — 이 메모를 위키 밖에서 볼 땐 해당 노트를 위키에서 찾으면 된다.
