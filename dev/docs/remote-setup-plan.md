# 원격 서버 세팅 계획 (빌드 재현 + 런타임)

> 원격 서버/CI에 어떻게 올릴지 고민 정리. 핵심: **클론(cn-quickstart) 의존을 없애고 공식 출처에서 버전 고정해 재현**.
> (dev 문서 — 위키와는 목적상 분리. 대외비는 아님: 공개 정보 기반.)

## 두 층을 분리해서 본다
| 층 | 하는 일 | 원격에서 핵심 |
|---|---|---|
| **① 빌드/CI** | Daml → DAR 컴파일 | **공식 fetch + 버전 핀**(클론 없이 재현) |
| **② 런타임** | 실제 정산 서비스 실행 | 노드·Synchronizer·백엔드 환경 |

"DAR 만드는 것(①)"과 "정산 돌리는 것(②)"은 별개다.

---

## ① 빌드/CI — 재현 가능한 DAR 생성

cn-quickstart 클론에서 복사하던 것(로컬 편의)을 **공식 출처 다운로드**로 대체:

```bash
# --- 버전 핀 (환경과 일치) ---
SDK_VER=3.4.11        # daml.yaml sdk-version
SPLICE_VER=0.5.3      # LocalNet과 동일 (.env SPLICE_VERSION / scan version)
# 토큰표준 API DAR은 splice 릴리스와 무관하게 v1-1.0.0 (API 안정 버전)

# --- 1) dpm(빌드 도구) 설치 ---
curl https://get.digitalasset.com/install/install.sh | sh
export PATH="$HOME/.dpm/bin:$PATH"     # 설치 스크립트가 PATH 자동 추가 안 함 → 명시
dpm install "$SDK_VER"

# --- 2) 토큰표준 DAR을 Splice 릴리스 번들에서 추출 (정석) ---
DEST=./dars; mkdir -p "$DEST"; cd /tmp
curl -L -o splice-node.tar.gz \
  "https://github.com/digital-asset/decentralized-canton-sync/releases/download/v${SPLICE_VER}/${SPLICE_VER}_splice-node.tar.gz"
tar -tzf splice-node.tar.gz \
  | grep -E 'splice-api-token-(metadata|holding|allocation|allocation-request)-v1-.*\.dar$' \
  | xargs tar -xzf splice-node.tar.gz -C /tmp/splice-extract
find /tmp/splice-extract -name 'splice-api-token-*-v1-*.dar' -exec cp {} "$DEST"/ \;

# --- 3) 빌드 ---
cd <project>; dpm build           # → .daml/dist/<pkg>-0.0.1.dar
# (선택) dpm test                  # Daml Script 단위테스트
```
> ⚠️ 번들 자산명(`${SPLICE_VER}_splice-node.tar.gz`)·내부 DAR 경로는 릴리스 페이지에서 1회 확인. 비면 `tar -tzf ... | grep token`으로 실제 경로 확인 후 보정.
> 로컬 개발 단계에선 **cn-quickstart에서 복사**가 더 빠름(파일 동일). 위 정석은 **원격/CI 재현용**.

## 버전 핀 표 (현재 기준)
| 구성 | 버전 | 출처 |
|---|---|---|
| dpm | 1.0.17 | get.digitalasset.com |
| Daml SDK | 3.4.11 | `dpm install 3.4.11` |
| Splice | 0.5.3 | decentralized-canton-sync 릴리스 |
| 토큰표준 API DAR | v1-1.0.0 | 위 번들 내 |

---

## ② 런타임 — 실제 실행 환경 (원격)

DAR만으론 안 돈다. 두 옵션:

### 옵션 A — 데모/공유용 (가장 빠름)
- **cn-quickstart(Docker Compose)를 클라우드 VM에 통째로** 올리고 우리 settlement DAR 로드.
- 8GB+ VM, 리버스 프록시(nginx/caddy)+TLS 또는 터널, 접근제한. (dev 전용, 공개 노출 금지)
- 성격: 여전히 LocalNet(시뮬레이션)을 공용 dev 서버에 올린 것.
- 상세: [deployment-and-demo-options.md](deployment-and-demo-options.md)

### 옵션 B — 실서비스(정식 노드)
- Musubi 노드 footprint: **Musubi 백엔드 + Canton 참여자 + PostgreSQL + settlement network mTLS**.
- DevNet/TestNet 온보딩(스폰서 SV·IP allowlist) 필요. 실제 CC/할당 정산.
- 상세: [dvp-licensing-code-walkthrough.md](dvp-licensing-code-walkthrough.md) · [architecture-b2b-b2c-multichain.md](architecture-b2b-b2c-multichain.md) · 위키 [환경 4단계](../../wiki/notes/canton-environments-localnet-to-mainnet.md)

| | 옵션 A (Compose on VM) | 옵션 B (정식 노드) |
|---|---|---|
| 목적 | 데모·팀 공유 | 실서비스 |
| 네트워크 | LocalNet(시뮬) | DevNet→TestNet |
| 노력 | 낮음 | 높음(온보딩·운영) |
| 실제 CC 정산 | 흉내 | 진짜 |

---

## 결정/미해결
- [ ] 원격 네트워크 선택: 데모(LocalNet on VM) vs 연동(DevNet)
- [ ] 빌드 재현 스크립트를 CI(예: GitHub Action)로 정식화 — 위 ① 스크립트 기반
- [ ] 토큰표준 DAR 정석 다운로드 경로(번들 자산명) 실측 확인
- [ ] 런타임 옵션 B로 갈 때 스폰서 SV·VPN·보안(키 관리: 로컬/외부 파티) 설계
- [ ] (멀티체인) B2C 퍼블릭체인 ↔ Canton 브릿지 연동 지점 — [architecture-b2b-b2c-multichain.md](architecture-b2b-b2c-multichain.md)

## 관련
- standalone 빌드 셋업: [../daml/settlement/README.md](../daml/settlement/README.md)
- 로컬 셋업 기록: [local-setup.md](local-setup.md) · 로드맵 Phase 4: [roadmap.md](roadmap.md)
