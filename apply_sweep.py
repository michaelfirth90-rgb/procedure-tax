#!/usr/bin/env python3
"""Link brand-sweep.css and menu-sweep.css into every page, and tell each page
which row of the contents menu it sits under.

Idempotent: run it again and nothing changes. Adds nothing but two <link> tags
and one attribute, so removing the two links reverts the site completely.
"""
import json, os, re, sys

SITE = sys.argv[1] if len(sys.argv) > 1 else '.'
pos = json.load(open(os.path.join(SITE, 'menu-pos.json')))
LINKS = '<link rel="stylesheet" href="brand-sweep.css">\n<link rel="stylesheet" href="menu-sweep.css">'

linked = tagged = skipped = 0
missing = []
for f in sorted(x for x in os.listdir(SITE) if x.endswith('.html')):
    p = os.path.join(SITE, f)
    t = open(p, encoding='utf-8', errors='replace').read()
    before = t

    # the two links go after the last stylesheet already on the page
    t = re.sub(r'\n?<link rel="stylesheet" href="(?:brand-sweep|menu-sweep)\.css">', '', t)
    links = list(re.finditer(r'<link rel="stylesheet"[^>]*>', t))
    if links:
        t = t[:links[-1].end()] + '\n' + LINKS + t[links[-1].end():]
        linked += 1
    else:
        skipped += 1

    n = pos.get(f)
    t = re.sub(r'<body([^>]*?)(?: data-menu-pos="\d+")?>',
               lambda m: f'<body{m.group(1)}' + (f' data-menu-pos="{n}"' if n is not None else '') + '>',
               t, count=1)
    if n is not None:
        tagged += 1
    else:
        missing.append(f)

    if t != before:
        open(p, 'w', encoding='utf-8').write(t)

print(f'  {linked} pages linked, {tagged} given a menu position')
if skipped:
    print(f'  {skipped} page(s) had no stylesheet link to attach to')
if missing:
    print(f'  {len(missing)} page(s) are not under a menu row, so keep their Part shading:')
    for m in missing:
        print(f'      {m}')
