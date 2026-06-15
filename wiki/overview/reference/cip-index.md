---
title: CIP 인덱스
source: https://docs.canton.network/overview/reference/cip-index
translated: 2026-06-15
status: done
tags: [overview, reference, CIP, 거버넌스]
---

> **출처(원문)**: [CIP Index](https://docs.canton.network/overview/reference/cip-index) · 번역일 2026-06-15

## 📌 개발자 노트
- **한 줄 요약**: 유형(Standards Track / Tokenomics / Process / Governance)·번호·상태별 CIP 목록. 정식 출처는 CIP GitHub 저장소. (CIP 제목은 원문 그대로 유지)
- **선행 개념**: [CIP 소개](../understand/cips-introduction.md), [CIP란?](what-are-cips.md).

---

# CIP 인덱스

> 유형·번호·상태별 Canton 개선 제안(CIP) 레퍼런스 인덱스

이 페이지는 모든 유형의 Canton 개선 제안을 분류한다. 정식 출처(source of truth)는 [CIP GitHub 저장소](https://github.com/global-synchronizer-foundation/cips)이며, 각 CIP는 전체 제안 텍스트를 담은 자체 디렉토리를 갖는다. CIP가 무엇이고 어떻게 작동하는지에 대한 배경은 [CIP란?](what-are-cips.md)을 참고하라. 새 제안을 제출하려면 [CIP 레퍼런스](what-are-cips.md#cip를-제안하는-방법)를 참고하라.

> 참고: 아래 표의 CIP 제목은 원문(영문) 그대로 유지하며, 상태(Status)만 영문 그대로 둔다.

## Standards Track CIP

| 번호 | 제목 | 상태 |
| --- | --- | --- |
| [CIP-0012](https://github.com/global-synchronizer-foundation/cips/blob/main/cip-0012/cip-0012.md) | Minor Adjustments to <abbr class="gloss" title="트랜잭션 수수료와 밸리데이터 보상에 쓰이는 네이티브 유틸리티 토큰(CC)">Canton Coin</abbr> Processing and Operational Configuration | Final |
| [CIP-0013](https://github.com/global-synchronizer-foundation/cips/blob/main/cip-0013/cip-0013.md) | Correct an Error in the <abbr class="gloss" title="다자간 워크플로를 위해 설계된 Canton의 스마트 컨트랙트 언어">Daml</abbr> Models Controlling the Re-onboarding Process | Final |
| [CIP-0056](https://github.com/global-synchronizer-foundation/cips/blob/main/cip-0056/cip-0056.md) | Canton Network Token Standard | Final |
| [CIP-0062](https://github.com/global-synchronizer-foundation/cips/blob/main/cip-0062/cip-0062.md) | Synchronizer Migration with Downtime to Splice 0.4.0 / Canton 3.3 | Final |
| [CIP-0064](https://github.com/global-synchronizer-foundation/cips/blob/main/cip-0064/cip-0064.md) | Delegateless Automation | Final |
| [CIP-0068](https://github.com/global-synchronizer-foundation/cips/blob/main/cip-0068/cip-0068.md) | Bootstrap Network from Non-Zero Round | Final |
| [CIP-0103](https://github.com/global-synchronizer-foundation/cips/blob/main/cip-0103/cip-0103.md) | dApp Standard | Approved |

## Tokenomics CIP

| 번호 | 제목 | 상태 |
| --- | --- | --- |
| [CIP-0001](https://github.com/global-synchronizer-foundation/cips/blob/main/cip-0001/cip-0001.md) | Replace the SV Tranche Time Delays with a Weighted Reward | Final |
| [CIP-0002](https://github.com/global-synchronizer-foundation/cips/blob/main/cip-0002/cip-0002.md) | Minor Adjustments to the Tokenomics Variables | Replaced |
| [CIP-0003](https://github.com/global-synchronizer-foundation/cips/blob/main/cip-0003/cip-0003.md) | Distribute Canton Coin Rewards to Any Validator on the Network | Final |
| [CIP-0007](https://github.com/global-synchronizer-foundation/cips/blob/main/cip-0007/cip-0007.md) | SVs Can Earn Extra SV Reward Weight When Bringing Validators or Apps | Replaced |
| [CIP-0008](https://github.com/global-synchronizer-foundation/cips/blob/main/cip-0008/cip-0008.md) | Update and Refinement to CIP-0002 | Replaced |
| [CIP-0020](https://github.com/global-synchronizer-foundation/cips/blob/main/cip-0020/cip-0020.md) | Update and Refinement to CIP-0002 | Final |
| [CIP-0024](https://github.com/global-synchronizer-foundation/cips/blob/main/cip-0024/cip-0024.md) | SVs and Validators Can Earn SV Reward Weight When Bringing Validators or Apps | Final |
| [CIP-0047](https://github.com/global-synchronizer-foundation/cips/blob/main/cip-0047/cip-0047.md) | Featured App Activity Markers | Final |
| [CIP-0048](https://github.com/global-synchronizer-foundation/cips/blob/main/cip-0048/cip-0048.md) | Raising the Rewards Cap for Validators and Application Providers | Final |
| [CIP-0066](https://github.com/global-synchronizer-foundation/cips/blob/main/cip-0066/cip-0066.md) | Mint Canton Coin from Unminted/Unclaimed Pool | Final |
| [CIP-0067](https://github.com/global-synchronizer-foundation/cips/blob/main/cip-0067/cip-0067.md) | One-Time Allocation of Historical Unclaimed Rewards to GSF | Final |
| [CIP-0070](https://github.com/global-synchronizer-foundation/cips/blob/main/cip-0070/cip-0070.md) | Adjusting Reward Caps for Validators | Withdrawn |
| [CIP-0073](https://github.com/global-synchronizer-foundation/cips/blob/main/cip-0073/cip-0073.md) | Weighted Validator Liveness Rewards for SV-Determined Parties | Replaced |
| [CIP-0078](https://github.com/global-synchronizer-foundation/cips/blob/main/cip-0078/cip-0078.md) | Canton Coin Fee Removal | Final |
| [CIP-0084](https://github.com/global-synchronizer-foundation/cips/blob/main/cip-0084/cip-0084.md) | Tokenomics Committee to Recommend $/MB Price Tuning | Approved |
| [CIP-0086](https://github.com/global-synchronizer-foundation/cips/blob/main/cip-0086/cip-0086.md) | ERC-20 Middleware and Distributed Indexer for Canton Network | Approved |
| [CIP-0089](https://github.com/global-synchronizer-foundation/cips/blob/main/cip-0089/cip-0089.md) | Synchronizer Migration with Downtime to Splice 0.5.0 / Canton 3.4 | Approved |
| [CIP-0096](https://github.com/global-synchronizer-foundation/cips/blob/main/cip-0096/cip-0096.md) | Removing Liveness Rewards from Validator Rewards Pool | Approved |
| [CIP-0098](https://github.com/global-synchronizer-foundation/cips/blob/main/cip-0098/cip-0098.md) | Cap Per-Transaction Application Rewards at $1.50 | Approved |
| [CIP-0104](https://github.com/global-synchronizer-foundation/cips/blob/main/cip-0104/cip-0104.md) | Traffic-Based App Rewards | Proposed |

## Process CIP

| 번호 | 제목 | 상태 |
| --- | --- | --- |
| [CIP-0000](https://github.com/global-synchronizer-foundation/cips/blob/main/cip-0000/cip-0000.md) | CIP Process | Active |
| [CIP-0006](https://github.com/global-synchronizer-foundation/cips/blob/main/cip-0006/cip-0006.md) | Define the Process of Distributing and Approving | Active |
| [CIP-0050](https://github.com/global-synchronizer-foundation/cips/blob/main/cip-0050/cip-0050.md) | Controlled Validator Growth Through Trusted Operators | Withdrawn |

## Governance CIP

CIP의 대다수는 <abbr class="gloss" title="글로벌 동기화자를 운영하고 네트워크 거버넌스에 참여하는 노드">슈퍼 밸리데이터</abbr> 온보딩, 위원회 구성, 운영 정책을 다루는 거버넌스 제안이다. 주목할 만한 거버넌스 CIP 일부를 아래에 나열한다. 전체 집합(60개 이상의 거버넌스 제안)은 [CIP 저장소](https://github.com/global-synchronizer-foundation/cips)를 참고하라.

| 번호 | 제목 | 상태 |
| --- | --- | --- |
| [CIP-0014](https://github.com/global-synchronizer-foundation/cips/blob/main/cip-0014/cip-0014.md) | Enhancements to the Scan API to Facilitate Tax Accounting | Final |
| [CIP-0021](https://github.com/global-synchronizer-foundation/cips/blob/main/cip-0021/cip-0021.md) | Introduce Featured Application and Validator Committee | Active |
| [CIP-0042](https://github.com/global-synchronizer-foundation/cips/blob/main/cip-0042/cip-0042.md) | Stable Price per Canton Coin Transfer via Synchronizer Fees | Active |
| [CIP-0045](https://github.com/global-synchronizer-foundation/cips/blob/main/cip-0045/cip-0045.md) | SV Operating Requirements | Active |
| [CIP-0051](https://github.com/global-synchronizer-foundation/cips/blob/main/cip-0051/cip-0051.md) | Streamline On-Chain Governance Votes | Final |
| [CIP-0079](https://github.com/global-synchronizer-foundation/cips/blob/main/cip-0079/cip-0079.md) | Demonstrate Third-Party Price Feed Integration for CC Listing | Approved |
| [CIP-0082](https://github.com/global-synchronizer-foundation/cips/blob/main/cip-0082/cip-0082.md) | Establish a 5% Development Fund (Foundation-Governed) | Approved |
| [CIP-0092](https://github.com/global-synchronizer-foundation/cips/blob/main/cip-0092/cip-0092.md) | Controlled Transition to Dynamic Market Feeds Post-Listing | Approved |
| [CIP-0100](https://github.com/global-synchronizer-foundation/cips/blob/main/cip-0100/cip-0100.md) | Governance of the CIP-0082 Development Fund | Approved |

> ℹ️ 이 인덱스는 작성 시점의 CIP 저장소 상태를 반영하며, 이 페이지가 마지막으로 갱신된 후 추가된 제안은 포함하지 않을 수 있다. 최신 제안은 항상 [GitHub 저장소](https://github.com/global-synchronizer-foundation/cips)를 확인하라.
