# Next Step — 남은 번역 작업과 읽는 순서

> overview 섹션(50페이지)은 **전체 완료**. 이 문서는 **남은 3개 섹션**(appdev / global-synchronizer / integrations)의
> 작업 우선순위와 **읽는 순서**를 정리한다. 새 세션에서 이어서 작업하거나, 미팅 후 더 깊이 파고들 때의 길잡이.

## 현재 진행률 (2026-06-15 기준)

| 섹션 | 완료 | 남음 | 비고 |
|---|---|---|---|
| overview | 46 | 0 | ✅ **완료** — 미팅 핵심 자료 |
| appdev | 3 | 141 | 앱 개발자 가이드 (<abbr class="gloss" title="다자간 워크플로를 위해 설계된 Canton의 스마트 컨트랙트 언어">Daml</abbr> 개발) |
| global-synchronizer | 0 | 95 | SV·<abbr class="gloss" title="파티를 호스팅하고 그 파티의 컨트랙트 데이터를 저장하는 참여자 노드">밸리데이터</abbr> 노드 운영/배포 |
| integrations | 0 | 30 | 지갑·거래소·dApp 연동 (B2B 정산 직결) |
| **합계** | **49** | **266** | overview 전체(understand/learn/reference) 완료 |

> 진행 상황 <abbr class="gloss" title="이해관계자 밸리데이터가 트랜잭션이 유효함을 미디에이터에 응답하는 것(confirmation)">확인</abbr>: `grep -c "| ☑ |" sources.md` (완료) / `grep -c "| ☐ |" sources.md` (남음)

---

## 우선순위 권고

미팅 목표(Canton 이해도 향상)와 **멀티체인 B2B 정산** 맥락을 기준으로:

1. **integrations (30페이지)** — 가장 작고, B2B 정산·지갑·거래소 연동과 직결. **다음 1순위.**
2. **appdev 모듈+get-started (핵심만 ~20페이지)** — 실제 Daml 앱 개발 입문. 전체 141 중 모듈/입문만 선별.
3. **global-synchronizer 이해편 (understand 5 + splice-fundamentals)** — 운영 배경 개념만.
4. 나머지 (appdev/reference·deep-dives, gs/deployment·operations) — 레퍼런스성. 필요 시 on-demand.

> ⚠️ 141 + 94는 대부분 자동생성성 레퍼런스/운영 절차. **전부 번역하기보다 학습에 필요한 핵심을 선별**하는 편이 비용 대비 효과가 좋다.

---

## 섹션별 읽는 순서

### A. integrations — 연동/연계 (30페이지) · 1순위
B2B 정산·지갑·거래소 연동의 큰 그림 → 패턴 → SDK 순.

1. `integrations/overview` (Integrations Overview) — 연동 전체 지도
2. `integrations/.../ecosystem` (Canton Network Ecosystem) — 생태계 구성요소
3. `integrations/.../integration-patterns` (Integration Patterns) — 연동 패턴 분류
4. `integrations/.../dapp-building-overview` (dApp Building Overview)
5. **지갑 트랙**: How Canton Wallets Differ from Web3 Wallets → Wallets for Users → Wallet Provider Integration → Wallet SDK (Usage/APIs/Configuration) → Wallet Gateway
6. **거래소 트랙**: Exchange Integration Guide → Exchange SDK (Download/Usage) → Validator Node Operations → Proof of Transfer
7. **앱 탐색**: Finding Canton Network Apps, Adapters and Discovery, Best Practices

### B. appdev — 앱 개발자 가이드 (핵심 선별)
이미 완료: [choose-your-path](appdev/get-started/choose-your-path.md), [m1](appdev/modules/m1-understanding-canton.md), [m2](appdev/modules/m2-canton-for-ethereum-devs.md).

이어서 권장 순서:
1. `appdev/modules/m2-concept-translation` — (미번역) Ethereum↔Canton 개념 변환표. m2 직후 필독.
2. `appdev/modules/m3` 이후 — 모듈 순서대로 (Daml 작성→테스트→배포)
3. `appdev/get-started/*` 나머지 — 환경 설정·첫 앱
4. `appdev/quickstart/*` (9페이지) — 빠른 시작 실습
5. `appdev/deep-dives/*` (23페이지) — authorization, app-architecture-design, command-deduplication 등 주제별 심화
6. `appdev/reference/*` (43), `appdev/tooling/*` (3), `appdev/troubleshooting-guide/*` (6) — 레퍼런스, on-demand

> appdev/modules는 학습용 커리큘럼이라 **번호 순서가 곧 읽는 순서**. 모듈 → quickstart → deep-dives 순으로 깊어진다.

### C. global-synchronizer — GS 운영 (운영자용)
개념→운영 순:
1. `global-synchronizer/understand/*` (5페이지) — GS 운영 개념
2. `global-synchronizer/splice-fundamentals/*` (5, glossary 포함) — <abbr class="gloss" title="글로벌 Synchronizer를 구동하는 오픈소스 애플리케이션 모음(SV·밸리데이터·월렛 등)">Splice</abbr> 기초
3. `global-synchronizer/canton-console/*` (6) — 콘솔 사용
4. `global-synchronizer/deployment/*` (21) — 노드 배포
5. `global-synchronizer/production-operations/*` (25) — 운영
6. `global-synchronizer/extension-synchronizers/*` (8), `reference/*` (12), `troubleshooting-guide/*` (10), `release-notes/*` (2)

> 이 섹션은 **밸리데이터/SV를 직접 운영**할 때 필요. 학습 목적이면 understand만 보고 나머지는 보류 가능.

---

## 작업 방법 (리마인더)

각 페이지는 `translate-canton` 스킬의 워크플로를 따른다:
1. `sources.md`에서 대상 원문 URL 확인 → `<url>.md` 가져오기
2. `glossary.md` 확인 후 새 용어 추가
3. 페이지 <abbr class="gloss" title="컨트랙트의 구조와 규칙(권한·초이스)을 정의하는 Daml 청사진">템플릿</abbr>대로 번역 저장 (**출처 링크·frontmatter 필수**)
4. `sources.md` 상태 ☐ → ☑
5. `index.md` 카테고리에 한 줄 요약 등록 + 교차링크
6. `log.md`에 이력 추가
7. `python3 scripts/gen_tooltips.py && python3 scripts/gen_sidebar.py`
8. 검증: abbr open/close 균형, nest:0, theme:0, 출처 1
9. <abbr class="gloss" title="트랜잭션이 최종 확정되어 원장에 반영되는 것">커밋</abbr>·푸시 → GitHub Pages 배포 확인

검증은 `verify-canton` 스킬 (page 모드: 원문 1:1 대조 / lint 모드: 위키 전체 건강 점검).
