---
title: Canton Foundation 정책 (CF Policies)
source: https://docs.canton.network/overview/reference/gsf-policies
translated: 2026-06-15
status: done
tags: [overview, reference, 거버넌스, 정책]
---

> **출처(원문)**: [CF Policies](https://docs.canton.network/overview/reference/gsf-policies) · 번역일 2026-06-15

## 📌 개발자 노트
- **한 줄 요약**: Canton Foundation(CF)의 정책·거버넌스 프레임워크 — 목적·역할, 멤버십 등급, 멤버 위원회, 거버넌스 프레임워크, 네트워크 정책(<abbr class="gloss" title="파티를 호스팅하고 그 파티의 컨트랙트 데이터를 저장하는 참여자 노드">밸리데이터</abbr> 온보딩·트래픽/수수료·참여 요건·보상), 업그레이드 조율, CIP 거버넌스, 커뮤니케이션 채널.
- **핵심 용어**: Canton Foundation, 멤버십(Premier/General/Associate), 멤버 위원회, DSO <abbr class="gloss" title="Canton에서 권한과 데이터 가시성의 주체가 되는 식별 가능한 참여 주체">파티</abbr>, 밸리데이터 온보딩·allowlist, CometBFT
- **선행 개념**: [글로벌 동기화자](../understand/global-synchronizer.md), [SV 거버넌스 레퍼런스](sv-governance-reference.md), [CIP 레퍼런스](what-are-cips.md).

---

# Canton Foundation 정책 (CF Policies)

[Canton Foundation](https://canton.foundation)(CF)은 Linux Foundation과 협력해 만들어진 독립적 비영리 조직이다. Canton Network의 탈중앙화 상호운용·동기화 인프라인 <abbr class="gloss" title="슈퍼 밸리데이터들이 공동 운영하는 Canton의 퍼블릭 조율(합의) 계층">글로벌 동기화자</abbr>를 거버넌스한다.

## 목적과 역할

CF는 글로벌 <abbr class="gloss" title="상태를 저장하지 않고 트랜잭션 합의·순서를 조율하는 Canton 구성요소">동기화자</abbr>에 대한 투명한 거버넌스를 제공하고 그 주변 생태계를 성장시키기 위해 일한다. 책임은:

* 글로벌 동기화자의 거버넌스 프레임워크 정의·유지
* <abbr class="gloss" title="글로벌 동기화자를 운영하고 네트워크 거버넌스에 참여하는 노드">슈퍼 밸리데이터</abbr> 운영과 거버넌스 투표에 대한 투명성 제공
* 슈퍼 밸리데이터 노드를 운영하고 회원을 대신해 거버넌스에 참여
* 슈퍼 밸리데이터 집합 전반의 업그레이드 일정과 네트워크 정책 조율
* 아웃리치, 개발자 프로그램, 프로토콜 개발 기금을 통한 생태계 개발 지원

CF는 네트워크를 일방적으로 통제하지 않는다. 거버넌스 결정은 온체인 투표 메커니즘을 통한 슈퍼 밸리데이터 간 합의를 요구한다. CF는 이 투표에 여럿 중 하나의 슈퍼 밸리데이터로 참여한다.

## 멤버십

CF는 세 멤버십 등급을 제공한다:

* **Premier** (연 $150,000) — 이사회 의석, 이사회 위원회 대의원직, 이사회 전략일 참여, 마케팅 자료의 프리미엄 배치 포함
* **General** (연 $5,000~$30,000, 조직 규모에 따라 차등) — 멤버 위원회 참여와 블로그 게시 접근 포함
* **Associate** (무료) — 정부 기관, 규제 기관, 비영리, 학술 기관으로 제한; 이사회 승인 필요

모든 회원은 CF의 멤버 위원회에 참여할 수 있다. [CF 멤버십 페이지](https://canton.foundation/membership)에서 멤버십을 신청할 수 있다.

## 멤버 위원회

CF는 거버넌스·운영 작업을 여섯 멤버 위원회로 조직한다:

* **기술·운영(Tech and Operations)** — 기술 방향과 운영 표준
* **토크노믹스(Tokenomics)** — <abbr class="gloss" title="트랜잭션 수수료와 밸리데이터 보상에 쓰이는 네이티브 유틸리티 토큰(CC)">Canton Coin</abbr> 경제, 수수료 보정, 보상 파라미터
* **책임(Accountability)** — 감독과 규정 준수
* **마케팅(Marketing)** — 생태계 아웃리치와 커뮤니케이션
* **법무(Legal)** — 법적 프레임워크와 규제 사안
* **감사·재무(Audit and Finance)** — 재무 감독

Premier 회원은 추가로 이사회 위원회에 접근하고 그 위원회에 대의원을 임명할 수 있다.

## 거버넌스 프레임워크

글로벌 동기화자는 슈퍼 밸리데이터라 부르는 독립적으로 행동하는 조직들이 운영한다. 이 조직들은 핵심 인프라 — 시퀀서, 미디에이터, SV 애플리케이션 노드 — 를 운영하고 온체인 거버넌스 애플리케이션을 통해 거버넌스에 참여한다.

거버넌스 동작은 온보딩된 슈퍼 밸리데이터의 약 2/3 확인 임계값을 가진 탈중앙화 <abbr class="gloss" title="다자간 워크플로를 위해 설계된 Canton의 스마트 컨트랙트 언어">Daml</abbr> 파티인 DSO(탈중앙화 동기화자 운영) 파티를 통해 실행된다. CF를 포함한 어떤 단일 주체도 일방적 변경을 할 수 없다. DSO 파티, 확인 프로토콜, 투표 메커니즘의 상세 분해는 [SV 거버넌스 레퍼런스](sv-governance-reference.md)를 참고하라.

거버넌스 프레임워크가 다루는 것:

* **네트워크 구성** — 트래픽 가격, 수수료 스케줄, 토크노믹스 구성 같은 파라미터
* **슈퍼 밸리데이터 멤버십** — 슈퍼 밸리데이터 온보딩·오프보딩
* **소프트웨어 업그레이드** — Canton·Splice 버전 업그레이드 조율
* **Daml 패키지 업그레이드** — 온체인 거버넌스·토크노믹스 패키지 업그레이드 관리
* **Canton 개선 제안(CIP)** — 네트워크 규칙·표준 변경을 제안·비준하는 구조화된 절차

## 네트워크 정책

### 밸리데이터 온보딩

밸리데이터는 TestNet이나 MainNet에 합류하기 전 승인되어야 한다. 절차는 다음과 같다:

1. [CF 밸리데이터 요청 양식](https://sync.global/validator-request/)으로 요청을 제출한다.
2. 토크노믹스 위원회가 신청을 검토·승인한다.
3. 후원 슈퍼 밸리데이터가 SV 집합이 유지하는 allowlist에 당신의 egress IP를 제공한다. 네트워크당 하나의 IP만 허용되며, DevNet·TestNet·MainNet 전반에서 구별되어야 한다.
4. 슈퍼 밸리데이터 다수가 갱신된 allowlist를 채택하면(보통 2~7일), 후원 SV로부터 일회성 온보딩 시크릿을 받는다. 이 시크릿은 48시간 후 만료된다.
5. 온보딩 시크릿으로 밸리데이터 노드를 배포한다.

DevNet은 토크노믹스 위원회 승인 없이 어떤 밸리데이터에게도 열려 있지만, IP는 여전히 allowlist에 추가되어야 한다.

### 트래픽·수수료 정책

슈퍼 밸리데이터는 거버넌스 투표로 트래픽 가격 파라미터를 집합적으로 설정한다. `extraTrafficPrice` 파라미터는 동기화자의 쓰기 트래픽 비용을 결정하며, 표준 Canton Coin 이전이 약 1 USD가 들도록 보정된다([CIP-0042](https://github.com/canton-foundation/cips/blob/main/cip-0042/cip-0042.pdf)에 따라). 슈퍼 밸리데이터는 주기적으로 실제 트래픽 비용을 측정하고 파라미터를 그에 맞게 조정할 것으로 기대된다.

수수료 파라미터는 온체인 중앙값 기반 투표 메커니즘으로 갱신된다: 각 SV가 선호 값을 공표하고 시스템이 중앙값을 쓴다. 이는 어떤 단일 SV도 파라미터를 소량 이상 움직일 수 없게 한다.

### 참여 요건

슈퍼 밸리데이터는 네트워크에 참여하기 위해 운영 요건을 충족해야 한다:

* 필요한 인프라 구성 요소(시퀀서, 미디에이터, SV 애플리케이션) 운영
* BFT 합의를 지원하기 위한 가동 시간과 연결성 유지
* 거버넌스 투표와 업그레이드 조율에 참여
* 합의 참여를 위한 CometBFT 밸리데이터 요건 준수

글로벌 동기화자가 쓰는 CometBFT 합의 프로토콜은 네트워크가 진전하려면 슈퍼 밸리데이터의 2/3 초과가 운영 중이어야 한다. 각 슈퍼 밸리데이터 장애는 장애 허용 버퍼를 줄인다.

### 보상 정책

슈퍼 밸리데이터는 인프라 운영에 대해 보상을 벌며, 이는 보상 가중치 파라미터로 구성된다. 보상 가중치 변경은 거버넌스 투표 절차를 따른다:

1. 슈퍼 밸리데이터 소유자가 갱신된 가중치에 합의한다.
2. SV 웹 UI로 거버넌스 투표가 개시된다.
3. 투표가 슈퍼 밸리데이터 정족수의 승인을 받아야 한다.
4. 갱신된 가중치가 온보딩 이벤트 전반의 일관성을 위해 [CF configs 저장소](https://github.com/global-synchronizer-foundation/configs)에 반영된다.

## 업그레이드 조율

네트워크 업그레이드 — Canton 버전이든, Splice 버전이든, Daml 패키지 업그레이드든 — 는 모든 슈퍼 밸리데이터 전반의 조율을 요구한다. CF는 다음으로 이를 촉진한다:

* 업그레이드 일정과 요건을 모든 운영자에게 전달
* 슈퍼 밸리데이터 집합 전반의 준비 상태 추적
* 특정 업그레이드 절차(예: Daml 업그레이드 중 트리거 일시 중지)에 대한 운영 지침 제공

제때 업그레이드하지 않는 슈퍼 밸리데이터는 운영 문제를 일으킬 수 있다. 예컨대 Daml 패키지 업그레이드 중 구버전을 실행하는 밸리데이터가 보상 만료 자동화를 막을 수 있다. CF는 이런 상황에 대한 우회책을 조율하고 준수 데드라인을 설정한다.

## CIP 거버넌스

네트워크 규칙·표준·프로토콜 변경은 Canton 개선 제안(CIP)을 통해 제안된다. CIP 절차는 생태계의 누구나 변경을 제안할 구조화된 방법을 제공하며, 최종 비준은 슈퍼 밸리데이터 투표로 이뤄진다.

CIP 절차의 상세와 제안 방법은 [CIP 레퍼런스](what-are-cips.md)를 참고하라. CIP 전체 목록은 [github.com/global-synchronizer-foundation/cips](https://github.com/global-synchronizer-foundation/cips)에서 유지된다.

## 커뮤니케이션 채널

CF는 밸리데이터 운영자와 생태계 참여자를 위한 여러 채널을 유지한다:

* **Slack** — 운영 조율은 `#validator-operations`, 애플리케이션 개발은 `#gsf-global-synchronizer-appdev`, 생태계 논의는 `#gsf-outreach`
* [lists.sync.global](https://lists.sync.global/)의 **메일링 리스트** — `main`(일반 Canton Network 공지), `cip-announce`(새 CIP 알림), `tokenomics-announce`(토크노믹스 위원회 결정), `validator-announce`(운영자 대상 공지) 등
* **지원(Support)** — 최선 노력 지원은 `da-support@digitalasset.com`, SLA 기반 지원은 `support@digitalasset.com`

## 추가 자원

* [CF 웹사이트](https://canton.foundation) — 재단 정보와 멤버십
* [Canton Network](https://canton.network) — 네트워크 개요와 진입점
* [CF configs 저장소](https://github.com/global-synchronizer-foundation/configs) — 네트워크 구성 파라미터
* [CIP 저장소](https://github.com/global-synchronizer-foundation/cips) — Canton 개선 제안
* [SV 거버넌스 레퍼런스](sv-governance-reference.md) — DSO 파티와 투표 메커니즘의 기술 상세

<!-- nav:start -->
---
<sub>⬅️ **이전**: [로컬 파티와 외부 파티](external-party.md) ・ ➡️ **다음**: [인과성과 시간 (Causality and Time)](ledger-causality.md)</sub>
<!-- nav:end -->
