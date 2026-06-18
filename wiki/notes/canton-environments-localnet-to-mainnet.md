---
title: Canton 환경 4단계 — LocalNet → DevNet → TestNet → MainNet
type: note
translated: 2026-06-16
status: done
tags: [appdev, 정리, note, 환경, 배포, 온보딩]
---

> ⚠️ **내부 작성 정리 노트** — Canton 공식 문서의 충실 번역본이 아니라, 학습을 돕기 위해 직접 작성한 배경 설명입니다. 사실관계는 아래 참고 링크로 <abbr class="gloss" title="이해관계자 밸리데이터가 트랜잭션이 유효함을 미디에이터에 응답하는 것(confirmation)">확인</abbr>하세요.

# Canton 환경 4단계 — LocalNet → DevNet → TestNet → MainNet

"테스트넷을 로컬에서 돌리나?" 같은 질문이 자주 나온다. 답은 **"로컬 테스트는 LocalNet으로 하고, TestNet은 로컬이 아니라 연결하는 공유망"** 이다.

## 한눈에 비교

| 환경 | 무엇 | 로컬에서? | 붙는 절차 |
|---|---|---|---|
| **LocalNet** | 내 PC에 띄우는 **시뮬레이션 네트워크**(Docker) | ✅ 완전 로컬 | 없음 — 혼자 띄움 |
| **DevNet** | 공유 **개발 스테이징**망 | ❌ 연결 | 온보딩 필요(승인 X, IP allowlist O) |
| **TestNet** | 공유 **프로덕션 스테이징**망 | ❌ 연결 | 온보딩 + **토크노믹스 위원회 승인** |
| **MainNet** | **프로덕션**(실제 운영) | ❌ 연결 | 가장 엄격 |

> **로컬 = LocalNet**, **공유망 = DevNet/TestNet/MainNet**. TestNet 자체를 로컬에 띄우는 게 아니라, 내 <abbr class="gloss" title="파티를 호스팅하고 그 파티의 컨트랙트 데이터를 저장하는 참여자 노드">밸리데이터</abbr>를 그 망에 *연결*한다.

## 왜 공유망은 "절차"가 필요한가

기술적으로 못 붙는 게 아니라(내 PC/서버의 밸리데이터로 연결 가능), **온보딩 승인·등록**을 거쳐야 한다. LocalNet은 이 절차가 전혀 없다.

### 공유망 온보딩 절차

1. **CF 밸리데이터 요청 양식** 제출 → `https://sync.global/validator-request/`
2. (TestNet/MainNet) **토크노믹스 위원회 승인** — DevNet은 이 단계 불필요
3. 내 밸리데이터의 **egress IP**를 **후원 SV(<abbr class="gloss" title="글로벌 Synchronizer를 운영하고 네트워크 거버넌스에 참여하는 노드">슈퍼 밸리데이터</abbr>)** 에게 전달 → 후원 SV가 **SV 집합이 유지하는 allowlist에 등록**
4. **SV 다수가 갱신된 allowlist 채택**(보통 2~7일) → **일회성 온보딩 시크릿**(48시간 내 만료) 수령
5. 온보딩 시크릿으로 밸리데이터 배포 + 후원 SV로부터 받은 **VPN 연결 정보**로 접속

### IP allowlist 핵심
- **등록 장소** = 슈퍼 밸리데이터들이 **공동 유지하는 allowlist** (내가 직접 편집하는 콘솔이 아님)
- **등록 창구** = 나를 후원하는 **SV** (egress IP를 SV에게 주면 SV가 올려줌)
- **네트워크당 IP 1개**만 허용, **DevNet·TestNet·MainNet에서 서로 구별되는 IP**여야 함
- DevNet도 위원회 승인은 없지만 **IP allowlist 등록은 필요**

## 하드웨어 요구사항

