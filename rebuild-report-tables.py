#!/usr/bin/env python3
"""Swap the litigation report's table pictures for real HTML tables.

The report's tables are pictures. A picture cannot be searched, cannot be
selected or quoted, does not reflow on a phone, and reads as nothing at all to
a screen reader. This replaces each one with a <table> transcribed from it.

The transcriptions live in a JSON file, keyed by the anchor of the item the
picture sits under, so a correction is a one-line edit and a re-run rather than
hand-surgery on the page:

    {
      "fttsubstantivedecisions": {
        "groups":  [["Tax", 1], ["Cases", 2]],       # optional top header row
        "columns": ["Tax", "2024", "2025"],           # bottom header row
        "rows":    [["CGT", "19", "5"], ...],
        "foot":    ["Total", "193", "164"]            # optional total row
      }
    }

A row whose cells are all empty except the first is a section break — the
"Taxpayer" / "HMRC" / "Combinations" bands in the representatives table — and
is rendered as one heading spanning the width rather than as a row of blanks.

    python3 scripts/tables_from_images.py PAGE report-tables.json [--keep]

--keep leaves the picture below the table instead of removing it.
"""
import json
import os
import sys

from bs4 import BeautifulSoup


def esc(s):
    return str(s).replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


def alignment(spec):
    """First column names the row; everything else is a figure.

    Figures are right-aligned on tabular numerals so that a column of them
    lines up on the digit — the original pictures left-align them, which makes
    "9%" and "100%" impossible to compare down the column.
    """
    if spec.get('align'):
        return spec['align']
    return ['left'] + ['right'] * (len(spec['columns']) - 1)


def is_section(row):
    return bool(row) and row[0].strip() and not any(c.strip() for c in row[1:])


def widths(n):
    """Column widths, as percentages, for a table stretched to the text width.

    Left to itself the browser hands the slack to whichever column has the most
    content, which on a four-column table is the label: "CGT" then 400px of
    nothing then "5". So the figures get a fixed share each and the label column
    takes what is left — a wide share on a narrow table, a narrow one on a table
    with eight columns of figures to fit.
    """
    figs = n - 1
    if figs < 1:
        return [100.0]
    each = 100.0 / (figs + 2.6)
    return [round(100.0 - each * figs, 2)] + [round(each, 2)] * figs


def table_html(spec):
    cols, align = spec['columns'], alignment(spec)
    n = len(cols)
    out = ['<table class="content-table content-table--report">']
    out.append('  <colgroup>' + ''.join(f'<col style="width:{w}%">'
                                        for w in widths(n)) + '</colgroup>')
    if spec.get('caption'):
        out.append(f'  <caption>{esc(spec["caption"])}</caption>')

    out.append('  <thead>')
    groups = spec.get('groups')
    if groups:
        # a single-column group carrying the same label as the column beneath
        # it is one heading two rows tall, not two headings
        first_spans_both = groups[0][1] == 1 and groups[0][0] == cols[0]
        cells = []
        for i, (label, span) in enumerate(groups):
            rs = ' rowspan="2"' if i == 0 and first_spans_both else ''
            scope = 'col' if span == 1 else 'colgroup'
            # colspan only where it spans: the stylesheet centres a group
            # heading by selecting on [colspan], and a colspan="1" written out
            # in full would sweep every ordinary column heading in with them
            cs = f' colspan="{span}"' if span > 1 else ''
            cells.append(f'<th scope="{scope}"{cs}{rs}>{esc(label)}</th>')
        out.append('    <tr>' + ''.join(cells) + '</tr>')
        start = 1 if first_spans_both else 0
        out.append('    <tr>' + ''.join(
            f'<th scope="col" class="ta-{align[i]}">{esc(cols[i])}</th>'
            for i in range(start, n)) + '</tr>')
    else:
        out.append('    <tr>' + ''.join(
            f'<th scope="col" class="ta-{align[i]}">{esc(c)}</th>'
            for i, c in enumerate(cols)) + '</tr>')
    out.append('  </thead>')

    out.append('  <tbody>')
    # Banding is written on the row rather than left to :nth-child, because a
    # section band is itself a row: counted, it flips the alternation halfway
    # down the representatives table and the stripes stop meaning anything.
    band = False
    for row in spec['rows']:
        if is_section(row):
            out.append(f'    <tr class="tr-section"><th colspan="{n}" scope="colgroup">'
                       f'{esc(row[0])}</th></tr>')
            band = False                       # each block starts again
            continue
        cells = [f'<th scope="row" class="ta-{align[0]}">{esc(row[0])}</th>']
        cells += [f'<td class="ta-{align[i]}">{esc(c)}</td>'
                  for i, c in enumerate(row[1:], start=1)]
        cls = ' class="band"' if band else ''
        out.append(f'    <tr{cls}>' + ''.join(cells) + '</tr>')
        band = not band
    out.append('  </tbody>')

    if spec.get('foot'):
        f = spec['foot']
        out.append('  <tfoot>')
        out.append('    <tr>' + f'<th scope="row" class="ta-{align[0]}">{esc(f[0])}</th>'
                   + ''.join(f'<td class="ta-{align[i]}">{esc(c)}</td>'
                             for i, c in enumerate(f[1:], start=1)) + '</tr>')
        out.append('  </tfoot>')
    out.append('</table>')
    return '\n'.join(out)


def check(name, spec):
    """Refuse to write a table whose rows do not match its own header."""
    n = len(spec['columns'])
    bad = []
    if spec.get('groups') and sum(s for _l, s in spec['groups']) != n:
        bad.append(f'group spans total {sum(s for _l, s in spec["groups"])}, not {n}')
    for i, r in enumerate(spec['rows']):
        if len(r) != n:
            bad.append(f'row {i} has {len(r)} cells, not {n}')
    if spec.get('foot') and len(spec['foot']) != n:
        bad.append(f'foot has {len(spec["foot"])} cells, not {n}')
    for b in bad:
        print(f'  ! {name}: {b}')
    return not bad


def main():
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    page, data_path = sys.argv[1], sys.argv[2]
    keep = '--keep' in sys.argv

    specs = json.load(open(data_path, encoding='utf-8'))
    if not all(check(k, v) for k, v in specs.items()):
        sys.exit('nothing written')

    soup = BeautifulSoup(open(page, encoding='utf-8').read(), 'html.parser')
    main_el = soup.find('main')
    inner = main_el.find('div', class_='page__inner') or main_el
    kids = list(inner.find_all(['div', 'figure', 'table'], recursive=False))

    done = missing = 0
    for anchor_id, spec in specs.items():
        at = next((i for i, e in enumerate(kids)
                   if e.name == 'div' and 'anchor' in (e.get('class') or [])
                   and e.get('id') == anchor_id), None)
        if at is None:
            print(f'  ! no anchor {anchor_id!r} on the page')
            missing += 1
            continue
        fig = next((e for e in kids[at:] if e.name == 'figure'), None)
        if fig is None:
            print(f'  ! nothing to replace under {anchor_id!r}')
            missing += 1
            continue
        fig.insert_before(BeautifulSoup(table_html(spec), 'html.parser'))
        if keep:
            fig['class'] = (fig.get('class') or []) + ['page-image--original']
        else:
            fig.decompose()
        done += 1

    if done:
        open(page, 'w', encoding='utf-8').write(str(soup))
    print(f'{done} tables written into {os.path.basename(page)}'
          + (f', {missing} could not be placed' if missing else ''))


if __name__ == '__main__':
    main()
