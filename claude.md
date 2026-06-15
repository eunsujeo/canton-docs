# Canton 문서 한국어 위키 — 메인터너 가이드 (Schema)

이 저장소는 **Canton Network 공식 문서를 한국어로 번역**해 다른 개발자와 공유하기 위한 지식베이스다.
이 파일은 LLM 에이전트가 위키를 일관되게 구축·유지하도록 하는 **규칙 문서**다. 패턴의 배경은 `llm-wiki.md` 참고.

## 목표
- 개발자가 Canton을 이해하도록 돕는 **충실한 한국어 번역** + 상단 **개발자 노트**(요약·핵심 용어·선행 개념)를 제공한다.
- 모든 페이지는 **반드시 원문 출처 링크**를 포함한다. (출처 누락 금지)
- 위키는 누적되는 산출물이다. 번역할수록 인덱스·용어집·교차링크가 풍부해진다.

## 3개 레이어
1. **원본 소스 (immutable)** — Canton 공식 문서. 모든 페이지는 `<url>.md`로 클린 마크다운을 받을 수 있다.
   전체 목록은 루트의 `llms.txt`. 절대 수정하지 않는다.
2. **위키 (`wiki/`)** — LLM이 생성·유지하는 한국어 마크다운. 원본 URL 경로 구조를 그대로 미러링한다.
3. **스키마 (이 파일)** — 구조·규칙·워크플로 정의.

## 범위 (Scope)
- **포함 (315페이지)**: `overview/`, `appdev/`, `global-synchronizer/`, `integrations/`
- **제외**: 루트 `reference/`(자동생성 API 레퍼런스 473개), `api-reference.md`
- 작업 큐와 상태는 `wiki/sources.md`에서 관리한다.

## 디렉토리 구조
```
canton/
├─ CLAUDE.md            # 이 파일 (스키마)
├─ llm-wiki.md          # 패턴 설명 (참고용)
├─ llms.txt             # 원문 전체 인덱스 (소스 오브 트루스)
└─ wiki/
   ├─ index.md          # 카탈로그 + 추천 학습 순서
   ├─ sources.md        # 315개 소스 목록 + 번역 상태 (작업 큐 겸 출처 레지스트리)
   ├─ glossary.md       # 용어 번역 일관성 규칙
   ├─ log.md            # 작업 이력 (append-only)
   ├─ overview/…        # 원문 경로 미러링
   ├─ appdev/…
   ├─ global-synchronizer/…
   └─ integrations/…
```
저장 경로 규칙: 원문 `https://docs.canton.network/<PATH>.md` → `wiki/<PATH>.md`

## 페이지 템플릿 (필수 형식)
번역 페이지는 반드시 아래 형식을 따른다. **상단 출처 링크와 frontmatter는 필수.**

```markdown
---
title: <한국어 제목>
source: <원문 전체 URL>
translated: <YYYY-MM-DD>
status: done            # done | partial
tags: [overview, ...]   # 섹션/주제
---

> **출처(원문)**: [<원문 제목>](<원문 URL>) · 번역일 <YYYY-MM-DD>

## 📌 개발자 노트
- **한 줄 요약**: 이 페이지가 무엇을 다루는지 1~2문장.
- **핵심 용어**: 새로 등장한 용어 2~5개 (한국어(영문)).
- **선행 개념**: 먼저 읽으면 좋은 위키 페이지 링크 `[제목](상대경로)`.

---

<여기부터 원문의 충실한 한국어 번역>
```

## 번역 규칙
- **충실 번역**: 원문의 문단·제목·표·순서를 1:1로 유지한다. 임의 요약/생략 금지. (요약은 상단 개발자 노트에만.)
- **용어 일관성**: 번역 전 `wiki/glossary.md`를 확인한다. 새 용어는 용어집에 먼저 추가하고 번역한다.
- **번역하지 않는 것**: 코드 블록, 명령어, 식별자, API/타입/함수명, 파일 경로, 제품·프로토콜 고유명(Canton, Daml, Splice 등).
- **링크 처리**: 원문 내 `docs.canton.network` 내부 링크가 이미 번역된 위키 페이지를 가리키면 위키 상대경로로 교체하고, 아니면 원문 URL을 유지한다.
- **이미지**: `![alt](url)` 형태는 원문 URL을 유지하고 alt 텍스트만 번역한다.
- **mermaid 펜스 정규화**: 원문의 `` ```mermaid theme={...} ``는 Mintlify 전용이라 Obsidian/Docsify에서 렌더 문제를 일으킨다 → 표준 `` ```mermaid ``로만 쓴다(다이어그램 내부 내용은 그대로 유지). 큰 다이어그램 잘림은 `wiki/.obsidian/snippets/mermaid-fit.css` 스니펫으로 해결.

## 워크플로

### Ingest (페이지 번역) — `translate-canton` skill 사용
1. `wiki/sources.md`에서 다음 대상 페이지의 원문 URL을 고른다 (또는 사용자가 지정).
2. 원문 `<url>.md`를 가져온다 (`curl -s <url> -o /tmp/...` 또는 WebFetch raw).
3. glossary 확인 → 새 용어 추가.
4. 페이지 템플릿대로 `wiki/<PATH>.md`에 저장. **출처 링크 필수.**
5. `wiki/sources.md`의 해당 행 상태를 ☐ → ☑로 변경.
6. `wiki/index.md`의 카테고리 섹션에 한 줄 요약과 함께 등록. 선행/관련 페이지 교차링크 추가.
7. `wiki/log.md`에 `## [날짜] ingest | <제목>` 추가.
8. 한 번에 여러 페이지를 처리할 때는 병렬로 가져오되 위의 갱신 단계를 빠짐없이 수행한다.

### Query (질문 답변)
- 먼저 `wiki/index.md`와 `sources.md`를 보고 관련 페이지를 찾아 읽고, 출처를 인용해 답한다.
- 유용한 답변(비교표·개념 정리 등)은 위키 페이지로 환원해 저장한다.

### Verify / Lint (검증·건강 점검) — `verify-canton` skill 사용
- **page 모드**: 번역 페이지를 원문(`<source>.md`)과 1:1 대조 — 출처·구조 충실도·내용 누락·코드 불변·용어 일관성·오역.
- **lint 모드**: 위키 전체 — 상태 불일치(sources.md↔파일), 출처 누락, 인덱스 누락, 깨진/고아 링크, 용어 불일치, 모순/구식.
- 검증은 보고 우선, 수정은 승인 후. 자주 등장하지만 페이지 없는 핵심 개념은 새 페이지 후보로 제안한다.

## 보기(Viewing)
- **Obsidian (로컬)**: `wiki/` 폴더를 보관소(vault)로 열기. 그래프 뷰·백링크. 안내는 `wiki/how-to-read.md`.
- **Docsify (웹)**: `wiki/index.html`이 셸. 로컬은 `cd wiki && python3 -m http.server 4500`, 웹은 GitHub Pages(`/wiki`) 배포. 검색·mermaid·코드복사 플러그인 포함.
- 번역 페이지 간 교차링크는 **상대경로 마크다운 링크**로 작성한다(Obsidian·Docsify 둘 다 해석). 미번역 대상 링크만 원문 URL 유지.
- 새 페이지를 추가하면 `cd wiki && python3 scripts/gen_sidebar.py`로 Docsify `_sidebar.md`를 재생성한다(translate-canton이 자동 수행).

## 진행 상황 확인
- 남은 작업: `grep -c "| ☐ |" wiki/sources.md`
- 완료: `grep -c "| ☑ |" wiki/sources.md`
- 최근 이력: `grep "^## \[" wiki/log.md | tail -5`
