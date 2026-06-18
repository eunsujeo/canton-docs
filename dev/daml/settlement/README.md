# settlement — Musubi 2-leg FX DvP Daml 패키지 (Phase 2)

**여기가 추적되는 원본(source of truth).** 실제 빌드는 cn-quickstart 안의 사본에서 한다(아래).

## 무엇
적격기관 ↔ 적격기관 **통화↔통화 원자적 정산(DvP)** Daml 패키지.
- 청사진: cn-quickstart의 **OTCTrade** 예제(다중 leg 토큰표준 DvP)를 본뜸.
- 라이선싱(단방향 B2C)과 달리 **대칭 P2P, 다중 leg**.
- 핵심 템플릿: `SettlementProposal`(제안·합의), `Settlement`(개시·원자 실행).
- 설계 배경: [../../docs/dvp-licensing-code-walkthrough.md](../../docs/dvp-licensing-code-walkthrough.md)

## 파일
```
settlement/
├─ daml.yaml                       # 패키지 설정(토큰표준 DAR 의존)
└─ daml/Settlement/FxDvp.daml      # SettlementProposal, Settlement (+ 헬퍼)
```

## 빌드 (현재 상태: ✅ 컴파일 성공)
cn-quickstart는 gitignore라, 빌드는 그 안에 **사본을 두고** 한다:
1. 이 폴더를 `dev/cn-quickstart/quickstart/daml/settlement/` 로 복사(동기화).
   ```bash
   cp -R dev/daml/settlement/. dev/cn-quickstart/quickstart/daml/settlement/
   ```
2. `dev/cn-quickstart/quickstart/daml/multi-package.yaml` 의 `packages:` 에 `- ./settlement` 등록(1회).
3. 빌드:
   ```bash
   cd dev/cn-quickstart/quickstart
   nix develop ../ --command ./gradlew :daml:compileDaml   # dpm build --all
   ```
   → `Created .daml/dist/quickstart-settlement-0.0.1.dar`

> ⚠️ 코드 수정은 **이 추적 원본에서** 하고 cn-quickstart로 동기화. (반대로 하면 gitignore라 유실 위험)

## 다음 (TODO)
- [ ] Daml Script 테스트: 두 기관 + 통화 2종 인스트루먼트로 제안→합의→할당→실행(원자 정산) 시나리오. (참고: splice-token-standard-test 인프라)
- [ ] 통화 인스트루먼트 표현(토큰표준 instrumentId) 설계 — 발행 체인 미정과 연결.
- [ ] 백엔드(Ledger API)에서 SettlementProposal 생성·구독 연동.
