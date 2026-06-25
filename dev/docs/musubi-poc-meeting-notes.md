# 회의록 — 무스비 단기/최종 PoC 협의

> 무스비 운영사(노드인프라) ↔ 국내은행 담당자 간 협의 정리. 비즈니스·협상 맥락 포함 전체 기록.
> 개발/인프라 관점의 정리·진행 방식은 별도: [poc/](poc/README.md) 폴더.
> 용어는 역할 기반(국내은행 / 일본은행 그룹 / 무스비 / 노드인프라).

## 참석/주체

- **노드인프라** — 무스비 프로젝트 운영사. 문의점 제기·기술 회신.
- **국내은행** — PoC 추진 주체. VASP 가정. KRWK 보유.
- (언급) **일본은행 그룹** — 카운터파티. 신세이 / VCT / 홀딩스 등 계열사. 공동운영사가 Startale → 일본은행 그룹으로 이전 중(MOU 준비), 일본은행 개발 직접 관여 예정.

## 1. 노드인프라가 제기한 문의점 (8)

- **KPI** — 최종 PoC의 가장 중요한 목적(일본은행 관계 형성 / 규제 정합성 / 캔톤 기술 탐구 / 시간·비용 절약)?
- **카운터파티 확정** — 해외송금 파트너를 일본은행 그룹으로 픽스?
- **VASP** — 한국 VASP 미사용인지, 국내은행이 VASP가 되는 가정인지?
- **마켓메이커 Role** — 국내은행/일본은행 그룹이 직접(예: KRW-JPYSC 풀) vs 외부 MM?
- **코인** — KRW vs USD. JPY→USD→KRW 경유 atomic도 테스트 가능.
- **캔톤 지갑**(국내은행=VASP 가정) — 지갑 솔루션? 캔톤 네이티브 기능 제공하는 **HSM/망분리 노드월렛 SW** + 네이티브 트래블룰(예: VerifyVASP) 사용 가능. 노드월렛은 국내 10개+ 은행/PG/카드사와 솔라나 PoC 진행 중.
- **캔톤노드/네트워크** — Devnet/Testnet/Mainnet 선택, 브랜드 노출 vs 미노출(예: 노드인프라 명의 노드).
- **망분리** — 국내은행 망분리 안 vs 외부 AWS Sandbox?
- **온오프램프** — 무스비는 Stablecoin-to-Stablecoin만. Fiat(KRW/JPY)까지 연동? 이 경우 신세이 등 관여 가능.

## 2. 국내은행 답변

- **KPI** — 일본은행 그룹과 관계 형성 + 한·일 국경 간 환전/정산 기술 탐구 / 기관 간 Canton 정산 확인.
- **카운터파티** — 일본은행 그룹 내 참여 가능 엔티티(신세이/VCT/홀딩스 무관, 다 참여 가능).
- **VASP** — 국내은행이 VASP라는 가정.
- **MM Role** — 일본은행 그룹과 협의 희망. **스테이블코인 발행자들끼리 풀**이 궁극적으로 가장 안정적.
- **코인** — MM 여부에 따라 `KRWK↔JPYSC` 또는 `KRWK↔USDC↔JPYSC`.
- **캔톤 지갑** — Fireblocks 사용 가능성 높으나 시간 소요 가능. 안 되면 노드인프라 솔루션 사용을 개발팀과 논의.
- **캔톤노드/네트워크** — 나중에 결정. 캔톤과 NDA 진행 중.
- **망분리** — 개발팀과 확인 예정.
- **온오프램프** — 신세이 껴서 온오프까지 가면 더 담대하나 Fiat 끼면 일이 커짐 → 일단 가능성만 열어둠.

## 3. 합의·확인 (노드인프라 회신)

- **KPI/카운터파티/VASP** — 확인.
- **MM** — 일본은행 그룹 홀딩스 캔톤팀·JPYSC팀 양쪽 논의 필요(예: 이번 WebX).
- **코인** — 확인.
- **캔톤 지갑** — Fireblocks도 일반 무스비 PoC엔 무방. 단 Fireblocks는 SQL 최대 사용 **옴니버스** 지갑이라 추후 더 밀접한 캔톤 기능 지원 불가 → **DFNS·노드월렛** 등 필요.
- **망분리/온오프램프** — 확인.

## 4. 캔톤 지갑(Fireblocks) 논의

