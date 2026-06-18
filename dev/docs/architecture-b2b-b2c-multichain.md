# 아키텍처 — B2B/B2C 역할 분담 & 멀티체인 (프로젝트)

> 우리 프로젝트의 계층 분담 결정 메모. 일반 Canton B2B/B2C 적합성은 위키 [Canton B2B vs B2C](../../wiki/notes/canton-b2b-vs-b2c.md) 참고.
> (dev 문서 — 위키와는 목적상 분리. 대외비는 아님: 공개 정보 기반.)

## 결정된 방향: 계층별 역할 분담
```
[B2C] 일반유저 ↔ 스테이블코인        → 퍼블릭 체인 (Base/Ethereum)
                       │ 브릿지(필수)
[B2B] 적격기관 ↔ 적격기관 정산(DvP)   → Canton (프라이버시·원자적 결정적 정산)
```
- **B2C는 Canton에서 안 한다.** 리테일 접점(소비자용 스테이블코인)은 **퍼블릭 체인**(Base/Ethereum)에서.
- **Canton은 B2B 정산 전용** — 기관 간 원자적 DvP(통화↔통화), 프라이버시 보존.
- 두 계층은 **브릿지로 연결**(필수 컴포넌트).

## 왜 이렇게 나누나
| 계층 | 체인 | 이유 |
|---|---|---|
| B2C(리테일) | 퍼블릭(Base/Eth) | 대량·저비용·간편 온보딩·기존 지갑 생태계(리테일이 이미 있음) |
| B2B(기관 정산) | Canton | 프라이버시(거래 상대·금액 비공개)·결정적 확정·허가형 자산·다자 권한 |

→ Canton 강점은 B2B에서만 결정적이고, B2C엔 오버스펙. 그래서 분담.

## 미확정 (열어둘 것)
- **스테이블코인 발행 체인 세부**: KRWStable·JPYSC를 어느 체인에서 발행할지 **미정** → 양쪽 시나리오 병기.
  (퍼블릭 체인 발행 후 브릿지 vs Canton 토큰표준으로 직접 발행 등)
- 브릿지 방식(어떤 브릿지·신뢰 모델)도 설계 대상.

## Musubi 매핑
- Musubi가 담당하는 건 **B2B 정산 계층(Canton)** — OTCTrade형 기관↔기관 DvP. (참고: [dvp-licensing-code-walkthrough.md](dvp-licensing-code-walkthrough.md))
- B2C 측(소비자 스테이블코인)은 Musubi/Canton 범위 밖 — 퍼블릭 체인 + 브릿지 연동 지점만 신경.

## 관련
- 위키 일반 정리: [Canton B2B vs B2C](../../wiki/notes/canton-b2b-vs-b2c.md)
- 로드맵 Phase 3(백엔드·브릿지 연동): [roadmap.md](roadmap.md)
