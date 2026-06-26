# 1차 PoC — 개요

> **목적: 무스비/캔톤을 "왜 쓰는지" 그 이유들을 실제로 검증한다.** 캔톤 네트워크 이해를 높이는 동시에, 무스비 기능 정상동작·원자적 DvP·익명(프라이버시)·DAML 로직을 직접 돌려 확인한다.
> 환경: **DevNet/TestNet** · 인프라: **AWS Sandbox** · 지갑: **노드월렛**(캔톤 네이티브 파티 호스팅·고객 HSM).
> 용어는 역할 기반 — 국내은행 / 해외은행(일본은행 그룹) / 무스비 / MM. 참여사 실명 미사용.

## 1차 PoC가 검증하려는 것 (왜 쓰는지 = 무엇을 확인하나)

| 검증 항목 | 왜 중요한가(가치) | 합격 신호 |
|---|---|---|
| **원자적 DvP** | 카운터파티(Herstatt) 리스크 0 | 양 통화 동시 이동, 한쪽 실패 시 전체 롤백 |
| **익명/프라이버시** | 거래 상대·금액 비공개 | MM에 신원 익명, 무관 제3자 거래 0건 |
| **무스비 기능 정상동작** | 정산 레일이 실제로 작동 | 주문→견적(RFQ)→정산 end-to-end ~15초 |
| **DAML 검증** | 컨트랙트 로직·권한이 정확 | FXOrder 상태전이·서명자 규칙대로, 잘못된 호출 거부 |
| **캔톤 이해** | 팀 역량 축적 | 파티/뷰/2계층 합의/Synchronizer 직접 관찰 |

→ 상세 검증 방법·합격 기준은 [verification.md](verification.md).

## 전제

| 항목 | 내용 |
|---|---|
| **환경** | DevNet 또는 TestNet. 인프라는 AWS Sandbox(**망분리** 때문 — 은행 내부망 밖 격리). |
| **방식** | AWS Sandbox에 국내은행 스택(participant + **노드월렛** + Musubi backend + Postgres)을 띄워 연결. 내부 시스템 연동 최소화, 대부분 노드인프라/무스비 준비. |
| **역할** | 국내은행 = 송신 Institution + Custodian(VASP 가정). 지갑은 **노드월렛**(내부, 캔톤 네이티브 파티 호스팅). |
| **시나리오** | 국내은행 보유 **KRWK**를 무스비로 해외은행에 **JPYC 송수신** (고객 없음 — 은행 자기계정). |
| **지갑** | 1차 = **노드월렛**(내부). 최종 = **Fireblocks**(외부) 가능성 — 비교는 [wallet-comparison.md](wallet-comparison.md). |

## 문서 (읽는 순서)

1. **[musubi-overview.md](musubi-overview.md)** — 무스비가 무엇을·어떻게(4-leg 정산·역할·API/SDK). 검증 대상이 되는 "주장"들.
2. **[architecture.md](architecture.md)** — AWS Sandbox + 노드월렛 + DevNet/TestNet 구성, 데이터 흐름.
3. **[verification.md](verification.md)** — 검증 항목별 목적·방법·합격 기준 + 정산 시나리오. (이 PoC의 핵심)
4. **[wallet-comparison.md](wallet-comparison.md)** — 외부(Fireblocks) vs 내부(노드월렛) 지갑 비교 + 국내은행→해외은행 시퀀스 차이.
5. **[aws-sandbox-devnet-setup.md](aws-sandbox-devnet-setup.md)** — AWS Sandbox + DevNet/TestNet 진행·온보딩.
6. **[nodeinfra-asks.md](nodeinfra-asks.md)** — 노드인프라에 받아야 할 것 체크리스트.

> 회의 배경(비즈니스 포함)은 poc 밖 `dev/docs/musubi-poc-meeting-notes.md`.

## 참고 (출처)

- 무스비 소개: https://musubinetwork.com/introduction
- 무스비 동작(정산 흐름): https://musubinetwork.com/how-it-works
- Canton Network 문서: https://docs.canton.network
