/* P&N Digital assistant widget (shared by every website).
   Load a business pack first, then this file:
     <script src="/assets/assistant/packs/<id>.js"></script>
     <script src="/assets/assistant/assistant.js" data-business="<id>"></script>
   Live mode: the pack has an "endpoint" (the deployed engine) -> answers stream from the AI engine.
   Demo mode: no endpoint, or the engine is not configured -> clearly labelled answers taken only from
   the website's own information. Nothing typed in demo mode leaves the browser. Nothing is stored. */
(function () {
  'use strict';
  var me = document.currentScript;
  var ID = (me && me.getAttribute('data-business')) || window.PN_ASSISTANT_ID;
  var PACK = window.PN_ASSISTANT_PACKS && window.PN_ASSISTANT_PACKS[ID];
  if (!PACK || PACK.enabled === false || document.getElementById('pn-ai-host')) return;
  var K = PACK.knowledge || {}, B = PACK.branding || {};
  var RM = window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches;

  var UI = {
    en: { open: 'Ask our AI assistant', launcher: 'Ask AI', close: 'Close assistant', reset: 'Start a new conversation', badge: 'AI assistant', demo: 'Demo mode',
      demoNote: 'Demo mode: not connected to AI yet. Answers come only from this website’s information, and nothing you type is sent anywhere.',
      liveNote: 'AI answers can be wrong. Please don’t share sensitive information. Messages are sent to the AI service only to answer you and are not stored.',
      input: 'Your message', placeholder: 'Ask a question…', send: 'Send', typing: 'The assistant is typing', demoTag: 'Demo answer · from website information',
      fallback: 'I couldn’t find that in this website’s information, so I won’t guess. You could try one of these questions:', limit: 'This conversation has reached its limit. Start a new one with the ↺ button.',
      busy: 'The assistant is busy right now. Please try again in a moment.', offline: 'You seem to be offline. Please check your connection and try again.',
      error: 'Sorry, something went wrong. Please try again.', notConfigured: 'The AI service isn’t switched on yet, so I’ve switched to demo mode.', slow: 'Please wait a moment before sending another message.',
      daily: 'The assistant has reached today’s limit. Please use the contact options on this website.', you: 'You', bot: 'Assistant',
      identity: 'I’m the website’s assistant. Right now I’m running in demo mode, which means I’m not connected to an AI model: I can only answer from this website’s information.',
      identityLive: 'I’m an AI assistant for this website. I answer from the business’s own information and I can make mistakes.',
      otherLang: 'In the meantime, here are some questions I can answer in English:', planStart: 'Plan my website', restart: 'Start over', go: 'Show me', provisional: 'This is a provisional starting price, not a quote. The final price depends on the agreed scope.' },
    el: { open: 'Ρωτήστε τον βοηθό AI', launcher: 'Ρωτήστε', close: 'Κλείσιμο βοηθού', reset: 'Νέα συζήτηση', badge: 'Βοηθός AI', demo: 'Λειτουργία επίδειξης',
      demoNote: 'Λειτουργία επίδειξης: δεν είναι ακόμη συνδεδεμένος με AI. Οι απαντήσεις βασίζονται μόνο στις πληροφορίες αυτής της ιστοσελίδας και ό,τι γράφετε δεν αποστέλλεται πουθενά.',
      liveNote: 'Οι απαντήσεις AI μπορεί να περιέχουν λάθη. Μη μοιράζεστε ευαίσθητες πληροφορίες. Τα μηνύματα αποστέλλονται στην υπηρεσία AI μόνο για να σας απαντήσει και δεν αποθηκεύονται.',
      input: 'Το μήνυμά σας', placeholder: 'Κάντε μια ερώτηση…', send: 'Αποστολή', typing: 'Ο βοηθός πληκτρολογεί', demoTag: 'Απάντηση επίδειξης · από τις πληροφορίες της ιστοσελίδας',
      fallback: 'Δεν βρήκα κάτι σχετικό στις πληροφορίες αυτής της ιστοσελίδας, οπότε δεν θα μαντέψω. Δοκιμάστε μία από αυτές τις ερωτήσεις:', limit: 'Αυτή η συζήτηση έφτασε στο όριό της. Ξεκινήστε νέα με το κουμπί ↺.',
      busy: 'Ο βοηθός είναι απασχολημένος αυτή τη στιγμή. Δοκιμάστε ξανά σε λίγο.', offline: 'Φαίνεται ότι δεν είστε συνδεδεμένοι. Ελέγξτε τη σύνδεσή σας και δοκιμάστε ξανά.',
      error: 'Συγγνώμη, κάτι πήγε στραβά. Δοκιμάστε ξανά.', notConfigured: 'Η υπηρεσία AI δεν έχει ενεργοποιηθεί ακόμη, οπότε πέρασα σε λειτουργία επίδειξης.', slow: 'Περιμένετε λίγο πριν στείλετε άλλο μήνυμα.',
      daily: 'Ο βοηθός έφτασε το σημερινό όριο. Χρησιμοποιήστε τους τρόπους επικοινωνίας της ιστοσελίδας.', you: 'Εσείς', bot: 'Βοηθός',
      identity: 'Είμαι ο βοηθός της ιστοσελίδας. Αυτή τη στιγμή λειτουργώ σε λειτουργία επίδειξης, δηλαδή δεν είμαι συνδεδεμένος με μοντέλο AI: απαντώ μόνο από τις πληροφορίες αυτής της ιστοσελίδας.',
      identityLive: 'Είμαι βοηθός AI αυτής της ιστοσελίδας. Απαντώ από τις πληροφορίες της επιχείρησης και μπορεί να κάνω λάθη.',
      otherLang: 'Στο μεταξύ, να μερικές ερωτήσεις που μπορώ να απαντήσω στα ελληνικά:', planStart: 'Σχεδιάστε την ιστοσελίδα μου', restart: 'Από την αρχή', go: 'Δείτε το', provisional: 'Πρόκειται για ενδεικτική τιμή εκκίνησης και όχι για προσφορά. Η τελική τιμή εξαρτάται από το συμφωνημένο πλαίσιο εργασιών.' }
  };
  // pageLang(): the page's own language, any code ('en', 'el', 'ru', 'he'...). It is sent to the AI, which can answer in any language.
  // lang(): the language of the widget's built-in texts (Greek or English; a pack can add its own texts for other languages in "ui").
  function pageLang() { return String(document.documentElement.lang || 'en').toLowerCase().split('-')[0]; }
  function lang() { return pageLang() === 'el' ? 'el' : 'en'; }
  function t(k) { var own = PACK.ui && PACK.ui[pageLang()]; return (own && own[k]) || UI[lang()][k]; }
  function L(v) { return v && typeof v === 'object' && !Array.isArray(v) ? (v[lang()] || v.en || '') : (v || ''); }
  function norm(s) { return String(s || '').toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g, '').replace(/ς/g, 'σ').replace(/[^\p{L}\p{N}€+ -]/gu, ' ').replace(/\s+/g, ' ').trim(); }

  // ---------- markup (Shadow DOM keeps the widget's styles separate from each website's styles)
  var host = document.createElement('div'); host.id = 'pn-ai-host'; host.setAttribute('data-no-i18n', '');
  var root = host.attachShadow ? host.attachShadow({ mode: 'open' }) : host;
  var css = ':host{all:initial}*{box-sizing:border-box}[hidden]{display:none!important}' +
    '.w{--a:' + (B.accent || '#0e7c7b') + ';--on:' + (B.onAccent || '#fff') + ';--bg:' + (B.surface || '#fff') + ';--fg:' + (B.text || '#111') + ';--mut:' + (B.muted || '#555') + ';--ln:' + (B.line || '#ddd') + ';font:15px/1.5 ' + (B.font || 'system-ui,sans-serif') + ';color:var(--fg)}' +
    '.launcher{position:fixed;' + (B.position === 'left' ? 'left' : 'right') + ':18px;bottom:18px;z-index:2147483000;display:flex;align-items:center;gap:.5rem;height:52px;padding:0 1.1rem 0 .9rem;border:0;border-radius:26px;background:var(--a);color:var(--on);font:600 15px/1 ' + (B.font || 'system-ui,sans-serif') + ';box-shadow:0 10px 28px rgba(0,0,0,.35);cursor:pointer;transition:transform .25s,box-shadow .25s}' +
    '.launcher:hover{transform:translateY(-2px);box-shadow:0 14px 34px rgba(0,0,0,.4)}.launcher svg{width:22px;height:22px;flex:none}' +
    '.launcher[aria-expanded=true]{transform:scale(.9);opacity:0;pointer-events:none}' +
    ':focus-visible{outline:3px solid var(--a);outline-offset:2px}.launcher:focus-visible{outline-color:var(--fg)}' +
    '.panel{position:fixed;' + (B.position === 'left' ? 'left' : 'right') + ':18px;bottom:18px;z-index:2147483001;width:min(390px,calc(100vw - 24px));height:min(600px,calc(100vh - 36px));display:flex;flex-direction:column;background:var(--bg);color:var(--fg);border:1px solid var(--ln);border-radius:14px;box-shadow:0 24px 60px rgba(0,0,0,.45);overflow:hidden}' +
    '.hd{display:flex;align-items:flex-start;gap:.5rem;padding:.8rem .8rem .7rem 1rem;border-bottom:1px solid var(--ln)}.hd .id{flex:1;min-width:0}.hd strong{display:block;font-size:15px}' +
    '.tags{display:flex;flex-wrap:wrap;gap:.3rem;margin-top:.3rem}.tag{font-size:11px;font-weight:700;letter-spacing:.03em;padding:.1rem .45rem;border-radius:20px;background:var(--a);color:var(--on)}.tag.m{background:transparent;color:var(--fg);border:1px solid var(--ln)}' +
    '.ib{flex:none;width:36px;height:36px;border:1px solid var(--ln);border-radius:8px;background:transparent;color:var(--fg);font-size:17px;cursor:pointer}.ib:hover{border-color:var(--a)}' +
    '.note{margin:0;padding:.55rem 1rem;font-size:12px;color:var(--mut);border-bottom:1px solid var(--ln)}' +
    '.log{flex:1;overflow-y:auto;padding:1rem;display:flex;flex-direction:column;gap:.7rem;overscroll-behavior:contain}' +
    '.msg{max-width:88%;padding:.6rem .8rem;border-radius:12px;white-space:pre-wrap;overflow-wrap:anywhere}.msg.bot{align-self:flex-start;background:rgba(127,127,127,.12)}.msg.me{align-self:flex-end;background:var(--a);color:var(--on)}' +
    '.msg .src{display:block;margin-top:.35rem;font-size:11px;color:var(--mut)}.msg ul{margin:.3rem 0 0;padding-left:1.1rem}.msg li{margin:.15rem 0}' +
    '.act{display:inline-block;margin-top:.5rem;padding:.4rem .75rem;border-radius:8px;background:var(--a);color:var(--on);font-weight:600;font-size:13px;text-decoration:none}' +
    '.chips{display:flex;flex-wrap:nowrap;gap:.4rem;padding:.1rem 1rem .6rem;overflow-x:auto;scrollbar-width:thin;scroll-snap-type:x proximity}.chip{flex:none;white-space:nowrap;scroll-snap-align:start;font:inherit;font-size:13px;color:var(--fg);background:transparent;border:1px solid var(--ln);border-radius:16px;padding:.4rem .75rem;cursor:pointer;text-align:left;transition:border-color .2s,background .2s}.chip:hover{border-color:var(--a)}' +
    '.typing{align-self:flex-start;padding:.7rem .9rem;border-radius:12px;background:rgba(127,127,127,.12)}.typing i{display:inline-block;width:7px;height:7px;margin:0 2px;border-radius:50%;background:var(--mut);animation:b 1.1s infinite}.typing i:nth-child(2){animation-delay:.15s}.typing i:nth-child(3){animation-delay:.3s}' +
    '@keyframes b{0%,80%,100%{opacity:.3;transform:translateY(0)}40%{opacity:1;transform:translateY(-3px)}}' +
    '.f{display:flex;gap:.5rem;padding:.7rem .8rem;border-top:1px solid var(--ln)}.f textarea{flex:1;resize:none;font:inherit;color:var(--fg);background:transparent;border:1px solid var(--ln);border-radius:10px;padding:.55rem .7rem;max-height:120px;min-height:44px}.f textarea:focus{border-color:var(--a);outline:none}' +
    '.f button{flex:none;width:44px;height:44px;border:0;border-radius:10px;background:var(--a);color:var(--on);font-size:18px;cursor:pointer}.f button[disabled]{opacity:.45;cursor:not-allowed}' +
    '.sr{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap}' +
    '@media(max-width:600px){.launcher .lbl{display:none}.launcher{width:52px;padding:0;justify-content:center}.panel{left:0;right:0;bottom:0;width:100%;height:min(88vh,100%);border-radius:14px 14px 0 0}}' +
    (RM ? '*{transition:none!important;animation:none!important}' : '.panel{animation:up .28s cubic-bezier(.2,.7,.2,1)}@keyframes up{from{opacity:0;transform:translateY(14px) scale(.98)}}.msg{animation:in .25s ease}@keyframes in{from{opacity:0;transform:translateY(6px)}}');
  root.innerHTML = '<style>' + css + '</style><div class="w">' +
    '<button class="launcher" type="button" aria-expanded="false" aria-controls="pn-ai-panel"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M21 12a8 8 0 0 1-11.6 7.1L4 20l1-4.6A8 8 0 1 1 21 12z"/><path d="M8.5 11h.01M12 11h.01M15.5 11h.01" stroke-width="3" stroke-linecap="round"/></svg><span class="lbl"></span></button>' +
    '<section class="panel" id="pn-ai-panel" role="dialog" aria-modal="false" aria-labelledby="pn-ai-title" hidden>' +
    '<div class="hd"><div class="id"><strong id="pn-ai-title"></strong><div class="tags"><span class="tag ai"></span><span class="tag m mode"></span></div></div>' +
    '<button class="ib reset" type="button">↺</button><button class="ib x" type="button">×</button></div>' +
    '<p class="note"></p><div class="log" role="log" aria-live="polite" aria-relevant="additions"></div><div class="chips"></div>' +
    '<form class="f"><label class="sr" for="pn-ai-in"></label><textarea id="pn-ai-in" rows="1" maxlength="800"></textarea><button type="submit">➤</button></form></section></div>';
  document.body.appendChild(host);
  var pad = document.createElement('style'); pad.textContent = '@media(max-width:760px){body{padding-bottom:84px!important}}'; document.head.appendChild(pad); // keep page controls reachable above the launcher

  var $ = function (s) { return root.querySelector(s); };
  var launcher = $('.launcher'), panel = $('.panel'), log = $('.log'), chips = $('.chips'), form = $('.f'), input = $('textarea'), sendBtn = $('.f button');
  var mode = PACK.endpoint ? 'live' : 'demo', history = [], busy = false, flow = null;

  function paint() {
    launcher.setAttribute('aria-label', t('open')); $('.lbl').textContent = t('launcher');
    $('#pn-ai-title').textContent = L(PACK.assistant.name); $('.tag.ai').textContent = t('badge');
    $('.mode').textContent = t('demo'); $('.mode').hidden = mode !== 'demo';
    $('.note').textContent = mode === 'demo' ? t('demoNote') : (PACK.assistant.liveNote ? L(PACK.assistant.liveNote) : t('liveNote')); // a business can describe its own AI service honestly
    $('.reset').setAttribute('aria-label', t('reset')); $('.reset').title = t('reset');
    $('.x').setAttribute('aria-label', t('close')); $('.x').title = t('close');
    $('label').textContent = t('input'); input.placeholder = t('placeholder'); sendBtn.setAttribute('aria-label', t('send'));
    if (!history.length && !flow) suggestions();
  }
  function el(tag, cls, text) { var e = document.createElement(tag); if (cls) e.className = cls; if (text != null) e.textContent = text; return e; }
  function scroll() { log.scrollTop = log.scrollHeight; }
  function add(role, text, extra) {
    var m = el('div', 'msg ' + (role === 'user' ? 'me' : 'bot'));
    var sr = el('span', 'sr', (role === 'user' ? t('you') : t('bot')) + ': '); m.appendChild(sr);
    var body = el('span', 'tx'); body.dir = 'auto'; body.textContent = text || ''; m.appendChild(body); // 'auto' shows Hebrew or Arabic right-to-left
    if (extra && extra.lang) { m.lang = extra.lang; m.dir = extra.dir || 'auto'; }
    if (extra && extra.list) { var ul = el('ul'); extra.list.forEach(function (x) { ul.appendChild(el('li', null, x)); }); m.appendChild(ul); }
    if (extra && extra.link) { m.appendChild(document.createElement('br')); m.appendChild(linkEl(extra.link, extra.linkLabel)); }
    if (extra && extra.demo) m.appendChild(el('span', 'src', t('demoTag')));
    log.appendChild(m); scroll(); return body;
  }
  function linkEl(href, label) {
    var a = el('a', 'act', label || t('go'));
    var target = window.PN_ASSISTANT_LINK ? window.PN_ASSISTANT_LINK(href, lang()) : (lang() === 'el' && href.charAt(0) === '/' && href.indexOf('/el/') !== 0 ? '/el' + href : href);
    a.href = target;
    a.addEventListener('click', function (e) { if (target.charAt(0) === '#') { e.preventDefault(); location.hash = target; if (matchMedia('(max-width:600px)').matches) close(); } });
    return a;
  }
  function setChips(list, onPick) {
    chips.innerHTML = '';
    list.forEach(function (c) { var b = el('button', 'chip', typeof c === 'string' ? c : c.label); b.type = 'button'; b.addEventListener('click', function () { onPick(c); }); chips.appendChild(b); });
    chips.scrollLeft = 0; scroll();
  }
  function suggestions() {
    var s = (PACK.assistant.suggestions && PACK.assistant.suggestions[lang()]) || [];
    setChips(s, function (q) { if (PACK.assistant.guidedFlow && q === s[0] && mode === 'demo') startFlow(); else ask(q); });
  }
  function welcome() { add('bot', L(PACK.assistant.welcome)); }
  function open() { panel.hidden = false; launcher.setAttribute('aria-expanded', 'true'); if (!log.childNodes.length) welcome(); paint(); setTimeout(function () { input.focus(); }, 30); }
  function close() { panel.hidden = true; launcher.setAttribute('aria-expanded', 'false'); launcher.focus(); }
  function reset() { history = []; flow = null; busy = false; log.innerHTML = ''; welcome(); paint(); input.focus(); }

  // ---------- demo mode: answers only from the public pack
  function has(text, words) { return words.some(function (w) { return text.indexOf(norm(w)) >= 0; }); }
  function demoAnswer(q) {
    var n = norm(q), lg = lang(), r;
    if (/^(hi|hello|hey|γεια|καλησπερα|καλημερα|γεια σασ)\b/.test(n) && n.split(' ').length <= 3) return { text: L(PACK.assistant.welcome) };
    if (/\b(are|r) (you|u) (an? )?(real|human|person|bot|robot|ai|machine|chatbot)\b|\bwho are you\b|\bwhat are you\b|εισαι (ενα |ενασ )?(ai|ανθρωπ|ρομποτ|πραγματικ|μηχανη|bot)|ποιοσ εισαι|τι εισαι/.test(n)) return { text: t(mode === 'demo' ? 'identity' : 'identityLive') };
    var f0 = faqMatch(n);
    if (f0 && f0.score >= 2) return { text: L(f0.f.a), link: f0.f.link }; // a strong FAQ match (two or more keywords) wins over generic lists
    if ((r = menuAnswer(n, lg))) return r;
    if ((r = serviceAnswer(n, lg))) return r;
    if (f0) return { text: L(f0.f.a), link: f0.f.link };
    return null;
  }
  function faqMatch(n) {
    var best = null, bestScore = 0;
    (K.faqs || []).forEach(function (f) {
      var s = 0; (f.keywords || []).forEach(function (k) { var kk = norm(k); if (!kk) return; var hit = (' ' + n + ' ').indexOf(kk.length < 4 ? ' ' + kk + ' ' : kk) >= 0;
        if (!hit && kk.length >= 6 && kk.indexOf(' ') < 0) hit = n.indexOf(kk.slice(0, Math.max(5, kk.length - 2))) >= 0; // Greek and English word endings change: match the stem
        if (hit) s += kk.indexOf(' ') > 0 ? 2 : 1; });
      if (s > bestScore) { bestScore = s; best = f; }
    });
    return best ? { f: best, score: bestScore } : null;
  }
  function labelName(l, lg) { return ({ vegan: { en: 'vegan', el: 'βίγκαν' }, vegetarian: { en: 'vegetarian', el: 'χορτοφαγικό' }, 'gluten-free': { en: 'gluten-free', el: 'χωρίς γλουτένη' } })[l][lg]; }
  function menuAnswer(n, lg) {
    var M = K.menu; if (!M) return null;
    var D = M.dishes, note = lg === 'el' ? 'Οι σημάνσεις είναι ενδεικτικές· για αλλεργίες ρωτήστε ένα πραγματικό εστιατόριο.' : 'Labels are samples; for allergies, check with a real restaurant.';
    function line(d) { return L(d.name) + ' — ' + d.price; }
    if (has(n, ['allerg', 'nut', 'celiac', 'coeliac', 'αλλεργ', 'ξηρ'])) return null; // the allergy FAQ answers carefully
    var want = has(n, ['vegan', 'βιγκαν', 'vegan']) ? 'vegan' : has(n, ['vegetarian', 'veggie', 'χορτοφαγ']) ? 'vegetarian' : has(n, ['gluten', 'γλουτεν']) ? 'gluten-free' : null;
    if (want) { var l = D.filter(function (d) { return d.labels.indexOf(want) >= 0; }); return { text: (lg === 'el' ? 'Πιάτα με την ένδειξη «' + labelName(want, lg) + '» σε αυτό το μενού επίδειξης (' + l.length + '):' : 'Dishes labelled ' + labelName(want, lg) + ' on this demo menu (' + l.length + '):'), list: l.map(line).concat([note]), link: '#menu' }; }
    if (has(n, ['recommend', 'suggest', 'signature', 'best', 'popular', 'chef', 'προτειν', 'προταση', 'καλυτερ', 'σεφ', 'δημοφιλ'])) { var s = D.filter(function (d) { return d.tags.indexOf('sig') >= 0 || d.tags.indexOf('chef') >= 0; }); return { text: lg === 'el' ? 'Χαρακτηριστικά πιάτα και προτάσεις του σεφ (δείγμα):' : 'Signature dishes and chef’s picks (sample menu):', list: s.map(line), link: '#menu' }; }
    var CAT = { starters: ['starter', 'appetizer', 'ορεκτικ'], mains: ['main', 'κυριως'], seafood: ['seafood', 'fish', 'θαλασσιν', 'ψαρι'], pasta: ['pasta', 'ζυμαρικ', 'μακαρον'], desserts: ['dessert', 'sweet', 'επιδορπ', 'γλυκ'], drinks: ['drink', 'coffee', 'ποτα', 'ποτο', 'ποτου', 'καφε'] };
    for (var c in CAT) if (has(n, CAT[c])) { var cl = D.filter(function (d) { return d.category === c; }); return { text: (lg === 'el' ? 'Στο μενού επίδειξης:' : 'On the demo menu:'), list: cl.map(line), link: '#menu' }; }
    var hit = D.filter(function (d) { return [L(d.name), d.name.en].some(function (nm) { return norm(nm).split(',')[0].split(' ').filter(function (w) { return w.length > 4; }).some(function (w) { return n.indexOf(w) >= 0; }); }); });
    if (hit.length === 1) { var d = hit[0]; return { text: L(d.name) + ' — ' + d.price + '\n' + L(d.description) + (d.labels.length ? '\n' + d.labels.map(function (x) { return labelName(x, lg); }).join(', ') : '') + '\n' + note }; }
    if (has(n, ['menu', 'μενου', 'dishes', 'πιατα', 'food', 'φαγητ'])) return { text: lg === 'el' ? 'Το μενού επίδειξης έχει ορεκτικά, κυρίως πιάτα, θαλασσινά, ζυμαρικά, επιδόρπια και ποτά (' + D.length + ' πιάτα).' : 'The demo menu has starters, mains, seafood, pasta, desserts and drinks (' + D.length + ' dishes).', link: '#menu' };
    return null;
  }
  function serviceAnswer(n, lg) {
    var S = K.services, A = K.addons || [], P = K.pricing, BB = K.barbers;
    if (BB && has(n, ['barber', 'κουρεα', 'κουρεισ', 'κουρεων'])) {
      var pickB = has(n, ['beard', 'shave', 'γενει', 'ξυρισ']) ? 'nikos' : has(n, ['kid', 'child', 'son', 'παιδ', 'γιο']) ? 'eleni' : has(n, ['fade', 'taper', 'φειντ', 'ντεγκραντε']) ? 'andreas' : null;
      if (pickB) { var b = BB.filter(function (x) { return x.id === pickB; })[0]; return { text: (lg === 'el' ? 'Ταιριάζει: ' : 'A good match: ') + L(b.name) + ' — ' + L(b.specialty) + '. ' + L(b.bio) + (lg === 'el' ? ' (Φανταστικό προφίλ επίδειξης.)' : ' (Fictional demo profile.)'), link: '#book' }; }
      return { text: lg === 'el' ? 'Οι κουρείς (φανταστικά προφίλ):' : 'Our barbers (fictional profiles):', list: BB.map(function (x) { return L(x.name) + ' — ' + L(x.specialty); }), link: '#barbers' };
    }
    if (S && S[0] && S[0].price) {
      var hit = S.concat(A).filter(function (s) { var nm = norm(L(s.name)), en = norm(s.name.en); return n.indexOf(nm) >= 0 || n.indexOf(en) >= 0 || nm.split(' ').concat(en.split(' ')).filter(function (w) { return w.length > 4 && ['haircut', 'κουρεμα'].indexOf(w) < 0; }).some(function (w) { return n.indexOf(w) >= 0; }); });
      if (hit.length) return { text: lg === 'el' ? 'Από τις υπηρεσίες επίδειξης:' : 'From the demo services:', list: hit.map(function (s) { return L(s.name) + ' — ' + s.price + ' · ' + s.minutes + (lg === 'el' ? ' λεπτά' : ' min'); }), link: '#book' };
      if (has(n, ['service', 'price', 'cost', 'how much', 'how long', 'υπηρεσ', 'τιμ', 'κοστιζ', 'ποσο'])) return { text: lg === 'el' ? 'Υπηρεσίες επίδειξης (ενδεικτικές τιμές και διάρκειες):' : 'Demo services (sample prices and durations):', list: S.map(function (s) { return L(s.name) + ' — ' + s.price + ' · ' + s.minutes + (lg === 'el' ? ' λεπτά' : ' min'); }), link: '#services' };
    }
    if (S && S[0] && S[0].summary) {
      var hs = S.filter(function (s) { return norm(L(s.name)).split(' ').concat(norm(s.name.en).split(' ')).filter(function (w) { return w.length > 5; }).some(function (w) { return n.indexOf(w) >= 0; }); });
      if (hs.length === 1) return { text: L(hs[0].name) + ': ' + L(hs[0].summary), link: '#services' };
      if (has(n, ['service', 'fit', 'help with', 'offer', 'υπηρεσ', 'ταιριαζ', 'προσφερ', 'βοηθ'])) return { text: lg === 'el' ? 'Οι υπηρεσίες (δείγμα). Πείτε μου λίγα λόγια για την επιχείρησή σας και ποιος είναι ο στόχος σας, ή κάντε ένα αίτημα:' : 'The services (sample). Tell me a little about your business and your goal, or make an enquiry:', list: S.map(function (s) { return L(s.name) + ' — ' + L(s.summary); }), link: '#enquire' };
    }
    if (P && P.packages && has(n, ['package', 'which plan', 'πακετο', 'ποιο πακετο'])) return { text: lg === 'el' ? 'Τα πακέτα (ενδεικτικές τιμές εκκίνησης):' : 'The packages (provisional starting prices):', list: P.packages.map(function (p) { return p.name + ' — ' + L(p.price); }).concat([t('provisional')]), link: '/#pricing' };
    if (S && typeof S[0] === 'string' && has(n, ['service', 'offer', 'what do you do', 'build', 'υπηρεσ', 'προσφερ', 'τι κανετε', 'φτιαχν'])) return { text: lg === 'el' ? 'Η P&N Digital προσφέρει σχεδιασμό και κατασκευή ιστοσελίδων, ανανεώσεις, landing pages, βασικό SEO, συντήρηση και πολύγλωσσες ιστοσελίδες σε όποια γλώσσα χρειάζεστε.' : 'P&N Digital offers:', list: lg === 'el' ? null : S, link: '/services/' };
    return null;
  }
  // P&N guided website plan (demo mode). Nothing is sent: it only summarises and points to the contact page.
  var FLOW = [
    { k: 'type', q: { en: 'What kind of business do you have?', el: 'Τι είδους επιχείρηση έχετε;' }, o: { en: ['Restaurant or café', 'Barbershop or salon', 'Hotel or tourism', 'Shop', 'Professional services', 'Something else'], el: ['Εστιατόριο ή καφέ', 'Κουρείο ή κομμωτήριο', 'Ξενοδοχείο ή τουρισμός', 'Κατάστημα', 'Επαγγελματικές υπηρεσίες', 'Κάτι άλλο'] } },
    { k: 'need', q: { en: 'What do you need?', el: 'Τι χρειάζεστε;' }, o: { en: ['A new website', 'A redesign of my current site', 'One landing page'], el: ['Νέα ιστοσελίδα', 'Ανανέωση της τωρινής μου', 'Μία σελίδα προορισμού'] } },
    { k: 'size', q: { en: 'How big should it be?', el: 'Πόσο μεγάλη θέλετε να είναι;' }, o: { en: ['One page', 'A few pages (2–5)', 'Many pages or something custom'], el: ['Μία σελίδα', 'Λίγες σελίδες (2–5)', 'Πολλές σελίδες ή κάτι ειδικό'] } },
    { k: 'feature', q: { en: 'Which feature matters most?', el: 'Ποια λειτουργία είναι πιο σημαντική;' }, o: { en: ['Menu or services list', 'Booking or enquiry flow', 'Photo gallery', 'Not sure yet'], el: ['Μενού ή λίστα υπηρεσιών', 'Κρατήσεις ή αιτήματα', 'Γκαλερί φωτογραφιών', 'Δεν είμαι σίγουρος/η'] } },
    { k: 'langs', q: { en: 'Which languages?', el: 'Σε ποιες γλώσσες;' }, o: { en: ['Greek', 'English', 'Greek and English', 'Three or more languages'], el: ['Ελληνικά', 'Αγγλικά', 'Ελληνικά και αγγλικά', 'Τρεις ή περισσότερες γλώσσες'] } }];
  function startFlow() { flow = { i: 0, a: {} }; chips.innerHTML = ''; add('user', t('planStart')); stepFlow(); }
  function stepFlow() {
    var s = FLOW[flow.i]; add('bot', L(s.q), { demo: true });
    setChips(s.o[lang()].map(function (label, idx) { return { label: label, idx: idx }; }), function (c) {
      add('user', c.label); flow.a[s.k] = c.idx; flow.i++;
      if (flow.i < FLOW.length) stepFlow(); else finishFlow();
    });
  }
  function finishFlow() {
    var a = flow.a, lg = lang(), P = (K.pricing && K.pricing.packages) || [];
    var pkg = (a.feature === 1 || a.size === 2) ? 2 : (a.size === 0 || a.need === 2) ? 0 : 1;
    if (a.langs === 3 && pkg === 0) pkg = 1; // Starter includes up to 2 languages, Business up to 3, Premium up to 5
    var p = P[pkg] || { name: '', price: '' }; var price = L(p.price);
    var sum = FLOW.map(function (s) { return L(s.q).replace(/[?;]$/, '') + ': ' + s.o[lg][a[s.k]]; });
    var extra = a.feature === 1 ? (lg === 'el' ? 'Οι πραγματικές κρατήσεις συχνά χρειάζονται εξωτερική υπηρεσία· αυτό συζητείται και τιμολογείται ξεχωριστά.' : 'Real bookings often need an external service; that is discussed and priced separately.') : '';
    if (a.langs === 3) extra = (extra ? extra + '\n' : '') + (lg === 'el' ? 'Γλώσσες: το Business περιλαμβάνει έως 3 και το Premium έως 5, όποιες επιλέξετε· περισσότερες τιμολογούνται ξεχωριστά.' : 'Languages: Business includes up to 3 and Premium up to 5, all of your choosing; more are quoted separately.');
    add('bot', (lg === 'el' ? 'Σύνοψη των αναγκών σας:' : 'Here’s a summary of what you need:'), { list: sum, demo: true });
    add('bot', (lg === 'el' ? 'Ενδεικτική αφετηρία: ' : 'Suggested starting point: ') + p.name + ' (' + price + '). ' + t('provisional') + (extra ? '\n' + extra : '') + '\n' + (lg === 'el' ? 'Επόμενο βήμα: στείλτε αυτή τη σύνοψη μέσω της σελίδας επικοινωνίας. Τίποτα δεν έχει σταλεί από αυτή τη συζήτηση.' : 'Next step: share this summary through the contact page. Nothing has been sent from this chat.'),
      { link: '/contact/', linkLabel: lg === 'el' ? 'Σελίδα επικοινωνίας' : 'Contact page', demo: true });
    flow = null; setChips([{ label: t('restart') }], function () { startFlow(); });
  }

  // ---------- sending
  function ask(text) {
    text = String(text || '').trim(); if (!text || busy) return;
    if (history.filter(function (m) { return m.role === 'user'; }).length >= 20) { add('bot', t('limit')); return; }
    flow = null; chips.innerHTML = '';
    add('user', text); history.push({ role: 'user', content: text }); input.value = ''; grow();
    if (mode === 'demo') return demoReply(text);
    liveReply();
  }
  function typing(on) {
    var e = root.querySelector('.typing'); if (e) e.remove();
    if (on) { e = el('div', 'typing'); e.setAttribute('role', 'status'); e.innerHTML = '<span class="sr"></span><i></i><i></i><i></i>'; e.firstChild.textContent = t('typing'); log.appendChild(e); scroll(); }
  }
  // Demo mode only knows the website's Greek and English texts. If a visitor writes in another language,
  // say so honestly in their language: with real AI switched on, the assistant replies in any language.
  var OTHER = {
    ru: { d: 'ltr', t: 'Это демо-версия, поэтому здесь я отвечаю только на английском и греческом. Когда AI-ассистент будет включён, он будет отвечать на вашем языке.' },
    uk: { d: 'ltr', t: 'Це демоверсія, тому тут я відповідаю лише англійською та грецькою. Коли AI-асистента буде увімкнено, він відповідатиме вашою мовою.' },
    he: { d: 'rtl', t: 'זו גרסת הדגמה, ולכן כאן אני עונה רק באנגלית וביוונית. כשהעוזר מבוסס הבינה המלאכותית יופעל, הוא יענה בשפה שלך.' },
    ar: { d: 'rtl', t: 'هذه نسخة تجريبية، لذلك أجيب هنا بالإنجليزية واليونانية فقط. عند تشغيل المساعد الذكي سيجيب بلغتك.' },
    tr: { d: 'ltr', t: 'Bu bir demo sürümüdür; bu yüzden burada yalnızca İngilizce ve Yunanca yanıt verebiliyorum. Yapay zekâ asistanı açıldığında sizin dilinizde yanıt verecek.' },
    zh: { d: 'ltr', t: '这是演示版，所以这里我只能用英语和希腊语回答。启用 AI 助手后，它会用您的语言回答。' },
    ja: { d: 'ltr', t: 'これはデモ版のため、ここでは英語とギリシャ語でのみお答えします。AIアシスタントを有効にすると、あなたの言語でお答えします。' }
  };
  function detectOther(s) {
    if (/[\u0590-\u05FF]/.test(s)) return 'he';
    if (/[\u0600-\u06FF]/.test(s)) return 'ar';
    if (/[\u3040-\u30FF]/.test(s)) return 'ja';
    if (/[\u4E00-\u9FFF]/.test(s)) return 'zh';
    if (/[іїєґІЇЄҐ]/.test(s)) return 'uk';
    if (/[\u0400-\u04FF]/.test(s)) return 'ru';
    if (/[ğşıİĞŞ]/.test(s)) return 'tr';
    return null;
  }
  function demoReply(text) {
    busy = true; sendBtn.disabled = true; typing(true);
    setTimeout(function () {
      typing(false); busy = false; sendBtn.disabled = false;
      var other = detectOther(text);
      if (other && other !== pageLang()) {
        add('bot', OTHER[other].t, { lang: other, dir: OTHER[other].d, demo: true });
        add('bot', t('otherLang'), { demo: true }); history.push({ role: 'assistant', content: OTHER[other].t });
        suggestions(); return;
      }
      var r = demoAnswer(text);
      if (r) { add('bot', r.text, { list: r.list, link: r.link, demo: true }); history.push({ role: 'assistant', content: r.text }); }
      else { add('bot', t('fallback') + (PACK.contactFallback ? '\n' + L(PACK.contactFallback) : ''), { demo: true }); }
      suggestions();
    }, RM ? 50 : 450);
  }
  function liveReply() {
    busy = true; sendBtn.disabled = true; typing(true);
    if (navigator.onLine === false) { typing(false); add('bot', t('offline')); history.pop(); busy = false; sendBtn.disabled = false; return; }
    var ctrl = new AbortController(), timer = setTimeout(function () { ctrl.abort(); }, 30000), body = null, got = '';
    fetch(PACK.endpoint, { method: 'POST', headers: { 'content-type': 'application/json' }, signal: ctrl.signal, body: JSON.stringify({ business: PACK.id, lang: pageLang(), messages: history.slice(-12) }) })
      .then(function (res) {
        if (!res.ok) return res.json().catch(function () { return {}; }).then(function (j) { throw { status: res.status, code: j.error }; });
        var reader = res.body.getReader(), dec = new TextDecoder(), buf = '';
        function pump() {
          return reader.read().then(function (r) {
            if (r.done) return;
            buf += dec.decode(r.value, { stream: true }); var i;
            while ((i = buf.indexOf('\n\n')) >= 0) {
              var line = buf.slice(0, i); buf = buf.slice(i + 2);
              if (line.indexOf('data:') !== 0) continue;
              var ev; try { ev = JSON.parse(line.slice(5)); } catch (e) { continue; }
              if (ev.t) { if (!body) { typing(false); body = add('bot', ''); } got += ev.t; body.textContent = got; scroll(); }
              if (ev.error) throw { code: ev.error };
            }
            return pump();
          });
        }
        return pump();
      })
      .then(function () { if (!got) throw { code: 'empty' }; history.push({ role: 'assistant', content: got }); })
      .catch(function (e) {
        typing(false);
        var code = e && e.code, status = e && e.status;
        if (code === 'not_configured') { mode = 'demo'; paint(); add('bot', t('notConfigured')); var q = history[history.length - 1]; if (q && q.role === 'user') { busy = false; sendBtn.disabled = false; return demoReply(q.content); } }
        else add('bot', code === 'busy' ? t('busy') : code === 'slow_down' ? t('slow') : code === 'daily_limit' ? t('daily') : (status === 0 || code === 'timeout' || (e && e.name === 'AbortError') || (e instanceof TypeError)) ? t('offline') : t('error'));
        if (!got && history.length && history[history.length - 1].role === 'user') history.pop();
      })
      .then(function () { clearTimeout(timer); busy = false; sendBtn.disabled = false; suggestions(); });
  }
  function grow() { input.style.height = 'auto'; input.style.height = Math.min(input.scrollHeight, 120) + 'px'; }

  launcher.addEventListener('click', open);
  $('.x').addEventListener('click', close);
  $('.reset').addEventListener('click', reset);
  form.addEventListener('submit', function (e) { e.preventDefault(); ask(input.value); });
  input.addEventListener('keydown', function (e) { if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); ask(input.value); } });
  input.addEventListener('input', grow);
  root.addEventListener('keydown', function (e) { if (e.key === 'Escape' && !panel.hidden) { e.stopPropagation(); close(); } });
  new MutationObserver(paint).observe(document.documentElement, { attributes: true, attributeFilter: ['lang'] });
  paint();
  window.PN_ASSISTANT = { open: open, close: close, mode: function () { return mode; }, ask: ask };
})();
