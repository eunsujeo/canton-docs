# 앞으로 할 일 (Roadmap)

> Canton 기반 개발 작업의 단계별 계획. 학습 → 로컬 구축 → 정산 로직 → 공유/데모 순으로 진행.
> 우선순위는 위에서 아래로. 세부 배포/데모 옵션은 [deployment-and-demo-options.md](deployment-and-demo-options.md) 참고.

## 현재 상태 (2026-06-16)
- ✅ **학습(개념)**: Canton overview 핵심 완료 — 파티·컨트랙트·뷰·2계층 합의·프라이버시·DvP·환경 사다리.
- ✅ **위키**: 번역·정리 + Cloudflare Pages 자동 배포(push → 배포) 구축 완료.
- ⬜ **개발**: 아직 시작 전. 아래 Phase 1부터.

---

## Phase 0 — 학습 마무리 (병행)
- [ ] appdev **모듈 3(Daml)** 학습 — 컨트랙트/초이스/시그니처를 코드로 작성하는 법. (DvP 템플릿 작성의 직접 선행)
- [ ] 헷갈리는 개념 나오면 위키에 노트/툴팁으로 환원(기존 방식 유지).
- 참고: [용어 한 컷 카드](../../wiki/notes/term-cheatsheet.md) · [DvP 정산 앱 2층 구조](../../wiki/notes/dvp-settlement-app-architecture.md)

## Phase 1 — 로컬 환경 구축 (LocalNet)
- [ ] **cn-quickstart 클론** → `dev/` 안에 개발 베이스 마련.
- [ ] [사전 요구사항·설치](../../wiki/appdev/quickstart/prerequisites.md)대로 Docker/Daml SDK 등 준비.
- [ ] `make start`로 LocalNet 기동 → [데모 실행](../../wiki/appdev/quickstart/running-the-demo.md) 확인.
- [ ] 기본 대시보드 접속 확인: Scan / SV / Wallet UI. (목록: [deployment-and-demo-options.md](deployment-and-demo-options.md))
- 참고: [LocalNet 개발](../../wiki/appdev/modules/m5-localnet-development.md) · [환경 4단계·스펙](../../wiki/notes/canton-environments-localnet-to-mainnet.md)

## Phase 2 — DvP 정산 로직 구현 (핵심)
- [x] **참고 예제 = OTCTrade**(P2P 다중 leg DvP), 라이선싱(단방향 B2C)보다 Musubi(기관↔기관)에 맞음. `daml/external-test-sources/splice-token-test-trading-app/.../TradingApp.daml`
- [x] **Daml 템플릿 작성**: `settlement/` 패키지 — `SettlementProposal`/`Settlement`(2-leg 원자 DvP). **컴파일 성공**(2026-06-18). 원본: [../daml/settlement/](../daml/settlement/README.md)
- [ ] Daml Script 테스트: 두 기관 + 통화 2종으로 제안→합의→할당→원자 실행 시나리오
- [ ] 파티 모델 정의: 기관 A / 기관 B / (필요 시) 커스터디언·마켓메이커 — RFQ 흐름.
- [ ] 서명자·관찰자·컨트롤러 권한 설계(누가 제안/수락/정산을 트리거하나).
- [ ] **Daml Script로 시나리오 자동 실행** — "제안 → 수락 → 원자적 정산 / 실패 시 전부 롤백" 재현.
- [ ] 부분 트랜잭션 프라이버시 확인(각 파티가 자기 view만 보는지).
- ⭐ 직접 근거: [예제 라이선싱 코드 → DvP 골격 → Musubi](dvp-licensing-code-walkthrough.md) — License.daml이 Musubi DvP의 골격(다리 1개→2개).
- 참고: [원장 모델](../../wiki/overview/ledger-model.md) · [파티 설계: 1인1파티 vs 옴니버스](../../wiki/notes/party-design-per-user-vs-omnibus.md) · [로컬/외부 파티](../../wiki/notes/local-vs-external-party.md)

## Phase 3 — 백엔드 앱 레이어
- [ ] 정산 앱(백엔드)에서 Ledger API 연동 — 트랜잭션 제출·구독.
- [ ] (스테이블코인 발행 체인은 미확정 — Base/Ethereum vs Canton 두 시나리오 병기하며 설계.)
- [ ] 브릿지 연동 지점 식별(B2C 체인 ↔ Canton B2B 정산).

## Phase 4 — 원격 공유 & 데모 (나중)
- [ ] 클라우드 VM에 LocalNet 올리기 + 리버스 프록시/터널 + 접근제한.
- [ ] **설명용 커스텀 대시보드** — 공식 Wallet/Scan UI가 처음 보는 사람에겐 너무 어려움(잔액=보상코인, Tap→트래픽 등 숨은 맥락 많음). **다른 사람에게 설명할 때** 쓸, 쉬운 말 요약 대시보드를 다시 만든다. (지금은 공식 UI + `scan-status.py`로 충분)
- [ ] 시나리오 버튼 시연 + 팀 공유용 URL.
- 상세: [deployment-and-demo-options.md](deployment-and-demo-options.md) · **원격 세팅 계획(빌드 재현+런타임): [remote-setup-plan.md](remote-setup-plan.md)**

## Phase 5 — 다른 기관 연동 (그 다음)
- [ ] **DevNet 온보딩**(스폰서 SV·IP allowlist) — 진짜 기관 간 연동이 필요할 때.
- [ ] TestNet PoC로 확장.

---

## 메모
- 우선순위 1순위는 **Phase 1~2(로컬에서 DvP 로직 구현)**. 원격/데모(Phase 4)는 급하지 않음.
- 대외비 코드는 비공개 repo 또는 `.gitignore` (위키만 공개 배포).
- 추가 번역이 필요해지면 그때 `wiki/sources.md` 큐에서 해당 페이지 진행.
