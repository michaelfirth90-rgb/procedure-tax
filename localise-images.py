#!/usr/bin/env python3
"""Bring the site's pictures onto your own disk, and stop pointing at Wix.

The tables in the 2026 Tax Litigation Report are pictures, and they are still
served from Wix's CDN. They display, but the site is not self-contained: the
pictures go the day the Wix account lapses, and they cannot be seen offline.

Run this in the site folder. For every picture served from wixstatic.com it
downloads the ORIGINAL — not the 600px rendering the page asks for, because
these are tables and they have to survive being zoomed into — into images/,
then rewrites the src to point there. The displayed size does not change: the
width and height on the tag stay as they are.

    python3 localise-images.py            # do it
    python3 localise-images.py --list     # show what it would fetch, change nothing

Safe to run twice: anything already in images/ is left alone, and a page that
already points at images/ is not touched. If a download fails, that picture
keeps its Wix URL and the page still works.
"""
import os
import re
import sys
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
IMAGES = os.path.join(HERE, 'images')
SRC = re.compile(r'src="(https://static\.wixstatic\.com/media/[^"]+)"')
MEDIA = re.compile(r'/media/([^/"]+)')
UA = ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 '
      '(KHTML, like Gecko) Chrome/124.0 Safari/537.36')


def local_name(url, alt):
    m = MEDIA.search(url)
    if not m:
        return None
    media = m.group(1)
    ext = os.path.splitext(media)[1].lower()
    if ext not in ('.png', '.jpg', '.jpeg', '.gif', '.webp', '.svg'):
        ext = '.png'
    label = os.path.splitext(alt or '')[0]
    stem = re.sub(r'-+', '-', re.sub(r'[^a-z0-9]+', '-', label.lower())).strip('-')[:46]
    uid = re.sub(r'[^a-z0-9]', '', media.lower())[-10:]
    return f'{stem}-{uid}{ext}' if stem else f'image-{uid}{ext}'


def original(url):
    """Strip Wix's resizing instruction to get the picture as uploaded."""
    return re.sub(r'/v1/.*$', '', url)


def main():
    listing = '--list' in sys.argv
    pages = sorted(f for f in os.listdir(HERE) if f.endswith('.html'))
    found = {}                                   # local name -> original url
    where = {}                                   # local name -> pages using it

    for page in pages:
        text = open(os.path.join(HERE, page), encoding='utf-8').read()
        for url in SRC.findall(text):
            # the alt text sitting after this src, for a readable file name
            at = text.find(url)
            tail = text[at:at + 600]
            alt = re.search(r'alt="([^"]*)"', tail)
            name = local_name(url, alt.group(1) if alt else '')
            if not name:
                continue
            found.setdefault(name, original(url))
            where.setdefault(name, set()).add(page)

    if not found:
        print('No pictures are being served from Wix — nothing to do.')
        return
    print(f'{len(found)} pictures across {len({p for s in where.values() for p in s})} pages')
    if listing:
        for n, u in sorted(found.items()):
            print(f'  {n}\n    {u}')
        return

    os.makedirs(IMAGES, exist_ok=True)
    ok = set()
    for name, url in sorted(found.items()):
        dest = os.path.join(IMAGES, name)
        if os.path.exists(dest):
            ok.add(name)
            continue
        try:
            req = urllib.request.Request(url, headers={'User-Agent': UA})
            with urllib.request.urlopen(req, timeout=60) as r:
                data = r.read()
            if not data:
                raise OSError('empty response')
            open(dest, 'wb').write(data)
            ok.add(name)
            print(f'  fetched {name}  {len(data) // 1024} KB')
        except Exception as e:                    # noqa: BLE001
            print(f'  FAILED  {name}: {e}  (page keeps the Wix URL)')

    changed = 0
    for page in pages:
        path = os.path.join(HERE, page)
        text = open(path, encoding='utf-8').read()
        out = text
        for url in set(SRC.findall(text)):
            at = text.find(url)
            alt = re.search(r'alt="([^"]*)"', text[at:at + 600])
            name = local_name(url, alt.group(1) if alt else '')
            if name in ok:
                out = out.replace(url, f'images/{name}')
        if out != text:
            open(path, 'w', encoding='utf-8').write(out)
            changed += 1
    print(f'\n{len(ok)} pictures in images/, {changed} pages rewritten to use them')


if __name__ == '__main__':
    main()
