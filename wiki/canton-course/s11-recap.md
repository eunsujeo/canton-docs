---
title: S11 — 정리·실습·심화
type: note
translated: 2026-06-23
status: done
tags: [course, s11, 정리, 적합성]
---

> **학습 코스 (번역본 아님)** — [코스 맵](index.md) · 이전: [S10](s10-finality-consensus.md)

# S11 — 정리·실습·심화

## 질문
**여기까지 배운 걸 한 장에 묶으면? 그래서 언제 Canton이 맞고, 언제 안 맞나?**

## 기초

### 핵심 차별 3가지 (한 장 요약)
| 차별점 | 한 줄 | 어디서 배웠나 |
|---|---|---|
| **프라이버시** | 한 <abbr class="gloss" title="원장 상태를 바꾸는 원자적 작업 단위. 하나 이상의 컨트랙트를 생성·보관하며, 전부 적용되거나 전혀 적용되지 않음">트랜잭션</abbr>을 <abbr class="gloss" title="한 트랜잭션을 당사자별로 나눈 조각. 각 당사자는 자기 권한에 해당하는 뷰(자기 몫)만 받아 본다">뷰</abbr>로 쪼개 당사자에게만 배달(제3자 0건) | [S5](s05-privacy.md) |
| **<abbr class="gloss" title="트랜잭션이 전부 적용되거나 전혀 적용되지 않는 성질. 일부만 반영되는 일이 없음">원자성</abbr>** | 두 다리를 한 트랜잭션에 묶어 전부/전무 | [S6](s06-atomicity-dvp.md), [S7](s07-scenario-flows.md) |
| **신원/<abbr class="gloss" title="트랜잭션이 되돌려지지 않는다고 보장되는 상태. 확률적(점점 굳음) vs 결정적(즉시 최종)">확정성</abbr>** | 신원 기반 <abbr class="gloss" title="Canton에서 권한과 데이터 가시성의 주체가 되는 식별 가능한 참여 주체">파티</abbr> + 즉시 결정적 확정(되돌림 없음) | [S2](s02-party-ownership.md), [S10](s10-finality-consensus.md) |

이 셋은 따로따로면 다른 체인에도 있다. Canton의 가치는 **셋을 함께** 준다는 것이다([S6](s06-atomicity-dvp.md)의 결합 논지).

### 두 시나리오에 어떻게 적용됐나
| 개념 | 해외송금(주축) | 정산/<abbr class="gloss" title="인도-대-지급(Delivery vs Payment). 자산 인도와 대금 지급을 동시·원자적으로 처리">DvP</abbr>(고급) |
|---|---|---|
| 파티(S2) | 보내는·받는 기관 | + <abbr class="gloss" title="정산에서 주문을 매칭하고 원자적 실행을 개시하는 중립 당사자(venue). 자산을 보관하진 않음">운영사</abbr> |
| 규칙(S3) | transfer <abbr class="gloss" title="원장에 기록되는 불변 데이터 단위. 상태 변경은 새 컨트랙트 생성으로 표현됨">컨트랙트</abbr> | SettlementProposal/Settlement |
| 저장(S4) | 당사자 노드 <abbr class="gloss" title="활성 컨트랙트 집합(Active Contract Set). 노드가 보관 중인, 현재 유효한 컨트랙트 전체">ACS</abbr> | 〃 |
| 프라이버시(S5) | 당사자만 | 당사자만 |
| 원자성(S6) | 단일 이전(확정) | 두 다리 전부/전무 |
| 흐름(S7) | 단일 transfer | 제안→수락→개시→잠금→실행 |
| 토큰(S8) | <abbr class="gloss" title="토큰(자산)의 발행자가 운영하며 발행·소각과 정산 증빙(choice context)을 책임지는 주체">레지스트리</abbr> 발행 자산 | 〃(두 통화) |
| 확정(S10) | 즉시 최종 | 즉시 최종 |

### 전통(국경 간) 대비 무엇을 줄이나
- **중개** — <abbr class="gloss" title="다른 나라 은행과 제휴해 국경 간 송금·결제를 대행하는 중개 은행(correspondent bank)">환거래은행</abbr> 사슬·중앙 정산기관 의존 ↓ (<abbr class="gloss" title="거래·컨트랙트가 기록되는 장부. Canton에선 활성 컨트랙트의 모음">원장</abbr> 위 직접·당사자 노드).
- **시간** — T+1~<abbr class="gloss" title="거래 체결(T) 후 2영업일 뒤에 실제 결제가 이뤄지는 전통 금융 관행">T+2</abbr> → 즉시 결정적 확정.
- **대조(reconciliation)** — 공유 컨트랙트는 같은 한 건이라 맞춰볼 게 없음.
- **<abbr class="gloss" title="거래 상대가 의무(지급·인도)를 이행하지 않을 위험">카운터파티 리스크</abbr>** — 원자적 DvP로 "한쪽만 가는" 일 제거.

