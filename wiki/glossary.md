# 용어집 (Glossary) — 번역 일관성 규칙

모든 페이지 번역 시 이 표를 따른다. 새 용어를 만나면 여기에 먼저 추가하고 번역한다.

## 번역 원칙
- **고유 제품/프로토콜명은 원문 유지**: Canton, Daml, Splice, Canton Coin, Global Synchronizer 등.
- **기술 용어는 "한국어(영문)" 병기**를 첫 등장 시 1회**: 예) 동기화자(Synchronizer). 이후에는 한국어만 사용.
- **코드, 명령어, 식별자, 파일 경로, API 이름은 절대 번역하지 않음.**
- 의미가 왜곡될 수 있으면 원문 용어를 그대로 두고 괄호로 설명을 단다.

## 핵심 용어 대응표
| 원문 | 한국어 표기 | 비고 |
|---|---|---|
| Canton | Canton | 원문 유지 |
| Canton Network | Canton 네트워크 | |
| Daml | Daml | 스마트 컨트랙트 언어, 원문 유지 |
| Synchronizer | 동기화자(Synchronizer) | |
| Global Synchronizer | 글로벌 동기화자(Global Synchronizer) | |
| Super Validator (SV) | 슈퍼 밸리데이터(Super Validator, SV) | |
| Validator | 밸리데이터(Validator) | |
| Validator node | 밸리데이터 노드 | |
| Ledger | 원장(ledger) | |
| Ledger API | Ledger API | 원문 유지 |
| Party | 파티(party) | Canton의 권한 주체 |
| Contract | 컨트랙트(contract) | |
| Smart contract | 스마트 컨트랙트 | |
| Template | 템플릿(template) | |
| Choice | 초이스(choice) | Daml 용어, 원문 유지 권장 |
| Transaction | 트랜잭션 | |
| Topology | 토폴로지(topology) | |
| Privacy | 프라이버시 | |
| Sub-transaction privacy | 부분 트랜잭션 프라이버시 | |
| Consensus | 합의(consensus) | |
| Reassignment | 재할당(reassignment) | |
| Tokenomics | 토크노믹스(tokenomics) | |
| Canton Coin (CC) | Canton Coin(CC) | 원문 유지 |
| Wallet | 월렛(wallet) | |
| Decentralization | 탈중앙화 | |
| Trust model | 신뢰 모델 | |
| Staking | 스테이킹 | |
| Pruning | 프루닝(pruning) | |
| CIP (Canton Improvement Proposal) | CIP(Canton 개선 제안) | |

## 툴팁 정의 (tooltip terms)
본문에서 이 용어가 처음 나올 때 `gen_tooltips.py`가 자동으로 `<abbr>` 툴팁을 붙인다.
**용어**는 본문에 나타나는 한국어 표기와 정확히 일치해야 하며, **정의**는 한 줄로 간결하게 쓴다.
새 페이지에서 설명이 필요한 용어를 만나면 먼저 이 표에 추가한다.

| 용어 | 정의 |
|---|---|
| 부분 트랜잭션 프라이버시 | 한 트랜잭션을 "뷰"로 분해해, 각 파티가 자신과 관련된 부분만 보도록 하는 Canton의 핵심 프라이버시 방식 |
| 글로벌 동기화자 | 슈퍼 밸리데이터들이 공동 운영하는 Canton의 퍼블릭 조율(합의) 계층 |
| 슈퍼 밸리데이터 | 글로벌 동기화자를 운영하고 네트워크 거버넌스에 참여하는 노드 |
| 동기화자 | 상태를 저장하지 않고 트랜잭션 합의·순서를 조율하는 Canton 구성요소 |
| 밸리데이터 | 파티를 호스팅하고 그 파티의 컨트랙트 데이터를 저장하는 참여자 노드 |
| 파티 | Canton에서 권한과 데이터 가시성의 주체가 되는 식별 가능한 참여 주체 |
| 컨트랙트 | 원장에 기록되는 불변 데이터 단위. 상태 변경은 새 컨트랙트 생성으로 표현됨 |
| 템플릿 | 컨트랙트의 구조와 규칙(권한·초이스)을 정의하는 Daml 청사진 |
| 초이스 | 컨트랙트에서 수행 가능한 동작(권한이 부여된 당사자만 실행 가능) |
| 이해관계자 | 어떤 컨트랙트와 관계를 맺어 그것을 보거나 승인하는 파티 = 서명자 + 관찰자 |
| 서명자 | 컨트랙트의 주된 권한자. 생성·보관(소비)에 반드시 동의해야 하는 파티 |
| 관찰자 | 컨트랙트를 볼 수 있으나 단독으로 행위할 수는 없는 파티 |
| Daml | 다자간 워크플로를 위해 설계된 Canton의 스마트 컨트랙트 언어 |
| Canton Coin | 트랜잭션 수수료와 밸리데이터 보상에 쓰이는 네이티브 유틸리티 토큰(CC) |
| 토폴로지 | 어떤 노드·파티·키가 네트워크에 참여하는지를 정의하는 구성 정보 |
| 재할당 | 컨트랙트를 한 동기화자에서 다른 동기화자로 옮기는 프로토콜 |
| 프루닝 | 더 이상 필요 없는 과거 원장 데이터를 정리해 저장공간을 줄이는 작업 |
| 레이어 0 | 여러 L1 블록체인을 구축·연결하도록 받쳐주는 기반 인프라 계층(예: Polkadot, Cosmos) |
| 레이어 1 | 자체 합의로 트랜잭션을 직접 확정하는 기반 블록체인(L1). 다른 체인에 의존하지 않음 |
| 레이어 2 | L1 위에 얹혀 처리량을 늘리는 확장 계층(L2). 보안은 L1에 의존(예: Base, Arbitrum) |
| ZK-롤업 | 영지식 증명으로 다수 트랜잭션을 체인 밖에서 처리하고 유효성 증명만 L1에 올리는 L2 기술. 내용을 공개하지 않고 검증 가능해 프라이버시에도 활용 |
| 프라이빗 채널 | 특정 참여자끼리만 거래 데이터를 공유하는 별도 통로. 채널 밖에서는 내용이 보이지 않음(예: 상태/결제 채널, Hyperledger Fabric channel) |
