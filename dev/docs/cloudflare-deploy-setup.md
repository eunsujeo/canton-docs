# 위키 Cloudflare Pages 배포 설정

위키(`canton/wiki/`)를 **canton repo의 GitHub Action**으로 **Cloudflare Pages**에 배포한다.
(repo는 비공개 가능 · Cloudflare가 공개 사이트 서빙 · GitHub Pages는 안 씀)

## 흐름
```
wiki/ 수정 → git push (main) → GitHub Action(deploy-cloudflare.yml)
   → wrangler pages deploy wiki --project-name=canton-docs → Cloudflare Pages 공개
```
- 워크플로: `.github/workflows/deploy-cloudflare.yml`
- 배포 대상: `wiki/` 디렉토리(빌드 없는 정적 Docsify)
- 트리거: `wiki/**` 변경 push, 또는 Actions 탭에서 수동 실행(workflow_dispatch)

## 최초 1회 설정 (이게 돼야 배포 성공)

### 1) Cloudflare Pages 프로젝트 생성
- Cloudflare Dashboard → **Workers & Pages → Create → Pages → "Direct Upload"** → 프로젝트명 **`canton-docs`**
  - (또는 로컬에서 `npx wrangler pages project create canton-docs` 한 번)
- 워크플로의 `--project-name`과 **이름이 일치**해야 함. 다른 이름 쓰려면 워크플로도 같이 수정.

### 2) Cloudflare API 토큰 발급
- Cloudflare Dashboard → **My Profile → API Tokens → Create Token**
- 템플릿 또는 커스텀으로 **권한: `Account → Cloudflare Pages → Edit`** 부여 → 토큰 복사

### 3) GitHub repo 시크릿 등록
- GitHub repo(`eunsujeo/canton-docs`) → **Settings → Secrets and variables → Actions → New repository secret**
  - `CLOUDFLARE_API_TOKEN` = 위에서 발급한 토큰
  - `CLOUDFLARE_ACCOUNT_ID` = `58a2bb6c0901025e0b4c0f1ac2265d80`

### 4) 배포 확인
- main에 push하거나 Actions 탭에서 수동 실행 → 성공 시 Cloudflare Pages URL(`https://canton-docs.pages.dev` 또는 커스텀 도메인)에 공개.

## 참고
- 기존 docs-site(`waas-wiki/docs-site`, 프로젝트 `wiki-docs`)와는 **별개 프로젝트**. (그쪽은 패스코드 `_worker.js` 보호 / 이 위키는 공개 학습용)
- 비공개로 하고 싶으면 그쪽처럼 `_worker.js` 패스코드 게이트를 wiki/에도 추가하는 방법이 있음(필요 시).
- Docsify는 해시 라우팅·정적 서빙이라 별도 빌드·`_redirects` 불필요.
