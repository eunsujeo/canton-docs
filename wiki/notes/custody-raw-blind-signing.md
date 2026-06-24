---
title: 외부 파티 키는 누가 보관·서명하나 — raw signing & blind signing
type: note
translated: 2026-06-24
status: done
tags: [개요, 정리, note, 파티, 키관리, 커스터디, 신뢰모델, 서명]
---

> ⚠️ **내부 작성 정리 노트** — Canton 공식 문서의 충실 번역본이 아니라, 학습을 돕기 위해 직접 작성한 배경 설명입니다. 사실관계는 아래 참고 링크로 <abbr class="gloss" title="이해관계자 밸리데이터가 트랜잭션이 유효함을 미디에이터에 응답하는 것(confirmation)">확인</abbr>하세요.

# 외부 파티 키는 누가 보관·서명하나 — raw signing & blind signing

<abbr class="gloss" title="키를 파티 주인이 직접 보관하고 거래마다 외부 서명하는 파티(=자기수탁). '외부'는 노드 시점 — 키가 노드 밖에 있음">외부 파티</abbr>는 "키를 본인이 직접 쥔다(자기수탁)"고 했다([로컬 파티 vs 외부 파티](local-vs-external-party.md)). 그런데 "직접"이 꼭 *내 손에 든 USB*를 뜻하진 않는다 — 키를 안전하게 **<abbr class="gloss" title="컨트랙트를 소비해 비활성으로 만드는 것(archive). 보관된 컨트랙트는 더 이상 쓸 수 없음">보관</abbr>하고 서명해 주는 <abbr class="gloss" title="자산·키를 대신 보관·관리해 주는 수탁 서비스. 자기 보관, 서드파티(MPC), 노드월렛 등">커스터디</abbr>(수탁) 솔루션**에 맡길 수 있다. 그러면 자연히 묻게 된다: **그런 커스터디가 Canton 거래를 서명할 수 있나? 어디까지 안전한가?**

핵심부터: **가능하다. 단, 커스터디가 거래 내용을 못 보고 서명하는 "<abbr class="gloss" title="raw signing의 다른 이름. 서명기가 거래의 의미를 못 보고 서명 → 정상 거래와 악성 drain 거래를 구분 못 함">blind signing</abbr>"이 되기 쉬워, 악성 거래를 커스터디 계층에서 막지 못한다는 대가가 따른다.**

## 1. 외부 파티 서명의 실제 모양 = "해시에 서명"

외부 <abbr class="gloss" title="Canton에서 권한과 데이터 가시성의 주체가 되는 식별 가능한 참여 주체">파티</abbr>가 거래를 서명하는 흐름은 <abbr class="gloss" title="원장 상태를 바꾸는 원자적 작업 단위. 하나 이상의 컨트랙트를 생성·보관하며, 전부 적용되거나 전혀 적용되지 않음">트랜잭션</abbr> 통째가 아니라 **짧은 해시 한 조각**에 서명하는 것이다(상세는 [로컬 파티 vs 외부 파티](local-vs-external-party.md)의 prepare/execute 참고):

1. **준비(Prepare)** — <abbr class="gloss" title="파티를 호스팅하고 그 파티의 컨트랙트를 저장·실행하는 노드. 밸리데이터의 핵심 구성요소">참여자 노드</abbr>가 트랜잭션을 만들고 그 **<abbr class="gloss" title="참여자 노드가 준비한 트랜잭션. 외부 파티는 이것의 해시에 서명한다">prepared transaction</abbr>의 해시**(짧은 byte[])를 돌려준다.
2. **서명(Sign)** — 파티 키로 **그 해시에 서명**한다. ← 이 단계가 곧 커스터디 업계 용어로 **<abbr class="gloss" title="거래 내용 해석 없이 주어진 해시(byte[])에 그대로 서명하는 것. 외부 파티 서명이 이 형태라 일반 커스터디로 운용 가능">raw signing</abbr>**.
3. **실행(Execute)** — 서명을 붙여 <abbr class="gloss" title="상태를 저장하지 않고 트랜잭션 합의·순서를 조율하는 Canton 구성요소">Synchronizer</abbr>로 보낸다.

즉 서명기 입장에서 보이는 건 "이 byte[]에 서명하라"가 전부다. 여러 당사자가 얽힌 <abbr class="gloss" title="다자간 워크플로를 위해 설계된 Canton의 스마트 컨트랙트 언어">Daml</abbr> <abbr class="gloss" title="원장에 기록되는 불변 데이터 단위. 상태 변경은 새 컨트랙트 생성으로 표현됨">컨트랙트</abbr> 호출이라도, 서명해야 하는 대상은 결국 **하나의 해시**다.

## 2. 그래서 커스터디 선택지가 넓다

서명 대상이 "임의의 해시"이기만 하면, **그 해시에 서명해 줄 수 있는 무엇이든** 외부 파티의 키 보관소가 될 수 있다.

| 커스터디 방식 | 설명 |
|---|---|
| **자기 보관** | 파티 주인이 키를 직접 들고 서명(가장 단순한 자기수탁) |
| **서드파티 커스터디(<abbr class="gloss" title="Multi-Party Computation. 키를 여러 조각으로 분산 보관해 단일 노출 없이 함께 서명하는 커스터디 기법">MPC</abbr>)** | Fireblocks·DFNS 같은 솔루션이 키를 분산 보관하고 raw signing 제공 |
| **노드월렛** | 참여자 노드에 파티 키를 네이티브로 발급·<abbr class="gloss" title="참여자 노드가 파티를 대신해 원장에서 활동(컨트랙트 저장·트랜잭션 제출·확인)해 주는 것. 로컬 파티는 키까지 노드가 관리하고, 외부 파티는 제출 키를 파티 자신이 보유(노드는 중계)">호스팅</abbr> |

