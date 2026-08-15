#!/usr/bin/env python3
"""Take the inline margin-top off the FIRST body block after the contents card.

Every .rich-text on a page carries an inline margin-top and together they are the
site's vertical rhythm, so only the first one — the one that sets the gap under
the card — is touched. Everything below it is left exactly as it is.

Idempotent. Reports anything that does not match the expected shape rather than
guessing.
"""
import os, re, sys

SITE = sys.argv[1] if len(sys.argv) > 1 else '.'
changed, values, odd = 0, [], []

for f in sorted(x for x in os.listdir(SITE) if x.endswith('.html')):
    p = os.path.join(SITE, f)
    t = open(p, encoding='utf-8', errors='replace').read()
    j = t.find('<nav class="toc-card"')
    if j < 0:
        continue
    k = t.find('</nav>', j)
    if k < 0:
        odd.append(f'{f}: contents card never closes'); continue
    k += 6

    # the first style attribute after the card, within the next few hundred chars
    m = re.search(r'style="([^"]*)"', t[k:k + 700])
    if not m:
        odd.append(f'{f}: nothing with an inline style follows the card'); continue

    decls = [d.strip() for d in m.group(1).split(';') if d.strip()]
    keep = [d for d in decls if not re.match(r'margin-top\s*:', d)]
    if len(keep) == len(decls):
        continue                      # already stripped, or never had one
    values.extend(d for d in decls if re.match(r'margin-top\s*:', d))

    a, b = k + m.start(), k + m.end()
    new = f'style="{"; ".join(keep)}"' if keep else ''
    t = t[:a] + new + t[b:]
    t = re.sub(r'<(\w+)([^>]*?)\s{2,}>', r'<\1\2>', t)
    open(p, 'w', encoding='utf-8').write(t)
    changed += 1

print(f'  {changed} pages: inline margin-top removed from the first block after the card')
if values:
    nums = sorted(float(re.search(r'(-?[\d.]+)', v).group(1)) for v in values)
    print(f'  the values it replaced ran {nums[0]:.0f}px to {nums[-1]:.0f}px, median {nums[len(nums)//2]:.0f}px')
for o in odd:
    print('  ! ' + o)
