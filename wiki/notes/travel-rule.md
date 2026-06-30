---
title: 트래블룰 (Travel Rule) — 규제 개요와 구현 방식(다른 곳은 어떻게 하나)
type: note
translated: 2026-06-30
status: done
tags: [정리, note, 규제, 컴플라이언스, VASP, 트래블룰, AML]
---

> ⚠️ **내부 작성 정리 노트** — Canton 공식 문서의 충실 번역본이 아니라, "<abbr class="gloss" title="FATF 권고 16의 가상자산 적용 — 일정액 이상 이전 시 송신·수신 VASP가 송금인·수취인 신원을 교환·기록해야 하는 규제">트래블룰</abbr>이 뭐고 다른 곳에선 어떻게 구현돼 있나"를 조사해 정리한 배경 설명입니다. 사실관계·수치는 아래 [출처](#출처-참고)로 <abbr class="gloss" title="이해관계자 밸리데이터가 트랜잭션이 유효함을 미디에이터에 응답하는 것(confirmation)">확인</abbr>하세요. 정확한 용어 정의는 [용어집](../glossary.md) 참고.

# 트래블룰 (Travel Rule)

## 한 줄

**<abbr class="gloss" title="국제자금세탁방지기구 — 자금세탁·테러자금조달 방지(AML/CFT) 국제 표준을 만드는 정부간 기구">FATF</abbr> 권고 16(Recommendation 16)을 가상자산에 적용한 규제.** 일정 금액 이상을 이전할 때, **송신 <abbr class="gloss" title="가상자산사업자(Virtual Asset Service Provider) — 거래소·커스터디 등 가상자산을 취급하는 규제 대상 사업자">VASP</abbr>와 수신 VASP가 송금인·수취인의 검증된 신원정보를 서로 주고받아야** 한다. 전통 은행 전신송금(wire transfer)에 붙던 의무를 가상자산으로 확장한 것.

---

## 1. 무엇이고 왜 있나

- **출처 규범**: FATF(국제자금세탁방지기구) 권고 16 — 원래 은행 전신송금의 "송금인 정보 동행" 규칙을 가상자산(VA) 이전으로 확장.
- **목적**: 익명 이전을 막아 자금세탁·테러자금조달(AML/CFT)을 추적 가능하게.
- **적용 대상**: VASP(가상자산사업자) — 거래소·<abbr class="gloss" title="자산·키를 대신 보관·관리해 주는 수탁 서비스. 자기 보관, 서드파티(MPC), 노드월렛 등">커스터디</abbr>·일부 지갑 사업자. 개인 간 자기수탁 이전은 직접 대상이 아니나(6절), VASP가 끼면 의무가 생긴다.
- **임계값**(이상이면 의무):
  - FATF 권장: **USD/EUR 1,000**
  - EU **TFR**(Transfer of Funds Regulation): **2026년 임계값 0** — 사실상 전액
  - 한국: **100만원**(약 USD 820)
- **현황**: 2024년 65개 → 현재 85개 관할권이 입법(진행 포함), 70여 곳 집행 중.
- **sunrise issue**(일출 문제): 관할권마다 시행 시점이 달라, 한쪽 VASP만 의무이고 상대는 아닌 **비대칭** 상황이 생긴다. 글로벌 거래의 실무 난점.

## 2. 무슨 데이터를 주고받나 — IVMS101

교환해야 하는 정보(임계값 이상 이전 1건당):

| 묶음 | 내용 |
|---|---|
| **송금인(originator)** | 이름, 계좌/지갑주소, (관할권에 따라) 주소·생년월일·고객번호 |
| **수취인(beneficiary)** | 이름, 계좌/지갑주소 |
| **송신 VASP(originating)** | 사업자 식별 |
| **수신 VASP(beneficiary)** | 사업자 식별 |

- 데이터 표준은 **<abbr class="gloss" title="VASP 간 송금인·수취인 정보를 주고받는 국제 공통 데이터 표준(interVASP Messaging Standard)">IVMS101</abbr>**(interVASP Messaging Standard, 2020년 interVASP 공동작업반 발표) — 모든 주요 솔루션이 쓰는 **공통 언어**. 표준이 있어야 솔루션·관할권이 달라도 필드가 맞는다.
- **선택적 공개(selective disclosure)**: 신원정보를 정산 메시지 본문이 아니라 **별도로, 권한 있는 상대에게만 최소한** 전달하는 게 권장 — 데이터 노출 최소화.

핵심 난제 네 가지(여기서 구현 차이가 갈린다):
1. **카운터<abbr class="gloss" title="Canton에서 권한과 데이터 가시성의 주체가 되는 식별 가능한 참여 주체">파티</abbr> VASP 식별·발견** — 이 지갑주소가 어느 VASP 소속인가?
2. **안전한 교환** — PII를 어떻게 E2E로 주고받나?
3. **검증** — 상대가 진짜 인가받은 VASP인가?
4. **자기수탁(unhosted) 지갑** — 상대가 VASP가 아니면?(6절)

## 3. 다른 곳에선 어떻게 구현되나 — 메시징 프로토콜/네트워크

트래블룰의 실제 데이터 교환은 **<abbr class="gloss" title="거래·컨트랙트가 기록되는 장부. Canton에선 활성 컨트랙트의 모음">원장</abbr> 밖(off-chain) 메시징 프로토콜**이 담당하는 게 일반적이다. 주요 프로토콜·네트워크:

| 프로토콜/네트워크 | 성격 | 카운터파티 발견·검증 | 비고 |
|---|---|---|---|
| **TRISA** | 오픈소스, **P2P 메시징 + 중앙 CA**(인증서 권한) | 중앙 CA가 VASP 공개키 인증서 디렉토리 역할 | PII는 VASP끼리 직접 P2P 교환 |
| **TRP**(Travel Rule Protocol) | 오픈, **중앙 디렉토리 + E2E API** | 중앙 디렉토리 서비스로 VASP 발견 | Coinbase 등 업계 컨소시엄 주도 |
| **OpenVASP** | 오픈, **탈중앙 발견** | 공유 인프라 최소화·메시지 표준 중심 | 프라이버시·탈중앙 강조 |
| **TRUST** | **폐쇄망**(미국 중심) | 멤버 한정 | 코인베이스 등 미 거래소 연합 |
| **Sygna Bridge** | 상용 | 자체 네트워크 | (VerifyVASP가 2025년 인수) |
| **VerifyVASP** | 상용, **P2P·E2E**, API | 검증된 VASP 네트워크(150+/30+국가) | **한국계**, 4절 |
| **Shyft / Veriscope** | **온체인** 접근 | 블록체인 기반 디렉토리 | 프로토콜 자체가 체인 |
| **Netki / TransactID** | 상용 | — | |
| **Notabene** | **프로토콜 비종속 게이트웨이** | W3C **DID·검증가능자격증명(VC)** 으로 기존 프로토콜을 **브릿지** | 여러 프로토콜을 한 대시보드로 |

**공통점**: 거의 다 IVMS101 데이터 + E2E 암호화. **차이는** 주로 **(1) 카운터파티 발견 방식**(중앙 디렉토리 vs P2P+CA vs 온체인), **(2) 거버넌스·멤버십**(오픈 vs 폐쇄망 vs 상용).

**상호운용성 문제**: 단일 프로토콜이 모든 상대를 못 덮는다 → VASP는 보통 **여러 프로토콜을 동시에 지원**하거나, Notabene 같은 **브릿지/게이트웨이**를 쓴다. TRISA는 TRP/OpenVASP·Sygna Bridge와 일부 상호운용을 달성했다.

## 4. 한국의 구현 (특금법)

한국은 트래블룰을 상대적으로 일찍·강하게 도입한 편이라, 한국 적격기관엔 직접 참고가 된다.

- **근거**: 특정금융정보법(특금법) 개정 → **2022년 3월 25일 전면 시행**.
- **임계값**: **100만원 이상** 이전 시 송신·수신 VASP가 양측 신원 기록·교환.
- **두 진영(초기 비호환)**:
  - **VerifyVASP** — 업비트가 채택(자회사 람다256(Lambda256)이 구축). 이후 글로벌 확장(2025년 Sygna 인수).
  - **CODE** — 빗썸·코인원·코빗 연합이 만든 자체 시스템.
  - 초기엔 CODE↔VerifyVASP가 **서로 호환 안 돼** 투자자 혼란 → 이후 상호연동 진행.
- **결합 요건**: 실명확인 입출금 계좌 + ISMS 인증을 갖춘 소수 거래소만 원화 입출금 가능 → 트래블룰이 **실명계좌 체계와 함께** 작동.

## 5. 자기수탁(unhosted) 지갑 문제

상대가 VASP가 아니라 **개인 자기수탁 지갑**이면 정보를 교환할 상대 사업자가 없다. 관할권별 처리:
- **주소 소유 증명**(예: 소액 전송·서명으로 본인 지갑임을 입증),
- 일정액 이상 자기수탁 이전 **신고** 요구,
- DeFi·NFT 등 비-VASP 영역은 가장 크게 영향(특히 한국에서 입출금 제한으로 이어짐).

## 6. Canton과의 관계 — 왜 이 위키에 있나

**Canton 자체는 트래블룰 메시징 프로토콜이 아니다.** 역할은 두 층으로 나뉜다.

**(A) 온원장(가시성) 층 — Canton이 강한 부분**
- [부분 트랜잭션 프라이버시](../glossary.md)·**선택적 공개**·**규제기관 옵저버**로, 트래블룰이 다루는 신원·거래 데이터를 **프라이버시를 깨지 않고** <abbr class="gloss" title="컨트랙트를 소비해 비활성으로 만드는 것(archive). 보관된 컨트랙트는 더 이상 쓸 수 없음">보관</abbr>·감사할 수 있다.
- Canton·TRM Labs 협업 자료는 금융기관이 **"Canton Network 위에서 기록보존·트래블룰 의무를 충족할 수 있다"** 고 명시 — 거래 참여 기관 내에서 송금인·수취인을 식별·스크리닝하는 방식. **guardian 모델**(암호화 데이터 접근을 정책으로 부여) + **TEE**(위험 신호 생성에 필요한 정보만) + 법집행기관 **시한부 접근**.

**(B) VASP 간 신원 교환 층 — Canton이 직접 하지 않는 부분**
- 송금인/수취인 정보를 **상대 VASP와 교환**하는 행위(IVMS101)는 3절의 **오프체인 프로토콜**(VerifyVASP 등)이나 **지갑/VASP 소프트웨어**가 담당.

**우리 PoC(기관 간 정산) 맥락**: 정산 프로토콜은 컴플라이언스를 프로토콜에서 빼고(대부분 VASP가 오프체인 해결), **트래블룰은 지갑/VASP 층**(예: 노드월렛 컴플라이언스 정책 엔진 + VerifyVASP 연동)이, **Canton은 정산·프라이버시·감사 층**이 맡는 분담이 자연스럽다. (지갑 비교·자기수탁 맥락은 [외부 파티 키 보관·서명](custody-raw-blind-signing.md))

> 주의: "캔톤 네이티브 트래블룰"이라는 말은 VerifyVASP가 Canton 전용이라는 뜻이 **아니다**. VerifyVASP는 체인 비종속(P2P·E2E·API) 프로토콜이고, 지갑 소프트웨어가 그것을 **Canton 파티 지갑에 통합**해 제공한다는 의미.

## 한 줄

> 트래블룰 = **VASP끼리 송금인·수취인 신원을 주고받는** FATF 규제. 데이터 표준은 IVMS101, 교환은 TRISA·TRP·OpenVASP·VerifyVASP 등 **오프체인 프로토콜**이 담당(상호운용이 과제). 한국은 특금법으로 100만원↑ 의무이고 VerifyVASP·CODE 두 진영이 있다. **Canton은 이 신원교환을 직접 하지 않고**, 선택적 공개·규제기관 옵저버로 **데이터를 프라이버시 보존하며 보관·감사**하는 토대를 댄다.

## 관련 문서

- [외부 파티 키는 누가 보관·서명하나 — raw signing & blind signing](custody-raw-blind-signing.md) · [파티는 유저마다? — per-user vs 옴니버스](party-design-per-user-vs-omnibus.md)
- [Canton 위 기관 간 DvP 정산 앱 — 2층 구조](dvp-settlement-app-architecture.md) · [Canton의 B2B vs B2C](canton-b2b-vs-b2c.md)
- [용어집](../glossary.md)

## 출처 (참고)

- FATF 권고 16 / 트래블룰 개요: [Sumsub](https://sumsub.com/blog/what-is-the-fatf-travel-rule/) · [Chainalysis](https://www.chainalysis.com/glossary/travel-rule/) · [FATF Best Practices(2025)](https://www.fatf-gafi.org/content/dam/fatf-gafi/recommendations/Best-Practices-Travel-Rule-Supervision.pdf)
- IVMS101: [interVASP](https://www.intervasp.org/) · [Notabene 분석](https://notabene.id/travel-rule-messaging-protocols/ivms-101)
- 프로토콜 비교(TRISA·TRP·OpenVASP·Shyft·Notabene): [Notabene](https://notabene.id/travel-rule-messaging-protocols) · [Didit](https://didit.me/blog/travel-rule-protocols-trisa-trp/) · [OpenVASP–TRISA 상호운용](https://www.openvasp.org/blog/trisa-and-trp-announce-travel-rule-interoperability)
- VerifyVASP: [TravelRule Protocol](https://www.verifyvasp.com/en/products/travel-rule/) · [Sygna 인수](https://www.prnewswire.com/news-releases/verifyvasp-acquires-sygna-consolidating-the-global-travel-rule-network-302756098.html)
- 한국(특금법·CODE vs VerifyVASP): [CoinGeek](https://coingeek.com/south-korean-exchanges-begin-a-new-travel-rule-era-with-defi-and-nfts-taking-biggest-hit/) · [Cryptoshimbun](https://cryptoshimbun.jp/en/news-en/korea-travel-rule-threshold-crypto-transfers-en/)
- Canton 프라이버시·컴플라이언스: [TRM Labs × Canton](https://www.canton.network/blog/how-trm-labs-and-canton-network-make-privacy-and-compliance-complementary) · [21Shares](https://www.21shares.com/en-us/research/why-canton-solves-defis-institutional-privacy-gap)

<!-- nav:start -->

---

⬅️ **이전**: [스테이블코인 발행·소각과 레지스트리 — 외부발행+브릿지 vs Canton 직접발행](token-issuance-bridge-patterns.md)

<!-- nav:end -->
