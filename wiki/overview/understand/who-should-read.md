---
title: 누가 이 문서를 읽어야 하나
source: https://docs.canton.network/overview/understand/who-should-read
translated: 2026-06-15
status: done
tags: [overview, understand, 입문]
---

> **출처(원문)**: [Who Should Use This Documentation](https://docs.canton.network/overview/understand/who-should-read) · 번역일 2026-06-15

## 📌 개발자 노트
- **한 줄 요약**: 역할(앱 개발자/블록체인 개발자/노드 운영자/솔루션 아키텍트)과 목표별로 Canton 문서의 알맞은 시작점을 안내하는 길잡이 페이지.
- **핵심 용어**: <abbr class="gloss" title="다자간 워크플로를 위해 설계된 Canton의 스마트 컨트랙트 언어">Daml</abbr>, Ledger API, <abbr class="gloss" title="파티를 호스팅하고 그 파티의 컨트랙트 데이터를 저장하는 참여자 노드">밸리데이터</abbr>(Validator), <abbr class="gloss" title="상태를 저장하지 않고 트랜잭션 합의·순서를 조율하는 Canton 구성요소">동기화자</abbr>(Synchronizer)
- **선행 개념**: [Canton Network이란?](what-is-canton.md). 다음 → [Canton이 푸는 문제](the-problem.md)

---

# 누가 이 문서를 읽어야 하나

> 역할과 목표에 맞는 시작점을 찾으세요

이 문서는 Canton Network 위에서 무언가를 만들거나 운영하는 여러 독자를 대상으로 한다. 아래에서 자신의 경로를 찾자.

## 역할별 (By Role)

**[애플리케이션 개발자](https://docs.canton.network/appdev/get-started/choose-your-path)**
Daml 스마트 <abbr class="gloss" title="원장에 기록되는 불변 데이터 단위. 상태 변경은 새 컨트랙트 생성으로 표현됨">컨트랙트</abbr>와 Ledger API를 사용해 Canton Network 위에 애플리케이션을 구축한다.
다음을 하고 싶다면 여기서 시작:
* Daml로 스마트 컨트랙트 작성
* 원장과 상호작용하는 프론트엔드·백엔드 구축
* 애플리케이션 설계를 위한 Canton의 프라이버시 모델 이해

**[Ethereum/Web3 개발자](https://docs.canton.network/appdev/modules/m2-canton-for-ethereum-devs)**
기존 블록체인 지식을 Canton 개념과 패턴으로 옮긴다.
다음에 해당하면 여기서 시작:
* Solidity, EVM 또는 다른 블록체인 플랫폼 경험이 있음
* Canton이 전통적 블록체인과 어떻게 다른지 이해하고 싶음
* 기존 멘탈 모델을 적응시켜야 함

**[노드 운영자](https://docs.canton.network/global-synchronizer/understand/introduction)**
<abbr class="gloss" title="슈퍼 밸리데이터들이 공동 운영하는 Canton의 퍼블릭 조율(합의) 계층">글로벌 동기화자</abbr>에서 밸리데이터 인프라를 운영한다.
다음을 하고 싶다면 여기서 시작:
* 밸리데이터 노드 배포·운영
* 인프라 요구사항 이해
* 운영자로서 Canton Network 참여

**[솔루션 아키텍트](https://docs.canton.network/overview/understand/five-minute-overview)**
엔터프라이즈 활용 사례를 위해 Canton을 평가한다.
다음이 필요하면 여기서 시작:
* Canton의 아키텍처 접근 방식 이해
* 프라이버시가 중요한 애플리케이션에 대한 적합성 평가
* Canton을 다른 블록체인 솔루션과 비교

## 목표별 (By Goal)

| 하고 싶은 것... | 시작점 |
| --- | --- |
| 5분 만에 Canton이 무엇인지 이해 | [5분 개요](https://docs.canton.network/overview/understand/five-minute-overview) |
| 블록체인에 프라이버시가 왜 중요한지 학습 | [Canton이 푸는 문제](the-problem.md) |
| Canton 구성 요소가 함께 작동하는 방식 보기 | [아키텍처 개요](https://docs.canton.network/overview/learn/architecture) |
| 첫 스마트 컨트랙트 작성 | [모듈 3: Daml 스마트 컨트랙트](https://docs.canton.network/appdev/modules/m3-dev-environment) |
| 예제 애플리케이션 실행 | [QuickStart](https://docs.canton.network/appdev/quickstart) |
| 밸리데이터 노드 배포 | [밸리데이터 설정](https://docs.canton.network/global-synchronizer/understand/introduction) |
| 앱에 월렛 통합 | [통합 개요](https://docs.canton.network/integrations/overview) |

## 문서 구조

이 문서는 네 개 섹션으로 구성된다:

* **Overview(개요)**: Canton 개념, 아키텍처, 프로토콜 — 모두를 위한 내용
* **App Development(앱 개발)**: Daml과 API로 애플리케이션 구축 — 개발자용
* **Global Synchronizer(글로벌 동기화자)**: 밸리데이터·인프라 운영 — 운영자용
* **Building Blocks(빌딩 블록)**: 월렛, 앱, 구성 요소, 통합 — 개발자·사용자용

각 섹션 안에서 내용은 점진적 깊이 모델을 따른다:

* **Understand(이해)**: 모두를 위한 개념적 토대
* **Learn(학습)**: 실무 적용을 포함한 더 상세한 이해
* **Reference(레퍼런스)**: 심층 프로토콜 메커니즘과 API 문서

## 사전 요구사항

본격적으로 시작하기 전에 다음을 갖추면 좋다:

* **개발자**: 임의의 언어로의 프로그래밍 경험. 함수형 프로그래밍 개념에 익숙하면 도움이 되지만 필수는 아님.
* **운영자**: 컨테이너 기반 배포(Docker, Kubernetes) 경험과 기본 네트워킹 개념.
* **모두**: 블록체인 사전 경험 불필요. 개념을 처음 원리부터 설명한다.

## 도움 받기

* **[커뮤니티 Slack](https://docs.canton.network/shared/support-channels)**: 개발자·운영자 커뮤니티 채널에 참여.
* **[지원(Support)](https://docs.canton.network/shared/support-channels)**: 엔터프라이즈 지원은 Digital Asset 지원팀에 문의.

<!-- nav:start -->
---
<sub>⬅️ **이전**: [Canton Network이란?](what-is-canton.md) ・ ➡️ **다음**: [아키텍처 개요](../learn/architecture.md)</sub>
<!-- nav:end -->
