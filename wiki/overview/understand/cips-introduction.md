---
title: Canton 개선 제안 (CIP) 소개
source: https://docs.canton.network/overview/understand/cips-introduction
translated: 2026-06-15
status: done
tags: [overview, understand, 거버넌스, CIP]
---

> **출처(원문)**: [Canton Improvement Proposals (CIPs)](https://docs.canton.network/overview/understand/cips-introduction) · 번역일 2026-06-15

## 📌 개발자 노트
- **한 줄 요약**: <abbr class="gloss" title="Canton 개선 제안(Canton Improvement Proposal). 네트워크 규칙·표준 변경을 제안·비준하는 절차">CIP</abbr>는 Canton Network에 변경·표준·개선을 제안하는 공식 메커니즘. CIP 유형, 핵심 CIP(CIP-0056 토큰 표준), 생애주기, 제안 주체, 구현·기여 방법.
- **핵심 용어**: CIP(Canton 개선 제안), Standards Track/Process/Informational, CIP-0056 토큰 표준, Holding/Transfer/Lock 인터페이스
- **선행 개념**: [글로벌 Synchronizer](global-synchronizer.md). 다음 → [앱 피처드 되기](getting-app-featured.md)

---

# Canton 개선 제안 (CIP)

> Canton Network 표준·거버넌스를 위한 CIP 절차 소개

Canton 개선 제안(Canton Improvement Proposals, CIP)은 Canton Network에 변경·표준·개선을 제안하는 공식 메커니즘이다.

## CIP란?

CIP는 Canton 커뮤니티에 정보를 제공하는 설계 문서로, Canton Network을 위한 새 기능·절차·표준을 기술한다.

| CIP 유형 | 목적 |
| --- | --- |
| **Standards Track** | 기술 명세와 표준 |
| **Process** | 거버넌스·운영 절차 |
| **Informational** | 일반 지침과 정보 |

## CIP가 중요한 이유

CIP는 다음을 보장한다:

* 변경이 구현 전에 공개적으로 논의됨
* 표준이 상호운용성을 가능하게 함
* 커뮤니티가 네트워크 진화에 의견을 냄
* 결정이 투표되고 이후 참조용으로 문서화됨

## 핵심 CIP

### CIP-0056: Canton Network 토큰 표준

토큰 표준은 Canton Network의 대체 가능(fungible) 토큰을 위한 인터페이스를 정의한다.

| 측면 | 명세 |
| --- | --- |
| **목적** | 토큰 연산 표준화 |
| **인터페이스** | Holding, Transfer, Lock |
| **상호운용성** | 월렛·앱 호환성 |

**GitHub:** [CIP-0056](https://github.com/global-synchronizer-foundation/cips/blob/main/cip-0056/cip-0056.md)

주요 기능:

* 표준 보유(holding) 표현
* 일관된 이전(transfer) 의미론
* 고급 워크플로를 위한 사전 승인(pre-approval) 지원
* 다단계 이전을 위한 할당(allocation) 패턴

## CIP 절차

### 생애주기

| 단계 | 설명 |
| --- | --- |
| **Draft(초안)** | 논의를 위한 초기 제안 |
| **Review(검토)** | 커뮤니티 검토와 피드백 |
| **Accepted(수락)** | 구현 승인됨 |
| **Final(최종)** | 구현되고 안정됨 |
| **Rejected(거부)** | 수락되지 않음 (근거와 함께) |

### 누가 제안할 수 있나

CIP는 다음이 제안할 수 있다:

* <abbr class="gloss" title="글로벌 Synchronizer를 운영하고 네트워크 거버넌스에 참여하는 노드">슈퍼 밸리데이터</abbr>
* 커뮤니티 구성원
* 개발팀
* 생태계 참여자

## CIP 구현

### 애플리케이션 개발자용

애플리케이션을 구축할 때 관련 CIP를 고려하라:

| 상황 | 조치 |
| --- | --- |
| **토큰 생성** | CIP-0056 인터페이스 구현 |
| **월렛 통합** | 표준 인터페이스 지원 |
| **상호운용성** | 공개된 표준 준수 |

### 예시: 토큰 표준 구현

```haskell
-- Implement CIP-0056 holding interface
template MyToken
  with
    issuer : Party
    holder : Party
    amount : Decimal
  where
    signatory issuer
    observer holder

    -- Standard interface implementation
    interface instance Holding.I for MyToken where
      view = Holding.View with ...
```

## CIP 찾기

| 자원 | 내용 |
| --- | --- |
| [GitHub 저장소](https://github.com/global-synchronizer-foundation/cips) | 모든 CIP 문서 |
| [canton.foundation](https://canton.foundation) | 거버넌스 정보 |
| 커뮤니티 채널 | 논의와 업데이트 |

## CIP에 기여하기

CIP를 제안하거나 기여하려면:

1. 형식을 이해하기 위해 **기존 CIP 검토**
2. 커뮤니티 채널에서 **비공식 논의**
3. CIP <abbr class="gloss" title="컨트랙트의 구조와 규칙(권한·초이스)을 정의하는 Daml 청사진">템플릿</abbr>을 따라 **초안 작성**
4. 적절한 절차를 통해 **검토 제출**
5. 피드백을 바탕으로 **반복**

## 다음 단계

* **[토큰 표준](https://github.com/global-synchronizer-foundation/cips/blob/main/cip-0056/cip-0056.md)** — Canton 토큰 표준 구현.
* **[CIP 저장소](https://github.com/global-synchronizer-foundation/cips)** — GitHub에서 모든 CIP 둘러보기.

<!-- nav:start -->

---

⬅️ **이전**: [Canton의 해법 — 세 가지 기둥](cantons-solution.md) ・ ➡️ **다음**: [핵심 개념](core-concepts.md)

<!-- nav:end -->
