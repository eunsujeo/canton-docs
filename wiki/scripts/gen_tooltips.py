#!/usr/bin/env python3
"""glossary.md의 '툴팁 정의' 표를 읽어, 각 콘텐츠 페이지에서 용어의 첫 등장에
<abbr class="gloss" title="정의">용어</abbr> 를 자동으로 씌운다 (웹·Obsidian 공용).

사용법: wiki/ 에서  python3 scripts/gen_tooltips.py
- 멱등(idempotent): 기존 gloss abbr를 먼저 벗기고 다시 씌우므로 반복 실행/정의 수정 안전.
- 코드펜스/인라인코드/링크/제목(#)/HTML 태그 안의 텍스트는 건드리지 않는다.
- 용어당 페이지에서 첫 1회만 래핑 (긴 용어 우선)."""
import os, re

WIKI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
META = {'index.md','sources.md','glossary.md','log.md','how-to-read.md',
        '_sidebar.md','_coverpage.md','README.md'}

def load_terms():
    txt = open(os.path.join(WIKI,'glossary.md'), encoding='utf-8').read()
    sec = txt.split('## 툴팁 정의', 1)
    terms = {}
    if len(sec) == 2:
        for line in sec[1].splitlines():
            m = re.match(r'\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|', line)
            if not m: continue
            term, defn = m.group(1).strip(), m.group(2).strip()
            if term in ('용어','---') or term.startswith('-'): continue
            terms[term] = defn
    # 긴 용어 먼저 (부분 매칭 방지: '슈퍼 밸리데이터' 가 '밸리데이터'보다 먼저)
    return dict(sorted(terms.items(), key=lambda kv: -len(kv[0])))

UNWRAP = re.compile(r'<abbr class="gloss"[^>]*>(.*?)</abbr>', re.S)

def strip_existing(text):
    return UNWRAP.sub(r'\1', text)

# 보호: 인라인코드 `...`, 이미지 ![..](..), 링크 [..](..) / [..][..], HTML 태그 <...>
PROTECT = re.compile(r'(`[^`]*`|!\[[^\]]*\]\([^)]*\)|\[[^\]]*\]\([^)]*\)|\[[^\]]*\]\[[^\]]*\]|<[^>]+>)')
SENT = re.compile('\x00(\\d+)\x00')

def esc_attr(s):
    return s.replace('&','&amp;').replace('"','&quot;').replace('<','&lt;').replace('>','&gt;')

def wrap_in_text(line, terms, done):
    """한 줄에서 코드/링크/HTML 및 이미 래핑한 부분을 플레이스홀더로 보호하며 용어 첫 등장을 래핑.
    래핑한 abbr(정의문 포함)는 플레이스홀더로 격리되어 다른 용어가 그 안을 다시 매칭하지 못함 → 중첩 방지."""
    ph = []
    def stash(s):
        ph.append(s); return f'\x00{len(ph)-1}\x00'
    # 1) 코드/링크/HTML 보호
    text = PROTECT.sub(lambda m: stash(m.group(0)), line)
    # 2) 용어 첫 등장 래핑 (긴 용어 우선; done은 페이지 단위)
    for term, defn in terms.items():
        if term in done:
            continue
        idx = text.find(term)
        if idx == -1:
            continue
        abbr = f'<abbr class="gloss" title="{esc_attr(defn)}">{term}</abbr>'
        text = text[:idx] + stash(abbr) + text[idx+len(term):]
        done.add(term)
    # 3) 복원 (플레이스홀더 내용에는 \x00 토큰이 없으므로 1패스로 충분)
    return SENT.sub(lambda m: ph[int(m.group(1))], text)

def process(path, terms):
    raw = open(path, encoding='utf-8').read()
    # frontmatter 분리
    fm = ''
    body = raw
    m = re.match(r'(---\n.*?\n---\n)(.*)', raw, re.S)
    if m:
        fm, body = m.group(1), m.group(2)
    body = strip_existing(body)

    out, in_fence, done = [], False, set()
    for line in body.split('\n'):
        s = line.lstrip()
        if s.startswith('```') or s.startswith('~~~'):
            in_fence = not in_fence
            out.append(line); continue
        if in_fence or s.startswith('#') or s.startswith('|') and set(s) <= set('|-: '):
            out.append(line); continue
        out.append(wrap_in_text(line, terms, done))
    new = fm + '\n'.join(out)
    if new != raw:
        open(path,'w',encoding='utf-8').write(new)
        return sum(1 for _ in re.finditer(r'<abbr class="gloss"', new))
    return 0

def main():
    terms = load_terms()
    total_pages = 0
    for root,_,files in os.walk(WIKI):
        rp = root.replace(os.sep,'/')
        if '/.obsidian' in rp or '/scripts' in rp:
            continue
        for f in files:
            if not f.endswith('.md'): continue
            rel = os.path.relpath(os.path.join(root,f), WIKI).replace('\\','/')
            if rel in META: continue
            n = process(os.path.join(root,f), terms)
            if n:
                total_pages += 1
                print(f"  {rel}: {n} tooltip(s)")
    print(f"gen_tooltips: {len(terms)} terms, updated {total_pages} page(s)")

if __name__ == '__main__':
    main()
