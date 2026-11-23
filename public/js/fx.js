// Interaction layer. Every effect below is off when the visitor prefers reduced motion;
// pointer effects only run on devices with a real mouse. Content is fully usable without this file.
(function () {
  var d = document, root = d.documentElement;
  var rm = matchMedia('(prefers-reduced-motion: reduce)').matches;
  var fine = matchMedia('(hover: hover) and (pointer: fine)').matches;
  function all(s) { return [].slice.call(d.querySelectorAll(s)); }

  // scroll progress bar + header that tightens on scroll + timeline that fills as you read
  var bar = d.createElement('div'); bar.className = 'progress'; bar.setAttribute('aria-hidden', 'true'); d.body.appendChild(bar);
  var hdr = d.querySelector('header.top'), tl = d.querySelector('.timeline'), ticking = false;
  function timeline() {
    if (!tl) return;
    var r = tl.getBoundingClientRect(), p = Math.max(0, Math.min(1, (innerHeight * 0.65 - r.top) / r.height));
    tl.style.setProperty('--tl', p.toFixed(3));
    [].forEach.call(tl.children, function (li) { li.classList.toggle('on', li.getBoundingClientRect().top < innerHeight * 0.65); });
  }
  function onScroll() {
    var h = root.scrollHeight - innerHeight, y = window.scrollY;
    bar.style.transform = 'scaleX(' + (h > 0 ? Math.min(1, y / h) : 0).toFixed(4) + ')';
    if (hdr) hdr.classList.toggle('scrolled', y > 24);
    timeline(); ticking = false;
  }
  addEventListener('scroll', function () { if (!ticking) { ticking = true; requestAnimationFrame(onScroll); } }, { passive: true });
  addEventListener('resize', onScroll);

  // animated counters (the numbers are real facts about this site; the final value is also in the HTML)
  var cs = all('.count');
  if (cs.length && !rm && 'IntersectionObserver' in window) {
    var cio = new IntersectionObserver(function (es) {
      es.forEach(function (x) {
        if (!x.isIntersecting) return; cio.unobserve(x.target);
        var el = x.target, to = +el.dataset.to, t0 = performance.now();
        (function tick(t) { var p = Math.min(1, (t - t0) / 1100); el.textContent = Math.round(to * (1 - Math.pow(1 - p, 3))); if (p < 1) requestAnimationFrame(tick); })(t0);
      });
    }, { threshold: 0.6 });
    cs.forEach(function (c) { c.textContent = '0'; cio.observe(c); });
  }

  if (!rm) {
    // headline: words rise into place one after another
    var h1 = d.querySelector('.hero2 h1');
    if (h1) {
      var i = 0;
      (function walk(n) {
        [].slice.call(n.childNodes).forEach(function (c) {
          if (c.nodeType === 3) {
            var frag = d.createDocumentFragment();
            c.textContent.split(/(\s+)/).forEach(function (t) {
              if (!t) return;
              if (/^\s+$/.test(t)) { frag.appendChild(d.createTextNode(t)); return; }
              var w = d.createElement('span'), s = d.createElement('span');
              w.className = 'w'; s.textContent = t; s.style.setProperty('--d', (i++ * 70) + 'ms'); w.appendChild(s); frag.appendChild(w);
            });
            n.replaceChild(frag, c);
          } else if (c.nodeType === 1) walk(c);
        });
      })(h1);
      h1.classList.add('wsplit');
    }
  }

  if (fine && !rm) {
    // hero depth: mockups drift opposite to the cursor, a soft spotlight follows it
    var hero = d.querySelector('.hero2'), raf = 0;
    if (hero) {
      hero.addEventListener('pointermove', function (e) {
        var r = hero.getBoundingClientRect(), x = (e.clientX - r.left) / r.width - 0.5, y = (e.clientY - r.top) / r.height - 0.5, px = e.clientX - r.left, py = e.clientY - r.top;
        if (raf) return;
        raf = requestAnimationFrame(function () { raf = 0; hero.style.setProperty('--mx', x.toFixed(3)); hero.style.setProperty('--my', y.toFixed(3)); hero.style.setProperty('--px', px + 'px'); hero.style.setProperty('--py', py + 'px'); });
      });
      hero.addEventListener('pointerleave', function () { hero.style.setProperty('--mx', 0); hero.style.setProperty('--my', 0); });
    }
    // magnetic buttons
    all('.hero2 .btn, .cta-final .btn').forEach(function (b) {
      b.addEventListener('pointermove', function (e) { var r = b.getBoundingClientRect(); b.style.translate = ((e.clientX - r.left - r.width / 2) * 0.18).toFixed(1) + 'px ' + ((e.clientY - r.top - r.height / 2) * 0.28).toFixed(1) + 'px'; });
      b.addEventListener('pointerleave', function () { b.style.translate = ''; });
    });
    // project previews tilt toward the cursor
    all('.feature').forEach(function (f) {
      var a = f.querySelector('.feature-art');
      f.addEventListener('pointermove', function (e) { var r = f.getBoundingClientRect(), x = (e.clientX - r.left) / r.width - 0.5, y = (e.clientY - r.top) / r.height - 0.5; a.style.transform = 'perspective(900px) rotateX(' + (-y * 7).toFixed(2) + 'deg) rotateY(' + (x * 9).toFixed(2) + 'deg) scale(1.02)'; });
      f.addEventListener('pointerleave', function () { a.style.transform = ''; });
    });
    // price cards: a soft light follows the cursor
    all('.plan').forEach(function (p) {
      p.addEventListener('pointermove', function (e) { var r = p.getBoundingClientRect(); p.style.setProperty('--px', (e.clientX - r.left) + 'px'); p.style.setProperty('--py', (e.clientY - r.top) + 'px'); });
    });
  }
  onScroll();
})();