| 환경/용도 | 노드 | DB |
|---|---|---|
| **LocalNet(개발·PoC)** | Docker에 **RAM 8GB+** 할당 가능한 일반 노트북, 디스크 여유 (16GB면 여유) | (단일 PostgreSQL 포함) |
| **운영 밸리데이터(활동 적음)** | CPU 2코어 · **RAM 8GB** | 2코어 · 4GB · 디스크 10GB |
| **운영 밸리데이터(앱 제공자, 중간 활동)** | CPU 2코어 · **RAM 16GB** | 2코어 · 4GB · 디스크 **100GB** |

- **DB 지연(latency)에 민감** → 관리형 DB를 노드와 **같은 리전·존**에 둔다.
- "실제 요구치는 사용량에 따라 달라짐" → 운영 중 CPU·메모리·디스크 **모니터링하며 조정**.
- 소프트웨어(Canton·<abbr class="gloss" title="글로벌 Synchronizer를 구동하는 오픈소스 애플리케이션 모음(SV·밸리데이터·월렛 등)">Splice</abbr>)는 **오픈소스(무료)** — Docker 이미지/cn-quickstart로 받음. 비용은 *글로벌 <abbr class="gloss" title="Synchronizer에 쓰기를 요청할 때 소비하는 자원. Canton Coin으로 비용을 지불">트래픽</abbr>(CC)·서버 운영비*뿐.
- ⚠️ 위는 **밸리데이터** 기준. **슈퍼 밸리데이터/<abbr class="gloss" title="상태를 저장하지 않고 트랜잭션 합의·순서를 조율하는 Canton 구성요소">Synchronizer</abbr> 노드(<abbr class="gloss" title="Synchronizer 구성요소. 암호화된 메시지에 전체 순서·타임스탬프를 부여하고 참여자에게 전달">시퀀서</abbr>·<abbr class="gloss" title="Synchronizer 구성요소. 이해관계자들의 확인을 모아 트랜잭션 승인/거부를 판정">미디에이터</abbr>)** 는 <abbr class="gloss" title="여러 노드가 트랜잭션의 유효성·순서에 함께 동의하는 절차">합의</abbr> 부하로 더 크며, 값은 deployment 문서 별도 절 참고. (출처: [Validator 배포 Prerequisites](https://docs.canton.network/global-synchronizer/deployment/prerequisites))

## 권장 개발 흐름

```
LocalNet (내 PC, 매일 개발·단위 테스트 — 절차 없음)
   → DevNet (공유 개발망, 다른 노드와 통합 테스트 — 붙기 가장 쉬움)
   → TestNet (프로덕션 스테이징, 출시 전 검증 — 승인 필요)
   → MainNet (실제 운영)
```

대부분의 개발은 **LocalNet에서 끝내고**, 다른 기관과의 상호운용·실환경 검증이 필요할 때만 **DevNet → TestNet** 으로 올린다.

## 멀티체인 B2B 정산 맥락
- Canton 쪽 검증은 **LocalNet에서 대부분** 처리.
- 실제 기관 간 연동 테스트가 필요해지면 **DevNet**부터(붙기 쉬움), 출시 직전엔 **TestNet**.
- (실제 배포 설계는 미확정이므로 참고용)

## 참고 링크
- [사전 요구사항·설치](../appdev/quickstart/prerequisites.md) — LocalNet 설치, 공유망 연결, DevNet 접근
- [모듈 5 — LocalNet 개발](../appdev/modules/m5-localnet-development.md) — LocalNet 구조·운영
- [Canton Foundation 정책](../overview/reference/gsf-policies.md) — 밸리데이터 온보딩·allowlist·네트워크 정책

<!-- nav:start -->

---

⬅️ **이전**: [Canton의 B2B vs B2C — 어디에 맞나 (적합성·쓰임새)](canton-b2b-vs-b2c.md) ・ ➡️ **다음**: [Canton vs Splice — 엔진 vs 운영 소프트웨어](canton-vs-splice.md)

<!-- nav:end -->
