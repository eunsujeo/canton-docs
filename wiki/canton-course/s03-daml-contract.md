---
title: S3 — Daml 컨트랙트
type: note
translated: 2026-06-23
status: done
tags: [course, s03, daml, 컨트랙트, choice]
---

> **학습 코스 (번역본 아님)** — [코스 맵](index.md) · 이전: [S2](s02-party-ownership.md)

# S3 — Daml 컨트랙트

## 질문
**"보낸다"·"맞교환한다"는 규칙은 어떻게 코드가 되나? 솔리디티랑 뭐가 다른가? 코드는 실제로 어떻게 생겼나?**

## 기초

Canton에서 비즈니스 규칙은 **<abbr class="gloss" title="다자간 워크플로를 위해 설계된 Canton의 스마트 컨트랙트 언어">Daml</abbr>** 언어로 쓴 **<abbr class="gloss" title="컨트랙트의 구조와 규칙(권한·초이스)을 정의하는 Daml 청사진">템플릿</abbr>(template)**이 된다. 템플릿은 두 가지를 정의한다.

1. **데이터** — 이 <abbr class="gloss" title="원장에 기록되는 불변 데이터 단위. 상태 변경은 새 컨트랙트 생성으로 표현됨">컨트랙트</abbr>가 담는 필드(누가 보내는지, 얼마인지 등).
2. **규칙** — 누가, 무엇을, 어떤 조건에서 할 수 있는지(**choice**).

배포하면 템플릿은 **틀**이고, 실제 <abbr class="gloss" title="거래·컨트랙트가 기록되는 장부. Canton에선 활성 컨트랙트의 모음">원장</abbr> 위의 데이터 한 줄이 **컨트랙트(contract)** 한 건이다. 클래스와 인스턴스 관계로 보면 된다.

### 컨트랙트 = 활성 원장의 한 줄, choice = 그 줄에 대한 동작
- 컨트랙트가 **활성(active)**이라는 건 "지금 유효한 원장 상태"라는 뜻. 이 활성 집합이 [S4](s04-nodes-ledger.md)의 **<abbr class="gloss" title="활성 컨트랙트 집합(Active Contract Set). 노드가 보관 중인, 현재 유효한 컨트랙트 전체">ACS</abbr>**다.
- **choice**를 실행(exercise)하면 동작이 일어난다. choice는 두 종류:
  - **소비형(consuming)** — 실행하면 그 컨트랙트를 **<abbr class="gloss" title="컨트랙트를 소비해 비활성으로 만드는 것(archive). 보관된 컨트랙트는 더 이상 쓸 수 없음">보관</abbr>(archive)**한다. 즉 활성에서 빠진다. 상태 변경은 "옛 컨트랙트 보관 + 새 컨트랙트 생성"으로 표현된다.
  - **비소비형(nonconsuming)** — 컨트랙트를 그대로 둔 채 동작만 한다(예: 조회, 단계적 승인).

이더리움이 "가변 상태 변수를 덮어쓰기"라면, Canton은 **불변 컨트랙트를 보관하고 새것을 만드는** <abbr class="gloss" title="확장 UTXO. 금액만이 아니라 임의의 상태·규칙을 담는 컨트랙트로 원장을 구성하는 모델">eUTXO</abbr>식이다.

### 권한: signatory / observer / controller
- **signatory** — 이 컨트랙트가 존재하려면 동의가 필요한 <abbr class="gloss" title="Canton에서 권한과 데이터 가시성의 주체가 되는 식별 가능한 참여 주체">파티</abbr>(주된 권한자).
- **observer** — 동의권은 없지만 이 컨트랙트를 볼 수 있는 파티.
- **controller** — 특정 choice를 **실행할 수 있는** 파티. choice마다 다르게 지정한다.

### 이더리움 비교 — 솔리디티와 무엇이 다른가
| | 솔리디티(EVM) | Daml |
|---|---|---|
| 호출 권한 | 기본적으로 **누구나** 호출, 함수 안에서 `require(msg.sender==…)`로 직접 검사 | choice의 **controller**로 권한이 타입에 박힘 |
| 행위자 수 | `msg.sender` 한 명 | 한 <abbr class="gloss" title="원장 상태를 바꾸는 원자적 작업 단위. 하나 이상의 컨트랙트를 생성·보관하며, 전부 적용되거나 전혀 적용되지 않음">트랜잭션</abbr>에 **여러 <abbr class="gloss" title="컨트랙트의 주된 권한자. 생성·보관(소비)에 반드시 동의해야 하는 파티">서명자</abbr>** 가능 |
| 상태 | 가변 변수 덮어쓰기 | 불변 컨트랙트 보관 + 새 생성 |
| 가시성 | 전부 공개 | signatory·observer만 |
| 권한 실수 | 검사 누락 시 누구나 호출(흔한 취약점) | 권한이 구조라 "검사 깜빡"이 구조적으로 어려움 |

