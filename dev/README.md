# dev — 개발 워크스페이스

Canton 기반 개발(코드·실험·배포·데모)을 진행하는 작업 폴더. 여러 기능이 들어갈 수 있다.

- **이 폴더(`dev/`)** = 실제 개발 산출물(앱 코드, 배포·데모 계획, 실험 메모 등). **비공개**.
- **위키(`../wiki/`)** = 학습·참고용 지식베이스(번역·정리 노트). 공개 배포(GitHub Pages). 개발 중 **레퍼런스로만** 참조.

> 위키는 "무엇을/왜"(개념 레퍼런스), 이 폴더는 "어떻게 만든다"(개발 실물). 둘을 섞지 않는다.

## 구조
```
canton/
├─ wiki/                      # 학습·참고 (공개)
└─ dev/                       # 개발 (비공개) ← 여기
    ├─ README.md
    ├─ docs/                  # 개발·배포·데모 계획 메모
    │   └─ deployment-and-demo-options.md
    └─ (이후 앱 코드: cn-quickstart 기반 등)
```

> ⚠️ `dev/`는 위키와 같은 git 저장소 안에 있다. 저장소가 공개라면 `dev/` 내용도 공개될 수 있으니, 대외비 코드는 `.gitignore` 처리하거나 저장소를 비공개로 둘 것. (GitHub Pages는 `wiki/`만 배포하므로 사이트엔 노출 안 됨)

## 참고 (위키)
- 시작: [QuickStart](../wiki/appdev/quickstart/index.md) · [사전 요구사항·설치](../wiki/appdev/quickstart/prerequisites.md) · [LocalNet 개발](../wiki/appdev/modules/m5-localnet-development.md)
- 개념 복습: [용어 한 컷 카드](../wiki/notes/term-cheatsheet.md)
- 환경/스펙: [환경 4단계](../wiki/notes/canton-environments-localnet-to-mainnet.md)
