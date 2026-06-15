---
title: Splice 월렛 레퍼런스
source: https://docs.canton.network/overview/reference/splice-wallet-reference
translated: 2026-06-15
status: done
tags: [overview, reference, 월렛, Splice]
---

> **출처(원문)**: [Splice Wallet Reference](https://docs.canton.network/overview/reference/splice-wallet-reference) · 번역일 2026-06-15

## 📌 개발자 노트
- **한 줄 요약**: 모든 <abbr class="gloss" title="파티를 호스팅하고 그 파티의 컨트랙트 데이터를 저장하는 참여자 노드">밸리데이터</abbr> 노드에 내장된 <abbr class="gloss" title="글로벌 Synchronizer를 구동하는 오픈소스 애플리케이션 모음(SV·밸리데이터·월렛 등)">Splice</abbr> 월렛 — UI·자동화(보상 수집·<abbr class="gloss" title="Synchronizer에 쓰기를 요청할 때 소비하는 자원. Canton Coin으로 비용을 지불">트래픽</abbr> 충전·스윕·자동수락), 사전 승인(TransferPreapproval) 설정·갱신·취소, 이전 워크플로(2단계/1단계), 월렛 API, UTXO 관리(병합 위임), 외부 <abbr class="gloss" title="Canton에서 권한과 데이터 가시성의 주체가 되는 식별 가능한 참여 주체">파티</abbr> 지원.
- **핵심 용어**: Splice 월렛, TransferPreapproval(provider/receiver), 스윕(sweep), MergeDelegation, UTXO·더스트, 외부 파티 서명
- **선행 개념**: [Canton Coin](../understand/canton-coin.md), [Canton Coin 토크노믹스](canton-coin-tokenomics.md).

---

# Splice 월렛 레퍼런스

Splice 월렛은 Canton Network의 모든 밸리데이터 노드에 내장된 월렛 구성 요소다. 해당 밸리데이터에 <abbr class="gloss" title="참여자 노드가 파티를 대신해 원장에서 활동(컨트랙트 저장·트랜잭션 제출·확인)해 주는 것. 로컬 파티는 키까지 노드가 관리하고, 외부 파티는 제출 키를 파티 자신이 보유(노드는 중계)">호스팅</abbr>된 파티를 위한 <abbr class="gloss" title="트랜잭션 수수료와 밸리데이터 보상에 쓰이는 네이티브 유틸리티 토큰(CC)">Canton Coin</abbr>(CC) 관리를 제공하며, 웹 UI, 백그라운드 자동화, 프로그래밍적 API를 포함한다.

## 월렛 UI

월렛 UI는 모든 밸리데이터 노드에 함께 제공되며 사용자에게 CC 연산을 위한 브라우저 기반 인터페이스를 준다. 로그인과 온보딩(새 파티를 할당) 후 사용자는:

* CC 잔액과 개별 Holding <abbr class="gloss" title="원장에 기록되는 불변 데이터 단위. 상태 변경은 새 컨트랙트 생성으로 표현됨">컨트랙트</abbr>(UTXO)를 본다
* 이전 오퍼 또는 1단계 사전 승인 이전으로 다른 파티에 CC를 보낸다
* 들어오는 이전 오퍼를 수락·거부·철회한다
* <abbr class="gloss" title="원장 상태를 바꾸는 원자적 작업 단위. 하나 이상의 컨트랙트를 생성·보관하며, 전부 적용되거나 전혀 적용되지 않음">트랜잭션</abbr> 이력을 검토한다
* 네트워크의 임의 밸리데이터에 대해 트래픽을 구매한다
* 발행 위임을 관리한다(외부 파티의 제안을 수락·거부·철회)

밸리데이터 운영자의 파티는 밸리데이터 초기화 중 자동 생성되어 구성된 `validatorWalletUser`와 연관된다. 다른 사용자는 UI 또는 `/v0/admin/users` API 엔드포인트로 온보딩한다.

## 월렛 자동화

밸리데이터 앱은 월렛 사용자를 대신해 여러 백그라운드 자동화를 실행한다. 이들은 수동 개입 없이 반복적 CC 연산을 처리한다.

**보상 수집.** 월렛 자동화는 각 온보딩된 파티에 대해 보상 쿠폰(밸리데이터 보상, 앱 보상, 라이브니스 활동 레코드)을 주기적으로 수집·발행한다. 이는 획득한 쿠폰을 CC 보유로 변환한다.

**트래픽 충전.** 구성되면, 밸리데이터는 추가 트래픽 잔액이 임계값 아래로 떨어질 때마다 운영자 월렛의 CC를 써서 자동으로 트래픽 크레딧을 구매한다. 운영자가 `targetThroughput`와 `minTopupInterval`을 설정하면, 자동화가 그 처리량을 유지할 만큼의 트래픽을 산다. DevNet에서는 월렛에 자금이 없으면 밸리데이터가 충분한 코인을 자동으로 탭한다.

**스윕(Sweeps).** 운영자는 자동 스윕을 구성할 수 있다. 송신자 잔액이 `maxBalanceUSD` 임계값을 초과하면 CC가 한 파티에서 다른 파티로 이전된다. 자동화는 자금을 구성된 `minBalanceUSD`까지 낮추는 이전 오퍼를 생성한다. 스윕 구성은 송신자 파티 ID를 수신자 파티 ID와 잔액 임계값에 매핑한다. 스윕은 1단계 전달을 위해 이전 사전 승인을 쓸 수 있다.

**자동 수락(Auto-accept).** 운영자는 특정 송신자 파티로부터 들어오는 이전 오퍼의 자동 수락을 구성할 수 있다. 이는 밸리데이터의 Helm 차트 또는 Docker Compose 구성에서 송신자-수신자 파티 ID 쌍별로 구성된다.

Eth나 Bitcoin 같은 다른 자산과 달리, Canton Coin은 파티가 Canton Coin을 보유하는 데 명시적으로 동의할 것을 요구한다. 여기에는 들어오는 모든 이전에 명시적으로 동의하는 것도 포함된다.

어떤 송신자로부터든 들어오는 Canton Coin 이전을 받아도 괜찮은 파티는 `TransferPreapproval`을 설정할 수 있다. 이로써 임의의 파티가 `TransferPreapproval`을 설정한 파티에게 Canton Coin을 보낼 수 있다. 이는 Canton Coin 이전에만 적용되고 다른 자산에는 적용되지 않는다. 다른 자산은 별도로 설정해야 하는 자체 사전 승인 변형을 제공하거나, 들어오는 각 이전에 개별 승인을 요구할 수 있다.

<abbr class="gloss" title="글로벌 Synchronizer를 운영하고 네트워크 거버넌스에 참여하는 노드">슈퍼 밸리데이터</abbr>가 더 이상 활성이 아닌 파티의 `TransferPreapproval` 컨트랙트를 저장·제공하지 않아도 되도록, 또 악의적 파티가 스팸하지 못하도록, 사전 승인은 만료까지의 제한된 수명을 가지며 생성 시 수명에 비례한 수수료를 소각해야 한다. 수수료는 슈퍼 밸리데이터가 `transferPreapprovalFee` 파라미터로 통제한다. 현재 값은 CC Scan([링크](https://scan.sv-1.unknown_cluster.global.canton.network.sync.global/dso))에서 관찰할 수 있으며 기본값은 연 $1이다.

각 사전 승인에는 두 파티가 있다: 들어오는 이전을 승인하는 `receiver` 파티와 `provider` 파티. provider 파티는 수수료를 내고 만료일이 가까워지면 사전 승인을 갱신할 책임이 있다. 그 대가로 `provider` 파티는 이 사전 승인을 쓰는 모든 들어오는 이전의 앱 제공자가 되어 그에 대한 앱 보상을 받는다. `provider` 파티가 `receiver` 파티와 같은 노드에 호스팅될 필요는 없으나, 실무에서는 그것이 가장 흔한 설정이다.

## 사전 승인 설정

외부 서명을 쓰지 않는 파티의 경우, 사용자가 Splice 월렛 UI에서 로그아웃 버튼 옆 버튼으로 사전 승인을 생성할 수 있다:

<img src="https://mintcdn.com/cantonfoundation/Ps1aWN9aLFijpT3F/images/splice/preapproval_button.png?fit=max&auto=format&n=Ps1aWN9aLFijpT3F&q=85&s=feabdf575485595c7c0aa26911e133dd" width="600" alt="사전 승인 생성 버튼" />

외부 서명을 쓰는 파티의 경우, 가장 흔한 방법은 밸리데이터 운영자가 `ExternalPartySetupProposal` 컨트랙트를 생성하는 것이다. 그런 다음 외부 파티가 `ExternalPartySetupProposal_Accept`를 실행하는 트랜잭션에 서명한다. 이는 외부 파티의 밸리데이터 보상 발행에 필요한 `ValidatorRight` 컨트랙트와, provider가 밸리데이터 운영자 파티로 설정된 `TransferPreapproval` 컨트랙트를 모두 생성한다. 밸리데이터는 제안 생성을 위한 `/v0/admin/external-party/setup-proposal` 엔드포인트와, 외부 파티의 서명된 수락을 준비·제출하기 위한 `/v0/admin/external-party/setup-proposal/prepare-accept`·`/v0/admin/external-party/setup-proposal/submit-accept`를 노출한다. 상세는 API 문서 참고. provider를 누구로 할지 다른 설정을 원하면, 자체 설정 <abbr class="gloss" title="다자간 워크플로를 위해 설계된 Canton의 스마트 컨트랙트 언어">Daml</abbr> 컨트랙트를 만들어 밸리데이터 API 대신 Ledger API로 생성해야 할 수 있다.

provider를 밸리데이터 운영자로 설정해 사전 승인을 설정할 때 파티 수 제한에 유의하라.

밸리데이터 API는 항상 90일 후 만료일로 사전 승인을 생성한다.

## 사전 승인의 만료와 갱신

위에서 설명했듯, 사전 승인은 항상 만료일을 갖는다. 그 날짜에 도달하고 갱신되지 않으면, 더 이상 이전에 쓸 수 없고 슈퍼 밸리데이터가 실행하는 자동화가 결국 컨트랙트를 <abbr class="gloss" title="컨트랙트를 소비해 비활성으로 만드는 것(archive). 보관된 컨트랙트는 더 이상 쓸 수 없음">보관</abbr>한다.

밸리데이터 운영자 파티를 provider로 갖는 사전 승인은 만료가 30일 미만으로 남으면 밸리데이터 앱의 자동화를 통해 또 90일 자동 갱신된다.

다른 파티를 provider로 사전 승인을 설정했다면, `TransferPreapproval_Renew` <abbr class="gloss" title="컨트랙트에서 수행 가능한 동작(권한이 부여된 당사자만 실행 가능)">초이스</abbr>를 주기적으로 실행하는 자체 갱신 자동화를 설정해야 한다.

## 사전 승인의 취소

사전 승인은 `TransferPreapproval_Cancel` 초이스를 통해 receiver와 provider 모두가 철회할 수 있다.

현재 Splice 월렛 UI에서는 지원되지 않지만, 밸리데이터 운영자를 provider로 갖는 사전 승인의 경우 운영자가 `/v0/admin/transfer-preapprovals/by-party/{receiver-party}`에 `DELETE` 요청을 쓸 수 있다. 상세는 API 문서 참고.

## 사전 승인을 통한 이전

Splice 월렛 UI는 수신자가 사전 승인을 설정했으면 이전에 자동으로 사전 승인을 쓰도록 기본 설정한다.

API로 작업하는 경우, 특히 외부 파티의 경우, Canton Coin 이전을 실행하는 선호 방법은 토큰 표준 API를 통하는 것이며 이 역시 가능한 경우 사전 승인을 쓴다. 사용 예시는 [CIP](https://github.com/global-synchronizer-foundation/cips/blob/main/cip-0056/cip-0056.md)와 [토큰 표준 레퍼런스 CLI](https://github.com/canton-network/splice/blob/main/token-standard/cli/src/commands/transfer.ts)를 참고하라.

마지막으로, 비표준 Canton Coin 이전을 위한 밸리데이터의 레거시 외부 서명 API `/v0/admin/external-party/transfer-preapproval/prepare-send`·`/v0/admin/external-party/transfer-preapproval/submit-send`도 쓸 수 있다. 상세는 API 문서 참고.

## 이전 워크플로

파티 간 CC 이전은 세 패턴 중 하나를 따른다.

**2단계 토큰 표준 이전.** 송신자가 CC를 `TransferInstruction` 컨트랙트에 잠근다. 수신자가 수락(잠금 해제 후 이전 완료)하거나, 거부하거나, 만료시킨다. 송신자는 수락 전에 오퍼를 철회해 잠긴 자금을 회수할 수도 있다. [CIP-0078](https://github.com/global-synchronizer-foundation/cips/blob/main/cip-0078/cip-0078.md) 이후 이 이전에는 수수료가 부과되지 않는다.

**1단계 사전 승인 이전.** 수신자가 `TransferPreapproval` 컨트랙트를 설정했으면, 송신자는 수신자의 수락 없이 한 단계로 CC를 이전할 수 있다. 수신자의 밸리데이터 운영자가 사전 승인의 `provider` 파티 역할을 하며 주기적 갱신을 처리한다. provider가 피처드 애플리케이션 제공자면, 이전이 `AppRewardCoupon`을 생성한다.

## 월렛 API 엔드포인트

밸리데이터 앱은 `/v0/wallet/*` 경로 아래 월렛 API를 노출한다. 두 범주로 나뉜다.

**External API** (`wallet-external.yaml`) — 하위 호환성 보장을 갖춘 프로그래밍적 월렛 상호작용용. 주체(subject) 클레임이 월렛 사용자를 식별하는 JWT를 요구한다. 엔드포인트:

* `POST /v0/wallet/transfer-offers` — 이전 오퍼 생성
* `POST /v0/wallet/transfer-offers/{tracking_id}/status` — 이전 오퍼 상태 <abbr class="gloss" title="이해관계자 밸리데이터가 트랜잭션이 유효함을 미디에이터에 응답하는 것(confirmation)">확인</abbr>
* `GET /v0/wallet/transfer-offers` — 이전 오퍼 나열
* `POST /v0/wallet/buy-traffic-requests` — 트래픽 구매 요청
* `POST /v0/wallet/buy-traffic-requests/{tracking_id}/status` — 트래픽 구매 상태 확인

**Internal API** (`wallet-internal.yaml`) — 월렛 UI 프론트엔드가 사용. 하위 호환성 보장 없음. 엔드포인트:

* `GET /v0/wallet/balance` — 월렛 잔액 조회
* `GET /v0/wallet/amulets` — UTXO 나열
* `POST /v0/wallet/transactions` — 트랜잭션 이력
* `POST /v0/wallet/transfer-offers/accept` — 이전 오퍼 수락
* `POST /v0/wallet/transfer-offers/reject` — 이전 오퍼 거부
* `POST /v0/wallet/transfer-offers/withdraw` — 이전 오퍼 철회
* `GET /v0/wallet/user-status` — 사용자 온보딩·월렛 상태

전체 OpenAPI 명세는 [wallet-external.yaml](https://raw.githubusercontent.com/canton-network/splice/refs/heads/main/apps/wallet/src/main/openapi/wallet-external.yaml)과 [wallet-internal.yaml](https://raw.githubusercontent.com/canton-network/splice/refs/heads/main/apps/wallet/src/main/openapi/wallet-internal.yaml) 파일 참고.

## UTXO 관리

Canton Coin은 Splice의 기반 Amulet 컨트랙트 구조에서 물려받은 UTXO 모델을 쓴다. <abbr class="gloss" title="거래·컨트랙트가 기록되는 장부. Canton에선 활성 컨트랙트의 모음">원장</abbr>의 각 활성 `Holding` 컨트랙트는 특정 CC 양을 가진 단일 UTXO를 나타낸다. 계정 잔액 모델과 달리, 파티의 총 잔액은 그들의 모든 개별 Holding UTXO의 합이다. 활성 Holding 컨트랙트가 호스팅 밸리데이터의 저장·연산을 소비하고, 이전에 입력되는 각 UTXO가 추가 트래픽 비용을 발생시키므로, UTXO 관리는 월렛 제공자에게 중요하다.

Canton Coin은 이전당 입력 컨트랙트 100개 제한을 강제하고, 초기 금액이 누적 보유 수수료보다 작은 더스트 UTXO를 만료시킨다. 월렛 제공자는 사용자당 평균 대략 10개 이하의 UTXO를 목표로 해야 한다.

**MergeDelegation 컨트랙트**는 월렛 제공자가 사용자를 대신해 작은 Holding UTXO를 병합하게 한다. 워크플로:

1. 사용자가 온보딩 중 `MergeDelegationProposal` 생성에 서명한다.
2. 월렛 제공자가 제안을 수락해 활성 `MergeDelegation`을 생성한다.
3. 백그라운드 프로세스가 UTXO 10개 초과인 사용자를 식별하고, 레지스트리 API로 병합 연산을 구성하고, `BatchMergeUtility_MergeHoldings` 초이스를 써서 ~100개 배치로 실행한다.

MergeDelegation 컨트랙트는 또한 월렛 제공자가 에어드롭 캠페인과 보유 자동 병합을 단일 배치 호출로 결합하게 한다. 피처드 월렛 제공자는 병합 수행에 대해 피처드 앱 보상을 번다.

## 외부 파티 월렛 지원

밸리데이터는 외부 파티 — 트랜잭션 서명 키를 <abbr class="gloss" title="파티를 호스팅하고 그 파티의 컨트랙트를 저장·실행하는 노드. 밸리데이터의 핵심 구성요소">참여자 노드</abbr> 외부에 보유하는 파티 — 의 CC를 관리하는 API를 제공한다. 외부 서명 워크플로는 Canton의 대화형 제출(interactive submission) 기능을 쓴다. 트랜잭션이 참여자에서 준비되고, 외부에서 서명되고, 다시 제출된다.

외부 파티의 상위 수준 흐름:

1. `/v0/admin/external-party/topology/*`로 외부 파티의 <abbr class="gloss" title="어떤 노드·파티·키가 네트워크에 참여하는지를 정의하는 구성 정보">토폴로지</abbr> 설정
2. `/v0/admin/external-party/setup-proposal`로 `TransferPreapproval`을 생성해 CC 송수신 활성화
3. `/v0/admin/external-party/transfer-preapproval/*`로 CC 전송
4. `GET /v0/admin/external-party/balance`로 잔액 조회

각 이전에 대해 호출자는 트랜잭션을 준비(해시 획득)하고, 외부 파티의 개인키로 해시에 서명하고, 서명된 트랜잭션을 참여자에 다시 제출해야 한다. 전체 엔드포인트 목록은 [validator-internal.yaml](https://raw.githubusercontent.com/canton-network/splice/refs/heads/main/apps/validator/src/main/openapi/validator-internal.yaml) OpenAPI 스펙 참고.

TypeScript Wallet SDK로 커스텀 월렛 통합을 구축하려면 [Wallet SDK 문서](https://docs.canton.network/integrations/wallet/sdk-download)를 참고하라.

<!-- nav:start -->

---

⬅️ **이전**: [스마트 컨트랙트 합의](smart-contract-consensus.md) ・ ➡️ **다음**: [슈퍼 밸리데이터 구성 요소](super-validator-components.md)

<!-- nav:end -->