- 국내은행: 무스비 PoC에 Fireblocks 사용 무방한지, "더 밀접한 캔톤 기능"이 무엇인지, PoC와 무관한지 질문.
- 노드인프라:
  1. **Fireblocks 무방** — 단 4자간 Daml 컨트랙트 호출이라 **Raw Signing(blind signing, byte[] 서명)** 필요. 노드인프라가 Fireblocks 접근권한 없음 → 권한 개방 또는 연동 개발 공수 공동 투입 요청.
  2. **더 밀접한 기능** — blind signing으로 byte[]만 서명하면 이론상 모든 기능 가능하나, 악성 fund-drain tx를 byte[] 서명으로 막을 수 있는지 등 내부 보안 절차 테스트가 어려움. 슈퍼밸리데이터용 내부 캔톤 dApp을 커스터디 한 개 안에서 만들면 옴니버스(SQL DB)라 **캔톤 TX가 발생 안 해** 유의미한 dApp 개발 불가 → **노드월렛/DFNS처럼 캔톤 노드에 party를 호스팅하는 네이티브 방식** 필요.
- 국내은행: 초기엔 내부 dApp 안 함, 고객에게 캔톤 서비스 제공 안 할 가능성 높음.
- 상세 분석: [wallet-custody-fireblocks.md](wallet-custody-fireblocks.md).

## 5. 무스비 측 기능 현황 / 타 PoC

- **Settlement** 모두 구현(비디오 첨부).
- **Compliance** — VASP가 오프체인으로 대부분 해결 → 무스비 프로토콜에서 빼는 중. 국내은행 PoC 계기로 재점검 제안.
- **Netting** — CLS 유사하나 중앙 은행 없이 VASP 간 합의로 기술적 네팅 구현 중.
- **Combined atomic transaction** — 예) JPY→USD→KRW. 스테이블 측 JPY-KRW 유동성 장벽 대비.
- **Membership** — 초기 논의: Governance member + Settlement member(VASP) 구상.
- **타 PoC** — 일본은행 그룹 + 국내 금융사(은행 아님)에서 진행 중. VASP 연동·규제 정합성 검토에 공수 가장 큼. 참여사 많음 ↔ 국내은행 PoC는 참여사 적음(예상).
- **참고** — 노무라 투자 ClearToken(중앙화 라이선스 엔티티, stablecoin+fiat) 자료 공유. 분산화+스테이블 중심 무스비와 대비: [cleartoken-vs-musubi.md](cleartoken-vs-musubi.md).

## 6. 단기/최종 PoC 정의 (국내은행 정리)

| 항목 | 단기 PoC | 최종 PoC |
|---|---|---|
| 목표 | 캔톤 네트워크 이해도 향상 | 국내은행 지갑 시스템과 연동 |
| 시기 | 올해 안 | 내년 중 |
| 방식 | Sandbox, 국내은행 시스템 연동 최소화, 무스비/노드인프라 준비분으로, **파블(Fireblocks) 미사용** | **Fireblocks 활용**, 국내은행 지갑 시스템 연동 (지갑 시스템이 Fireblocks 예정이라 되는 방향 모색) |
| 시나리오 | 국내은행 고유자산 KRWK를 무스비로 JPYC 송수신 (**고객 없음**) | 국내은행 유저가 온램프로 KRWK 전환 → 무스비로 상대방에 JPYC 전송, 역방향도 |

## 7. 액션 아이템

- [ ] (노드인프라) MM 구조 — 일본은행 그룹 홀딩스 캔톤팀·JPYSC팀과 협의(WebX 등).
- [ ] (양측) 단기 PoC를 DevNet/TestNet(AWS Sandbox)에서 KRWK↔JPYC 정산 1건까지 — 진행: [poc/aws-sandbox-devnet-setup.md](poc/aws-sandbox-devnet-setup.md), 시나리오: [poc/short-term-scenario.md](poc/short-term-scenario.md), 노드인프라 요청: [poc/nodeinfra-asks.md](poc/nodeinfra-asks.md).
- [ ] (국내은행) 망분리(내부망 vs AWS Sandbox) 개발팀 확인 → 단기는 AWS Sandbox 전제.
- [ ] (양측·최종) Fireblocks Raw Signing 검증·접근권한/공수 협의(최종 PoC 범위).
- [ ] (국내은행) 캔톤 NDA 마무리, 노드/네트워크·브랜드 노출 결정.

## 8. 개발/인프라 정리로 이어짐

이 회의에서 정해진 단기 PoC를 개발/인프라 관점으로 풀어둔 곳:
- 개요·인덱스: [poc/README.md](poc/README.md)
- 무스비 제품/SDK: [poc/musubi-overview.md](poc/musubi-overview.md)
- 아키텍처: [poc/architecture.md](poc/architecture.md)
- AWS Sandbox + DevNet/TestNet 진행: [poc/aws-sandbox-devnet-setup.md](poc/aws-sandbox-devnet-setup.md)
- 노드인프라 요청 체크리스트: [poc/nodeinfra-asks.md](poc/nodeinfra-asks.md)
- 기술 시나리오: [poc/short-term-scenario.md](poc/short-term-scenario.md)
</content>
