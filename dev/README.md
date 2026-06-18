# dev — 개발 워크스페이스

Canton 기반 개발(코드·실험·배포·데모)을 진행하는 작업 폴더. 여러 기능이 들어갈 수 있다.

- **이 폴더(`dev/`)** = 실제 개발 산출물(앱 코드, 배포·데모 계획, 실험 메모 등). **비공개**.
- **위키(`../wiki/`)** = 학습·참고용 지식베이스(번역·정리 노트). 공개 배포(Cloudflare Pages, `canton-docs.pages.dev`). 개발 중 **레퍼런스로만** 참조.

> 위키는 "무엇을/왜"(개념 레퍼런스), 이 폴더는 "어떻게 만든다"(개발 실물). 둘을 섞지 않는다.

## 구조
```
canton/
├─ wiki/                      # 학습·참고 (공개)
└─ dev/                       # 개발 (비공개) ← 여기
    ├─ README.md
    ├─ docs/                  # 개발·배포·데모 계획 메모
    │   ├─ roadmap.md             # 앞으로 할 일(단계별 계획)
    │   ├─ deployment-and-demo-options.md
    │   └─ cloudflare-deploy-setup.md
    └─ (이후 앱 코드: cn-quickstart 기반 등)
```

> `dev/`와 `wiki/`는 **목적상 분리**(개발 vs 참고)일 뿐, 대외비는 아니다 — 전부 공개 정보 기반. (Cloudflare Pages는 `wiki/`만 배포하므로 dev/는 사이트엔 노출 안 됨)

## 앞으로 할 일
- 단계별 계획: [docs/roadmap.md](docs/roadmap.md)

## 참고 (위키)
- 시작: [QuickStart](../wiki/appdev/quickstart/index.md) · [사전 요구사항·설치](../wiki/appdev/quickstart/prerequisites.md) · [LocalNet 개발](../wiki/appdev/modules/m5-localnet-development.md)
- 개념 복습: [용어 한 컷 카드](../wiki/notes/term-cheatsheet.md)
- 환경/스펙: [환경 4단계](../wiki/notes/canton-environments-localnet-to-mainnet.md)
