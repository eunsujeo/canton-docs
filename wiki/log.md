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

## [2026-06-15] ingest | 글로벌 동기화자 묶음 2종
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
