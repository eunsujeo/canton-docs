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
