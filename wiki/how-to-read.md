---
title: 읽는 방법 & Obsidian으로 보기
tags: [가이드, meta]
---

# 이 위키 읽는 방법

Canton 공식 문서를 한국어로 번역한 개발자용 지식베이스입니다. 처음 보는 분을 위한 안내.

## 1) Obsidian으로 열기 (권장)
이 위키는 [Obsidian](https://obsidian.md)에서 보기 좋게 만들어졌습니다.

1. Obsidian 설치 후 **"Open folder as vault"** 선택.
2. 이 저장소의 **`wiki/` 폴더**를 보관소(vault)로 연다. (루트가 아니라 `wiki/`를 열어야 깔끔함)
3. 왼쪽 파일 탐색기에서 `index.md`를 먼저 연다 → 추천 학습 순서대로 링크를 따라간다.
4. 상단 **그래프 뷰(graph view)** 아이콘으로 페이지 간 연결 관계를 한눈에 본다.
5. 각 페이지의 **백링크(backlinks)** 패널로 "이 페이지를 참조하는 다른 페이지"를 확인한다.

> 팁: 페이지 상단의 **📌 개발자 노트**(한 줄 요약·핵심 용어·선행 개념)를 먼저 읽고 본문으로 들어가면 빠릅니다.
> 모르는 용어는 [glossary.md](glossary.md)에서 한국어-영문 대응을 확인하세요.

## 2) 추천 학습 순서 (Reading Path)
전체 카탈로그와 최신 순서는 [index.md](index.md) 참고. 요약하면:

1. **이게 뭔가** — `overview/understand/`: who-should-read → [what-is-canton](overview/understand/what-is-canton.md) → the-problem → cantons-solution
2. **빠른 개요** — five-minute-overview → core-concepts → glossary(원문) → use-cases
3. **작동 원리** — `overview/learn/`: architecture → ledger-model → how-transactions-work → privacy-model → trust-model
4. **글로벌 동기화자** — global-synchronizer → global-synchronizer-architecture
5. **앱 개발** — `appdev/`: choose-your-path → m1-understanding-canton, (블록체인 경험자) m2-canton-for-ethereum-devs

## 3) 웹으로 보기 (Docsify — 세팅 완료)
이 `wiki/` 폴더는 **Docsify** 정적 사이트로 바로 볼 수 있게 세팅돼 있습니다(빌드 불필요). `index.html`이 마크다운을 그대로 렌더링합니다.

**로컬 미리보기** (이 폴더에서):
```bash
python3 -m http.server 4500
# 브라우저에서 http://localhost:4500 접속
```

**GitHub Pages로 무료 배포** (다른 개발자에게 웹 링크 공유):
> ⚠️ GitHub의 "Deploy from a branch"는 폴더를 `/ (root)` 또는 `/docs`만 허용한다. `/wiki`는 못 고른다.
> 그래서 폴더명을 유지한 채 **GitHub Actions**로 배포한다 (`.github/workflows/deploy-pages.yml` 포함됨).

1. 이 저장소를 GitHub에 푸시 (기본 브랜치 `main` 또는 `master`).
2. 저장소 **Settings → Pages → Source**를 **"GitHub Actions"**로 변경.
3. 푸시 때마다 워크플로가 `wiki/` 폴더를 자동 배포. Actions 탭에서 완료되면 URL이 발급됨.

> 대안(Actions 없이): `wiki/` 폴더를 `docs/`로 이름만 바꾸면 "Deploy from a branch + /docs"로도 배포 가능.

> `_sidebar.md`(왼쪽 내비)는 번역이 늘면 다시 생성해야 합니다 → `translate-canton` 실행 시 자동 갱신.
> 검색·이전/다음·코드 복사·mermaid 렌더링 플러그인이 포함돼 있습니다.

> 대안: **Obsidian Publish**(유료)로 그래프·백링크까지 그대로 웹 게시도 가능.

## 4) 핵심 파일
- [index.md](index.md) — 카탈로그 + 학습 순서
- [glossary.md](glossary.md) — 용어 대응표
- [sources.md](sources.md) — 원문 출처 + 번역 진행 상태
- [log.md](log.md) — 작업 이력
