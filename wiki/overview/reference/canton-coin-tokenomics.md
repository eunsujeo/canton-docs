---
title: Canton Coin 토크노믹스
source: https://docs.canton.network/overview/reference/canton-coin-tokenomics
translated: 2026-06-15
status: done
tags: [overview, reference, 토크노믹스, CantonCoin]
---

> **출처(원문)**: [Canton Coin Tokenomics](https://docs.canton.network/overview/reference/canton-coin-tokenomics) · 번역일 2026-06-15

## 📌 개발자 노트
- **한 줄 요약**: CC 수수료 구조(트래픽·보유 수수료), 마이닝 라운드(5단계)·활동 레코드(5개 <abbr class="gloss" title="컨트랙트의 구조와 규칙(권한·초이스)을 정의하는 Daml 청사진">템플릿</abbr>), 소각-발행 균형, 외부 <abbr class="gloss" title="Canton에서 권한과 데이터 가시성의 주체가 되는 식별 가능한 참여 주체">파티</abbr> 발행, UTXO 모델·더스트 만료, CN 토큰 표준(CIP-0056)의 기술 레퍼런스.
- **핵심 용어**: Amulet, AmuletRules/OpenMiningRound/IssuingMiningRound, 활동 레코드·가중치, 보유 수수료(holding fee), 피처드 앱, UTXO 더스트 만료
- **선행 개념**: [Canton Coin](../understand/canton-coin.md), [GS 토크노믹스](tokenomics-of-gs.md).

---

# Canton Coin 토크노믹스

<abbr class="gloss" title="트랜잭션 수수료와 밸리데이터 보상에 쓰이는 네이티브 유틸리티 토큰(CC)">Canton Coin</abbr>(CC)은 <abbr class="gloss" title="슈퍼 밸리데이터들이 공동 운영하는 Canton의 퍼블릭 조율(합의) 계층">글로벌 동기화자</abbr>의 네이티브 유틸리티 토큰이다. [Splice](https://github.com/canton-network/splice) 오픈소스 인프라를 통해 구현되며, <abbr class="gloss" title="다자간 워크플로를 위해 설계된 Canton의 스마트 컨트랙트 언어">Daml</abbr> <abbr class="gloss" title="원장에 기록되는 불변 데이터 단위. 상태 변경은 새 컨트랙트 생성으로 표현됨">컨트랙트</abbr> 수준에서는 "Amulet"이라 불린다. CC는 세 기능을 한다: 네트워크 사용료(트래픽) 지불, 인프라 운영자·애플리케이션 제공자 보상, <abbr class="gloss" title="글로벌 동기화자를 운영하고 네트워크 거버넌스에 참여하는 노드">슈퍼 밸리데이터</abbr> 참여를 통한 네트워크 거버넌스.

CC의 네트워크 내 역할과 획득 방법에 대한 배경은 [Canton Coin과 글로벌 동기화자](../understand/canton-coin.md)를 참고하라. [Canton Coin 백서](https://www.digitalasset.com/hubfs/Canton%20Network%20Files/Documents%20(whitepapers%2c%20etc...)/Canton%20Coin_%20A%20Canton-Network-native%20payment%20application.pdf)가 전체 형식 명세를 제공한다.

## 수수료 구조

CC는 세 가지 수수료 유형이 있었다. [CIP-0078](https://github.com/global-synchronizer-foundation/cips/blob/main/cip-0078/cip-0078.md)에 따라 이전 수수료와 잠금 수수료가 제거되어, 트래픽 수수료와 보유 수수료가 두 활성 메커니즘으로 남는다.

### 트래픽 수수료

트래픽 크레딧은 양도 불가다. CC가 트래픽으로 변환되면 트랜잭션 제출 비용에만 쓸 수 있다. <abbr class="gloss" title="파티를 호스팅하고 그 파티의 컨트랙트 데이터를 저장하는 참여자 노드">밸리데이터</abbr>의 트래픽 예산이 소진되면 트랜잭션이 실패한다. 자동 충전 자동화가 제공되며 권장된다.

> **참고:** 소비되는 컨트랙트의 경합으로 확인 요청이 실패해도 트래픽 크레딧은 소비된다 — 예컨대 두 이전이 같은 코인 컨트랙트를 소비하려 할 때.

### 보유 수수료 (Holding Fees)

Canton Network 토크노믹스는 *활동 레코드(Activity Record)* 에 기반한다. 활동 레코드는 네트워크에 가치를 제공하는 동작을 수행한 파티를 식별한다. 활동 레코드는 *가중치(weight)* 를 가지며, 이는 그 활동 레코드와 연관된 CC 발행의 상대적 몫이다.

활동 레코드를 생성하는 것과 연관된 CC를 발행하는 것은 두 별개 단계다. 생성·발행 단계는 다섯 단계를 가진 *라운드(round)* 라 부르는 사이클로 수행된다. 첫 단계에서 그 라운드의 수수료 값이 원장에 기록된다(수수료는 Scan State API로 얻을 수 있다). 두 번째 단계는 *활동 기록(activity recording)* 으로, 활동 레코드가 생성되는 때다; 이 단계에 생성된 레코드는 그 라운드에 속한다. 다음 단계는 각 종류의 활동 레코드에 대한 [활동 가중치당 CC 발행량](https://github.com/canton-network/splice/blob/332e06a7ae9e13fde5bba0bf7dcb059aa36f979e/daml/splice-amulet/daml/Splice/Issuance.daml#L67)을 계산하는데, 이는 그 유형의 활동 레코드에 대해 발행될 수 있는 총 CC의 몫이다. 그 뒤 *발행 단계(minting phase)* 에서 활동 레코드의 소유자가 발행 가중치에 비례해 CC를 발행할 수 있다.

여러 라운드가 동시에 활성이며, 각 라운드는 서로 다른 단계에 있다. 라운드는 10분마다 시작하며, 이는 슈퍼 밸리데이터가 향후 거버넌스 투표로 바꿀 수 있는 구성 파라미터다. 자세한 내용은 CC 백서 참고.

외부 파티든 로컬 파티든 활동 레코드 생성에는 차이가 없지만, 발행 단계에 쓰이는 자동화 지원에는 차이가 있다. 밸리데이터에 온보딩된 로컬 파티의 경우, 밸리데이터 애플리케이션이 모든 활동 레코드를 자동 발행하는 백그라운드 자동화를 실행한다. 외부 파티는 자신이 통제하는 키로 트랜잭션에 서명한다. 따라서 밸리데이터 자동화가 외부 파티를 대신해 직접 발행할 수 없다. 외부 파티에는 두 옵션이 있다:

1. 발행 위임(minting delegation)을 써서 보상 수집을 밸리데이터에 위임 — 커스텀 자동화 구축 불필요.
2. 모든 활동 레코드를 입력으로 하여 라운드당 적어도 한 번 `AmuletRules_Transfer`를 호출하는 커스텀 자동화 개발.

[SV가 결정한 파티에 대한 가중 밸리데이터 라이브니스 보상(CIP-0073)](https://github.com/global-synchronizer-foundation/cips/blob/main/cip-0073/cip-0073.md)이 이 지원 제공을 설명한다.

참고로 토크노믹스에 중요한 흥미로운 템플릿:

* 수수료 스케줄을 저장하는 AmuletRules;
* 라운드 개시 시점의 가격·수수료를 저장하는 OpenMiningRound;
* 활동 가중치당 발행량을 저장하는 IssuingMiningRound.

## 활동 레코드의 종류

네트워크 활동 회계에 관여하는 다섯 핵심 템플릿이 있다:

* 두 템플릿은 애플리케이션 관련:

  > * FeaturedAppActivityMarker
  > * AppRewardCoupon

* 세 템플릿은 애플리케이션을 위한 인프라 제공 관련:

  > * ValidatorRewardCoupon
  > * ValidatorLivenessActivityRecord
  > * SvRewardCoupon

뒤의 넷은 활동 레코드인 반면 `FeaturedAppActivityMarker`는 활동 레코드로 간주되지 않는다. 뒤에서 논하듯, `FeaturedAppActivityMarker`는 슈퍼 밸리데이터가 실행하는 자동화를 통해 `AppRewardCoupon`으로 변환된다. 피처드 CC 이전과 `FeaturedAppActivityMarker`는 둘 다 같은 보상을 생성한다. `FeaturedAppActivityMarker`가 앱 활동 레코드를 생성하는 선호 방식이다.

`FeaturedAppActivityMarker`, `AppRewardCoupon`, `ValidatorRewardCoupon` 컨트랙트는 애플리케이션의 트랜잭션이 성공할 때 생성된다. 일반적으로 애플리케이션은 자기 Daml 코드가 `FeaturedAppActivityMarker` 컨트랙트를 직접 생성하거나 애플리케이션 제공자의 파티를 피처링하는 Daml 모델과 상호작용할 때 보상을 받는다. `ValidatorRewardCoupon`은 `AmuletRules_Transfer`를 호출할 때마다(예: Splice 월렛 UI를 쓴 CC 이전) 또는 CC가 소각될 때 생성된다.

발행 가중치 외에, 애플리케이션의 보상은 그것이 *피처드(featured)* 인지 *비피처드(unfeatured)*(기본 상태)인지에도 좌우된다. CIP-0078이 구현된 후, 피처드 애플리케이션만 보상을 받는다. 피처드 애플리케이션은 약 $1 USD에 상당하는 총 가치의 발행 가중치를 받는다(슈퍼 밸리데이터가 향후 조정할 수 있다).

## 피처드 애플리케이션이 되는 방법

피처드 애플리케이션이 되려면 애플리케이션의 입력인 *애플리케이션 제공자의 파티 ID* 가 필요하다. 그 절차는 [이 양식](https://sync.global/featured-app-request/) 작성으로 시작한다. 요청은 애플리케이션을 검토하고 응답하는 토크노믹스 위원회로 간다. [이 웹페이지](https://lists.sync.global/g/tokenomics/topics)는 추적을 위한 토크노믹스 위원회 주제를 나열한다. [성공한 제출 예시](https://lists.sync.global/g/tokenomics/topic/new_featured_app_request/112787885). 테스트 목적으로 DevNet에서 애플리케이션을 셀프 피처링할 수 있다.

일부 템플릿의 경우, 활동의 귀속을 여러 수혜자(beneficiary) 파티와 공유할 수 있다. 예컨대 피처드 애플리케이션 보상을 각각의 주어진 `weight`에 따라 애플리케이션 제공자와 애플리케이션 사용자 간에 나눌 수 있다. 일반 패턴은:

* 각각 `weight`를 가진 수혜자 목록이 제공된다. 가중치 합은 `1.0`이다.
* 이후 처리가 각 수혜자/가중치 쌍에 대해 별도 컨트랙트를 생성해 컨트랙트의 `beneficiary`와 `weight` 필드를 그에 맞게 설정한다.

수혜자는 다음 절에서 더 논한다.

[CIP-0078](https://github.com/global-synchronizer-foundation/cips/blob/main/cip-0078/cip-0078.md)은 CC 이전·잠금에 대한 거의 모든 수수료를 없애 비피처드 애플리케이션은 더 이상 보상을 받지 않는다. 보유 수수료는 남지만, 코인을 이전의 입력으로 쓸 때는 보유 수수료가 부과되지 않도록 동작이 바뀌었다.

보유 수수료는 코인 양과 무관하게, 별도 코인 컨트랙트(UTXO)당 단위 시간당 고정 수수료다. 더스트(dust) 코인의 병합·제거를 유도해 네트워크 저장 사용을 줄이도록 CC 병합을 촉진한다. 보유 수수료는 코인 이전 시에는 부과되지 않고, `Amulet_Expire` <abbr class="gloss" title="컨트랙트에서 수행 가능한 동작(권한이 부여된 당사자만 실행 가능)">초이스</abbr>를 통해 만료된 코인 컨트랙트에만 명시적으로 부과된다. 코인 컨트랙트(UTXO)는 누적 보유 수수료가 코인 가치보다 커지면 슈퍼 밸리데이터에 의해 만료될 수 있다. 이로써 코인 컨트랙트의 가치가 보유 수수료와 무관하게 일정하므로 보유 수수료 회계가 단순해진다.

보유 수수료가 CC 양당이 아니라 UTXO당이므로, 작은 "더스트" 코인은 가치 대비 더 빨리 수수료를 누적한다. 누적 보유 수수료가 코인 가치를 초과하면 슈퍼 밸리데이터가 컨트랙트를 만료시켜 원장에서 제거할 수 있다. 이는 회계를 단순하게 한다: 코인 컨트랙트의 액면가는 일정하며 누적 수수료로 감소하지 않는다.

### 이전·잠금 수수료 (CIP-0078 이후)

[CIP-0078](https://github.com/global-synchronizer-foundation/cips/blob/main/cip-0078/cip-0078.md)은 CC 이전·잠금에 대한 거의 모든 수수료를 없앴다. 레거시 Amulet 이전, CN 토큰 표준 2단계 이전, 1단계 `TransferPreapproval` 이전 모두 수수료를 부과하지 않는다. 유일한 예외는 피처드 1단계 이전이 여전히 `TransferPreapproval` 컨트랙트를 유지하는 제공자 파티를 위해 `AppRewardCoupon`을 생성한다는 것이다.

## 소각-발행 균형

따라서 CC 공급은 고정이 아니라 동적이다. 최대 발행 곡선이 새 코인이 유통에 들어오는 속도를 제약하고, 트래픽 구매의 소각 이벤트가 코인을 제거한다.

발행 보상은 네 범주의 기여자에게 분배된다:

* **슈퍼 밸리데이터**는 <abbr class="gloss" title="상태를 저장하지 않고 트랜잭션 합의·순서를 조율하는 Canton 구성요소">동기화자</abbr> 노드(시퀀서, 미디에이터, 거버넌스 인프라)를 운영해 발행 권한을 번다.
* **애플리케이션 제공자**는 피처드 애플리케이션을 통해 트랜잭션을 촉진할 때 보상을 번다.
* **밸리데이터**는 자신이 소각하는 수수료에 비례해 발행 권한을 번다. 네트워크는 이를 그 노드가 생성한 활동의 대리 지표로 취급한다.
* **라이브니스 인센티브**는 가동 시간과 준비 상태에 대해 밸리데이터에 보상한다. 밸리데이터가 직접 활동으로 발행 허용량을 다 쓰지 않으면, 일부가 라이브니스 보너스로 할당된다.

## 마이닝 라운드

세 Daml 템플릿이 라운드 생애주기를 구동한다:

* **`AmuletRules`** — 수수료 스케줄 저장
* **`OpenMiningRound`** — 라운드 개시 시점의 가격·수수료 저장
* **`IssuingMiningRound`** — 계산된 활동 가중치당 CC 발행량 저장

### 외부 파티를 위한 발행

로컬 파티의 경우, 밸리데이터 애플리케이션이 모든 활동 레코드를 자동 발행하는 백그라운드 자동화를 실행한다. 외부 파티는 자신이 통제하는 키로 트랜잭션에 서명하므로 밸리데이터 자동화가 그들을 대신해 직접 발행할 수 없다. 외부 파티에는 두 옵션이 있다:

* **발행 위임** — 보상 수집을 밸리데이터에 위임, 커스텀 자동화 회피.
* **커스텀 자동화** — 모든 활동 레코드를 입력으로 하여 라운드당 적어도 한 번 `AmuletRules_Transfer` 호출.

[CIP-0073(SV가 결정한 파티에 대한 가중 밸리데이터 라이브니스 보상)](https://github.com/global-synchronizer-foundation/cips/blob/main/cip-0073/cip-0073.md)이 이 워크플로에 대한 추가 지원을 설명한다.

## 활동 레코드

활동 레코드 귀속은 여러 수혜자 간에 공유될 수 있다. 각 수혜자가 `weight`(합 1.0)를 받고, 시스템이 발행 중 수혜자/가중치 쌍별로 별도 컨트랙트를 생성한다.

## 피처드 vs. 비피처드 애플리케이션

애플리케이션의 보상은 그것이 *피처드* 인지 *비피처드*(기본)인지에 좌우된다. CIP-0078 후, 피처드 애플리케이션만 보상을 받는다. 피처드 애플리케이션은 적격 활동당 약 $1 USD 상당의 총 가치를 가진 발행 가중치를 받는다(슈퍼 밸리데이터가 이 금액을 조정할 수 있다).

`FeaturedAppActivityMarker`가 애플리케이션 활동 레코드를 생성하는 선호 메커니즘이다. `TransferPreapproval`을 통한 피처드 1단계 이전도 제공자 파티를 위해 `AppRewardCoupon`을 생성한다.

피처드 애플리케이션이 되려면 [CF 피처드 앱 요청 양식](https://sync.global/featured-app-request/)으로 요청을 제출하라. 토크노믹스 위원회가 제출을 검토한다; 진행은 [토크노믹스 위원회 주제 페이지](https://lists.sync.global/g/tokenomics/topics)에서 추적된다. DevNet에서는 테스트 목적으로 애플리케이션을 셀프 피처링할 수 있다.

## UTXO 모델과 더스트 만료

CC 보유는 UTXO(미사용 트랜잭션 출력) 모델을 쓴다. 각 코인은 특정 액면가를 가진 개별 `Amulet` 컨트랙트로 원장에 표현된다. 이전은 입력 UTXO를 소비하고 새 출력 UTXO를 생성하며, Bitcoin의 트랜잭션 모델과 유사하지만 프라이버시가 있다 — 잔액은 권한 있는 파티에게만 보이고, 모든 보유의 공개 원장이 없다.

이전이 거스름돈을 만들면(입력이 보내는 금액을 초과), 나머지에 대해 새 UTXO가 생성된다. 시간이 지나면 월렛이 많은 소액 UTXO를 보유하게 될 수 있다.

### 더스트 만료

UTXO당 보유 수수료는 더스트에 대한 자연스러운 정리 메커니즘을 만든다. 수수료가 코인 액면가와 무관하게 컨트랙트당 고정이므로, 0.001 CC 코인과 1000 CC 코인이 단위 시간당 같은 보유 수수료를 누적한다. 따라서 작은 코인이 더 빨리 비경제적이 된다.

UTXO의 누적 보유 수수료가 액면가를 초과하면, 슈퍼 밸리데이터가 `Amulet_Expire` 초이스를 실행해 컨트랙트를 만료시킬 수 있다. 이는 컨트랙트를 원장에서 완전히 제거한다. 사용자는 UTXO 수를 최소화하고 보유 수수료 노출을 줄이기 위해 작은 코인을 큰 것으로 병합하도록 유도된다. Splice 월렛 자동화가 가능할 때 이 병합을 자동 처리한다.

## CN 토큰 표준 (CIP-0056)

[CIP-0056](https://github.com/global-synchronizer-foundation/cips/blob/main/cip-0056/cip-0056.md)은 이전, 잠금, 메타데이터 조회를 포함한 토큰 연산을 위한 Daml 인터페이스 집합인 Canton Network 토큰 표준을 정의한다. Splice 월렛이 CC에 대해 CIP-0056을 구현하며, CC를 프로그래밍적으로 다루는 애플리케이션은 이 표준 인터페이스를 통해 상호작용한다.

CIP-0056 기반 2단계 이전은 다음과 같이 작동한다:

1. 송신자가 원하는 CC 양을 잠가 이전 오퍼를 생성한다.
2. 수신자가 오퍼를 수락하면, CC가 잠금 해제되고 이전이 완료된다.

이 2단계 흐름은 송신자 측 자동화에 의존하지 않으며 외부 파티에 잘 맞는다. CIP-0078 이후 이 연산들은 수수료가 없고 활동 레코드를 생성하지 않는다.

API 상세는 [CIP-0056 텍스트](https://github.com/global-synchronizer-foundation/cips/blob/main/cip-0056/cip-0056.md)와 [토큰 표준 소스 코드](https://github.com/canton-network/splice/tree/main/token-standard#readme)를 참고하라.

## 관련 자원

* [Canton Coin과 글로벌 동기화자](../understand/canton-coin.md) — 개념 개요와 CC 획득 방법
* [CIP-0078 (CC 수수료 제거)](https://github.com/global-synchronizer-foundation/cips/blob/main/cip-0078/cip-0078.md) — 이전·잠금 수수료를 없앤 제안
* [CIP-0056 (CN 토큰 표준)](https://github.com/global-synchronizer-foundation/cips/blob/main/cip-0056/cip-0056.md) — 토큰 연산을 위한 표준 인터페이스
* [CIP-0073 (가중 밸리데이터 라이브니스 보상)](https://github.com/global-synchronizer-foundation/cips/blob/main/cip-0073/cip-0073.md) — SV가 결정한 파티를 위한 라이브니스 보상 지원
* [Canton Coin 백서](https://www.digitalasset.com/hubfs/Canton%20Network%20Files/Documents%20(whitepapers%2c%20etc...)/Canton%20Coin_%20A%20Canton-Network-native%20payment%20application.pdf) — 전체 형식 명세
