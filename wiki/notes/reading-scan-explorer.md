---
title: Scan 읽는 법 — 네트워크 익스플로러 화면 이해
type: note
translated: 2026-06-17
status: done
tags: [appdev, note, scan, 익스플로러, 운영, CC, 라운드]
---

> ⚠️ **내부 작성 정리 노트** — Canton 공식 문서의 충실 번역본이 아니라, LocalNet을 띄워 <abbr class="gloss" title="네트워크의 공개 통계·활동을 보여주는 익스플로러(블록 익스플로러의 Canton판)">Scan</abbr> UI를 직접 보며 학습한 내용을 정리한 노트입니다. 정확한 정의는 [용어집](../glossary.md)·[Canton Coin](../overview/canton-coin.md) 참고.

# Scan 읽는 법

**Scan = 네트워크 익스플로러** (블록체인의 블록 익스플로러에 해당하는 Canton판). 누가 봐도 되는 **공개 통계·활동**을 보여준다: <abbr class="gloss" title="글로벌 Synchronizer를 운영하고 네트워크 거버넌스에 참여하는 노드">슈퍼 밸리데이터</abbr>, <abbr class="gloss" title="탈중앙 Synchronizer 운영(Decentralized Synchronizer Operations) 파티. 슈퍼 밸리데이터들의 공동 거버넌스 주체">DSO</abbr>, CC(<abbr class="gloss" title="Canton Coin(CC)의 Daml/Scan상 기술적 이름. CC = Amulet">Amulet</abbr>) 발행, 라운드, 최근 활동.

> LocalNet 기준 주소: `http://scan.localhost:4000` · 데이터 출처 API: `http://scan.localhost:4000/api/scan/v0/...`

## 화면에서 보게 되는 핵심 항목

### 1. Super Validator / DSO
- **SV party**(`sv::…`): 이 네트워크의 슈퍼 <abbr class="gloss" title="파티를 호스팅하고 그 파티의 컨트랙트 데이터를 저장하는 참여자 노드">밸리데이터</abbr>. **LocalNet은 SV가 딱 1개**라 거버넌스를 혼자 결정(의결 임계치=1). MainNet이면 여러 SV가 나열되고 임계치도 커진다.
- **DSO party**(`DSO::…`): **D**ecentralized **S**ynchronizer **O**perations. SV들이 함께 운영하는 **거버넌스 주체**(법인격 같은 가상 <abbr class="gloss" title="Canton에서 권한과 데이터 가시성의 주체가 되는 식별 가능한 참여 주체">파티</abbr>). CC 발행량·수수료 규칙을 이 이름으로 정한다.

### 2. 마이닝 라운드(Mining Round) — CC 발행의 시간 단위
CC(<abbr class="gloss" title="트랜잭션 수수료와 밸리데이터 보상에 쓰이는 네이티브 유틸리티 토큰(CC)">Canton Coin</abbr>)는 한 번에 다 찍지 않고 **라운드마다** 발행·정산된다. ("마이닝"이지만 PoW 채굴이 아니라 **기여 비례 보상**.)

```
라운드 N:  열림(open) → 발행중(issuing) → 닫힘(closed)
            ↑거래 받음    ↑보상 계산        ↑정산·스냅샷 확정
```
- 매 라운드, 밸리데이터는 **자기가 처리한 일(<abbr class="gloss" title="Synchronizer에 쓰기를 요청할 때 소비하는 자원. Canton Coin으로 비용을 지불">트래픽</abbr> 등)에 비례해 CC 보상**을 받는다.
- "최신 라운드 = 3" → 3번째 주기 진행 중이라는 뜻.
- **closed rounds(닫힌 라운드)** 가 쌓여야 총 잔액 통계가 계산된다.

> ⚠️ **라운드 ≠ 블록 ≠ <abbr class="gloss" title="원장 상태를 바꾸는 원자적 작업 단위. 하나 이상의 컨트랙트를 생성·보관하며, 전부 적용되거나 전혀 적용되지 않음">트랜잭션</abbr>.** 라운드는 **CC 발행 정산 주기(시간 구간)** 일 뿐이다. 한 라운드 안에 여러 트랜잭션이 들어가고, 트랜잭션은 라운드와 무관하게 **개별·즉시 확정**된다. (블록은 <abbr class="gloss" title="Synchronizer 구성요소. 암호화된 메시지에 전체 순서·타임스탬프를 부여하고 참여자에게 전달">시퀀서</abbr> 순서화 계층에 별도로 존재 → [ISS 노트](iss-consensus.md)의 "시퀀서 블록 vs 전통 블록")

