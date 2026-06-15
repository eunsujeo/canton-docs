---
title: 원장 모델 (상세)
source: https://docs.canton.network/overview/reference/ledger-model-detailed
translated: 2026-06-15
status: done
tags: [overview, reference, 원장모델, 프로토콜, 형식명세]
---

> **출처(원문)**: [Ledger Model (Detailed)](https://docs.canton.network/overview/reference/ledger-model-detailed) · 번역일 2026-06-15

## 📌 개발자 노트
- **한 줄 요약**: Canton <abbr class="gloss" title="거래·컨트랙트가 기록되는 장부. Canton에선 활성 컨트랙트의 모음">원장</abbr> 모델의 형식 명세 — 구조(액션·<abbr class="gloss" title="원장 상태를 바꾸는 원자적 작업 단위. 하나 이상의 컨트랙트를 생성·보관하며, 전부 적용되거나 전혀 적용되지 않음">트랜잭션</abbr>·<abbr class="gloss" title="트랜잭션이 최종 확정되어 원장에 반영되는 것">커밋</abbr>·원장), 유효성(일관성·적합성·인가), 프라이버시(인포미·증인·투영·디벌전스·공개), 다중 <abbr class="gloss" title="상태를 저장하지 않고 트랜잭션 합의·순서를 조율하는 Canton 구성요소">Synchronizer</abbr> 상호운용성(멀티원장 인과성 그래프·원장 인지 투영). <abbr class="gloss" title="인도-대-지급(Delivery vs Payment). 자산 인도와 대금 지급을 동시·원자적으로 처리">DvP</abbr> 워크플로 예시 중심.
- **핵심 용어**: 액션(Create/Exercise/Fetch)·트랜잭션·커밋, 일관성·적합성·인가, <abbr class="gloss" title="컨트랙트의 주된 권한자. 생성·보관(소비)에 반드시 동의해야 하는 파티">서명자</abbr>/<abbr class="gloss" title="컨트랙트를 볼 수 있으나 단독으로 행위할 수는 없는 파티">관찰자</abbr>/액터, 인포미·증인·투영, 디벌전스·공개, 멀티원장 인과성 그래프
- **선행 개념**: [원장 모델](../learn/ledger-model.md), [프라이버시 모델](../learn/privacy-model.md), [인과성과 시간](ledger-causality.md).
- **참고**: 원문 첨자(actₙ, cₙ, txₙ 등)는 act1, c1, tx1 형태로 표기. 다수의 도식은 원문 이미지를 그대로 포함.

---

# 구조 (Structure)

이 절은 <abbr class="gloss" title="Canton에서 권한과 데이터 가시성의 주체가 되는 식별 가능한 참여 주체">파티</abbr> 간 상호작용을 원장 변경으로 기록하는 원장의 구조를 본다. 여기 제시된 정의는 첫 질문 "변경과 원장은 어떻게 생겼나?"를 다룬다. 기록된 상호작용의 기본 빌딩 블록은 액션(action)이며, 이는 트랜잭션, *업데이트*, *커밋*, 원장으로 그룹화된다.

## 실행 워크플로 예시

이 절의 대부분 예시는 실행 예제 <abbr class="gloss" title="컨트랙트의 구조와 규칙(권한·초이스)을 정의하는 Daml 청사진">템플릿</abbr>에 기반한 다음 <abbr class="gloss" title="다자간 워크플로를 위해 설계된 Canton의 스마트 컨트랙트 언어">Daml</abbr> Script 시나리오를 본다. 두 은행이 각각 Alice 또는 Bob에게 자산을 하나씩 발행한 뒤, Alice가 Bob에게 DvP를 제안한다. Bob이 제안을 수락하고 DvP를 정산한다.

```haskell
let eurAsset = SimpleAsset with
      issuer = bank1
      owner = alice
      asset = "1 EUR"
eur <- submit bank1 do createCmd eurAsset
    
let usdAsset = SimpleAsset with
      issuer = bank2
      owner = bob
      asset = "1 USD"
usd <- submit bank2 do createCmd usdAsset
    
proposeDvP <- submit alice $ do
  createCmd ProposeSimpleDvP with
      proposer = alice
      counterparty = bob
      allocated = eur
      expected = usdAsset
disclosedEur <- fromSome <$> queryDisclosure alice eur
```

수락과 정산은 `AcceptAndSettle` <abbr class="gloss" title="컨트랙트에서 수행 가능한 동작(권한이 부여된 당사자만 실행 가능)">초이스</abbr>로 단일 단계에 일어날 수 있다.

```haskell
(newUsd, newEur) <- submitWithDisclosures bob [disclosedEur] do
    exerciseCmd proposeDvP $ AcceptAndSettle with toBeAllocated = usd
```

또는 `Accept` 다음 `Settle`의 두 별도 단계로:

```haskell
dvp <- submit bob $
  do exerciseCmd proposeDvp $ Accept with toBeAllocated = usd

(newUsd, newEur) <- submitWithDisclosures bob [disclosedEur] do
    exerciseCmd dvp $ Settle with actor = bob
```

## 액션 (Actions)

### 계층 구조

원장 모델의 주요 특징 하나는 *계층적 액션 구조* 다. 이 구조는 위 시나리오에서 Bob이 `Settle` 초이스를 실행해 DvP를 정산하는 것으로 설명된다. Alice와 Bob은 자기 자산(<abbr class="gloss" title="원장에 기록되는 불변 데이터 단위. 상태 변경은 새 컨트랙트 생성으로 표현됨">컨트랙트</abbr> #1과 #2)을 `SimpleDvp` 컨트랙트(#4)에 할당했다. 이 컨트랙트들은 아래 다이어그램에서 입력(왼쪽의 점선 상자)으로 나타난다.

<img src="https://mintcdn.com/cantonfoundation/zmlOjLpKuDjnaObr/images/docs_website/dvp-settle-action.svg?fit=max&auto=format&n=zmlOjLpKuDjnaObr&q=85&s=92dcd6bdccf7c5050568bbe072b6cb47" alt="Alice와 Bob 간 SimpleDvp 컨트랙트의 정산 액션, 스왑의 두 다리를 결과로 가짐" width="1642" height="1093" />

`Settle` 초이스 실행은 Exercise 액션을 산출하며, 이는 파란색으로 표시된 노드 트리다. 왼쪽 입력 컨트랙트는 액션의 일부가 아니다. 루트 노드는 초이스의 파라미터를 기술하고 `SimpleDvp` 입력 컨트랙트 #4를 참조한다. 두 하위 트리를 가지며, `Settle` 초이스의 일부로 자산 이전을 자동 수행한다.

1. 왼쪽 하위 트리는 Alice가 자기 `SimpleAsset` 컨트랙트 #1에 `Transfer` 초이스를 실행하는 것을 나타낸다. 두 노드로 구성된다: 루트 노드는 초이스 파라미터와 입력 컨트랙트 #1을 기술한다. 자식 노드(자체로 한 노드 하위 트리)는 Bob의 새 `SimpleAsset` 컨트랙트 #5 생성을 인코딩한다.
2. 오른쪽 하위 트리는 유사하다: 하위 트리 루트 노드는 Bob이 자기 `SimpleAsset` 컨트랙트 #2에 `Transfer` 초이스를 실행하는 것을 기술하고, 그 자식은 Alice의 새 `SimpleAsset` 컨트랙트 #6 생성을 인코딩한다.

특히, 루트 노드가 이미 모든 관련 파라미터를 기술하더라도 Exercise 액션은 트리 전체다. 원장 모델은 노드가 아니라 액션에 집중하는데, 루트 노드가 자식 없이 단독으로 존재할 수 없기 때문이다 — Daml 모델의 초이스 본문은 초이스가 실행될 때 항상 실행되어야 하기 때문이다. 무결성 절에서 이 상세를 다룬다.

그럼에도 액션은 분리 불가능한 게 아니라 계층적이다: 왼쪽·오른쪽 하위 트리는 그 자체로 액션이며, 각각 Alice와 Bob이 자기 `SimpleAsset` 입력 컨트랙트 #1과 #2에 `Transfer` 초이스를 실행하는 Exercise 액션이다. 그리고 두 하위 트리 각각은 또 다른 하위 트리, 즉 Bob과 Alice의 새 `SimpleAsset` 컨트랙트 #5와 #6 생성을 담는다. 이 각 하위 트리도 그 자체로 액션이다. 이 계층 구조는 아래에서 설명할 하위액션(subaction) 관계를 유도하고 프라이버시 모델의 기초를 이룬다.

### 정의

전체적으로, 위 예시의 정산은 두 유형의 액션을 담는다:

1. 컨트랙트 생성
2. 컨트랙트에 초이스 실행.

이것이 원장 모델의 두 주요 종류의 액션이기도 하다.

**노드(node)** 는 다음 중 하나다:

1. **Create 노드** 는 컨트랙트 생성을 기록한다. 다음 정보를 담는다:
   * **컨트랙트 ID** 는 컨트랙트의 고유 식별자다. 미사용 트랜잭션 출력(UTxO) 기반 원장의 트랜잭션 출력(TxO)에 해당한다.
   * **템플릿 ID** 는 컨트랙트와 연관된 Daml 코드를 식별하고, 그 인자가 컨트랙트 ID와 연관된 불변 데이터인 **컨트랙트 인스턴스** 를 정의한다.
   * **서명자(signatories)** 는 컨트랙트 생성·<abbr class="gloss" title="컨트랙트를 소비해 비활성으로 만드는 것(archive). 보관된 컨트랙트는 더 이상 쓸 수 없음">보관</abbr>을 인가해야 하는 비어 있지 않은 파티 집합이다.
   * **컨트랙트 관찰자(observers)**, 줄여서 관찰자는 서명자 외에 컨트랙트 생성·보관을 통지받는 파티 집합이다.

   Daml에서 서명자와 컨트랙트 관찰자는 템플릿이 정의한 `signatory`와 `observer` 절로 결정된다.

   <img src="https://mintcdn.com/cantonfoundation/QAGFSphBsRkeZIBi/images/docs_website/create-node.svg?fit=max&auto=format&n=QAGFSphBsRkeZIBi&q=85&s=9c64445fa65cb58481369dade79bc801" style="width: 30%;" alt="Create 노드의 구조" width="442" height="202" />

2. **Exercise 노드** 는 하나 이상의 파티가 컨트랙트에 실행한 초이스의 파라미터를 기록한다. 다음 정보를 담는다:
   * 실행 **종류(kind)**, **소비형(consuming)** 또는 **비소비형(non-consuming)**. 일단 소비되면 컨트랙트는 다시 쓸 수 없다; 예컨대 Alice가 자기 자산을 두 번 이전할 수 없어야 한다(<abbr class="gloss" title="같은 자산을 두 번 쓰는 부정행위">이중지불</abbr>). 반면 비소비형으로 실행된 컨트랙트는 재사용될 수 있으며, 예컨대 한 파티에서 다른 파티로의 위임 표현에 쓰인다.
   * 초이스가 실행되는 **컨트랙트 ID**. 이 컨트랙트를 **입력 컨트랙트** 라 한다.
   * 이 초이스가 Daml 인터페이스를 통해 실행되었다면 **인터페이스 ID**.
   * 주어진 **초이스 이름** 으로 초이스의 <abbr class="gloss" title="원장 위에서 규칙대로 자동 실행되는 코드화된 계약. Canton에선 Daml 템플릿으로 작성">스마트 컨트랙트</abbr> 코드를 정의하는 **템플릿 ID**; 그리고 그 코드에 전달되는 **초이스 인자**.
   * **액터(actors)** 라 부르는 연관 파티 집합. 액션을 수행하는 파티들이다. Daml 템플릿의 `controller` 절에 명시된다.
   * 연관된 **초이스 관찰자(choice observers)** 집합. 이 파티들은 초이스 실행을 통지받는다.
   * 초이스 본문 평가로 반환되는 Daml 값인 **실행 결과**.

   <img src="https://mintcdn.com/cantonfoundation/zmlOjLpKuDjnaObr/images/docs_website/exercise-node.svg?fit=max&auto=format&n=zmlOjLpKuDjnaObr&q=85&s=52697fa7f7bd95a232ddd2c1588c62b6" style="width: 30%;" alt="Exercise 노드의 구조" width="442" height="282" />

3. 컨트랙트에 대한 **Fetch 노드** 는 페치 시점에 컨트랙트가 존재하고 활성임을 보인다. Fetch는 결과 없는 비소비형 Exercise처럼 동작하며 반복될 수 있다. Fetch 노드는 Exercise 노드와 유사하게 다음 정보를 담는다: **컨트랙트 ID**, **인터페이스 ID**, **템플릿 ID**, 그리고 컨트랙트를 페치하는 파티인 **액터**.

   <img src="https://mintcdn.com/cantonfoundation/QAGFSphBsRkeZIBi/images/docs_website/fetch-node.svg?fit=max&auto=format&n=QAGFSphBsRkeZIBi&q=85&s=6c854090ce405fc45ba634de15d55ca1" style="width: 30%;" alt="Fetch 노드의 구조" width="442" height="202" />

**액션(action)** 은 **루트 노드** 와, 그 자체가 액션인 **결과(consequences)** 목록으로 구성된다. 이것이 액션의 트리 구조를 낳는다: 액션의 루트 노드는 그 결과의 루트 노드를 자식으로 갖는다.

액션은 루트 노드로부터 종류를 물려받는다:

1. **Create 액션** 은 Create 노드를 루트로 갖는다. 결과는 비어 있다.
2. **Exercise 액션** 은 Exercise 노드를 루트로 갖고 결과는 하위액션이다. Exercise 액션은 그 결과의 **부모 액션** 이다.
3. **Fetch 액션** 은 Fetch 노드를 루트로 갖는다. 결과는 비어 있다.

노드에 대한 용어는 루트 노드를 통해 액션으로 확장된다. 예컨대 Create 액션의 서명자는 Create 노드의 서명자이고, Exercise 액션은 그 루트 노드가 (비)소비형일 때만 (비)소비형이다. 또한 컨트랙트에 대한 Exercise나 Fetch 액션은 그 컨트랙트를 **사용(use)** 한다고 한다. 마지막으로 소비형 Exercise는 그 컨트랙트를 **소비(consume)** (또는 **보관(archive)**)한다고 한다.

### 예시

Fetch 액션의 예는 `ProposeSimpleDvP` 템플릿의 DvP 제안 컨트랙트의 `Accept` 초이스에 나타난다. 초이스 본문은 Bob이 DvP에 할당하는 `SimpleAsset`을 페치하며, 이는 자산 컨트랙트가 활성인지 <abbr class="gloss" title="이해관계자 밸리데이터가 트랜잭션이 유효함을 미디에이터에 응답하는 것(confirmation)">확인</abbr>하고 컨트랙트 인스턴스를 계산에 들여와, 초이스 구현이 이 자산이 제안 컨트랙트에 표현된 기대를 충족하는지 단언할 수 있게 한다. 다음 다이어그램은 Fetch 액션을 첫 결과로 가진 이 Exercise 액션을 보여준다.

<img src="https://mintcdn.com/cantonfoundation/QAGFSphBsRkeZIBi/images/docs_website/dvp-propose-accept-action.svg?fit=max&auto=format&n=QAGFSphBsRkeZIBi&q=85&s=7985f68cb49127abf9d49ef7688d6c67" style="width: 100%;" alt="Bob이 실행한 Alice의 ProposeSimpleDvP의 accept 액션" width="1562" height="715" />

비소비형 Exercise는 `ProposeSimpleDvP` 컨트랙트의 결합 `AcceptAndSettle` 초이스에 나타난다: 이 초이스는 비소비형이라, 초이스 본문에서 실행되는 `Accept` 초이스가 제안 컨트랙트를 소비할 수 있다. 다음 다이어그램이 보이듯, 비소비형 Exercise는 같은 입력 컨트랙트 #3에 대한 여러 참조를 산출한다. 다이어그램은 또한 페치가 같은 효과를 가짐을 보인다: 입력 컨트랙트 #2가 두 번 쓰인다.

<img src="https://mintcdn.com/cantonfoundation/zmlOjLpKuDjnaObr/images/docs_website/dvp-propose-accept-and-settle-action.svg?fit=max&auto=format&n=zmlOjLpKuDjnaObr&q=85&s=7fb2fa37d4a5585387ad222a9afe9349" style="width: 100%;" alt="Bob이 실행한 Alice의 ProposeSimpleDvP의 accept-and-settle 액션" width="2283" height="1255" />

### 하위액션 (Subactions)

이 예시는 다시 액션의 계층 구조를 강조한다: `AcceptAndSettle` 액션은 `Accept`와 `Settle`에 해당하는 액션을 결과로 담는다.

더 일반적으로, 액션 `act`에 대해 그 **고유 하위액션(proper subactions)** 은 `act`의 결과에 있는 모든 액션과 그 모든 고유 하위액션이다. 또한 `act`는 자기 자신의 (비고유) **하위액션** 이다.

하위액션 관계는 Bob의 `Settle` Exercise에 대해 아래에 시각화된다. 각 테두리 없는 상자는 (노드 트리를 통해) 액션을 담고, 이 상자들의 중첩이 하위액션 관계를 인코딩한다. 상세히, 파란색·보라색 상자 모두 회색으로 표시된 Bob의 `Settle` 액션의 고유 하위액션이다. 녹색 상자는 파란색·회색 상자의 고유 하위액션이고, 노란색 상자는 보라색·회색 상자의 고유 하위액션이다.

<img src="https://mintcdn.com/cantonfoundation/zmlOjLpKuDjnaObr/images/docs_website/dvp-settle-subactions.svg?fit=max&auto=format&n=zmlOjLpKuDjnaObr&q=85&s=18826aee2e0d531ab1f060dfc332fc00" style="width: 60%;" alt="Bob이 DvP 컨트랙트에 Settle 초이스를 실행하는 것의 하위액션" width="1122" height="1122" />

## 트랜잭션 (Transactions)

**트랜잭션(transaction)** 은 원자적으로 실행되는 액션 목록이다. 그 액션들을 트랜잭션의 **루트 액션(root actions)** 이라 한다. 즉, 트랜잭션 `tx = act1, …, actn`에 대해 모든 `acti`는 루트 액션이다. 예컨대 Alice와 Charlie가 각각 Bob에게 DvP 제안을 하나씩 했다면, Bob은 둘을 동시에 수락하고 싶을 수 있다. 이를 위해 Bob은 다음에 보이듯 두 루트 액션(파란색·보라색)을 가진 단일 트랜잭션에서 두 `Accept` 초이스를 실행한다. 시각적으로 트랜잭션은 액션과 구별하기 위해 양쪽 점선으로 구분된다. 액션처럼 왼쪽 입력 컨트랙트는 트랜잭션의 일부가 아니다.

<img src="https://mintcdn.com/cantonfoundation/QAGFSphBsRkeZIBi/images/docs_website/dvp-accept-two.svg?fit=max&auto=format&n=QAGFSphBsRkeZIBi&q=85&s=ee3f6ea1f8df103166460369377101d2" style="width: 100%;" alt="Bob이 Alice와 Charlie로부터의 두 DvP 제안을 수락하는 두 최상위 액션 트랜잭션" width="2442" height="1155" />

또 다른 예로, Exercise 액션의 결과는 액션 목록이므로 트랜잭션을 이룬다. Alice와 Bob의 `SimpleDvP`에 대한 `Settle` 액션 예에서, `Settle` 액션의 결과는 다음 트랜잭션을 이루며, 액션은 앞서처럼 왼쪽에서 오른쪽으로 정렬된다. 트랜잭션은 두 루트 액션(파란색·보라색), 즉 DvP의 두 다리의 두 `Transfer` 액션으로 구성된다.

<img src="https://mintcdn.com/cantonfoundation/zmlOjLpKuDjnaObr/images/docs_website/dvp-settle-consequences-are-transactions.svg?fit=max&auto=format&n=zmlOjLpKuDjnaObr&q=85&s=5b0538ddeb688764316720634ea98d6a" style="width: 50%;" alt="Settle 액션의 결과는 DvP의 두 Transfer 다리의 두 액션 트랜잭션이다" width="962" height="612" />

액션의 계층 구조는 트랜잭션으로 확장되어 하위트랜잭션 개념을 낳는다. 트랜잭션의 **고유 하위트랜잭션(proper subtransaction)** 은 액션을 그 결과로 (반복) 치환해 얻는다; 트랜잭션의 **하위트랜잭션** 은 트랜잭션 자체이거나 그 고유 하위트랜잭션이다.

예컨대 `Settle` 액션의 두 결과만으로 구성된 위 트랜잭션이 주어지면, 다음 다이어그램은 점선 구분자와 함께 일곱 개의 고유 비어 있지 않은 하위트랜잭션을 모두 보여준다.

<img src="https://mintcdn.com/cantonfoundation/zmlOjLpKuDjnaObr/images/docs_website/dvp-settle-consequences-subtransactions.svg?fit=max&auto=format&n=zmlOjLpKuDjnaObr&q=85&s=809e7066dbf0b44649bada35081b06d9" style="width: 100%;" alt="Settle 액션 결과의 모든 고유 하위트랜잭션" width="1942" height="1308" />

프라이버시 모델은 하위트랜잭션 개념을 써서 가시성 규칙을 정의한다.

## 입력과 출력

원장 모델은 미사용 트랜잭션 출력(UTxO) 집합이 원장의 현재 상태를 이루는 (확장) UTxO 스타일 원장 범주에 속한다. 여기서 **트랜잭션 출력** 은 트랜잭션에서 생성된 컨트랙트의 컨트랙트 ID다. 컨트랙트가 소비되면 그 컨트랙트 ID가 소비되어 UTxO 집합에서 제거된다. 각 UTxO와 연관된 데이터는 불변이다; 수정은 컨트랙트 ID를 소비하고 다른 컨트랙트 ID로 새 컨트랙트를 재생성해 일어난다.

이 원장 모델은 두 측면에서 UTXO 모델을 확장한다:

* 트랜잭션은 컨트랙트를 소비하지 않고 쓸 수 있다, 예컨대 비소비형 초이스를 실행하거나 페치함으로써. 그 경우 컨트랙트 ID는 트랜잭션 입력으로 나타나도 UTxO 집합에 남는다.
* 트랜잭션은 계층적으로 구조화되고 트랜잭션에서 생성된 컨트랙트 ID가 같은 트랜잭션 내에서 소비될 수 있다. 예컨대 `AcceptAndSettle` 액션 내에서 첫 결과에서 생성된 `SimpleDvP`가 두 번째 결과에서 소비된다. 그런 컨트랙트를 **일시적(transient)** 이라 한다.

이 측면들은 원장 모델의 나머지 절에서 더 상세히 논한다.

## 원장 (Ledger)

트랜잭션 구조는 파티 상호작용의 내용을 기록한다. 원장은 상호작용의 두 측면을 더 기록한다:

* 특정 파티 상호작용을 고유하게 가리키는 식별자.
* 특정 파티 상호작용을 요청한 파티.

프라이버시 모델 때문에 모두가 파티 상호작용의 모든 부분을 보지는 않는다. 파티 상호작용의 고유 식별자는 서로 다른 파티가 같은 상호작용의 부분을 보는지 상관지을 수 있게 한다. **업데이트(update)** 개념이 그런 식별자를 더한다. 단일 트랜잭션과 이른바 **업데이트 ID(update ID)** 라는 문자열로 구성된다. 원장 모델의 예시는 Daml Studio의 트랜잭션 <abbr class="gloss" title="한 트랜잭션을 당사자별로 나눈 조각. 각 당사자는 자기 권한에 해당하는 뷰(자기 몫)만 받아 본다">뷰</abbr>와 유사하게 어떤 수 `i`에 대해 `TX i` 형태의 업데이트 ID를 쓴다. Ledger API에서 업데이트 ID는 사전식 순서가 원장 순서와 독립적인 임의 문자열이다.

**커밋(commit)** 은 *누가 파티 상호작용을 요청했는지* 정보를 더한다. 업데이트와 그것을 요청한 하나 이상의 파티로 구성된다. 그 파티들을 커밋의 **요청자(requesters)** 라 한다. Daml Script에서 요청자는 `submit` <abbr class="gloss" title="애플리케이션이 원장에 제출하는 명령(컨트랙트 생성·초이스 실행 요청)">커맨드</abbr>에 주어진 `actAs` 파티에 해당한다.

> **정의: 원장(Ledger)**
> **원장** 은 업데이트 ID가 고유한 커밋의 방향 비순환 그래프(DAG)다.

> **정의: 최상위 액션(top-level action)**
> 커밋에 대해, 그 트랜잭션의 루트 액션을 **최상위 액션** 이라 한다. 임의의 원장 커밋의 최상위 액션은 원장의 최상위 액션이기도 하다.

따라서 Canton 원장은 파티가 취한 모든 액션의 전체 이력을 나타낸다. 원장의 그래프 구조는 커밋에 **선행 관계(happens-before order)** 를 유도한다. 원장이 `c1`에서 `c2`로의 비어 있지 않은 경로를 담으면(동등하게, 그래프의 전이적 닫힘이 `c1`에서 `c2`로 간선을 담으면) 커밋 `c1`이 `c2`보다 *먼저 일어난다(happens before)* 고 한다.

> **참고:** 원장의 무결성 조건은 선행 관계가 컨트랙트 생애주기를 존중할 것을 요구한다. 예컨대 컨트랙트를 생성하는 커밋은 그것을 소비하는 커밋보다 먼저 일어나야 한다(같은 커밋이 아닌 한). 다음 몇 절에서는 이 조건을 충족하는 원장만 고려한다.

시각적으로, 원장은 시간이 흐르며 왼쪽에서 오른쪽으로 성장하는 시퀀스로 표현될 수 있다. 아래에서 보라색 점선 수직선이 커밋 경계를 표시하고, 각 커밋은 요청자와 업데이트 ID로 주석된다. 파란 화살표는 각 Exercise·Fetch 액션을 입력 컨트랙트의 Create 액션에 연결한다. 이 화살표는 원장이 UTXO 블록체인의 의미에서 **트랜잭션 그래프(transaction graph)** 를 이룸을 강조한다.

예컨대 다음 Daml Script는 실행 DvP 예시의 전체 워크플로를 인코딩한다.

```haskell
let eurAsset = SimpleAsset with
      issuer = bank1
      owner = alice
      asset = "1 EUR"
eur <- submit bank1 do createCmd eurAsset
    
let usdAsset = SimpleAsset with
      issuer = bank2
      owner = bob
      asset = "1 USD"
usd <- submit bank2 do createCmd usdAsset
    
proposeDvP <- submit alice $ do
  createCmd ProposeSimpleDvP with
      proposer = alice
      counterparty = bob
      allocated = eur
      expected = usdAsset
disclosedEur <- fromSome <$> queryDisclosure alice eur
```

```haskell
(newUsd, newEur) <- submitWithDisclosures bob [disclosedEur] do
    exerciseCmd proposeDvP $ AcceptAndSettle with toBeAllocated = usd
```

이 워크플로는 네 커밋을 가진 아래 원장을 낳는다:

* 첫 커밋에서, Bank 1이 Alice에게 발행되는 `1 EUR`의 `SimpleAsset`(컨트랙트 #1) 생성을 요청한다.
* 둘째 커밋에서, Bank 2가 Bob에게 발행되는 `1 USD`의 `SimpleAsset`(컨트랙트 #2) 생성을 요청한다.
* 셋째 커밋에서, Alice가 `SimpleDvpPoposal`(컨트랙트 #3) 생성을 요청한다.
* 넷째 커밋에서, Bob이 DvP 제안에 `AcceptAndSettle` 초이스 실행을 요청한다.

<img src="https://mintcdn.com/cantonfoundation/QAGFSphBsRkeZIBi/images/docs_website/dvp-ledger.svg?fit=max&auto=format&n=QAGFSphBsRkeZIBi&q=85&s=2905a7d8b725484c0035079b45d2ba07" alt="전체 DvP 워크플로의 커밋 시퀀스" width="3322" height="1362" />

> **참고:** 무결성 제약은 독립적 커밋 간 순서를 부과하지 않는다. 이 예에서 첫 세 커밋 `TX 0`, `TX 1`, `TX 2` 사이에 간선이 없어도 되므로 어느 순서로든 제시될 수 있다.
> 원장이 DAG이므로 위상 정렬로 순서를 선형 시퀀스로 항상 확장할 수 있다. 다음 절에서는 (달리 명시하지 않는 한) 원장이 전체 순서되었다고 가정한다. 더 일반적인 부분 순서는 인과성 절에서 논한다.

---

# 유효한 원장 (Valid Ledgers)

핵심에는 *유효한 원장(valid ledger)* 개념이 있다; 해당 커밋을 원장에 추가했을 때 유효한 원장이 되면 변경이 허용된다. **유효한 원장** 은 세 조건을 충족하는 원장이다:

**일관성(consistency)**
비<abbr class="gloss" title="아직 보관(소비)되지 않아 현재 유효한 컨트랙트">활성 컨트랙트</abbr>에 대한 Exercise와 Fetch는 허용되지 않는다, 즉 아직 생성되지 않았거나 이미 Exercise로 소비된 컨트랙트. 컨트랙트 키를 가진 컨트랙트는 그 키가 다른 미소비 컨트랙트와 연관되지 않고 모든 키 단언이 성립할 때만 생성될 수 있다.

**적합성(conformance)**
주어진 컨트랙트에 대해 제한된 액션 집합만 허용된다.

**인가(authorization)**
특정 변경을 요청할 수 있는 파티가 제한된다.

이 중 마지막만 변경을 요청하는 파티에 의존하고, 나머지 둘은 일반적이다.

---

# 무결성 (Integrity)

이 절은 "누가 어떤 변경을 요청할 수 있나"라는 질문을 다룬다.

"누가 어떤 변경을 요청할 수 있나"에 답하려면, 어떤 원장이 허용되고 어떤 게 아닌지의 정확한 정의가 필요하다. 예컨대 위 페인트 오퍼 원장은 직관적으로 허용되는 반면, 다음 원장들은 모두 허용되지 않는다.

* Alice가 자기 IOU를 두 번 지출(이중지불) — `B`에게 한 번, `P`에게 한 번 이전.
* Alice가 `Iou` 이전을 제거해 오퍼의 결과를 바꿈.
* 페인터의 동의 없이 그에게 부과된 의무.
* 페인터가 Alice의 IOU를 훔침. (마지막 커밋을 Alice가 수행했다면 직관적으로 허용됨에 유의.)
* 페인터가 오퍼가 없다고 거짓 주장.
* 페인터가 같은 참조 번호로 두 다른 페인트 오퍼를 생성하려 함.

(원문은 위 각 무효 사례를 도식으로 보여준다.)

## 일관성 (Consistency)

일관성은 두 부분으로 구성된다:

1. 컨트랙트 일관성: 컨트랙트는 사용 전에 생성되어야 하고, 일단 소비되면 쓸 수 없다.
2. 키 일관성: 키는 고유하고 키 단언이 충족된다.

이를 정확히 정의하려면 "전(before)"과 "후(after)" 개념이 필요하다. 이는 모든 액션을 시퀀스에 놓아 주어진다. 기술적으로, 시퀀스는 원장 액션의 전위 순회(pre-order traversal)로 얻으며, 이 액션들이 (순서 있는) 포레스트를 이룸에 유의한다. 직관적으로, 부모 액션을 그 고유 하위액션보다 항상 먼저 고르고, 그 외에는 왼쪽 액션을 오른쪽 액션보다 항상 먼저 골라 얻는다. 아래 이미지는 페인트 오퍼 예시의 결과 순서를 보여준다.

<img src="https://mintcdn.com/cantonfoundation/QAGFSphBsRkeZIBi/images/docs_website/consistency-order-on-actions.svg?fit=max&auto=format&n=QAGFSphBsRkeZIBi&q=85&s=dad56899a6c7f7695b4b59005554d5cf" style="width: 100%;" alt="커밋의 시간 시퀀스" width="1251" height="518" />

이미지에서, `act`에서 `act'`로 (비어 있지 않은) 경로가 있으면 액션 `act`가 액션 `act'`보다 먼저 일어난다. 그러면 `act'`는 `act` 후에 일어난다.

### 컨트랙트 일관성

컨트랙트 일관성은 컨트랙트가 생성된 후·소비되기 전에 쓰이도록 보장한다.

> **정의 «컨트랙트 일관성»**
> 원장이 컨트랙트 `c`에 대한 모든 액션 `act`에 대해 다음이 모두 성립하면 **컨트랙트 c에 대해 일관**된다:
> 1. `act`가 그 자체로 **Create c** 이거나 **Create c** 가 `act`보다 먼저 일어남
> 2. `act`가 어떤 **Create c** 액션보다 먼저 일어나지 않음
> 3. `act`가 `c`를 소비하는 어떤 **Exercise** 액션 후에 일어나지 않음.

일관성 조건은 이중지불 예시를 배제한다. 아래 빨간 경로가 나타내듯, 예시의 두 번째 exercise는 같은 컨트랙트의 소비형 exercise 후에 일어나 컨트랙트 일관성 기준을 위반한다.

<img src="https://mintcdn.com/cantonfoundation/QAGFSphBsRkeZIBi/images/docs_website/consistency-banning-double-spends.svg?fit=max&auto=format&n=QAGFSphBsRkeZIBi&q=85&s=f905e3b64ca7636365f4631da7185fe1" style="width: 100%;" alt="이중지불을 금지하는 일관성" width="1220" height="362" />

> 일관성 개념 외에, 액션에 대한 선후 관계는 주어진 트랜잭션의 임의 지점에서 **컨트랙트 상태(contract state)** 개념을 정의하는 데도 쓸 수 있다. 컨트랙트 상태는 컨트랙트를 생성하고 소비형으로 실행함으로써 바뀐다. 트랜잭션의 임의 지점에서 가장 최근 상태 변경을 자명하게 정의할 수 있다. 그러면 트랜잭션의 한 지점에서 `c`의 컨트랙트 상태는:

1. **활성(active)**, `c`의 가장 최근 상태 변경이 create면;
2. **보관(archived)**, `c`의 가장 최근 상태 변경이 소비형 exercise면;
3. **부재(inexistent)**, `c`가 상태를 한 번도 바꾸지 않았으면.

원장은 `c`에 대한 **Exercise** ·**Fetch** 액션이 `c`가 활성일 때만, **Create** 액션이 `c`가 부재일 때만 일어나면 정확히 `c`에 대해 일관된다. 아래 그림은 예시 원장의 모든 지점에서 서로 다른 컨트랙트의 상태를 시각화한다.

<img src="https://mintcdn.com/cantonfoundation/QAGFSphBsRkeZIBi/images/docs_website/consistency-paint-offer-activeness.svg?fit=max&auto=format&n=QAGFSphBsRkeZIBi&q=85&s=166f2ac81a3fbf9309dd910c050956cf" style="width: 100%;" alt="PaintOffer 컨트랙트의 활성성" width="1251" height="502" />
<img src="https://mintcdn.com/cantonfoundation/QAGFSphBsRkeZIBi/images/docs_website/consistency-alice-iou-activeness.svg?fit=max&auto=format&n=QAGFSphBsRkeZIBi&q=85&s=1707ba950349e96fa049806cf0dc1350" style="width: 100%;" alt="Iou Bank A 컨트랙트의 활성성" width="1251" height="502" />

순서 개념은 모든 다른 원장 구조 — 액션, 트랜잭션, 트랜잭션 목록, 원장 — 에 정의될 수 있다. 따라서 일관성, 입력·출력, 컨트랙트 상태 개념도 이 모든 구조에 정의될 수 있다. 원장의 **활성 컨트랙트 집합(active contract set)** 은 원장에서 활성인 모든 컨트랙트의 집합이다. 위 예에서는 컨트랙트 `Iou Bank P`와 `PaintAgree P A`로 구성된다.

### 키 일관성

컨트랙트 키는 원장에 키 고유성 제약을 도입한다. 이 개념을 포착하기 위해, 컨트랙트 모델은 시스템의 모든 컨트랙트가 키를 갖는지, 그렇다면 그 키를 명시해야 한다. 모든 컨트랙트는 최대 하나의 키를 가질 수 있다.

컨트랙트처럼, 모든 키는 상태를 갖는다. 액션 `act`는 다음이면 **키 `k`에 대한 액션** 이다:

* `act`가 키 `k`를 가진 컨트랙트 `c`에 대한 **Create**, **Exercise**, 또는 **Fetch** 액션, 또는
* `act`가 키 단언 **NoSuchKey** `k`.

> **정의 «키 상태(key state)»**
> 원장에서 키의 **키 상태** 는 키에 대한 마지막 액션 `act`로 결정된다:
> * `act`가 컨트랙트 `c`에 대한 **Create**, 비소비형 **Exercise**, 또는 **Fetch** 액션이면, 키 상태는 `c`에 **할당됨(assigned)**.
> * `act`가 소비형 **Exercise** 액션이거나 **NoSuchKey** 단언이면, 키 상태는 **자유(free)**.
> * 그런 액션 `act`가 없으면, 키 상태는 **미지(unknown)**.

키는 그 키 상태가 **자유** 또는 **미지** 면 **미할당(unassigned)** 이다.

키 일관성은 각 키에 대해 최대 하나의 활성 컨트랙트가 있고 모든 키 단언이 충족되도록 보장한다.

> **정의 «키 일관성»**
> 원장이 키 `k`에 대한 모든 액션 `act`에 대해 `act` 전의 키 상태 `s`가 다음을 충족하면 **키 `k`에 대해 일관**된다:
> * `act`가 **Create** 액션이거나 **NoSuchKey** 단언이면, `s`는 **자유** 또는 **미지**.
> * `act`가 어떤 컨트랙트 `c`에 대한 **Exercise** 또는 **Fetch** 액션이면, `s`는 `c`에 **할당됨** 또는 **미지**.

키 일관성은 키 일관성 관련 문제 예시를 배제한다. 예컨대 페인터 `P`가 `A`에게 참조 번호 `P123`으로 페인트 오퍼를 했지만 `A`가 아직 수락하지 않았다고 하자. `P`가 같은 참조 번호 `P123`으로 `David`에게 또 다른 페인트 오퍼를 생성하려 하면, 이 생성 액션은 키 고유성을 위반한다.

<img src="https://mintcdn.com/cantonfoundation/QAGFSphBsRkeZIBi/images/docs_website/double-key-creation-highlighted.svg?fit=max&auto=format&n=QAGFSphBsRkeZIBi&q=85&s=acbd46af202ad664921151e0e182811a" style="width: 100%;" alt="중복 키 생성" width="1220" height="202" />

키 단언은 특정 종류의 컨트랙트의 부재를 증명하기 위해 워크플로에 쓸 수 있다. 예컨대 페인터 `P`가 페인터 조합 `U`의 회원이라고 하자. 이 조합은 회원이 거래해서는 안 되는 잠재 고객 블랙리스트를 유지한다. 활성 컨트랙트 `Blacklist @U &A`가 있으면 고객 `A`가 블랙리스트에 있는 것으로 간주된다. 페인터 `P`가 `A`가 블랙리스트면 페인트 오퍼를 하지 않도록, 페인터는 키 `(U, A)`에 대한 **NoSuchKey** 단언을 자기 커밋에 결합한다. 다음 원장은 그 트랜잭션을 보여주며, `UnionMember U P`는 조합 `U`에서 `P`의 회원 자격을 나타낸다. 이는 인가에 필요한 그런 단언을 수행할 초이스를 `P`에게 부여한다.

<img src="https://mintcdn.com/cantonfoundation/zmlOjLpKuDjnaObr/images/docs_website/paint-offer-blacklist.svg?fit=max&auto=format&n=zmlOjLpKuDjnaObr&q=85&s=75d1f46d626bebacf828a8139db90405" style="width: 100%;" alt="페인트 오퍼 블랙리스트" width="1251" height="371" />

키 일관성은 다른 일관성 개념처럼 액션, 트랜잭션, 트랜잭션 목록으로 확장된다.

### 원장 일관성

> **정의 «원장 일관성»**: 원장이 모든 컨트랙트와 모든 키에 대해 일관되면 **일관**된다.

### 내부 일관성

위 일관성 요구는 고립된 액션·트랜잭션에는 너무 강하다. 예컨대 페인트 오퍼 예시의 수락 트랜잭션은 `PaintOffer A P Bank`와 `Iou Bank A` 컨트랙트가 먼저 생성되지 않고 쓰이므로 원장으로서는 일관되지 않는다.

그러나 그 트랜잭션은 이 컨트랙트들을 생성하는 원장에 덧붙여져 일관된 원장을 산출할 수 있다. 그런 트랜잭션을 내부적으로 일관(internally consistent)된다 하고, `PaintOffer A P Bank P123`과 `Iou Bank A` 같은 컨트랙트를 트랜잭션의 입력 컨트랙트라 한다. 쌍대로, 트랜잭션의 출력 컨트랙트는 트랜잭션이 생성하고 보관하지 않는 컨트랙트다.

> **정의 «컨트랙트에 대한 내부 일관성»**
> 트랜잭션이 컨트랙트 `c`에 대한 모든 하위액션 `act`에 대해 다음이 성립하면 **컨트랙트 c에 대해 내부적으로 일관**된다:
> 1. `act`가 어떤 **Create c** 액션보다 먼저 일어나지 않음
> 2. `act`가 `c`를 소비하는 어떤 exercise 후에 일어나지 않음.
> 트랜잭션이 모든 컨트랙트에 대해 내부적으로 일관되고 모든 키에 대해 일관되면 **내부적으로 일관**된다.

> **정의 «입력 컨트랙트»**
> 내부적으로 일관된 트랜잭션에 대해, 트랜잭션이 `c`에 대한 **Exercise** 나 **Fetch** 액션을 담지만 **Create c** 액션은 담지 않으면 컨트랙트 `c`는 트랜잭션의 **입력 컨트랙트** 다.

> **정의 «출력 컨트랙트»**
> 내부적으로 일관된 트랜잭션에 대해, 트랜잭션이 **Create c** 액션을 담지만 `c`에 대한 소비형 **Exercise** 액션은 담지 않으면 컨트랙트 `c`는 트랜잭션의 **출력 컨트랙트** 다.

입력·출력 컨트랙트는 내부적으로 일관되지 않은 트랜잭션에는 정의되지 않음에 유의하라. 아래 이미지는 내부적으로 일관된·일관되지 않은 트랜잭션의 예시를 보여준다.

<img src="https://mintcdn.com/cantonfoundation/zmlOjLpKuDjnaObr/images/docs_website/internal-consistency-examples.svg?fit=max&auto=format&n=zmlOjLpKuDjnaObr&q=85&s=ac4fdf1301dcb0ae79c2da90326df85f" style="width: 100%;" alt="내부 일관성 예시: 첫 두 트랜잭션은 위반, 마지막은 내부적으로 일관됨" width="1100" height="583" />

입력 컨트랙트와 유사하게, 입력 키를 트랜잭션 시작에 미할당이어야 하는 집합으로 정의한다.

> **정의 «입력 키»**: 내부적으로 일관된 트랜잭션에서 키 `k`에 대한 첫 액션 `act`가 **Create** 액션이거나 **NoSuchKey** 단언이면 `k`는 **입력 키** 다.

블랙리스트 예시에서, `P`의 트랜잭션은 두 입력 키를 갖는다: **NoSuchKey** 액션에 의한 `(U, A)`와 `PaintOffer` 컨트랙트를 생성하므로 `(P, P123)`.

## 적합성 (Conformance)

*적합성* 조건은 원장에 일어날 수 있는 액션을 제약한다. 이는 모든 가능한 액션 집합을 명시하는 **컨트랙트 모델(contract model)** `M`(줄여서 모델)을 고려해 이뤄진다. 원장의 모든 최상위 액션이 `M`의 멤버면 원장은 **M에 적합(conformant to M)** (또는 M에 부합)하다. 일관성처럼 적합성 개념은 커밋의 요청자에 의존하지 않으므로 트랜잭션과 트랜잭션 목록에도 적용될 수 있다.

예컨대 IOU 컨트랙트에 허용되는 액션 집합은 다음과 같이 기술될 수 있다.

<img src="https://mintcdn.com/cantonfoundation/zmlOjLpKuDjnaObr/images/docs_website/models-simple-iou.svg?fit=max&auto=format&n=zmlOjLpKuDjnaObr&q=85&s=367e3af7930fd69042909a29a8eff573" style="width: 80%;" alt="IOU 컨트랙트에 허용되는 create, transfer, settle 액션 집합" width="907" height="420" />

이미지의 상자는 상자 안의 컨트랙트 파라미터(채무자나 소유자 같은)가 적절한 타입의 임의 값으로 인스턴스화될 수 있다는 의미에서 템플릿이다. 이해를 돕기 위해 각 상자는 해당 액션 집<abbr class="gloss" title="여러 노드가 트랜잭션의 유효성·순서에 함께 동의하는 절차">합의</abbr> 직관적 목적을 기술하는 레이블을 포함한다. 이미지가 시사하듯, transfer 상자는 실행된 IOU 컨트랙트와 새로 생성된 IOU 컨트랙트 모두에서 은행이 같아야 한다는 제약을 부과한다. 다만 소유자는 임의로 바뀔 수 있다. 반면 settle 액션에서는 은행과 소유자 모두 같아야 한다. 나아가 적합하려면 transfer 액션의 액터가 컨트랙트 소유자와 같아야 한다.

물론 파라미터 간 관계의 제약은 임의로 복잡할 수 있고 이 그래픽 표현으로 편리하게 재현될 수 없다. 이것이 Daml의 역할이다 — 컨트랙트 모델을 표현하는 훨씬 편리한 방법을 제공한다. Daml과 컨트랙트 모델의 연결은 이후 절에서 더 상세히 설명한다.

적합성 기준이 작동하는 것을 보기 위해, 컨트랙트 모델이 `PaintOffer`와 `PaintAgree` 컨트랙트에 다음 액션만 허용한다고 가정하자.

<img src="https://mintcdn.com/cantonfoundation/zmlOjLpKuDjnaObr/images/docs_website/models-paint-offer.svg?fit=max&auto=format&n=zmlOjLpKuDjnaObr&q=85&s=18c41c80ee34b639d2667e24cd9cb211" style="width: 90%;" alt="PaintOffer와 PaintAgree 컨트랙트에 가능한 create, accept 액션" width="942" height="551" />

Alice가 돈을 이전하지 않으려고 오퍼의 결과를 바꾸는 예시의 문제가 이제 분명해진다.

<img src="https://mintcdn.com/cantonfoundation/zmlOjLpKuDjnaObr/images/docs_website/non-conformant-action.svg?fit=max&auto=format&n=zmlOjLpKuDjnaObr&q=85&s=8c316201ce7b19be6d74a60c83d5e1fc" alt="비적합 액션을 보여주는 시간 시퀀스" width="1220" height="502" />

`A`의 커밋은 컨트랙트 모델에 적합하지 않다 — 모델이 그녀가 커밋하려는 최상위 액션을 담지 않기 때문이다.

## 인가 (Authorization)

마지막 기준은 마지막 두 문제 예시 — 페인터에게 부과된 의무와 페인터가 Alice의 돈을 훔치는 것 — 를 배제한다. 첫 번째는 아래에 시각화된다.

<img src="https://mintcdn.com/cantonfoundation/zmlOjLpKuDjnaObr/images/docs_website/invalid-obligation.svg?fit=max&auto=format&n=zmlOjLpKuDjnaObr&q=85&s=87da739c05b2ea006c1370a44095d7c4" style="width: 100%;" alt="A가 요청한 PaintAgree P A P123의 단일 커밋" width="1220" height="242" />

이 예시가 직관적으로 허용되지 않는 이유는 `PaintAgree` 컨트랙트가 페인터가 Alice의 집을 칠할 의무를 표현하기로 되어 있지만, 그가 그 의무에 동의한 적이 없기 때문이다. 종이 계약에서 의무는 계약 본문에 표현되고 계약의 *서명자(signatories)* 에게 부과된다.

### 서명자와 유지자

실세계 계약의 이 요소를 포착하기 위해, **컨트랙트 모델** 은 시스템의 각 컨트랙트에 대해 추가로 다음을 명시한다:

1. 계약에 구속되는 파티인 비어 있지 않은 **서명자(signatories)** 집합.
2. 컨트랙트가 키와 연관되면, 키에 대해 최대 하나의 미소비 컨트랙트가 존재하도록 하는 파티인 비어 있지 않은 **유지자(maintainers)** 집합. 유지자는 서명자의 부분집합이어야 하고 키에만 의존해야 한다. 이 의존은 키를 받아 그 키의 유지자를 반환하는 함수 `maintainers`로 포착된다.

예시에서 컨트랙트 모델은 다음을 명시한다:

1. `Iou obligor owner` 컨트랙트는 `obligor`만 서명자로 가짐.
2. `MustPay obligor owner` 컨트랙트는 `obligor`와 `owner` 모두를 서명자로 가짐.
3. `PaintOffer houseOwner painter obligor refNo` 컨트랙트는 painter만 서명자로 가짐. 연관 키는 painter와 참조 번호로 구성된다. painter가 유지자.
4. `PaintAgree houseOwner painter refNo` 컨트랙트는 house owner와 painter 모두를 서명자로 가짐. 키는 painter와 참조 번호로 구성된다. painter가 유일한 유지자.

아래 그래픽 표현에서, 컨트랙트의 서명자는 (의무의 연상으로) 달러 기호로 표시되고 굵은 글꼴을 쓴다. 유지자는 (고유성을 강제하는 자의 연상으로) `@`로 표시된다. 유지자는 항상 서명자이므로 `@`로 표시된 파티는 암묵적으로 서명자다. 예컨대 페인트 오퍼 수락 액션에 서명자를 주석하면 아래 이미지가 된다.

<img src="https://mintcdn.com/cantonfoundation/zmlOjLpKuDjnaObr/images/docs_website/signatories-paint-offer.svg?fit=max&auto=format&n=zmlOjLpKuDjnaObr&q=85&s=f59d4caeae372b52ca5a79b4043248b9" style="width: 60%;" alt="페인트 거래 흐름도. P는 유지자; A와 Bank는 서명자." width="620" height="363" />

### 인가 규칙

서명자는 페인터가 의무를 갖는다는 것을 정확히 진술하게 한다. 부과된 의무는 페인터가 동의하지 않았으므로 직관적으로 무효다. 즉, 페인터가 의무 생성을 *인가(authorize)* 하지 않았다.

Daml 원장에서, 파티는 다음 중 한 방법으로 커밋의 하위액션을 **인가** 할 수 있다:

* 커밋의 모든 최상위 액션은 커밋의 모든 요청자에 의해 인가된다.
* 컨트랙트 `c`에 대한 exercise 액션 `act`의 모든 결과는 `c`의 모든 서명자와 `act`의 모든 액터에 의해 인가된다.

두 번째 인가 규칙은 계약법에서 계약 성립의 전제인 오퍼-수락(offer-acceptance) 패턴을 인코딩한다. 컨트랙트 `c`는 사실상 오퍼 제공자로 행위하는 서명자의 오퍼다. exercise는 오퍼 수락자인 액터의 수락이다. exercise의 결과는 계약 본문으로 해석될 수 있어, Daml 원장의 인가 규칙은 계약법의 계약 성립 규칙을 밀접하게 모델링한다.

> 커밋은 모든 하위액션 `act`가 적어도 `act`의 모든 **필요 인가자(required authorizers)** 에 의해 인가되면 **잘 인가(well-authorized)** 된다. 여기서:

1. 컨트랙트 `c`에 대한 **Create** 액션의 필요 인가자는 `c`의 서명자.
2. **Exercise** 또는 **Fetch** 액션의 필요 인가자는 그 액터.
3. **NoSuchKey** 단언의 필요 인가자는 키의 유지자.

이 개념을 원장으로 들어올려, 원장은 그 모든 커밋이 잘 인가될 때 정확히 잘 인가된다.

### 예시

인가 정의가 작동하는 방식에 대한 직관은 예시를 보면 가장 쉽게 길러진다. 주 예시인 페인트 오퍼 원장은 직관적으로 정당하다. 따라서 우리 정의에 따라 잘 인가되어야 하며, 실제로 그렇다.

아래 시각화에서 `Π ✓ act`는 파티 `Π`가 액션 `act`를 인가함을 나타낸다.

<img src="https://mintcdn.com/cantonfoundation/QAGFSphBsRkeZIBi/images/docs_website/authorization-paint-offer.svg?fit=max&auto=format&n=QAGFSphBsRkeZIBi&q=85&s=489df8e52d59814ff917a1f669b1e202" alt="인가 관점에서 설명된 페인트 거래 시간 시퀀스" width="1311" height="502" />

첫 커밋에서, 은행이 그 커밋을 요청해 IOU 생성을 인가한다. 은행이 IOU 컨트랙트의 유일한 서명자이므로 이 커밋은 잘 인가된다. 유사하게 둘째 커밋에서 페인터가 페인트 오퍼 컨트랙트 생성을 인가하고, painter가 그 컨트랙트의 유일한 서명자라 이 커밋도 잘 인가된다.

셋째 커밋은 더 복잡하다. 먼저 Alice가 페인트 오퍼에 대한 exercise를 요청해 인가한다. 그녀가 이 exercise의 유일한 액터이므로 인가 요구를 충족한다. painter가 페인트 오퍼의 서명자이고 Alice가 exercise의 액터이므로, 그들이 함께 exercise의 모든 결과를 인가한다. 첫 결과는 Alice를 액터로 하는 IOU에 대한 exercise이므로 허용된다. 둘째 결과는 (A를 위한) 옛 IOU를 실행해 (P를 위한) 새 IOU를 생성하는 것이다. IOU가 이전에 은행이 서명했고 Alice가 exercise의 액터이므로 그들이 함께 이 생성을 인가한다. 은행이 유일한 서명자이므로 이 액션은 허용된다. 마지막 결과는 Alice와 painter를 서명자로 하는 페인트 합의 생성이다. 둘 다 액션을 인가하므로 이도 허용된다. 따라서 전체 셋째 커밋도 잘 인가되고, 원장도 그렇다.

유사하게, 직관적으로 문제인 예시는 우리 인가 기준에 의해 금지된다. 첫 예시에서 Alice가 페인터에게 집을 칠하도록 강제했다.

<img src="https://mintcdn.com/cantonfoundation/QAGFSphBsRkeZIBi/images/docs_website/authorization-invalid-obligation.svg?fit=max&auto=format&n=QAGFSphBsRkeZIBi&q=85&s=d200a3bae13cf1b9de6cbf4664112c70" alt="Alice가 페인터에게 집을 칠하도록 강제하는 시나리오" width="1220" height="242" />

Alice가 `PaintAgree` 컨트랙트의 **Create** 액션을 요청해 인가한다. 그러나 painter도 `PaintAgree` 컨트랙트의 서명자인데 **Create** 액션을 인가하지 않았다. 따라서 이 원장은 잘 인가되지 않는다.

둘째 예시에서 페인터가 Alice의 돈을 훔친다.

<img src="https://mintcdn.com/cantonfoundation/QAGFSphBsRkeZIBi/images/docs_website/authorization-stealing-ious.svg?fit=max&auto=format&n=QAGFSphBsRkeZIBi&q=85&s=46bd84bcbf8f39ac6fff1787bc759dc4" alt="페인터가 Alice의 돈을 훔치는 시나리오" width="1220" height="355" />

은행이 이 액션을 요청해 IOU 생성을 인가한다. 유사하게 페인터가 IOU를 자신에게 이전하는 exercise를 인가한다. 그러나 이 exercise의 액터는 Alice인데, 그녀가 exercise를 인가하지 않았다. 따라서 이 원장은 잘 인가되지 않는다.

## 유효한 원장, 의무, 오퍼, 권리

Daml 원장은 계약법이 지배하는 파티 간 실세계 상호작용을 모방하도록 설계되었다. 원장의 유효성 조건과 컨트랙트 모델에 담긴 정보는 짚을 가치가 있는 계약법 개념과 미묘한 연결이 있다.

첫째, 컨트랙트는 컨트랙트의 exercise 결과에서 비롯되는 암묵적 **온-원장 의무(on-ledger obligations)** 를 명시한다. 예컨대 `PaintOffer`는 `A`가 오퍼를 수락하면 자기 IOU를 이전할 온-원장 의무를 담는다.

둘째, Daml 원장의 모든 컨트랙트는 실세계 오퍼를 모델링할 수 있으며, 그 결과(온-원장·오프-원장)는 컨트랙트 모델이 허용하는 컨트랙트의 **Exercise** 액션으로 명시된다.

셋째, Daml 원장에서, 실세계처럼, 한 사람의 권리는 다른 사람의 의무다. 예컨대 `A`가 `PaintOffer`를 수락할 권리는 그녀가 수락하면 `P`가 그녀의 집을 칠할 의무다. Daml 원장에서 컨트랙트 모델에 따른 파티의 권리는 인가·적합성 규칙에 기반해 파티가 수행할 수 있는 exercise 액션이다.

마지막으로, 유효성 조건은 계약법을 모방하는 Daml 원장 모델의 세 중요한 속성을 보장한다.

1. **의무에는 동의가 필요하다.** Daml 원장은 계약법의 오퍼-수락 패턴을 따르며, 따라서 모든 원장 컨트랙트가 자발적으로 형성되도록 보장한다. 예컨대 다음 원장은 유효하지 않다.

   <img src="https://mintcdn.com/cantonfoundation/QAGFSphBsRkeZIBi/images/docs_website/authorization-invalid-obligation.svg?fit=max&auto=format&n=QAGFSphBsRkeZIBi&q=85&s=d200a3bae13cf1b9de6cbf4664112c70" style="width: 100%;" alt="Alice가 페인터에게 집을 칠하도록 강제하는 시나리오" width="1220" height="242" />

2. **온-원장 권리를 빼앗으려면 동의가 필요하다.** **Exercise** 액션만 컨트랙트를 소비하므로, 액터에게서 권리를 빼앗을 수 없다; 컨트랙트 모델이 액터가 누구인지 정확히 명시하고, 인가 규칙이 그들의 컨트랙트 소비 승인을 요구한다.

   예시에서 Alice는 자기 IOU를 이전할 권리가 있었다; 페인터가 직접 이전을 수행해 그 권리를 빼앗으려 한 것은 유효하지 않았다.

   <img src="https://mintcdn.com/cantonfoundation/QAGFSphBsRkeZIBi/images/docs_website/authorization-stealing-ious.svg?fit=max&auto=format&n=QAGFSphBsRkeZIBi&q=85&s=46bd84bcbf8f39ac6fff1787bc759dc4" style="width: 100%;" alt="페인터가 Alice의 돈을 훔치는 시나리오" width="1220" height="355" />

   파티는 여전히 권리를 다른 파티에 **위임(delegate)** 할 수 있다. 예컨대 Alice가 페인터의 오퍼를 수락하는 대신 카운터오퍼를 하기로 한다고 하자. 그러면 페인터가 이 카운터오퍼를 앞서와 같은 결과로 수락할 수 있다:

   <img src="https://mintcdn.com/cantonfoundation/QAGFSphBsRkeZIBi/images/docs_website/counteroffer-acceptance.svg?fit=max&auto=format&n=QAGFSphBsRkeZIBi&q=85&s=9923105b566068031bd08e1f6787c44d" style="width: 60%;" alt="최상위 컨트랙트가 CounterOffer인 PaintAgreement 흐름도" width="600" height="363" />

   여기서 `CounterOffer` 컨트랙트를 생성함으로써 Alice가 IOU 컨트랙트를 이전할 권리를 페인터에게 위임한다. 위임의 경우, 제출 전에 요청자는 요청 트랜잭션의 일부이지만 요청자가 서명자가 아닌 컨트랙트에 대해 알아야 한다. 위 예에서 페인터는 `CounterOffer` 수락을 요청하기 전에 Alice를 위한 IOU의 존재를 알아야 한다. 다음 절에서 소개하는 관찰자와 디벌전스 개념이 그런 시나리오를 가능하게 한다.

3. **온-원장 의무를 일방적으로 회피할 수 없다.** 의무가 Daml 원장에 기록되면, 컨트랙트 모델에 따라서만 제거될 수 있다. 예컨대 앞서 보인 IOU 컨트랙트 모델을 가정할 때, 원장이 `MustPay` 컨트랙트 생성을 기록하면 은행이 나중에 단순히 이 컨트랙트를 소비하는 액션을 기록할 수 없다:

   <img src="https://mintcdn.com/cantonfoundation/zmlOjLpKuDjnaObr/images/docs_website/validity-no-removal-of-obligations.svg?fit=max&auto=format&n=zmlOjLpKuDjnaObr&q=85&s=8eb83f0989399fc8152a044a779fa839" style="width: 100%;" alt="MustPay 컨트랙트 생성 후 은행이 그것을 소비하는 시간 시퀀스" width="1220" height="251" />

   즉, 위 액션이 컨트랙트 모델에 적합하지 않으므로 이 원장은 무효다.

---

# 프라이버시 (Privacy)

원장 구조 절은 파티 상호작용을 변경으로 기록하는 계층 형식을 도입해 "원장은 어떻게 생겼나?"라는 질문에 답했다. 이 절은 "누가 어떤 변경과 데이터를 보나?"라는 질문을 다룬다. 즉, Canton 원장의 프라이버시 모델을 설명한다.

Canton 원장의 프라이버시 모델은 **알 필요(need-to-know)** 에 기반하며, **하위트랜잭션 수준** 의 프라이버시를 제공한다. 즉, 파티는 자신이 지분을 가진 컨트랙트에 영향을 주는 파티 상호작용 부분과 그 결과만 안다. 계층 구조가 여기서 핵심인데, 자연스러운 하위트랜잭션 프라이버시 개념을 낳기 때문이다. 하위트랜잭션 프라이버시 개념을 정확히 하기 위해 *인포미(informee)* 와 *증인(witness)* 개념을 소개한다.

## 인포미 (Informee)

파티는 Daml 템플릿과 초이스에서 서로 다른 역할을 가질 수 있다; 파티는 `signatory`, 초이스 `controller`, 또는 컨트랙트나 초이스 `observer`로 선언될 수 있다. 컨트랙트에 대해, 파티가 컨트랙트의 서명자나 컨트랙트 관찰자면 **<abbr class="gloss" title="어떤 컨트랙트와 관계를 맺어 그것을 보거나 승인하는 파티 = 서명자 + 관찰자">이해관계자</abbr>(stakeholder)** 다.

* 모든 컨트랙트·초이스 `observer`는 이름이 시사하듯 각각 컨트랙트 변경(생성·보관)과 초이스 실행을 관찰해야 한다.
* `signatory`는 컨트랙트에 구속되어 지분을 가지므로, 컨트랙트가 생성·사용될 때 알아야 한다.
* Exercise의 액터, 즉 초이스의 `controller`는 액션에 지분을 가지므로 exercise를 봐야 한다; 다만 컨트랙트에 지분이 없을 수 있다.

이 관찰이 다음 **인포미(informee)** 정의, 즉 액션에 대해 통지받아야 하는 파티 집합을 동기 짓는다. 노드의 인포미는 다음 표에서 X로 표시된 집합의 합집합이다.

> | 액션 | 서명자 | 컨트랙트 관찰자 | 액터 | 초이스 관찰자 |
> | --- | --- | --- | --- | --- |
> | **Create** | X | X | | |
> | 소비형 **Exercise** | X | X | X | X |
> | 비소비형 **Exercise** | X | | X | X |
> | **Fetch** | X | | X | |
>
> 정의: 노드의 **인포미** 는 X로 표시된 집합의 합집합이다.

예컨대 **Create** 노드의 인포미는 생성된 컨트랙트의 이해관계자, 즉 서명자와 관찰자다. 소비형 **Exercise** 노드의 경우, 인포미는 소비된 컨트랙트의 이해관계자, 액션의 액터, 초이스 관찰자로 구성된다.

설계 결정으로, 컨트랙트 관찰자는 명시적으로 액터나 초이스 관찰자에 속하지 않는 한 비소비형 **Exercise** ·**Fetch** 액션을 통지받지 않는다. 그런 액션이 컨트랙트 자체 상태를 바꾸지 않기 때문이다.

> **참고:** 템플릿은 `preconsuming`·`postconsuming` 초이스를 선언할 수 있다. Daml은 그런 초이스를, 첫 또는 마지막 결과가 템플릿의 `Archive` 초이스를 실행하는 비소비형 초이스로 컴파일한다. 따라서 컨트랙트 관찰자는 `Archive` 하위액션의 인포미일 뿐 주 **Exercise** 액션 자체의 인포미는 아니다.

인포미 개념을 설명하기 위해 Alice와 Bob이 자산을 스왑하는 실행 예시를 쓴다. `AcceptAndSettle` 액션의 노드는 다음 그림의 파란 육각형에 표시된 인포미를 갖는다. 예컨대 Alice는 입력 컨트랙트 #3의 서명자이므로 루트 노드 ①의 인포미이고, Bob은 초이스의 액터이므로 인포미다. 유사하게 Bank 2와 Bob은 Fetch 노드 ③의 인포미인데, Bank 2가 입력 컨트랙트 #2의 서명자이고 Bob이 액터이기 때문이다. Bob이 액터가 아니었다면, 컨트랙트 관찰자는 비소비형 Exercise·Fetch의 인포미가 자동으로 되지 않으므로 인포미가 아니었을 것이다.

<img src="https://mintcdn.com/cantonfoundation/QAGFSphBsRkeZIBi/images/docs_website/dvp-acceptandsettle-informees.svg?fit=max&auto=format&n=QAGFSphBsRkeZIBi&q=85&s=deab88d50ec2ecdae62259b6fc20baa5" style="width: 100%;" alt="AcceptAndSettle 액션의 노드의 인포미" width="2321" height="1311" />

액션의 인포미는 그 루트 노드의 인포미다. 중요하게, 원장 구조 절에서 언급했듯 노드는 자식 없이 존재할 수 없다; 액션만 전체 트리로서 존재할 수 있다. 따라서 액션의 인포미는 자신이 개별 노드의 인포미가 아니더라도 액션의 모든 노드를 볼 권한이 있다. 이 불일치는 다음 절의 증인(witness) 개념으로 형식화된다.

## 증인 (Witness)

단일 노드는 여러 액션의 일부일 수 있다. 예컨대 아래 다이어그램은 각 하위액션의 테두리 없는 상자 우상단에 표시된 인포미로 하위액션 다이어그램을 확장한다. 여기서 Create 노드 ③은 세 하위액션, 즉 노드 ①, ②, ③에 뿌리를 둔 것의 일부다. 따라서 이 Create 노드는 자신이 노드 자체의 인포미가 아니어도 이 모든 액션의 인포미에게 보인다. 그 파티들을 증인이라 한다. 형식적으로, 주어진 트랜잭션 `tx`에 대해, `tx`의 노드의 **증인(witnesses)** 은 그 노드를 담는 `tx`의 모든 하위액션의 인포미의 합집합이다. 특히 노드의 모든 인포미는 증인이기도 하다.

다이어그램은 하위액션의 증인을 그 루트 액션에 보라색으로 보인다. 노드 ③의 경우, 증인은 Alice, Bob, Bank 1이다 — Bob이 ①과 ③의 인포미; Bank 1이 ②와 ③의 인포미; Alice가 ①과 ②의 인포미이기 때문이다.

<img src="https://mintcdn.com/cantonfoundation/zmlOjLpKuDjnaObr/images/docs_website/dvp-settle-witness.svg?fit=max&auto=format&n=zmlOjLpKuDjnaObr&q=85&s=fced7c0cefb8dc1176e5657ff6ce9e75" style="width: 60%;" alt="Settle 초이스 하위액션의 인포미와 노드의 증인" width="1122" height="1082" />

## 투영 (Projection)

인포미는 자신이 볼 권한이 있는 변경을 봐야 하지만, 이는 그런 변경을 담은 전체 트랜잭션을 볼 권한이 있다는 뜻은 아니다. 이는 트랜잭션의 *투영(projection)* 으로 정확히 표현되며, 이는 파티 그룹이 트랜잭션에 대해 얻는 뷰를 정의한다. 직관적으로, 커밋 내 트랜잭션이 주어지면, 파티 그룹은 그 인포미가 파티 중 적어도 하나를 포함하는 컨트랙트의 모든 액션으로 구성된 하위트랜잭션만 본다. 동등하게, 그 증인이 파티 중 적어도 하나를 포함하는 노드만 본다. 따라서 프라이버시가 하위트랜잭션 수준에서 얻어진다.

이 절은 먼저 트랜잭션의 투영을, 그다음 원장의 투영을 정의한다.

### 트랜잭션 투영

다음 다이어그램은 `AcceptAndSettle` Exercise 액션을 유일한 루트 액션으로 가진 트랜잭션의 예를 준다.

<img src="https://mintcdn.com/cantonfoundation/QAGFSphBsRkeZIBi/images/docs_website/dvp-acceptandsettle-projection.svg?fit=max&auto=format&n=QAGFSphBsRkeZIBi&q=85&s=19d1943bd83536d7d81d2d3748a81ef1" style="width: 100%;" alt="AcceptAndSettle 투영" width="1748" height="3362" />

Alice와 Bob 모두 루트 액션(Bob이 Alice의 `ProposeSimpleDvP` 컨트랙트에 `AcceptAndSettle` 초이스를 실행)의 인포미이므로, Alice나 Bob 또는 둘 다로의 투영은 전체 Exercise 액션으로 구성된다. 액션이 루트 노드 아래 전체 하위 트리로 구성되므로, Alice와 Bob 각자는 자신이 증인인 모든 노드를 본다. 예컨대 Alice의 투영은 Fetch 하위액션, Bob의 #2에 대한 `Transfer` exercise, Bob의 `SimpleAsset` 컨트랙트 #5 생성을 포함한다. 유사하게 Bob의 투영은 Alice의 #1에 대한 `Transfer` Exercise와 Alice의 `SimpleAsset` 컨트랙트 #6 생성을 포함한다.

반면 은행들은 루트 액션의 인포미가 *아니다*. 실제로 Bank 1은 #1에 대한 `Transfer` Exercise 액션과 그 하위액션인 Bob의 새 자산 #5 생성에서만 인포미로 나타난다. 따라서 Bank 1로의 투영은 이 Exercise 액션만으로 구성된다. Bank 2는 트리에서 두 무관한 액션의 인포미로 나타난다: Fetch 액션과 #2에 대한 `Transfer` Exercise 액션. 따라서 Bank 2로의 투영은 이 두 액션을 루트 액션으로 가진 트랜잭션으로 구성된다. 이는 투영이 단일 루트 액션을 하위액션 목록으로 바꿀 수 있음을 보인다.

> **참고:** 은행 투영의 프라이버시 함의에 주목하라. 각 은행은 Alice에서 Bob으로 또는 그 반대의 `Transfer`가 일어났음을 알지만, *왜* 이전이 일어났는지는 알지 *못한다*. 특히 Bank 2는 컨트랙트 #2의 Fetch와 Exercise 사이에 무슨 일이 일어나는지 알지 못한다. 실무에서 이는 Bank 1과 Bank 2가 Alice와 Bob이 무엇과 자산을 교환하는지 알지 못함을 의미하며, 은행에 대해 Alice와 Bob에게 프라이버시를 제공한다.

하단의 Bank 1과 Bank 2 둘 다로의 투영은 여러 파티로의 투영이 각 파티로의 투영을 합친 것보다 엄격히 더 많은 정보를 담을 수 있음을 보인다. 다르게 말해, Bank 1과 Bank 2로의 투영을 Bank 1 투영과 Bank 2 투영만으로 재구성하는 것은 불가능하다. 여기서는 세 루트 액션의 순서가 개별 투영으로 고유하게 결정될 수 없기 때문이다. 이 이유로 투영은 파티 집합에 대해 정의된다.

> **정의: 투영(projection)**
> 파티 집합 `P`에 대한 트랜잭션의 **투영** 은 트랜잭션의 각 루트 액션 `act`에 대해 다음을 수행해 얻는 하위트랜잭션이다.
> 1. `P`가 `act`의 인포미 중 적어도 하나를 담으면, `act`를 결과를 포함해 그대로 유지.
> 2. 그러지 않고 `act`에 결과가 있으면, `act`를 그 결과의 (`P`에 대한) 투영으로 치환(비어 있을 수 있음).
> 3. 그러지 않으면, `act`를 결과를 포함해 버림.

이 정의는 노드가 아니라 액션, 즉 노드의 하위 트리에 작용한다. 따라서 파티 집합 `P`에 대한 트랜잭션의 투영은 `P`가 노드의 증인 중 적어도 하나를 담을 때만 그 노드를 담는다.

투영이 트랜잭션이므로, 투영을 더 투영하는 것이 가능하다. 투영 연산은 다음 **흡수(absorption)** 속성을 갖는다: 감소하는 파티 부분집합으로의 투영은 흡수적이다. 즉, 파티 집합 `P`가 `Q`의 부분집합이면, 트랜잭션을 먼저 `Q`로 투영한 뒤 `P`로 투영하는 것은 직접 `P`로 투영하는 것과 같다. 직관적으로, 이 속성은 파티 그룹이 트랜잭션에 대해 그 부분그룹이 스스로 배우는 것만큼은 함께 배운다는 사실을 표현한다. 역은 거짓이며, 위 Bank 1·2로의 투영 예가 보였다.

반대로 `P`가 `Q`의 부분집합이 아니면, 트랜잭션을 먼저 `Q`로 투영한 뒤 `P`로 투영하는 것은 단지 `P`로의 투영의 하위트랜잭션을 낳는다. 예컨대 위 Bank 1 투영을 Bob으로 투영하면, 결과 트랜잭션은 컨트랙트 #5의 Create 액션만으로 구성된다. 이는 Bob 투영의 고유 하위트랜잭션이다.

이 차이는 Bank 1이 Bob보다 Exercise 노드에 대해 덜 안다는 것을 반영한다. 특히 Bank 1은 자기 투영에서 Bob이 Exercise 노드의 증인임을 추론할 수 없다. 이는 일반적 패턴이다: 액션의 인포미는 그 안의 노드의 증인에 대해 알지 못할 수 있다. 이는 트랜잭션의 숨겨진 부분에 누가 관여하는지 숨기므로 프라이버시 관점에서 결정적이다.

### 원장 투영

마지막으로, 파티 집합 `P`에 대한 **원장의 투영** `l`은 다음과 같이 얻는 업데이트의 DAG다:

* `l`의 각 업데이트의 트랜잭션을 `P`에 대해 투영하되 업데이트 ID는 유지.
* 결과에서 빈 트랜잭션을 가진 업데이트를 제거.

투영의 간선 정의는 인과성 절로 미룬다. 그때까지는 원장이 전체 순서되었고 투영이 같은 순서를 유지한다고 가정한다.

특히, 원장의 투영은 원장이 아니라 업데이트의 DAG다. 커밋의 요청자는 보통 투영의 액션의 증인이지 인포미가 아니므로 유지될 수 없다. 그러나 액션의 인포미가 모든 증인을 알아서는 안 된다. 예컨대 Bank 1 투영이 마지막 커밋의 요청자로 Bob을 언급하면, Bank 1이 Bob이 컨트랙트 #1에 `Transfer` 초이스를 실행하는 Alice의 증인임을 추론할 수 있다.

전체 DvP 예시의 원장을 투영하면 각 파티에 대해 다음 투영이 나온다.

<img src="https://mintcdn.com/cantonfoundation/QAGFSphBsRkeZIBi/images/docs_website/dvp-ledger-projections.svg?fit=max&auto=format&n=QAGFSphBsRkeZIBi&q=85&s=9f32669cafa03a1f454985a745255eee" style="width: 100%;" alt="각 파티 투영의 시간 시퀀스" width="3802" height="5682" />

각 파티의 투영을 차례로 살펴보면:

1. Alice는 첫째, 셋째, 넷째 커밋의 전부를 본다 — 모든 루트 액션의 인포미이기 때문이다. 반면 Alice는 Bob의 1 USD `SimpleAsset`의 이해관계자가 아니므로 둘째 커밋의 어떤 것도 보지 않는다. 이 트랜잭션은 Alice 투영에 전혀 없다. 그러나 이 트랜잭션의 출력(컨트랙트 #2)이 Alice 투영의 마지막 커밋에서 쓰인다. 따라서 컨트랙트 #2가 원장 밖 왼쪽에 입력으로 표시된다. 이 효과는 아래 소급 디벌전스에서 논한다.
2. Bob의 투영은 Alice와 유사하다: 둘째, 셋째, 넷째 커밋의 전부를 보지만 첫 커밋은 보지 않고 대신 컨트랙트 #1을 입력으로만 본다.
3. Bank 1과 Bank 2는 자기 `SimpleAsset`을 생성하는 커밋과 그것에 대한 `Transfer` Exercise만 본다. 추가로 Bank 2는 마지막 커밋의 `SimpleAsset` Fetch를 본다(위 트랜잭션 투영에서 이미 논함).

업데이트 ID는 서로 다른 투영 간 상관을 가능하게 한다. 예컨대 Bank 1과 Bank 2 모두 업데이트 ID `TX 3`을 본다. 따라서 그들의 투영이 단일 노드를 공유하지 않아도 같은 원자적 트랜잭션에서 일어났음을 추론할 수 있다.

> **참고:** <abbr class="gloss" title="파티를 호스팅하고 그 파티의 컨트랙트를 저장·실행하는 노드. 밸리데이터의 핵심 구성요소">참여자 노드</abbr>의 사용자는 업데이트 트리 스트림으로 자기 파티의 원장 투영을 요청할 수 있다.

## 디벌전스: 비이해관계자가 컨트랙트를 볼 때

Canton 원장 프라이버시 모델의 지도 원칙은 컨트랙트가 그 이해관계자에게만 보여야 한다는 것이다. 그러나 원장 투영은 컨트랙트가 다른 파티에게도 보이게 할 수 있다. 원장 투영을 통해 비이해관계자에게 컨트랙트를 보이는 것을 **디벌전스(divulgence)** 라 한다. 디벌전스는 Canton 원장 설계의 의도적 선택이며 두 형태로 온다:

* **즉시 디벌전스(Immediate divulgence)** 는 증인이 자신이 인포미가 아닌 컨트랙트 생성을 보는 것을 가리킨다. DvP의 원장 투영 예에서, Bob은 Alice의 새 `SimpleAsset`(컨트랙트 #6)의 Create 액션의 증인이지만 인포미는 아니다. 개념적으로, Bob이 `Transfer` 초이스를 실행하는 순간, 그는 `Transfer`의 결과, 즉 자산이 이제 Alice에게 속함을 볼 일시적 지분도 얻는다.

  일반적으로 액션의 결과를 숨길 이유가 없다. Daml이 결정론적이므로 Bob은 어쨌든 자신이 인포미인 액션의 결과를 계산할 수 있다.

* **소급 디벌전스(Retroactive divulgence)** 는 이 컨트랙트를 쓰는 노드의 비인포미 증인에게 입력 컨트랙트가 보이는 것을 가리킨다. 예컨대 Bob의 `SimpleAsset`(컨트랙트 #2)의 Fetch는 Alice에게 보이고, 따라서 #2의 Create 액션이 Alice 투영의 일부가 아니어도 Alice 투영은 이 컨트랙트를 입력으로 참조한다.

  소급 디벌전스는 Alice가 자기 투영의 트랜잭션을 검증할 수 있게 한다(원장 무결성의 일관성 참고). 즉, Alice는 Bob이 자기 제안에 명시한 대로 적합한 `SimpleAsset`을 할당하는지 확인할 수 있다.

  소급 디벌전스는 Alice를 Bob의 `SimpleAsset`(컨트랙트 #2)의 Create 액션의 증인으로 만들지 않는다 — 입력 컨트랙트는 그 Create 액션과 같지 않기 때문이다. 다이어그램에서 이 구분은 입력 컨트랙트의 점선 테두리와 왼쪽 배치로 시각화된다.

Ledger API의 업데이트 서비스로, 사용자는 파티 투영의 트리에서 즉시 디벌전된 컨트랙트를 볼 수 있다(이 트리가 Create 노드를 담으므로). 반면 Ledger API는 현재 소급 디벌전스의 컨트랙트 ID를 조회할 수단을 제공하지 않는다.

## 공개(Disclosure): 비이해관계자가 컨트랙트를 쓸 때

앞 절의 디벌전스는 파티가 자신이 이해관계자가 아닌 컨트랙트를 알게 되는 것을 가리킨다. 공개(Disclosure)는 그런 파티가 자기 트랜잭션에서 컨트랙트를 쓰는 것에 관한 것이다.

실행 예시에서 Bob이 `Settle` 초이스 실행에 `submitWithDisclosures`를 쓰는 것을 상기하라. 이는 Bob(과 그 참여자 노드)이 일반적으로 Alice가 제안에 할당한 `SimpleAsset` 컨트랙트 #2를 모르기 때문이다. 공개는 Alice가 오프-원장 통신 채널로 Bob에게 이 컨트랙트를 알려주는 것을 의미한다. Daml 스크립트 실행 예시에서는 스크립트 자체가 통신 채널이다. 실세계 맥락에서 Alice는 Bob이 관련 데이터를 가져올 API를 제공할 것이다.

즉시 디벌전스가 후속 트랜잭션의 공개를 수반하지 않는 것은 설계 결정이다. 예컨대 DvP가 정산된 후 Alice가 Bob에게 두 자산을 다시 스왑하는 또 다른 DvP 제안을 생성한다:

```haskell
proposeDvP2 <- submit alice $ do
  createCmd ProposeSimpleDvP with
      proposer = alice
      counterparty = bob
      allocated = newUsd
      expected = eurAsset
```

그러면 Bob의 커맨드 제출은 Bob이 Alice의 `SimpleAsset` 생성의 증인이어도 Alice의 `SimpleAsset` 공개를 포함해야 한다. 공개 없는 평범한 `submit`은 작동하지 않는다.

즉시 디벌전스를 공개에 암묵적으로 쓰지 않는 동기는 그것이 취약한 워크플로로 이어지기 때문이다. 문제는 비이해관계자가 컨트랙트 생성만 알 뿐 보관 같은 후속 액션은 모른다는 것이다. 따라서 비이해관계자가 컨트랙트를 얼마나 오래 보관해야 하는지에 대한 일반 규칙이 없다. 너무 오래 보관하면 저장을 낭비하고; 너무 짧게 보관하면 특정 애플리케이션이 깨질 수 있다. 대신 이 규칙은 애플리케이션이 디벌전된 컨트랙트에 대해서도 공개를 명시적으로 설계하고 적합한 애플리케이션별 규칙을 마련하도록 강제한다.

공개의 대안 접근은 원래 `SimpleAsset` 컨트랙트를 Bob이 컨트랙트 관찰자가 되는 것으로 교체하는 것이다. 이는 Alice의 선택의 관찰자로 새 `SimpleAsset`을 생성하는 (소비형) exercise 액션으로 컨트랙트 모델을 확장해야 한다. 원장의 액션 증가 외에, 두 접근은 컨트랙트에 대해 통지받는 파티를 누가 아는지에서 다르다:

* Alice가 오프-원장 채널로 Bob에게 `SimpleAsset`을 공개하면, Alice와 Bob만 이 공개를 알면 된다. 따라서 Alice가 같은 컨트랙트를 Charlie에게 공개할 때, Charlie는 Alice가 이미 Bob에게 컨트랙트를 보였음을 알 필요가 없고, Bob은 Alice가 Charlie에게 공개함을 알 필요가 없다.
* 반면 Alice가 Bob을 컨트랙트 관찰자로 추가한 뒤 Charlie를 또 다른 관찰자로 추가하면, 컨트랙트 관찰자인 Bob이 보관과 생성을 통지받는다. 유사하게 Charlie도 Bob이 관찰자임을 안다. 즉, 모든 이해관계자가 서로를 안다. 이는 Alice가 실제로 Bob과 Charlie가 서로 아는 것을 원치 않을 때 프라이버시 문제를 만든다.

나아가 파티를 관찰자로 추가하는 것은 큰 수에 잘 확장되지 않는다 — 모든 관찰자가 다른 모든 관찰자를 알기 때문이다: `N`개 관찰자를 가진 Create 이벤트는 적어도 그 `N`개 파티의 투영에 나타난다. 따라서 모든 투영의 크기 합은 이미 `N`에 대해 이차(quadratic)다 — 크기 적어도 `N`인 액션이 `N`개 다른 투영에 나타나기 때문이다. 관찰자가 하나씩 추가되면 `N`개 보관·생성이 필요하므로 모든 투영의 크기 합은 `N`에 대해 삼차(cubic)다.

---

# Synchronizer 인지 투영 (Synchronizer-aware projection)

특정 Daml 원장은 다른 Daml 원장과 상호운용할 수 있다. 즉, 한 원장에서 생성된 컨트랙트가 다른 원장의 트랜잭션에서 쓰이고 보관될 수 있다. 일부 참여자 노드는 여러 원장에 연결해 Ledger API로 그 원장에 대한 통합 접근을 파티에 제공할 수 있다. 예컨대 조직이 처음에 두 워크플로를 두 Daml 원장에 배포하면, 나중에 그것들을 두 원장에 걸친 더 큰 워크플로로 조합할 수 있다.

상호운용성은 파티가 여러 참여자 노드에 <abbr class="gloss" title="참여자 노드가 파티를 대신해 원장에서 활동(컨트랙트 저장·트랜잭션 제출·확인)해 주는 것. 로컬 파티는 키까지 노드가 관리하고, 외부 파티는 제출 키를 파티 자신이 보유(노드는 중계)">호스팅</abbr>될 때 참여자 노드가 파티의 원장 투영(즉 로컬 원장)에 갖는 가시성을 제한할 수 있다. 이 제한은 파티가 각 참여자 노드의 Ledger API로 관찰할 수 있는 것에 영향을 준다. 특히 상호운용성은 파티가 관찰하는 이벤트와 그 순서에 영향을 준다. 이 문서는 상호운용성으로 인한 가시성 제한과 업데이트 서비스에 대한 그 결과를, 예시로 그리고 상호운용 가능한 버전의 인과성 그래프와 투영을 도입해 형식적으로 설명한다.

> **참고:** Daml 원장의 상호운용성은 활발히 개발 중이다. 이 문서는 상호운용성 비전을 기술하고 Ledger API 서비스가 어떻게 바뀔지와 어떤 보장이 제공되는지에 대한 아이디어를 준다. 기술된 서비스와 보장은 상호운용성 구현이 진행되면서 예고 없이 바뀔 수 있다.

## 상호운용성 예시

### 토폴로지

참여자 노드는 Daml 원장에 연결하고 파티는 Ledger API로 이 원장의 투영에 접근한다. 다음 그림은 그런 설정을 보인다.

<img src="https://mintcdn.com/cantonfoundation/zmlOjLpKuDjnaObr/images/docs_website/multiple-domains.svg?fit=max&auto=format&n=zmlOjLpKuDjnaObr&q=85&s=8a18fc12d93bfbf8bdfc408395b6650c" alt="두 상호운용 가능한 원장의 예시 토폴로지" width="1200" height="637" />

이 다이어그램의 구성 요소:

* 상호운용 가능한 **Daml 원장** 집합이 있다: 원장 1(녹색)과 원장 2(노란색).
* 각 **참여자 노드** 는 Daml 원장의 부분집합에 연결된다.
  * 참여자 노드 1과 3은 원장 1과 2에 연결.
  * 참여자 노드 2는 원장 1에만 연결.
* 참여자 노드는 연결된 Daml 원장의 부분집합에서 파티를 호스팅한다. 참여자 노드는 파티를 호스팅하는 Daml 원장에 대한 접근을 파티에 제공한다.
  * 참여자 노드 1은 원장 1과 2에서 Alice를 호스팅.
  * 참여자 노드 2는 원장 1에서 Alice를 호스팅.
  * 참여자 노드 3은 원장 1과 2에서 페인터를 호스팅.

### 참여자에서의 집계

참여자 노드는 이 원장들의 업데이트를 모아 파티의 업데이트 서비스·상태 서비스로 출력한다. 참여자 노드가 상호운용 가능한 Daml 원장의 부분집합에서만 파티를 호스팅하면, 그 참여자 노드의 업데이트·상태 서비스는 그 원장들에서만 도출된다.

예컨대 위 <abbr class="gloss" title="어떤 노드·파티·키가 네트워크에 참여하는지를 정의하는 구성 정보">토폴로지</abbr>에서, 트랜잭션이 원장 2에서 이해관계자 Alice를 가진 컨트랙트를 생성하면, `P1`의 Alice 트랜잭션 스트림은 이 트랜잭션을 방출하고 컨트랙트를 활성으로 보고하지만, `P2`의 Alice 스트림은 그러지 않는다.

### Enter와 Leave 이벤트

상호운용성으로, 트랜잭션은 생성이 다른 원장에 기록된 컨트랙트를 쓸 수 있다. 위 토폴로지에서 예컨대 한 트랜잭션이 원장 1에서 이해관계자 Alice를 가진 컨트랙트 `c1`을 생성하고 다른 트랜잭션이 원장 2에서 컨트랙트를 보관한다. 그러면 참여자 노드 `P2`는 **Create** 액션을 `CreatedEvent`로 출력하지만, `P2`가 원장 2에서 Alice를 호스팅하지 않아 원장 2가 `P2`에 통지할 수 없으므로 업데이트 서비스에 `ArchiveEvent` 형태의 **Exercise** 는 출력하지 않는다. 반대로 한 트랜잭션이 원장 2에서 이해관계자 Alice를 가진 컨트랙트 `c2`를 생성하고 다른 트랜잭션이 원장 1에서 보관하면, `P2`는 `ArchivedEvent`를 출력하지만 `CreatedEvent`는 출력하지 않는다.

트랜잭션 스트림을 일관되게 유지하기 위해, `P2`는 추가로 Alice의 트랜잭션 스트림에 **Leave** `c1` 액션을 출력한다. 이 액션은 참여자 노드가 이 컨트랙트에 관한 이벤트를 더 이상 출력하지 않음을, 특히 컨트랙트가 보관될 때 출력하지 않음을 신호한다. 따라서 컨트랙트는 상태 서비스에 더 이상 보고되지 않고 커맨드 제출에 쓸 수 없다.

반대로 `P2`는 `ArchivedEvent` 전 어느 시점에 트랜잭션 스트림에 **Enter** `c2` 액션을 출력한다. 이 액션은 참여자 노드가 이 컨트랙트에 관한 이벤트를 출력하기 시작함을 신호한다. 컨트랙트는 상태 서비스에 보고되고 커맨드 제출에 쓸 수 있다.

**Enter** 와 **Leave** 액션은 각각 **Create** 와 소비형 **Exercise** 액션과 유사하나, **Enter** 와 **Leave** 는 같은 컨트랙트에 여러 번 일어날 수 있는 반면 각 컨트랙트에 최대 하나의 **Create** 와 최대 하나의 소비형 **Exercise** 액션이 있어야 한다는 점이 다르다.

이 **Enter** 와 **Leave** 이벤트는 기반 상호운용성 프로토콜이 생성한다. 이는 커맨드 제출의 일부로 또는 부하 분산 같은 다른 이유로 일어날 수 있다. 기반 원장과 상호운용성 프로토콜의 신뢰 가정을 전제로, **Enter** 액션이 컨트랙트 사용에 선행함이 보장된다.

컨트랙트는 참여자 노드의 가시성에 여러 번 진입·이탈할 수 있다. 예컨대 페인터가 다음 커맨드를 제출하고 그 커밋이 주어진 원장에 도착한다고 하자.

1. 원장 2에서 서명자 Alice와 페인터를 가진 컨트랙트 `c` 생성
2. 원장 1에서 `c`에 비소비형 초이스 `ch1` 실행.
3. 원장 2에서 `c`에 비소비형 초이스 `ch2` 실행.
4. 원장 1에서 `c`에 소비형 초이스 `ch3` 실행.

그러면 `P2`가 `A`에게 제공하는 트랜잭션 트리 스트림은 컨트랙트 `c`에 관한 다섯 액션을 담는다: **Enter**, 비소비형 **Exercise**, **Leave**, **Enter**, 소비형 **Exercise**. 중요하게, `P2`는 **Leave** 와 후속 **Enter** 가 상쇄되어 보여도 생략해서는 안 된다. 그 존재가 `P2`의 Alice 이벤트 스트림이 그 사이 일부 이벤트(이 예에서 초이스 `ch2` 실행)를 놓칠 수 있음을 나타내기 때문이다.

`P2`의 플랫 트랜잭션 스트림은 비소비형 exercise 초이스를 생략한다. 그럼에도 소비형 **Exercise** 전에 세 액션 **Enter**, **Leave**, **Enter** 를 담는다. 참여자 노드가 **Leave** 액션 시점에 또 다른 **Enter** 액션이 올지 알 수 없기 때문이다.

반면 `P1`은 원장 둘 다에서 Alice를 호스팅하므로 이 예에서 **Enter** 와 **Leave** 액션을 전혀 출력할 필요가 없다.

### 크로스-원장 트랜잭션

상호운용성으로, 크로스-원장 트랜잭션은 여러 상호운용 가능한 Daml 원장에서 동시에 커밋될 수 있다. 그런 크로스-원장 트랜잭션은 **Enter** 와 **Leave** 액션의 동기화 오버헤드 일부를 피한다. 크로스-원장 트랜잭션이 여러 Daml 원장의 컨트랙트를 쓰면, 이해관계자가 실제로 참여자 노드에서 보이지 않는 자기 컨트랙트의 액션을 목격할 수 있다.

예컨대 인과성 예시의 분할 페인트 카운터오퍼 워크플로가 다음과 같이 커밋된다고 하자: `CounterOffer`와 `PaintAgree` 컨트랙트의 액션은 원장 1에 커밋된다. 모든 `Iou` 액션은 (어떤 참여자 노드가 원장 2에서 은행을 호스팅한다고 가정하고) 원장 2에 커밋된다. 마지막 트랜잭션은 크로스-원장 트랜잭션인데, `CounterOffer`의 보관과 `PaintAgree`의 생성이 원장 1에, Alice의 `Iou`를 페인터에게 이전하는 것이 원장 2에 동시에 커밋되기 때문이다.

마지막 트랜잭션에 대해, 참여자 노드 1은 평소처럼 업데이트 서비스로 Alice에게 트랜잭션 트리, 두 보관, `PaintAgree` 생성을 통지한다. 참여자 노드 2도 Alice의 트랜잭션 트리 스트림에 Alice의 `Iou`의 소비형 **Exercise** 를 담은 전체 트랜잭션 트리를 출력한다. 그러나 `Iou` 액션이 원장 2에 커밋되고 참여자 노드 2가 원장 2에서 Alice를 호스팅하지 않으므로 Alice의 `Iou`의 **Create** 는 출력하지 않았다. 따라서 Alice는 exercise의 인포미여도 단지 보관을 *목격(witness)* 한다. 따라서 **Exercise** 액션은 참여자 노드 2의 트랜잭션 트리 스트림에서 단지 목격된 것으로 표시된다.

일반적으로, 파티가 액션의 인포미이지만 그 액션이 참여자 노드가 파티를 호스팅하는 원장에 커밋되지 않으면, 액션은 **단지 목격됨(merely being witnessed)** 으로 표시된다. **Enter** 와 **Leave** 와 달리, 그런 목격된 액션은 참여자 관점에서 인과성에 영향을 주지 않으므로 더 약한 순서 보장을 제공한다. 그런 목격된 액션은 플랫 트랜잭션 스트림에도, 상태 서비스에도 나타나지 않는다.

예컨대 **Create** `PaintAgree` 액션이 원장 1 대신 원장 2에 커밋된다고 하자, 즉 `CounterOffer` 액션만 원장 1에 커밋된다. 그러면 참여자 노드 2는 **Create** `PaintAgree` 액션도 트랜잭션 트리 스트림에서 단지 목격된 것으로 표시한다. 따라서 컨트랙트를 활성으로 보고하지 않고 Alice가 참여자 노드 2를 통한 제출에 컨트랙트를 쓸 수도 없다.

## 멀티원장 인과성 그래프

이 절은 인과성 그래프를 상호운용 설정으로 일반화한다.

모든 활성 Daml 컨트랙트는 최대 하나의 Daml 원장에 거주한다. 컨트랙트의 어떤 사용도 그것이 거주하는 Daml 원장에 커밋되어야 한다. 처음 컨트랙트가 생성될 때, **Create** 액션이 커밋되는 Daml 원장에 거주를 둔다. 서로 다른 Daml 원장에 거주하는 컨트랙트를 쓰려면, 크로스-원장 트랜잭션이 여러 Daml 원장에 커밋된다.

다만 크로스-원장 트랜잭션은 오버헤드를 발생시키고, 컨트랙트가 자기 거주지가 아닌 Daml 원장에서 자주 쓰이면 상호운용성 프로토콜이 컨트랙트를 다른 Daml 원장으로 이주(migrate)시킬 수 있다. 컨트랙트가 기원 Daml 원장에서 거주를 포기하고 대상 Daml 원장에 거주를 두는 과정을 **컨트랙트 이전(contract transfer)** 이라 한다. 트랜잭션 스트림의 **Enter** 와 **Leave** 이벤트는 아래 설명하듯 그런 컨트랙트 이전에서 비롯된다. 또한 컨트랙트 이전은 기원과 대상 Daml 원장 간 동기화 지점이므로 순서 보장에 영향을 준다. 따라서 인과성 그래프를 상호운용성을 위해 일반화한다.

> **정의 «이전 액션(transfer action)»**: 컨트랙트 `c`에 대한 **이전 액션** 은 **Transfer** `c`로 쓴다. 이전 액션의 **인포미** 는 `c`의 이해관계자다.

이후 *액션* 이라는 용어는 트랜잭션 액션(**Create**, **Exercise**, **Fetch**, **NoSuchKey**)과 이전 액션을 모두 가리킨다. 특히 컨트랙트 `c`에 대한 이전 액션은 `c`에 대한 액션이다. 다만 이전 액션은 트랜잭션에 나타나지 않는다. 따라서 트랜잭션 액션은 이전 액션을 결과로 가질 수 없고, 이전 액션은 결과를 전혀 갖지 않는다.

> **정의 «멀티원장 인과성 그래프»**: Daml 원장 집합 `Y`에 대한 **멀티원장 인과성 그래프** `G`는 유한·전이적으로 닫힌·방향 비순환 그래프다. 정점은 트랜잭션이거나 이전 액션이다. 모든 액션은 다음 표에 따라 `Y`의 **들어오는 원장(incoming ledger)** 과 **나가는 원장(outgoing ledger)** 으로 주석될 수 있다:

| 액션 | 들어오는 원장 | 나가는 원장 |
| --- | --- | --- |
| **Create** | 아니오 | 예 |
| 소비형 **Exercise** | 예 | 아니오 |
| 비소비형 **Exercise** | 예 | 예 |
| **Fetch** | 예 | 예 |
| **NoSuchKey** | 아니오 | 아니오 |
| **Transfer** | 아마도 | 아마도 |

비소비형 **Exercise** 와 **Fetch** 액션은 들어오는 원장이 나가는 원장과 같아야 한다. **Transfer** 액션은 적어도 하나를 가져야 한다. 둘 다 설정된 **transfer** 액션은 완전한 이전을 나타낸다. 들어오는 원장만 설정되면 **Enter** 이벤트의 부분 정보를 나타내고; 나가는 것만 설정되면 **Leave** 이벤트의 부분 정보다. 들어오거나 나가는 원장 주석이 없는 **Transfer** 액션을 각각 **Enter** 또는 **Leave** 액션이라 한다.

액션 순서는 멀티원장 인과성 그래프로 그에 맞게 일반화된다.

페인터가 서명자 Alice와 페인터를 가진 컨트랙트 `c`에 세 초이스를 실행하는 Enter·Leave 이벤트 예에서, 네 트랜잭션은 다음 멀티원장 인과성 그래프를 낳는다. 들어오는·나가는 원장은 색으로 인코딩된다(원장 1은 녹색, 원장 2는 노란색). **Transfer** 정점은 원으로 표시되며, 왼쪽 반은 들어오는 원장 색, 오른쪽 반은 나가는 원장 색이다.

<img src="https://mintcdn.com/cantonfoundation/zmlOjLpKuDjnaObr/images/docs_website/interoperable-causality-graph-linear.svg?fit=max&auto=format&n=zmlOjLpKuDjnaObr&q=85&s=24daba5cd4c959fd25e6e92123ae70de" style="width: 100%;" alt="이전 액션을 가진 멀티원장 인과성 그래프" width="1440" height="183" />

> **참고:** 일반 인과성 그래프처럼, 멀티원장 인과성 그래프 다이어그램도 가독성을 위해 전이 간선을 생략한다.

크로스-도메인 트랜잭션 예로, 크로스-도메인 트랜잭션을 가진 분할 페인트 카운터오퍼 워크플로를 보자. 해당 멀티원장 인과성 그래프가 아래 표시된다. 마지막 트랜잭션 `tx4`는 그 액션이 둘 이상의 색을 가지므로 크로스-원장 트랜잭션이다.

<img src="https://mintcdn.com/cantonfoundation/QAGFSphBsRkeZIBi/images/docs_website/counteroffer-interoperable-causality-graph.svg?fit=max&auto=format&n=QAGFSphBsRkeZIBi&q=85&s=a00a595da5b5ff73b7432c091c20ac2f" style="width: 100%;" alt="두 Daml 원장의 분할 페인트 카운터오퍼 워크플로 멀티원장 인과성 그래프" width="1440" height="380" />

### 일관성

> **정의 «원장 트레이스(ledger trace)»**: **원장 트레이스** 는 모든 `i > 0`에 대해 `b(i-1) = ai`인 쌍 `(ai, bi)`의 유한 목록이다. 여기서 `ai`와 `bi`는 Daml 원장을 식별하거나, 모든 Daml 원장 식별자와 다른 특수 값 `NONE`이다.

> **정의 «컨트랙트에 대한 멀티원장 인과적 일관성»**: `G`를 멀티원장 인과성 그래프, `X`를 `G`의 컨트랙트 `c`에 대한 액션 집합이라 하자. `G`는 다음이 모두 성립하면 `X`에서 **컨트랙트 `c`에 대해 멀티원장 일관**된다:
> 1. `X`가 비어 있지 않으면, `X`는 **Create** 또는 적어도 하나의 **Enter** 액션을 담는다. create를 담으면 이 create가 `X`의 다른 모든 액션에 선행한다. 안 담으면 `X`의 다른 모든 액션에 선행하는 **Enter** 액션이 하나 존재한다.
> 2. `X`는 최대 하나의 **Create** 액션을 담는다.
> 3. `X`가 소비형 **Exercise** 액션 `act`를 담으면, `act`는 `G`의 액션 순서에서 `X`의 다른 모든 액션을 뒤따른다.
> 4. `X`의 모든 **Transfer** 액션은 `X`의 다른 모든 액션과 순서된다.
> 5. `X`의 모든 극대 사슬(maximal chain, 즉 `X`의 극대 전체순서 부분집합)에 대해, (들어오는 원장, 나가는 원장) 쌍의 시퀀스는 원장 트레이스다(액션에 들어오거나 나가는 원장 주석이 없으면 `NONE` 사용).

첫 세 조건은 일반 인과성 그래프의 인과적 일관성 조건을 모방한다. **Create** 액션이 먼저 오고 소비형 **Exercise** 액션이 마지막에 오도록 보장한다. **Create** 가 없으면 **Enter** 액션이 **Create** 역할을 한다. 넷째 조건은 모든 이전 액션이 컨트랙트의 동기화 지점이도록 보장한다. 원장 트레이스에 관한 마지막 조건은 컨트랙트가 단 하나의 Daml 원장에 거주하고 모든 사용이 거주 원장에서 일어나도록 보장한다. 특히 **Leave** 이후 다음 컨트랙트 액션은 **Enter** 여야 한다.

예컨대 위 이전 액션을 가진 멀티원장 인과성 그래프는 `c`에 대해 멀티원장 일관된다. 특히 `c`의 액션에 단 하나의 극대 사슬이 있다:

> **Create** `c` -> `tf1` -> **ExeN** `B` `c` `ch1` -> `tf2` -> **ExeN** `B` `c` `ch2` -> `tf3` -> **ExeN** `B` `c` `ch3`,

그리고 각 간선 `act1 -> act2`에 대해 `act1`의 나가는 원장 색이 `act2`의 들어오는 원장 색과 같다. 극대 사슬로 제한하는 것은 어떤 노드도 건너뛰지 않도록 보장한다. 예컨대 (비극대) 사슬

> **Create** `c` -> **ExeN** `B` `c` `ch1` -> `tf2` -> **ExeN** `B` `c` `ch2` -> `tf3` -> **Exe** `B` `c` `ch3`

은 **Create** 액션의 나가는 원장(노란색)이 `ch1`에 대한 비소비형 **Exercise** 액션의 들어오는 원장(녹색)과 같지 않으므로 원장 트레이스가 아니다. 따라서 `tf1` 정점 없는 부분그래프는 멀티원장 인과성 그래프여도 `c`에 대해 멀티원장 일관되지 않는다.

> **정의 «멀티원장 인과성 그래프의 일관성»**: `X`를 멀티원장 인과성 그래프 `G`의 액션 부분집합이라 하자. `G`가 `X` 내 모든 컨트랙트 `c`의 액션 집합에서 멀티원장 일관되면 `G`는 `X`에 대해 **멀티원장 일관**(또는 `X`-멀티원장 일관)된다. `G`가 `G`의 모든 액션에서 멀티원장 일관되면 **멀티원장 일관**된다.

> **참고:** 컨트랙트 키에 대한 멀티원장 일관성 요구는 아직 없다. 따라서 상호운용성은 참조하는 컨트랙트에서 오는 것 외의 일관성 보장을 제공하지 않는다. 특히 컨트랙트 키는 고유할 필요가 없고 **NoSuchKey** 액션은 컨트랙트 키가 미할당인지 확인하지 않는다.

분할 페인트 카운터오퍼 워크플로의 멀티원장 인과성 그래프는 멀티원장 일관된다. 특히 컨트랙트의 모든 극대 액션 사슬이 원장 트레이스다:

| 컨트랙트 | 극대 사슬 |
| --- | --- |
| `Iou Bank A` | **Create** -> **Fetch** -> **Exercise** |
| `ShowIou A P Bank` | **Create** -> **Exercise** |
| `Counteroffer A P Bank` | **Create** -> **Exercise** |
| `Iou Bank P` | **Create** |
| `PaintAgree P A` | **Create** |

### 최소성과 축소

`X`-멀티원장 일관 인과성 그래프에 비순환·전이적 닫힘을 유지하며 간선을 추가하면, 결과 그래프도 다시 `X`-멀티원장 일관된다. 따라서 최소 일관·축소 개념이 일반 인과성 그래프에서 그에 맞게 일반화된다.

> **정의 «최소 멀티원장 일관 인과성 그래프»**: `X`-멀티원장 일관 인과성 그래프 `G`는 `G`의 어떤 진부분그래프(같은 정점, 더 적은 간선)도 `X`-멀티원장 일관 인과성 그래프가 아니면 `X`-**최소** 다. `X`가 `G`의 모든 액션이면 생략.

> **정의 «멀티원장 일관 인과성 그래프의 축소»**: `X`-멀티원장 일관 인과성 그래프 `G`에 대해, 같은 정점과 `G`의 부분집합인 간선을 가진 고유한 최소 `X`-멀티원장 일관 인과성 그래프 `reduceX(G)`가 존재한다. `reduceX(G)`를 `G`의 `X`-**축소** 라 한다.

멀티원장 인과성 그래프가 비순환이므로 정점을 위상 정렬할 수 있고, 결과 목록은 모든 정점이 모든 이후 정점에 나가는 간선을 갖는 다시 인과성 그래프다. 원래 그래프가 `X`-일관되면, 위상 정렬도 그러하다.

### 멀티원장 인과성 그래프에서 원장으로

멀티원장 인과성 그래프 `G`는 위상 정렬과 축소를 통해 Daml 원장 모델의 원장 `L`에 연결된다.

* 멀티원장 인과성 그래프 `G`가 주어지면, 들어오는·나가는 원장 주석과 모든 이전 정점을 버리고, 트랜잭션 정점을 위상 정렬하고, 결과 트랜잭션 목록을 요청자로 확장해 커밋 시퀀스 `L`을 얻는다.
* 커밋 시퀀스 `L`이 주어지면, 트랜잭션을 정점으로 쓰고 시퀀스에서 `tx1`의 커밋이 `tx2`의 커밋에 선행할 때마다 `tx1`에서 `tx2`로 간선을 추가한다. 그다음 필요에 따라 이전 정점과 들어오는·나가는 원장 주석을 추가하고 트랜잭션 정점에 간선으로 연결한다.

이 연결은 일관성을 일정 정도만 보존한다. 즉, 멀티원장 인과성 그래프가 컨트랙트 `c`에 대해 멀티원장 일관되면 해당 원장도 컨트랙트 `c`에 대해 일관된다. 그러나 멀티원장 일관 인과성 그래프는 키 일관성이 위반될 수 있어 일관된 원장을 산출하지 않는다. 반대로, 일관된 원장은 들어오는·나가는 원장 주석을 말하지 않으므로 주석이 일관됨을 강제할 수 없다.

## 원장 인지 투영 (Ledger-aware Projection)

참여자 노드는 호스팅하는 각 파티에 대해 로컬 원장을 유지하고 업데이트 서비스는 이 로컬 원장의 위상 정렬을 출력한다. 참여자 노드가 여러 원장에서 파티를 호스팅하면, 이 로컬 원장은 멀티원장 인과성 그래프다. 이 절은 그런 로컬 원장을 산출하는 멀티원장 인과성 그래프의 원장 인지 투영을 정의한다.

> **정의 «Y-레이블 액션»**: 들어오는·나가는 원장 주석을 가진 액션은 그 들어오거나 나가는 원장 주석이 집합 `Y`의 원소면 `Y`에 대해 **Y-레이블** 된다.

> **정의 «트랜잭션의 원장 인지 투영»**: `Y`를 Daml 원장 집합, `tx`를 액션이 들어오는·나가는 원장으로 주석된 트랜잭션이라 하자. `Act`를 파티 `P`가 인포미인 `tx`의 `Y`-레이블 하위액션 집합이라 하자. `P`에 대한 `tx`의 `Y`에서의 **원장 인지 투영**(`Y`에서의 `P`-투영)은 `Act`의 (하위액션 관계 기준) 모든 극대 원소를 실행 순서로 구성한다.

> **참고:** 모든 액션은 그 모든 하위액션을 담는다. 따라서 `act`가 `tx`의 `Y`에서의 `P`-투영에 포함되면, `act`의 모든 하위액션도 투영의 일부다. 그런 하위액션 `act'`는 자신은 `Y`-레이블이 아닐 수 있다, 즉 다른 원장에 속할 수 있다. `P`가 `act'`의 인포미면, 참여자 노드는 아래 설명하듯 `act'`를 `P`의 트랜잭션 스트림에서 단지 목격된 것으로 표시한다.

분할 페인트 카운터오퍼 워크플로의 크로스-도메인 트랜잭션은 예컨대 `Iou` 원장(노란색)과 페인팅 원장(녹색)에서 Alice와 페인터에 대해 다음 투영을 갖는다. 여기서 녹색 원장 투영은 투영이 하위액션을 포함하므로 노란색 원장의 액션을 포함한다.

<img src="https://mintcdn.com/cantonfoundation/zmlOjLpKuDjnaObr/images/docs_website/projecting-transactions-paint-offer-ledger-aware.svg?fit=max&auto=format&n=zmlOjLpKuDjnaObr&q=85&s=9545c405bf28aaf0d8098af837f2e42a" style="width: 60%;" alt="분할 페인트 카운터오퍼 워크플로의 파티별 투영" width="660" height="1100" />

> **정의 «이전 액션의 투영»**: `act`를 들어오는 원장 그리고/또는 나가는 원장으로 주석된 이전 액션이라 하자. 원장 집합 `Y`에서의 `act`의 **투영** 은 `Y`에 없는 주석을 `act`에서 제거한다. 투영이 모든 주석을 제거하면 비어 있다.
> 파티 `P`에 대한 `Y`에서의 `act`의 **투영**(`Y`에서의 `P`-투영)은 `P`가 컨트랙트의 이해관계자면 `Y`에서의 `act`의 투영이고, 그렇지 않으면 비어 있다.

> **정의 «파티에 대한 멀티원장 일관성»**: 멀티원장 인과성 그래프 `G`는 `G`가 `P`가 이해관계자 인포미인 `G`의 `Y`-레이블 액션 집합에서 멀티원장 일관되면 원장 집합 `Y`에서 **파티 `P`에 대해 일관**(`Y`에서 `P`-일관)된다.

`X`-최소성과 `X`-축소 개념은 원장 집합 `Y`의 파티 `P`로 그에 맞게 확장된다.

> **정의 «멀티원장 인과성 그래프의 원장 인지 투영»**: `G`를 멀티원장 일관 인과성 그래프, `Y`를 Daml 원장 집합이라 하자. 파티 `P`에 대한 `Y`에서의 `G`의 **투영**(`Y`에서의 `P`-투영)은 다음 인과성 그래프 `G'`(`Y`에서 `P`-일관)의 `Y`에서의 `P`-축소다:
> * `G'`의 정점은 `Y`에서 `P`로 투영된 `G`의 정점이며, 빈 투영은 제외.
> * `G'`에서 두 정점 `v1`과 `v2` 사이에 간선이 있으려면 `v1`에 대응하는 `G`-정점에서 `v2`에 대응하는 `G`-정점으로 간선이 있어야 함.

`G`가 멀티원장 일관 인과성 그래프면, `Y`에서의 `P`-투영도 `Y`에서 `P`-일관된다.

예컨대 분할 페인트 카운터오퍼 워크플로의 멀티원장 인과성 그래프는 다음과 같이 투영된다:

<img src="https://mintcdn.com/cantonfoundation/QAGFSphBsRkeZIBi/images/docs_website/counteroffer-causality-ledgeraware-projection.svg?fit=max&auto=format&n=QAGFSphBsRkeZIBi&q=85&s=56332b2eb0f3b2c26fdf386b3b4fb024" style="width: 100%;" alt="분할 페인트 카운터오퍼 워크플로의 파티별 원장 인지 투영" width="1452" height="2389" />

강조할 점:

* Alice의 녹색 원장 투영에서, Alice는 자기 `Iou`의 보관을 목격한다. 아래 Ledger API 순서 보장에서 설명하듯, **Exercise** 액션은 Alice를 녹색 원장에서 호스팅하지만 노란색 원장에서는 호스팅하지 않는 참여자 노드의 트랜잭션 스트림에서 단지 목격된 것으로 표시된다. 유사하게 페인터는 페인터의 녹색 원장 투영에서 자기 `Iou`의 **Create** 를 단지 목격한다.
* 페인터의 투영에서, `ShowIou` 트랜잭션 `tx3`은 일반 인과성 그래프처럼 `tx4`의 `CounterOffer` 수락에 대해 순서가 없다. 간선 `tx3 -> tx4`는 투영 중 축소 단계로 제거된다.

이전 액션의 투영은 선형 멀티원장 인과성 그래프로 설명할 수 있다. 노란색·녹색 원장에서의 `A`-투영은 다음과 같다. 흰색은 이전 액션이 들어오거나 나가는 원장 주석을 갖지 않음을 나타낸다. 즉, **Leave** 액션은 오른쪽이 흰색이고 **Enter** 액션은 왼쪽이 흰색이다.

<img src="https://mintcdn.com/cantonfoundation/zmlOjLpKuDjnaObr/images/docs_website/transfer-projection.svg?fit=max&auto=format&n=zmlOjLpKuDjnaObr&q=85&s=08e1311acdd7eadfa8f1cd145f8c6ccc" style="width: 100%;" alt="녹색 또는 노란색 원장만 보이는 인과성 그래프" width="1464" height="451" />

## Ledger API 순서 보장

업데이트 서비스와 상태 서비스는 참여자 노드가 파티에 대해 유지하는 로컬 원장에서 도출된다. `Y`를 참여자 노드가 파티를 호스팅하는 원장 집합이라 하자. 트랜잭션 트리 스트림은 다음 수정과 함께 `Y`에서의 파티 로컬 원장의 위상 정렬을 출력한다:

1. 들어오는 또는 나가는 원장 주석 중 하나를 가진 **Transfer** 액션은 **Enter** 와 **Leave** 이벤트로 출력된다. 들어오는·나가는 원장 주석을 모두 가진 **Transfer** 액션은 생략된다.
2. 들어오는·나가는 원장 주석은 출력되지 않는다. `Y`에 없는 들어오거나 나가는 원장 주석을 가진 트랜잭션 액션은 파티가 그 액션의 인포미면 단지 목격된 것으로 표시된다.
3. **Fetch** 노드와 **NoSuchKey** 는 생략된다.

플랫 트랜잭션 스트림은 트랜잭션 트리 스트림의 트랜잭션 트리에서 파티가 영향받는 컨트랙트의 이해관계자이고 단지 목격된 것으로 표시되지 않은 **Create**, 소비형 **Exercise**, **Enter**, **Leave** 액션에 대응하는 `CreatedEvent`, `ArchivedEvent`, **Enter**, **Leave** 액션을 정확히 담는다.

유사하게, 상태 서비스는 플랫 트랜잭션 스트림에 따라 반환된 오프셋에 활성인 컨트랙트 집합을 제공한다. 즉, 트랜잭션 이벤트 스트림의 모든 이벤트의 컨트랙트 상태 변경이 제공된 컨트랙트 집합에 반영된다.

단일 Daml 원장의 순서 보장이 그에 맞게 확장된다. 특히 상호운용성은 모든 로컬 원장이 위에서 기술한 대로 Daml 원장 모델에 연결되는 가상 공유 멀티원장 인과성 그래프의 투영임을 보장한다. 따라서 원장 유효성 보장이 로컬 원장을 통해 Ledger API로 확장된다.

<!-- nav:start -->

---

⬅️ **이전**: [인과성과 시간 (Causality and Time)](ledger-causality.md) ・ ➡️ **다음**: [순서화 합의 (Ordering Consensus)](ordering-consensus.md)

<!-- nav:end -->
