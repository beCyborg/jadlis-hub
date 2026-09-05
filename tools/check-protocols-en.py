#!/usr/bin/env python3
"""check-protocols-en.py — verify the RU→EN protocol translation (Plan 2, tranche 2).
For each protocol: fence-line count vs git HEAD, remaining Cyrillic lines, and a diff of the
fenced code blocks (HEAD vs working copy) so command drift is visible. Exit 1 on fence mismatch."""
import re, subprocess, sys, difflib
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
PROTO = ROOT / 'plugins/jadlis-research/skills/full-research/protocols'
CYR = re.compile(r'[А-Яа-яЁё]')
def head(path):
    try:
        return subprocess.run(['git', '-C', str(ROOT), 'show', f'HEAD:{path.relative_to(ROOT)}'], capture_output=True, text=True, check=True).stdout
    except subprocess.CalledProcessError:
        return ''
def fences(text):
    out, cur, inside = [], [], False
    for line in text.splitlines():
        if line.strip().startswith('```'):
            if inside: out.append('\n'.join(cur)); cur = []
            inside = not inside; continue
        if inside: cur.append(line)
    return out
bad = 0
for p in sorted(PROTO.glob('*.md')):
    new = p.read_text(encoding='utf-8'); old = head(p)
    nf, of = new.count('```'), old.count('```') if old else None
    cyr = [(i + 1, l.strip()[:90]) for i, l in enumerate(new.splitlines()) if CYR.search(l)]
    flag = '' if (of is None or nf == of) else '  !! FENCE MISMATCH'
    if flag: bad += 1
    print(f"{p.name:26} fences {of}→{nf}{flag}  cyrillic lines: {len(cyr)}")
    for ln, txt in cyr: print(f"    L{ln}: {txt}")
    if old and '--blocks' in sys.argv:
        ob, nb = fences(old), fences(new)
        for i, (a, b) in enumerate(zip(ob, nb)):
            if a != b:
                print(f"  -- block {i+1} changed:")
                for d in difflib.unified_diff(a.splitlines(), b.splitlines(), lineterm='', n=0):
                    if d.startswith(('+', '-')) and not d.startswith(('+++', '---')): print('    ' + d[:160])
sys.exit(1 if bad else 0)
