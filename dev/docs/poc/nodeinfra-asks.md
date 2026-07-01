# 노드인프라 요청 — 적격기관 체크리스트

> 국내은행은 적격기관(송신 Institution + Custodian)으로 1차 PoC에 참여한다.
> **AWS Sandbox**에 국내은행 스택(participant + **노드월렛** + Musubi backend + Postgres)을 띄우고 **DevNet/TestNet**에 연결한다. 노드월렛 SW·배포물·네트워크는 노드인프라/무스비가 준비.
> 각 항목 옆에 받은 답을 채워가며 쓴다.

## A. 네트워크/환경
- [ ] **DevNet vs TestNet** — 이번 PoC는 어느 쪽으로? 차이(안정성·리셋 주기·비용)와 권장.
- [ ] **온보딩 방식** — 어느 Synchronizer에 연결·온보딩 절차·소요. (이번 PoC는 별도 스폰서 SV 없음 — 노드인프라가 온보딩)
- [ ] **IP allowlist** — 국내은행 AWS Sandbox egress IP 등록 필요 여부·방법.
- [ ] **배포 지원 범위** — AWS Sandbox 스택을 국내은행이 직접 띄우나, 노드인프라가 배포 지원/대행하나.
- [ ] **노드월렛 SW** — 자가 키보유(고객 HSM, FIPS 140-3 L3)·3-키 멀티시그·컴플라이언스 정책 엔진·망분리 내장(Fireblocks 옴니버스 대안). 배포물·라이선스, AWS Sandbox 구동 요구사양.
  - [ ] **Canton 지원** — 담당자는 **캔톤 네이티브 파티 호스팅** 확인(공개 문서는 Solana뿐). **Daml(prepared-tx) raw 서명·컴플라이언스 엔진의 Canton 적용·버전**을 문서/데모로 확인.
  - [ ] **키 HSM 관리 주체**(노드인프라 vs 국내은행)·망분리·SGX 요건.
  - [ ] (선택) 캔톤 네이티브 트래블룰(예: VerifyVASP) 연동 가능 여부.

## B. 프로비저닝(자격증명) — 무스비 발급
- [ ] **Canton Party ID** — 국내은행 정산 네트워크 신원.
- [ ] **JWT signing credentials** — API 인증용.
- [ ] **정산 네트워크 endpoint + TLS(mTLS) 인증서** — 발급 주체·신뢰 체인·회전/폐기 절차 ([verification.md](verification.md) 6절 보안 C).
- [ ] **국내은행에 부여되는 role** — `institution` / `custodian`. 수신측은 누구 role로.

## C. 소프트웨어/패키지
AWS Sandbox에 띄울 국내은행 스택 구성요소(노드월렛 SW는 A절).
- [ ] **Musubi Backend 배포물** — 도커 이미지명/레지스트리/**버전**, 설정 방식(env/config).
- [ ] **Canton Participant Node** — 이미지/버전, 요구사양.
- [ ] **DAML 배포·벳팅 과정** — `FXOrder` 등 정산 패키지(DAR)를 **누가 우리 participant에 업로드·벳팅**하나(우리 vs 노드월렛/무스비 ops), **모든 참여자 패키지 일치(벳팅)** 보장, **버전·업그레이드** 절차, **패키지 ID** 공유(검증·raw Ledger용 — [verification.md](verification.md) 4절).
- [ ] **DAML 소스/감사용 공유** — 적격기관(또는 제3자) 검증을 위해 `FXOrder` **DAML 소스(최소 DAR)+패키지 ID** 공유 가능 여부. (소스가 IP라 불가면 DAR+패키지로 행동 검증) + **raw Ledger API 접근** — [verification.md](verification.md) 4절(적격기관 주도 DAML 검증).
- [ ] **OpenAPI 스펙 파일 + Console 접근** — 역할별 OpenAPI 스펙 파일 위치, Console 계정. (Webhook 지원 여부 확인)
- [ ] **배포물 무결성/출처** — 노드월렛 SW·Musubi backend·participant 이미지·DAR의 체크섬/서명·출처(provenance) 검증 방법 ([verification.md](verification.md) 6절 보안 E).

## D. 자산/인스트루먼트
- [ ] **KRWK 인스트루먼트** — 라이브는 JPYSC인데, PoC용 **KRWK는 누가/어떻게 발행**하나. 테스트 발행자/레지스트리.
- [ ] **상대 통화** — JPYSC로 시연. 테스트 토큰 발급(faucet) 절차.

## E. 카운터파티 / 마켓메이커 (4-leg 필수)
- [ ] **Market Maker** — 4-leg엔 MM이 필수. PoC에서 MM은 누가(노드인프라/무스비가 테스트 MM 제공?).
- [ ] **수신 카운터파티(해외은행)** — 측 엔티티와 수신 Custodian은 누가. 샌드박스에선 노드인프라가 모킹/대행하나.
- [ ] **카운터파티 디렉토리** — receiver·custodian의 Party ID를 어디서 받나.

## F. 인프라/배포 (AWS Sandbox)
- [ ] **권장 배포 구성(footprint)** — participant + 노드월렛 + Musubi backend + Postgres의 인스턴스 사양·OS·리소스.
- [ ] **배포 자료** — AWS용 배포 가이드/Terraform/Compose 등 제공 여부.
- [ ] **아웃바운드 연결 요구** — 어떤 호스트/포트로 나가야 하나(Synchronizer·무스비 endpoint).

## G. 운영/검증
- [ ] **연결 테스트 절차** — `/health`, `/whoami`, 테스트 order 생성 등.
- [ ] **모니터링** — `GET /api/v1/dashboard/stats`(상태별 order·정산량) 등 대시보드.
- [ ] **검증 지원** — 실패 주입(롤백 확인)·프라이버시 조회 등 [verification.md](verification.md) 항목 검증에 필요한 접근/도구.
- [ ] **지원/에스컬레이션** — PoC 기간 지원 채널, 담당자, 일정.

## H. 키 보관
- [ ] **키 보관** — 노드월렛(HSM/망분리) 키 관리 주체·격리 요건(A절과 연계).
- [ ] **키 생성·백업·복구** — 키가 HSM(FIPS 140-3 L3)을 벗어나지 않는지, 3-키 멀티시그 분산·임계값·분실 시 절차 ([verification.md](verification.md) 6절 보안 A).
- [ ] **서명 권한·차단** — 컴플라이언스 정책 엔진(Allow/Held/Deny)이 악의적·오류 트랜잭션을 내용을 보고 차단할 수 있는지(blind raw signing 대비).

## 우선순위 (먼저 받아야 진행되는 것)
1. **A(환경·온보딩·노드월렛) + B(프로비저닝)** — AWS Sandbox에서 스택을 띄워 연결하는 데 필수.
2. **C(소프트웨어·패키지) + F(배포 자료)** — 실제 기동.
3. **D(KRWK·통화) + E(MM·카운터파티)** — 정산·검증 시나리오 실행.
4. **G(검증·운영) + H(키 보관)** — 마무리·합격 판정.

## 참고 (출처)

- 배포·연동: https://musubinetwork.com/custodian/integration/deploy
- 인증: https://musubinetwork.com/authentication
- API 규약: https://musubinetwork.com/api-conventions
- 역할별 API 레퍼런스: https://musubinetwork.com/institution/api-reference · https://musubinetwork.com/custodian/api-reference · https://musubinetwork.com/market-maker/api-reference
- 노드월렛 문서: https://docs.nodeinfra.com (접근 코드 필요)
- Canton Network 문서: https://docs.canton.network