## 심화

### 언제 Canton이 맞나 / 안 맞나 (균형)
**맞는 곳 — 기관 간(B2B) 워크플로**
- 거래 상대·금액이 **비공개여야** 하는 기관 정산.
- **신원 기반** 참여가 필요한 규제 환경(KYC된 상대와만).
- 다자 동의·원자적 맞교환·즉시 완결성이 중요한 정산·증권·국경 간.

**안 맞는 곳**
- **리테일·B2C 대중 서비스** — 파티 생성·노드 운영 비용, UX 면에서 퍼블릭 체인/일반 결제가 보통 낫다.
- **완전 공개·익명 DeFi** — Canton의 강점(프라이버시·신원)이 오히려 안 맞는 영역. 투명·무허가가 목적이면 퍼블릭 체인이 적합.
- 단순 1:1 공개 이체만 필요한 경우 — 굳이 Canton일 이유가 약하다.

> 한 줄: **B2B 기관 정산엔 강하고, 리테일·퍼블릭 DeFi엔 약하다.** 도구를 용도에 맞게.

### 다른 시나리오로 확장
이 코스의 두 시나리오(송금·정산)는 같은 원리의 두 적용이었다. 같은 개념으로 <abbr class="gloss" title="실물·금융 자산을 원장 위의 토큰(컨트랙트)으로 표현하는 것">토큰화</abbr> 증권 결제, 신디케이트 대출, 공급망 금융 등으로 확장된다 — 파티·규칙·프라이버시·원자성·확정성은 그대로다.

### 직접 해보기
- 공식 LocalNet QuickStart로 로컬에 <abbr class="gloss" title="파티를 호스팅하고 그 파티의 컨트랙트를 저장·실행하는 노드. 밸리데이터의 핵심 구성요소">참여자 노드</abbr>·<abbr class="gloss" title="상태를 저장하지 않고 트랜잭션 합의·순서를 조율하는 Canton 구성요소">Synchronizer</abbr>·발행자를 띄우고 라이선싱/정산 워크플로를 굴려본다([appdev/quickstart](../appdev/quickstart/index.md)).
- 파티별로 ACS를 질의해 [S5](s05-privacy.md)의 "당사자는 보고 제3자는 0건"을 직접 점검.
- 향후: 핵심 단계(프라이버시·정산 흐름)의 자기완결 인터랙티브 데모를 별도로 둘 수 있다(코스 Phase 2).

### 더 배울 거리 (공식 번역 위키)
- 원장·트랜잭션: [원장 모델](../overview/learn/ledger-model.md) · [트랜잭션 작동 방식](../overview/learn/how-transactions-work.md)
- 프라이버시·신뢰: [프라이버시 모델](../overview/learn/privacy-model.md) · [신뢰 모델](../overview/learn/trust-model.md)
- <abbr class="gloss" title="여러 노드가 트랜잭션의 유효성·순서에 함께 동의하는 절차">합의</abbr>·확정: [2계층 합의](../overview/learn/two-layer-consensus.md) · [글로벌 Synchronizer 아키텍처](../overview/learn/global-synchronizer-architecture.md)
- 이더리움 개발자: [블록체인 개발자를 위한 Canton (모듈 2)](../appdev/modules/m2-canton-for-ethereum-devs.md)

## 강의 노트
- **핵심 한 문장**: "프라이버시·원자성·신원/확정성 — 따로는 흔하지만 함께면 Canton. B2B 정산엔 강하고 리테일·퍼블릭 DeFi엔 약하다."
- **비유**: 스위스 군용칼이 아니라 정밀 수술도구. 만능이 아니라 '기관 정산'이라는 용도에 날카롭게 맞춰진 도구.
- **무엇을 보여주며 짚을지**: '핵심 차별 3' 표와 '맞는 곳/안 맞는 곳'을 나란히. 균형(과장 금지)을 강조.
- **예상 질문 & 답**:
  - Q: "결국 허가형 DB랑 뭐가 다른가요?" → A: "공유 컨트랙트로 대조가 사라지고, 원자성·결정적 확정·다자 권한이 프로토콜로 보장된다. 단일 운영자 DB가 아니라 상호 신뢰 없는 다자 원장."
  - Q: "우리 케이스가 B2B인지 B2C인지 헷갈려요." → A: "거래 상대가 기관이고 비공개·완결성이 핵심이면 B2B(Canton). 대중 소비자 대상이면 보통 퍼블릭 체인+브릿지."

## 코스 끝
[코스 맵으로 돌아가기](index.md) · 처음부터: [S0](s00-opening.md)

<!-- nav:start -->

---

⬅️ **이전**: [S10 — 확정성 & 합의](s10-finality-consensus.md) ・ ➡️ **다음**: [Canton Coin과 글로벌 Synchronizer](../overview/understand/canton-coin.md)

<!-- nav:end -->
