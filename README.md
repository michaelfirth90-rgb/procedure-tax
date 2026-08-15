# procedure.tax — converted to plain, editable HTML

This is the whole of procedure.tax rebuilt as static HTML, CSS and one small
JavaScript file, with no Wix runtime, no build step and no framework. Open the
folder in Pinegrow and edit it directly.

## What is here

```
index.html                            the home page, with the contents tree
a1-care-and-management-general.html   one file per page: its number, then its title
m4-disclosure.html                    ...
part-1-tax-compliance.html            the eight Part pages
a-general-principles-and-concepts.html   the lettered section pages
search.html              search (new — see below)
proceduretax.css         the whole site's styling, derived by measurement
fonts.css                @font-face rules pointing at the fonts the site uses
search.css, search.js    only used by search.html
search-index.json        the prebuilt search index
```

319 pages, plus the stylesheets and the search files.

Each file is named from the page's own number followed by its title, so the
files sort into the handbook's reading order and are recognisable in an editor
without opening them. The number is the one on the page's heading, which is the
authoritative one on this site — see the conversion report. Every internal link
was rewritten to match: 4,399 page-to-page links, none broken.

## How it was built

Every original page was rendered in a headless browser and measured, and each
page was then rebuilt from its own text using that measured geometry. Nothing
was reconstructed by reading Wix's CSS, and nothing was converted in document
order — Wix lays components out on a mesh grid, so the order in the exported
file is not the order things appear on screen.

The result was checked back against the original two ways:

- **Word for word**, every page: the bag of words from the rendered original
  against the rendered rebuild.
- **Pixel for pixel**, on a long page at three scroll positions: 0 differing
  pixels out of 1,440,000 in the middle of the page, and 0.1–0.14% at the top
  and bottom, all of it either antialiasing or the two CDN-hosted assets that
  cannot load offline.

## Editing it in Pinegrow

The markup is deliberately plain: `<header>`, `<main>`, `<footer>`, and inside
the content a flat sequence of `<p>`, `<h2>`, `<h3>`, `<ul>` and one `<table>`.
Wix's fifteen-deep `<span>` nesting has been flattened to one span per run of
text that shares a style.

Two things to know before you edit:

**The colour system is the `font_N` and `color_N` classes.** They are the
site's own type and colour scheme, kept by name — green for legislation, blue
for case law, red for HMRC material. They are all defined at the top of
`proceduretax.css`, so the whole site's colour key can be changed in one place.
The colour defaults are written with `:where()` so they have zero specificity
and never beat these classes, and repeated in a `:not([class*="font_"])` form
so they still apply in an engine that does not support `:where()`. The margin
reset is kept in a separate rule of plain selectors on purpose — the page's
whole vertical rhythm depends on it, and it must not be lost with the rest of
a `:where()` rule that an engine cannot parse.

**Vertical spacing is set inline, per block, as `margin-top`.** Those numbers
are the measured gaps from the original. They are ordinary margins, so the page
still flows and reflows normally; if you delete a block, the one below keeps
its own gap. If you would rather have uniform spacing, the inline margins can
be stripped and a single rule put in the stylesheet.

**The blank paragraphs between blocks are load-bearing.** The site's vertical
rhythm is built out of them, not out of CSS margins. They each hold a
zero-width space (`&#8203;`) rather than a non-breaking space, deliberately:
Pinegrow's editor discards a paragraph whose only content is a non-breaking
space, which silently removes about half the gaps on the page in the editor
while the browser still shows them. If you add spacing of your own, add it the
same way — a blank paragraph holding `&#8203;` — or as an explicit margin.
A blank paragraph holding ordinary spaces collapses to nothing in a browser.

`line-height` is also stamped inline on each block. That is not decoration:
the original mixes blocks computing `normal` with blocks taking 1.4em, and the
difference compounds — a blanket rule either way moves the foot of a long page
by hundreds of pixels. Leave those alone unless you are changing the design.

## The contents on each page

Two things, on every page that has a contents menu:

**A rail down the left** listing the categories and sections — not the points.
On M4 that is 38 lines rather than 104. It sticks as you scroll and marks the
section you are reading. It appears only at 1340px and wider; below that there
is not room for it beside a 975px column without the page overflowing, so it
is hidden.

**The full contents at the top of the column**, all three tiers, in tinted
cards. This is what carries navigation on a laptop, tablet or phone, which is
why both are present rather than one.

The three tiers come from the page's own headings: an ALL-CAPS heading is a
category, an `h2` opens a section, anything deeper is a point inside it. The
same three tiers are marked on the body headings (`bh-cat`, `bh-sec`,
`bh-point`) so the page and its contents agree.

Category headings are `#8B0000` — the same red this site already uses for case
citations. It is set once, as `--cat-red` at the top of `proceduretax.css`,
along with `--card-tint` for the pastel green fill.

When the rail is showing, the whole 980px grid shifts right by `--rail-shift`
to make room for it. Because the header, nav, content column and footer all
position from `--grid-offset`, they move together and stay aligned — worth
knowing before changing any of those numbers.

`toc.js` marks the current section in the rail. It does nothing when the rail
is hidden, and deleting it costs only that highlight.

## Search

Wix's search ran on Wix's servers and no static export can carry it. The header
box now points at `search.html`, which searches a prebuilt index of all 319
pages in the browser. No server, no dependencies.

If you would rather not have it, delete `search.html`, `search.css`,
`search.js` and `search-index.json` — nothing else refers to them.

If you add or edit pages, the index needs rebuilding, or search will still be
looking at the old text.

## Three things that are not mine to decide

**The fonts are still Wix's.** Brandon Grotesque, DIN Next, Cormorant Garamond,
Droid Serif and Futura are commercially licensed faces, and `fonts.css` points
at the same `static.parastorage.com` URLs the live site uses. No font data has
been copied. If the site moves off Wix, they will need licensing and hosting —
or the stack in `proceduretax.css` can fall back to what is already listed
there.

**The images are still on Wix's CDN.** The logo in the header and footer loads
from `static.wixstatic.com`. It will keep working while the Wix site exists.
To be self-contained, it needs downloading and the two `<img src>` values
changing.

**Search is new.** It is an addition, not a reproduction. See above.

## Opening the files

Double-clicking `index.html` works for everything except search, which needs to
read `search-index.json` — some browsers block that over `file://`. To use
search locally, serve the folder:

```
python3 -m http.server 8000
```

then open <http://localhost:8000/>.
