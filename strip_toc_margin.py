#!/usr/bin/env python3
"""Take the inline margin-top off every toc-card, so one stylesheet rule sets it.

Idempotent. Only touches margin-top inside the style attribute of
<nav class="toc-card">; any other inline property on that tag is left alone, and
the attribute is dropped only if nothing else remains in it.
"""
import os, re, sys

SITE = sys.argv[1] if len(sys.argv) > 1 else '.'
TAG = re.compile(r'<nav class="toc-card"([^>]*)>')
changed, values = 0, []

for f in sorted(x for x in os.listdir(SITE) if x.endswith('.html')):
    p = os.path.join(SITE, f)
    t = open(p, encoding='utf-8', errors='replace').read()

    def fix(m):
        global changed
        attrs = m.group(1)
        sm = re.search(r'\sstyle="([^"]*)"', attrs)
        if not sm:
            return m.group(0)
        decls = [d.strip() for d in sm.group(1).split(';') if d.strip()]
        keep, dropped = [], []
        for d in decls:
            (dropped if re.match(r'margin-top\s*:', d) else keep).append(d)
        if not dropped:
            return m.group(0)
        values.extend(dropped)
        new = f' style="{"; ".join(keep)}"' if keep else ''
        return '<nav class="toc-card"' + attrs[:sm.start()] + new + attrs[sm.end():] + '>'

    new = TAG.sub(fix, t)
    if new != t:
        open(p, 'w', encoding='utf-8').write(new)
        changed += 1

print(f'  {changed} pages: inline margin-top removed from the contents card')
if values:
    nums = sorted(float(re.search(r'(-?[\d.]+)', v).group(1)) for v in values)
    print(f'  the values it replaced ran {nums[0]:.0f}px to {nums[-1]:.0f}px, median {nums[len(nums)//2]:.0f}px')
