# 메모 — Canton 지갑/커스터디 전략 (Fireblocks · raw signing · drain 리스크)

> 목적: PoC 정산에서 파티 키를 누가 어떻게 보관·서명할지 정리. 특히 Fireblocks 사용 가능성과
> 그 한계, 그리고 실제 도입 전 검증해야 할 항목을 기록한다.
> 관련: [멀티체인 아키텍처](architecture-b2b-b2c-multichain.md) · [스테이블코인 인스트루먼트 계획](stablecoin-instruments-plan.md)
> 출처(Fireblocks): [Create a new transaction](https://developers.fireblocks.com/api-reference/transactions/create-a-new-transaction)

## 0. 한 줄 요약
Fireblocks로도 PoC는 **가능**하다 — Canton의 external party 서명이 결국 **prepared-tx 해시(byte[])에 서명**하는 흐름이라
Fireblocks **raw signing(=blind signing)** 과 맞아떨어지기 때문. 단 blind signing은 **커스터디가 거래 내용을 못 봐서**
악성 fund-drain tx를 **커스터디 계층에선 막지 못한다.** 방어를 다른 계층으로 옮겨야 하며, 실제 도입 전 Fireblocks와 검증 필요.

---

## 1. 헷갈리지 말 것 — 서로 다른 두 개의 축
지갑 논의가 어려운 이유는 두 질문을 하나로 합쳐 보기 때문이다. 분리하면 풀린다.

| 축 | 질문 | 답 |
|---|---|---|
| A. 자산의 위치 | 자산이 Canton 체인 위에 있나? | Fireblocks가 Canton wallet을 지원하면 **있음** (온체인) |
| B. 파티의 입도 | 고객 1명 = 파티 1개인가, 다수 고객이 파티 1개를 공유하나? | **여기가 진짜 쟁점** |

**Canton의 모든 보장(프라이버시·원자성·잠금)은 "파티"라는 단위에 묶인다.** 따라서 자산을 온체인에 올려도(축 A 충족),
파티를 거칠게 세우면(축 B) 보장도 그 입도에서 멈춘다. "온체인이냐"와 "파티를 얼마나 잘게 쪼개느냐"는 별개다.

---

## 2. 옴니버스(Omnibus) 모델의 한계 — 조건부
옴니버스 커스터디 = 다수 고객을 **원장 위의 단 하나의 파티** 아래 뭉치고, 누가 얼마인지는 **내부 SQL 장부**로 관리.
(거래소 통상 방식. Fireblocks는 SQL을 많이 쓰는 옴니버스형.)

- **파티별 프라이버시**: 고객이 다 한 파티 안에 있으면 원장은 고객 A·B를 구분할 수단이 없다 → 고객 간 프라이버시가
  Canton 강제가 아니라 **커스터디 DB 신뢰**로 회귀. 같은 커스터디언 고객끼리 거래는 **내부 장부 이전**이라 원장에 안 찍힘.
- **원자적 DvP**: 두 커스터디언(파티) 사이 원자 스왑은 됨. 그러나 (a) 원자성 보장이 **고객까지 안 내려감**(고객은 파티가
  아니라 서명·참여 안 함), (b) "고객 A 몫을 콕 집어 잠근다(allocate)"가 **원장 개념이 아니라 DB 메모**.

**공통 원리**: 옴니버스는 실제 경제 주체를 파티 선 아래(오프체인 DB)로 내린다 → 모든 Canton 보장이 "커스터디 DB를 믿어라"로
강등 = 블록체인 이전 모델. **단 조건부** — 실제 거래 당사자가 1급 파티여야 하는 기관 간 정산이면 치명적이지만,
고객이 온체인 정체성 불필요한 B2C 거래소 모델이면 옴니버스로 충분.

### 2.1 시나리오 — 단일 커스터디 안의 내부 dApp은 무의미
(상대측 의견) 참여 기관이 슈퍼밸리데이터(Super Validator)로서 추후 **내부 Canton dApp**을 만들 때,
그 dApp이 **커스터디 한 개 안에서만** 동작한다면 Fireblocks 사용 시 **옴니버스 형태**가 된다 →
내부 사용자들이 **SQL DB에 기록**되고, 사용자 간 거래는 내부 장부 이전이라 **Canton TX가 발생하지 않는다.**
→ Canton의 원장·프라이버시·원자성을 쓸 일이 없으니 **유의미한 dApp 개발이 불가능.**
→ 노드월렛·DFNS처럼 **Canton 노드에 party들을 직접 호스팅하는 네이티브 방식**이 필요.

평가: §2의 옴니버스 한계를 이 시나리오에 그대로 적용한 것으로 **타당**. 핵심은 "단일 커스터디 = 단일 파티로
수렴하면 내부 거래가 온체인에 안 찍힌다"는 점. dApp이 의미를 가지려면 **다수의 실제 파티**가 필요하고,
그건 파티별 키를 네이티브로 발급하는 방식(node wallet / DFNS)에서 자연스럽다.

---

## 3. 우회 경로 — external party + raw signing
옴니버스가 아니라 **Fireblocks가 그 파티의 키를 들고 진짜 파티로서 서명**하면 §2 한계를 우회한다.

Canton **interactive submission service**(external party 서명) 흐름:
1. 참여자 노드가 트랜잭션을 **prepare** → **prepared transaction의 해시**(짧은 byte[]) 반환
2. 파티 키로 **그 해시에 서명** ← 이 단계가 곧 **raw signing**
3. 서명 붙여 **execute**

→ 4자간 Daml 컨트랙트 호출도 Fireblocks raw signing으로 승인 가능. 이건 옴니버스가 아니므로 §2 한계를 우회하는
**더 나은 경로.** (상대측 의견: blind signing으로 byte[]만 서명하면 이론상 모든 Canton 기능 지원 가능 — 맞음.)

---

## 4. 한계 — blind signing은 악성 거래를 못 거른다
blind signing의 대가는 **커스터디 정책엔진이 눈을 감는 것**이다.

- raw signing 입장에서 정상 DvP tx와 "내 holding 전부를 공격자에게" drain tx는 **둘 다 그냥 byte[]** → 구분 불가.
- Canton에서 파티 P의 holding 이전엔 P의 서명이 필요한데, 그 키가 Fireblocks에 있으니 **drain tx도 P의 정당한 서명으로 승인**됨.
- 위협이 "키 탈취"에서 **"서명기에 악성 해시를 먹이는 것"**(=prepare 단계 장악)으로 이동.

| 방어 계층 | drain을 막나 | 한계 |
|---|---|---|
| Fireblocks 정책(TAP) | Canton tx엔 **못 막음** | 내용을 못 봐서 무력 |
| Daml 컨트랙트 제약(signatory·precondition) | DvP 워크플로 오용은 막음 | "owner가 자기 토큰 전송"은 본질적으로 허용 → 막기 어려움 |
| prepare 단계 보안(누가 tx 해시를 만드나) | **실질적 방어선** | 앱·참여자 노드가 뚫리면 그대로 통과 |
| WYSIWYS(서명 전 해시 독립 검증) | 이상적 해법 | Fireblocks가 Canton tx를 **디코딩**해야 성립 |

**결론**: blind signing 자체로는 fund drain을 막을 수 없다. 방어는 (1) prepare 인프라 무결성, (2) Daml 컨트랙트 제약,
(3) 가능하면 WYSIWYS로 옮겨야 한다.

---

## 5. 실제 도입 전 Fireblocks 검증 항목
1. **RAW 서명에 co-signer / callback 검증 훅을 걸 수 있나** — 서명 직전 우리 검증기가 prepared tx를 디코딩·승인/거부 가능한가. (가능하면 더 이상 blind 아님)
2. **prepared tx 메타데이터를 정책 조건으로 쓸 수 있나** — 한도·상대 파티·인스트루먼트를 RAW 서명 정책에 반영 가능한가.
3. **RAW 서명 활성화 가능 여부** — 해당 workspace에서 RAW 서명을 켤 수 있는지, 어떤 승인·격리가 붙는지. (보통 제한 기능)
4. **곡선(curve) 호환** — Canton 키(Ed25519 등)를 Fireblocks raw signing이 지원하는지. 실제 prepared-tx 해시 1건 서명 PoC로 확인.
5. **검증 훅(1·2)이 불가하면** — drain 방어가 전적으로 *우리 prepare 인프라* 책임이 된다. 이 리스크를 수용 가능한가. (이 경우 Fireblocks는 "안전한 키 보관"만, "거래 검증"은 안 함 — 도입 가부의 핵심 결정)

## 6. 실무 진행 메모
- 현재 우리 쪽 **Fireblocks 접근권한 없음.** 상대측이 제안: ① 접근권한 개방, 또는 ② 연동코드 테스트 공수 공동 투입.
- 보안상 "Canton/daml 문법에 맞는 내부 보안 절차" 테스트는 blind signing 전제에선 어렵다(상대측 단서). → §4·§5가 그 이유.
- 대안 커스터디: **DFNS, 노드월렛** 등 파티별 키 발급에 자연스러운 방식 — 더 밀접한 Canton 기능 단계, 그리고
  §2.1의 슈퍼밸리데이터 내부 dApp 시나리오(단일 커스터디 수렴 시 무의미)에서 필요.
- 정리: **단순 정산 PoC = Fireblocks raw signing 가능**(§3) / **다수 파티가 필요한 내부 dApp = 네이티브 파티 호스팅 필요**(§2.1).

---

## 7. Q&A — Musubi 측 문답 (원문)
위 §2.1·§3·§6의 "(상대측 의견)" 줄들은 아래 문답에서 나왔다. 추적용으로 원문을 그대로 남긴다.

### Q1. Fireblocks 사용 가능성
> 1. 파이어블록스 무방함
>
> 파이어블록 가능할 수도 있을 것 같습니다.
>
> 엄밀히 말해서 4자간 Daml 스마트컨트랙트를 호출하는 것이다보니, "Raw Signing"을 해야합니다.
>
> blind-signing 방식으로 호출 tx 자체를 서명하면 되지 않을까 싶기도 합니다.
>
> https://developers.fireblocks.com/api-reference/transactions/create-a-new-transaction
>
> 단 저희가 Fireblocks 접근권한이 없다보니, 저희에게 혹시 접근권한을 열어주시거나, 또는 같이 Fireblocks 연동코드 테스트에 개발 공수를 넣어주실 수 있으실지 문의드립니다.

**우리 평가/반영**: 맞다 — 4자간 Daml 호출은 prepared-tx 해시(byte[]) 서명이라 raw signing이 맞고, 그래서 Fireblocks로 PoC 가능(§3). 단 blind signing이면 커스터디가 내용을 못 봐 fund-drain을 못 거른다는 대가가 따른다(§4). 접근권한 개방/공수 공동 투입 제안은 §6에 기록, 도입 전 확인할 항목은 §5.

### Q2. 추후 더 밀접한 기능
> 2. 추후 더 밀접한 기능
>
> 이론상 blind signing으로 byte[]를 그냥 fireblocks에서 사인하면 모든 기능 지원이 가능할 것 같긴 합니다.
>
> 단, 보안상 이슈가 될 수 있어서 canton/daml 문법에 맞는 내부 보안 절차들 테스트는 어려울 것 같습니다.

**우리 평가/반영**: "byte[]만 서명하면 이론상 모든 Canton 기능 지원" — 맞다(§3). "보안상 내부 절차 테스트가 어렵다"가 바로 §4의 핵심(정상 DvP tx와 drain tx가 둘 다 byte[]라 커스터디 정책엔진이 구분 불가 → 위협이 'prepare 단계 장악'으로 이동). 그 어려움을 푸는 길이 §5의 검증 항목(서명 직전 co-signer/callback 훅, 메타데이터 정책화, WYSIWYS) — 이게 되면 더 이상 blind이 아니다.
