---
title: S3 — Daml 컨트랙트
type: note
translated: 2026-06-23
status: done
tags: [course, s03, daml, 컨트랙트, choice]
---

> **학습 코스 (번역본 아님)** — [코스 맵](index.md) · 이전: [S2](s02-party-ownership.md)

# S3 — Daml 컨트랙트

**"보낸다"·"맞교환한다"는 규칙은 어떻게 코드가 되나? 솔리디티와 뭐가 다르고, 코드는 실제로 어떻게 생겼나?**

Canton에서 비즈니스 규칙은 **<abbr class="gloss" title="다자간 워크플로를 위해 설계된 Canton의 스마트 컨트랙트 언어">Daml</abbr>** 언어로 쓴 **<abbr class="gloss" title="컨트랙트의 구조와 규칙(권한·초이스)을 정의하는 Daml 청사진">템플릿</abbr>(template)**이 된다. 템플릿은 두 가지를 정의한다 — 이 <abbr class="gloss" title="원장에 기록되는 불변 데이터 단위. 상태 변경은 새 컨트랙트 생성으로 표현됨">컨트랙트</abbr>가 담는 **데이터**(누가 보내는지, 얼마인지)와, 누가 무엇을 할 수 있는지의 **규칙(choice)**이다.

## 템플릿은 틀, 컨트랙트는 활성 원장의 한 줄

배포된 템플릿은 **틀**이고, 그 틀로 만들어진 <abbr class="gloss" title="거래·컨트랙트가 기록되는 장부. Canton에선 활성 컨트랙트의 모음">원장</abbr> 위의 데이터 한 줄이 **컨트랙트** 한 건이다. 클래스와 인스턴스 관계로 보면 된다. 컨트랙트가 **활성(active)**이라는 건 "지금 유효한 원장 상태"라는 뜻이고, 이 <abbr class="gloss" title="아직 보관(소비)되지 않아 현재 유효한 컨트랙트">활성 컨트랙트</abbr>의 모음이 [S4](s04-nodes-ledger.md)의 <abbr class="gloss" title="활성 컨트랙트 집합(Active Contract Set). 노드가 보관 중인, 현재 유효한 컨트랙트 전체">ACS</abbr>다.

상태를 바꾸려면 **choice**를 실행(exercise)한다. choice는 두 종류다.

- **소비형(consuming)** — 실행하면 그 컨트랙트를 **<abbr class="gloss" title="컨트랙트를 소비해 비활성으로 만드는 것(archive). 보관된 컨트랙트는 더 이상 쓸 수 없음">보관</abbr>(archive)**한다. 활성에서 빠진다. 상태 변경은 "옛 컨트랙트 보관 + 새 컨트랙트 생성"으로 표현된다.
- **비소비형(nonconsuming)** — 컨트랙트를 그대로 둔 채 동작만 한다(조회 등).

이더리움이 "가변 상태 변수를 덮어쓰기"라면 Canton은 **불변 컨트랙트를 보관하고 새것을 만드는** <abbr class="gloss" title="확장 UTXO. 금액만이 아니라 임의의 상태·규칙을 담는 컨트랙트로 원장을 구성하는 모델">eUTXO</abbr>식이다. 같은 컨트랙트를 두 번 소비할 수 없으니 <abbr class="gloss" title="같은 자산을 두 번 쓰는 부정행위">이중지불</abbr>이 구조적으로 막힌다([S4](s04-nodes-ledger.md)).

## 권한이 코드에 박힌다

솔리디티 함수는 기본적으로 누구나 호출할 수 있고, 함수 안에서 `require(msg.sender == owner)`처럼 직접 권한을 검사한다. 검사를 깜빡하면 그대로 취약점이 된다. Daml은 권한을 타입에 박는다.

- **signatory** — 이 컨트랙트가 존재하려면 동의가 필요한 <abbr class="gloss" title="Canton에서 권한과 데이터 가시성의 주체가 되는 식별 가능한 참여 주체">파티</abbr>.
- **observer** — 동의권은 없지만 볼 수 있는 파티.
- **controller** — 특정 choice를 실행할 수 있는 파티. choice마다 지정한다.

"누가 실행할 수 있나"가 함수 본문의 검사가 아니라 choice의 선언에 들어가므로, "권한 검사 누락" 같은 실수가 구조적으로 어렵다.

## 송금 규칙을 컨트랙트로 옮기면

개념을 단순화한 송금 컨트랙트는 이렇게 생겼다(구조를 보이기 위한 예시 — 실제 패키지 코드는 아래에서 따로 본다).

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
        create this with sender = receiver   -- 소비형: 이 컨트랙트는 보관되고 결과가 새로 생긴다
```

`MoneyTransfer`는 보내는 A가 <abbr class="gloss" title="컨트랙트의 주된 권한자. 생성·보관(소비)에 반드시 동의해야 하는 파티">서명자</abbr>, 받는 B가 <abbr class="gloss" title="컨트랙트를 볼 수 있으나 단독으로 행위할 수는 없는 파티">관찰자</abbr>다. `Transfer_Execute`는 A만(`controller sender`) 실행할 수 있고, 실행하면 이 컨트랙트는 보관되고 새 컨트랙트가 생긴다.

## 실제 정산 패키지의 권한 선언

이 PoC의 정산 패키지에는 `SettlementProposal`이라는 실제 템플릿이 있다. 권한 선언과 첫 choice만 보면:

```daml
template SettlementProposal with
    venue        : Party                 -- 운영사(정산에서만 등장; S6)
    transferLegs : TextMap TransferLeg   -- 맞교환의 두 다리
    approvers    : [Party]               -- 동의한 거래 당사자들
  where
    signatory approvers                  -- 동의한 당사자들이 곧 서명자
    observer  venue, tradingParties transferLegs

    choice SettlementProposal_Accept : ContractId SettlementProposal
      with approver : Party
      controller approver
      do ...                             -- 제안서를 보관하고, 승인자를 추가한 새 제안서를 생성
```

눈여겨볼 점은 **서명자가 한 명이 아니라 리스트(`approvers`)**라는 것이다 — 여러 당사자가 함께 권한자다. `SettlementProposal_Accept`는 소비형이고 반환형이 `ContractId SettlementProposal`이다. 즉 한 당사자가 승인하면 제안서를 보관하고 **승인자를 추가한 새 제안서를 만든다**. 이 "보관 + 재생성"이 반복되며 서명자가 한 명씩 쌓이는 게 Daml의 단계적 다자 동의 방식이다. 솔리디티에선 오프체인 서명·사전 승인으로 우회해야 할 일이 여기선 원장 위 컨트랙트로 자연스럽게 남는다. 전체 choice 시퀀스는 [S7](s07-scenario-flows.md)에서 본다.

규칙은 코드가 됐다. 그럼 이 컨트랙트들은 어디에 저장될까 — 글로벌 체인인가, 내 노드인가? → [S4 — 참여자 노드 & 원장](s04-nodes-ledger.md)

<!-- nav:start -->

---

⬅️ **이전**: [S2 — 파티 & 소유권](s02-party-ownership.md) ・ ➡️ **다음**: [S4 — 참여자 노드 & 원장](s04-nodes-ledger.md)

<!-- nav:end -->
