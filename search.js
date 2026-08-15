/* ==========================================================================
   Client-side search for procedure.tax.

   Wix's search ran on Wix's servers, so a static export cannot carry it. This
   reads a prebuilt inverted index (search-index.json, ~1.3 MB) and searches in
   the browser. No dependencies, no build step, no network calls beyond the
   index and the pages it quotes.

   Snippets are pulled from the matched pages on demand rather than stored in
   the index, which keeps the index small enough to load in one go.

   Pinegrow note: this file and search.css only affect search.html. Nothing
   else on the site depends on them, so both can be deleted outright if you
   would rather wire up your own search.

   NOTE: this file lives in assets/ and is copied into the output at packaging
   time. Anything written straight into the build directory is destroyed the
   next time the converter runs.
   ========================================================================== */
(function () {
  'use strict';

  var MAX_RESULTS = 40;      // results listed
  var SNIPPET_FOR = 12;      // pages actually fetched for a snippet
  var idx = null, loading = null;

  var $q = document.getElementById('q');
  var $status = document.getElementById('status');
  var $results = document.getElementById('results');

  function tokenise(s) {
    return (s.toLowerCase().match(/[a-z0-9]+(?:'[a-z]+)?/g) || [])
      .filter(function (t) { return t.length >= 2; });
  }

  function loadIndex() {
    if (loading) return loading;
    loading = fetch('search-index.json')
      .then(function (r) {
        if (!r.ok) throw new Error('HTTP ' + r.status);
        return r.json();
      })
      .then(function (j) { idx = j; return j; });
    return loading;
  }

  // Rank: every query term must appear (AND), then prefer pages matching more
  // distinct terms, then pages whose heading matches.
  function search(query) {
    var terms = tokenise(query);
    if (!terms.length) return [];
    var counts = Object.create(null), n = 0;

    terms.forEach(function (t) {
      var posting = idx.terms[t];
      if (!posting) {
        // fall back to a prefix match, so "assess" finds "assessment"
        var seen = Object.create(null);
        posting = [];
        for (var k in idx.terms) {
          if (k.indexOf(t) === 0) {
            idx.terms[k].forEach(function (p) { seen[p] = 1; });
          }
        }
        for (var pk in seen) posting.push(+pk);
      }
      if (!posting.length) return;
      n++;
      posting.forEach(function (p) { counts[p] = (counts[p] || 0) + 1; });
    });

    if (!n) return [];
    var out = [];
    for (var p in counts) {
      if (counts[p] < n) continue;               // AND across the terms found
      var page = idx.pages[p];
      var titleHits = 0, lt = page.t.toLowerCase();
      terms.forEach(function (t) { if (lt.indexOf(t) >= 0) titleHits++; });
      out.push({ u: page.u, t: page.t, score: counts[p] * 10 + titleHits * 5 });
    }
    out.sort(function (a, b) { return b.score - a.score || a.t.localeCompare(b.t); });
    return out;
  }

  function esc(s) {
    return s.replace(/[&<>"]/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c];
    });
  }

  // Pull a snippet out of the page itself, so the index does not have to carry
  // the whole handbook's text.
  function snippet(url, terms, el) {
    fetch(url).then(function (r) { return r.text(); }).then(function (page) {
      var m = page.match(/<main[\s\S]*?<\/main>/i);
      if (!m) return;
      var div = document.createElement('div');
      div.innerHTML = m[0].replace(/<nav[\s\S]*?<\/nav>/gi, '');
      var text = (div.textContent || '').replace(/​/g, ' ').replace(/\s+/g, ' ').trim();
      var low = text.toLowerCase(), at = -1;
      for (var i = 0; i < terms.length && at < 0; i++) at = low.indexOf(terms[i]);
      if (at < 0) return;
      var start = Math.max(0, at - 90), end = Math.min(text.length, at + 220);
      var frag = (start > 0 ? '…' : '') + text.slice(start, end) +
                 (end < text.length ? '…' : '');
      var out = esc(frag);
      terms.forEach(function (t) {
        out = out.replace(new RegExp('(' + t.replace(/[.*+?^${}()|[\]\\]/g, '\\$&') + ')', 'gi'),
                          '<mark>$1</mark>');
      });
      el.innerHTML = out;
    }).catch(function () { /* a missing page just means no snippet */ });
  }

  function render(query) {
    var hits = search(query);
    var terms = tokenise(query);
    $results.innerHTML = '';

    if (!hits.length) {
      $status.textContent = 'No pages match ' + JSON.stringify(query) + '.';
      return;
    }
    $status.textContent = hits.length + (hits.length === 1 ? ' page matches ' : ' pages match ') +
      JSON.stringify(query) +
      (hits.length > MAX_RESULTS ? ' — showing the first ' + MAX_RESULTS : '');

    hits.slice(0, MAX_RESULTS).forEach(function (h, i) {
      var li = document.createElement('li');
      var a = document.createElement('a');
      a.className = 'search-results__title';
      a.href = h.u;
      a.textContent = h.t;
      var p = document.createElement('p');
      p.className = 'search-results__snippet';
      li.appendChild(a);
      li.appendChild(p);
      $results.appendChild(li);
      if (i < SNIPPET_FOR) snippet(h.u, terms, p);
    });
  }

  function run(query) {
    if (!query || !query.trim()) {
      $status.textContent = 'Type a word or phrase to search all ' +
        (idx ? idx.pages.length : '') + ' pages of the handbook.';
      $results.innerHTML = '';
      return;
    }
    $status.textContent = 'Searching…';
    loadIndex().then(function () { render(query.trim()); })
      .catch(function (e) {
        $status.textContent = 'The search index could not be loaded (' + e.message + '). ' +
          'If you are opening these files straight off disk, some browsers block that — ' +
          'serve the folder over http instead.';
      });
  }

  // the header's search box submits ?q=... to this page
  var initial = new URLSearchParams(location.search).get('q') || '';
  if ($q) {
    $q.value = initial;
    var timer = null;
    $q.addEventListener('input', function () {
      clearTimeout(timer);
      var v = $q.value;
      timer = setTimeout(function () { run(v); }, 180);
    });
  }
  loadIndex().then(function () { run(initial); }).catch(function () { run(initial); });
})();
