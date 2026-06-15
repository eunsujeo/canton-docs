---
name: translate-canton
description: Canton Network 공식 문서를 한국어로 번역해 wiki/에 저장하고 인덱스·용어집·로그를 갱신한다. 사용자가 Canton 문서 번역, "다음 페이지 번역", 특정 Canton URL/주제 번역, 또는 번역 진행 상황을 요청할 때 사용.
---

# translate-canton

Canton 공식 문서를 한국어로 번역해 이 저장소의 위키에 누적한다. 규칙 전문은 루트 `CLAUDE.md` 참고.

## 핵심 규칙 (반드시 지킬 것)
- **출처 필수**: 모든 번역 페이지 상단에 원문 URL 링크와 frontmatter `source:`를 넣는다. 출처 없는 페이지 생성 금지.
- **충실 번역**: 원문 구조(제목·문단·표·순서)를 1:1 유지. 요약·생략은 상단 "개발자 노트"에만.
- **번역 제외**: 코드/명령어/식별자/API·타입·함수명/경로/고유명(Canton, Daml, Splice, Canton Coin, Global Synchronizer 등).
- **용어 일관성**: 번역 전 `wiki/glossary.md` 확인, 새 용어는 먼저 추가.
- **mermaid 펜스**: 원문 `` ```mermaid theme={...} ``는 표준 `` ```mermaid ``로 정규화(내부 내용 유지). Obsidian/Docsify 렌더 호환.

## 대상 선정
- 사용자가 URL·제목·주제를 지정하면 그것을. 아니면 `wiki/sources.md`에서 상태 `☐`인 다음 페이지를 추천 학습 순서(`wiki/index.md`)에 따라 고른다.
- 범위: `overview/ appdev/ global-synchronizer/ integrations/` 만. 루트 `reference/`(API 자동생성)는 제외.

## 절차
1. **원문 수집**: 원문은 `<url>.md`로 클린 마크다운을 받을 수 있다.
   - 예: `curl -s https://docs.canton.network/overview/understand/what-is-canton.md -o /tmp/canton-src.md`
   - 여러 페이지면 병렬로 받는다.
2. **용어 점검**: `wiki/glossary.md`를 읽고 새 용어를 추가한다.
3. **번역·저장**: 저장 경로는 원문 경로 미러링 → `wiki/<PATH>.md`. 아래 템플릿을 따른다.
4. **상태 갱신**: `wiki/sources.md`에서 해당 행 `☐` → `☑`.
5. **인덱스 갱신**: `wiki/index.md` 카테고리 섹션에 한 줄 요약 + 교차링크 추가.
6. **로그**: `wiki/log.md`에 `## [YYYY-MM-DD] ingest | <제목>` 추가. (오늘 날짜는 환경의 currentDate 사용.)
7. **웹 내비 갱신**: `wiki/`에서 `python3 scripts/gen_sidebar.py` 실행해 Docsify `_sidebar.md`를 재생성한다.
8. **용어 tooltip**: 설명이 필요한 용어를 `glossary.md`의 "툴팁 정의" 표에 추가한 뒤 `python3 scripts/gen_tooltips.py` 실행 → 각 페이지 첫 등장에 `<abbr>` 자동 삽입(웹·Obsidian 공용).
9. **이전/다음 내비**: `python3 scripts/gen_nav.py` 실행 → `_sidebar.md` 순서대로 각 페이지 하단에 이전/다음 링크 삽입(웹·Obsidian 공용, 멱등). gen_sidebar 다음에 실행.

## 페이지 템플릿
```markdown
---
title: <한국어 제목>
source: <원문 전체 URL>
translated: <YYYY-MM-DD>
status: done
tags: [<섹션>, ...]
---

> **출처(원문)**: [<원문 제목>](<원문 URL>) · 번역일 <YYYY-MM-DD>

## 📌 개발자 노트
- **한 줄 요약**: …
- **핵심 용어**: 용어A(EnglishA), 용어B(EnglishB)
- **선행 개념**: [관련 페이지](상대경로)

---

<원문의 충실한 한국어 번역>
```

## 진행 상황
- 남은: `grep -c "| ☐ |" wiki/sources.md` / 완료: `grep -c "| ☑ |" wiki/sources.md`
- 최근 이력: `grep "^## \[" wiki/log.md | tail -5`

## 배치 처리
여러 페이지를 한 번에 요청받으면: 원문을 병렬로 받고 각 페이지를 템플릿대로 저장한 뒤, sources/index/log 갱신을 빠짐없이 수행한다. 작업 후 몇 개 완료/남았는지 보고한다.
