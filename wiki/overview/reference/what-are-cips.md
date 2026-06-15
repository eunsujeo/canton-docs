---
title: CIP 레퍼런스 (CIP란?)
source: https://docs.canton.network/overview/reference/what-are-cips
translated: 2026-06-15
status: done
tags: [overview, reference, CIP, 거버넌스]
---

> **출처(원문)**: [CIP Reference](https://docs.canton.network/overview/reference/what-are-cips) · 번역일 2026-06-15

## 📌 개발자 노트
- **한 줄 요약**: CIP의 형식 구조·생애주기·거버넌스 메커니즘 — 5개 유형, 생애주기(Draft→Proposed→Approved→Active/Final), 번호 규칙, 제안 주체, 검토·승인(SV 2/3 투표), 온체인 거버넌스 관계, 문서 구조, 주목할 CIP, 제안 방법.
- **핵심 용어**: CIP-0000, Standards Track/Governance/Tokenomics/Process/Informational, SV 후원·2/3 투표, cip-discuss/cip-vote
- **선행 개념**: [CIP 소개](../understand/cips-introduction.md), [CIP 인덱스](cip-index.md), [SV 거버넌스 레퍼런스](sv-governance-reference.md).

---

# CIP 레퍼런스

Canton 개선 제안(CIP)은 Canton Network을 위한 표준, 프로토콜 변경, 거버넌스 절차, 지침을 기술하는 형식 설계 문서다. 커뮤니티가 네트워크 변경을 제안하고 비준하는 주된 메커니즘 역할을 한다.

CIP 절차는 확립된 개선 제안 프레임워크(Ethereum의 EIP, Python의 PEP 등)를 본떴으며 [CIP-0000](https://github.com/global-synchronizer-foundation/cips/blob/main/cip-0000/cip-0000.md)에 형식적으로 정의되어 있다. 모든 CIP는 Canton Foundation이 관리하는 [공개 GitHub 저장소](https://github.com/global-synchronizer-foundation/cips)에서 유지된다.

CIP에 대한 입문 개요와 그 중요성은 [CIP 소개](../understand/cips-introduction.md)를 참고하라.

## CIP 유형

각 CIP는 다섯 범주 중 하나에 속한다:

* **Standards Track** — <abbr class="gloss" title="슈퍼 밸리데이터들이 공동 운영하는 Canton의 퍼블릭 조율(합의) 계층">글로벌 동기화자</abbr> 구현에 영향을 주는 기술 명세와 프로토콜 변경. Final 상태에 도달하기 전에 설계 문서와 레퍼런스 구현을 요구한다.
* **Governance** — <abbr class="gloss" title="글로벌 동기화자를 운영하고 네트워크 거버넌스에 참여하는 노드">슈퍼 밸리데이터</abbr> 권리, 투표 가중치, 기초 거버넌스 규칙(온체인 투표 절차 포함)을 정의·수정하는 제안.
* **Tokenomics** — 보상 구조, <abbr class="gloss" title="트랜잭션 수수료와 밸리데이터 보상에 쓰이는 네이티브 유틸리티 토큰(CC)">Canton Coin</abbr> 수수료, <abbr class="gloss" title="상태를 저장하지 않고 트랜잭션 합의·순서를 조율하는 Canton 구성요소">동기화자</abbr> 트래픽 가격에 대한 변경.
* **Process** — 워크플로·도구 조정, 또는 CIP 절차 자체에 관한 메타-CIP. 보통 커뮤니티 합의가 적용된다.
* **Informational** — 일반 설계 지침이나 권고. Informational CIP는 채택을 요구하지 않으며 구속력이 없다.

## CIP 생애주기

CIP는 정의된 단계 집합을 거친다:

* **Draft** — 작성자가 제안을 개발하고 `cip-discuss` 메일링 리스트에서 피드백을 모은다. 이 단계에서 CIP는 아직 공식 번호가 없다.
* **Proposed** — 두 슈퍼 <abbr class="gloss" title="파티를 호스팅하고 그 파티의 컨트랙트 데이터를 저장하는 참여자 노드">밸리데이터</abbr>의 후원을 확보한 후, 작성자가 CIP를 `cip-vote` 메일링 리스트에 정식 검토를 위해 제출한다. 이 시점에 CIP 편집자가 공식 번호를 부여한다.
* **Approved** — 10일 투표 창 동안 슈퍼 밸리데이터 권리 보유자의 2/3 다수 투표를 받는다.
* **Active** — 온체인 구현이 필요 없는 승인된 CIP(Process나 Informational CIP 등)의 경우, 승인 즉시 효력이 발생한다.
* **Final** — 온체인 채택이 필요한 승인된 CIP(보통 Standards Track, Governance, Tokenomics CIP)의 경우, 슈퍼 밸리데이터의 2/3가 변경을 온체인으로 구현하면 Final에 도달한다.

CIP는 정상 진행 외의 세 종료 상태 중 하나에 도달할 수도 있다: **Withdrawn**(작성자가 제안을 철회), **Deferred**(향후 검토로 연기), **Rejected**(2/3 투표 임계값 달성 실패). 후속 제안으로 대체된 CIP는 **Replaced**로 표시된다 — 예컨대 CIP-0073은 CIP-0096으로 대체되었다.

## 번호 규칙

작성자는 CIP 번호를 스스로 부여하지 않는다. 초안 단계에서는 서술적 별칭(예: `CIP-johndoe-token-lockup`)을 쓴다. 제안이 편집 검토를 통과하면 CIP 편집자가 공식 순차 번호를 부여한다. 번호는 네 자리 0-패딩 형식을 쓴다: CIP-0000, CIP-0056, CIP-0103 등. 번호는 엄격히 순차적이며 유형이나 범주 정보를 인코딩하지 않는다 — CIP의 유형은 번호가 아니라 서문(preamble) 메타데이터로 판단한다.

## 누가 CIP를 제안할 수 있나

대중의 누구나 CIP를 작성할 수 있다. [lists.sync.global](https://lists.sync.global/)에서 `cip-discuss` 메일링 리스트에 가입해 거기서 논의를 시작한다. 실무에서 CIP 작성자에는 슈퍼 밸리데이터 운영자, 애플리케이션 개발자, 생태계 기여자가 포함된다.

모든 변경에 CIP가 필요한 것은 아니다. 특정 소프트웨어 프로젝트의 작은 개선은 그 프로젝트 자체의 개발 워크플로를 거친다. 변경이 밸리데이터 간 상호운용성에 영향을 주거나, 거버넌스 규칙을 수정하거나, 토크노믹스 파라미터를 변경하거나, 여러 <abbr class="gloss" title="Canton에서 권한과 데이터 가시성의 주체가 되는 식별 가능한 참여 주체">파티</abbr>가 구현해야 하는 네트워크 전체 표준을 확립할 때 CIP가 필요하다. 의심스러우면 `cip-discuss` 리스트에서 논의를 시작하라 — 커뮤니티와 편집자가 형식 CIP가 정당한지 조언할 것이다.

논의에서 정식 투표로 넘어가려면 두 슈퍼 밸리데이터의 후원이 필요하다. 후원은 적어도 두 SV 운영자가 제안을 네트워크 전체 투표에 부칠 가치가 있다고 본다는 신호다. 제안 내용에 대한 지지를 의미하지는 않는다.

## 검토와 승인

CIP 편집자가 검토 과정을 관리한다. 그 책임에는 기술적 건전성 검증, 메일링 리스트에서 커뮤니티 논의가 일어났는지 확인, 형식 준수 검증, 공식 CIP 번호와 범주 부여가 포함된다. 편집자는 편집상 수정을 독립적으로 할 수 있지만 CIP 승인 여부는 결정하지 않는다 — 그 결정은 슈퍼 밸리데이터 투표에 속한다. 현재 편집팀은 [CIP-0000](https://github.com/global-synchronizer-foundation/cips/blob/main/cip-0000/cip-0000.md)에 나열되어 있다.

CIP가 투표로 넘어가기 전에, `cip-discuss` 메일링 리스트에서 최소 논의 기간이 적용된다:

* Standards Track: 3개월
* Governance와 Tokenomics: 각 1개월
* Process: 1개월
* Informational: 2주

이 최소 기간은 제안이 그 영향에 비례한 충분한 검토를 받도록 보장하기 위해 존재한다. 프로토콜 동작을 바꾸는 Standards Track CIP는 Informational 지침보다 긴 논의가 정당하다.

논의 기간이 지나고 두 슈퍼 밸리데이터가 제안 후원에 동의하면, GitHub Team Voting을 써서 `cip-vote` 리스트에서 투표가 진행된다. 투표 창은 10일간 지속된다. 승인에는 슈퍼 밸리데이터 권리 보유자의 2/3 다수 찬성이 필요하다.

## 온체인 거버넌스와의 관계

투표 절차를 통한 CIP 승인은 온체인 변경이 필요한 제안의 최종 단계가 아니다. CIP가 승인되면, 슈퍼 밸리데이터는 [SV 거버넌스 레퍼런스](sv-governance-reference.md)에 기술된 것과 같은 BFT 투표 메커니즘인 온체인 거버넌스 동작을 통해 그것을 채택해야 한다. CIP는 슈퍼 밸리데이터의 2/3가 변경을 온체인으로 구현한 후에만 Final 상태에 도달한다.

이 2단계 구조는 설계 합의(오프체인 CIP 투표)와 운영 약속(온체인 채택)을 분리해, 승인된 제안이 권위를 갖기 전에 실제로 배포되도록 보장한다. 온체인 구현 결과는 Canton Coin Scan API로 볼 수 있으므로, 슈퍼 밸리데이터 전반의 채택을 확인해 특정 CIP가 Final에 도달했는지 검증할 수 있다.

## CIP 문서 구조

CIP는 일관된 형식을 따라, 검토자가 제안을 효율적으로 평가하고 구현자가 필요한 정보를 찾을 수 있게 한다. 모든 CIP는 다음 섹션을 포함해야 한다:

* **서문(Preamble)** — 메타데이터 헤더: CIP 번호, 제목, 작성자, 상태, 유형, 날짜, 라이선스
* **초록(Abstract)** — 문제와 제안 해법의 약 200단어 요약
* **명세(Specification)** — 슈퍼 밸리데이터가 준수를 검증할 만큼 정확하게 쓰인 상세 기술·거버넌스 변경
* **동기(Motivation)** — 현재 상태가 왜 부족하고 제안이 무엇을 다루는지
* **근거(Rationale)** — 설계 결정, 고려한 트레이드오프, 기각한 대안
* **하위 호환성(Backwards Compatibility)** — (해당 시) 깨지는 변경과 마이그레이션 경로
* **레퍼런스 구현(Reference Implementation)** — Standards Track CIP가 Final에 도달하기 전에 필요
* **저작권(Copyright)** — 승인된 라이선스 하의 라이선싱 조건

CIP 저장소에는 시작점으로 쓸 수 있는 <abbr class="gloss" title="컨트랙트의 구조와 규칙(권한·초이스)을 정의하는 Daml 청사진">템플릿</abbr>이 있다. CIP 작성·제출의 단계별 과정은 아래 [CIP를 제안하는 방법](#cip를-제안하는-방법)을 참고하라.

## 주목할 만한 CIP

다음 CIP들은 이 절차가 다루는 주제 범위를 보여준다.

**[CIP-0056: Canton Network 토큰 표준](https://github.com/global-synchronizer-foundation/cips/blob/main/cip-0056/cip-0056.md)** (Standards Track, Final) — Canton Network의 토큰 연산을 위한 표준화된 6개 API를 정의하며, 메타데이터·보유·P2P 이전·인도-지불 정산을 다룬다. Canton Coin이 모든 표준 API를 구현한다. CIP-0056은 ERC-20의 아이디어를 가져오되 Canton의 UTXO 모델과 프라이버시 아키텍처에 맞게 조정했다. Canton Network에서 토큰을 만든다면, 이것이 구현해야 할 표준이다.

**[CIP-0078: Canton Coin 수수료 제거](https://github.com/global-synchronizer-foundation/cips/blob/main/cip-0078/cip-0078.md)** (Tokenomics, Final) — Canton Coin 이전에 대한 트랜잭션 수수료를 없앤다. 보유 수수료는 경제적으로 비현실적인 더스트 코인 누적을 막기 위해 코인 만료 시에만 남는다. 이 변경은 이전에 수수료 자금 로직을 요구하던 개발자 워크플로를 단순화했으며, MainNet 소각의 약 95%가 이미 이전 수수료가 아니라 트래픽 구매에서 비롯되었기에 실현 가능했다.

**[CIP-0073: 가중 밸리데이터 라이브니스 보상](https://github.com/global-synchronizer-foundation/cips/blob/main/cip-0073/cip-0073.md)** (Tokenomics, CIP-0096으로 대체) — 밸리데이터 라이브니스 보상을 임의 파티로 확장하고 거버넌스 조정 가능한 보상 가중치 승수를 도입했다. 이 CIP는 이후 보상 모델을 정제한 CIP-0096으로 대체되었다.

**[CIP-0103: dApp 표준](https://github.com/global-synchronizer-foundation/cips/blob/main/cip-0103/cip-0103.md)** (Standards Track, Approved) — 네트워크 연결성과 키 관리를 애플리케이션 로직과 분리하는 벤더 중립 dApp API를 명세한다. 동기·비동기 운영 모델을 모두 지원해 어떤 dApp이든 어떤 월렛 구현과도 작동하게 한다.

## 자원

* [GitHub의 CIP 저장소](https://github.com/global-synchronizer-foundation/cips) — 모든 CIP 문서와 정식 CIP-0000 절차 정의
* [CIP-0000: CIP 절차](https://github.com/global-synchronizer-foundation/cips/blob/main/cip-0000/cip-0000.md) — 편집팀, 투표 규칙, 형식 요건을 포함한 CIP 절차의 권위 있는 명세
* [CF 메일링 리스트](https://lists.sync.global/) — CIP 논의·투표가 일어나는 `cip-discuss`·`cip-vote` 리스트
* [SV 거버넌스 레퍼런스](sv-governance-reference.md) — 승인 후 CIP가 흘러드는 온체인 거버넌스 메커니즘

## CIP를 제안하는 방법

누구나 CIP를 작성할 수 있다. 제안이 Canton Network 표준의 일부로 받아들여지기 전에 여러 단계를 거친다:

1. **Draft** — 작성자가 제안을 쓰고 커뮤니티 검토에 제출
2. **Discussion** — 커뮤니티가 검토·토론하고 변경을 제안
3. **Review** — 피드백을 바탕으로 제안을 정제하고 정식 검토
4. **Acceptance** — 슈퍼 밸리데이터가 온체인 거버넌스로 제안에 투표
5. **Implementation** — 수락된 변경이 구축·배포

모든 CIP가 수락에 도달하지는 않는다. 제안은 작성자가 철회하거나, 향후 검토로 연기되거나, 슈퍼 밸리데이터 투표로 거부될 수 있다.

### CIP 작성

CIP는 [GitHub의 CIP 저장소](https://github.com/global-synchronizer-foundation/cips)에 풀 리퀘스트로 제출된다. 각 CIP는 자체 디렉토리에 존재한다(예: `cip-0056/cip-0056.md`).

CIP 문서는 다음 섹션을 포함해야 한다:

* **서문** — CIP 번호, 제목, 작성자, 상태, 유형, 생성일
* **초록** — 제안의 짧은(200단어 이하) 설명
* **동기** — 이 변경이 왜 필요하고, 어떤 문제를 풀고, 누가 이득을 보는지
* **명세** — 구현자가 작업할 수 있을 만큼 명확하게 쓰인 제안 변경의 정확한 기술 상세
* **근거** — 명세가 그렇게 설계된 이유, 고려·기각된 대안 포함
* **하위 호환성** — 변경이 기존 배포·<abbr class="gloss" title="원장에 기록되는 불변 데이터 단위. 상태 변경은 새 컨트랙트 생성으로 표현됨">컨트랙트</abbr>·통합에 미치는 영향
* **레퍼런스 구현** — (해당 시) 작동하는 구현의 링크나 설명
* **보안 고려사항** — 제안의 보안 함의

명세 섹션이 가장 중요하다. 두 독립 팀이 구현해 호환되는 결과에 도달할 만큼 모호하지 않고 완전해야 한다.

### CIP 유형

CIP는 일반적으로 다음 범주 중 하나에 속한다:

* **Standards track** — 상호운용성에 영향을 주는 네트워크 프로토콜, <abbr class="gloss" title="다자간 워크플로를 위해 설계된 Canton의 스마트 컨트랙트 언어">Daml</abbr> 패키지, API, 기타 명세에 대한 변경
* **Process** — CIP 절차 자체나 거버넌스 절차에 대한 변경
* **Informational** — 거버넌스 투표가 필요 없는 지침, 권고, 설계 근거

### 논의 단계

풀 리퀘스트 제출 후, 제안은 커뮤니티 논의에 들어간다. 이는 다음을 통해 일어난다:

* GitHub 풀 리퀘스트의 댓글
* [CIP 논의 메일링 리스트](https://lists.sync.global/g/cip-discuss)의 스레드
* 관련 Slack 채널(#gsf-global-synchronizer-appdev, #gsf-outreach)의 대화

작성자는 피드백을 예상하고 제안을 수정할 준비를 해야 한다. 흔한 피드백에는 더 정확한 명세 언어 요청, 하위 호환성 질문, 추가 보안 분석 제안이 포함된다.

논의 기간은 고정된 길이가 없다. 작성자와 커뮤니티가 제안이 잘 명세되었고 미해결 질문이 다뤄졌다는 대략적 합의에 도달하면 CIP가 정식 검토 준비가 된 것이다.

### 정식 검토와 수락

CIP가 충분히 성숙했다고 간주되면 정식 검토로 넘어간다. 이 단계에서:

1. CIP가 저장소에서 "Review" 상태로 표시된다.
2. 슈퍼 밸리데이터가 자신의 운영·비즈니스 요구에 대해 제안을 평가한다.
3. SV 웹 UI를 통해 거버넌스 투표가 개시된다. 수락에는 슈퍼 밸리데이터 정족수(온보딩된 SV의 약 2/3)의 승인이 필요하다.

투표가 통과하면 CIP 상태가 "Accepted"로 갱신되고 구현이 진행될 수 있다. 투표가 실패하면 작성자가 제안을 수정해 재제출하거나 철회할 수 있다.

### 수락 후

수락된 CIP는 Canton Network 표준의 일부가 된다. 구현은 다음을 수반할 수 있다:

* Splice 코드베이스([github.com/canton-network/splice](https://github.com/canton-network/splice)) 변경
* Canton 또는 Daml SDK 구성 요소 업데이트
* 슈퍼 밸리데이터 집합 전반에 조율된 구성 변경
* 표준 업그레이드 절차를 통해 배포되는 새 Daml 패키지

CIP 저장소는 각 수락된 제안의 구현 상태를 추적한다.

### 효과적인 제안을 위한 팁

* 아이디어가 이미 제안·다뤄지지 않았는지 확인하기 위해 [기존 CIP](https://github.com/global-synchronizer-foundation/cips)와 논의 아카이브를 먼저 검색하라.
* 커뮤니티와 일찍 대화하라. 전체 CIP를 쓰기 전에 논의 채널에서 아이디어를 띄우면 시간을 절약하고 제안을 개선할 수 있다.
* 명세 섹션에서 구체적이어라. 모호한 언어는 논의 연장과 지연을 부른다.
* 변경이 완전히 하위 호환된다고 믿더라도 하위 호환성을 명시적으로 다뤄라. 검토자가 물어볼 것이다.
* CIP와 함께 레퍼런스 구현을 작성하는 것을 고려하라. 작동하는 코드가 있는 제안은 검토를 더 빨리 통과하는 경향이 있다.

<!-- nav:start -->
---
<sub>⬅️ **이전**: [밸리데이터 노드 구성 요소](validator-node-components.md) ・ ➡️ **다음**: [학습 경로 선택](../../appdev/get-started/choose-your-path.md)</sub>
<!-- nav:end -->
