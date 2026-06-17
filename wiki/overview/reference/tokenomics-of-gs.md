---
title: 글로벌 Synchronizer의 토크노믹스
source: https://docs.canton.network/overview/reference/tokenomics-of-gs
translated: 2026-06-15
status: done
tags: [overview, reference, 토크노믹스]
---

> **출처(원문)**: [Tokenomics of the Global Synchronizer](https://docs.canton.network/overview/reference/tokenomics-of-gs) · 번역일 2026-06-15

## 📌 개발자 노트
- **한 줄 요약**: <abbr class="gloss" title="슈퍼 밸리데이터들이 공동 운영하는 Canton의 퍼블릭 조율(합의) 계층">글로벌 Synchronizer</abbr>를 지탱하는 경제 모델 — 소각-발행 균형(burn-mint equilibrium), <abbr class="gloss" title="Synchronizer에 쓰기를 요청할 때 소비하는 자원. Canton Coin으로 비용을 지불">트래픽</abbr> 경제(무료 베이스 + 유료 추가), 보상 분배(5개 활동 레코드), 발행 곡선, 수수료·라운드 스냅숏, CC-USD 환율, <abbr class="gloss" title="파티를 호스팅하고 그 파티의 컨트랙트 데이터를 저장하는 참여자 노드">밸리데이터</abbr> 수익 방식.
- **핵심 용어**: 소각-발행 균형, <abbr class="gloss" title="Canton Coin(CC)의 Daml/Scan상 기술적 이름. CC = Amulet">Amulet</abbr>Rules, burstAmount/burstWindow, RewardCoupon, OpenMiningRound, amuletPrice
- **선행 개념**: [Canton Coin](../understand/canton-coin.md), [Canton Coin 토크노믹스](canton-coin-tokenomics.md).

---

# 글로벌 Synchronizer의 토크노믹스

> 글로벌 <abbr class="gloss" title="상태를 저장하지 않고 트랜잭션 합의·순서를 조율하는 Canton 구성요소">Synchronizer</abbr>를 지탱하는 경제 모델: 트래픽 수수료, 보상 분배, 발행, CC-USD 환율

<abbr class="gloss" title="트랜잭션 수수료와 밸리데이터 보상에 쓰이는 네이티브 유틸리티 토큰(CC)">Canton Coin</abbr>(CC)은 글로벌 Synchronizer의 경제 엔진이다. 밸리데이터, <abbr class="gloss" title="글로벌 Synchronizer를 운영하고 네트워크 거버넌스에 참여하는 노드">슈퍼 밸리데이터</abbr>, 애플리케이션 제공자는 네트워크에 인프라와 활동을 기여해 CC를 번다. 사용자는 Synchronizer 트래픽을 구매하기 위해 CC를 (소각해) 쓴다. 그 결과인 소각-발행 균형(burn-mint equilibrium)이 토큰의 가치를 실제 네트워크 유틸리티에 연결한다.

## 소각-발행 균형 (Burn-Mint Equilibrium)

Canton Coin 애플리케이션은 소각-발행 균형 메커니즘을 채택해, Canton Coin이 네트워크 사용자에게 제공하는 내재 가치 부근으로 환율을 안정화하는 것을 목표로 한다:

* **수수료 소각** — 사용자는 Synchronizer 트래픽을 구매할 때 수수료(USD로 표시되지만 Canton Coin을 소각해 지불)를 낸다. 소각된 코인은 유통에서 영구히 제거된다.
* **발행 보상** — 밸리데이터, 슈퍼 밸리데이터, 애플리케이션 제공자는 네트워크 기여(인프라 운영, 애플리케이션 서비스, 사용, 라이브니스)의 대가로 새 CC를 발행(mint)한다.
* **동적 균형** — 장기적으로, 소각된 총 CC(실제 네트워크 유틸리티 반영)는 발행된 CC(미리 정해진 최대 발행 곡선 하에서)와 대략 균형을 이룬다. 사용이 많으면 더 많은 코인이 소각되어 토큰 환율을 올리는 경향이 있고, 사용이 적으면 균형이 회복될 때까지 공급이 늘어난다.

## 트래픽 경제

글로벌 Synchronizer에 제출되는 모든 메시지는 트래픽을 소비한다. 보내는 밸리데이터가 부과되며, 수신자는 부과되지 않는다.

### 베이스 레이트 할당 (무료 등급)

각 밸리데이터는 `AmuletRules` <abbr class="gloss" title="원장에 기록되는 불변 데이터 단위. 상태 변경은 새 컨트랙트 생성으로 표현됨">컨트랙트</abbr>의 두 파라미터로 정의되는 무료·재생성 트래픽 허용량을 받는다:

* `burstAmount` — 밸리데이터가 하나의 버스트 윈도 내에서 수수료 없이 쓸 수 있는 최대 바이트 수.
* `burstWindow` — 버스트 양이 재생성되는 시간 창. 한 윈도 동안 활동이 없으면 무료 잔액이 완전히 복원된다.

베이스 레이트 트래픽이 항상 먼저 소비된다. 그것이 소진될 때만 추가(유료) 트래픽이 차감된다.

### 추가 트래픽 (CC 소각으로 구매)

밸리데이터는 현재 USD-CC 환율(USD/MB 가격)로 CC를 소각해 트래픽 크레딧 잔액을 늘린다. 필요할 때 밸리데이터 운영자(또는 제3자 서비스 제공자)가 CC를 소각해 트래픽 크레딧을 받는다. 소각된 CC는 소각량을 기록하는 `ValidatorRewardCoupon`을 생성하며, 여기서 `user`는 구매 <abbr class="gloss" title="Canton에서 권한과 데이터 가시성의 주체가 되는 식별 가능한 참여 주체">파티</abbr>를 <abbr class="gloss" title="참여자 노드가 파티를 대신해 원장에서 활동(컨트랙트 저장·트랜잭션 제출·확인)해 주는 것. 로컬 파티는 키까지 노드가 관리하고, 외부 파티는 제출 키를 파티 자신이 보유(노드는 중계)">호스팅</abbr>하는 밸리데이터 운영자다. 트래픽 구매에 대해서는 `AppRewardCoupon`이 생성되지 않는다.

밸리데이터가 예기치 않게 트래픽을 소진하지 않도록 자동 충전 자동화가 제공된다. `minTopupAmount` 파라미터는 각 구매가 슈퍼 밸리데이터의 처리 비용을 상각할 만큼 충분히 크도록 보장한다.

트래픽 회계는 밸리데이터별이다 — 같은 밸리데이터에 호스팅된 모든 파티가 하나의 트래픽 잔액을 공유한다. 밸리데이터가 <abbr class="gloss" title="키를 파티 주인이 직접 보관하고 거래마다 외부 서명하는 파티(=자기수탁). '외부'는 노드 시점 — 키가 노드 밖에 있음">외부 파티</abbr>를 호스팅하면 그들을 대신해 트래픽을 구매한다. <abbr class="gloss" title="네트워크의 공개 통계·활동을 보여주는 익스플로러(블록 익스플로러의 Canton판)">Scan</abbr> API는 밸리데이터가 외부 파티가 제출한 <abbr class="gloss" title="원장 상태를 바꾸는 원자적 작업 단위. 하나 이상의 컨트랙트를 생성·보관하며, 전부 적용되거나 전혀 적용되지 않음">트랜잭션</abbr>의 비용을 추정하는 데 쓸 수 있는 트래픽 가격 파라미터를 제공한다.

### 비용 요인

특정 메시지에 대해 밸리데이터 잔액에서 차감되는 실제 트래픽은 다음에 좌우된다:

* **페이로드 크기** — 시퀀싱된 메시지의 바이트 크기.
* **수신자 수** — 각 수신자는 `readVsWriteScalingFactor`(베이시스 포인트로 지정)로 통제되는 전달 추가요금을 더한다. 예컨대 계수 4에서, 수신자 10명인 1 MB 메시지의 비용은 `1,000,000 * (1 + 10 * 0.004) = 1,040,000`바이트다.
* **추가 트래픽 가격** — MB당 USD의 `extraTrafficPrice`로, 현행 환율의 CC로 부과된다.

이 모든 파라미터는 `AmuletRules` 컨트랙트에 존재하며 Scan API로 조회할 수 있다.

## 보상 분배

네트워크 활동은 **활동 레코드(activity records)** 로 추적되며, 각각은 주어진 라운드의 CC 발행에서 파티의 몫을 결정하는 가중치를 갖는다. 다섯 가지 핵심 컨트랙트 <abbr class="gloss" title="컨트랙트의 구조와 규칙(권한·초이스)을 정의하는 Daml 청사진">템플릿</abbr>이 회계를 구동한다:

* **`SvRewardCoupon`** — 라운드당 슈퍼 밸리데이터당 하나. SV 발행 권한은 SV 인프라 운영이나 핵심 자원 기여의 대가로 토크노믹스 위원회가 [CIP 절차](https://github.com/global-synchronizer-foundation/cips/blob/main/cip-0000/cip-0000.md)를 통해 부여한다.
* **`ValidatorRewardCoupon`** — CC가 소각되거나(트래픽 구매) `AmuletRules_Transfer`가 실행될 때마다 생성. 쿠폰의 가중치는 밸리데이터가 소각한 CC 양을 반영한다.
* **`ValidatorLivenessActivityRecord`** — 라운드당 라이브 밸리데이터당 하나. 트랜잭션을 검증·<abbr class="gloss" title="이해관계자 밸리데이터가 트랜잭션이 유효함을 미디에이터에 응답하는 것(confirmation)">확인</abbr>할 수 있게 가용한 데 대해 밸리데이터에 보상하고, 온보딩 후 추가 트래픽 구매를 위한 초기 자금을 제공한다.
* **`AppRewardCoupon`** — 피처드 애플리케이션의 트랜잭션이 성공하거나 `FeaturedAppActivityMarker`가 SV 자동화에 의해 변환될 때 생성. 피처드 애플리케이션만 보상을 받는다([CIP-0078](https://github.com/global-synchronizer-foundation/cips/blob/main/cip-0078/cip-0078.md)에 따라).
* **`FeaturedAppActivityMarker`** — 경제적으로 의미 있는 이벤트(자산 이전, 토큰 발행/소각)에 대해 비즈니스 트랜잭션에서 생성. SV 자동화가 이를 `AppRewardCoupon` 컨트랙트로 변환한다.

## 발행 곡선과 발행 일정

`AmuletRules` 컨트랙트의 `IssuanceConfig`는 발행될 수 있는 최대 CC를 정의한다. 핵심 필드는:

* `amuletToIssuePerYear` — 새 CC 발행의 연간 상한. 라운드당 발행은 이 수를 연간 라운드 수로 나눠 도출된다(라운드는 기본적으로 10분마다 시작하므로 연간 약 52,560 라운드).
* `validatorRewardPercentage` — 라운드당 발행 중 밸리데이터 활동 보상(소각 비례 쿠폰과 라이브니스 포셋)에 할당되는 비율.
* `appRewardPercentage` — 애플리케이션 보상에 할당되는 비율.
* 밸리데이터·앱 분량(tranche) 이후의 나머지는 슈퍼 밸리데이터 보상으로 가며, 각 SV의 가중치에 비례해 분배된다.

각 분량 내에서 쿠폰당 발행은 상한이 있다(`validatorRewardCap`, `featuredAppRewardCap`, `unfeaturedAppRewardCap`, `validatorFaucetCap`). 한 분량의 총 쿠폰 수요가 상한 미만이면 잉여는 다음 분량으로 흐른다 — 예컨대 미청구 밸리데이터 활동 보상은 밸리데이터 라이브니스 포셋으로, 미청구 비피처드 앱 보상은 피처드 앱 보상으로 흐른다. 모든 분량을 넘어선 미청구 보상은 SV 보상으로 간다.

`developmentFundPercentage`(기본 5%)는 위 분량들로 나누기 전에 각 라운드 발행에서 [CIP-0082](https://github.com/global-synchronizer-foundation/cips/blob/main/cip-0082/cip-0082.md)에 따른 개발 기금을 위해 따로 떼어둔다.

## 수수료 스케줄과 라운드 스냅숏

수수료 파라미터는 **`AmuletRules`** 컨트랙트에 저장되며, <abbr class="gloss" title="탈중앙 Synchronizer 운영(Decentralized Synchronizer Operations) 파티. 슈퍼 밸리데이터들의 공동 거버넌스 주체">DSO</abbr>가 <abbr class="gloss" title="원장(Daml 컨트랙트) 위에서 실행·기록되는 것. 모든 이해관계자가 공유·검증·강제">온-원장</abbr> 투표로 거버넌스한다. 새 <abbr class="gloss" title="CC가 발행·정산되는 시간 단위. 열림→발행중→닫힘으로 진행되며 라운드마다 기여 비례 보상">마이닝 라운드</abbr>가 열리면, 현재 수수료 값과 환율이 **`OpenMiningRound`** 컨트랙트로 스냅숏되어 그 라운드 내 모든 트랜잭션이 일관된 가격을 쓰게 한다. 라운드가 단계를 거치며, **`IssuingMiningRound`** 컨트랙트가 각 보상 유형에 대한 활동 가중치당 발행량을 기록한다.

[CIP-0078](https://github.com/global-synchronizer-foundation/cips/blob/main/cip-0078/cip-0078.md)은 CC 이전과 잠금에 대한 거의 모든 수수료를 없앴다. 보유 수수료(holding fee)는 남는다 — 코인 양과 무관하게 별도 코인 컨트랙트(UTXO)당 단위 시간당 고정 수수료다. 보유 수수료는 온-<abbr class="gloss" title="거래·컨트랙트가 기록되는 장부. Canton에선 활성 컨트랙트의 모음">원장</abbr> 저장을 줄이기 위해 작은 코인을 병합하도록 유도한다. 이전 중이 아니라 `Amulet_Expire`를 통해 만료된 코인 컨트랙트에만 부과된다.

## CC-USD 환율

각 슈퍼 밸리데이터는 자신이 적절하다고 보는 CC 환율을 공표한다. 각 마이닝 라운드에 쓰이는 환율은 모든 공표된 SV 환율의 **중앙값(median)** 이다. 이 중앙값 기반 방식은 어떤 단일 SV도 일방적으로 가격을 옮기지 못하게 막는다.

그 결과인 `amuletPrice`(CC당 USD)는 각 `OpenMiningRound` 컨트랙트에 기록되며 Scan API나 Scan UI로 조회할 수 있다. 모든 USD 표시 수수료(트래픽 비용, 보상 상한)는 적용 시 이 환율로 CC로 변환된다.

## 밸리데이터가 버는 방법

밸리데이터는 매 라운드 실행되는 두 메커니즘으로 CC를 번다:

* **라이브니스 보상** — 각 라이브 밸리데이터는 `ValidatorLivenessActivityRecord`를 생성해 밸리데이터 포셋 분량의 몫을 번다. 밸리데이터당 포셋 상한은 라운드당 $2.85 USD 상당이 기본이다. 라이브니스 보상은 새 밸리데이터에게 트래픽 구매 자금이 될 초기 CC를 준다.
* **활동 보상** — 밸리데이터의 사용자가 CC를 소각하면(트래픽 구매나 이전), 그 결과인 `ValidatorRewardCoupon`이 밸리데이터에게 소각량에 비례해 CC를 발행할 권한을 준다. 더 많은 네트워크 사용을 이끄는 밸리데이터가 더 많이 번다.

외부 파티(밸리데이터를 통하지 않고 자기 키로 서명하는 파티)를 호스팅하는 밸리데이터의 경우, 발행은 밸리데이터로의 **발행 위임(minting delegation)** 을 통하거나 매 라운드 `AmuletRules_Transfer`를 호출하는 커스텀 자동화를 통해 처리될 수 있다. [CIP-0073](https://github.com/global-synchronizer-foundation/cips/blob/main/cip-0073/cip-0073.md)은 SV가 결정한 파티에 대한 가중 밸리데이터 라이브니스 보상을 설명한다.

## 더 읽기

* [Canton Coin 백서](https://www.digitalasset.com/hubfs/Canton%20Network%20Files/Documents%20(whitepapers%2c%20etc...)/Canton%20Coin_%20A%20Canton-Network-native%20payment%20application.pdf) — 소각-발행 메커니즘의 전체 기술 명세
* [Canton Network 백서](https://www.digitalasset.com/hubfs/Canton/Canton%20Network%20-%20White%20Paper.pdf) — 더 넓은 네트워크 아키텍처와 설계
* [CIP 저장소](https://github.com/global-synchronizer-foundation/cips) — 수수료·보상 변경을 포함한 거버넌스 제안

<!-- nav:start -->

---

⬅️ **이전**: [Synchronizer 개요](synchronizer-overview.md) ・ ➡️ **다음**: [토폴로지 (Topology)](topology.md)

<!-- nav:end -->
