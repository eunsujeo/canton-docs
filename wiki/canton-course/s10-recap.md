---
title: S10 — 정리·실습·심화
type: note
translated: 2026-06-23
status: done
tags: [course, s10, 정리, 적합성]
---

> **학습 코스 (번역본 아님)** — [코스 맵](index.md) · 이전: [S9](s09-architecture.md)

# S10 — 정리·실습·심화

**여기까지 배운 걸 한 장에 묶으면? 그래서 언제 Canton이 맞고, 언제 안 맞나?**

## 핵심 차별 세 가지

| 차별점 | 한 줄 | 어디서 |
|---|---|---|
| 프라이버시 | 한 <abbr class="gloss" title="원장 상태를 바꾸는 원자적 작업 단위. 하나 이상의 컨트랙트를 생성·보관하며, 전부 적용되거나 전혀 적용되지 않음">트랜잭션</abbr>을 <abbr class="gloss" title="한 트랜잭션을 당사자별로 나눈 조각. 각 당사자는 자기 권한에 해당하는 뷰(자기 몫)만 받아 본다">뷰</abbr>로 쪼개 당사자에게만 배달(제3자 0건) | [S5](s05-privacy.md) |
| <abbr class="gloss" title="트랜잭션이 전부 적용되거나 전혀 적용되지 않는 성질. 일부만 반영되는 일이 없음">원자성</abbr> | 두 다리를 한 트랜잭션에 묶어 전부/전무 | [S6](s06-atomicity-dvp.md)·[S7](s07-scenario-flows.md) |
| 신원/<abbr class="gloss" title="트랜잭션이 되돌려지지 않는다고 보장되는 상태. 확률적(점점 굳음) vs 결정적(즉시 최종)">확정성</abbr> | 신원 기반 <abbr class="gloss" title="Canton에서 권한과 데이터 가시성의 주체가 되는 식별 가능한 참여 주체">파티</abbr> + 즉시 결정적 확정(되돌림 없음) | [S2](s02-party-ownership.md)·[S9](s09-architecture.md) |

이 셋은 따로따로면 다른 체인에도 있다. Canton의 가치는 **셋을 함께** 준다는 데 있다([S6](s06-atomicity-dvp.md)의 결합 논지).

## 같은 원리, 두 시나리오

| 개념 | 해외송금(주축) | 정산/<abbr class="gloss" title="인도-대-지급(Delivery vs Payment). 자산 인도와 대금 지급을 동시·원자적으로 처리">DvP</abbr>(고급) |
|---|---|---|
| 파티(S2) | 보내는·받는 기관 | + <abbr class="gloss" title="정산에서 주문을 매칭하고 원자적 실행을 개시하는 중립 당사자(venue). 자산을 보관하진 않음">운영사</abbr> |
| 규칙(S3) | transfer <abbr class="gloss" title="원장에 기록되는 불변 데이터 단위. 상태 변경은 새 컨트랙트 생성으로 표현됨">컨트랙트</abbr> | SettlementProposal/Settlement |
| 저장(S4) | 당사자 노드 <abbr class="gloss" title="활성 컨트랙트 집합(Active Contract Set). 노드가 보관 중인, 현재 유효한 컨트랙트 전체">ACS</abbr> | 〃 |
| 프라이버시(S5) | 당사자만 | 당사자만 |
| 원자성(S6) | 단일 이전(확정) | 두 다리 전부/전무 |
| 흐름(S7) | 단일 transfer | 제안→수락→개시→잠금→실행 |
| 토큰(S8) | <abbr class="gloss" title="토큰(자산)의 발행자가 운영하며 발행·소각과 정산 증빙(choice context)을 책임지는 주체">레지스트리</abbr> 발행 자산 | 〃(두 통화) |
| 확정(S9) | 즉시 최종 | 즉시 최종 |