## 심화

### 가르치기용 송금 템플릿 (구조 감각)
아래는 **개념 설명용**으로 단순화한 송금 컨트랙트다(실제 패키지 코드가 아니라 구조를 보이려는 예시).

```daml
template MoneyTransfer with
    sender   : Party       -- 국내 기관 A
    receiver : Party       -- 해외 기관 B
    amount   : Decimal
  where
    signatory sender       -- 보내는 쪽이 주된 권한자
    observer  receiver     -- 받는 쪽은 볼 수 있음

    choice Transfer_Execute : ContractId MoneyTransfer
      controller sender    -- 이 동작은 sender만 실행 가능
      do
        -- 소비형: 이 컨트랙트는 보관되고, 결과 컨트랙트가 새로 생긴다
        create this with sender = receiver
```

읽는 법: `MoneyTransfer`는 보내는 A가 서명자, 받는 B가 <abbr class="gloss" title="컨트랙트를 볼 수 있으나 단독으로 행위할 수는 없는 파티">관찰자</abbr>. `Transfer_Execute`는 A만(`controller sender`) 실행할 수 있고, 실행하면 이 컨트랙트는 보관되고 새 컨트랙트가 생긴다.

### 실제 정산 패키지의 권한 선언 (검증된 코드)
이 PoC의 정산 패키지에는 `SettlementProposal`이라는 실제 템플릿이 있다. 권한 선언 부분만 보면:

```daml
template SettlementProposal with
    venue        : Party                 -- 운영사(정산에서만 등장; S6)
    transferLegs : TextMap TransferLeg   -- 맞교환의 두 다리
    approvers    : [Party]               -- 동의한 거래 당사자들
  where
    signatory approvers                  -- 동의한 당사자들이 서명자
    observer  venue, tradingParties transferLegs

    choice SettlementProposal_Accept : ContractId SettlementProposal
      with approver : Party
      controller approver                -- 각 당사자가 자기 동의를 더함
      do ...                             -- 제안서를 보관하고, 승인자를 추가한 새 제안서를 생성
```

핵심만: **서명자가 리스트(`approvers`)**다 — 여러 당사자가 함께 권한자다. `SettlementProposal_Accept`는 **소비형**이며, 반환형이 `ContractId SettlementProposal`인 데서 보이듯 한 당사자가 승인하면 **제안서를 보관하고 승인자를 추가한 새 제안서를 만든다**. 이 "보관 + 재생성"으로 서명자가 한 명씩 쌓이는 게 Daml의 **단계적 다자 동의** 패턴이다 — 솔리디티에선 까다롭지만 Daml에선 자연스럽다. 이 choice들의 전체 시퀀스는 [S7](s07-scenario-flows.md)에서 본다.

## 강의 노트
- **핵심 한 문장**: "솔리디티는 '누구나 호출, 함수 안에서 권한 검사', Daml은 '권한이 choice의 controller로 타입에 박힘'. 그래서 권한 실수가 구조적으로 어렵다."
- **비유**: 템플릿 = 양식(서식). 컨트랙트 = 그 양식을 채운 한 장. choice = 그 장에 누가 도장 찍을 수 있나.
- **무엇을 보여주며 짚을지**: 위 `MoneyTransfer`에서 `signatory`/`observer`/`controller` 세 줄을 손가락으로 짚는다. 그다음 실제 `SettlementProposal`의 `signatory approvers`(리스트!)를 보여주며 "다자 권한"을 강조.
- **예상 질문 & 답**:
  - Q: "상태를 그냥 못 바꾸나요? 매번 새 컨트랙트?" → A: "그렇다. 불변+보관/생성. 이게 <abbr class="gloss" title="같은 자산을 두 번 쓰는 부정행위">이중지불</abbr>을 구조적으로 막는다(S4)."
  - Q: "Daml은 어디서 도나요? EVM 같은 게 있나요?" → A: "각 <abbr class="gloss" title="파티를 호스팅하고 그 파티의 컨트랙트를 저장·실행하는 노드. 밸리데이터의 핵심 구성요소">참여자 노드</abbr> 안에서 실행된다. 전역 VM이 아니라 당사자 노드들에서. S4·S9."

## 다음 단계
규칙은 코드가 됐다. 그럼 이 컨트랙트들은 어디에 저장되나 — 글로벌 체인인가? → [S4 — 참여자 노드 & 원장](s04-nodes-ledger.md)

<!-- nav:start -->

---

⬅️ **이전**: [S2 — 파티 & 소유권](s02-party-ownership.md) ・ ➡️ **다음**: [S4 — 참여자 노드 & 원장](s04-nodes-ledger.md)

<!-- nav:end -->
