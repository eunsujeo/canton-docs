---
title: Synchronizer 종류 — 사설 vs 컨소시엄 vs 글로벌
type: note
translated: 2026-06-16
status: done
tags: [개요, 정리, note, synchronizer, 토폴로지]
---

> ⚠️ **내부 작성 정리 노트** — Canton 공식 문서의 충실 번역본이 아니라, 학습을 돕기 위해 직접 작성한 배경 설명입니다. 정확한 정의는 [아키텍처 개요](../overview/learn/architecture.md)·[다중 Synchronizer](../overview/learn/multi-synchronizer.md) 참고.

# Synchronizer 종류 — 사설 vs 컨소시엄 vs 글로벌

<abbr class="gloss" title="상태를 저장하지 않고 트랜잭션 합의·순서를 조율하는 Canton 구성요소">Synchronizer</abbr>는 **"누가 운영하고 누가 참여하느냐"** 에 따라 사설 → 컨소시엄 → 글로벌 스펙트럼이 있다. 운영 주체·참여 범위가 넓어질수록 탈중앙·신뢰분산이 커진다.

## 한눈에 비교

| | **사설(Private)** | **컨소시엄(Consortium)** | **글로벌(Global)** |
|---|---|---|---|
| **누가 운영** | 한 조직이 단독 | 여러 조직이 **공동** | <abbr class="gloss" title="글로벌 Synchronizer를 운영하고 네트워크 거버넌스에 참여하는 노드">슈퍼 밸리데이터</abbr>들(공개) |
| **누가 참여** | 그 조직(내부) | **정해진 멤버 그룹** | 누구나(온보딩하면) |
| **거버넌스** | 그 조직 단독 | 멤버들이 <abbr class="gloss" title="여러 노드가 트랜잭션의 유효성·순서에 함께 동의하는 절차">합의</abbr> | Canton Foundation·<abbr class="gloss" title="Canton 개선 제안(Canton Improvement Proposal). 네트워크 규칙·표준 변경을 제안·비준하는 절차">CIP</abbr> |
| **신뢰** | 운영자 1곳 신뢰 | 멤버 그룹에 분산(<abbr class="gloss" title="비잔틴 장애 허용(Byzantine Fault Tolerance). 일부 노드가 악의적이거나 고장 나도 시스템이 올바르게 동작하는 성질">BFT</abbr> 가능) | 독립 SV 전반에 분산(BFT) |
| **탈중앙화** | 낮음 | 중간 | 최대 |

## 한 줄씩

- **사설** = "우리 회사 전용 정산 창구." 한 조직이 운영·통제. 내부 워크플로·테스트용. → 그 운영자를 믿어야 함.
- **컨소시엄** = "몇몇 기관이 공동 운영하는 정산 창구." 정해진 멤버(예: 은행 컨소시엄)끼리. 운영·규칙을 함께 거버넌스, 신뢰가 그룹에 분산.
- **글로벌** = "모두가 쓰는 공개 창구." 독립 SV들이 운영, 최대 탈중앙·BFT.

> 비유: **사설** = 사내 결제 시스템 / **컨소시엄** = 몇몇 은행이 공동 설립한 청산소 / **글로벌** = 누구나 접속하는 공용 결제망.

## 알아둘 점

- 한 참여자는 **여러 Synchronizer에 동시 연결** 가능(예: 사설 + 글로벌).
- 각 Synchronizer는 **자기만의 순서줄(total order)** 을 가진다 — <abbr class="gloss" title="원장에 기록되는 불변 데이터 단위. 상태 변경은 새 컨트랙트 생성으로 표현됨">컨트랙트</abbr>를 다른 Synchronizer로 옮기려면 **<abbr class="gloss" title="컨트랙트를 한 Synchronizer에서 다른 Synchronizer로 옮기는 프로토콜">재할당</abbr>(reassignment)** 프로토콜이 필요.
- **<abbr class="gloss" title="원장 위에서 규칙대로 자동 실행되는 코드화된 계약. Canton에선 Daml 템플릿으로 작성">스마트 컨트랙트</abbr> 합의(<abbr class="gloss" title="어떤 컨트랙트와 관계를 맺어 그것을 보거나 승인하는 파티 = 서명자 + 관찰자">이해관계자</abbr> 검증)는 종류와 무관하게 동일**; 달라지는 건 **순서화(ordering) 신뢰 모델**뿐 (사설=단일 운영자, 컨소시엄·글로벌=BFT).

## B2B 정산 맥락

- 특정 **기관 그룹끼리만** 정산하고 외부엔 닫고 싶다 → **컨소시엄 Synchronizer**
- 사전 관계 없는 **누구와도** 정산 → **글로벌**
- 내부 개발·테스트 → 사설 (또는 LocalNet)

## 참고 링크
- [아키텍처 개요](../overview/learn/architecture.md) — 단일/다중/글로벌 <abbr class="gloss" title="어떤 노드·파티·키가 네트워크에 참여하는지를 정의하는 구성 정보">토폴로지</abbr> 옵션
- [다중 Synchronizer 아키텍처](../overview/learn/multi-synchronizer.md) — 재할당·라우팅
- [2계층 합의](../overview/learn/two-layer-consensus.md) — 순서화 신뢰 모델은 Synchronizer마다 다름
- [신뢰 모델](../overview/learn/trust-model.md) · [환경 4단계](canton-environments-localnet-to-mainnet.md)

<!-- nav:start -->

---

⬅️ **이전**: [파티는 유저마다 만들까? — per-user vs 옴니버스](party-design-per-user-vs-omnibus.md) ・ ➡️ **다음**: [용어 한 컷 카드 — 자주 막히는 용어 모음](term-cheatsheet.md)

<!-- nav:end -->
