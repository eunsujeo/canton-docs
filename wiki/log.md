# 작업 로그 (Log)

추가 전용(append-only) 기록. 각 줄은 `## [날짜] 작업유형 | 대상` 형식으로 시작한다.
조회: `grep "^## \[" wiki/log.md | tail -5`

## [2026-06-15] setup | 위키 초기화
- `llms.txt`에서 전체 789페이지 중 학습용 315페이지를 범위로 확정 (overview/appdev/global-synchronizer/integrations). 자동생성 API 레퍼런스 473개 제외.
- `wiki/sources.md`(소스 매니페스트 겸 작업 큐), `index.md`, `log.md`, `glossary.md` 생성.
- CLAUDE.md 번역 가이드 및 `translate-canton` skill 작성.

## [2026-06-15] ingest | Canton Network이란? (what-is-canton)
- 첫 번역 페이지. `wiki/overview/understand/what-is-canton.md`. 동작 예시로 작성. glossary 용어 적용.

## [2026-06-15] verify | what-is-canton
- verify-canton page 모드 검증: 출처·구조·코드·표·용어·오역 전부 ✅ 통과.

## [2026-06-15] setup | Obsidian 보기 환경
- `wiki/how-to-read.md`(읽는 방법+Obsidian 안내), `.obsidian/app.json`(상대 마크다운 링크 기본값) 추가. index에서 링크.

## [2026-06-15] setup | Docsify 웹 뷰어
- `index.html`(Docsify 셸: 검색·mermaid·코드복사·페이지네이션), `_sidebar.md`, `.nojekyll`, `scripts/gen_sidebar.py` 추가.
- 로컬 서빙 검증: 셸/콘텐츠/사이드바 HTTP 200. translate-canton에 사이드바 자동 갱신 단계 연결.
- GitHub Pages는 branch 배포 시 root/docs 폴더만 허용 → `wiki/` 유지 위해 `.github/workflows/deploy-pages.yml`(Actions 배포) 추가. Source를 "GitHub Actions"로 설정.

## [2026-06-15] setup | 용어 tooltip
- `glossary.md` "툴팁 정의" 표 + `scripts/gen_tooltips.py`(멱등, 중첩방지). 웹은 tippy.js, Obsidian은 네이티브 abbr title.

## [2026-06-15] ingest | 개요 "이게 뭔가" 묶음 3종
- who-should-read, the-problem, cantons-solution 번역 완료. Mintlify 컴포넌트(Card/Note)→마크다운, mermaid 펜스 정규화. 완료 4/315.

## [2026-06-15] ingest | 개요 "빠른 개요" 묶음 3종
- five-minute-overview, core-concepts, use-cases 번역 완료. haskell/mermaid 펜스 정규화, Card/Note/Warning→마크다운. 완료 7/315.

## [2026-06-15] ingest | overview/learn "작동 원리" 5종
- architecture, ledger-model, how-transactions-work, privacy-model, trust-model 번역 완료. haskell/mermaid 펜스 정규화, Card/Note/Warning/Check→마크다운. 완료 12/315.

## [2026-06-15] ingest | 글로벌 Synchronizer 묶음 2종
- overview/understand/global-synchronizer, overview/learn/global-synchronizer-architecture 번역 완료. 내부 todo div 제외, mermaid 펜스 정규화. 완료 14/315.

## [2026-06-15] ingest | appdev 앱 개발 입문 3종
- choose-your-path, m1-understanding-canton, m2-canton-for-ethereum-devs 번역 완료. Accordion/Card→마크다운, solidity/haskell/mermaid 펜스 정규화. 완료 17/315.

## [2026-06-15] ingest | overview 완결 (understand 4 + learn 4)
- understand: canton-coin, cips-introduction, getting-app-featured, glossary.
- learn: cryptographic-keys, multi-synchronizer, two-layer-consensus, validator-architecture.
- 내부 todo div/COPIED 마커 제외, Note/Warning/Tip/img·mermaid·protobuf 펜스 정규화. overview/understand·overview/learn 학습 페이지 전부 완료. 완료 25/315.

## [2026-06-15] ingest | overview/reference Group A (8)
- synchronizer-overview, canton-protocol-specification, cip-index, canton-name-service, tokenomics-of-gs, decentralization, ordering-consensus, cross-sync-dvp-example. 완료 33/315.

## [2026-06-15] ingest | overview/reference Group B (9)
- transaction-lifecycle, smart-contract-consensus, splice-wallet-reference, sv-governance-reference, canton-coin-tokenomics, reassignment-protocol, cip-0056, what-are-cips, super-validator-components. 완료 42/315.

## [2026-06-15] ingest | overview/reference Group C (5)
- pruning, validator-node-components, external-party, topology, ledger-causality. 완료 47/315.

## [2026-06-15] note | 블록체인 계층 (L0/L1/L2)
- 내부 작성 정리 노트 `notes/blockchain-layers-l0-l1-l2.md` 추가. L0/L1/L2 구분 + Canton 위치. glossary에 레이어 0/2 정의 추가. 사이드바에 "정리 노트" 섹션.

## 2026-06-15 — overview/reference 완료
- `ledger-model-detailed.md` (원장 모델 상세 형식 명세, 1018행) 번역
- `gsf-policies.md` (Canton Foundation 정책 — 멤버십·위원회·거버넌스·네트워크 정책·업그레이드·CIP·채널) 번역
- **overview/reference 24개 전부 완료** → overview 섹션(understand+learn+reference) 전체 번역 완료
- 누적: 49 content pages + 1 note