#### 집계(결산)는 언제? — "틱(tick)"과 "라운드 수명"은 다르다 (헷갈림 주의)
- **tickDuration(예: 10분)** = 라운드 *번호가 하나 오르는* 간격. (round 4→5→6이 10분 간격으로 열림)
- 하지만 **한 라운드의 수명은 약 2틱(~20분)**: `열림(open, ~10분) → 발행중(issuing, ~10분) → 닫힘(closed)`.
- 그래서 "최신 라운드"가 6이어도, *가장 오래된* 라운드가 닫힐 때까지는 **closed=0**일 수 있다.
- 실측 예(LocalNet): round 1이 02:03 열림 → **02:23 닫힘 예정**. 즉 네트워크 시작 후 **20분 남짓** 지나야 첫 closed가 생기고 총 잔액이 채워진다.
- 결산은 **SV 자동화가 자동으로** 수행한다. 사람이 할 일 없음 — 시간이 지나면 `scan-status.py`의 `닫힌 라운드`가 0→1→2…로 오른다.

> ⚠️ "tickDuration 10분"을 "10분이면 집계됨"으로 오해하기 쉽다. 10분은 *틱*이고, 라운드가 **닫히기까지는 약 2틱**이 걸린다.

#### 보상은 누가 받나 — 활동 피드의 "밸리데이터 보상"이 여러 파티에 찍히는 이유
- LocalNet엔 밸리데이터(<abbr class="gloss" title="파티를 호스팅하고 그 파티의 컨트랙트를 저장·실행하는 노드. 밸리데이터의 핵심 구성요소">참여자 노드</abbr>)가 **여러 개**다: SV의 밸리데이터, app-provider의 밸리데이터, app-user의 밸리데이터.
- 매 라운드 **각 밸리데이터가 *자기* 보상을 따로 수령**한다 → 활동 피드에 app-provider·app-user·SV가 *각각* "Transfer(보상 수령, self)"로 찍힌다. (한 보상을 셋이 나누는 게 아니라, 셋이 각자 받는 것)
- 보상 구성: **밸리데이터 보상**(처리한 일 비례) + **밸리데이터 faucet**(DevNet·LocalNet에서 *살아있기만 해도* 주는 가동 보상). SV는 여기에 **SV 보상**까지 더해져 잔액이 압도적으로 크다.
- 이 "Transfer"들은 receivers가 비어있는 **self-transfer**(자기 보상을 자기 잔액에 합치는 정리 거래)다.

### 3. 총 CC(Amulet) 잔액
- <abbr class="gloss" title="다자간 워크플로를 위해 설계된 Canton의 스마트 컨트랙트 언어">Daml</abbr>/Scan에서 **Canton Coin의 기술적 이름이 Amulet**이다 (CC = Amulet).
- "Could not retrieve total amulet balance" 메시지는 **에러가 아니라**, **닫힌 라운드가 0개**라 스냅샷이 아직 없을 때 나온다(갓 띄운 LocalNet). 라운드가 몇 개 닫히면 자동으로 채워진다.

### 4. 최근 활동(Activity) 피드
부팅 직후 자주 보이는 활동 종류:

| 화면 표시 | API 타입 | 뜻 |
|---|---|---|
| **<abbr class="gloss" title="DevNet·LocalNet에서 테스트용 CC를 무료로 받는 동작(수도꼭지/faucet). MainNet엔 없음">Tap</abbr>** | `devnet_tap` | **무료 CC 받기(수도꼭지/faucet)**. DevNet·LocalNet에서만 가능 — 테스트용 CC를 "탭"해 받는다. **MainNet엔 없음**(거기선 실제로 벌어야 함). |
| **Automation** | SV 자동화 | 네트워크 **자동 관리 작업** — 라운드 열고/닫기, 보상 수거 등 백그라운드 봇이 수행. |
| **Transfer** | `transfer` | 파티 간 CC 이동(송금). |

## "내가 아무것도 안 했는데 왜 활동이 있지?"
`make start` 한 번이 두 종류의 자동 작업을 깨운다:
1. **초기 온보딩(1회성)** — `splice-onboarding`·`register-app-user-tenant` 컨테이너가 스크립트를 자동 실행해 파티 생성·테스트 CC Tap·테넌트 등록을 한다(→ 피드의 tap/transfer).
2. **SV 자동화(상시)** — SV 노드 안의 봇이 멈추지 않고 라운드를 굴리고 정산한다(→ Automation, 라운드 번호 자동 증가).

> 핵심: Canton 네트워크는 **사람이 트랜잭션을 안 넣어도 SV가 시간(라운드)을 굴리며 스스로 유지**된다. 가만히 둬도 라운드가 닫히고 잔액 통계가 채워지는 이유.

## 관련 문서
- [Canton Coin](../overview/canton-coin.md) — CC 발행·트래픽·라운드의 공식 설명
- [Canton 환경 4단계](canton-environments-localnet-to-mainnet.md) — LocalNet에서만 Tap이 되는 이유(환경 차이)
- [Synchronizer 종류](synchronizer-types-private-consortium-global.md) · [용어 한 컷 카드](term-cheatsheet.md)

<!-- nav:start -->

---

⬅️ **이전**: [파티는 유저마다 만들까? — per-user vs 옴니버스](party-design-per-user-vs-omnibus.md) ・ ➡️ **다음**: [Synchronizer 종류 — 사설 vs 컨소시엄 vs 글로벌](synchronizer-types-private-consortium-global.md)

<!-- nav:end -->
