# Canton 한국어 위키 — 인덱스

Canton Network 공식 문서를 한국어로 번역한 개발자용 지식베이스. 다른 개발자와 공유 목적.

- **👉 처음이라면**: [how-to-read.md](how-to-read.md) — 읽는 방법 & Obsidian으로 보기
- **소스/작업 큐**: [sources.md](sources.md) — 전체 315개 페이지 목록과 번역 상태
- **용어집**: [glossary.md](glossary.md) — 번역 일관성 규칙
- **로그**: [log.md](log.md) — 작업 이력
- **원문 인덱스**: 프로젝트 루트의 `llms.txt` (Canton 공식 문서 전체 목록)

## 추천 학습 순서 (Reading Path)
처음 읽는 개발자에게 권장하는 순서. 번역이 완료되면 링크가 채워진다.

1. **이게 뭔가** — `overview/understand/who-should-read.md`, `what-is-canton.md`, `the-problem.md`, `cantons-solution.md`
2. **빠른 개요** — `overview/understand/five-minute-overview.md`, `core-concepts.md`, `glossary.md`(원문), `use-cases.md`
3. **작동 원리** — `overview/learn/architecture.md`, `ledger-model.md`, `how-transactions-work.md`, `privacy-model.md`, `trust-model.md`
4. **글로벌 동기화자** — `overview/understand/global-synchronizer.md`, `overview/learn/global-synchronizer-architecture.md`
5. **앱 개발 입문** — `appdev/get-started/choose-your-path.md`, `appdev/modules/m1-understanding-canton.md`
6. **블록체인 개발자라면** — `appdev/modules/m2-canton-for-ethereum-devs.md`, `m2-concept-translation.md`

## 카테고리별 페이지 (번역 완료분)
> 각 섹션은 번역이 진행되며 채워진다. 페이지를 완료하면 아래에 한 줄 요약과 함께 등록한다.

### overview — 개념/아키텍처 이해
- [누가 이 문서를 읽어야 하나](overview/understand/who-should-read.md) — 역할·목표별 문서 시작점 길잡이.
- [Canton Network이란?](overview/understand/what-is-canton.md) — 규제 자산·다자간 워크플로를 위한 프라이버시 보존형 L1. Canton의 60초 요약과 차별점(부분 트랜잭션 프라이버시, 동기화자, Daml).
- [Canton이 푸는 문제](overview/understand/the-problem.md) — 공개 가시성의 폐해와 기존 프라이버시 보완책(프라이빗 채널·ZK·L2·암호화)의 한계.
- [Canton의 해법 — 세 가지 기둥](overview/understand/cantons-solution.md) — 부분 트랜잭션 프라이버시 + 이해관계자 합의 + 가시성 없는 동기화로 프라이버시·무결성 동시 달성.
- [5분 만에 보는 Canton Network](overview/understand/five-minute-overview.md) — "데이터는 필요한 곳에만" 통찰부터 네트워크 구성·타 체인 차이까지 빠른 개요.
- [핵심 개념](overview/understand/core-concepts.md) — 파티·밸리데이터·동기화자·템플릿 네 개념과 트랜잭션 흐름.
- [활용 사례](overview/understand/use-cases.md) — DvP·토큰화 증권·국경 간 결제·신디케이트 대출·공급망 금융 사례와 적합/부적합 기준.

### overview/learn — 작동 원리
- [아키텍처 개요](overview/learn/architecture.md) — 조율(동기화자)과 저장(밸리데이터)의 분리, 트랜잭션 흐름, 네트워크 토폴로지, 코드 실행 위치.
- [원장 모델](overview/learn/ledger-model.md) — 불변 컨트랙트(eUTXO), 이해관계자 역할, 트랜잭션 트리·뷰·키·원장 시간.
- [트랜잭션 작동 방식](overview/learn/how-transactions-work.md) — 제출→순서화·분배→검증·확인→커밋 4단계 생애주기.
- [프라이버시 모델 설명](overview/learn/privacy-model.md) — 뷰 분해, 가시성 규칙, 디벌전스, 프라이버시 패턴·실수·체크리스트.
- [신뢰 모델 개요](overview/learn/trust-model.md) — 선택적 신뢰의 5개 영역과 완화책, 탈중앙화 옵션.
- [글로벌 동기화자](overview/understand/global-synchronizer.md) — SV(DSO)가 운영하는 퍼블릭 백본, Canton Coin·트래픽, 4개 환경, 거버넌스·Splice·업그레이드.
- [글로벌 동기화자 아키텍처](overview/learn/global-synchronizer-architecture.md) — 분산 시퀀서·미디에이터의 BFT 합의, 트랜잭션 흐름, SV 1/3 미만 결함 허용.

### appdev — 앱 개발자 가이드
_(아직 없음)_

### global-synchronizer — 글로벌 동기화자 운영
_(아직 없음)_

### integrations — 통합/연동
_(아직 없음)_

### notes — 정리 노트 (직접 작성)
- [블록체인 계층 (L0/L1/L2)와 Canton의 위치](notes/blockchain-layers-l0-l1-l2.md) — L0·L1·L2 구분과 대표 네트워크, Canton이 프라이버시 보존 L1으로서 갖는 위치.
