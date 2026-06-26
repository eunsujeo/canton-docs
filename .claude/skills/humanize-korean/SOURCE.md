# humanize-korean — 출처 / 라이선스

- **원본**: https://github.com/epoko77-ai/im-not-ai (MIT License, 동봉 `LICENSE`)
- **버전**: 1.5.0
- **구성**: 스킬 3개(`humanize-korean`·`humanize`·`humanize-redo`) + 서브에이전트 12개(`.claude/agents/`)
- **용도**: AI(ChatGPT·Claude 등)가 쓴 한글을 사람 글처럼 윤문 — 번역투·AI 티 패턴 탐지·재작성(내용 불변). 위키 한국어 번역 품질에 활용.
- **사용**: `/humanize-korean` (또는 "이 글 AI 티 없애줘" 등 자연어 트리거). 정밀 검증은 `--strict`(5인 파이프라인).
- **팀 공유**: 스킬·에이전트를 이 저장소 `.claude/`에 vendor → 클론하면 자동 인식(개별 설치 불필요).
- **갱신**: 원본 저장소 신버전 적용 시 `.claude/skills/humanize*`·`.claude/agents/*` 재복사.
