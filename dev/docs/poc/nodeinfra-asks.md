# 노드인프라에 문의/요구할 것 (적격기관 체크리스트)

> 우리는 **적격기관(국내은행, 송신 Institution + Custodian)** 으로 단기 PoC에 참여한다.
> **AWS Sandbox**(망분리 때문)에 우리 스택(participant + **노드월렛** + Musubi backend + Postgres)을 띄우고 **DevNet/TestNet**에 연결한다. 노드월렛 SW·배포물·네트워크는 노드인프라/무스비가 준비.
> 아래는 그 전제에서 **노드인프라에 받아야/물어야 할 것**들이다. 각 항목 옆에 받은 답을 채워가며 쓴다.

## A. 네트워크/환경
- [ ] **DevNet vs TestNet** — 이번 PoC는 어느 쪽으로? 둘의 차이(안정성·리셋 주기·비용)와 권장.
- [ ] **온보딩 방식** — 어느 Synchronizer(글로벌 도메인)·**스폰서 SV**에 연결하나. 온보딩 절차·소요.
- [ ] **IP allowlist** — 우리 AWS Sandbox의 egress IP를 등록해야 하나? 등록 방법.
- [ ] **배포 지원 범위** — 우리 AWS Sandbox에 스택을 우리가 직접 띄우나, 노드인프라가 배포를 지원/대행하나. (단기엔 "대부분 노드인프라 준비"가 전제)
- [ ] **노드월렛 SW** — 캔톤 노드에 파티를 네이티브로 호스팅 + 키 HSM/망분리(Fireblocks 옴니버스 대안). 배포물·라이선스 제공 방식, AWS Sandbox 구동 요구사양.
  - [ ] **키 HSM 관리 주체**(노드인프라 vs 우리)·망분리 요건.
  - [ ] (선택) 캔톤 네이티브 트래블룰(예: VerifyVASP) 연동 가능 여부.

## B. 프로비저닝(자격증명) — 무스비가 발급
- [ ] **Canton Party ID** — 우리 정산 네트워크 신원.
- [ ] **JWT signing credentials** — API 인증용.
- [ ] **정산 네트워크 endpoint + TLS(mTLS) 인증서**.
- [ ] **우리에게 부여되는 role** — `institution` / `custodian-sender`(자가 커스터디면). 수신측은 누구 role로.

## C. 소프트웨어/패키지
AWS Sandbox에 띄울 우리 스택의 구성요소(노드월렛 SW는 §A).
- [ ] **Musubi Backend 배포물** — 도커 이미지명/레지스트리/**버전**, 설정 방식(env/config).
- [ ] **Canton Participant Node** — 이미지/버전, 요구사양.
- [ ] **DAR/패키지 ID** — `FXOrder` 등 정산 패키지가 네트워크에 이미 있나/우리가 업로드하나, **패키지 ID**.
- [ ] **OpenAPI 스펙 파일 + Console 접근** — 역할별 OpenAPI 스펙 파일 위치, Console 계정. (Webhook 지원 여부 확인)

## D. 자산/인스트루먼트
- [ ] **KRWK 인스트루먼트** — 라이브는 JPYSC0/USDCx인데, PoC용 **KRWK는 누가/어떻게 발행**하나. 테스트 발행자/레지스트리.
- [ ] **상대 통화** — JPYC(JPYSC0)·USDCx 중 무엇으로 시연. 테스트 토큰 발급(faucet) 절차.

## E. 카운터파티 / 마켓메이커 (4-leg 필수)
- [ ] **Market Maker** — 4-leg엔 MM이 필수. PoC에서 MM은 누가 맡나(노드인프라/무스비가 테스트 MM 제공?).
- [ ] **수신 카운터파티** — 일본은행 그룹 측 엔티티(신세이/VCT/홀딩스)와 수신 Custodian은 누가. 샌드박스에선 노드인프라가 모킹/대행하나.
- [ ] **카운터파티 디렉토리** — receiver·custodian의 Party ID를 어디서 받나.

## F. 인프라/배포 (AWS Sandbox)
- [ ] **권장 footprint** — participant + 노드월렛 + Musubi backend + Postgres의 인스턴스 사양·OS·리소스.
- [ ] **배포 자료** — AWS용 배포 가이드/Terraform/Compose 등 제공 여부.
- [ ] **아웃바운드 연결 요구** — 어떤 호스트/포트로 나가야 하나(Synchronizer·SV·무스비 endpoint).
- [ ] **whitelist** — 커스터디 플랫폼에 "Musubi 정산 주소" whitelist가 필요한가(자가 커스터디 시 무엇을).

## G. 운영/검증
- [ ] **연결 테스트 절차** — `/health`, `/whoami`, 테스트 order 생성 등.
- [ ] **모니터링** — `GET /api/v1/dashboard/stats`(상태별 order·정산량) 등 대시보드.
- [ ] **지원/에스컬레이션** — PoC 기간 지원 채널, 담당자, 일정.

## H. 키 보관
- [ ] **키 보관** — 노드월렛(HSM/망분리) 사용 시 키 관리 주체·격리 요건. (위 A의 노드월렛 항목과 연계)

## 우선순위 (먼저 받아야 진행되는 것)
1. **A(환경 선택·온보딩) + B(프로비저닝)** — 이게 있어야 AWS에서 노드를 띄워 연결 가능.
2. **C(소프트웨어·패키지) + F(배포 자료)** — 실제 기동.
3. **D(KRWK·통화) + E(MM·카운터파티)** — 정산 시나리오 실행.
4. **G(검증) + H(키 보관)** — 마무리·합격 판정.
</content>
