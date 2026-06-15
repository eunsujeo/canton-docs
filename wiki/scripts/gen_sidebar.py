#!/usr/bin/env python3
"""wiki/ 의 번역 페이지로부터 Docsify _sidebar.md 를 재생성한다.
사용법: wiki/ 디렉토리에서  python3 scripts/gen_sidebar.py
translate-canton 으로 새 페이지를 추가한 뒤 실행하면 왼쪽 내비가 갱신된다."""
import os, re
from collections import OrderedDict

WIKI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
META = {'index.md','sources.md','glossary.md','log.md','how-to-read.md',
        '_sidebar.md','_coverpage.md','README.md'}
SEC_LABEL = {'overview':'개요 (Overview)','appdev':'앱 개발 (App Dev)',
             'global-synchronizer':'글로벌 동기화자','integrations':'통합 (Integrations)',
             'notes':'정리 노트 (Notes)'}

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

out = ["- **시작하기**",
       "  - [📖 읽는 방법](how-to-read.md)",
       "  - [🗂 인덱스/학습순서](index.md)",
       "  - [📚 용어집](glossary.md)",
       "  - [🔗 출처/진행상태](sources.md)",
       "  - [🕒 작업 로그](log.md)"]
for sec, ps in groups.items():
    out.append(f"- **{SEC_LABEL.get(sec, sec)}**")
    for p in ps:
        out.append(f"  - [{title_of(p)}]({p})")

open(os.path.join(WIKI,'_sidebar.md'),'w',encoding='utf-8').write("\n".join(out)+"\n")
print(f"_sidebar.md regenerated with {len(pages)} content pages")
