import os, sys, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[1]          # the repository folder
SITE = str(ROOT / 'public')                                   # the website
AI = os.environ.get('PN_AI_ASSISTANT_DIR', str(ROOT.parent / 'pn-digital-ai-assistant'))  # the engine repo, cloned next to this one
OUT = ROOT / 'tests' / 'output'; OUT.mkdir(exist_ok=True)
PY = sys.executable
"""Site-wide regression suite (real Chromium). Usage: python3 test_site.py <port>"""
import subprocess, sys, time, json
from playwright.sync_api import sync_playwright

PORT = sys.argv[1] if len(sys.argv) > 1 else '8990'
srv = subprocess.Popen([PY, '-m', 'http.server', PORT, '--directory', SITE], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
time.sleep(1)
B = f'http://127.0.0.1:{PORT}'
R = []


def chk(n, ok, d=''):
    R.append((n, bool(ok), str(d)[:200]))
    if not ok:
        print('FAIL:', n, '|', str(d)[:200])


EN = ['/', '/work/', '/services/', '/about/', '/contact/', '/privacy/', '/projects/olive-and-oak/', '/projects/the-cut/', '/projects/nexora-business-solutions/', '/projects/halcyon-bay/', '/projects/myrtle-beauty-studio/']
EL = ['/el' + p if p != '/' else '/el/' for p in EN]
VPS = [(1920, 1080), (1440, 900), (1280, 800), (768, 1024), (390, 844), (375, 812)]
LEAK = """(allow) => { const out=new Set(), rx=/[A-Za-z][A-Za-z&’'-]{2,}/g; const w=document.createTreeWalker(document.body,NodeFilter.SHOW_TEXT); let n;
  while((n=w.nextNode())){ const el=n.parentElement; if(!el||el.closest('script,style,noscript,dialog:not([open]),[data-no-i18n]')) continue; const ol=el.closest('[lang]'); if(ol&&ol!==document.documentElement&&ol.lang!==document.documentElement.lang) continue; let p=el,hid=false; while(p){ if(p.hidden){hid=true;break} p=p.parentElement }
   if(hid) continue; const cs=getComputedStyle(el); if(cs.display==='none'||cs.visibility==='hidden') continue; (n.textContent.match(rx)||[]).forEach(x=>{ if(!allow.includes(x)) out.add(x) }) }
  document.querySelectorAll('[aria-label],[title],[alt],[placeholder]').forEach(e=>{ if(e.closest('dialog:not([open]),[data-no-i18n]')) return; ['aria-label','title','alt','placeholder'].forEach(a=>{ const v=e.getAttribute(a); if(v)(v.match(rx)||[]).forEach(x=>{ if(!allow.includes(x)) out.add('['+a+'] '+x) }) }) });
  return [...out] }"""
ALLOW = ['Olive', 'Oak', 'THE', 'CUT', 'Nexora', 'Business', 'Solutions', 'P&N', 'Digital', 'Starter', 'Premium', 'SEO', 'JavaScript', 'responsive', 'Responsive',
         'domain', 'Landing', 'landing', 'pages', 'sitemap', 'tablet', 'account', 'managers', 'editorial', 'Editorial', 'demo', 'email', 'Email', 'workshops', 'brand',
         'FAQ', 'English', 'Demo', 'Google', 'Gemini', 'WhatsApp', 'pndigitalwebsites', 'gmail', 'com', 'CSS', 'serif', 'sans-serif', 'pixel', 'fade',
         'Halcyon', 'Bay', 'Myrtle', 'Beauty', 'Studio', 'Cloudflare', 'cookies']
PAGE = """() => ({w:document.documentElement.scrollWidth, iw:innerWidth, lang:document.documentElement.lang, h1:document.querySelectorAll('h1').length,
  imgs:[...document.images].filter(i=>!i.complete||i.naturalWidth===0).length, unnamed:[...document.querySelectorAll('a,button')].filter(e=>!e.closest('dialog')&&!e.hidden&&getComputedStyle(e).display!=='none'&&!(e.textContent.trim()||e.getAttribute('aria-label'))).length})"""
try:
    with sync_playwright() as pw:
        br = pw.chromium.launch(args=['--no-sandbox'])
        # 1. every page x every width
        for (w, h) in VPS:
            c = br.new_context(viewport={'width': w, 'height': h}, reduced_motion='reduce'); p = c.new_page(); bag = []
            p.on('console', lambda m: bag.append(m.text) if m.type == 'error' else None); p.on('pageerror', lambda e: bag.append(str(e)))
            p.on('response', lambda r: bag.append(f'HTTP {r.status} {r.url}') if r.status >= 400 else None)
            for path in EN + EL + ['/404.html']:
                bag.clear(); p.goto(B + path); p.wait_for_timeout(120); r = p.evaluate(PAGE)
                chk(f'{path} @{w}: no errors / failed requests', not bag, bag[:2])
                chk(f'{path} @{w}: no horizontal overflow', r['w'] <= r['iw'] + 1, f"{r['w']}>{r['iw']}")
                chk(f'{path} @{w}: images load, every control has a name', r['imgs'] == 0 and r['unnamed'] == 0, r)
                if w == 1440 and path != '/404.html':
                    chk(f'{path}: lang + one h1', r['lang'] == ('el' if path.startswith('/el') else 'en') and r['h1'] == 1, r)
            c.close()
        # 2. Greek pages: no English leaks
        c = br.new_context(viewport={'width': 1440, 'height': 900}, reduced_motion='reduce'); p = c.new_page()
        for path in EL:
            p.goto(B + path); p.wait_for_timeout(150); p.evaluate("document.querySelectorAll('#faq button.q').forEach(b=>b.click())"); p.wait_for_timeout(300)
            lk = p.evaluate(LEAK, ALLOW); chk(f'{path}: no English text in the Greek page', not lk, lk[:8])
            sw = p.evaluate("document.querySelector('li.lang a').getAttribute('href')"); chk(f'{path}: switcher points to the same page in English', sw == (path[3:] or '/'), sw)
        c.close()
        # 2b. every page links to the privacy page in its own language; the privacy page states the key facts
        c = br.new_context(viewport={'width': 1440, 'height': 900}); p = c.new_page()
        for path in EN + EL + ['/404.html']:
            p.goto(B + path); want = '/el/privacy/' if path.startswith('/el') else '/privacy/'
            chk(f'{path}: footer links to the privacy page ({want})', p.locator(f'footer a[href="{want}"]').count() == 1)
        for path, facts in (('/privacy/', ('no cookies', 'Gemini', 'Cloudflare', 'pndigitalwebsites@gmail.com', 'demo mode')), ('/el/privacy/', ('cookies', 'Gemini', 'Cloudflare', 'pndigitalwebsites@gmail.com', 'λειτουργία επίδειξης'))):
            p.goto(B + path); t = p.inner_text('main')
            chk(f'{path}: states the facts (cookies, AI provider, host, contact, demos send nothing)', all(x in t for x in facts), [x for x in facts if x not in t])
        p.goto(B + '/'); chk('homepage counts five concept websites', p.get_attribute('.facts .count', 'data-to') == '5' and p.locator('.feature-list .feature').count() == 5)
        p.goto(B + '/work/'); chk('work page lists five projects with previews', p.locator('article.row').count() == 5 and p.locator('[data-preview]').count() == 5)
        c.close()
        # 3. navigation + CTAs
        c = br.new_context(viewport={'width': 1440, 'height': 900}); p = c.new_page()
        for pre in ('', '/el'):
            for key in ('work', 'services', 'about', 'contact'):
                p.goto(B + pre + '/'); p.click(f'header nav a[href="{pre}/{key}/"]'); p.wait_for_load_state()
                chk(f'nav {pre or "/en"} -> {key}', p.url == f'{B}{pre}/{key}/' and p.get_attribute(f'header nav a[href="{pre}/{key}/"]', 'aria-current') == 'page', p.url)
            p.goto(B + pre + '/'); p.click('#pricing .plan >> nth=1 >> a.btn'); p.wait_for_load_state(); chk(f'pricing CTA {pre or "/en"} -> contact', p.url == f'{B}{pre}/contact/', p.url)
            p.goto(B + pre + '/'); p.click('header nav .cta a'); p.wait_for_load_state(); chk(f'header quote button {pre or "/en"} -> contact', p.url == f'{B}{pre}/contact/', p.url)
        p.goto(B + '/'); t = p.inner_text('#pricing'); chk('prices €250 / €450 / from €750 / €50 month shown', all(x in t for x in ('€250', '€450', '€750', '€50')))
        c.close()
        # 4. mobile menu + headline
        for path, lab in (('/', 'Get a quote'), ('/el/', 'Ζητήστε προσφορά')):
            c = br.new_context(viewport={'width': 390, 'height': 844}); p = c.new_page(); p.goto(B + path); p.wait_for_timeout(2600)
            hh = p.evaluate("document.querySelector('.hero2 h1').getBoundingClientRect().height"); chk(f'{path} @390: headline flows normally (not one word per line)', hh < 260, hh)
            chk(f'{path} @390: header bar solid', p.evaluate("getComputedStyle(document.querySelector('header.top')).backgroundColor") == 'rgb(16, 19, 21)')
            p.click('.menu-btn'); p.wait_for_timeout(600)
            b = p.locator('header nav .cta .btn'); s = b.evaluate("e=>{const c=getComputedStyle(e);return [c.color,c.backgroundColor]}")
            chk(f'{path} @390: menu quote button readable (dark text on ivory), label "{lab}"', s[0] != s[1] and s[0] == 'rgb(16, 19, 21)' and b.inner_text().strip() == lab, s)
            chk(f'{path} @390: menu opens', p.get_attribute('.menu-btn', 'aria-expanded') == 'true' and p.is_visible('header nav li.lang a'))
            p.keyboard.press('Escape'); p.wait_for_timeout(600); chk(f'{path} @390: Escape closes the menu', p.get_attribute('.menu-btn', 'aria-expanded') == 'false')
            c.close()
        # 5. previews + open full website
        for lp in ('/work/', '/el/work/'):
            L = 'el' if lp.startswith('/el') else 'en'
            for w in (1440, 390):
                c = br.new_context(viewport={'width': w, 'height': 900}); p = c.new_page(); bag = []; p.on('pageerror', lambda e: bag.append(str(e)))
                for slug, d in (('olive-and-oak', 'olive-and-oak'), ('the-cut', 'the-cut'), ('nexora-business-solutions', 'nexora'), ('halcyon-bay', 'halcyon-bay'), ('myrtle-beauty-studio', 'myrtle')):
                    p.goto(B + lp); p.locator(f'[data-preview="{slug}"]').first.focus(); p.keyboard.press('Enter')
                    p.wait_for_function("document.querySelector('#pv-msg').hidden===true", timeout=9000); p.wait_for_timeout(300)
                    fr = p.query_selector('#pv iframe').content_frame()
                    chk(f'[{L} {w}] {slug}: preview loads the real demo in {L}', fr.evaluate('document.documentElement.lang') == L and fr.locator('[data-p=home]').count() == 1)
                    if w >= 720:
                        chk(f'[{L} {w}] {slug}: desktop viewport 1280', fr.evaluate('innerWidth') == 1280)
                        fr.evaluate('window.__k=1'); p.click('#pv [data-mode=phone]'); p.wait_for_timeout(700)
                        chk(f'[{L} {w}] {slug}: phone viewport 390, no reload, button state', fr.evaluate('innerWidth') == 390 and fr.evaluate('window.__k') == 1 and p.get_attribute('#pv [data-mode=phone]', 'aria-pressed') == 'true')
                        p.click('#pv [data-mode=desktop]'); p.wait_for_timeout(700); chk(f'[{L} {w}] {slug}: back to desktop', fr.evaluate('innerWidth') == 1280)
                    else:
                        chk(f'[{L} {w}] {slug}: phone opens in phone mode at 390', fr.evaluate('innerWidth') == 390)
                    href = p.get_attribute('#pv-open', 'href')
                    with c.expect_page() as np: p.click('#pv-open')
                    n = np.value; n.wait_for_load_state()
                    chk(f'[{L} {w}] {slug}: "Open full website" opens the demo in a new tab, in {L}', n.url.replace(B, '').startswith(f'/demos/{d}/') and n.evaluate('document.documentElement.lang') == L and n.locator('[data-p=home]').is_visible(), (href, n.url))
                    n.close()
                    p.keyboard.press('Escape'); p.wait_for_timeout(450); chk(f'[{L} {w}] {slug}: Escape closes the preview, focus returns', not p.evaluate("document.getElementById('pv').open") and p.evaluate('document.activeElement.dataset.preview') == slug)
                    p.goto(B + ('/el' if L == 'el' else '') + f'/projects/{slug}/'); a = p.locator('a[data-open]')
                    with c.expect_page() as np: a.click()
                    n = np.value; n.wait_for_load_state(); chk(f'[{L} {w}] {slug}: project page "Open full website" works in {L}', n.url.replace(B, '').startswith(f'/demos/{d}/') and n.evaluate('document.documentElement.lang') == L, n.url); n.close()
                chk(f'[{L} {w}] previews: no page errors', not bag, bag[:2]); c.close()
        # 6. demos opened directly
        for d, pages in (('olive-and-oak', ('home', 'menu', 'reserve')), ('the-cut', ('home', 'services', 'barbers', 'book')), ('nexora', ('home', 'services', 'cases', 'enquire')),
                         ('halcyon-bay', ('home', 'rooms', 'experiences', 'book')), ('myrtle', ('home', 'treatments', 'team', 'book'))):
            for (w, h) in ((1440, 900), (390, 844), (375, 812)):
                for q in ('', '?lang=el'):
                    c = br.new_context(viewport={'width': w, 'height': h}); p = c.new_page(); bag = []
                    p.on('console', lambda m: bag.append(m.text) if m.type == 'error' else None); p.on('pageerror', lambda e: bag.append(str(e)))
                    p.goto(B + f'/demos/{d}/' + q); p.wait_for_timeout(250); ok = True; of = True
                    for hsh in pages:
                        p.evaluate(f"location.hash='#{hsh}'"); p.wait_for_timeout(120); ok &= p.is_visible(f'[data-p={hsh}]'); of &= p.evaluate('document.documentElement.scrollWidth<=innerWidth+1')
                    chk(f'demo {d}{q} @{w}: every page reachable, no overflow, no errors', ok and of and not bag, (ok, of, bag[:2]))
                    c.close()
        br.close()
finally:
    srv.terminate()
f = [r for r in R if not r[1]]
print(f'SITE TOTAL {len(R)} | PASSED {len(R) - len(f)} | FAILED {len(f)}')
json.dump(R, open(str(OUT / 'results-site.json'), 'w'))
