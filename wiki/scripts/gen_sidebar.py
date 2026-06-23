#!/usr/bin/env python3
"""wiki/ 의 번역 페이지로부터 Docsify _sidebar.md 를 재생성한다.
사용법: wiki/ 디렉토리에서  python3 scripts/gen_sidebar.py
translate-canton 으로 새 페이지를 추가한 뒤 실행하면 왼쪽 내비가 갱신된다."""
import os, re
from collections import OrderedDict

WIKI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
META = {'index.md','sources.md','glossary.md','log.md','how-to-read.md','next-step.md',
        '_sidebar.md','_coverpage.md','README.md'}
SEC_LABEL = {'canton-course':'입문 학습 코스 (Course)','overview':'개요 (Overview)','appdev':'앱 개발 (App Dev)',
             'global-synchronizer':'글로벌 동기화자','integrations':'통합 (Integrations)',
             'notes':'정리 노트 (Notes)'}
# 섹션 표시 순서 (학습 흐름: 입문 코스→개념→앱개발→운영→통합→노트)
SECTION_ORDER = ['canton-course','overview','appdev','global-synchronizer','integrations','notes']
# 섹션 내 하위 디렉토리 순서 (그 외/루트 파일은 뒤에서 알파벳순)
SUBDIR_ORDER = {
    'overview': ['understand','learn','reference'],
    'appdev': ['get-started','modules','quickstart','deep-dives','reference','tooling','troubleshooting-guide'],
    'global-synchronizer': ['understand','splice-fundamentals','canton-console','deployment',
                            'production-operations','extension-synchronizers','reference',
                            'troubleshooting-guide','release-notes'],
}

def page_sort_key(rel):
    parts = rel.split('/')
    sec = parts[0]
    subdir = parts[1] if len(parts) >= 3 else ''
    order = SUBDIR_ORDER.get(sec, [])
    sub_rank = order.index(subdir) if subdir in order else len(order)
    return (sub_rank, rel)

def title_of(path):
    try:
        txt = open(path, encoding='utf-8').read()
        m = re.search(r'^title:\s*(.+)$', txt, re.M)
        if m: return m.group(1).strip()
        m = re.search(r'^#\s+(.+)$', txt, re.M)
        if m: return m.group(1).strip()
    except Exception:
        pass
    return os.path.basename(path)

pages = []
for root,_,files in os.walk(WIKI):
    if os.sep + '.' in root.replace(WIKI,'') or '/scripts' in root.replace(os.sep,'/'):
        continue
    for f in files:
        if not f.endswith('.md'):
            continue
        rel = os.path.relpath(os.path.join(root,f), WIKI).replace('\\','/')
        if rel in META or rel.startswith('scripts/'):
            continue
        pages.append(rel)
pages.sort()

groups = OrderedDict()
for p in pages:
    groups.setdefault(p.split('/')[0], []).append(p)
# 섹션 순서 정렬 + 섹션 내 하위 디렉토리 순서 정렬
groups = OrderedDict(sorted(groups.items(),
                            key=lambda kv: (SECTION_ORDER.index(kv[0]) if kv[0] in SECTION_ORDER else len(SECTION_ORDER), kv[0])))
for sec in groups:
    groups[sec].sort(key=page_sort_key)

# 링크는 루트 기준(앞에 /)으로 emit한다.
# relativePath:true 환경에서 상대링크는 현재 페이지 기준으로 해석돼 경로가 누적되는 버그가 있다.
# 루트 기준(/...)이면 Docsify가 항상 사이트 루트에서 해석 → 누적 없음.
out = ["- **시작하기**",
       "  - [📖 읽는 방법](/how-to-read.md)",
       "  - [🗂 인덱스/학습순서](/index.md)",
       "  - [🗺️ 다음 작업/남은 순서](/next-step.md)",
       "  - [📚 용어집](/glossary.md)",
       "  - [🔗 출처/진행상태](/sources.md)",
       "  - [🕒 작업 로그](/log.md)"]
for sec, ps in groups.items():
    out.append(f"- **{SEC_LABEL.get(sec, sec)}**")
    for p in ps:
        out.append(f"  - [{title_of(p)}](/{p})")

open(os.path.join(WIKI,'_sidebar.md'),'w',encoding='utf-8').write("\n".join(out)+"\n")
print(f"_sidebar.md regenerated with {len(pages)} content pages")
