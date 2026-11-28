(function () {
  // Light / dark theme: the header button switches it, the choice is remembered in this browser only.
  (function () {
    var root = document.documentElement, btns = document.querySelectorAll('.theme-btn');
    function sync() { var on = root.dataset.theme === 'light'; [].forEach.call(btns, function (b) { b.setAttribute('aria-pressed', String(on)); }); }
    [].forEach.call(btns, function (b) {
      b.addEventListener('click', function () {
        var on = root.dataset.theme !== 'light';
        if (on) root.dataset.theme = 'light'; else delete root.dataset.theme;
        try { localStorage.setItem('pn-theme', on ? 'light' : 'dark'); } catch (e) { /* private mode: works for this page only */ }
        sync();
      });
    });
    sync();
  })();
  var ST = {"en": {"live": "Working demo", "local": "Local preview", "in-progress": "Work in progress", "coming-soon": "Coming soon"}, "el": {"live": "Λειτουργικό demo", "local": "Τοπική προεπισκόπηση", "in-progress": "Σε εξέλιξη", "coming-soon": "Σύντομα"}};
  var cfg = window.PN_SITE || {};
  function lang() { return document.documentElement.lang === 'el' ? 'el' : 'en'; }
  function each(sel, fn) { [].forEach.call(document.querySelectorAll(sel), fn); }
  var blobs = {};
  if (window.PN) {
    PN.full = function (slug) {
      var d = window.PN_DEMOS && PN_DEMOS[slug];
      if (d) { if (!blobs[slug]) blobs[slug] = URL.createObjectURL(new Blob([d], { type: 'text/html' })); return blobs[slug]; }
      return PN.url(slug);
    };
  }
  function refresh() {
    var P = window.PN, L = ST[lang()];
    if (P) {
      each('[data-status]', function (el) { var p = P.projects[el.dataset.status]; if (p) el.textContent = L[p.status] || L['coming-soon']; });
      each('[data-open]', function (a) { var u = P.url(a.dataset.open); a.hidden = !u; if (!u) return; var f = P.full(a.dataset.open); if (lang() === 'el' && f.charAt(0) === '/') f += (f.indexOf('?') < 0 ? '?' : '&') + 'lang=el'; a.href = f; });
      each('[data-unavailable]', function (n) { n.hidden = !!P.url(n.dataset.unavailable); });
    }
    each('[data-contact]', function (el) {
      var k = el.dataset.contact, v = cfg[k];
      if (!v) return;
      if (k === 'area') { el.textContent = v; return; }
      var a = document.createElement('a');
      a.href = k === 'email' ? 'mailto:' + v : 'tel:' + v.replace(/[^+\d]/g, '');
      a.textContent = v; el.textContent = ''; el.appendChild(a);
    });
    each('[data-mailto]', function (a) { a.hidden = !cfg.email; if (cfg.email) a.href = 'mailto:' + cfg.email; });
  }
  document.addEventListener('click', function (e) {
    var b = e.target.closest('.menu-btn');
    if (!b) return;
    var n = b.parentNode.querySelector('nav'), o = n.classList.toggle('open');
    b.setAttribute('aria-expanded', String(o));
  });
  document.addEventListener('keydown', function (e) {
    if (e.key !== 'Escape') return;
    each('nav.open', function (n) { n.classList.remove('open'); var b = n.parentNode.querySelector('.menu-btn'); if (b) { b.setAttribute('aria-expanded', 'false'); b.focus(); } });
  });
  if ('IntersectionObserver' in window && !matchMedia('(prefers-reduced-motion: reduce)').matches) {
    document.documentElement.classList.add('rv');
    var io = new IntersectionObserver(function (es) { es.forEach(function (x) { if (x.isIntersecting) { x.target.classList.add('in'); io.unobserve(x.target); } }); }, { threshold: 0.12, rootMargin: '0px 0px -6% 0px' });
    each('.reveal', function (el) { io.observe(el); });
  }
  window.PNrefresh = refresh; refresh();
  // PN_HOME: reveal-on-scroll and FAQ accordion for the homepage (safe to run on any page)
  (function () {
    var reduce = window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches;
    var els = [].slice.call(document.querySelectorAll('.reveal'));
    function showNow(e) { var r = e.getBoundingClientRect(); return r.top < window.innerHeight && r.bottom > 0; }
    if (!('IntersectionObserver' in window) || reduce) { els.forEach(function (e) { e.classList.add('in'); }); }
    else if (!els.length) { }
    else {
      var io = new IntersectionObserver(function (entries) {
        entries.forEach(function (x) { if (x.isIntersecting) { x.target.classList.add('in'); io.unobserve(x.target); } });
      }, { threshold: 0.14, rootMargin: '0px 0px -8% 0px' });
      els.forEach(function (e) { if (showNow(e)) e.classList.add('in'); else io.observe(e); });
      setTimeout(function () { els.forEach(function (e) { if (e.getBoundingClientRect().top < window.innerHeight + 200) e.classList.add('in'); }); }, 1500);
      window.addEventListener('scroll', function () {
        if (document.documentElement.scrollHeight - (window.innerHeight + window.scrollY) < 60) { els.forEach(function (e) { e.classList.add('in'); }); }
      }, { passive: true });
    }
    document.addEventListener('click', function (e) {
      var q = e.target.closest('.faq button.q');
      if (!q) return;
      var item = q.closest('.item'), open = item.classList.toggle('open');
      q.setAttribute('aria-expanded', String(open));
    });
  })();
})();
