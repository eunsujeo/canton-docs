# 계획 — 외부 공유용 "Canton DvP 정산 개념 설명서" (입문자 대상)

> 다음 세션에서 이 계획대로 설명 문서를 작성한다. (이 파일 = 세션 리셋 후 핸드오프 문서)

## 확정된 방향 (사용자 결정)
- **청중**: Canton/블록체인을 모르는 일반 독자
- **형식**: 읽는 **개념 설명서** (발표 자료 아님)
- **대외비**: **외부 공유용 = 일반화** — 회사·Musubi·POC 참여사 실명 금지, **역할 기반 용어**(참여 기관·운영사·발행자)
- → **위치: `wiki/`** (공유 지식베이스 성격과 일치). 권장 파일명: `wiki/notes/canton-dvp-settlement-explainer.md` (또는 별도 top-level guide)

## 목표 / 성공 기준
- Canton을 모르는 사람이 **끝까지 읽으면** "기관 간 정산을 Canton으로 *왜*·*어떻게* 하는지" 그림이 잡힌다.
- 전문용어는 **처음 등장 시 한 줄 정의**(툴팁/괄호). **다이어그램으로 보여주기 우선**, 설명은 짧게.
- 깊은 내용은 기존 노트로 **링크**(이 문서는 *입문 온램프*).

## 구성 (입문자 narrative — zero부터)
1. **훅: 문제부터** — "통화/자산을 맞바꾸는데 누가 먼저 보내?" = 카운터파티 리스크(Herstatt 일화).
2. **블록체인이 답? + Canton의 위치** — L1/프라이버시 보존 L1을 아주 가볍게.
3. **Canton 핵심 3개념** — ① 파티/노드(누가 무엇을 보관) ② 부분 트랜잭션 프라이버시(관련자만 봄) ③ 원자성(전부/전무).
4. **DvP 정산이란 + 교환 과정** — 제안→수락→개시→양측 잠금→원자적 실행 (시퀀스 다이어그램).
5. **프라이버시 — 제3자는 못 본다** — 데모로 증명한 장면을 일반화해 서술(외부자 패널이 빈다).
6. **토큰은 어디서 오나** — 발행자=레지스트리, 두 패턴(외부발행+브릿지 / Canton 직접발행) 흐름도.
7. **누가 무엇을 운영하나** — 참여 기관 / 운영사(venue) / 발행자 역할 + "정산 DAR은 모든 노드, 운영사 백엔드는 운영사만" 한 줄.
8. **한 장 요약 + 더 읽기** — 기존 노트 링크.

## 재사용할 기존 자료 (이미 작성됨 — 새로 쓰지 말고 엮기)
| 절 | 기존 노트/자료 |
|---|---|
| 문제·원자성 | `wiki/notes/atomic-dvp-real-differentiator.md` |
| Canton 위치·계층 | `wiki/notes/blockchain-layers-l0-l1-l2.md` |
| B2B/B2C 적합성 | `wiki/notes/canton-b2b-vs-b2c.md` |
| 정산 앱 2층 구조 | `wiki/notes/dvp-settlement-app-architecture.md` |
| 발행/브릿지 패턴·flow | `wiki/notes/token-issuance-bridge-patterns.md` |
| 용어 | `wiki/glossary.md` · `wiki/notes/term-cheatsheet.md` |
| 프라이버시 시연 수치(일반화해 인용) | `dev/demo/` (회사·포트 등 내부 디테일 제외) |

→ 새 글은 이것들을 **하나의 입문 흐름으로 stitch**하고, 다이어그램은 핵심만 인라인(시퀀스 1~2개), 나머지는 링크.

## 작성 규칙 (CLAUDE.md 위키 규칙 준수)
- frontmatter(title, type: note, translated, status, tags) + 상단 ⚠️ 내부작성 정리 노트 배너(번역본 아님).
- **회사·Musubi·POC 참여사명 절대 금지** → 역할 기반(참여 기관 A/B·운영사·발행자). 통화도 일반화(통화 A/B 또는 예시 표기).
- mermaid는 **표준 펜스** ```mermaid (theme 금지).
- 새 페이지 → `wiki/index.md` 카탈로그 등록 + 추천 학습순서에도 추가 검토.
- 스크립트 재생성: `cd wiki && python3 scripts/gen_sidebar.py && python3 scripts/gen_nav.py && python3 scripts/gen_tooltips.py`
- 어려운 새 용어는 **glossary 툴팁 표에 먼저 추가**(카운터파티 리스크 등).
- `wiki/log.md`에 이력 한 줄.

## 작업 순서 (새 세션에서)
1. 이 계획 + 위 재사용 노트 6개 훑기.
2. outline 확정 → 초안(plain 언어 + 시퀀스 다이어그램 인라인).
3. index 등록 + 스크립트 재생성 + 툴팁.
4. **입문자 관점 검토**(용어 막히는 곳 없나) → 커밋·푸시.

## 새 세션 킥오프 프롬프트 (그대로 붙여넣기)
> `dev/docs/explainer-doc-plan.md`를 읽고, 그 계획대로 **Canton을 모르는 일반 독자용 "DvP 정산 개념 설명서"** 를 `wiki/`에 만들어줘. 외부 공유용이라 회사·프로젝트 고유명은 빼고 **역할 기반**으로. 기존 `wiki/notes`의 관련 노트들을 **입문자용 한 흐름으로 엮고**, CLAUDE.md 위키 규칙(인덱스 등록·스크립트 재생성·툴팁)도 지켜줘. 먼저 outline을 보여주고 확정받은 뒤 작성해줘.
