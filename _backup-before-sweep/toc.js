/* Marks the section you are reading in the docked contents rail.
   The rail is hidden below 1200px, where this does nothing. */
(function () {
  'use strict';
  var rail = document.querySelector('.toc-side');
  if (!rail) return;

  var marks = [];
  [].forEach.call(rail.querySelectorAll('a'), function (a) {
    var id = (a.getAttribute('href') || '').replace(/^#/, '');
    var el = id ? document.getElementById(id) : null;
    if (el) marks.push({ row: a.parentElement, el: el });
  });
  if (!marks.length) return;

  function spy() {
    if (!rail.offsetParent && getComputedStyle(rail).display === 'none') return;
    var y = window.scrollY + 90, cur = null;
    for (var i = 0; i < marks.length; i++) {
      if (marks[i].el.getBoundingClientRect().top + window.scrollY <= y) cur = marks[i];
    }
    for (var j = 0; j < marks.length; j++) marks[j].row.classList.remove('here');
    if (!cur) return;
    cur.row.classList.add('here');
    var r = cur.row.getBoundingClientRect(), s = rail.getBoundingClientRect();
    if (r.top < s.top || r.bottom > s.bottom) cur.row.scrollIntoView({ block: 'nearest' });
  }

  var ticking = false;
  window.addEventListener('scroll', function () {
    if (ticking) return;
    ticking = true;
    requestAnimationFrame(function () { spy(); ticking = false; });
  }, { passive: true });
  spy();
})();
