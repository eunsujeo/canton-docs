---
title: 원자적 DvP는 Canton만 되나? — 원자성·잠금·조합성, "이더도 되잖아?"에 답하기
type: note
translated: 2026-06-17
status: done
tags: [정리, note, DvP, 원자성, 조합성, 비교, 프라이버시]
---

> ⚠️ **내부 작성 정리 노트** — 학습 중 "원자적 <abbr class="gloss" title="인도-대-지급(Delivery vs Payment). 자산 인도와 대금 지급을 동시·원자적으로 처리">DvP</abbr>가 UTXO/Canton이라서 가능한 거냐"는 질문을 파고들어 정리한 것. 정확한 정의는 [용어집](../glossary.md)·각 페이지 참고.

# 원자적 DvP의 진짜 차별점

"DvP가 UTXO라서 가능하다 / Canton만 된다"는 말은 **방향은 맞지만 부정확**하다. DvP를 구성하는 3요소는 **다른 체인(특히 이더리움)에서도 된다.** Canton의 차별점은 개별 기능이 아니라 **그 조합 + 프라이버시 + 다자 권한 + 결정적 확정**이다.

## 3요소: 각각은 Canton 전용이 아니다

| 요소 | 출처 | 이더리움도? | Canton의 추가점 |
|---|---|---|---|
| **<abbr class="gloss" title="트랜잭션이 전부 적용되거나 전혀 적용되지 않는 성질. 일부만 반영되는 일이 없음">원자성</abbr>** (전부 or 전무) | **<abbr class="gloss" title="원장 상태를 바꾸는 원자적 작업 단위. 하나 이상의 컨트랙트를 생성·보관하며, 전부 적용되거나 전혀 적용되지 않음">트랜잭션</abbr> 모델**(UTXO 아님) | ✅ 한 <abbr class="gloss" title="원장에 기록되는 불변 데이터 단위. 상태 변경은 새 컨트랙트 생성으로 표현됨">컨트랙트</abbr> 호출 내 원자 스왑 | 결정적 확정(되감기 없음) |
| **자산 잠금** | 에스크로/allowance(이더) vs Locked 컨트랙트(Canton) | ✅ 에스크로·approve | **특정 컨트랙트(UTXO)를 집어 잠금** → 가변 잔액 아님, approve류 함정 없음 |
| **조합성** | "머니 레고" — 이더가 원조 | ✅ 매우 강력(DeFi) | **프라이버시 보존 + 다자 네이티브 권한** |

### ① 원자성 — 트랜잭션 성질이지 UTXO 덕분 아님
- "전부 성공 or 전부 롤백"은 **한 트랜잭션(한 `do` 블록)** 의 성질. 계정 모델(이더)도 한 호출 내에서 원자적.
- <abbr class="gloss" title="확장 UTXO. 금액만이 아니라 임의의 상태·규칙을 담는 컨트랙트로 원장을 구성하는 모델">eUTXO</abbr>는 그 안에서 자산을 **표현·소비**하는 방식일 뿐.

### ② 자산 잠금 — 이더도 되지만 "무엇을 잠그냐"가 다름
- 이더: **가변 잔액에 대한 권한**(allowance) 또는 에스크로로 이전. → 잔액 가변·approve 악용·레이스 위험.
- Canton(eUTXO): **특정 불변 코인 컨트랙트(Locked<abbr class="gloss" title="Canton Coin(CC)의 Daml/Scan상 기술적 이름. CC = Amulet">Amulet</abbr>/Allocation)** 를 집어 잠금. → 결정적, "내 밑에서 잔액이 변함" 없음.

### ③ 조합성 — 이더가 원조, Canton은 프라이버시+다자권한 추가
- 이더 조합: 강력하지만 **전부 공개** + **발신자 1명(msg.sender)**. 다자 동의는 오프체인 서명·사전 approve 필요.
- Canton 조합: **<abbr class="gloss" title="한 트랜잭션을 &quot;뷰&quot;로 분해해, 각 파티가 자신과 관련된 부분만 보도록 하는 Canton의 핵심 프라이버시 방식">부분 트랜잭션 프라이버시</abbr>**(각자 자기 다리만) + **한 트랜잭션에 여러 <abbr class="gloss" title="컨트랙트의 주된 권한자. 생성·보관(소비)에 반드시 동의해야 하는 파티">서명자</abbr> 네이티브**. 발행자 다른 자산도 원자 조합(예: <abbr class="gloss" title="글로벌 Synchronizer를 구동하는 오픈소스 애플리케이션 모음(SV·밸리데이터·월렛 등)">Splice</abbr>의 CC ↔ 우리 앱의 License).

## 그래서 Canton의 진짜 차별점 = "결합"
> 원자성·잠금·조합성은 다 흔하다. Canton이 기관 정산에 맞는 이유는 이것들을
> **① 프라이버시(거래 상대·금액 비공개) + ② 다자 네이티브 권한 + ③ 결정적 확정**
> 과 **함께** 제공하기 때문이다. 단일 기능이 아니라 묶음이 차별점.

## 실측 근거(LocalNet 라이선싱 예제)
`CompleteRenewal` 한 <abbr class="gloss" title="컨트랙트에서 수행 가능한 동작(권한이 부여된 당사자만 실행 가능)">초이스</abbr>가: 잠긴 CC(Splice 발행) 소비 + 옛 License(우리 앱) 폐기 + 새 License 생성을 **한 트랜잭션·원자적**으로 처리했고, **카운터<abbr class="gloss" title="Canton에서 권한과 데이터 가시성의 주체가 되는 식별 가능한 참여 주체">파티</abbr>는 자기 다리만** 봤다. → 발행자 다른 자산의 **프라이버시 보존 원자 조합**.

## 관련 문서
- [eUTXO와 이중지불 방지](eutxo-double-spend.md) · [BTC vs Ethereum vs Canton](btc-ethereum-canton-compare.md)
- [원장 모델 / 트랜잭션 작동](../overview/learn/how-transactions-work.md) · [프라이버시 모델](../overview/learn/privacy-model.md)
- [DvP 정산 앱 2층 구조](dvp-settlement-app-architecture.md)

<!-- nav:start -->

---

⬅️ **이전**: [데모 실행하기 (Running the Demo)](../appdev/quickstart/running-the-demo.md) ・ ➡️ **다음**: [블록체인 계층 (L0 / L1 / L2)와 Canton의 위치](blockchain-layers-l0-l1-l2.md)

<!-- nav:end -->
