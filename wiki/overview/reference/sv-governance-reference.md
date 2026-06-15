---
title: SV 거버넌스 레퍼런스
source: https://docs.canton.network/overview/reference/sv-governance-reference
translated: 2026-06-15
status: done
tags: [overview, reference, 거버넌스, DSO]
---

> **출처(원문)**: [SV Governance Reference](https://docs.canton.network/overview/reference/sv-governance-reference) · 번역일 2026-06-15

## 📌 개발자 노트
- **한 줄 요약**: DSO(<abbr class="gloss" title="글로벌 동기화자를 운영하고 네트워크 거버넌스에 참여하는 노드">슈퍼 밸리데이터</abbr> 집합)의 거버넌스 모델·투표 메커니즘·거버넌스 동작 — BFT 거버넌스(DSO <abbr class="gloss" title="Canton에서 권한과 데이터 가시성의 주체가 되는 식별 가능한 참여 주체">파티</abbr>·온체인 확인·탈중앙 자동화·중앙값 투표), 투표 역할·절차, 거버넌스 동작 유형, 파라미터 거버넌스, CIP 절차, Canton Foundation.
- **핵심 용어**: DSO 파티, 확인 임계값 t=ceil(2n/3), VoteRequest, ARC_DsoRules/ARC_AmuletRules/ARC_AnsEntryContext, 중앙값 투표, BFT
- **선행 개념**: [글로벌 동기화자](../understand/global-synchronizer.md), [CIP 레퍼런스](what-are-cips.md), [탈중앙화](decentralization.md).

---

# SV 거버넌스 레퍼런스

<abbr class="gloss" title="슈퍼 밸리데이터들이 공동 운영하는 Canton의 퍼블릭 조율(합의) 계층">글로벌 동기화자</abbr>는 탈중앙화 <abbr class="gloss" title="상태를 저장하지 않고 트랜잭션 합의·순서를 조율하는 Canton 구성요소">동기화자</abbr> 운영자(DSO)로서 집합적으로 행동하는 슈퍼 <abbr class="gloss" title="파티를 호스팅하고 그 파티의 컨트랙트 데이터를 저장하는 참여자 노드">밸리데이터</abbr>(SV)가 거버넌스한다. 거버넌스 결정은 `splice-dso-governance` 패키지에 정의된 <abbr class="gloss" title="다자간 워크플로를 위해 설계된 Canton의 스마트 컨트랙트 언어">Daml</abbr> <abbr class="gloss" title="원장에 기록되는 불변 데이터 단위. 상태 변경은 새 컨트랙트 생성으로 표현됨">컨트랙트</abbr>를 써서 온체인 투표로 이루어진다.

## DSO 거버넌스 모델

CC, CNS, 글로벌 동기화자 거버넌스는 `f = numSvNodes - t`이고 확인 임계값 `t = ceiling(numSvNodes * 2.0 / 3.0)`일 때 최대 `f`개의 결함이 있거나 부정직한 SV 노드를 허용하도록 탈중앙화 방식으로 구현된다.

이 구현은 비잔틴 장애 허용을 달성하기 위해 세(네) 핵심 기법을 쓴다:

* **DSO 파티**: 확인 임계값 `t`로, 모든 SV 노드에 호스팅되는 DSO 파티라 부르는 탈중앙화 Daml 파티를 설정한다.
* **온체인 확인**: DSO 파티의 이름으로 오프-원장 입력이 있는 <abbr class="gloss" title="컨트랙트에서 수행 가능한 동작(권한이 부여된 당사자만 실행 가능)">초이스</abbr>를 실행하려면 `t`개 SV 노드의 명시적 온체인 확인을 요구한다.
* **탈중앙 자동화**: 모든 SV 노드가 DSO 파티가 실행해야 하는 초이스를 실행하려 시도하는 자동화 코드를 실행한다. 초이스는 오프-원장 입력이 필요 없으면 직접 실행되거나, 필요하면 해당 확인을 생성해 간접 실행된다. 자동화는 목표 시간과 실제 시간 사이의 편차가 평균적으로 제한되도록 초이스를 적시에 실행한다.
* **중앙값 기반 투표**: 환율과 유사 구성 파라미터에 대한 합의는 중앙값 기반 투표로 달성된다. 모든 SV 운영자가 원하는 값을 온체인에 공표하고 DSO 파티가 그 값들의 중앙값을 쓴다.

따라서 `f`개를 넘지 않는 SV 노드가 부정직하다고 가정할 의향이 있는 CC·CNS 사용자는 다음 보장에 의존할 수 있다:

* **유효한 트랜잭션**: DSO 파티의 확인이 필요한 모든 트랜잭션은 [유효하다](../learn/ledger-model.md).
* **적시 자동화**: DSO 파티가 취해야 하는 동작이 적시에 취해진다.
* **예측 가능한 수수료·구성 값**: 수수료와 구성 값은 자기 이익을 위해 행동한다고 가정할 수 있는 ~2/3 SV 운영자의 *집계 선호* 를 나타내므로 합리적으로 예측 가능하다.

유효한 트랜잭션 보장은 CC·CNS 사용자에게 특히 중요하다. 탈중앙 자동화·거버넌스 구현의 관심사를 CC·CNS의 토크노믹스·비즈니스 로직 구현의 관심사와 분리하는 데 쓰이기 때문이다.

`splice-dso-governance`와 `splice-validator-lifecycle` 외의 모든 코드는 DSO 파티가 CC·CNS 애플리케이션의 정직한 제공자로 행동한다는 가정 하에 작성된다. 그 의미를 아래 절에서 정의한다.

탈중앙화 파티를 써서 탈중앙화 관심사를 분리하는 이 접근은 코드를 크게 단순화하고, 패키지 의존성 그래프에 보이는 대로 코드 분할을 가능하게 한다:

<img src="https://mintcdn.com/cantonfoundation/805bfL5zagaL0yiJ/overview/reference/images/daml-package-dependencies.png?fit=max&auto=format&n=805bfL5zagaL0yiJ&q=85&s=f3dd07a1160b603f0771882b48e0ea5a" alt="Daml 패키지 의존성 그래프" width="1712" height="1133" />

DSO는 모든 SV 노드에 걸쳐 호스팅되는 탈중앙화 파티다. 동작이 SV의 초다수(supermajority) 승인을 요구하는 비잔틴 장애 허용(BFT) 확인 모델을 쓴다. 시스템은 최대 `f`개의 결함이 있거나 부정직한 노드를 허용하며, `f = floor((n - 1) / 3)`이고 `n`은 총 SV 수다.

임의의 거버넌스 동작에 필요한 투표 수는:

```
requiredNumVotes = ceiling((numSVs + f + 1) / 2)
```

이 임계값은 두 속성을 보장한다: **무결성**(부정직한 소수가 동작을 밀어붙일 수 없음)과 **가용성**(최대 `f`개의 기권 SV가 진전을 막을 수 없음).

## 거버넌스 역할

어떤 SV든 온체인에 `VoteRequest`를 생성해 거버넌스 동작을 제안할 수 있다. 다른 모든 SV가 그 요청에 투표(수락 또는 거부)할 수 있다. 투표 임계값이 충족되면, [CIP-0064](https://github.com/canton-foundation/cips/blob/main/cip-0064/cip-0064.md)에 기술된 위임 없는(delegateless) 자동화를 통해 어떤 SV든 동작을 실행할 수 있어, 지정된 DSO 위임자가 필요 없다.

확인이 필요한 동작에는 두 실행 경로가 있다:

* **투표 동작(Voted actions)** — 어떤 SV가 투표 요청을 생성하고; 다른 SV가 수락/거부 투표로 응답한다. `requiredNumVotes`개의 수락 투표가 모이면 동작이 실행된다.
* **자동 확인(Automated confirmations)** — 일상적 운영 동작(예: 마이닝 라운드 진행)의 경우, 각 SV 노드가 전제 조건이 충족되면 자동으로 확인을 생성한다. 충분한 확인이 쌓이면 수동 투표 없이 실행이 진행된다.

## 투표 메커니즘

투표 요청은 DSO 원장의 `VoteRequest` Daml 컨트랙트로 표현된다. 각 요청은 제안된 `ActionRequiringConfirmation`, `voteBefore` 데드라인, 예약된 동작을 위한 선택적 `targetEffectiveAt` 타임스탬프를 명시한다.

투표는 다음으로 해소된다:

* **Accepted** — 적어도 `requiredNumVotes`개 SV가 수락에 투표. 동작이 온체인 실행됨.
* **Rejected** — 적어도 `requiredNumVotes`개 SV가 거부에 투표. 요청이 보관됨.
* **Expired** — 어느 방향으로도 충분한 투표 없이 `voteBefore` 데드라인이 지남.

`targetEffectiveAt` 날짜가 있는 투표 요청의 경우, 임계값 도달과 효력 시간 경과가 모두 충족된 후에만 동작이 실행된다. 이로써 SV가 파라미터 업데이트나 업그레이드 활성화 같은 변경을 미리 예약할 수 있다.

SV 운영자는 SV 웹 UI의 **거버넌스 탭**을 통해 투표를 관리하며, 새 투표 요청 생성, 대기 중 제안 검토, 투표, 결과 추적을 할 수 있다. UI는 추적을 쉽게 하기 위해 투표 요청을 "Action Needed", "In Progress", "Planned", "Executed", "Rejected" 같은 범주로 묶는다.

## 거버넌스 동작의 유형

거버넌스 동작은 그것을 나타내는 Daml 데이터 타입에 따라 세 범주로 나뉜다: `ARC_DsoRules`, `ARC_AmuletRules`, `ARC_AnsEntryContext`.

### DSO 규칙 동작 (`ARC_DsoRules`)

* **SV 추가** (`SRARC_AddSv`) — 새 슈퍼 밸리데이터를 DSO에 온보딩
* **SV 오프보딩** (`SRARC_OffboardSv`) — 슈퍼 밸리데이터를 DSO에서 제거
* **피처드 앱 권리 부여** (`SRARC_GrantFeaturedAppRight`) — 애플리케이션 제공자를 피처드 앱 보상에 승인
* **피처드 앱 권리 철회** (`SRARC_RevokeFeaturedAppRight`) — 제공자에게서 피처드 앱 상태 제거
* **SV 보상 가중치 업데이트** (`SRARC_UpdateSvRewardWeight`) — SV에 배정된 보상 가중치 변경
* **DSO 구성 설정** (`SRARC_SetConfig`) — 네트워크 수준 파라미터를 통제하는 `DsoRulesConfig` 수정

### Amulet 규칙 동작 (`ARC_AmuletRules`)

* **Amulet 구성 설정** (`CRARC_SetConfig`) — 수수료 스케줄, 발행 곡선, 트래픽 가격을 포함한 <abbr class="gloss" title="트랜잭션 수수료와 밸리데이터 보상에 쓰이는 네이티브 유틸리티 토큰(CC)">Canton Coin</abbr> 경제를 거버넌스하는 `AmuletConfig` 변경

### Canton 네임 서비스 동작 (`ARC_AnsEntryContext`)

* **초기 엔트리 결제 수집** (`ANSRARC_CollectInitialEntryPayment`) — 새 CNS 엔트리의 결제 자동 수집
* **엔트리 결제 거부** (`ANSRARC_RejectEntryInitialPayment`) — 무효한 CNS 엔트리 결제 자동 거부

### 자동 동작

일부 동작은 수동 투표가 필요 없다. SV 노드가 전제 조건이 충족되면 자동으로 확인을 생성한다:

* **발행 라운드 시작** (`CRARC_MiningRound_StartIssuing`) — 보상 요약이 계산되면 마이닝 라운드를 발행으로 전환
* **닫힌 마이닝 라운드 보관** (`CRARC_MiningRound_Archive`) — 완전히 만료된 마이닝 라운드 정리
* **SV 온보딩 확인** (`SRARC_ConfirmSvOnboarding`) — 신원 검증 후 파티가 SV가 될 수 있음을 확인

## 파라미터 거버넌스

SV는 투표된 구성 변경을 통해 네트워크 파라미터를 거버넌스한다. 핵심 구성 가능 파라미터:

* **트래픽 가격** (`extraTrafficPrice`) — 동기화자 트래픽 MB당 USD 비용. [CIP-0042](https://github.com/global-synchronizer-foundation/cips/blob/main/cip-0042/cip-0042.md)에 따라, 표준 Canton Coin 이전이 1 USD가 들도록 보정되어야 한다.
* **읽기 vs 쓰기 스케일링 계수** (`readVsWriteScalingFactor`) — 쓰기 트래픽 비용 대비 읽기 트래픽 비용의 비율로, 순서화·영속화 대비 메시지 전달의 더 낮은 인프라 비용을 반영한다.
* **CC-USD 환율** — 각 SV가 원하는 달러-CC 환율을 온체인에 공표한다. DSO가 모든 공표 값의 **중앙값**을 쓰므로, 어떤 단일 SV의 조작에 저항한다.
* **라운드 기간** — 마이닝 라운드 길이(기본: 10분)로, 보상이 얼마나 자주 계산·발행되는지 결정한다.
* **SV 보상 가중치** — 각 SV는 SV 보상 분배에서의 몫을 결정하는 구성 가능한 보상 가중치를 갖는다. 변경에는 거버넌스 투표가 필요하며 [CF configs 저장소](https://github.com/global-synchronizer-foundation/configs)에도 반영되어야 한다.

CC-USD 환율의 중앙값 기반 접근은 모든 SV 운영자가 선호 값을 공표하고 시스템이 자동으로 중앙값을 선택함을 의미한다. 이는 약 2/3 SV 운영자의 입장을 나타내는 예측 가능한 집계 선호 가격을 만든다.

트래픽 파라미터는 주기적 재보정이 필요하다. 실제 트래픽 비용은 DSO의 SV 수와 Canton 프로토콜 버전 같은 요인에 따라 변하므로, SV는 현재 비용을 측정하고 거버넌스 투표로 파라미터를 그에 맞게 조정할 것으로 기대된다.

## CIP 절차

Canton Network 표준·프로토콜에 대한 형식 변경은 Canton 개선 제안(CIP) 절차를 거친다. CIP는 기술 명세, 거버넌스 절차, 정보성 지침을 다룬다. SV는 위에서 기술한 같은 온체인 거버넌스 메커니즘으로 CIP 채택에 투표한다.

CIP 생애주기와 참여 방법의 전체 개요는 [CIP란?](what-are-cips.md)을 참고하라. CIP 저장소는 [github.com/global-synchronizer-foundation/cips](https://github.com/global-synchronizer-foundation/cips)에서 유지된다.

## Canton Foundation

[Canton Foundation(CF)](https://sync.global)은 글로벌 동기화자의 거버넌스와 성장을 지원하기 위해 만들어진 Linux Foundation 산하의 독립적 비영리 기구다. CF는:

* 자체 SV 노드를 운영하고 회원을 대신해 거버넌스 투표에 참여
* 슈퍼 밸리데이터 거버넌스 결정과 네트워크 운영에 대한 투명성 제공
* SV 운영자 그룹 전반의 업그레이드 일정과 유지보수 조율
* Splice 코드베이스 거버넌스 관리와 피처드 애플리케이션 검토 감독

CF는 네트워크에 대한 일방적 통제권이 없다. 그 SV 노드는 다른 SV와 같은 투표 가중치를 가지며, 모든 거버넌스 동작은 여전히 표준 BFT 투표 임계값을 통과해야 한다. 현재 슈퍼 밸리데이터 목록은 CF가 유지한다.

## 온체인 거버넌스 아키텍처

모든 거버넌스 상태는 Daml 컨트랙트로 온체인에 존재한다. `DsoRules` 컨트랙트가 DSO 멤버십(`svs` 맵)의 권위 있는 기록과 현재 구성을 보유한다. `AmuletRules` 컨트랙트가 Canton Coin 구성 스케줄을 보유한다. 투표 요청, 확인, SV 상태 컨트랙트가 모두 원장에서 보이므로, Scan 앱에 접근할 수 있는 누구나 거버넌스를 감사할 수 있다.

탈중앙화 파티 모델은 DSO 파티 자체가 `ceiling(numSVs * 2.0 / 3.0)`의 확인 임계값을 가짐을 의미한다. DSO 파티가 서명한 모든 트랜잭션은 적어도 그만큼의 SV 참여자 노드가 확인해야 하며, 이는 애플리케이션 수준 투표 로직과 독립적으로 Canton 프로토콜 계층에서 BFT를 강제한다.

## BFT 보장

온체인 투표와 탈중앙 자동화의 결합은 `f`개를 넘지 않는 SV가 부정직하다고 신뢰하는 네트워크 참여자에게 세 보장을 제공한다:

* **유효한 트랜잭션** — 모든 DSO 확인 트랜잭션은 Daml의 [원장 유효성 모델](../learn/ledger-model.md)을 만족한다
* **적시 자동화** — 일상적 운영 동작(라운드 진행, 보상 발행)이 지연 없이 실행된다
* **예측 가능한 파라미터** — 수수료와 구성 값이 적어도 2/3 SV 운영자의 집계 선호를 반영한다