전통(국경 간) 대비 줄어드는 것도 한눈에 정리된다 — <abbr class="gloss" title="다른 나라 은행과 제휴해 국경 간 송금·결제를 대행하는 중개 은행(correspondent bank)">환거래은행</abbr> 사슬·중앙 정산기관 같은 **중개**, T+1~<abbr class="gloss" title="거래 체결(T) 후 2영업일 뒤에 실제 결제가 이뤄지는 전통 금융 관행">T+2</abbr>의 **시간**, 별도 장부 **대조(reconciliation)**, 그리고 맞교환의 **<abbr class="gloss" title="거래 상대가 의무(지급·인도)를 이행하지 않을 위험">카운터파티 리스크</abbr>**가 사라진다.

## 언제 Canton이 맞고, 언제 안 맞나

만능 도구가 아니다. 용도에 맞게 써야 한다.

**맞는 곳 — 기관 간(B2B) 워크플로.** 거래 상대·금액이 비공개여야 하는 기관 정산, 신원 기반 참여가 필요한 규제 환경(KYC된 상대와만), 다자 동의·원자적 맞교환·즉시 완결성이 중요한 정산·증권·국경 간 거래.

**안 맞는 곳.** 리테일·B2C 대중 서비스(파티 생성·노드 운영 비용과 UX 면에서 퍼블릭 체인/일반 결제가 보통 낫다), 완전 공개·익명 DeFi(투명·무허가가 목적이면 퍼블릭 체인이 적합 — Canton의 강점인 프라이버시·신원이 오히려 안 맞는다), 단순 1:1 공개 이체만 필요한 경우.

> 한 줄: **B2B 기관 정산엔 강하고, 리테일·퍼블릭 DeFi엔 약하다.**

## 다른 시나리오로, 그리고 직접 해보기

이 코스의 두 시나리오(송금·정산)는 같은 원리의 두 적용이었다. 같은 개념으로 <abbr class="gloss" title="실물·금융 자산을 원장 위의 토큰(컨트랙트)으로 표현하는 것">토큰화</abbr> 증권 결제, 신디케이트 대출, 공급망 금융 등으로 확장된다 — 파티·규칙·프라이버시·원자성·확정성은 그대로다.

직접 굴려보려면 공식 LocalNet QuickStart로 <abbr class="gloss" title="파티를 호스팅하고 그 파티의 컨트랙트를 저장·실행하는 노드. 밸리데이터의 핵심 구성요소">참여자 노드</abbr>·<abbr class="gloss" title="상태를 저장하지 않고 트랜잭션 합의·순서를 조율하는 Canton 구성요소">Synchronizer</abbr>·발행자를 띄우고 라이선싱/정산 워크플로를 실행해 본다([appdev/quickstart](../appdev/quickstart/index.md)). 파티별로 ACS를 질의해 [S5](s05-privacy.md)의 "당사자는 보고 제3자는 0건"을 눈으로 <abbr class="gloss" title="이해관계자 밸리데이터가 트랜잭션이 유효함을 미디에이터에 응답하는 것(confirmation)">확인</abbr>할 수 있다.

더 깊이 들어가려면 공식 번역 위키를 본다 — <abbr class="gloss" title="거래·컨트랙트가 기록되는 장부. Canton에선 활성 컨트랙트의 모음">원장</abbr>·트랜잭션은 [원장 모델](../overview/learn/ledger-model.md)·[트랜잭션 작동 방식](../overview/learn/how-transactions-work.md), 프라이버시·신뢰는 [프라이버시 모델](../overview/learn/privacy-model.md)·[신뢰 모델](../overview/learn/trust-model.md), <abbr class="gloss" title="여러 노드가 트랜잭션의 유효성·순서에 함께 동의하는 절차">합의</abbr>·확정은 [2계층 합의](../overview/learn/two-layer-consensus.md)·[글로벌 Synchronizer 아키텍처](../overview/learn/global-synchronizer-architecture.md), 이더리움 배경이면 [블록체인 개발자를 위한 Canton (모듈 2)](../appdev/modules/m2-canton-for-ethereum-devs.md)이 좋은 진입점이다.

[코스 맵으로 돌아가기](index.md) · 처음부터: [S1](s01-problem.md)

<!-- nav:start -->

---

⬅️ **이전**: [S9 — 아키텍처 & 합의·확정](s09-architecture.md) ・ ➡️ **다음**: [Canton Coin과 글로벌 Synchronizer](../overview/understand/canton-coin.md)

<!-- nav:end -->
