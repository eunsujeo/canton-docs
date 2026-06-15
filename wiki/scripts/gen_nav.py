#!/usr/bin/env python3
"""각 콘텐츠 페이지 하단에 '이전 / 다음' 네비게이션 링크를 삽입한다 (웹·Obsidian 공용).

- 순서는 `_sidebar.md`(gen_sidebar.py가 생성)의 등장 순서를 그대로 따른다 → 사이드바와 prev/next 일관.
- 멱등: <!-- nav:start --> ~ <!-- nav:end --> 블록을 먼저 제거하고 다시 삽입하므로 반복 실행 안전.
- 링크는 현재 파일 기준 상대경로(Obsidian·Docsify relativePath 둘 다 해석).
- 네비 내용은 모두 마크다운 링크라, gen_tooltips는 이를 건드리지 않는다(링크 보호). 실행 순서 무관.

사용법: wiki/ 에서  python3 scripts/gen_nav.py"""
import os, re

WIKI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# 시작하기(메타) 페이지는 prev/next 흐름에서 제외
META = {'index.md','sources.md','glossary.md','log.md','how-to-read.md','next-step.md',
        '_sidebar.md','_coverpage.md','README.md'}

NAV_BLOCK = re.compile(r'\n*<!-- nav:start -->.*?<!-- nav:end -->\n*', re.S)
SIDEBAR_LINK = re.compile(r'\[([^\]]+)\]\(([^)]+\.md)\)')

def load_order():
    """_sidebar.md에서 콘텐츠 페이지를 등장 순서대로 (title, relpath) 추출."""
    sb = os.path.join(WIKI, '_sidebar.md')
    order = []
    for line in open(sb, encoding='utf-8'):
        for title, path in SIDEBAR_LINK.findall(line):
            if path.startswith('http') or path in META:
                continue
            if not os.path.exists(os.path.join(WIKI, path)):
                continue
            order.append((title.strip(), path))
    return order

def rel_link(from_path, to_path):
    """from_path(콘텐츠 파일) 기준 to_path 로의 상대 경로."""
    start = os.path.dirname(os.path.join(WIKI, from_path))
    return os.path.relpath(os.path.join(WIKI, to_path), start).replace('\\', '/')

def build_block(cur, order):
    i = next(k for k, (_, p) in enumerate(order) if p == cur)
    parts = []
    if i > 0:
        t, p = order[i-1]
        parts.append(f'⬅️ **이전**: [{t}]({rel_link(cur, p)})')
    if i < len(order) - 1:
        t, p = order[i+1]
        parts.append(f'➡️ **다음**: [{t}]({rel_link(cur, p)})')
    if not parts:
        return ''
    return ('\n\n<!-- nav:start -->\n---\n<sub>' + ' ・ '.join(parts) +
            '</sub>\n<!-- nav:end -->\n')

def main():
    order = load_order()
    paths = {p for _, p in order}
    changed = 0
    for _, rel in order:
        full = os.path.join(WIKI, rel)
        raw = open(full, encoding='utf-8').read()
        body = NAV_BLOCK.sub('\n', raw).rstrip('\n')
        new = body + build_block(rel, order) if rel in paths else body + '\n'
        if not new.endswith('\n'):
            new += '\n'
        if new != raw:
            open(full, 'w', encoding='utf-8').write(new)
            changed += 1
    print(f"gen_nav: {len(order)} pages in order, updated {changed} page(s)")

if __name__ == '__main__':
    main()
