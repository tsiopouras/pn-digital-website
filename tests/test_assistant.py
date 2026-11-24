import os, sys, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[1]          # the repository folder
SITE = str(ROOT / 'public')                                   # the website
AI = os.environ.get('PN_AI_ASSISTANT_DIR', str(ROOT.parent / 'pn-digital-ai-assistant'))  # the engine repo, cloned next to this one
OUT = ROOT / 'tests' / 'output'; OUT.mkdir(exist_ok=True)
PY = sys.executable
import subprocess, time, json, re
from playwright.sync_api import sync_playwright
SITE_PORT, ENG, ENG_NOKEY = '9161', '9162', '9163'
srv = subprocess.Popen([PY, '-m', 'http.server', SITE_PORT, '--directory', SITE], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
O = f'http://127.0.0.1:{SITE_PORT}'
eng = subprocess.Popen(['node', AI + '/engine/test/mock-server.mjs', ENG, O], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
eng2 = subprocess.Popen(['node', AI + '/engine/test/mock-server.mjs', ENG_NOKEY, O, 'nokey'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
time.sleep(1.5); R = []
def chk(n, ok, d=''):
    R.append((n, bool(ok), str(d)[:220]))
    if not ok: print('FAIL:', n, '|', str(d)[:220])
SH = lambda sel: f"document.getElementById('pn-ai-host').shadowRoot.querySelector({json.dumps(sel)})"
def txt(p, sel): return p.evaluate(f"({SH(sel)}||{{}}).textContent||''")
def bot_last(p): return p.evaluate("(()=>{const m=[...document.getElementById('pn-ai-host').shadowRoot.querySelectorAll('.msg.bot')];return m.length?m[m.length-1].textContent.replace(/^(Assistant|Βοηθός): /,''):''})()")
def nbot(p): return p.evaluate("document.getElementById('pn-ai-host').shadowRoot.querySelectorAll('.msg.bot').length")
def ask(p, q, wait=900):
    n0 = nbot(p); host = p.locator('#pn-ai-host'); host.locator('textarea').fill(q); host.locator('textarea').press('Enter')
    for _ in range(40):
        p.wait_for_timeout(100)
        if nbot(p) > n0 and not p.evaluate(f"!!{SH('.typing')}"): break
    p.wait_for_timeout(150); return bot_last(p)
def openw(p): p.locator('#pn-ai-host .launcher').click(); p.wait_for_timeout(350)
CASES = [  # page, lang, question, must contain (any of), must not contain
 ('/', 'en', 'How much does a website cost?', ['€250', '€450', '€750'], []),
 ('/', 'en', 'Can my website be in Greek and English?', ['any language your customers speak'], []),
 ('/', 'en', 'Can you build my site in Russian and Hebrew?', ['right-to-left', 'Starter includes up to 2'], []),
 ('/el/', 'el', 'Μπορείτε να φτιάξετε την ιστοσελίδα στα ρωσικά;', ['όποια γλώσσα', 'έως 2 γλώσσες'], []),
 ('/', 'en', 'Who is behind P&N Digital?', ['one person'], []),
 ('/', 'en', 'What is the capital of France?', ['won’t guess'], ['Paris']),
 ('/', 'en', 'Are you a real person?', ['demo mode'], []),
 ('/el/', 'el', 'Πόσο κοστίζει μια ιστοσελίδα;', ['€250', '€450'], []),
 ('/el/', 'el', 'Πόσο χρόνο χρειάζεται;', ['Εξαρτάται'], []),
 ('/el/', 'el', 'Πώς επικοινωνώ μαζί σας;', ['σελίδα επικοινωνίας'], []),
 ('/el/', 'el', 'Κάνετε συντήρηση;', ['€50'], []),
 ('/demos/olive-and-oak/?lang=el', 'el', 'Πότε είστε ανοιχτά;', ['Τρίτη έως Κυριακή'], []),
 ('/demos/olive-and-oak/', 'en', 'What vegan dishes do you have?', ['Hummus', 'Spaghetti', 'Labels are samples'], ['Grilled halloumi']),
 ('/demos/olive-and-oak/', 'en', 'Is the halloumi safe for a nut allergy?', ['can’t give allergy'], []),
 ('/demos/olive-and-oak/', 'en', 'When are you open?', ['Tuesday to Sunday'], []),
 ('/demos/olive-and-oak/?lang=el', 'el', 'Ποια βίγκαν πιάτα έχετε;', ['Χούμους', 'ενδεικτικές'], []),
 ('/demos/olive-and-oak/?lang=el', 'el', 'Τι προτείνετε;', ['Χαλλούμι'], []),
 ('/demos/the-cut/', 'en', 'How much is a skin fade?', ['€18', '40 min'], []),
 ('/demos/the-cut/', 'en', 'Which barber is best for beards?', ['Nikos'], []),
 ('/demos/the-cut/', 'en', 'Do you take walk-ins?', ['walk-ins could be welcome'], []),
 ('/demos/the-cut/?lang=el', 'el', 'Πόσο κοστίζει ένα κούρεμα;', ['€15', 'Κλασικό κούρεμα'], ['Ανδρέας']),
 ('/demos/the-cut/?lang=el', 'el', 'Ποιος κουρέας είναι καλύτερος για γενειάδες;', ['Νίκος'], []),
 ('/demos/nexora/', 'en', 'What does process improvement include?', ['Process improvement'], []),
 ('/demos/nexora/', 'en', 'How is pricing handled?', ['depend on scope'], []),
 ('/demos/nexora/?lang=el', 'el', 'Πώς υποβάλλω αίτημα;', ['επτά βημάτων'], []),
 ('/demos/halcyon-bay/', 'en', 'Which rooms have a sea view?', ['Sea View Double', '€130', 'Rooftop Loft Suite'], ['Family Suite', 'Garden Double']),
 ('/demos/halcyon-bay/', 'en', 'Is breakfast included?', ['€14', 'half board'], []),
 ('/demos/halcyon-bay/', 'en', 'Do you have family rooms?', ['Family Suite', 'sleeps up to 4'], ['Rooftop Loft Suite']),
 ('/demos/halcyon-bay/', 'en', 'How much is the Family Suite?', ['€210', 'Two connected rooms'], []),
 ('/demos/halcyon-bay/', 'en', 'Can you arrange an airport transfer?', ['€45'], []),
 ('/demos/halcyon-bay/', 'en', 'Is this hotel real?', ['fictional'], []),
 ('/demos/halcyon-bay/?lang=el', 'el', 'Ποια δωμάτια έχουν θέα θάλασσα;', ['Δίκλινο με θέα θάλασσα', '€130'], ['Οικογενειακή σουίτα']),
 ('/demos/halcyon-bay/?lang=el', 'el', 'Περιλαμβάνεται πρωινό;', ['€14'], []),
 ('/demos/myrtle/', 'en', 'How much is a gel manicure?', ['Gel manicure', '€28', '50 min'], ['Classic manicure']),
 ('/demos/myrtle/', 'en', 'Who does lash lifts?', ['Christina', 'Friday'], ['Sofia', 'Maria']),
 ('/demos/myrtle/', 'en', 'Do I need a patch test?', ['48 hours'], []),
 ('/demos/myrtle/', 'en', 'What nail treatments do you have?', ['Classic manicure', 'Gel manicure', 'Spa pedicure'], ['Balayage', 'Nail art']),
 ('/demos/myrtle/', 'en', 'How long is a hot stone massage?', ['75 min'], []),
 ('/demos/myrtle/?lang=el', 'el', 'Πόσο κοστίζει το ημιμόνιμο μανικιούρ;', ['€28', '50 λεπτά'], []),
 ('/demos/myrtle/?lang=el', 'el', 'Ποια κάνει ανόρθωση βλεφαρίδων;', ['Χριστίνα'], ['Σοφία']),
]
try:
  with sync_playwright() as pw:
    br = pw.chromium.launch(args=['--no-sandbox'])
    # The published packs point at the real engine. Tests never call it: every page gets the packs with the endpoint
    # replaced (empty = demo mode, or a local mock engine for the live-mode checks).
    _new_context = br.new_context
    def new_context(endpoint='', **kw):
      c = _new_context(**kw)
      def serve(route, request):
        name = request.url.split('?')[0].rsplit('/', 1)[-1]
        src = open(f'{SITE}/assets/assistant/packs/{name}', encoding='utf-8').read()
        route.fulfill(status=200, content_type='application/javascript', body=re.sub(r'"endpoint":"[^"]*"', '"endpoint":' + json.dumps(endpoint), src))
      c.route('**/assets/assistant/packs/*.js', serve)
      return c
    br.new_context = new_context
    packs = {n: open(f'{SITE}/assets/assistant/packs/{n}', encoding='utf-8').read() for n in os.listdir(f'{SITE}/assets/assistant/packs')}
    eps = {n: re.findall(r'"endpoint":"([^"]*)"', s) for n, s in packs.items()}
    chk('the P&N pack points at the deployed engine over https', re.fullmatch(r'https://[^"]+/chat', (eps.get('pn-digital.js') or [''])[0]), eps)
    chk('every demo pack has no engine address, so demos stay in demo mode and send nothing', len(eps) >= 6 and all(v == [''] for n, v in eps.items() if n != 'pn-digital.js'), eps)
    # ---- demo mode answers (every business, both languages)
    for (w, h) in ((1440, 900), (390, 844)):
      c = br.new_context(viewport={'width': w, 'height': h}); p = c.new_page(); errs = []
      p.on('pageerror', lambda e: errs.append(str(e))); p.on('console', lambda m: errs.append(m.text) if m.type == 'error' else None)
      reqs = []; p.on('request', lambda r: reqs.append(r.url) if not r.url.startswith(O) else None)
      last_page = None
      for page, L, q, must, mustnot in CASES:
        if page != last_page:
          p.goto(O + page); p.wait_for_timeout(500); openw(p); last_page = page
          chk(f'[{w}] {page}: launcher opens a labelled AI assistant in {L}', p.evaluate(f"!{SH('.panel')}.hidden") and (('Βοηθός AI' if L == 'el' else 'AI assistant') in txt(p, '.tag.ai')), txt(p, '.hd'))
          chk(f'[{w}] {page}: demo mode clearly labelled', ('Λειτουργία επίδειξης' if L == 'el' else 'Demo mode') in txt(p, '.mode') and ('δεν είναι ακόμη συνδεδεμένος' if L == 'el' else 'not connected to AI yet') in txt(p, '.note'))
          chk(f'[{w}] {page}: welcome message + suggestions in {L}', nbot(p) == 1 and p.evaluate(f"{SH('.chips')}.children.length") >= 3 and (bool(re.search('[Ͱ-Ͽ]', bot_last(p))) == (L == 'el')), bot_last(p)[:60])
        a = ask(p, q)
        chk(f'[{w}] {page} "{q}" -> correct demo answer', all(m in a for m in must) and not any(x in a for x in mustnot), a[:160])
        chk(f'[{w}] {page} "{q}" -> answer marked as demo', ('Απάντηση επίδειξης' if L == 'el' else 'Demo answer') in a)
      chk(f'[{w}] demo mode sends nothing off-site (no external requests)', not reqs, reqs[:3])
      chk(f'[{w}] no JS errors in demo mode', not errs, errs[:3])
      c.close()
    # ---- guided website plan (P&N, demo) + links + keyboard + mobile layout
    for L, page in (('en', '/'), ('el', '/el/')):
      c = br.new_context(viewport={'width': 390, 'height': 844}); p = c.new_page(); p.goto(O + page); p.wait_for_timeout(500)
      lb = p.locator('#pn-ai-host .launcher').bounding_box(); chk(f'[{L}] phone: launcher is a compact 52px round button in the corner', lb['width'] <= 54 and lb['x'] + lb['width'] > 330 and lb['y'] > 760, lb)
      chk(f'[{L}] phone: page gets bottom padding so the launcher never hides the last controls', p.evaluate("parseInt(getComputedStyle(document.body).paddingBottom)") >= 80)
      openw(p); pb = p.evaluate(f"(()=>{{const r={SH('.panel')}.getBoundingClientRect();return [r.left,r.width,Math.round(r.bottom)]}})()")
      chk(f'[{L}] phone: chat opens as a full-width bottom sheet', pb[0] == 0 and pb[1] == 390 and pb[2] == 844, pb)
      p.locator('#pn-ai-host .chip').first.click(); p.wait_for_timeout(700)
      for i in range(5):
        p.locator('#pn-ai-host .chip').nth(1 if i != 3 else 1).click(); p.wait_for_timeout(650)
      a = bot_last(p); allb = p.evaluate("[...document.getElementById('pn-ai-host').shadowRoot.querySelectorAll('.msg.bot')].map(m=>m.textContent).join(' || ')")
      chk(f'[{L}] guided plan (barbershop, redesign, few pages, booking): Premium suggested, booking caveat, nothing sent', (('Premium (από €750)' in a and 'ξεχωριστά' in a) if L == 'el' else ('Premium (from €750)' in a and 'priced separately' in a)) and (('ενδεικτική τιμή εκκίνησης' in a and 'Τίποτα δεν έχει σταλεί' in a) if L == 'el' else ('provisional starting price' in a and 'Nothing has been sent' in a)), a[:200])
      href = p.evaluate(f"{SH('.msg.bot:last-of-type a.act')}.getAttribute('href')"); chk(f'[{L}] guided plan: contact link points to the {L} contact page', href == ('/el/contact/' if L == 'el' else '/contact/'), href)
      
      with p.expect_navigation(): p.evaluate(f"{SH('.msg.bot:last-of-type a.act')}.click()")
      chk(f'[{L}] contact link works', p.url == O + ('/el/contact/' if L == 'el' else '/contact/'), p.url)
      c.close()
    # ---- other languages (demo mode): honest note in the visitor's own language, right-to-left shown correctly
    c = br.new_context(viewport={'width': 1440, 'height': 900}); p = c.new_page(); p.goto(O + '/'); p.wait_for_timeout(500); openw(p)
    def lastmsg(js): return p.evaluate("(()=>{const m=[...document.getElementById('pn-ai-host').shadowRoot.querySelectorAll('.msg.bot')];return " + js + "})()")
    for q, code, must, rtl in (('Сколько стоит сайт?', 'ru', 'на вашем языке', False), ('Скільки коштує сайт?', 'uk', 'вашою мовою', False), ('כמה עולה אתר?', 'he', 'בשפה שלך', True), ('كم تكلفة الموقع؟', 'ar', 'بلغتك', True), ('Web sitesinin fiyatı ne kadar? Bilgi öğrenmek istiyorum.', 'tr', 'sizin dilinizde', False), ('网站多少钱？', 'zh', '您的语言', False)):
      n0 = nbot(p); ask(p, q)
      note = lastmsg("m[m.length-2]"); 
      info = lastmsg("(e=>({t:e.textContent,lang:e.lang,dir:getComputedStyle(e.querySelector('.tx')).direction}))(m[m.length-2])")
      chk(f'demo, visitor writes {code}: honest note in {code}, marked lang={code}' + (', shown right-to-left' if rtl else ''), must in info['t'] and info['lang'] == code and (info['dir'] == 'rtl') == rtl, info)
      chk(f'demo, visitor writes {code}: then offers English questions', 'questions I can answer in English' in bot_last(p) and p.evaluate(f"{SH('.chips')}.children.length") >= 3, bot_last(p)[:80])
    ask(p, 'Kaç dilde site yapıyorsunuz?'); chk('demo: Turkish detected from Turkish letters (ı)', 'sizin dilinizde' in lastmsg("m[m.length-2].textContent"))
    a = ask(p, 'Can you do French?'); chk('demo: English question about French is answered from the language FAQ', 'any language' in a, a[:90])
    c.close()
    for L, page in (('en', '/'), ('el', '/el/')):
      c = br.new_context(viewport={'width': 1440, 'height': 900}); p = c.new_page(); p.goto(O + page); p.wait_for_timeout(500); openw(p)
      p.locator('#pn-ai-host .chip').first.click(); p.wait_for_timeout(700)
      for pick in (0, 0, 0, 3, 3):  # restaurant, new site, ONE page, not sure, THREE OR MORE languages
        p.locator('#pn-ai-host .chip').nth(pick).click(); p.wait_for_timeout(650)
      a = bot_last(p)
      chk(f'[{L}] plan: one page but 3+ languages suggests Business (Starter covers 2) and explains language counts', (('Business (€450)' in a and 'έως 3' in a and 'έως 5' in a) if L == 'el' else ('Business (€450)' in a and 'up to 3' in a and 'up to 5' in a)), a[:220])
      c.close()
    c = br.new_context(viewport={'width': 1440, 'height': 900}); p = c.new_page(); p.goto(O + '/'); p.wait_for_timeout(500)
    for _ in range(40):
      p.keyboard.press('Tab')
      if p.evaluate("document.activeElement && document.activeElement.id==='pn-ai-host'"): break
    chk('keyboard: the launcher can be reached with Tab', p.evaluate("document.activeElement.id==='pn-ai-host' && document.activeElement.shadowRoot.activeElement.classList.contains('launcher')"))
    p.keyboard.press('Enter'); p.wait_for_timeout(400)
    chk('keyboard: Enter opens it and focus moves to the message box', p.evaluate("document.activeElement.shadowRoot.activeElement.tagName")=='TEXTAREA')
    p.keyboard.type('How does the process work?'); p.keyboard.press('Enter'); p.wait_for_timeout(1000); chk('keyboard: typing + Enter sends and gets an answer', 'Six steps' in bot_last(p), bot_last(p)[:80])
    p.keyboard.press('Escape'); p.wait_for_timeout(300); chk('keyboard: Escape closes and focus returns to the launcher', p.evaluate(f"{SH('.panel')}.hidden") and p.evaluate("document.activeElement.shadowRoot.activeElement.classList.contains('launcher')"))
    chk('screen readers: messages area is a live log, controls are labelled', p.evaluate(f"{SH('.log')}.getAttribute('role')")=='log' and p.evaluate(f"{SH('.log')}.getAttribute('aria-live')")=='polite' and p.evaluate(f"{SH('.x')}.getAttribute('aria-label')")=='Close assistant' and p.evaluate(f"{SH('label')}.textContent")=='Your message')
    openw(p); p.locator('#pn-ai-host .reset').click(); p.wait_for_timeout(300); chk('↺ starts a new conversation', nbot(p) == 1)
    c.close()
    # ---- language follows the demo's switcher
    c = br.new_context(viewport={'width': 1440, 'height': 900}); p = c.new_page(); p.goto(O + '/demos/the-cut/'); p.wait_for_timeout(500); openw(p)
    p.locator('header .lg button[data-l=el]').click(); p.wait_for_timeout(300)
    chk('assistant labels switch to Greek when the demo switches to Greek', txt(p, '.tag.ai') == 'Βοηθός AI' and 'Σύνοψη' not in txt(p, '.hd'))
    chk('the demo’s translation layer leaves the assistant alone (no double translation)', p.evaluate("document.getElementById('pn-ai-host').hasAttribute('data-no-i18n')"))
    c.close()
    # ---- booking controls are never covered (THE CUT and Olive & Oak on phones)
    for d, sel in (('the-cut', '#wiz [data-a=next]'), ('olive-and-oak', '#wiz [data-a=next]'), ('halcyon-bay', '#wiz [data-a=next]'), ('myrtle', '#wiz [data-a=next]')):
      c = br.new_context(viewport={'width': 375, 'height': 812}); p = c.new_page(); p.goto(O + f'/demos/{d}/#' + ('reserve' if d == 'olive-and-oak' else 'book')); p.wait_for_timeout(500)
      p.evaluate("window.scrollTo(0, document.documentElement.scrollHeight)"); p.wait_for_timeout(300)
      b = p.locator(sel).bounding_box(); lb = p.locator('#pn-ai-host .launcher').bounding_box()
      overlap = not (b['x'] + b['width'] <= lb['x'] or lb['x'] + lb['width'] <= b['x'] or b['y'] + b['height'] <= lb['y'] or lb['y'] + lb['height'] <= b['y'])
      chk(f'{d} @375: launcher does not cover the booking "Continue" button', not overlap, (b, lb))
      c.close()
    # ---- LIVE mode end to end: widget -> real engine -> fake Claude (streamed)
    def live_ctx(endpoint):
      return br.new_context(endpoint=endpoint, viewport={'width': 1440, 'height': 900})
    c = live_ctx(f'http://127.0.0.1:{ENG}/chat'); p = c.new_page(); errs = []; p.on('pageerror', lambda e: errs.append(str(e)))
    p.goto(O + '/'); p.wait_for_timeout(500); openw(p)
    n = txt(p, '.note')
    chk('live: no "Demo mode" label; P&N note honestly says Gemini/Google may keep messages', p.evaluate(f"{SH('.mode')}.hidden") and 'Google' in n and 'may keep' in n and 'P&N Digital does not store' in n, n)
    a = ask(p, 'Hi, what do you build?', 3000); chk('live: answer streams back from Gemini for the right business', a.startswith('Hello! [P&N Digital assistant] (gemini) You asked: Hi, what do you build?'), a)
    a = ask(p, 'And the price?', 3000); chk('live: follow-up keeps the conversation going', 'You asked: And the price?' in a, a)
    a = ask(p, 'please fail', 3000); chk('live: provider overload shows a friendly busy message', 'busy right now' in a, a)
    p.goto(O + '/demos/olive-and-oak/?lang=el'); p.wait_for_timeout(500); openw(p)
    n = txt(p, '.note'); chk('live: Olive & Oak (Claude) keeps the standard Greek note, no Google mention', 'δεν αποθηκεύονται' in n and 'Google' not in n, n)
    a = ask(p, 'Έχετε βίγκαν πιάτα;', 3000); chk('live: Greek visitor on Olive & Oak gets the Olive & Oak assistant in Greek', a.startswith('Γεια! [Olive & Oak assistant]'), a)
    p.goto(O + '/el/'); p.wait_for_timeout(500); openw(p); n = txt(p, '.note')
    chk('live: Greek P&N page shows the Greek Gemini note', 'Gemini της Google' in n, n)
    a = ask(p, 'Τι φτιάχνετε;', 3000); chk('live: Greek P&N visitor gets a Greek answer via Gemini', a.startswith('Γεια! [P&N Digital assistant] (gemini)'), a)
    sent = []; p.on('request', lambda r: sent.append(r.post_data) if r.url.endswith('/chat') and r.method == 'POST' else None)
    p.evaluate("document.documentElement.lang='ru'"); p.wait_for_timeout(200)
    a = ask(p, 'Сколько стоит сайт?', 3000)
    chk('live: a Russian page sends lang=ru to the engine and the Russian question reaches the AI', sent and json.loads(sent[-1])['lang'] == 'ru' and 'Сколько стоит сайт?' in a, (sent[-1:] , a[:90]))
    p.evaluate("document.documentElement.lang='he'"); p.wait_for_timeout(200)
    a = ask(p, 'כמה עולה אתר?', 3000)
    d = p.evaluate("(()=>{const m=[...document.getElementById('pn-ai-host').shadowRoot.querySelectorAll('.msg.me .tx')];return getComputedStyle(m[m.length-1]).direction})()")
    chk('live: Hebrew page sends lang=he; Hebrew text is shown right-to-left', json.loads(sent[-1])['lang'] == 'he' and d == 'rtl', d)
    chk('live: widget texts fall back to English on a page in another language (never blank)', len(txt(p, '.note')) > 20 and txt(p, '.lbl') == 'Ask AI', txt(p, '.lbl'))
    chk('live: no JS errors', not errs, errs[:2]); c.close()
    c = live_ctx(f'http://127.0.0.1:{ENG_NOKEY}/chat'); p = c.new_page(); p.goto(O + '/'); p.wait_for_timeout(500); openw(p)
    a = ask(p, 'How much does a website cost?', 3000)
    allb = p.evaluate("[...document.getElementById('pn-ai-host').shadowRoot.querySelectorAll('.msg.bot')].map(m=>m.textContent).join(' || ')")
    chk('engine without an API key: widget says so, switches to labelled demo mode and still answers', 'switched to demo mode' in allb and '€250' in a and not p.evaluate(f"{SH('.mode')}.hidden"), allb[-220:])
    c.close()
    c = live_ctx('http://127.0.0.1:9/chat'); p = c.new_page(); p.goto(O + '/'); p.wait_for_timeout(500); openw(p)
    a = ask(p, 'hello there', 4000); chk('engine unreachable: friendly offline/error message, no crash', 'offline' in a or 'went wrong' in a, a); c.close()
    br.close()
finally:
  srv.terminate(); eng.terminate(); eng2.terminate()
f = [r for r in R if not r[1]]; print(f'ASSISTANT TOTAL {len(R)} | PASSED {len(R)-len(f)} | FAILED {len(f)}')
json.dump(R, open(str(OUT / 'results-assistant.json'), 'w'))
