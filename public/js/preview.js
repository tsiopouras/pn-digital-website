(function () {
  var dlg = document.getElementById('pv');
  if (!dlg || !dlg.showModal) return;
  var MSG = {
    en: { title: 'quick preview', size: 'Preview size', desktop: 'Desktop', phone: 'Phone', open: 'Open full website', close: 'Close',
      note: 'Concept project: the business and its details are fictional, and demonstration forms do not send anything. If the preview does not load, use “Open full website”.',
      loading: 'Loading preview…', none: ' does not have a working preview yet. Its status is shown on the project page.',
      slow: 'Still loading. If this stays blank, the site may not allow embedding. Use “Open full website” instead.', frame: ' website preview' },
    el: { title: 'γρήγορη προεπισκόπηση', size: 'Μέγεθος προεπισκόπησης', desktop: 'Υπολογιστής', phone: 'Κινητό', open: 'Άνοιγμα πλήρους ιστοσελίδας', close: 'Κλείσιμο',
      note: 'Πρότυπο έργο: η επιχείρηση και τα στοιχεία της είναι φανταστικά και οι φόρμες επίδειξης δεν στέλνουν τίποτα. Αν η προεπισκόπηση δεν φορτώσει, χρησιμοποιήστε το «Άνοιγμα πλήρους ιστοσελίδας».',
      loading: 'Φόρτωση προεπισκόπησης…', none: ' δεν έχει ακόμη λειτουργική προεπισκόπηση. Η κατάστασή του φαίνεται στη σελίδα του έργου.',
      slow: 'Φορτώνει ακόμη. Αν παραμείνει κενό, η ιστοσελίδα ίσως δεν επιτρέπει ενσωμάτωση. Χρησιμοποιήστε το «Άνοιγμα πλήρους ιστοσελίδας».', frame: ' προεπισκόπηση ιστοσελίδας' }
  };
  function $(s) { return dlg.querySelector(s); }
  var title = $('#pv-title'), openLink = $('#pv-open'), msg = $('#pv-msg'), stage = $('.pv-stage'), fit = $('.pv-fit'),
      dev = $('.pv-device'), frame = $('iframe'), note = $('#pv-note'), group = $('[role=group]');
  var buttons = [].slice.call(dlg.querySelectorAll('button[data-mode]'));
  var SIZE = { desktop: [1280, 800], phone: [410, 860] }, mode = 'desktop', timer, m = MSG.en; // phone size includes the bezel
  function layout() {
    var d = SIZE[mode], s = Math.min(1, (stage.clientWidth - 32) / d[0], (stage.clientHeight - 32) / d[1]);
    dev.style.width = d[0] + 'px'; dev.style.height = d[1] + 'px'; dev.style.transform = 'scale(' + s + ')';
    fit.style.width = Math.floor(d[0] * s) + 'px'; fit.style.height = Math.floor(d[1] * s) + 'px';
  }
  function setMode(x) {
    mode = x; dev.dataset.mode = x;
    buttons.forEach(function (b) { b.setAttribute('aria-pressed', String(b.dataset.mode === x)); });
    layout();
  }
  function show(t, loading) { msg.textContent = t; msg.classList.toggle('loading', !!loading); msg.hidden = false; }
  function close() {
    if (!dlg.open) return;
    if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) { dlg.close(); return; }
    dlg.classList.add('closing');
    setTimeout(function () { dlg.classList.remove('closing'); dlg.close(); }, 200);
  }
  document.addEventListener('click', function (e) {
    var b = e.target.closest('[data-preview]');
    if (!b) return;
    m = MSG[document.documentElement.lang === 'el' ? 'el' : 'en'];
    var slug = b.dataset.preview, name = b.dataset.name, url = window.PN ? PN.url(slug) : '';
    var lang = document.documentElement.lang === 'el' ? 'el' : 'en';
    clearTimeout(timer); frame.onload = null;
    title.textContent = name + ': ' + m.title; frame.title = name + m.frame; group.setAttribute('aria-label', m.size);
    buttons[0].textContent = m.desktop; buttons[1].textContent = m.phone;
    $('#pv-close').textContent = m.close; openLink.textContent = m.open; note.textContent = m.note;
    if (!dlg.open) dlg.showModal();
    dlg.classList.add('notr'); setMode(window.innerWidth < 720 ? 'phone' : 'desktop'); void dev.offsetWidth;
    requestAnimationFrame(function () { dlg.classList.remove('notr'); });
    if (!url) { dev.hidden = true; openLink.hidden = true; show(name + m.none); return; }
    dev.hidden = false; dev.classList.add('wait'); openLink.hidden = false; var full = PN.full ? PN.full(slug) : url; if (lang === 'el' && full.indexOf('blob:') !== 0) full += (full.indexOf('?') < 0 ? '?' : '&') + 'lang=el'; openLink.href = full;
    show(m.loading, true);
    frame.onload = function () {
      clearTimeout(timer); dev.classList.remove('wait'); msg.hidden = true;
      try { frame.contentWindow.postMessage({ pnLang: lang }, '*'); } catch (x) { /* demo without a language switcher */ }
      try { frame.contentWindow.addEventListener('keydown', function (ev) { if (ev.key === 'Escape') close(); }); } catch (x) { /* cross-origin demo: use the Close button */ }
    };
    var inline = window.PN_DEMOS && PN_DEMOS[slug];
    if (inline) { frame.removeAttribute('src'); frame.srcdoc = inline; } else { frame.removeAttribute('srcdoc'); frame.src = url + (lang === 'el' ? (url.indexOf('?') < 0 ? '?' : '&') + 'lang=el' : ''); }
    timer = setTimeout(function () { show(m.slow); }, 8000);
  });
  buttons.forEach(function (b) { b.addEventListener('click', function () { setMode(b.dataset.mode); }); });
  $('#pv-close').addEventListener('click', close);
  dlg.addEventListener('cancel', function (e) { e.preventDefault(); close(); });
  dlg.addEventListener('click', function (e) { if (e.target === dlg) close(); });
  dlg.addEventListener('close', function () { clearTimeout(timer); frame.onload = null; frame.removeAttribute('src'); frame.removeAttribute('srcdoc'); });
  window.addEventListener('resize', function () { if (dlg.open) layout(); });
})();