→ raw signing(임의 해시 서명)을 지원하는 커스터디라면, 다자간 Daml 호출도 그 위에서 승인할 수 있다. 이게 "Canton 외부 파티를 일반 커스터디로 운용할 수 있다"의 근거다.

## 3. 대가 — blind signing은 악성 거래를 못 거른다

raw signing의 다른 이름이 **blind signing**이다. 서명기가 거래의 *의미*를 못 보고 byte[]만 서명하기 때문이다.

- 커스터디 입장에서 **정상 <abbr class="gloss" title="인도-대-지급(Delivery vs Payment). 자산 인도와 대금 지급을 동시·원자적으로 처리">DvP</abbr> 거래**와 **"내 holding 전부를 공격자에게 보내라"는 <abbr class="gloss" title="소유자 키로 그 소유자의 자산 전부를 공격자에게 빼내는 악성 거래">drain</abbr> 거래**는 **둘 다 그냥 byte[]** → 구분 불가.
- Canton에서 내 holding을 옮기려면 내 서명이 필요한데, 그 키가 커스터디에 있으니 **drain 거래도 내 정당한 서명으로 통과**된다.
- 그래서 위협이 "키 탈취"에서 **"서명기에 악성 해시를 먹이는 것"**(= prepare 단계 장악)으로 옮겨간다.

## 4. 그럼 방어는 어디로 옮기나

커스터디 정책엔진이 눈을 감으므로, 방어선을 다른 계층으로 옮겨야 한다.

| 방어 계층 | drain을 막나 | 한계 |
|---|---|---|
| 커스터디 거래 정책(예: Fireblocks TAP) | Canton 거래엔 **못 막음** | 내용을 못 봐서 무력 |
| Daml 컨트랙트 제약(signatory·precondition) | 워크플로 오용은 막음 | "owner가 자기 토큰을 전송"은 본질적으로 허용 → 막기 어려움 |
| prepare 단계 보안(누가 해시를 만드나) | **실질적 방어선** | 앱·참여자 노드가 뚫리면 그대로 통과 |
| <abbr class="gloss" title="What You See Is What You Sign. 서명 직전 거래를 디코딩해 내용을 확인·승인하는 것 — 되면 더 이상 blind signing이 아님">WYSIWYS</abbr>(서명 전 해시를 독립 검증) | 이상적 해법 | 커스터디가 Canton 거래를 **디코딩**해야 성립 |

> **WYSIWYS** = "What You See Is What You Sign". 서명 직전 커스터디(또는 보조 검증기)가 prepared transaction을 **디코딩해 내용을 확인**하고 승인/거부하면, 그 순간 더 이상 blind signing이 아니다. 커스터디에 co-signer/callback 검증 훅을 걸 수 있는지가 관건.

## 5. "옴니버스로 뭉치면?" — 다른 함정

키 보관이 번거롭다고 **다수 고객을 <abbr class="gloss" title="거래·컨트랙트가 기록되는 장부. Canton에선 활성 컨트랙트의 모음">원장</abbr> 위 단 하나의 파티 아래로 뭉치고** 내부 DB로 누가 얼마인지 관리하면(옴니버스), 또 다른 문제가 생긴다([파티는 유저마다 만들까?](party-design-per-user-vs-omnibus.md) 참고):

- 같은 커스터디 고객끼리 거래는 **내부 장부 이전**이라 원장에 안 찍힌다 → 프라이버시·<abbr class="gloss" title="트랜잭션이 전부 적용되거나 전혀 적용되지 않는 성질. 일부만 반영되는 일이 없음">원자성</abbr>이 Canton 강제가 아니라 **DB 신뢰**로 강등.
- "고객 A 몫을 콕 집어 잠근다(allocate)"가 **원장 개념이 아니라 DB 메모**가 된다.

→ 실제 거래 당사자가 1급 파티여야 하는 **기관 간 정산**이면 옴니버스는 치명적이고, **다수의 진짜 파티**가 필요하다 → 파티별 키를 네이티브로 발급하는 방식(노드월렛 등)이 자연스럽다. (반대로 고객이 온체인 정체성을 필요로 하지 않는 거래소형 B2C면 옴니버스로 충분.)

## 한 줄 정리

> 외부 파티 서명은 결국 **해시 한 조각(byte[])에 서명**하는 것이라 raw signing 커스터디로 운용할 수 있다. 단 그건 **blind signing**이라 커스터디가 악성 drain 거래를 못 거른다 → 방어를 **prepare 인프라 무결성·Daml 제약·WYSIWYS**로 옮겨야 한다.

## 참고 링크
- [로컬 파티 vs 외부 파티](local-vs-external-party.md) — 자기수탁/위탁 키 모델과 prepare/execute 서명 흐름
- [파티는 유저마다 만들까? — per-user vs 옴니버스](party-design-per-user-vs-omnibus.md) — 옴니버스 한계와 파티 입도
- [로컬·외부 파티(원문 번역)](../overview/reference/external-party.md) — 권한·키·제출 흐름 전체
- [Create a new transaction (Fireblocks API)](https://developers.fireblocks.com/api-reference/transactions/create-a-new-transaction) — raw signing 트랜잭션 생성 레퍼런스

<!-- nav:start -->

---

⬅️ **이전**: [ClearToken vs Musubi — 같은 Canton DvP, 정반대 포지셔닝](cleartoken-vs-musubi.md) ・ ➡️ **다음**: [Canton 위 기관 간 DvP 정산 앱 — 2층 구조](dvp-settlement-app-architecture.md)

<!-- nav:end -->
