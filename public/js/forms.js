/* P&N Digital: WhatsApp button, contact form, quote calculator and the wireframe/finished comparison slider.
   Nothing here sends or stores data. The form and the calculator only open the visitor's own WhatsApp or
   email app with a ready-made message; the visitor decides whether to send it. */
(function () {
  'use strict';
  var C = window.PN_SITE || {};
  var WA = C.whatsapp || '35794426190', MAIL = C.email || 'pndigitalwebsites@gmail.com';
  var RM = window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches;
  function pageLang() { return document.documentElement.lang === 'el' ? 'el' : 'en'; }
  function each(sel, fn, root) { [].forEach.call((root || document).querySelectorAll(sel), fn); }
  function waUrl(text) { return 'https://wa.me/' + WA + '?text=' + encodeURIComponent(text); }
  function mailUrl(subject, body) { return 'mailto:' + MAIL + '?subject=' + encodeURIComponent(subject) + '&body=' + encodeURIComponent(body); }
  // a 'noopener' feature string makes window.open return null even when it worked, so detach the opener by hand instead
  function openWa(url) { var w = window.open(url, '_blank'); if (w) { try { w.opener = null; } catch (e) { /* ignore */ } } else location.href = url; }
  var WA_ICON = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 3a9 9 0 0 0-7.8 13.5L3 21l4.6-1.2A9 9 0 1 0 12 3z" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round"/><path d="M9 8.2c.3-.4.7-.4 1-.1l.9 1.6c.1.3 0 .6-.2.8l-.5.5c.5 1.1 1.4 2 2.6 2.6l.5-.5c.2-.2.5-.3.8-.2l1.6.9c.3.2.3.7-.1 1-.6.6-1.4.9-2.2.7-2.6-.7-4.6-2.7-5.2-5.2-.2-.8.1-1.6.8-2.1z" fill="currentColor"/></svg>';

  var X = {
    en: {
      hello: 'Hi P&N Digital, I’d like to ask about a website.', waLabel: 'Message us on WhatsApp (opens WhatsApp)',
      errName: 'Please enter your name.', errMsg: 'Please write a short message (at least 10 characters).', errSum: 'Please check the highlighted fields.',
      openingWa: 'Opening WhatsApp with your message. If nothing happens, message us on +357 94426190.',
      openingMail: 'Opening your email app with your message. If nothing happens, email us at ' + MAIL + '.',
      greet: 'Hello P&N Digital,', fName: 'Name', fBiz: 'Business', fType: 'Type of business', fNeed: 'I need', fLangs: 'Languages', subj: 'Website enquiry from ',
      // quote calculator
      pk: ['Starter', 'Business', 'Premium'], price: ['€250', '€450', 'from €750'], from: 'from', startPrice: 'Starting price',
      why: 'Why this package', incl: function (n) { return 'Includes up to ' + n + ' languages of your choice'; },
      r: { size2: 'You need 2–5 pages', size6: 'You need 6 or more pages', l3: 'Business includes up to 3 languages', l5: 'Premium includes up to 5 languages', motion: 'Advanced animations start at Business', integr: 'Integrations start at Premium', base: 'A focused site of one page fits Starter' },
      sep: 'Quoted separately', extraL: function (n) { return n + (n === 1 ? ' extra language' : ' extra languages'); }, integrS: 'Online bookings, payments or integrations (these need an external service)', aiS: 'AI chat assistant',
      maint: 'Plus €50 a month for maintenance (€600 a year)',
      note: 'A provisional starting price, not a quote. The final price is agreed with you after we discuss the scope. Domain and hosting may cost extra.',
      sendWa: 'Send this on WhatsApp', sendMail: 'Send by email', useForm: 'Use the contact form', contact: '/contact/',
      eHead: 'Hi P&N Digital, I used the quote calculator on your website.', eNeed: 'What I need', eSize: 'Size', eLangs: 'Languages', eExtras: 'Extras', eMaint: 'Maintenance', yes: 'yes', no: 'no', none: 'none',
      eEst: 'Estimated starting price', ePlus: 'plus €50 a month for maintenance', eSep: 'Quoted separately', eAsk: 'Could you give me a quote?', eSubj: 'Quote request: '
    },
    el: {
      hello: 'Γεια σας P&N Digital, θα ήθελα πληροφορίες για μια ιστοσελίδα.', waLabel: 'Στείλτε μας μήνυμα στο WhatsApp (ανοίγει το WhatsApp)',
      errName: 'Συμπληρώστε το όνομά σας.', errMsg: 'Γράψτε ένα σύντομο μήνυμα (τουλάχιστον 10 χαρακτήρες).', errSum: 'Ελέγξτε τα επισημασμένα πεδία.',
      openingWa: 'Ανοίγει το WhatsApp με το μήνυμά σας. Αν δεν συμβεί τίποτα, στείλτε μας μήνυμα στο +357 94426190.',
      openingMail: 'Ανοίγει η εφαρμογή email με το μήνυμά σας. Αν δεν συμβεί τίποτα, γράψτε μας στο ' + MAIL + '.',
      greet: 'Γεια σας P&N Digital,', fName: 'Όνομα', fBiz: 'Επιχείρηση', fType: 'Είδος επιχείρησης', fNeed: 'Χρειάζομαι', fLangs: 'Γλώσσες', subj: 'Αίτημα για ιστοσελίδα από ',
      pk: ['Starter', 'Business', 'Premium'], price: ['€250', '€450', 'από €750'], from: 'από', startPrice: 'Τιμή εκκίνησης',
      why: 'Γιατί αυτό το πακέτο', incl: function (n) { return 'Περιλαμβάνει έως ' + n + ' γλώσσες της επιλογής σας'; },
      r: { size2: 'Χρειάζεστε 2–5 σελίδες', size6: 'Χρειάζεστε 6 ή περισσότερες σελίδες', l3: 'Το Business περιλαμβάνει έως 3 γλώσσες', l5: 'Το Premium περιλαμβάνει έως 5 γλώσσες', motion: 'Τα προχωρημένα εφέ κίνησης ξεκινούν από το Business', integr: 'Οι ενσωματώσεις ξεκινούν από το Premium', base: 'Μια εστιασμένη ιστοσελίδα μίας σελίδας ταιριάζει στο Starter' },
      sep: 'Τιμολογούνται ξεχωριστά', extraL: function (n) { return n + (n === 1 ? ' επιπλέον γλώσσα' : ' επιπλέον γλώσσες'); }, integrS: 'Ηλεκτρονικές κρατήσεις, πληρωμές ή ενσωματώσεις (χρειάζονται εξωτερική υπηρεσία)', aiS: 'Βοηθός συνομιλίας AI',
      maint: 'Συν €50 τον μήνα για συντήρηση (€600 τον χρόνο)',
      note: 'Ενδεικτική τιμή εκκίνησης και όχι προσφορά. Η τελική τιμή συμφωνείται μαζί σας αφού συζητήσουμε το πλαίσιο εργασιών. Το domain και η φιλοξενία μπορεί να έχουν επιπλέον κόστος.',
      sendWa: 'Αποστολή μέσω WhatsApp', sendMail: 'Αποστολή με email', useForm: 'Χρήση της φόρμας επικοινωνίας', contact: '/el/contact/',
      eHead: 'Γεια σας P&N Digital, χρησιμοποίησα τον υπολογισμό κόστους στην ιστοσελίδα σας.', eNeed: 'Τι χρειάζομαι', eSize: 'Μέγεθος', eLangs: 'Γλώσσες', eExtras: 'Επιπλέον', eMaint: 'Συντήρηση', yes: 'ναι', no: 'όχι', none: 'κανένα',
      eEst: 'Ενδεικτική τιμή εκκίνησης', ePlus: 'συν €50 τον μήνα για συντήρηση', eSep: 'Τιμολογούνται ξεχωριστά', eAsk: 'Μπορείτε να μου στείλετε προσφορά;', eSubj: 'Αίτημα προσφοράς: '
    }
  };

  // ---------- 1. floating WhatsApp button (every agency page)
  if (!document.querySelector('.wa-float')) {
    var wf = document.createElement('a');
    wf.className = 'wa-float'; wf.target = '_blank'; wf.rel = 'noopener';
    wf.innerHTML = WA_ICON + '<span>WhatsApp</span>';
    document.body.appendChild(wf);
    var paintWa = function () { var t = X[pageLang()]; wf.href = waUrl(t.hello); wf.setAttribute('aria-label', t.waLabel); };
    paintWa();
    new MutationObserver(paintWa).observe(document.documentElement, { attributes: true, attributeFilter: ['lang'] });
  }

  // ---------- 2. contact form: opens WhatsApp or email with the message ready; nothing is sent from here
  function readEstimate() {
    try { var q = new URLSearchParams(location.search).get('estimate'); if (q) return q; } catch (e) { /* old browser */ }
    try { return sessionStorage.getItem('pn-estimate') || ''; } catch (e) { return ''; }
  }
  each('form.cform', function (f) {
    var L = f.dataset.lang === 'el' ? 'el' : 'en', t = X[L], last = 'wa';
    var name = f.elements.name, msg = f.elements.msg, status = f.querySelector('.fstatus');
    var est = readEstimate(); if (est && !msg.value) msg.value = est;
    function setErr(input, text) {
      var e = document.getElementById(input.id + '-err');
      input.setAttribute('aria-invalid', text ? 'true' : 'false');
      if (e) { e.textContent = text || ''; e.hidden = !text; }
    }
    [name, msg].forEach(function (i) { i.addEventListener('input', function () { if (i.getAttribute('aria-invalid') === 'true') validate(false); }); });
    function validate(focus) {
      var bad = [];
      if (name.value.trim().length < 2) { setErr(name, t.errName); bad.push(name); } else setErr(name, '');
      if (msg.value.trim().length < 10) { setErr(msg, t.errMsg); bad.push(msg); } else setErr(msg, '');
      if (focus && bad.length) { bad[0].focus(); status.textContent = t.errSum; status.hidden = false; status.className = 'fstatus bad'; }
      return !bad.length;
    }
    each('button[type=submit]', function (b) { b.addEventListener('click', function () { last = b.value; }); }, f);
    f.addEventListener('submit', function (e) {
      e.preventDefault();
      var via = (e.submitter && e.submitter.value) || last;
      if (!validate(true)) return;
      var v = function (n) { var el = f.elements[n]; if (!el) return ''; if (el.length && !el.tagName) { for (var i = 0; i < el.length; i++) if (el[i].checked) return el[i].value; return ''; } return String(el.value || '').trim(); };
      var lines = [t.greet, '', t.fName + ': ' + v('name')];
      if (v('biz')) lines.push(t.fBiz + ': ' + v('biz'));
      if (v('type')) lines.push(t.fType + ': ' + v('type'));
      if (v('need')) lines.push(t.fNeed + ': ' + v('need'));
      if (v('langs')) lines.push(t.fLangs + ': ' + v('langs'));
      lines.push('', v('msg'));
      var body = lines.join('\n');
      status.className = 'fstatus ok'; status.hidden = false;
      if (via === 'mail') { status.textContent = t.openingMail; (window.PN_NAV || function (u) { location.href = u; })(mailUrl(t.subj + v('name'), body)); } // PN_NAV: lets automated tests see the link
      else { status.textContent = t.openingWa; openWa(waUrl(body)); }
      try { sessionStorage.removeItem('pn-estimate'); } catch (err) { /* ignore */ }
    });
  });

  // ---------- 3. quote calculator (only real, published prices; anything else is "quoted separately")
  function countTo(el, to, prefix) {
    var from = +el.dataset.v || 0; el.dataset.v = to;
    if (RM || from === to) { el.textContent = prefix + to; return; }
    var t0 = performance.now();
    (function tick(now) { var p = Math.min(1, (now - t0) / 500), e = 1 - Math.pow(1 - p, 3); el.textContent = prefix + Math.round(from + (to - from) * e); if (p < 1) requestAnimationFrame(tick); })(t0);
  }
  each('section.quote', function (q) {
    var L = q.dataset.lang === 'el' ? 'el' : 'en', t = X[L], f = q.querySelector('.q-form'), out = q.querySelector('.q-result');
    var langs = 2, out0 = q.querySelector('.st-v');
    out.innerHTML = '<p class="q-pk"></p><p class="q-price"><small class="q-from"></small><span class="q-num">€250</span></p><p class="q-sub"></p>' +
      '<div class="q-why"><p class="q-h"></p><ul></ul></div><div class="q-sep" hidden><p class="q-h"></p><ul></ul></div><p class="q-maint" hidden></p>' +
      '<p class="q-note"></p><div class="q-act"><a class="btn btn-wa q-wa" target="_blank" rel="noopener"></a><a class="btn alt q-mail"></a><a class="q-form-link"></a></div>';
    var $ = function (s) { return out.querySelector(s); };
    $('.q-wa').innerHTML = WA_ICON + '<span></span>'; $('.q-wa span').textContent = t.sendWa; $('.q-mail').textContent = t.sendMail; $('.q-form-link').textContent = t.useForm + ' →';
    $('.q-why .q-h').textContent = t.why; $('.q-sep .q-h').textContent = t.sep; $('.q-note').textContent = t.note;
    function label(name, value) { var i = f.querySelector('input[name="' + name + '"][value="' + value + '"]'); return i ? i.parentNode.textContent.trim() : value; }
    function state() {
      var s = { need: f.querySelector('input[name=need]:checked').value, size: f.querySelector('input[name=size]:checked').value, langs: langs, feats: [], maint: f.elements.maint.checked };
      each('input[name=feat]:checked', function (c) { s.feats.push(c.value); }, f);
      if (s.need === 'landing') s.size = '1';
      return s;
    }
    var text = '';
    function render() {
      var s = state(), lvl = 0, why = [], sep = [];
      q.querySelector('.q-size').disabled = s.need === 'landing';
      // each rule names the package it needs; only the rules that decide the final package are shown as the reason
      var rules = [];
      if (s.size === '2') rules.push([1, t.r.size2]);
      if (s.size === '6') rules.push([2, t.r.size6]);
      if (s.langs === 3) rules.push([1, t.r.l3]);
      if (s.langs >= 4) rules.push([2, t.r.l5]);
      if (s.feats.indexOf('motion') >= 0) rules.push([1, t.r.motion]);
      if (s.feats.indexOf('integr') >= 0) { rules.push([2, t.r.integr]); sep.push(t.integrS); }
      rules.forEach(function (r) { lvl = Math.max(lvl, r[0]); });
      rules.forEach(function (r) { if (r[0] === lvl) why.push(r[1]); });
      if (s.feats.indexOf('ai') >= 0) sep.push(t.aiS);
      if (s.langs > 5) sep.unshift(t.extraL(s.langs - 5));
      if (!why.length) why.push(t.r.base);
      var num = [250, 450, 750][lvl];
      $('.q-pk').textContent = t.pk[lvl];
      $('.q-from').textContent = lvl === 2 ? t.from + ' ' : '';
      countTo($('.q-num'), num, '€');
      $('.q-sub').textContent = t.incl([2, 3, 5][lvl]);
      var wu = $('.q-why ul'); wu.innerHTML = ''; why.forEach(function (w) { var li = document.createElement('li'); li.textContent = w; wu.appendChild(li); });
      var su = $('.q-sep ul'); su.innerHTML = ''; sep.forEach(function (w) { var li = document.createElement('li'); li.textContent = w; su.appendChild(li); });
      $('.q-sep').hidden = !sep.length;
      $('.q-maint').hidden = !s.maint; $('.q-maint').textContent = t.maint;
      out.parentNode.dataset.level = lvl;
      var extras = s.feats.map(function (v) { return label('feat', v); });
      text = [t.eHead, '', t.eNeed + ': ' + label('need', s.need), t.eSize + ': ' + label('size', s.size), t.eLangs + ': ' + s.langs,
        t.eExtras + ': ' + (extras.length ? extras.join(', ') : t.none), t.eMaint + ': ' + (s.maint ? t.yes : t.no), '',
        t.eEst + ': ' + t.pk[lvl] + ' — ' + t.price[lvl] + (s.maint ? ', ' + t.ePlus : '') + '.',
        sep.length ? t.eSep + ': ' + sep.join('; ') + '.' : '', '', t.eAsk].filter(function (x, i, a) { return !(x === '' && a[i - 1] === ''); }).join('\n');
      $('.q-wa').href = waUrl(text);
      $('.q-mail').href = mailUrl(t.eSubj + t.pk[lvl], text);
      var base = t.contact;
      $('.q-form-link').href = window.PN_ASSISTANT_LINK ? window.PN_ASSISTANT_LINK(base, L) : base + '?estimate=' + encodeURIComponent(text);
    }
    $('.q-form-link').addEventListener('click', function (e) {
      if (window.PN_ASSISTANT_LINK) { e.preventDefault(); location.hash = window.PN_ASSISTANT_LINK(t.contact, L); } // single-page test copy
      try { sessionStorage.setItem('pn-estimate', text); } catch (e) { /* ignore */ }
      each('form.cform[data-lang="' + L + '"] textarea[name=msg]', function (m) { m.value = text; }); // single-page test copy
    });
    each('.st-b', function (b) {
      b.addEventListener('click', function () { langs = Math.min(12, Math.max(1, langs + (+b.dataset.step))); out0.textContent = langs; render(); });
    }, q);
    f.addEventListener('change', render);
    render();
  });

  // ---------- 4. wireframe / finished comparison slider
  each('.cmp-box', function (box) {
    var r = box.querySelector('input[type=range]');
    function set(v) { box.style.setProperty('--x', v + '%'); }
    r.addEventListener('input', function () { box.classList.add('touched'); set(r.value); });
    if (RM || !('IntersectionObserver' in window)) return;
    // one gentle sweep the first time it scrolls into view, so people see it moves
    var io = new IntersectionObserver(function (es) {
      if (!es[0].isIntersecting) return; io.disconnect();
      var t0 = performance.now(), keys = [50, 18, 82, 50];
      (function tick(now) {
        if (box.classList.contains('touched')) return;
        var p = Math.min(1, (now - t0) / 2600), seg = Math.min(2, Math.floor(p * 3)), lp = p * 3 - seg, e = lp < .5 ? 2 * lp * lp : 1 - Math.pow(-2 * lp + 2, 2) / 2;
        var v = keys[seg] + (keys[seg + 1] - keys[seg]) * e; set(v); r.value = Math.round(v);
        if (p < 1) requestAnimationFrame(tick);
      })(t0);
    }, { threshold: 0.55 });
    io.observe(box);
  });
})();
