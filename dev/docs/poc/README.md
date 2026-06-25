# 단기 PoC — 개발/인프라 문서

> **목표: 캔톤 네트워크에 대한 이해를 높이기.** 적격기관(국내은행)으로서 무스비에 직접 연결해 정산 한 건을 끝까지 돌려보며 캔톤을 이해한다.
> 이 폴더는 **개발/인프라 내용만** 담는다(비즈니스/협상은 제외). 자립형 — 다른 문서에 의존하지 않는다.
> 용어는 역할 기반(국내은행 / 일본은행 그룹 / 무스비 / MM). 참여사 실명은 쓰지 않는다.

## 전제

| 항목 | 내용 |
|---|---|
| **환경** | **DevNet 또는 TestNet** (LocalNet 검증은 완료). 인프라는 **AWS Sandbox**(망분리 때문 — 은행 내부망 밖 격리). |
| **방식** | AWS Sandbox에 우리 스택(participant + **노드월렛** + Musubi backend + Postgres)을 띄워 연결. 내부 시스템 연동 **최소화**, 대부분 노드인프라/무스비 준비. **Fireblocks 미사용**(단기). |
| **역할** | 국내은행 = 송신 Institution + Custodian (VASP 가정). 지갑은 **노드월렛**(네이티브 파티 호스팅). |
| **시나리오** | 국내은행 보유 **KRWK**를 무스비로 **JPYC 송수신** (고객 없음 — 은행 자기계정) |

## 문서

| 문서 | 내용 |
|---|---|
| [musubi-overview.md](musubi-overview.md) | **무스비 제품/SDK 개요** — 4-leg 정산·역할·연동/배포·지원 자산. |
| [architecture.md](architecture.md) | **아키텍처 메모** — 단기 PoC 구성요소·데이터 흐름·신뢰 지점. |
| [aws-sandbox-devnet-setup.md](aws-sandbox-devnet-setup.md) | **AWS Sandbox + DevNet/TestNet 진행 방식** — 구성·온보딩 순서(시퀀스). |
| [nodeinfra-asks.md](nodeinfra-asks.md) | **노드인프라에 요구할 것** — 환경·프로비저닝·소프트웨어·배포 체크리스트. |
| [short-term-scenario.md](short-term-scenario.md) | **기술 시나리오** — 4-leg 정산을 파티·상태·합격 기준·시퀀스로. |

## 읽는 순서

개념 → 구조 → 실행 → 준비물 순으로 읽으면 된다.

1. **[musubi-overview.md](musubi-overview.md)** — 무스비가 무엇을·어떻게(4-leg 정산·역할·API/배포) 하는지 먼저 파악.
2. **[architecture.md](architecture.md)** — 그 위에서 우리(적격기관) PoC가 어떻게 구성되는지(구성요소·데이터 흐름).
3. **[short-term-scenario.md](short-term-scenario.md)** — 실제로 무엇을 어떤 순서로 돌리고 무엇을 확인하는지(정산 시나리오·합격 기준).
4. **[aws-sandbox-devnet-setup.md](aws-sandbox-devnet-setup.md)** — 그걸 AWS Sandbox + DevNet/TestNet에 올리는 절차.
5. **[nodeinfra-asks.md](nodeinfra-asks.md)** — 그 절차에 필요한, 노드인프라에 받아야 할 것들(체크리스트).

## 단기 PoC로 이해하려는 것 (캔톤 핵심)

1. **원자적 DvP** — KRWK·JPYC가 한 트랜잭션에 전부 실행되거나 전부 롤백.
2. **프라이버시** — MM에 신원 익명(익명 RFQ) · 무관한 제3자는 거래를 데이터로 갖고 있지도 않음.
3. **Synchronizer 활동** — 시퀀서가 순서를 확정해 전달.
4. **파티/참여자/뷰/2계층 합의** — 캔톤 기본 개념을 실물로 확인.
</content>