## 2026-06-15 — note | eUTXO와 이중지불 방지 (지폐 비유)
- `notes/eutxo-double-spend.md` 신설: "존재하지 않는 것은 쓸 수 없다"를 지폐 비유로 쉽게 설명(eUTXO·세 방어선·전역 가시성 없는 무결성)
- `cantons-solution.md`: 욱여넣은 이중지불 방지 한 문장을 풀어주는 💡 설명 + 노트 링크 추가(충실성 유지)

## 2026-06-15 — 용어 변경 | 동기화자 → Synchronizer
- 사용자 결정: Synchronizer를 시퀀서·미디에이터·밸리데이터 등 형제 구성요소와 톤을 맞춰 영문 유지
- 위키 전체 일괄 치환(동기화자→Synchronizer, 723곳/51파일), 첫등장 병기 중복 정리, glossary 변환표·툴팁 갱신
- 동사 '동기화'(synchronize)는 보존

## 2026-06-15 — 가독성 | 툴팁 용어 대폭 확대 + 뷰 인라인 역주
- 사용자 피드백: 충실 번역이라 본문에 용어가 정의 없이 등장(예: '뷰')해 어렵다
- 결정(툴팁 대폭 확대): glossary 툴팁 표에 22개 용어 추가(시퀀서·미디에이터·참여자 노드·원장·합의·BFT·커밋·확인·보관·활성 컨트랙트·eUTXO·트래픽·DvP·토큰화·DSO·CIP·Splice·커맨드·다자간 워크플로·이중지불·트랜잭션·스마트 컨트랙트) → 47개 용어, 전 페이지 자동 마우스오버 정의
- cantons-solution: '뷰' 첫 등장에 💡 인라인 역주 추가
- CLAUDE.md 번역 규칙에 '정의 없이 등장하는 용어 처리(툴팁 1차+필요시 💡역주)' 정책 명문화

## 2026-06-15 — note | 로컬 파티 vs 외부 파티
- `notes/local-vs-external-party.md` 신설: 키 보유 주체(노드 vs 본인) 중심 비교, SPN/CPN/OPN 권한, 자기수탁, 외부 파티 제출 흐름(PPN/EPN), B2B 정산 맥락

## 2026-06-15 — note | 파티 설계 per-user vs 옴니버스
- `notes/party-design-per-user-vs-omnibus.md` 신설: 파티 생성 비용·상태 때문에 유저별 파티는 선택사항, 거래소식 옴니버스 패턴, B2B 정산 맥락

## 2026-06-15 — ingest | appdev 입문 묶음(로컬 실습)
- `appdev/quickstart/index.md` (Canton Network QuickStart)
- `appdev/quickstart/prerequisites.md` (사전 요구사항·설치)
- `appdev/quickstart/running-the-demo.md` (데모 실행하기 — 라이선스 워크플로)
- `appdev/modules/m5-localnet-development.md` (LocalNet 개발)
- 목적: overview 학습 후 로컬 PC에서 직접 실습(LocalNet)하기 위한 입문 4페이지

## 2026-06-16 — note | Canton 환경 4단계(LocalNet→DevNet→TestNet→MainNet)
- `notes/canton-environments-localnet-to-mainnet.md` 신설: 로컬=LocalNet vs 공유망(연결+온보딩), 절차·IP allowlist·환경별 차이

## 2026-06-16 — note | Canton vs Splice
- `notes/canton-vs-splice.md` 신설: Canton=기반 프로토콜(엔진), Splice=공개망 운영 앱 묶음(토큰·월렛·Scan·거버넌스). CC=Splice의 Amulet

## 2026-06-16 — note | 용어 한 컷 카드(치트시트)
- `notes/term-cheatsheet.md` 신설: 학습 중 자주 재질문한 핵심 용어를 한 줄 비유로 모음(복습용). index notes 최상단 ⭐ 등록

## 2026-06-16 — note | Canton 위 기관 간 DvP 정산 앱 2층 구조
- `notes/dvp-settlement-app-architecture.md` 신설: 온-원장 Daml(정산 강제)+오프-원장 백엔드, 구조도, 밸리데이터 자체호스팅/NaaS. 역할 기반(공개 배포)

## 2026-06-16 — note | BTC vs Ethereum vs Canton 비교
- `notes/btc-ethereum-canton-compare.md` 신설: 데이터모델·합의·확정·프라이버시·용도 3자 비교 + 블록 익스플로러(mempool/etherscan/cantonscan) URL

## 2026-06-16 — note + 다듬기 | Synchronizer 종류(사설/컨소시엄/글로벌)
- two-layer-consensus: "그 Synchronizer에 대해 전역적으로 고유한" → "그 Synchronizer 안에서 고유한"으로 명확화
- `notes/synchronizer-types-private-consortium-global.md` 신설: 운영주체·참여범위·신뢰·탈중앙 비교

## 2026-06-16 — note | ISS 합의 알고리즘
- `notes/iss-consensus.md` 신설: 멀티 리더 BFT 순서화, 단일 리더 병목 해소, 1/3 비잔틴·결정적 확정·프라이버시

## [2026-06-17] ingest | Scan 읽는 법 (notes)
- LocalNet Scan UI 학습 정리 노트 추가. SV/DSO·마이닝 라운드·Amulet·Tap·Automation. glossary 툴팁 4개(Scan/Amulet/마이닝 라운드/Tap) 추가, index 등록, gen 3종 실행.

## [2026-06-17] edit | 블록 개념 정정 (ISS·Scan 노트)
- "Canton엔 블록 없음" 오해 정정: 시퀀서 순서화 계층엔 블록 있음(암호봉투 순서묶음), 확정은 이해관계자 계층. 라운드≠블록≠트랜잭션 박스 추가.

## [2026-06-17] ingest | 원자적 DvP 차별점 노트
- 원자성·잠금·조합성은 이더도 됨, Canton 차별점=프라이버시+다자권한+결정적확정 결합. index 등록, gen 3종.
