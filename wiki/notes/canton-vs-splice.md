---
title: Canton vs Splice — 엔진 vs 운영 소프트웨어
type: note
translated: 2026-06-16
status: done
tags: [개요, 정리, note, splice, 글로벌Synchronizer]
---

> ⚠️ **내부 작성 정리 노트** — Canton 공식 문서의 충실 번역본이 아니라, 학습을 돕기 위해 직접 작성한 배경 설명입니다. 사실관계는 아래 참고 링크로 <abbr class="gloss" title="이해관계자 밸리데이터가 트랜잭션이 유효함을 미디에이터에 응답하는 것(confirmation)">확인</abbr>하세요.

# Canton vs Splice — 엔진 vs 운영 소프트웨어

"<abbr class="gloss" title="글로벌 Synchronizer를 구동하는 오픈소스 애플리케이션 모음(SV·밸리데이터·월렛 등)">Splice</abbr>"가 자주 나오는데 Canton과 뭐가 다른지 헷갈린다. 한 번 정리.

## 한 줄 차이

> **Canton = 기반 프로토콜(엔진)** · **Splice = 그 위에서 공개 <abbr class="gloss" title="슈퍼 밸리데이터들이 공동 운영하는 Canton의 퍼블릭 조율(합의) 계층">글로벌 Synchronizer</abbr>를 운영·재정·거버넌스하는 오픈소스 앱 묶음.**

| | Canton (프로토콜) | Splice (애플리케이션) |
|---|---|---|
| 무엇 | <abbr class="gloss" title="거래·컨트랙트가 기록되는 장부. Canton에선 활성 컨트랙트의 모음">원장</abbr>·<abbr class="gloss" title="여러 노드가 트랜잭션의 유효성·순서에 함께 동의하는 절차">합의</abbr>·프라이버시 **기반 프로토콜** (<abbr class="gloss" title="다자간 워크플로를 위해 설계된 Canton의 스마트 컨트랙트 언어">Daml</abbr>, <abbr class="gloss" title="파티를 호스팅하고 그 파티의 컨트랙트를 저장·실행하는 노드. 밸리데이터의 핵심 구성요소">참여자 노드</abbr>, <abbr class="gloss" title="상태를 저장하지 않고 트랜잭션 합의·순서를 조율하는 Canton 구성요소">Synchronizer</abbr> 프로토콜) | 그 위에 얹혀 **공개 네트워크를 운영**하는 Daml 앱 묶음 (Hyperledger Labs 산하 오픈소스) |
| 비유 | 자동차 **엔진** | 그 엔진으로 운수회사를 **운영하는 소프트웨어** |

Canton 프로토콜만으로는 "공개 네트워크"가 안 굴러간다. **누가 수수료를 내고(토큰), 운영자에게 보상하고, 거버넌스로 결정하고, 지갑·익스플로러를 제공하느냐** — 이 "운영 살림살이"를 Splice가 채운다. Splice는 **Canton 위에 만들어진 Daml 앱**이다.

## Splice가 포함하는 것

| 구성 요소 | 역할 |
|---|---|
| **<abbr class="gloss" title="트랜잭션 수수료와 밸리데이터 보상에 쓰이는 네이티브 유틸리티 토큰(CC)">Canton Coin</abbr>** | 네이티브 토큰 구현(수수료·보상). Daml <abbr class="gloss" title="컨트랙트의 구조와 규칙(권한·초이스)을 정의하는 Daml 청사진">템플릿</abbr> `Amulet` |
| **Validator App** | <abbr class="gloss" title="파티를 호스팅하고 그 파티의 컨트랙트 데이터를 저장하는 참여자 노드">밸리데이터</abbr> 노드 관리 |
| **Wallet** | CC용 사용자 월렛 |
| **<abbr class="gloss" title="네트워크의 공개 통계·활동을 보여주는 익스플로러(블록 익스플로러의 Canton판)">Scan</abbr>** | 네트워크 익스플로러 |
| **Governance** | 투표·제안 관리 |
| **토큰 표준(<abbr class="gloss" title="Canton 개선 제안(Canton Improvement Proposal). 네트워크 규칙·표준 변경을 제안·비준하는 절차">CIP</abbr>-0056)** | 토큰 만들기 표준 인터페이스 |

→ LocalNet/QuickStart에서 본 **월렛·Scan·SV 앱**이 전부 Splice 구성요소다.

## 자주 헷갈리는 점

- **"Canton Coin은 Splice를 통해 구현된다"** = CC는 별도 블록체인이 아니라 **Splice 안의 Daml 토큰(`Amulet`)**. 즉 "Splice가 Canton 위에 구현한 토큰 앱".
- **글로벌 Synchronizer** = Canton의 Synchronizer 프로토콜을 **Splice로 운영·재정·거버넌스**해 공개망으로 만든 것. (Synchronizer 프로토콜=Canton, 그걸 공개 운영하는 살림=Splice)

## 한 줄 정리

> **Canton(엔진) 위에서 공개 글로벌 Synchronizer를 굴리는 운영 소프트웨어 묶음 = Splice.** 토큰·월렛·Scan·거버넌스가 전부 Splice이고, Canton Coin도 그 일부다.

## 참고 링크
- [글로벌 Synchronizer](../overview/understand/global-synchronizer.md) — Splice 애플리케이션 구성·거버넌스
- [CIP-0056 토큰 표준](../overview/reference/cip-0056.md) — Splice가 포함하는 토큰 표준(<abbr class="gloss" title="Canton Coin(CC)의 Daml/Scan상 기술적 이름. CC = Amulet">Amulet</abbr>)
- [Canton Coin 토크노믹스](../overview/reference/canton-coin-tokenomics.md) — CC 경제

<!-- nav:start -->

---

⬅️ **이전**: [Canton 환경 4단계 — LocalNet → DevNet → TestNet → MainNet](canton-environments-localnet-to-mainnet.md) ・ ➡️ **다음**: [ClearToken vs Musubi — 같은 Canton DvP, 정반대 포지셔닝](cleartoken-vs-musubi.md)

<!-- nav:end -->
