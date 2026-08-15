/* ==========================================================================
   procedure.tax — builds the Part > group > chapter drop-downs in the header
   from nav-data.js, and keeps each panel inside the site's content column.
   ========================================================================== */
(function () {
  'use strict';

  var NAV = window.PT_NAV;
  var nav = document.querySelector('nav.main-nav');
  if (!NAV || !nav) return;

  function esc(s) {
    return String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
  }
  function key(href) {
    try { return decodeURIComponent(href).split('/').pop(); } catch (e) { return href; }
  }

  var byFile = {};
  NAV.parts.forEach(function (p) { byFile[key(p.file)] = p; });

  /* ---- build ----------------------------------------------------------- */
  var items = [];
  Array.prototype.forEach.call(nav.querySelectorAll('li'), function (li) {
    var a = li.querySelector('a');
    if (!a) return;
    var part = byFile[key(a.getAttribute('href') || '')];
    if (!part || !part.groups.length) return;

    var h = '<div class="mega"><div class="mega__cols">';
    part.groups.forEach(function (g) {
      h += '<div class="mega__group"><a href="' + g.landing + '">' +
           g.letter + '. ' + esc(g.title) + '</a><ul>';
      g.chapters.forEach(function (c) {
        h += '<li><a href="' + c.u + '"><span class="mega__code">' + c.c + '</span>' +
             esc(c.t) + '</a></li>';
      });
      h += '</ul></div>';
    });
    li.classList.add('has-menu');
    li.setAttribute('data-part', String(NAV.parts.indexOf(part) + 1));
    li.insertAdjacentHTML('beforeend', h + '</div></div>');
    items.push(li);
  });
  if (!items.length) return;

  /* ---- keep the panel inside the content column ------------------------ */
  /* The panel is absolutely positioned against its <li>. Left on its own it
     runs off the right edge of the page for the last few PART links, so on
     open we measure and clamp it to the width of .main-nav.               */
  function place(li) {
    var panel = li.querySelector('.mega');
    if (!panel || window.innerWidth <= 1000) { if (panel) panel.style.left = ''; return; }

    panel.style.left = '0px';                       /* measure from a known state */
    var navBox = nav.getBoundingClientRect();
    var liBox = li.getBoundingClientRect();
    var w = panel.offsetWidth;

    var min = navBox.left;                          /* never past the left edge  */
    var max = navBox.right - w;                     /* never past the right edge */
    var want = liBox.left + liBox.width / 2 - w / 2; /* centred under the link    */

    if (max < min) max = min;                       /* panel wider than the column */
    var left = Math.min(Math.max(want, min), max);
    panel.style.left = Math.round(left - liBox.left) + 'px';
  }

  items.forEach(function (li) {
    li.addEventListener('mouseenter', function () { place(li); });
    li.addEventListener('focusin', function () { place(li); });
  });

  var t;
  window.addEventListener('resize', function () {
    clearTimeout(t);
    t = setTimeout(function () {
      items.forEach(function (li) { var p = li.querySelector('.mega'); if (p) p.style.left = ''; });
    }, 120);
  });

  /* ---- touch / narrow: tap to open, tap again to follow the link -------- */
  items.forEach(function (li) {
    var a = li.querySelector('a');
    a.addEventListener('click', function (e) {
      var coarse = window.matchMedia('(hover: none)').matches || window.innerWidth <= 1000;
      if (!coarse) return;                          /* desktop: link works as normal */
      if (li.classList.contains('open')) return;    /* second tap follows the link    */
      e.preventDefault();
      items.forEach(function (o) { o.classList.remove('open'); });
      li.classList.add('open');
    });
  });
  document.addEventListener('click', function (e) {
    if (e.target.closest && e.target.closest('nav.main-nav')) return;
    items.forEach(function (o) { o.classList.remove('open'); });
  });
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') items.forEach(function (o) { o.classList.remove('open'); });
  });
})();
